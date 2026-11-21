#!/usr/bin/env python3
"""Mate: un lenguaje chico, en español, para escribir código claro y para que
los agentes se hablen entre ellos con mensajes que tienen contrato.

Uso:
    python3 mate.py correr    archivo.mate [--traza] [--traza=conversacion.txt]
                                           [--sin-limite] [--depurar]
    python3 mate.py probar    archivo.mate   (o varios archivos, o una carpeta)
    python3 mate.py verificar archivo.mate
    python3 mate.py guia
    python3 mate.py ayuda     (o: ayuda si, ayuda largo... para una palabra o función)
    python3 mate.py consola   (para probar renglones sueltos)
"""

import datetime
import decimal
import difflib
import json
import math
import os
import re
import sys
import unicodedata
from collections import deque

VERSION = "0.3"

# El tope para que Mate siga siendo chico (mejora 90): no puede haber más palabras propias
# ni más funciones incluidas que estas. Para agregar una hay que sacar otra, o discutir el
# tope. Y cada agregado lleva su renglón en el README y su prueba (las pruebas lo controlan).
TOPE_DE_PALABRAS = 40
TOPE_DE_FUNCIONES = 40

PALABRAS = {
    "sea", "var", "funcion", "devolver", "si", "sino", "mientras", "para", "en",
    "y", "o", "no", "verdadero", "falso", "nada", "mensaje", "agente", "estado",
    "al", "recibir", "como", "enviar", "preguntar", "responder", "fallar",
    "intentar", "falla", "asegurar", "prueba", "remitente", "yo", "crear", "usar",
    "romper", "continuar", "simular",
}

TIPOS_BASE = {"numero", "texto", "logico", "lista", "mapa", "agente", "cualquiera"}

MAX_MENSAJES = 100_000
MAX_PASOS = 10_000_000  # freno para los programas que nunca terminan
MAX_LARGO = 10_000_000  # tope de elementos de una lista o de letras de un texto
MAX_BITS = 14_000  # tope de tamaño de un entero (unas 4.200 cifras)
MAX_LLAMADAS = 3_000  # funciones abiertas a la vez (una que se llama a sí misma, casi siempre)
# Cada llamada de Mate gasta varios niveles de Python. Desde Python 3.12 esos niveles no
# ocupan la pila del sistema (y lo que sí la ocupa tiene su propio freno), así que se
# puede pedir lugar para miles de llamadas sin riesgo de que Python se caiga. En un
# Python más viejo se deja el tope de siempre (unas 120 llamadas).
NIVELES_DE_PYTHON = 30 * MAX_LLAMADAS if sys.version_info >= (3, 12) else 0

ORDENES = ("correr", "probar", "verificar")
OPCIONES = ("--traza", "--depurar", "--sin-limite", "--version", "--ayuda")

COMPARADORES = ("==", "!=", "<", "<=", ">", ">=")

# La tabla única de funciones incluidas: nombre -> (cuántos valores lleva como mínimo,
# como máximo, un ejemplo, qué hace). De acá salen el control de la cantidad de valores,
# el ejemplo de los errores, la lista de la guía y la tabla del README.
FUNCIONES = {
    "mostrar": (0, None, 'mostrar("Total:", total)', "escribe en pantalla"),
    "leer": (1, 2, 'leer("¿Cuántos?", "3")',
             "le pide un texto a la persona (en las pruebas da el 2.º valor)"),
    "texto": (1, 1, "texto(3.5)", 'lo pasa a texto: "3.5"'),
    "numero": (1, 1, 'numero("1.234,50")', "lee un número escrito como texto: 1234.5"),
    "tipo": (1, 1, "tipo(x)", 'dice qué es: "numero", "texto", "lista", "mapa"...'),
    "largo": (1, 1, "largo(lista)", "cuántos elementos tiene (o letras, o claves)"),
    "redondear": (1, 2, "redondear(3.14159, 2)", "3.14 (sin el 2.º valor, sin decimales)"),
    "pesos": (1, 2, "pesos(1234.5)", 'el texto "$ 1.234,50"'),
    "absoluto": (1, 1, "absoluto(-5)", "5: el número sin el signo"),
    "sumar": (1, 1, "sumar([1, 2, 3])", "6"),
    "promedio": (1, 1, "promedio([4, 6])", "5"),
    "minimo": (1, 1, "minimo([3, 1, 2])", "1: el más chico de la lista"),
    "maximo": (1, 1, "maximo([3, 1, 2])", "3: el más grande de la lista"),
    "rango": (1, 3, "rango(1, 10, 3)", "[1, 4, 7]; rango(3) es [0, 1, 2] y rango(2, 5) es [2, 3, 4]"),
    "tiene": (2, 2, "tiene(lista, x)",
              "verdadero si x está en la lista, es clave del mapa o parte del texto"),
    "claves": (1, 1, "claves(mapa)", "la lista de sus claves"),
    "valores": (1, 1, "valores(mapa)", "la lista de sus valores"),
    "obtener": (3, 3, 'obtener(mapa, "clave", 0)',
                "el valor de esa clave o, si el mapa no la tiene, el 3.er valor"),
    "agregar": (2, 2, "agregar(lista, x)", "una lista NUEVA con x al final"),
    "quitar": (2, 2, "quitar(lista, x)",
               "una lista NUEVA sin los que valen x (en un mapa, sin esa clave)"),
    "ordenar": (1, 2, 'ordenar(lista, "precio")',
                "una lista NUEVA ordenada; el campo es opcional: ordenar(lista)"),
    "ultimo": (1, 1, "ultimo(lista)", "el último elemento (o la última letra de un texto)"),
    "porcion": (2, 3, "porcion(lista, 1, 3)",
                "los de las posiciones 1 y 2; sin el 3.er valor, hasta el final"),
    "unir": (2, 2, 'unir(lista, ", ")', "un texto con los elementos separados por coma"),
    "partir": (2, 2, 'partir("a,b", ",")', 'la lista ["a", "b"]'),
    "mayusculas": (1, 1, 'mayusculas("hola")', '"HOLA"'),
    "minusculas": (1, 1, 'minusculas("HOLA")', '"hola"'),
    "recortar": (1, 1, 'recortar("  hola ")', '"hola": sin los espacios de las puntas'),
    "reemplazar": (3, 3, 'reemplazar(t, "a", "b")', "el texto con cada a cambiada por b"),
    "empieza_con": (2, 2, 'empieza_con(t, "Sr.")', "verdadero si el texto empieza así"),
    "termina_con": (2, 2, 'termina_con(t, ".txt")', "verdadero si el texto termina así"),
    "a_json": (1, 1, "a_json(valor)", "el valor escrito como texto JSON"),
    "de_json": (1, 2, 'de_json(texto, "Pedido")',
                "el valor que describe ese JSON; el 2.º valor (opcional) exige ese tipo"),
    "a_mapa": (1, 1, "a_mapa(pedido)",
               "un mapa común con los campos de ese mensaje, para recorrerlos"),
    "detalle_de": (1, 1, "detalle_de(e)",
                   "los datos de un error atajado: un mapa con texto, linea, clase y dato"),
    "hoy": (0, 0, "hoy()", 'la fecha, "21/11/2026" (en las pruebas, siempre "01/01/2025")'),
    "ahora": (0, 0, "ahora()",
              'fecha y hora, "21/11/2026 14:30" (en las pruebas, "01/01/2025 12:00")'),
    "leer_archivo": (1, 1, 'leer_archivo("notas.txt")',
                     "el texto de ese archivo (de la carpeta del programa)"),
    "escribir_archivo": (2, 2, 'escribir_archivo("notas.txt", t)',
                         "guarda el texto t en ese archivo (si ya existía, lo pisa)"),
}


def lista_de_funciones(formato_de_renglon="- {ejemplo:<27} {que}"):
    """Un renglón por función incluida, para la guía y para el README."""
    return "\n".join(formato_de_renglon.format(ejemplo=ejemplo, que=que)
                     for _, _, ejemplo, que in FUNCIONES.values())


# Las funciones incluidas que hacen algo además de devolver un valor: pueden ir solas
# en un renglón. Las demás, sueltas, no sirven de nada y Mate lo avisa.
HACEN_ALGO = ("mostrar", "leer", "escribir_archivo")

# Palabras de otros lenguajes, o con tilde, y cómo se escriben en Mate. No se aceptan
# como sinónimos: solo sirven para explicar el error.
PISTAS = {
    "print": "mostrar", "imprimir": "mostrar", "if": "si", "else": "sino",
    "while": "mientras", "for": "para", "let": "sea", "const": "sea",
    "true": "verdadero", "false": "falso", "null": "nada", "none": "nada",
    "return": "devolver", "function": "funcion", "def": "funcion",
    "and": "y", "or": "o", "not": "no", "to": "a",
    "break": "romper", "continue": "continuar",
    "función": "funcion", "sinó": "sino", "número": "numero", "lógico": "logico",
    "mayúsculas": "mayusculas", "minúsculas": "minusculas",
}

INCLUIDA = ("'{n}' es una función incluida de Mate; elegí otro nombre "
            "(por ejemplo 'mi_{n}')")
DEMASIADO_GRANDE = "el resultado es demasiado grande para calcularlo"
NO_ASIGNABLE = ("solo se puede asignar a una variable o a una parte de una variable "
                "(x, x.campo, x[0])")
COMO_VAN_LAS_RUTAS = ('Si es una ruta de Windows, escribila con barras comunes '
                      '("C:/datos/lista.txt") o con doble barra ("C:\\\\datos\\\\lista.txt")')
_RUTA_DE_WINDOWS = re.compile(r"(?<!\w)[A-Za-z]:\\(?!\\)")  # C:\ con una sola barra


def parece_ruta(crudo):
    r"""¿Ese texto trae una ruta de Windows con barras simples ("C:\temp\nuevo")? Un
    renglón que termina en dos puntos y sigue abajo ("Opción A:\nyerba") no lo es."""
    for m in _RUTA_DE_WINDOWS.finditer(crudo):
        resto = re.match(r"\S*", crudo[m.end():]).group()
        if resto[:1] not in ("n", "t"):
            return True  # C:\datos: esa barra no es ni un salto ni un espacio largo
        if "\\" in resto or "/" in resto or re.search(r"\.[A-Za-z]\w{0,4}$", resto):
            return True  # C:\temp\nuevo, C:\notas.txt
        if m.start() == 0 and len(resto) > 1:
            return True  # el texto entero es la ruta: "C:\temp"
    return False


ESPERA_OTRA_CANTIDAD = "{n}() espera {espera} argumento(s) y recibió {recibe}"
DEVOLVER_SUELTO = "'devolver' solo va dentro de una función"
RESPONDER_SUELTO = "'responder' solo va dentro de 'al recibir' (o de una función del agente)"
# El 'al fallar' de un agente se guarda junto a sus 'al recibir', con este nombre (que
# no puede ser el de un mensaje: tiene un espacio y empieza con minúscula).
AL_FALLAR = "al fallar"
SIN_A_QUIEN = ("en 'al fallar' no hay a quién responder: es un aviso, no una pregunta. "
               "Para mandar algo usá 'enviar'")
# Lo que escribir_archivo() no pisa nunca: programas (de Mate, de Python o de Windows).
NO_SE_PISAN = (".mate", ".mate.txt", ".py", ".bat", ".cmd", ".ps1")
# En las pruebas hoy() y ahora() dan siempre esto, para que el resultado no dependa del día.
FECHA_DE_PRUEBA = datetime.datetime(2025, 1, 1, 12, 0)
SIN_MEMORIA = ("el programa se quedó sin memoria: está armando un texto, una lista o un "
               "número demasiado grande")


class ErrorMate(Exception):
    """Un error del programa escrito en Mate. 'clase' dice de qué tipo es:
    'falla' (lo común, se puede atajar con 'intentar'), 'asegurar' (un 'asegurar' que
    no se cumplió: dentro de una prueba no se ataja) o 'limite' (el freno: no se ataja)."""

    def __init__(self, mensaje, linea=None, clase="falla", familia=None, dato=None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.linea = linea
        self.clase = clase
        # Para detalle_de(e): de qué familia es el error (no cambia con la redacción) y,
        # si salió de un 'fallar', el valor que le dieron.
        self.familia = familia or ("asegurar" if clase == "asegurar" else "otro")
        self.dato = dato
        self.camino = []  # por dónde se llegó: las funciones y las preguntas de por medio


def anotar_paso(error, paso):
    """Suma un paso al camino del error. Si el camino es muy largo se guardan el principio
    y el final (el origen), que son los que se muestran; se pierde lo del medio."""
    if len(error.camino) >= 40:
        del error.camino[20]
    error.camino.append(paso)


def sin_tildes(texto):
    """El texto en minúsculas y sin tildes, para comparar nombres parecidos."""
    return "".join(c for c in unicodedata.normalize("NFD", texto)
                   if unicodedata.category(c) != "Mn").lower()


def sugerir(nombre, candidatos):
    """Devuelve '' o " ¿Quisiste decir 'x'?" con el candidato más parecido al nombre."""
    candidatos = [c for c in candidatos if isinstance(c, str) and c != nombre]
    plano = sin_tildes(nombre)
    parecidos = [c for c in candidatos if sin_tildes(c) == plano]
    if not parecidos:
        parecidos = difflib.get_close_matches(nombre, candidatos, n=1, cutoff=0.7)
    return f" ¿Quisiste decir '{parecidos[0]}'?" if parecidos else ""


def con_sugerencia(mensaje, nombre, candidatos):
    """El mensaje tal cual o, si hay un nombre parecido, con la sugerencia al final."""
    sugerencia = sugerir(nombre, candidatos)
    return f"{mensaje}.{sugerencia}" if sugerencia else mensaje


def nombre_que_no_existe(nombre, visibles, al_asignar=False):
    """El error de un nombre que no existe, con el parecido si lo hay. 'visibles' son los
    nombres que sí se ven desde ahí. Lo usan la revisión previa y la corrida: dicen lo mismo."""
    mensaje = f"no existe '{nombre}'"
    if va_en_minuscula(nombre):
        return ErrorMate(f"{mensaje}: va en minúscula, '{nombre.lower()}'", familia="nombre")
    # Un nombre propio parecido se sugiere enseguida; una función incluida, solo si
    # es casi igual ('mostar'): 'precio' no es 'porcion'. Y a una función no se le
    # asigna, así que al asignar no se sugiere ninguna.
    propios = [n for n in visibles if n not in FUNCIONES]
    completo = con_pista(mensaje, nombre, propios)
    if completo == mensaje and not al_asignar:
        parecida = difflib.get_close_matches(nombre, list(FUNCIONES), n=1, cutoff=0.8)
        if parecida:
            completo = f"{mensaje}. ¿Quisiste decir '{parecida[0]}'?"
    if al_asignar and completo == mensaje:
        completo += f". Para crear la variable escribí: var {nombre} = ..."
    return ErrorMate(completo, familia="nombre")


def cantidad_equivocada(nombre, cuantos):
    """Si una función incluida no lleva esa cantidad de valores, el texto del error."""
    minimo, maximo, ejemplo, _ = FUNCIONES[nombre]
    if cuantos >= minimo and (maximo is None or cuantos <= maximo):
        return None
    if minimo == maximo:
        lleva = f"{minimo} valor" + ("" if minimo == 1 else "es")
    elif maximo == minimo + 1:
        lleva = f"{minimo} o {maximo} valores"
    else:
        lleva = f"entre {minimo} y {maximo} valores"
    return f"{nombre}() lleva {lleva} y recibió {cuantos}. Por ejemplo: {ejemplo}"


def pista_de(nombre):
    """Si el nombre es una palabra de otro lenguaje (o lleva tilde), cómo va en Mate."""
    forma = PISTAS.get(nombre.lower())
    if not forma:
        return ""
    if " " in forma:
        palabra, resto = forma.split(" ", 1)
        return f"en Mate '{nombre}' sería '{palabra}' {resto}"
    if sin_tildes(nombre) == forma:
        return f"en Mate se escribe '{forma}', sin tilde"
    return f"en Mate '{nombre}' se escribe '{forma}'"


def con_pista(mensaje, nombre, candidatos):
    """Como con_sugerencia, pero primero mira si es una palabra de otro lenguaje."""
    pista = pista_de(nombre)
    return f"{mensaje}: {pista}" if pista else con_sugerencia(mensaje, nombre, candidatos)


def va_en_minuscula(nombre):
    """'Si', 'Mientras': una palabra propia de Mate escrita con mayúscula."""
    return nombre != nombre.lower() and nombre.lower() in PALABRAS


class Linea(int):
    """Un número de línea que además recuerda de qué archivo salió."""

    def __new__(cls, numero, archivo=None):
        obj = super().__new__(cls, numero)
        obj.archivo = archivo
        return obj


# ───────────────────────────── Lexer ─────────────────────────────

_TOKEN = re.compile(
    r"""
    (?P<ws>[ \t\r\f\v\u00a0\u00ad\u1680\u2000-\u200f\u2028-\u202f\u205f-\u2064\u3000\ufeff]+|\#[^\n]*)
  | (?P<nl>\n)
  | (?P<num>\d+(?:_\d+)*(?:\.\d+)?)
  | (?P<str>"(?:\\.|[^"\\\n])*")
  | (?P<curva>[“”„](?:\\.|[^"“”„\\\n])*[“”„"])
  | (?P<id>[^\W\d]\w*)
  | (?P<op>==|!=|<=|>=|\+=|-=|[-+*/%<>=(){}\[\],.:?])
    """,
    re.X,
)


_PISTAS_DE_CARACTER = {
    '"': "a este texto le falta la comilla de cierre (los textos van en un solo renglón)",
    "'": 'los textos van entre comillas dobles: "así"',
    ";": "en Mate no hace falta el punto y coma: borralo",
    "&": "en Mate 'y' se escribe con la palabra: a y b",
    "|": "en Mate 'o' se escribe con la palabra: a o b",
    "!": "en Mate 'no' se escribe con la palabra: no a",
}
for _c in "“”„":  # comillas dobles curvas (Word, WhatsApp) sin su pareja
    _PISTAS_DE_CARACTER[_c] = _PISTAS_DE_CARACTER['"']
for _c in "‘’":
    _PISTAS_DE_CARACTER[_c] = _PISTAS_DE_CARACTER["'"]


_COMILLAS = '"“”„'
# Lo que no ocupa lugar en la pantalla: pegado en el medio de una palabra, la parte en dos.
_INVISIBLES = "\u00ad\u200b\u200c\u200d\u200e\u200f\u2060\u2061\u2062\u2063\u2064\ufeff"
_LETRA = re.compile(r"\w")


def _fin_de_texto(s, i):
    """s[i] abre un texto: devuelve dónde termina (después de la comilla de cierre), o -1
    si no cierra en ese renglón. Lo que va entre { y } es una cuenta, y adentro puede
    haber otros textos con sus propias comillas: "precio: {precios["yerba"]}"."""
    cierres = '"' if s[i] == '"' else _COMILLAS
    i += 1
    while i < len(s) and s[i] != "\n":
        c = s[i]
        if c == "\\":
            if s[i + 1:i + 2] in ("", "\n"):
                return -1
            i += 2
        elif c in cierres:
            return i + 1
        elif c == "{":
            i = _fin_de_llave(s, i)
            if i < 0:
                return -1
        else:
            i += 1
    return -1


def _fin_de_llave(s, i):
    """s[i] es la { de una cuenta dentro de un texto: devuelve dónde termina (después de
    su }), o -1. Las llaves que estén dentro de otro texto no cuentan."""
    prof = 0
    while i < len(s) and s[i] != "\n":
        c = s[i]
        if c in _COMILLAS:
            i = _fin_de_texto(s, i)
            if i < 0:
                return -1
            continue
        if c == "{":
            prof += 1
        elif c == "}":
            prof -= 1
            if prof == 0:
                return i + 1
        i += 1
    return -1


_MILES = re.compile(r"[1-9]\d{0,2}\.\d\d0")  # 1.500, 12.000, 3.250


def revisar_numero(txt, fuente, pos, hondo, linea):
    """Los números que casi seguro quieren decir otra cosa: 1.500, 1.500.000 y 3,5."""
    sin_puntos = txt.replace(".", "").replace("_", "")
    if re.match(r"\.\d", fuente[pos:pos + 2]) and "." in txt:
        raise ErrorMate(
            "un número lleva un solo punto, y es el de los decimales. Los miles no llevan "
            "punto: se escriben todos juntos o con guion bajo (1500000 o 1_500_000)", linea)
    if _MILES.fullmatch(txt):
        corto = txt.rstrip("0").rstrip(".")
        raise ErrorMate(
            f"en Mate el punto es el de los decimales: {txt} vale {corto}, no {sin_puntos}. "
            f"Si querías decir {sin_puntos}, escribilo sin punto ({sin_puntos}) o con guion "
            f"bajo ({txt.replace('.', '_')}); si era el decimal, escribí {corto}", linea)
    if not hondo and re.match(r",\d+(?![\w.])", fuente[pos:]) and "." not in txt:
        decimales = re.match(r",(\d+)", fuente[pos:]).group(1)
        raise ErrorMate(f"los decimales van con punto, no con coma: {txt}.{decimales}", linea)


def tokenizar(fuente, archivo=None):
    tokens, pos, linea = [], 0, Linea(1, archivo)
    hondo = 0  # paréntesis y corchetes abiertos: ahí adentro una coma separa valores
    while pos < len(fuente):
        if fuente[pos] in _COMILLAS:
            fin = _fin_de_texto(fuente, pos)
            if fin > 0:
                tokens.append(("str", fuente[pos + 1:fin - 1], linea))
                pos = fin
                continue
        m = _TOKEN.match(fuente, pos)
        if not m:
            c = fuente[pos]
            if c in _PISTAS_DE_CARACTER:
                raise ErrorMate(_PISTAS_DE_CARACTER[c], linea)
            if not c.isprintable() or unicodedata.category(c)[0] in "CZ":
                antes = fuente[fuente.rfind("\n", 0, pos) + 1:pos].strip()
                lugar = f"después de '{antes[-12:]}'" if antes else "al principio del renglón"
                raise ErrorMate(
                    f"hay un carácter invisible {lugar} (código U+{ord(c):04X}): borrá esa "
                    "parte del renglón y escribila de nuevo", linea)
            raise ErrorMate(f"carácter inesperado: '{c}'", linea)
        pos = m.end()
        clase, txt = m.lastgroup, m.group()
        if clase == "nl":
            linea = Linea(linea + 1, archivo)
        elif clase == "ws":
            if (not txt.startswith("#") and not txt.strip(_INVISIBLES)
                    and _LETRA.fullmatch(fuente[m.start() - 1:m.start()])
                    and _LETRA.fullmatch(fuente[pos:pos + 1])):
                antes = re.search(r"\w+$", fuente[:m.start()]).group()
                raise ErrorMate(
                    f"hay un carácter invisible después de '{antes[-12:]}', en el medio de "
                    f"una palabra (código U+{ord(txt[0]):04X}): borrá esa palabra y escribila "
                    "de nuevo", linea)
        elif clase == "num":
            revisar_numero(txt, fuente, pos, hondo, linea)
            txt = txt.replace("_", "")
            try:
                valor = float(txt) if "." in txt else int(txt)
            except ValueError:  # Python no convierte enteros de miles de cifras
                valor = math.inf
            if type(valor) is float and not math.isfinite(valor):
                raise ErrorMate("ese número es demasiado grande", linea)
            tokens.append(("num", valor, linea))
        elif clase in ("str", "curva"):  # "curva": texto entre comillas “de Word”
            tokens.append(("str", txt[1:-1], linea))
        elif clase == "id":
            tokens.append(("kw" if txt in PALABRAS else "id", txt, linea))
        elif clase == "op":
            if txt == "/" and fuente.startswith("/", pos):
                raise ErrorMate("los comentarios empiezan con #", linea)
            hondo += (txt in "([") - (txt in ")]")
            tokens.append(("op", txt, linea))
    # El final se anota en el último renglón con algo escrito: es el que hay que mirar.
    tokens.append(("eof", None, tokens[-1][2] if tokens else linea))
    return tokens


_CIERRES = {"(": ")", "[": "]", "{": "}"}
_SIGNOS = {"(": "el paréntesis", "[": "el corchete", "{": "la llave"}


def revisar_cierres(tokens, fuente):
    """Si una llave, un paréntesis o un corchete nunca se cierra, dice dónde se abrió
    (y no "falta algo al final del archivo"). Lo demás lo explica el análisis."""
    renglones = fuente.split("\n")

    def texto_de(linea):
        return renglones[linea - 1] if 0 < linea <= len(renglones) else ""

    def sangria(linea):
        t = texto_de(linea)
        return len(t) - len(t.lstrip())

    def sin_cerrar(signo, linea, hasta):
        # El error se anota donde se notó la falta (el final del archivo, o la llave
        # que cerró otra cosa); el mensaje dice dónde se abrió.
        de_que = texto_de(linea).strip().rstrip("{([").strip()
        de_que = f" ({de_que})" if de_que and signo == "{" else ""
        return ErrorMate(f"{_SIGNOS[signo]} que se abrió en la línea {linea}{de_que} "
                         "nunca se cierra", hasta)

    abiertos, sospechoso, previa = [], None, None
    for tipo, valor, linea in tokens:
        if tipo == "op" and valor in _CIERRES:
            abiertos.append((valor, linea))
        elif tipo == "op" and valor in ")]}":
            if not abiertos:
                return  # sobra un cierre: lo dice el análisis
            signo, donde = abiertos[-1]
            if _CIERRES[signo] != valor:
                if signo != "{" and valor == "}":
                    raise sin_cerrar(signo, donde, linea)
                return
            abiertos.pop()
            # Una '}' sola en su renglón y más a la izquierda que el renglón que abrió:
            # casi seguro cierra otra cosa, y la que quedó abierta es esa.
            if (valor == "}" and linea != previa and linea != donde
                    and sangria(linea) < sangria(donde) and sospechoso is None):
                sospechoso = (signo, donde)
        previa = linea
    if abiertos:
        raise sin_cerrar(*(sospechoso or abiertos[-1]), tokens[-1][2])


# ───────────────────────────── Parser ─────────────────────────────


_DEFINEN = ("sea", "var", "funcion", "para", "como", "falla", "mensaje", "agente", "estado")


class Parser:
    def __init__(self, tokens, en_consola=False):
        self.t = tokens
        self.i = 0
        self.en_consola = en_consola  # ahí un valor suelto vale: la consola lo muestra
        self.en_cabecera = 0  # dentro de la condición de un 'si' o un 'mientras'
        # Para avisar de 'devolver' y 'responder' fuera de lugar antes de correr.
        self.en_funcion = self.en_recibir = self.en_agente = self.en_bucle = 0
        self.en_prueba = 0
        self.en_al_fallar = 0
        self.abiertos = 0  # paréntesis, corchetes o llaves de un valor sin cerrar
        # Los nombres que el programa le pone a algo: si alguien llama 'def' o 'Crear' a
        # una variable o función suya, no se le da la pista de "en Mate se escribe...".
        self.definidos = {
            tk[1] for previo, tk in zip(tokens, tokens[1:])
            if tk[0] == "id" and previo[0] == "kw" and previo[1] in _DEFINEN}

    # utilidades
    def ver(self, d=0):
        return self.t[min(self.i + d, len(self.t) - 1)]

    def es(self, tipo, valor=None, d=0):
        tk = self.ver(d)
        return tk[0] == tipo and (valor is None or tk[1] == valor)

    def tomar(self):
        tk = self.t[self.i]
        self.i += 1
        return tk

    def acepta(self, tipo, valor=None):
        if self.es(tipo, valor):
            return self.tomar()
        return None

    def espera(self, tipo, valor=None, que=None):
        if self.es(tipo, valor):
            return self.tomar()
        tk = self.ver()
        if tipo == "id" and valor is None and tk[0] == "kw":
            raise ErrorMate(
                f"'{tk[1]}' es una palabra propia de Mate y no se puede usar como nombre; "
                f"elegí otro (por ejemplo '{tk[1]}2')", tk[2])
        self.pista_de_palabra(tk)
        visto = "el final del archivo" if tk[0] == "eof" else f"'{tk[1]}'"
        raise ErrorMate(f"esperaba {que or repr(valor)} y encontré {visto}", tk[2])

    def pista_de_palabra(self, tk):
        """'if', 'función', 'Y': una palabra de otro lenguaje, con tilde o con mayúscula
        donde no se la esperaba. Si el programa la definió como nombre suyo, no es eso."""
        if tk[0] != "id" or tk[1] in self.definidos:
            return
        if va_en_minuscula(tk[1]):
            raise ErrorMate(f"'{tk[1]}' va en minúscula: '{tk[1].lower()}'", tk[2])
        if pista_de(tk[1]):
            raise ErrorMate(pista_de(tk[1]), tk[2])

    def pista_de_igual(self):
        """Un '=' suelto donde iba una comparación: x = 5, x => 5, x =< 5."""
        tk = self.ver()
        if tk[:2] != ("op", "="):
            return
        sigue = self.ver(1)
        if sigue[:2] == ("op", ">") and sigue[2] == tk[2]:
            raise ErrorMate("'mayor o igual' se escribe '>=' (primero el '>')", tk[2])
        if sigue[:2] == ("op", "<") and sigue[2] == tk[2]:
            raise ErrorMate("'menor o igual' se escribe '<=' (primero el '<')", tk[2])
        raise ErrorMate("para comparar se usa '==' (un solo '=' es para asignar)", tk[2])

    def nombre_nuevo(self, que="un nombre"):
        """El nombre de una variable, función o parámetro que se está creando."""
        tk = self.espera("id", que=que)
        if tk[1] in incluidas():
            raise ErrorMate(INCLUIDA.format(n=tk[1]), tk[2])
        if tk[1][0].isupper():
            minuscula = tk[1][0].lower() + tk[1][1:]
            if minuscula in PALABRAS or minuscula in incluidas():
                minuscula = "mi_" + minuscula
            raise ErrorMate(
                f"'{tk[1]}' empieza con mayúscula, y esos nombres quedan para los mensajes "
                f"y los agentes. Para lo demás van en minúscula: '{minuscula}'", tk[2])
        self.definidos.add(tk[1])
        return tk[1]

    def nombre_de_campo(self):
        """Un nombre de campo: también puede ser una palabra propia de Mate (estado, para)."""
        if self.es("kw"):
            return self.tomar()[1]
        return self.espera("id", que="un nombre de campo")[1]

    def condicion(self):
        """La condición de un 'si' o un 'mientras', con pistas para los errores comunes."""
        self.en_cabecera += 1
        try:
            e = self.expr()
        finally:
            self.en_cabecera -= 1
        self.pista_de_igual()
        tk = self.ver()
        if tk[0] == "id" and tk[1].lower() in ("entonces", "then"):
            raise ErrorMate(f"en Mate no va '{tk[1]}': después de la condición va "
                            "directamente la llave {", tk[2])
        return e

    def recorrido(self):
        """Lo que recorre un 'para': como en una condición, la llave que sigue es la del bloque."""
        self.en_cabecera += 1
        try:
            return self.expr()
        finally:
            self.en_cabecera -= 1

    def es_comparador(self):
        return self.ver()[0] == "op" and self.ver()[1] in COMPARADORES

    def tras_y_o(self, palabra):
        """Después de 'y' u 'o' no puede venir un comparador: x > 3 y < 10."""
        if self.es_comparador():
            ejemplo = "x > 3 y x < 10" if palabra == "y" else "x < 3 o x > 10"
            raise ErrorMate(
                f"después de '{palabra}' hay que repetir la variable: {ejemplo}", self.ver()[2])

    def linea_previa(self):
        return self.t[self.i - 1][2] if self.i else 0

    # La regla de los renglones: una sentencia termina donde termina su renglón, salvo
    # que quede abierto un paréntesis, un corchete o una llave, o que el renglón termine
    # en un operador (+, -, y, ==, =...) o en una coma.
    def sigue_con(self, tipo, valores):
        """¿Viene uno de esos operadores a continuar la cuenta?"""
        tk = self.ver()
        if tk[0] != tipo or tk[1] not in valores:
            return False
        if self.abiertos or tk[2] == self.linea_previa():
            return True
        if tk[1] == "-":
            return False  # un '-' al principio de un renglón empieza otra sentencia
        raise ErrorMate(
            f"un renglón no puede empezar con '{tk[1]}': si la cuenta sigue abajo, dejá el "
            f"'{tk[1]}' al final del renglón de arriba", tk[2])

    def en_su_renglon(self, palabra, ln, ejemplo):
        """Lo que acompaña a 'responder', 'fallar', etc. empieza en el mismo renglón."""
        if self.ver()[2] != ln or self.es("eof") or self.es("op", "}"):
            raise ErrorMate(f"a '{palabra}' le falta lo que sigue, en el mismo renglón: "
                            f"{ejemplo}", ln)

    def fin_de_sentencia(self, s, vale_suelto=False):
        """'mostrar "hola"': un nombre suelto y algo más en el mismo renglón. Y un renglón
        que solo calcula (i + 1): se avisa antes de correr, esté donde esté."""
        tk = self.ver()
        if (s[0] == "expr" and s[2][0] == "nombre" and tk[2] == self.linea_previa()
                and tk[0] in ("str", "num", "id")):
            raise ErrorMate(f"a '{s[2][2]}' le faltan los paréntesis: {s[2][2]}(...)", tk[2])
        if s[0] == "expr" and not vale_suelto and s[2][0] not in (
                "llamar", "preguntar", "crear", "nombre"):
            raise renglon_sin_uso(s[2])

    # programa y sentencias
    def programa(self):
        cuerpo = []
        while not self.es("eof"):
            cuerpo.append(self.sentencia(nivel_superior=True))
            self.fin_de_sentencia(cuerpo[-1], self.en_consola)
        return cuerpo

    def bloque(self, vale_suelto=False):
        """vale_suelto: en 'asegurar falla { 10 / 0 }' una cuenta suelta tiene sentido."""
        self.espera("op", "{")
        cuerpo = []
        while not self.es("op", "}"):
            if self.es("eof"):
                raise ErrorMate("falta cerrar un bloque con '}'", self.ver()[2])
            cuerpo.append(self.sentencia())
            self.fin_de_sentencia(cuerpo[-1], vale_suelto)
        self.tomar()
        return cuerpo

    def sentencia(self, nivel_superior=False):
        tipo, val, ln = self.ver()
        if tipo == "kw":
            if val in ("sea", "var"):
                self.tomar()
                nombre = self.nombre_nuevo()
                self.espera("op", "=")
                return ("sea", ln, nombre, self.expr(), val == "var")
            if val == "funcion":
                return self.funcion()
            if val == "devolver":
                # Dentro de 'al recibir' también vale: termina de atender sin responder.
                if not (self.en_funcion or self.en_recibir):
                    raise ErrorMate(DEVOLVER_SUELTO, ln)
                self.tomar()
                e = None
                if self.ver()[2] == ln and not self.es("op", "}") and not self.es("eof"):
                    e = self.expr()
                return ("devolver", ln, e)
            if val == "si":
                self.tomar()
                if self.es("kw", "no") and self.es("op", "{", 1) and self.ver(1)[2] == ln:
                    raise ErrorMate("en Mate se escribe 'sino', todo junto (no 'si no')", ln)
                ramas, otro = [(self.condicion(), self.bloque())], None
                while self.acepta("kw", "sino"):
                    if self.acepta("kw", "si"):
                        ramas.append((self.condicion(), self.bloque()))
                    else:
                        otro = self.bloque()
                        break
                return ("si", ln, ramas, otro)
            if val == "mientras":
                self.tomar()
                return ("mientras", ln, self.condicion(), self.vuelta())
            if val == "para":
                self.tomar()
                nombre = self.nombre_nuevo()
                if self.acepta("op", ","):  # para posicion, item en lista
                    segundo = self.nombre_nuevo()
                    if segundo == nombre:
                        raise ErrorMate(f"los dos nombres del 'para' no pueden ser iguales "
                                        f"('{nombre}')", ln)
                    self.espera("kw", "en", que="'en' (para posicion, item en lista)")
                    return ("para2", ln, nombre, segundo, self.recorrido(), self.vuelta())
                self.espera("kw", "en", que="'en' (para item en lista)")
                return ("para", ln, nombre, self.recorrido(), self.vuelta())
            if val in ("romper", "continuar"):
                if not self.en_bucle:
                    raise ErrorMate(
                        f"'{val}' solo va dentro de un 'mientras' o de un 'para'", ln)
                self.tomar()
                return (val, ln)
            if val in ("mensaje", "agente", "prueba", "usar") and not nivel_superior:
                raise ErrorMate(f"'{val}' solo puede declararse en el nivel superior", ln)
            if val == "usar":
                self.tomar()
                return ("usar", ln, self.espera("str", que="el nombre de un archivo")[1])
            if val == "mensaje":
                return self.mensaje()
            if val == "agente":
                return self.agente()
            if val == "prueba":
                self.tomar()
                nombre = self.espera("str", que="el nombre de la prueba")[1]
                self.en_prueba += 1
                try:
                    return ("prueba", ln, nombre, self.bloque())
                finally:
                    self.en_prueba -= 1
            if val == "simular":
                return self.simular()
            if val == "enviar":
                self.tomar()
                self.en_su_renglon(val, ln, "enviar Aviso { ... } a Agente")
                msg = self.expr()
                self.espera("id", "a", que="'a' (enviar Mensaje a Agente)")
                return ("enviar", ln, msg, self.expr())
            if val == "responder":
                if not (self.en_recibir or (self.en_funcion and self.en_agente)):
                    raise ErrorMate(RESPONDER_SUELTO, ln)
                if self.en_al_fallar and not self.en_funcion:
                    raise ErrorMate(SIN_A_QUIEN, ln)
                self.tomar()
                self.en_su_renglon(val, ln, "responder valor")
                return ("responder", ln, self.expr())
            if val == "fallar":
                self.tomar()
                self.en_su_renglon(val, ln, 'fallar "el motivo"')
                return ("fallar", ln, self.expr())
            if val == "intentar":
                self.tomar()
                cuerpo = self.bloque()
                self.espera("kw", "si", que="'si falla'")
                self.espera("kw", "falla", que="'si falla'")
                var = None if self.es("op", "{") else self.nombre_nuevo()
                return ("intentar", ln, cuerpo, var, self.bloque())
            if val == "asegurar":
                self.tomar()
                self.en_su_renglon(val, ln, "asegurar total == 10")
                if self.es("kw", "falla"):  # asegurar falla { ... }: esto tiene que fallar
                    self.tomar()
                    cuerpo = self.bloque(vale_suelto=True)
                    msg = self.expr() if self.acepta("op", ",") else None
                    return ("asegurar_falla", ln, cuerpo, msg)
                cond = self.expr()
                self.pista_de_igual()
                msg = self.expr() if self.acepta("op", ",") else None
                return ("asegurar", ln, cond, msg)
        if (tipo == "id" and va_en_minuscula(val) and val not in self.definidos
                and not (self.es("op", d=1) and self.ver(1)[1] in ("=", ".", "["))):
            raise ErrorMate(f"'{val}' va en minúscula: '{val.lower()}'", ln)
        e = self.expr()
        if self.acepta("op", "="):
            if not self.asignable(e):
                raise ErrorMate(NO_ASIGNABLE, ln)
            return ("asignar", ln, e, self.expr())
        for atajo in ("+=", "-="):  # suma += precio es suma = suma + precio
            if self.acepta("op", atajo):
                if not self.asignable(e):
                    raise ErrorMate(NO_ASIGNABLE, ln)
                return ("asignar", ln, e, ("bin", ln, atajo[0], e, self.expr()))
        return ("expr", ln, e)

    def simular(self):
        """simular Vendedor al recibir Pedido como p { responder ... }: en lo que queda de
        la prueba, ese agente contesta eso."""
        ln = self.tomar()[2]
        if not self.en_prueba or self.en_funcion or self.en_recibir:
            raise ErrorMate("'simular' solo va dentro de una prueba", ln)
        ejemplo = "simular Vendedor al recibir Pedido como p { responder ... }"
        self.en_su_renglon("simular", ln, ejemplo)
        agente = self.postfijo()
        self.espera("kw", "al", que=f"'al recibir' ({ejemplo})")
        self.espera("kw", "recibir", que=f"'al recibir' ({ejemplo})")
        tipo = self.espera("id", que="un tipo de mensaje")[1]
        var = self.nombre_nuevo() if self.acepta("kw", "como") else None
        self.en_recibir += 1
        try:
            cuerpo = self.aparte()
        finally:
            self.en_recibir -= 1
        return ("simular", ln, agente, tipo, var, cuerpo)

    def vuelta(self):
        """El bloque de un 'mientras' o un 'para': adentro valen 'romper' y 'continuar'."""
        self.en_bucle += 1
        try:
            return self.bloque()
        finally:
            self.en_bucle -= 1

    def aparte(self):
        """El bloque de una función o de un 'al recibir': empieza de cero, no está
        dentro del bucle que lo rodee."""
        afuera, self.en_bucle = self.en_bucle, 0
        try:
            return self.bloque()
        finally:
            self.en_bucle = afuera

    def asignable(self, e):
        """Se asigna a una variable o a una parte de una variable: x, x.campo, x[0]."""
        return e[0] == "nombre" or (e[0] in ("indice", "campo") and self.asignable(e[2]))

    def funcion(self):
        ln = self.tomar()[2]
        nombre = self.nombre_nuevo("el nombre de la función")
        self.espera("op", "(")
        params = []
        while not self.es("op", ")"):
            params.append(self.nombre_nuevo("un parámetro"))
            if not self.acepta("op", ","):
                break
        self.espera("op", ")")
        self.en_funcion += 1
        try:
            cuerpo = self.aparte()
        finally:
            self.en_funcion -= 1
        return ("funcion", ln, nombre, params, cuerpo)

    def mensaje(self):
        ln = self.tomar()[2]
        nombre = self.nombre_propio("mensaje")
        campos = []
        # La llave también puede venir en el renglón de abajo: un renglón nunca empieza
        # con '{' por otro motivo.
        if self.es("op", "{"):
            self.tomar()
            while not self.es("op", "}"):
                campo = self.nombre_de_campo()
                self.espera("op", ":")
                tipo = self.tipo_de_campo()
                opcional = bool(self.acepta("op", "?"))
                campos.append((campo, tipo, opcional))
                if not self.acepta("op", ","):
                    break
            self.espera("op", "}")
        responde = None  # mensaje Pedido { ... } responde Cotizacion
        if self.es("id", "responde") and self.ver()[2] == self.linea_previa():
            self.tomar()
            responde = self.tipo_de_campo()
        return ("mensaje", ln, nombre, campos, responde)

    def tipo_de_campo(self):
        """numero, texto, Pedido... o 'lista de' cualquiera de esos."""
        tipo = (self.acepta("kw", "agente") or self.espera("id", que="un tipo"))[1]
        if tipo == "lista" and self.es("id", "de"):
            self.tomar()
            return "lista de " + self.tipo_de_campo()
        return tipo

    def nombre_propio(self, que):
        tk = self.espera("id", que=f"el nombre del {que}")
        if not tk[1][0].isupper():
            raise ErrorMate(f"el nombre de un {que} empieza con mayúscula: '{tk[1]}'", tk[2])
        return tk[1]

    def agente(self):
        ln = self.tomar()[2]
        nombre = self.nombre_propio("agente")
        self.espera("op", "{")
        estados, manejadores, funciones = [], [], []
        self.en_agente += 1
        try:
            self.miembros_de_agente(estados, manejadores, funciones)
        finally:
            self.en_agente -= 1
        return ("agente", ln, nombre, estados, manejadores, funciones)

    def miembros_de_agente(self, estados, manejadores, funciones):
        while not self.acepta("op", "}"):
            tk = self.ver()
            if self.acepta("kw", "estado"):
                n = self.nombre_nuevo()
                self.espera("op", "=")
                estados.append((tk[2], n, self.expr()))
            elif self.acepta("kw", "al"):
                if self.acepta("kw", "fallar"):  # al fallar como f { ... }
                    tipo = AL_FALLAR
                    self.en_al_fallar += 1
                else:
                    self.espera("kw", "recibir", que="'recibir' o 'fallar' (al recibir "
                                                     "Pedido como p, al fallar como f)")
                    tipo = self.espera("id", que="un tipo de mensaje")[1]
                var = self.nombre_nuevo() if self.acepta("kw", "como") else None
                self.en_recibir += 1
                try:
                    cuerpo = self.aparte()
                finally:
                    self.en_recibir -= 1
                    self.en_al_fallar = 0
                manejadores.append((tk[2], tipo, var, cuerpo))
            elif self.es("kw", "funcion"):
                funciones.append(self.funcion())
            elif tk[0] == "id" and va_en_minuscula(tk[1]):
                raise ErrorMate(f"'{tk[1]}' va en minúscula: '{tk[1].lower()}'", tk[2])
            else:
                raise ErrorMate(
                    "dentro de un agente solo van 'estado', 'al recibir' y 'funcion'", tk[2]
                )

    # expresiones
    def expr(self):
        izq = self.expr_y()
        while self.sigue_con("kw", ("o",)):
            ln = self.tomar()[2]
            self.tras_y_o("o")
            izq = ("o", ln, izq, self.expr_y())
        return izq

    def expr_y(self):
        izq = self.expr_no()
        while self.sigue_con("kw", ("y",)):
            ln = self.tomar()[2]
            self.tras_y_o("y")
            izq = ("y", ln, izq, self.expr_no())
        return izq

    def expr_no(self):
        if self.es("kw", "no"):
            ln = self.tomar()[2]
            return ("no", ln, self.expr_no())
        return self.comparacion()

    def comparacion(self):
        izq = self.suma()
        if self.sigue_con("op", COMPARADORES):
            _, op, ln = self.tomar()
            if self.es("op", "=") and self.ver()[2] == ln:
                raise ErrorMate("para comparar se usa '==' (con dos signos '=', no más)", ln)
            if op == "<" and self.es("op", ">") and self.ver()[2] == ln:
                raise ErrorMate("'distinto' se escribe '!='", ln)
            izq = ("bin", ln, op, izq, self.suma())
            if self.es_comparador():
                raise ErrorMate(
                    "las comparaciones no se encadenan: escribí 1 < x y x < 10", self.ver()[2])
        return izq

    def suma(self):
        izq = self.producto()
        while self.sigue_con("op", ("+", "-")):
            _, op, ln = self.tomar()
            izq = ("bin", ln, op, izq, self.producto())
        return izq

    def producto(self):
        izq = self.unario()
        while self.sigue_con("op", ("*", "/", "%")):
            _, op, ln = self.tomar()
            previo = self.t[self.i - 2]
            if op == "%" and previo[0] == "num" and (
                    self.ver()[2] != ln or self.es("eof")
                    or (self.es("op") and self.ver()[1] in (")", "]", "}", ","))):
                n = formato(previo[1])  # sea iva = 21%
                raise ErrorMate(
                    f"en Mate '%' es el resto de una división, no un porcentaje. El {n}% se "
                    f"escribe como una cuenta: {n} / 100 (o {formato(previo[1] / 100)}). Si de "
                    "verdad era el resto, escribí la cuenta entera en este renglón", ln)
            izq = ("bin", ln, op, izq, self.unario())
        return izq

    def unario(self):
        if self.es("op", "-"):
            ln = self.tomar()[2]
            return ("neg", ln, self.unario())
        return self.postfijo()

    def postfijo(self):
        e = self.primario()
        while True:
            tk = self.ver()
            misma = tk[2] == self.linea_previa()
            if misma and self.es("op", "("):
                self.tomar()
                args = self.lista_hasta(")")
                e = ("llamar", tk[2], e, args)
            elif misma and self.es("op", "["):
                self.tomar()
                self.abiertos += 1
                idx = self.expr()
                self.abiertos -= 1
                self.espera("op", "]")
                e = ("indice", tk[2], e, idx)
            elif self.es("op", "."):
                self.tomar()
                e = ("campo", tk[2], e, self.nombre_de_campo())
            else:
                return e

    def lista_hasta(self, cierre):
        items = []
        self.abiertos += 1
        while not self.es("op", cierre):
            items.append(self.expr())
            if not self.acepta("op", ","):
                break
        self.abiertos -= 1
        self.espera("op", cierre)
        return items

    def pares(self, claves_texto):
        pares = []
        self.abiertos += 1
        while not self.es("op", "}"):
            tk = self.tomar()
            if not (tk[0] == "id" or (claves_texto and tk[0] == "str")
                    or (tk[0] == "kw" and self.es("op", ":"))):
                raise ErrorMate("esperaba un nombre de campo", tk[2])
            self.espera("op", ":")
            pares.append((tk[1], self.expr()))
            if not self.acepta("op", ","):
                break
        self.abiertos -= 1
        self.espera("op", "}")
        return pares

    def primario(self):
        tipo, val, ln = self.tomar()
        if tipo == "num":
            return ("num", ln, val)
        if tipo == "str":
            return self.texto(val, ln)
        if tipo == "kw":
            if val in ("verdadero", "falso"):
                return ("bool", ln, val == "verdadero")
            if val == "nada":
                return ("nada", ln)
            if val in ("remitente", "yo"):
                return (val, ln)
            if val == "crear":
                agente = self.espera("id", que="el nombre de un agente")[1]
                apodo, pares = None, []
                if self.es("id", "llamado"):
                    self.tomar()
                    tk = self.ver()
                    if tk[0] == "id" and tk[1][0].isupper():  # crear Vendedor llamado Sur
                        raise ErrorMate(
                            f"el nombre de la copia es un texto y va entre comillas: "
                            f'crear {agente} llamado "{tk[1]}"', tk[2])
                    apodo = self.suma()  # cualquier texto: "Sucursal " + nombre
                # La llave puede venir en el renglón de abajo, salvo en la condición de un
                # 'si' o un 'mientras': ahí la llave de abajo es la del bloque.
                if self.es("op", "{") and (self.ver()[2] == self.linea_previa() or not (
                        self.abiertos or self.en_cabecera)):
                    self.tomar()  # (la llave puede venir en el renglón de abajo)
                    pares = self.pares(False)
                return ("crear", ln, agente, apodo, pares)
            if val == "preguntar":
                msg = self.expr()
                self.espera("id", "a", que="'a' (preguntar Mensaje a Agente)")
                return ("preguntar", ln, msg, self.postfijo())
        if tipo == "id":
            if val[0].isupper() and self.es("op", "{") and self.ver()[2] == ln:
                self.tomar()
                return ("ctor", ln, val, self.pares(False))
            if pista_de(val) and val not in self.definidos:
                # 'if', 'true', 'función'...: ese nombre no existe, así que el programa
                # iba a fallar igual; mejor explicarlo antes de correr.
                raise ErrorMate(pista_de(val), ln)
            return ("nombre", ln, val)
        if tipo == "op":
            if val == "(":
                self.abiertos += 1
                e = self.expr()
                self.abiertos -= 1
                self.pista_de_igual()
                self.espera("op", ")")
                return e
            if val == "[":
                return ("lista", ln, self.lista_hasta("]"))
            if val == "{":
                return ("mapa", ln, self.pares(True))
        previo = self.t[self.i - 2] if self.i >= 2 else (None, None, None)
        if (tipo, val) == ("op", "=") and previo[0] == "op" and previo[1] in ("*", "/", "%") \
                and previo[2] == ln:  # x *= 2
            raise ErrorMate("los únicos atajos son '+=' y '-='; lo demás se escribe "
                            f"entero: x = x {previo[1]} ...", ln)
        visto = "el final del archivo" if tipo == "eof" else f"'{val}'"
        raise ErrorMate(f"no esperaba {visto} acá", ln)

    def texto(self, crudo, ln):
        """Texto con escapes e interpolación: "Total: {precio * 2}"."""
        partes, actual, i = [], [], 0
        escapes = {"n": "\n", "t": "\t", "\\": "\\", "{": "{", "}": "}"}
        escapes.update((c, c) for c in _COMILLAS)
        if parece_ruta(crudo):
            raise ErrorMate(
                "esto parece una ruta de Windows, y dentro de un texto la barra \\ es "
                "especial (\\n es un salto de renglón y \\t un espacio largo). "
                + COMO_VAN_LAS_RUTAS, ln)
        while i < len(crudo):
            c = crudo[i]
            if c == "\\" and i + 1 < len(crudo):
                if crudo[i + 1] not in escapes:
                    raise ErrorMate(
                        f"dentro de un texto la barra \\ es especial, y \\{crudo[i + 1]} no "
                        "significa nada. Para escribir una barra de verdad va doble: \\\\. "
                        + COMO_VAN_LAS_RUTAS, ln)
                actual.append(escapes[crudo[i + 1]])
                i += 2
            elif c == "{":
                fin = _fin_de_llave(crudo, i)
                if fin < 0:  # no cierra bien: se cuenta a la antigua, para explicar el error
                    fin, prof = i + 1, 1
                    while fin < len(crudo) and prof:
                        prof += {"{": 1, "}": -1}.get(crudo[fin], 0)
                        fin += 1
                    if prof:
                        raise ErrorMate(
                            "falta '}' en el texto (usá \\{ para una llave literal)", ln)
                if actual:
                    partes.append("".join(actual))
                    actual = []
                adentro = crudo[i + 1 : fin - 1]
                if not adentro.strip():
                    raise ErrorMate("dentro del texto: entre { y } falta algo "
                                    "(usá \\{ para una llave literal)", ln)
                try:
                    sub = Parser([(t, v, ln) for t, v, _ in tokenizar(adentro)])
                    sub.definidos = self.definidos
                    partes.append(sub.expr())
                    sub.espera("eof", que="el fin de la expresión")
                except ErrorMate as e:
                    if "el final del archivo" in e.mensaje:
                        raise ErrorMate(
                            "dentro del texto: lo que está entre { y } quedó a medio escribir "
                            "(usá \\{ para una llave literal)", ln)
                    raise ErrorMate(f"dentro del texto: {e.mensaje}", ln)
                i = fin
            else:
                actual.append(c)
                i += 1
        if actual:
            partes.append("".join(actual))
        if all(isinstance(p, str) for p in partes):
            return ("str", ln, "".join(partes))
        return ("interp", ln, partes)


def renglon_sin_uso(e):
    """El error de un renglón que solo calcula un valor y no hace nada con él."""
    pista = ""
    if e[0] == "neg":
        pista = (". Si era la continuación de la cuenta de arriba, dejá el '-' al "
                 "final de ese renglón")
    return ErrorMate("este renglón calcula un valor y no hace nada con él: guardalo "
                     f"(sea x = ...), mostralo con mostrar(...) o borralo{pista}", e[1],
                     clase="escritura")


def leer_fuente(ruta):
    """Lee un archivo .mate en cualquiera de las codificaciones que usa el Bloc de notas:
    UTF-8 (con o sin marca), "Unicode" (UTF-16) o ANSI (Windows-1252)."""
    with open(ruta, "rb") as f:
        datos = f.read()
    if datos[:2] in (b"\xff\xfe", b"\xfe\xff"):
        codificaciones = ("utf-16",)
    elif len(datos) >= 4 and datos.count(0) >= len(datos) // 4:
        # "Unicode" sin la marca del principio: una letra de por medio es un cero
        codificaciones = ("utf-16-le" if datos[1::2].count(0) >= datos[0::2].count(0)
                          else "utf-16-be", "utf-8-sig", "cp1252")
    else:
        codificaciones = ("utf-8-sig", "cp1252")
    for codificacion in codificaciones:
        try:
            texto = datos.decode(codificacion)
        except UnicodeError:
            continue
        return texto.replace("\r\n", "\n").replace("\r", "\n")
    raise ErrorMate(f"no pude leer las letras de {ruta}. En el Bloc de notas: "
                    "Archivo > Guardar como > Codificación: UTF-8")


def analizar(fuente, ruta=None, _vistos=None, en_consola=False):
    """Convierte el texto en un programa, incluyendo lo que traiga con 'usar'."""
    vistos = _vistos if _vistos is not None else set()
    if ruta:
        vistos.add(os.path.realpath(ruta))
    carpeta = os.path.dirname(os.path.abspath(ruta)) if ruta else os.getcwd()
    programa = []
    tokens = tokenizar(fuente, ruta)
    revisar_cierres(tokens, fuente)
    for s in Parser(tokens, en_consola).programa():
        if s[0] != "usar":
            programa.append(s)
            continue
        otra = os.path.join(carpeta, s[2])
        if not os.path.isfile(otra) and os.path.isfile(otra + ".mate"):
            otra += ".mate"  # usar "catalogo" también encuentra catalogo.mate
        try:
            otra = os.path.relpath(otra)
        except ValueError:  # en Windows, si está en otro disco
            pass
        if os.path.realpath(otra) in vistos:
            continue
        try:
            texto = leer_fuente(otra)
        except OSError:
            raise ErrorMate(f"no pude abrir '{s[2]}' (lo busqué en {carpeta})"
                            + pista_de_usar(carpeta, s[2]), s[1])
        except ErrorMate as e:
            e.linea = e.linea or s[1]
            raise
        try:
            traido = analizar(texto, otra, vistos)
        except ErrorMate as e:
            if not getattr(e, "traido", False):  # se dice una vez: quién lo trajo
                desde = f"desde {os.path.basename(ruta)}, línea {s[1]}" if ruta \
                    else f"en la línea {s[1]}"
                e.mensaje += (f" (este archivo, {os.path.basename(otra)}, se trajo con "
                              f"'usar' {desde})")
                e.traido = True
            raise
        # De un archivo usado se toman las declaraciones, no lo que ejecuta ni sus pruebas.
        programa.extend(x for x in traido
                        if x[0] in ("mensaje", "agente", "funcion", "sea"))
    return programa


def pista_de_usar(carpeta, nombre):
    """Qué pudo haber pasado con un archivo de 'usar' que no aparece."""
    # usar "catalogo" vale por usar "catalogo.mate": las pistas se buscan con las dos formas
    formas = [nombre] if nombre.lower().endswith(".mate") else [nombre + ".mate", nombre]
    for forma in formas:
        if os.path.isfile(os.path.join(carpeta, forma + ".txt")):
            return (f". Encontré {os.path.basename(forma)}.txt: el Bloc de notas le agregó "
                    ".txt; renombralo, o al guardar elegí Tipo: Todos los archivos")
    try:
        hay = sorted(a for a in os.listdir(os.path.dirname(os.path.join(carpeta, nombre)))
                     if a.lower().endswith(".mate"))
    except OSError:
        return ". Esa carpeta no existe"
    for forma in formas:
        parecido = difflib.get_close_matches(os.path.basename(forma), hay, n=1, cutoff=0.75)
        if parecido:
            return f". ¿Quisiste decir '{parecido[0]}'?"
    if hay:
        return (". Los archivos .mate que hay ahí: " + ", ".join(hay[:10])
                + (", ..." if len(hay) > 10 else ""))
    return ""


# ─────────────────────── Verificación estática ───────────────────────

_LITERALES = {"num": "numero", "str": "texto", "interp": "texto", "bool": "logico",
              "lista": "lista", "mapa": "mapa"}


def _es_nodo(n, clase, largo):
    """¿Es una sentencia o expresión de esa clase? (y no un par 'clave: valor' de un mapa)"""
    return (isinstance(n, tuple) and len(n) == largo and n[0] == clase
            and isinstance(n[1], int))


def _ligaduras(programa):
    """Cuántas veces se le pone cada nombre a algo (variable, parámetro, función...).
    Un nombre puesto una sola vez no puede estar tapado por otro igual."""
    veces = {}

    def anotar(nombre):
        if nombre:
            veces[nombre] = veces.get(nombre, 0) + 1

    def visitar(n):
        if isinstance(n, list):
            for x in n:
                visitar(x)
            return
        if not isinstance(n, tuple):
            return
        if _es_nodo(n, "sea", 5) or _es_nodo(n, "para", 5):
            anotar(n[2])
        elif _es_nodo(n, "para2", 6):
            anotar(n[2])
            anotar(n[3])
        elif _es_nodo(n, "funcion", 5):
            anotar(n[2])
            for parametro in n[3]:
                anotar(parametro)
        elif _es_nodo(n, "intentar", 5):
            anotar(n[3])
        elif _es_nodo(n, "simular", 6):
            anotar(n[4])
        elif _es_nodo(n, "agente", 6):
            anotar(n[2])
            for _, nombre, _ in n[3]:
                anotar(nombre)
            for _, _, var, _ in n[4]:
                anotar(var)
        for x in n:
            visitar(x)

    visitar(programa)
    return veces


def _contiene(n, clase, largo):
    """¿Hay adentro alguna sentencia de esa clase?"""
    if isinstance(n, (list, tuple)):
        return _es_nodo(n, clase, largo) or any(_contiene(x, clase, largo) for x in n)
    return False


def _nombra(n, nombres):
    """¿Se usa adentro alguno de esos nombres?"""
    if isinstance(n, (list, tuple)):
        return ((_es_nodo(n, "nombre", 3) and n[2] in nombres)
                or any(_nombra(x, nombres) for x in n))
    return False


def literal_que_no_cumple(e, tipo):
    """Si ese valor escrito a mano seguro no es de ese tipo, dice de qué tipo es (y si el
    problema está adentro de una lista): (tipo, adentro). Si cumple o no se sabe, None."""
    real = e[2] if e[0] == "ctor" else _LITERALES.get(e[0])
    if not real or tipo == "cualquiera":
        return None
    if not tipo.startswith("lista de "):
        return (real, False) if real != tipo else None
    if real != "lista":
        return (real, False)
    for x in e[2]:
        malo = literal_que_no_cumple(x, tipo[len("lista de "):])
        if malo:
            return (malo[0], True)
    return None


def no_es_condicion(e):
    """Si eso, escrito así, seguro no da verdadero ni falso, el error; si no, None."""
    if not isinstance(e, tuple) or not e:
        return None
    principio = "la condición tiene que ser verdadero o falso"
    if e[0] == "nada":
        return f"{principio}, no el valor nada"
    if e[0] in _LITERALES and e[0] != "bool":
        return f"{principio}, no {_LITERALES[e[0]]}"
    if e[0] == "ctor":
        return f"{principio}, no un mensaje {e[2]}"
    if e[0] == "neg" or (e[0] == "bin" and e[2] in "+-*/%"):
        return (f"{principio}, y esto es una cuenta: da un número o un texto. ¿Faltó "
                "compararla con algo (por ejemplo: x + 1 > 0)?")
    return None


def de_donde_viene(previa, actual):
    """' (línea 3)' o, si el nombre vino de otro archivo, ' en lib.mate, que se trajo con
    'usar' (línea 3)': para el error de un nombre que se declara dos veces."""
    if not previa:
        return ""
    otro = getattr(previa, "archivo", None)
    if otro and otro != getattr(actual, "archivo", None):
        return (f": viene de {os.path.basename(otro)}, que se trajo con 'usar' (línea "
                f"{int(previa)} de ese archivo). Elegí otro nombre")
    return f" (línea {int(previa)})"


def repetidos(nombres):
    """Los nombres que aparecen más de una vez, en el orden en que se repiten."""
    vistos, dobles = set(), []
    for nombre in nombres:
        if nombre in vistos and nombre not in dobles:
            dobles.append(nombre)
        vistos.add(nombre)
    return dobles


def revisar_nombres(programa, mensajes, veces, en_consola=False):
    """Los nombres que no existen y las llamadas con la cantidad equivocada de valores,
    antes de correr: [(linea, texto)]. Ante la duda no avisa: solo dice lo que seguro
    fallaría al llegar a ese renglón.

    - Lo declarado en el nivel superior (sea, var, funcion, agente) se ve desde todos
      lados, esté arriba o abajo en el archivo, y venga o no de un 'usar'.
    - Lo de adentro de un bloque se ve en ese bloque y en los de más adentro.
    - Adentro de 'intentar { }' y de 'asegurar falla { }' no se mira: ahí una falla se
      ataja, o es justo lo que se quiere probar.
    - En la consola solo se mira la cantidad de valores de las funciones incluidas: ahí
      lo que falta se puede escribir en el renglón siguiente, y una función se puede rehacer."""
    errores, avisados = [], set()
    arriba = set(FUNCIONES) | {s[2] for s in programa if s[0] in ("sea", "funcion", "agente")}
    # Las funciones propias que seguro son esa función donde se las nombre: las de un
    # nombre que en todo el programa se le pone a una sola cosa.
    cuantos_lleva = {}

    def juntar_funciones(n):
        if isinstance(n, list):
            for x in n:
                juntar_funciones(x)
        elif isinstance(n, tuple):
            if _es_nodo(n, "funcion", 5) and isinstance(n[3], list) and veces.get(n[2]) == 1:
                cuantos_lleva[n[2]] = len(n[3])
            for x in n:
                juntar_funciones(x)

    if not en_consola:
        juntar_funciones(programa)

    def falta(nombre, linea, alcance, al_asignar=False):
        if en_consola:
            return
        if nombre in mensajes or nombre in avisados or any(nombre in a for a in alcance):
            return  # (un mensaje sin llaves ya tiene su propio aviso)
        avisados.add(nombre)  # una vez por nombre: lo demás sería repetir el mismo error
        visibles = [n for a in reversed(alcance) for n in sorted(a)]
        errores.append((linea, nombre_que_no_existe(nombre, visibles, al_asignar).mensaje))

    def bloque(cuerpo, alcance):
        propios = {s[2] for s in cuerpo if s[0] in ("sea", "funcion")}
        alcance = alcance + [propios]
        for s in cuerpo:
            sentencia(s, alcance)

    def funcion(s, alcance):
        bloque(s[4], alcance + [set(s[3])])

    def sentencia(s, alcance):
        clase = s[0]
        if clase == "sea":
            valor(s[3], alcance)
        elif clase == "funcion":
            funcion(s, alcance)
        elif clase in ("devolver", "responder", "fallar", "expr"):
            if s[2] is not None:
                valor(s[2], alcance)
        elif clase == "si":
            for condicion, cuerpo in s[2]:
                valor(condicion, alcance)
                bloque(cuerpo, alcance)
            if s[3] is not None:
                bloque(s[3], alcance)
        elif clase == "mientras":
            valor(s[2], alcance)
            bloque(s[3], alcance)
        elif clase == "para":
            valor(s[3], alcance)
            bloque(s[4], alcance + [{s[2]}])
        elif clase == "para2":
            valor(s[4], alcance)
            bloque(s[5], alcance + [{s[2], s[3]}])
        elif clase == "agente":
            adentro = alcance + [{e[1] for e in s[3]} | {f[2] for f in s[5]}]
            for _, _, inicial in s[3]:
                valor(inicial, adentro)
            for _, _, var, cuerpo in s[4]:
                bloque(cuerpo, adentro + [{var} if var else set()])
            for f in s[5]:
                funcion(f, adentro)
        elif clase == "prueba":
            bloque(s[3], alcance)
        elif clase == "simular":
            # Lo simulado ve lo de la prueba (y no el estado del agente).
            valor(s[2], alcance)
            bloque(s[5], alcance + [{s[4]} if s[4] else set()])
        elif clase == "enviar":
            valor(s[2], alcance)
            valor(s[3], alcance)
        elif clase == "intentar":
            # (lo de adentro del 'intentar' no se mira; lo de 'si falla', sí)
            bloque(s[4], alcance + [{s[3]} if s[3] else set()])
        elif clase == "asegurar":
            valor(s[2], alcance)
            if s[3] is not None:
                valor(s[3], alcance)
        elif clase == "asegurar_falla":
            if s[3] is not None:
                valor(s[3], alcance)
        elif clase == "asignar":
            raiz = s[2]
            while raiz[0] in ("indice", "campo"):
                raiz = raiz[2]
            if raiz[0] == "nombre":
                falta(raiz[2], raiz[1], alcance, al_asignar=True)
            valor(s[2], alcance)
            valor(s[3], alcance)

    def valor(e, alcance):
        clase = e[0]
        if clase == "nombre":
            falta(e[2], e[1], alcance)
        elif clase == "interp":
            for parte in e[2]:
                if not isinstance(parte, str):
                    valor(parte, alcance)
        elif clase == "lista":
            for x in e[2]:
                valor(x, alcance)
        elif clase == "mapa":
            for _, x in e[2]:
                valor(x, alcance)
        elif clase == "ctor":
            for _, x in e[3]:
                valor(x, alcance)
        elif clase == "crear":
            if e[3] is not None:
                valor(e[3], alcance)
            for _, x in e[4]:
                valor(x, alcance)
        elif clase in ("y", "o", "indice", "preguntar"):
            valor(e[2], alcance)
            valor(e[3], alcance)
        elif clase in ("no", "neg", "campo"):
            valor(e[2], alcance)
        elif clase == "bin":
            valor(e[3], alcance)
            valor(e[4], alcance)
        elif clase == "llamar":
            valor(e[2], alcance)
            for x in e[3]:
                valor(x, alcance)
            if e[2][0] != "nombre" or not any(e[2][2] in a for a in alcance):
                return
            nombre, texto = e[2][2], None
            if nombre in FUNCIONES:  # (una función incluida no se puede tapar)
                texto = cantidad_equivocada(nombre, len(e[3]))
            elif nombre in cuantos_lleva and cuantos_lleva[nombre] != len(e[3]):
                texto = ESPERA_OTRA_CANTIDAD.format(
                    n=nombre, espera=cuantos_lleva[nombre], recibe=len(e[3]))
            if texto:
                errores.append((e[1], texto))

    for s in programa:
        sentencia(s, [arriba])
    return errores


def verificar(programa, en_consola=False):
    """Revisa el programa antes de correr: los contratos de los mensajes, los nombres que
    no existen y lo demás que se puede saber sin ejecutarlo. Devuelve [(linea, texto)].
    en_consola: ahí no se avisa de los nombres que faltan (ver revisar_nombres)."""
    errores = []
    mensajes, agentes, estados = {}, {}, {}
    declarados = {}  # la declaración completa de cada agente
    veces = _ligaduras(programa)
    # Funciones que seguro son funciones donde se las nombre: las incluidas y las del
    # nivel superior cuyo nombre no se repite.
    funciones = set(incluidas()) | {
        s[2] for s in programa if s[0] == "funcion" and veces.get(s[2]) == 1}
    copias = {}  # 'sea v = crear V': la variable v es una copia de V

    def buscar_copias(n):
        if isinstance(n, list):
            for x in n:
                buscar_copias(x)
        elif isinstance(n, tuple):
            if (_es_nodo(n, "sea", 5) and not n[4] and veces.get(n[2]) == 1
                    and _es_nodo(n[3], "crear", 5)):
                copias[n[2]] = n[3][2]
            for x in n:
                buscar_copias(x)

    buscar_copias(programa)
    pruebas = {}
    for s in programa:
        if s[0] == "prueba":
            if s[2] in pruebas:
                errores.append((s[1], f'ya hay una prueba llamada "{s[2]}" (línea '
                                      f"{pruebas[s[2]]}): poneles nombres distintos, así se "
                                      "sabe cuál es la que falla"))
            pruebas.setdefault(s[2], s[1])
    def ya_declarado(s):
        previo = mensajes.get(s[2]) or declarados[s[2]]
        return f"'{s[2]}' ya está declarado" + de_donde_viene(previo[1], s[1])

    for s in programa:
        if s[0] == "mensaje":
            if s[2] in mensajes or s[2] in agentes:
                errores.append((s[1], ya_declarado(s)))
            mensajes[s[2]] = s
        elif s[0] == "agente":
            if s[2] in mensajes or s[2] in agentes:
                errores.append((s[1], ya_declarado(s)))
            agentes[s[2]] = [m[1] for m in s[4]]
            estados[s[2]] = {e[1]: e[2] for e in s[3]}
            declarados[s[2]] = s

    def respuestas_de(agente, tipo, cuerpo):
        """Los 'responder' con un valor escrito a mano que no cumple el contrato."""
        esperado = mensajes[tipo][4] if tipo in mensajes else None

        def mirar(n):
            if isinstance(n, list):
                for x in n:
                    mirar(x)
            elif isinstance(n, tuple):
                if _es_nodo(n, "responder", 3) and isinstance(n[2], tuple):
                    malo = literal_que_no_cumple(n[2], esperado)
                    if malo:
                        que = f"una lista con un valor de tipo {malo[0]}" if malo[1] else malo[0]
                        errores.append((n[1], (
                            f"{agente} responde {que} a '{tipo}', y el contrato dice "
                            f"que a {tipo} se le responde {esperado}")))
                for x in n:
                    mirar(x)

        if esperado:
            mirar(cuerpo)

    for s in mensajes.values():
        vistos = set()
        for campo, tipo, _ in s[3]:
            if campo in vistos:
                errores.append((s[1], f"{s[2]}: el campo '{campo}' está repetido"))
            vistos.add(campo)
            tipo = tipo.rsplit(" de ", 1)[-1]  # de 'lista de Pedido' importa 'Pedido'
            if tipo not in TIPOS_BASE and tipo not in mensajes:
                errores.append((s[1], con_pista(
                    f"{s[2]}.{campo}: no existe el tipo '{tipo}'", tipo,
                    sorted(TIPOS_BASE) + list(mensajes))))
        if s[4]:
            tipo = s[4].rsplit(" de ", 1)[-1]
            if tipo not in TIPOS_BASE and tipo not in mensajes:
                errores.append((s[1], con_pista(
                    f"{s[2]} responde '{tipo}', que no es un tipo ni un mensaje declarado",
                    tipo, sorted(TIPOS_BASE) + list(mensajes))))

    for s in programa:
        if s[0] == "agente":
            for k in repetidos(e[1] for e in s[3]):
                errores.append((next(e[0] for e in reversed(s[3]) if e[1] == k),
                                f"{s[2]}: el estado '{k}' está repetido"))
            vistos = set()
            for ln, tipo, _, cuerpo in s[4]:
                if tipo == AL_FALLAR:
                    if tipo in vistos:
                        errores.append((ln, f"{s[2]} ya tiene un 'al fallar': va uno solo"))
                    vistos.add(tipo)
                    continue
                if tipo not in mensajes:
                    errores.append((ln, con_sugerencia(
                        f"{s[2]} recibe '{tipo}', que no es un mensaje declarado",
                        tipo, mensajes)))
                if tipo in vistos:
                    errores.append((ln, f"{s[2]} ya tiene un 'al recibir {tipo}'"))
                vistos.add(tipo)
                respuestas_de(s[2], tipo, cuerpo)

    def agente_de(dest, ag):
        """A qué agente declarado le habla, si se puede saber antes de correr."""
        if _es_nodo(dest, "nombre", 3):
            if dest[2] in agentes:
                return dest[2]
            return copias.get(dest[2]) if copias.get(dest[2]) in agentes else None
        if _es_nodo(dest, "yo", 2):
            return ag if ag in agentes else None
        return None

    def nunca_responde(agente, tipo):
        s = declarados[agente]
        cuerpo = next(m[3] for m in s[4] if m[1] == tipo)
        if _contiene(cuerpo, "responder", 3):
            return False
        if cuerpo and _es_nodo(cuerpo[-1], "fallar", 3):
            return False  # falla siempre, a propósito: eso se ataja con 'intentar'
        return not _nombra(cuerpo, {f[2] for f in s[5]})  # quizá responde una función suya

    def visitar(n, ag=None):
        if isinstance(n, list):
            for x in n:
                visitar(x, ag)
            return
        if not isinstance(n, tuple):
            return
        if _es_nodo(n, "agente", 6):
            ag = n[2]
        # Lo que va de condición y, escrito así, nunca puede dar verdadero o falso.
        condiciones = []
        if _es_nodo(n, "si", 4) and isinstance(n[2], list):
            condiciones = [rama[0] for rama in n[2]]
        elif _es_nodo(n, "mientras", 4) or _es_nodo(n, "asegurar", 4) or _es_nodo(n, "no", 3):
            condiciones = [n[2]]
        elif _es_nodo(n, "y", 4) or _es_nodo(n, "o", 4):
            condiciones = [n[2], n[3]]
        for cond in condiciones:
            if no_es_condicion(cond):
                errores.append((cond[1] if isinstance(cond[1], int) else n[1],
                                no_es_condicion(cond)))
        if _es_nodo(n, "nombre", 3) and n[2] in mensajes:
            errores.append((n[1], (
                f"'{n[2]}' es un mensaje: para armar uno van las llaves, aunque no tenga "
                f"campos. Escribí {n[2]} {{}}")))
        if _es_nodo(n, "simular", 6) and isinstance(n[5], list):
            a_quien = agente_de(n[2], ag)
            if n[3] not in mensajes:
                errores.append((n[1], con_sugerencia(
                    f"no existe el mensaje '{n[3]}'", n[3], mensajes)))
            elif a_quien and n[3] not in agentes[a_quien]:
                errores.append((n[1], f"{a_quien} no sabe recibir '{n[3]}': solo se simula "
                                      "un mensaje que el agente ya recibe"))
            else:
                respuestas_de(a_quien or "el agente simulado", n[3], n[5])
            ag = ag or "(simulado)"  # adentro valen 'yo' y 'remitente'
        if len(n) == 4 and n[0] == "ctor" and isinstance(n[3], list):
            _, ln, nombre, pares = n
            if nombre not in mensajes:
                errores.append((ln, con_sugerencia(
                    f"no existe el mensaje '{nombre}'", nombre, mensajes)))
            else:
                decl = {c: (t, op) for c, t, op in mensajes[nombre][3]}
                dados = {}
                for k, e in pares:
                    if k in dados:
                        errores.append((ln, f"{nombre}: el campo '{k}' está repetido"))
                    dados[k] = e
                    if k not in decl:
                        errores.append((ln, con_sugerencia(
                            f"{nombre} no tiene un campo '{k}'", k, decl)))
                        continue
                    tipo = decl[k][0]
                    if e[0] == "nada" and not decl[k][1] and tipo != "cualquiera":
                        errores.append((ln, (
                            f"{nombre}.{k} es obligatorio y le diste nada. Si puede faltar, "
                            f"declaralo opcional en el mensaje: {k}: {tipo}?")))
                        continue
                    if _es_nodo(e, "nombre", 3) and e[2] in funciones:
                        errores.append((ln, "los mensajes llevan datos, no funciones "
                                            f"(campo '{k}' de {nombre})"))
                        continue
                    base = tipo.rsplit(" de ", 1)[-1]
                    if base not in TIPOS_BASE and base not in mensajes:
                        continue  # ese tipo no existe: ya lo dice el error del mensaje
                    malo = literal_que_no_cumple(e, tipo)
                    if malo and malo[1]:
                        errores.append((ln, f"{nombre}.{k} es de tipo {tipo}, y adentro de "
                                            f"la lista hay un valor de tipo {malo[0]}"))
                    elif malo:
                        errores.append((ln, f"{nombre}.{k} es de tipo {tipo}, no {malo[0]}"))
                for c, (_, opcional) in decl.items():
                    if c not in dados and not opcional:
                        errores.append((ln, f"a {nombre} le falta el campo '{c}'"))
        elif len(n) == 5 and n[0] == "crear" and isinstance(n[4], list):
            _, ln, nombre, _, pares = n
            if nombre not in agentes:
                errores.append((ln, con_sugerencia(
                    f"no existe el agente '{nombre}'", nombre, agentes)))
            else:
                for k in repetidos(k for k, _ in pares):
                    errores.append((ln, f"{nombre}: el estado '{k}' está repetido"))
                for k, e in pares:
                    if k not in estados[nombre]:
                        errores.append((ln, f"{nombre} no tiene un estado '{k}'"))
                        continue
                    declarado = _LITERALES.get(estados[nombre][k][0])
                    dado = _LITERALES.get(e[0])
                    if declarado and dado and declarado != dado:
                        errores.append((ln, f"{nombre}.{k} arranca como {declarado} "
                                            f"y le diste {dado}"))
        elif len(n) == 4 and n[0] in ("enviar", "preguntar"):
            _, ln, msg, dest = n
            varios = n[0] == "enviar" and _es_nodo(dest, "lista", 3)  # enviar ... a [a, b]
            for uno in (dest[2] if varios else [dest]):
                a_quien = agente_de(uno, ag)
                if a_quien and _es_nodo(msg, "ctor", 4) and msg[2] in mensajes:
                    if msg[2] not in agentes[a_quien]:
                        errores.append((ln, f"{a_quien} no sabe recibir '{msg[2]}'"))
                    elif n[0] == "preguntar" and nunca_responde(a_quien, msg[2]):
                        errores.append((ln, f"{a_quien} recibe '{msg[2]}' pero nunca "
                                            "responde: no se le puede preguntar (le falta "
                                            "un 'responder')"))
        elif _es_nodo(n, "mapa", 3) and isinstance(n[2], list):
            for k in repetidos(k for k, _ in n[2]):
                errores.append((n[1], f"la clave '{k}' está repetida en el mapa: la segunda "
                                      "taparía a la primera"))
        elif _es_nodo(n, "funcion", 5) and isinstance(n[3], list):
            for k in repetidos(n[3]):
                errores.append((n[1], f"{n[2]}(): el parámetro '{k}' está repetido"))
        elif (_es_nodo(n, "yo", 2) or _es_nodo(n, "remitente", 2)) and ag is None:
            que = ("el agente que está atendiendo" if n[0] == "yo"
                   else "quien le mandó el mensaje que está atendiendo")
            errores.append((n[1], f"'{n[0]}' solo existe dentro de un agente (es {que}); "
                                  "acá afuera no hay ninguno"))
        for x in n:
            visitar(x, ag)

    visitar(programa)
    errores += revisar_nombres(programa, mensajes, veces, en_consola)
    return sorted(set(errores))


# ───────────────────────────── Valores ─────────────────────────────


class Registro:
    """Un mensaje ya construido y validado. Inmutable."""

    def __init__(self, tipo, campos):
        self.tipo = tipo
        self.campos = campos

    def __eq__(self, otro):
        return igual(self, otro)

    __hash__ = None


class ErrorAtajado(str):
    """El error que ataja 'si falla e'. Es un texto como cualquier otro, que además
    recuerda los datos del error para detalle_de(e)."""

    def __new__(cls, error):
        obj = super().__new__(cls, error.mensaje)
        obj.detalle = {"texto": error.mensaje,
                       "linea": int(error.linea) if error.linea else None,
                       "clase": error.familia, "dato": error.dato}
        return obj


class Agente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.decl = None
        self.env = None
        self.manejadores = {}
        self.ocupado = False
        self.inicial = None  # el estado con el que nació (para empezar limpia cada prueba)
        self.creador = None  # si es una copia: el agente que la creó mientras atendía


class Funcion:
    def __init__(self, nombre, params, cuerpo, env):
        self.nombre, self.params, self.cuerpo, self.env = nombre, params, cuerpo, env


class Nativa:
    def __init__(self, nombre, fn):
        self.nombre, self.fn = nombre, fn


class _Retorno(Exception):
    def __init__(self, valor):
        self.valor = valor


class _Respuesta(Exception):
    def __init__(self, valor, linea=None):
        self.valor = valor
        self.linea = linea  # el renglón del 'responder'


class _Romper(Exception):
    """'romper': sale del bucle."""


class _Continuar(Exception):
    """'continuar': salta a la vuelta siguiente."""


def es_num(v):
    return type(v) in (int, float)


def nombre_tipo(v):
    if v is None:
        return "nada"
    if type(v) is bool:
        return "logico"
    if es_num(v):
        return "numero"
    if isinstance(v, str):
        return "texto"
    if isinstance(v, list):
        return "lista"
    if isinstance(v, dict):
        return "mapa"
    if isinstance(v, Registro):
        return v.tipo
    if isinstance(v, Agente):
        return "agente"
    return "funcion"


CAUSA_DE_NADA = ("'nada' es la falta de valor: ¿a la función le falta un 'devolver', o es "
                 "un campo opcional que vino vacío?")
_CON_ARTICULO = {"nada": "el valor nada", "numero": "un número", "texto": "un texto",
                 "logico": "un valor lógico", "lista": "una lista", "mapa": "un mapa",
                 "agente": "un agente", "funcion": "una función"}
_VERBOS = {"+": "sumar", "-": "restar", "*": "multiplicar", "/": "dividir", "%": "dividir"}


def tipo_claro(v):
    """El tipo para un mensaje de error: 'nada' suelto se lee como otra frase ("no se
    puede hacer nada"), así que se dice "el valor nada"."""
    return "el valor nada" if v is None else nombre_tipo(v)


def un(v):
    """'un número', 'una lista', 'el valor nada', 'un mensaje Pedido'."""
    return _CON_ARTICULO.get(nombre_tipo(v), f"un mensaje {nombre_tipo(v)}")


def alfabetico(t):
    """La clave para ordenar textos como en el diccionario: sin importar mayúsculas ni
    tildes, y con la ñ después de la n."""
    return sin_tildes(unicodedata.normalize("NFC", t).lower().replace("ñ", "n\U0010ffff"))


def claves_de_orden(valores):
    """Con qué comparar esos valores para ordenarlos: los números por su valor y los
    textos por el abecedario. Si están mezclados o son otra cosa, None."""
    if all(es_num(x) for x in valores):
        return list(valores)
    if all(isinstance(x, str) for x in valores):
        return [(alfabetico(x), x) for x in valores]
    return None


def lo_que_tiene(nombres):
    """' (tiene: a, b, c)' para el error de una clave o un campo que no está."""
    nombres = [str(n) for n in nombres]
    if not nombres:
        return " (está vacío)"
    return " (tiene: " + ", ".join(nombres[:8]) + (", ..." if len(nombres) > 8 else "") + ")"


def no_esta(mensaje, nombre, disponibles):
    """El error de una clave o un campo que no está: con el nombre parecido si lo hay
    y, si no, con la lista de los que sí hay."""
    return (con_sugerencia(mensaje, nombre, disponibles) if sugerir(nombre, disponibles)
            else mensaje + lo_que_tiene(disponibles))


def lleva_funcion(v):
    """¿Hay una función en este valor, aunque sea adentro de una lista, mapa o mensaje?"""
    if isinstance(v, (Funcion, Nativa)):
        return True
    if isinstance(v, list):
        return any(lleva_funcion(x) for x in v)
    if isinstance(v, dict):
        return any(lleva_funcion(x) for x in v.values())
    if isinstance(v, Registro):
        return any(lleva_funcion(x) for x in v.campos.values())
    return False


def igual(a, b):
    """Igualdad sin conversiones a escondidas, también adentro de listas y mapas:
    1 no es igual a verdadero, ni [1] a [verdadero]."""
    if es_num(a) and es_num(b):
        return a == b
    if isinstance(a, str) and isinstance(b, str):
        return str(a) == str(b)
    if type(a) is not type(b):
        return False
    if isinstance(a, list):
        return len(a) == len(b) and all(igual(x, y) for x, y in zip(a, b))
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(igual(v, b[k]) for k, v in a.items())
    if isinstance(a, Registro):
        return a.tipo == b.tipo and igual(a.campos, b.campos)
    return a == b


def muy_largo(que="el texto"):
    tope = f"{MAX_LARGO:,}".replace(",", ".")
    return ErrorMate(f"{que} quedaría demasiado largo (más de {tope} letras)"
                     if que.startswith("el") else
                     f"{que} quedaría demasiado larga (más de {tope} elementos)")


def revisar_peso(v, por_elemento=1):
    """Antes de pasar a texto una lista, un mapa o un mensaje: si entre todo lo que tiene
    adentro hay más de 10.000.000 de elementos o letras, es un error (y no una espera
    eterna). Lo de adentro puede estar repetido muchas veces sin ocupar memoria.
    por_elemento: cuántas letras ocupa como mínimo cada elemento al escribirlo ("1, ")."""
    def peso(x):
        if isinstance(x, str):
            return len(x)
        if isinstance(x, Registro):
            x = x.campos
        if isinstance(x, dict):
            x = x.values()
        elif not isinstance(x, list):
            return 1
        total = len(x) * por_elemento
        for y in x:
            if isinstance(y, (str, list, dict, Registro)):
                total += peso(y)
                if total > MAX_LARGO:
                    raise muy_largo()
        if total > MAX_LARGO:
            raise muy_largo()
        return total

    if isinstance(v, (list, dict, Registro)):
        peso(v)
    return v


def a_texto(v):
    """formato(v), cuidando que el texto no pase el tope."""
    t = formato(revisar_peso(v, 3))
    if len(t) > MAX_LARGO:
        raise muy_largo()
    return t


_FECHA = re.compile(r"\d\d/\d\d/\d{4}( \d\d:\d\d)?")


def se_juntan(a, b):
    """¿Son dos textos o dos listas? (lo que '+' pega uno atrás del otro)"""
    return any(isinstance(a, clase) and isinstance(b, clase) for clase in (str, list))


def decimal_limpio(v):
    """Un decimal como lo escribiría una persona: 0.1 + 0.2 se ve 0.3 y nunca sale 1e-05.
    Solo cambia cómo se muestra: el valor guardado es el mismo."""
    if math.isnan(v):
        return "no es un número"
    if math.isinf(v):
        return "infinito" if v > 0 else "-infinito"
    if v.is_integer():
        return str(int(v))
    t = repr(v)
    cifras = len(t.lstrip("-").split("e")[0].replace(".", "").lstrip("0"))
    if cifras > 15:  # trae el "ruido" de las cuentas con decimales: se muestra redondeado
        if abs(v) < 1e10:
            t = format(v, ".12g")
        else:  # en los números grandes solo se quita el ruido, no cifras de verdad
            corto = format(v, ".15g")
            if abs(float(corto) - v) <= abs(v) * 4.5e-16:
                t = corto
    if "e" in t:
        t = format(decimal.Decimal(t), "f")
    if "." in t:
        t = t.rstrip("0").rstrip(".")
    return t


def redondeo(x, decimales):
    """x redondeado a esa cantidad de decimales, con el medio hacia arriba (2.5 -> 3;
    en los negativos se aleja del cero: -2.5 -> -3). Devuelve un Decimal."""
    d = decimal.Decimal(x) if type(x) is int else decimal.Decimal(repr(x))
    if type(x) is float:
        # Se redondea el número como se muestra: 0.57 * 50 se ve 28.5 (por dentro es
        # 28.499999999999996) y redondea a 29, no a 28.
        limpio = decimal.Decimal(decimal_limpio(x))
        if -limpio.as_tuple().exponent > decimales:
            d = limpio
    if -d.as_tuple().exponent <= decimales:
        return d  # ya tiene esa cantidad de decimales o menos
    contexto = decimal.Context(prec=max(d.adjusted(), 0) + decimales + 10)
    return d.quantize(decimal.Decimal(1).scaleb(-decimales, contexto),
                      rounding=decimal.ROUND_HALF_UP, context=contexto)


_NUMERO_AR = re.compile(r"[+-]?[0-9]{1,3}(\.[0-9]{3})+,[0-9]+")       # 1.234,50
_NUMERO_COMA = re.compile(r"[+-]?[0-9]+,[0-9]+")                      # 3,5
_NUMERO_COMUN = re.compile(r"[+-]?[0-9]+(\.[0-9]+)?")                 # 12 y 3.5
_NUMERO_PESOS = re.compile(r"[+-]?[0-9]{1,3}(\.[0-9]{3})+")           # $ 3.500
_NUMERO_MILES = re.compile(r"[+-]?[0-9]{1,3}(\.[0-9]{3}){2,}")        # 1.234.567


def numero_de_texto(texto):
    """Lee un número escrito como texto, también a la argentina ("$ 1.234,50")."""
    def no_es():
        return ErrorMate(f"'{texto}' no es un número", familia="numero")

    t = texto.strip()
    if not t:
        raise ErrorMate("un texto vacío no es un número", familia="numero")
    con_signo = re.match(r"([+-]?)\$\s*", t)
    if con_signo:  # "$ 100" y también "-$ 100", que es como escribe pesos()
        t = con_signo.group(1) + t[con_signo.end():]
        if _NUMERO_PESOS.fullmatch(t):  # con el signo $, "3.500" son tres mil quinientos
            t = t.replace(".", "")
    if "." in t and "," in t:
        if not _NUMERO_AR.fullmatch(t):
            raise no_es()
        t = t.replace(".", "").replace(",", ".")
    elif "," in t:
        if not _NUMERO_COMA.fullmatch(t):
            raise no_es()
        t = t.replace(",", ".")
    elif _NUMERO_MILES.fullmatch(t):
        t = t.replace(".", "")
    elif not _NUMERO_COMUN.fullmatch(t):
        raise no_es()
    try:
        n = float(t) if "." in t else int(t)
    except ValueError:  # Python no convierte enteros de miles de cifras
        raise no_es()
    if type(n) is float and not math.isfinite(n):
        raise no_es()
    return n


def formato(v, raiz=True):
    if v is None:
        return "nada"
    if type(v) is bool:
        return "verdadero" if v else "falso"
    if type(v) is float:
        return decimal_limpio(v)
    if isinstance(v, str):
        return v if raiz else json.dumps(v, ensure_ascii=False)
    if isinstance(v, list):
        return "[" + ", ".join(formato(x, False) for x in v) + "]"
    if isinstance(v, dict):
        return "{" + ", ".join(f"{k}: {formato(x, False)}" for k, x in v.items()) + "}"
    if isinstance(v, Registro):
        if not v.campos:
            return v.tipo
        return v.tipo + " { " + ", ".join(
            f"{k}: {formato(x, False)}" for k, x in v.campos.items()) + " }"
    if isinstance(v, Agente):
        return v.nombre if raiz else f"<agente {v.nombre}>"
    if isinstance(v, (Funcion, Nativa)):
        return f"<funcion {v.nombre}>"
    try:
        return str(v)
    except ValueError:  # Python no escribe enteros de miles de cifras
        raise ErrorMate("ese número es demasiado grande para mostrarlo")


_JSON_EN_CRIOLLO = (
    ("Expecting value", "falta un valor"),
    ("Expecting ',' delimiter", "falta una coma o el cierre (']' o '}')"),
    ("Expecting ':' delimiter", "faltan los dos puntos ':' después de una clave"),
    ("Expecting property name", "las claves van entre comillas dobles"),
    ("Illegal trailing comma", "sobra una coma antes del cierre"),
    ("Extra data", "sobra texto después del final"),
    ("Unterminated string", "hay un texto al que le falta la comilla de cierre"),
    ("Invalid control character", "hay un salto de renglón dentro de un texto"),
    ("Invalid", "hay una barra \\ mal usada dentro de un texto"),
)


def json_invalido(texto, error):
    """El error de leer un JSON, explicado en español."""
    if not texto.strip():
        return "JSON inválido: el texto está vacío"
    motivo = next((criollo for ingles, criollo in _JSON_EN_CRIOLLO
                   if error.msg.startswith(ingles)), "no lo pude entender")
    if error.pos >= len(texto.rstrip()):
        return f"JSON inválido: {motivo} (al final del texto)"
    return f"JSON inválido: {motivo} (en la letra {error.pos + 1} del texto)"


# Por qué no se puede cambiar un nombre, según de dónde salió.
NO_SE_CAMBIA = {
    "sea": "'{n}' es fijo (sea); declaralo con 'var' para cambiarlo",
    "parametro": "'{n}' es un parámetro y no se cambia; guardalo en otra variable: "
                 "var {n}2 = {n}",
    "para": "'{n}' es la variable del 'para' y no se cambia adentro del bucle",
    "mensaje": "'{n}' es el mensaje recibido y no se cambia; copiá lo que necesites a una "
               "variable con 'var'",
    "falla": "'{n}' es el error atajado y no se cambia",
    "funcion": "'{n}' es una función y no se le puede asignar un valor",
    "agente": "'{n}' es un agente y no se le puede asignar un valor",
    "nativa": "'{n}' es una función incluida de Mate y no se le puede asignar un valor",
}


def por_teclado(pregunta):
    """Muestra la pregunta y espera que la persona escriba y apriete Enter."""
    return input(pregunta if pregunta.endswith((" ", "\n")) or not pregunta
                 else pregunta + " ")


def incluidas():
    """Los nombres de las funciones incluidas (mostrar, texto, pesos...)."""
    return frozenset(FUNCIONES)


class Entorno:
    nacidos = 0  # cuántos entornos se crearon: sirve para saber cuál es anterior a cuál
    se_pisa = False  # solo en la consola: declarar de nuevo un nombre reemplaza al anterior

    def __init__(self, padre=None, frontera=False, borde=False):
        Entorno.nacidos += 1
        self.serie = Entorno.nacidos
        self.vars = {}
        self.origen = {}  # de dónde salió cada nombre: sea, var, parametro, para, funcion...
        self.renglon = {}  # en qué renglón se declaró cada variable
        self.padre = padre
        self.frontera = frontera  # el estado de un agente: de acá para arriba no se escribe
        self.borde = borde  # donde empieza una función, un 'al recibir' o una prueba

    def definir(self, nombre, valor, mutable=False, origen=None, linea=None):
        if nombre in self.vars and not (
                self.se_pisa and self.origen.get(nombre) in ("sea", "var", "funcion", "agente")):
            previo = self.origen.get(nombre)
            if previo == "nativa":
                raise ErrorMate(INCLUIDA.format(n=nombre))
            de_otro = getattr(self.renglon.get(nombre), "archivo", None)
            if de_otro and de_otro != getattr(linea, "archivo", None):
                raise ErrorMate(f"'{nombre}' ya existe"
                                + de_donde_viene(self.renglon[nombre], linea))
            ayuda = ""
            if previo in ("sea", "var"):
                ayuda = (f"; para cambiarle el valor se escribe {nombre} = ... "
                         "(y tiene que ser 'var')")
            raise ErrorMate(f"'{nombre}' ya está definido en este bloque{ayuda}")
        if self.padre is not None:  # tampoco se tapa una función incluida desde adentro
            raiz = self.padre
            while raiz.padre is not None:
                raiz = raiz.padre
            if raiz.origen.get(nombre) == "nativa":
                raise ErrorMate(INCLUIDA.format(n=nombre))
        self.vars[nombre] = [valor, mutable]
        self.origen[nombre] = origen or ("var" if mutable else "sea")
        if linea:
            self.renglon[nombre] = linea

    def no_tapar(self, nombre):
        """Un 'sea' o 'var' de un bloque de adentro (si, mientras, para, intentar) no
        puede repetir el nombre de una variable de más afuera: casi siempre se quiso
        cambiar esa variable, y con el 'sea' de más no cambia nada."""
        ya_existe = ErrorMate(
            f"'{nombre}' ya existe afuera de este bloque. Si querés cambiarle el "
            f"valor, sacá el 'sea' o el 'var': {nombre} = ... Si es otra cosa, "
            "ponele otro nombre")
        e = self
        while not e.borde and e.padre is not None:
            e = e.padre
            if nombre in e.vars and e.origen.get(nombre) in (
                    "sea", "var", "parametro", "para", "mensaje", "falla"):
                raise ya_existe
        # Desde un bloque de adentro de una función, una prueba o un 'al recibir' tampoco
        # se tapa una variable 'var' del programa: ahí también se la quiso cambiar.
        afuera = e.padre if (e.borde and e is not self) else None
        while afuera is not None:
            if nombre in afuera.vars:
                if afuera.origen.get(nombre) == "var" and not afuera.frontera:
                    raise ya_existe
                break
            afuera = afuera.padre
        if e.borde and e.padre is not None and e.padre.frontera and nombre in e.padre.vars \
                and e.padre.origen.get(nombre) == "var":
            raise ErrorMate(
                f"'{nombre}' es un estado de este agente. Si querés cambiarle el valor, "
                f"sacá el 'sea' o el 'var': {nombre} = ... Si es otra cosa, ponele otro nombre")

    def visibles(self):
        """Todos los nombres que se ven desde acá, de adentro hacia afuera."""
        nombres, e = [], self
        while e:
            nombres.extend(e.vars)
            e = e.padre
        return nombres

    def no_existe(self, nombre, al_asignar=False):
        return nombre_que_no_existe(nombre, self.visibles(), al_asignar)

    def buscar(self, nombre):
        e = self
        while e:
            if nombre in e.vars:
                return e.vars[nombre][0]
            e = e.padre
        raise self.no_existe(nombre)

    def asignar(self, nombre, valor):
        e, cruzo = self, False
        while e:
            if nombre in e.vars:
                if not e.vars[nombre][1]:
                    motivo = NO_SE_CAMBIA.get(e.origen.get(nombre), NO_SE_CAMBIA["sea"])
                    raise ErrorMate(motivo.format(n=nombre))
                if cruzo:
                    raise ErrorMate(
                        f"un agente no puede modificar '{nombre}': es de afuera. "
                        "Los agentes solo cambian su propio estado")
                e.vars[nombre][0] = valor
                return
            cruzo = cruzo or e.frontera
            e = e.padre
        raise self.no_existe(nombre, al_asignar=True)


# ───────────────────────────── Intérprete ─────────────────────────────


class Interprete:
    def __init__(self, salida=print, traza=False):
        self.salida = salida
        self.traza = traza
        self.anotar = None  # si la traza va a un archivo, quién recibe cada renglón
        self.cuenta = {"enviar": 0, "preguntar": 0, "fallaron": 0}  # para el resumen
        self.glob = Entorno()
        self.mensajes = {}
        self.responde = {}  # mensaje -> qué se le contesta, si el contrato lo dice
        self.agentes = {}
        self.decl_agentes = []
        self.copias = {}
        self.cola = deque()
        self.contexto = None  # (agente, remitente, tipo de mensaje) mientras se atiende uno
        self.entregados = 0
        self.pasos = 0
        self.max_pasos = MAX_PASOS  # None = sin tope
        self.linea_actual = None  # la última sentencia que se empezó a ejecutar
        self.errores_agentes = []  # textos: "línea 10: V al recibir Pedido: ..."
        self.errores_agentes_det = []  # lo mismo como (linea, texto), para decir el archivo
        self.errores_principal = []  # los del programa principal, antes de las pruebas
        self.vivos = []  # las copias nacidas con 'crear'
        self.en_prueba = False
        self.naciendo = 0  # agentes que están calculando su estado inicial
        self.tipos_estado = {}  # (agente, estado) -> tipo con el que arrancó
        self.archivo = None  # el archivo principal, para nombrar los otros en los errores
        self.detalle_pruebas = []  # por cada prueba, [(linea, texto)] de lo que falló
        self.separar_salida = False  # 'probar': lo que muestra cada prueba se guarda aparte
        self.mostrado_pruebas = []  # por cada prueba, los renglones que mostró
        self.llamadas = []  # nombres de las funciones que se están ejecutando
        self.abiertas = 0  # cuántas llamadas a funciones hay sin terminar
        self.ultima_funcion = None  # la última función que se llamó
        self.atendiendo = []  # (agente, renglón de la pregunta) de los que están atendiendo
        self.entrada = por_teclado  # de dónde saca leer() lo que contesta la persona
        self.sin_teclado = False  # en las pruebas leer() usa la respuesta preparada
        self.fecha_fija = False  # en las pruebas hoy() y ahora() dan siempre lo mismo
        self._nativas()

    # ── funciones incorporadas ──
    def _nativas(self):
        def nativa(nombre):
            def deco(fn):
                def envuelta(args):
                    if cantidad_equivocada(nombre, len(args)):
                        raise ErrorMate(cantidad_equivocada(nombre, len(args)))
                    return protegida(nombre, fn, args)
                self.glob.definir(nombre, Nativa(nombre, envuelta), origen="nativa")
                return fn
            return deco

        def protegida(nombre, fn, args):
            """Ninguna función incluida falla con un error de Python."""
            try:
                r = fn(*args)
            except ErrorMate:
                raise
            except MemoryError:
                raise ErrorMate(f"{nombre}(): {SIN_MEMORIA}", clase="limite")
            except (TypeError, ValueError, ArithmeticError, KeyError, IndexError,
                    AttributeError):
                raise ErrorMate(f"{nombre}(): no pude hacer eso con esos valores")
            if type(r) is float and not math.isfinite(r):
                raise ErrorMate(f"{nombre}(): {DEMASIADO_GRANDE}")
            return r

        def pedir(v, tipo, donde):
            if nombre_tipo(v) != tipo:
                raise ErrorMate(f"{donde} espera {tipo} y recibió {tipo_claro(v)}")
            return v

        def no_vacia(l, donde):
            if not l:
                raise ErrorMate(f"{donde} no puede con una lista vacía: no hay de dónde "
                                "elegir. Preguntá antes con largo(lista) > 0")
            return l

        def numeros(l, donde):
            if not all(es_num(x) for x in pedir(l, "lista", donde)):
                raise ErrorMate(f"{donde} espera una lista de números")
            return l

        def posicion_de(n, donde):
            if type(n) is not int or n < 0:
                raise ErrorMate(f"{donde} espera posiciones enteras, de 0 en adelante")
            return n

        nativa("mostrar")(lambda *xs: self.salida(" ".join(
            formato(revisar_peso(a)) for a in xs)))

        @nativa("largo")
        def _(x):
            if isinstance(x, (str, list, dict)):
                return len(x)
            raise ErrorMate(f"largo() no aplica a{'l valor nada' if x is None else ' ' + nombre_tipo(x)}")

        nativa("texto")(a_texto)
        nativa("tipo")(nombre_tipo)

        @nativa("numero")
        def _(x):
            return x if es_num(x) else numero_de_texto(pedir(x, "texto", "numero()"))

        @nativa("tiene")
        def _(col, x):
            if isinstance(col, dict):  # las claves son textos: otra cosa no puede estar
                return isinstance(x, str) and x in col
            if isinstance(col, list):
                return any(igual(x, y) for y in col)
            if isinstance(col, str) and isinstance(x, str):
                return x in col
            if isinstance(col, str):
                raise ErrorMate(
                    f"tiene(): dentro de un texto se busca otro texto, y recibió {un(x)}"
                    + (f". Pasalo a texto: tiene(t, texto({formato(x)}))" if es_num(x) else ""))
            raise ErrorMate("tiene() busca en una lista, un mapa o un texto, y recibió "
                            + un(col))

        nativa("claves")(lambda m: list(pedir(m, "mapa", "claves()")))
        nativa("valores")(lambda m: list(pedir(m, "mapa", "valores()").values()))
        @nativa("agregar")
        def _(l, x):
            if len(pedir(l, "lista", "agregar()")) >= MAX_LARGO:
                raise muy_largo("la lista")
            return l + [x]

        @nativa("quitar")
        def _(col, x):
            if isinstance(col, dict):
                self.clave_de_mapa(x)
                return {k: v for k, v in col.items() if k != x}
            if isinstance(col, list):
                return [y for y in col if not igual(x, y)]
            raise ErrorMate(
                f"quitar() saca de una lista los que valen eso (o de un mapa, esa clave), "
                f"y recibió {un(col)}"
                + (". Para sacar una parte de un texto usá reemplazar(t, parte, \"\")"
                   if isinstance(col, str) else ""))

        @nativa("rango")
        def _(a, b=None, salto=1):
            ini, fin = (0, a) if b is None else (a, b)
            if type(ini) is not int or type(fin) is not int or type(salto) is not int:
                raise ErrorMate("rango() espera números enteros")
            if salto == 0:
                raise ErrorMate("rango(): el salto (el tercer valor) no puede ser 0: "
                                "nunca llegaría")
            numeros_del_rango = range(ini, fin, salto)
            if len(numeros_del_rango) > MAX_LARGO:
                raise ErrorMate("rango(): son demasiados números (el tope es "
                                + f"{MAX_LARGO:,})".replace(",", "."))
            return list(numeros_del_rango)

        nativa("sumar")(lambda l: sum(numeros(l, "sumar()")))

        @nativa("promedio")
        def _(l):
            total, cuantos = sum(no_vacia(numeros(l, "promedio()"), "promedio()")), len(l)
            if type(total) is int and total % cuantos == 0:
                return total // cuantos
            return total / cuantos

        def extremo(nombre, elegir):
            @nativa(nombre)
            def _(l):
                claves = claves_de_orden(no_vacia(pedir(l, "lista", f"{nombre}()"),
                                                  f"{nombre}()"))
                if claves is None:
                    raise ErrorMate(f"{nombre}() espera una lista de números (o toda de "
                                    "textos), sin mezclar")
                return l[elegir(range(len(l)), key=claves.__getitem__)]

        extremo("minimo", min)
        extremo("maximo", max)
        nativa("absoluto")(lambda n: abs(pedir(n, "numero", "absoluto()")))

        @nativa("ultimo")
        def _(col):
            if not isinstance(col, (list, str)):
                raise ErrorMate(f"ultimo() espera una lista o un texto y recibió "
                                f"{tipo_claro(col)}")
            if not col:
                raise ErrorMate("ultimo() no puede con "
                                + ("un texto vacío" if isinstance(col, str) else
                                   "una lista vacía") + ": no tiene ningún elemento")
            return col[-1]

        @nativa("porcion")
        def _(col, desde, hasta=None):
            if not isinstance(col, (list, str)):
                raise ErrorMate(f"porcion() espera una lista o un texto y recibió "
                                f"{tipo_claro(col)}")
            posicion_de(desde, "porcion()")
            hasta = len(col) if hasta is None else posicion_de(hasta, "porcion()")
            if desde > hasta:
                raise ErrorMate(f"porcion(): la posición donde empieza ({desde}) no puede "
                                f"ser mayor que la posición donde termina ({hasta})")
            return col[desde:hasta]  # si 'hasta' se pasa del final, llega hasta el final

        @nativa("obtener")
        def _(m, clave, por_defecto):
            pedir(m, "mapa", "obtener()")
            self.clave_de_mapa(clave)
            return m.get(clave, por_defecto)

        @nativa("ordenar")
        def _(l, campo=None):
            por = pedir(l, "lista", "ordenar()")
            if campo is not None:
                pedir(campo, "texto", "ordenar()")
                por = []
                for x in l:
                    campos = x.campos if isinstance(x, Registro) else x
                    if not isinstance(campos, dict):
                        raise ErrorMate(
                            f'ordenar(lista, "{campo}") espera una lista de mapas o de '
                            f"mensajes, y adentro hay {un(x)}")
                    if campo not in campos:
                        raise ErrorMate(no_esta(
                            f"ordenar(): un elemento de la lista no tiene '{campo}'",
                            campo, campos))
                    por.append(campos[campo])
            claves = claves_de_orden(por)
            if claves is None and campo is not None:
                raise ErrorMate(f"ordenar(): los '{campo}' tienen que ser todos números o "
                                "todos textos, sin mezclar")
            if claves is None:
                try:
                    return sorted(l)
                except TypeError:
                    raise ErrorMate("ordenar() espera elementos comparables entre sí: todos "
                                    "números o todos textos")
            return [l[i] for i in sorted(range(len(l)), key=claves.__getitem__)]

        @nativa("redondear")
        def _(x, n=0):
            pedir(x, "numero", "redondear()")
            if type(n) is not int or n < 0:
                raise ErrorMate("redondear() espera una cantidad entera de decimales, de 0 "
                                "en adelante (no puede ser negativa ni tener coma), "
                                "por ejemplo redondear(3.14159, 2)")
            if not math.isfinite(x):
                raise ErrorMate("redondear() no puede con un número infinito")
            if type(x) is int:
                return x
            r = redondeo(x, n)  # el medio va hacia arriba: redondear(2.5) da 3
            return int(r) if r == r.to_integral_value() else float(r)

        @nativa("pesos")
        def _(n, decimales=2):
            pedir(n, "numero", "pesos()")
            if type(decimales) is not int or not 0 <= decimales <= 6:
                raise ErrorMate("pesos() espera una cantidad de decimales entre 0 y 6, "
                                "por ejemplo pesos(1234.5, 2)")
            if not math.isfinite(n):
                raise ErrorMate("pesos() no puede con un número infinito")
            r = redondeo(n, decimales)
            entero, _, fraccion = format(r.copy_abs(), "f").partition(".")
            texto = "$ " + format(int(entero), ",").replace(",", ".")
            if decimales:
                texto += "," + fraccion.ljust(decimales, "0")
            return ("-" if r < 0 else "") + texto

        @nativa("unir")
        def _(l, sep):
            revisar_peso(pedir(l, "lista", "unir()"))
            minimo = sum(len(x) if isinstance(x, str) else 1 for x in l)
            if minimo + len(l) * len(pedir(sep, "texto", "unir()")) > MAX_LARGO:
                raise muy_largo()
            t = sep.join(formato(x) for x in l)
            if len(t) > MAX_LARGO:
                raise muy_largo()
            return t

        @nativa("partir")
        def _(t, sep):
            pedir(t, "texto", "partir()")
            if pedir(sep, "texto", "partir()") == "":
                return list(t)  # sin separador: letra por letra
            return t.split(sep)

        @nativa("leer")
        def _(pregunta, preparada=None):
            pedir(pregunta, "texto", "leer()")
            if preparada is not None:
                pedir(preparada, "texto", "leer()")
            if self.contexto is not None or self.naciendo:
                raise ErrorMate(
                    "leer() solo se usa desde el programa principal: un agente no puede "
                    "frenar todo esperando el teclado. Leé el dato afuera y mandáselo en "
                    "un mensaje")
            if self.sin_teclado:
                if preparada is None:
                    raise ErrorMate(
                        "en las pruebas leer() no espera el teclado: dale una respuesta "
                        'preparada como segundo valor, por ejemplo leer("¿Cuántos?", "3")')
                return preparada
            try:
                return self.entrada(pregunta).strip()
            except EOFError:
                if preparada is not None:
                    return preparada
                raise ErrorMate("leer(): no hay nadie para contestar (el programa no "
                                "está corriendo en una consola con teclado)")
            except UnicodeError:
                raise ErrorMate("leer(): lo que llegó trae una letra que no pude entender "
                                "(una tilde o una ñ en otra codificación). Si viene de un "
                                "archivo, guardalo como UTF-8")

        def momento():
            return FECHA_DE_PRUEBA if self.fecha_fija else datetime.datetime.now()

        nativa("hoy")(lambda: momento().strftime("%d/%m/%Y"))
        nativa("ahora")(lambda: momento().strftime("%d/%m/%Y %H:%M"))

        def archivo_de_datos(nombre, donde):
            """La ruta completa de un archivo de la carpeta del programa (y solo de ahí)."""
            pedir(nombre, "texto", donde)
            if self.contexto is not None or self.naciendo:
                raise ErrorMate(
                    f"{donde} solo se usa desde el programa principal: un agente no toca "
                    "archivos. Leé o guardá el archivo afuera y pasale los datos en un "
                    "mensaje", familia="archivo")
            carpeta = os.path.realpath(
                os.path.dirname(os.path.abspath(self.archivo)) if self.archivo else os.getcwd())
            ruta = os.path.realpath(os.path.join(carpeta, nombre)) if nombre.strip() else carpeta
            try:
                adentro = os.path.normcase(os.path.commonpath([carpeta, ruta])) \
                    == os.path.normcase(carpeta)
            except ValueError:  # en Windows, si está en otro disco
                adentro = False
            if not nombre.strip():
                raise ErrorMate(f'{donde}: falta el nombre del archivo, por ejemplo "notas.txt"',
                                familia="archivo")
            if not adentro:
                suelto = os.path.basename(nombre.replace("\\", "/").rstrip("/")) or "notas.txt"
                raise ErrorMate(
                    f"{donde} solo trabaja con archivos de la carpeta del programa "
                    f"({carpeta}), y '{nombre}' queda afuera. Copiá el archivo a esa carpeta "
                    f'y nombralo sin la ruta: "{suelto}"', familia="archivo")
            return carpeta, ruta

        @nativa("leer_archivo")
        def _(nombre):
            carpeta, ruta = archivo_de_datos(nombre, "leer_archivo()")
            if os.path.isdir(ruta):
                raise ErrorMate(f"leer_archivo(): '{nombre}' es una carpeta, no un archivo",
                                familia="archivo")
            try:
                contenido = leer_fuente(ruta)
            except FileNotFoundError:
                try:
                    otros = sorted(a for a in os.listdir(os.path.dirname(ruta))
                                   if os.path.isfile(os.path.join(os.path.dirname(ruta), a)))
                except OSError:
                    otros = []
                suelto = os.path.basename(ruta)
                if suelto + ".txt" in otros:  # el Bloc de notas le agregó .txt
                    pista = f" ¿Quisiste decir '{suelto}.txt'?"
                else:
                    pista = sugerir(suelto, otros)
                raise ErrorMate(f"leer_archivo(): no encuentro el archivo '{nombre}' en "
                                f"{os.path.dirname(ruta)}.{pista}".rstrip("."), familia="archivo")
            except OSError:
                raise ErrorMate(f"leer_archivo(): no pude abrir '{nombre}'", familia="archivo")
            except ErrorMate:
                raise ErrorMate(f"leer_archivo(): no pude leer las letras de '{nombre}': "
                                "¿seguro que es un archivo de texto?", familia="archivo")
            if len(contenido) > MAX_LARGO:
                raise ErrorMate(f"leer_archivo(): '{nombre}' es demasiado grande para leerlo "
                                "entero", familia="archivo")
            return contenido

        @nativa("escribir_archivo")
        def _(nombre, contenido):
            carpeta, ruta = archivo_de_datos(nombre, "escribir_archivo()")
            if nombre_tipo(contenido) != "texto":
                raise ErrorMate(
                    f"escribir_archivo() guarda un texto y recibió {tipo_claro(contenido)}. "
                    'Pasalo a texto antes: texto(valor), unir(lista, "\\n") o a_json(valor)')
            # (Windows ignora los puntos y espacios del final, y lo que sigue a un ':')
            if os.path.basename(ruta).split(":")[0].rstrip(". ").lower().endswith(NO_SE_PISAN):
                raise ErrorMate(
                    f"escribir_archivo() no escribe en '{nombre}' para no pisar un programa: "
                    'elegí otro nombre, por ejemplo "notas.txt"', familia="archivo")
            if os.path.isdir(ruta):
                raise ErrorMate(f"escribir_archivo(): '{nombre}' es una carpeta, no un archivo",
                                familia="archivo")
            try:
                contenido.encode("utf-8")  # antes de tocar el archivo: si falla, queda como estaba
            except UnicodeError:
                raise ErrorMate(
                    f"escribir_archivo(): el texto trae una letra que no se puede guardar "
                    f"(un símbolo roto, que suele venir de un JSON). '{nombre}' quedó como "
                    "estaba", familia="archivo")
            try:
                # con la marca del principio, para que el Bloc de notas muestre bien las tildes
                with open(ruta, "w", encoding="utf-8-sig") as f:
                    f.write(contenido)
            except FileNotFoundError:
                raise ErrorMate(f"escribir_archivo(): no existe la carpeta donde iría "
                                f"'{nombre}'. Creala antes, o guardá el archivo al lado del "
                                "programa", familia="archivo")
            except (OSError, UnicodeError):
                raise ErrorMate(f"escribir_archivo(): no pude guardar '{nombre}' (¿está "
                                "abierto en otro programa, o no hay permiso?)",
                                familia="archivo")

        @nativa("recortar")
        def _(t):
            return pedir(t, "texto", "recortar()").strip()

        @nativa("reemplazar")
        def _(t, viejo, nuevo):
            for x in (t, viejo, nuevo):
                pedir(x, "texto", "reemplazar()")
            if viejo == "":
                raise ErrorMate("reemplazar(): el texto a buscar (el segundo valor) no "
                                "puede estar vacío")
            if len(t) + t.count(viejo) * (len(nuevo) - len(viejo)) > MAX_LARGO:
                raise ErrorMate("reemplazar(): el texto quedaría demasiado largo")
            return t.replace(viejo, nuevo)

        nativa("empieza_con")(lambda t, p: pedir(t, "texto", "empieza_con()").startswith(
            pedir(p, "texto", "empieza_con()")))
        nativa("termina_con")(lambda t, p: pedir(t, "texto", "termina_con()").endswith(
            pedir(p, "texto", "termina_con()")))

        nativa("mayusculas")(lambda t: pedir(t, "texto", "mayusculas()").upper())
        nativa("minusculas")(lambda t: pedir(t, "texto", "minusculas()").lower())

        @nativa("a_json")
        def _(v):
            try:
                t = json.dumps(self._a_json(revisar_peso(v, 3)), ensure_ascii=False,
                               allow_nan=False)
            except ValueError:  # inf, nan o un entero de miles de cifras
                raise ErrorMate("ese número no se puede pasar a JSON")
            if len(t) > MAX_LARGO:
                raise muy_largo()
            return t

        def numero_invalido(_):
            raise ErrorMate("el JSON trae un número que no es válido")

        def decimal_de_json(t):
            f = float(t)
            return f if math.isfinite(f) else numero_invalido(t)

        @nativa("de_json")
        def _(t, tipo=None):
            try:
                valor = self._de_json(json.loads(
                    pedir(t, "texto", "de_json()"),
                    parse_constant=numero_invalido, parse_float=decimal_de_json))
            except json.JSONDecodeError as e:
                raise ErrorMate(json_invalido(t, e), familia="json")
            except ValueError:  # un entero de miles de cifras
                numero_invalido(t)
            if tipo is None:
                return valor
            # de_json(texto, "Pedido"): lo que viene de afuera tiene que ser de ese tipo.
            base = pedir(tipo, "texto", "de_json()").rsplit(" de ", 1)[-1]
            if base not in TIPOS_BASE and base not in self.mensajes:
                raise ErrorMate(con_sugerencia(
                    f"de_json(): no existe el tipo '{tipo}'", base,
                    sorted(TIPOS_BASE) + list(self.mensajes)))
            valor = self.amoldar(valor, tipo)  # un mapa suelto con esos campos sirve
            if not self.cumple(valor, tipo):
                raise ErrorMate(f"de_json(): se esperaba {tipo} y el texto trae "
                                f"{self.no_cumple(valor, tipo)}", familia="contrato")
            return valor

        @nativa("a_mapa")
        def _(m):
            if isinstance(m, dict):
                return m  # ya es un mapa
            if not isinstance(m, Registro):
                raise ErrorMate(f"a_mapa() espera un mensaje y recibió {un(m)}")
            return dict(m.campos)

        @nativa("detalle_de")
        def _(e):
            if not isinstance(e, ErrorAtajado):
                raise ErrorMate(
                    "detalle_de() espera el error que ataja 'si falla e', tal cual llegó "
                    f"(sin cambiarle nada), y recibió {un(e)}")
            return dict(e.detalle)

    def _a_json(self, v):
        if isinstance(v, Registro):
            return {"tipo": v.tipo, "campos": {k: self._a_json(x) for k, x in v.campos.items()}}
        if isinstance(v, Agente):
            return {"agente": v.nombre}
        if isinstance(v, list):
            return [self._a_json(x) for x in v]
        if isinstance(v, dict):
            return {k: self._a_json(x) for k, x in v.items()}
        if isinstance(v, (Funcion, Nativa)):
            raise ErrorMate("una función no se puede pasar a JSON")
        return v

    def amoldar(self, valor, tipo):
        """Lo que llegó de afuera, con los mensajes que pide el contrato ya armados: donde
        se espera un Pedido y hay un mapa con sus campos, queda el Pedido (también
        adentro de una lista o de otro mensaje)."""
        if tipo.startswith("lista de ") and isinstance(valor, list):
            return [self.amoldar(x, tipo[len("lista de "):]) for x in valor]
        if tipo in self.mensajes and isinstance(valor, dict):
            tipos = {campo: t for campo, t, _ in self.mensajes[tipo]}
            return self.construir(tipo, {
                k: self.amoldar(v, tipos[k]) if k in tipos else v for k, v in valor.items()})
        return valor

    def _de_json(self, v):
        if isinstance(v, list):
            return [self._de_json(x) for x in v]
        if isinstance(v, dict):
            if set(v) == {"tipo", "campos"} and isinstance(v["tipo"], str) \
                    and v["tipo"] in self.mensajes and isinstance(v["campos"], dict):
                return self.construir(
                    v["tipo"], {k: self._de_json(x) for k, x in v["campos"].items()})
            if set(v) == {"agente"} and isinstance(v["agente"], str):
                # un agente declarado o una copia: los nombres no se repiten
                ag = self.agentes.get(v["agente"]) or next(
                    (a for a in self.vivos if a.nombre == v["agente"]), None)
                if ag is not None:
                    return ag
            return {k: self._de_json(x) for k, x in v.items()}
        return v

    # ── mensajes ──
    def cumple(self, valor, tipo):
        if tipo == "cualquiera":
            return True
        if tipo.startswith("lista de "):
            return isinstance(valor, list) and all(
                self.cumple(x, tipo[len("lista de "):]) for x in valor)
        return nombre_tipo(valor) == tipo

    def no_cumple(self, valor, tipo):
        """Qué recibió, dicho para un error: 'texto', o qué hay de más adentro de la lista."""
        if tipo.startswith("lista de ") and isinstance(valor, list):
            de = tipo[len("lista de "):]
            i = next(i for i, x in enumerate(valor) if not self.cumple(x, de))
            return f"una lista que en la posición {i} tiene {un(valor[i])}"
        return tipo_claro(valor)

    def construir(self, nombre, dados):
        try:
            return self._construir(nombre, dados)
        except ErrorMate as e:
            e.familia = "contrato"
            raise

    def _construir(self, nombre, dados):
        if nombre not in self.mensajes:
            raise ErrorMate(con_sugerencia(
                f"no existe el mensaje '{nombre}'", nombre, self.mensajes))
        campos = {}
        for campo, tipo, opcional in self.mensajes[nombre]:
            if campo not in dados:
                if not opcional:
                    raise ErrorMate(f"a {nombre} le falta el campo '{campo}'")
                campos[campo] = None
                continue
            v = dados[campo]
            if lleva_funcion(v):
                raise ErrorMate("los mensajes llevan datos, no funciones "
                                f"(campo '{campo}' de {nombre})")
            if not (self.cumple(v, tipo) or (opcional and v is None)):
                raise ErrorMate(
                    f"{nombre}.{campo} es de tipo {tipo} y recibió {self.no_cumple(v, tipo)}")
            campos[campo] = v
        for k in dados:
            if k not in campos:
                raise ErrorMate(con_sugerencia(f"{nombre} no tiene un campo '{k}'", k, campos))
        return Registro(nombre, campos)

    # ── carga del programa ──
    def cargar(self, programa):
        for s in programa:
            if s[0] == "mensaje":
                self.mensajes[s[2]] = s[3]
                if s[4]:
                    self.responde[s[2]] = s[4]
        for s in programa:
            try:
                if s[0] == "funcion":
                    self.glob.definir(s[2], Funcion(s[2], s[3], s[4], self.glob),
                                      origen="funcion", linea=s[1])
                elif s[0] == "agente":
                    ag = Agente(s[2])
                    ag.decl = s
                    ag.manejadores = self.manejadores_de(s)
                    self.agentes[s[2]] = ag
                    self.decl_agentes.append(s)
                    self.glob.definir(s[2], ag, origen="agente")
            except ErrorMate as e:
                e.linea = e.linea or s[1]
                raise

    def manejadores_de(self, decl):
        """Qué mensajes entiende un agente: queda fijo desde la declaración."""
        return {tipo: (ln, var, cuerpo) for ln, tipo, var, cuerpo in decl[4]}

    def instanciar(self, ag, dados=None, linea=None):
        """Deja al agente recién nacido: estado inicial (o el que le den) y sin pendientes."""
        s, dados = ag.decl, dados or {}
        env = Entorno(self.glob, frontera=True)
        for f in s[5]:
            env.definir(f[2], Funcion(f[2], f[3], f[4], env), origen="funcion")
        # Mientras nace no se le entregan mensajes: todavía no tiene todo su estado.
        self.naciendo += 1
        ag.ocupado = True  # si alguien le habla mientras nace, es un ciclo
        try:
            for ln, nombre, e in s[3]:
                try:
                    env.definir(nombre, self.estado_inicial(s[2], nombre, e, env, dados, linea),
                                mutable=True)
                except ErrorMate as err:
                    err.linea = err.linea or ln
                    raise
        finally:
            self.naciendo -= 1
            ag.ocupado = False
        ag.env = env
        ag.manejadores = self.manejadores_de(s)
        if ag.inicial is None:
            ag.inicial = self.copia_de(env)

    def estado_inicial(self, agente, nombre, e, env, dados, linea):
        """El valor con que arranca un estado: el que le dieron a 'crear' o el declarado.
        Si se lo dieron, lo declarado no se calcula (no repite lo que muestre o cree)."""
        if nombre not in dados:
            valor = self.ev(e, env)
            if valor is not None:
                self.tipos_estado.setdefault((agente, nombre), nombre_tipo(valor))
            return valor
        valor = dados[nombre]
        declarado = self.tipos_estado.get((agente, nombre)) or _LITERALES.get(e[0])
        # 'nada' siempre vale: "sin tope", "sin cliente todavía"
        if valor is not None and declarado and declarado != nombre_tipo(valor):
            raise ErrorMate(f"{agente}.{nombre} arranca como {declarado} y le diste "
                            f"{nombre_tipo(valor)}", linea)
        return valor

    @staticmethod
    def copia_de(env):
        return {k: list(v) for k, v in env.vars.items()}, dict(env.origen)

    @staticmethod
    def restaurar(env, guardado):
        env.vars = {k: list(v) for k, v in guardado[0].items()}
        env.origen = dict(guardado[1])

    def reiniciar_agentes(self):
        """Los agentes declarados vuelven al estado con el que nacieron."""
        for s in self.decl_agentes:
            ag = self.agentes[s[2]]
            if ag.inicial is None:
                self.instanciar(ag)
            else:
                self.restaurar(ag.env, ag.inicial)
                ag.ocupado = False
                ag.manejadores = self.manejadores_de(s)  # sin lo que se haya simulado
        self.cola.clear()

    def entornos_vivos(self):
        """Todos los lugares donde quedó guardada una variable: lo de afuera, los agentes
        y lo que recuerdan las funciones hechas por otras funciones."""
        vistos, pendientes = {}, [self.glob]
        pendientes += [ag.env for ag in list(self.agentes.values()) + self.vivos if ag.env]

        def mirar(v):
            if isinstance(v, Funcion):
                pendientes.append(v.env)
            elif isinstance(v, Agente):
                if v.env:
                    pendientes.append(v.env)
            elif isinstance(v, list):
                for x in v:
                    mirar(x)
            elif isinstance(v, dict):
                for x in v.values():
                    mirar(x)
            elif isinstance(v, Registro):
                for x in v.campos.values():
                    mirar(x)

        while pendientes:
            env = pendientes.pop()
            while env is not None and id(env) not in vistos:
                vistos[id(env)] = env
                for valor, _ in list(env.vars.values()):
                    mirar(valor)
                env = env.padre
        return list(vistos.values())

    def foto(self):
        """Cómo quedó el mundo al terminar el programa: las variables de afuera, las copias
        y lo que guardan las funciones."""
        return ([(env, self.copia_de(env)) for env in self.entornos_vivos()],
                list(self.vivos), dict(self.copias))

    def volver_a(self, foto):
        """Cada prueba empieza limpia: todo como en la foto, y los agentes declarados
        como recién nacidos."""
        for env, guardado in foto[0]:
            self.restaurar(env, guardado)
        self.vivos = list(foto[1])
        for ag in self.vivos:
            ag.ocupado = False
            ag.manejadores = self.manejadores_de(ag.decl)
        self.copias = dict(foto[2])
        self.reiniciar_agentes()

    def crear(self, n, env):
        if n[2] not in self.agentes:
            raise ErrorMate(con_sugerencia(
                f"no existe el agente '{n[2]}'", n[2], self.agentes))
        molde = self.agentes[n[2]]
        declarados = {nombre for _, nombre, _ in molde.decl[3]}
        dados = {}
        for k, e in n[4]:
            if k not in declarados:
                raise ErrorMate(f"{n[2]} no tiene un estado '{k}'")
            dados[k] = self.ev(e, env)
        apodo = None if n[3] is None else self.ev(n[3], env)
        if n[3] is not None and not isinstance(apodo, str):
            raise ErrorMate(
                "el nombre de la copia (después de 'llamado') tiene que ser un texto, y "
                f"recibió {un(apodo)}"
                + ('. Pasalo a texto: llamado "Sucursal {numero}"' if es_num(apodo) else ""),
                n[1])
        if apodo is not None and not apodo.strip():
            raise ErrorMate("el nombre de la copia (después de 'llamado') no puede estar "
                            "vacío", n[1])
        if apodo is not None and any(a.nombre == f"{n[2]} {apodo}" for a in self.vivos):
            raise ErrorMate(
                f'ya hay un {n[2]} llamado "{apodo}": dos copias no pueden llamarse igual, '
                "porque no se las podría distinguir. Elegí otro nombre", n[1])
        ag = Agente(f"{n[2]} {apodo}" if apodo is not None else f"{n[2]} nuevo")
        ag.decl = molde.decl
        self.instanciar(ag, dados, n[1])
        # Recién ahora gasta un número: un 'crear' rechazado no corre la numeración.
        self.copias[n[2]] = self.copias.get(n[2], 1) + 1
        if apodo is None:
            ag.nombre = f"{n[2]}#{self.copias[n[2]]}"
        ag.creador = self.contexto[0] if self.contexto else None
        self.vivos.append(ag)
        return ag

    def correr(self, programa, pruebas=False):
        """Ejecuta el programa. Con pruebas=True devuelve [(nombre, error|None)]."""
        # El análisis ya rechaza 'devolver' y 'responder' fuera de lugar; esto es la red.
        tope = sys.getrecursionlimit()
        try:
            if NIVELES_DE_PYTHON > tope:
                sys.setrecursionlimit(NIVELES_DE_PYTHON)
            return self._correr(programa, pruebas)
        except _Retorno:
            raise ErrorMate(DEVOLVER_SUELTO, self.linea_actual)
        except _Respuesta:
            raise ErrorMate(RESPONDER_SUELTO, self.linea_actual)
        except (_Romper, _Continuar):
            raise ErrorMate("'romper' y 'continuar' solo van dentro de un 'mientras' o de "
                            "un 'para'", self.linea_actual)
        finally:
            sys.setrecursionlimit(tope)

    def demasiada_recursion(self, nombre, linea=None):
        """El error de una función que se llama a sí misma sin parar."""
        if nombre is None:
            return ErrorMate("demasiada recursión: hay demasiadas cosas una adentro de la "
                             "otra", linea, clase="limite")
        return ErrorMate(
            "demasiada recursión: hay demasiadas llamadas a funciones sin terminar, una "
            f"adentro de la otra (la última, a {nombre}()). Si {nombre}() se llama a sí "
            "misma, revisá que tenga un 'si' que la frene y que cada llamada se acerque a "
            "ese final", linea, clase="limite")

    def _correr(self, programa, pruebas):
        self.sin_teclado = self.sin_teclado or pruebas
        self.fecha_fija = self.fecha_fija or pruebas
        self.cargar(programa)
        for s in programa:
            if s[0] == "agente":
                # El estado inicial se calcula donde está declarado el agente,
                # salvo que alguien le haya hablado antes.
                if self.agentes[s[2]].env is None:
                    self.instanciar(self.agentes[s[2]])
            elif s[0] not in ("mensaje", "funcion", "prueba"):
                self.ejecutar(s, self.glob)
        self.vaciar_cola()
        if not pruebas:
            return []
        self.errores_principal = list(self.errores_agentes_det)
        foto = self.foto()
        resultados = []
        self.en_prueba = True
        try:
            for s in programa:
                if s[0] != "prueba":
                    continue
                self.volver_a(foto)
                self.errores_agentes, self.errores_agentes_det = [], []
                self.pasos = 0
                self.entregados = 0
                fallas, mostrado, salida = [], [], self.salida
                if self.separar_salida:
                    self.salida = mostrado.append
                try:
                    self.bloque(s[3], Entorno(self.glob, borde=True), nuevo=False)
                    self.vaciar_cola()
                except ErrorMate as e:
                    fallas.append((e.linea, self.con_camino(e.mensaje, e)))
                finally:
                    self.salida = salida
                self.mostrado_pruebas.append(mostrado)
                # Además de lo que cortó la prueba, lo que falló en los agentes: suele
                # ser la causa.
                fallas += self.errores_agentes_det
                self.detalle_pruebas.append(fallas)
                resultados.append((s[2], "\n".join(
                    self.con_lugar(linea, texto) for linea, texto in fallas) or None))
        finally:
            self.en_prueba = False
        return resultados

    def donde(self, linea):
        """'línea 7', o 'lib.mate, línea 7' si el renglón es de un archivo traído con usar."""
        archivo = getattr(linea, "archivo", None)
        if archivo and self.archivo and archivo != self.archivo:
            return f"{os.path.basename(archivo)}, línea {linea}"
        return f"línea {linea}"

    def con_lugar(self, linea, texto):
        """Todos los errores se escriben igual, con el renglón adelante: 'línea 7: ...'."""
        return f"{self.donde(linea)}: {texto}" if linea else texto

    # ── agentes ──
    def vaciar_cola(self):
        while self.cola:
            rem, dest, msg = self.cola.popleft()
            try:
                self.entregar(rem, dest, msg, pregunta=False)
            except ErrorMate as e:
                if e.clase == "limite":  # el freno corta todo el programa, no un solo mensaje
                    raise
                if rem is not None and msg.tipo != AL_FALLAR and AL_FALLAR in rem.manejadores:
                    # El que lo envió pidió enterarse: el aviso le llega como un mensaje
                    # más, y la falla queda en sus manos (no se anota como error).
                    self.cola.append((dest, rem, Registro(AL_FALLAR, {
                        "motivo": e.mensaje, "mensaje": msg, "destino": dest})))
                    continue
                que = "en 'al fallar'" if msg.tipo == AL_FALLAR else f"al recibir {msg.tipo}"
                linea = e.linea or getattr(e, "renglon", None)
                texto = self.con_camino(f"{dest.nombre} {que}: {e.mensaje}", e)
                self.errores_agentes.append(self.con_lugar(linea, texto))
                self.errores_agentes_det.append((linea, texto))

    def ciclo(self, dest, linea):
        """El error de un ciclo de preguntas, con la cadena: A → B → A."""
        fin = f"{dest.nombre} todavía está atendiendo otro mensaje"
        desde = next((i for i, a in enumerate(self.atendiendo) if a[0] is dest), None)
        if desde is None:
            return ErrorMate(f"ciclo de preguntas: {fin}", familia="ciclo")
        cadena = self.atendiendo[desde:] + [(dest, linea)]
        pasos = []
        for (quien, _), (a_quien, renglon) in zip(cadena, cadena[1:]):
            en = f" ({self.donde(renglon)})" if renglon else ""
            pasos.append(f"{quien.nombre} le preguntó a {a_quien.nombre}{en}")
        flecha = simbolo(" → ", " -> ")
        return ErrorMate(f"ciclo de preguntas: {flecha.join(a.nombre for a, _ in cadena)}. "
                         f"{', '.join(pasos)}, y {fin}", familia="ciclo")

    def camino(self, e):
        """Por dónde se llegó al error: '' o un renglón como "cómo se llegó: en precio(),
        llamada desde total() (línea 4), llamada desde la línea 9"."""
        partes, pendiente = [], None  # pendiente: el renglón desde donde se llamó a la última
        for paso in e.camino:
            if paso[0] == "funcion":
                partes.append(f"en {paso[1]}()" if pendiente is None else
                              f"llamada desde {paso[1]}() ({self.donde(pendiente)})")
                pendiente = paso[2] or 0
            else:
                if pendiente:
                    partes.append(f"llamada desde la {self.donde(pendiente)}")
                pendiente = None
                en = f" ({self.donde(paso[3])})" if paso[3] else ""
                partes.append(f"se lo preguntó {paso[2] or 'el programa'} a {paso[1]}{en}")
        if pendiente:
            partes.append(f"llamada desde la {self.donde(pendiente)}")
        if len(partes) > 7:  # una función que se llama a sí misma muchas veces
            partes = partes[:4] + ["..."] + partes[-2:]
        return "cómo se llegó: " + ", ".join(partes) if partes else ""

    def con_camino(self, texto, e):
        camino = self.camino(e)
        return f"{texto}\n{camino}" if camino else texto

    def entregar(self, rem, dest, msg, pregunta, linea=None):
        self.entregados += 1
        if self.entregados > MAX_MENSAJES:
            raise ErrorMate(
                f"se superaron {MAX_MENSAJES} mensajes: ¿los agentes entraron en bucle?",
                clase="limite")
        aviso = msg.tipo == AL_FALLAR  # no es un mensaje: es el aviso de que uno falló
        # En la traza cada mensaje lleva su número, y lo que pasa mientras un agente
        # atiende (lo que él pregunta) va con sangría debajo.
        numero, hondo = None, len(self.atendiendo)
        if not aviso:
            self.cuenta["preguntar" if pregunta else "enviar"] += 1
            numero = self.cuenta["preguntar"] + self.cuenta["enviar"]
        de = rem.nombre if rem else "(programa)"
        if self.traza and aviso:
            self.trazar(f"{dest.nombre} se entera de que {rem.nombre} no pudo atender "
                        f"{msg.campos['mensaje'].tipo}: {msg.campos['motivo']}", None, hondo)
        elif self.traza:
            flecha = "pregunta a" if pregunta else "→"
            self.trazar(f"{de} {flecha} {dest.nombre}: {formato(msg)}", numero, hondo)
        try:
            respondio, valor = self.atender(rem, dest, msg, pregunta, linea)
        except ErrorMate as e:
            self.cuenta["fallaron"] += 1
            if self.traza and getattr(e, "sin_respuesta", None) is dest:
                self.trazar(f"{dest.nombre} sin respuesta: terminó de atender {msg.tipo} sin "
                            "llegar a un 'responder'", numero, hondo)
            elif self.traza:
                donde = " en su 'al fallar'" if aviso else ""
                self.trazar(f"{dest.nombre} falló{donde}: {e.mensaje}", numero, hondo)
            raise
        if pregunta:
            if self.traza:
                self.trazar(f"{dest.nombre} responde a {de}: {formato(valor, False)}",
                            numero, hondo)
            return valor
        if respondio and rem is not None:
            self.cola.append((dest, rem, valor))
        elif respondio and self.traza:
            # Lo mandó el programa con 'enviar': no hay quién reciba la respuesta.
            self.trazar(f"la respuesta de {dest.nombre} se descartó (para recibirla, usá "
                        f"'preguntar' en vez de 'enviar'): {formato(valor, False)}",
                        numero, hondo)
        return None

    def trazar(self, texto, numero=None, hondo=0):
        """Un renglón de la traza: '  ·  3.    Vendedor responde a Comprador: ...'."""
        marca = f"{numero:>2}." if numero is not None else "   "
        (self.anotar or self.salida)(f"  · {marca} {'   ' * hondo}{texto}")

    def atender(self, rem, dest, msg, pregunta, linea):
        """El agente atiende el mensaje. Devuelve (si respondió, qué respondió)."""
        aviso = msg.tipo == AL_FALLAR
        if msg.tipo not in dest.manejadores:
            raise ErrorMate(f"{dest.nombre} no sabe recibir '{msg.tipo}'", familia="agente")
        if dest.ocupado and dest.env is None:
            raise ErrorMate(f"{dest.nombre} todavía está armando su estado inicial y no "
                            "puede recibir mensajes")
        if dest.ocupado:
            raise self.ciclo(dest, linea)
        if dest.env is None:
            self.instanciar(dest)
        # Un 'al recibir' simulado en una prueba corre con las variables de esa prueba
        # a la vista (no con el estado del agente).
        renglon, var, cuerpo, *de_la_prueba = dest.manejadores[msg.tipo]
        env = Entorno(de_la_prueba[0] if de_la_prueba else dest.env, borde=True)
        if var:  # (el aviso de 'al fallar' llega como un mapa común)
            env.definir(var, dict(msg.campos) if aviso else msg, origen="mensaje")
        previo, dest.ocupado = self.contexto, True
        self.contexto = (dest, rem, msg.tipo, env.serie)
        respondio, valor = False, None
        # Si falla, el agente vuelve a como estaba antes de recibir este mensaje.
        estado_previo = {k: list(v) for k, v in dest.env.vars.items()}
        en_cola, llamadas, nacidos = len(self.cola), self.llamadas, len(self.vivos)
        self.llamadas = []
        self.atendiendo.append((dest, linea))
        try:
            try:
                self.bloque(cuerpo, env, nuevo=False)
            except _Respuesta as r:
                respondio, valor, renglon_respuesta = True, r.valor, r.linea
            except _Retorno:
                pass
            if aviso and respondio:
                raise ErrorMate(SIN_A_QUIEN, renglon_respuesta)
            # Responder mal (o no responder) también es una falla del que atiende.
            esperado = self.responde.get(msg.tipo)
            if respondio and esperado and not self.cumple(valor, esperado):
                raise ErrorMate(
                    f"{dest.nombre} respondió {self.no_cumple(valor, esperado)} a "
                    f"'{msg.tipo}', y el contrato dice que a {msg.tipo} se le responde "
                    f"{esperado}", renglon_respuesta, familia="contrato")
            if pregunta and not respondio:
                mudo = ErrorMate(f"{dest.nombre} no respondió a '{msg.tipo}': el 'al recibir' "
                                 "terminó sin llegar a un 'responder'", familia="agente")
                mudo.sin_respuesta = dest  # (para la traza: no falló, se quedó callado)
                raise mudo
            if not pregunta and respondio and rem is not None:
                # (si lo mandó el programa, no hay a quién contestar)
                if not isinstance(valor, Registro):
                    raise ErrorMate("a un 'enviar' solo se le responde con un mensaje",
                                    renglon_respuesta)
                if valor.tipo not in rem.manejadores:
                    raise ErrorMate(
                        f"{dest.nombre} respondió {valor.tipo} a {rem.nombre}, pero "
                        f"{rem.nombre} no tiene 'al recibir {valor.tipo}'", renglon_respuesta)
        except ErrorMate as e:
            if pregunta:
                anotar_paso(e, ("pregunta", dest.nombre, rem.nombre if rem else None, linea))
            if not e.linea and not pregunta:
                e.renglon = renglon  # para señalar al menos el 'al recibir' que atendía
            dest.env.vars = estado_previo
            # Las copias que creó atendiendo este mensaje tampoco quedan: nadie las tiene.
            self.vivos[nacidos:] = [a for a in self.vivos[nacidos:] if a.creador is not dest]
            nuevos = [self.cola.pop() for _ in range(len(self.cola) - en_cola)]
            self.cola.extend(m for m in reversed(nuevos) if m[0] is not dest)
            if e.clase == "asegurar":  # para quien le habló es una falla como cualquiera
                e.clase = "falla"
            raise
        finally:
            self.contexto, dest.ocupado, self.llamadas = previo, False, llamadas
            self.atendiendo.pop()
        return respondio, valor

    def destino(self, nodo, env):
        dest = self.ev(nodo, env)
        if not isinstance(dest, Agente):
            pista = ""
            if isinstance(dest, list):
                pista = (". Se le pregunta a un agente por vez: recorré la lista con "
                         "'para agente en lista { ... }'")
            raise ErrorMate(f"el destino tiene que ser un agente, no {tipo_claro(dest)}"
                            + pista)
        return dest

    def destinos(self, nodo, env):
        """A quiénes va un 'enviar': un agente, o una lista de agentes."""
        dest = self.ev(nodo, env)
        if isinstance(dest, Agente):
            return [dest]
        if not isinstance(dest, list):
            raise ErrorMate("el destino tiene que ser un agente o una lista de agentes, no "
                            + tipo_claro(dest))
        for i, x in enumerate(dest):
            if not isinstance(x, Agente):
                raise ErrorMate("en una lista de destinos tienen que ser todos agentes, y "
                                f"en la posición {i} hay {un(x)}")
        return dest

    def un_mensaje(self, nodo, env):
        msg = self.ev(nodo, env)
        if not isinstance(msg, Registro):
            raise ErrorMate(f"solo se envían mensajes declarados, no {tipo_claro(msg)}")
        return msg

    # ── sentencias ──
    def bloque(self, cuerpo, env, nuevo=True):
        if nuevo:
            env = Entorno(env)
        for s in cuerpo:
            self.ejecutar(s, env)

    def condicion(self, nodo, env):
        v = self.ev(nodo, env)
        if type(v) is not bool:
            raise ErrorMate("la condición tiene que ser verdadero o falso, no "
                            + tipo_claro(v))
        return v

    def contar_paso(self, linea):
        """El freno para los programas que nunca terminan."""
        self.pasos += 1
        if self.max_pasos is not None and self.pasos > self.max_pasos:
            tope = f"{self.max_pasos:,}".replace(",", ".")
            tope += " de pasos" if self.max_pasos % 1_000_000 == 0 else " pasos"
            quien = (f"{self.contexto[0].nombre} atendiendo {self.contexto[2]}: "
                     if self.contexto else "")
            raise ErrorMate(
                f"{quien}el programa lleva más de {tope}: ¿quedó en un bucle que nunca "
                "termina? Si es un 'mientras', revisá que su condición cambie adentro. Si "
                "el programa es largo de verdad, corrélo con --sin-limite",
                linea, clase="limite")

    def ejecutar(self, s, env, vale_suelto=False):
        self.linea_actual = s[1]
        self.contar_paso(s[1])
        try:
            if vale_suelto and s[0] == "expr":
                self.ev(s[2], env)
            else:
                self._ejecutar(s, env)
        except ErrorMate as e:
            e.linea = e.linea or s[1]
            raise
        except RecursionError:
            raise self.demasiada_recursion(self.recursiva(), s[1])
        except MemoryError:
            raise ErrorMate(SIN_MEMORIA, s[1], clase="limite")

    def _ejecutar(self, s, env):
        clase = s[0]
        if clase == "expr":
            self.suelta(s[2], env)
        elif clase == "sea":
            valor = self.ev(s[3], env)
            if s[2] not in env.vars:  # (si está en este mismo bloque, lo dice definir)
                env.no_tapar(s[2])
            env.definir(s[2], valor, mutable=s[4], linea=s[1])
        elif clase == "asignar":
            self.asignar(s[2], self.ev(s[3], env), env)
        elif clase == "si":
            for cond, cuerpo in s[2]:
                if self.condicion(cond, env):
                    self.bloque(cuerpo, env)
                    return
            if s[3] is not None:
                self.bloque(s[3], env)
        elif clase == "mientras":
            while self.condicion(s[2], env):
                self.contar_paso(s[1])  # una vuelta cuenta aunque el cuerpo esté vacío
                try:
                    self.bloque(s[3], env)
                except _Continuar:
                    pass
                except _Romper:
                    break
        elif clase in ("para", "para2"):
            # 'para2' es "para posicion, item en lista" (o "para clave, valor en mapa")
            nombres = (s[2],) if clase == "para" else (s[2], s[3])
            col = self.ev(s[-2], env)
            if not isinstance(col, (list, dict, str)):
                raise ErrorMate(f"no se puede recorrer {tipo_claro(col)}: 'para' recorre "
                                "listas, mapas y textos")
            if clase == "para":
                vueltas = [(x,) for x in col]
            else:
                vueltas = list(col.items() if isinstance(col, dict) else enumerate(col))
            for valores in vueltas:
                self.contar_paso(s[1])
                paso = Entorno(env)
                for nombre, x in zip(nombres, valores):
                    paso.definir(nombre, x, origen="para")
                try:
                    self.bloque(s[-1], paso, nuevo=False)
                except _Continuar:
                    pass
                except _Romper:
                    break
        elif clase == "romper":
            raise _Romper()
        elif clase == "continuar":
            raise _Continuar()
        elif clase == "funcion":
            env.definir(s[2], Funcion(s[2], s[3], s[4], env), origen="funcion")
        elif clase == "devolver":
            raise _Retorno(None if s[2] is None else self.ev(s[2], env))
        elif clase == "enviar":
            msg = self.un_mensaje(s[2], env)
            destinos = self.destinos(s[3], env)
            for dest in destinos:  # primero se revisan todos: sale para todos o para nadie
                if msg.tipo not in dest.manejadores:
                    raise ErrorMate(f"{dest.nombre} no sabe recibir '{msg.tipo}'", s[1],
                                    familia="agente")
            for dest in destinos:
                self.cola.append((self.contexto[0] if self.contexto else None, dest, msg))
        elif clase == "responder":
            if not self.contexto:
                raise ErrorMate(RESPONDER_SUELTO)
            valor = self.ev(s[2], env)
            if lleva_funcion(valor):
                raise ErrorMate("no se puede responder con una función: "
                                "las respuestas llevan datos", s[1])
            raise _Respuesta(valor, s[1])
        elif clase == "fallar":
            motivo = self.ev(s[2], env)
            raise ErrorMate(formato(motivo), s[1], familia="fallar",
                            dato=None if lleva_funcion(motivo) else motivo)
        elif clase == "intentar":
            try:
                self.bloque(s[2], env)
            except ErrorMate as e:
                # El freno no se ataja nunca, ni un renglón mal escrito. Un 'asegurar'
                # tampoco dentro de una prueba (si no, pasaría en verde); al correr el
                # programa es una falla más.
                if e.clase in ("limite", "escritura") or (
                        e.clase == "asegurar" and self.en_prueba):
                    raise
                manejo = Entorno(env)
                if s[3]:
                    manejo.definir(s[3], ErrorAtajado(e), origen="falla")
                self.bloque(s[4], manejo, nuevo=False)
        elif clase == "asegurar":
            cond, valores = s[2], ""
            if self.contexto is None and self.en_prueba:
                self.vaciar_cola()  # lo enviado en la prueba llega antes de asegurar
            if cond[0] == "bin" and cond[2] in COMPARADORES:
                # Se evalúa cada lado una sola vez, para poder mostrar qué dio.
                izq, der = self.ev(cond[3], env), self.ev(cond[4], env)
                try:
                    cumple = self.binaria(cond[2], izq, der)
                except ErrorMate as e:
                    e.linea = e.linea or cond[1]
                    raise
                if not cumple:
                    valores = self.valores_de(cond[2], izq, der)
            else:
                cumple = self.condicion(cond, env)
            if not cumple:
                if s[3]:
                    detalle = formato(self.ev(s[3], env)) + (f" ({valores})" if valores else "")
                else:
                    detalle = "no se cumplió lo asegurado" + (f": {valores}" if valores else "")
                raise ErrorMate(detalle, s[1], clase="asegurar")
        elif clase == "simular":
            if not self.en_prueba or self.contexto is not None:
                raise ErrorMate("'simular' solo va dentro de una prueba")
            dest = self.destino(s[2], env)
            if s[3] not in dest.manejadores:
                raise ErrorMate(f"{dest.nombre} no sabe recibir '{s[3]}': solo se simula un "
                                "mensaje que el agente ya recibe", familia="agente")
            dest.manejadores = {**dest.manejadores, s[3]: (s[1], s[4], s[5], env)}
        elif clase == "asegurar_falla":
            if self.contexto is None and self.en_prueba:
                self.vaciar_cola()
            try:
                adentro = Entorno(env)
                for x in s[2]:
                    # Acá una cuenta o una función suelta vale: se prueba que falle.
                    self.ejecutar(x, adentro, vale_suelto=True)
            except ErrorMate as e:
                # Igual que 'intentar': ni el freno, ni un renglón mal escrito, ni un
                # 'asegurar' de la prueba cuentan.
                if e.clase in ("limite", "escritura") or (
                        e.clase == "asegurar" and self.en_prueba):
                    raise
                if e.familia == "nombre":  # un nombre mal tipeado no es la falla esperada
                    raise ErrorMate(
                        f"lo de adentro de 'asegurar falla' no llegó a probarse: {e.mensaje}",
                        e.linea or s[1], clase="asegurar")
                return
            raise ErrorMate(formato(self.ev(s[3], env)) if s[3] else
                            "se esperaba que esto fallara, y no falló", s[1], clase="asegurar")
        else:
            raise ErrorMate(f"'{clase}' no puede ir acá")

    def suelta(self, e, env):
        """Un renglón que es solo un valor: vale si hace algo (llamar a una función
        propia, mostrar, preguntar, crear). Si solo calcula y no lo usa, es un error."""
        if e[0] in ("preguntar", "crear"):
            self.ev(e, env)
            return
        if e[0] != "llamar":
            valor = self.ev(e, env)
            if isinstance(valor, (Funcion, Nativa)):
                raise ErrorMate(f"a '{valor.nombre}' le faltan los paréntesis: "
                                f"{valor.nombre}(...)", e[1], clase="escritura")
            raise renglon_sin_uso(e)
        f = self.ev(e[2], env)
        try:
            self.llamar(f, [self.ev(a, env) for a in e[3]], e[1])
        except ErrorMate as error:
            error.linea = error.linea or e[1]
            raise
        if isinstance(f, Nativa) and f.nombre not in HACEN_ALGO:
            if f.nombre in ("agregar", "quitar"):
                raise ErrorMate(
                    f"{f.nombre}() no cambia la lista: devuelve una nueva. Guardá el "
                    f"resultado: lista = {f.nombre}(lista, ...)", e[1], clase="escritura")
            raise ErrorMate(f"{f.nombre}() devuelve un valor y este renglón no lo usa: "
                            f"guardalo (sea x = {f.nombre}(...)) o mostralo con mostrar(...)",
                            e[1], clase="escritura")

    def valores_de(self, op, izq, der):
        """Qué dio cada lado de un 'asegurar' que no se cumplió."""
        a, b = formato(izq, False), formato(der, False)
        if op != "==":
            return f"{a} {op} {b} es falso"
        if a != b:
            return f"dio {a} y se esperaba {b}"
        # Se ven iguales pero no lo son: el resto minúsculo de las cuentas con decimales.
        if type(izq) is float:
            a = repr(izq)
        if type(der) is float:
            b = repr(der)
        return (f"dio {a} y se esperaba {b}: se muestran igual, pero las cuentas con "
                "decimales dejan un resto minúsculo. Redondeá antes de comparar, por "
                "ejemplo redondear(a, 2) == redondear(b, 2)")

    def asignar(self, destino, valor, env):
        """Asignación con semántica de valor: cambiar m.a.b reconstruye m."""
        clase = destino[0]
        if clase == "nombre":
            if self.contexto is not None:
                self.cuidar_lo_de_afuera(destino[2], env)
            env.asignar(destino[2], valor)
            return
        if clase not in ("indice", "campo"):
            raise ErrorMate(NO_ASIGNABLE)
        base = self.ev(destino[2], env)
        if clase == "indice":
            clave = self.ev(destino[3], env)
            if isinstance(base, list):
                self.posicion(base, clave, al_asignar=True)
                nueva = list(base)
                nueva[clave] = valor
            elif isinstance(base, dict):
                self.clave_de_mapa(clave)
                nueva = {**base, clave: valor}
            else:
                raise ErrorMate(f"no se puede asignar por índice en {tipo_claro(base)}")
        elif clase == "campo":
            campo = destino[3]
            if isinstance(base, dict):
                nueva = {**base, campo: valor}
            elif isinstance(base, Registro):
                nueva = self.construir(base.tipo, {**base.campos, campo: valor})
            else:
                raise ErrorMate(f"{tipo_claro(base)} no tiene campos"
                                + (f". {CAUSA_DE_NADA}" if base is None else ""))
        else:
            raise ErrorMate(NO_ASIGNABLE)
        self.asignar(destino[2], nueva, env)

    def cuidar_lo_de_afuera(self, nombre, env):
        """Mientras un agente atiende, nadie cambia las variables del programa: tampoco
        una función de afuera que el agente llame."""
        e = env
        while e is not None and nombre not in e.vars:
            e = e.padre
        if e is None or not e.vars[nombre][1]:
            return  # no existe o es fijo: lo explica el error de siempre
        agente, _, _, desde = self.contexto
        if e.serie >= desde:
            return  # una variable nacida mientras atiende este mensaje
        propio = e
        while propio is not None and propio is not agente.env:
            propio = propio.padre
        if propio is None:  # ni su estado ni algo suyo: es de afuera
            por = f" (ni siquiera a través de la función {self.llamadas[-1]}())" \
                if self.llamadas else ""
            raise ErrorMate(f"{agente.nombre} no puede modificar '{nombre}'{por}: "
                            "es de afuera. Los agentes solo cambian su propio estado")

    def clave_de_mapa(self, clave):
        if not isinstance(clave, str):
            raise ErrorMate(f"las claves de un mapa son textos, no {tipo_claro(clave)}")

    def posicion(self, sec, i, al_asignar=False):
        """Controla que i sea una posición de esa lista (o de ese texto)."""
        if type(i) is float and i.is_integer():
            # Se ve entero, pero salió de una cuenta con decimales (4 * 0.5): no se acepta
            # a escondidas, y el error no dice "dio 2" como si el 2 estuviera mal.
            raise ErrorMate(
                f"la posición tiene que ser un número entero, y este {formato(i)} salió de "
                "una cuenta con decimales (por ejemplo 4 * 0.5), así que por dentro no es "
                "un entero. Pasalo por redondear(): lista[redondear(...)]")
        if type(i) is float:
            raise ErrorMate(
                f"la posición tiene que ser un número entero y dio {formato(i)}. Si salió "
                "de una cuenta (una división, por ejemplo), pasala por redondear()")
        if type(i) is not int:
            raise ErrorMate("la posición tiene que ser un número entero, no "
                            + tipo_claro(i))
        cuantos = len(sec)
        if 0 <= i < cuantos:
            return
        que, cosas = ("el texto", "letra") if isinstance(sec, str) else ("la lista", "elemento")
        if cuantos == 0:
            tiene = f"{que} no tiene ningún {cosas}"
        elif cuantos == 1:
            tiene = f"{que} tiene 1 {cosas}, así que la única posición es la 0"
        else:
            tiene = (f"{que} tiene {cuantos} {cosas}s, así que las posiciones van de 0 a "
                     f"{cuantos - 1}")
        pista = ""
        if i < 0:
            pista = ". Las posiciones no son negativas: para el último usá ultimo(...)"
        elif al_asignar:
            pista = ". Para sumar un elemento al final usá agregar(lista, valor)"
        elif i == cuantos and cuantos:
            pista = (f". Como se cuenta desde 0, el último está en la posición "
                     f"{cuantos - 1} (o usá ultimo(...))")
        raise ErrorMate(f"la posición {i} está fuera de rango: {tiene}{pista}",
                        familia="posicion")

    # ── expresiones ──
    def ev(self, n, env):
        try:
            return self._ev(n, env)
        except ErrorMate as e:
            e.linea = e.linea or n[1]
            raise

    def _ev(self, n, env):
        clase = n[0]
        if clase in ("num", "str", "bool"):
            return n[2]
        if clase == "nombre":
            return env.buscar(n[2])
        if clase == "nada":
            return None
        if clase == "interp":
            partes, largo = [], 0
            for p in n[2]:
                partes.append(p if isinstance(p, str) else a_texto(self.ev(p, env)))
                largo += len(partes[-1])
                if largo > MAX_LARGO:
                    raise muy_largo()
            return "".join(partes)
        if clase == "lista":
            return [self.ev(x, env) for x in n[2]]
        if clase == "mapa":
            return {k: self.ev(e, env) for k, e in n[2]}
        if clase == "ctor":
            return self.construir(n[2], {k: self.ev(e, env) for k, e in n[3]})
        if clase == "remitente":
            return self.contexto[1] if self.contexto else None
        if clase == "yo":
            return self.contexto[0] if self.contexto else None
        if clase == "crear":
            return self.crear(n, env)
        if clase == "y":
            return self.condicion(n[2], env) and self.condicion(n[3], env)
        if clase == "o":
            return self.condicion(n[2], env) or self.condicion(n[3], env)
        if clase == "no":
            return not self.condicion(n[2], env)
        if clase == "neg":
            v = self.ev(n[2], env)
            if not es_num(v):
                raise ErrorMate(f"no se puede negar {tipo_claro(v)}: el signo menos va "
                                "delante de un número")
            return -v
        if clase == "bin":
            return self.binaria(n[2], self.ev(n[3], env), self.ev(n[4], env))
        if clase == "llamar":
            return self.llamar(self.ev(n[2], env), [self.ev(a, env) for a in n[3]], n[1])
        if clase == "indice":
            base, i = self.ev(n[2], env), self.ev(n[3], env)
            if isinstance(base, (list, str)):
                self.posicion(base, i)
                return base[i]
            if isinstance(base, dict):
                self.clave_de_mapa(i)
                if i not in base:
                    raise ErrorMate(no_esta(
                        f"el mapa no tiene la clave {formato(i, False)}", i, base),
                        familia="clave")
                return base[i]
            raise ErrorMate(f"{tipo_claro(base)} no tiene posiciones ni claves: los "
                            "corchetes van después de una lista, un texto o un mapa"
                            + (f". {CAUSA_DE_NADA}" if base is None else ""))
        if clase == "campo":
            base = self.ev(n[2], env)
            campos = base.campos if isinstance(base, Registro) else base
            if not isinstance(campos, dict):
                raise ErrorMate(f"{tipo_claro(base)} no tiene campos"
                                + (f". {CAUSA_DE_NADA}" if base is None else ""))
            if n[3] not in campos:
                raise ErrorMate(no_esta(
                    f"{nombre_tipo(base)} no tiene un campo '{n[3]}'", n[3], campos),
                    familia="clave")
            return campos[n[3]]
        if clase == "preguntar":
            msg = self.un_mensaje(n[2], env)
            dest = self.destino(n[3], env)
            if self.contexto is None and not self.naciendo:
                self.vaciar_cola()  # lo que el programa ya envió llega antes que la pregunta
            return self.entregar(self.contexto[0] if self.contexto else None, dest, msg, True,
                                 n[1])
        raise ErrorMate(f"expresión desconocida: {clase}")

    def binaria(self, op, a, b):
        if type(a) is int and type(b) is int:
            # Un entero que crece sin parar (x = x * x) cuelga la consola: se corta antes.
            if op == "*" and a.bit_length() + b.bit_length() > MAX_BITS:
                raise ErrorMate(DEMASIADO_GRANDE)
            if op in "+-" and max(a.bit_length(), b.bit_length()) >= MAX_BITS:
                raise ErrorMate(DEMASIADO_GRANDE)
        elif op == "+" and se_juntan(a, b) and len(a) + len(b) > MAX_LARGO:
            raise muy_largo("el texto" if isinstance(a, str) else "la lista")
        try:
            r = self._binaria(op, a, b)
        except OverflowError:
            raise ErrorMate(DEMASIADO_GRANDE)
        if type(r) is float and not math.isfinite(r):
            raise ErrorMate(DEMASIADO_GRANDE)
        return r

    def _binaria(self, op, a, b):
        if op in ("==", "!="):
            if (isinstance(a, str) and es_num(b)) or (es_num(a) and isinstance(b, str)):
                t = a if isinstance(a, str) else b
                raise ErrorMate(
                    f"no se puede comparar un texto con un número ({formato(a, False)} "
                    f"{op} {formato(b, False)}): nunca son iguales. Convertí uno de los "
                    f"dos: numero({formato(t, False)}) o texto(...)")
            return igual(a, b) if op == "==" else not igual(a, b)
        ambos_num = es_num(a) and es_num(b)
        if op in ("<", "<=", ">", ">="):
            if not (ambos_num or (isinstance(a, str) and isinstance(b, str))):
                if a is None or b is None:
                    raise ErrorMate(f"no se puede comparar {un(a)} con {un(b)} usando "
                                    f"'{op}'. {CAUSA_DE_NADA}")
                raise ErrorMate(f"no se puede comparar {nombre_tipo(a)} con {nombre_tipo(b)}")
            if not ambos_num and _FECHA.fullmatch(a) and _FECHA.fullmatch(b):
                raise ErrorMate(
                    f"las fechas son textos, y '{op}' las compararía letra por letra: "
                    f'"{a}" {op} "{b}" daría cualquier cosa. Mate todavía no sabe comparar '
                    "fechas; con == y != sí se puede ver si son la misma")
            return {"<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}[op]
        if op == "+" and (ambos_num or se_juntan(a, b)):
            return a + b
        if ambos_num:
            if op == "-":
                return a - b
            if op == "*":
                return a * b
            if b == 0:
                raise ErrorMate("división por cero", familia="division")
            if op == "%":
                return a % b
            if type(a) is int and type(b) is int and a % b == 0:
                return a // b  # la división exacta entre enteros no pierde cifras
            return a / b
        if a is None or b is None:
            raise ErrorMate(f"no se puede {_VERBOS[op]} {un(a)} con {un(b)}. {CAUSA_DE_NADA}")
        pista = ""
        if op == "+" and isinstance(a, list):
            pista = " (para sumarle un valor a una lista usá agregar(lista, valor))"
        elif op == "+" and (isinstance(a, str) or isinstance(b, str)):
            pista = " (usá texto() o \"{...}\" para armar textos)"
        raise ErrorMate(f"no se puede hacer {nombre_tipo(a)} {op} {nombre_tipo(b)}{pista}")

    def llamar(self, f, args, linea=None):
        if isinstance(f, Nativa):
            return f.fn(args)
        if not isinstance(f, Funcion):
            raise ErrorMate(f"{tipo_claro(f)} no es una función: no se le pueden poner "
                            "paréntesis")
        if len(args) != len(f.params):
            raise ErrorMate(ESPERA_OTRA_CANTIDAD.format(
                n=f.nombre, espera=len(f.params), recibe=len(args)))
        if self.abiertas >= MAX_LLAMADAS:
            self.ultima_funcion = f.nombre
            raise self.demasiada_recursion(f.nombre)
        env = Entorno(f.env, borde=True)
        for p, a in zip(f.params, args):
            env.definir(p, a, origen="parametro")
        self.llamadas.append(f.nombre)
        self.abiertas += 1
        self.ultima_funcion = f.nombre
        try:
            self.bloque(f.cuerpo, env, nuevo=False)
        except _Retorno as r:
            return r.valor
        except ErrorMate as e:
            anotar_paso(e, ("funcion", f.nombre, linea))
            raise
        finally:
            self.llamadas.pop()
            self.abiertas -= 1
        return None

    def recursiva(self):
        """Si se acabó el lugar en medio de llamadas a funciones, el nombre de la última."""
        return self.ultima_funcion if self.abiertas > 20 else None


# ───────────────────────────── CLI ─────────────────────────────


def simbolo(s, reemplazo):
    """Devuelve s si la consola lo puede mostrar; si no, el reemplazo en letras comunes."""
    try:
        s.encode(getattr(sys.stdout, "encoding", None) or "utf-8")
        return s
    except (UnicodeError, LookupError):
        return reemplazo


GUIA = r"""GUÍA DE MATE {version} (para pegarle a un asistente de IA antes de pedirle un programa)

Mate es un lenguaje chico con palabras en español. Escribí solo lo que figura en esta guía:
no inventes palabras ni funciones, y no uses las de otros lenguajes (if, print, return...).

RENGLONES
- Una sentencia por renglón, sin punto y coma. Los comentarios empiezan con #.
- Un renglón sigue en el de abajo solo si queda abierto un ( [ {{ o si termina en un
  operador o una coma. Un renglón no puede empezar con + * / == y o.
- Los bloques van entre llaves {{ }}. Los textos, entre comillas dobles y en un renglón.

VALORES
- numero: 3   3.5 (decimales con punto)   1500 o 1_500 (los miles nunca llevan punto)
- texto: "hola"        logico: verdadero  falso
- nada (la ausencia de valor)
- lista: [1, 2, 3]   lista[0] es el primero (las posiciones arrancan en 0)
- mapa: {{ nombre: "yerba", precio: 3500 }}   mapa.nombre   mapa["nombre"]
- Dentro de un texto, {{...}} se calcula: "Total: {{precio * 2}}". Adentro de las llaves
  puede haber otros textos, con sus comillas: "Sale {{precios["yerba"]}}". \n es salto de
  renglón, \{{ una llave de verdad y \\ una barra (las rutas de Windows van con / o con
  doble barra).

VARIABLES
- sea x = 1        fijo, no cambia más
- var y = 0        puede cambiar:   y = y + 1     y += 1     y -= 1
- y.campo = 5 y lista[0] = 5 cambian una parte (la variable tiene que ser 'var').
- Copiar un valor lo copia entero: cambiar la copia no toca el original.
- Un 'sea' o 'var' dentro de un bloque no puede repetir el nombre de una variable de afuera.
- Un porcentaje se escribe como cuenta: 21 / 100 o 0.21 (el signo % es el resto de dividir).
- No se usan como nombre las palabras de Mate ni las funciones incluidas.
- Nombres de variables y funciones en minúscula; mensajes y agentes con Mayúscula inicial.

OPERADORES
- + - * / %        == != < <= > >=        y  o  no
- Nada se convierte solo: "a" + 1 es un error (usar "a{{1}}" o texto(1)), y "18" == 18
  también (usar numero("18")). Las condiciones tienen que dar verdadero o falso.

CONTROL
- si cond {{ ... }} sino si cond {{ ... }} sino {{ ... }}
- mientras cond {{ ... }}
- para item en lista {{ ... }}      (también recorre las claves de un mapa y las letras de un texto)
- para i, item en lista {{ ... }}   con la posición (desde 0); en un mapa: para clave, valor en mapa
- romper sale del bucle; continuar salta a la vuelta siguiente.
- funcion nombre(a, b) {{ devolver a + b }}        'devolver' solo, sin valor, devuelve nada
- fallar "motivo"                                 corta con un error
- intentar {{ ... }} si falla e {{ ... }}             e es el texto del error (el 'e' es opcional)
  detalle_de(e).clase dice qué pasó sin depender de la redacción: "fallar", "asegurar",
  "contrato", "clave", "posicion", "division", "nombre", "numero", "json", "agente",
  "ciclo", "archivo" u "otro". detalle_de(e).dato es el valor que se le dio a 'fallar'.

FUNCIONES INCLUIDAS (no hay otras)
{funciones}
- agregar, quitar, ordenar y porcion devuelven una copia NUEVA, no cambian la original:
  lista = agregar(lista, x)
- quitar(lista, x) saca por valor, no por posición: se van todos los que valen x.
- Una función incluida suelta en un renglón (salvo mostrar, leer y escribir_archivo) es un
  error: hay que usar lo que devuelve. Ese error no se ataja con 'intentar': para validar
  un dato se escribe  intentar {{ sea n = numero(dato) ... }} si falla e {{ ... }}
- hoy() y ahora() dan textos: no se restan ni se comparan con < o > (sí con == y !=).
- leer_archivo y escribir_archivo solo andan desde el programa principal (no desde un agente),
  con archivos de la carpeta del programa, y no pisan archivos .mate ni .py.

AGENTES Y MENSAJES
- mensaje Pedido {{ producto: texto, cantidad: numero, nota: texto? }}     (? = opcional)
  Tipos: numero texto logico lista mapa agente cualquiera, u otro mensaje. Una lista
  puede decir de qué es: items: lista de Pedido     vendedores: lista de agente
- mensaje Pedido {{ ... }} responde Cotizacion     declara qué se le contesta a un Pedido
- Crear un mensaje: Pedido {{ producto: "yerba", cantidad: 2 }}     Sin campos: Ping {{}}
- agente Nombre {{
      estado contador = 0                  memoria privada; solo él la cambia
      al recibir Pedido como p {{ ... }}     uno por cada mensaje que entiende
      funcion ayuda(x) {{ ... }}             funciones propias
  }}
- responder valor        contesta y termina (solo dentro de 'al recibir')
- enviar Mensaje {{ ... }} a Agente              lo deja en la cola y sigue
- enviar Mensaje {{ ... }} a [norte, sur]        el mismo mensaje a cada agente de la lista
- sea r = preguntar Mensaje {{ ... }} a Agente   espera la respuesta; si el otro falla, falla acá
- remitente es quien mandó el mensaje; yo es el agente que está atendiendo.
- Dentro de un agente, opcional: al fallar como f {{ ... }}   se entera cuando un mensaje que
  él mandó con 'enviar' no pudo atenderse. f.motivo es el texto del error, f.mensaje el
  mensaje que mandó y f.destino el agente que falló. Ahí no va 'responder'.
- sea otro = crear Vendedor llamado "Norte" {{ contador: 5 }}     otra copia, con su estado
- Un agente no puede cambiar variables de afuera ni el estado de otro. Los mensajes llevan
  datos, nunca funciones.
- usar "otro.mate" trae los mensajes, agentes, funciones y variables ('sea' y 'var') de
  otro archivo. Un nombre que ya vino de ahí no se puede declarar de nuevo.

PRUEBAS
- prueba "nombre" {{ asegurar total == 10 }}        asegurar cond, "mensaje si falla"
- asegurar falla {{ dividir(1, 0) }}                 se cumple si lo de adentro falla
  (un nombre mal escrito ahí adentro no cuenta como la falla esperada)
- simular Vendedor al recibir Pedido como p {{ responder Cotizacion {{ total: 1 }} }}
  Solo dentro de una prueba: hasta que termina, ese agente contesta eso a ese mensaje.
- Van en el nivel superior y corren con la orden 'probar'. Cada una empieza limpia.

ANTES DE CORRER
- Mate revisa todo el programa y no arranca si un nombre no existe (totl por total) o si una
  función recibe valores de más o de menos, aunque sea en una parte que no se ejecuta.
  Lo declarado afuera de todo puede estar más abajo en el archivo. No revisa adentro de
  intentar {{ }} ni de asegurar falla {{ }}. Los errores salen así: archivo:renglón: error: ...
- --traza numera los mensajes y muestra cuál falló o quedó sin respuesta.

UN PROGRAMA COMPLETO
--- ejemplo ---
mensaje Pedido {{ producto: texto, cantidad: numero }}
mensaje Cotizacion {{ producto: texto, total: numero }}

agente Vendedor {{
    estado precios = {{ yerba: 3500, azucar: 1200 }}
    estado cotizados = 0

    al recibir Pedido como p {{
        si no tiene(precios, p.producto) {{
            fallar "no vendo {{p.producto}}"
        }}
        cotizados += 1
        responder Cotizacion {{ producto: p.producto, total: precios[p.producto] * p.cantidad }}
    }}
}}

funcion total_de(pedidos) {{
    var total = 0
    para pedido en pedidos {{
        si pedido.cantidad <= 0 {{
            continuar
        }}
        intentar {{
            sea c = preguntar Pedido {{
                producto: pedido.producto, cantidad: pedido.cantidad,
            }} a Vendedor
            total += c.total
        }} si falla motivo {{
            mostrar("Se saltea: {{motivo}}")
        }}
    }}
    devolver total
}}

sea lista = [{{ producto: "yerba", cantidad: 2 }}, {{ producto: "café", cantidad: 1 }}]
mostrar("Total: {{pesos(total_de(lista))}}")

prueba "suma solo lo que el vendedor vende" {{
    asegurar total_de([{{ producto: "azucar", cantidad: 3 }}]) == 3600
    asegurar total_de([]) == 0
}}
--- fin del ejemplo ---

CÓMO SE CORRE (Windows)
  python mate\mate.py correr archivo.mate        python mate\mate.py probar archivo.mate
  python mate\mate.py verificar archivo.mate     (revisa sin correr)
"""


def texto_de_guia():
    return GUIA.format(version=VERSION, funciones=lista_de_funciones())


_EJ_AGENTE = """mensaje Sumar { a: numero, b: numero }
agente Calculadora {
    estado cuentas = 0
    al recibir Sumar como s {
        cuentas += 1
        responder s.a + s.b
    }
}
sea r = preguntar Sumar { a: 2, b: 3 } a Calculadora
mostrar(r)"""
_EJ_FALLAR = """funcion dividir(a, b) {
    si b == 0 { fallar "no se puede dividir por cero" }
    devolver a / b
}
intentar {
    mostrar(dividir(1, 0))
} si falla e {
    mostrar("No anduvo: {e}")
}"""
_EJ_PRUEBA = """funcion doble(n) { devolver n * 2 }
prueba "el doble de 4 es 8" {
    asegurar doble(4) == 8
    asegurar doble(0) == 0, "el doble de cero es cero"
}"""

# La ayuda de cada palabra de Mate: qué hace y un ejemplo que se puede copiar y correr.
# (La de las funciones incluidas sale de la tabla FUNCIONES.)
AYUDA = {
    "sea": ("guarda un valor con un nombre. Es fijo: no cambia más (para que pueda "
            "cambiar va 'var')", 'sea iva = 0.21\nmostrar("El IVA es {iva}")'),
    "var": ("guarda un valor que después se puede cambiar",
            "var total = 0\ntotal = total + 10\ntotal += 5\nmostrar(total)"),
    "funcion": ("le pone nombre a unos pasos para usarlos muchas veces. 'devolver' entrega "
                "el resultado y termina la función",
                "funcion doble(n) {\n    devolver n * 2\n}\nmostrar(doble(4))"),
    "si": ("hace una cosa u otra según una condición, que tiene que dar verdadero o falso. "
           "'sino si' y 'sino' son opcionales y van en el renglón de la llave que cierra",
           'sea edad = 20\nsi edad >= 18 {\n    mostrar("mayor")\n} sino si edad >= 13 {\n'
           '    mostrar("adolescente")\n} sino {\n    mostrar("chico")\n}'),
    "mientras": ("repite el bloque mientras la condición sea verdadera",
                 "var n = 3\nmientras n > 0 {\n    mostrar(n)\n    n -= 1\n}"),
    "para": ("recorre una lista de a un elemento (también las claves de un mapa o las "
             "letras de un texto). Con dos nombres, el primero es la posición",
             'sea frutas = ["pera", "uva"]\npara fruta en frutas {\n    mostrar(fruta)\n}\n'
             'para i, fruta en frutas {\n    mostrar("{i}: {fruta}")\n}'),
    "romper": ("'romper' corta el bucle ('para' o 'mientras') en el que está; 'continuar' "
               "salta a la vuelta siguiente",
               'para cosa en ["pan", "", "fin", "leche"] {\n    si cosa == "" { continuar }\n'
               '    si cosa == "fin" { romper }\n    mostrar(cosa)\n}'),
    "y": ("'y', 'o' y 'no' combinan condiciones: las dos, alguna de las dos, o lo contrario",
          'sea edad = 20\nsea socio = falso\nsi edad >= 18 y no socio {\n'
          '    mostrar("puede asociarse")\n}\nsi edad < 13 o edad > 65 {\n'
          '    mostrar("entra gratis")\n}'),
    "verdadero": ("'verdadero' y 'falso' son los dos valores lógicos: lo que da una "
                  "comparación y lo que espera un 'si'",
                  'sea abierto = verdadero\nsi abierto {\n    mostrar("pasá")\n}\n'
                  "mostrar(3 > 5)"),
    "nada": ("es la falta de valor: lo que devuelve una función sin 'devolver', o un campo "
             "opcional que no vino",
             'sea precios = { yerba: 3500 }\nsea p = obtener(precios, "cafe", nada)\n'
             'si p == nada {\n    mostrar("no vendo café")\n}'),
    "lista": ("varios valores en orden, entre corchetes. Las posiciones arrancan en 0",
              'var compras = ["yerba", "pan"]\ncompras = agregar(compras, "leche")\n'
              "mostrar(compras[0], largo(compras), ultimo(compras))"),
    "mapa": ("valores con nombre, entre llaves. Las claves son siempre textos",
             'var producto = { nombre: "yerba", precio: 3500 }\nproducto.precio = 3800\n'
             'mostrar(producto.nombre, producto["precio"], claves(producto))'),
    "mensaje": ("declara el contrato de un mensaje: qué campos lleva y de qué tipo (numero, "
                "texto, logico, lista, mapa, agente, cualquiera u otro mensaje; con ? es "
                "opcional). Con 'responde' dice además qué se le contesta",
                "mensaje Pedido { producto: texto, cantidad: numero, nota: texto? }\n"
                'sea p = Pedido { producto: "yerba", cantidad: 2 }\nmostrar(p.producto)'),
    "agente": ("alguien que recibe mensajes. Tiene su 'estado' privado, que solo él cambia, "
               "y un 'al recibir' por cada mensaje que entiende", _EJ_AGENTE),
    "responder": ("contesta al que mandó el mensaje y termina de atenderlo. Solo va dentro "
                  "de 'al recibir'", _EJ_AGENTE),
    "preguntar": ("le manda un mensaje a un agente y espera lo que responde. Si el agente "
                  "falla, el error llega acá y se puede atajar con 'intentar'", _EJ_AGENTE),
    "enviar": ("le manda un mensaje a un agente (o a una lista de agentes) y sigue de "
               "largo, sin esperar respuesta",
               'mensaje Aviso { nota: texto }\nagente Cartelera {\n    al recibir Aviso como a {'
               '\n        mostrar("Aviso: {a.nota}")\n    }\n}\n'
               'enviar Aviso { nota: "llegó la yerba" } a Cartelera'),
    "remitente": ("dentro de un agente, 'remitente' es quien le mandó el mensaje que está "
                  "atendiendo, y 'yo' es el propio agente",
                  "mensaje Arrancar {}\nmensaje Hola { quien: agente }\nmensaje Gracias {}\n"
                  "agente Ana {\n    al recibir Hola como h { enviar Gracias {} a remitente }\n"
                  "}\nagente Beto {\n    al recibir Arrancar { enviar Hola { quien: yo } a Ana }"
                  '\n    al recibir Gracias { mostrar("Ana me contestó") }\n}\n'
                  "enviar Arrancar {} a Beto"),
    "crear": ("hace otra copia de un agente ya declarado, con su propio estado. 'llamado' "
              "le pone nombre",
              "mensaje Cuanto {}\nagente Caja {\n    estado plata = 0\n"
              "    al recibir Cuanto { responder plata }\n}\n"
              'sea norte = crear Caja llamado "Norte" { plata: 500 }\n'
              "mostrar(preguntar Cuanto {} a norte)"),
    "fallar": ("corta lo que se está haciendo con un error que lleva ese motivo", _EJ_FALLAR),
    "intentar": ("prueba hacer algo y, si falla, sigue por el bloque de 'si falla' en vez "
                 "de cortar el programa. El nombre de después de 'falla' guarda el texto "
                 "del error", _EJ_FALLAR),
    "prueba": ("una comprobación que vive al lado del código. No corre con 'correr': corre "
               "con la orden 'probar archivo.mate'", _EJ_PRUEBA),
    "asegurar": ("comprueba que algo sea verdadero; si no lo es, falla (después de una coma "
                 "se le puede poner un texto que lo explique). 'asegurar falla { ... }' "
                 "comprueba que algo falle", _EJ_PRUEBA),
    "simular": ("solo dentro de una prueba: hasta que termina, ese agente contesta lo que "
                "diga este bloque en vez de lo suyo",
                "mensaje Precio { producto: texto }\nagente Vendedor {\n"
                "    al recibir Precio como p { responder 3500 }\n}\n"
                'prueba "con otro precio" {\n'
                "    simular Vendedor al recibir Precio como p { responder 10 }\n"
                '    asegurar preguntar Precio { producto: "yerba" } a Vendedor == 10\n}'),
    "usar": ("trae los mensajes, agentes, funciones y variables ('sea' y 'var') de otro "
             "archivo, que se busca al lado de este", 'usar "catalogo.mate"\nmostrar(iva)'),
    "al fallar": ("dentro de un agente: se entera cuando un mensaje que él mandó con "
                  "'enviar' no pudo atenderse. Lo que llega trae motivo, mensaje y destino. "
                  "Ahí no va 'responder'",
                  "mensaje Arrancar {}\nmensaje Pedido { producto: texto }\n"
                  "agente Deposito {\n"
                  '    al recibir Pedido como p { fallar "no hay {p.producto}" }\n}\n'
                  "agente Vendedor {\n"
                  '    al recibir Arrancar { enviar Pedido { producto: "yerba" } a Deposito }\n'
                  '    al fallar como f { mostrar("No salió: {f.motivo}") }\n}\n'
                  "enviar Arrancar {} a Vendedor"),
}
# Las palabras que se explican junto con otra.
VER_AYUDA_DE = {
    "devolver": "funcion", "sino": "si", "en": "para", "continuar": "romper",
    "o": "y", "no": "y", "falso": "verdadero", "logico": "verdadero",
    "estado": "agente", "al": "agente", "recibir": "agente", "como": "agente",
    "yo": "remitente", "falla": "intentar", "llamado": "crear", "responde": "mensaje",
    "cualquiera": "mensaje", "a": "enviar",
}


def ayuda_de(palabra):
    """La ayuda de una palabra de Mate o de una función incluida (o None si no es)."""
    nombre = " ".join(sin_tildes(palabra).split())
    nombre = nombre[:-2] if nombre.endswith("()") else nombre
    nota = []
    if nombre in FUNCIONES:
        _, _, ejemplo, que = FUNCIONES[nombre]
        titulo, ejemplo = f"{nombre} (función incluida): {que}", ejemplo
    else:
        tema = VER_AYUDA_DE.get(nombre, nombre)
        if tema not in AYUDA:
            return None
        que, ejemplo = AYUDA[tema]
        titulo = f"{nombre}: {que}" if tema == nombre else f"{nombre} (va con '{tema}'): {que}"
    renglones, largo = [], 0
    for parte in titulo.split(" "):  # el título, cortado para que entre en la consola
        if renglones and largo + len(parte) < 88:
            renglones[-1] += " " + parte
            largo += len(parte) + 1
        else:
            renglones.append(parte)
            largo = len(parte)
    if nombre in ("al", "fallar"):
        nota = ["", "(Dentro de un agente también existe 'al fallar': mirá 'ayuda al fallar')"]
    return "\n".join(renglones + ["", "Ejemplo:"]
                     + ["    " + r for r in ejemplo.split("\n")] + nota)


def temas_de_ayuda():
    return sorted(set(AYUDA) | set(VER_AYUDA_DE) | PALABRAS) + sorted(FUNCIONES)


def ayuda_de_palabra(palabra, mostrar, avisar):
    """'ayuda si', 'ayuda largo': muestra la explicación. Devuelve el código de salida."""
    texto = ayuda_de(palabra)
    if texto is None and PISTAS.get(palabra.lower()) and ayuda_de(PISTAS[palabra.lower()]):
        mostrar(pista_de(palabra)[0].upper() + pista_de(palabra)[1:] + ".")
        texto = ayuda_de(PISTAS[palabra.lower()])
    if texto is None and len(palabra.split()) > 1:
        # 'ayuda si falla', 'ayuda al recibir': se explica la primera palabra que tenga ayuda
        for parte in palabra.split():
            if ayuda_de(parte):
                mostrar(f"No tengo ayuda sobre '{palabra}' todo junto: la ayuda es de a una "
                        f"palabra. Esta es la de '{parte}':")
                mostrar("")
                mostrar(ayuda_de(parte))
                return 0
    if texto is None:
        avisar(f"no tengo ayuda sobre '{palabra}'.{sugerir(palabra, temas_de_ayuda())}")
        avisar("Hay ayuda de las palabras de Mate: " + ", ".join(sorted(PALABRAS)))
        avisar("y de las funciones incluidas: " + ", ".join(sorted(FUNCIONES)))
        return 2
    mostrar(texto)
    return 0


def falta_cerrar(texto):
    """En la consola: ¿quedó abierto un paréntesis, un corchete o una llave?"""
    try:
        tokens = tokenizar(texto)
    except ErrorMate:
        return False  # está mal escrito: que lo diga el error
    if sum((t[1] in _CIERRES) - (t[1] in _CIERRES.values())
           for t in tokens if t[0] == "op") > 0:
        return True
    # Como en un archivo: un renglón que termina en un operador o en una coma sigue abajo.
    if len(tokens) < 2:
        return False
    tipo, valor = tokens[-2][:2]
    if tipo == "kw":
        return valor in ("y", "o")
    if tipo != "op" or valor not in _SIGUEN:
        return False
    # (salvo '21%': eso no sigue abajo, es un porcentaje mal escrito y lo dice el error)
    return not (valor == "%" and len(tokens) > 2 and tokens[-3][0] == "num")


_SIGUEN = COMPARADORES + ("+", "-", "*", "/", "%", "=", "+=", "-=", ",")


def consola(entrada=None, mostrar=print):
    """La orden 'consola': para probar renglones sueltos sin crear un archivo. Lo que se
    declara queda para los renglones siguientes, y un valor suelto se muestra solo."""
    interprete = Interprete(salida=mostrar)
    interprete.glob.se_pisa = True  # acá se puede volver a declarar algo para corregirlo
    if entrada is not None:
        interprete.entrada = entrada  # (en las pruebas: de ahí saca leer() su respuesta)
    entrada = entrada or input
    mostrar(f"Mate {VERSION}, consola. Escribí un renglón y apretá Enter; para terminar, salir")
    mostrar("(un valor suelto, como 2 + 3, se muestra solo; 'ayuda si' explica una palabra)")
    declarado = []  # lo ya declarado, para revisar los contratos de lo que se escriba
    renglon, pendiente = 1, []  # los renglones se numeran de corrido, como en un archivo

    def decir(linea, texto, ultimo):
        texto, _, camino = texto.partition("\ncómo se llegó: ")
        antes = f"línea {linea}: " if linea and int(linea) != ultimo else ""
        mostrar(f"{antes}error: {texto}")
        if camino:
            mostrar(f"    cómo se llegó: {camino}")

    def correr_pedazo(fuente, ultimo):
        try:
            programa = analizar(fuente, en_consola=True)
            se_declaran = [s for s in programa
                           if s[0] in ("sea", "funcion", "agente", "mensaje")]
            nuevos = {s[2] for s in se_declaran}
            previo = [s for s in declarado if s[2] not in nuevos]
            errores = verificar(previo + programa, en_consola=True)
            if errores:
                for linea, texto in errores:
                    decir(linea, texto, ultimo)
                return
            declarado[:] = previo + se_declaran
            suelto = len(programa) == 1 and programa[0][0] == "expr"
            if suelto:  # un valor suelto se guarda un momento para poder mostrarlo
                programa = [("sea", programa[0][1], "_", programa[0][2], False)]
            interprete.pasos = interprete.entregados = 0
            interprete.glob.vars.pop("_", None)
            interprete.correr(programa)
            if any(s[0] == "prueba" for s in programa):
                mostrar("(las pruebas no corren en la consola: guardalas en un archivo y "
                        "usá la orden 'probar')")
            if suelto:
                valor = interprete.glob.vars.pop("_")[0]
                if isinstance(valor, (Funcion, Nativa)):
                    mostrar(f"error: a '{valor.nombre}' le faltan los paréntesis: "
                            f"{valor.nombre}(...)")
                elif valor is not None:
                    mostrar(formato(valor, False))
        except ErrorMate as e:
            for linea, texto in interprete.errores_agentes_det:
                decir(linea, texto, ultimo)
            interprete.errores_agentes, interprete.errores_agentes_det = [], []
            # (acá no hay archivo: lo que se terminó es lo que escribió la persona)
            e.mensaje = e.mensaje.replace(
                "no esperaba el final del archivo acá",
                "lo que escribiste quedó a medio terminar: falta algo al final").replace(
                "el final del archivo", "el final de lo que escribiste")
            decir(e.linea, interprete.con_camino(e.mensaje, e), ultimo)
            avisar_pendientes(interprete, mostrar)
            interprete.cola.clear()
        except KeyboardInterrupt:
            mostrar("cortado con Ctrl+C (la consola sigue abierta)")
            interprete.cola.clear()
        for linea, texto in interprete.errores_agentes_det:
            decir(linea, texto, ultimo)
        interprete.errores_agentes, interprete.errores_agentes_det = [], []

    while True:
        try:
            linea = entrada(f"{renglon + len(pendiente):>3}{'.' if pendiente else '>'} ")
        except (EOFError, KeyboardInterrupt):
            mostrar("")
            break
        except UnicodeError:  # una entrada redirigida, con letras en otra codificación
            mostrar("error: ese renglón trae una letra que no pude entender (una tilde o una "
                    "ñ en otra codificación): escribilo de nuevo")
            continue
        orden = linea.strip().lower()
        if not pendiente:
            if orden in ("salir", "chau", "exit", "quit"):
                break
            if not orden:
                continue
            if orden == "ayuda":
                mostrar("Escribí un renglón de Mate y apretá Enter. Si queda una llave "
                        "abierta (o el renglón termina en + , =), seguís en el de abajo.")
                mostrar("'ayuda si' o 'ayuda largo' explican una palabra o una función. "
                        "Para terminar: salir")
                continue
            if orden.startswith("ayuda ") and all(p.isalpha() or p.endswith("()")
                                                  for p in orden.split()[1:]):
                ayuda_de_palabra(" ".join(orden.split()[1:]), mostrar, mostrar)
                continue
        # Sigue abajo si quedó algo abierto (un renglón vacío corta y muestra el error).
        if orden and falta_cerrar("\n".join(pendiente + [linea])):
            pendiente.append(linea)
            continue
        fuente = "\n" * (renglon - 1) + "\n".join(pendiente + [linea])
        renglon += len(pendiente) + 1
        pendiente = []
        # (el último renglón con algo escrito: un error ahí no hace falta decir dónde está)
        correr_pedazo(fuente, fuente.rstrip().count("\n") + 1)
    return 0


def texto_de_ayuda():
    if os.name == "nt":
        ejemplo = "python mate\\mate.py correr mate\\ejemplos\\hola.mate"
    else:
        ejemplo = "python3 mate/mate.py correr mate/ejemplos/hola.mate"
    return "\n".join([
        f"Mate {VERSION}: un lenguaje chico, con palabras en español.",
        "",
        "Órdenes:",
        "  correr    archivo.mate   corre el programa",
        "  probar    archivo.mate   corre las pruebas que el programa trae adentro",
        "  probar    carpeta        corre las pruebas de todos los .mate de esa carpeta",
        "  verificar archivo.mate   revisa el programa sin correrlo (nombres, contratos...)",
        "  guia                     una página con todo Mate, para pegarle a una IA",
        "  ayuda                    muestra esta ayuda",
        "  ayuda si                 explica una palabra o una función de Mate, con un ejemplo",
        "  consola                  para probar renglones sueltos sin crear un archivo",
        "",
        "Opciones:",
        "  --traza       muestra la conversación entre agentes, numerada y con lo que falló",
        "  --traza=conversacion.txt   la guarda en ese archivo, con un resumen al final",
        "  --sin-limite  no corta los programas que dan muchísimos pasos",
        "  --depurar     si Mate falla por dentro, muestra el detalle técnico",
        "  --version     dice qué versión de Mate es",
        "",
        "Un ejemplo listo para copiar:",
        f"  {ejemplo}",
    ])


def _ubicar(ruta):
    """Busca el archivo a correr. Devuelve (ruta, None) o (None, explicación)."""
    if os.path.isfile(ruta):
        return ruta, None
    if os.path.isfile(ruta + ".mate"):
        return ruta + ".mate", None
    if os.path.isdir(ruta):
        return None, f"'{ruta}' es una carpeta, no un archivo .mate"
    nombre = os.path.basename(ruta)
    if os.path.isfile(ruta + ".txt"):
        return None, (f"encontré {nombre}.txt: el Bloc de notas le agregó .txt. "
                      "Renombralo, o al guardar elegí Tipo: Todos los archivos")
    if os.path.exists(ruta):
        return ruta, None  # algo raro (ni archivo ni carpeta): que lo diga al abrirlo
    carpeta = os.path.dirname(os.path.abspath(ruta))
    texto = f"no encuentro '{nombre}' en {carpeta}"
    try:
        otros = sorted(a for a in os.listdir(carpeta) if a.lower().endswith(".mate"))
    except OSError:
        return None, texto + " (esa carpeta no existe)"
    if otros:
        texto += "\narchivos .mate que sí hay ahí: " + ", ".join(otros[:10])
        texto += ", ..." if len(otros) > 10 else ""
    return None, texto


def renglon_de(archivo, linea):
    """El renglón del archivo donde cayó el error, como '    N | texto' (o None)."""
    try:
        renglones = leer_fuente(archivo).split("\n")
    except (OSError, ErrorMate):
        return None
    n = int(linea)
    if n < 1:
        return None
    if n > len(renglones) or not any(r.strip() for r in renglones[n - 1:]):
        # El error cayó después del final: se muestra el último renglón con algo escrito.
        n = min(n, len(renglones))
        while n >= 1 and not renglones[n - 1].strip():
            n -= 1
    if n < 1 or not renglones[n - 1].strip():
        return None
    return f"    {n} | {renglones[n - 1].rstrip()}"


def error_escrito(ruta, linea, texto):
    """Un error como se muestra siempre, sea de un agente o no, con 'correr' o con
    'probar': 'archivo:renglón: error: texto', debajo el renglón señalado y, si lo hay,
    por dónde se llegó. Devuelve esas tres partes (las dos últimas pueden ser None)."""
    archivo = getattr(linea, "archivo", None) or ruta
    texto, _, camino = texto.partition("\ncómo se llegó: ")
    cabecera = (f"{archivo}:{linea}: error: {texto}" if linea
                else f"{archivo}: error: {texto}")
    renglon = renglon_de(archivo, linea) if linea else None
    return cabecera, renglon, f"    cómo se llegó: {camino}" if camino else None


def avisar_pendientes(interprete, avisar):
    """Si el programa se cortó con mensajes en la cola, dice cuáles no llegaron."""
    cola = list(getattr(interprete, "cola", ()))
    if not cola:
        return
    avisar(f"quedaron {len(cola)} mensaje(s) sin entregar:")
    for rem, dest, msg in cola[:5]:
        avisar(f"  {rem.nombre if rem else '(programa)'} -> {dest.nombre}: {formato(msg)}")
    if len(cola) > 5:
        avisar(f"  ... y {len(cola) - 5} más")


def guardar_conversacion(destino, programa, renglones, cuenta, sumar=False):
    """Deja la conversación en un archivo de texto, con un resumen al final. Devuelve
    None si salió bien o la explicación de por qué no se pudo. Con sumar=True la agrega
    al final de lo que ya hay ('probar' con varios archivos: una sección por archivo)."""
    total = cuenta["enviar"] + cuenta["preguntar"]
    resumen = (f"Resumen: {total} mensaje(s) entregado(s): {cuenta['enviar']} con 'enviar' "
               f"y {cuenta['preguntar']} con 'preguntar'. ")
    resumen += ("Ninguno falló." if not cuenta["fallaron"]
                else f"Fallaron {cuenta['fallaron']}.")
    texto = "\n".join([f"Conversación de {programa}", ""] + renglones + ["", resumen, ""])
    try:
        # con la marca del principio, para que el Bloc de notas muestre bien las tildes
        with open(destino, "a" if sumar else "w",
                  encoding="utf-8" if sumar else "utf-8-sig") as f:
            f.write(("\n" if sumar else "") + texto)
    except OSError:
        return f"no pude guardar la conversación en '{destino}'"
    return None


def probar_varios(pedidos, opciones, avisar):
    """'probar' con varios archivos o con una carpeta: corre las pruebas de cada uno y
    da un total general."""
    archivos = []
    for pedido in pedidos:
        if not os.path.isdir(pedido):
            archivos.append(pedido)
            continue
        try:
            adentro = sorted(a for a in os.listdir(pedido) if a.lower().endswith(".mate"))
        except OSError:
            avisar(f"no pude mirar adentro de la carpeta '{pedido}'")
            return 2
        if not adentro:
            avisar(f"en la carpeta '{pedido}' no hay ningún archivo .mate")
            return 2
        archivos += [os.path.join(pedido, a) for a in adentro]
    pasaron = total = 0
    con_problemas = []
    guardadas = []  # con --traza=archivo: las conversaciones ya guardadas (van una tras otra)
    for archivo in archivos:
        print(f"{archivo}:")
        sys.stdout.flush()
        donde = {"ruta": None, "interprete": None, "varios": True, "guardadas": guardadas}
        codigo = _main(["probar", archivo] + opciones, donde)
        sys.stderr.flush()
        bien, cuantas = donde.get("pruebas", (0, 0))
        pasaron, total = pasaron + bien, total + cuantas
        if codigo:
            con_problemas.append(archivo)
        print()
    print(f"En total: {pasaron} de {total} pruebas pasaron, en {len(archivos)} archivos")
    if con_problemas:
        print("Con problemas: " + ", ".join(con_problemas))
    return 1 if con_problemas else 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    for flujo in (sys.stdout, sys.stderr, sys.stdin):
        try:  # que una consola vieja de Windows no rompa por un símbolo que no conoce
            flujo.reconfigure(errors="replace")
        except Exception:
            pass
    depurar = any(a.lower() == "--depurar" for a in argv)
    donde = {"ruta": None, "interprete": None}

    def lugar():
        linea = getattr(donde["interprete"], "linea_actual", None)
        if not linea:
            return None
        return f"{getattr(linea, 'archivo', None) or donde['ruta']}:{linea}"

    def avisar(texto):
        print(texto, file=sys.stderr)

    # Red de seguridad: pase lo que pase, nunca un error interno de Python en inglés.
    try:
        return _main(argv, donde)
    except BrokenPipeError:  # la salida iba a otro programa que dejó de leer (| more)
        try:
            os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        except Exception:
            pass
        return 1
    except KeyboardInterrupt:
        if lugar():
            avisar(f"{lugar()}: cortado con Ctrl+C mientras corría esta línea")
        else:
            avisar("cortaste el programa con Ctrl+C")
        avisar_pendientes(donde["interprete"], avisar)
        return 130
    except RecursionError:
        if depurar:
            raise
        antes = f"{donde['ruta']}: " if donde["ruta"] else ""
        avisar(f"{antes}error: el programa tiene demasiados niveles anidados "
               "(paréntesis, bloques o llamadas)")
        return 1
    except MemoryError:
        if depurar:
            raise
        avisar(f"{lugar() or donde['ruta'] or 'mate'}: error: {SIN_MEMORIA}")
        return 1
    except Exception as e:
        if depurar:
            raise
        avisar(f"error interno de Mate (no es culpa tuya): {type(e).__name__}: {e}")
        if lugar():
            avisar(f"pasó cerca de {lugar()}")
        avisar("corré de nuevo con --depurar para ver el detalle")
        avisar_pendientes(donde["interprete"], avisar)
        return 1


def _main(argv, donde):
    def avisar(texto):
        print(texto, file=sys.stderr)

    alias = {"-h": "--ayuda", "--help": "--ayuda", "-?": "--ayuda", "/?": "--ayuda"}
    opciones, args, conversacion = set(), [], None
    for a in argv:
        if a.lower() in alias:
            opciones.add(alias[a.lower()])
        elif a.lower().startswith("--traza="):
            conversacion = a[len("--traza="):].strip('"')
            if not conversacion:
                avisar("a --traza= le falta el nombre del archivo, por ejemplo: "
                       "--traza=conversacion.txt")
                return 2
            if conversacion.lower().endswith((".mate", ".py")):
                avisar(f"no guardo la conversación en '{conversacion}' para no pisar un "
                       "programa: elegí otro nombre, por ejemplo --traza=conversacion.txt")
                return 2
        elif a.startswith("-") and a != "-":
            if a.lower() not in OPCIONES:
                parecidas = difflib.get_close_matches(a.lower(), OPCIONES, 1)
                avisar(f"no conozco la opción {a}" + (
                    f", ¿quisiste decir {parecidas[0]}?" if parecidas
                    else ". Las opciones son: " + ", ".join(OPCIONES)))
                return 2
            opciones.add(a.lower())
        else:
            args.append(a)

    if "--version" in opciones:
        print(f"Mate {VERSION} (Python {sys.version_info[0]}.{sys.version_info[1]})")
        return 0
    if args and args[0].lower() == "ayuda" and len(args) >= 2 and not (
            len(args) == 2 and args[1].lower() in ORDENES + ("ayuda", "guia", "guía", "consola")):
        # 'ayuda si', 'ayuda largo', 'ayuda al fallar'
        return ayuda_de_palabra(" ".join(args[1:]), print, avisar)
    if "--ayuda" in opciones or (args and args[0].lower() == "ayuda"):
        print(texto_de_ayuda())
        return 0
    if not args:
        print(texto_de_ayuda())
        return 2
    if args[0].lower() in ("guia", "guía"):
        print(texto_de_guia())
        return 0
    if args[0].lower() == "consola":
        if len(args) > 1:
            avisar("'consola' va sola, sin archivo: ahí adentro se escriben los renglones")
            return 2
        return consola()

    def parece_archivo(a):
        return (a.lower().endswith((".mate", ".mate.txt")) or os.path.isfile(a)
                or os.path.isfile(a + ".mate"))

    if args[0].lower() not in ORDENES and parece_archivo(args[0]):
        if len(args) == 1:
            args = ["correr"] + args  # 'mate.py hola.mate' es 'mate.py correr hola.mate'
        elif len(args) == 2 and args[1].lower() in ORDENES:
            avisar(f"la orden va primero y el archivo después: {args[1].lower()} {args[0]}")
            return 2
    orden, archivos = args[0].lower(), args[1:]
    if orden not in ORDENES:
        parecidas = difflib.get_close_matches(orden, ORDENES + ("ayuda", "guia", "consola"), 1)
        avisar(f"no conozco la orden '{args[0]}'" + (
            f", ¿quisiste decir '{parecidas[0]}'?" if parecidas
            else ". Las órdenes son: correr, probar, verificar, consola, guia y ayuda"))
        return 2
    if not archivos:
        avisar(f"a '{orden}' le falta el archivo, por ejemplo: {orden} hola.mate")
        return 2
    if orden == "probar" and (len(archivos) > 1 or os.path.isdir(archivos[0])):
        return probar_varios(archivos, [a for a in argv if a.startswith("-")], avisar)
    if len(archivos) > 1:
        avisar(f"'{orden}' lleva un solo archivo y recibió {len(archivos)}: "
               + ", ".join(archivos)
               + " (si el nombre tiene espacios, ponelo entre comillas)")
        return 2

    ruta, problema = _ubicar(archivos[0])
    if problema:
        avisar(problema)
        return 2
    donde["ruta"] = ruta
    if ruta.lower().endswith(".mate.txt"):
        avisar(f"aviso: {os.path.basename(ruta)} termina en .txt (se lo agregó el Bloc de "
               "notas). Lo corro igual; para que quede bien, al guardar elegí "
               "Tipo: Todos los archivos")

    mostrado = {}

    def reportar(linea, texto):
        cabecera, renglon, camino = error_escrito(ruta, linea, texto)
        archivo = getattr(linea, "archivo", None) or ruta
        avisar(cabecera)
        if renglon and (archivo, renglon) != mostrado.get("ultimo"):
            avisar(renglon)  # el mismo renglón no se repite si trae varios errores
        mostrado["ultimo"] = (archivo, renglon)
        if camino:
            avisar(camino)

    if simbolo("·→", ""):
        salida = print
    else:  # consola que no conoce esos símbolos: la traza se escribe con letras comunes
        def salida(texto):
            print(texto.replace("→", "->").replace("·", "-"))

    renglones = []  # la conversación, si va a un archivo

    def cerrar_conversacion():
        interprete = donde["interprete"]
        if not conversacion or interprete is None:
            return
        guardadas = donde.get("guardadas", [])
        problema = guardar_conversacion(conversacion, ruta, renglones, interprete.cuenta,
                                        sumar=bool(guardadas))
        if problema:
            avisar(problema)
        elif guardadas:
            print(f"La conversación se sumó a {conversacion}")
        else:
            print(f"La conversación quedó guardada en {conversacion}")
        guardadas.append(ruta)

    try:
        try:
            fuente = leer_fuente(ruta)
        except PermissionError:
            avisar(f"no pude abrir {ruta}: no tengo permiso para leerlo")
            return 2
        except OSError:
            avisar(f"no pude abrir {ruta}")
            return 2
        programa = analizar(fuente, ruta)
        errores = verificar(programa)
        if errores:
            for linea, texto in errores:
                reportar(linea, texto)
            return 1
        if orden == "verificar":
            print(f"{ruta}: sin errores")
            return 0
        interprete = donde["interprete"] = Interprete(
            salida=salida, traza="--traza" in opciones or bool(conversacion))
        if conversacion:
            interprete.anotar = renglones.append
        interprete.archivo = ruta
        interprete.separar_salida = orden == "probar"
        if "--sin-limite" in opciones:
            interprete.max_pasos = None
        resultados = interprete.correr(programa, pruebas=orden == "probar")
    except ErrorMate as e:
        # Primero lo que ya había fallado en los agentes: suele ser la causa del corte.
        for linea, texto in getattr(donde["interprete"], "errores_agentes_det", ()):
            reportar(linea, texto)
        if donde["interprete"] is not None:
            reportar(e.linea, donde["interprete"].con_camino(e.mensaje, e))
        else:
            reportar(e.linea, e.mensaje)
        avisar_pendientes(donde["interprete"], avisar)
        cerrar_conversacion()
        return 1

    cerrar_conversacion()
    if orden == "probar":
        if interprete.errores_principal:
            avisar("errores al correr el programa (antes de las pruebas):")
            for linea, texto in interprete.errores_principal:
                reportar(linea, texto)
        fallidas = 0
        bien, mal = simbolo("✓", "OK"), simbolo("✗", "FALLA")
        donde["pruebas"] = (0, len(resultados))
        if not resultados:
            print("este archivo no tiene pruebas. Una prueba se escribe así:  "
                  'prueba "suma bien" { asegurar 1 + 1 == 2 }' if not donde.get("varios")
                  else "  (sin pruebas)")
            return 1 if interprete.errores_principal else 0
        for (nombre, error), fallas, mostrado in zip(
                resultados, interprete.detalle_pruebas, interprete.mostrado_pruebas):
            print(f"  {mal if error else bien} {nombre}")
            for texto in mostrado:  # lo que la prueba mostró, debajo de su nombre
                for parte in str(texto).split("\n"):
                    print(f"      | {parte}")
            for linea, texto in fallas:
                # igual que con 'correr': archivo:renglón: error: ..., y el renglón debajo
                for parte in filter(None, error_escrito(ruta, linea, texto)):
                    for pedazo in parte.split("\n"):
                        print(f"      {pedazo}")
            fallidas += bool(error)
        donde["pruebas"] = (len(resultados) - fallidas, len(resultados))
        print(f"{len(resultados) - fallidas} de {len(resultados)} pruebas pasaron")
        return 1 if fallidas or interprete.errores_principal else 0
    for linea, texto in interprete.errores_agentes_det:
        reportar(linea, texto)
    return 1 if interprete.errores_agentes else 0


if __name__ == "__main__":
    sys.exit(main())
