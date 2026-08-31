"""El precio de vidriera no es el precio que pagás."""
from datetime import datetime, timedelta

import pytest

from buscador.modelos import Equipaje, Itinerario, Oferta, Segmento
from buscador.precios_ar import (
    PERCEPCION_RG5617,
    Cotizaciones,
    ahorro_pagando_en_dolares,
    aplicar_costo_real,
    calcular_costo_real,
    cotizaciones,
    oferta_es_internacional,
)

# Cotizaciones fijas para que los tests no dependan del dólar de hoy.
COTIZ = Cotizaciones(oficial=1500.0, tarjeta=1950.0, mep=1520.0, fuente="test")


def seg(o, d, hora=8, dur=140, aer="AR"):
    salida = datetime(2026, 11, 10, hora, 0)
    return Segmento(o, d, salida, salida + timedelta(minutes=dur), aer, "1000")


def oferta(precio, moneda, origen="AEP", destino="BRC", con_vuelta=False,
           aer="AR", equipaje=None):
    vuelta = Itinerario([seg(destino, origen, hora=18, aer=aer)]) if con_vuelta else None
    return Oferta(
        proveedor="test", precio=precio, moneda=moneda,
        ida=Itinerario([seg(origen, destino, aer=aer)]), vuelta=vuelta,
        equipaje=equipaje or Equipaje(mano_incluido=True, bodega_incluidas=0),
    )


class TestDeteccionDeTramoInternacional:
    def test_cabotaje(self):
        assert not oferta_es_internacional(oferta(100, "ARS", "AEP", "BRC"))

    def test_internacional(self):
        assert oferta_es_internacional(oferta(100, "USD", "EZE", "MAD"))

    def test_alcanza_con_que_una_punta_cruce(self):
        o = oferta(100, "USD", "AEP", "BRC", con_vuelta=True)
        o.vuelta = Itinerario([seg("BRC", "SCL", hora=18)])
        assert oferta_es_internacional(o)


class TestCabotaje:
    def test_no_lleva_percepcion(self):
        c = calcular_costo_real(oferta(200_000, "ARS"), cotiz=COTIZ)
        assert c.percepcion_ars == 0
        assert c.total_hoy == 200_000
        assert c.total_neto == 200_000

    def test_suma_el_equipaje_que_falta(self):
        o = oferta(200_000, "ARS", aer="FO",
                   equipaje=Equipaje(mano_incluido=False, bodega_incluidas=0))
        c = calcular_costo_real(o, quiere_carry_on=True, cotiz=COTIZ)
        assert c.equipaje_ars == pytest.approx(14_149)   # una sola punta
        assert c.total_hoy == pytest.approx(214_149)

    def test_el_equipaje_se_cobra_por_tramo(self):
        o = oferta(200_000, "ARS", aer="FO", con_vuelta=True,
                   equipaje=Equipaje(mano_incluido=False, bodega_incluidas=0))
        c = calcular_costo_real(o, quiere_carry_on=True, cotiz=COTIZ)
        assert c.equipaje_ars == pytest.approx(14_149 * 2)


class TestInternacional:
    def test_precio_en_pesos_recibe_la_percepcion_del_30(self):
        c = calcular_costo_real(oferta(1_000_000, "ARS", "EZE", "MAD"),
                                forma_de_pago="tarjeta_pesos", cotiz=COTIZ)
        assert c.percepcion_ars == pytest.approx(300_000)
        assert c.total_hoy == pytest.approx(1_300_000)

    def test_la_percepcion_se_recupera(self):
        c = calcular_costo_real(oferta(1_000_000, "ARS", "EZE", "MAD"), cotiz=COTIZ)
        assert c.total_recuperable == pytest.approx(300_000)
        assert c.total_neto == pytest.approx(1_000_000)

    def test_precio_en_dolares_con_tarjeta_usa_el_dolar_tarjeta(self):
        c = calcular_costo_real(oferta(800, "USD", "EZE", "MAD"),
                                forma_de_pago="tarjeta_pesos", cotiz=COTIZ)
        assert c.publicado_ars == pytest.approx(800 * 1950)
        # El dólar tarjeta ya trae la percepción adentro: se informa para que
        # el usuario la vea, pero no se vuelve a sumar.
        assert c.percepcion_ya_incluida
        assert c.percepcion_ars == pytest.approx(800 * (1950 - 1500))
        assert c.total_hoy == pytest.approx(800 * 1950)

    def test_la_percepcion_embebida_tambien_se_recupera(self):
        c = calcular_costo_real(oferta(800, "USD", "EZE", "MAD"), cotiz=COTIZ)
        assert c.total_recuperable == pytest.approx(800 * (1950 - 1500))
        assert c.total_neto == pytest.approx(800 * 1500)

    def test_pagando_en_dolares_se_liquida_al_mep(self):
        c = calcular_costo_real(oferta(800, "USD", "EZE", "MAD"),
                                forma_de_pago="dolares", cotiz=COTIZ)
        assert c.publicado_ars == pytest.approx(800 * 1520)
        assert c.percepcion_ars == 0

    def test_pagar_en_dolares_es_el_ahorro_mas_grande(self):
        o = oferta(800, "USD", "EZE", "MAD")
        ahorro = ahorro_pagando_en_dolares(o, cotiz=COTIZ)
        assert ahorro == pytest.approx(800 * (1950 - 1520))
        # Más del 20% del total: ninguna otra palanca da tanto.
        assert ahorro / (800 * 1950) > 0.20

    def test_en_cabotaje_no_hay_nada_que_ahorrar_cambiando_el_pago(self):
        assert ahorro_pagando_en_dolares(oferta(200_000, "ARS"), cotiz=COTIZ) == 0


class TestAplicarATodaLaLista:
    def test_completa_el_precio_comparable(self):
        ofertas = [oferta(1_000_000, "ARS", "EZE", "MAD"), oferta(200_000, "ARS")]
        aplicar_costo_real(ofertas, cotiz=COTIZ)

        internacional, cabotaje = ofertas
        assert internacional.precio_ars_final == pytest.approx(1_300_000)
        assert internacional.precio_comparable == pytest.approx(1_300_000)
        assert internacional.moneda_comparable == "ARS"
        assert cabotaje.precio_ars_final == pytest.approx(200_000)

    def test_deja_el_desglose_para_poder_explicarlo(self):
        o = oferta(1_000_000, "ARS", "EZE", "MAD")
        aplicar_costo_real([o], cotiz=COTIZ)
        assert o.desglose_precio["percepcion_rg5617"] == pytest.approx(300_000)
        assert o.desglose_precio["publicado"] == pytest.approx(1_000_000)
        assert o.desglose_precio["total_neto"] == pytest.approx(1_000_000)

    def test_el_orden_por_precio_puede_darse_vuelta(self):
        # Un cabotaje en pesos contra un internacional: sin la percepción, el
        # segundo parecía competitivo.
        barato_aparente = oferta(1_000_000, "ARS", "EZE", "MAD")
        caro_aparente = oferta(1_250_000, "ARS", "AEP", "USH")
        assert barato_aparente.precio < caro_aparente.precio

        aplicar_costo_real([barato_aparente, caro_aparente], cotiz=COTIZ)
        assert barato_aparente.precio_comparable > caro_aparente.precio_comparable


class TestCotizaciones:
    def test_usd_ars_fijado_a_mano_evita_salir_a_internet(self, monkeypatch):
        monkeypatch.setenv("USD_ARS", "1500")
        c = cotizaciones()
        assert c.oficial == 1500
        assert c.tarjeta == pytest.approx(1500 * (1 + PERCEPCION_RG5617))
        assert "a mano" in c.fuente

    def test_el_recargo_de_tarjeta_es_la_percepcion(self):
        assert COTIZ.recargo_tarjeta == pytest.approx(0.30)

    def test_sin_red_y_sin_usd_ars_avisa_en_vez_de_devolver_basura(self, monkeypatch):
        import buscador.precios_ar as pa

        monkeypatch.delenv("USD_ARS", raising=False)
        monkeypatch.setattr(pa, "_leer_cache", lambda: None)

        def sin_red(*a, **kw):
            raise pa.requests.RequestException("sin conexión")

        monkeypatch.setattr(pa.requests, "get", sin_red)
        with pytest.raises(RuntimeError, match="USD_ARS"):
            cotizaciones(forzar=True)
