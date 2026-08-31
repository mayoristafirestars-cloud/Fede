"""Proveedor SerpApi — motor `google_flights`.

Es el proveedor primario porque es el único de acceso self-service que ve el
mercado argentino completo: Flybondi y JetSmart (que no publican en ningún
GDS) aparecen en Google Flights, y la API devuelve precios nativos en pesos
con `currency=ARS&gl=ar`. Cualquier búsqueda de cabotaje argentino que
ignore a las low-cost da una respuesta directamente equivocada.

Además trae `price_insights`, que es lo que permite decir "este precio está
barato para esta ruta" en vez de tirar un número sin contexto.

Dos cosas a tener en cuenta:

- El plan gratuito son 250 búsquedas por mes (~8 por día). El orquestador
  respeta un presupuesto de requests y la caché en disco evita repetir.
- En ida y vuelta, Google devuelve primero los tramos de IDA con el precio
  total del viaje; el tramo de vuelta se pide en una segunda llamada con el
  `departure_token`. Eso cuesta otro crédito, así que sólo se completa para
  las mejores opciones y bajo pedido explícito.
"""
from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Any, Optional

import requests

from buscador.config import env, env_int
from buscador.equipaje_ar import equipaje_de_tarifa_base
from buscador.modelos import Consulta, Itinerario, Oferta, Segmento
from buscador.proveedores.base import ErrorProveedor, Proveedor, ProveedorSinCredenciales

log = logging.getLogger(__name__)

_URL = "https://serpapi.com/search"

#: Google Flights informa los horarios en hora local de cada aeropuerto.
_FORMATO_HORA = "%Y-%m-%d %H:%M"

_TIPO_VIAJE = {"ida_vuelta": "1", "ida": "2"}

_CLASE = {"ECONOMY": 1, "PREMIUM_ECONOMY": 2, "BUSINESS": 3, "FIRST": 4}


def _hora(texto: str) -> datetime:
    return datetime.strptime(texto.strip(), _FORMATO_HORA)


def _partir_numero_de_vuelo(texto: str) -> tuple[str, str]:
    """'AR 1132' -> ('AR', '1132'). Tolera formatos sin espacio."""
    texto = (texto or "").strip()
    if " " in texto:
        codigo, _, numero = texto.partition(" ")
        return codigo.strip(), numero.strip()
    for i, c in enumerate(texto):
        if c.isdigit():
            return texto[:i], texto[i:]
    return texto, ""


class SerpApi(Proveedor):
    nombre = "serpapi"
    costo_por_busqueda = 1

    def __init__(self) -> None:
        self.api_key = env("SERPAPI_KEY")
        self.pais = env("SERPAPI_GL", "ar")
        self.idioma = env("SERPAPI_HL", "es")
        self.deep_search = env("SERPAPI_DEEP_SEARCH", "true").lower() in {"1", "true", "si", "sí"}
        self.timeout = env_int("SERPAPI_TIMEOUT", 60)
        self.sesion = requests.Session()

    def disponible(self) -> bool:
        return bool(self.api_key)

    # ── HTTP ───────────────────────────────────────────────────────────────
    def _pedir(self, params: dict[str, Any]) -> dict:
        if not self.disponible():
            raise ProveedorSinCredenciales("falta SERPAPI_KEY")

        params = {**params, "api_key": self.api_key}
        try:
            r = self.sesion.get(_URL, params=params, timeout=self.timeout)
        except requests.RequestException as e:
            raise ErrorProveedor(f"error de red: {e}") from e

        if r.status_code == 401:
            raise ErrorProveedor("SERPAPI_KEY inválida o vencida")
        if r.status_code == 429:
            raise ErrorProveedor(
                "cuota de SerpApi agotada (250 búsquedas/mes en el plan gratuito, "
                "50 por hora)"
            )
        if r.status_code >= 400:
            raise ErrorProveedor(f"HTTP {r.status_code}")

        datos = r.json()
        if datos.get("error"):
            # SerpApi devuelve 200 con "error" cuando simplemente no hay vuelos.
            mensaje = str(datos["error"])
            if "hasn't returned any results" in mensaje.lower():
                return {}
            raise ErrorProveedor(mensaje)
        return datos

    # ── Traducción ─────────────────────────────────────────────────────────
    def _segmento(self, tramo: dict) -> Segmento:
        aerolinea, numero = _partir_numero_de_vuelo(tramo.get("flight_number", ""))
        return Segmento(
            origen=tramo["departure_airport"]["id"],
            destino=tramo["arrival_airport"]["id"],
            salida=_hora(tramo["departure_airport"]["time"]),
            llegada=_hora(tramo["arrival_airport"]["time"]),
            aerolinea=aerolinea,
            numero_vuelo=numero,
            aeronave=tramo.get("airplane", ""),
            duracion_min=int(tramo.get("duration") or 0),
        )

    def _a_oferta(
        self,
        cruda: dict,
        consulta: Consulta,
        insights: dict,
        es_ida_y_vuelta: bool,
    ) -> Optional[Oferta]:
        tramos = cruda.get("flights") or []
        if not tramos:
            return None

        segmentos = [self._segmento(t) for t in tramos]
        precio = cruda.get("price")
        if precio is None:
            return None

        cabina = (tramos[0].get("travel_class") or "").upper().replace(" ", "_") or consulta.cabina

        oferta = Oferta(
            proveedor=self.nombre,
            # Google devuelve el precio total del viaje para el conjunto de
            # pasajeros que se le pidió, ya con tasas e impuestos del ticket.
            precio=float(precio),
            moneda=consulta.moneda,
            ida=Itinerario(segmentos),
            vuelta=None,
            cabina=cabina if cabina in _CLASE else consulta.cabina,
            id_externo=str(cruda.get("booking_token", ""))[:64],
        )
        # Google Flights no informa la franquicia de equipaje, así que la
        # deducimos de la aerolínea y la ruta. Es la diferencia entre comparar
        # precios y comparar viajes.
        oferta.equipaje = equipaje_de_tarifa_base(
            oferta.ida.aerolineas[0] if oferta.ida.aerolineas else "",
            internacional=_es_internacional(oferta.ida),
        )
        oferta.datos_proveedor = {
            "departure_token": cruda.get("departure_token", ""),
            "booking_token": cruda.get("booking_token", ""),
            "falta_tramo_de_vuelta": bool(es_ida_y_vuelta),
            "escalas_google": [
                {"aeropuerto": l.get("id"), "minutos": l.get("duration"),
                 "nocturna": bool(l.get("overnight"))}
                for l in (cruda.get("layovers") or [])
            ],
        }
        if insights:
            oferta.datos_proveedor["contexto_precio"] = insights
        return oferta

    def _parsear(self, datos: dict, consulta: Consulta, es_ida_y_vuelta: bool) -> list[Oferta]:
        insights = datos.get("price_insights") or {}
        ofertas: list[Oferta] = []
        # `best_flights` es la selección de Google; `other_flights` es el resto.
        # Nos quedamos con ambas: nuestro ranking es el que decide, no el de ellos.
        for grupo in ("best_flights", "other_flights"):
            for cruda in datos.get(grupo) or []:
                try:
                    o = self._a_oferta(cruda, consulta, insights, es_ida_y_vuelta)
                except (KeyError, ValueError, TypeError) as e:
                    log.debug("itinerario de serpapi ilegible, se descarta: %s", e)
                    continue
                if o and o.precio > 0:
                    ofertas.append(o)
        return ofertas

    # ── API pública ────────────────────────────────────────────────────────
    def buscar(
        self,
        consulta: Consulta,
        origen: str,
        destino: str,
        fecha_ida: date,
        fecha_vuelta: Optional[date],
        limite: int = 20,
    ) -> list[Oferta]:
        params: dict[str, Any] = {
            "engine": "google_flights",
            "departure_id": origen.upper(),
            "arrival_id": destino.upper(),
            "outbound_date": fecha_ida.isoformat(),
            "type": _TIPO_VIAJE["ida_vuelta" if fecha_vuelta else "ida"],
            "currency": consulta.moneda,
            "gl": self.pais,
            "hl": self.idioma,
            "adults": consulta.adultos,
            "travel_class": _CLASE.get(consulta.cabina, 1),
            "sort_by": 2,          # 2 = por precio
        }
        if fecha_vuelta:
            params["return_date"] = fecha_vuelta.isoformat()
        if consulta.ninos:
            params["children"] = consulta.ninos
        if consulta.infantes:
            # Google separa infantes en falda y en asiento; sin más datos,
            # asumimos en falda, que es lo habitual y lo más barato.
            params["infants_in_seat"] = 0
            params["infants_on_lap"] = consulta.infantes
        if consulta.solo_directos:
            params["stops"] = 1
        elif consulta.max_escalas == 1:
            params["stops"] = 2
        elif consulta.max_escalas == 2:
            params["stops"] = 3
        if consulta.aerolineas_excluidas:
            params["exclude_airlines"] = ",".join(consulta.aerolineas_excluidas)
        if consulta.precio_max:
            params["max_price"] = int(consulta.precio_max)
        if self.deep_search:
            params["deep_search"] = "true"

        datos = self._pedir(params)
        if not datos:
            return []
        return self._parsear(datos, consulta, es_ida_y_vuelta=bool(fecha_vuelta))[:limite]

    def completar_vuelta(self, oferta: Oferta, consulta: Consulta) -> Oferta:
        """Pide el tramo de vuelta de una oferta de ida y vuelta.

        Cuesta un request extra, así que se llama sólo para las opciones que
        el usuario realmente está mirando. Si falla, la oferta vuelve intacta:
        el precio ya es el del viaje completo, lo único que falta es el detalle
        de horarios de la vuelta.
        """
        token = oferta.datos_proveedor.get("departure_token")
        if not token or oferta.vuelta is not None:
            return oferta

        params = {
            "engine": "google_flights",
            "departure_id": oferta.ida.origen,
            "arrival_id": oferta.ida.destino,
            "outbound_date": oferta.ida.salida.date().isoformat(),
            "return_date": consulta.fecha_vuelta.isoformat() if consulta.fecha_vuelta else "",
            "type": "1",
            "currency": consulta.moneda,
            "gl": self.pais,
            "hl": self.idioma,
            "adults": consulta.adultos,
            "departure_token": token,
        }
        try:
            datos = self._pedir(params)
        except ErrorProveedor as e:
            log.debug("no se pudo completar el tramo de vuelta: %s", e)
            return oferta

        candidatas = self._parsear(datos, consulta, es_ida_y_vuelta=False)
        if not candidatas:
            return oferta

        # Google ya devuelve el precio total con cada opción de vuelta elegida;
        # nos quedamos con la más barata, que es la que sostiene el precio
        # mostrado en el listado.
        mejor = min(candidatas, key=lambda o: o.precio)
        oferta.vuelta = mejor.ida
        oferta.precio = mejor.precio
        oferta.datos_proveedor["falta_tramo_de_vuelta"] = False
        oferta.datos_proveedor["booking_token"] = mejor.datos_proveedor.get("booking_token", "")
        return oferta


def _es_internacional(it: Itinerario) -> bool:
    from buscador.aeropuertos import AEROPUERTOS

    paises = set()
    for s in it.segmentos:
        for codigo in (s.origen, s.destino):
            ap = AEROPUERTOS.get(codigo)
            if ap:
                paises.add(ap.pais)
    return len(paises) > 1
