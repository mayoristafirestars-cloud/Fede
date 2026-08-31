"""El ranking: qué significa 'el mejor' además de 'el más barato'."""
from datetime import date, datetime, timedelta

import pytest

from buscador.modelos import Consulta, Equipaje, Itinerario, Oferta, Segmento
from buscador.ranking import (
    Preferencias,
    costo_generalizado,
    evaluar_precio,
    mas_barata,
    mas_rapida,
    mct,
    probabilidad_de_perder,
    rankear,
)

CONSULTA = Consulta(origen="EZE", destino="MAD",
                    fecha_ida=date(2026, 11, 10), fecha_vuelta=date(2026, 11, 24))
# Preferencias en dólares para que los números del test se lean directo.
OCIO = Preferencias.perfil("ocio", tipo_cambio=1.0, moneda="USD")


def tramo(o, d, salida: datetime, minutos: int, aer="LA", nro="1000"):
    return Segmento(o, d, salida, salida + timedelta(minutes=minutos), aer, nro)


def directo(precio, hora=10, minutos=140, origen="AEP", destino="BRC", aer="AR"):
    salida = datetime(2026, 11, 10, hora, 0)
    return Oferta(proveedor="t", precio=precio, moneda="USD",
                  ida=Itinerario([tramo(origen, destino, salida, minutos, aer)]))


def con_escala(precio, espera_min, escala="COR", origen="AEP", destino="BRC",
               hora=10, aer="AR", self_transfer=False):
    salida = datetime(2026, 11, 10, hora, 0)
    primero = tramo(origen, escala, salida, 80, aer)
    segundo = tramo(escala, destino, primero.llegada + timedelta(minutes=espera_min), 90, aer)
    return Oferta(proveedor="t", precio=precio, moneda="USD",
                  ida=Itinerario([primero, segundo]), self_transfer=self_transfer)


class TestMCT:
    def test_cabotaje_es_mas_rapido_que_internacional(self):
        salida = datetime(2026, 11, 10, 10, 0)
        cab = tramo("AEP", "COR", salida, 80)
        intl = tramo("EZE", "GRU", salida, 180)
        assert mct("COR", cab, cab) < mct("GRU", intl, intl)

    def test_aeropuerto_con_mct_propio_manda_sobre_el_generico(self):
        salida = datetime(2026, 11, 10, 10, 0)
        cab = tramo("AEP", "COR", salida, 80)
        assert mct("AEP", cab, cab) == 40      # publicado
        assert mct("COR", cab, cab) == 45      # genérico cabotaje-cabotaje


class TestRiesgoDeConexion:
    def test_sin_colchon_el_riesgo_es_alto(self):
        assert probabilidad_de_perder(0, OCIO) == pytest.approx(0.30)

    def test_el_riesgo_cae_con_el_colchon(self):
        assert probabilidad_de_perder(90, OCIO) < probabilidad_de_perder(30, OCIO)
        assert probabilidad_de_perder(30, OCIO) < probabilidad_de_perder(0, OCIO)

    def test_por_debajo_del_minimo_es_casi_seguro_que_se_pierde(self):
        assert probabilidad_de_perder(-20, OCIO) > 0.8

    def test_nunca_baja_de_cero(self):
        assert probabilidad_de_perder(100_000, OCIO) >= 0


class TestCostoGeneralizado:
    def test_a_igual_itinerario_gana_el_mas_barato(self):
        barato = costo_generalizado(directo(200), CONSULTA, OCIO, 250).total
        caro = costo_generalizado(directo(300), CONSULTA, OCIO, 250).total
        assert barato < caro
        assert caro - barato == pytest.approx(100)

    def test_una_escala_cuesta_mas_que_un_directo_al_mismo_precio(self):
        d = costo_generalizado(directo(200), CONSULTA, OCIO, 200)
        e = costo_generalizado(con_escala(200, 90), CONSULTA, OCIO, 200)
        assert e.total > d.total
        assert e.escalas > 0

    def test_una_conexion_justa_cuesta_mas_que_una_holgada(self):
        justa = costo_generalizado(con_escala(200, 45), CONSULTA, OCIO, 200)
        holgada = costo_generalizado(con_escala(200, 120), CONSULTA, OCIO, 200)
        assert justa.riesgo_conexion > holgada.riesgo_conexion

    def test_una_espera_eterna_se_penaliza(self):
        normal = costo_generalizado(con_escala(200, 120), CONSULTA, OCIO, 200)
        eterna = costo_generalizado(con_escala(200, 600), CONSULTA, OCIO, 200)
        assert eterna.escalas_largas > 0 and normal.escalas_largas == 0
        assert eterna.total > normal.total

    def test_la_segunda_escala_pesa_mas_que_la_primera(self):
        salida = datetime(2026, 11, 10, 8, 0)
        a = tramo("AEP", "COR", salida, 80)
        b = tramo("COR", "MDZ", a.llegada + timedelta(minutes=90), 70)
        c = tramo("MDZ", "BRC", b.llegada + timedelta(minutes=90), 90)
        dos = Oferta(proveedor="t", precio=200, moneda="USD", ida=Itinerario([a, b, c]))

        una = costo_generalizado(con_escala(200, 90), CONSULTA, OCIO, 200)
        doble = costo_generalizado(dos, CONSULTA, OCIO, 200)
        assert doble.escalas > una.escalas * 2

    def test_salir_de_madrugada_se_penaliza(self):
        madrugada = costo_generalizado(directo(200, hora=3), CONSULTA, OCIO, 200)
        media_manana = costo_generalizado(directo(200, hora=10), CONSULTA, OCIO, 200)
        assert madrugada.horarios > media_manana.horarios

    def test_cambiar_de_aeropuerto_es_la_peor_escala(self):
        salida = datetime(2026, 11, 10, 8, 0)
        a = tramo("BHI", "AEP", salida, 90)
        b = tramo("EZE", "MAD", salida + timedelta(hours=6), 720)
        o = Oferta(proveedor="t", precio=900, moneda="USD", ida=Itinerario([a, b]))

        d = costo_generalizado(o, CONSULTA, OCIO, 900)
        assert d.cambio_aeropuerto > 0

    def test_tramos_separados_cuestan_mas_que_un_billete_unico(self):
        unico = costo_generalizado(con_escala(200, 90), CONSULTA, OCIO, 200)
        separado = costo_generalizado(con_escala(200, 90, self_transfer=True),
                                      CONSULTA, OCIO, 200)
        assert separado.total > unico.total
        assert separado.self_transfer > 0
        # Además de la penalización fija, el riesgo pesa más: hay que recuperar
        # el equipaje y no hay a quién reclamarle.
        assert separado.riesgo_conexion > unico.riesgo_conexion

    def test_el_traslado_terrestre_se_cobra_ida_y_vuelta(self):
        o = directo(200)
        o.desglose_precio["km_terrestres"] = 345.0     # Santa Rosa a Bahía Blanca
        d = costo_generalizado(o, CONSULTA, OCIO, 200)
        assert d.traslado_terrestre > 0

    def test_el_desglose_suma_el_total(self):
        d = costo_generalizado(con_escala(200, 45), CONSULTA, OCIO, 200)
        componentes = sum(getattr(d, c) for c in d.__dataclass_fields__)
        assert d.total == pytest.approx(componentes)
        assert d.sobrecosto == pytest.approx(d.total - d.precio)


class TestPerfiles:
    def _ordenar(self, perfil):
        ofertas = [directo(320), con_escala(200, 90), con_escala(150, 480)]
        p = (Preferencias.solo_precio("USD") if perfil == "solo-precio"
             else Preferencias.perfil(perfil, tipo_cambio=1.0, moneda="USD"))
        return [round(o.precio) for o in rankear(ofertas, CONSULTA, p)]

    def test_solo_precio_ordena_por_plata_y_nada_mas(self):
        assert self._ordenar("solo-precio") == [150, 200, 320]

    def test_el_mochilero_aguanta_la_escala_larga_por_ahorrar(self):
        assert self._ordenar("mochilero")[0] == 150

    def test_quien_viaja_por_trabajo_paga_el_directo(self):
        assert self._ordenar("trabajo")[0] == 320

    def test_subir_el_valor_del_tiempo_mueve_el_orden(self):
        assert self._ordenar("mochilero") != self._ordenar("trabajo")


class TestRankear:
    def test_devuelve_todas_las_ofertas_ordenadas(self):
        ofertas = [directo(300), directo(200), directo(250)]
        r = rankear(ofertas, CONSULTA, OCIO)
        assert len(r) == 3
        assert [o.precio for o in r] == [200, 250, 300]

    def test_anota_puntaje_motivos_y_desglose(self):
        r = rankear([directo(200), con_escala(180, 45)], CONSULTA, OCIO)
        for o in r:
            assert 0 <= o.puntaje <= 100
            assert o.motivos
            assert "costo_generalizado" in o.desglose_precio

    def test_el_mejor_saca_cien_puntos(self):
        r = rankear([directo(200), directo(400)], CONSULTA, OCIO)
        assert r[0].puntaje == 100

    def test_el_puntaje_no_se_usa_para_ordenar(self):
        # Se ordena por costo generalizado; el puntaje es su reflejo.
        r = rankear([directo(300), directo(200), con_escala(150, 30)], CONSULTA, OCIO)
        puntajes = [o.puntaje for o in r]
        assert puntajes == sorted(puntajes, reverse=True)

    def test_marca_el_mas_barato(self):
        r = rankear([directo(400), con_escala(150, 30)], CONSULTA, OCIO)
        barata = next(o for o in r if o.precio == 150)
        assert any("más barato" in m for m in barata.motivos)

    def test_avisa_cuando_lo_barato_sale_caro(self):
        # Escala de 12 horas y conexión imposible: el sobrecosto supera al precio.
        mala = con_escala(100, 720)
        r = rankear([directo(300), mala], CONSULTA, OCIO)
        assert any("vidriera" in m for m in mala.motivos)

    def test_lista_vacia_no_explota(self):
        assert rankear([], CONSULTA, OCIO) == []

    def test_una_sola_oferta_saca_cien(self):
        r = rankear([directo(200)], CONSULTA, OCIO)
        assert r[0].puntaje == 100

    def test_el_orden_no_depende_de_que_aparezca_una_opcion_absurda(self):
        """La razón por la que se usa costo generalizado y no min-max."""
        base = [directo(300), directo(200), con_escala(250, 90)]
        orden_solo = [o.precio for o in rankear(list(base), CONSULTA, OCIO)]

        absurda = con_escala(900, 2400)     # 40 horas de espera
        orden_con_absurda = [
            o.precio for o in rankear(base + [absurda], CONSULTA, OCIO)
            if o is not absurda
        ]
        assert orden_solo == orden_con_absurda


class TestContextoDePrecio:
    def test_un_precio_bajo_es_una_oferta(self):
        r = evaluar_precio(600, list(range(800, 1200, 10)))
        assert r["etiqueta"] == "excelente"

    def test_un_precio_alto_esta_caro(self):
        r = evaluar_precio(1500, list(range(800, 1200, 10)))
        assert r["etiqueta"] == "caro"

    def test_el_precio_del_medio_es_tipico(self):
        r = evaluar_precio(1000, list(range(800, 1200, 10)))
        assert r["etiqueta"] == "tipico"

    def test_sin_historico_no_inventa(self):
        assert evaluar_precio(1000, []) is None


def test_atajos_de_mas_barata_y_mas_rapida():
    lento = con_escala(150, 300)
    veloz = directo(400)
    ofertas = [lento, veloz]
    assert mas_barata(ofertas) is lento
    assert mas_rapida(ofertas) is veloz
    assert mas_barata([]) is None
