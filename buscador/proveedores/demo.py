"""Proveedor de demostración: genera ofertas verosímiles sin salir a internet.

Existe para dos cosas: probar el pipeline completo (ranking, impuestos,
reportes) sin gastar cuota de API, y para que el agente sea usable el primer
día, antes de que el usuario saque sus credenciales. Los precios son
sintéticos pero deterministas por ruta+fecha, así que las corridas se pueden
comparar entre sí.

NUNCA se usa si hay un proveedor real disponible, salvo que se pida explícito.
"""
from __future__ import annotations

import hashlib
import random
from datetime import date, datetime, time, timedelta
from typing import Optional

from buscador.aeropuertos import distancia_km
from buscador.modelos import Consulta, Equipaje, Itinerario, Oferta, Segmento
from buscador.proveedores.base import Proveedor

# Aerolíneas con presencia real en las rutas argentinas, con su perfil tarifario.
# (código, nombre, factor de precio, es_low_cost)
_AEROLINEAS = [
    ("AR", "Aerolíneas Argentinas", 1.00, False),
    ("FO", "Flybondi", 0.68, True),
    ("WJ", "JetSmart", 0.70, True),
    ("LA", "LATAM", 1.05, False),
    ("CM", "Copa Airlines", 1.12, False),
    ("AV", "Avianca", 1.08, False),
]

_HUBS = ["AEP", "EZE", "COR", "GRU", "SCL", "PTY", "LIM", "BOG"]


def _es_desvio_razonable(origen: str, hub: str, destino: str, tolerancia: float = 1.6) -> bool:
    """Descarta escalas absurdas (un Buenos Aires-Bariloche vía Bogotá).

    Una conexión real casi nunca alarga el recorrido más allá de ~60% sobre
    la ruta directa.
    """
    directo = distancia_km(origen, destino)
    ida = distancia_km(origen, hub)
    vuelta = distancia_km(hub, destino)
    if not directo or ida is None or vuelta is None:
        return True
    # Un hub en la misma ciudad que la punta no es una escala, es un traslado.
    if ida < 100 or vuelta < 100:
        return False
    return (ida + vuelta) <= directo * tolerancia + 300


class Demo(Proveedor):
    nombre = "demo"
    costo_por_busqueda = 0

    def disponible(self) -> bool:
        # Siempre "disponible", pero el orquestador lo deja último y sólo lo
        # usa como red de seguridad cuando no hay ningún proveedor real.
        return True

    def _rng(self, origen: str, destino: str, fecha: date) -> random.Random:
        semilla = hashlib.sha256(f"{origen}{destino}{fecha}".encode()).hexdigest()
        return random.Random(int(semilla[:16], 16))

    def _precio_base_usd(self, origen: str, destino: str, rng: random.Random) -> float:
        km = distancia_km(origen, destino) or 1200.0
        # Tarifa aérea típica: costo fijo por operar + costo por distancia,
        # con rendimientos decrecientes en rutas largas.
        base = 45 + (km ** 0.82) * 0.32
        return base * rng.uniform(0.85, 1.25)

    def _armar_itinerario(
        self,
        origen: str,
        destino: str,
        dia: date,
        escalas: int,
        aerolinea: str,
        rng: random.Random,
    ) -> Itinerario:
        km = distancia_km(origen, destino) or 1200.0
        # ~800 km/h de crucero + 40 min de rodaje, despegue y aproximación.
        vuelo_min = int(km / 800 * 60) + 40

        hora_salida = time(hour=rng.choice([6, 7, 9, 11, 13, 15, 17, 19, 21, 23]),
                           minute=rng.choice([0, 5, 15, 25, 35, 40, 50]))
        cursor = datetime.combine(dia, hora_salida)

        if escalas == 0:
            llegada = cursor + timedelta(minutes=vuelo_min)
            return Itinerario([
                Segmento(origen, destino, cursor, llegada, aerolinea,
                         numero_vuelo=f"{aerolinea}{rng.randint(1000, 1999)}")
            ])

        segmentos: list[Segmento] = []
        puntos = [origen]
        for _ in range(escalas):
            candidatos = [
                h for h in _HUBS
                if h not in (origen, destino) and h not in puntos and _es_desvio_razonable(origen, h, destino)
            ]
            if not candidatos:
                candidatos = [h for h in _HUBS if h not in (origen, destino) and h not in puntos]
            puntos.append(rng.choice(candidatos) if candidatos else "GRU")
        puntos.append(destino)

        # El desvío por la escala agrega distancia: repartimos el vuelo total
        # con un 25% de recargo sobre el tiempo del directo.
        tramo_min = int(vuelo_min * 1.25 / (escalas + 1))
        for i in range(len(puntos) - 1):
            if i > 0:
                cursor += timedelta(minutes=rng.choice([65, 85, 110, 140, 190, 260, 420]))
            llegada = cursor + timedelta(minutes=tramo_min)
            segmentos.append(
                Segmento(puntos[i], puntos[i + 1], cursor, llegada, aerolinea,
                         numero_vuelo=f"{aerolinea}{rng.randint(1000, 1999)}")
            )
            cursor = llegada
        return Itinerario(segmentos)

    def buscar(
        self,
        consulta: Consulta,
        origen: str,
        destino: str,
        fecha_ida: date,
        fecha_vuelta: Optional[date],
        limite: int = 20,
    ) -> list[Oferta]:
        rng = self._rng(origen, destino, fecha_ida)
        base_usd = self._precio_base_usd(origen, destino, rng)

        # Los fines de semana y la temporada alta empujan la tarifa.
        if fecha_ida.weekday() in (4, 6):
            base_usd *= 1.18
        if fecha_ida.month in (1, 2, 7, 12):
            base_usd *= 1.22
        # Comprar con poca antelación se paga.
        dias_antelacion = (fecha_ida - date.today()).days
        if dias_antelacion < 14:
            base_usd *= 1.35
        elif dias_antelacion < 30:
            base_usd *= 1.12

        ofertas: list[Oferta] = []
        for codigo, _nombre, factor, low_cost in _AEROLINEAS:
            for escalas in (0, 1, 2):
                if rng.random() > (0.9 if escalas == 0 else 0.6):
                    continue
                # Cada escala abarata: es el descuento por incomodidad.
                precio_usd = base_usd * factor * (1 - 0.13 * escalas) * rng.uniform(0.92, 1.15)
                ida = self._armar_itinerario(origen, destino, fecha_ida, escalas, codigo, rng)
                vuelta = None
                if fecha_vuelta:
                    vuelta = self._armar_itinerario(destino, origen, fecha_vuelta, escalas, codigo, rng)
                    precio_usd *= 1.85  # el roundtrip rinde algo mejor que 2 one-way

                ofertas.append(
                    Oferta(
                        proveedor=self.nombre,
                        precio=round(precio_usd * consulta.pasajeros, 2),
                        moneda="USD",
                        ida=ida,
                        vuelta=vuelta,
                        equipaje=Equipaje(
                            mano_incluido=not low_cost,
                            bodega_incluidas=0 if low_cost else 1,
                        ),
                        cabina=consulta.cabina,
                        asientos_restantes=rng.choice([None, 1, 2, 4, 9]),
                        id_externo=f"demo-{codigo}-{fecha_ida}-{escalas}",
                        url_reserva="",
                    )
                )
        ofertas.sort(key=lambda o: o.precio)
        return ofertas[:limite]
