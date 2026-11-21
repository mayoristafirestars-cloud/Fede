#!/usr/bin/env python3
"""Mate: un lenguaje chico, en español, para escribir código claro y para que
los agentes se hablen entre ellos con mensajes que tienen contrato.

Uso:
    python3 mate.py correr    archivo.mate [--traza] [--sin-limite] [--depurar]
    python3 mate.py probar    archivo.mate
    python3 mate.py verificar archivo.mate
    python3 mate.py guia
    python3 mate.py ayuda
"""

import decimal
import difflib
import json
import math
import os
import re
import sys
import unicodedata
from collections import deque

VERSION = "0.2"

PALABRAS = {
    "sea", "var", "funcion", "devolver", "si", "sino", "mientras", "para", "en",
    "y", "o", "no", "verdadero", "falso", "nada", "mensaje", "agente", "estado",
    "al", "recibir", "como", "enviar", "preguntar", "responder", "fallar",
    "intentar", "falla", "asegurar", "prueba", "remitente", "yo", "crear", "usar",
    "romper", "continuar",
}

TIPOS_BASE = {"numero", "texto", "logico", "lista", "mapa", "agente", "cualquiera"}

MAX_MENSAJES = 100_000
MAX_PASOS = 10_000_000  # freno para los programas que nunca terminan
MAX_LARGO = 10_000_000  # tope de elementos de una lista o de letras de un texto
MAX_BITS = 14_000  # tope de tamaño de un entero (unas 4.200 cifras)

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
    "de_json": (1, 1, "de_json(texto)", "el valor que describe ese texto JSON"),
}


def lista_de_funciones(formato_de_renglon="- {ejemplo:<27} {que}"):
    """Un renglón por función incluida, para la guía y para el README."""
    return "\n".join(formato_de_renglon.format(ejemplo=ejemplo, que=que)
                     for _, _, ejemplo, que in FUNCIONES.values())


# Las funciones incluidas que hacen algo además de devolver un valor: pueden ir solas
# en un renglón. Las demás, sueltas, no sirven de nada y Mate lo avisa.
HACEN_ALGO = ("mostrar", "leer")

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
_RUTA_DE_WINDOWS = re.compile(r"(?<![A-Za-z])[A-Za-z]:\\(?!\\)")  # C:\ con una sola barra
DEVOLVER_SUELTO = "'devolver' solo va dentro de una función"
RESPONDER_SUELTO = "'responder' solo va dentro de 'al recibir' (o de una función del agente)"
SIN_MEMORIA = ("el programa se quedó sin memoria: está armando un texto, una lista o un "
               "número demasiado grande")


class ErrorMate(Exception):
    """Un error del programa escrito en Mate. 'clase' dice de qué tipo es:
    'falla' (lo común, se puede atajar con 'intentar'), 'asegurar' (un 'asegurar' que
    no se cumplió: dentro de una prueba no se ataja) o 'limite' (el freno: no se ataja)."""

    def __init__(self, mensaje, linea=None, clase="falla"):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.linea = linea
        self.clase = clase


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
    tokens.append(("eof", None, linea))
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
    def __init__(self, tokens):
        self.t = tokens
        self.i = 0
        # Para avisar de 'devolver' y 'responder' fuera de lugar antes de correr.
        self.en_funcion = self.en_recibir = self.en_agente = self.en_bucle = 0
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
        self.definidos.add(tk[1])
        return tk[1]

    def nombre_de_campo(self):
        """Un nombre de campo: también puede ser una palabra propia de Mate (estado, para)."""
        if self.es("kw"):
            return self.tomar()[1]
        return self.espera("id", que="un nombre de campo")[1]

    def condicion(self):
        """La condición de un 'si' o un 'mientras', con pistas para los errores comunes."""
        e = self.expr()
        self.pista_de_igual()
        tk = self.ver()
        if tk[0] == "id" and tk[1].lower() in ("entonces", "then"):
            raise ErrorMate(f"en Mate no va '{tk[1]}': después de la condición va "
                            "directamente la llave {", tk[2])
        return e

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

    def fin_de_sentencia(self, s):
        """'mostrar "hola"': un nombre suelto y algo más en el mismo renglón."""
        tk = self.ver()
        if (s[0] == "expr" and s[2][0] == "nombre" and tk[2] == self.linea_previa()
                and tk[0] in ("str", "num", "id")):
            raise ErrorMate(f"a '{s[2][2]}' le faltan los paréntesis: {s[2][2]}(...)", tk[2])

    # programa y sentencias
    def programa(self):
        cuerpo = []
        while not self.es("eof"):
            cuerpo.append(self.sentencia(nivel_superior=True))
            self.fin_de_sentencia(cuerpo[-1])
        return cuerpo

    def bloque(self):
        self.espera("op", "{")
        cuerpo = []
        while not self.es("op", "}"):
            if self.es("eof"):
                raise ErrorMate("falta cerrar un bloque con '}'", self.ver()[2])
            cuerpo.append(self.sentencia())
            self.fin_de_sentencia(cuerpo[-1])
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
                self.espera("kw", "en")
                return ("para", ln, nombre, self.expr(), self.vuelta())
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
                return ("prueba", ln, nombre, self.bloque())
            if val == "enviar":
                self.tomar()
                self.en_su_renglon(val, ln, "enviar Aviso { ... } a Agente")
                msg = self.expr()
                self.espera("id", "a", que="'a' (enviar Mensaje a Agente)")
                return ("enviar", ln, msg, self.expr())
            if val == "responder":
                if not (self.en_recibir or (self.en_funcion and self.en_agente)):
                    raise ErrorMate(RESPONDER_SUELTO, ln)
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
        if self.es("op", "{") and self.ver()[2] == self.linea_previa():
            self.tomar()
            while not self.es("op", "}"):
                campo = self.nombre_de_campo()
                self.espera("op", ":")
                tipo = (self.acepta("kw", "agente") or self.espera("id", que="un tipo"))[1]
                opcional = bool(self.acepta("op", "?"))
                campos.append((campo, tipo, opcional))
                if not self.acepta("op", ","):
                    break
            self.espera("op", "}")
        return ("mensaje", ln, nombre, campos)

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
                self.espera("kw", "recibir")
                tipo = self.espera("id", que="un tipo de mensaje")[1]
                var = self.nombre_nuevo() if self.acepta("kw", "como") else None
                self.en_recibir += 1
                try:
                    cuerpo = self.aparte()
                finally:
                    self.en_recibir -= 1
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
                    apodo = self.primario()
                if self.es("op", "{") and self.ver()[2] == self.linea_previa():
                    self.tomar()
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
        if _RUTA_DE_WINDOWS.search(crudo):
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


def analizar(fuente, ruta=None, _vistos=None):
    """Convierte el texto en un programa, incluyendo lo que traiga con 'usar'."""
    vistos = _vistos if _vistos is not None else set()
    if ruta:
        vistos.add(os.path.realpath(ruta))
    carpeta = os.path.dirname(os.path.abspath(ruta)) if ruta else os.getcwd()
    programa = []
    tokens = tokenizar(fuente, ruta)
    revisar_cierres(tokens, fuente)
    for s in Parser(tokens).programa():
        if s[0] != "usar":
            programa.append(s)
            continue
        otra = os.path.join(carpeta, s[2])
        try:
            otra = os.path.relpath(otra)
        except ValueError:  # en Windows, si está en otro disco
            pass
        if os.path.realpath(otra) in vistos:
            continue
        try:
            texto = leer_fuente(otra)
        except OSError:
            raise ErrorMate(f"no pude abrir '{s[2]}' (lo busqué en {carpeta})", s[1])
        except ErrorMate as e:
            e.linea = e.linea or s[1]
            raise
        # De un archivo usado se toman las declaraciones, no lo que ejecuta ni sus pruebas.
        programa.extend(x for x in analizar(texto, otra, vistos)
                        if x[0] in ("mensaje", "agente", "funcion", "sea"))
    return programa


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
        elif _es_nodo(n, "funcion", 5):
            anotar(n[2])
            for parametro in n[3]:
                anotar(parametro)
        elif _es_nodo(n, "intentar", 5):
            anotar(n[3])
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


def repetidos(nombres):
    """Los nombres que aparecen más de una vez, en el orden en que se repiten."""
    vistos, dobles = set(), []
    for nombre in nombres:
        if nombre in vistos and nombre not in dobles:
            dobles.append(nombre)
        vistos.add(nombre)
    return dobles


def verificar(programa):
    """Revisa los contratos de mensajes antes de correr. Devuelve [(linea, texto)]."""
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
    for s in programa:
        if s[0] == "mensaje":
            if s[2] in mensajes or s[2] in agentes:
                errores.append((s[1], f"'{s[2]}' ya está declarado"))
            mensajes[s[2]] = s
        elif s[0] == "agente":
            if s[2] in mensajes or s[2] in agentes:
                errores.append((s[1], f"'{s[2]}' ya está declarado"))
            agentes[s[2]] = [m[1] for m in s[4]]
            estados[s[2]] = {e[1]: e[2] for e in s[3]}
            declarados[s[2]] = s

    for s in mensajes.values():
        vistos = set()
        for campo, tipo, _ in s[3]:
            if campo in vistos:
                errores.append((s[1], f"{s[2]}: el campo '{campo}' está repetido"))
            vistos.add(campo)
            if tipo not in TIPOS_BASE and tipo not in mensajes:
                errores.append((s[1], con_pista(
                    f"{s[2]}.{campo}: no existe el tipo '{tipo}'", tipo,
                    sorted(TIPOS_BASE) + list(mensajes))))

    for s in programa:
        if s[0] == "agente":
            for k in repetidos(e[1] for e in s[3]):
                errores.append((next(e[0] for e in reversed(s[3]) if e[1] == k),
                                f"{s[2]}: el estado '{k}' está repetido"))
            vistos = set()
            for ln, tipo, _, _ in s[4]:
                if tipo not in mensajes:
                    errores.append((ln, f"{s[2]} recibe '{tipo}', que no es un mensaje declarado"))
                if tipo in vistos:
                    errores.append((ln, f"{s[2]} ya tiene un 'al recibir {tipo}'"))
                vistos.add(tipo)

    def agente_de(dest, ag):
        """A qué agente declarado le habla, si se puede saber antes de correr."""
        if _es_nodo(dest, "nombre", 3):
            if dest[2] in agentes:
                return dest[2]
            return copias.get(dest[2]) if copias.get(dest[2]) in agentes else None
        if _es_nodo(dest, "yo", 2):
            return ag
        return None

    def nunca_responde(agente, tipo):
        s = declarados[agente]
        cuerpo = next(m[3] for m in s[4] if m[1] == tipo)
        if _contiene(cuerpo, "responder", 3) or _contiene(cuerpo, "fallar", 3):
            return False
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
                    real = e[2] if e[0] == "ctor" else _LITERALES.get(e[0])
                    if real and tipo != "cualquiera" and real != tipo:
                        errores.append((ln, f"{nombre}.{k} es de tipo {tipo}, no {real}"))
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
            a_quien = agente_de(dest, ag)
            if a_quien and _es_nodo(msg, "ctor", 4) and msg[2] in mensajes:
                if msg[2] not in agentes[a_quien]:
                    errores.append((ln, f"{a_quien} no sabe recibir '{msg[2]}'"))
                elif n[0] == "preguntar" and nunca_responde(a_quien, msg[2]):
                    errores.append((ln, f"{a_quien} recibe '{msg[2]}' pero nunca responde: no "
                                        "se le puede preguntar (le falta un 'responder')"))
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


class Agente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.decl = None
        self.env = None
        self.manejadores = {}
        self.ocupado = False
        self.inicial = None  # el estado con el que nació (para empezar limpia cada prueba)


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
    def __init__(self, valor):
        self.valor = valor


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
    if type(a) is not type(b):
        return False
    if isinstance(a, list):
        return len(a) == len(b) and all(igual(x, y) for x, y in zip(a, b))
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(igual(v, b[k]) for k, v in a.items())
    if isinstance(a, Registro):
        return a.tipo == b.tipo and igual(a.campos, b.campos)
    return a == b


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
        return ErrorMate(f"'{texto}' no es un número")

    t = texto.strip()
    if not t:
        raise ErrorMate("un texto vacío no es un número")
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

    def __init__(self, padre=None, frontera=False, borde=False):
        Entorno.nacidos += 1
        self.serie = Entorno.nacidos
        self.vars = {}
        self.origen = {}  # de dónde salió cada nombre: sea, var, parametro, para, funcion...
        self.padre = padre
        self.frontera = frontera  # el estado de un agente: de acá para arriba no se escribe
        self.borde = borde  # donde empieza una función, un 'al recibir' o una prueba

    def definir(self, nombre, valor, mutable=False, origen=None):
        if nombre in self.vars:
            previo = self.origen.get(nombre)
            if previo == "nativa":
                raise ErrorMate(INCLUIDA.format(n=nombre))
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

    def no_tapar(self, nombre):
        """Un 'sea' o 'var' de un bloque de adentro (si, mientras, para, intentar) no
        puede repetir el nombre de una variable de más afuera: casi siempre se quiso
        cambiar esa variable, y con el 'sea' de más no cambia nada."""
        e = self
        while not e.borde and e.padre is not None:
            e = e.padre
            if nombre in e.vars and e.origen.get(nombre) in (
                    "sea", "var", "parametro", "para", "mensaje", "falla"):
                raise ErrorMate(
                    f"'{nombre}' ya existe afuera de este bloque. Si querés cambiarle el "
                    f"valor, sacá el 'sea' o el 'var': {nombre} = ... Si es otra cosa, "
                    "ponele otro nombre")
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
        mensaje = f"no existe '{nombre}'"
        if va_en_minuscula(nombre):
            return ErrorMate(f"{mensaje}: va en minúscula, '{nombre.lower()}'")
        completo = con_pista(mensaje, nombre, self.visibles())
        if al_asignar and completo == mensaje:
            completo += f". Para crear la variable escribí: var {nombre} = ..."
        return ErrorMate(completo)

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
        self.glob = Entorno()
        self.mensajes = {}
        self.agentes = {}
        self.decl_agentes = []
        self.copias = {}
        self.cola = deque()
        self.contexto = None  # (agente, remitente, tipo de mensaje) mientras se atiende uno
        self.entregados = 0
        self.pasos = 0
        self.max_pasos = MAX_PASOS  # None = sin tope
        self.linea_actual = None  # la última sentencia que se empezó a ejecutar
        self.errores_agentes = []  # textos: "V al recibir Pedido (línea 10): ..."
        self.errores_agentes_det = []  # lo mismo como (linea, texto), para decir el archivo
        self.errores_principal = []  # los del programa principal, antes de las pruebas
        self.vivos = []  # las copias nacidas con 'crear'
        self.en_prueba = False
        self.naciendo = 0  # agentes que están calculando su estado inicial
        self.tipos_estado = {}  # (agente, estado) -> tipo con el que arrancó
        self.archivo = None  # el archivo principal, para nombrar los otros en los errores
        self.detalle_pruebas = []  # por cada prueba, [(linea, texto)] de lo que falló
        self.llamadas = []  # nombres de las funciones que se están ejecutando
        self.entrada = por_teclado  # de dónde saca leer() lo que contesta la persona
        self.sin_teclado = False  # en las pruebas leer() usa la respuesta preparada
        self._nativas()

    # ── funciones incorporadas ──
    def _nativas(self):
        def nativa(nombre):
            minimo, maximo, ejemplo, _ = FUNCIONES[nombre]

            def deco(fn):
                def envuelta(args):
                    if len(args) < minimo or (maximo is not None and len(args) > maximo):
                        if minimo == maximo:
                            lleva = f"{minimo} valor" + ("" if minimo == 1 else "es")
                        elif maximo == minimo + 1:
                            lleva = f"{minimo} o {maximo} valores"
                        else:
                            lleva = f"entre {minimo} y {maximo} valores"
                        raise ErrorMate(f"{nombre}() lleva {lleva} y recibió {len(args)}. "
                                        f"Por ejemplo: {ejemplo}")
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

        nativa("mostrar")(lambda *xs: self.salida(" ".join(formato(a) for a in xs)))

        @nativa("largo")
        def _(x):
            if isinstance(x, (str, list, dict)):
                return len(x)
            raise ErrorMate(f"largo() no aplica a{'l valor nada' if x is None else ' ' + nombre_tipo(x)}")

        nativa("texto")(formato)
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
            raise ErrorMate(f"tiene() no aplica a{'l valor nada' if col is None else ' ' + nombre_tipo(col)}")

        nativa("claves")(lambda m: list(pedir(m, "mapa", "claves()")))
        nativa("valores")(lambda m: list(pedir(m, "mapa", "valores()").values()))
        nativa("agregar")(lambda l, x: pedir(l, "lista", "agregar()") + [x])

        @nativa("quitar")
        def _(col, x):
            if isinstance(col, dict):
                return {k: v for k, v in col.items() if k != x}
            if isinstance(col, list):
                return [y for y in col if not igual(x, y)]
            raise ErrorMate(f"quitar() no aplica a{'l valor nada' if col is None else ' ' + nombre_tipo(col)}")

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

        nativa("unir")(lambda l, sep: pedir(sep, "texto", "unir()").join(
            formato(x) for x in pedir(l, "lista", "unir()")))

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
                return json.dumps(self._a_json(v), ensure_ascii=False, allow_nan=False)
            except ValueError:  # inf, nan o un entero de miles de cifras
                raise ErrorMate("ese número no se puede pasar a JSON")

        def numero_invalido(_):
            raise ErrorMate("el JSON trae un número que no es válido")

        def decimal_de_json(t):
            f = float(t)
            return f if math.isfinite(f) else numero_invalido(t)

        @nativa("de_json")
        def _(t):
            try:
                return self._de_json(json.loads(
                    pedir(t, "texto", "de_json()"),
                    parse_constant=numero_invalido, parse_float=decimal_de_json))
            except json.JSONDecodeError as e:
                raise ErrorMate(json_invalido(t, e))
            except ValueError:  # un entero de miles de cifras
                numero_invalido(t)

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

    def _de_json(self, v):
        if isinstance(v, list):
            return [self._de_json(x) for x in v]
        if isinstance(v, dict):
            if set(v) == {"tipo", "campos"} and isinstance(v["tipo"], str) \
                    and v["tipo"] in self.mensajes and isinstance(v["campos"], dict):
                return self.construir(
                    v["tipo"], {k: self._de_json(x) for k, x in v["campos"].items()})
            if set(v) == {"agente"} and isinstance(v["agente"], str) \
                    and v["agente"] in self.agentes:
                return self.agentes[v["agente"]]
            return {k: self._de_json(x) for k, x in v.items()}
        return v

    # ── mensajes ──
    def cumple(self, valor, tipo):
        if tipo == "cualquiera":
            return True
        return nombre_tipo(valor) == tipo

    def construir(self, nombre, dados):
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
                    f"{nombre}.{campo} es de tipo {tipo} y recibió {tipo_claro(v)}")
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
        for s in programa:
            try:
                if s[0] == "funcion":
                    self.glob.definir(s[2], Funcion(s[2], s[3], s[4], self.glob),
                                      origen="funcion")
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
        apodo = None if n[3] is None else formato(self.ev(n[3], env))
        ag = Agente(f"{n[2]} {apodo}" if apodo is not None else f"{n[2]} nuevo")
        ag.decl = molde.decl
        self.instanciar(ag, dados, n[1])
        # Recién ahora gasta un número: un 'crear' rechazado no corre la numeración.
        self.copias[n[2]] = self.copias.get(n[2], 1) + 1
        if apodo is None:
            ag.nombre = f"{n[2]}#{self.copias[n[2]]}"
        self.vivos.append(ag)
        return ag

    def correr(self, programa, pruebas=False):
        """Ejecuta el programa. Con pruebas=True devuelve [(nombre, error|None)]."""
        # El análisis ya rechaza 'devolver' y 'responder' fuera de lugar; esto es la red.
        try:
            return self._correr(programa, pruebas)
        except _Retorno:
            raise ErrorMate(DEVOLVER_SUELTO, self.linea_actual)
        except _Respuesta:
            raise ErrorMate(RESPONDER_SUELTO, self.linea_actual)
        except (_Romper, _Continuar):
            raise ErrorMate("'romper' y 'continuar' solo van dentro de un 'mientras' o de "
                            "un 'para'", self.linea_actual)

    def _correr(self, programa, pruebas):
        self.sin_teclado = self.sin_teclado or pruebas
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
                fallas = []
                try:
                    self.bloque(s[3], Entorno(self.glob, borde=True), nuevo=False)
                    self.vaciar_cola()
                except ErrorMate as e:
                    fallas.append((e.linea, f"{self.donde(e.linea)}: {e.mensaje}"
                                   if e.linea else e.mensaje))
                # Además de lo que cortó la prueba, lo que falló en los agentes: suele
                # ser la causa.
                fallas += [(linea, texto) for (linea, _), texto
                           in zip(self.errores_agentes_det, self.errores_agentes)]
                self.detalle_pruebas.append(fallas)
                resultados.append((s[2], "\n".join(t for _, t in fallas) or None))
        finally:
            self.en_prueba = False
        return resultados

    def donde(self, linea):
        """'línea 7', o 'lib.mate, línea 7' si el renglón es de un archivo traído con usar."""
        archivo = getattr(linea, "archivo", None)
        if archivo and self.archivo and archivo != self.archivo:
            return f"{os.path.basename(archivo)}, línea {linea}"
        return f"línea {linea}"

    # ── agentes ──
    def vaciar_cola(self):
        while self.cola:
            rem, dest, msg = self.cola.popleft()
            try:
                self.entregar(rem, dest, msg, pregunta=False)
            except ErrorMate as e:
                if e.clase == "limite":  # el freno corta todo el programa, no un solo mensaje
                    raise
                donde = f" ({self.donde(e.linea)})" if e.linea else ""
                self.errores_agentes.append(
                    f"{dest.nombre} al recibir {msg.tipo}{donde}: {e.mensaje}")
                self.errores_agentes_det.append(
                    (e.linea or getattr(e, "renglon", None),
                     f"{dest.nombre} al recibir {msg.tipo}: {e.mensaje}"))

    def entregar(self, rem, dest, msg, pregunta):
        self.entregados += 1
        if self.entregados > MAX_MENSAJES:
            raise ErrorMate(
                f"se superaron {MAX_MENSAJES} mensajes: ¿los agentes entraron en bucle?",
                clase="limite")
        if self.traza:
            flecha = "pregunta a" if pregunta else "→"
            self.salida(f"  · {rem.nombre if rem else '(programa)'} {flecha} "
                        f"{dest.nombre}: {formato(msg)}")
        if msg.tipo not in dest.manejadores:
            raise ErrorMate(f"{dest.nombre} no sabe recibir '{msg.tipo}'")
        if dest.ocupado and dest.env is None:
            raise ErrorMate(f"{dest.nombre} todavía está armando su estado inicial y no "
                            "puede recibir mensajes")
        if dest.ocupado:
            raise ErrorMate(
                f"ciclo de preguntas: {dest.nombre} todavía está atendiendo otro mensaje")
        if dest.env is None:
            self.instanciar(dest)
        renglon, var, cuerpo = dest.manejadores[msg.tipo]
        env = Entorno(dest.env, borde=True)
        if var:
            env.definir(var, msg, origen="mensaje")
        previo, dest.ocupado = self.contexto, True
        self.contexto = (dest, rem, msg.tipo, env.serie)
        respondio, valor = False, None
        # Si falla, el agente vuelve a como estaba antes de recibir este mensaje.
        estado_previo = {k: list(v) for k, v in dest.env.vars.items()}
        en_cola, llamadas = len(self.cola), self.llamadas
        self.llamadas = []
        try:
            try:
                self.bloque(cuerpo, env, nuevo=False)
            except _Respuesta as r:
                respondio, valor = True, r.valor
            except _Retorno:
                pass
            # Responder mal (o no responder) también es una falla del que atiende.
            if pregunta and not respondio:
                raise ErrorMate(f"{dest.nombre} no respondió a '{msg.tipo}': el 'al recibir' "
                                "terminó sin llegar a un 'responder'")
            if not pregunta and respondio and rem is not None:
                # (si lo mandó el programa, no hay a quién contestar)
                if not isinstance(valor, Registro):
                    raise ErrorMate("a un 'enviar' solo se le responde con un mensaje")
                if valor.tipo not in rem.manejadores:
                    raise ErrorMate(
                        f"{dest.nombre} respondió {valor.tipo} a {rem.nombre}, pero "
                        f"{rem.nombre} no tiene 'al recibir {valor.tipo}'")
        except ErrorMate as e:
            if not e.linea and not pregunta:
                e.renglon = renglon  # para señalar al menos el 'al recibir' que atendía
            dest.env.vars = estado_previo
            nuevos = [self.cola.pop() for _ in range(len(self.cola) - en_cola)]
            self.cola.extend(m for m in reversed(nuevos) if m[0] is not dest)
            if e.clase == "asegurar":  # para quien le habló es una falla como cualquiera
                e.clase = "falla"
            raise
        finally:
            self.contexto, dest.ocupado, self.llamadas = previo, False, llamadas
        if pregunta:
            if self.traza:
                self.salida(f"  · {dest.nombre} responde a "
                            f"{rem.nombre if rem else '(programa)'}: {formato(valor, False)}")
            return valor
        if respondio and rem is not None:
            self.cola.append((dest, rem, valor))
        return None

    def destino(self, nodo, env):
        dest = self.ev(nodo, env)
        if not isinstance(dest, Agente):
            raise ErrorMate(f"el destino tiene que ser un agente, no {tipo_claro(dest)}")
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

    def ejecutar(self, s, env):
        self.linea_actual = s[1]
        self.contar_paso(s[1])
        try:
            self._ejecutar(s, env)
        except ErrorMate as e:
            e.linea = e.linea or s[1]
            raise
        except RecursionError:
            raise ErrorMate("demasiada recursión", s[1], clase="limite")
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
            env.definir(s[2], valor, mutable=s[4])
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
        elif clase == "para":
            col = self.ev(s[3], env)
            if not isinstance(col, (list, dict, str)):
                raise ErrorMate(f"no se puede recorrer {tipo_claro(col)}: 'para' recorre "
                                "listas, mapas y textos")
            for x in list(col):
                self.contar_paso(s[1])
                paso = Entorno(env)
                paso.definir(s[2], x, origen="para")
                try:
                    self.bloque(s[4], paso, nuevo=False)
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
            dest = self.destino(s[3], env)
            if msg.tipo not in dest.manejadores:
                raise ErrorMate(f"{dest.nombre} no sabe recibir '{msg.tipo}'", s[1])
            self.cola.append((self.contexto[0] if self.contexto else None, dest, msg))
        elif clase == "responder":
            if not self.contexto:
                raise ErrorMate(RESPONDER_SUELTO)
            valor = self.ev(s[2], env)
            if lleva_funcion(valor):
                raise ErrorMate("no se puede responder con una función: "
                                "las respuestas llevan datos", s[1])
            raise _Respuesta(valor)
        elif clase == "fallar":
            raise ErrorMate(formato(self.ev(s[2], env)), s[1])
        elif clase == "intentar":
            try:
                self.bloque(s[2], env)
            except ErrorMate as e:
                # El freno no se ataja nunca. Un 'asegurar' tampoco dentro de una prueba
                # (si no, pasaría en verde); al correr el programa es una falla más.
                if e.clase == "limite" or (e.clase == "asegurar" and self.en_prueba):
                    raise
                manejo = Entorno(env)
                if s[3]:
                    manejo.definir(s[3], e.mensaje, origen="falla")
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
                                f"{valor.nombre}(...)", e[1])
            pista = ""
            if e[0] == "neg":
                pista = (". Si era la continuación de la cuenta de arriba, dejá el '-' al "
                         "final de ese renglón")
            raise ErrorMate("este renglón calcula un valor y no hace nada con él: guardalo "
                            f"(sea x = ...), mostralo con mostrar(...) o borralo{pista}", e[1])
        f = self.ev(e[2], env)
        try:
            self.llamar(f, [self.ev(a, env) for a in e[3]])
        except ErrorMate as error:
            error.linea = error.linea or e[1]
            raise
        if isinstance(f, Nativa) and f.nombre not in HACEN_ALGO:
            if f.nombre in ("agregar", "quitar"):
                raise ErrorMate(
                    f"{f.nombre}() no cambia la lista: devuelve una nueva. Guardá el "
                    f"resultado: lista = {f.nombre}(lista, ...)", e[1])
            raise ErrorMate(f"{f.nombre}() devuelve un valor y este renglón no lo usa: "
                            f"guardalo (sea x = {f.nombre}(...)) o mostralo con mostrar(...)",
                            e[1])

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
        raise ErrorMate(f"la posición {i} está fuera de rango: {tiene}{pista}")

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
            return "".join(p if isinstance(p, str) else formato(self.ev(p, env)) for p in n[2])
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
            return self.llamar(self.ev(n[2], env), [self.ev(a, env) for a in n[3]])
        if clase == "indice":
            base, i = self.ev(n[2], env), self.ev(n[3], env)
            if isinstance(base, (list, str)):
                self.posicion(base, i)
                return base[i]
            if isinstance(base, dict):
                self.clave_de_mapa(i)
                if i not in base:
                    raise ErrorMate(no_esta(
                        f"el mapa no tiene la clave {formato(i, False)}", i, base))
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
                    f"{nombre_tipo(base)} no tiene un campo '{n[3]}'", n[3], campos))
            return campos[n[3]]
        if clase == "preguntar":
            msg = self.un_mensaje(n[2], env)
            dest = self.destino(n[3], env)
            if self.contexto is None and not self.naciendo:
                self.vaciar_cola()  # lo que el programa ya envió llega antes que la pregunta
            return self.entregar(self.contexto[0] if self.contexto else None, dest, msg, True)
        raise ErrorMate(f"expresión desconocida: {clase}")

    def binaria(self, op, a, b):
        if type(a) is int and type(b) is int:
            # Un entero que crece sin parar (x = x * x) cuelga la consola: se corta antes.
            if op == "*" and a.bit_length() + b.bit_length() > MAX_BITS:
                raise ErrorMate(DEMASIADO_GRANDE)
            if op in "+-" and max(a.bit_length(), b.bit_length()) >= MAX_BITS:
                raise ErrorMate(DEMASIADO_GRANDE)
        elif op == "+" and isinstance(a, (str, list)) and type(a) is type(b) \
                and len(a) + len(b) > MAX_LARGO:
            tope = f"{MAX_LARGO:,}".replace(",", ".")
            raise ErrorMate(f"el texto quedaría demasiado largo (más de {tope} letras)"
                            if isinstance(a, str) else
                            f"la lista quedaría demasiado larga (más de {tope} elementos)")
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
            return {"<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}[op]
        if op == "+" and (ambos_num or (type(a) is type(b) and isinstance(a, (str, list)))):
            return a + b
        if ambos_num:
            if op == "-":
                return a - b
            if op == "*":
                return a * b
            if b == 0:
                raise ErrorMate("división por cero")
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

    def llamar(self, f, args):
        if isinstance(f, Nativa):
            return f.fn(args)
        if not isinstance(f, Funcion):
            raise ErrorMate(f"{tipo_claro(f)} no es una función: no se le pueden poner "
                            "paréntesis")
        if len(args) != len(f.params):
            raise ErrorMate(
                f"{f.nombre}() espera {len(f.params)} argumento(s) y recibió {len(args)}")
        env = Entorno(f.env, borde=True)
        for p, a in zip(f.params, args):
            env.definir(p, a, origen="parametro")
        self.llamadas.append(f.nombre)
        try:
            self.bloque(f.cuerpo, env, nuevo=False)
        except _Retorno as r:
            return r.valor
        finally:
            self.llamadas.pop()
        return None


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
- Dentro de un texto, {{...}} se calcula: "Total: {{precio * 2}}". Adentro de las llaves no se
  puede haber otros textos: "Sale {{precios["yerba"]}}". \n es salto de renglón, \{{ una
  llave de verdad y \\ una barra (las rutas de Windows van con / o con doble barra).

VARIABLES
- sea x = 1        fijo, no cambia más
- var y = 0        puede cambiar:   y = y + 1     y += 1     y -= 1
- y.campo = 5 y lista[0] = 5 cambian una parte (la variable tiene que ser 'var').
- Copiar un valor lo copia entero: cambiar la copia no toca el original.
- Un 'sea' o 'var' dentro de un bloque no puede repetir el nombre de una variable de afuera.
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
- romper sale del bucle; continuar salta a la vuelta siguiente.
- funcion nombre(a, b) {{ devolver a + b }}        'devolver' solo, sin valor, devuelve nada
- fallar "motivo"                                 corta con un error
- intentar {{ ... }} si falla e {{ ... }}             e es el texto del error (el 'e' es opcional)

FUNCIONES INCLUIDAS (no hay otras)
{funciones}
- agregar, quitar, ordenar y porcion devuelven una copia NUEVA, no cambian la original:
  lista = agregar(lista, x)
- Una función incluida suelta en un renglón (salvo mostrar y leer) es un error: hay que usar
  lo que devuelve.

AGENTES Y MENSAJES
- mensaje Pedido {{ producto: texto, cantidad: numero, nota: texto? }}     (? = opcional)
  Tipos: numero texto logico lista mapa agente cualquiera, u otro mensaje.
- Crear un mensaje: Pedido {{ producto: "yerba", cantidad: 2 }}     Sin campos: Ping {{}}
- agente Nombre {{
      estado contador = 0                  memoria privada; solo él la cambia
      al recibir Pedido como p {{ ... }}     uno por cada mensaje que entiende
      funcion ayuda(x) {{ ... }}             funciones propias
  }}
- responder valor        contesta y termina (solo dentro de 'al recibir')
- enviar Mensaje {{ ... }} a Agente              lo deja en la cola y sigue
- sea r = preguntar Mensaje {{ ... }} a Agente   espera la respuesta; si el otro falla, falla acá
- remitente es quien mandó el mensaje; yo es el agente que está atendiendo.
- sea otro = crear Vendedor llamado "Norte" {{ contador: 5 }}     otra copia, con su estado
- Un agente no puede cambiar variables de afuera ni el estado de otro. Los mensajes llevan
  datos, nunca funciones.
- usar "otro.mate" trae los mensajes, agentes, funciones y 'sea' de otro archivo.

PRUEBAS
- prueba "nombre" {{ asegurar total == 10 }}        asegurar cond, "mensaje si falla"
- Van en el nivel superior y corren con la orden 'probar'. Cada una empieza limpia.

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
        "  verificar archivo.mate   revisa el programa sin correrlo",
        "  guia                     una página con todo Mate, para pegarle a una IA",
        "  ayuda                    muestra esta ayuda",
        "",
        "Opciones:",
        "  --traza       muestra la conversación entre agentes, mensaje por mensaje",
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


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    for flujo in (sys.stdout, sys.stderr):
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
    opciones, args = set(), []
    for a in argv:
        if a.lower() in alias:
            opciones.add(alias[a.lower()])
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
    if "--ayuda" in opciones or (args and args[0].lower() == "ayuda"):
        print(texto_de_ayuda())
        return 0
    if not args:
        print(texto_de_ayuda())
        return 2
    if args[0].lower() in ("guia", "guía"):
        print(texto_de_guia())
        return 0

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
        parecidas = difflib.get_close_matches(orden, ORDENES + ("ayuda", "guia"), 1)
        avisar(f"no conozco la orden '{args[0]}'" + (
            f", ¿quisiste decir '{parecidas[0]}'?" if parecidas
            else ". Las órdenes son: correr, probar, verificar, guia y ayuda"))
        return 2
    if not archivos:
        avisar(f"a '{orden}' le falta el archivo, por ejemplo: {orden} hola.mate")
        return 2
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
        archivo = getattr(linea, "archivo", None) or ruta
        avisar(f"{archivo}:{linea}: error: {texto}" if linea else f"{archivo}: error: {texto}")
        renglon = renglon_de(archivo, linea) if linea else None
        if renglon and (archivo, renglon) != mostrado.get("ultimo"):
            avisar(renglon)  # el mismo renglón no se repite si trae varios errores
        mostrado["ultimo"] = (archivo, renglon)

    if simbolo("·→", ""):
        salida = print
    else:  # consola que no conoce esos símbolos: la traza se escribe con letras comunes
        def salida(texto):
            print(texto.replace("→", "->").replace("·", "-"))

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
        interprete = donde["interprete"] = Interprete(salida=salida, traza="--traza" in opciones)
        interprete.archivo = ruta
        if "--sin-limite" in opciones:
            interprete.max_pasos = None
        resultados = interprete.correr(programa, pruebas=orden == "probar")
    except ErrorMate as e:
        # Primero lo que ya había fallado en los agentes: suele ser la causa del corte.
        for linea, texto in getattr(donde["interprete"], "errores_agentes_det", ()):
            reportar(linea, texto)
        reportar(e.linea, e.mensaje)
        avisar_pendientes(donde["interprete"], avisar)
        return 1

    if orden == "probar":
        if interprete.errores_principal:
            avisar("errores al correr el programa (antes de las pruebas):")
            for linea, texto in interprete.errores_principal:
                reportar(linea, texto)
        fallidas = 0
        bien, mal = simbolo("✓", "OK"), simbolo("✗", "FALLA")
        for (nombre, error), fallas in zip(resultados, interprete.detalle_pruebas):
            print(f"  {mal if error else bien} {nombre}")
            for linea, texto in fallas:
                for parte in texto.split("\n"):
                    print(f"      {parte}")
                # debajo, el renglón señalado (como hace 'correr')
                renglon = renglon_de(getattr(linea, "archivo", None) or ruta, linea) \
                    if linea else None
                if renglon:
                    print(f"      {renglon}")
            fallidas += bool(error)
        print(f"{len(resultados) - fallidas} de {len(resultados)} pruebas pasaron")
        return 1 if fallidas or interprete.errores_principal else 0
    for linea, texto in interprete.errores_agentes_det:
        reportar(linea, texto)
    return 1 if interprete.errores_agentes else 0


if __name__ == "__main__":
    sys.exit(main())
