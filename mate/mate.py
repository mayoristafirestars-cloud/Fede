#!/usr/bin/env python3
"""Mate: un lenguaje chico, en español, para escribir código claro y para que
los agentes se hablen entre ellos con mensajes que tienen contrato.

Uso:
    python3 mate.py correr    archivo.mate [--traza]
    python3 mate.py probar    archivo.mate
    python3 mate.py verificar archivo.mate
"""

import json
import re
import sys
from collections import deque

VERSION = "0.1"

PALABRAS = {
    "sea", "var", "funcion", "devolver", "si", "sino", "mientras", "para", "en",
    "y", "o", "no", "verdadero", "falso", "nada", "mensaje", "agente", "estado",
    "al", "recibir", "como", "enviar", "preguntar", "responder", "fallar",
    "intentar", "falla", "asegurar", "prueba", "remitente",
}

TIPOS_BASE = {"numero", "texto", "logico", "lista", "mapa", "agente", "cualquiera"}

MAX_MENSAJES = 100_000


class ErrorMate(Exception):
    def __init__(self, mensaje, linea=None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.linea = linea


# ───────────────────────────── Lexer ─────────────────────────────

_TOKEN = re.compile(
    r"""
    (?P<ws>[ \t\r]+|\#[^\n]*)
  | (?P<nl>\n)
  | (?P<num>\d+(?:\.\d+)?)
  | (?P<str>"(?:\\.|[^"\\\n])*")
  | (?P<id>[^\W\d]\w*)
  | (?P<op>==|!=|<=|>=|[-+*/%<>=(){}\[\],.:?])
    """,
    re.X,
)


def tokenizar(fuente):
    tokens, pos, linea = [], 0, 1
    while pos < len(fuente):
        m = _TOKEN.match(fuente, pos)
        if not m:
            raise ErrorMate(f"carácter inesperado: {fuente[pos]!r}", linea)
        pos = m.end()
        clase, txt = m.lastgroup, m.group()
        if clase == "nl":
            linea += 1
        elif clase == "num":
            tokens.append(("num", float(txt) if "." in txt else int(txt), linea))
        elif clase == "str":
            tokens.append(("str", txt[1:-1], linea))
        elif clase == "id":
            tokens.append(("kw" if txt in PALABRAS else "id", txt, linea))
        elif clase == "op":
            tokens.append(("op", txt, linea))
    tokens.append(("eof", None, linea))
    return tokens


# ───────────────────────────── Parser ─────────────────────────────


class Parser:
    def __init__(self, tokens):
        self.t = tokens
        self.i = 0

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
        visto = "el final del archivo" if tk[0] == "eof" else f"'{tk[1]}'"
        raise ErrorMate(f"esperaba {que or repr(valor)} y encontré {visto}", tk[2])

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
                nombre = self.espera("id", que="un nombre")[1]
                self.espera("op", "=")
                return ("sea", ln, nombre, self.expr(), val == "var")
            if val == "funcion":
                return self.funcion()
            if val == "devolver":
                self.tomar()
                e = None
                if self.ver()[2] == ln and not self.es("op", "}") and not self.es("eof"):
                    e = self.expr()
                return ("devolver", ln, e)
            if val == "si":
                self.tomar()
                ramas, otro = [(self.expr(), self.bloque())], None
                while self.acepta("kw", "sino"):
                    if self.acepta("kw", "si"):
                        ramas.append((self.expr(), self.bloque()))
                    else:
                        otro = self.bloque()
                        break
                return ("si", ln, ramas, otro)
            if val == "mientras":
                self.tomar()
                return ("mientras", ln, self.expr(), self.bloque())
            if val == "para":
                self.tomar()
                nombre = self.espera("id", que="un nombre")[1]
                self.espera("kw", "en")
                return ("para", ln, nombre, self.expr(), self.bloque())
            if val in ("mensaje", "agente", "prueba") and not nivel_superior:
                raise ErrorMate(f"'{val}' solo puede declararse en el nivel superior", ln)
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
                var = self.acepta("id")
                return ("intentar", ln, cuerpo, var[1] if var else None, self.bloque())
            if val == "asegurar":
                self.tomar()
                cond = self.expr()
                msg = self.expr() if self.acepta("op", ",") else None
                return ("asegurar", ln, cond, msg)
        e = self.expr()
        if self.acepta("op", "="):
            if e[0] not in ("nombre", "indice", "campo"):
                raise ErrorMate("no se puede asignar a esa expresión", ln)
            return ("asignar", ln, e, self.expr())
        return ("expr", ln, e)

    def funcion(self):
        ln = self.tomar()[2]
        nombre = self.espera("id", que="el nombre de la función")[1]
        self.espera("op", "(")
        params = []
        while not self.es("op", ")"):
            params.append(self.espera("id", que="un parámetro")[1])
            if not self.acepta("op", ","):
                break
        self.espera("op", ")")
        return ("funcion", ln, nombre, params, self.bloque())

    def mensaje(self):
        ln = self.tomar()[2]
        nombre = self.nombre_propio("mensaje")
        campos = []
        if self.es("op", "{") and self.ver()[2] == self.linea_previa():
            self.tomar()
            while not self.es("op", "}"):
                campo = self.espera("id", que="un nombre de campo")[1]
                self.espera("op", ":")
                tipo = self.espera("id", que="un tipo")[1]
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
        while not self.acepta("op", "}"):
            tk = self.ver()
            if self.acepta("kw", "estado"):
                n = self.espera("id", que="un nombre")[1]
                self.espera("op", "=")
                estados.append((tk[2], n, self.expr()))
            elif self.acepta("kw", "al"):
                self.espera("kw", "recibir")
                tipo = self.espera("id", que="un tipo de mensaje")[1]
                var = self.espera("id", que="un nombre")[1] if self.acepta("kw", "como") else None
                manejadores.append((tk[2], tipo, var, self.bloque()))
            elif self.es("kw", "funcion"):
                funciones.append(self.funcion())
            else:
                raise ErrorMate(
                    "dentro de un agente solo van 'estado', 'al recibir' y 'funcion'", tk[2]
                )
        return ("agente", ln, nombre, estados, manejadores, funciones)

    # expresiones
    def expr(self):
        izq = self.expr_y()
        while self.es("kw", "o"):
            ln = self.tomar()[2]
            izq = ("o", ln, izq, self.expr_y())
        return izq

    def expr_y(self):
        izq = self.expr_no()
        while self.es("kw", "y"):
            ln = self.tomar()[2]
            izq = ("y", ln, izq, self.expr_no())
        return izq

    def expr_no(self):
        if self.es("kw", "no"):
            ln = self.tomar()[2]
            return ("no", ln, self.expr_no())
        return self.comparacion()

    def comparacion(self):
        izq = self.suma()
        if self.ver()[0] == "op" and self.ver()[1] in ("==", "!=", "<", "<=", ">", ">="):
            _, op, ln = self.tomar()
            return ("bin", ln, op, izq, self.suma())
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
                e = ("campo", tk[2], e, self.espera("id", que="un nombre de campo")[1])
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
            if tk[0] != "id" and not (claves_texto and tk[0] == "str"):
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
            if val == "remitente":
                return ("remitente", ln)
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


def analizar(fuente):
    return Parser(tokenizar(fuente)).programa()


# ─────────────────────── Verificación estática ───────────────────────

_LITERALES = {"num": "numero", "str": "texto", "interp": "texto", "bool": "logico",
              "lista": "lista", "mapa": "mapa"}


def verificar(programa):
    """Revisa los contratos de mensajes antes de correr. Devuelve [(linea, texto)]."""
    errores = []
    mensajes, agentes = {}, {}
    for s in programa:
        if s[0] == "mensaje":
            if s[2] in mensajes or s[2] in agentes:
                errores.append((s[1], f"'{s[2]}' ya está declarado"))
            mensajes[s[2]] = s
        elif s[0] == "agente":
            if s[2] in mensajes or s[2] in agentes:
                errores.append((s[1], f"'{s[2]}' ya está declarado"))
            agentes[s[2]] = [m[1] for m in s[4]]

    for s in mensajes.values():
        vistos = set()
        for campo, tipo, _ in s[3]:
            if campo in vistos:
                errores.append((s[1], f"{s[2]}: el campo '{campo}' está repetido"))
            vistos.add(campo)
            if tipo not in TIPOS_BASE and tipo not in mensajes:
                errores.append((s[1], f"{s[2]}.{campo}: no existe el tipo '{tipo}'"))

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
                errores.append((ln, f"no existe el mensaje '{nombre}'"))
            else:
                decl = {c: (t, op) for c, t, op in mensajes[nombre][3]}
                dados = {}
                for k, e in pares:
                    if k in dados:
                        errores.append((ln, f"{nombre}: el campo '{k}' está repetido"))
                    dados[k] = e
                    if k not in decl:
                        errores.append((ln, f"{nombre} no tiene un campo '{k}'"))
                        continue
                    tipo = decl[k][0]
                    real = e[2] if e[0] == "ctor" else _LITERALES.get(e[0])
                    if real and tipo != "cualquiera" and real != tipo:
                        errores.append((ln, f"{nombre}.{k} es de tipo {tipo}, no {real}"))
                for c, (_, opcional) in decl.items():
                    if c not in dados and not opcional:
                        errores.append((ln, f"a {nombre} le falta el campo '{c}'"))
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


def formato(v, raiz=True):
    if v is None:
        return "nada"
    if type(v) is bool:
        return "verdadero" if v else "falso"
    if type(v) is float:
        return str(int(v)) if v.is_integer() else repr(v)
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
        return f"<agente {v.nombre}>"
    if isinstance(v, (Funcion, Nativa)):
        return f"<funcion {v.nombre}>"
    return str(v)


class Entorno:
    def __init__(self, padre=None, frontera=False):
        self.vars = {}
        self.padre = padre
        self.frontera = frontera  # el estado de un agente: de acá para arriba no se escribe

    def definir(self, nombre, valor, mutable=False):
        if nombre in self.vars:
            raise ErrorMate(f"'{nombre}' ya está definido en este bloque")
        self.vars[nombre] = [valor, mutable]

    def buscar(self, nombre):
        e = self
        while e:
            if nombre in e.vars:
                return e.vars[nombre][0]
            e = e.padre
        raise ErrorMate(f"no existe '{nombre}'")

    def asignar(self, nombre, valor):
        e, cruzo = self, False
        while e:
            if nombre in e.vars:
                if not e.vars[nombre][1]:
                    raise ErrorMate(f"'{nombre}' es fijo (sea); declaralo con 'var' para cambiarlo")
                if cruzo:
                    raise ErrorMate(
                        f"un agente no puede modificar '{nombre}': es de afuera. "
                        "Los agentes solo cambian su propio estado")
                e.vars[nombre][0] = valor
                return
            cruzo = cruzo or e.frontera
            e = e.padre
        raise ErrorMate(f"no existe '{nombre}'")


# ───────────────────────────── Intérprete ─────────────────────────────


class Interprete:
    def __init__(self, salida=print, traza=False):
        self.salida = salida
        self.traza = traza
        self.glob = Entorno()
        self.mensajes = {}
        self.agentes = {}
        self.decl_agentes = []
        self.cola = deque()
        self.contexto = None  # (agente, remitente) mientras se atiende un mensaje
        self.entregados = 0
        self.errores_agentes = []
        self._nativas()

    # ── funciones incorporadas ──
    def _nativas(self):
        def nativa(nombre, minimo, maximo=None):
            maximo = minimo if maximo is None else maximo

            def deco(fn):
                def envuelta(args):
                    if not minimo <= len(args) <= maximo:
                        raise ErrorMate(f"{nombre}() recibió {len(args)} argumento(s)")
                    return fn(*args)
                self.glob.definir(nombre, Nativa(nombre, envuelta))
                return fn
            return deco

        def pedir(v, tipo, donde):
            if nombre_tipo(v) != tipo:
                raise ErrorMate(f"{donde} espera {tipo} y recibió {nombre_tipo(v)}")
            return v

        self.glob.definir("mostrar", Nativa(
            "mostrar", lambda args: self.salida(" ".join(formato(a) for a in args))))

        @nativa("largo", 1)
        def _(x):
            if isinstance(x, (str, list, dict)):
                return len(x)
            raise ErrorMate(f"largo() no aplica a {nombre_tipo(x)}")

        nativa("texto", 1)(formato)
        nativa("tipo", 1)(nombre_tipo)

        @nativa("numero", 1)
        def _(x):
            if es_num(x):
                return x
            try:
                t = pedir(x, "texto", "numero()").strip().replace(",", ".")
                f = float(t)
                return int(f) if f.is_integer() and "." not in t else f
            except ValueError:
                raise ErrorMate(f"'{x}' no es un número")

        @nativa("tiene", 2)
        def _(col, x):
            if isinstance(col, dict):
                return x in col
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
            r = round(pedir(x, "numero", "redondear()"), n)
            return int(r) if n == 0 else r

        nativa("unir", 2)(lambda l, sep: pedir(sep, "texto", "unir()").join(
            formato(x) for x in pedir(l, "lista", "unir()")))
        nativa("partir", 2)(lambda t, sep: pedir(t, "texto", "partir()").split(
            pedir(sep, "texto", "partir()")))
        nativa("mayusculas", 1)(lambda t: pedir(t, "texto", "mayusculas()").upper())
        nativa("minusculas", 1)(lambda t: pedir(t, "texto", "minusculas()").lower())
        nativa("a_json", 1)(lambda v: json.dumps(self._a_json(v), ensure_ascii=False))

        @nativa("de_json", 1)
        def _(t):
            try:
                return self._de_json(json.loads(pedir(t, "texto", "de_json()")))
            except json.JSONDecodeError as e:
                raise ErrorMate(f"JSON inválido: {e.msg}")

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
            if set(v) == {"tipo", "campos"} and v["tipo"] in self.mensajes \
                    and isinstance(v["campos"], dict):
                return self.construir(
                    v["tipo"], {k: self._de_json(x) for k, x in v["campos"].items()})
            if set(v) == {"agente"} and v["agente"] in self.agentes:
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
            raise ErrorMate(f"no existe el mensaje '{nombre}'")
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
                raise ErrorMate(f"{nombre} no tiene un campo '{k}'")
        return Registro(nombre, campos)

    # ── carga del programa ──
    def cargar(self, programa):
        for s in programa:
            if s[0] == "mensaje":
                self.mensajes[s[2]] = s[3]
        for s in programa:
            try:
                if s[0] == "funcion":
                    self.glob.definir(s[2], Funcion(s[2], s[3], s[4], self.glob))
                elif s[0] == "agente":
                    ag = Agente(s[2])
                    self.agentes[s[2]] = ag
                    self.decl_agentes.append(s)
                    self.glob.definir(s[2], ag)
            except ErrorMate as e:
                e.linea = e.linea or s[1]
                raise
        self.reiniciar_agentes()

    def reiniciar_agentes(self):
        for s in self.decl_agentes:
            ag = self.agentes[s[2]]
            ag.env = Entorno(self.glob, frontera=True)
            ag.ocupado = False
            ag.manejadores = {tipo: (var, cuerpo) for _, tipo, var, cuerpo in s[4]}
            for f in s[5]:
                ag.env.definir(f[2], Funcion(f[2], f[3], f[4], ag.env))
        for s in self.decl_agentes:
            ag = self.agentes[s[2]]
            for ln, nombre, e in s[3]:
                try:
                    ag.env.definir(nombre, self.ev(e, ag.env), mutable=True)
                except ErrorMate as err:
                    err.linea = err.linea or ln
                    raise
        self.cola.clear()

    def correr(self, programa, pruebas=False):
        """Ejecuta el programa. Con pruebas=True devuelve [(nombre, error|None)]."""
        self.cargar(programa)
        for s in programa:
            if s[0] not in ("mensaje", "agente", "funcion", "prueba"):
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
        if msg.tipo not in dest.manejadores:
            raise ErrorMate(f"{dest.nombre} no sabe recibir '{msg.tipo}'")
        if dest.ocupado:
            raise ErrorMate(
                f"ciclo de preguntas: {dest.nombre} todavía está atendiendo otro mensaje")
        var, cuerpo = dest.manejadores[msg.tipo]
        env = Entorno(dest.env)
        if var:
            env.definir(var, msg)
        previo, self.contexto, dest.ocupado = self.contexto, (dest, rem), True
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
        if respondio:
            if rem is None:
                raise ErrorMate(f"{dest.nombre} quiso responder, pero el mensaje no vino de un agente")
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

    def ejecutar(self, s, env):
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
                self.bloque(s[3], env)
        elif clase == "para":
            col = self.ev(s[3], env)
            if not isinstance(col, (list, dict, str)):
                raise ErrorMate(f"no se puede recorrer {nombre_tipo(col)}")
            for x in list(col):
                paso = Entorno(env)
                paso.definir(s[2], x)
                self.bloque(s[4], paso, nuevo=False)
        elif clase == "funcion":
            env.definir(s[2], Funcion(s[2], s[3], s[4], env))
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
                manejo = Entorno(env)
                if s[3]:
                    manejo.definir(s[3], e.mensaje)
                self.bloque(s[4], manejo, nuevo=False)
        elif clase == "asegurar":
            if not self.condicion(s[2], env):
                detalle = formato(self.ev(s[3], env)) if s[3] else "no se cumplió lo asegurado"
                raise ErrorMate(detalle, s[1])
        else:
            raise ErrorMate(f"'{clase}' no puede ir acá")

    def asignar(self, destino, valor, env):
        """Asignación con semántica de valor: cambiar m.a.b reconstruye m."""
        clase = destino[0]
        if clase == "nombre":
            env.asignar(destino[2], valor)
            return
        base = self.ev(destino[2], env)
        if clase == "indice":
            clave = self.ev(destino[3], env)
            if isinstance(base, list):
                self.posicion(base, clave)
                nueva = list(base)
                nueva[clave] = valor
            elif isinstance(base, dict):
                if not isinstance(clave, str):
                    raise ErrorMate("las claves de un mapa son textos")
                nueva = {**base, clave: valor}
            else:
                raise ErrorMate(f"no se puede asignar por índice en {nombre_tipo(base)}")
        else:
            campo = destino[3]
            if isinstance(base, dict):
                nueva = {**base, campo: valor}
            elif isinstance(base, Registro):
                nueva = self.construir(base.tipo, {**base.campos, campo: valor})
            else:
                raise ErrorMate(f"{nombre_tipo(base)} no tiene campos")
        self.asignar(destino[2], nueva, env)

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
                if i not in base:
                    raise ErrorMate(f"el mapa no tiene la clave {formato(i, False)}")
                return base[i]
            raise ErrorMate(f"no se puede indexar {nombre_tipo(base)}")
        if clase == "campo":
            base = self.ev(n[2], env)
            campos = base.campos if isinstance(base, Registro) else base
            if not isinstance(campos, dict):
                raise ErrorMate(f"{nombre_tipo(base)} no tiene campos")
            if n[3] not in campos:
                raise ErrorMate(f"{nombre_tipo(base)} no tiene un campo '{n[3]}'")
            return campos[n[3]]
        if clase == "preguntar":
            msg = self.un_mensaje(n[2], env)
            dest = self.destino(n[3], env)
            return self.entregar(self.contexto[0] if self.contexto else None, dest, msg, True)
        raise ErrorMate(f"expresión desconocida: {clase}")

    def binaria(self, op, a, b):
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
            env.definir(p, a)
        try:
            self.bloque(f.cuerpo, env, nuevo=False)
        except _Retorno as r:
            return r.valor
        return None


# ───────────────────────────── CLI ─────────────────────────────


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    opciones = [a for a in argv if a.startswith("--")]
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 2 or args[0] not in ("correr", "probar", "verificar"):
        print(__doc__.strip())
        return 2
    orden, ruta = args

    def reportar(linea, texto):
        print(f"{ruta}:{linea}: error: {texto}" if linea else f"{ruta}: error: {texto}",
              file=sys.stderr)

    try:
        with open(ruta, encoding="utf-8-sig") as f:
            fuente = f.read()
    except OSError as e:
        print(f"no pude abrir {ruta}: {e.strerror}", file=sys.stderr)
        return 2

    try:
        programa = analizar(fuente)
        errores = verificar(programa)
        if errores:
            for linea, texto in errores:
                reportar(linea, texto)
            return 1
        if orden == "verificar":
            print(f"{ruta}: sin errores")
            return 0
        interprete = Interprete(traza="--traza" in opciones)
        resultados = interprete.correr(programa, pruebas=orden == "probar")
    except ErrorMate as e:
        reportar(e.linea, e.mensaje)
        return 1

    for texto in interprete.errores_agentes if orden == "correr" else []:
        print(f"{ruta}: error en agente: {texto}", file=sys.stderr)
    if orden == "probar":
        fallidas = 0
        for nombre, error in resultados:
            print(f"  {'✗' if error else '✓'} {nombre}" + (f"\n      {error}" if error else ""))
            fallidas += bool(error)
        print(f"{len(resultados) - fallidas} de {len(resultados)} pruebas pasaron")
        return 1 if fallidas else 0
    return 1 if interprete.errores_agentes else 0


if __name__ == "__main__":
    sys.exit(main())
