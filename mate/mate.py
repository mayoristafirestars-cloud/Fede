#!/usr/bin/env python3
"""Mate: un lenguaje chico, en español, para escribir código claro y para que
los agentes se hablen entre ellos con mensajes que tienen contrato.

Uso:
    python3 mate.py correr    archivo.mate [--traza] [--sin-limite] [--depurar]
    python3 mate.py probar    archivo.mate
    python3 mate.py verificar archivo.mate
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
}

TIPOS_BASE = {"numero", "texto", "logico", "lista", "mapa", "agente", "cualquiera"}

MAX_MENSAJES = 100_000
MAX_PASOS = 10_000_000  # freno para los programas que nunca terminan

ORDENES = ("correr", "probar", "verificar")
OPCIONES = ("--traza", "--depurar", "--sin-limite", "--version", "--ayuda")

COMPARADORES = ("==", "!=", "<", "<=", ">", ">=")

# Palabras de otros lenguajes, o con tilde, y cómo se escriben en Mate. No se aceptan
# como sinónimos: solo sirven para explicar el error.
PISTAS = {
    "print": "mostrar", "imprimir": "mostrar", "if": "si", "else": "sino",
    "while": "mientras", "for": "para", "let": "sea", "const": "sea",
    "true": "verdadero", "false": "falso", "null": "nada", "none": "nada",
    "return": "devolver", "function": "funcion", "def": "funcion",
    "and": "y", "or": "o", "not": "no", "to": "a",
    "break": "romper (todavía no existe en Mate)",
    "función": "funcion", "sinó": "sino", "número": "numero", "lógico": "logico",
    "mayúsculas": "mayusculas", "minúsculas": "minusculas",
}

INCLUIDA = ("'{n}' es una función incluida de Mate; elegí otro nombre "
            "(por ejemplo 'mi_{n}')")
DEMASIADO_GRANDE = "el resultado es demasiado grande para calcularlo"
NO_ASIGNABLE = ("solo se puede asignar a una variable o a una parte de una variable "
                "(x, x.campo, x[0])")
DEVOLVER_SUELTO = "'devolver' solo va dentro de una función"
RESPONDER_SUELTO = "'responder' solo va dentro de 'al recibir' (o de una función del agente)"


class ErrorMate(Exception):
    """Un error del programa escrito en Mate. 'clase' dice de qué tipo es:
    'falla' (lo común, se puede atajar con 'intentar'), 'asegurar' (un 'asegurar' que
    no se cumplió) o 'limite' (el freno: no se ataja)."""

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
    (?P<ws>[ \t\r\u00a0\u2009\u202f\u200b\ufeff]+|\#[^\n]*)
  | (?P<nl>\n)
  | (?P<num>\d+(?:\.\d+)?)
  | (?P<str>"(?:\\.|[^"\\\n])*")
  | (?P<curva>[“”„](?:\\.|[^"“”„\\\n])*[“”„"])
  | (?P<id>[^\W\d]\w*)
  | (?P<op>==|!=|<=|>=|[-+*/%<>=(){}\[\],.:?])
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


def tokenizar(fuente, archivo=None):
    tokens, pos, linea = [], 0, Linea(1, archivo)
    while pos < len(fuente):
        m = _TOKEN.match(fuente, pos)
        if not m:
            c = fuente[pos]
            raise ErrorMate(_PISTAS_DE_CARACTER.get(c, f"carácter inesperado: '{c}'"), linea)
        pos = m.end()
        clase, txt = m.lastgroup, m.group()
        if clase == "nl":
            linea = Linea(linea + 1, archivo)
        elif clase == "num":
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
            if txt not in PALABRAS and PISTAS.get(txt.lower()) in PALABRAS:
                # 'if', 'función'...: se explica, salvo que sea el nombre de un campo
                tras_punto = bool(tokens) and tokens[-1][:2] == ("op", ".")
                if not tras_punto and not fuente[pos:].lstrip(" \t").startswith(":"):
                    raise ErrorMate(pista_de(txt), linea)
            tokens.append(("kw" if txt in PALABRAS else "id", txt, linea))
        elif clase == "op":
            if txt == "/" and fuente.startswith("/", pos):
                raise ErrorMate("los comentarios empiezan con #", linea)
            tokens.append(("op", txt, linea))
    tokens.append(("eof", None, linea))
    return tokens


# ───────────────────────────── Parser ─────────────────────────────


class Parser:
    def __init__(self, tokens):
        self.t = tokens
        self.i = 0
        # Para avisar de 'devolver' y 'responder' fuera de lugar antes de correr.
        self.en_funcion = self.en_recibir = self.en_agente = 0

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
        visto = "el final del archivo" if tk[0] == "eof" else f"'{tk[1]}'"
        raise ErrorMate(f"esperaba {que or repr(valor)} y encontré {visto}", tk[2])

    def nombre_nuevo(self, que="un nombre"):
        """El nombre de una variable, función o parámetro que se está creando."""
        tk = self.espera("id", que=que)
        if tk[1] in incluidas():
            raise ErrorMate(INCLUIDA.format(n=tk[1]), tk[2])
        return tk[1]

    def nombre_de_campo(self):
        """Un nombre de campo: también puede ser una palabra propia de Mate (estado, para)."""
        if self.es("kw"):
            return self.tomar()[1]
        return self.espera("id", que="un nombre de campo")[1]

    def condicion(self):
        """La condición de un 'si' o un 'mientras', con pistas para los errores comunes."""
        e = self.expr()
        tk = self.ver()
        if tk[:2] == ("op", "="):
            raise ErrorMate("para comparar se usa '==' (un solo '=' es para asignar)", tk[2])
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

    # programa y sentencias
    def programa(self):
        cuerpo = []
        while not self.es("eof"):
            cuerpo.append(self.sentencia(nivel_superior=True))
        return cuerpo

    def bloque(self):
        self.espera("op", "{")
        cuerpo = []
        while not self.es("op", "}"):
            if self.es("eof"):
                raise ErrorMate("falta cerrar un bloque con '}'", self.ver()[2])
            cuerpo.append(self.sentencia())
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
                return ("mientras", ln, self.condicion(), self.bloque())
            if val == "para":
                self.tomar()
                nombre = self.nombre_nuevo()
                self.espera("kw", "en")
                return ("para", ln, nombre, self.expr(), self.bloque())
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
                msg = self.expr()
                self.espera("id", "a", que="'a' (enviar Mensaje a Agente)")
                return ("enviar", ln, msg, self.expr())
            if val == "responder":
                if not (self.en_recibir or (self.en_funcion and self.en_agente)):
                    raise ErrorMate(RESPONDER_SUELTO, ln)
                self.tomar()
                return ("responder", ln, self.expr())
            if val == "fallar":
                self.tomar()
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
                cond = self.expr()
                msg = self.expr() if self.acepta("op", ",") else None
                return ("asegurar", ln, cond, msg)
        if (tipo == "id" and va_en_minuscula(val)
                and not (self.es("op", d=1) and self.ver(1)[1] in ("=", ".", "["))):
            raise ErrorMate(f"'{val}' va en minúscula: '{val.lower()}'", ln)
        e = self.expr()
        if self.acepta("op", "="):
            if not self.asignable(e):
                raise ErrorMate(NO_ASIGNABLE, ln)
            return ("asignar", ln, e, self.expr())
        return ("expr", ln, e)

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
            cuerpo = self.bloque()
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
                    cuerpo = self.bloque()
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
        while self.es("kw", "o"):
            ln = self.tomar()[2]
            self.tras_y_o("o")
            izq = ("o", ln, izq, self.expr_y())
        return izq

    def expr_y(self):
        izq = self.expr_no()
        while self.es("kw", "y"):
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
        if self.es_comparador():
            _, op, ln = self.tomar()
            izq = ("bin", ln, op, izq, self.suma())
            if self.es_comparador():
                raise ErrorMate(
                    "las comparaciones no se encadenan: escribí 1 < x y x < 10", self.ver()[2])
        return izq

    def suma(self):
        izq = self.producto()
        while self.ver()[0] == "op" and self.ver()[1] in ("+", "-"):
            _, op, ln = self.tomar()
            izq = ("bin", ln, op, izq, self.producto())
        return izq

    def producto(self):
        izq = self.unario()
        while self.ver()[0] == "op" and self.ver()[1] in ("*", "/", "%"):
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
                idx = self.expr()
                self.espera("op", "]")
                e = ("indice", tk[2], e, idx)
            elif self.es("op", "."):
                self.tomar()
                e = ("campo", tk[2], e, self.nombre_de_campo())
            else:
                return e

    def lista_hasta(self, cierre):
        items = []
        while not self.es("op", cierre):
            items.append(self.expr())
            if not self.acepta("op", ","):
                break
        self.espera("op", cierre)
        return items

    def pares(self, claves_texto):
        pares = []
        while not self.es("op", "}"):
            tk = self.tomar()
            if not (tk[0] == "id" or (claves_texto and tk[0] == "str")
                    or (tk[0] == "kw" and self.es("op", ":"))):
                raise ErrorMate("esperaba un nombre de campo", tk[2])
            self.espera("op", ":")
            pares.append((tk[1], self.expr()))
            if not self.acepta("op", ","):
                break
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
            return ("nombre", ln, val)
        if tipo == "op":
            if val == "(":
                e = self.expr()
                self.espera("op", ")")
                return e
            if val == "[":
                return ("lista", ln, self.lista_hasta("]"))
            if val == "{":
                return ("mapa", ln, self.pares(True))
        visto = "el final del archivo" if tipo == "eof" else f"'{val}'"
        raise ErrorMate(f"no esperaba {visto} acá", ln)

    def texto(self, crudo, ln):
        """Texto con escapes e interpolación: "Total: {precio * 2}"."""
        partes, actual, i = [], [], 0
        escapes = {"n": "\n", "t": "\t"}
        while i < len(crudo):
            c = crudo[i]
            if c == "\\" and i + 1 < len(crudo):
                actual.append(escapes.get(crudo[i + 1], crudo[i + 1]))
                i += 2
            elif c == "{":
                fin, prof = i + 1, 1
                while fin < len(crudo) and prof:
                    prof += {"{": 1, "}": -1}.get(crudo[fin], 0)
                    fin += 1
                if prof:
                    raise ErrorMate("falta '}' en el texto (usá \\{ para una llave literal)", ln)
                if actual:
                    partes.append("".join(actual))
                    actual = []
                try:
                    sub = Parser([(t, v, ln) for t, v, _ in tokenizar(crudo[i + 1 : fin - 1])])
                    partes.append(sub.expr())
                    sub.espera("eof", que="el fin de la expresión")
                except ErrorMate as e:
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
    for s in Parser(tokenizar(fuente, ruta)).programa():
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


def verificar(programa):
    """Revisa los contratos de mensajes antes de correr. Devuelve [(linea, texto)]."""
    errores = []
    mensajes, agentes, estados = {}, {}, {}
    for s in programa:
        if s[0] == "mensaje":
            if s[2] in mensajes or s[2] in agentes:
                errores.append((s[1], f"'{s[2]}' ya está declarado"))
            mensajes[s[2]] = s
        elif s[0] == "agente":
            if s[2] in mensajes or s[2] in agentes:
                errores.append((s[1], f"'{s[2]}' ya está declarado"))
            agentes[s[2]] = [m[1] for m in s[4]]
            estados[s[2]] = {e[1] for e in s[3]}

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
            vistos = set()
            for ln, tipo, _, _ in s[4]:
                if tipo not in mensajes:
                    errores.append((ln, f"{s[2]} recibe '{tipo}', que no es un mensaje declarado"))
                if tipo in vistos:
                    errores.append((ln, f"{s[2]} ya tiene un 'al recibir {tipo}'"))
                vistos.add(tipo)

    def visitar(n):
        if isinstance(n, list):
            for x in n:
                visitar(x)
            return
        if not isinstance(n, tuple):
            return
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
                for k, _ in pares:
                    if k not in estados[nombre]:
                        errores.append((ln, f"{nombre} no tiene un estado '{k}'"))
        elif len(n) == 4 and n[0] in ("enviar", "preguntar"):
            _, ln, msg, dest = n
            if (isinstance(msg, tuple) and msg[0] == "ctor" and isinstance(dest, tuple)
                    and dest[0] == "nombre" and dest[2] in agentes
                    and msg[2] in mensajes and msg[2] not in agentes[dest[2]]):
                errores.append((ln, f"{dest[2]} no sabe recibir '{msg[2]}'"))
        for x in n:
            visitar(x)

    visitar(programa)
    return sorted(set(errores))


# ───────────────────────────── Valores ─────────────────────────────


class Registro:
    """Un mensaje ya construido y validado. Inmutable."""

    def __init__(self, tipo, campos):
        self.tipo = tipo
        self.campos = campos

    def __eq__(self, otro):
        return isinstance(otro, Registro) and self.tipo == otro.tipo and self.campos == otro.campos

    __hash__ = None


class Agente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.decl = None
        self.env = None
        self.manejadores = {}
        self.ocupado = False


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


def igual(a, b):
    if es_num(a) and es_num(b):
        return a == b
    return type(a) is type(b) and a == b


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
    if -d.as_tuple().exponent <= decimales:
        return d  # ya tiene esa cantidad de decimales o menos
    contexto = decimal.Context(prec=max(d.adjusted(), 0) + decimales + 10)
    return d.quantize(decimal.Decimal(1).scaleb(-decimales, contexto),
                      rounding=decimal.ROUND_HALF_UP, context=contexto)


_NUMERO_AR = re.compile(r"[+-]?[0-9]{1,3}(\.[0-9]{3})+,[0-9]+")       # 1.234,50
_NUMERO_COMA = re.compile(r"[+-]?[0-9]+,[0-9]+")                      # 3,5
_NUMERO_COMUN = re.compile(r"[+-]?[0-9]+(\.[0-9]+)?")                 # 12 y 3.5
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


_INCLUIDAS = []


def incluidas():
    """Los nombres de las funciones incluidas (mostrar, texto, pesos...)."""
    if not _INCLUIDAS:
        _INCLUIDAS.append(frozenset(Interprete(salida=lambda _: None).glob.vars))
    return _INCLUIDAS[0]


class Entorno:
    def __init__(self, padre=None, frontera=False):
        self.vars = {}
        self.origen = {}  # de dónde salió cada nombre: sea, var, parametro, para, funcion...
        self.padre = padre
        self.frontera = frontera  # el estado de un agente: de acá para arriba no se escribe

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
        self.errores_agentes = []
        self._nativas()

    # ── funciones incorporadas ──
    def _nativas(self):
        def nativa(nombre, minimo, maximo=None):
            maximo = minimo if maximo is None else maximo

            def deco(fn):
                def envuelta(args):
                    if not minimo <= len(args) <= maximo:
                        if minimo == maximo:
                            lleva = f"{minimo} valor" + ("" if minimo == 1 else "es")
                        elif maximo == minimo + 1:
                            lleva = f"{minimo} o {maximo} valores"
                        else:
                            lleva = f"entre {minimo} y {maximo} valores"
                        raise ErrorMate(f"{nombre}() lleva {lleva} y recibió {len(args)}")
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
            except (TypeError, ValueError, ArithmeticError, KeyError, IndexError,
                    AttributeError):
                raise ErrorMate(f"{nombre}(): no pude hacer eso con esos valores")
            if type(r) is float and not math.isfinite(r):
                raise ErrorMate(f"{nombre}(): {DEMASIADO_GRANDE}")
            return r

        def pedir(v, tipo, donde):
            if nombre_tipo(v) != tipo:
                raise ErrorMate(f"{donde} espera {tipo} y recibió {nombre_tipo(v)}")
            return v

        self.glob.definir("mostrar", Nativa("mostrar", lambda args: protegida(
            "mostrar", lambda *xs: self.salida(" ".join(formato(a) for a in xs)), args)),
            origen="nativa")

        @nativa("largo", 1)
        def _(x):
            if isinstance(x, (str, list, dict)):
                return len(x)
            raise ErrorMate(f"largo() no aplica a {nombre_tipo(x)}")

        nativa("texto", 1)(formato)
        nativa("tipo", 1)(nombre_tipo)

        @nativa("numero", 1)
        def _(x):
            return x if es_num(x) else numero_de_texto(pedir(x, "texto", "numero()"))

        @nativa("tiene", 2)
        def _(col, x):
            if isinstance(col, dict):  # las claves son textos: otra cosa no puede estar
                return isinstance(x, str) and x in col
            if isinstance(col, list):
                return any(igual(x, y) for y in col)
            if isinstance(col, str) and isinstance(x, str):
                return x in col
            raise ErrorMate(f"tiene() no aplica a {nombre_tipo(col)}")

        nativa("claves", 1)(lambda m: list(pedir(m, "mapa", "claves()")))
        nativa("valores", 1)(lambda m: list(pedir(m, "mapa", "valores()").values()))
        nativa("agregar", 2)(lambda l, x: pedir(l, "lista", "agregar()") + [x])

        @nativa("quitar", 2)
        def _(col, x):
            if isinstance(col, dict):
                return {k: v for k, v in col.items() if k != x}
            if isinstance(col, list):
                return [y for y in col if not igual(x, y)]
            raise ErrorMate(f"quitar() no aplica a {nombre_tipo(col)}")

        @nativa("rango", 1, 2)
        def _(a, b=None):
            ini, fin = (0, a) if b is None else (a, b)
            if type(ini) is not int or type(fin) is not int:
                raise ErrorMate("rango() espera números enteros")
            return list(range(ini, fin))

        @nativa("sumar", 1)
        def _(l):
            if not all(es_num(x) for x in pedir(l, "lista", "sumar()")):
                raise ErrorMate("sumar() espera una lista de números")
            return sum(l)

        @nativa("ordenar", 1)
        def _(l):
            try:
                return sorted(pedir(l, "lista", "ordenar()"))
            except TypeError:
                raise ErrorMate("ordenar() espera elementos comparables entre sí")

        @nativa("redondear", 1, 2)
        def _(x, n=0):
            pedir(x, "numero", "redondear()")
            if type(n) is not int or n < 0:
                raise ErrorMate("redondear() espera una cantidad entera de decimales, "
                                "por ejemplo redondear(3.14159, 2)")
            if not math.isfinite(x):
                raise ErrorMate("redondear() no puede con un número infinito")
            if type(x) is int:
                return x
            r = redondeo(x, n)  # el medio va hacia arriba: redondear(2.5) da 3
            return int(r) if r == r.to_integral_value() else float(r)

        @nativa("pesos", 1, 2)
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

        nativa("unir", 2)(lambda l, sep: pedir(sep, "texto", "unir()").join(
            formato(x) for x in pedir(l, "lista", "unir()")))

        @nativa("partir", 2)
        def _(t, sep):
            pedir(t, "texto", "partir()")
            if pedir(sep, "texto", "partir()") == "":
                return list(t)  # sin separador: letra por letra
            return t.split(sep)

        nativa("mayusculas", 1)(lambda t: pedir(t, "texto", "mayusculas()").upper())
        nativa("minusculas", 1)(lambda t: pedir(t, "texto", "minusculas()").lower())

        @nativa("a_json", 1)
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

        @nativa("de_json", 1)
        def _(t):
            try:
                return self._de_json(json.loads(
                    pedir(t, "texto", "de_json()"),
                    parse_constant=numero_invalido, parse_float=decimal_de_json))
            except json.JSONDecodeError as e:
                raise ErrorMate(f"JSON inválido: {e.msg}")
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
            if not (self.cumple(v, tipo) or (opcional and v is None)):
                raise ErrorMate(
                    f"{nombre}.{campo} es de tipo {tipo} y recibió {nombre_tipo(v)}")
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
                    self.agentes[s[2]] = ag
                    self.decl_agentes.append(s)
                    self.glob.definir(s[2], ag, origen="agente")
            except ErrorMate as e:
                e.linea = e.linea or s[1]
                raise

    def instanciar(self, ag, dados=None):
        """Deja al agente recién nacido: estado inicial (o el que le den) y sin pendientes."""
        s, dados = ag.decl, dados or {}
        ag.env = Entorno(self.glob, frontera=True)
        ag.ocupado = False
        ag.manejadores = {tipo: (var, cuerpo) for _, tipo, var, cuerpo in s[4]}
        for f in s[5]:
            ag.env.definir(f[2], Funcion(f[2], f[3], f[4], ag.env), origen="funcion")
        for ln, nombre, e in s[3]:
            try:
                valor = dados[nombre] if nombre in dados else self.ev(e, ag.env)
                ag.env.definir(nombre, valor, mutable=True)
            except ErrorMate as err:
                err.linea = err.linea or ln
                raise

    def reiniciar_agentes(self):
        self.copias = {}
        for s in self.decl_agentes:
            self.instanciar(self.agentes[s[2]])
        self.cola.clear()

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
        self.copias[n[2]] = self.copias.get(n[2], 1) + 1
        if n[3] is not None:
            nombre = f"{n[2]} {formato(self.ev(n[3], env))}"
        else:
            nombre = f"{n[2]}#{self.copias[n[2]]}"
        ag = Agente(nombre)
        ag.decl = molde.decl
        self.instanciar(ag, dados)
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

    def _correr(self, programa, pruebas):
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
        resultados = []
        for s in programa:
            if s[0] != "prueba":
                continue
            self.reiniciar_agentes()
            self.errores_agentes = []
            self.pasos = 0
            error = None
            try:
                self.bloque(s[3], Entorno(self.glob))
                self.vaciar_cola()
                if self.errores_agentes:
                    error = self.errores_agentes[0]
            except ErrorMate as e:
                error = f"línea {e.linea}: {e.mensaje}" if e.linea else e.mensaje
            resultados.append((s[2], error))
        return resultados

    # ── agentes ──
    def vaciar_cola(self):
        while self.cola:
            rem, dest, msg = self.cola.popleft()
            try:
                self.entregar(rem, dest, msg, pregunta=False)
            except ErrorMate as e:
                if e.clase == "limite":  # el freno corta todo el programa, no un solo mensaje
                    raise
                donde = f" (línea {e.linea})" if e.linea else ""
                self.errores_agentes.append(
                    f"{dest.nombre} al recibir {msg.tipo}{donde}: {e.mensaje}")

    def entregar(self, rem, dest, msg, pregunta):
        self.entregados += 1
        if self.entregados > MAX_MENSAJES:
            raise ErrorMate(f"se superaron {MAX_MENSAJES} mensajes: ¿los agentes entraron en bucle?")
        if self.traza:
            flecha = "pregunta a" if pregunta else "→"
            self.salida(f"  · {rem.nombre if rem else '(programa)'} {flecha} "
                        f"{dest.nombre}: {formato(msg)}")
        if dest.env is None:
            self.instanciar(dest)
        if msg.tipo not in dest.manejadores:
            raise ErrorMate(f"{dest.nombre} no sabe recibir '{msg.tipo}'")
        if dest.ocupado:
            raise ErrorMate(
                f"ciclo de preguntas: {dest.nombre} todavía está atendiendo otro mensaje")
        var, cuerpo = dest.manejadores[msg.tipo]
        env = Entorno(dest.env)
        if var:
            env.definir(var, msg, origen="mensaje")
        previo, self.contexto, dest.ocupado = self.contexto, (dest, rem, msg.tipo), True
        respondio, valor = False, None
        try:
            self.bloque(cuerpo, env, nuevo=False)
        except _Respuesta as r:
            respondio, valor = True, r.valor
        except _Retorno:
            pass
        finally:
            self.contexto, dest.ocupado = previo, False
        if pregunta:
            if not respondio:
                raise ErrorMate(f"{dest.nombre} no respondió a '{msg.tipo}'")
            if self.traza:
                self.salida(f"  · {dest.nombre} responde a "
                            f"{rem.nombre if rem else '(programa)'}: {formato(valor, False)}")
            return valor
        if respondio and rem is not None:  # si lo mandó el programa, no hay a quién contestar
            if not isinstance(valor, Registro):
                raise ErrorMate("a un 'enviar' solo se le responde con un mensaje")
            self.cola.append((dest, rem, valor))
        return None

    def destino(self, nodo, env):
        dest = self.ev(nodo, env)
        if not isinstance(dest, Agente):
            raise ErrorMate(f"el destino tiene que ser un agente, no {nombre_tipo(dest)}")
        return dest

    def un_mensaje(self, nodo, env):
        msg = self.ev(nodo, env)
        if not isinstance(msg, Registro):
            raise ErrorMate(f"solo se envían mensajes declarados, no {nombre_tipo(msg)}")
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
            raise ErrorMate(f"la condición tiene que ser verdadero o falso, no {nombre_tipo(v)}")
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
                "termina? Revisá que la condición del 'mientras' cambie adentro",
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
            raise ErrorMate("demasiada recursión", s[1])

    def _ejecutar(self, s, env):
        clase = s[0]
        if clase == "expr":
            self.ev(s[2], env)
        elif clase == "sea":
            env.definir(s[2], self.ev(s[3], env), mutable=s[4])
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
                self.bloque(s[3], env)
        elif clase == "para":
            col = self.ev(s[3], env)
            if not isinstance(col, (list, dict, str)):
                raise ErrorMate(f"no se puede recorrer {nombre_tipo(col)}")
            for x in list(col):
                self.contar_paso(s[1])
                paso = Entorno(env)
                paso.definir(s[2], x, origen="para")
                self.bloque(s[4], paso, nuevo=False)
        elif clase == "funcion":
            env.definir(s[2], Funcion(s[2], s[3], s[4], env), origen="funcion")
        elif clase == "devolver":
            raise _Retorno(None if s[2] is None else self.ev(s[2], env))
        elif clase == "enviar":
            msg = self.un_mensaje(s[2], env)
            dest = self.destino(s[3], env)
            self.cola.append((self.contexto[0] if self.contexto else None, dest, msg))
        elif clase == "responder":
            if not self.contexto:
                raise ErrorMate("'responder' solo tiene sentido dentro de 'al recibir'")
            raise _Respuesta(self.ev(s[2], env))
        elif clase == "fallar":
            raise ErrorMate(formato(self.ev(s[2], env)), s[1])
        elif clase == "intentar":
            try:
                self.bloque(s[2], env)
            except ErrorMate as e:
                if e.clase == "limite":  # el freno no se puede atajar
                    raise
                manejo = Entorno(env)
                if s[3]:
                    manejo.definir(s[3], e.mensaje, origen="falla")
                self.bloque(s[4], manejo, nuevo=False)
        elif clase == "asegurar":
            cond, valores = s[2], ""
            if cond[0] == "bin" and cond[2] in COMPARADORES:
                # Se evalúa cada lado una sola vez, para poder mostrar qué dio.
                izq, der = self.ev(cond[3], env), self.ev(cond[4], env)
                try:
                    cumple = self.binaria(cond[2], izq, der)
                except ErrorMate as e:
                    e.linea = e.linea or cond[1]
                    raise
                if not cumple:
                    izq, der = formato(izq, False), formato(der, False)
                    valores = (f"dio {izq} y se esperaba {der}" if cond[2] == "=="
                               else f"{izq} {cond[2]} {der} es falso")
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

    def asignar(self, destino, valor, env):
        """Asignación con semántica de valor: cambiar m.a.b reconstruye m."""
        clase = destino[0]
        if clase == "nombre":
            env.asignar(destino[2], valor)
            return
        if clase not in ("indice", "campo"):
            raise ErrorMate(NO_ASIGNABLE)
        base = self.ev(destino[2], env)
        if clase == "indice":
            clave = self.ev(destino[3], env)
            if isinstance(base, list):
                self.posicion(base, clave)
                nueva = list(base)
                nueva[clave] = valor
            elif isinstance(base, dict):
                self.clave_de_mapa(clave)
                nueva = {**base, clave: valor}
            else:
                raise ErrorMate(f"no se puede asignar por índice en {nombre_tipo(base)}")
        elif clase == "campo":
            campo = destino[3]
            if isinstance(base, dict):
                nueva = {**base, campo: valor}
            elif isinstance(base, Registro):
                nueva = self.construir(base.tipo, {**base.campos, campo: valor})
            else:
                raise ErrorMate(f"{nombre_tipo(base)} no tiene campos")
        else:
            raise ErrorMate(NO_ASIGNABLE)
        self.asignar(destino[2], nueva, env)

    def clave_de_mapa(self, clave):
        if not isinstance(clave, str):
            raise ErrorMate(f"las claves de un mapa son textos, no {nombre_tipo(clave)}")

    def posicion(self, sec, i):
        if type(i) is not int:
            raise ErrorMate("el índice tiene que ser un número entero")
        if not 0 <= i < len(sec):
            raise ErrorMate(f"índice {i} fuera de rango (largo {len(sec)})")

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
                raise ErrorMate(f"no se puede negar {nombre_tipo(v)}")
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
                    raise ErrorMate(con_sugerencia(
                        f"el mapa no tiene la clave {formato(i, False)}", i, base))
                return base[i]
            raise ErrorMate(f"no se puede indexar {nombre_tipo(base)}")
        if clase == "campo":
            base = self.ev(n[2], env)
            campos = base.campos if isinstance(base, Registro) else base
            if not isinstance(campos, dict):
                raise ErrorMate(f"{nombre_tipo(base)} no tiene campos")
            if n[3] not in campos:
                raise ErrorMate(con_sugerencia(
                    f"{nombre_tipo(base)} no tiene un campo '{n[3]}'", n[3], campos))
            return campos[n[3]]
        if clase == "preguntar":
            msg = self.un_mensaje(n[2], env)
            dest = self.destino(n[3], env)
            return self.entregar(self.contexto[0] if self.contexto else None, dest, msg, True)
        raise ErrorMate(f"expresión desconocida: {clase}")

    def binaria(self, op, a, b):
        try:
            r = self._binaria(op, a, b)
        except OverflowError:
            raise ErrorMate(DEMASIADO_GRANDE)
        if type(r) is float and not math.isfinite(r):
            raise ErrorMate(DEMASIADO_GRANDE)
        return r

    def _binaria(self, op, a, b):
        if op == "==":
            return igual(a, b)
        if op == "!=":
            return not igual(a, b)
        ambos_num = es_num(a) and es_num(b)
        if op in ("<", "<=", ">", ">="):
            if not (ambos_num or (isinstance(a, str) and isinstance(b, str))):
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
            r = a / b
            return int(r) if type(a) is int and type(b) is int and r.is_integer() else r
        pista = " (usá texto() o \"{...}\" para armar textos)" if op == "+" else ""
        raise ErrorMate(f"no se puede hacer {nombre_tipo(a)} {op} {nombre_tipo(b)}{pista}")

    def llamar(self, f, args):
        if isinstance(f, Nativa):
            return f.fn(args)
        if not isinstance(f, Funcion):
            raise ErrorMate(f"{nombre_tipo(f)} no es una función")
        if len(args) != len(f.params):
            raise ErrorMate(
                f"{f.nombre}() espera {len(f.params)} argumento(s) y recibió {len(args)}")
        env = Entorno(f.env)
        for p, a in zip(f.params, args):
            env.definir(p, a, origen="parametro")
        try:
            self.bloque(f.cuerpo, env, nuevo=False)
        except _Retorno as r:
            return r.valor
        return None


# ───────────────────────────── CLI ─────────────────────────────


def simbolo(s, reemplazo):
    """Devuelve s si la consola lo puede mostrar; si no, el reemplazo en letras comunes."""
    try:
        s.encode(getattr(sys.stdout, "encoding", None) or "utf-8")
        return s
    except (UnicodeError, LookupError):
        return reemplazo


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
        return 130
    except RecursionError:
        if depurar:
            raise
        antes = f"{donde['ruta']}: " if donde["ruta"] else ""
        avisar(f"{antes}error: el programa tiene demasiados niveles anidados "
               "(paréntesis, bloques o llamadas)")
        return 1
    except Exception as e:
        if depurar:
            raise
        avisar(f"error interno de Mate (no es culpa tuya): {type(e).__name__}: {e}")
        if lugar():
            avisar(f"pasó cerca de {lugar()}")
        avisar("corré de nuevo con --depurar para ver el detalle")
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
    if "--ayuda" in opciones or [a.lower() for a in args] == ["ayuda"]:
        print(texto_de_ayuda())
        return 0
    if not args:
        print(texto_de_ayuda())
        return 2

    if len(args) == 1 and args[0].lower().endswith(".mate"):
        args = ["correr"] + args  # 'mate.py hola.mate' es 'mate.py correr hola.mate'
    orden, archivos = args[0].lower(), args[1:]
    if orden not in ORDENES:
        parecidas = difflib.get_close_matches(orden, ORDENES + ("ayuda",), 1)
        avisar(f"no conozco la orden '{args[0]}'" + (
            f", ¿quisiste decir '{parecidas[0]}'?" if parecidas
            else ". Las órdenes son: correr, probar, verificar y ayuda"))
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
        if "--sin-limite" in opciones:
            interprete.max_pasos = None
        resultados = interprete.correr(programa, pruebas=orden == "probar")
    except ErrorMate as e:
        reportar(e.linea, e.mensaje)
        return 1

    for texto in interprete.errores_agentes if orden == "correr" else []:
        avisar(f"{ruta}: error en agente: {texto}")
    if orden == "probar":
        fallidas = 0
        bien, mal = simbolo("✓", "OK"), simbolo("✗", "FALLA")
        for nombre, error in resultados:
            print(f"  {mal if error else bien} {nombre}" + (f"\n      {error}" if error else ""))
            fallidas += bool(error)
        print(f"{len(resultados) - fallidas} de {len(resultados)} pruebas pasaron")
        return 1 if fallidas else 0
    return 1 if interprete.errores_agentes else 0


if __name__ == "__main__":
    sys.exit(main())
