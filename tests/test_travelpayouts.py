"""El proveedor barato: sirve para elegir fechas, no para cotizar."""
from datetime import date, timedelta

import pytest

from buscador.modelos import Consulta
from buscador.proveedores.base import ErrorProveedor, ProveedorSinCredenciales
from buscador.proveedores.travelpayouts import Travelpayouts, _fecha_hora

IDA = date(2026, 11, 10)
VUELTA = date(2026, 11, 24)

PRECIOS = {
    "success": True,
    "data": [
        {
            "origin": "BUE", "destination": "MAD",
            "origin_airport": "EZE", "destination_airport": "MAD",
            "price": 1_284_300, "airline": "AV", "flight_number": "84",
            "departure_at": "2026-11-10T09:15:00Z", "return_at": "2026-11-24T22:40:00Z",
            "transfers": 1, "return_transfers": 1,
            "duration_to": 1180, "duration_back": 1240,
            "link": "/search/EZE1011MAD1?t=abc",
            "expires_at": "2026-09-02T11:03:00Z",
        },
        {
            "origin": "BUE", "destination": "MAD",
            "price": 1_450_000, "airline": "IB", "flight_number": "6841",
            "departure_at": "2026-11-11T12:00:00Z",
            "transfers": 0, "duration_to": 770,
        },
    ],
}

CALENDARIO = {
    "success": True,
    "data": {
        "2026-11-10": {"price": 1_284_300},
        "2026-11-11": {"price": 1_450_000},
        "2026-11-12": {"price": 1_190_000},
        "roto": {"price": 1},
    },
}


@pytest.fixture
def consulta():
    return Consulta(origen="EZE", destino="MAD", fecha_ida=IDA, fecha_vuelta=VUELTA,
                    moneda="ARS", flex_dias=3)


@pytest.fixture
def tp():
    p = Travelpayouts()
    p.token = "token-falso"
    return p


def test_no_consume_cuota():
    # Es la razón por la que se usa para el barrido: no cobra por request.
    assert Travelpayouts.costo_por_busqueda == 0


@pytest.mark.parametrize("texto", ["2026-11-10T09:15:00Z", "2026-11-10T09:15:00"])
def test_fecha_hora_tolera_zona(texto):
    assert _fecha_hora(texto).hour == 9


class TestBuscar:
    def _ofertas(self, tp, consulta, monkeypatch, respuesta=PRECIOS):
        monkeypatch.setattr(Travelpayouts, "_get", lambda self, ruta, params: respuesta)
        return tp.buscar(consulta, "EZE", "MAD", IDA, VUELTA)

    def test_traduce_las_filas(self, tp, consulta, monkeypatch):
        ofertas = self._ofertas(tp, consulta, monkeypatch)
        assert len(ofertas) == 2
        assert ofertas[0].precio == 1_284_300
        assert ofertas[0].aerolineas == ["AV"]

    def test_marca_todo_como_indicativo(self, tp, consulta, monkeypatch):
        # Sus precios son caché de búsquedas ajenas: no se muestran como firmes.
        assert all(o.indicativo for o in self._ofertas(tp, consulta, monkeypatch))

    def test_prefiere_el_aeropuerto_al_codigo_de_ciudad(self, tp, consulta, monkeypatch):
        o = self._ofertas(tp, consulta, monkeypatch)[0]
        assert o.ida.origen == "EZE", "BUE es la ciudad; queremos el aeropuerto"

    def test_arma_la_vuelta_cuando_viene(self, tp, consulta, monkeypatch):
        con, sin = self._ofertas(tp, consulta, monkeypatch)
        assert con.vuelta is not None and con.vuelta.origen == "MAD"
        assert sin.vuelta is None

    def test_conserva_las_escalas_reales(self, tp, consulta, monkeypatch):
        # El itinerario que arma es aproximado; la cantidad real de escalas se
        # guarda aparte para no mentir.
        o = self._ofertas(tp, consulta, monkeypatch)[0]
        assert o.datos_proveedor["escalas_ida"] == 1
        assert o.datos_proveedor["itinerario_estimado"]

    def test_arma_el_link_de_reserva(self, tp, consulta, monkeypatch):
        o = self._ofertas(tp, consulta, monkeypatch)[0]
        assert o.url_reserva.startswith("https://www.aviasales.com/search/")

    def test_descarta_filas_sin_precio_o_sin_fecha(self, tp, consulta, monkeypatch):
        respuesta = {"success": True, "data": [
            {"price": 0, "departure_at": "2026-11-10T09:15:00Z"},
            {"price": 100, "departure_at": "no es una fecha"},
            {"departure_at": "2026-11-10T09:15:00Z"},
        ]}
        assert self._ofertas(tp, consulta, monkeypatch, respuesta) == []

    def test_tolera_la_forma_vieja_de_diccionario(self, tp, consulta, monkeypatch):
        viejo = {"success": True, "data": {"2026-11-10": PRECIOS["data"][0]}}
        assert len(self._ofertas(tp, consulta, monkeypatch, viejo)) == 1


class TestCalendario:
    def test_devuelve_precio_minimo_por_dia(self, tp, consulta, monkeypatch):
        monkeypatch.setattr(Travelpayouts, "_get", lambda self, ruta, params: CALENDARIO)
        cal = tp.fechas_mas_baratas(consulta, "EZE", "MAD")
        assert cal == {
            date(2026, 11, 10): 1_284_300.0,
            date(2026, 11, 11): 1_450_000.0,
            date(2026, 11, 12): 1_190_000.0,
        }

    def test_si_falla_devuelve_vacio_y_la_busqueda_sigue(self, tp, consulta, monkeypatch):
        def explota(self, ruta, params):
            raise ErrorProveedor("no disponible para esta ruta")

        monkeypatch.setattr(Travelpayouts, "_get", explota)
        assert tp.fechas_mas_baratas(consulta, "EZE", "MAD") == {}

    def test_pide_el_mes_completo(self, tp, consulta, monkeypatch):
        capturado = {}
        monkeypatch.setattr(Travelpayouts, "_get",
                            lambda self, ruta, params: capturado.update(params) or CALENDARIO)
        tp.fechas_mas_baratas(consulta, "EZE", "MAD")
        assert capturado["depart_date"] == "2026-11"
        assert capturado["calendar_type"] == "departure_date"
        assert capturado["currency"] == "ars"


class TestCredenciales:
    def test_sin_token_no_esta_disponible(self, monkeypatch):
        monkeypatch.delenv("TRAVELPAYOUTS_TOKEN", raising=False)
        assert not Travelpayouts().disponible()

    def test_sin_token_el_error_dice_qué_falta(self, monkeypatch):
        monkeypatch.delenv("TRAVELPAYOUTS_TOKEN", raising=False)
        with pytest.raises(ProveedorSinCredenciales, match="TRAVELPAYOUTS_TOKEN"):
            Travelpayouts()._get("/x", {})

    def test_token_invalido_se_explica(self, tp, monkeypatch):
        class Respuesta:
            status_code = 401

        monkeypatch.setattr(tp.sesion, "get", lambda *a, **k: Respuesta())
        with pytest.raises(ErrorProveedor, match="inválido"):
            tp._get("/x", {})
