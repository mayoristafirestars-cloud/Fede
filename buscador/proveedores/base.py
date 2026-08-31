"""Contrato que cumple todo proveedor de precios.

Agregar una fuente nueva = escribir una clase con `buscar()` y registrarla.
El resto del sistema (ranking, reportes, CLI) no cambia.
"""
from __future__ import annotations

import abc
import logging
from datetime import date
from typing import Optional

from buscador.modelos import Consulta, Oferta

log = logging.getLogger(__name__)


class ErrorProveedor(RuntimeError):
    """Falla recuperable de un proveedor: se registra y se sigue con los demás."""


class ProveedorSinCredenciales(ErrorProveedor):
    """Faltan API keys. No es un bug: el proveedor simplemente se saltea."""


class Proveedor(abc.ABC):
    nombre: str = "base"

    #: Cuántas llamadas HTTP cuesta, aproximadamente, una búsqueda concreta.
    #: Lo usa el orquestador para repartir el presupuesto de requests.
    costo_por_busqueda: int = 1

    @abc.abstractmethod
    def disponible(self) -> bool:
        """True si tiene credenciales y puede usarse."""

    @abc.abstractmethod
    def buscar(
        self,
        consulta: Consulta,
        origen: str,
        destino: str,
        fecha_ida: date,
        fecha_vuelta: Optional[date],
        limite: int = 20,
    ) -> list[Oferta]:
        """Devuelve ofertas normalizadas para UNA combinación ruta+fechas."""

    def fechas_mas_baratas(
        self,
        consulta: Consulta,
        origen: str,
        destino: str,
    ) -> dict[date, float]:
        """Calendario precio-por-fecha, si el proveedor lo soporta.

        Sirve para elegir qué fechas vale la pena consultar en detalle en vez
        de quemar la cuota probando todas. Devolver {} significa "no soportado".
        """
        return {}
