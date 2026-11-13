"""
Pruebas de caracterización: fijan cómo funciona HOY la facturación.
Si alguna falla después de un cambio, el comportamiento para el usuario cambió.
"""

from conftest import stock_de


def _emitir(cliente, tipo="factura", items=None, descuento=0.0, nombre="Almacén Don Pepe"):
    body = {"tipo": tipo, "cliente_nombre": nombre, "descuento": descuento, "items": items or []}
    return cliente.post("/api/facturacion/nuevo", json=body)


def _item(pid=None, cantidad=2, precio=1000.0, desc="Yerba 1kg"):
    return {"producto_id": pid, "producto_desc": desc, "cantidad": cantidad, "precio_unitario": precio, "precio_costo": 600.0}


def test_crear_factura_devuelve_numero_y_total(cliente, cargar_producto):
    pid = cargar_producto()
    r = _emitir(cliente, items=[_item(pid, 2, 1000.0)], descuento=10)
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["numero"] == "F-000001"
    assert data["total"] == 1800.0


def test_crear_presupuesto_usa_prefijo_p(cliente, cargar_producto):
    pid = cargar_producto()
    r = _emitir(cliente, tipo="presupuesto", items=[_item(pid)])
    assert r.status_code == 200
    assert r.json()["numero"] == "P-000001"


def test_factura_descuenta_stock_y_presupuesto_no(cliente, cargar_producto):
    pid = cargar_producto(stock=10)
    _emitir(cliente, tipo="presupuesto", items=[_item(pid, 3)])
    assert stock_de(pid) == 10
    _emitir(cliente, tipo="factura", items=[_item(pid, 3)])
    assert stock_de(pid) == 7


def test_item_sin_producto_no_toca_stock(cliente, cargar_producto):
    pid = cargar_producto(stock=10)
    r = _emitir(cliente, items=[_item(None, 5, desc="Flete")])
    assert r.status_code == 200
    assert stock_de(pid) == 10


def test_comprobante_sin_items_da_400(cliente):
    r = _emitir(cliente, items=[])
    assert r.status_code == 400


def test_historial_lista_y_filtra(cliente, cargar_producto):
    pid = cargar_producto()
    _emitir(cliente, tipo="factura", items=[_item(pid)])
    _emitir(cliente, tipo="presupuesto", items=[_item(pid)])
    todos = cliente.get("/api/facturacion/historial").json()
    assert [c["numero"] for c in todos] == ["P-000001", "F-000001"]   # más nuevo primero
    solo_f = cliente.get("/api/facturacion/historial?tipo=factura").json()
    assert [c["numero"] for c in solo_f] == ["F-000001"]
    campos = set(todos[0].keys())
    assert {"id", "tipo", "numero", "cliente_nombre", "fecha", "subtotal", "descuento", "total", "estado"} <= campos


def test_detalle_incluye_items(cliente, cargar_producto):
    pid = cargar_producto()
    cid = _emitir(cliente, items=[_item(pid, 2, 1000.0)]).json()["comprobante_id"]
    det = cliente.get(f"/api/facturacion/{cid}").json()
    assert det["numero"] == "F-000001"
    assert len(det["items"]) == 1
    assert det["items"][0]["cantidad"] == 2
    assert det["items"][0]["subtotal"] == 2000.0


def test_detalle_inexistente_da_404(cliente):
    assert cliente.get("/api/facturacion/999").status_code == 404


def test_anular_factura_revierte_stock_y_sale_del_historial(cliente, cargar_producto):
    pid = cargar_producto(stock=10)
    cid = _emitir(cliente, items=[_item(pid, 4)]).json()["comprobante_id"]
    assert stock_de(pid) == 6
    r = cliente.post(f"/api/facturacion/{cid}/anular")
    assert r.status_code == 200
    assert stock_de(pid) == 10
    assert cliente.get("/api/facturacion/historial").json() == []
    assert cliente.get(f"/api/facturacion/{cid}").json()["estado"] == "anulado"


def test_anular_dos_veces_da_400(cliente, cargar_producto):
    pid = cargar_producto()
    cid = _emitir(cliente, items=[_item(pid)]).json()["comprobante_id"]
    assert cliente.post(f"/api/facturacion/{cid}/anular").status_code == 200
    r = cliente.post(f"/api/facturacion/{cid}/anular")
    assert r.status_code == 400
    assert r.json()["detail"] == "Ya está anulado"


def test_anular_inexistente_da_404(cliente):
    assert cliente.post("/api/facturacion/999/anular").status_code == 404


def test_buscar_producto_solo_con_stock(cliente, cargar_producto):
    cargar_producto(codigo="A1", descripcion="Azucar 1kg", stock=5)
    cargar_producto(codigo="A2", descripcion="Azucar 5kg", stock=0)
    res = cliente.get("/api/facturacion/buscar-producto?q=azucar").json()
    assert [p["codigo"] for p in res] == ["A1"]


def test_estado_productos_y_rubros(cliente, cargar_producto):
    cargar_producto(codigo="A1", rubro="Almacen")
    cargar_producto(codigo="B1", rubro="Bebidas")
    assert cliente.get("/api/estado").json()["registros"]["productos"] == 2
    assert len(cliente.get("/api/productos").json()) == 2
    assert len(cliente.get("/api/productos?rubro=Bebidas").json()) == 1
    rubros = {r["rubro"] for r in cliente.get("/api/rubros").json()}
    assert rubros == {"Almacen", "Bebidas"}


def test_pagina_principal_responde(cliente):
    r = cliente.get("/")
    assert r.status_code == 200
    assert "Coronel Sur" in r.text
