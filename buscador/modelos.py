"""Modelos de dominio del buscador de pasajes.

Todo el sistema habla estas estructuras: los proveedores traducen su JSON
propio a `Oferta`, y el ranking / los reportes solo conocen `Oferta`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Literal, Optional

TipoViaje = Literal["ida", "ida_vuelta"]
ClaseCabina = Literal["ECONOMY", "PREMIUM_ECONOMY", "BUSINESS", "FIRST"]


@dataclass(frozen=True)
class Segmento:
    """Un tramo operado sin cambio de avión (un número de vuelo)."""

    origen: str                      # IATA, ej. "AEP"
    destino: str                     # IATA, ej. "BRC"
    salida: datetime                 # hora local del aeropuerto de origen
    llegada: datetime                # hora local del aeropuerto de destino
    aerolinea: str                   # código IATA de la aerolínea, ej. "AR"
    numero_vuelo: str = ""
    aeronave: str = ""
    duracion_min: int = 0            # 0 => se calcula de salida/llegada

    def __post_init__(self) -> None:
        if not self.duracion_min:
            minutos = int((self.llegada - self.salida).total_seconds() // 60)
            object.__setattr__(self, "duracion_min", max(minutos, 0))


@dataclass
class Itinerario:
    """Una dirección del viaje (la ida, o la vuelta), con sus escalas."""

    segmentos: list[Segmento]

    @property
    def origen(self) -> str:
        return self.segmentos[0].origen

    @property
    def destino(self) -> str:
        return self.segmentos[-1].destino

    @property
    def salida(self) -> datetime:
        return self.segmentos[0].salida

    @property
    def llegada(self) -> datetime:
        return self.segmentos[-1].llegada

    @property
    def escalas(self) -> int:
        return max(len(self.segmentos) - 1, 0)

    @property
    def duracion_min(self) -> int:
        """Duración puerta a puerta, incluyendo esperas en conexión."""
        return int((self.llegada - self.salida).total_seconds() // 60)

    @property
    def aerolineas(self) -> list[str]:
        vistas: list[str] = []
        for s in self.segmentos:
            if s.aerolinea not in vistas:
                vistas.append(s.aerolinea)
        return vistas

    @property
    def layovers_min(self) -> list[int]:
        """Minutos de espera en cada conexión."""
        esperas = []
        for anterior, siguiente in zip(self.segmentos, self.segmentos[1:]):
            esperas.append(int((siguiente.salida - anterior.llegada).total_seconds() // 60))
        return esperas

    @property
    def cambia_de_aeropuerto(self) -> bool:
        """True si alguna conexión obliga a trasladarse entre aeropuertos."""
        return any(
            anterior.destino != siguiente.origen
            for anterior, siguiente in zip(self.segmentos, self.segmentos[1:])
        )


@dataclass
class Equipaje:
    """Qué incluye la tarifa. Decisivo para comparar low-cost contra flag carriers."""

    mano_incluido: bool = True       # bolso de mano / carry-on
    bodega_incluidas: int = 0        # piezas despachadas incluidas
    mochila_incluida: bool = True    # artículo personal bajo el asiento


@dataclass
class Oferta:
    """Una opción de vuelo comparable, ya normalizada."""

    proveedor: str                   # "amadeus", "travelpayouts", ...
    precio: float                    # total del viaje para todos los pasajeros
    moneda: str                      # "USD", "ARS", "EUR"
    ida: Itinerario
    vuelta: Optional[Itinerario] = None
    equipaje: Equipaje = field(default_factory=Equipaje)
    cabina: ClaseCabina = "ECONOMY"
    asientos_restantes: Optional[int] = None
    reembolsable: Optional[bool] = None
    url_reserva: str = ""
    id_externo: str = ""
    self_transfer: bool = False      # tramos comprados por separado, sin protección
    obtenida_en: datetime = field(default_factory=datetime.now)

    # --- Campos derivados que completa la capa de precios / ranking ---
    precio_ars_final: Optional[float] = None   # con impuestos y percepciones AR
    desglose_precio: dict[str, float] = field(default_factory=dict)
    puntaje: Optional[float] = None
    motivos: list[str] = field(default_factory=list)

    @property
    def tipo_viaje(self) -> TipoViaje:
        return "ida_vuelta" if self.vuelta else "ida"

    @property
    def precio_comparable(self) -> float:
        """El número con el que se compara esta oferta contra las demás.

        Si ya se calculó el costo real en pesos (impuestos, percepciones,
        equipaje, traslado terrestre), gana ese; si no, el precio de lista.
        """
        return self.precio_ars_final if self.precio_ars_final is not None else self.precio

    @property
    def moneda_comparable(self) -> str:
        return "ARS" if self.precio_ars_final is not None else self.moneda

    @property
    def escalas_totales(self) -> int:
        return self.ida.escalas + (self.vuelta.escalas if self.vuelta else 0)

    @property
    def duracion_total_min(self) -> int:
        return self.ida.duracion_min + (self.vuelta.duracion_min if self.vuelta else 0)

    @property
    def es_directo(self) -> bool:
        return self.escalas_totales == 0

    @property
    def aerolineas(self) -> list[str]:
        vistas = list(self.ida.aerolineas)
        if self.vuelta:
            for a in self.vuelta.aerolineas:
                if a not in vistas:
                    vistas.append(a)
        return vistas

    @property
    def noches(self) -> Optional[int]:
        if not self.vuelta:
            return None
        return (self.vuelta.salida.date() - self.ida.llegada.date()).days

    def clave_dedupe(self) -> tuple:
        """Identidad de la oferta, para descartar duplicados entre proveedores.

        El itinerario no alcanza: la misma aerolínea vende el mismo vuelo en
        varias tarifas (con equipaje, sin equipaje, flexible). Son opciones
        distintas y el usuario tiene que poder elegir, así que la tarifa entra
        en la identidad.
        """
        def firma(it: Optional[Itinerario]) -> tuple:
            if it is None:
                return ()
            return tuple(
                (s.aerolinea, s.numero_vuelo, s.origen, s.destino, s.salida.isoformat())
                for s in it.segmentos
            )

        return (
            firma(self.ida),
            firma(self.vuelta),
            self.cabina,
            self.equipaje.mano_incluido,
            self.equipaje.bodega_incluidas,
        )


@dataclass
class Consulta:
    """Lo que el usuario pide. Una consulta puede expandirse en muchas búsquedas."""

    origen: str
    destino: str
    fecha_ida: date
    fecha_vuelta: Optional[date] = None
    adultos: int = 1
    ninos: int = 0
    infantes: int = 0
    cabina: ClaseCabina = "ECONOMY"
    moneda: str = "ARS"

    # Flexibilidad
    flex_dias: int = 0                       # +/- N dias sobre las fechas pedidas
    origenes_alternativos: list[str] = field(default_factory=list)
    destinos_alternativos: list[str] = field(default_factory=list)

    # Filtros duros
    solo_directos: bool = False
    max_escalas: Optional[int] = None
    aerolineas_excluidas: list[str] = field(default_factory=list)
    precio_max: Optional[float] = None
    requiere_equipaje_bodega: bool = False

    @property
    def pasajeros(self) -> int:
        return self.adultos + self.ninos + self.infantes

    @property
    def tipo_viaje(self) -> TipoViaje:
        return "ida_vuelta" if self.fecha_vuelta else "ida"

    def fechas_a_probar(self) -> list[tuple[date, Optional[date]]]:
        """Expande la flexibilidad en pares (ida, vuelta) concretos.

        Mantiene fija la cantidad de noches: correr la ida corre la vuelta,
        que es lo que casi siempre quiere quien viaja.
        """
        if self.flex_dias <= 0:
            return [(self.fecha_ida, self.fecha_vuelta)]

        pares: list[tuple[date, Optional[date]]] = []
        for delta_ida in range(-self.flex_dias, self.flex_dias + 1):
            ida = self.fecha_ida + timedelta(days=delta_ida)
            if ida < date.today():
                continue
            if self.fecha_vuelta is None:
                pares.append((ida, None))
                continue
            for delta_vuelta in range(-self.flex_dias, self.flex_dias + 1):
                vuelta = self.fecha_vuelta + timedelta(days=delta_vuelta)
                if vuelta >= ida:
                    pares.append((ida, vuelta))
        return pares

    def rutas_a_probar(self) -> list[tuple[str, str]]:
        origenes = [self.origen] + [o for o in self.origenes_alternativos if o != self.origen]
        destinos = [self.destino] + [d for d in self.destinos_alternativos if d != self.destino]
        return [(o, d) for o in origenes for d in destinos]
