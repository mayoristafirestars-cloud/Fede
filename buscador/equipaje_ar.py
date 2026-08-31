"""Qué incluye realmente cada tarifa base, y cuánto cuesta lo que no incluye.

Ésta es la regla de negocio más importante del buscador. Un pasaje de
Flybondi $15.000 más barato que uno de Aerolíneas no es más barato si el
carry-on cuesta $14.149 aparte: en Flybondi la tarifa base sólo incluye un
bulto de 6 kg de 30×40×20 cm, mientras que la tarifa Base de Aerolíneas
incluye carry-on de 8 kg. Comparar los precios de vidriera favorece
sistemáticamente a las low-cost y da una respuesta equivocada.

Ninguna API de búsqueda informa la franquicia de equipaje de forma
confiable, así que la deducimos de la aerolínea.

⚠ Los importes son de agosto de 2026 y cambian seguido (Aerolíneas modificó
su política dos veces sólo en 2026). Están acá para estimar, no para
facturar: el precio firme es el del checkout de la aerolínea.
"""
from __future__ import annotations

from dataclasses import dataclass

from buscador.modelos import Equipaje

#: Aerolíneas cuyo modelo comercial es vender todo por separado.
LOW_COST = {"FO", "JA", "WJ", "H2", "F9", "NK", "G4", "FR", "U2", "W6"}


@dataclass(frozen=True)
class TarifaEquipaje:
    """Franquicia de la tarifa más barata de una aerolínea, y qué cuesta sumar."""

    aerolinea: str
    nombre: str
    #: Qué viene incluido sin pagar nada extra.
    incluido: Equipaje
    #: Precio de sumar carry-on al comprar el pasaje (ARS, por tramo).
    precio_carry_on: float = 0.0
    #: Precio de sumar una pieza despachada al comprar el pasaje (ARS, por tramo).
    precio_bodega: float = 0.0
    notas: str = ""


#: Comprar el equipaje en la puerta de embarque cuesta entre 2,1x y 2,4x lo
#: que cuesta comprarlo junto con el pasaje. El buscador siempre cotiza con
#: el precio de compra anticipada, que es el escenario correcto.
RECARGO_EN_PUERTA = 2.2

_TARIFAS: dict[str, TarifaEquipaje] = {
    "FO": TarifaEquipaje(
        aerolinea="FO", nombre="Flybondi",
        # Un solo bulto de 30x40x20 y hasta 6 kg. Ni carry-on ni bodega.
        incluido=Equipaje(mano_incluido=False, bodega_incluidas=0, mochila_incluida=True),
        precio_carry_on=14_149, precio_bodega=10_399,
        notas="tarifa base: sólo 1 bulto de 6 kg (30×40×20)",
    ),
    "JA": TarifaEquipaje(
        aerolinea="JA", nombre="JetSmart",
        # Bolso de 45x35x25 y hasta 10 kg bajo el asiento. Desde 2026 el
        # control es por volumen total, no por cantidad de bultos.
        incluido=Equipaje(mano_incluido=False, bodega_incluidas=0, mochila_incluida=True),
        precio_carry_on=9_990, precio_bodega=12_590,
        notas="tarifa base: sólo bolso de 10 kg (45×35×25) bajo el asiento",
    ),
    "AR": TarifaEquipaje(
        aerolinea="AR", nombre="Aerolíneas Argentinas",
        # La tarifa Base perdió el carry-on en mayo de 2026 y lo recuperó en
        # junio tras el rechazo de los pasajeros. La tarifa Promo se eliminó.
        incluido=Equipaje(mano_incluido=True, bodega_incluidas=0, mochila_incluida=True),
        precio_carry_on=0, precio_bodega=42_350,
        notas="tarifa Base: artículo personal 3 kg + carry-on 8 kg, sin bodega",
    ),
}
_TARIFAS["WJ"] = TarifaEquipaje(  # JetSmart Argentina opera con su propio código
    aerolinea="WJ", nombre="JetSmart Argentina",
    incluido=_TARIFAS["JA"].incluido,
    precio_carry_on=_TARIFAS["JA"].precio_carry_on,
    precio_bodega=_TARIFAS["JA"].precio_bodega,
    notas=_TARIFAS["JA"].notas,
)

#: Lo que incluye una tarifa económica de una aerolínea tradicional cuando no
#: tenemos datos específicos: carry-on sí, bodega según el alcance del vuelo.
_LEGACY_CABOTAJE = Equipaje(mano_incluido=True, bodega_incluidas=0)
_LEGACY_INTERNACIONAL = Equipaje(mano_incluido=True, bodega_incluidas=1)

#: Bodega adicional en vuelos internacionales: primera pieza online.
PRECIO_BODEGA_INTERNACIONAL_USD = 100.0


def es_low_cost(aerolinea: str) -> bool:
    return (aerolinea or "").upper() in LOW_COST


def equipaje_de_tarifa_base(aerolinea: str, internacional: bool = False) -> Equipaje:
    """Qué incluye la tarifa más barata de esta aerolínea.

    Es una estimación informada, no un dato de la reserva: sirve para que la
    comparación sea justa, no para prometerle nada al pasajero.
    """
    codigo = (aerolinea or "").upper()
    tarifa = _TARIFAS.get(codigo)

    if tarifa:
        if internacional and codigo == "AR":
            # En internacional Aerolíneas no aplicó los recortes de cabotaje:
            # la Base incluye carry-on de 10 kg.
            return Equipaje(mano_incluido=True, bodega_incluidas=0)
        return tarifa.incluido

    if es_low_cost(codigo):
        return Equipaje(mano_incluido=False, bodega_incluidas=0)

    return _LEGACY_INTERNACIONAL if internacional else _LEGACY_CABOTAJE


def costo_de_igualar(
    aerolinea: str,
    incluido: Equipaje,
    quiere_carry_on: bool = True,
    piezas_bodega: int = 0,
    tramos: int = 1,
    internacional: bool = False,
    tipo_cambio: float = 1.0,
) -> tuple[float, list[str]]:
    """Cuánto hay que sumarle a esta tarifa para que cubra lo que el pasajero lleva.

    Devuelve (costo en ARS, detalle legible). `tramos` es la cantidad de
    tramos pagos: una ida y vuelta son 2, porque el equipaje se cobra por
    trayecto. `tipo_cambio` convierte los cargos que las aerolíneas cobran
    en dólares.
    """
    codigo = (aerolinea or "").upper()
    tarifa = _TARIFAS.get(codigo)
    total = 0.0
    detalle: list[str] = []

    if quiere_carry_on and not incluido.mano_incluido:
        precio = tarifa.precio_carry_on if tarifa else 12_000.0
        if precio:
            total += precio * tramos
            detalle.append(f"carry-on x{tramos}: ${precio * tramos:,.0f}".replace(",", "."))

    faltan = max(piezas_bodega - incluido.bodega_incluidas, 0)
    if faltan:
        if internacional and not (tarifa and tarifa.precio_bodega and not es_low_cost(codigo)):
            precio = PRECIO_BODEGA_INTERNACIONAL_USD * tipo_cambio
        else:
            precio = tarifa.precio_bodega if tarifa else 40_000.0
        costo = precio * faltan * tramos
        total += costo
        detalle.append(f"bodega x{faltan} x{tramos} tramos: ${costo:,.0f}".replace(",", "."))

    return total, detalle


def describir_tarifa(aerolinea: str) -> str:
    tarifa = _TARIFAS.get((aerolinea or "").upper())
    if tarifa:
        return f"{tarifa.nombre}: {tarifa.notas}"
    if es_low_cost(aerolinea):
        return f"{aerolinea}: low-cost, la tarifa base no incluye equipaje"
    return f"{aerolinea}: tarifa económica estándar"
