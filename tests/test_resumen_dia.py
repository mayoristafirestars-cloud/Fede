"""Ganancia y margen del día con el costo real de cada ítem."""

import sqlite3
from datetime import date

from conftest import crear_usuario, login


def _item(cantidad, precio, costo, desc="Producto"):
    return {"producto_desc": desc, "cantidad": cantidad, "precio_unitario": precio, "precio_costo": costo}


def _emitir(c, items, tipo="factura", descuento=0):
    r = c.post("/api/facturacion/nuevo", json={"tipo": tipo, "descuento": descuento, "items": items})
    assert r.status_code == 200, r.text
    return r.json()


def test_sin_ventas(cliente):
    d = cliente.get("/api/facturacion/resumen-dia").json()
    assert d["fecha"] == date.today().isoformat()
    assert (d["facturas"], d["total"], d["costo"], d["ganancia"], d["margen_pct"]) == (0, 0.0, 0.0, 0.0, None)


def test_ganancia_con_costos_reales_y_descuento(cliente):
    _emitir(cliente, [_item(2, 1000.0, 600.0)], descuento=10)           # venta 1800, costo 1200
    _emitir(cliente, [_item(1.5, 1000.0, 700.0), _item(3, 50.0, 20.0)])  # venta 1650, costo 1110
    d = cliente.get("/api/facturacion/resumen-dia").json()
    assert d["facturas"] == 2
    assert d["total"] == 3450.0
    assert d["costo"] == 2310.0
    assert d["ganancia"] == 1140.0
    assert d["margen_pct"] == 33.04                                      # 1140 / 3450
    assert d["items_sin_costo"] == 0


def test_presupuestos_y_anuladas_no_cuentan(cliente):
    _emitir(cliente, [_item(1, 1000.0, 500.0)])
    _emitir(cliente, [_item(10, 1000.0, 500.0)], tipo="presupuesto")
    anulada = _emitir(cliente, [_item(5, 1000.0, 500.0)])
    cliente.post(f"/api/facturacion/{anulada['comprobante_id']}/anular")
    d = cliente.get("/api/facturacion/resumen-dia").json()
    assert (d["facturas"], d["total"], d["ganancia"]) == (1, 1000.0, 500.0)


def test_venta_bajo_costo_da_ganancia_negativa(cliente):
    _emitir(cliente, [_item(1, 800.0, 1000.0)])
    d = cliente.get("/api/facturacion/resumen-dia").json()
    assert d["ganancia"] == -200.0 and d["margen_pct"] == -25.0


def test_items_sin_costo_se_informan(cliente):
    _emitir(cliente, [_item(1, 1000.0, 600.0), _item(1, 500.0, 0.0, "Flete")])
    d = cliente.get("/api/facturacion/resumen-dia").json()
    assert d["items_sin_costo"] == 1
    assert d["ganancia"] == 900.0          # el flete sin costo infla la ganancia: por eso se avisa


def test_filtra_por_fecha(cliente, db_temporal):
    _emitir(cliente, [_item(1, 1000.0, 600.0)])
    conn = sqlite3.connect(db_temporal)
    conn.execute("UPDATE comprobantes SET fecha = '2026-01-15'")
    conn.commit()
    conn.close()
    assert cliente.get("/api/facturacion/resumen-dia").json()["facturas"] == 0
    d = cliente.get("/api/facturacion/resumen-dia?fecha=2026-01-15").json()
    assert (d["facturas"], d["ganancia"]) == (1, 400.0)


def test_fecha_invalida_da_400(cliente):
    assert cliente.get("/api/facturacion/resumen-dia?fecha=15-01-2026").status_code == 400


def test_rol_consulta_puede_verlo_y_sin_sesion_no(cliente_anonimo):
    assert cliente_anonimo.get("/api/facturacion/resumen-dia").status_code == 401
    crear_usuario("mirador", {"consulta"})
    login(cliente_anonimo, "mirador")
    assert cliente_anonimo.get("/api/facturacion/resumen-dia").status_code == 200


def test_funciona_con_comprobantes_migrados(db_temporal):
    """Comprobantes viejos (migración 0006): usa los centavos convertidos."""
    from fastapi.testclient import TestClient
    from main import app
    from test_importes_fechas import _base_legacy
    _base_legacy(db_temporal)
    with TestClient(app) as c:
        crear_usuario("admin", {"admin"})
        login(c, "admin")
        d = c.get("/api/facturacion/resumen-dia?fecha=2026-11-13").json()
        assert (d["facturas"], d["total"], d["costo"], d["ganancia"]) == (1, 1800.0, 1200.0, 600.0)


# ─── Ganancia sin IVA (Responsable Inscripto: precios y costos con IVA incluido) ───

def test_sin_iva(cliente):
    _emitir(cliente, [_item(2, 1000.0, 600.0)], descuento=10)
    _emitir(cliente, [_item(1.5, 1000.0, 700.0), _item(3, 50.0, 20.0)])
    d = cliente.get("/api/facturacion/resumen-dia").json()
    assert d["alicuota_iva"] == 21.0
    assert d["total_sin_iva"] == 2851.24          # 3450 / 1,21
    assert d["costo_sin_iva"] == 1909.09          # 2310 / 1,21
    assert d["ganancia_sin_iva"] == 942.15        # 1140 / 1,21
    assert d["margen_pct"] == 33.04               # el margen no cambia


def test_sin_iva_con_perdida(cliente):
    _emitir(cliente, [_item(1, 800.0, 1000.0)])
    d = cliente.get("/api/facturacion/resumen-dia").json()
    assert d["ganancia_sin_iva"] == -165.29


def test_alicuota_configurable(cliente, monkeypatch):
    monkeypatch.setenv("IVA_ALICUOTA", "10.5")
    _emitir(cliente, [_item(1, 1105.0, 0.0)])
    d = cliente.get("/api/facturacion/resumen-dia").json()
    assert d["alicuota_iva"] == 10.5 and d["total_sin_iva"] == 1000.0


def test_quitar_iva():
    from decimal import Decimal
    from dinero import sin_iva
    assert sin_iva(121000, Decimal("21")) == 100000
    assert sin_iva(0, Decimal("21")) == 0
    assert sin_iva(100, Decimal("0")) == 100
