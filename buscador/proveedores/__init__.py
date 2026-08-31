"""Registro de proveedores de precios de vuelos.

El orden de esta lista es el orden de preferencia. `serpapi` va primero
porque es el único que ve el mercado argentino completo —incluidas Flybondi
y JetSmart, que no publican en ningún GDS— con precios nativos en pesos.
"""
from __future__ import annotations

import logging

from buscador.proveedores.base import (
    ErrorProveedor,
    Proveedor,
    ProveedorSinCredenciales,
)

log = logging.getLogger(__name__)

__all__ = [
    "ErrorProveedor",
    "Proveedor",
    "ProveedorSinCredenciales",
    "proveedores_disponibles",
    "todos_los_proveedores",
]


def todos_los_proveedores() -> list[Proveedor]:
    from buscador.proveedores.demo import Demo
    from buscador.proveedores.serpapi import SerpApi
    from buscador.proveedores.travelpayouts import Travelpayouts

    return [SerpApi(), Travelpayouts(), Demo()]


def proveedores_disponibles(solo: list[str] | None = None) -> list[Proveedor]:
    """Proveedores con credenciales cargadas, en orden de preferencia.

    `solo` fuerza un subconjunto por nombre, para tests y para el flag
    `--proveedor` de la línea de comandos.
    """
    elegidos = []
    for p in todos_los_proveedores():
        if solo and p.nombre not in solo:
            continue
        if p.disponible():
            elegidos.append(p)
        else:
            log.debug("proveedor %s sin credenciales, se saltea", p.nombre)
    return elegidos
