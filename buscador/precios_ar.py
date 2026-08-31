"""El precio de vidriera no es el precio que pagás — motor de costo real argentino.

Ningún metabuscador muestra lo que efectivamente sale un pasaje comprado
desde Argentina, porque la carga impositiva más pesada no está en el ticket
sino en el medio de pago. Este módulo cierra esa brecha.

Reglas vigentes a agosto de 2026, verificadas contra fuentes oficiales:

- **Impuesto PAÍS: derogado.** Perdió vigencia el 23/12/2024. Cualquier
  calculadora que lo siga sumando está mal.
- **Percepción RG 5617/2024, 30%:** vigente. Se aplica a pasajes al exterior
  y a servicios contratados a agencias argentinas, cuando se paga en pesos
  con tarjeta. Aparece en el resumen como `DB.RG 5617 30%`. Es **a cuenta**
  de Ganancias y Bienes Personales: se recupera.
  ⚠ Circuló en diciembre de 2025 la noticia de que se eliminaba en enero de
  2026. Era una inocentada del 28/12; el propio artículo lo aclara. Sigue vigente.
- **Impuesto DNT 7%:** vigente hasta el 31/12/2027 sobre pasajes al exterior.
  Ya viene dentro del precio que publican las aerolíneas y los buscadores.
- **Cabotaje:** IVA 10,5% + IIBB, ya incluidos en el precio publicado. No hay
  percepción ni DNT.

La consecuencia práctica es que **pagar en dólares evita el 30%**, y ése es
el ahorro más grande disponible: más que cambiar de fecha o de aerolínea.
"""
from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional

import requests

from buscador.aeropuertos import AEROPUERTOS
from buscador.config import RAIZ, env, env_float
from buscador.modelos import Itinerario, Oferta

log = logging.getLogger(__name__)

FormaDePago = Literal["tarjeta_pesos", "dolares", "efectivo_pesos"]

#: Alícuota de la percepción RG 5617/2024, a cuenta de Ganancias y Bienes
#: Personales. Recuperable vía ARCA (no inscriptos) o SIRADIG (asalariados).
PERCEPCION_RG5617 = 0.30

_CACHE = Path(RAIZ) / ".cache" / "cotizaciones.json"
_TTL_COTIZACION = 6 * 3600      # el dólar no se mueve tanto dentro del día


@dataclass
class Cotizaciones:
    """Tipos de cambio relevantes para comprar un pasaje."""

    oficial: float
    tarjeta: float
    mep: float
    actualizado: str = ""
    fuente: str = "dolarapi.com"

    @property
    def recargo_tarjeta(self) -> float:
        """Cuánto más caro sale el dólar tarjeta que el oficial, en tanto por uno."""
        if not self.oficial:
            return 0.0
        return self.tarjeta / self.oficial - 1


def _leer_cache() -> Optional[Cotizaciones]:
    try:
        datos = json.loads(_CACHE.read_text(encoding="utf-8"))
        if time.time() - datos["_guardado"] < _TTL_COTIZACION:
            datos.pop("_guardado")
            return Cotizaciones(**datos)
    except (OSError, ValueError, KeyError, TypeError):
        pass
    return None


def _guardar_cache(c: Cotizaciones) -> None:
    try:
        _CACHE.parent.mkdir(parents=True, exist_ok=True)
        _CACHE.write_text(
            json.dumps({**c.__dict__, "_guardado": time.time()}), encoding="utf-8"
        )
    except OSError as e:
        log.debug("no se pudo cachear la cotización: %s", e)


def cotizaciones(forzar: bool = False) -> Cotizaciones:
    """Trae el dólar oficial, tarjeta y MEP, con caché en disco.

    Si la variable USD_ARS está seteada, manda ella y no se sale a internet:
    sirve para tests, para reproducir un análisis y para trabajar sin red.
    """
    fijo = env_float("USD_ARS", 0.0)
    if fijo:
        return Cotizaciones(oficial=fijo, tarjeta=fijo * (1 + PERCEPCION_RG5617),
                            mep=fijo, fuente="USD_ARS (fijado a mano)")

    if not forzar:
        cacheada = _leer_cache()
        if cacheada:
            return cacheada

    valores: dict[str, float] = {}
    actualizado = ""
    for casa in ("oficial", "tarjeta", "bolsa"):
        try:
            r = requests.get(f"https://dolarapi.com/v1/dolares/{casa}", timeout=15)
            r.raise_for_status()
            d = r.json()
            # "venta" es lo que a uno le cuesta comprar el dólar: el lado correcto.
            valores[casa] = float(d["venta"])
            actualizado = d.get("fechaActualizacion", actualizado)
        except (requests.RequestException, ValueError, KeyError) as e:
            log.warning("no se pudo obtener el dólar %s: %s", casa, e)

    if "oficial" not in valores:
        raise RuntimeError(
            "No se pudo obtener el tipo de cambio. Fijá USD_ARS en el .env "
            "para trabajar sin conexión."
        )

    c = Cotizaciones(
        oficial=valores["oficial"],
        # Si la API no da el tarjeta, se deduce: oficial + percepción.
        tarjeta=valores.get("tarjeta", valores["oficial"] * (1 + PERCEPCION_RG5617)),
        mep=valores.get("bolsa", valores["oficial"]),
        actualizado=actualizado,
    )
    _guardar_cache(c)
    return c


def es_internacional(it: Itinerario) -> bool:
    paises = {
        AEROPUERTOS[c].pais
        for s in it.segmentos for c in (s.origen, s.destino)
        if c in AEROPUERTOS
    }
    return len(paises) > 1


def oferta_es_internacional(o: Oferta) -> bool:
    return es_internacional(o.ida) or (o.vuelta is not None and es_internacional(o.vuelta))


@dataclass
class CostoReal:
    """Lo que sale el pasaje según cómo se pague, todo en pesos."""

    publicado_ars: float                 # lo que muestra el buscador, en pesos
    equipaje_ars: float = 0.0            # lo que hay que sumar para llevar lo que se lleva
    percepcion_ars: float = 0.0          # RG 5617, sólo en pasajes al exterior
    #: True cuando la percepción ya viene adentro de `publicado_ars`. Pasa
    #: cuando el precio venía en dólares y se convirtió al dólar tarjeta, que
    #: la lleva incorporada. Si no se distinguiera, se sumaría dos veces.
    percepcion_ya_incluida: bool = False
    internacional: bool = False
    forma_de_pago: FormaDePago = "tarjeta_pesos"
    detalle_equipaje: list[str] = field(default_factory=list)
    cotizacion: Optional[Cotizaciones] = None

    @property
    def total_hoy(self) -> float:
        """La plata que sale del bolsillo el día de la compra."""
        a_sumar = 0.0 if self.percepcion_ya_incluida else self.percepcion_ars
        return self.publicado_ars + self.equipaje_ars + a_sumar

    @property
    def total_recuperable(self) -> float:
        """Lo que se recupera después vía ARCA/SIRADIG. Cero en cabotaje."""
        return self.percepcion_ars

    @property
    def total_neto(self) -> float:
        """El costo real del viaje una vez recuperada la percepción."""
        return self.total_hoy - self.total_recuperable

    def como_dict(self) -> dict[str, float]:
        return {
            "publicado": round(self.publicado_ars, 2),
            "equipaje": round(self.equipaje_ars, 2),
            "percepcion_rg5617": round(self.percepcion_ars, 2),
            "percepcion_ya_incluida": float(self.percepcion_ya_incluida),
            "total_hoy": round(self.total_hoy, 2),
            "total_neto": round(self.total_neto, 2),
        }


def calcular_costo_real(
    oferta: Oferta,
    forma_de_pago: FormaDePago = "tarjeta_pesos",
    quiere_carry_on: bool = True,
    piezas_bodega: int = 0,
    cotiz: Optional[Cotizaciones] = None,
) -> CostoReal:
    """Traduce una oferta al costo efectivo en pesos para un comprador argentino.

    Es lo que convierte "el más barato de la lista" en "el que menos plata te
    saca del bolsillo", que casi nunca son el mismo.
    """
    from buscador.equipaje_ar import costo_de_igualar

    cotiz = cotiz or cotizaciones()
    internacional = oferta_es_internacional(oferta)

    # 1) Llevar el precio publicado a pesos.
    if oferta.moneda == "ARS":
        publicado = oferta.precio
    else:
        # Pagando en pesos con tarjeta, el precio en dólares se liquida al
        # dólar tarjeta, que YA lleva adentro la percepción del 30%.
        # Pagando en dólares (MEP, débito en USD, stop debit), se liquida al MEP.
        tc = cotiz.tarjeta if forma_de_pago == "tarjeta_pesos" else cotiz.mep
        publicado = oferta.precio * tc

    # 2) La percepción del 30%, que sólo alcanza a los pasajes al exterior
    #    pagados en pesos con tarjeta.
    percepcion = 0.0
    ya_incluida = False
    if internacional and forma_de_pago == "tarjeta_pesos":
        if oferta.moneda == "ARS":
            # Los buscadores publican la tarifa con las tasas del ticket
            # (DNT 7%, aeroestación, seguridad) pero sin la percepción, que es
            # un cargo del medio de pago y aparece recién en el resumen.
            percepcion = publicado * PERCEPCION_RG5617
        else:
            # El precio se convirtió al dólar tarjeta, que ya la trae adentro.
            # Se calcula igual para poder mostrarla y para que el consejo de
            # pagar en dólares tenga un número concreto, pero no se suma.
            percepcion = oferta.precio * (cotiz.tarjeta - cotiz.oficial)
            ya_incluida = True

    # 3) El equipaje que la tarifa no incluye.
    tramos = 2 if oferta.vuelta else 1
    aerolinea = oferta.aerolineas[0] if oferta.aerolineas else ""
    equipaje, detalle = costo_de_igualar(
        aerolinea,
        oferta.equipaje,
        quiere_carry_on=quiere_carry_on,
        piezas_bodega=piezas_bodega,
        tramos=tramos,
        internacional=internacional,
        tipo_cambio=cotiz.tarjeta if forma_de_pago == "tarjeta_pesos" else cotiz.mep,
    )

    return CostoReal(
        publicado_ars=publicado,
        equipaje_ars=equipaje,
        percepcion_ars=percepcion,
        percepcion_ya_incluida=ya_incluida,
        internacional=internacional,
        forma_de_pago=forma_de_pago,
        detalle_equipaje=detalle,
        cotizacion=cotiz,
    )


def aplicar_costo_real(
    ofertas: list[Oferta],
    forma_de_pago: FormaDePago = "tarjeta_pesos",
    quiere_carry_on: bool = True,
    piezas_bodega: int = 0,
    cotiz: Optional[Cotizaciones] = None,
) -> list[Oferta]:
    """Completa `precio_ars_final` en cada oferta para que se comparen en serio."""
    cotiz = cotiz or cotizaciones()
    for o in ofertas:
        costo = calcular_costo_real(o, forma_de_pago, quiere_carry_on, piezas_bodega, cotiz)
        o.precio_ars_final = costo.total_hoy
        o.desglose_precio.update(costo.como_dict())
        if costo.detalle_equipaje:
            o.desglose_precio["_detalle_equipaje"] = costo.detalle_equipaje  # type: ignore[assignment]
    return ofertas


def ahorro_pagando_en_dolares(oferta: Oferta, cotiz: Optional[Cotizaciones] = None) -> float:
    """Cuánto se ahorra evitando la percepción del 30%. Cero en cabotaje."""
    cotiz = cotiz or cotizaciones()
    if not oferta_es_internacional(oferta):
        return 0.0
    con_tarjeta = calcular_costo_real(oferta, "tarjeta_pesos", cotiz=cotiz).total_hoy
    en_dolares = calcular_costo_real(oferta, "dolares", cotiz=cotiz).total_hoy
    return max(con_tarjeta - en_dolares, 0.0)
