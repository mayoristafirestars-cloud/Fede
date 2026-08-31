"""Tests de la línea de comandos."""
import json
from datetime import date, timedelta

import pytest

from buscador.cli import construir_parser, main, parsear_fecha, resolver_aeropuerto

HOY = date(2026, 8, 31)


class TestParseoDeFechas:
    @pytest.mark.parametrize("texto,esperado", [
        ("2026-10-15", date(2026, 10, 15)),
        ("15/10/2026", date(2026, 10, 15)),
        ("15-10-2026", date(2026, 10, 15)),
        ("15/10", date(2026, 10, 15)),
        ("hoy", HOY),
        ("mañana", date(2026, 9, 1)),
        ("+45d", date(2026, 10, 15)),
    ])
    def test_formatos_aceptados(self, texto, esperado):
        assert parsear_fecha(texto, referencia=HOY) == esperado

    def test_dia_y_mes_ya_pasados_saltan_al_ano_siguiente(self):
        # Pedir "15/03" el 31 de agosto significa marzo del año que viene.
        assert parsear_fecha("15/03", referencia=HOY) == date(2027, 3, 15)

    def test_fecha_ininteligible_da_un_error_util(self):
        with pytest.raises(Exception, match="no entiendo la fecha"):
            parsear_fecha("el martes que viene", referencia=HOY)


class TestResolucionDeAeropuertos:
    def test_codigo_iata(self):
        assert resolver_aeropuerto("brc") == "BRC"

    def test_nombre_de_ciudad(self):
        assert resolver_aeropuerto("bariloche") == "BRC"

    def test_ciudad_con_acento(self):
        assert resolver_aeropuerto("cordoba") == "COR"

    def test_ciudad_con_varios_aeropuertos_avisa(self, capsys):
        assert resolver_aeropuerto("buenos aires") in {"AEP", "EZE"}
        assert "coincide con varios" in capsys.readouterr().err

    def test_desconocido_falla_con_una_explicación(self):
        with pytest.raises(SystemExit, match="IATA"):
            resolver_aeropuerto("narnia")


class TestParser:
    def test_origen_y_destino_son_obligatorios(self):
        with pytest.raises(SystemExit):
            construir_parser().parse_args([])

    def test_la_ida_es_obligatoria(self):
        with pytest.raises(SystemExit):
            construir_parser().parse_args(["AEP", "BRC"])

    def test_valores_por_defecto_sensatos(self):
        a = construir_parser().parse_args(["AEP", "BRC", "--ida", "15/10"])
        assert a.adultos == 1 and a.flex == 0 and a.perfil == "ocio"
        assert a.pago == "tarjeta" and a.moneda == "ARS"

    def test_perfil_invalido_se_rechaza(self):
        with pytest.raises(SystemExit):
            construir_parser().parse_args(["AEP", "BRC", "--ida", "15/10",
                                           "--perfil", "inventado"])


class TestEjecucion:
    """Se corre contra el proveedor demo: sin red, sin credenciales, sin cuota."""

    def _correr(self, argv, monkeypatch, capsys):
        monkeypatch.setenv("USD_ARS", "1500")
        codigo = main(argv + ["--proveedor", "demo", "--sin-color"])
        return codigo, capsys.readouterr().out

    def test_busqueda_basica(self, monkeypatch, capsys):
        codigo, salida = self._correr(
            ["AEP", "BRC", "--ida", "+60d", "--vuelta", "+67d"], monkeypatch, capsys)
        assert codigo == 0
        assert "MEJOR OPCIÓN" in salida
        assert "Bariloche" in salida

    def test_solo_ida(self, monkeypatch, capsys):
        codigo, salida = self._correr(["AEP", "BRC", "--ida", "+60d"], monkeypatch, capsys)
        assert codigo == 0
        assert "VUELTA" not in salida

    def test_vuelta_anterior_a_la_ida_se_rechaza(self, monkeypatch):
        monkeypatch.setenv("USD_ARS", "1500")
        with pytest.raises(SystemExit, match="anterior"):
            main(["AEP", "BRC", "--ida", "+60d", "--vuelta", "+30d", "--proveedor", "demo"])

    def test_salida_json_es_json_valido(self, monkeypatch, capsys):
        codigo, salida = self._correr(
            ["AEP", "BRC", "--ida", "+60d", "--json"], monkeypatch, capsys)
        datos = json.loads(salida)
        assert codigo == 0
        assert datos["consulta"]["origen"] == "AEP"
        assert datos["ofertas"]
        primera = datos["ofertas"][0]
        assert primera["puntaje"] is not None
        assert primera["precio_final_ars"] is not None
        assert primera["ida"]["segmentos"]

    def test_salida_markdown(self, monkeypatch, capsys):
        _, salida = self._correr(
            ["AEP", "BRC", "--ida", "+60d", "--markdown"], monkeypatch, capsys)
        assert salida.startswith("# ")
        assert "| # | Precio |" in salida

    def test_top_limita_lo_que_se_muestra(self, monkeypatch, capsys):
        _, salida = self._correr(
            ["AEP", "BRC", "--ida", "+60d", "--top", "2"], monkeypatch, capsys)
        assert " 3. " not in salida

    def test_solo_directos(self, monkeypatch, capsys):
        _, salida = self._correr(
            ["AEP", "BRC", "--ida", "+60d", "--directo", "--json"], monkeypatch, capsys)
        assert all(o["escalas"] == 0 for o in json.loads(salida)["ofertas"])

    def test_el_perfil_cambia_el_orden(self, monkeypatch, capsys):
        base = ["AEP", "BRC", "--ida", "+60d", "--vuelta", "+67d", "--json"]
        _, mochilero = self._correr(base + ["--perfil", "mochilero"], monkeypatch, capsys)
        _, trabajo = self._correr(base + ["--perfil", "trabajo"], monkeypatch, capsys)

        primero_barato = json.loads(mochilero)["ofertas"][0]
        primero_comodo = json.loads(trabajo)["ofertas"][0]
        assert primero_barato["precio"] <= primero_comodo["precio"]

    def test_solo_precio_ordena_por_plata(self, monkeypatch, capsys):
        _, salida = self._correr(
            ["AEP", "BRC", "--ida", "+60d", "--perfil", "solo-precio", "--json"],
            monkeypatch, capsys)
        precios = [o["precio_final_ars"] for o in json.loads(salida)["ofertas"]]
        assert precios == sorted(precios)

    def test_pedir_bodega_descarta_las_tarifas_que_no_la_traen(self, monkeypatch, capsys):
        _, salida = self._correr(
            ["AEP", "BRC", "--ida", "+60d", "--bodega", "1", "--json"], monkeypatch, capsys)
        ofertas = json.loads(salida)["ofertas"]
        assert ofertas
        assert all(o["equipaje"]["bodega_incluidas"] >= 1 for o in ofertas)

    def test_excluir_una_aerolinea(self, monkeypatch, capsys):
        _, salida = self._correr(
            ["AEP", "BRC", "--ida", "+60d", "--sin-aerolinea", "AR", "--json"],
            monkeypatch, capsys)
        assert all("AR" not in o["aerolineas"] for o in json.loads(salida)["ofertas"])

    def test_precio_max(self, monkeypatch, capsys):
        _, salida = self._correr(
            ["AEP", "BRC", "--ida", "+60d", "--precio-max", "300", "--json"],
            monkeypatch, capsys)
        assert all(o["precio"] <= 300 for o in json.loads(salida)["ofertas"])

    def test_sin_resultados_devuelve_codigo_de_error(self, monkeypatch, capsys):
        codigo, _ = self._correr(
            ["AEP", "BRC", "--ida", "+60d", "--precio-max", "1"], monkeypatch, capsys)
        assert codigo == 1

    def test_un_internacional_muestra_la_percepcion(self, monkeypatch, capsys):
        _, salida = self._correr(
            ["EZE", "MAD", "--ida", "+90d", "--vuelta", "+104d", "--moneda", "ARS"],
            monkeypatch, capsys)
        assert "percepción" in salida.lower()
        assert "dólares" in salida

    def test_pagando_en_dolares_no_hay_percepcion(self, monkeypatch, capsys):
        _, salida = self._correr(
            ["EZE", "MAD", "--ida", "+90d", "--pago", "dolares", "--json"],
            monkeypatch, capsys)
        for o in json.loads(salida)["ofertas"]:
            assert not o["desglose"].get("percepcion_rg5617")
