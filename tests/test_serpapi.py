"""Tests del proveedor primario, con una respuesta real de google_flights."""
import copy
from datetime import date, timedelta

import pytest

from buscador.modelos import Consulta
from buscador.proveedores.base import ErrorProveedor, ProveedorSinCredenciales
from buscador.proveedores.serpapi import SerpApi, _partir_numero_de_vuelo

IDA = date.today() + timedelta(days=60)
VUELTA = IDA + timedelta(days=14)

# Recorte de una respuesta de engine=google_flights con currency=ARS y gl=ar:
# una opción de Aerolíneas directa y una de Flybondi con escala.
RESPUESTA = {
    "best_flights": [
        {
            "flights": [
                {
                    "departure_airport": {"name": "Aeroparque", "id": "AEP",
                                          "time": "2026-11-10 13:55"},
                    "arrival_airport": {"name": "Bariloche", "id": "BRC",
                                        "time": "2026-11-10 16:15"},
                    "duration": 140, "airplane": "Boeing 737",
                    "airline": "Aerolíneas Argentinas", "flight_number": "AR 1132",
                    "travel_class": "Economy",
                }
            ],
            "layovers": [],
            "total_duration": 140,
            "price": 285400,
            "type": "Round trip",
            "booking_token": "WyJDalJJIiwiYWJjIl0=",
            "departure_token": "WyJDalJJZGVwIl0=",
        }
    ],
    "other_flights": [
        {
            "flights": [
                {
                    "departure_airport": {"id": "AEP", "time": "2026-11-10 06:10"},
                    "arrival_airport": {"id": "COR", "time": "2026-11-10 07:30"},
                    "duration": 80, "airline": "Flybondi", "flight_number": "FO 5210",
                    "travel_class": "Economy",
                },
                {
                    "departure_airport": {"id": "COR", "time": "2026-11-10 09:05"},
                    "arrival_airport": {"id": "BRC", "time": "2026-11-10 11:00"},
                    "duration": 115, "airline": "Flybondi", "flight_number": "FO 5330",
                    "travel_class": "Economy",
                },
            ],
            "layovers": [{"duration": 95, "name": "Córdoba", "id": "COR"}],
            "total_duration": 290,
            "price": 214900,
            "type": "Round trip",
            "booking_token": "WyJDalJJIiwiZGVmIl0=",
        }
    ],
    "price_insights": {
        "lowest_price": 214900,
        "price_level": "low",
        "typical_price_range": [230000, 390000],
    },
}


@pytest.fixture
def consulta():
    return Consulta(origen="AEP", destino="BRC", fecha_ida=IDA, fecha_vuelta=VUELTA,
                    moneda="ARS")


@pytest.fixture
def serpapi():
    p = SerpApi()
    p.api_key = "clave-falsa"
    return p


@pytest.mark.parametrize("texto,esperado", [
    ("AR 1132", ("AR", "1132")),
    ("FO 5210", ("FO", "5210")),
    ("LA800", ("LA", "800")),
    ("", ("", "")),
])
def test_partir_numero_de_vuelo(texto, esperado):
    assert _partir_numero_de_vuelo(texto) == esperado


class TestTraduccion:
    def _ofertas(self, serpapi, consulta, monkeypatch, respuesta=RESPUESTA):
        monkeypatch.setattr(SerpApi, "_pedir", lambda self, params: respuesta)
        return serpapi.buscar(consulta, "AEP", "BRC", IDA, VUELTA)

    def test_toma_los_dos_grupos_de_google(self, serpapi, consulta, monkeypatch):
        # `best_flights` es la selección de Google; nuestro ranking decide solo.
        ofertas = self._ofertas(serpapi, consulta, monkeypatch)
        assert len(ofertas) == 2
        assert {o.precio for o in ofertas} == {285400, 214900}

    def test_arma_el_itinerario_con_escalas(self, serpapi, consulta, monkeypatch):
        con_escala = [o for o in self._ofertas(serpapi, consulta, monkeypatch)
                      if o.escalas_totales][0]
        assert con_escala.ida.origen == "AEP" and con_escala.ida.destino == "BRC"
        assert con_escala.ida.escalas == 1
        assert con_escala.ida.layovers_min == [95]
        assert con_escala.aerolineas == ["FO"]

    def test_usa_la_moneda_que_se_pidio(self, serpapi, consulta, monkeypatch):
        assert all(o.moneda == "ARS" for o in self._ofertas(serpapi, consulta, monkeypatch))

    def test_deduce_el_equipaje_de_la_aerolinea(self, serpapi, consulta, monkeypatch):
        # Google Flights no informa franquicia; sin esto, la comparación miente.
        ofertas = {o.aerolineas[0]: o for o in self._ofertas(serpapi, consulta, monkeypatch)}
        assert ofertas["AR"].equipaje.mano_incluido
        assert not ofertas["FO"].equipaje.mano_incluido

    def test_guarda_el_contexto_de_precio(self, serpapi, consulta, monkeypatch):
        o = self._ofertas(serpapi, consulta, monkeypatch)[0]
        assert o.datos_proveedor["contexto_precio"]["price_level"] == "low"

    def test_marca_que_falta_el_tramo_de_vuelta(self, serpapi, consulta, monkeypatch):
        # En ida y vuelta Google devuelve primero sólo la ida, con el precio
        # total del viaje. El detalle de la vuelta cuesta otro request.
        o = self._ofertas(serpapi, consulta, monkeypatch)[0]
        assert o.datos_proveedor["falta_tramo_de_vuelta"]
        assert o.vuelta is None

    def test_en_solo_ida_no_marca_nada_pendiente(self, serpapi, consulta, monkeypatch):
        monkeypatch.setattr(SerpApi, "_pedir", lambda self, params: RESPUESTA)
        o = serpapi.buscar(consulta, "AEP", "BRC", IDA, None)[0]
        assert not o.datos_proveedor["falta_tramo_de_vuelta"]

    def test_descarta_itinerarios_rotos_sin_perder_los_buenos(self, serpapi, consulta, monkeypatch):
        r = copy.deepcopy(RESPUESTA)
        r["best_flights"].insert(0, {"flights": [], "price": 1})
        r["other_flights"].append({
            "flights": [{"departure_airport": {"id": "AEP"}, "arrival_airport": {"id": "BRC"}}],
            "price": 99,
        })
        assert len(self._ofertas(serpapi, consulta, monkeypatch, r)) == 2

    def test_respuesta_sin_vuelos_devuelve_lista_vacia(self, serpapi, consulta, monkeypatch):
        assert self._ofertas(serpapi, consulta, monkeypatch, {}) == []

    def test_respeta_el_limite(self, serpapi, consulta, monkeypatch):
        monkeypatch.setattr(SerpApi, "_pedir", lambda self, params: RESPUESTA)
        assert len(serpapi.buscar(consulta, "AEP", "BRC", IDA, VUELTA, limite=1)) == 1


class TestParametros:
    def _params(self, serpapi, consulta, monkeypatch, **kw):
        capturado = {}

        def fake(self, params):
            capturado.update(params)
            return {}

        monkeypatch.setattr(SerpApi, "_pedir", fake)
        serpapi.buscar(consulta, kw.get("origen", "AEP"), "BRC", IDA,
                       kw.get("vuelta", VUELTA))
        return capturado

    def test_pide_el_mercado_argentino_y_pesos(self, serpapi, consulta, monkeypatch):
        p = self._params(serpapi, consulta, monkeypatch)
        assert p["engine"] == "google_flights"
        assert p["gl"] == "ar" and p["hl"] == "es"
        assert p["currency"] == "ARS"
        assert p["sort_by"] == 2

    def test_ida_y_vuelta_vs_solo_ida(self, serpapi, consulta, monkeypatch):
        assert self._params(serpapi, consulta, monkeypatch)["type"] == "1"
        p = self._params(serpapi, consulta, monkeypatch, vuelta=None)
        assert p["type"] == "2" and "return_date" not in p

    def test_solo_directos(self, serpapi, consulta, monkeypatch):
        consulta.solo_directos = True
        assert self._params(serpapi, consulta, monkeypatch)["stops"] == 1

    def test_max_escalas_se_traduce_al_codigo_de_google(self, serpapi, consulta, monkeypatch):
        consulta.max_escalas = 1
        assert self._params(serpapi, consulta, monkeypatch)["stops"] == 2

    def test_infantes_van_en_falda(self, serpapi, consulta, monkeypatch):
        consulta.infantes = 1
        p = self._params(serpapi, consulta, monkeypatch)
        assert p["infants_on_lap"] == 1 and p["infants_in_seat"] == 0

    def test_excluye_aerolineas(self, serpapi, consulta, monkeypatch):
        consulta.aerolineas_excluidas = ["FO", "JA"]
        assert self._params(serpapi, consulta, monkeypatch)["exclude_airlines"] == "FO,JA"


class TestErrores:
    def test_sin_clave_no_esta_disponible(self, monkeypatch):
        monkeypatch.delenv("SERPAPI_KEY", raising=False)
        assert not SerpApi().disponible()

    def test_sin_clave_el_error_dice_qué_falta(self, monkeypatch):
        monkeypatch.delenv("SERPAPI_KEY", raising=False)
        with pytest.raises(ProveedorSinCredenciales, match="SERPAPI_KEY"):
            SerpApi()._pedir({})

    def test_cuota_agotada_se_explica(self, serpapi, monkeypatch):
        class Respuesta:
            status_code = 429

        monkeypatch.setattr(serpapi.sesion, "get", lambda *a, **k: Respuesta())
        with pytest.raises(ErrorProveedor, match="250 búsquedas"):
            serpapi._pedir({})

    def test_sin_resultados_no_es_un_error(self, serpapi, monkeypatch):
        class Respuesta:
            status_code = 200

            def json(self):
                return {"error": "Google Flights hasn't returned any results for this query."}

        monkeypatch.setattr(serpapi.sesion, "get", lambda *a, **k: Respuesta())
        assert serpapi._pedir({}) == {}


class TestCompletarVuelta:
    def test_completa_el_tramo_y_el_precio(self, serpapi, consulta, monkeypatch):
        monkeypatch.setattr(SerpApi, "_pedir", lambda self, params: RESPUESTA)
        oferta = serpapi.buscar(consulta, "AEP", "BRC", IDA, VUELTA)[0]
        assert oferta.vuelta is None

        vuelta = {
            "best_flights": [{
                "flights": [{
                    "departure_airport": {"id": "BRC", "time": "2026-11-24 18:00"},
                    "arrival_airport": {"id": "AEP", "time": "2026-11-24 20:20"},
                    "duration": 140, "airline": "Aerolíneas Argentinas",
                    "flight_number": "AR 1133", "travel_class": "Economy",
                }],
                "layovers": [], "price": 291000, "booking_token": "final",
            }]
        }
        monkeypatch.setattr(SerpApi, "_pedir", lambda self, params: vuelta)
        completa = serpapi.completar_vuelta(oferta, consulta)

        assert completa.vuelta is not None
        assert completa.vuelta.origen == "BRC" and completa.vuelta.destino == "AEP"
        assert completa.precio == 291000
        assert not completa.datos_proveedor["falta_tramo_de_vuelta"]

    def test_si_falla_la_oferta_vuelve_intacta(self, serpapi, consulta, monkeypatch):
        monkeypatch.setattr(SerpApi, "_pedir", lambda self, params: RESPUESTA)
        oferta = serpapi.buscar(consulta, "AEP", "BRC", IDA, VUELTA)[0]
        precio = oferta.precio

        def explota(self, params):
            raise ErrorProveedor("se cayó")

        monkeypatch.setattr(SerpApi, "_pedir", explota)
        assert serpapi.completar_vuelta(oferta, consulta).precio == precio

    def test_no_gasta_un_request_si_ya_esta_completa(self, serpapi, consulta, monkeypatch):
        monkeypatch.setattr(SerpApi, "_pedir", lambda self, params: RESPUESTA)
        oferta = serpapi.buscar(consulta, "AEP", "BRC", IDA, None)[0]
        oferta.datos_proveedor["departure_token"] = ""

        def no_deberia_llamarse(self, params):
            raise AssertionError("no hay que gastar un crédito acá")

        monkeypatch.setattr(SerpApi, "_pedir", no_deberia_llamarse)
        serpapi.completar_vuelta(oferta, consulta)
