"""Paso 0.4: importes en centavos (Decimal, redondeo bancario) y fechas ISO."""

import glob
import json
import os
import sqlite3
from datetime import date
from decimal import Decimal

import pytest

from conftest import crear_usuario, login


# ─── Conversión de plata ───────────────────────────────────

@pytest.mark.parametrize("pesos,centavos", [
    (0.005, 0),          # medio centavo con dígito par → baja
    (0.015, 2),          # medio centavo con dígito impar → sube
    (2.675, 268),        # float 2.675 tomado como texto: no sufre el error de float
    (1999.995, 200000),
    (10000, 1000000),
    (-1.005, -100),
    ("1499.985", 149998),
])
def test_a_centavos_con_redondeo_bancario(pesos, centavos):
    from dinero import a_centavos
    assert a_centavos(pesos) == centavos


def test_formato_argentino():
    from dinero import formato_ar
    assert formato_ar(123456789) == "$ 1.234.567,89"
    assert formato_ar(5) == "$ 0,05"
    assert formato_ar(-150000) == "-$ 1.500,00"


# ─── Migración sobre una base como la de producción ────────

def _base_legacy(ruta):
    """Base creada con el esquema viejo, sin control de migraciones, con datos."""
    from db.migrador import DIR_MIGRACIONES
    conn = sqlite3.connect(ruta)
    conn.executescript(open(os.path.join(DIR_MIGRACIONES, "0001_esquema_inicial.sql"), encoding="utf-8").read())
    filas = [
        (1, "factura", "F-000001", "13-11-2026", 2000.0, 10, 1800.0),
        (2, "factura", "F-000002", "31-02-2026", 1000.0, 0, 333.3333),   # fecha imposible, total con 4 decimales
        (3, "presupuesto", "P-000001", "ayer", 0.015, 0, 0.015),          # fecha ilegible
        (4, "factura", "F-000003", "2026-10-05", 100.0, 0, 100.0),        # ya en ISO
    ]
    conn.executemany("INSERT INTO comprobantes (id, tipo, numero, fecha, subtotal, descuento, total) VALUES (?,?,?,?,?,?,?)", filas)
    conn.executemany(
        "INSERT INTO comprobante_items (comprobante_id, producto_desc, cantidad, precio_unitario, precio_costo, subtotal) VALUES (?,?,?,?,?,?)",
        [(1, "Yerba", 2, 1000.0, 600.0, 2000.0), (2, "Azúcar", 1, 1000.0, 700.0, 1000.0)],
    )
    conn.commit()
    conn.close()


def _filas(ruta, sql):
    conn = sqlite3.connect(ruta)
    conn.row_factory = sqlite3.Row
    salida = [dict(f) for f in conn.execute(sql)]
    conn.close()
    return salida


def _reportes(tmp_path):
    return sorted(glob.glob(str(tmp_path / "respaldos" / "reporte_migracion_0006_*.json")))


def test_migracion_convierte_importes_y_fechas(db_temporal, tmp_path):
    from db.migrador import aplicar_migraciones
    _base_legacy(db_temporal)
    aplicar_migraciones()

    c = {f["id"]: f for f in _filas(db_temporal, "SELECT * FROM comprobantes")}
    assert (c[1]["fecha"], c[1]["fecha_original"]) == ("2026-11-13", "13-11-2026")
    assert (c[2]["fecha"], c[2]["fecha_original"]) == ("31-02-2026", "31-02-2026")   # no se tocó
    assert c[3]["fecha"] == "ayer"
    assert c[4]["fecha"] == "2026-10-05"
    assert [c[i]["total_centavos"] for i in (1, 2, 3, 4)] == [180000, 33333, 2, 10000]
    assert c[1]["subtotal_centavos"] == 200000
    assert c[1]["total"] == 1800.0                       # las columnas viejas siguen intactas

    items = _filas(db_temporal, "SELECT * FROM comprobante_items ORDER BY id")
    assert [(i["precio_unitario_centavos"], i["precio_costo_centavos"], i["subtotal_centavos"]) for i in items] == \
        [(100000, 60000, 200000), (100000, 70000, 100000)]

    # hubo respaldo previo y reporte
    assert glob.glob(str(tmp_path / "respaldos" / "*pre_migracion_0001*.db"))
    reporte = json.load(open(_reportes(tmp_path)[-1], encoding="utf-8"))
    assert reporte["resultado"] == "aplicada"
    assert reporte["comprobantes_migrados"] == 4 and reporte["items_migrados"] == 2
    assert reporte["fechas_convertidas"] == 1
    assert Decimal(reporte["total_antes_pesos"]) == Decimal("2233.3483")
    assert Decimal(reporte["total_despues_pesos"]) == Decimal("2233.35")
    problemas = " | ".join(p["problema"] for p in reporte["problemas"])
    assert "fecha ilegible ('31-02-2026')" in problemas and "fecha ilegible ('ayer')" in problemas


def test_migracion_se_puede_correr_dos_veces(db_temporal):
    from db.migrador import aplicar_migraciones, _modulo, DIR_MIGRACIONES
    _base_legacy(db_temporal)
    aplicar_migraciones()
    antes = _filas(db_temporal, "SELECT * FROM comprobantes ORDER BY id")
    conn = sqlite3.connect(db_temporal)
    _modulo(6, os.path.join(DIR_MIGRACIONES, "0006_importes_fechas.py")).migrar(conn)
    conn.commit()
    conn.close()
    assert _filas(db_temporal, "SELECT * FROM comprobantes ORDER BY id") == antes


def test_dato_corrupto_deshace_toda_la_migracion(db_temporal, tmp_path):
    from db.migrador import aplicar_migraciones
    _base_legacy(db_temporal)
    conn = sqlite3.connect(db_temporal)
    conn.execute("UPDATE comprobantes SET total = 'abc' WHERE id = 2")   # importe ilegible
    conn.commit()
    conn.close()
    with pytest.raises(Exception):
        aplicar_migraciones()
    columnas = {f["name"] for f in _filas(db_temporal, "PRAGMA table_info(comprobantes)")}
    assert "total_centavos" not in columnas                        # nada a medias
    assert _filas(db_temporal, "SELECT fecha FROM comprobantes WHERE id = 1")[0]["fecha"] == "13-11-2026"
    versiones = [f["version"] for f in _filas(db_temporal, "SELECT version FROM schema_migraciones")]
    assert 6 not in versiones and 5 in versiones


def test_verificar_totales_rechaza_diferencias():
    from db.migrador import _modulo, DIR_MIGRACIONES
    m = _modulo(6, os.path.join(DIR_MIGRACIONES, "0006_importes_fechas.py"))
    m.verificar_totales(Decimal("100.00"), 10000, 0)
    m.verificar_totales(Decimal("0.015"), 2, 1)                   # medio centavo por redondeo: ok
    with pytest.raises(ValueError):
        m.verificar_totales(Decimal("100.00"), 10001, 0)          # un centavo de más: se deshace


# ─── API y emisión ─────────────────────────────────────────

def test_emision_guarda_centavos_y_fecha_iso(cliente, db_temporal):
    item = {"producto_desc": "Queso por kg", "cantidad": 1.5, "precio_unitario": 999.99, "precio_costo": 700.0}
    r = cliente.post("/api/facturacion/nuevo", json={"tipo": "factura", "items": [item]})
    assert r.json()["total"] == 1499.98                         # 1499,985 → redondeo bancario
    fila = _filas(db_temporal, "SELECT * FROM comprobantes")[0]
    assert fila["fecha"] == date.today().isoformat()
    assert (fila["subtotal_centavos"], fila["total_centavos"]) == (149998, 149998)
    assert fila["total"] == 1499.98                              # doble escritura
    hist = cliente.get("/api/facturacion/historial").json()[0]
    assert hist["fecha"] == date.today().isoformat() and hist["total"] == 1499.98


def test_descuento_se_redondea_una_sola_vez(cliente):
    item = {"producto_desc": "X", "cantidad": 1, "precio_unitario": 100.0}
    r = cliente.post("/api/facturacion/nuevo", json={"tipo": "factura", "descuento": 33.333, "items": [item]})
    assert r.json()["total"] == 66.67


def test_api_responde_en_pesos_desde_centavos_tras_migrar(db_temporal):
    from fastapi.testclient import TestClient
    from main import app
    _base_legacy(db_temporal)
    with TestClient(app) as c:
        crear_usuario("admin", {"admin"})
        login(c, "admin")
        hist = {h["numero"]: h for h in c.get("/api/facturacion/historial").json()}
        assert hist["F-000002"]["total"] == 333.33               # no 333.3333
        assert hist["F-000001"]["fecha"] == "2026-11-13"
        det = c.get("/api/facturacion/1").json()
        assert det["items"][0]["subtotal"] == 2000.0 and det["total"] == 1800.0
