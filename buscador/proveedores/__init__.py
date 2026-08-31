"""Registro de proveedores de precios de vuelos."""
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
]


def _todas() -> list[Proveedor]:
    from buscador.proveedores.amadeus import Amadeus
    from buscador.proveedores.demo import Demo
    from buscador.proveedores.travelpayouts import Travelpayouts

    return [Amadeus(), Travelpayouts(), Demo()]


def proveedores_disponibles(solo: list[str] | None = None) -> list[Proveedor]:
    """Proveedores con credenciales cargadas, en orden de preferencia.

    `solo` permite forzar un subconjunto por nombre (útil para tests y CLI).
    """
    elegidos = []
    for p in _todas():
        if solo and p.nombre not in solo:
            continue
        if p.disponible():
            elegidos.append(p)
        else:
            log.debug("proveedor %s sin credenciales, se saltea", p.nombre)
    return elegidos
