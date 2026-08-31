"""La regla de negocio más importante: comparar viajes, no precios pelados."""
import pytest

from buscador.equipaje_ar import (
    RECARGO_EN_PUERTA,
    costo_de_igualar,
    describir_tarifa,
    equipaje_de_tarifa_base,
    es_low_cost,
)


class TestQueIncluyeLaTarifaBase:
    def test_flybondi_no_incluye_carry_on(self):
        e = equipaje_de_tarifa_base("FO")
        assert not e.mano_incluido
        assert e.bodega_incluidas == 0
        assert e.mochila_incluida, "el bulto de 6 kg bajo el asiento sí viene"

    def test_jetsmart_no_incluye_carry_on(self):
        for codigo in ("JA", "WJ"):
            e = equipaje_de_tarifa_base(codigo)
            assert not e.mano_incluido, codigo
            assert e.bodega_incluidas == 0, codigo

    def test_aerolineas_base_si_incluye_carry_on(self):
        # Lo sacó en mayo de 2026 y lo repuso en junio tras el rechazo.
        e = equipaje_de_tarifa_base("AR")
        assert e.mano_incluido
        assert e.bodega_incluidas == 0

    def test_aerolineas_internacional_tambien_incluye_carry_on(self):
        assert equipaje_de_tarifa_base("AR", internacional=True).mano_incluido

    def test_tradicional_internacional_asume_una_bodega(self):
        assert equipaje_de_tarifa_base("LA", internacional=True).bodega_incluidas == 1

    def test_tradicional_cabotaje_no_asume_bodega(self):
        assert equipaje_de_tarifa_base("LA", internacional=False).bodega_incluidas == 0

    def test_low_cost_desconocida_se_trata_como_low_cost(self):
        assert not equipaje_de_tarifa_base("FR").mano_incluido   # Ryanair

    def test_aerolinea_vacia_no_explota(self):
        assert equipaje_de_tarifa_base("") is not None


class TestCostoDeIgualar:
    def test_aerolineas_no_cobra_por_el_carry_on(self):
        costo, detalle = costo_de_igualar("AR", equipaje_de_tarifa_base("AR"),
                                          quiere_carry_on=True, tramos=2)
        assert costo == 0
        assert detalle == []

    def test_flybondi_cobra_el_carry_on_por_tramo(self):
        costo, detalle = costo_de_igualar("FO", equipaje_de_tarifa_base("FO"),
                                          quiere_carry_on=True, tramos=2)
        assert costo == pytest.approx(14_149 * 2)
        assert "carry-on x2" in detalle[0]

    def test_una_ida_sola_cobra_un_solo_tramo(self):
        costo, _ = costo_de_igualar("FO", equipaje_de_tarifa_base("FO"),
                                    quiere_carry_on=True, tramos=1)
        assert costo == pytest.approx(14_149)

    def test_quien_no_lleva_carry_on_no_paga_carry_on(self):
        costo, _ = costo_de_igualar("FO", equipaje_de_tarifa_base("FO"),
                                    quiere_carry_on=False, tramos=2)
        assert costo == 0

    def test_bodega_se_cobra_por_pieza_y_por_tramo(self):
        costo, detalle = costo_de_igualar("FO", equipaje_de_tarifa_base("FO"),
                                          quiere_carry_on=False, piezas_bodega=2, tramos=2)
        assert costo == pytest.approx(10_399 * 2 * 2)
        assert "bodega x2 x2 tramos" in detalle[0]

    def test_no_se_cobra_la_bodega_que_ya_viene_incluida(self):
        incluido = equipaje_de_tarifa_base("LA", internacional=True)
        costo, _ = costo_de_igualar("LA", incluido, quiere_carry_on=False,
                                    piezas_bodega=1, tramos=2, internacional=True)
        assert costo == 0

    def test_bodega_internacional_se_cotiza_en_dolares(self):
        incluido = equipaje_de_tarifa_base("CM", internacional=True)
        costo, _ = costo_de_igualar("CM", incluido, quiere_carry_on=False,
                                    piezas_bodega=2, tramos=1,
                                    internacional=True, tipo_cambio=1500)
        # Una pieza ya viene; se cobra la segunda a USD 100.
        assert costo == pytest.approx(100 * 1500)


class TestComparacionJusta:
    """Los casos que motivan todo el módulo."""

    def _total(self, aerolinea, tarifa, **kw):
        extra, _ = costo_de_igualar(aerolinea, equipaje_de_tarifa_base(aerolinea),
                                    tramos=2, **kw)
        return tarifa + extra

    def test_con_carry_on_la_low_cost_barata_termina_mas_cara(self):
        # Pasaje base: Flybondi $180.000, Aerolíneas $205.000, ida y vuelta.
        # Aerolíneas incluye el carry-on; Flybondi lo cobra $14.149 por tramo.
        total_fo = self._total("FO", 180_000, quiere_carry_on=True)
        total_ar = self._total("AR", 205_000, quiere_carry_on=True)

        assert total_fo > total_ar, (
            "quien viaja con carry-on paga más en la low-cost 'barata', "
            "y ése es justamente el punto"
        )

    def test_con_valija_despachada_la_low_cost_vuelve_a_ganar(self):
        # No es una regla fija a favor de nadie: Aerolíneas cobra la bodega
        # $42.350 por tramo contra $10.399 de Flybondi, así que en cuanto hay
        # que despachar, la cuenta se da vuelta. Por eso hay que calcularlo
        # caso por caso en vez de asumir quién es más barato.
        total_fo = self._total("FO", 180_000, quiere_carry_on=True, piezas_bodega=1)
        total_ar = self._total("AR", 205_000, quiere_carry_on=True, piezas_bodega=1)

        assert total_fo < total_ar

    def test_sin_equipaje_gana_el_precio_de_vidriera(self):
        total_fo = self._total("FO", 180_000, quiere_carry_on=False)
        total_ar = self._total("AR", 205_000, quiere_carry_on=False)
        assert total_fo < total_ar


def test_es_low_cost():
    assert es_low_cost("FO") and es_low_cost("ja")
    assert not es_low_cost("AR") and not es_low_cost("")


def test_recargo_en_puerta_es_mayor_que_uno():
    # Comprar el equipaje en la puerta cuesta más del doble.
    assert RECARGO_EN_PUERTA > 2


def test_describir_tarifa_menciona_la_restriccion():
    assert "6 kg" in describir_tarifa("FO")
    assert "carry-on" in describir_tarifa("AR")
    assert describir_tarifa("XX")
