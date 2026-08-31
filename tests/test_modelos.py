from datetime import date, datetime, timedelta

import pytest

from buscador.modelos import Consulta, Itinerario, Oferta, Segmento


def seg(o, d, salida, dur_min, aer="AR", nro="1234"):
    return Segmento(o, d, salida, salida + timedelta(minutes=dur_min), aer, numero_vuelo=nro)


def test_segmento_calcula_duracion_sola():
    s = seg("AEP", "BRC", datetime(2026, 10, 1, 8, 0), 140)
    assert s.duracion_min == 140


def test_itinerario_directo():
    it = Itinerario([seg("AEP", "BRC", datetime(2026, 10, 1, 8, 0), 140)])
    assert it.escalas == 0
    assert it.duracion_min == 140
    assert it.layovers_min == []
    assert not it.cambia_de_aeropuerto


def test_itinerario_con_escala_incluye_espera_en_la_duracion():
    salida = datetime(2026, 10, 1, 8, 0)
    tramo1 = seg("AEP", "COR", salida, 80)
    tramo2 = seg("COR", "BRC", tramo1.llegada + timedelta(minutes=90), 120)
    it = Itinerario([tramo1, tramo2])

    assert it.escalas == 1
    assert it.layovers_min == [90]
    assert it.duracion_min == 80 + 90 + 120
    assert it.aerolineas == ["AR"]


def test_itinerario_detecta_cambio_de_aeropuerto():
    salida = datetime(2026, 10, 1, 8, 0)
    tramo1 = seg("BHI", "AEP", salida, 90)
    tramo2 = seg("EZE", "MAD", salida + timedelta(hours=6), 720)
    assert Itinerario([tramo1, tramo2]).cambia_de_aeropuerto


def test_oferta_roundtrip_suma_ambas_puntas():
    ida = Itinerario([seg("AEP", "BRC", datetime(2026, 10, 1, 8, 0), 140)])
    vuelta = Itinerario([seg("BRC", "AEP", datetime(2026, 10, 8, 18, 0), 140)])
    o = Oferta(proveedor="test", precio=100.0, moneda="USD", ida=ida, vuelta=vuelta)

    assert o.tipo_viaje == "ida_vuelta"
    assert o.duracion_total_min == 280
    assert o.es_directo
    assert o.noches == 7


def test_precio_comparable_prefiere_el_final_en_pesos():
    it = Itinerario([seg("AEP", "BRC", datetime(2026, 10, 1, 8, 0), 140)])
    o = Oferta(proveedor="test", precio=100.0, moneda="USD", ida=it)
    assert o.precio_comparable == 100.0 and o.moneda_comparable == "USD"

    o.precio_ars_final = 150_000.0
    assert o.precio_comparable == 150_000.0 and o.moneda_comparable == "ARS"


def test_dedupe_distingue_itinerarios_distintos():
    base = datetime(2026, 10, 1, 8, 0)
    a = Oferta("x", 100, "USD", Itinerario([seg("AEP", "BRC", base, 140, nro="1111")]))
    b = Oferta("y", 120, "USD", Itinerario([seg("AEP", "BRC", base, 140, nro="1111")]))
    c = Oferta("z", 100, "USD", Itinerario([seg("AEP", "BRC", base, 140, nro="2222")]))

    assert a.clave_dedupe() == b.clave_dedupe()   # mismo vuelo, distinto precio
    assert a.clave_dedupe() != c.clave_dedupe()


class TestFlexibilidad:
    def base(self, **kw):
        hoy = date.today()
        return Consulta(
            origen="AEP", destino="BRC",
            fecha_ida=hoy + timedelta(days=60),
            fecha_vuelta=hoy + timedelta(days=67),
            **kw,
        )

    def test_sin_flex_devuelve_una_sola_combinacion(self):
        assert self.base().fechas_a_probar() == [
            (self.base().fecha_ida, self.base().fecha_vuelta)
        ]

    def test_flex_expande_ambas_puntas(self):
        pares = self.base(flex_dias=2).fechas_a_probar()
        assert len(pares) == 25          # 5 fechas de ida x 5 de vuelta
        assert all(v >= i for i, v in pares)

    def test_flex_nunca_propone_fechas_pasadas(self):
        c = Consulta(origen="AEP", destino="BRC", fecha_ida=date.today(), flex_dias=3)
        assert all(i >= date.today() for i, _ in c.fechas_a_probar())

    def test_flex_solo_ida(self):
        c = Consulta(origen="AEP", destino="BRC",
                     fecha_ida=date.today() + timedelta(days=30), flex_dias=1)
        pares = c.fechas_a_probar()
        assert len(pares) == 3
        assert all(v is None for _, v in pares)


def test_rutas_a_probar_combina_alternativas():
    c = Consulta(origen="RSA", destino="BRC", fecha_ida=date.today() + timedelta(days=30),
                 origenes_alternativos=["BHI", "RSA"], destinos_alternativos=["NQN"])
    rutas = c.rutas_a_probar()
    assert ("RSA", "BRC") in rutas and ("BHI", "NQN") in rutas
    assert len(rutas) == 4        # RSA/BHI x BRC/NQN, sin duplicar RSA
