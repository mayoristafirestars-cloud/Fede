# Funciones de Python para el ejemplo 09_con_python.mate.
#
# Esto NO es Mate: es Python, el lenguaje en el que está hecho Mate. Sirve para sumarle
# a un programa lo que Mate no trae. Desde el .mate se trae con
#     usar python "ayudas.py"
# y cada función de acá se llama con el nombre del archivo adelante: ayudas.raiz(144)
#
# Lo que hay que saber para escribir uno propio:
#   - Cada función empieza con 'def', y entrega su resultado con 'return'.
#   - Desde Mate llegan números, textos, True/False (verdadero/falso), None (nada),
#     listas y diccionarios (los mapas). Lo mismo es lo que puede volver.
#   - Las funciones cuyo nombre empieza con guion bajo (_asi) no se ven desde Mate.
#   - Si algo sale mal acá adentro, Mate lo muestra como un error del renglón del .mate
#     que hizo la llamada, y se puede atajar con 'intentar'.
#
# OJO: lo que está en este archivo corre con todos los permisos de tu computadora (puede
# leer y borrar archivos, o salir a internet). Usá solo archivos tuyos o de confianza.

import math
import statistics
from datetime import datetime


def raiz(numero):
    """La raíz cuadrada. De un número negativo no hay: Python da un error."""
    return math.sqrt(numero)


def dias_entre(desde, hasta):
    """Cuántos días van de una fecha a la otra, escritas como en Mate: "21/11/2026"."""
    como_van = "%d/%m/%Y"
    return (datetime.strptime(hasta, como_van) - datetime.strptime(desde, como_van)).days


def resumen(numeros):
    """Recibe una lista de números y devuelve un diccionario: a Mate le llega un mapa."""
    return {
        "del_medio": statistics.median(numeros),
        "mayor": max(numeros),
        "menor": min(numeros),
    }
