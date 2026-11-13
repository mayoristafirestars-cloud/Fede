"""Lectura de archivos y normalización de datos argentinos."""

from datetime import date
from decimal import Decimal

import pytest

from copiloto import lectura
from copiloto.lectura import ErrorDato


def cuit_valido(prefijo: str, dni: str) -> str:
    """Arma un CUIT válido (para datos de prueba inventados)."""
    base = prefijo + dni.zfill(8)
    resto = 11 - sum(int(d) * p for d, p in zip(base, (5, 4, 3, 2, 7, 6, 5, 4, 3, 2))) % 11
    v = 0 if resto == 11 else 9 if resto == 10 else resto
    if resto == 10:
        return cuit_valido(prefijo, str(int(dni) + 1))
    return f"{prefijo}-{dni.zfill(8)}-{v}"


@pytest.mark.parametrize("texto,esperado", [
    ("1.234,56", "1234.56"), ("1.500", "1500"), ("850.5", "850.5"), ("2,00", "2.00"),
    ("$ -1.000", "-1000"), ("1.234.567", "1234567"), ("125.000,50", "125000.50"),
    ("(500,00)", "-500.00"), (1500.25, "1500.25"), ("0", "0"),
])
def test_parsear_importe(texto, esperado):
    assert lectura.parsear_importe(texto) == Decimal(esperado)


@pytest.mark.parametrize("texto", ["", "abc", "1,2,3"])
def test_parsear_importe_invalido(texto):
    with pytest.raises(ErrorDato):
        lectura.parsear_importe(texto)


@pytest.mark.parametrize("texto,esperado", [
    ("15/10/2026", date(2026, 10, 15)), ("15-10-2026", date(2026, 10, 15)), ("5/1/2026", date(2026, 1, 5)),
    ("2026-10-15", date(2026, 10, 15)), ("2026-10-15 00:00:00", date(2026, 10, 15)),
])
def test_parsear_fecha(texto, esperado):
    assert lectura.parsear_fecha(texto) == esperado


@pytest.mark.parametrize("texto", ["31/02/2026", "ayer", "", "2026/10/15"])
def test_parsear_fecha_invalida(texto):
    with pytest.raises(ErrorDato):
        lectura.parsear_fecha(texto)


def test_cuit():
    assert lectura.normalizar_cuit("20-12345678-6") == "20123456786"
    valido = cuit_valido("30", "71234567")
    assert lectura.normalizar_cuit(valido) == valido.replace("-", "")
    with pytest.raises(ErrorDato):
        lectura.normalizar_cuit("20-12345678-5")          # verificador incorrecto
    with pytest.raises(ErrorDato):
        lectura.normalizar_cuit("12345")


@pytest.mark.parametrize("texto,esperado", [
    ("2954 525928", "+5492954525928"),
    ("02954-15-525928", "+5492954525928"),
    ("+54 9 2954 525928", "+5492954525928"),
    ("11 4444 5555", "+5491144445555"),
    ("525928", "+5492954525928"),                       # local: se asume Santa Rosa
    ("15525928", "+5492954525928"),
    ("123", None), ("", None),
])
def test_telefono(texto, esperado):
    assert lectura.normalizar_telefono(texto) == esperado


def test_ubicar_columnas_con_titulo_arriba_y_tildes():
    filas = [["Mis Comprobantes Emitidos - CUIT 30-00000000-0"], [],
             ["Fecha de Emisión", "Tipo de Comprobante", "Punto de Venta", "Número Desde",
              "Nro. Doc. Receptor", "Imp. Total"], ["01/10/2026", "1 - Factura A", "3", "1", "20123456786", "100"]]
    inicio, columnas = lectura.ubicar_columnas(filas, lectura.cargar_mapeo("arca_emitidos"))
    assert inicio == 2 and columnas["total"] == 5 and columnas["cuit"] == 4


def test_faltan_columnas_obligatorias():
    with pytest.raises(ErrorDato):
        lectura.ubicar_columnas([["Cliente", "Saldo"]], lectura.cargar_mapeo("saldo_inicial"))


def test_csv_con_coma_y_utf8():
    filas = lectura.leer_filas("x.csv", "Cliente,Saldo,Fecha\nPepe,100,01/10/2026\n".encode("utf-8-sig"))
    assert filas[0] == ["Cliente", "Saldo", "Fecha"]


def test_formato_desconocido():
    with pytest.raises(ErrorDato):
        lectura.cargar_mapeo("../secreto")
