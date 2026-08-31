"""Ranking de ofertas: qué significa "el mejor" además de "el más barato".

El enfoque es el **costo generalizado** de la economía del transporte: todo
lo que molesta de un itinerario se convierte a plata y se suma al precio. El
resultado tiene unidades de dinero, así que es interpretable — "esta opción
sale $80.000 menos pero te cuesta 9 horas más de viaje y una conexión que se
pierde una de cada cuatro veces; en total te sale $40.000 más cara".

Por qué esto y no un puntaje normalizado de 0 a 100:

1. **Escala absoluta.** El costo de un itinerario no depende de qué otros
   itinerarios haya en la lista. Un min-max se estira entero si aparece una
   opción absurda de 40 horas, y ahí cambian *todos* los puntajes. Eso rompe
   la caché, la comparación entre fechas y las alertas de precio.
2. **Pesos con unidades.** "Evitar una escala vale $25.000" es una afirmación
   discutible y calibrable. "el peso de la duración es 0,3" no significa nada.
3. **Explicabilidad.** Se muestra el desglose y se entiende.

Los parámetros vienen de la literatura de elección de itinerarios aéreos
(modelos logit tipo Coldren & Koppelman, guía de valor del tiempo del US DOT,
tiempos mínimos de conexión de IATA), reescalados a ingresos argentinos.

El puntaje de 0 a 100 que se muestra en pantalla se **deriva** del costo
generalizado; nunca se usa para ordenar.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from buscador.aeropuertos import AEROPUERTOS
from buscador.modelos import Consulta, Itinerario, Oferta, Segmento

# ── Tiempos mínimos de conexión ────────────────────────────────────────────
# IATA administra los MCT oficiales (Resolución PSC 765) y los fija cada
# aeropuerto. Estos son los valores típicos por tipo de conexión, en minutos.
# Clave: (tramo que llega, tramo que sale) — "D" cabotaje, "I" internacional.
MCT_POR_DEFECTO = {("D", "D"): 45, ("D", "I"): 90, ("I", "I"): 60, ("I", "D"): 75}

#: Aeropuertos con MCT publicado distinto del típico.
MCT_POR_AEROPUERTO: dict[str, dict[tuple[str, str], int]] = {
    "AEP": {("D", "D"): 40},
    "EZE": {("I", "I"): 90, ("D", "I"): 90, ("I", "D"): 90},
    "GRU": {("I", "I"): 90},
    "SCL": {("I", "I"): 70},
    "PTY": {("I", "I"): 45},     # Copa diseñó Tocumen como hub de conexión rápida
    "LIM": {("I", "I"): 70},
    "MAD": {("I", "I"): 60},
    "LHR": {("I", "I"): 75},
    "CDG": {("I", "I"): 60},
    "ATL": {("D", "D"): 40},
    "MIA": {("I", "D"): 90},
}

#: Penalización por hora de SALIDA, en dólares a un valor del tiempo de 15/h.
#: Salir a las 3 de la mañana implica levantarse a la medianoche y pagar un
#: remise nocturno: el costo es real y observable.
_PENAL_SALIDA = {0: 28, 1: 30, 2: 30, 3: 28, 4: 22, 5: 14, 6: 7, 7: 2,
                 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0,
                 17: 1, 18: 3, 19: 5, 20: 8, 21: 12, 22: 18, 23: 24}

#: Penalización por hora de LLEGADA. Llegar de madrugada tiene el mismo
#: problema del otro lado, más el check-in de hotel fuera de horario.
_PENAL_LLEGADA = {0: 22, 1: 26, 2: 28, 3: 28, 4: 24, 5: 16, 6: 8, 7: 3,
                  8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0,
                  17: 0, 18: 0, 19: 2, 20: 4, 21: 8, 22: 14, 23: 18}

#: Las penalizaciones hedónicas están expresadas en dólares a este valor del
#: tiempo; se escalan proporcionalmente cuando el perfil usa otro.
_VOT_REFERENCIA_USD = 15.0


@dataclass
class Preferencias:
    """Cuánto vale, en plata, cada molestia. Todo en la moneda de comparación.

    Los valores se construyen con `perfil()`, que parte de anclas en dólares
    de la literatura y las convierte a pesos.
    """

    moneda: str = "ARS"

    #: Valor de una hora del pasajero. Es la perilla que más mueve el ranking:
    #: en 0, el orden se vuelve "el más barato y listo".
    valor_hora: float = 0.0

    #: El tiempo no vale lo mismo según qué se esté haciendo. Esperar en un
    #: aeropuerto es peor que estar volando; manejar hasta otro aeropuerto,
    #: peor todavía. Multiplicadores de la literatura de transporte.
    peso_tiempo_vuelo: float = 1.0
    peso_tiempo_escala: float = 1.5
    peso_tiempo_terrestre: float = 1.3

    #: Molestia de una escala más allá del tiempo que consume. Se toma el
    #: mayor entre un piso fijo y un porcentaje del precio de referencia de la
    #: ruta: el sobreprecio de mercado del vuelo directo es 15-25% de la
    #: tarifa, y la mitad de eso ya lo cobra el tiempo de espera. Por eso el
    #: porcentaje es 8% y no 20%: si no, se cuenta dos veces.
    escala_piso: float = 0.0
    escala_porcentaje: float = 0.08
    #: La segunda escala es peor que la primera: dos chances de perder el
    #: equipaje, dos de perder la conexión, y el cansancio no es lineal.
    escala_crecimiento: float = 1.6

    #: Riesgo de perder la conexión. P(perder) decae exponencialmente con el
    #: colchón por encima del mínimo del aeropuerto.
    riesgo_sin_colchon: float = 0.30      # probabilidad con colchón cero
    riesgo_constante_min: float = 45.0    # minutos de decaimiento
    riesgo_piso: float = 0.01

    #: Escala larga: el tiempo ya se cobró; esto es el cansancio adicional.
    escala_larga_horas: float = 4.0
    escala_larga_por_hora: float = 0.0
    noche_en_aeropuerto: float = 0.0      # ~ lo que costaría un hotel de tránsito

    #: Horarios incómodos.
    escala_horarios: float = 1.0

    #: Cambiar de aeropuerto en la conexión: traslado, tráfico y volver a
    #: hacer todo el check-in. Google lo nombra como uno de sus tres factores.
    cambio_aeropuerto_fijo: float = 0.0
    cambio_aeropuerto_traslado: float = 0.0
    cambio_aeropuerto_horas: float = 2.0
    cambio_aeropuerto_mct_extra: int = 150

    #: Tramos comprados por separado: si el primero se atrasa, el segundo se
    #: pierde y nadie responde.
    self_transfer_fijo: float = 0.0
    self_transfer_mct_extra: int = 45

    #: Puntualidad de la aerolínea, cuando se conoce.
    puntualidad_referencia: float = 0.80
    puntualidad_por_punto: float = 0.0

    #: Traslado por tierra hasta un aeropuerto alternativo.
    costo_por_km: float = 0.0
    velocidad_terrestre_kmh: float = 85.0

    @classmethod
    def perfil(cls, nombre: str = "ocio", tipo_cambio: float = 1.0,
               moneda: str = "ARS") -> "Preferencias":
        """Construye preferencias a partir de un perfil de viajero.

        El valor del tiempo está calibrado para Argentina: la guía del US DOT
        usa 1,9 veces el ingreso horario mediano del hogar para viaje aéreo
        personal, y los estudios de aviación reportan 75-150 dólares la hora.
        Esos números salen de países de ingreso alto; aplicados tal cual acá,
        el vuelo directo caro gana siempre y el buscador deja de servir.
        Reescalados al ingreso mediano argentino quedan bastante más abajo.
        """
        vot_usd = {
            "mochilero": 3.0,    # elige explícitamente tiempo por sobre plata
            "ocio": 7.0,         # el default: prioriza precio, pero no a cualquier costo
            "comodo": 16.0,      # paga por no sufrir el viaje
            "trabajo": 38.0,     # el tiempo pesa más que la tarifa
        }.get(nombre, 7.0)

        k = vot_usd / _VOT_REFERENCIA_USD          # escala de lo hedónico
        tc = tipo_cambio

        return cls(
            moneda=moneda,
            valor_hora=vot_usd * tc,
            escala_piso=25.0 * tc,
            escala_larga_por_hora=6.0 * k * tc,
            noche_en_aeropuerto=90.0 * k * tc,
            escala_horarios=k * tc,
            cambio_aeropuerto_fijo=55.0 * k * tc,
            cambio_aeropuerto_traslado=45.0 * tc,
            self_transfer_fijo=30.0 * k * tc,
            puntualidad_por_punto=1.5 * tc,
            # Nafta, peajes y desgaste en ruta argentina, por kilómetro.
            costo_por_km=205.0 if moneda == "ARS" else 0.14 * tc,
        )

    @classmethod
    def solo_precio(cls, moneda: str = "ARS") -> "Preferencias":
        """"No me importa nada más que el precio". Ordena por plata y listo."""
        return cls(moneda=moneda, valor_hora=0.0, escala_porcentaje=0.0)


def _tipo_de_tramo(s: Segmento) -> str:
    """'I' si el tramo cruza una frontera, 'D' si es de cabotaje."""
    a, b = AEROPUERTOS.get(s.origen), AEROPUERTOS.get(s.destino)
    if a and b and a.pais != b.pais:
        return "I"
    return "D"


def mct(aeropuerto: str, llega: Segmento, sale: Segmento) -> int:
    """Tiempo mínimo de conexión para este aeropuerto y este tipo de conexión."""
    clave = (_tipo_de_tramo(llega), _tipo_de_tramo(sale))
    especifico = MCT_POR_AEROPUERTO.get(aeropuerto.upper(), {})
    return especifico.get(clave, MCT_POR_DEFECTO[clave])


def probabilidad_de_perder(colchon_min: float, p: Preferencias) -> float:
    """Chance de perder la conexión, según el colchón sobre el mínimo legal.

    Sale de la formulación estándar de propagación de demoras: la conexión se
    pierde cuando la demora del primer tramo supera el colchón. Con demoras de
    cola exponencial da esta forma cerrada. Con 30 minutos de colchón la
    probabilidad ronda el 15%; con 90, el 4%.
    """
    if colchon_min < 0:
        # Por debajo del mínimo legal la aerolínea ni siquiera vende la
        # conexión; si aparece, es porque son tickets separados.
        return 0.85
    return max(p.riesgo_piso,
               p.riesgo_sin_colchon * math.exp(-colchon_min / p.riesgo_constante_min))


def costo_de_perder(o: Oferta, p: Preferencias, precio_referencia: float) -> float:
    """Cuánto cuesta perder una conexión. Depende de quién se hace cargo."""
    if not o.self_transfer:
        # Un solo billete: la aerolínea reacomoda. Se pierden unas horas.
        return 5.0 * p.valor_hora + 25.0 * (p.valor_hora / max(_VOT_REFERENCIA_USD, 1e-9))
    # Tramos separados sin protección: pasaje nuevo de último momento, hotel y
    # un día perdido. No hay a quién reclamarle.
    return 12.0 * p.valor_hora + max(150.0, 0.55 * precio_referencia)


def _interpolar_hora(tabla: dict[int, float], momento: datetime) -> float:
    """Lee la tabla horaria de forma continua: las 21:30 valen entre 21 y 22."""
    h = momento.hour + momento.minute / 60.0
    entera = int(h)
    fraccion = h - entera
    return tabla[entera % 24] * (1 - fraccion) + tabla[(entera + 1) % 24] * fraccion


def _cruza_la_madrugada(desde: datetime, hasta: datetime) -> bool:
    cursor = desde
    while cursor < hasta:
        if 1 <= cursor.hour < 5:
            return True
        cursor += timedelta(minutes=30)
    return False


@dataclass
class Desglose:
    """De dónde sale cada peso del costo generalizado, para poder explicarlo."""

    precio: float = 0.0
    tiempo: float = 0.0
    escalas: float = 0.0
    riesgo_conexion: float = 0.0
    escalas_largas: float = 0.0
    horarios: float = 0.0
    cambio_aeropuerto: float = 0.0
    self_transfer: float = 0.0
    puntualidad: float = 0.0
    traslado_terrestre: float = 0.0

    @property
    def total(self) -> float:
        return sum(getattr(self, c) for c in self.__dataclass_fields__)

    @property
    def sobrecosto(self) -> float:
        """Todo lo que no es plata de la tarifa: el costo oculto del itinerario."""
        return self.total - self.precio

    def como_dict(self) -> dict[str, float]:
        d = {c: round(getattr(self, c), 2) for c in self.__dataclass_fields__
             if getattr(self, c)}
        d["costo_generalizado"] = round(self.total, 2)
        return d


def _costo_itinerario(
    it: Itinerario, o: Oferta, p: Preferencias, d: Desglose, precio_referencia: float
) -> None:
    """Acumula en `d` el costo no monetario de una punta del viaje."""
    minutos_vuelo = sum(s.duracion_min for s in it.segmentos)
    minutos_escala = sum(it.layovers_min)

    d.tiempo += (minutos_vuelo / 60) * p.peso_tiempo_vuelo * p.valor_hora
    d.tiempo += (minutos_escala / 60) * p.peso_tiempo_escala * p.valor_hora

    unidad = max(p.escala_piso, p.escala_porcentaje * precio_referencia)
    for i in range(it.escalas):
        d.escalas += unidad * (p.escala_crecimiento ** i)

    for i, espera in enumerate(it.layovers_min):
        llega, sale = it.segmentos[i], it.segmentos[i + 1]
        minimo = mct(llega.destino, llega, sale)
        if llega.destino != sale.origen:
            minimo += p.cambio_aeropuerto_mct_extra
            d.cambio_aeropuerto += (
                p.cambio_aeropuerto_fijo
                + p.cambio_aeropuerto_horas * p.peso_tiempo_terrestre * p.valor_hora
                + p.cambio_aeropuerto_traslado
            )
        if o.self_transfer:
            # Hay que retirar el equipaje, volver a despacharlo y pasar
            # seguridad de nuevo.
            minimo += p.self_transfer_mct_extra

        d.riesgo_conexion += (
            probabilidad_de_perder(espera - minimo, p)
            * costo_de_perder(o, p, precio_referencia)
        )

        horas = espera / 60
        if horas > p.escala_larga_horas:
            d.escalas_largas += (horas - p.escala_larga_horas) * p.escala_larga_por_hora
        if horas >= 6 and _cruza_la_madrugada(llega.llegada, sale.salida):
            d.escalas_largas += p.noche_en_aeropuerto

    d.horarios += (_interpolar_hora(_PENAL_SALIDA, it.salida)
                   + _interpolar_hora(_PENAL_LLEGADA, it.llegada)) * p.escala_horarios


def costo_generalizado(
    o: Oferta, consulta: Consulta, p: Preferencias, precio_referencia: float
) -> Desglose:
    """Traduce una oferta a un único número comparable, en plata."""
    d = Desglose(precio=o.precio_comparable)

    _costo_itinerario(o.ida, o, p, d, precio_referencia)
    if o.vuelta:
        _costo_itinerario(o.vuelta, o, p, d, precio_referencia)

    if o.self_transfer:
        d.self_transfer += p.self_transfer_fijo

    km = o.desglose_precio.get("km_terrestres", 0.0)
    if km:
        ida_y_vuelta = km * 2          # hay que volver del aeropuerto también
        d.traslado_terrestre += ida_y_vuelta * p.costo_por_km
        d.traslado_terrestre += (
            (ida_y_vuelta / p.velocidad_terrestre_kmh) * p.peso_tiempo_terrestre * p.valor_hora
        )

    return d


# ── Contexto de precio: ¿está barato para esta ruta? ──────────────────────
# Va aparte del ranking a propósito. El precio ya pesa dentro del costo
# generalizado; si además se bonificara por "es un buen precio histórico", se
# estaría contando dos veces. Esto es una etiqueta para mostrar y para
# disparar alertas, no un insumo del orden.

def evaluar_precio(precio: float, historico: list[float]) -> Optional[dict]:
    """Ubica un precio contra el histórico de la ruta."""
    if not historico:
        return None
    orden = sorted(historico)
    n = len(orden)
    percentil = 100.0 * sum(1 for x in orden if x < precio) / n
    mediana = orden[n // 2]
    indice = precio / mediana if mediana else 1.0

    if percentil < 10 or indice < 0.75:
        etiqueta, texto = "excelente", "🔥 precio excelente para esta ruta"
    elif percentil < 25 or indice < 0.90:
        etiqueta, texto = "bueno", "👍 buen precio para esta ruta"
    elif percentil < 75:
        etiqueta, texto = "tipico", "precio típico para esta ruta"
    else:
        etiqueta, texto = "caro", "⚠ caro para esta ruta"

    return {
        "percentil": round(percentil, 1),
        "indice": round(indice, 3),
        "etiqueta": etiqueta,
        "texto": texto,
        "mediana": mediana,
        "p25": orden[n // 4],
        "p75": orden[(3 * n) // 4],
    }


def _motivos(o: Oferta, d: Desglose, mejor_precio: float, mejor_duracion: int) -> list[str]:
    """Etiquetas cortas que explican por qué una oferta está donde está."""
    motivos: list[str] = []

    if o.precio_comparable <= mejor_precio * 1.001:
        motivos.append("🏷 el más barato")
    elif o.precio_comparable <= mejor_precio * 1.10:
        motivos.append("🏷 a menos de 10% del más barato")

    if o.es_directo:
        motivos.append("✈ sin escalas")
    elif o.duracion_total_min <= mejor_duracion * 1.05:
        motivos.append("⏱ de los más rápidos")

    if d.precio and d.sobrecosto > d.precio * 0.5:
        motivos.append("⚠ barato en la vidriera, caro en la práctica")
    if d.riesgo_conexion > d.precio * 0.08:
        motivos.append("⚠ conexión muy justa")
    if d.cambio_aeropuerto:
        motivos.append("⚠ cambia de aeropuerto en la escala")
    if d.self_transfer:
        motivos.append("⚠ tramos separados, sin protección")
    if d.escalas_largas:
        motivos.append("⚠ espera muy larga en la escala")
    if d.traslado_terrestre:
        km = int(o.desglose_precio.get("km_terrestres", 0))
        motivos.append(f"🚗 sale de otro aeropuerto ({km} km de ida)")
    if o.equipaje.bodega_incluidas:
        motivos.append("🧳 incluye bodega")
    elif not o.equipaje.mano_incluido:
        motivos.append("🎒 sin carry-on incluido")

    contexto = o.datos_proveedor.get("evaluacion_precio")
    if contexto:
        motivos.append(contexto["texto"])

    return motivos


def rankear(
    ofertas: list[Oferta],
    consulta: Consulta,
    preferencias: Preferencias | None = None,
) -> list[Oferta]:
    """Ordena las ofertas de mejor a peor y las anota con su explicación.

    Completa `puntaje` (0 a 100, sólo para mostrar), `desglose_precio` y
    `motivos` en cada oferta, y devuelve una lista nueva ordenada por costo
    generalizado.
    """
    if not ofertas:
        return []

    p = preferencias or Preferencias.perfil("ocio")
    precios = sorted(o.precio_comparable for o in ofertas)
    # El precio de referencia de la ruta es la mediana del conjunto: sirve
    # para dimensionar la penalización por escala en rutas de $80.000 y en
    # rutas de $2.400.000 sin tocar los parámetros.
    referencia = precios[len(precios) // 2]
    mejor_precio = precios[0]
    mejor_duracion = min(o.duracion_total_min for o in ofertas) or 1

    desgloses: dict[int, Desglose] = {}
    for o in ofertas:
        d = costo_generalizado(o, consulta, p, referencia)
        desgloses[id(o)] = d
        o.desglose_precio.update(d.como_dict())

    costos = sorted(d.total for d in desgloses.values())
    minimo = costos[0]
    p75 = costos[min(len(costos) - 1, int(0.75 * len(costos)))]
    # La escala del puntaje sale de la dispersión del conjunto, no de su
    # nivel: así discrimina igual de bien en cabotaje barato que en un vuelo
    # a Europa.
    escala = max(p75 - minimo, 0.05 * minimo, 1.0)

    for o in ofertas:
        d = desgloses[id(o)]
        o.puntaje = round(100 * math.exp(-(d.total - minimo) / escala), 1)
        o.desglose_precio["diferencia_vs_mejor"] = round(d.total - minimo, 2)
        o.motivos = _motivos(o, d, mejor_precio, mejor_duracion)

    # Se ordena por costo generalizado, nunca por el puntaje de pantalla.
    return sorted(
        ofertas,
        key=lambda o: (desgloses[id(o)].total, o.precio_comparable, o.duracion_total_min),
    )


def mas_barata(ofertas: list[Oferta]) -> Oferta | None:
    return min(ofertas, key=lambda o: o.precio_comparable, default=None)


def mas_rapida(ofertas: list[Oferta]) -> Oferta | None:
    return min(ofertas, key=lambda o: o.duracion_total_min, default=None)
