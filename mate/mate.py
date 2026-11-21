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
    python3 mate.py corregir  archivo.mate Agente "la lección"   (y: lecciones, bitacora)
    python3 mate.py informe   (los errores de uso anotados; --para-mejorar, --borrar)
    python3 mate.py curso     (las clases para aprender Mate; curso 1 muestra la primera)
"""

import ast
import csv
import datetime
import decimal
import difflib
import io
import json
import math
import operator
import os
import re
import sys
import types
import unicodedata
from collections import deque

VERSION = "0.5"

# El tope para que Mate siga siendo chico (mejora 90): no puede haber más palabras propias
# ni más funciones incluidas que estas. Para agregar una hay que sacar otra, o discutir el
# tope. Y cada agregado lleva su renglón en el README y su prueba (las pruebas lo controlan).
TOPE_DE_PALABRAS = 40
# (En la 0.4 subió de 42 a 45, lo justo para que un agente aprenda: aprender, lecciones y
# consultas_ia. 'recordado' no gasta una palabra: solo vale después de 'estado'.)
# (En la 0.5 subió de 45 a 48, para trabajar con datos de verdad y charlar por teclado:
# leer_tabla, agregar_a_archivo y simular_teclado.)
# (Los frenos para la IA, el tope de gasto y las lecciones propuestas, también de la 0.5,
# no gastaron nada: 'frenos' solo vale dentro de un agente y seguida de una llave, y sus
# reglas (precios, prohibido, largo, reserva...) son nombres comunes en cualquier otro lado.)
TOPE_DE_FUNCIONES = 48

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
# Python más viejo se deja el tope de siempre (unas 180 llamadas; eran unas 120 hasta la
# 0.4, cuando cada llamada de Mate gastaba más niveles de Python).
NIVELES_DE_PYTHON = 30 * MAX_LLAMADAS if sys.version_info >= (3, 12) else 0

ORDENES = ("correr", "probar", "verificar")
# Las órdenes de lo que un agente aprende (0.4): llevan el programa y miran sus archivos
# de memoria y de bitácora, sin correrlo.
ORDENES_DE_MEMORIA = ("bitacora", "corregir", "lecciones", "propuestas", "proponer")
OPCIONES = ("--traza", "--depurar", "--sin-limite", "--version", "--ayuda",
            "--ia-simulada", "--olvidar", "--para-mejorar", "--sin-registro")
# El registro de errores de uso (0.4): lo que Mate anota de los errores que le muestra a
# la persona, para poder mejorar el lenguaje. Queda al lado de mate.py y no sale de ahí.
NOMBRE_DEL_REGISTRO = "errores_de_uso.txt"
MAX_REGISTRO = 500  # renglones que guarda (los últimos)
MINUTOS_SEGUIDO = 30  # el mismo error otra vez dentro de este rato cuenta como "seguido"
# Lo que un agente aprende (0.4). Las lecciones viajan en cada consulta a la IA, y eso se
# paga: por eso tienen tope de cantidad y de largo.
MAX_LECCIONES = 20  # por agente; si se pasa, se olvida la más vieja
LARGO_DE_LECCION = 300  # letras de una lección
MAX_BITACORA = 200  # renglones que guarda la bitácora de errores (los últimos)
TITULO_DE_LECCIONES = ("LECCIONES APRENDIDAS (correcciones que te hicieron antes: tenelas "
                       "siempre en cuenta)")

COMPARADORES = ("==", "!=", "<", "<=", ">", ">=")

# La tabla única de funciones incluidas: nombre -> (cuántos valores lleva como mínimo,
# como máximo, un ejemplo, qué hace). De acá salen el control de la cantidad de valores,
# el ejemplo de los errores, la lista de la guía y la tabla del README.
FUNCIONES = {
    "mostrar": (0, None, 'mostrar("Total:", total)', "escribe en pantalla"),
    "leer": (1, 2, 'leer("¿Cuántos?", "3")',
             "le pide un texto a la persona (en las pruebas da el 2.º valor)"),
    "simular_teclado": (1, 1, 'simular_teclado(["hola", "chau"])',
                        "solo en una prueba: lo que 'teclea' la persona en cada leer()"),
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
    "agregar_a_archivo": (2, 2, 'agregar_a_archivo("pedidos.txt", t)',
                          "suma el texto t como un renglón más al final de ese archivo"),
    "leer_tabla": (1, 1, 'leer_tabla("precios.csv")',
                   "la planilla guardada como CSV: una lista con un mapa por fila"),
    "mensajes_enviados": (0, 1, 'mensajes_enviados("Pedido")',
                          "solo en una prueba: los mensajes que se mandaron (o los de ese "
                          "tipo)"),
    "consultar_ia": (2, 3, "consultar_ia(reglas, duda)",
                     "lo que contesta una IA de verdad (Claude), como texto; es pago"),
    "simular_ia": (1, 1, 'simular_ia("Sale $ 100")',
                   "solo en una prueba: lo que contesta la IA desde ahí (o una lista)"),
    "aprender": (1, 2, 'aprender("Hoy no hay pan")',
                 "dentro de un agente: se anota esa lección, y no la olvida al terminar"),
    "lecciones": (0, 1, "lecciones()",
                  "dentro de un agente: la lista de sus lecciones (cada una es un texto)"),
    "consultas_ia": (0, 0, "consultas_ia()",
                     "solo en una prueba: lo que se le consultó a la IA, con las lecciones"),
}


def lista_de_funciones(formato_de_renglon="- {ejemplo:<27} {que}"):
    """Un renglón por función incluida, para la guía y para el README."""
    return "\n".join(formato_de_renglon.format(ejemplo=ejemplo, que=que)
                     for _, _, ejemplo, que in FUNCIONES.values())


# Las funciones incluidas que hacen algo además de devolver un valor: pueden ir solas
# en un renglón. Las demás, sueltas, no sirven de nada y Mate lo avisa.
HACEN_ALGO = ("mostrar", "leer", "escribir_archivo", "simular_ia", "aprender",
              "agregar_a_archivo", "simular_teclado")
# Las funciones que llegaron con la 0.4 y con la 0.5. Un programa de antes puede tener algo
# suyo con esos nombres ('sea lecciones = [...]'): se le deja, y en ese programa el nombre
# es suyo.
SE_PUEDEN_TAPAR = ("aprender", "lecciones", "consultas_ia",
                   "leer_tabla", "agregar_a_archivo", "simular_teclado")

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


def espera_otra_cantidad(nombre, minimo, maximo, recibe):
    """El error de una función propia llamada con valores de más o de menos. Si tiene
    parámetros con valor por defecto, dice entre cuántos y cuántos lleva."""
    espera = str(maximo) if minimo == maximo else f"entre {minimo} y {maximo}"
    return ESPERA_OTRA_CANTIDAD.format(n=nombre, espera=espera, recibe=recibe)
DEVOLVER_SUELTO = "'devolver' solo va dentro de una función"
SOLO_EN_PRUEBA = ("mensajes_enviados() solo va dentro de una prueba: es para comprobar "
                  "qué mensajes se mandaron")
SIMULAR_IA_SUELTO = ("simular_ia() solo va dentro de una prueba: fija lo que contesta la IA "
                     "mientras dura esa prueba. Para correr el programa sin la IA de verdad "
                     "está la opción --ia-simulada")
# Las funciones incluidas que solo sirven adentro de una prueba, y lo que se avisa si no.
CONSULTAS_IA_SUELTO = ("consultas_ia() solo va dentro de una prueba: es para comprobar qué se "
                       "le consultó a la IA (y con qué lecciones)")
SIMULAR_TECLADO_SUELTO = ("simular_teclado() solo va dentro de una prueba: fija lo que "
                          "'teclea' la persona en los leer() de esa prueba. Al correr el "
                          "programa de verdad, leer() espera el teclado")
SOLO_EN_PRUEBAS = {"mensajes_enviados": SOLO_EN_PRUEBA, "simular_ia": SIMULAR_IA_SUELTO,
                   "consultas_ia": CONSULTAS_IA_SUELTO,
                   "simular_teclado": SIMULAR_TECLADO_SUELTO}
SOLO_EN_AGENTE = ("{n}() solo va dentro de un agente: cada agente anota y lee sus propias "
                  "lecciones. Para corregirlo desde afuera, sin tocar el programa, está la "
                  "orden 'corregir'; y en una prueba se le dice a cuál: {n}({antes}Mostrador)")
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
    """Un número de línea que además recuerda de qué archivo salió. 'fin' es el renglón
    donde termina un texto de varios renglones (lo demás empieza y termina en el mismo)."""

    def __new__(cls, numero, archivo=None, fin=None):
        obj = super().__new__(cls, numero)
        obj.archivo = archivo
        obj.fin = fin
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


TRES_COMILLAS = '"""'
SIN_CERRAR_TEXTO = ("a este texto de varios renglones le falta el cierre: termina con tres "
                    'comillas, igual que empieza (""" ... """)')


_BARRA_Y_CIERRE = re.compile(r'(?<!\\)(?:\\\\)*\\"""[ \t\r]*$', re.M)


def comillas_de_mas(fuente, abierto):
    """Para el error de un texto de tres comillas sin cerrar: si en el archivo hay una
    cantidad impar de juegos de tres comillas (tres o más: se pegó un bloque dentro de
    otro), dice cuántos hay y en qué renglones. Con uno solo, o con cantidad par, nada."""
    renglones = []
    for tira in re.finditer(r'(?<!\\)"{3,}', fuente):
        renglones += [1 + fuente.count("\n", 0, tira.start())] * (len(tira.group()) // 3)
    if len(renglones) < 3 or len(renglones) % 2 == 0:
        return ""
    if len(renglones) <= 15:
        lista = ", ".join(str(r) for r in renglones[:-1]) + f" y {renglones[-1]}"
    else:
        lista = ", ".join(str(r) for r in renglones[:15]) + "..."
    return (f'. En este archivo hay {len(renglones)} juegos de tres comillas ("""), en los '
            f"renglones {lista}: es una cantidad impar, y como van de a pares (uno abre y "
            "otro cierra) sobra o falta uno. Suele pasar al pegar un bloque dentro de otro. "
            f"Leyendo de arriba para abajo, el que queda sin pareja es el del renglón "
            f"{int(abierto)}, pero el que sobra o el que falta puede estar más arriba")


class VariosRenglones(str):
    """El contenido de un texto de tres comillas, ya sin la sangría común. 'salto' dice
    cuántos renglones de arriba se le quitaron (para saber en qué renglón cae cada parte)."""
    salto = 0


def _fin_de_texto_largo(s, i):
    """s[i] abre un texto de tres comillas: devuelve dónde termina (después de las tres de
    cierre), o -1 si no cierra. Las comillas de adentro de una cuenta { } no cuentan."""
    i += 3
    while i < len(s):
        c = s[i]
        if c == "\\":
            i += 2
        elif s.startswith(TRES_COMILLAS, i):
            # Una tira de cuatro o más comillas: las de adelante son del texto y cierran
            # las últimas tres ("""Ella dijo "hola"""" termina en "hola").
            while s.startswith('"', i + 3):
                i += 1
            return i + 3
        elif c == "{":
            fin = _fin_de_llave(s, i)
            i = fin if fin > 0 else i + 1
        else:
            i += 1
    return -1


def sin_sangria(crudo):
    """Lo de adentro de un texto de tres comillas, para poder escribirlo prolijo dentro de
    un bloque: sin el renglón de las comillas que abren ni el de las que cierran (si no
    tienen nada más) y sin los espacios que todos los renglones tienen de más a la
    izquierda. Esa sangría común se mide en los renglones escritos y en el del cierre."""
    renglones = crudo.split("\n")
    varios = len(renglones) > 1
    salto = 0
    if varios and not renglones[0].strip():
        renglones.pop(0)
        salto = 1
    sangrias = []
    if varios and renglones and not renglones[-1].strip():
        sangrias.append(renglones.pop())  # el renglón del cierre no es parte del texto
    # (el primer renglón, si está pegado a las comillas que abren, no tiene sangría)
    desde = 0 if salto else 1
    for r in renglones[desde:]:
        if r.strip():
            sangrias.append(r[:len(r) - len(r.lstrip(" \t"))])
    comun = os.path.commonprefix(sangrias) if sangrias else ""
    for i in range(desde, len(renglones)):
        r = renglones[i]
        renglones[i] = r[len(comun):] if r.strip() else ""
    texto = VariosRenglones("\n".join(renglones))
    texto.salto = salto
    return texto


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
        if fuente.startswith(TRES_COMILLAS, pos):  # un texto de varios renglones
            fin = _fin_de_texto_largo(fuente, pos)
            if fin < 0:
                # (el renglón culpable suele estar más arriba: ese texto "cerró" recién
                # en las comillas que abrían el siguiente)
                barra = _BARRA_Y_CIERRE.search(fuente)
                if barra:  # el renglón termina en \""": la barra se "come" una comilla
                    raise ErrorMate(
                        'este renglón termina en \\""": la barra hace que la primera comilla '
                        "sea parte del texto, y para el cierre quedan dos en vez de tres. "
                        "Poné las tres comillas del cierre solas, en el renglón de abajo",
                        Linea(1 + fuente.count("\n", 0, barra.start()), archivo))
                error = ErrorMate(SIN_CERRAR_TEXTO + comillas_de_mas(fuente, linea), linea)
                error.texto_abierto = True  # (en la consola: se sigue en el renglón de abajo)
                raise error
            saltos = fuente.count("\n", pos, fin)
            tokens.append(("str", sin_sangria(fuente[pos + 3:fin - 3]),
                           Linea(linea, archivo, fin=linea + saltos)))
            linea = Linea(linea + saltos, archivo)
            pos = fin
            continue
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


class EstadoRecordado(tuple):
    """Un 'estado recordado' de un agente: (renglón, nombre, valor inicial), igual que
    cualquier estado, pero se guarda al terminar y se recupera en la próxima corrida."""


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
        if tk[1] in incluidas() and tk[1] not in SE_PUEDEN_TAPAR:
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
        """El renglón donde terminó lo último que se leyó."""
        linea = self.t[self.i - 1][2] if self.i else 0
        return getattr(linea, "fin", None) or linea

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
                # usar python "ayudas.py": trae funciones escritas en Python (0.5). 'python'
                # no es una palabra reservada: solo significa algo acá, antes de un texto.
                if self.es("id", "python"):
                    self.tomar()
                    return ("usar_python", ln, self.espera(
                        "str", que="el nombre del archivo de Python entre comillas (usar "
                                   'python "ayudas.py")')[1])
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
        # Los parámetros con valor por defecto (tasa = 0.21) van al final y quedan
        # anotados aparte: [(nombre, valor)].
        params, defectos = [], []
        self.abiertos += 1
        while not self.es("op", ")"):
            parametro = self.nombre_nuevo("un parámetro")
            if self.acepta("op", "="):
                defectos.append((parametro, self.expr()))
            elif defectos:
                raise ErrorMate(
                    f"{nombre}(): '{parametro}' no tiene valor por defecto y está después "
                    f"de '{defectos[-1][0]}', que sí tiene. Los parámetros con valor por "
                    f"defecto van al final: {nombre}({parametro}, {defectos[-1][0]} = ...)",
                    self.linea_previa())
            params.append(parametro)
            if not self.acepta("op", ","):
                break
        self.abiertos -= 1
        self.espera("op", ")")
        self.en_funcion += 1
        try:
            cuerpo = self.aparte()
        finally:
            self.en_funcion -= 1
        return ("funcion", ln, nombre, params, cuerpo, defectos)

    def mensaje(self):
        ln = self.tomar()[2]
        nombre = self.nombre_propio("mensaje")
        campos, reglas = [], {}  # reglas: campo -> lo que dice de sus valores
        # La llave también puede venir en el renglón de abajo: un renglón nunca empieza
        # con '{' por otro motivo.
        if self.es("op", "{"):
            self.tomar()
            while not self.es("op", "}"):
                campo = self.nombre_de_campo()
                self.espera("op", ":")
                tipo = self.tipo_de_campo()
                opcional = bool(self.acepta("op", "?"))
                regla = self.regla_de_campo(f"{nombre}.{campo}", tipo, opcional)
                if regla:
                    reglas[campo] = regla
                # Un campo con valor por defecto puede faltar: toma ese valor.
                campos.append((campo, tipo, opcional or "defecto" in regla))
                if not self.acepta("op", ","):
                    break
            self.espera("op", "}")
        responde = None  # mensaje Pedido { ... } responde Cotizacion
        if self.es("id", "responde") and self.ver()[2] == self.linea_previa():
            self.tomar()
            responde = self.tipo_de_campo()
        return ("mensaje", ln, nombre, campos, responde, reglas)

    def regla_de_campo(self, donde, tipo, opcional):
        """Lo que un campo dice de sus valores, después del tipo y en el mismo renglón:
        'desde 1 hasta 100', 'en ["baja", "alta"]' y '= valor por defecto'. Todo escrito
        a mano, así se puede revisar antes de correr. Devuelve un mapa (vacío si no hay)."""
        regla = {}

        def sigue(tipo_de_token, palabra):
            return self.es(tipo_de_token, palabra) and self.ver()[2] == self.linea_previa()

        def escrito(que, ejemplo):
            ln = self.ver()[2]
            if self.es("op", "}") or self.es("op", ",") or self.es("eof"):
                raise ErrorMate(f"{donde}: después de {que} falta el valor, por ejemplo: "
                                f"{ejemplo}", self.linea_previa())
            hay, valor = valor_escrito(self.suma())
            if not hay:
                raise ErrorMate(
                    f"{donde}: después de {que} va un valor escrito a mano (no una cuenta "
                    f"ni una variable), por ejemplo: {ejemplo}", ln)
            return valor

        for palabra in ("desde", "hasta"):
            if sigue("id", palabra):
                ln = self.tomar()[2]
                valor = escrito(f"'{palabra}'", "cantidad: numero desde 1 hasta 100")
                if not es_num(valor):
                    raise ErrorMate(f"{donde}: después de '{palabra}' va un número, y hay "
                                    f"{un(valor)}", ln)
                regla[palabra] = valor
        if sigue("kw", "en"):
            ln = self.tomar()[2]
            ejemplo = 'prioridad: texto en ["baja", "media", "alta"]'
            opciones = escrito("'en'", ejemplo)
            if not isinstance(opciones, list) or not opciones:
                raise ErrorMate(f"{donde}: después de 'en' va la lista de las opciones que "
                                f"valen, por ejemplo: {ejemplo}", ln)
            regla["en"] = opciones
        ln = self.ver()[2]
        if ("desde" in regla or "hasta" in regla) and tipo != "numero":
            raise ErrorMate(f"{donde}: 'desde' y 'hasta' solo van en un campo de tipo "
                            f"numero, y este es de tipo {tipo}", self.linea_previa())
        if "desde" in regla and "hasta" in regla and regla["desde"] > regla["hasta"]:
            raise ErrorMate(
                f"{donde}: 'desde {formato(regla['desde'])}' es más que 'hasta "
                f"{formato(regla['hasta'])}', así que ningún valor podría cumplirlo",
                self.linea_previa())
        if "en" in regla:
            if len(regla) > 1:
                raise ErrorMate(f"{donde}: o va un rango ('desde', 'hasta') o va la lista "
                                "de opciones ('en'), no las dos cosas", self.linea_previa())
            if tipo not in ("numero", "texto"):
                raise ErrorMate(f"{donde}: las opciones con 'en' solo van en un campo de "
                                f"tipo texto o numero, y este es de tipo {tipo}",
                                self.linea_previa())
            for opcion in regla["en"]:
                if nombre_tipo(opcion) != tipo:
                    raise ErrorMate(
                        f"{donde} es de tipo {tipo}, y entre sus opciones está "
                        f"{formato(opcion, False)}, que es {un(opcion)}", self.linea_previa())
        if sigue("op", "="):
            self.tomar()
            valor = escrito("'='", 'prioridad: texto = "media"')
            if opcional:
                raise ErrorMate(
                    f"{donde}: un campo con valor por defecto ya puede faltar (toma ese "
                    "valor): sacale el '?'", ln)
            if not cumple_tipo(valor, tipo):
                raise ErrorMate(f"{donde} es de tipo {tipo}, y su valor por defecto es "
                                f"{un(valor)}: {formato(valor, False)}", ln)
            rota = rompe_regla(donde, valor, regla)
            if rota:
                raise ErrorMate(f"el valor por defecto no cumple su propia regla: {rota}", ln)
            regla["defecto"] = valor
        if self.ver()[2] == self.linea_previa() and (
                self.es("op", "=") or self.es("kw", "en")
                or (self.es("id") and self.ver()[1] in ("desde", "hasta"))):
            raise ErrorMate(f"{donde}: las reglas van en este orden: primero 'desde', "
                            "después 'hasta' (o 'en [...]') y al final '= valor'. Por "
                            "ejemplo: cantidad: numero desde 1 hasta 100 = 1", ln)
        return regla

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
        estados, manejadores, funciones, frenos = [], [], [], []
        self.en_agente += 1
        try:
            self.miembros_de_agente(estados, manejadores, funciones, frenos, nombre)
        finally:
            self.en_agente -= 1
        return ("agente", ln, nombre, estados, manejadores, funciones, frenos)

    def frenos(self, nombre_del_agente, frenos):
        """frenos { precios: lista  reserva: "..." }: las reglas que Mate comprueba sobre
        cada respuesta de consultar_ia() de ese agente (0.5). 'frenos' no es una palabra
        reservada: solo significa esto dentro de un agente y seguida de una llave."""
        ln = self.tomar()[2]
        if frenos:
            raise ErrorMate(f"{nombre_del_agente} ya tiene sus 'frenos' (línea "
                            f"{frenos[0][0]}): van todos juntos, en un solo bloque", ln)
        self.espera("op", "{")
        while not self.acepta("op", "}"):
            tk = self.tomar()
            if tk[0] == "eof":
                raise ErrorMate("a los 'frenos' les falta la llave de cierre }", ln)
            if tk[0] not in ("id", "kw") or not self.es("op", ":"):
                raise ErrorMate(
                    "dentro de 'frenos' va una regla por renglón, con su nombre, dos puntos "
                    f"y el valor (por ejemplo  largo: 400). Las reglas son: {REGLAS_EN_LISTA}",
                    tk[2])
            if tk[1] not in REGLAS_DE_FRENO:
                raise ErrorMate(con_sugerencia(
                    f"'{tk[1]}' no es una regla de 'frenos'", tk[1], REGLAS_DE_FRENO)
                    + f". Las reglas son: {REGLAS_EN_LISTA}", tk[2])
            if any(tk[1] == regla for _, regla, _ in frenos):
                raise ErrorMate(f"la regla '{tk[1]}' está dos veces en los frenos de "
                                f"{nombre_del_agente}: va una sola", tk[2])
            self.tomar()
            if self.es("op", "}") or self.ver()[2] != tk[2]:
                raise ErrorMate(f"a la regla '{tk[1]}' le falta el valor, en el mismo "
                                f"renglón: {REGLAS_DE_FRENO[tk[1]][1]}", tk[2])
            frenos.append((tk[2], tk[1], self.expr()))
            self.acepta("op", ",")
        if not frenos:
            raise ErrorMate("estos 'frenos' están vacíos: poneles al menos una regla, por "
                            f"ejemplo  {REGLAS_DE_FRENO['largo'][1]}", ln)

    def miembros_de_agente(self, estados, manejadores, funciones, frenos, nombre):
        while not self.acepta("op", "}"):
            tk = self.ver()
            if tk[:2] == ("id", "frenos") and self.es("op", "{", d=1):
                self.frenos(nombre, frenos)
            elif self.acepta("kw", "estado"):
                # 'estado recordado atendidos = 0': ese dato vuelve en la próxima corrida.
                # 'recordado' no es una palabra reservada: 'estado recordado = 5' sigue
                # siendo un estado que se llama así.
                clase = tuple
                if self.es("id", "recordado") and not self.es("op", "=", d=1):
                    self.tomar()
                    clase = EstadoRecordado
                n = self.nombre_nuevo()
                self.espera("op", "=")
                estados.append(clase((tk[2], n, self.expr())))
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
                    "dentro de un agente solo van 'estado', 'al recibir', 'funcion' y "
                    "'frenos'" if tk[:2] == ("id", "frenos") or self.es("op", ":", d=1)
                    else "dentro de un agente solo van 'estado', 'al recibir' y 'funcion'",
                    tk[2])

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
        # Si es de varios renglones: cuántos se le sacaron arriba, para saber en qué
        # renglón cae cada cuenta { }.
        salto, inicio = getattr(crudo, "salto", None), ln
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
                if salto is not None:
                    ln = Linea(inicio + salto + crudo.count("\n", 0, i),
                               getattr(inicio, "archivo", None))
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
            return ("str", inicio, "".join(partes))
        return ("interp", inicio, partes)


def renglon_sin_uso(e):
    """El error de un renglón que solo calcula un valor y no hace nada con él."""
    pista = ""
    if e[0] == "neg":
        pista = (". Si era la continuación de la cuenta de arriba, dejá el '-' al "
                 "final de ese renglón")
    return ErrorMate("este renglón calcula un valor y no hace nada con él: guardalo "
                     f"(sea x = ...), mostralo con mostrar(...) o borralo{pista}", e[1],
                     clase="escritura")


def es_de_excel(ruta):
    """¿Ese archivo es una planilla de Excel (.xlsx o .xls) y no un texto?"""
    try:
        with open(ruta, "rb") as f:
            return f.read(4) in (b"PK\x03\x04", b"\xd0\xcf\x11\xe0")
    except OSError:
        return False


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


# Lo que a veces queda pegado adentro de un archivo .mate: la pantalla de PowerShell
# ("PS C:\Users\...> ") o el comando con el que se corre Mate.
_PANTALLA_PEGADA = re.compile(r"\s*PS\s+[A-Za-z]:[\\/][^>\n]*>")
_COMANDO_PEGADO = re.compile(
    r"\s*(?:(?:python3?|py)(?:\.exe)?\s+(?:-\S+\s+)*\S*mate\.py\b"
    r"|notepad(?:\.exe)?\s+\S"
    r"|(?:\.[\\/])?mate(?:\.bat)?\s+(?:correr|probar|verificar|consola|guia|ayuda|informe"
    r"|corregir|lecciones|bitacora)\b"
    r"|cd\s+[\w.\\/:~-]+\s*$)", re.I)
PEGADO_EN_EL_ARCHIVO = {
    "pantalla": ('este renglón no es de Mate: es la pantalla de PowerShell (empieza con '
                 '"PS C:\\..."). Parece que se pegó la pantalla adentro del archivo. Abrilo '
                 "con el Bloc de notas, borrá todo lo que no sea del programa y guardá"),
    "comando": ("este renglón no es de Mate: es un comando de PowerShell. Parece que el "
                "comando se pegó adentro del archivo. Abrilo con el Bloc de notas, borrá ese "
                "renglón y guardá: los comandos se escriben en la ventana de PowerShell, no "
                "en el programa"),
}


def pegado_de_powershell(renglon):
    """¿Ese renglón es la pantalla de PowerShell ("pantalla"), un comando ("comando") o
    ninguna de las dos (None)?"""
    if _PANTALLA_PEGADA.match(renglon):
        return "pantalla"
    return "comando" if _COMANDO_PEGADO.match(renglon) else None


def revisar_pegado(fuente, archivo=None):
    """Si el primer renglón escrito del archivo es de PowerShell, lo dice claro."""
    primero = re.match(r"\s*([^\n]*)", fuente)
    que = pegado_de_powershell(primero.group(1))
    if que:
        raise ErrorMate(PEGADO_EN_EL_ARCHIVO[que],
                        Linea(1 + fuente.count("\n", 0, primero.start(1)), archivo))


def analizar(fuente, ruta=None, _vistos=None, en_consola=False):
    """Convierte el texto en un programa, incluyendo lo que traiga con 'usar'."""
    vistos = _vistos if _vistos is not None else set()
    if ruta:
        vistos.add(os.path.realpath(ruta))
    carpeta = os.path.dirname(os.path.abspath(ruta)) if ruta else os.getcwd()
    programa = []
    if not en_consola:
        revisar_pegado(fuente, ruta)
    tokens = tokenizar(fuente, ruta)
    revisar_cierres(tokens, fuente)
    for s in Parser(tokens, en_consola).programa():
        if s[0] == "usar_python":
            try:
                nombre, archivo = archivo_de_python(carpeta, s[2])
            except ErrorMate as e:
                e.linea = e.linea or s[1]
                raise
            if "python:" + os.path.realpath(archivo) not in vistos:  # una vez alcanza
                vistos.add("python:" + os.path.realpath(archivo))
                programa.append(("usar_python", s[1], nombre, archivo))
            continue
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
                        if x[0] in ("mensaje", "agente", "funcion", "sea", "usar_python"))
    return programa


def archivo_de_python(carpeta, escrito):
    """De 'usar python "ayudas.py"': (el nombre con que se usa en el programa, la ruta del
    archivo). El archivo tiene que estar en la carpeta del programa (o en una de adentro)
    y llamarse como una variable de Mate, porque después se escribe ayudas.algo(...)."""
    ejemplo = 'usar python "ayudas.py"'
    partes = [p for p in re.split(r"[\\/]", escrito.strip()) if p not in ("", ".")]
    if not partes or not partes[-1].lower().endswith(".py") or len(partes[-1]) < 4:
        raise ErrorMate(f"'usar python' trae un archivo de Python, y su nombre termina en "
                        f'.py; acá dice "{escrito}". Por ejemplo: {ejemplo}')
    afuera = ErrorMate(
        f"'usar python' solo trae archivos de la carpeta del programa ({carpeta}), y "
        f'"{escrito}" queda afuera. Copiá el archivo a esa carpeta y nombralo sin la '
        f'ruta: usar python "{partes[-1]}"', familia="archivo")
    if ".." in partes or escrito.strip()[:1] in ("/", "\\") or re.match(r"[A-Za-z]:", partes[0]):
        raise afuera
    nombre = partes[-1][:-3]
    if not nombre.isidentifier() or nombre != nombre.lower() or nombre in PALABRAS \
            or nombre in FUNCIONES:
        porque = ("es una palabra de Mate" if nombre in PALABRAS else
                  "es una función incluida de Mate" if nombre in FUNCIONES else
                  "tiene mayúsculas, espacios, guiones o empieza con un número")
        raise ErrorMate(
            f"el nombre de un archivo de Python es el que después se escribe en el programa "
            f"(ayudas.py se usa así: ayudas.algo(...)), y '{nombre}' no sirve: {porque}. "
            "Renombrá el archivo con minúsculas, números y guion bajo, por ejemplo "
            "mis_ayudas.py")
    ruta = os.path.join(carpeta, *partes)
    try:  # (un acceso directo que lleva afuera de la carpeta tampoco vale)
        adentro = os.path.normcase(os.path.commonpath(
            [os.path.realpath(carpeta), os.path.realpath(ruta)])) \
            == os.path.normcase(os.path.realpath(carpeta))
    except ValueError:  # en Windows, si está en otro disco
        adentro = False
    if not adentro:
        raise afuera
    if os.path.isfile(ruta):
        return nombre, ruta
    donde = os.path.dirname(ruta)
    pista = ""
    if os.path.isfile(ruta + ".txt"):
        pista = (f". Encontré {partes[-1]}.txt: el Bloc de notas le agregó .txt; renombralo, "
                 "o al guardar elegí Tipo: Todos los archivos")
    elif not os.path.isdir(donde):
        pista = ". Esa carpeta no existe"
    else:
        try:
            hay = sorted(a for a in os.listdir(donde) if a.lower().endswith(".py"))
        except OSError:
            hay = []
        parecido = difflib.get_close_matches(partes[-1], hay, n=1, cutoff=0.75)
        if parecido:
            pista = f". ¿Quisiste decir '{parecido[0]}'?"
        elif hay:
            pista = (". Los archivos .py que hay ahí: " + ", ".join(hay[:10])
                     + (", ..." if len(hay) > 10 else ""))
    raise ErrorMate(f"no encuentro el archivo de Python '{escrito}' (lo busqué en {donde})"
                    + pista, familia="archivo")


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
        elif _es_nodo(n, "funcion", 6):
            anotar(n[2])
            for parametro in n[3]:
                anotar(parametro)
        elif _es_nodo(n, "usar_python", 4):
            anotar(n[2])
        elif _es_nodo(n, "intentar", 5):
            anotar(n[3])
        elif _es_nodo(n, "simular", 6):
            anotar(n[4])
        elif _es_nodo(n, "agente", 7):
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


def valor_escrito(e):
    """Si eso es un valor escrito a mano (un número, un texto sin cuentas adentro,
    verdadero, falso o una lista de esos), (verdadero, el valor); si no, (falso, nada)."""
    if e[0] in ("num", "str", "bool"):
        return True, e[2]
    if e[0] == "neg" and e[2][0] == "num":
        return True, -e[2][2]
    if e[0] == "lista":
        valores = [valor_escrito(x) for x in e[2]]
        if all(hay for hay, _ in valores):
            return True, [v for _, v in valores]
    return False, None


def cumple_tipo(valor, tipo):
    """¿Ese valor es del tipo que pide el contrato? (numero, texto, lista de numero...)"""
    if tipo == "cualquiera":
        return True
    if tipo.startswith("lista de "):
        return isinstance(valor, list) and all(
            cumple_tipo(x, tipo[len("lista de "):]) for x in valor)
    return nombre_tipo(valor) == tipo


def rompe_regla(donde, valor, regla, _por_el_resto=False):
    """Si ese valor no cumple lo que el mensaje dice de ese campo (mejora 97), el texto del
    error, con el campo, el valor y la regla; si la cumple, None. Es el mismo texto antes
    de correr y al armar el mensaje."""
    if valor is None or not regla:
        return None
    no_puede = f"{donde} no puede valer {formato(valor, False)}"
    if type(valor) is float and math.isfinite(valor) and not _por_el_resto:
        # 0.1 + 0.2 se muestra 0.3 pero guarda 0.30000000000000004: si lo que se ve sí
        # cumple la regla, el error muestra el valor de verdad y dice cómo arreglarlo.
        rota = rompe_regla(donde, valor, regla, True)
        if rota and rompe_regla(donde, float(formato(valor)), regla, True) is None:
            return (rota.replace(no_puede, f"{donde} no puede valer {valor!r}", 1).rstrip(".")
                    + f". Se muestra {formato(valor)}, pero las cuentas con decimales "
                    "dejan un resto minúsculo: redondeá el valor antes de ponerlo en el "
                    "mensaje, por ejemplo redondear(valor, 2)")
        return rota
    if "en" in regla:
        if any(igual(valor, opcion) for opcion in regla["en"]):
            return None
        opciones = ", ".join(formato(opcion, False) for opcion in regla["en"])
        parecida = sugerir(valor, regla["en"]) if isinstance(valor, str) else ""
        return (f"{no_puede}: el mensaje dice que tiene que ser una de estas opciones: "
                f"{opciones}." + parecida.replace("'", '"'))
    desde, hasta = regla.get("desde"), regla.get("hasta")
    if not es_num(valor) or ((desde is None or valor >= desde)
                             and (hasta is None or valor <= hasta)):
        return None
    if desde is not None and hasta is not None:
        return (f"{no_puede}: el mensaje dice 'desde {formato(desde)} hasta "
                f"{formato(hasta)}', así que tiene que estar entre {formato(desde)} y "
                f"{formato(hasta)}")
    if desde is not None:
        return (f"{no_puede}: el mensaje dice 'desde {formato(desde)}', así que tiene que "
                f"ser {formato(desde)} o más")
    return (f"{no_puede}: el mensaje dice 'hasta {formato(hasta)}', así que tiene que ser "
            f"{formato(hasta)} o menos")


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
    arriba = set(FUNCIONES) | {s[2] for s in programa
                               if s[0] in ("sea", "funcion", "agente", "usar_python")}
    tapadas = set(SE_PUEDEN_TAPAR) & set(_ligaduras(programa))  # nombres que el programa usa
    # Las funciones propias que seguro son esa función donde se las nombre: las de un
    # nombre que en todo el programa se le pone a una sola cosa.
    cuantos_lleva = {}

    def juntar_funciones(n):
        if isinstance(n, list):
            for x in n:
                juntar_funciones(x)
        elif isinstance(n, tuple):
            if _es_nodo(n, "funcion", 6) and isinstance(n[3], list) and veces.get(n[2]) == 1:
                cuantos_lleva[n[2]] = (len(n[3]) - len(n[5]), len(n[3]))
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
        # Un valor por defecto ve lo de afuera y los parámetros que están antes que él.
        for parametro, e in s[5]:
            valor(e, alcance + [set(s[3][:s[3].index(parametro)])])
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
            for _, _, regla in s[6]:  # los frenos ven el estado y las funciones del agente
                valor(regla, adentro)
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
            if nombre in FUNCIONES and nombre not in tapadas:  # (las demás no se tapan)
                texto = cantidad_equivocada(nombre, len(e[3]))
            elif nombre in cuantos_lleva and not (
                    cuantos_lleva[nombre][0] <= len(e[3]) <= cuantos_lleva[nombre][1]):
                texto = espera_otra_cantidad(nombre, *cuantos_lleva[nombre], len(e[3]))
            if texto:
                errores.append((e[1], texto))

    for s in programa:
        sentencia(s, [arriba])
    return errores


def revisar_python(programa, veces):
    """Lo que se puede saber de un archivo traído con 'usar python' SIN ejecutarlo: si
    Python lo puede leer, y si tiene las funciones que el programa le pide. Devuelve
    [(linea, texto)]. (Que el archivo exista ya lo controló 'analizar'.)"""
    errores, tienen = [], {}
    for s in programa:
        if s[0] != "usar_python":
            continue
        archivo = os.path.basename(s[3])
        try:
            arbol = ast.parse(leer_fuente(s[3]))
        except SyntaxError as e:
            donde = f" en su línea {e.lineno}" if e.lineno else ""
            errores.append((s[1], f"{archivo} está mal escrito{donde} y Python no lo pudo "
                                  f"leer. Python dice: {recortado(e.msg or 'SyntaxError', 300)}"))
            continue
        except (OSError, ValueError, ErrorMate, RecursionError, MemoryError):
            continue  # no se pudo mirar: si hay un problema, lo dirá al correr
        # Los nombres que el archivo define arriba de todo (con 'def' o con '='): si el
        # programa pide otro, seguro que no está. No se entra en las funciones ni clases.
        nombres, pendientes = set(), list(arbol.body)
        while pendientes:
            n = pendientes.pop()
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                nombres.add(n.name)
            elif isinstance(n, ast.ClassDef):
                pass
            else:
                nombres.update(x.id for x in ast.walk(n)
                               if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Store))
                pendientes += [x for x in ast.iter_child_nodes(n) if isinstance(x, ast.stmt)]
        if veces.get(s[2]) == 1:  # (si otra cosa se llama igual, no se sabe cuál es cuál)
            tienen[s[2]] = (archivo, {n for n in nombres if not n.startswith("_")})
    avisados = set()

    def visitar(n):
        if isinstance(n, (list, tuple)):
            if (_es_nodo(n, "campo", 4) and _es_nodo(n[2], "nombre", 3) and n[2][2] in tienen
                    and (n[2][2], n[3]) not in avisados):
                archivo, nombres = tienen[n[2][2]]
                if n[3] not in nombres:
                    avisados.add((n[2][2], n[3]))
                    errores.append((n[1], no_esta(
                        f"{archivo} no tiene una función '{n[3]}'", n[3], sorted(nombres))
                        if nombres else
                        f"{archivo} no tiene ninguna función para usar desde Mate: se ven "
                        "las que están escritas ahí con 'def' y no empiezan con guion bajo"))
            # (como con los nombres: adentro de 'intentar' y de 'asegurar falla' no se mira)
            if _es_nodo(n, "intentar", 5):
                n = n[4]
            elif _es_nodo(n, "asegurar_falla", 4):
                return
            for x in n:
                visitar(x)

    if tienen:
        visitar(programa)
    return errores


def verificar(programa, en_consola=False):
    """Revisa el programa antes de correr: los contratos de los mensajes, los nombres que
    no existen y lo demás que se puede saber sin ejecutarlo. Devuelve [(linea, texto)].
    en_consola: ahí no se avisa de los nombres que faltan (ver revisar_nombres)."""
    errores = []
    mensajes, agentes, estados = {}, {}, {}
    declarados = {}  # la declaración completa de cada agente
    veces = _ligaduras(programa)
    errores += revisar_python(programa, veces)
    # Funciones que seguro son funciones donde se las nombre: las incluidas y las del
    # nivel superior cuyo nombre no se repite.
    funciones = (set(incluidas()) - set(veces)) | {
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
            # Los frenos (0.5): un valor escrito que no es del tipo de su regla, y las
            # reglas que miran la respuesta sin un texto de 'reserva' para cuando saltan.
            for ln, regla, e in s[6]:
                escrito = "nada" if e[0] == "nada" else _LITERALES.get(e[0])
                if escrito and escrito not in REGLAS_DE_FRENO[regla][0]:
                    errores.append((ln, (
                        f"en los frenos de {s[2]}, '{regla}' no lleva "
                        f"{_CON_ARTICULO[escrito]}: son "
                        f"{REGLAS_DE_FRENO[regla][2]}. Por ejemplo:  "
                        f"{REGLAS_DE_FRENO[regla][1]}")))
            reglas = [regla for _, regla, _ in s[6]]
            if "reserva" not in reglas and any(r in REGLAS_DE_CONTENIDO for r in reglas):
                errores.append((s[6][0][0], (
                    f"a los frenos de {s[2]} les falta 'reserva': lo que contesta el agente "
                    "cuando la IA rompe una regla dos veces seguidas. Por ejemplo:  "
                    f"{REGLAS_DE_FRENO['reserva'][1]}")))
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

    def visitar(n, ag=None, atajado=False):
        """atajado: adentro de 'intentar { }' o de 'asegurar falla { }'. Ahí un valor que
        no cumple la regla de su campo (mejora 97) no frena el programa antes de correr:
        es la falla que se ataja, o justo la que se quiere probar."""
        if isinstance(n, list):
            for x in n:
                visitar(x, ag, atajado)
            return
        if not isinstance(n, tuple):
            return
        if _es_nodo(n, "agente", 7):
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
                    else:  # un valor escrito a mano que no cumple la regla del campo
                        hay, valor = valor_escrito(e)
                        rota = hay and not atajado and rompe_regla(f"{nombre}.{k}", valor,
                                                   mensajes[nombre][5].get(k))
                        if rota:
                            errores.append((ln, rota))
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
        elif _es_nodo(n, "funcion", 6) and isinstance(n[3], list):
            for k in repetidos(n[3]):
                errores.append((n[1], f"{n[2]}(): el parámetro '{k}' está repetido"))
        elif (_es_nodo(n, "yo", 2) or _es_nodo(n, "remitente", 2)) and ag is None:
            que = ("el agente que está atendiendo" if n[0] == "yo"
                   else "quien le mandó el mensaje que está atendiendo")
            errores.append((n[1], f"'{n[0]}' solo existe dentro de un agente (es {que}); "
                                  "acá afuera no hay ninguno"))
        if _es_nodo(n, "intentar", 5) or _es_nodo(n, "asegurar_falla", 4):
            visitar(n[2], ag, True)
            for x in n[3:]:  # (el 'si falla' y el texto esperado se miran como siempre)
                visitar(x, ag, atajado)
            return
        for x in n:
            visitar(x, ag, atajado)

    def fuera_de_prueba(n):
        """mensajes_enviados() o simular_ia() escritos en el programa o en un agente."""
        if isinstance(n, (list, tuple)):
            if (_es_nodo(n, "llamar", 4) and _es_nodo(n[2], "nombre", 3)
                    and n[2][2] in SOLO_EN_PRUEBAS and n[2][2] not in veces):
                errores.append((n[1], SOLO_EN_PRUEBAS[n[2][2]]))
            for x in n:
                fuera_de_prueba(x)

    visitar(programa)
    # (una función suelta sí puede usarla: quizá es una ayuda que llaman las pruebas)
    fuera_de_prueba([s for s in programa if s[0] not in ("prueba", "funcion")])
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


class TextoDeError(str):
    """El texto del error de un agente, que además recuerda de qué familia era (para el
    registro de errores de uso: lo que el programa dijo con 'fallar' no se anota)."""
    familia = "otro"


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
        self.recuerda = True  # una copia sin nombre ('crear' sin 'llamado') no tiene memoria
        self.lecciones = []  # [{"fecha", "texto"}]: nunca se cambia, se reemplaza por otra
        # Lo de la 0.5, solo en los agentes declarados (sus copias usan lo del original):
        self.propuestas = []  # lecciones propuestas, sin aprobar: [{"fecha", "texto", "motivo"}]
        self.gasto = {}  # la cuenta de consultas: {"2026-11-21": {"consultas", "simuladas", "tokens"}}


class Funcion:
    def __init__(self, nombre, params, cuerpo, env, defectos=()):
        self.nombre, self.params, self.cuerpo, self.env = nombre, params, cuerpo, env
        self.defectos = defectos  # [(parámetro, valor por defecto)]: son los últimos
        self.armado = None  # el cuerpo listo para correr: se arma en la primera llamada
        self.directa = None  # si sus parámetros se anotan sin más controles (ver llamar)


class Nativa:
    def __init__(self, nombre, fn):
        self.nombre, self.fn = nombre, fn


class DePython(Nativa):
    """Una función escrita en Python, traída con 'usar python' (0.5). Se llama como
    cualquier otra; un renglón que solo la llama vale, porque puede estar haciendo algo."""


class ModuloPython:
    """Un archivo .py traído con 'usar python "ayudas.py"': sus funciones se llaman
    ayudas.nombre(...). No es un dato: no viaja en mensajes ni se guarda."""

    def __init__(self, nombre, archivo, funciones):
        self.nombre, self.archivo, self.funciones = nombre, archivo, funciones

    def __str__(self):
        return f"<python {os.path.basename(self.archivo)}>"

    def funcion(self, nombre):
        if nombre in self.funciones:
            return self.funciones[nombre]
        archivo = os.path.basename(self.archivo)
        if not self.funciones:
            raise ErrorMate(f"{archivo} no tiene ninguna función para usar desde Mate: se "
                            "ven las que están escritas ahí con 'def' y no empiezan con "
                            "guion bajo", familia="python")
        if nombre.startswith("_"):
            raise ErrorMate(f"'{nombre}' empieza con guion bajo, y esas funciones de "
                            f"{archivo} no se ven desde Mate: en Python así se marcan las "
                            "que son de uso interno", familia="python")
        raise ErrorMate(no_esta(f"{archivo} no tiene una función '{nombre}'", nombre,
                                self.funciones), familia="python")


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


# Lo que devuelve una sentencia ya armada cuando corta el camino (ver Interprete._paso):
# 'romper', 'continuar' o, si fue un 'devolver', una tupla con el valor.
_ROMPER, _CONTINUAR = object(), object()
_SIN_VALOR = (None,)  # un 'devolver' solo
# Lo que puede fallar dentro de una sentencia y Mate explica con su renglón.
_SE_EXPLICAN = (ErrorMate, RecursionError, MemoryError)
# Una cuenta entre enteros más chicos que esto no puede pasar ningún tope: va directo.
_CHICO = 1 << 62
_CUENTAS = {"+": operator.add, "-": operator.sub, "*": operator.mul}
_COMPARACIONES = {"==": operator.eq, "!=": operator.ne, "<": operator.lt,
                  "<=": operator.le, ">": operator.gt, ">=": operator.ge}
_finito = math.isfinite


def condicion_rara(v, linea=None):
    """El error de una condición que no dio ni verdadero ni falso."""
    return ErrorMate("la condición tiene que ser verdadero o falso, no " + tipo_claro(v),
                     linea)


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
    if isinstance(v, ModuloPython):
        return "python"
    return "funcion"


CAUSA_DE_NADA = ("'nada' es la falta de valor: ¿a la función le falta un 'devolver', o es "
                 "un campo opcional que vino vacío?")
_CON_ARTICULO = {"nada": "el valor nada", "numero": "un número", "texto": "un texto",
                 "logico": "un valor lógico", "lista": "una lista", "mapa": "un mapa",
                 "agente": "un agente", "funcion": "una función",
                 "python": "un archivo de Python"}
_VERBOS = {"+": "sumar", "-": "restar", "*": "multiplicar", "/": "dividir", "%": "dividir"}


def tipo_claro(v):
    """El tipo para un mensaje de error: 'nada' suelto se lee como otra frase ("no se
    puede hacer nada"), así que se dice "el valor nada"."""
    if isinstance(v, ModuloPython):
        return "un archivo de Python"
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


_SUELTOS = frozenset((int, float, str, bool, type(None)))


def lleva_funcion(v):
    """¿Hay una función en este valor, aunque sea adentro de una lista, mapa o mensaje?"""
    if v.__class__ in _SUELTOS:  # un número, un texto, verdadero, falso o nada: seguro que no
        return False
    if isinstance(v, (Funcion, Nativa, ModuloPython)):
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
    "python": "'{n}' es el archivo de Python que trajo 'usar python' y no se le puede "
              "asignar un valor",
}


def por_teclado(pregunta):
    """Muestra la pregunta y espera que la persona escriba y apriete Enter."""
    return input(pregunta if pregunta.endswith((" ", "\n")) or not pregunta
                 else pregunta + " ")


class CorteEnElTeclado(KeyboardInterrupt):
    """Ctrl+C mientras leer() esperaba que la persona escribiera (0.5): es la manera normal
    de cortar una charla, así que el programa termina ahí, prolijo y sin cartel de error.
    (Lo que recuerdan los agentes se guarda igual, como con cualquier otro final.)"""


CORTE_EN_EL_TECLADO = ("Listo: cortaste con Ctrl+C mientras el programa esperaba que "
                       "escribieras, y terminó ahí.")


# ───────────────────────── Tablas: leer_tabla() (0.5) ─────────────────────────
# Una planilla de Excel guardada como CSV: la primera fila son los títulos, y cada fila de
# abajo queda como un mapa con esos títulos como claves. Se aceptan las dos formas en que
# Excel la guarda (separada por punto y coma, que es lo que hace en la Argentina, o por
# coma) y los números escritos a la argentina.
_SOLO_MILES = re.compile(r"[+-]?[0-9]{1,3}(\.[0-9]{3})+")   # 3.500 en una planilla: 3500
_EMPIEZA_CON_CERO = re.compile(r"[+-]?0[0-9]+")              # 00123: un código, no un número
COMO_GUARDAR_CSV = ("En Excel: Archivo > Guardar como > en 'Tipo' elegí "
                    "\"CSV (delimitado por comas) (*.csv)\" y guardalo en la carpeta del "
                    "programa")


def valor_de_celda(celda):
    """Lo que vale una celda de la planilla: un número si está escrita como número (también
    a la argentina: 3.500, 3.500,50, $ 3.500), y si no, el texto tal cual, sin los espacios
    de las puntas. Una celda vacía es el texto vacío."""
    t = celda.strip()
    sin_pesos = re.sub(r"^([+-]?)\$\s*", r"\1", t)
    if not t or _EMPIEZA_CON_CERO.fullmatch(sin_pesos):
        return t
    if _SOLO_MILES.fullmatch(sin_pesos):  # en una planilla argentina el punto es de los miles
        sin_pesos = sin_pesos.replace(".", "")
    try:
        return numero_de_texto(sin_pesos)
    except ErrorMate:
        return t


def separador_de(titulos):
    """Con qué están separadas las columnas: se mira la fila de los títulos. Si hay duda,
    punto y coma, que es lo que usa Excel en la Argentina."""
    cuenta, entre_comillas = {";": 0, ",": 0, "\t": 0}, False
    for letra in titulos:
        if letra == '"':
            entre_comillas = not entre_comillas
        elif letra in cuenta and not entre_comillas:
            cuenta[letra] += 1
    return max(cuenta, key=lambda s: cuenta[s])


def tabla_de_texto(texto, nombre):
    """Las filas de un CSV, como una lista de mapas. 'nombre' es para los errores."""
    def mal(que):
        return ErrorMate(f"leer_tabla(): {que}", familia="archivo")

    texto = texto.lstrip("\ufeff")
    corrido = 0  # renglones del archivo que quedaron arriba de lo que se lee
    aviso_de_excel = re.match(r"sep=(.)[ \t]*\n", texto)  # un renglón que a veces pone Excel
    if aviso_de_excel:
        texto, corrido = texto[aviso_de_excel.end():], 1
    renglones = texto.split("\n")
    while renglones and not renglones[0].strip(" \t;,"):
        renglones.pop(0)  # renglones en blanco antes de los títulos
        corrido += 1
    if not renglones:
        raise mal(f"'{nombre}' está vacío. Tiene que traer una primera fila con los títulos "
                   "de las columnas (por ejemplo producto;precio) y, debajo, un renglón por "
                   "cada producto")
    separador = aviso_de_excel.group(1) if aviso_de_excel else separador_de(renglones[0])
    try:
        lector = csv.reader(io.StringIO("\n".join(renglones)), delimiter=separador)
    except (csv.Error, TypeError):
        lector = csv.reader(io.StringIO("\n".join(renglones)), delimiter=";")
    titulos, filas, anterior = None, [], 0
    while True:
        try:
            celdas = next(lector)
        except StopIteration:
            break
        except csv.Error:
            raise mal(f"no pude entender el renglón {corrido + anterior + 1} de '{nombre}': "
                       "¿hay una comilla que abre y no cierra?")
        renglon, anterior = corrido + anterior + 1, lector.line_num
        celdas = [c.strip() for c in celdas]
        if not any(celdas):
            continue  # un renglón en blanco (o los ;;; que deja Excel al final)
        if titulos is None:
            while celdas and not celdas[-1]:
                celdas.pop()  # columnas vacías que Excel deja a la derecha
            sin_titulo = [i + 1 for i, t in enumerate(celdas) if not t]
            if sin_titulo:
                raise mal(f"en '{nombre}' la columna {sin_titulo[0]} no tiene título (los "
                           f"títulos van en la primera fila, el renglón {renglon}): "
                           "escribile uno, o borrá esa columna")
            repetido = repetidos(celdas)
            if repetido:
                raise mal(f"en '{nombre}' hay dos columnas con el mismo título, "
                           f"'{repetido[0]}': cambiale el nombre a una")
            titulos = celdas
            continue
        while len(celdas) > len(titulos) and not celdas[-1]:
            celdas.pop()
        if len(celdas) != len(titulos):
            if len(celdas) > len(titulos):
                pista = ("le sobra algo. Si un dato lleva coma o punto y coma adentro (un "
                         "precio como 3.500,50 en un archivo separado por comas), tiene que "
                         "ir entre comillas: \"3.500,50\"")
            else:
                pista = "le falta un dato, o un separador"
            separa = {";": "punto y coma", ",": "coma", "\t": "tabulación"}.get(
                separador, f"'{separador}'")
            raise mal(
                f"el renglón {renglon} de '{nombre}' tiene {len(celdas)} "
                f"{'columna' if len(celdas) == 1 else 'columnas'} y los títulos son "
                f"{len(titulos)} ({', '.join(titulos)}): {pista}. (Las columnas están "
                f"separadas por {separa}.) El renglón dice: "
                f"{recortado(separador.join(celdas), 80)}")
        filas.append({titulo: valor_de_celda(c) for titulo, c in zip(titulos, celdas)})
    return filas


# ───────────────────────────── La IA (mejora 100) ─────────────────────────────
# consultar_ia() le habla a Claude, de Anthropic, por la red. Todo con la biblioteca
# estándar. La clave nunca está en el programa: se lee de la variable ANTHROPIC_API_KEY.

IA_DIRECCION = "https://api.anthropic.com/v1/messages"
IA_VERSION = "2026-10-21"  # el encabezado anthropic-version
IA_MODELO = "claude-opus-5-5"  # se cambia con la variable MATE_MODELO
IA_MAX_TOKENS = 16000  # el largo máximo de una respuesta (pensar también gasta de acá)
IA_ESPERA = 180  # segundos que se espera una respuesta antes de darla por perdida
IA_REINTENTOS = 2  # si la IA está saturada o se corta la red, se prueba de nuevo
IA_ESPERA_MAXIMA = 30  # nunca se queda esperando más que esto entre dos intentos
MAX_CONSULTAS_IA = 50  # consultas de verdad (pagas) por corrida; --sin-limite lo saca
# Si un filtro de seguridad no deja contestar al modelo, Anthropic prueba con otro en el
# mismo pedido. Solo estos modelos lo aceptan.
IA_CON_RESPALDO = ("claude-fable-5-2", "claude-fable-5-1", "claude-opus-5-5",
                   "claude-opus-5", "claude-sonnet-5-5")
IA_RESPALDO = "server-side-fallback-2026-07-01"  # el encabezado anthropic-beta que lo pide
_IA_SIN_RESPALDO = set()  # modelos a los que Anthropic les rechazó ese pedido de respaldo
DONDE_SE_SACA = "platform.claude.com"
FALTA_LA_CLAVE = (
    "consultar_ia(): falta la clave para hablar con la IA. En PowerShell, antes de correr, "
    'escribí:  $env:ANTHROPIC_API_KEY = "tu-clave"\n'
    f"La clave se saca en {DONDE_SE_SACA} y el servicio es pago (se cobra cada consulta). "
    "Para probar sin clave y sin gastar: --ia-simulada")
SIN_RESPUESTA_SIMULADA = (
    "consultar_ia(): acá Mate no sale a la red y no hay una respuesta simulada para esta "
    'consulta. En una prueba, fijala antes con simular_ia("lo que contesta"); o dale un '
    "tercer valor a consultar_ia(), que es lo que contesta cuando no habla con la IA de "
    "verdad")


def error_de_ia(texto):
    return ErrorMate(f"consultar_ia(): {texto}", familia="ia")


def clave_de_ia():
    """La clave, de la variable de entorno. Nunca se muestra ni se guarda en otro lado."""
    clave = os.environ.get("ANTHROPIC_API_KEY", "").strip().strip("\"'").strip()
    if not clave:
        raise ErrorMate(FALTA_LA_CLAVE, familia="ia")
    if not (clave.isascii() and clave.isprintable()) or " " in clave:
        raise error_de_ia(
            "la clave guardada en ANTHROPIC_API_KEY tiene espacios o letras raras (no la "
            "muestro por seguridad). Copiala de nuevo, entera y sin nada de más")
    return clave


def tapar_clave(texto, clave):
    """El texto sin la clave: ni entera, ni en mayúsculas, ni un pedazo de 8 o más
    caracteres (por si un servidor la devuelve partida o cambiada en su error)."""
    texto = str(texto)
    if not clave:
        return texto
    minimo = min(8, len(clave))
    bajo, llave = texto.lower(), clave.lower()
    pedazos = {llave[i:i + minimo] for i in range(len(llave) - minimo + 1)}
    partes, i, desde = [], 0, 0
    while i <= len(bajo) - minimo:
        if bajo[i:i + minimo] not in pedazos:
            i += 1
            continue
        fin = i + minimo  # se estira mientras lo que sigue también sea parte de la clave
        while fin < len(bajo) and bajo[i:fin + 1] in llave:
            fin += 1
        partes += [texto[desde:i], "(la clave)"]
        i = desde = fin
    return "".join(partes) + texto[desde:]


def modelo_de_ia():
    modelo = os.environ.get("MATE_MODELO", "").strip().strip("\"'").strip() or IA_MODELO
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:@\[\]-]{0,99}", modelo):
        raise error_de_ia(
            "la variable MATE_MODELO no tiene el nombre de un modelo. Poné uno como "
            f'"{IA_MODELO}", o borrala para usar ese:  Remove-Item Env:MATE_MODELO')
    return modelo


def texto_de_la_ia(datos):
    """El texto de una respuesta de la IA que llegó bien (o el error que lo explica)."""
    bloques = datos.get("content") if isinstance(datos, dict) else None
    if not isinstance(bloques, list):
        raise error_de_ia("llegó una respuesta que no pude entender. Probá de nuevo")
    if datos.get("stop_reason") == "refusal":
        raise error_de_ia("la IA no quiso contestar esa consulta (la frenó un filtro de "
                          "seguridad de Anthropic). Probá preguntándolo de otra manera")
    texto = "".join(b["text"] for b in bloques if isinstance(b, dict)
                    and b.get("type") == "text" and isinstance(b.get("text"), str)).strip()
    if datos.get("stop_reason") == "max_tokens":
        raise error_de_ia("la respuesta llegó cortada: era más larga de lo que entra en una "
                          "consulta. Pedile en las instrucciones que conteste más corto")
    if not texto:
        raise error_de_ia("la IA contestó sin texto. Probá de nuevo o cambiá la pregunta")
    return texto


def explicar_error_de_ia(codigo, dicho, detalles, modelo):
    """Qué significa, en castellano, el error con el que contestó Anthropic."""
    dicho = " ".join(str(dicho or "").split())[:300]
    original = f" (Anthropic dijo: {dicho})" if dicho else ""
    poner = '$env:ANTHROPIC_API_KEY = "tu-clave"'
    if codigo == 401:
        return ("la clave no sirve: Anthropic no la reconoce (está mal copiada, vencida o "
                f"la borraron). Sacá una nueva en {DONDE_SE_SACA} y ponela otra vez:  {poner}")
    if codigo == 402 or "credit balance" in dicho.lower():
        return ("la cuenta de Anthropic no tiene crédito (o hay un problema con el pago). "
                f"Se carga en {DONDE_SE_SACA}, en la parte de facturación")
    if codigo == 403:
        return f"esa clave no tiene permiso para hacer esta consulta{original}"
    if codigo == 404:
        return (f"Anthropic no conoce el modelo '{modelo}', o tu cuenta no puede usarlo. "
                + ("Revisá la variable MATE_MODELO, o borrala para usar el de siempre:  "
                   "Remove-Item Env:MATE_MODELO" if os.environ.get("MATE_MODELO", "").strip()
                   else f"Fijate en {DONDE_SE_SACA} qué modelos tiene tu cuenta y elegí uno "
                   "con la variable MATE_MODELO"))
    if codigo == 413 or "prompt is too long" in dicho.lower():
        return "la consulta es demasiado larga para mandársela a la IA: achicá el texto"
    if codigo == 429 and detalles.get("error_code") == "enforced_spend_limit_reached":
        return ("la cuenta de Anthropic llegó a su tope de gasto del mes. Se cambia en "
                f"{DONDE_SE_SACA}, o hay que esperar al mes que viene")
    if codigo == 429:
        return ("demasiadas consultas en poco tiempo: se llegó al límite de uso de la "
                "cuenta. Esperá un minuto y probá de nuevo")
    if codigo == 529:
        return "la IA está saturada en este momento. Probá de nuevo en unos minutos"
    if codigo >= 500:
        return ("el servicio de la IA tuvo un problema (no es tu programa). Probá de nuevo "
                "en unos minutos")
    if codigo == 400:
        return f"Anthropic no aceptó la consulta{original or ' y no dijo por qué'}"
    return f"Anthropic contestó con un error que no conozco (código {codigo}){original}"


def pedir_a_la_ia(instrucciones, pregunta):
    """Le manda la consulta a Claude y devuelve el texto que contesta. Todo lo que puede
    salir mal es un ErrorMate en castellano, y la clave nunca aparece en ninguno."""
    import http.client
    import socket
    import ssl
    import time
    import urllib.error
    import urllib.request  # (usa el proxy del sistema: el de Windows o HTTPS_PROXY)

    clave, modelo = clave_de_ia(), modelo_de_ia()

    def error(texto):
        return error_de_ia(tapar_clave(texto, clave))

    tardo = error(f"la IA tardó más de {IA_ESPERA // 60} minutos en contestar y dejé de "
                  "esperar. Probá de nuevo, o con una pregunta más corta")
    reintentos = 0
    while True:
        respaldo = modelo in IA_CON_RESPALDO and modelo not in _IA_SIN_RESPALDO
        cuerpo = {"model": modelo, "max_tokens": IA_MAX_TOKENS,
                  "messages": [{"role": "user", "content": pregunta}]}
        encabezados = {"content-type": "application/json", "x-api-key": clave,
                       "anthropic-version": IA_VERSION, "user-agent": f"mate/{VERSION}"}
        if instrucciones.strip():
            cuerpo["system"] = instrucciones
        if respaldo:
            cuerpo["fallbacks"] = "default"
            encabezados["anthropic-beta"] = IA_RESPALDO
        codigo, cabeza, crudo, problema = 200, {}, b"", None
        try:
            pedido = urllib.request.Request(
                IA_DIRECCION, data=json.dumps(cuerpo).encode("utf-8"),
                headers=encabezados, method="POST")
            with urllib.request.urlopen(pedido, timeout=IA_ESPERA) as respuesta:
                crudo = respuesta.read()
        except urllib.error.HTTPError as e:  # Anthropic contestó, pero con un error
            codigo, cabeza = e.code, e.headers or {}
            try:
                crudo = e.read()
            except Exception:
                crudo = b""
        except (TimeoutError, socket.timeout):
            raise tardo
        except urllib.error.URLError as e:
            if isinstance(e.reason, (TimeoutError, socket.timeout)):
                raise tardo
            if isinstance(e.reason, ssl.SSLError):
                raise error(
                    "no pude armar una conexión segura con la IA (falló el certificado). "
                    "Suele ser un antivirus o la red de una oficina que revisa las "
                    "conexiones: probá desde otra red")
            problema = ("no pude conectarme con la IA: revisá que haya internet (y, si "
                        "estás en una oficina, que la red deje salir a api.anthropic.com)")
        except (OSError, http.client.HTTPException):
            problema = "se cortó la conexión con la IA antes de que llegara la respuesta"
        except (ValueError, TypeError):
            raise error("no pude armar la consulta para la IA con esos textos")
        try:
            datos = json.loads(crudo.decode("utf-8")) if not problema else None
        except (ValueError, UnicodeError):
            datos = None
        if problema is None and codigo == 200:
            texto = texto_de_la_ia(datos)
            _USO_DE_LA_IA["tokens"] = tokens_de(datos)
            return texto
        detalle = datos.get("error") if isinstance(datos, dict) else None
        detalle = detalle if isinstance(detalle, dict) else {}
        dicho = detalle.get("message") if isinstance(detalle.get("message"), str) else ""
        dicho = tapar_clave(dicho, clave)  # antes de recortarlo: que no quede media clave
        detalles = detalle.get("details") if isinstance(detalle.get("details"), dict) else {}
        if codigo == 400 and respaldo and re.search("anthropic-beta|fallback", dicho, re.I):
            _IA_SIN_RESPALDO.add(modelo)  # esta cuenta no tiene el respaldo: va sin él
            continue
        de_nuevo = problema is not None or codigo in (408, 409, 429) or codigo >= 500
        if (detalles.get("error_code") == "enforced_spend_limit_reached"
                or str(cabeza.get("x-should-retry", "")).lower() == "false"):
            de_nuevo = False
        if de_nuevo and reintentos < IA_REINTENTOS:
            try:
                pausa = float(cabeza.get("retry-after") or 2 + 3 * reintentos)
            except (TypeError, ValueError):
                pausa = 2 + 3 * reintentos
            if 0 <= pausa <= IA_ESPERA_MAXIMA:
                reintentos += 1
                time.sleep(pausa)
                continue
        raise error(problema or explicar_error_de_ia(codigo, dicho, detalles, modelo))


def respuestas_de_archivo(ruta):
    """Lee el archivo de --ia-simulada=archivo. Cada renglón es
    'lo que trae la pregunta => lo que contesta la IA'; con * adelante, contesta eso a
    cualquier pregunta. Devuelve la lista de pares, o falla con un ErrorMate que explica."""
    try:
        contenido = leer_fuente(ruta)
    except FileNotFoundError:
        raise ErrorMate(f"no encuentro el archivo de respuestas '{ruta}'")
    except (OSError, ErrorMate):
        raise ErrorMate(f"no pude leer el archivo de respuestas '{ruta}'")
    pares = []
    for numero, renglon in enumerate(contenido.splitlines(), 1):
        if not renglon.strip() or renglon.strip().startswith("#"):
            continue
        si_trae, flecha, contesta = renglon.partition("=>")
        if not flecha or not si_trae.strip() or not contesta.strip():
            raise ErrorMate(
                f"{ruta}:{numero}: no entiendo este renglón del archivo de respuestas. Cada "
                "uno va así:  lo que trae la pregunta => lo que contesta la IA   (o  "
                "* => lo que contesta a todo lo demás)")
        pares.append((" ".join(sin_tildes(si_trae).lower().split()),
                      contesta.strip().replace("\\n", "\n")))
    if not pares:
        raise ErrorMate(f"el archivo de respuestas '{ruta}' está vacío. Cada renglón va así:  "
                        "lo que trae la pregunta => lo que contesta la IA")
    return pares


def respuesta_del_archivo(pares, pregunta):
    """Lo que contesta el archivo de --ia-simulada a esa pregunta (o None): el primer
    renglón cuyo texto esté en la pregunta y, si ninguno, el del asterisco."""
    buscada = " ".join(sin_tildes(pregunta).lower().split())
    for si_trae, contesta in pares:
        if si_trae != "*" and si_trae in buscada:
            return contesta
    for si_trae, contesta in pares:
        if si_trae == "*":
            return contesta
    return None


def recortado(texto, largo=70):
    """Un texto en un solo renglón y no muy largo, para la traza."""
    texto = " ".join(texto.split())
    return '"' + (texto if len(texto) <= largo else texto[:largo].rstrip() + "...") + '"'


# ─────────────── Lo que un agente aprende: memoria, lecciones y bitácora (0.4) ───────────────
# Todo vive en dos archivos al lado del programa, que se abren con el Bloc de notas:
# mi_mostrador.memoria.json (lo que cada agente recuerda y sus lecciones) y
# mi_mostrador.bitacora.txt (las fallas de los agentes). Solo los toca 'correr': con
# 'probar' no se leen ni se escriben. Nada de esto sale nunca por la red.

def archivo_de(ruta, que):
    """El archivo que acompaña a un programa: mi_mostrador.mate -> mi_mostrador.memoria.json
    (que es "memoria.json" o "bitacora.txt")."""
    for final in (".mate.txt", ".mate"):
        if ruta.lower().endswith(final):
            return f"{ruta[:-len(final)]}.{que}"
    return f"{ruta}.{que}"


def escribir_entero(ruta, texto):
    """Escribe el archivo de una sola vez: primero en uno provisorio al lado y recién
    después lo pone en su lugar. Así nunca queda a medio escribir."""
    provisorio = ruta + ".tmp"
    try:
        # con la marca del principio, para que el Bloc de notas muestre bien las tildes
        with open(provisorio, "w", encoding="utf-8-sig", errors="backslashreplace") as f:
            f.write(texto)
        os.replace(provisorio, ruta)
    except BaseException:
        try:
            os.remove(provisorio)
        except OSError:
            pass
        raise


def en_un_renglon(texto, largo):
    texto = " ".join(str(texto).split())
    return texto if len(texto) <= largo else texto[:largo].rstrip() + "..."


def leer_memoria(ruta):
    """Lo que dice el archivo de memoria: ({agente: {"estado": {...}, "lecciones": [...]}},
    avisos). Si no existe, nada. Si está roto (alguien lo editó a mano y quedó mal), un
    ErrorMate que dice dónde y cómo seguir: no se pisa un archivo que no se entiende."""
    nombre = os.path.basename(ruta)

    def roto(que):
        return ErrorMate(
            f"no entiendo el archivo de memoria {nombre}: {que}. Abrilo con el Bloc de notas "
            "y arreglalo; o borralo para empezar de cero (se pierde lo que recordaban los "
            f"agentes y también sus lecciones). Está en {os.path.dirname(os.path.abspath(ruta))}")

    def numero_raro(_):
        raise ValueError

    def decimal(t):
        return float(t) if math.isfinite(float(t)) else numero_raro(t)

    try:
        texto = leer_fuente(ruta)
    except FileNotFoundError:
        return {}, []
    except (OSError, ErrorMate):
        raise ErrorMate(f"no pude abrir el archivo de memoria {nombre}: fijate que no esté "
                        "abierto en otro programa y que tengas permiso para leerlo")
    if not texto.strip():
        return {}, []
    try:
        datos = json.loads(texto, parse_constant=numero_raro, parse_float=decimal)
    except json.JSONDecodeError as e:
        raise roto(f"en el renglón {e.lineno} hay algo mal escrito (suele ser una coma o "
                   "una comilla de más o de menos)")
    except (ValueError, RecursionError):
        raise roto("trae un número que no es válido, o demasiadas cosas una adentro de otra")
    agentes = datos.get("agentes") if isinstance(datos, dict) else None
    if not isinstance(agentes, dict):
        raise roto('le falta la parte "agentes"')
    limpio, avisos = {}, []
    for agente, ficha in agentes.items():
        if not isinstance(ficha, dict) or not isinstance(ficha.get("estado", {}), dict) \
                or not isinstance(ficha.get("lecciones", []), list):
            raise roto(f'lo que guarda de "{agente}" no tiene la forma de siempre (un '
                       '"estado" entre llaves y las "lecciones" entre corchetes)')
        lecciones = []
        for leccion in ficha.get("lecciones", []):
            if isinstance(leccion, str):  # escrita a mano, sin fecha: vale igual
                leccion = {"texto": leccion}
            dicho = leccion.get("texto") if isinstance(leccion, dict) else None
            if not isinstance(dicho, str) or not dicho.strip():
                avisos.append(f"en {nombre} hay una lección de {agente} que no se entiende "
                              '(le falta el "texto"): la salteo')
                continue
            if len(" ".join(dicho.split())) > LARGO_DE_LECCION:
                avisos.append(f"en {nombre} hay una lección de {agente} de más de "
                              f"{LARGO_DE_LECCION} letras: uso solo el principio")
            fecha = leccion.get("fecha")
            lecciones.append({"fecha": fecha if isinstance(fecha, str) else "",
                              "texto": en_un_renglon(dicho, LARGO_DE_LECCION)})
        if len(lecciones) > MAX_LECCIONES:
            avisos.append(f"en {nombre}, {agente} tiene más de {MAX_LECCIONES} lecciones, "
                          "que es el tope: me quedo con las más nuevas")
        limpio[str(agente)] = {"estado": dict(ficha.get("estado", {})),
                               "lecciones": lecciones[-MAX_LECCIONES:]}
        # Lo de la 0.5 (lecciones propuestas y cuenta de consultas) solo está si hay algo.
        propuestas = []
        for propuesta in ficha.get("propuestas", []) \
                if isinstance(ficha.get("propuestas"), list) else []:
            dicho = propuesta.get("texto") if isinstance(propuesta, dict) else None
            if not isinstance(dicho, str) or not dicho.strip():
                continue
            fecha, motivo = propuesta.get("fecha"), propuesta.get("motivo")
            propuestas.append({"fecha": fecha if isinstance(fecha, str) else "",
                               "texto": en_un_renglon(dicho, LARGO_DE_LECCION),
                               "motivo": en_un_renglon(motivo, 400)
                               if isinstance(motivo, str) else ""})
        if propuestas:
            limpio[str(agente)]["propuestas"] = propuestas[-MAX_PROPUESTAS:]
        gasto = gasto_limpio(ficha.get("gasto"))
        if gasto:
            limpio[str(agente)]["gasto"] = gasto
    return limpio, avisos


def guardar_memoria(ruta, programa, agentes):
    """Deja la memoria en su archivo (o lo saca, si ya no hay nada que recordar). Devuelve
    None si salió bien o la explicación de por qué no se pudo."""
    agentes = {a: f for a, f in agentes.items() if any(f.values())}
    try:
        if not agentes:
            if os.path.lexists(ruta):
                os.remove(ruta)
            return None
        datos = {
            "que_es": f"La memoria de {programa}: lo que cada agente recuerda de una corrida "
                      "a la otra (estado) y las lecciones que aprendió. La escribe Mate "
                      "cada vez que el programa termina. Para empezar de cero: correr con "
                      "--olvidar.",
            "agentes": agentes}
        escribir_entero(ruta, json.dumps(datos, ensure_ascii=False, indent=2,
                                         allow_nan=False) + "\n")
    except (OSError, ValueError, RecursionError):
        return (f"no pude guardar la memoria en '{ruta}': lo que pasó en esta corrida no va "
                "a estar en la próxima. Fijate que el archivo no esté abierto en otro "
                "programa y que se pueda escribir en esa carpeta")
    return None


def leccion_limpia(texto):
    """La lección en un solo renglón (o el error, si está vacía o es demasiado larga)."""
    texto = " ".join(texto.split())
    if not texto:
        raise ErrorMate("la lección está vacía: escribí qué tiene que tener en cuenta el agente")
    if len(texto) > LARGO_DE_LECCION:
        raise ErrorMate(
            f"la lección tiene {len(texto)} letras y el tope es {LARGO_DE_LECCION} (cada "
            "lección viaja en cada consulta a la IA, y eso se paga): escribila más corta, "
            "o partila en dos")
    return texto


def sumar_leccion(lecciones, texto, fecha):
    """(la lista con esa lección al final, cuántas viejas hubo que olvidar). Si ya la
    tenía, devuelve la misma lista: una lección no se anota dos veces."""
    if any(leccion["texto"] == texto for leccion in lecciones):
        return lecciones, 0
    nuevas = lecciones + [{"fecha": fecha, "texto": texto}]
    sobran = max(0, len(nuevas) - MAX_LECCIONES)
    return nuevas[sobran:], sobran


def con_lecciones(instrucciones, lecciones):
    """Las instrucciones para la IA con las lecciones del agente al final, bajo su título."""
    lista = "\n".join(f"{i}. {leccion}" for i, leccion in enumerate(lecciones, 1))
    return f"{instrucciones.rstrip()}\n\n{TITULO_DE_LECCIONES}\n{lista}".lstrip()


# ─────────────── Frenos para la IA, tope de gasto y lecciones propuestas (0.5) ───────────────
# Un agente declara sus frenos:
#     frenos {
#         precios: lista                  (los importes que la IA puede nombrar)
#         prohibido: ["descuento"]        (palabras o temas que no puede tocar)
#         largo: 400                      (letras, como mucho)
#         reserva: "Eso te lo confirma una persona, ya te paso."
#         consultas_por_dia: 100          (tope de gasto)
#         tokens_por_dia: 200000
#     }
# y MATE (no la IA) revisa cada respuesta de consultar_ia() de ese agente antes de
# devolverla. Si una regla no se cumple, consulta UNA vez más diciéndole a la IA qué regla
# rompió; si la vuelve a romper, devuelve el texto de 'reserva'. Cada freno que salta queda
# en la bitácora y deja una lección PROPUESTA, que no se usa hasta que el dueño la aprueba.

# regla -> (qué tipo de valor lleva, un ejemplo, qué hace)
REGLAS_DE_FRENO = {
    "precios": (("lista", "mapa"), "precios: lista",
                "los importes en pesos que puede nombrar la IA: una lista de números, o la "
                "tabla de precios entera (valen todos sus números)"),
    "prohibido": (("lista",), 'prohibido: ["descuento", "garantía"]',
                  "palabras o temas que no pueden aparecer en la respuesta"),
    "largo": (("numero",), "largo: 400", "cuántas letras puede tener la respuesta, como mucho"),
    "reserva": (("texto",), 'reserva: "Eso te lo confirma una persona, ya te paso."',
                "lo que se contesta cuando la IA rompe una regla dos veces, o se llegó al tope"),
    "consultas_por_dia": (("numero",), "consultas_por_dia: 100",
                          "cuántas consultas a la IA puede hacer el agente por día"),
    "tokens_por_dia": (("numero",), "tokens_por_dia: 200000",
                       "cuántos tokens (lo que cobra el servicio) puede gastar por día"),
}
REGLAS_EN_LISTA = ", ".join(REGLAS_DE_FRENO)
REGLAS_DE_CONTENIDO = ("precios", "prohibido", "largo")  # las que miran la respuesta
MAX_PROPUESTAS = 20  # lecciones propuestas (sin aprobar) por agente; se va la más vieja
DIAS_DE_GASTO = 30  # cuántos días se guarda la cuenta de consultas de cada agente
MAX_PROHIBIDOS = 100  # textos en la regla 'prohibido'
# Un número suelto (sin $ ni "pesos") después de "sale", "cuesta"... cuenta como importe
# solo desde este valor: así "sale 2 por 1" o "vale 3 puntos" no hacen saltar el freno.
IMPORTE_SUELTO_DESDE = 100

_NUM_DE_IMPORTE = (r"(?:\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d{1,3}(?:,\d{3})+(?:\.\d+)?"
                   r"|\d+(?:[.,]\d+)?)(?!\d)")
_MIL_O_MILLON = r"(?:\s*(mil|millones|mill[oó]n)\b)?"
# $ 3.500   $3500   $ 3.500,00   AR$ 1.234,50   $ 3 mil
_IMPORTE_CON_SIGNO = re.compile(r"\$\s*(" + _NUM_DE_IMPORTE + ")" + _MIL_O_MILLON, re.I)
# 3500 pesos   3.500 pesos   3 mil pesos   2 millones de pesos   3500$
_IMPORTE_CON_PESOS = re.compile(
    r"(?<![\w.,$])(" + _NUM_DE_IMPORTE + ")" + _MIL_O_MILLON
    + r"(?:\s+de)?\s*(?:pesos?\b|\$)", re.I)
# sale 3500   cuesta 3.500   el precio es de 3500   (sin $ ni "pesos")
_IMPORTE_SUELTO = re.compile(
    r"\b(?:sale|salen|cuesta|cuestan|vale|valen|precio|cobramos)\b"
    r"(?:\s+(?:es|son|de|a|en|final|total|solo|sólo))*\s*:?\s*(" + _NUM_DE_IMPORTE + ")"
    + _MIL_O_MILLON
    + r"(?!\s*[/%:°x-]\s*\d)(?!\s*%)"
    r"(?!\s+(?!(?:por|cada|el|la|los|las|y|o|e|más|mas|con|c|final|en|al|si|pero|sin)\b)"
    r"[a-záéíóúñü])", re.I)


def valores_de_importe(escrito, cuanto=None):
    """Lo que puede valer un importe escrito. "3.500" es 3500 (acá el punto es de los
    miles) y "3,5" es tres y medio. "3,500" puede ser las dos cosas (a la inglesa son tres
    mil quinientos): ante la duda se dan las dos lecturas, y alcanza con que una esté
    permitida."""
    valores = set()
    if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", escrito):  # a la argentina: 1.234,50
        valores.add(float(escrito.replace(".", "").replace(",", ".")))
    elif re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d+)?", escrito):  # a la inglesa: 1,234.50
        valores.add(float(escrito.replace(",", "")))
        if escrito.count(",") == 1 and "." not in escrito:
            valores.add(float(escrito.replace(",", ".")))
    else:
        valores.add(float(escrito.replace(",", ".")))
    veces = {"mil": 1000}.get((cuanto or "").lower(), 1_000_000 if cuanto else 1)
    return {v * veces for v in valores}


def importes_de(texto):
    """Los importes en pesos que nombra un texto: [(como está escrito, lo que puede valer)].
    Cuenta como importe un número con el signo $ adelante o atrás, con la palabra "pesos",
    o suelto justo después de "sale", "cuesta", "vale", "precio" o "cobramos" (y de 100 o
    más). Lo demás (cantidades, teléfonos, fechas, porcentajes) no se mira: ante la duda,
    este freno prefiere no saltar. Tampoco ve los importes escritos con letras."""
    vistos = {}
    for patron, suelto in ((_IMPORTE_CON_SIGNO, False), (_IMPORTE_CON_PESOS, False),
                           (_IMPORTE_SUELTO, True)):
        for m in patron.finditer(texto):
            if m.start(1) in vistos:
                continue
            valores = valores_de_importe(m.group(1), m.group(2))
            if suelto and max(valores) < IMPORTE_SUELTO_DESDE:
                continue
            escrito = m.group(1) + (f" {m.group(2)}" if m.group(2) else "")
            vistos[m.start(1)] = (escrito if suelto else "$ " + escrito, valores)
    return [vistos[i] for i in sorted(vistos)]


def numeros_permitidos(valor, hondo=0):
    """Todos los números que hay en un valor: en una lista, en una tabla (una lista de
    mapas), en un mapa o en un mensaje. Son los importes que la IA puede nombrar."""
    if es_num(valor):
        return {float(valor)}
    if hondo > 20:
        return set()
    if isinstance(valor, Registro):
        valor = valor.campos
    if isinstance(valor, dict):
        valor = list(valor.values())
    if isinstance(valor, list):
        return set().union(*(numeros_permitidos(x, hondo + 1) for x in valor))
    return set()


def reglas_rotas(respuesta, frenos):
    """Qué reglas de esos frenos no cumple la respuesta: [(regla, qué pasó, la lección que
    se propone)]. Una lista vacía quiere decir que la respuesta pasa."""
    rotas = []
    if frenos.get("precios") is not None:
        permitidos = frenos["precios"]
        ajenos = [escrito for escrito, valores in importes_de(respuesta)
                  if not any(abs(v - p) < 0.005 for v in valores for p in permitidos)]
        if ajenos:
            ajenos = list(dict.fromkeys(ajenos))
            cuales = ", ".join(ajenos[:3]) + (" y otros" if len(ajenos) > 3 else "")
            rotas.append(("precios", (
                f"nombró {'el importe' if len(ajenos) == 1 else 'los importes'} {cuales}, "
                f"que no está{'' if len(ajenos) == 1 else 'n'} entre los precios permitidos"),
                "No nombres ningún importe que no esté en los precios que te dieron. Si no "
                "sabés un precio, decí que lo confirma una persona."))
    if frenos.get("prohibido"):
        llano = " ".join(sin_tildes(respuesta).lower().split())
        for palabra in frenos["prohibido"]:
            buscada = " ".join(sin_tildes(palabra).lower().split())
            if buscada and re.search(r"(?<!\w)" + re.escape(buscada), llano):
                rotas.append(("prohibido", f'dijo "{palabra}", que está entre lo prohibido',
                              f'No hables de "{en_un_renglon(palabra, 80)}": de eso acá no '
                              "se habla. Si te lo preguntan, decí que lo ve una persona."))
                break
    if frenos.get("largo") is not None and len(respuesta) > frenos["largo"]:
        rotas.append(("largo", f"la respuesta tiene {len(respuesta)} letras y el máximo es "
                               f"{frenos['largo']}",
                      f"Contestá corto: como mucho {frenos['largo']} letras."))
    return rotas


def aviso_de_freno(pregunta, rotas):
    """La consulta que se manda en el segundo intento: la misma, más qué regla se rompió."""
    que = "; ".join(motivo for _, motivo, _ in rotas)
    return (f"{pregunta}\n\n[Aviso del sistema: tu respuesta anterior a esta misma consulta "
            f"no se pudo usar porque {que}. Contestá de nuevo cumpliendo esa regla. Si no "
            "podés contestar sin romperla, decí que eso lo confirma una persona.]")


def sumar_propuesta(propuestas, lecciones, texto, motivo, fecha):
    """La lista de propuestas con esa lección al final (o la misma lista, si ya estaba
    propuesta o ya es una lección aprobada). Nunca más que el tope: se va la más vieja."""
    texto = en_un_renglon(texto, LARGO_DE_LECCION)
    if any(p["texto"] == texto for p in propuestas) \
            or any(leccion["texto"] == texto for leccion in lecciones):
        return propuestas
    nuevas = propuestas + [{"fecha": fecha, "texto": texto,
                            "motivo": en_un_renglon(motivo, 400)}]
    return nuevas[-MAX_PROPUESTAS:]


def gasto_limpio(gasto):
    """La cuenta de consultas de un agente como se guarda: {"2026-11-21": {"consultas": 3,
    "simuladas": 0, "tokens": 1200}}, con los últimos DIAS_DE_GASTO días y solo los que
    tienen algo. Lo que no tenga esa forma (alguien editó el archivo) se saltea."""
    limpio = {}
    for dia, cuenta in (gasto.items() if isinstance(gasto, dict) else ()):
        if not (isinstance(dia, str) and re.fullmatch(r"\d{4}-\d\d-\d\d", dia)
                and isinstance(cuenta, dict)):
            continue
        numeros = {k: cuenta.get(k, 0) for k in ("consultas", "simuladas", "tokens")}
        if all(type(n) is int and 0 <= n < 10 ** 15 for n in numeros.values()) \
                and any(numeros.values()):
            limpio[dia] = numeros
    return {dia: limpio[dia] for dia in sorted(limpio)[-DIAS_DE_GASTO:]}


def tokens_de(datos):
    """Los tokens que gastó una consulta, según lo que informa el servicio (los de la
    pregunta más los de la respuesta), o None si no lo dice."""
    uso = datos.get("usage") if isinstance(datos, dict) else None
    if not isinstance(uso, dict):
        return None
    partes = [uso.get(k) for k in ("input_tokens", "output_tokens")]
    if not all(type(n) is int and 0 <= n < 10 ** 12 for n in partes):
        return None
    return sum(partes)


# Lo que gastó la última consulta de verdad (lo deja pedir_a_la_ia): {"tokens": 1234}.
_USO_DE_LA_IA = {}


def usa_memoria(programa, propios=None):
    """¿El programa usa lo de aprender: un 'estado recordado', aprender(), lecciones() o
    los 'frenos' de un agente?
    Si no, 'correr' no lee ni escribe ningún archivo de más. (Si el programa le puso
    'aprender' o 'lecciones' a algo suyo, llamarlo no es usar lo de aprender.)"""
    if propios is None:
        propios = set(_ligaduras(programa))
    if isinstance(programa, EstadoRecordado):
        return True
    if not isinstance(programa, (list, tuple)):
        return False
    if _es_nodo(programa, "agente", 7) and programa[6]:
        return True  # un agente con frenos lleva la cuenta de sus consultas (0.5)
    if _es_nodo(programa, "llamar", 4) and _es_nodo(programa[2], "nombre", 3) \
            and programa[2][2] in ("aprender", "lecciones") and programa[2][2] not in propios:
        return True
    return any(usa_memoria(parte, propios) for parte in programa)


def se_puede_recordar(v):
    """Solo se recuerdan datos: ni agentes ni funciones (tampoco adentro de una lista)."""
    if isinstance(v, (Agente, Funcion, Nativa, ModuloPython)):
        return False
    if isinstance(v, (list, dict)):
        return all(se_puede_recordar(x) for x in (v.values() if isinstance(v, dict) else v))
    if isinstance(v, Registro):
        return all(se_puede_recordar(x) for x in v.campos.values())
    return True


def leer_renglones(ruta):
    """Los renglones de un archivo que escribe Mate (la bitácora, el registro). Si alguno
    trae letras que no se entienden (se dañó, o alguien pegó algo raro), solo ese se lee
    distinto: los demás conservan sus tildes."""
    with open(ruta, "rb") as f:
        datos = f.read()
    if datos[:2] in (b"\xff\xfe", b"\xfe\xff") or (
            len(datos) >= 4 and datos.count(0) >= len(datos) // 4):
        return leer_fuente(ruta).split("\n")  # guardado como "Unicode" en el Bloc de notas
    renglones = []
    for crudo in datos.replace(b"\r\n", b"\n").replace(b"\r", b"\n").split(b"\n"):
        try:
            renglones.append(crudo.decode("utf-8-sig"))
        except UnicodeError:
            renglones.append(crudo.decode("cp1252", errors="replace"))
    return renglones


def renglones_de_bitacora(ruta):
    """Las fallas anotadas en la bitácora, una por renglón (sin los títulos). Si el
    archivo no existe, ninguna; si no se puede leer, un ErrorMate."""
    try:
        renglones = leer_renglones(ruta)
    except FileNotFoundError:
        return []
    except (OSError, ErrorMate):
        raise ErrorMate(f"no pude leer la bitácora '{ruta}': fijate que no esté abierta en "
                        "otro programa")
    return [r.strip() for r in renglones if r.strip() and not r.startswith("#")]


def guardar_bitacora(ruta, programa, fallas, escrito=None):
    """Suma las fallas de esta corrida al final de la bitácora y deja las últimas
    MAX_BITACORA. Cada falla es (fecha, agente, qué pasó, qué atendía, motivo). La clave
    de la IA nunca queda escrita. Devuelve None o por qué no se pudo. escrito: el
    programa como se lo nombró al correrlo (con su carpeta), para el comando de arriba."""
    if not fallas:
        return None
    clave = os.environ.get("ANTHROPIC_API_KEY", "").strip().strip("\"'").strip()
    nuevos = [tapar_clave(" | ".join(
        [fecha] + [en_un_renglon(parte, 300).replace("|", "/") for parte in (quien, que, atendia)]
        + [en_un_renglon(motivo, 400)]), clave) for fecha, quien, que, atendia, motivo in fallas]
    try:
        renglones = (renglones_de_bitacora(ruta) + nuevos)[-MAX_BITACORA:]
        escribir_entero(ruta, "\n".join([
            f"# Bitácora de {programa}: las fallas de sus agentes, la más nueva abajo.",
            "# Cada renglón:  fecha | agente | qué pasó | qué mensaje atendía | el motivo",
            f"# La escribe Mate sola y guarda las últimas {MAX_BITACORA}. Para leerla "
            f"resumida:  {como_se_llama()} bitacora {para_pegar(escrito or programa)}",
            "# Si la borrás no pasa nada: empieza de nuevo.", ""] + renglones) + "\n")
    except (OSError, ValueError, ErrorMate):
        return (f"no pude anotar las fallas de esta corrida en la bitácora '{ruta}': fijate "
                "que no esté abierta en otro programa")
    return None


def para_pegar(a):
    """Un archivo o un nombre como hay que escribirlo en una orden: entre comillas si trae
    espacios, así el comando que Mate sugiere se puede copiar y pegar."""
    return f'"{a}"' if not a or re.search(r"\s", a) else a


def como_se_llama():
    """Cómo se escribe la orden para correr Mate en esta computadora. Si Mate se instaló
    con instalar.bat, la orden corta 'mate' anda desde cualquier carpeta: el lanzador que
    deja el instalador lo avisa con la variable MATE_ORDEN, y los comandos que Mate
    sugiere se escriben con esa orden."""
    if os.environ.get("MATE_ORDEN", "").strip().lower() == "mate":
        return "mate"
    return "python mate\\mate.py" if os.name == "nt" else "python3 mate/mate.py"


def incluidas():
    """Los nombres de las funciones incluidas (mostrar, texto, pesos...)."""
    return frozenset(FUNCIONES)


# ───────────────────────── Puente a Python (0.5) ─────────────────────────
# usar python "ayudas.py" trae las funciones de un archivo de Python que está al lado del
# programa, y se llaman ayudas.nombre(...). Sirve para sumar lo que Mate no trae sin tocar
# el intérprete. Tres reglas:
# - Solo cruzan valores simples: números, textos, verdadero/falso, nada, listas y mapas. Van
#   y vuelven COPIADOS: el Python no puede cambiarle una lista a Mate por atrás.
# - Un error dentro del Python llega como un error de Mate, con el renglón del .mate, y se
#   ataja con 'intentar'.
# - OJO: ese Python no tiene ninguno de los cuidados de Mate. Corre con todos los permisos
#   de la computadora (puede leer, escribir y borrar archivos, y salir a internet), también
#   con la orden 'probar'. Solo hay que usar archivos propios o de alguien de confianza.

# Los errores de Python más comunes, dichos en castellano (después va lo que dijo Python).
_ERRORES_DE_PYTHON = {
    "ZeroDivisionError": "una división por cero",
    "ValueError": "un valor que no sirve para lo que se quiso hacer",
    "TypeError": "una cuenta entre cosas de distinto tipo, o una función mal llamada",
    "KeyError": "una clave que no está en el diccionario",
    "IndexError": "una posición que no existe en la lista",
    "NameError": "un nombre que no existe (¿está mal escrito?)",
    "AttributeError": "se le pidió a un valor algo que no tiene",
    "FileNotFoundError": "un archivo que no está",
    "PermissionError": "falta permiso para tocar un archivo",
    "ModuleNotFoundError": "un 'import' de algo que no está instalado en esta computadora",
    "RecursionError": "una función que se llama a sí misma sin parar",
    "SystemExit": "el archivo quiso cerrar el programa (exit)",
}
SOLO_SIMPLES = "números, textos, verdadero o falso, nada, listas y mapas"


def dicho_por_python(e, ruta):
    """Un error de Python contado para quien no sabe Python: qué fue, en qué renglón del
    .py, y al final lo que dijo Python tal cual (eso viene en inglés)."""
    renglon, paso = None, e.__traceback__
    while paso is not None:  # el último renglón de ese archivo por el que pasó
        if paso.tb_frame.f_code.co_filename == ruta:
            renglon = paso.tb_lineno
        paso = paso.tb_next
    clase = type(e).__name__
    texto = str(e.args[0]) if clase == "KeyError" and e.args else str(e)
    crudo = recortado(f"{clase}: {texto}" if texto else clase, 300)
    que = _ERRORES_DE_PYTHON.get(clase)
    return ((f" (línea {renglon} de {os.path.basename(ruta)})" if renglon else "") + ": "
            + (f"{que}. Python dice: {crudo}" if que else f"Python dice: {crudo}"))


def a_python(v, donde):
    """Un valor de Mate, copiado, como lo recibe una función de Python."""
    if v is None or type(v) in (bool, int, float):
        return v
    if isinstance(v, str):
        return v[:]  # (un error atajado viaja como un texto común)
    if isinstance(v, list):
        return [a_python(x, donde) for x in v]
    if isinstance(v, dict):
        return {k[:]: a_python(x, donde) for k, x in v.items()}
    if isinstance(v, Registro):
        raise ErrorMate(f"{donde}(): a una función de Python solo se le pasan {SOLO_SIMPLES}, "
                        f"y recibió un mensaje {v.tipo}. Pasalo como mapa: a_mapa(...)",
                        familia="python")
    raise ErrorMate(f"{donde}(): a una función de Python solo se le pasan {SOLO_SIMPLES}, y "
                    f"recibió {un(v)}", familia="python")


def de_python(v, donde):
    """Lo que devolvió una función de Python, copiado, como valor de Mate."""
    if v is None or type(v) is bool:
        return v
    if type(v) is int:
        if v.bit_length() > MAX_BITS:
            raise ErrorMate(f"{donde}() devolvió un número demasiado grande para Mate",
                            familia="python")
        return v
    if type(v) is float:
        if not math.isfinite(v):
            raise ErrorMate(f"{donde}() devolvió un número que Mate no usa: infinito, o el "
                            "resultado de una cuenta imposible ('nan')", familia="python")
        return v
    if type(v) is str:
        if len(v) > MAX_LARGO:
            raise muy_largo()
        return v
    if isinstance(v, (list, tuple)):
        if len(v) > MAX_LARGO:
            raise muy_largo("la lista")
        return [de_python(x, donde) for x in v]
    if isinstance(v, dict):
        if len(v) > MAX_LARGO:
            raise muy_largo("la lista")
        for k in v:
            if type(k) is not str:
                raise ErrorMate(
                    f"{donde}() devolvió un diccionario con una clave que no es un texto "
                    f"({recortado(repr(k), 40)}): en Mate las claves de un mapa son textos. "
                    "Convertila en el .py con str(...)", familia="python")
        return {k: de_python(x, donde) for k, x in v.items()}
    raise ErrorMate(
        f"{donde}() devolvió algo que Mate no conoce (en Python se llama "
        f"'{type(v).__name__}'). A Mate solo vuelven números, textos, True o False, None, "
        "listas (o tuplas) y diccionarios con claves de texto. Convertilo en el .py antes "
        "de devolverlo", familia="python")


def funcion_de_python(completo, f, ruta):
    """La función de Python lista para llamarla desde Mate: controla cuántos valores lleva,
    copia lo que va y lo que vuelve, y lo que falle adentro sale como un error de Mate."""
    archivo, codigo = os.path.basename(ruta), f.__code__
    varios = bool(codigo.co_flags & 0x04)  # def f(*valores)
    maximo = None if varios else codigo.co_argcount
    minimo = codigo.co_argcount - len(f.__defaults__ or ())
    # Los parámetros que en Python solo se pueden dar con su nombre: desde Mate no se puede.
    con_nombre = codigo.co_varnames[codigo.co_argcount:
                                    codigo.co_argcount + codigo.co_kwonlyargcount]
    obligados = [n for n in con_nombre if n not in (f.__kwdefaults__ or {})]
    if minimo == maximo:
        lleva = f"{minimo} valor" + ("" if minimo == 1 else "es")
    elif maximo is None:
        lleva = (f"{minimo} valor{'' if minimo == 1 else 'es'} o más" if minimo
                 else "cualquier cantidad de valores")
    else:
        lleva = f"entre {minimo} y {maximo} valores"

    def llamada(args):
        if obligados:
            raise ErrorMate(
                f"{completo}() no se puede llamar desde Mate: en {archivo} pide '{obligados[0]}' "
                "por su nombre, y Mate pasa los valores en orden. En el .py, ponelo como un "
                "parámetro común", familia="python")
        if len(args) < minimo or (maximo is not None and len(args) > maximo):
            raise ErrorMate(f"{completo}() lleva {lleva} y recibió {len(args)} (así está "
                            f"escrita en {archivo})", familia="python")
        dados = [a_python(a, completo) for a in args]
        try:
            devuelto = f(*dados)
        except (ErrorMate, MemoryError):
            raise
        except (Exception, SystemExit) as e:
            raise ErrorMate(f"{completo}() falló adentro del Python"
                            + dicho_por_python(e, ruta), familia="python")
        try:
            return revisar_peso(de_python(devuelto, completo))
        except RecursionError:
            raise ErrorMate(f"{completo}() devolvió una lista o un diccionario que se tiene "
                            "a sí mismo adentro (o con demasiados niveles): Mate no lo "
                            "puede recibir", familia="python")
    return llamada


def cargar_python(nombre, ruta):
    """Abre el archivo de Python y devuelve su ModuloPython, con las funciones que se ven
    desde Mate: las escritas ahí con 'def' cuyo nombre no empieza con guion bajo. No deja
    ningún archivo al lado (ni la carpeta __pycache__ que arma Python cuando importa)."""
    archivo = os.path.basename(ruta)
    try:
        fuente = leer_fuente(ruta)
    except OSError:
        raise ErrorMate(f"no pude abrir {archivo}", familia="archivo")
    modulo = types.ModuleType(f"mate_python_{nombre}")
    modulo.__file__ = ruta
    try:
        exec(compile(fuente, ruta, "exec"), modulo.__dict__)
    except SyntaxError as e:
        donde = f" en su línea {e.lineno}" if e.lineno and e.filename == ruta else ""
        raise ErrorMate(f"{archivo} está mal escrito{donde} y Python no lo pudo leer. "
                        f"Python dice: {recortado(e.msg or 'SyntaxError', 300)}",
                        familia="python")
    except MemoryError:
        raise
    except (Exception, SystemExit) as e:
        raise ErrorMate(f"{archivo} falló apenas se lo abrió, antes de llamar a ninguna de "
                        "sus funciones" + dicho_por_python(e, ruta), familia="python")
    funciones = {
        n: DePython(f"{nombre}.{n}", funcion_de_python(f"{nombre}.{n}", f, ruta))
        for n, f in vars(modulo).items()
        if isinstance(f, types.FunctionType) and not n.startswith("_")
        and f.__module__ == modulo.__name__}
    return ModuloPython(nombre, ruta, funciones)


class Entorno:
    nacidos = 0  # cuántos entornos se crearon: sirve para saber cuál es anterior a cuál
    se_pisa = False  # solo en la consola: declarar de nuevo un nombre reemplaza al anterior

    def __init__(self, padre=None, frontera=False, borde=False):
        Entorno.nacidos = self.serie = Entorno.nacidos + 1
        self.vars = {}
        self.origen = {}  # de dónde salió cada nombre: sea, var, parametro, para, funcion...
        self.renglon = {}  # en qué renglón se declaró cada variable
        self.padre = padre
        self.raiz = self if padre is None else padre.raiz  # el de más afuera de todos
        self.frontera = frontera  # el estado de un agente: de acá para arriba no se escribe
        self.borde = borde  # donde empieza una función, un 'al recibir' o una prueba

    def definir(self, nombre, valor, mutable=False, origen=None, linea=None):
        # (el programa puede usar para lo suyo los nombres de SE_PUEDEN_TAPAR)
        if nombre in self.vars and not (
                nombre in SE_PUEDEN_TAPAR and self.origen.get(nombre) == "nativa") and not (
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
        raiz = self.raiz  # tampoco se tapa una función incluida desde adentro
        if raiz is not self and raiz.origen.get(nombre) == "nativa" \
                and nombre not in SE_PUEDEN_TAPAR:
            raise ErrorMate(INCLUIDA.format(n=nombre))
        self.vars[nombre] = [valor, mutable]
        self.origen[nombre] = origen or ("var" if mutable else "sea")
        if linea:
            self.renglon[nombre] = linea

    def no_tapar(self, nombre):
        """Un 'sea' o 'var' de un bloque de adentro (si, mientras, para, intentar) no
        puede repetir el nombre de una variable de más afuera: casi siempre se quiso
        cambiar esa variable, y con el 'sea' de más no cambia nada."""
        def ya_existe():
            return ErrorMate(
                f"'{nombre}' ya existe afuera de este bloque. Si querés cambiarle el "
                f"valor, sacá el 'sea' o el 'var': {nombre} = ... Si es otra cosa, "
                "ponele otro nombre")
        e = self
        while not e.borde and e.padre is not None:
            e = e.padre
            if nombre in e.vars and e.origen.get(nombre) in (
                    "sea", "var", "parametro", "para", "mensaje", "falla"):
                raise ya_existe()
        # Desde un bloque de adentro de una función, una prueba o un 'al recibir' tampoco
        # se tapa una variable 'var' del programa: ahí también se la quiso cambiar.
        afuera = e.padre if (e.borde and e is not self) else None
        while afuera is not None:
            if nombre in afuera.vars:
                if afuera.origen.get(nombre) == "var" and not afuera.frontera:
                    raise ya_existe()
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
        self.reglas = {}  # mensaje -> {campo: lo que dice de sus valores: desde, hasta...}
        self.agentes = {}
        self.decl_agentes = []
        self.copias = {}
        self.cola = deque()
        self.contexto = None  # (agente, remitente, tipo de mensaje) mientras se atiende uno
        self.entregados = 0
        # El "sobre" de cada entrega (mejora 99): su número, quién, a quién, en respuesta
        # a cuál y el número de conversación. Una conversación empieza cuando el programa
        # manda algo; lo que los agentes mandan mientras lo atienden sigue en la misma.
        self.conversaciones = 0  # cuántas conversaciones empezaron
        self.conversacion = None  # la del mensaje que se está atendiendo
        self.historial = []  # en una prueba: los sobres de lo que se mandó (mejora 98)
        self.desde = (0, 0)  # el número de mensaje y de conversación al empezar la prueba
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
        self.tecleado = None  # en una prueba: lo que dijo simular_teclado() (una lista)
        self.tecleados = 0  # cuántos de esa lista ya se dieron
        # Con 'probar', agregar_a_archivo() no toca el disco (0.5): lo agregado queda acá
        # (ruta -> texto entero) y leer_archivo() y leer_tabla() lo ven. None = se escribe.
        self.archivos_de_prueba = None
        self.fecha_fija = False  # en las pruebas hoy() y ahora() dan siempre lo mismo
        # La IA (mejora 100). Simulada no sale a la red: en las pruebas siempre es así.
        self.ia_simulada = False
        self.ia_respuestas = []  # del archivo de --ia-simulada=archivo: (si trae, contesta)
        self.ia_fijada = None  # en una prueba: lo que dijo simular_ia() (una lista)
        self.ia_en_orden = False  # si simular_ia() recibió una lista: se dan una por vez
        self.ia_usadas = 0  # cuántas de esa lista ya se dieron
        self.ia_consultas = 0  # consultas de verdad en esta corrida
        self.ia_historial = []  # en una prueba: lo que se le consultó a la IA
        # Lo que aprenden los agentes (0.4). Solo 'correr' con un archivo lo llena: con
        # 'probar', en la consola y en las pruebas queda así, y nada toca el disco.
        self.recordando = False  # si los 'estado recordado' se recuperan de la memoria
        self.memoria = {}  # lo leído del archivo: agente -> {"estado": ..., "lecciones": ...}
        self.bitacora = None  # una lista, si las fallas de los agentes se anotan
        self.avisar = lambda texto: None  # por dónde salen los avisos de la memoria
        self.avisados = set()  # los avisos que se dan una sola vez por corrida
        self.guardar_cuenta = None  # 'correr': deja la cuenta de consultas en el disco
        self.calculando_frenos = False  # mientras se calculan los valores de unos 'frenos'
        self._armados = {}  # lo que ya está armado para correr (ver 'armar_bloque')
        self._nativas()

    # ── funciones incorporadas ──
    def _nativas(self):
        def nativa(nombre):
            def deco(fn):
                minimo, maximo = FUNCIONES[nombre][:2]

                def envuelta(args):
                    """Ninguna función incluida falla con un error de Python."""
                    cuantos = len(args)
                    if cuantos < minimo or (maximo is not None and cuantos > maximo):
                        raise ErrorMate(cantidad_equivocada(nombre, cuantos))
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
                self.glob.definir(nombre, Nativa(nombre, envuelta), origen="nativa")
                return fn
            return deco

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
                if self.tecleado is not None and self.tecleados < len(self.tecleado):
                    self.tecleados += 1  # lo que fijó simular_teclado(), de a uno
                    return self.tecleado[self.tecleados - 1].strip()
                if preparada is None and self.tecleado is not None:
                    raise ErrorMate(
                        f"la prueba llegó a {self.tecleados + 1} leer() y simular_teclado() "
                        f"tenía {len(self.tecleado)} texto(s): agregá los que faltan a la "
                        "lista, o dale a ese leer() una respuesta preparada como segundo "
                        'valor, por ejemplo leer("Cliente:", "chau")')
                if preparada is None:
                    raise ErrorMate(
                        "en las pruebas leer() no espera el teclado: dale una respuesta "
                        'preparada como segundo valor, por ejemplo leer("¿Cuántos?", "3"), '
                        'o fijá antes lo que se teclea: simular_teclado(["3"])')
                return preparada
            try:
                # (si lo tecleado llega de un archivo con marca al principio, se le saca)
                return self.entrada(pregunta).replace("\ufeff", "").strip()
            except KeyboardInterrupt:
                raise CorteEnElTeclado()
            except (EOFError, OSError):
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

        def texto_del_archivo(nombre, donde, si_no_esta=None):
            """El texto de un archivo de la carpeta del programa, para leer_archivo() y
            leer_tabla(). Si no está, el error dice en qué carpeta se lo buscó."""
            carpeta, ruta = archivo_de_datos(nombre, donde)
            if os.path.isdir(ruta):
                raise ErrorMate(f"{donde}: '{nombre}' es una carpeta, no un archivo",
                                familia="archivo")
            if self.archivos_de_prueba is not None and ruta in self.archivos_de_prueba:
                return self.archivos_de_prueba[ruta]  # lo que 'agregó' la prueba
            try:
                if donde == "leer_tabla()" and es_de_excel(ruta):
                    raise ErrorMate("es una planilla de Excel sin convertir")
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
                if si_no_esta is not None:
                    return si_no_esta
                raise ErrorMate(f"{donde}: no encuentro el archivo '{nombre}' en "
                                f"{os.path.dirname(ruta)}.{pista}".rstrip("."), familia="archivo")
            except OSError:
                raise ErrorMate(f"{donde}: no pude abrir '{nombre}'", familia="archivo")
            except ErrorMate:
                if es_de_excel(ruta):
                    raise ErrorMate(f"{donde}: '{nombre}' es una planilla de Excel, y Mate "
                                    f"lee texto. {COMO_GUARDAR_CSV}", familia="archivo")
                raise ErrorMate(f"{donde}: no pude leer las letras de '{nombre}': "
                                "¿seguro que es un archivo de texto?", familia="archivo")
            if len(contenido) > MAX_LARGO:
                raise ErrorMate(f"{donde}: '{nombre}' es demasiado grande para leerlo "
                                "entero", familia="archivo")
            return contenido

        nativa("leer_archivo")(lambda nombre: texto_del_archivo(nombre, "leer_archivo()"))

        @nativa("leer_tabla")
        def _(nombre):
            pedir(nombre, "texto", "leer_tabla()")
            if nombre.strip().lower().endswith((".xlsx", ".xls", ".xlsm", ".ods")):
                raise ErrorMate(
                    f"leer_tabla(): '{nombre}' es una planilla de Excel, y Mate lee la "
                    f"planilla guardada como CSV. {COMO_GUARDAR_CSV}; después nombrala con "
                    f'.csv: leer_tabla("{os.path.splitext(nombre.strip())[0]}.csv")',
                    familia="archivo")
            return tabla_de_texto(texto_del_archivo(nombre, "leer_tabla()"), nombre)

        def donde_guardar(nombre, contenido, donde):
            """Los controles antes de guardar algo: devuelve la ruta completa."""
            carpeta, ruta = archivo_de_datos(nombre, donde)
            if nombre_tipo(contenido) != "texto":
                raise ErrorMate(
                    f"{donde} guarda un texto y recibió {tipo_claro(contenido)}. "
                    'Pasalo a texto antes: texto(valor), unir(lista, "\\n") o a_json(valor)')
            # (Windows ignora los puntos y espacios del final, y lo que sigue a un ':')
            if os.path.basename(ruta).split(":")[0].rstrip(". ").lower().endswith(NO_SE_PISAN):
                raise ErrorMate(
                    f"{donde} no escribe en '{nombre}' para no pisar un programa: "
                    'elegí otro nombre, por ejemplo "notas.txt"', familia="archivo")
            if os.path.isdir(ruta):
                raise ErrorMate(f"{donde}: '{nombre}' es una carpeta, no un archivo",
                                familia="archivo")
            try:
                contenido.encode("utf-8")  # antes de tocar el archivo: si falla, queda como estaba
            except UnicodeError:
                raise ErrorMate(
                    f"{donde}: el texto trae una letra que no se puede guardar "
                    f"(un símbolo roto, que suele venir de un JSON). '{nombre}' quedó como "
                    "estaba", familia="archivo")
            return ruta

        def guardar_en(ruta, nombre, donde, escribir):
            try:
                escribir()
            except FileNotFoundError:
                raise ErrorMate(f"{donde}: no existe la carpeta donde iría "
                                f"'{nombre}'. Creala antes, o guardá el archivo al lado del "
                                "programa", familia="archivo")
            except (OSError, UnicodeError):
                raise ErrorMate(f"{donde}: no pude guardar '{nombre}' (¿está "
                                "abierto en otro programa, o no hay permiso?)",
                                familia="archivo")

        @nativa("escribir_archivo")
        def _(nombre, contenido):
            ruta = donde_guardar(nombre, contenido, "escribir_archivo()")

            def escribir():
                # con la marca del principio, para que el Bloc de notas muestre bien las tildes
                with open(ruta, "w", encoding="utf-8-sig") as f:
                    f.write(contenido)
            guardar_en(ruta, nombre, "escribir_archivo()", escribir)

        @nativa("agregar_a_archivo")
        def _(nombre, renglon):
            ruta = donde_guardar(nombre, renglon, "agregar_a_archivo()")
            if not renglon.endswith("\n"):
                renglon += "\n"  # cada agregado es un renglón
            # Lo que el archivo ya tenía, y si se le puede sumar al final tal como está
            # (UTF-8) o hay que guardarlo entero de nuevo (lo dejó el Bloc de notas en ANSI
            # o en "Unicode": mezclar codificaciones rompería las tildes).
            antes = texto_del_archivo(nombre, "agregar_a_archivo()", si_no_esta="")
            if antes and not antes.endswith("\n"):
                antes += "\n"
            if len(antes) + len(renglon) > MAX_LARGO:
                raise ErrorMate(f"agregar_a_archivo(): '{nombre}' ya es demasiado grande: "
                                "empezá un archivo nuevo, con otro nombre", familia="archivo")
            if self.archivos_de_prueba is not None:
                self.archivos_de_prueba[ruta] = antes + renglon  # 'probar' no toca el disco
                return

            def escribir():
                try:
                    with open(ruta, "rb") as f:
                        crudo = f.read()
                except FileNotFoundError:
                    crudo = None
                if crudo is None or not crudo:
                    with open(ruta, "w", encoding="utf-8-sig") as f:
                        f.write(renglon)
                    return
                try:
                    crudo.decode("utf-8")
                except UnicodeError:
                    escribir_entero(ruta, antes + renglon)
                    return
                with open(ruta, "a", encoding="utf-8") as f:
                    f.write(renglon if crudo.endswith(b"\n") else "\n" + renglon)
            guardar_en(ruta, nombre, "agregar_a_archivo()", escribir)

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

        @nativa("consultar_ia")
        def _(instrucciones, pregunta, preparada=None):
            pedir(instrucciones, "texto", "consultar_ia()")
            pedir(pregunta, "texto", "consultar_ia()")
            if preparada is not None:
                pedir(preparada, "texto", "el tercer valor de consultar_ia()")
            if not pregunta.strip():
                raise error_de_ia("la pregunta está vacía: no hay nada para consultarle")
            quien = self.contexto[0].nombre if self.contexto else "(programa)"
            hondo = len(self.atendiendo)
            # Los frenos del agente (0.5). Sin frenos, todo sigue como siempre.
            agente = self.contexto[0] if self.contexto else None
            frenos = self.frenos_de(agente) if agente is not None and agente.decl[6] else None
            if frenos is None:
                return una_consulta(instrucciones, pregunta, preparada, quien, hondo)[0]
            return self.con_frenos(
                agente, frenos, instrucciones, pregunta, momento(),
                lambda de_nuevo=None: una_consulta(
                    instrucciones, de_nuevo or pregunta, preparada, quien, hondo,
                    simulada_con=pregunta))

        def una_consulta(instrucciones, pregunta, preparada, quien, hondo, simulada_con=None):
            """Una consulta a la IA (de verdad o simulada). Devuelve (lo que contestó, la
            anotación que queda para consultas_ia()). simulada_con: en el segundo intento
            de un freno, la respuesta simulada se busca por la pregunta original."""
            # Las lecciones del agente van solas al final de las instrucciones (0.4).
            aprendidas = self.lecciones_de(self.contexto[0]) if self.contexto else []
            if aprendidas:
                instrucciones = con_lecciones(instrucciones, aprendidas)
            if self.traza:
                self.trazar(f"{quien} consulta a la IA"
                            f"{' (simulada)' if self.ia_simulada else ''}: "
                            f"{recortado(pregunta)}", None, hondo)
                for i, leccion in enumerate(aprendidas, 1):
                    self.trazar(f"   con la lección {i}: {recortado(leccion)}", None, hondo)
            consulta = {"agente": quien, "instrucciones": instrucciones,
                        "pregunta": pregunta, "respuesta": None}
            if self.en_prueba:
                self.ia_historial.append(consulta)
            try:
                if self.ia_simulada:
                    respuesta = self.respuesta_simulada(simulada_con or pregunta, preparada)
                else:
                    if self.max_pasos is not None and self.ia_consultas >= MAX_CONSULTAS_IA:
                        raise ErrorMate(
                            f"el programa ya le hizo {MAX_CONSULTAS_IA} consultas a la IA y "
                            "cada una se paga: lo freno por si los agentes entraron en "
                            "bucle. Si de verdad hacen falta más, corré con --sin-limite",
                            clase="limite")
                    self.ia_consultas += 1
                    _USO_DE_LA_IA.clear()
                    try:
                        respuesta = pedir_a_la_ia(instrucciones, pregunta)
                    except (ErrorMate, KeyboardInterrupt, MemoryError):
                        raise
                    except Exception as e:  # nunca un error de Python (ni la clave) a la vista
                        raise error_de_ia("algo salió mal al hablar con la IA y no sé "
                                          f"explicarlo mejor ({type(e).__name__})")
            except ErrorMate as e:
                if self.traza:
                    self.trazar("la IA no contestó: " + e.mensaje.split("\n")[0], None, hondo)
                raise
            if len(respuesta) > MAX_LARGO:
                raise error_de_ia("la respuesta es demasiado larga para guardarla")
            if self.traza:
                self.trazar(f"la IA contesta: {recortado(respuesta)}", None, hondo)
            consulta["respuesta"] = respuesta
            return respuesta, consulta

        @nativa("consultas_ia")
        def _():
            if not self.en_prueba:
                raise ErrorMate(CONSULTAS_IA_SUELTO)
            if self.contexto is None:
                self.vaciar_cola()  # lo enviado en la prueba llega antes de mirar
            return [dict(consulta) for consulta in self.ia_historial]

        @nativa("aprender")
        def _(leccion, agente=None):
            quien = self.el_que_aprende("aprender", agente)
            try:
                texto = leccion_limpia(pedir(leccion, "texto", "aprender()"))
            except ErrorMate as e:
                e.mensaje = e.mensaje if e.mensaje.startswith("aprender()") \
                    else "aprender(): " + e.mensaje
                raise
            nuevas, olvidadas = sumar_leccion(
                quien.lecciones, texto, momento().strftime("%d/%m/%Y %H:%M"))
            if nuevas is quien.lecciones:
                return  # ya la sabía: no se anota dos veces
            quien.lecciones = nuevas
            if self.traza:
                self.trazar(f"{quien.nombre} aprende: {recortado(texto)}", None,
                            len(self.atendiendo))
            if olvidadas:
                self.avisar_una_vez(("tope", quien.nombre), (
                    f"{quien.nombre} ya tenía {MAX_LECCIONES} lecciones, que es el tope: "
                    "para anotar la nueva se olvidó de la más vieja"))

        @nativa("lecciones")
        def _(agente=None):
            return self.lecciones_de(self.el_que_aprende("lecciones", agente))

        @nativa("simular_ia")
        def _(respuesta):
            if not self.en_prueba:
                raise ErrorMate(SIMULAR_IA_SUELTO)
            en_orden = isinstance(respuesta, list)
            lista = respuesta if en_orden else [respuesta]
            if not lista or not all(isinstance(r, str) and r.strip() for r in lista):
                raise ErrorMate(
                    "simular_ia() espera el texto que va a contestar la IA, o una lista de "
                    f"textos para que los dé en orden, y recibió {tipo_claro(respuesta)}"
                    + (" (vacía, o con algo que no es un texto con letras)" if en_orden
                       else " (vacío)" if isinstance(respuesta, str) else ""))
            self.ia_fijada, self.ia_en_orden, self.ia_usadas = list(lista), en_orden, 0

        @nativa("simular_teclado")
        def _(tecleado):
            if not self.en_prueba:
                raise ErrorMate(SIMULAR_TECLADO_SUELTO)
            lista = tecleado if isinstance(tecleado, list) else [tecleado]
            if not lista or not all(isinstance(t, str) for t in lista):
                raise ErrorMate(
                    "simular_teclado() espera lo que 'teclea' la persona: un texto, o una "
                    'lista de textos para que salgan en orden, uno por cada leer() (por '
                    f'ejemplo simular_teclado(["hola", "chau"])), y recibió '
                    f"{un(tecleado)}"
                    + (" (vacía, o con algo que no es un texto)"
                       if isinstance(tecleado, list) else ""))
            self.tecleado, self.tecleados = list(lista), 0

        @nativa("mensajes_enviados")
        def _(tipo=None):
            if not self.en_prueba:
                raise ErrorMate(SOLO_EN_PRUEBA)
            if tipo is not None and pedir(tipo, "texto", "mensajes_enviados()") \
                    not in self.mensajes:
                raise ErrorMate(con_sugerencia(
                    f"mensajes_enviados(): no existe el mensaje '{tipo}'", tipo, self.mensajes))
            if self.contexto is None:
                self.vaciar_cola()  # lo enviado en la prueba llega antes de mirar
            numero0, conversacion0 = self.desde
            return [{"numero": numero - numero0, "de": de, "a": a, "tipo": msg.tipo,
                     "mensaje": msg, "pregunta": pregunta,
                     "conversacion": conversacion - conversacion0,
                     "respuesta_a": respuesta_a - numero0 if respuesta_a else None}
                    for numero, de, a, msg, pregunta, conversacion, respuesta_a
                    in self.historial if tipo is None or msg.tipo == tipo]

    # ── lo que aprenden los agentes (0.4) ──
    def el_que_aprende(self, funcion, agente):
        """De quién son las lecciones de aprender() o lecciones(): del agente que está
        atendiendo o, en una prueba, del que se nombra."""
        if self.contexto is not None:
            if agente is not None and agente is not self.contexto[0]:
                raise ErrorMate(f"{funcion}(): dentro de un agente va sin decir a cuál: cada "
                                "uno anota y lee solo sus propias lecciones")
            return self.contexto[0]
        antes = '"la lección", ' if funcion == "aprender" else ""
        if not self.en_prueba:
            raise ErrorMate(SOLO_EN_AGENTE.format(n=funcion, antes=antes))
        if agente is None:
            raise ErrorMate(f"{funcion}(): en una prueba hay que decir de qué agente: "
                            f"{funcion}({antes}Mostrador)")
        if not isinstance(agente, Agente):
            raise ErrorMate(f"{funcion}() espera un agente (por ejemplo "
                            f"{funcion}({antes}Mostrador)) y recibió {un(agente)}")
        self.vaciar_cola()  # lo enviado en la prueba llega antes de mirar
        return agente

    def lecciones_de(self, agente):
        """Las lecciones que valen para ese agente, como textos: las suyas y, si es una
        copia, antes las del agente del que es copia. Nunca más que el tope."""
        molde = self.agentes.get(agente.decl[2])
        todas = (molde.lecciones if molde is not None and molde is not agente else []) \
            + agente.lecciones
        if len(todas) > MAX_LECCIONES:
            self.avisar_una_vez(("muchas", agente.nombre), (
                f"entre las suyas y las de {agente.decl[2]}, {agente.nombre} tiene más de "
                f"{MAX_LECCIONES} lecciones, que es el tope: usa solo las más nuevas"))
        return [leccion["texto"] for leccion in todas[-MAX_LECCIONES:]]

    # ── frenos para la IA y tope de gasto (0.5) ──
    def frenos_de(self, agente):
        """Los frenos de ese agente con sus valores de ahora (se calculan en cada consulta,
        así 'precios: lista' sigue a la lista aunque cambie). Un valor 'nada' es "sin esa
        regla". Lo que no tiene la forma de su regla es un error que dice cuál y cómo va."""
        if self.calculando_frenos:
            raise error_de_ia("dentro de 'frenos' no se puede consultar a la IA: ahí van "
                              "datos (una lista, un número, un texto)")
        frenos = dict.fromkeys(REGLAS_DE_FRENO)
        self.calculando_frenos = True
        try:
            for ln, regla, e in agente.decl[6]:
                try:
                    valor = self.ev(e, agente.env)
                    if valor is None:
                        continue
                    que = f"en los frenos de {agente.decl[2]}, '{regla}'"
                    ejemplo = f". Por ejemplo:  {REGLAS_DE_FRENO[regla][1]}"
                    if nombre_tipo(valor) not in REGLAS_DE_FRENO[regla][0]:
                        raise ErrorMate(f"{que} recibió {un(valor)} y lleva otra cosa: son "
                                        f"{REGLAS_DE_FRENO[regla][2]}{ejemplo}")
                    if regla == "precios":
                        valor = numeros_permitidos(valor)
                    elif regla == "prohibido":
                        if len(valor) > MAX_PROHIBIDOS or not all(
                                isinstance(t, str) and t.strip() for t in valor):
                            raise ErrorMate(
                                f"{que} lleva una lista de textos (palabras o frases, hasta "
                                f"{MAX_PROHIBIDOS}, ninguna vacía){ejemplo}")
                    elif regla == "reserva":
                        if not valor.strip():
                            raise ErrorMate(f"{que} está vacía: es lo que va a leer el "
                                            f"cliente cuando salte un freno{ejemplo}")
                    elif type(valor) is not int or valor < (1 if regla == "largo" else 0):
                        raise ErrorMate(f"{que} lleva un número entero"
                                        f"{' mayor que cero' if regla == 'largo' else ''} y "
                                        f"recibió {formato(valor)}{ejemplo}")
                    frenos[regla] = valor
                except ErrorMate as error:
                    error.linea = ln
                    raise
        finally:
            self.calculando_frenos = False
        if frenos["reserva"] is None and any(
                frenos[regla] is not None for regla in REGLAS_DE_CONTENIDO):
            raise ErrorMate(f"a los frenos de {agente.decl[2]} les falta 'reserva' (quedó en "
                            "nada): es lo que contesta cuando la IA rompe una regla dos veces",
                            agente.decl[6][0][0])
        return frenos

    def anotar_freno(self, agente, que, pregunta, motivo):
        """Un freno que saltó (o un tope alcanzado), para la bitácora."""
        if self.bitacora is None or self.en_prueba:
            return
        self.bitacora.append((datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                              agente.nombre, que, f"la consulta {recortado(pregunta)}", motivo))

    def con_frenos(self, agente, frenos, instrucciones, pregunta, ahora, consultar):
        """consultar_ia() de un agente con frenos: mira el tope de gasto, consulta, revisa
        la respuesta y, si rompe una regla, consulta UNA vez más avisándole a la IA cuál;
        si la vuelve a romper, devuelve el texto de reserva. Todo queda en la traza, en la
        bitácora y en consultas_ia() (los campos 'freno' y 'devuelto')."""
        quien, hondo = agente.nombre, len(self.atendiendo)
        molde = self.agentes.get(agente.decl[2], agente)  # las copias cuentan con el original
        dia, simulada = ahora.strftime("%Y-%m-%d"), self.ia_simulada
        anotadas = []

        def en_el_tope():
            hoy = molde.gasto.get(dia, {})
            hechas = hoy.get("simuladas" if simulada else "consultas", 0)
            tope = frenos["consultas_por_dia"]
            if tope is not None and hechas >= tope:
                return (f"ya hizo {hechas} consulta(s) {'simuladas ' if simulada else ''}a "
                        f"la IA hoy y su tope es {tope} por día")
            tope = frenos["tokens_por_dia"]
            if tope is not None and not simulada and hoy.get("tokens", 0) >= tope:
                return f"ya gastó {hoy['tokens']} tokens hoy y su tope es {tope} por día"
            return None

        def contar():
            hoy = molde.gasto.setdefault(dia, {"consultas": 0, "simuladas": 0, "tokens": 0})
            if simulada:
                hoy["simuladas"] += 1
                return
            hoy["consultas"] += 1
            hoy["tokens"] += _USO_DE_LA_IA.get("tokens") or 0
            if self.guardar_cuenta is not None and not self.en_prueba:
                self.guardar_cuenta()  # ya, por si después cierran la ventana

        def devolver(valor):
            for consulta in anotadas:
                consulta.setdefault("freno", "")
                consulta["devuelto"] = valor
            return valor

        def trazar(texto):
            if self.traza:
                self.trazar(texto, None, hondo)

        def sin_consultar(tope, que):
            """Se llegó al tope: no se consulta. Sale la reserva o, si no hay, un error."""
            trazar(f"tope de {quien}: {tope}. No consulta"
                   + ("" if frenos["reserva"] is None else " y devuelve el texto de reserva"))
            if (quien, "tope") not in self.avisados:  # una vez por corrida en la bitácora
                self.avisados.add((quien, "tope"))
                self.anotar_freno(agente, "llegó al tope de gasto", pregunta, tope)
            if self.en_prueba and not anotadas:
                anotadas.append({"agente": quien, "instrucciones": instrucciones,
                                 "pregunta": pregunta, "respuesta": None, "freno": que})
                self.ia_historial.append(anotadas[-1])
            if frenos["reserva"] is None:
                devolver(None)
                raise ErrorMate(
                    f"consultar_ia(): {quien} {tope}: por hoy no consulta más. (Para que en "
                    "vez de fallar conteste algo, ponele una 'reserva' a sus frenos; el "
                    "tope se cambia ahí mismo)", familia="tope")
            return devolver(frenos["reserva"])

        tope = en_el_tope()
        if tope:
            return sin_consultar(tope, "tope de gasto: " + tope)
        respuesta, consulta = consultar()
        contar()
        anotadas.append(consulta)
        rotas = reglas_rotas(respuesta, frenos)
        if not rotas:
            return devolver(respuesta)
        que = "; ".join(motivo for _, motivo, _ in rotas)
        consulta["freno"] = que
        dicho = f"La IA había contestado: {recortado(respuesta, 200)}"
        trazar(f"freno de {quien}: la respuesta no pasa ({que}). Consulta una vez más")
        if self.recordando and not self.en_prueba:
            # Queda una lección propuesta: no se usa hasta que el dueño la aprueba.
            cuantas = len(molde.propuestas)
            for _, motivo, leccion in rotas:
                molde.propuestas = sumar_propuesta(
                    molde.propuestas, molde.lecciones, leccion,
                    f"saltó un freno: {motivo}. {dicho}", ahora.strftime("%d/%m/%Y %H:%M"))
            if len(molde.propuestas) != cuantas:
                self.avisar_una_vez(("propuestas", molde.nombre), (
                    f"saltó un freno de {molde.nombre} y quedó una lección propuesta, que "
                    "no se usa hasta que la apruebes. Para verlas:  "
                    f"{como_se_llama()} propuestas {para_pegar(self.archivo or 'programa.mate')}"))
        tope = en_el_tope()
        if tope:
            self.anotar_freno(agente, "saltó un freno (contestó con el texto de reserva)",
                              pregunta, f"{que}. {dicho}. No hubo segundo intento: {tope}")
            self.avisados.add((quien, "tope"))  # (ya quedó dicho en ese renglón)
            return sin_consultar(tope, que)
        try:
            respuesta, consulta = consultar(aviso_de_freno(pregunta, rotas))
        except ErrorMate as error:
            if error.clase != "falla":
                raise
            segundo = "el segundo intento falló (" + error.mensaje.split("\n")[0] + ")"
        else:
            contar()
            anotadas.append(consulta)
            rotas = reglas_rotas(respuesta, frenos)
            if not rotas:
                trazar(f"freno de {quien}: el segundo intento pasa")
                self.anotar_freno(agente, "saltó un freno (el segundo intento salió bien)",
                                  pregunta, f"{que}. {dicho}")
                return devolver(respuesta)
            consulta["freno"] = "; ".join(motivo for _, motivo, _ in rotas)
            segundo = f"el segundo intento tampoco pasa ({consulta['freno']})"
        trazar(f"freno de {quien}: {segundo}. Devuelve el texto de reserva: "
               f"{recortado(frenos['reserva'])}")
        self.anotar_freno(agente, "saltó un freno (contestó con el texto de reserva)",
                          pregunta, f"{que}. {dicho}")
        return devolver(frenos["reserva"])

    def avisar_una_vez(self, cual, texto):
        if cual not in self.avisados:
            self.avisados.add(cual)
            self.avisar(texto)

    def recordado(self, agente, nombre, inicial):
        """El valor con que arranca un 'estado recordado': el que quedó guardado en la
        corrida anterior o, si no hay (o ya no es del mismo tipo), el inicial."""
        if not self.recordando:
            return inicial
        if not agente.recuerda:
            molde = agente.decl[2]
            self.avisar_una_vez(("sin nombre", molde), (
                f"las copias de {molde} creadas sin nombre no recuerdan nada de una corrida "
                "a la otra (no se sabría cuál es cuál). Para que una copia tenga memoria, "
                f'dale un nombre:  crear {molde} llamado "Centro"'))
            return inicial
        guardado = self.memoria.get(agente.nombre, {}).get("estado", {})
        if nombre not in guardado:
            return inicial
        de = f"{agente.nombre}.{nombre}"
        try:
            valor = self._de_json(guardado[nombre], memoria=True)
        except ErrorMate as e:
            self.avisar(f"lo que {de} tenía guardado en la memoria ya no sirve "
                        f"({e.mensaje}): arranca con su valor inicial")
            return inicial
        if inicial is not None and valor is not None \
                and nombre_tipo(valor) != nombre_tipo(inicial):
            self.avisar(f"{de} está guardado en la memoria como {nombre_tipo(valor)} y en el "
                        f"programa ahora es {nombre_tipo(inicial)}: no uso lo guardado y "
                        "arranca con su valor inicial")
            return inicial
        return valor

    def memoria_actual(self):
        """Lo que hay que guardar al terminar: lo que se leyó, con el estado recordado y
        las lecciones de los agentes de esta corrida puestos encima."""
        nueva = {a: dict(f, estado=dict(f["estado"]), lecciones=list(f["lecciones"]))
                 for a, f in self.memoria.items()}
        for agente in list(self.agentes.values()) + self.vivos:
            if not agente.recuerda:
                continue
            previa = nueva.get(agente.nombre, {"estado": {}})["estado"]
            estado = {}
            for declarado in (agente.decl[3] if agente.env is not None else ()):
                nombre = declarado[1]
                if not isinstance(declarado, EstadoRecordado) or nombre not in agente.env.vars:
                    continue
                valor = agente.env.vars[nombre][0]
                try:
                    if not se_puede_recordar(valor):
                        raise ValueError
                    estado[nombre] = self._a_json(valor, memoria=True)
                    json.dumps(estado[nombre], allow_nan=False)
                except (ErrorMate, ValueError, RecursionError):
                    estado.pop(nombre, None)
                    if nombre in previa:
                        estado[nombre] = previa[nombre]
                    self.avisar(
                        f"{agente.nombre}.{nombre} no se pudo guardar en la memoria: solo "
                        "se recuerdan datos (números, textos, listas, mapas y mensajes), "
                        "no agentes ni funciones")
            if agente.env is None:
                estado = previa  # no llegó a nacer en esta corrida: queda lo que había
            ficha = {"estado": estado, "lecciones": list(agente.lecciones)}
            if self.agentes.get(agente.nombre) is agente:
                propuestas, gasto = list(agente.propuestas), gasto_limpio(agente.gasto)
            else:  # una copia con nombre: lo que tuviera anotado a mano queda como estaba
                anterior = nueva.get(agente.nombre, {})
                propuestas, gasto = anterior.get("propuestas"), anterior.get("gasto")
            if propuestas:
                ficha["propuestas"] = propuestas
            if gasto:
                ficha["gasto"] = gasto
            nueva[agente.nombre] = ficha
        return {a: f for a, f in nueva.items() if any(f.values())}

    def anotar_falla(self, agente, e, msg, atajada=False):
        """Una falla de un agente, para la bitácora (si este programa la lleva). El mismo
        error no se anota dos veces para el mismo agente."""
        if self.bitacora is None or self.en_prueba:
            return
        vistos = e.__dict__.setdefault("en_bitacora", set())
        if agente.nombre in vistos:
            return
        vistos.add(agente.nombre)
        que = {"ia": "la IA no contestó", "contrato": "contrato rechazado"}.get(
            e.familia, "falló")
        if atajada:
            que += " (lo atajó con 'intentar')"
        if msg is None:
            atendia = "(ningún mensaje)"
        elif msg.tipo == AL_FALLAR:
            atendia = "el aviso de que un mensaje suyo no se pudo atender"
        else:
            atendia = formato(msg)
        self.bitacora.append((datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                              agente.nombre, que, atendia, e.mensaje))

    def respuesta_simulada(self, pregunta, preparada):
        """Lo que contesta la IA cuando no se sale a la red. Manda lo que fijó la prueba con
        simular_ia(); si no, el archivo de respuestas; si no, el tercer valor de la llamada."""
        if self.ia_fijada is not None:
            if not self.ia_en_orden:
                return self.ia_fijada[0]
            if self.ia_usadas >= len(self.ia_fijada):
                raise error_de_ia(
                    f"la prueba le hizo {self.ia_usadas + 1} consultas a la IA y simular_ia() "
                    f"tenía {len(self.ia_fijada)} respuesta(s): agregá las que faltan a la "
                    "lista")
            self.ia_usadas += 1
            return self.ia_fijada[self.ia_usadas - 1]
        del_archivo = respuesta_del_archivo(self.ia_respuestas, pregunta)
        if del_archivo is not None:
            return del_archivo
        if preparada is not None:
            return preparada
        if self.ia_respuestas:
            raise error_de_ia(
                "el archivo de respuestas simuladas no tiene ninguna para esta consulta: "
                f"{recortado(pregunta)}. Agregale un renglón, o uno que conteste a todo:  "
                "* => lo que contesta")
        raise ErrorMate(SIN_RESPUESTA_SIMULADA, familia="ia")

    def _a_json(self, v, memoria=False):
        """memoria: para el archivo de memoria, donde lo que se guardó como mapa tiene que
        volver como mapa. Ahí un mapa del programa que tiene justo la forma de un mensaje
        ({tipo, campos}) se guarda envuelto: {"mapa": {...}}."""
        if isinstance(v, Registro):
            return {"tipo": v.tipo,
                    "campos": {k: self._a_json(x, memoria) for k, x in v.campos.items()}}
        if isinstance(v, Agente):
            return {"agente": v.nombre}
        if isinstance(v, list):
            return [self._a_json(x, memoria) for x in v]
        if isinstance(v, dict):
            mapa = {k: self._a_json(x, memoria) for k, x in v.items()}
            return {"mapa": mapa} if memoria and set(v) in ({"tipo", "campos"}, {"mapa"}) \
                else mapa
        if isinstance(v, (Funcion, Nativa, ModuloPython)):
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

    def _de_json(self, v, memoria=False):
        if isinstance(v, list):
            return [self._de_json(x, memoria) for x in v]
        if memoria and isinstance(v, dict):
            # En la memoria nunca hay agentes, y un mapa envuelto vuelve como mapa.
            if set(v) == {"mapa"} and isinstance(v["mapa"], dict):
                return {k: self._de_json(x, True) for k, x in v["mapa"].items()}
            if set(v) == {"tipo", "campos"} and isinstance(v["tipo"], str) \
                    and v["tipo"] in self.mensajes and isinstance(v["campos"], dict):
                return self.construir(
                    v["tipo"], {k: self._de_json(x, True) for k, x in v["campos"].items()})
            return {k: self._de_json(x, True) for k, x in v.items()}
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
        reglas = self.reglas.get(nombre) or {}
        for campo, tipo, opcional in self.mensajes[nombre]:
            regla = reglas.get(campo)
            if regla and "defecto" in regla and dados.get(campo) is None:
                campos[campo] = regla["defecto"]  # no vino (o vino nada): el de siempre
                continue
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
            rota = rompe_regla(f"{nombre}.{campo}", v, regla)
            if rota:
                raise ErrorMate(rota)
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
                self.reglas[s[2]] = s[5]
                if s[4]:
                    self.responde[s[2]] = s[4]
        for s in programa:
            try:
                if s[0] == "funcion":
                    self.glob.definir(s[2], Funcion(s[2], s[3], s[4], self.glob, s[5]),
                                      origen="funcion", linea=s[1])
                elif s[0] == "usar_python":
                    if self.glob.origen.get(s[2]) == "python" \
                            and self.glob.vars[s[2]][0].archivo == s[3]:
                        del self.glob.vars[s[2]]  # en la consola: se trae de nuevo, al día
                    self.glob.definir(s[2], cargar_python(s[2], s[3]), origen="python",
                                      linea=s[1])
                elif s[0] == "agente":
                    ag = Agente(s[2])
                    ag.decl = s
                    ag.lecciones = list(self.memoria.get(s[2], {}).get("lecciones", []))
                    ag.propuestas = list(self.memoria.get(s[2], {}).get("propuestas", []))
                    ag.gasto = {dia: dict(cuenta) for dia, cuenta in
                                self.memoria.get(s[2], {}).get("gasto", {}).items()}
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
            env.definir(f[2], Funcion(f[2], f[3], f[4], env, f[5]), origen="funcion")
        # Mientras nace no se le entregan mensajes: todavía no tiene todo su estado.
        self.naciendo += 1
        ag.ocupado = True  # si alguien le habla mientras nace, es un ciclo
        try:
            for declarado in s[3]:
                ln, nombre, e = declarado
                try:
                    valor = self.estado_inicial(s[2], nombre, e, env, dados, linea)
                    if isinstance(declarado, EstadoRecordado):
                        valor = self.recordado(ag, nombre, valor)
                    env.definir(nombre, valor, mutable=True)
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
        ag.recuerda = apodo is not None  # sin nombre no se sabría cuál es cuál
        if ag.recuerda:
            ag.lecciones = list(self.memoria.get(ag.nombre, {}).get("lecciones", []))
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
        self.ia_simulada = self.ia_simulada or pruebas  # 'probar' nunca sale a la red
        if pruebas and self.archivos_de_prueba is None:
            self.archivos_de_prueba = {}  # ...ni agrega renglones a los archivos de verdad
        if pruebas:  # ...ni lee ni escribe memoria o bitácora: cada prueba arranca limpia
            self.recordando, self.memoria, self.bitacora = False, {}, None
        self.cargar(programa)
        for s in programa:
            if s[0] == "agente":
                # El estado inicial se calcula donde está declarado el agente,
                # salvo que alguien le haya hablado antes.
                if self.agentes[s[2]].env is None:
                    self.instanciar(self.agentes[s[2]])
            elif s[0] not in ("mensaje", "funcion", "prueba", "usar_python"):
                self.ejecutar(s, self.glob)
        self.vaciar_cola()
        if not pruebas:
            return []
        self.errores_principal = list(self.errores_agentes_det)
        foto = self.foto()
        agregado = dict(self.archivos_de_prueba)  # lo que 'agregó' el programa, sin el disco
        resultados = []
        self.en_prueba = True
        try:
            for s in programa:
                if s[0] != "prueba":
                    continue
                self.volver_a(foto)
                for agente in list(self.agentes.values()) + self.vivos:
                    agente.lecciones = []  # las de la prueba se fijan con aprender()
                    agente.gasto = {}  # y la cuenta de consultas arranca de cero
                self.ia_historial = []
                self.errores_agentes, self.errores_agentes_det = [], []
                self.pasos = 0
                self.entregados = 0
                # El historial de cada prueba arranca vacío, y cuenta desde 1.
                self.historial = []
                self.ia_fijada, self.ia_en_orden, self.ia_usadas = None, False, 0
                self.tecleado, self.tecleados = None, 0
                self.archivos_de_prueba = dict(agregado)
                self.desde = (self.cuenta["enviar"] + self.cuenta["preguntar"],
                              self.conversaciones)
                fallas, mostrado, salida = [], [], self.salida
                if self.separar_salida:
                    self.salida = mostrado.append
                if self.traza and self.anotar:
                    # En el archivo de la conversación, cada prueba va con su título:
                    # adentro los mensajes se numeran desde 1.
                    self.anotar("")
                    self.anotar(f'Prueba "{s[2]}" (los números arrancan de nuevo, igual '
                                "que en mensajes_enviados()):")
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
            rem, dest, msg, sobre = self.cola.popleft()
            try:
                self.entregar(rem, dest, msg, pregunta=False, sobre=sobre)
            except ErrorMate as e:
                if e.clase == "limite":  # el freno corta todo el programa, no un solo mensaje
                    raise
                if rem is not None and msg.tipo != AL_FALLAR and AL_FALLAR in rem.manejadores:
                    # El que lo envió pidió enterarse: el aviso le llega como un mensaje
                    # más, y la falla queda en sus manos (no se anota como error).
                    self.cola.append((dest, rem, Registro(AL_FALLAR, {
                        "motivo": e.mensaje, "mensaje": msg, "destino": dest}),
                        (sobre[0], None)))
                    continue
                que = "en 'al fallar'" if msg.tipo == AL_FALLAR else f"al recibir {msg.tipo}"
                linea = e.linea or getattr(e, "renglon", None)
                texto = TextoDeError(self.con_camino(f"{dest.nombre} {que}: {e.mensaje}", e))
                texto.familia = e.familia
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

    def en_conversacion(self):
        """El número de conversación de lo que se manda ahora: el del mensaje que se está
        atendiendo o, si lo manda el programa, uno nuevo."""
        if self.conversacion is None:
            self.conversaciones += 1
            return self.conversaciones
        return self.conversacion

    def entregar(self, rem, dest, msg, pregunta, linea=None, sobre=None):
        """sobre: (número de conversación, número del mensaje al que responde o None). Lo
        trae lo que viene de la cola; una pregunta lo arma acá."""
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
        conversacion, respuesta_a = sobre or (self.en_conversacion(), None)
        # En una prueba la traza numera desde 1, igual que mensajes_enviados().
        numero0, conversacion0 = self.desde if self.en_prueba else (0, 0)
        visto = numero - numero0 if numero is not None else None
        if self.en_prueba and not aviso:
            self.historial.append(
                (numero, de, dest.nombre, msg, pregunta, conversacion, respuesta_a))
        if self.traza and aviso:
            self.trazar(f"{dest.nombre} se entera de que {rem.nombre} no pudo atender "
                        f"{msg.campos['mensaje'].tipo}: {msg.campos['motivo']}", None, hondo)
        elif self.traza:
            flecha = "pregunta a" if pregunta else "→"
            # El sobre se anota en los renglones sin sangría: lo de más adentro es de la
            # misma conversación que el renglón que lo contiene.
            anotado = ""
            if not hondo:
                anotado = f"   (conversación {conversacion - conversacion0}" + (
                    f", en respuesta al {respuesta_a - numero0})" if respuesta_a else ")")
            self.trazar(f"{de} {flecha} {dest.nombre}: {formato(msg)}{anotado}",
                        visto, hondo)
        afuera, self.conversacion = self.conversacion, conversacion
        try:
            respondio, valor = self.atender(rem, dest, msg, pregunta, linea)
        except ErrorMate as e:
            self.cuenta["fallaron"] += 1
            self.anotar_falla(dest, e, msg)
            if self.traza and getattr(e, "sin_respuesta", None) is dest:
                self.trazar(f"{dest.nombre} sin respuesta: terminó de atender {msg.tipo} sin "
                            "llegar a un 'responder'", visto, hondo)
            elif self.traza:
                donde = " en su 'al fallar'" if aviso else ""
                self.trazar(f"{dest.nombre} falló{donde}: {e.mensaje}", visto, hondo)
            raise
        finally:
            self.conversacion = afuera
        if pregunta:
            if self.traza:
                self.trazar(f"{dest.nombre} responde a {de}: {formato(valor, False)}",
                            visto, hondo)
            return valor
        if respondio and rem is not None:
            self.cola.append((dest, rem, valor, (conversacion, numero)))
        elif respondio and self.traza:
            # Lo mandó el programa con 'enviar': no hay quién reciba la respuesta.
            self.trazar(f"la respuesta de {dest.nombre} se descartó (para recibirla, usá "
                        f"'preguntar' en vez de 'enviar'): {formato(valor, False)}",
                        visto, hondo)
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
        self.contexto = (dest, rem, msg.tipo, env.serie, msg)
        respondio, valor = False, None
        # Si falla, el agente vuelve a como estaba antes de recibir este mensaje.
        estado_previo = {k: list(v) for k, v in dest.env.vars.items()}
        lecciones_previas = dest.lecciones
        en_cola, llamadas, nacidos = len(self.cola), self.llamadas, len(self.vivos)
        self.llamadas = []
        self.atendiendo.append((dest, linea))
        try:
            try:
                senal = self.armar_bloque(cuerpo, False)(env)
                if type(senal) is not tuple:  # (un 'devolver' termina de atender y listo)
                    self.fuera_de_lugar(senal)
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
            dest.lecciones = lecciones_previas
            # Las copias que creó atendiendo este mensaje tampoco quedan: nadie las tiene.
            self.vivos[nacidos:] = [a for a in self.vivos[nacidos:] if a.creador is not dest]
            nuevos = [self.cola.pop() for _ in range(len(self.cola) - en_cola)]
            self.cola.extend(m for m in reversed(nuevos) if m[0] is not dest)
            if e.clase == "asegurar":  # para quien le habló es una falla como cualquiera
                e.clase = "falla"
            raise
        except KeyboardInterrupt:
            # Cortado con Ctrl+C a mitad de un mensaje: lo que cambió atendiéndolo no queda
            # (si no, la memoria guardaría un estado a medio cambiar).
            dest.env.vars = estado_previo
            dest.lecciones = lecciones_previas
            raise
        finally:
            self.contexto, dest.ocupado, self.llamadas = previo, False, llamadas
            self.atendiendo.pop()
        return respondio, valor

    def destino(self, dest):
        """Controla que eso sea un agente: a quién se le pregunta o se le simula algo."""
        if not isinstance(dest, Agente):
            pista = ""
            if isinstance(dest, list):
                pista = (". Se le pregunta a un agente por vez: recorré la lista con "
                         "'para agente en lista { ... }'")
            raise ErrorMate(f"el destino tiene que ser un agente, no {tipo_claro(dest)}"
                            + pista)
        return dest

    def destinos(self, dest):
        """A quiénes va un 'enviar': un agente, o una lista de agentes."""
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

    def un_mensaje(self, msg):
        if not isinstance(msg, Registro):
            raise ErrorMate(f"solo se envían mensajes declarados, no {tipo_claro(msg)}")
        return msg

    # ── el programa, armado para correr (0.5) ──
    # Antes, cada vez que pasaba por un renglón, Mate volvía a preguntarse qué clase de
    # sentencia era (una cadena larga de 'si es esto, si es aquello'). Ahora cada sentencia
    # y cada valor se "arman" una sola vez: se convierten en una función de Python que ya
    # sabe qué tiene que hacer, y después solo se la llama. Hace lo mismo que antes, renglón
    # por renglón (mismos errores, mismo freno, misma traza), pero varias veces más rápido.
    #
    # Una sentencia armada recibe el entorno y devuelve nada... salvo que corte el camino:
    # (valor,) si fue un 'devolver', _ROMPER o _CONTINUAR. Así un 'devolver' no cuesta una
    # excepción de Python. Donde ya no hay quién reciba esa señal, se convierte en la
    # excepción de siempre (_Retorno, _Romper, _Continuar) y sigue el camino viejo.

    @staticmethod
    def fuera_de_lugar(senal):
        """Una señal que llegó hasta donde nadie la espera sigue como excepción."""
        if senal is None:
            return
        if senal is _ROMPER:
            raise _Romper()
        if senal is _CONTINUAR:
            raise _Continuar()
        raise _Retorno(senal[0])

    def bloque(self, cuerpo, env, nuevo=True):
        """Corre esas sentencias. (Lo que ya está armado no pasa por acá: se llama solo.)"""
        self.fuera_de_lugar(self.armar_bloque(cuerpo, nuevo)(env))

    def armar_bloque(self, cuerpo, nuevo=True):
        """El bloque listo para correr; se arma la primera vez y queda guardado."""
        clave = (id(cuerpo), nuevo)
        listo = self._armados.get(clave)
        if listo is None:  # (se guarda también el cuerpo: así su id no se repite)
            listo = self._armados[clave] = (self._bloque(cuerpo, nuevo), cuerpo)
        return listo[0]

    def ejecutar(self, s, env, vale_suelto=False):
        clave = (id(s), vale_suelto)
        listo = self._armados.get(clave)
        if listo is None:
            listo = self._armados[clave] = (self._paso(s, vale_suelto), s)
        self.fuera_de_lugar(listo[0](env))

    def freno(self, linea):
        """El error del freno para los programas que nunca terminan."""
        tope = f"{self.max_pasos:,}".replace(",", ".")
        tope += " de pasos" if self.max_pasos % 1_000_000 == 0 else " pasos"
        quien = (f"{self.contexto[0].nombre} atendiendo {self.contexto[2]}: "
                 if self.contexto else "")
        return ErrorMate(
            f"{quien}el programa lleva más de {tope}: ¿quedó en un bucle que nunca "
            "termina? Si es un 'mientras', revisá que su condición cambie adentro. Si "
            "el programa es largo de verdad, corrélo con --sin-limite",
            linea, clase="limite")

    def con_renglon(self, e, linea):
        """Lo que falló dentro de una sentencia, dicho como error de Mate y con su renglón."""
        if isinstance(e, ErrorMate):
            e.linea = e.linea or linea
            return e
        if isinstance(e, RecursionError):
            return self.demasiada_recursion(self.recursiva(), linea)
        return ErrorMate(SIN_MEMORIA, linea, clase="limite")

    def _bloque(self, cuerpo, nuevo=True):
        pasos = [self._paso(s) for s in cuerpo]
        # Un bloque solo necesita su propio entorno si declara algo ('sea', 'var' o una
        # función): si no, las variables que usa son las de afuera y se ahorra crearlo.
        if nuevo and any(s[0] in ("sea", "funcion") for s in cuerpo):
            def bloque(env):
                env = Entorno(env)
                for paso in pasos:
                    senal = paso(env)
                    if senal is not None:
                        return senal
            return bloque
        if not pasos:
            return lambda env: None
        if len(pasos) == 1:
            return pasos[0]

        def bloque(env):
            for paso in pasos:
                senal = paso(env)
                if senal is not None:
                    return senal
        return bloque

    def _paso(self, s, vale_suelto=False):
        """Arma una sentencia. Todas empiezan igual: anotan por qué renglón van, cuentan
        un paso (el freno) y, si algo falla adentro, le ponen su renglón al error."""
        if s[0] == "expr":
            return self._p_expr(s, vale_suelto)
        armar = getattr(self, "_p_" + s[0], None)
        if armar is None or s[0] in ("mensaje", "agente", "prueba", "usar"):
            clase = s[0]

            def no_va(env):
                raise ErrorMate(f"'{clase}' no puede ir acá")
            return self._contado(s[1], no_va)
        return armar(s)

    def _contado(self, linea, hacer):
        """El comienzo de toda sentencia, para las que no hace falta que vuelen."""
        it = self

        def paso(env):
            it.linea_actual = linea
            it.pasos = pasos = it.pasos + 1
            tope = it.max_pasos
            if tope is not None and pasos > tope:
                raise it.freno(linea)
            try:
                return hacer(env)
            except _SE_EXPLICAN as e:
                raise it.con_renglon(e, linea)
        return paso

    def _p_expr(self, s, vale_suelto):
        """Un renglón que es solo un valor: vale si hace algo (llamar a una función
        propia, mostrar, preguntar, crear). Si solo calcula y no lo usa, es un error."""
        it, linea, e = self, s[1], s[2]
        if vale_suelto or e[0] in ("preguntar", "crear"):
            de_valor = self.armar(e)

            def hacer(env):
                de_valor(env)
            return self._contado(linea, hacer)
        if e[0] != "llamar":
            de_valor = self.armar(e)

            def hacer(env):
                valor = de_valor(env)
                if isinstance(valor, (Funcion, Nativa)):
                    raise ErrorMate(f"a '{valor.nombre}' le faltan los paréntesis: "
                                    f"{valor.nombre}(...)", e[1], clase="escritura")
                raise renglon_sin_uso(e)
            return self._contado(linea, hacer)
        de_quien, de_args, renglon = self.armar(e[2]), [self.armar(a) for a in e[3]], e[1]
        llamar = self.llamar

        def paso(env):
            it.linea_actual = linea
            it.pasos = pasos = it.pasos + 1
            tope = it.max_pasos
            if tope is not None and pasos > tope:
                raise it.freno(linea)
            try:
                f = de_quien(env)
                nativa = isinstance(f, Nativa) and not isinstance(f, DePython)
                # (una consulta a la IA suelta no se llega a hacer: sería pagarla para
                # tirarla)
                if not (nativa and f.nombre == "consultar_ia"):
                    try:
                        llamar(f, [a(env) for a in de_args], renglon)
                    except ErrorMate as error:
                        error.linea = error.linea or renglon
                        raise
                if nativa and f.nombre not in HACEN_ALGO:
                    if f.nombre in ("agregar", "quitar"):
                        raise ErrorMate(
                            f"{f.nombre}() no cambia la lista: devuelve una nueva. Guardá "
                            f"el resultado: lista = {f.nombre}(lista, ...)", renglon,
                            clase="escritura")
                    raise ErrorMate(
                        f"{f.nombre}() devuelve un valor y este renglón no lo usa: "
                        f"guardalo (sea x = {f.nombre}(...)) o mostralo con mostrar(...)",
                        renglon, clase="escritura")
            except _SE_EXPLICAN as e:
                raise it.con_renglon(e, linea)
        return paso

    def _p_sea(self, s):
        it, linea, nombre, mutable = self, s[1], s[2], s[4]
        de_valor = self.armar(s[3])

        def paso(env):
            it.linea_actual = linea
            it.pasos = pasos = it.pasos + 1
            tope = it.max_pasos
            if tope is not None and pasos > tope:
                raise it.freno(linea)
            try:
                valor = de_valor(env)
                if nombre not in env.vars:  # (si está en este mismo bloque, lo dice definir)
                    env.no_tapar(nombre)
                env.definir(nombre, valor, mutable, None, linea)
            except _SE_EXPLICAN as e:
                raise it.con_renglon(e, linea)
        return paso

    def _p_asignar(self, s):
        it, linea, destino = self, s[1], s[2]
        de_valor = self.armar(s[3])
        if destino[0] != "nombre":  # una parte de una variable: lista[0] = ..., m.campo = ...
            asignar = self.asignar

            def hacer(env):
                asignar(destino, de_valor(env), env)
            return self._contado(linea, hacer)
        nombre = destino[2]

        def paso(env):
            it.linea_actual = linea
            it.pasos = pasos = it.pasos + 1
            tope = it.max_pasos
            if tope is not None and pasos > tope:
                raise it.freno(linea)
            try:
                valor = de_valor(env)
                if it.contexto is not None:
                    it.cuidar_lo_de_afuera(nombre, env)
                env.asignar(nombre, valor)
            except _SE_EXPLICAN as e:
                raise it.con_renglon(e, linea)
        return paso

    def _p_si(self, s):
        it, linea = self, s[1]
        ramas = [(self.armar(cond), self._bloque(cuerpo)) for cond, cuerpo in s[2]]
        otro = self._bloque(s[3]) if s[3] is not None else None
        if len(ramas) == 1:
            de_cond, cuerpo = ramas[0]

            def paso(env):
                it.linea_actual = linea
                it.pasos = pasos = it.pasos + 1
                tope = it.max_pasos
                if tope is not None and pasos > tope:
                    raise it.freno(linea)
                try:
                    v = de_cond(env)
                    if v is True:
                        return cuerpo(env)
                    if v is not False:
                        raise condicion_rara(v)
                    if otro is not None:
                        return otro(env)
                except _SE_EXPLICAN as e:
                    raise it.con_renglon(e, linea)
            return paso

        def hacer(env):
            for de_cond, cuerpo in ramas:
                v = de_cond(env)
                if v is True:
                    return cuerpo(env)
                if v is not False:
                    raise condicion_rara(v)
            if otro is not None:
                return otro(env)
        return self._contado(linea, hacer)

    def _p_mientras(self, s):
        it, linea = self, s[1]
        de_cond, cuerpo = self.armar(s[2]), self._bloque(s[3])

        def hacer(env):
            while True:
                v = de_cond(env)
                if v is not True:
                    if v is False:
                        return None
                    raise condicion_rara(v)
                # una vuelta cuenta aunque el cuerpo esté vacío
                it.pasos = pasos = it.pasos + 1
                tope = it.max_pasos
                if tope is not None and pasos > tope:
                    raise it.freno(linea)
                try:
                    senal = cuerpo(env)
                except _Continuar:
                    continue
                except _Romper:
                    return None
                if senal is not None:
                    if senal is _ROMPER:
                        return None
                    if senal is not _CONTINUAR:
                        return senal
        return self._contado(linea, hacer)

    def _p_para(self, s):
        # 'para2' es "para posicion, item en lista" (o "para clave, valor en mapa")
        it, linea, de_a_dos = self, s[1], s[0] == "para2"
        nombres = (s[2], s[3]) if de_a_dos else (s[2],)
        primero, segundo, repetida = nombres[0], nombres[-1], len(set(nombres)) != len(nombres)
        de_col, cuerpo = self.armar(s[-2]), self._bloque(s[-1], False)

        def hacer(env):
            col = de_col(env)
            if not isinstance(col, (list, dict, str)):
                raise ErrorMate(f"no se puede recorrer {tipo_claro(col)}: 'para' recorre "
                                "listas, mapas y textos")
            if de_a_dos:
                vueltas = list(col.items() if isinstance(col, dict) else enumerate(col))
            else:
                vueltas = list(col)
            # La variable de la vuelta se anota sin más controles, salvo que se llame
            # como una función incluida (o las dos igual): eso lo explica definir.
            de_afuera = env.raiz.origen
            directo = not repetida and not any(
                de_afuera.get(n) == "nativa" and n not in SE_PUEDEN_TAPAR for n in nombres)
            for valores in vueltas:
                it.pasos = pasos = it.pasos + 1
                tope = it.max_pasos
                if tope is not None and pasos > tope:
                    raise it.freno(linea)
                paso = Entorno(env)
                if not directo:
                    for nombre, x in zip(nombres, valores if de_a_dos else (valores,)):
                        paso.definir(nombre, x, False, "para")
                elif de_a_dos:
                    paso.vars = {primero: [valores[0], False], segundo: [valores[1], False]}
                    paso.origen = {primero: "para", segundo: "para"}
                else:
                    paso.vars[primero] = [valores, False]
                    paso.origen[primero] = "para"
                try:
                    senal = cuerpo(paso)
                except _Continuar:
                    continue
                except _Romper:
                    return None
                if senal is not None:
                    if senal is _ROMPER:
                        return None
                    if senal is not _CONTINUAR:
                        return senal
        return self._contado(linea, hacer)

    _p_para2 = _p_para

    def _p_romper(self, s):
        return self._contado(s[1], lambda env: _ROMPER)

    def _p_continuar(self, s):
        return self._contado(s[1], lambda env: _CONTINUAR)

    def _p_funcion(self, s):
        nombre, params, cuerpo, defectos = s[2], s[3], s[4], s[5]

        def hacer(env):
            env.definir(nombre, Funcion(nombre, params, cuerpo, env, defectos),
                        origen="funcion")
        return self._contado(s[1], hacer)

    def _p_devolver(self, s):
        it, linea = self, s[1]
        if s[2] is None:
            return self._contado(linea, lambda env: _SIN_VALOR)
        de_valor = self.armar(s[2])

        def paso(env):
            it.linea_actual = linea
            it.pasos = pasos = it.pasos + 1
            tope = it.max_pasos
            if tope is not None and pasos > tope:
                raise it.freno(linea)
            try:
                return (de_valor(env),)
            except _SE_EXPLICAN as e:
                raise it.con_renglon(e, linea)
        return paso

    def _p_enviar(self, s):
        it, linea = self, s[1]
        de_msg, de_dest = self.armar(s[2]), self.armar(s[3])

        def hacer(env):
            msg = it.un_mensaje(de_msg(env))
            destinos = it.destinos(de_dest(env))
            for dest in destinos:  # primero se revisan todos: sale para todos o para nadie
                if msg.tipo not in dest.manejadores:
                    raise ErrorMate(f"{dest.nombre} no sabe recibir '{msg.tipo}'", linea,
                                    familia="agente")
            sobre = (it.en_conversacion(), None)  # (a varios: una sola conversación)
            rem = it.contexto[0] if it.contexto else None
            for dest in destinos:
                it.cola.append((rem, dest, msg, sobre))
        return self._contado(linea, hacer)

    def _p_responder(self, s):
        it, linea = self, s[1]
        de_valor = self.armar(s[2])

        def hacer(env):
            if not it.contexto:
                raise ErrorMate(RESPONDER_SUELTO)
            valor = de_valor(env)
            if lleva_funcion(valor):
                raise ErrorMate("no se puede responder con una función: "
                                "las respuestas llevan datos", linea)
            raise _Respuesta(valor, linea)
        return self._contado(linea, hacer)

    def _p_fallar(self, s):
        linea, de_motivo = s[1], self.armar(s[2])

        def hacer(env):
            motivo = de_motivo(env)
            raise ErrorMate(formato(motivo), linea, familia="fallar",
                            dato=None if lleva_funcion(motivo) else motivo)
        return self._contado(linea, hacer)

    def _p_intentar(self, s):
        it, var = self, s[3]
        cuerpo, manejo = self._bloque(s[2]), self._bloque(s[4], False)

        def hacer(env):
            try:
                return cuerpo(env)
            except ErrorMate as e:
                # El freno no se ataja nunca, ni un renglón mal escrito. Un 'asegurar'
                # tampoco dentro de una prueba (si no, pasaría en verde); al correr el
                # programa es una falla más.
                if e.clase in ("limite", "escritura") or (
                        e.clase == "asegurar" and it.en_prueba):
                    raise
                if it.contexto is not None:  # un agente atajó una falla: va a la bitácora
                    it.anotar_falla(it.contexto[0], e, it.contexto[4], atajada=True)
                adentro = Entorno(env)
                if var:
                    adentro.definir(var, ErrorAtajado(e), origen="falla")
                return manejo(adentro)
        return self._contado(s[1], hacer)

    def _p_asegurar(self, s):
        it, linea, cond = self, s[1], s[2]
        de_texto = self.armar(s[3]) if s[3] else None
        comparada = cond[0] == "bin" and cond[2] in COMPARADORES
        if comparada:
            # Se evalúa cada lado una sola vez, para poder mostrar qué dio.
            de_izq, de_der = self.armar(cond[3]), self.armar(cond[4])
            op, renglon = cond[2], cond[1]
        else:
            de_cond = self.armar(cond)

        def hacer(env):
            valores = ""
            if it.contexto is None and it.en_prueba:
                it.vaciar_cola()  # lo enviado en la prueba llega antes de asegurar
            if comparada:
                izq, der = de_izq(env), de_der(env)
                try:
                    cumple = it.binaria(op, izq, der)
                except ErrorMate as e:
                    e.linea = e.linea or renglon
                    raise
                if not cumple:
                    valores = it.valores_de(op, izq, der)
            else:
                cumple = de_cond(env)
                if type(cumple) is not bool:
                    raise condicion_rara(cumple)
            if not cumple:
                if de_texto:
                    detalle = formato(de_texto(env)) + (f" ({valores})" if valores else "")
                else:
                    detalle = "no se cumplió lo asegurado" + (f": {valores}" if valores else "")
                raise ErrorMate(detalle, linea, clase="asegurar")
        return self._contado(linea, hacer)

    def _p_simular(self, s):
        it, linea, tipo, var, cuerpo = self, s[1], s[3], s[4], s[5]
        de_dest = self.armar(s[2])

        def hacer(env):
            if not it.en_prueba or it.contexto is not None:
                raise ErrorMate("'simular' solo va dentro de una prueba")
            dest = it.destino(de_dest(env))
            if tipo not in dest.manejadores:
                raise ErrorMate(f"{dest.nombre} no sabe recibir '{tipo}': solo se simula un "
                                "mensaje que el agente ya recibe", familia="agente")
            dest.manejadores = {**dest.manejadores, tipo: (linea, var, cuerpo, env)}
        return self._contado(linea, hacer)

    def _p_asegurar_falla(self, s):
        it, linea = self, s[1]
        # Acá una cuenta o una función suelta vale: se prueba que falle.
        pasos = [self._paso(x, vale_suelto=True) for x in s[2]]
        de_texto = self.armar(s[3]) if s[3] else None

        def hacer(env):
            if it.contexto is None and it.en_prueba:
                it.vaciar_cola()
            try:
                adentro = Entorno(env)
                for paso in pasos:
                    senal = paso(adentro)
                    if senal is not None:
                        return senal
            except ErrorMate as e:
                # Igual que 'intentar': ni el freno, ni un renglón mal escrito, ni un
                # 'asegurar' de la prueba cuentan.
                if e.clase in ("limite", "escritura") or (
                        e.clase == "asegurar" and it.en_prueba):
                    raise
                if e.familia == "nombre":  # un nombre mal tipeado no es la falla esperada
                    raise ErrorMate(
                        f"lo de adentro de 'asegurar falla' no llegó a probarse: {e.mensaje}",
                        e.linea or linea, clase="asegurar")
                return None
            raise ErrorMate(formato(de_texto(env)) if de_texto else
                            "se esperaba que esto fallara, y no falló", linea, clase="asegurar")
        return self._contado(linea, hacer)

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
        agente, _, _, desde, _ = self.contexto
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
        """El valor de esa expresión. (Lo que ya está armado no pasa por acá.)"""
        listo = self._armados.get(id(n))
        if listo is None:
            listo = self._armados[id(n)] = (self.armar(n), n)
        return listo[0](env)

    def armar(self, n):
        """Arma una expresión: devuelve una función que recibe el entorno y da el valor.
        Si falla, el error sale con el renglón de la expresión de más adentro."""
        armar = getattr(self, "_x_" + n[0], None)
        if armar is None:
            clase, linea = n[0], n[1]

            def desconocida(env):
                raise ErrorMate(f"expresión desconocida: {clase}", linea)
            return desconocida
        return armar(n)

    def _x_num(self, n):
        valor = n[2]
        return lambda env: valor

    _x_str = _x_bool = _x_num

    def _x_nada(self, n):
        return lambda env: None

    def _x_nombre(self, n):
        linea, nombre = n[1], n[2]

        def valor(env):
            e = env
            while e is not None:
                caja = e.vars.get(nombre)
                if caja is not None:
                    return caja[0]
                e = e.padre
            error = env.no_existe(nombre)
            error.linea = error.linea or linea
            raise error
        return valor

    def _x_interp(self, n):
        linea = n[1]
        partes = [(True, p) if isinstance(p, str) else (False, self.armar(p)) for p in n[2]]

        def valor(env):
            try:
                hechas, largo = [], 0
                for fija, p in partes:
                    if not fija:
                        p = p(env)
                        if type(p) is not str:
                            p = a_texto(p)
                    hechas.append(p)
                    largo += len(p)
                    if largo > MAX_LARGO:
                        raise muy_largo()
                return "".join(hechas)
            except ErrorMate as e:
                e.linea = e.linea or linea
                raise
        return valor

    def _x_lista(self, n):
        de_cada = [self.armar(x) for x in n[2]]
        return lambda env: [de(env) for de in de_cada]

    def _x_mapa(self, n):
        pares = [(k, self.armar(e)) for k, e in n[2]]
        return lambda env: {k: de(env) for k, de in pares}

    def _x_ctor(self, n):
        linea, tipo, construir = n[1], n[2], self.construir
        pares = [(k, self.armar(e)) for k, e in n[3]]

        def valor(env):
            try:
                return construir(tipo, {k: de(env) for k, de in pares})
            except ErrorMate as e:
                e.linea = e.linea or linea
                raise
        return valor

    def _x_remitente(self, n):
        it = self
        return lambda env: it.contexto[1] if it.contexto else None

    def _x_yo(self, n):
        it = self
        return lambda env: it.contexto[0] if it.contexto else None

    def _x_crear(self, n):
        it, linea = self, n[1]

        def valor(env):
            try:
                return it.crear(n, env)
            except ErrorMate as e:
                e.linea = e.linea or linea
                raise
        return valor

    def _x_y(self, n):
        linea, de_a, de_b, es_o = n[1], self.armar(n[2]), self.armar(n[3]), n[0] == "o"

        def valor(env):
            a = de_a(env)
            if a is es_o:  # 'y' con el primero falso, 'o' con el primero verdadero
                return a
            if a is True or a is False:
                b = de_b(env)
                if b is True or b is False:
                    return b
                a = b
            raise condicion_rara(a, linea)
        return valor

    _x_o = _x_y

    def _x_no(self, n):
        linea, de_a = n[1], self.armar(n[2])

        def valor(env):
            a = de_a(env)
            if a is True:
                return False
            if a is False:
                return True
            raise condicion_rara(a, linea)
        return valor

    def _x_neg(self, n):
        linea, de_a = n[1], self.armar(n[2])

        def valor(env):
            v = de_a(env)
            if not es_num(v):
                raise ErrorMate(f"no se puede negar {tipo_claro(v)}: el signo menos va "
                                "delante de un número", linea)
            return -v
        return valor

    def _x_bin(self, n):
        linea, op, binaria = n[1], n[2], self.binaria
        de_a, de_b = self.armar(n[3]), self.armar(n[4])

        def completa(a, b):
            """La cuenta con todos sus controles: para lo que no es el caso de siempre."""
            try:
                return binaria(op, a, b)
            except ErrorMate as e:
                e.linea = e.linea or linea
                raise

        # Lo de todos los días (números no gigantes, textos iguales o distintos) se
        # resuelve acá mismo; da exactamente lo que daría la cuenta completa.
        fijo = n[4][2] if n[4][0] == "num" and type(n[4][2]) is int else None
        if fijo is not None and not -_CHICO < fijo < _CHICO:
            fijo = None
        if op in _CUENTAS:
            cuenta = _CUENTAS[op]
            if fijo is not None:
                def valor(env):
                    a = de_a(env)
                    if type(a) is int and -_CHICO < a < _CHICO:
                        return cuenta(a, fijo)
                    return completa(a, fijo)
                return valor

            def valor(env):
                a = de_a(env)
                b = de_b(env)
                ta = type(a)
                if ta is int:
                    if type(b) is int and -_CHICO < a < _CHICO and -_CHICO < b < _CHICO:
                        return cuenta(a, b)
                elif ta is float and type(b) is float:
                    r = cuenta(a, b)
                    if _finito(r):
                        return r
                return completa(a, b)
            return valor
        if op in _COMPARACIONES:
            compara = _COMPARACIONES[op]
            if fijo is not None:
                def valor(env):
                    a = de_a(env)
                    ta = type(a)
                    if ta is int or ta is float:
                        return compara(a, fijo)
                    return completa(a, fijo)
                return valor

            def valor(env):
                a = de_a(env)
                b = de_b(env)
                ta, tb = type(a), type(b)
                if (ta is int or ta is float) and (tb is int or tb is float):
                    return compara(a, b)
                if ta is str and tb is str and (op == "==" or op == "!="):
                    return compara(a, b)
                return completa(a, b)
            return valor
        if op in ("/", "%"):
            resto = op == "%"

            def valor(env):
                a = de_a(env)
                b = de_b(env)
                if (type(a) is int and type(b) is int and b != 0
                        and -_CHICO < a < _CHICO and -_CHICO < b < _CHICO):
                    if resto:
                        return a % b
                    # la división exacta entre enteros no pierde cifras
                    return a // b if a % b == 0 else a / b
                return completa(a, b)
            return valor
        return lambda env: completa(de_a(env), de_b(env))

    def _x_llamar(self, n):
        linea, llamar = n[1], self.llamar
        de_quien, de_args = self.armar(n[2]), [self.armar(a) for a in n[3]]

        if len(de_args) == 1:  # (lo más común: se ahorra la vuelta que arma la lista)
            de_uno = de_args[0]

            def valor(env):
                f = de_quien(env)
                args = [de_uno(env)]
                try:
                    return llamar(f, args, linea)
                except ErrorMate as e:
                    e.linea = e.linea or linea
                    raise
            return valor

        def valor(env):
            f = de_quien(env)
            args = [de(env) for de in de_args]
            try:
                return llamar(f, args, linea)
            except ErrorMate as e:
                e.linea = e.linea or linea
                raise
        return valor

    def _x_indice(self, n):
        it, linea = self, n[1]
        de_base, de_i = self.armar(n[2]), self.armar(n[3])

        def valor(env):
            base, i = de_base(env), de_i(env)
            tipo = type(base)
            if tipo is list:
                if type(i) is int and 0 <= i < len(base):
                    return base[i]
            elif tipo is dict and type(i) is str and i in base:
                return base[i]
            try:
                if isinstance(base, (list, str)):
                    it.posicion(base, i)
                    return base[i]
                if isinstance(base, dict):
                    it.clave_de_mapa(i)
                    if i not in base:
                        raise ErrorMate(no_esta(
                            f"el mapa no tiene la clave {formato(i, False)}", i, base),
                            familia="clave")
                    return base[i]
                raise ErrorMate(f"{tipo_claro(base)} no tiene posiciones ni claves: los "
                                "corchetes van después de una lista, un texto o un mapa"
                                + (f". {CAUSA_DE_NADA}" if base is None else ""))
            except ErrorMate as e:
                e.linea = e.linea or linea
                raise
        return valor

    def _x_campo(self, n):
        linea, campo, de_base = n[1], n[3], self.armar(n[2])

        def valor(env):
            base = de_base(env)
            campos = base.campos if isinstance(base, Registro) else base
            if not isinstance(campos, dict):
                if isinstance(base, ModuloPython):  # ayudas.doble: una función de Python
                    try:
                        return base.funcion(campo)
                    except ErrorMate as e:
                        e.linea = e.linea or linea
                        raise
                raise ErrorMate(f"{tipo_claro(base)} no tiene campos"
                                + (f". {CAUSA_DE_NADA}" if base is None else ""), linea)
            if campo not in campos:
                raise ErrorMate(no_esta(
                    f"{nombre_tipo(base)} no tiene un campo '{campo}'", campo, campos),
                    linea, familia="clave")
            return campos[campo]
        return valor

    def _x_preguntar(self, n):
        it, linea = self, n[1]
        de_msg, de_dest = self.armar(n[2]), self.armar(n[3])

        def valor(env):
            try:
                msg = it.un_mensaje(de_msg(env))
                dest = it.destino(de_dest(env))
                if it.contexto is None and not it.naciendo:
                    it.vaciar_cola()  # lo que el programa ya envió llega antes
                return it.entregar(it.contexto[0] if it.contexto else None, dest, msg,
                                   True, linea)
            except ErrorMate as e:
                e.linea = e.linea or linea
                raise
        return valor

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
        if type(f) is Funcion:
            pass
        elif isinstance(f, Nativa):
            return f.fn(args)
        elif not isinstance(f, Funcion):
            raise ErrorMate(f"{tipo_claro(f)} no es una función: no se le pueden poner "
                            "paréntesis" + (
                                f". Se llama a una de sus funciones: {f.nombre}.nombre(...)"
                                if isinstance(f, ModuloPython) else ""))
        params, nombre, cuantos = f.params, f.nombre, len(args)
        minimo = len(params) - len(f.defectos)
        if not minimo <= cuantos <= len(params):
            raise ErrorMate(espera_otra_cantidad(nombre, minimo, len(params), cuantos))
        if self.abiertas >= MAX_LLAMADAS:
            self.ultima_funcion = nombre
            raise self.demasiada_recursion(nombre)
        env = Entorno(f.env, False, True)
        directa = f.directa
        if directa is None:
            # ¿Se pueden anotar los parámetros sin más controles? Sí, salvo que alguno
            # esté repetido o se llame como una función incluida: eso lo explica definir.
            de_afuera = env.raiz.origen
            directa = f.directa = len(set(params)) == len(params) and not any(
                de_afuera.get(p) == "nativa" and p not in SE_PUEDEN_TAPAR for p in params)
        if directa:
            if cuantos == 1:  # (lo más común, sin vueltas)
                env.vars[params[0]] = [args[0], False]
                env.origen[params[0]] = "parametro"
            elif cuantos:
                variables, origen = env.vars, env.origen
                for p, a in zip(params, args):
                    variables[p] = [a, False]
                    origen[p] = "parametro"
        else:
            for p, a in zip(params, args):
                env.definir(p, a, False, "parametro")
        self.llamadas.append(nombre)
        self.abiertas += 1
        self.ultima_funcion = nombre
        try:
            # Los que no vinieron toman su valor por defecto, que se calcula en cada
            # llamada y puede usar los parámetros de antes: f(a, b = a * 2).
            if cuantos != len(params):
                for p, e in f.defectos[cuantos - minimo:]:
                    env.definir(p, self.ev(e, env), False, "parametro")
            cuerpo = f.armado
            if cuerpo is None:  # se arma la primera vez que se la llama
                cuerpo = f.armado = self.armar_bloque(f.cuerpo, False)
            senal = cuerpo(env)
        except _Retorno as r:
            return r.valor
        except ErrorMate as e:
            anotar_paso(e, ("funcion", nombre, linea))
            raise
        finally:
            self.llamadas.pop()
            self.abiertas -= 1
        if senal is None:
            return None
        if type(senal) is tuple:  # un 'devolver'
            return senal[0]
        return self.fuera_de_lugar(senal)

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
- Los bloques van entre llaves {{ }}. Los textos, entre comillas dobles y en un renglón
  (los de varios renglones, entre tres comillas: ver VALORES).

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
- Un texto de varios renglones va entre tres comillas, con las mismas {{...}} y barras:
      sea carta = {tres}
          Hola {{nombre}}:
          tu pedido sale {{pesos(total)}}.
          {tres}
  No cuentan el renglón de las comillas ni la sangría que comparten todos los renglones.

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
- funcion con_iva(precio, tasa = 0.21) {{ ... }}    tasa tiene valor por defecto: con_iva(100)
  usa 0.21 y con_iva(100, 0.5) usa 0.5. Los parámetros con valor por defecto van al final.
- fallar "motivo"                                 corta con un error
- intentar {{ ... }} si falla e {{ ... }}             e es el texto del error (el 'e' es opcional)
  detalle_de(e).clase dice qué pasó sin depender de la redacción: "fallar", "asegurar",
  "contrato", "clave", "posicion", "division", "nombre", "numero", "json", "agente",
  "ciclo", "archivo", "ia", "tope", "python" u "otro". detalle_de(e).dato es el valor que
  se le dio a 'fallar'.

FUNCIONES INCLUIDAS (no hay otras)
{funciones}
- agregar, quitar, ordenar y porcion devuelven una copia NUEVA, no cambian la original:
  lista = agregar(lista, x)
- quitar(lista, x) saca por valor, no por posición: se van todos los que valen x.
- Una función incluida suelta en un renglón (salvo mostrar, leer, escribir_archivo,
  agregar_a_archivo y aprender) es un error: hay que usar lo que devuelve. Ese error no se
  ataja con 'intentar': para validar un dato se escribe
      intentar {{ sea n = numero(dato) ... }} si falla e {{ ... }}
- hoy() y ahora() dan textos: no se restan ni se comparan con < o > (sí con == y !=).
- leer_archivo, leer_tabla, escribir_archivo y agregar_a_archivo solo andan desde el programa
  principal (no desde un agente: se le pasan los datos en un mensaje), con archivos de la
  carpeta del programa, y no pisan archivos .mate ni .py.
- leer_tabla("precios.csv") lee una planilla guardada desde Excel como CSV (separada por
  punto y coma o por coma) y da una lista con un mapa por fila; las claves son los títulos
  de la primera fila, tal cual están escritos:
      para fila en leer_tabla("precios.csv") {{ mostrar(fila.producto, pesos(fila.precio)) }}
  Una celda escrita como número ya llega como número, también a la argentina (3.500 es 3500;
  3.500,50; $ 3.500). Lo demás llega como texto, y una celda vacía es "". Un título con
  espacios se lee con corchetes: fila["precio de lista"].
- agregar_a_archivo("pedidos.txt", renglon) suma ese texto como un renglón más, al final (si
  el archivo no existe, lo crea). Con 'probar' no toca el archivo de verdad: lo agregado se
  ve con leer_archivo() dentro de esa prueba y nada más.
- leer("Cliente:", "chau") espera que la persona escriba y apriete Enter; devuelve un texto.
  El 2.º valor es lo que da cuando no hay teclado (con 'probar' nunca lo espera). Una charla
  es un bucle que sale con una palabra (Ctrl+C también la termina bien):
      mientras verdadero {{
          sea dicho = leer("Cliente:", "chau")
          si minusculas(dicho) == "chau" {{ romper }}
          mostrar("Dijiste: {{dicho}}")
      }}
- consultar_ia(instrucciones, pregunta) le pregunta a una IA de verdad (Claude) y devuelve su
  respuesta como texto. Sirve adentro de un agente: el agente arma la pregunta, consulta y
  responde con su mensaje de siempre. Es paga y necesita la clave en la variable de entorno
  ANTHROPIC_API_KEY (nunca escrita en el programa). Si algo sale mal (sin clave, sin red,
  sin crédito) es un error que se ataja con 'intentar'; su clase es "ia".
  Con 'probar' y con la opción --ia-simulada no sale a la red: contesta lo que fijó la prueba
  con simular_ia("...") o, si no, el tercer valor:  consultar_ia(inst, pregunta, "Hola").

AGENTES Y MENSAJES
- mensaje Pedido {{ producto: texto, cantidad: numero, nota: texto? }}     (? = opcional)
  Tipos: numero texto logico lista mapa agente cualquiera, u otro mensaje. Una lista
  puede decir de qué es: items: lista de Pedido     vendedores: lista de agente
- Un campo puede decir qué valores acepta, después del tipo y con valores escritos a mano:
      cantidad: numero desde 1 hasta 100         (también solo 'desde 1' o solo 'hasta 100')
      prioridad: texto en ["baja", "media", "alta"]        una de esas opciones
      prioridad: texto en ["baja", "alta"] = "baja"        valor por defecto: puede faltar
  El orden es ese: desde, hasta (o en [...]) y al final = valor. Se controla al armar el
  mensaje y, si el valor está escrito a mano, antes de correr.
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
- estado recordado atendidos = 0     como 'estado', pero ese dato se guarda cuando el programa
  termina (en programa.memoria.json, al lado del programa) y vuelve en la próxima corrida.
  Solo datos: números, textos, listas, mapas y mensajes. Vale para los agentes declarados y
  para las copias con nombre (crear ... llamado "Centro"). Con 'probar' no se lee ni se
  guarda nada. 'correr programa.mate --olvidar' arranca de cero.
- Dentro de un agente, aprender("texto") le anota una lección (queda guardada junto con lo
  recordado; no se repite ni se pasa de {max_lecciones}) y lecciones() da la lista de las suyas.
  consultar_ia() dentro de ese agente las agrega solas al final de las instrucciones, bajo
  un título, para que la IA las tenga en cuenta. El dueño anota lecciones sin tocar el
  programa:  mate.py corregir programa.mate Agente "texto"
- Si el programa usa 'estado recordado' o lecciones, cada falla de un agente queda anotada
  sola en programa.bitacora.txt (se lee resumida con: mate.py bitacora programa.mate).
- FRENOS: reglas que el agente declara y que MATE comprueba sobre cada respuesta de
  consultar_ia() de ese agente, antes de devolverla (no se le pide a la IA que se controle):
      agente Mostrador {{
          estado lista = [3500, 1200]
          frenos {{
              precios: lista                    # los únicos importes en pesos que puede nombrar
              prohibido: ["descuento", "fiado"]  # palabras o temas que no pueden aparecer
              largo: 400                        # letras de la respuesta, como mucho
              reserva: "Eso te lo confirma una persona, ya te paso."
              consultas_por_dia: 100            # tope de gasto (opcional)
              tokens_por_dia: 200000            # tope de gasto (opcional)
          }}
          al recibir Consulta como c {{ responder consultar_ia("Atendés...", c.pregunta) }}
      }}
  Una regla por renglón; todas son opcionales, pero si hay precios, prohibido o largo tiene
  que haber reserva. Cada valor es una expresión que puede usar el estado y las funciones
  del agente, y se calcula en cada consulta. 'frenos' no es una palabra reservada.
  - precios: una lista de números (o una tabla o un mapa: valen todos sus números). Cuenta
    como importe un número con $ ($ 3.500, $3500, $ 3.500,00), con "pesos" (3500 pesos, 3 mil
    pesos) o suelto después de sale/cuesta/vale/precio si es de 100 o más. Cantidades,
    teléfonos, fechas, porcentajes e importes escritos con letras no se miran.
  - prohibido: sin distinguir mayúsculas ni tildes; "descuento" también frena "descuentos".
  - Si la respuesta rompe una regla, Mate consulta UNA vez más avisándole a la IA cuál; si
    la vuelve a romper, consultar_ia() devuelve el texto de reserva. Queda en --traza, en la
    bitácora y como lección PROPUESTA (no se usa hasta que el dueño la aprueba con
    mate.py propuestas programa.mate aprobar 1).
  - Al llegar a un tope, consultar_ia() no consulta: devuelve la reserva o, si no hay
    reserva, falla con un error que se ataja (clase "tope"). La cuenta es por día, se guarda
    en programa.memoria.json y se ve con mate.py bitacora programa.mate. Las consultas
    simuladas se cuentan aparte de las de verdad. El segundo intento también cuenta.
- usar "otro.mate" trae los mensajes, agentes, funciones y variables ('sea' y 'var') de
  otro archivo. Un nombre que ya vino de ahí no se puede declarar de nuevo.
- usar python "ayudas.py" trae las funciones escritas con 'def' en ese archivo de Python,
  que está en la carpeta del programa (nombre en minúsculas, sin espacios). Se llaman con el
  nombre del archivo adelante:  sea r = ayudas.raiz(144)
  Solo cruzan números, textos, verdadero/falso, nada, listas y mapas, y van y vuelven
  copiados. Un error dentro del Python es un error de Mate (clase "python") que se ataja
  con 'intentar'. Sirve para lo que Mate no trae; si hace falta, hay que entregar también
  el .py, y avisar que ese Python corre con todos los permisos de la computadora.

PRUEBAS
- prueba "nombre" {{ asegurar total == 10 }}        asegurar cond, "mensaje si falla"
- asegurar falla {{ dividir(1, 0) }}                 se cumple si lo de adentro falla
  (un nombre mal escrito ahí adentro no cuenta como la falla esperada)
- simular Vendedor al recibir Pedido como p {{ responder Cotizacion {{ total: 1 }} }}
  Solo dentro de una prueba: hasta que termina, ese agente contesta eso a ese mensaje.
- mensajes_enviados() solo dentro de una prueba: la lista de lo que se mandó en esa prueba,
  en orden. Cada elemento es un mapa: numero, de y a (nombres, como textos; el programa es
  "(programa)"), tipo, mensaje, pregunta (verdadero si fue con 'preguntar'), conversacion y
  respuesta_a (el numero del mensaje que contesta, o nada). Con un tipo, solo esos:
      asegurar largo(mensajes_enviados("Pedido")) == 1
      asegurar mensajes_enviados()[0].a == "Vendedor"
- simular_ia("Sale $ 100") solo dentro de una prueba: desde ahí, consultar_ia() contesta eso.
  Con una lista las da en orden, una por consulta: simular_ia(["Hola", "Chau"]). En las
  pruebas nunca se habla con la IA de verdad.
- simular_teclado(["hola", "chau"]) solo dentro de una prueba: lo que "teclea" la persona,
  un texto por cada leer(), en orden. Cuando se acaban, leer() da su 2.º valor.
- En una prueba ningún agente tiene lecciones ni memoria: se le fijan con
  aprender("texto", Mostrador), y lecciones(Mostrador) las devuelve. consultas_ia() da la
  lista de lo que se le consultó a la IA en esa prueba; cada elemento es un mapa con agente,
  instrucciones (con las lecciones al final), pregunta y respuesta:
      asegurar tiene(ultimo(consultas_ia()).instrucciones, "texto de la lección")
  Si el agente tiene frenos, cada elemento trae además freno (qué regla rompió esa
  respuesta, o "" si pasó) y devuelto (lo que consultar_ia() le devolvió al programa); el
  segundo intento es otro elemento, y en una prueba la cuenta del tope arranca de cero:
      simular_ia("Sale $ 9.999")
      asegurar (preguntar Consulta {{ pregunta: "¿yerba?" }} a Mostrador) == "Eso te lo ..."
      asegurar tiene(consultas_ia()[0].freno, "$ 9.999")
- Van en el nivel superior y corren con la orden 'probar'. Cada una empieza limpia.

ANTES DE CORRER
- Mate revisa todo el programa y no arranca si un nombre no existe (totl por total) o si una
  función recibe valores de más o de menos, aunque sea en una parte que no se ejecuta.
  Lo declarado afuera de todo puede estar más abajo en el archivo. No revisa adentro de
  intentar {{ }} ni de asegurar falla {{ }}. Los errores salen así: archivo:renglón: error: ...
- --traza numera los mensajes y muestra cuál falló o quedó sin respuesta. Al final del
  renglón dice de qué conversación es (una por cada cosa que manda el programa) y, si es una
  respuesta, a qué mensaje contesta: (conversación 2, en respuesta al 4).
  Con 'probar', la traza de cada prueba numera desde 1, igual que mensajes_enviados().

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
  python mate\mate.py corregir archivo.mate Agente "la lección"    (le anota una lección)
  python mate\mate.py lecciones archivo.mate     python mate\mate.py bitacora archivo.mate
  python mate\mate.py propuestas archivo.mate    (las lecciones propuestas, sin aprobar)
  python mate\mate.py propuestas archivo.mate aprobar 1         (o: descartar 1)
  python mate\mate.py proponer archivo.mate Agente "qué estuvo mal"   (Mate la redacta)
  python mate\mate.py informe      (los errores de uso que Mate fue anotando en esa
  computadora, sin datos de la persona; con --para-mejorar arma un texto para pedir mejoras)
  En PowerShell el comando se escribe una sola vez por renglón, y los comandos no van
  adentro del archivo .mate: si se pegan ahí, Mate lo avisa.
"""


def texto_de_guia():
    return GUIA.format(version=VERSION, funciones=lista_de_funciones(), tres=TRES_COMILLAS,
                       max_lecciones=MAX_LECCIONES)


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
                "el resultado y termina la función. Un parámetro puede tener un valor por "
                "defecto (tasa = 0.21), que se usa si no le dan otro; esos van al final",
                "funcion doble(n) {\n    devolver n * 2\n}\nmostrar(doble(4))\n"
                "funcion con_iva(precio, tasa = 0.21) {\n    devolver precio * (1 + tasa)\n}\n"
                "mostrar(con_iva(100), con_iva(100, 0.5))"),
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
                "opcional). Con 'responde' dice además qué se le contesta. Un campo puede "
                "decir qué valores acepta: 'desde 1 hasta 100', 'en [opciones]' y, al "
                "final, '= valor por defecto'",
                "mensaje Pedido {\n    producto: texto,\n"
                "    cantidad: numero desde 1 hasta 100,\n"
                '    prioridad: texto en ["baja", "media", "alta"] = "media",\n'
                "    nota: texto?\n}\n"
                'sea p = Pedido { producto: "yerba", cantidad: 2 }\n'
                "mostrar(p.producto, p.prioridad)"),
    "agente": ("alguien que recibe mensajes. Tiene su 'estado' privado, que solo él cambia, "
               "y un 'al recibir' por cada mensaje que entiende", _EJ_AGENTE),
    "recordado": ("dentro de un agente, después de 'estado': ese dato se guarda cuando el "
                  "programa termina y vuelve en la próxima corrida (queda en un archivo "
                  ".memoria.json al lado del programa). Con 'probar' no se guarda nada, y "
                  "con 'correr programa.mate --olvidar' se arranca de cero",
                  "mensaje Llego {}\nagente Mostrador {\n"
                  "    estado recordado atendidos = 0\n"
                  "    al recibir Llego {\n        atendidos += 1\n"
                  "        responder atendidos\n    }\n}\n"
                  'mostrar("Clientes hasta hoy:", preguntar Llego {} a Mostrador)'),
    "frenos": ("dentro de un agente: las reglas que Mate le revisa a cada respuesta de "
               "consultar_ia() antes de devolverla. precios (los importes que puede nombrar), "
               "prohibido (palabras que no pueden aparecer), largo (letras, como mucho), "
               "reserva (lo que contesta si la IA rompe una regla dos veces) y los topes "
               "consultas_por_dia y tokens_por_dia. Si una regla no se cumple, Mate consulta "
               "una vez más avisándole a la IA; si la rompe de nuevo, devuelve la reserva. "
               "Cada freno que salta queda en la bitácora y deja una lección propuesta "
               "(orden 'propuestas')",
               "mensaje Consulta { pregunta: texto }\nagente Mostrador {\n"
               "    estado lista = [3500, 1200]\n"
               "    frenos {\n        precios: lista\n"
               '        prohibido: ["descuento", "fiado"]\n        largo: 400\n'
               '        reserva: "Eso te lo confirma una persona, ya te paso."\n'
               "        consultas_por_dia: 100\n    }\n"
               "    al recibir Consulta como c {\n"
               '        responder consultar_ia("Atendés un almacén.", c.pregunta)\n    }\n}\n'
               'prueba "un precio inventado no llega al cliente" {\n'
               '    simular_ia("La yerba sale $ 9.999")\n'
               '    sea dicho = preguntar Consulta { pregunta: "¿Y la yerba?" } a Mostrador\n'
               '    asegurar dicho == "Eso te lo confirma una persona, ya te paso."\n'
               '    asegurar tiene(consultas_ia()[0].freno, "$ 9.999")\n}'),
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
             "archivo, que se busca al lado de este. (Para traer funciones escritas en "
             "Python: 'ayuda python')", 'usar "catalogo.mate"\nmostrar(iva)'),
    "python": ("después de 'usar': trae las funciones de un archivo de Python que está al "
               "lado del programa, para sumar lo que Mate no trae. Se llaman con el nombre "
               "del archivo adelante. Cruzan números, textos, verdadero/falso, nada, listas "
               "y mapas. Si el Python falla, es un error que se ataja con 'intentar'. OJO: "
               "ese Python corre con todos los permisos de la computadora (también con "
               "'probar'): usá solo archivos tuyos o de alguien de confianza",
               "# ayudas.py está al lado del programa y dice:\n"
               "#     def doble(numero):\n"
               "#         return numero * 2\n"
               'usar python "ayudas.py"\n'
               "mostrar(ayudas.doble(21))"),
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
# Las funciones incluidas que piden más explicación que su renglón de la tabla (0.5): lo
# que se agrega al título y un ejemplo más largo.
AYUDA_DE_FUNCION = {
    "leer": ("El 2.º valor es lo que da cuando no hay teclado (con 'probar' nunca lo "
             "espera). Con Ctrl+C mientras espera, el programa termina ahí sin error",
             "# Una charla: sigue hasta que escriben chau.\n"
             "mientras verdadero {\n"
             '    sea dicho = leer("Cliente:", "chau")\n'
             '    si minusculas(dicho) == "chau" {\n'
             "        romper\n"
             "    }\n"
             '    mostrar("Dijiste: {dicho}")\n'
             "}"),
    "simular_teclado": ("Cuando se acaban los textos, leer() da su 2.º valor",
                        "funcion saludar() {\n"
                        '    devolver "Hola, " + leer("¿Cómo te llamás?", "nadie")\n'
                        "}\n"
                        'prueba "saluda a quien escribe" {\n'
                        '    simular_teclado(["Ana"])\n'
                        '    asegurar saludar() == "Hola, Ana"\n'
                        '    asegurar saludar() == "Hola, nadie"\n'
                        "}"),
    "leer_tabla": ("En Excel: Archivo > Guardar como > Tipo: CSV (delimitado por comas), en "
                   "la carpeta del programa. Las claves son los títulos de la primera fila. "
                   "Los números llegan como números, también 3.500, 3.500,50 y $ 3.500",
                   "# precios.csv está al lado del programa y dice:\n"
                   "#     producto;precio\n"
                   "#     Yerba;3.500\n"
                   'para fila en leer_tabla("precios.csv") {\n'
                   '    mostrar("{fila.producto} sale {pesos(fila.precio)}")\n'
                   "}"),
    "agregar_a_archivo": ("Si el archivo no existe, lo crea. Con 'probar' no toca el archivo "
                          "de verdad: lo agregado se ve con leer_archivo() en esa prueba",
                          'agregar_a_archivo("pedidos.txt", "{hoy()}: 2 de yerba")\n'
                          'agregar_a_archivo("pedidos.txt", "{hoy()}: 1 de azúcar")\n'
                          'mostrar(leer_archivo("pedidos.txt"))'),
}
# Las palabras que se explican junto con otra.
VER_AYUDA_DE = {
    "devolver": "funcion", "sino": "si", "en": "para", "continuar": "romper",
    "o": "y", "no": "y", "falso": "verdadero", "logico": "verdadero",
    "estado": "agente", "al": "agente", "recibir": "agente", "como": "agente",
    "yo": "remitente", "falla": "intentar", "llamado": "crear", "responde": "mensaje",
    "cualquiera": "mensaje", "a": "enviar",
    "freno": "frenos", "reserva": "frenos", "prohibido": "frenos", "precios": "frenos",
    "consultas_por_dia": "frenos", "tokens_por_dia": "frenos", "propuestas": "frenos",
    "proponer": "frenos",
}


def ayuda_de(palabra):
    """La ayuda de una palabra de Mate o de una función incluida (o None si no es)."""
    nombre = " ".join(sin_tildes(palabra).split())
    nombre = nombre[:-2] if nombre.endswith("()") else nombre
    nota = []
    if nombre in FUNCIONES:
        _, _, ejemplo, que = FUNCIONES[nombre]
        titulo = f"{nombre} (función incluida): {que}"
        if nombre in AYUDA_DE_FUNCION:
            titulo += ". " + AYUDA_DE_FUNCION[nombre][0]
            ejemplo = AYUDA_DE_FUNCION[nombre][1]
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
    except ErrorMate as e:
        # Un texto de tres comillas sin cerrar sigue abajo (también tras un renglón vacío).
        # Lo demás está mal escrito: que lo diga el error.
        return "texto" if getattr(e, "texto_abierto", False) else False
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


def renglon_duplicado(renglon):
    """En la consola: si el renglón es el mismo texto pegado dos (o tres) veces seguidas,
    sin nada en el medio, devuelve ese texto una sola vez. Si no, None."""
    texto = renglon.strip()
    for veces in (3, 2):
        largo, resto = divmod(len(texto), veces)
        if not resto and largo >= 4 and texto == texto[:largo] * veces \
                and any(c.isalpha() for c in texto[:largo]):
            return renglon_duplicado(texto[:largo]) or texto[:largo]
    return None


def consola(entrada=None, mostrar=print, ia_simulada=False, ia_respuestas=(), anotar=None):
    """La orden 'consola': para probar renglones sueltos sin crear un archivo. Lo que se
    declara queda para los renglones siguientes, y un valor suelto se muestra solo.
    ia_simulada: con --ia-simulada, consultar_ia() tampoco sale a la red desde acá.
    anotar: a quién avisarle de cada error mostrado (el registro de errores de uso)."""
    anotar = anotar or (lambda *_a, **_k: None)
    interprete = Interprete(salida=mostrar)
    interprete.ia_simulada = bool(ia_simulada)
    interprete.ia_respuestas = list(ia_respuestas)
    interprete.glob.se_pisa = True  # acá se puede volver a declarar algo para corregirlo
    if entrada is not None:
        interprete.entrada = entrada  # (en las pruebas: de ahí saca leer() su respuesta)
    entrada = entrada or input
    mostrar(f"Mate {VERSION}, consola. Escribí un renglón y apretá Enter; para terminar, salir")
    mostrar("(un valor suelto, como 2 + 3, se muestra solo; 'ayuda si' explica una palabra)")
    declarado = []  # lo ya declarado, para revisar los contratos de lo que se escriba
    renglon, pendiente = 1, []  # los renglones se numeran de corrido, como en un archivo

    def decir(linea, texto, ultimo, familia=None):
        anotar(texto, familia=familia or getattr(texto, "familia", None))
        texto, _, camino = texto.partition("\ncómo se llegó: ")
        antes = f"línea {linea}: " if linea and int(linea) != ultimo else ""
        mostrar(f"{antes}error: {texto}")
        if camino:
            mostrar(f"    cómo se llegó: {camino}")

    def correr_pedazo(fuente, ultimo):
        try:
            programa = analizar(fuente, en_consola=True)
            se_declaran = [s for s in programa
                           if s[0] in ("sea", "funcion", "agente", "mensaje",
                                       "usar_python")]
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
            decir(e.linea, interprete.con_camino(e.mensaje, e), ultimo, e.familia)
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
            una_vez = renglon_duplicado(linea)
            if una_vez:
                texto = ("parece que el renglón se pegó dos veces. Escribilo una sola vez:  "
                         + una_vez)
                anotar("parece que el renglón se pegó dos veces (y Mate mostró el renglón "
                       "bien escrito)", categoria="renglón pegado dos veces", sugerencia=True)
                mostrar(f"error: {texto}")
                continue
            if pegado_de_powershell(linea):
                texto = ("eso es de PowerShell, y acá adentro (en la consola de Mate) van "
                         "renglones de Mate. Para volver a PowerShell escribí salir, y pegá "
                         "el comando allá")
                anotar(texto, categoria="un comando de PowerShell en la consola de Mate")
                mostrar(f"error: {texto}")
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
        falta = falta_cerrar("\n".join(pendiente + [linea]))
        if (orden and falta) or falta == "texto":
            pendiente.append(linea)
            continue
        fuente = "\n" * (renglon - 1) + "\n".join(pendiente + [linea])
        renglon += len(pendiente) + 1
        pendiente = []
        # (el último renglón con algo escrito: un error ahí no hace falta decir dónde está)
        correr_pedazo(fuente, fuente.rstrip().count("\n") + 1)
    return 0


# ─────────────────────── El curso: aprender Mate desde cero (0.5) ───────────────────────
# Al lado de mate.py, en la carpeta 'curso', hay una clase por archivo: clase_01_hola.md es
# el texto para leer (se abre con el Bloc de notas) y clase_01_hola.mate, el programa de
# esa clase. La orden 'curso' las lista y dice cómo abrir cada una; 'curso 3' muestra la
# clase 3 en la pantalla. Solo lee esos archivos: no corre nada ni escribe nada.
CARPETA_DEL_CURSO = "curso"
_ARCHIVO_DE_CLASE = re.compile(r"clase_(\d\d)_[a-z0-9_]+\.md")


def carpeta_del_curso():
    """La carpeta del curso: siempre al lado de mate.py."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), CARPETA_DEL_CURSO)


def clases_del_curso(carpeta=None):
    """Las clases que hay en la carpeta del curso, en orden: una lista de mapas con numero,
    titulo (el primer renglón escrito del texto), texto (la ruta del .md) y programa (la
    ruta del .mate de esa clase, o None si no está). Si la carpeta no existe, nada."""
    carpeta = carpeta_del_curso() if carpeta is None else os.fspath(carpeta)
    try:
        nombres = sorted(os.listdir(carpeta))
    except OSError:
        return []
    clases = []
    for nombre in nombres:
        es_clase = _ARCHIVO_DE_CLASE.fullmatch(nombre)
        if not es_clase:
            continue
        ruta = os.path.join(carpeta, nombre)
        try:
            renglones = leer_fuente(ruta).split("\n")
        except (OSError, ErrorMate):
            continue
        titulo = next((r.strip().lstrip("#").strip() for r in renglones if r.strip()), nombre)
        programa = ruta[:-len(".md")] + ".mate"
        clases.append({"numero": int(es_clase.group(1)), "titulo": titulo, "texto": ruta,
                       "programa": programa if os.path.isfile(programa) else None})
    return clases


def ruta_para_escribir(ruta):
    """Una ruta como conviene escribirla en una orden desde la carpeta donde está parada
    la persona: corta (mate\\curso\\...) si queda adentro de esa carpeta, completa si no,
    y entre comillas si trae espacios."""
    completa = os.path.abspath(ruta)
    try:
        corta = os.path.relpath(completa)
    except ValueError:  # (en Windows, cuando está en otro disco)
        corta = completa
    return para_pegar(completa if corta.startswith("..") else corta)


def orden_curso(args, avisar, carpeta=None, mostrar=print):
    """La orden 'curso': sin nada más, lista las clases y dice cómo abrir cada una; con un
    número, muestra esa clase. Devuelve el código de salida."""
    carpeta = carpeta_del_curso() if carpeta is None else os.fspath(carpeta)
    clases = clases_del_curso(carpeta)
    if not clases:
        avisar(f"no encuentro las clases del curso: tendrían que estar en {para_pegar(carpeta)}"
               " (la carpeta 'curso', al lado de mate.py). Si copiaste solo mate.py, bajá "
               "Mate de nuevo con todas sus carpetas",
               "al escribir la orden: no está la carpeta del curso")
        return 2
    numeros = [c["numero"] for c in clases]
    if numeros == list(range(numeros[0], numeros[-1] + 1)) and len(numeros) > 1:
        numeros = f"del {numeros[0]} al {numeros[-1]}"
    else:
        numeros = ", ".join(str(n) for n in numeros)
    if len(args) > 1 or (args and not (args[0].isascii() and args[0].isdigit()
                                       and len(args[0]) <= 4)):
        avisar(f"después de 'curso' va solo el número de la clase ({numeros}) y recibió "
               f"'{' '.join(args)}'. Por ejemplo:  {como_se_llama()} curso {clases[0]['numero']}",
               "al escribir la orden: 'curso' con algo que no es un número de clase")
        return 2
    if args:
        elegida = [c for c in clases if c["numero"] == int(args[0])]
        if not elegida:
            avisar(f"el curso no tiene una clase {int(args[0])}: van {numeros}. "
                   f"Para ver la lista:  {como_se_llama()} curso",
                   "al escribir la orden: 'curso' con un número de clase que no existe")
            return 2
        mostrar(leer_fuente(elegida[0]["texto"]).rstrip("\n"))
        return 0
    primera = clases[0]
    mostrar(f"El curso de Mate: {len(clases)} clases cortas, para hacer en orden. No hace falta "
            "saber programar.")
    mostrar("Cada clase es un texto para leer (termina en .md) y un programa para correr "
            "(termina en .mate).")
    mostrar("")
    ancho = max(len(re.sub(r"^Clase \d+:\s*", "", c["titulo"])) for c in clases)
    for clase in clases:
        titulo = re.sub(r"^Clase \d+:\s*", "", clase["titulo"])
        mostrar(f"  {clase['numero']:>2}. {titulo.ljust(ancho)}   "
                f"{os.path.basename(clase['texto'])}")
    mostrar("")
    mostrar(f"Para leer la clase {primera['numero']} acá mismo (las demás, con su número):")
    mostrar(f"  {como_se_llama()} curso {primera['numero']}")
    mostrar("Para abrirla con el Bloc de notas (las demás, con el nombre de su archivo):")
    mostrar(f"  notepad {ruta_para_escribir(primera['texto'])}")
    if primera["programa"]:
        mostrar("Para correr el programa de esa clase:")
        mostrar(f"  {como_se_llama()} correr {ruta_para_escribir(primera['programa'])}")
    mostrar("")
    mostrar(f"Todo está en la carpeta {ruta_para_escribir(carpeta)}. Ahí también hay un "
            "README.md que cuenta cómo")
    mostrar("hacer el curso. Ninguna clase necesita clave ni internet.")
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
        "  curso                    las clases para aprender Mate desde cero, en orden",
        "  curso 1                  muestra la clase 1 (también se abre con el Bloc de notas)",
        "",
        "Para que un agente aprenda (mirá 'ayuda recordado'):",
        '  corregir  archivo.mate Mostrador "la lección"   le anota una lección a ese agente',
        "  lecciones archivo.mate   muestra las lecciones de cada agente",
        "  lecciones archivo.mate Mostrador --borrar=2   le borra la lección 2",
        "  bitacora  archivo.mate   resume las fallas que anotaron sus agentes, los frenos",
        "                           que saltaron y cuánto consultó a la IA cada agente por día",
        "",
        "Para confiarle la atención a un agente con IA (mirá 'ayuda frenos'):",
        "  frenos { ... }           va en el programa, dentro del agente: las reglas que Mate",
        "                           le revisa a cada respuesta de la IA (precios permitidos,",
        "                           palabras prohibidas, largo) y el tope de consultas por día",
        "  propuestas archivo.mate  muestra las lecciones propuestas: las deja cada freno que",
        "                           salta, y ningún agente las usa hasta que las aprobás",
        "  propuestas archivo.mate aprobar 1     la aprueba (o: descartar 1)",
        '  proponer  archivo.mate Mostrador "qué estuvo mal"   Mate redacta la lección y la',
        "                           deja propuesta (con clave la redacta la IA, y se paga)",
        "",
        "Para trabajar con tus datos y charlar con el programa (son funciones: van adentro",
        "del programa, y cada una tiene su ayuda, por ejemplo 'ayuda leer_tabla'):",
        '  leer_tabla("precios.csv")   la planilla de Excel guardada como CSV, fila por fila',
        '  agregar_a_archivo("pedidos.txt", t)   anota un renglón más al final de ese archivo',
        '  leer("Cliente:", "chau")    espera que escribas y aprietes Enter (Ctrl+C termina)',
        "",
        "Para sumar lo que Mate no trae (mirá 'ayuda python'):",
        '  usar python "ayudas.py"  va en el programa: trae las funciones de ese archivo de',
        "                           Python, que está al lado, y se llaman ayudas.nombre(...).",
        "                           Ojo: ese Python corre con todos los permisos de la",
        "                           computadora. Usá solo archivos tuyos o de confianza",
        "",
        "Para que Mate mejore (anota en esta computadora los errores que te muestra):",
        "  informe                  resume los errores de uso: los más frecuentes y los que",
        "                           se repitieron seguido (el mensaje no alcanzó)",
        "  informe --para-mejorar   arma un texto para pegarle a un asistente y pedirle mejoras",
        "  informe --borrar         borra el registro de errores de uso",
        "",
        "Opciones:",
        "  --traza       muestra la conversación entre agentes, numerada y con lo que falló",
        "  --traza=conversacion.txt   la guarda en ese archivo, con un resumen al final",
        "  --sin-limite  no corta los programas que dan muchísimos pasos",
        "  --ia-simulada consultar_ia() no sale a la red ni gasta: da su respuesta preparada",
        "  --ia-simulada=respuestas.txt   ...o las que están escritas en ese archivo",
        "  --olvidar     con 'correr': los agentes arrancan de cero, sin lo que recordaban",
        "  --sin-registro  esta vez no anota nada en el registro de errores de uso",
        "  --depurar     si Mate falla por dentro, muestra el detalle técnico",
        "  --version     dice qué versión de Mate es",
        "",
        f"El registro de errores de uso es el archivo {NOMBRE_DEL_REGISTRO}, al lado de mate.py:",
        "no guarda tus programas, tapa tus datos y no sale de esta computadora. Para apagarlo",
        "del todo, en PowerShell:  $env:MATE_SIN_REGISTRO = \"1\"",
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
    for rem, dest, msg, _ in cola[:5]:
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


def con_puntos(n):
    """12345 -> "12.345" (los miles con punto, como se escribe acá)."""
    return f"{n:,}".replace(",", ".")


def lineas_de_gasto(memoria, hoy):
    """Los renglones de 'bitacora' que cuentan cuánto consultó a la IA cada agente con
    frenos: hoy, día por día en la última semana, y el total de lo guardado. Se cuentan
    consultas y tokens (lo que informa el servicio), no plata: el precio cambia."""
    def cuanto(cuentas):
        consultas, simuladas, tokens = (sum(c.get(k, 0) for c in cuentas)
                                        for k in ("consultas", "simuladas", "tokens"))
        partes = [f"{con_puntos(consultas)} consulta{'' if consultas == 1 else 's'}"]
        if tokens:
            partes.append(f"{con_puntos(tokens)} tokens")
        texto = ", ".join(partes)
        if simuladas:
            texto += (f"  (y {con_puntos(simuladas)} simulada{'' if simuladas == 1 else 's'}, "
                      "que no se pagan)")
        return texto

    lineas = []
    for agente, ficha in memoria.items():
        gasto = ficha.get("gasto")
        if not gasto:
            continue
        lineas.append(f"  {agente}")
        lineas.append(f"    hoy:              {cuanto([gasto.get(hoy.isoformat(), {})])}")
        for atras in range(1, 7):
            dia = hoy - datetime.timedelta(days=atras)
            if dia.isoformat() in gasto:
                lineas.append(f"    {dia.strftime('%d/%m/%Y')}:       "
                              f"{cuanto([gasto[dia.isoformat()]])}")
        lineas.append(f"    últimos {len(gasto)} día(s) con consultas (se guardan "
                      f"{DIAS_DE_GASTO}): {cuanto(list(gasto.values()))}")
    if not lineas:
        return []
    return (["Consultas a la IA (la cuenta la llevan los agentes que tienen 'frenos'):"]
            + lineas + ["  Se cuentan consultas y tokens, que es lo que cobra el servicio; el "
                        "tope por día se pone en los 'frenos' del agente."])


INSTRUCCIONES_PARA_REDACTAR = (
    "Vas a ayudar al dueño de un negocio a corregir a su asistente, que atiende clientes. El "
    "dueño cuenta qué hizo mal el asistente. Escribí UNA lección corta para ese asistente, "
    "en castellano rioplatense y hablándole de vos (por ejemplo: 'No ofrezcas envíos: el "
    "negocio no los hace.'). Un solo renglón de no más de 250 letras, sin comillas y sin "
    "explicaciones: solo la lección.")


def redactar_leccion(queja, respuesta, opciones, respuestas):
    """La lección que se propone a partir de lo que cuenta el dueño: (texto, quién la
    redactó, los tokens que costó). Con clave la redacta la IA; con --ia-simulada=archivo,
    el archivo; y si no hay IA (o falla, o se pasa de largo), va una redacción fija."""
    pregunta = f"Lo que estuvo mal, según el dueño: {queja}"
    if respuesta:
        pregunta += f"\nLo que había contestado el asistente: {respuesta}"
    fija = en_un_renglon(f"Una respuesta tuya estuvo mal: {queja.rstrip(' .')}. No lo "
                         "repitas.", LARGO_DE_LECCION)
    if "--ia-simulada" in opciones:
        pares = respuestas_de_archivo(respuestas) if respuestas else []
        dicho = respuesta_del_archivo(pares, pregunta)
        if dicho is None:
            return fija, "Es una redacción fija (con --ia-simulada sola no hay IA).", None
        como, tokens = "La redactó la IA simulada (el archivo de respuestas).", None
    elif not os.environ.get("ANTHROPIC_API_KEY", "").strip():
        return fija, ("Es una redacción fija: no hay clave para la IA (con la clave puesta "
                      "en ANTHROPIC_API_KEY la redacta la IA, y esa consulta se paga)."), None
    else:
        _USO_DE_LA_IA.clear()
        try:
            dicho = pedir_a_la_ia(INSTRUCCIONES_PARA_REDACTAR, pregunta)
        except ErrorMate as e:
            return fija, ("Es una redacción fija, porque la IA no contestó: "
                          + e.mensaje.split("\n")[0]), None
        except Exception as e:  # nunca un error de Python (ni la clave) a la vista
            return fija, ("Es una redacción fija, porque algo salió mal al hablar con la IA "
                          f"({type(e).__name__})."), None
        como, tokens = "La redactó la IA (fue una consulta de verdad, paga).", \
            _USO_DE_LA_IA.get("tokens") or 0
    dicho = " ".join(dicho.split()).strip('"“”')
    if not dicho or len(dicho) > LARGO_DE_LECCION:
        return fija, ("Es una redacción fija: lo que redactó la IA estaba vacío o pasaba las "
                      f"{LARGO_DE_LECCION} letras de una lección."), tokens
    return dicho, como, tokens


def mostrar_bitacora(ruta, avisar):
    """La orden 'bitacora': las fallas que anotaron los agentes de ese programa, resumidas."""
    programa, archivo = os.path.basename(ruta), archivo_de(ruta, "bitacora.txt")
    try:
        renglones = renglones_de_bitacora(archivo)
    except ErrorMate as e:
        avisar(e.mensaje)
        return 2
    fallas = [r.split(" | ", 4) for r in renglones]
    raros = sum(len(f) != 5 for f in fallas)
    fallas = [f for f in fallas if len(f) == 5]
    try:  # la cuenta de consultas a la IA de los agentes con frenos (0.5)
        gasto = lineas_de_gasto(leer_memoria(archivo_de(ruta, "memoria.json"))[0],
                                datetime.date.today())
    except ErrorMate:
        gasto = []  # (la memoria no se entiende: eso lo explican 'correr' y 'lecciones')
    if not fallas:
        print(f"{programa} no tiene fallas anotadas"
              + (f" ({archivo} tiene {raros} renglón(es) que no entiendo)." if raros else "."))
        if gasto:
            print("\n".join([""] + gasto))
            return 0
        print("La bitácora se arma sola cuando falla un agente de un programa que usa "
              "'estado recordado', lecciones o frenos, al correrlo con 'correr'.")
        return 0
    print(f"Bitácora de {programa}: {len(fallas)} falla(s) anotada(s), del {fallas[0][0]} "
          f"al {fallas[-1][0]}.")

    def tabla(titulo, columna, largo, cuantos=None):
        veces = {}
        for falla in fallas:
            clave = en_un_renglon(falla[columna], largo)
            veces[clave] = veces.get(clave, 0) + 1
        print("")
        print(titulo)
        for clave, n in sorted(veces.items(), key=lambda par: -par[1])[:cuantos]:
            print(f"  {n:>4} {'vez ' if n == 1 else 'veces'}  {clave}")

    tabla("Por agente:", 1, 60)
    tabla("Qué pasó:", 2, 60)
    tabla("Los motivos que más se repiten:", 4, 110, 5)
    print("")
    print("Las últimas:")
    for falla in fallas[-5:]:
        print(f"  {falla[0]}  {falla[1]} {falla[2]} atendiendo {en_un_renglon(falla[3], 70)}")
        print(f"      {en_un_renglon(falla[4], 110)}")
    if raros:
        print("")
        print(f"({raros} renglón(es) del archivo no tienen la forma de siempre y no los conté)")
    if gasto:
        print("\n".join([""] + gasto))
    print("")
    print(f"Está todo en {archivo} (se abre con el Bloc de notas; si lo borrás, empieza "
          "de nuevo).")
    return 0


def orden_de_memoria(orden, args, borrar, avisar, opciones=(), respuestas=None):
    """Las órdenes 'corregir', 'lecciones', 'bitacora', 'propuestas' y 'proponer': miran (o
    cambian) lo que aprendió un programa, sin correrlo. Devuelven el código de salida."""
    ejemplos = {"bitacora": "bitacora mi_mostrador.mate",
                "lecciones": "lecciones mi_mostrador.mate",
                "corregir": 'corregir mi_mostrador.mate Mostrador "Los lunes no hay pan"',
                "propuestas": "propuestas mi_mostrador.mate",
                "proponer": 'proponer mi_mostrador.mate Mostrador "Ofreció envíos y no '
                            'hacemos envíos"'}
    if not args:
        avisar(f"a '{orden}' le falta el programa, por ejemplo: {ejemplos[orden]}"
               + (f" (en esta carpeta hay un {orden}.mate: para correrlo, correr {orden}.mate)"
                  if os.path.isfile(f"{orden}.mate") else ""))
        return 2
    if borrar is not None and orden != "lecciones":
        avisar("--borrar va con 'lecciones', por ejemplo: lecciones mi_mostrador.mate "
               "Mostrador --borrar=2")
        return 2
    ruta, problema = _ubicar(args[0])
    if problema:
        avisar(problema)
        return 2
    programa = os.path.basename(ruta)
    if orden == "bitacora":
        if len(args) > 1:
            avisar(f"'bitacora' lleva solo el programa: {ejemplos[orden]}")
            return 2
        return mostrar_bitacora(ruta, avisar)
    try:
        fuente = leer_fuente(ruta)
        declarados = [s[2] for s in analizar(fuente, ruta) if s[0] == "agente"]
    except OSError:
        avisar(f"no pude abrir {ruta}")
        return 2
    except ErrorMate:
        avisar(f"{ruta} tiene un error y no puedo ver qué agentes tiene. Miralo con:  "
               f"{como_se_llama()} verificar {args[0]}")
        return 2
    archivo = archivo_de(ruta, "memoria.json")
    try:
        memoria, avisos = leer_memoria(archivo)
    except ErrorMate as e:
        avisar(e.mensaje)
        return 2
    for aviso in avisos:
        avisar(f"aviso: {aviso}")

    def conocido(nombre):
        """El agente con ese nombre, como está escrito en el programa (o None). Vale una
        copia con nombre ("Mostrador Centro") y da igual mayúsculas que minúsculas."""
        nombre = " ".join(nombre.split())
        posibles = declarados + [a for a in memoria if a not in declarados]
        for candidato in posibles:
            if candidato.lower() == nombre.lower():
                return candidato
        molde, _, apodo = nombre.partition(" ")
        for candidato in declarados:
            if apodo and candidato.lower() == molde.lower():
                return f"{candidato} {apodo}"
        return None

    def listar(agente):
        for i, leccion in enumerate(memoria[agente]["lecciones"], 1):
            print(f"  {i}. {leccion['texto']}"
                  + (f"   (del {leccion['fecha']})" if leccion["fecha"] else ""))

    def guardar():
        problema = guardar_memoria(archivo, programa, memoria)
        if problema:
            avisar(problema)
        return problema

    if orden == "propuestas":
        return orden_propuestas(args, memoria, guardar, listar, avisar)

    # Una copia se nombra con el agente y su nombre: "Mostrador Centro". Si se escribió sin
    # comillas (Mostrador Centro), también vale: con 'lecciones' siempre, y con 'corregir'
    # cuando esa copia existe (está en el programa o en la memoria).
    copias = {" ".join(f"{molde} {apodo}".lower().split()) for molde, apodo in re.findall(
        r'\bcrear\s+(\w+)\s+llamado\s+"([^"\n{}]+)"', fuente)} | {a.lower() for a in memoria}
    if orden == "lecciones" and len(args) > 2:
        args = [args[0], " ".join(args[1:])]
    elif orden in ("corregir", "proponer") and len(args) > 2 and args[2].strip() \
            and conocido(args[1]) in declarados \
            and " ".join(f"{args[1]} {args[2]}".lower().split()) in copias:
        args = [args[0], f"{args[1]} {args[2]}"] + args[3:]
    agente = None
    if len(args) > 1:
        agente = conocido(args[1])
        if agente is None:
            avisar(f"{programa} no tiene un agente '{args[1]}'.{sugerir(args[1], declarados)}"
                   + (" Sus agentes son: " + ", ".join(declarados) if declarados
                      else " Ese programa no tiene agentes"))
            return 2
    if orden == "proponer":
        if agente is None or len(args) < 3 or len(args) > 4 or not args[2].strip():
            avisar("a 'proponer' le faltan el agente y qué estuvo mal (entre comillas), por "
                   f"ejemplo: {ejemplos[orden]}"
                   + (". Los agentes de ese programa son: " + ", ".join(declarados)
                      if declarados and agente is None else "")
                   + (". Después puede ir, también entre comillas, lo que había contestado "
                      "el agente; nada más" if len(args) > 4 else ""))
            return 2
        queja = " ".join(args[2].split())
        if len(queja) > 220:
            avisar(f"lo que estuvo mal tiene {len(queja)} letras y el tope es 220: contalo "
                   "más corto (de ahí sale una lección, y las lecciones son cortas)")
            return 2
        try:
            texto, como, tokens = redactar_leccion(
                queja, en_un_renglon(args[3], 600) if len(args) > 3 else "", opciones,
                respuestas)
        except ErrorMate as e:
            avisar(e.mensaje)
            return 2
        ficha = memoria.setdefault(agente, {"estado": {}, "lecciones": []})
        if tokens is not None:  # fue una consulta de verdad: entra en la cuenta de hoy
            hoy = ficha.setdefault("gasto", {}).setdefault(
                datetime.date.today().isoformat(), {"consultas": 0, "simuladas": 0, "tokens": 0})
            hoy["consultas"], hoy["tokens"] = hoy["consultas"] + 1, hoy["tokens"] + tokens
        antes = ficha.get("propuestas", [])
        nuevas = sumar_propuesta(antes, ficha["lecciones"], texto,
                                 f"lo dijo el dueño: {queja}",
                                 datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
        if nuevas is antes:
            if tokens is not None:
                guardar()
            print(f"{agente} ya tenía esa lección (propuesta o aprobada): no la repito.")
            print(f"  {texto}")
            return 0
        ficha["propuestas"] = nuevas
        if guardar():
            return 1
        numero = sum(len(memoria[a].get("propuestas", [])) for a in list(memoria)[
            :list(memoria).index(agente) + 1])
        print(f"Quedó propuesta para {agente} (todavía NO la usa: falta que la apruebes):")
        print(f"  {numero}. {texto}")
        print(como)
        print(f"Para aprobarla:    {como_se_llama()} propuestas {para_pegar(args[0])} "
              f"aprobar {numero}")
        print(f"Para descartarla:  {como_se_llama()} propuestas {para_pegar(args[0])} "
              f"descartar {numero}")
        print(f"Si preferís escribirla vos:  {como_se_llama()} corregir "
              f'{para_pegar(args[0])} {para_pegar(agente)} "la lección"')
        return 0
    if orden == "corregir":
        if agente is None or len(args) < 3:
            avisar("a 'corregir' le faltan el agente y la lección (entre comillas), por "
                   f"ejemplo: {ejemplos[orden]}"
                   + (". Los agentes de ese programa son: " + ", ".join(declarados)
                      if declarados and agente is None else ""))
            return 2
        try:
            texto = leccion_limpia(" ".join(args[2:]))
        except ErrorMate as e:
            avisar(e.mensaje)
            return 2
        ficha = memoria.setdefault(agente, {"estado": {}, "lecciones": []})
        nuevas, olvidadas = sumar_leccion(
            ficha["lecciones"], texto, datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
        if nuevas is ficha["lecciones"]:
            print(f"{agente} ya tenía anotada esa lección: no la repito.")
            return 0
        ficha["lecciones"] = nuevas
        problema = guardar_memoria(archivo, programa, memoria)
        if problema:
            avisar(problema)
            return 1
        print(f"Anotado. {agente} tiene {len(nuevas)} lección(es):")
        listar(agente)
        if olvidadas:
            print(f"(El tope es {MAX_LECCIONES}: para anotar esta se borró la más vieja.)")
        print("La va a tener en cuenta cada vez que consulte a la IA con consultar_ia(), "
              f"desde la próxima corrida de {programa} (la memoria y las lecciones son del "
              "programa que se corre).")
        print(f"Para borrar una:  {como_se_llama()} lecciones {para_pegar(args[0])} "
              f"{para_pegar(agente)} --borrar=1")
        return 0
    # lecciones
    los_que_tienen = [a for a in memoria if memoria[a]["lecciones"]]
    if borrar is not None:
        if agente is None:
            avisar("para borrar una lección hay que decir de qué agente, por ejemplo: "
                   "lecciones mi_mostrador.mate Mostrador --borrar=2")
            return 2
        suyas = memoria.get(agente, {"lecciones": []})["lecciones"]
        if borrar.lower() == "todas" and suyas:
            quedan = []
        elif borrar.isdigit() and 1 <= int(borrar) <= len(suyas):
            quedan = suyas[:int(borrar) - 1] + suyas[int(borrar):]
        else:
            avisar(f"{agente} no tiene lecciones para borrar" if not suyas else
                   f"--borrar lleva el número de la lección (del 1 al {len(suyas)}) o "
                   f"'todas', y recibió '{borrar}'")
            return 2
        memoria[agente]["lecciones"] = quedan
        problema = guardar_memoria(archivo, programa, memoria)
        if problema:
            avisar(problema)
            return 1
        print(f"Borrada. A {agente} le quedan {len(quedan)} lección(es)"
              + (":" if quedan else "."))
        listar(agente)
        return 0
    mostrar_de = [agente] if agente else los_que_tienen
    if not any(memoria.get(a, {"lecciones": []})["lecciones"] for a in mostrar_de):
        if not agente and not declarados:
            print(f"{programa} no tiene agentes, así que no hay lecciones: las lecciones "
                  "son de los agentes.")
            return 0
        print((f"{agente} todavía no tiene lecciones." if agente
               else f"Los agentes de {programa} todavía no tienen lecciones.")
              + f" Se anota una con:  {como_se_llama()} corregir {para_pegar(args[0])} "
              + para_pegar(agente or declarados[0]) + ' "la lección"')
        return 0
    for a in mostrar_de:
        print(f"{a} tiene {len(memoria[a]['lecciones'])} lección(es):")
        listar(a)
    return 0


def orden_propuestas(args, memoria, guardar, listar, avisar):
    """La orden 'propuestas': ver las lecciones propuestas (las que dejó un freno al saltar
    o la orden 'proponer') y aprobarlas o descartarlas por su número. Una propuesta no se
    usa hasta que se aprueba; al aprobarla pasa a ser una lección como las de 'corregir'."""
    programa = para_pegar(args[0])
    todas = [(agente, propuesta) for agente, ficha in memoria.items()
             for propuesta in ficha.get("propuestas", [])]
    ver = f"{como_se_llama()} propuestas {programa}"
    if len(args) == 1:
        if not todas:
            print(f"{os.path.basename(args[0])} no tiene lecciones propuestas. Aparecen "
                  "solas cuando salta un freno de un agente, o las pedís con:  "
                  f'{como_se_llama()} proponer {programa} Agente "qué estuvo mal"')
            return 0
        print(f"Lecciones propuestas, sin aprobar ({len(todas)}). Ningún agente las usa "
              "todavía:")
        for numero, (agente, propuesta) in enumerate(todas, 1):
            print(f"  {numero}. Para {agente}: {propuesta['texto']}"
                  + (f"   (del {propuesta['fecha']})" if propuesta["fecha"] else ""))
            if propuesta["motivo"]:
                print(f"       Por qué: {propuesta['motivo']}")
        print(f"Para aprobar una:    {ver} aprobar 1")
        print(f"Para descartar una:  {ver} descartar 1     (o varias: descartar 1 2, o todas)")
        return 0
    que = sin_tildes(args[1].lower())
    if que not in ("aprobar", "descartar"):
        avisar(f"después del programa va 'aprobar' o 'descartar' y el número de la propuesta "
               f"(recibió '{args[1]}'). Para verlas con su número:  {ver}")
        return 2
    if not todas:
        avisar(f"no hay propuestas para {que}: {os.path.basename(args[0])} no tiene ninguna")
        return 2
    pedidas = args[2:]
    if [p.lower() for p in pedidas] == ["todas"]:
        numeros = list(range(1, len(todas) + 1))
    elif pedidas and all(p.isdigit() and 1 <= int(p) <= len(todas) for p in pedidas):
        numeros = sorted({int(p) for p in pedidas})
    else:
        avisar(f"a '{que}' le falta el número de la propuesta (del 1 al {len(todas)}; pueden "
               f"ser varios, o 'todas')" + (f" y recibió '{' '.join(pedidas)}'" if pedidas
                                            else "") + f". Para verlas:  {ver}")
        return 2
    tocados, olvidadas, repetidas = [], 0, 0
    for numero in numeros:
        agente, propuesta = todas[numero - 1]
        ficha = memoria[agente]
        ficha["propuestas"] = [p for p in ficha["propuestas"] if p is not propuesta]
        if not ficha["propuestas"]:
            del ficha["propuestas"]
        if que == "aprobar":
            nuevas, sobran = sumar_leccion(
                ficha["lecciones"], propuesta["texto"],
                datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
            repetidas += nuevas is ficha["lecciones"]
            ficha["lecciones"], olvidadas = nuevas, olvidadas + sobran
        if agente not in tocados:
            tocados.append(agente)
    if guardar():
        return 1
    cuantas = "1 propuesta" if len(numeros) == 1 else f"{len(numeros)} propuestas"
    if que == "descartar":
        print(f"Listo: descarté {cuantas}. Quedan {len(todas) - len(numeros)} sin aprobar.")
        return 0
    print(f"Listo: aprobé {cuantas}. Desde la próxima corrida "
          f"{'la' if len(numeros) == 1 else 'las'} va a tener en cuenta en cada consulta a "
          "la IA.")
    for agente in tocados:
        print(f"{agente} tiene {len(memoria[agente]['lecciones'])} lección(es):")
        listar(agente)
    if repetidas:
        print(f"({repetidas} ya estaba(n) entre las lecciones: no se repite(n).)")
    if olvidadas:
        print(f"(El tope es {MAX_LECCIONES} lecciones por agente: para anotar "
              f"{'esta' if len(numeros) == 1 else 'estas'} se borró la más vieja.)")
    if len(todas) > len(numeros):
        print(f"Quedan {len(todas) - len(numeros)} propuesta(s) sin aprobar:  {ver}")
    return 0


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


# ─────────────── Lo que el lenguaje aprende de quien lo usa (0.4) ───────────────
# Cada error que Mate le muestra a la persona deja un renglón en errores_de_uso.txt, al
# lado de mate.py, para que después se pueda ver qué mensajes no alcanzan y mejorar Mate.
# No guarda programas, tapa los datos de la persona y no sale nunca de la computadora.
# Solo anota cuando Mate se usa desde la línea de comandos (como módulo, o en las pruebas,
# no), nunca con la orden 'probar', y se apaga con MATE_SIN_REGISTRO=1 o --sin-registro.

ORDENES_SABIDAS = ORDENES + ORDENES_DE_MEMORIA + ("ayuda", "guia", "consola", "informe",
                                                  "curso")
_FECHA_DE_REGISTRO = "%d/%m/%Y %H:%M"
_LARGO_A_TAPAR = 800
# Cómo es una opción ('--traza', '-h', '--borrar=2'). Lo que empieza con guion y no tiene
# esa forma ("-10% a Juan") es algo que escribió la persona: una lección, casi siempre.
_FORMA_DE_OPCION = re.compile(r"--?[A-Za-zÀ-ÿ?][\w\-]*(=\S*)?")
# Al final del registro: después del último error hubo una corrida que anduvo bien, así
# que el próximo error, aunque sea el mismo, no viene "seguido".
_CORTE_DE_RACHA = "# (después de esto hubo una corrida que anduvo bien)"
_TEXTO_ENTRE_COMILLAS = re.compile(
    r'"""[\s\S]*?"""|"(?:\\.|[^"\\\n])*"|«[^»\n]*»|“[^”\n]*”')
# Una ruta puede traer espacios ("C:\Users\Juan Perez\Desktop"): se tapa hasta donde
# termina la frase (mejor tapar de más que dejar medio apellido a la vista).
_FIN_DE_RUTA = r"""[^\n"'|*?()]*?(?=$|\n|["'|*?()]|[,;:] |\.\s|\.$)"""
_RUTA_WIN_A_TAPAR = re.compile(r"(?:(?<![A-Za-z])[A-Za-z]:|\\)[\\/]" + _FIN_DE_RUTA, re.M)
_RUTA_LINUX_A_TAPAR = re.compile(r"(?<![\w<./])~?/[\w.\-<>]+/" + _FIN_DE_RUTA, re.M)
_NOMBRE_DE_ARCHIVO = re.compile(
    r"(?:[\w.\-<>]+[\\/])*[\w\-<>][\w.\-<>]*\.(?:mate|txt|json|py|bat|csv|md|tmp|log|ps1)\b",
    re.I)


def ruta_del_registro():
    """El archivo del registro de errores de uso: siempre al lado de mate.py."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), NOMBRE_DEL_REGISTRO)


def registro_apagado():
    """¿La persona pidió que no se anote nada? (la variable MATE_SIN_REGISTRO)"""
    return os.environ.get("MATE_SIN_REGISTRO", "").strip().lower() not in ("", "0", "no")


def donde_se_registra(registro, argv):
    """En qué archivo se anotan los errores de esta corrida, o None si no se anotan.
    registro: None (Mate usado como módulo: en ningún lado), True (la línea de comandos:
    al lado de mate.py, salvo dentro de una corrida de pytest) o la ruta de un archivo."""
    if registro is None or registro is False or registro_apagado():
        return None
    if any(a.lower() == "--sin-registro" for a in argv):
        return None
    if registro is True:
        return None if "PYTEST_CURRENT_TEST" in os.environ else ruta_del_registro()
    return os.fspath(registro)


def tapar_datos(texto, propios=()):
    """El mensaje de un error sin los datos de la persona: la clave de la IA y cualquier
    cosa con forma de clave, su nombre de usuario, los textos entre comillas, los nombres
    que eligió, las rutas, los nombres de archivos, los correos y los números largos
    quedan reemplazados por marcas como <texto> o <archivo>. Todo en un renglón.
    propios: lo que la persona escribió en la orden (archivos, nombres): se tapa
    dondequiera que aparezca."""
    texto = tapar_clave(str(texto),
                        os.environ.get("ANTHROPIC_API_KEY", "").strip().strip("\"'"))
    texto = re.sub(r"\bsk-[\w\-]{6,}|(?<![\w\-])(?=[\w\-]*\d)(?=[\w\-]*[A-Za-z])[\w\-]{24,}",
                   "<clave>", texto)
    # Igual se guardan 300 letras: de un mensaje larguísimo (trae un texto entero adentro)
    # se mira el principio y el final, para que anotar un error nunca tarde.
    cortado = len(texto) > 2 * _LARGO_A_TAPAR
    if cortado:
        texto = texto[:_LARGO_A_TAPAR] + texto[-_LARGO_A_TAPAR:]
    texto = re.sub(r"https?://\S+", "<dirección>", texto)
    texto = re.sub(r"[\w.+\-]+@[\w\-]+(?:\.[\w\-]+)+", "<correo>", texto)
    usuarios = {os.environ.get(v, "") for v in ("USERNAME", "USER", "LOGNAME")}
    usuarios.add(os.path.basename(os.path.expanduser("~").rstrip("\\/")))
    for usuario in sorted(usuarios, key=len, reverse=True):
        if len(usuario) >= 3 and usuario.lower() not in ("mate", "user", "users", "home"):
            texto = re.sub(re.escape(usuario), "<usuario>", texto, flags=re.I)
    sabidas = PALABRAS | set(FUNCIONES) | TIPOS_BASE | set(ORDENES_SABIDAS) | {
        "recordado", "salir", "llamado", "mate", "mate.py", "mate.bat", "python", "todas"}
    suyos = set()
    for propio in propios:
        nombre = re.split(r"[\\/]", propio.rstrip("\\/"))[-1]
        suyos |= {propio, nombre, re.sub(r"(?i)\.mate(\.txt)?$", "", nombre)}
    for suyo in sorted(suyos, key=len, reverse=True):
        if len(suyo) >= 3 and sin_tildes(suyo) not in sabidas:
            texto = re.sub(re.escape(suyo), "<dato>", texto, flags=re.I)
    hecha = "\x00"  # una comilla que ya se miró
    texto = _TEXTO_ENTRE_COMILLAS.sub(f"{hecha}<texto>{hecha}", texto)
    if cortado and '"' in texto:  # al cortar, una comilla quedó sin su par: se tapa de más
        primera, ultima = texto.find('"'), texto.rfind('"')
        texto = texto[:primera] + '"<texto>"' + (texto[ultima + 1:] if primera < ultima else "")
    texto = texto.replace(hecha, '"')

    def nombre(m):
        partes = m.group(1).lower().replace("(", " ").replace(")", " ").split()
        sabido = partes and all(p in sabidas for p in partes)
        return (m.group(0) if sabido else "'<nombre>'").replace("'", hecha)

    def archivo(m):
        propio = re.split(r"[\\/]", m.group(0))[-1].lower() in ("mate.py", "mate.bat")
        return m.group(0) if propio and "<" not in m.group(0) else "<archivo>"

    def opcion(m):
        sabida = m.group(1).lower() in OPCIONES + ("--borrar", "-h")
        return (m.group(1) if sabida else "--<opción>") + ("=<valor>" if m.group(2) else "")

    # Lo que va entre comillas simples puede traer un apóstrofo adentro ('O'Higgins 4500',
    # 'D'Angelo'): la comilla que cierra es la que no tiene una letra pegada después.
    texto = re.sub(r"(?<![\w'])'((?:[^'\n]|'(?=\w))*)'(?!\w)", nombre, texto)
    if "'" in texto:
        # Quedó una comilla suelta: no se sabe dónde termina el dato, así que se tapa
        # todo, de la primera comilla a la última (mejor de más que de menos).
        primera = min(i for i in (texto.find("'"), texto.find(hecha)) if i >= 0)
        ultima = max(texto.rfind("'"), texto.rfind(hecha))
        if primera < ultima:
            texto = texto[:primera] + "'<texto>'" + texto[ultima + 1:]
        elif cortado:
            texto = texto[:primera] + "'<texto>'"
        else:
            texto = re.sub(r"\S*'\S*", "<texto>", texto)
    texto = texto.replace(hecha, "'")
    # (las listas de nombres del programa: campos de un mapa, agentes)
    texto = re.sub(r"\((tiene|son|hay): [^)]*\)", r"(\1: <nombres>)", texto)
    texto = re.sub(r"(Sus agentes son|Los agentes de ese programa son): .*", r"\1: <nombres>",
                   texto)
    texto = _NOMBRE_DE_ARCHIVO.sub(archivo, texto)
    texto = _RUTA_WIN_A_TAPAR.sub("<ruta>", texto)
    texto = _RUTA_LINUX_A_TAPAR.sub("<ruta>", texto)
    texto = re.sub(r"(?<![\w\-<])(--?[A-Za-zÀ-ÿ][\w\-]*)(=[^\s,?]*)?", opcion, texto)
    texto = re.sub(r"\d{3,}(?:[.,]\d+)*", "<número>", texto)
    return en_un_renglon(texto, 300).replace("|", "/")


def categoria_de(etapa, tapado):
    """El nombre estable de un error: la etapa y el arranque de su mensaje ya tapado,
    hasta el primer punto o los dos puntos, sin números. No lleva datos de la persona."""
    molde = re.sub(r"<número>|\d+", "N", tapado)
    corte = re.compile(r"\. |: | \(|,? ¿|; ").search(molde, 12)
    if corte:
        molde = molde[:corte.start()]
    return f"{etapa}: {en_un_renglon(molde, 80)}"


def entradas_del_registro(ruta):
    """Lo que dice el registro: (entradas, renglones tal cual están, cuántos no se
    entienden). Cada entrada es un mapa con fecha, version, orden, categoria, sugerencia,
    seguidas y mensaje. Si el archivo no existe, nada; si no se puede leer, un ErrorMate."""
    try:
        texto = leer_renglones(ruta)
    except FileNotFoundError:
        return [], [], 0
    except (OSError, ErrorMate):
        raise ErrorMate(f"no pude leer el registro de errores de uso '{ruta}': fijate que "
                        "no esté abierto en otro programa")
    renglones = [r.rstrip() for r in texto
                 if r.strip() and not r.lstrip().startswith("#")]
    entradas, raros = [], 0
    for renglon in renglones:
        partes = [parte.strip() for parte in renglon.split(" | ", 6)]
        seguidas = re.fullmatch(r"(\d{1,6}) (?:vez|veces seguidas)", partes[5]) \
            if len(partes) == 7 else None
        try:
            fecha = datetime.datetime.strptime(partes[0], _FECHA_DE_REGISTRO)
        except ValueError:
            fecha = None
        if not seguidas or fecha is None or partes[4] not in ("con sugerencia",
                                                              "sin sugerencia"):
            raros += 1
            continue
        entradas.append({
            "fecha": fecha, "version": partes[1], "orden": partes[2], "categoria": partes[3],
            "sugerencia": partes[4] == "con sugerencia", "seguidas": int(seguidas.group(1)),
            "mensaje": partes[6]})
    return entradas, renglones, raros


def anotar_error_de_uso(ruta, orden, etapa, mensaje, categoria=None, sugerencia=None,
                        familia=None, otros=0, ahora=None, propios=()):
    """Suma un renglón al registro de errores de uso y deja los últimos MAX_REGISTRO.
    Si el mismo error ya era el último anotado, hace poco y con la misma orden, cuenta
    cuántas veces seguidas va (la señal de que el mensaje no alcanzó). Nunca molesta: si
    no se puede escribir, o el archivo no se entiende, no se anota y listo."""
    if not ruta:
        return
    try:
        mensaje = str(mensaje).partition("\ncómo se llegó: ")[0]
        en_agente = re.match(r"(?s).+? (?:al recibir \S+|en 'al fallar'): ", mensaje)
        if en_agente and etapa == "al correr":
            etapa, mensaje = "al correr, en un agente", mensaje[en_agente.end():]
        if sugerencia is None:
            sugerencia = "¿quisiste decir" in mensaje.lower()
        if familia == "fallar":  # eso lo escribió la persona en su programa: no se guarda
            categoria = categoria or f"{etapa}: el programa cortó con 'fallar'"
            mensaje = "<lo que el programa dijo con 'fallar'>"
        elif familia == "asegurar":
            categoria = categoria or f"{etapa}: no se cumplió un 'asegurar'"
            mensaje = "<un 'asegurar' del programa que no se cumplió>"
        elif familia == "python":  # lo que diga un archivo de Python de la persona, tampoco
            categoria = categoria or (f"{etapa}: falló algo de un archivo traído con "
                                      "'usar python'")
            mensaje = "<lo que pasó en el archivo de Python del programa>"
        else:
            mensaje = tapar_datos(mensaje, propios)
        categoria = en_un_renglon(categoria or categoria_de(etapa, mensaje), 110)
        if otros:
            mensaje += f" (y {otros} error(es) más en la misma corrida)"
        ahora = ahora or datetime.datetime.now()
        entradas, renglones, _ = entradas_del_registro(ruta)
        seguidas = 1
        if entradas and not racha_cortada(ruta) and renglones[-1].startswith(
                entradas[-1]["fecha"].strftime(_FECHA_DE_REGISTRO)):
            ultima = entradas[-1]  # (solo si el último renglón del archivo se entiende)
            minutos = (ahora - ultima["fecha"]).total_seconds() / 60
            if (ultima["categoria"], ultima["orden"].split()[:1]) == (
                    categoria, orden.split()[:1]) and 0 <= minutos <= MINUTOS_SEGUIDO:
                seguidas = ultima["seguidas"] + 1
        renglones.append(" | ".join([
            ahora.strftime(_FECHA_DE_REGISTRO), f"Mate {VERSION}",
            en_un_renglon(orden, 80).replace("|", "/"), categoria.replace("|", "/"),
            "con sugerencia" if sugerencia else "sin sugerencia",
            "1 vez" if seguidas == 1 else f"{seguidas} veces seguidas", mensaje]))
        escribir_entero(ruta, "\n".join([
            "# Registro de errores de uso de Mate: cada error que Mate te mostró, el más "
            "nuevo abajo.",
            "# Sirve para mejorar Mate. Queda solo en esta computadora: Mate no lo manda a "
            "ningún lado.",
            "# No guarda tus programas, y tapa tus datos con marcas como <texto>, <nombre>, "
            "<archivo> o <ruta>.",
            "# Cada renglón:  fecha | versión | orden | qué error fue | si traía sugerencia "
            "| cuántas veces seguidas | el mensaje, tapado",
            f"# Guarda los últimos {MAX_REGISTRO}. Para verlo resumido:  {como_se_llama()} "
            "informe",
            f"# Para borrarlo:  {como_se_llama()} informe --borrar   (o borrá este archivo: "
            "no pasa nada)",
            "# Para que Mate no anote más: la opción --sin-registro, o la variable "
            "MATE_SIN_REGISTRO con un 1.", ""] + renglones[-MAX_REGISTRO:]) + "\n")
    except Exception:  # (carpeta de solo lectura, archivo abierto en otro programa...)
        pass


def racha_cortada(ruta):
    """¿Lo último que dice el registro es que después hubo una corrida que anduvo bien?"""
    try:
        escritos = [r.strip() for r in leer_renglones(ruta) if r.strip()]
    except (OSError, ErrorMate):
        return False
    return bool(escritos) and escritos[-1] == _CORTE_DE_RACHA


def cortar_racha(ruta, ahora=None):
    """Al terminar bien un 'correr' o un 'verificar': si el último error anotado es de
    hace un rato nomás, deja dicho que después hubo una corrida que anduvo bien, para que
    el próximo error no cuente como 'seguido'. Solo toca un registro que ya existe."""
    try:
        if not ruta or not os.path.isfile(ruta) or racha_cortada(ruta):
            return
        entradas, _, _ = entradas_del_registro(ruta)
        minutos = ((ahora or datetime.datetime.now()) - entradas[-1]["fecha"]
                   ).total_seconds() / 60 if entradas else None
        if minutos is None or not 0 <= minutos <= MINUTOS_SEGUIDO:
            return
        with open(ruta, "rb") as f:
            termina_bien = f.read()[-1:] in (b"\n", b"")
        with open(ruta, "a", encoding="utf-8") as f:
            f.write(("" if termina_bien else "\n") + _CORTE_DE_RACHA + "\n")
    except Exception:  # el registro nunca molesta
        pass


def orden_usada(argv):
    """La orden y las opciones de esta corrida, sin archivos ni nada que haya escrito la
    persona: 'correr --traza'."""
    orden = "(sin orden)"
    for a in argv:
        if not a.startswith("-"):
            bajo = sin_tildes(a.lower())
            orden = bajo if bajo in ORDENES_SABIDAS else (
                "correr" if bajo.endswith((".mate", ".mate.txt")) else "(orden desconocida)")
            break
    nombres = {a.lower().split("=")[0] for a in argv if a.startswith("-")}
    return " ".join([orden] + sorted(nombres & set(OPCIONES + ("--borrar",))))


def anotar_corrida(argv, donde, codigo):
    """Al terminar una corrida que mostró un error: lo anota en el registro (el primero
    que vio la persona, y cuántos más hubo). Con 'probar' y sin errores, nada."""
    orden = orden_usada(argv)
    if donde.get("registro") and not codigo and orden.split()[0] in ("correr", "verificar"):
        cortar_racha(donde["registro"])
    if not donde.get("registro") or not codigo or orden.split()[0] in ("probar", "consola"):
        return
    errores = donde.get("errores") or [
        {"etapa": "al escribir la orden", "mensaje": texto, "categoria": categoria,
         "sugerencia": sugerencia} for texto, categoria, sugerencia in donde.get("avisado", [])]
    if not errores:
        return
    primero = errores[0]
    if primero["etapa"] == "al escribir la orden":
        errores = errores[:1]  # (los renglones que siguen son parte del mismo aviso)
    propios = [a for a in argv if not a.startswith("-")]
    propios += [a.partition("=")[2].strip('"') for a in argv if a.startswith("-")]
    propios += [a for a in argv if a.startswith("-") and not _FORMA_DE_OPCION.fullmatch(a)]
    anotar_error_de_uso(
        donde["registro"], orden, primero["etapa"], primero["mensaje"],
        categoria=primero.get("categoria"), sugerencia=primero.get("sugerencia"),
        familia=primero.get("familia"), otros=len(errores) - 1, propios=propios)


def comando_pegado(argv):
    """Si en PowerShell el comando se pegó dos (o más) veces seguidas en el mismo renglón
    ('correr mio.matepython mate\\mate.py correr mio.mate'), devuelve el comando escrito
    una sola vez. Si se pegaron dos comandos distintos, el último. Si no, None."""
    def entero(partes):
        return " ".join(para_pegar(a) for a in partes)

    junto = " ".join(argv)
    for k in range(1, len(argv)):
        cola = " ".join(argv[k:])
        if not cola.strip() or not junto.startswith(cola):
            continue  # (un "" suelto al final no es un comando pegado)
        resto = junto[len(cola):]
        for veces in (4, 3, 2, 1):  # el comando completo, repetido después del primero
            largo, sobra = divmod(len(resto), veces)
            comando = resto[:largo]
            lanzador = comando[:-len(cola) - 1]
            if (not sobra and resto == comando * veces and comando.endswith(" " + cola)
                    and lanzador.strip() == lanzador != ""
                    and re.search(r"mate|py", lanzador, re.I)):
                return f"{lanzador} {entero(argv[k:])}"
    for i, a in enumerate(argv[:-1]):
        lanzador = re.search(r"(?i)(?<=.)(python3?|py)(\.exe)?$", a)
        if lanzador and re.split(r"[\\/]", argv[i + 1])[-1].lower() == "mate.py":
            return f"{lanzador.group(0)} {entero(argv[i + 1:])}"
    return None


def lineas_de_informe(entradas, raros):
    """El informe de errores de uso, renglón por renglón."""
    def veces(n):
        return f"{n:>5} {'vez ' if n == 1 else 'veces'}"

    por_categoria = {}
    for e in entradas:
        ficha = por_categoria.setdefault(e["categoria"], {
            "veces": 0, "sugerencia": 0, "repetidas": 0, "racha": 1, "mensaje": ""})
        ficha["veces"] += 1
        ficha["sugerencia"] += e["sugerencia"]
        ficha["repetidas"] += e["seguidas"] > 1
        ficha["racha"] = max(ficha["racha"], e["seguidas"])
        ficha["mensaje"] = e["mensaje"]
    orden = sorted(por_categoria.items(), key=lambda par: -par[1]["veces"])
    versiones = sorted({e["version"] for e in entradas})
    total = len(entradas)
    lineas = [
        f"Hay {total} error(es) de uso anotado(s), del "
        f"{entradas[0]['fecha'].strftime(_FECHA_DE_REGISTRO)} al "
        f"{entradas[-1]['fecha'].strftime(_FECHA_DE_REGISTRO)} ({', '.join(versiones)}).",
        "",
        "Los más frecuentes:"]
    for categoria, ficha in orden[:10]:
        lineas.append(f"{veces(ficha['veces'])}  {categoria}")
        lineas.append(f"             el mensaje: {en_un_renglon(ficha['mensaje'], 200)}")
    if len(orden) > 10:
        lineas.append(f"             ... y {len(orden) - 10} error(es) distinto(s) más")
    lineas += ["", "Los que se repitieron seguido (la persona volvió a intentar y le salió "
                   "el mismo error: el mensaje no alcanzó):"]
    repetidos = sorted(((c, f) for c, f in orden if f["repetidas"]),
                       key=lambda par: (-par[1]["racha"], -par[1]["repetidas"]))
    for categoria, ficha in repetidos[:10]:
        lineas.append(f"  hasta {ficha['racha']} veces seguidas ({ficha['repetidas']} "
                      f"repetición(es) en total)  {categoria}")
    if not repetidos:
        lineas.append("  ninguno")
    con = sum(e["sugerencia"] for e in entradas)
    lineas += ["", f"Con sugerencia de Mate (un \"¿quisiste decir...?\" o el comando bien "
                   f"escrito): {con} de {total}."]
    sin = [(c, f) for c, f in orden if not f["sugerencia"]][:5]
    if sin:
        lineas.append("Los más frecuentes que no traían ninguna sugerencia:")
        lineas += [f"{veces(f['veces'])}  {c}" for c, f in sin]
    por_orden = {}
    for e in entradas:
        palabra = e["orden"].split(" --")[0] or "?"
        por_orden[palabra] = por_orden.get(palabra, 0) + 1
    lineas += ["", "Con qué orden pasaron: " + ", ".join(
        f"{o} {n}" for o, n in sorted(por_orden.items(), key=lambda par: -par[1]))]
    if raros:
        lineas += ["", f"({raros} renglón(es) del archivo no tienen la forma de siempre y "
                       "no los conté)"]
    return lineas


def orden_informe(args, opciones, borrar, ruta, avisar):
    """La orden 'informe': resume el registro de errores de uso, arma el texto para pedir
    mejoras (--para-mejorar) o borra el registro (--borrar)."""
    if args:
        avisar("'informe' va sola, o con --para-mejorar o --borrar, por ejemplo: informe "
               "--para-mejorar")
        return 2
    if borrar is not None and "--para-mejorar" in opciones:
        avisar("--para-mejorar y --borrar no van juntas, y no borré nada. Primero armá el "
               "texto (informe --para-mejorar) y, cuando ya lo tengas, borrá el registro "
               "(informe --borrar)")
        return 2
    if borrar is not None:
        if borrar.lower() not in ("", "todo", "todos"):
            avisar("con 'informe', --borrar va sola (borra todo el registro): informe "
                   "--borrar")
            return 2
        if not os.path.lexists(ruta):
            print("No hay registro de errores de uso para borrar.")
            return 0
        try:
            os.remove(ruta)
        except OSError:
            avisar(f"no pude borrar '{ruta}': fijate que no esté abierto en otro programa")
            return 1
        print(f"Borrado el registro de errores de uso ({ruta}). Empieza de nuevo solo.")
        return 0
    try:
        entradas, _, raros = entradas_del_registro(ruta)
    except ErrorMate as e:
        avisar(e.mensaje)
        return 2
    apagado = ("Ahora el registro está apagado (la variable MATE_SIN_REGISTRO): Mate no "
               "anota nada." if registro_apagado() else None)
    if not entradas:
        print("Todavía no hay errores de uso anotados"
              + (f" ({ruta} tiene {raros} renglón(es) que no entiendo: abrilo con el Bloc "
                 f"de notas, o borralo con:  {como_se_llama()} informe --borrar)." if raros
                 else "."))
        print("Mate anota solo, en esta computadora, cada error que te muestra (sin tus "
              "programas y con tus datos tapados), para que después se pueda ver qué "
              "mensajes no alcanzan. Nada de eso sale por internet.")
        print(apagado or f"El archivo va a ser {ruta}")
        return 0
    lineas = lineas_de_informe(entradas, raros)
    if "--para-mejorar" in opciones:
        print("\n".join([
            "(Copiá desde el renglón de abajo hasta el final y pegáselo a un asistente o a "
            "tu equipo de agentes.)",
            "",
            f"Uso Mate (versión {VERSION}): un lenguaje de programación chico, con palabras "
            "en español, cuyo intérprete es un solo archivo de Python sin dependencias "
            "(mate.py). Está pensado para gente que no programa, que usa Windows con "
            "PowerShell y el Bloc de notas, y para armar agentes que se mandan mensajes con "
            "contrato. Mate anota en mi computadora cada error que me muestra: qué error "
            "fue, con qué orden, si traía una sugerencia y si me volvió a salir enseguida. "
            "No guarda mis programas, y mis datos están tapados con marcas como <texto>, "
            "<nombre>, <archivo> o <ruta>. Este es el resumen:",
            ""] + lineas + [
            "",
            "Con estos datos te pido propuestas concretas para mejorar Mate:",
            "1. Para cada uno de los tres errores más frecuentes, y para cada uno de los "
            "que se repitieron seguido: ¿qué cambiarías para que la persona lo resuelva al "
            "primer intento, o para que ese error directamente no pueda pasar? Si es el "
            "mensaje, escribí el mensaje nuevo completo, en castellano rioplatense claro y "
            "sin palabras técnicas. Si es el lenguaje o la línea de comandos, decí "
            "exactamente qué cambia y mostrá un ejemplo de antes y después.",
            "2. ¿Cuál conviene arreglar primero y por qué?",
            "3. ¿Hay algún error de esta lista que en realidad sea un problema de la "
            "documentación o de los ejemplos y no del lenguaje?",
            "Reglas que no se negocian: Mate tiene que seguir siendo chico (un solo "
            "archivo, solo la biblioteca estándar de Python, palabras clave en español), "
            "los programas que hoy andan tienen que seguir dando el mismo resultado, y "
            "cada cambio lleva su prueba."]))
        return 0
    print("Informe de errores de uso de Mate")
    print("\n".join(lineas))
    print("")
    print(f"Está todo en {ruta} (se abre con el Bloc de notas; no sale de esta "
          "computadora).")
    print(f"Para pedirle mejoras a un asistente:  {como_se_llama()} informe --para-mejorar")
    print(f"Para borrarlo:  {como_se_llama()} informe --borrar")
    if apagado:
        print(apagado)
    return 0


def main(argv=None, registro=None):
    """registro: dónde se anotan los errores de uso. None (Mate usado como módulo, y en
    las pruebas): en ningún lado. True (la línea de comandos): en errores_de_uso.txt, al
    lado de mate.py. O la ruta de un archivo."""
    argv = list(sys.argv[1:] if argv is None else argv)
    donde = {"ruta": None, "interprete": None, "errores": [], "avisado": [],
             "registro": donde_se_registra(registro, argv),
             "informe": (ruta_del_registro() if registro is None or isinstance(registro, bool)
                         else os.fspath(registro))}
    codigo = _con_red(argv, donde)
    try:
        anotar_corrida(argv, donde, codigo)
    except Exception:  # el registro nunca le cambia el resultado a nadie
        pass
    return codigo


def _con_red(argv, donde):
    for flujo in (sys.stdout, sys.stderr, sys.stdin):
        try:  # que una consola vieja de Windows no rompa por un símbolo que no conoce
            flujo.reconfigure(errors="replace")
        except Exception:
            pass
    depurar = any(a.lower() == "--depurar" for a in argv)

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
    except CorteEnElTeclado:
        # Ctrl+C en un leer(): la charla se cortó a propósito. No es un error.
        print()
        print(CORTE_EN_EL_TECLADO)
        return 0
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
        donde["errores"].insert(0, {
            "etapa": "por dentro de Mate", "mensaje": "error interno de Mate",
            "categoria": f"por dentro de Mate: error interno ({type(e).__name__})"})
        if lugar():
            avisar(f"pasó cerca de {lugar()}")
        avisar("corré de nuevo con --depurar para ver el detalle")
        avisar_pendientes(donde["interprete"], avisar)
        return 1


def _main(argv, donde):
    def avisar(texto, categoria=None, sugerencia=None, anotado=None):
        print(texto, file=sys.stderr)
        if not texto.startswith("aviso:"):  # (para el registro de errores de uso)
            donde.setdefault("avisado", []).append((anotado or texto, categoria, sugerencia))

    una_vez = comando_pegado(argv)
    if una_vez:
        avisar("parece que el comando se pegó dos veces en el mismo renglón. Escribilo una "
               f"sola vez:\n  {una_vez}", "al escribir la orden: comando pegado dos veces",
               True, "parece que el comando se pegó dos veces en el mismo renglón (y Mate "
               "mostró el comando bien escrito)")
        return 2
    alias = {"-h": "--ayuda", "--help": "--ayuda", "-?": "--ayuda", "/?": "--ayuda"}
    opciones, args, conversacion, respuestas, borrar = set(), [], None, None, None
    for a in argv:
        corrige = bool(args) and sin_tildes(args[0].lower()) == "corregir"
        if a.lower() in alias:
            opciones.add(alias[a.lower()])
        elif a.lower().startswith("--borrar"):
            borrar = a[len("--borrar="):].strip('"')
            if a.lower() == "--borrar":
                borrar = ""  # sola va con 'informe': se revisa más abajo
            elif not a.lower().startswith("--borrar=") or not borrar:
                avisar("a --borrar le falta el número de la lección, por ejemplo: lecciones "
                       "mi_mostrador.mate Mostrador --borrar=2")
                return 2
        elif a.lower().startswith("--ia-simulada="):
            opciones.add("--ia-simulada")
            respuestas = a[len("--ia-simulada="):].strip('"')
            if not respuestas:
                avisar("a --ia-simulada= le falta el nombre del archivo de respuestas, por "
                       "ejemplo: --ia-simulada=respuestas.txt (o --ia-simulada sola)")
                return 2
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
        elif corrige and len(args) >= 3 and a.startswith("-") and (
                not _FORMA_DE_OPCION.fullmatch(a)):
            args.append(a)  # con 'corregir', la lección puede empezar con un guion: "-10% a..."
        elif a.startswith("-") and a != "-":
            if a.lower() not in OPCIONES:
                todas = OPCIONES + ("--borrar",)
                nombre, igual, valor = a.partition("=")
                parecidas = difflib.get_close_matches(nombre.lower(), todas, 1)
                con_valor = parecidas and parecidas[0] in ("--borrar", "--traza", "--ia-simulada")
                avisar(f"no conozco la opción {a}" + (
                    f", ¿quisiste decir {parecidas[0]}{igual + valor if con_valor else ''}?"
                    if parecidas else ". Las opciones son: " + ", ".join(todas))
                    + (". Si era parte de la lección, escribila entre comillas y sin el "
                       "guion adelante" if corrige and len(args) >= 3 else ""),
                    "al escribir la orden: opción que no existe")
                return 2
            opciones.add(a.lower())
        else:
            args.append(a)

    if borrar == "" and not (args and args[0].lower() == "informe"):
        avisar("a --borrar le falta el número de la lección, por ejemplo: lecciones "
               "mi_mostrador.mate Mostrador --borrar=2 (sola, --borrar va con 'informe')")
        return 2
    if "--version" in opciones:
        print(f"Mate {VERSION} (Python {sys.version_info[0]}.{sys.version_info[1]})")
        return 0
    if args and args[0].lower() == "ayuda" and len(args) >= 2 and not (
            len(args) == 2 and sin_tildes(args[1].lower()) in ORDENES + (
                "ayuda", "guia", "consola", "informe", "curso") + ORDENES_DE_MEMORIA[:2]):
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
    if args[0].lower() == "curso":
        if len(args) == 1 and os.path.isfile("curso.mate"):
            avisar("aviso: en esta carpeta hay un curso.mate, pero 'curso' sola es una orden "
                   "de Mate (muestra las clases para aprender). Para correr tu programa:  "
                   f"{como_se_llama()} correr curso.mate")
        return orden_curso(args[1:], avisar)
    if args[0].lower() == "consola":
        if len(args) > 1:
            avisar("'consola' va sola, sin archivo: ahí adentro se escriben los renglones")
            return 2
        preparadas = []
        if respuestas:
            try:
                preparadas = respuestas_de_archivo(respuestas)
            except ErrorMate as e:
                avisar(e.mensaje)
                return 2
        def anotar(texto, categoria=None, sugerencia=None, familia=None):
            anotar_error_de_uso(donde.get("registro"), orden_usada(argv), "en la consola",
                                texto, categoria and f"en la consola: {categoria}",
                                sugerencia, familia)

        return consola(ia_simulada="--ia-simulada" in opciones, ia_respuestas=preparadas,
                       anotar=anotar)
    if args[0].lower() == "informe":
        if len(args) == 1 and borrar is None and os.path.isfile("informe.mate"):
            avisar("aviso: en esta carpeta hay un informe.mate, pero 'informe' sola es una "
                   "orden de Mate (muestra los errores de uso). Para correr tu programa:  "
                   f"{como_se_llama()} correr informe.mate")
        return orden_informe(args[1:], opciones, borrar,
                             donde.get("informe") or ruta_del_registro(), avisar)
    if "--para-mejorar" in opciones:
        avisar("--para-mejorar va con 'informe', sin archivo: informe --para-mejorar")
        return 2
    if sin_tildes(args[0].lower()) in ORDENES_DE_MEMORIA:
        return orden_de_memoria(sin_tildes(args[0].lower()), args[1:], borrar, avisar,
                                opciones, respuestas)
    if borrar is not None:
        avisar("--borrar va con 'lecciones', por ejemplo: lecciones mi_mostrador.mate "
               "Mostrador --borrar=2")
        return 2

    def parece_archivo(a):
        return (a.lower().endswith((".mate", ".mate.txt")) or os.path.isfile(a)
                or os.path.isfile(a + ".mate"))

    if args[0].lower() not in ORDENES and parece_archivo(args[0]):
        if len(args) == 1:
            args = ["correr"] + args  # 'mate.py hola.mate' es 'mate.py correr hola.mate'
        elif len(args) == 2 and args[1].lower() in ORDENES:
            avisar(f"la orden va primero y el archivo después: {args[1].lower()} {args[0]}",
                   "al escribir la orden: el archivo antes que la orden", True)
            return 2
    orden, archivos = args[0].lower(), args[1:]
    if orden not in ORDENES:
        parecidas = difflib.get_close_matches(orden, ORDENES_SABIDAS, 1)
        avisar(f"no conozco la orden '{args[0]}'" + (
            f", ¿quisiste decir '{parecidas[0]}'?" if parecidas
            else ". Las órdenes son: correr, probar, verificar, consola, guia, ayuda, "
                 "curso, corregir, lecciones, propuestas, proponer, bitacora e informe"),
            "al escribir la orden: orden que no existe")
        return 2
    if not archivos:
        avisar(f"a '{orden}' le falta el archivo, por ejemplo: {orden} hola.mate",
               "al escribir la orden: falta el archivo")
        return 2
    if orden == "probar" and (len(archivos) > 1 or os.path.isdir(archivos[0])):
        return probar_varios(archivos, [a for a in argv if a.startswith("-")], avisar)
    if "--olvidar" in opciones and orden != "correr":
        avisar("--olvidar va con 'correr': el programa corre con sus agentes de cero, sin "
               "lo que recordaban")
        return 2
    if len(archivos) > 1:
        avisar(f"'{orden}' lleva un solo archivo y recibió {len(archivos)}: "
               + ", ".join(archivos)
               + " (si el nombre tiene espacios, ponelo entre comillas)",
               "al escribir la orden: más de un archivo")
        return 2

    ruta, problema = _ubicar(archivos[0])
    if problema:
        avisar(problema, "al escribir la orden: no está el archivo"
               if problema.startswith("no encuentro") else None)
        return 2
    donde["ruta"] = ruta
    if ruta.lower().endswith(".mate.txt"):
        avisar(f"aviso: {os.path.basename(ruta)} termina en .txt (se lo agregó el Bloc de "
               "notas). Lo corro igual; para que quede bien, al guardar elegí "
               "Tipo: Todos los archivos")

    mostrado = {}
    etapa = ["al leer el programa"]  # en qué andaba Mate cuando mostró cada error

    def reportar(linea, texto, familia=None):
        donde.setdefault("errores", []).append({
            "etapa": etapa[0] if donde["interprete"] is None else "al correr",
            "mensaje": texto, "familia": familia or getattr(texto, "familia", None)})
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

    archivo_memoria = archivo_de(ruta, "memoria.json")
    aprendido = {"leida": None, "abierta": False}  # leida: lo que decía el archivo al abrirlo

    def cerrar_memoria():
        """Al terminar 'correr': guarda lo que recuerdan los agentes (si cambió) y suma
        sus fallas a la bitácora. Un programa que no usa nada de esto no crea archivos."""
        interprete = donde["interprete"]
        if not aprendido["abierta"]:
            return
        aprendido["abierta"] = False
        nueva = interprete.memoria_actual()
        if nueva != aprendido["leida"] and (nueva or os.path.lexists(archivo_memoria)):
            problema = guardar_memoria(archivo_memoria, os.path.basename(ruta), nueva)
            if problema:
                avisar(f"aviso: {problema}")
        problema = guardar_bitacora(archivo_de(ruta, "bitacora.txt"), os.path.basename(ruta),
                                    interprete.bitacora or [], escrito=ruta)
        if problema:
            avisar(f"aviso: {problema}")

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
        etapa[0] = "antes de correr"
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
        interprete.ia_simulada = "--ia-simulada" in opciones
        if respuestas:
            try:
                interprete.ia_respuestas = respuestas_de_archivo(respuestas)
            except ErrorMate as e:
                avisar(e.mensaje)
                return 2
        if orden == "correr":
            # Lo que aprendieron los agentes (0.4): solo 'correr' lee y escribe su memoria.
            try:
                memoria, avisos = leer_memoria(archivo_memoria)
                aprendido["leida"] = json.loads(json.dumps(memoria))
            except ErrorMate as e:
                if "--olvidar" not in opciones:
                    avisar(e.mensaje)
                    return 2
                # No se entendía, y pidieron empezar de cero: ahí adentro puede haber
                # lecciones, así que el archivo roto no se pisa: queda guardado aparte.
                memoria, avisos, rota = {}, [], archivo_de(ruta, "memoria.rota.json")
                try:
                    os.replace(archivo_memoria, rota)
                except OSError:
                    avisar(f"{e.mensaje}\n(--olvidar no lo pisa: ahí pueden estar las "
                           "lecciones, y no pude guardarlo aparte)")
                    return 2
                avisar("aviso: --olvidar: los agentes arrancan de cero. "
                       f"{os.path.basename(archivo_memoria)} estaba mal escrito y no se "
                       "entendía, así que esta vez se pierden también las "
                       f"lecciones. Lo dejé como estaba en {rota} (se abre con el Bloc de "
                       "notas) por si querés rescatar alguna y anotarla de nuevo con "
                       "'corregir'")
            for aviso in avisos:
                avisar(f"aviso: {aviso}")
            if "--olvidar" in opciones:
                for ficha in memoria.values():
                    ficha["estado"] = {}
                if aprendido["leida"] is not None:
                    avisar("aviso: --olvidar: los agentes arrancan de cero, sin lo que "
                           "recordaban (las lecciones no se borran: eso se hace con la "
                           "orden 'lecciones')")
            # La memoria y las lecciones son del programa que se corre: si un archivo
            # traído con 'usar' tiene las suyas (alguien lo corrigió por su nombre), se avisa.
            traidos = {}  # archivo traído con 'usar' -> el primer agente que declara
            for s in programa:
                if s[0] == "agente" and (getattr(s[1], "archivo", None) or ruta) != ruta:
                    traidos.setdefault(s[1].archivo, s[2])
            for otro, agente in sorted(traidos.items()):
                if os.path.isfile(archivo_de(otro, "memoria.json")):
                    avisar(f"aviso: {os.path.basename(otro)} tiene su propia memoria "
                           f"({os.path.basename(archivo_de(otro, 'memoria.json'))}) y acá no "
                           "se usa: la memoria y las lecciones son del programa que se "
                           "corre. Para que a un agente le llegue una lección en este "
                           f"programa:  {como_se_llama()} corregir {para_pegar(ruta)} "
                           f'{agente} "la lección"')
            interprete.memoria, interprete.recordando = memoria, True

            def guardar_cuenta():
                """Después de cada consulta de verdad de un agente con frenos: la cuenta de
                hoy queda en el disco ya, por si cierran la ventana sin dejar terminar. Lo
                demás de la memoria queda como estaba al empezar; se guarda al final."""
                en_disco = json.loads(json.dumps(aprendido["leida"] or {}))
                for nombre, agente in interprete.agentes.items():
                    gasto = gasto_limpio(agente.gasto)
                    if gasto:
                        en_disco.setdefault(
                            nombre, {"estado": {}, "lecciones": []})["gasto"] = gasto
                if en_disco != aprendido["leida"] and not guardar_memoria(
                        archivo_memoria, os.path.basename(ruta), en_disco):
                    aprendido["leida"] = en_disco

            interprete.guardar_cuenta = guardar_cuenta
            interprete.avisar = lambda texto: avisar(f"aviso: {texto}")
            if usa_memoria(programa) or any(f["lecciones"] for f in memoria.values()):
                interprete.bitacora = []
            aprendido["abierta"] = True
        try:
            resultados = interprete.correr(programa, pruebas=orden == "probar")
        finally:  # también si el programa termina con un error, o lo cortan con Ctrl+C
            cerrar_memoria()
    except ErrorMate as e:
        # Primero lo que ya había fallado en los agentes: suele ser la causa del corte.
        for linea, texto in getattr(donde["interprete"], "errores_agentes_det", ()):
            reportar(linea, texto)
        if donde["interprete"] is not None:
            reportar(e.linea, donde["interprete"].con_camino(e.mensaje, e), e.familia)
        else:
            reportar(e.linea, e.mensaje, e.familia)
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
    sys.exit(main(registro=True))
