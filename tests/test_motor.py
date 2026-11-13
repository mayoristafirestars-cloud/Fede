"""Motor de saldos: código puro, sin base."""

from datetime import date

import pytest

from copiloto.motor import (Ajuste, Aplicacion, Documento, ErrorAplicacion, ajustes_efectivos,
                            estado_documento, resumir, tramo, validar_aplicacion)

CORTE = date(2026, 11, 13)


def _doc(id, tipo, importe, venc, emision=date(2026, 9, 1), anulado=False):
    return Documento(id, tipo, importe, emision, venc, anulado)


@pytest.mark.parametrize("dias,esperado", [
    (-5, "al_dia"), (0, "al_dia"), (1, "1_30"), (30, "1_30"), (31, "31_60"),
    (60, "31_60"), (61, "61_90"), (90, "61_90"), (91, "mas_90"),
])
def test_tramos(dias, esperado):
    assert tramo(dias) == esperado


def test_estado_documento():
    assert estado_documento(1000, 1000, False) == "emitido"
    assert estado_documento(1000, 400, False) == "parcialmente_cancelado"
    assert estado_documento(1000, 0, False) == "cancelado"
    assert estado_documento(1000, 1000, True) == "anulado"


def test_pago_parcial_por_nota_de_credito():
    docs = [_doc(1, "FC", 100000, date(2026, 10, 1)), _doc(2, "NC", 30000, date(2026, 10, 1))]
    apl = [Aplicacion(1, "nota_credito", 2, 30000)]
    r = resumir(docs, apl, [], CORTE)
    assert r.partidas[0].saldo == 70000 and r.partidas[0].estado == "parcialmente_cancelado"
    assert r.creditos_sin_imputar == 0
    assert r.saldo == 70000 and r.vencido == 70000 and r.tramos["31_60"] == 70000


def test_nota_de_credito_sin_imputar_resta_del_saldo_pero_no_del_vencido():
    docs = [_doc(1, "FC", 100000, date(2026, 10, 1)), _doc(2, "NC", 30000, date(2026, 10, 1))]
    r = resumir(docs, [], [], CORTE)
    assert r.deuda_bruta == 100000 and r.creditos_sin_imputar == 30000 and r.saldo == 70000
    assert r.vencido == 100000                      # el vencido es de las partidas; la NC queda a cuenta


def test_nota_de_credito_total_cancela():
    docs = [_doc(1, "FC", 50000, date(2026, 10, 1)), _doc(2, "NC", 50000, date(2026, 10, 1))]
    r = resumir(docs, [Aplicacion(1, "nota_credito", 2, 50000)], [], CORTE)
    assert r.partidas[0].estado == "cancelado" and r.saldo == 0 and r.vencido == 0


def test_nota_de_credito_aplicada_a_dos_facturas_conserva_suma_y_remanentes():
    """Prueba 14 (parcial)."""
    docs = [_doc(1, "FC", 100000, date(2026, 10, 1)), _doc(2, "FC", 80000, date(2026, 11, 1)),
            _doc(3, "NC", 150000, date(2026, 11, 1))]
    apl = [Aplicacion(1, "nota_credito", 3, 100000), Aplicacion(2, "nota_credito", 3, 50000)]
    r = resumir(docs, apl, [], CORTE)
    saldos = {p.clave: (p.saldo, p.estado) for p in r.partidas}
    assert saldos == {"doc:1": (0, "cancelado"), "doc:2": (30000, "parcialmente_cancelado")}
    assert r.creditos_sin_imputar == 0
    assert r.saldo == 30000 == (100000 + 80000 - 150000)


def test_ajuste_y_su_reverso_se_compensan():
    docs = [_doc(1, "FC", 100000, date(2026, 12, 1))]
    ajustes = [Ajuste(10, "credito", 20000, date(2026, 11, 1)),
               Ajuste(11, "credito", 20000, date(2026, 11, 2), revierte_a=10)]
    assert ajustes_efectivos(ajustes) == []
    assert resumir(docs, [], ajustes, CORTE).saldo == 100000


def test_ajuste_debito_suma_deuda_vencida_desde_su_fecha():
    r = resumir([], [], [Ajuste(5, "debito", 15000, date(2026, 10, 1))], CORTE)
    assert r.saldo == 15000 and r.tramos["31_60"] == 15000


def test_documento_anulado_no_suma():
    docs = [_doc(1, "FC", 100000, date(2026, 10, 1), anulado=True), _doc(2, "NC", 5000, date(2026, 10, 1), anulado=True)]
    r = resumir(docs, [], [], CORTE)
    assert r.saldo == 0 and r.partidas[0].estado == "anulado"


def test_aplicacion_revertida_devuelve_saldo():
    docs = [_doc(1, "FC", 100000, date(2026, 10, 1)), _doc(2, "NC", 30000, date(2026, 10, 1))]
    apl = [Aplicacion(1, "nota_credito", 2, 30000), Aplicacion(1, "nota_credito", 2, -30000)]
    r = resumir(docs, apl, [], CORTE)
    assert r.partidas[0].saldo == 100000 and r.creditos_sin_imputar == 30000 and r.saldo == 70000


def test_al_dia_no_es_vencido():
    r = resumir([_doc(1, "SI", 99999, date(2026, 11, 13))], [], [], CORTE)
    assert r.vencido == 0 and r.tramos["al_dia"] == 99999


def test_validar_aplicacion():
    validar_aplicacion(1000, 1000, 1000)
    with pytest.raises(ErrorAplicacion):
        validar_aplicacion(1000, 5000, 1001)          # supera el saldo del documento
    with pytest.raises(ErrorAplicacion):
        validar_aplicacion(5000, 1000, 1001)          # supera lo disponible del crédito
    with pytest.raises(ErrorAplicacion):
        validar_aplicacion(1000, 1000, 0)
