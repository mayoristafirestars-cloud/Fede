"""Numeración de comprobantes con secuencia."""

import os
import sqlite3
import threading


def _emitir(cliente, tipo="factura"):
    body = {"tipo": tipo, "cliente_nombre": "X", "items": [{"producto_desc": "Item", "cantidad": 1, "precio_unitario": 100.0}]}
    r = cliente.post("/api/facturacion/nuevo", json=body)
    assert r.status_code == 200
    return r.json()


def test_emisiones_y_anulacion_no_repiten(cliente):
    f1 = _emitir(cliente)
    f2 = _emitir(cliente)
    assert cliente.post(f"/api/facturacion/{f2['comprobante_id']}/anular").status_code == 200
    f3 = _emitir(cliente)
    p1 = _emitir(cliente, "presupuesto")
    assert [f1["numero"], f2["numero"], f3["numero"]] == ["F-000001", "F-000002", "F-000003"]
    assert p1["numero"] == "P-000001"


def test_secuencia_arranca_desde_el_maximo_existente(db_temporal):
    """Base de producción con comprobantes previos (sin tabla secuencias)."""
    from db.migrador import DIR_MIGRACIONES
    conn = sqlite3.connect(db_temporal)
    conn.executescript(open(os.path.join(DIR_MIGRACIONES, "0001_esquema_inicial.sql"), encoding="utf-8").read())
    for n in (1, 2, 5):
        conn.execute("INSERT INTO comprobantes (tipo, numero, fecha, total) VALUES ('factura', ?, '01-10-2026', 10)", (f"F-{n:06d}",))
    conn.execute("INSERT INTO comprobantes (tipo, numero, fecha, total) VALUES ('presupuesto', 'P-000007', '01-10-2026', 10)")
    conn.commit()
    conn.close()

    from fastapi.testclient import TestClient
    from main import app
    with TestClient(app) as cliente:
        assert _emitir(cliente)["numero"] == "F-000006"
        assert _emitir(cliente, "presupuesto")["numero"] == "P-000008"


def test_concurrencia_no_repite_numeros(db_temporal):
    from db.migrador import aplicar_migraciones
    from db.database import conectar
    from db.secuencias import siguiente_numero
    aplicar_migraciones()
    obtenidos, errores = [], []

    def tomar():
        try:
            conn = conectar()
            n = siguiente_numero(conn, 1, "factura")
            conn.commit()
            conn.close()
            obtenidos.append(n)
        except Exception as e:      # pragma: no cover
            errores.append(e)

    hilos = [threading.Thread(target=tomar) for _ in range(20)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    assert errores == []
    assert sorted(obtenidos) == list(range(1, 21))


def test_emision_fallida_no_consume_numero(db_temporal):
    from db.migrador import aplicar_migraciones
    from db.database import conectar
    from db.secuencias import siguiente_numero
    aplicar_migraciones()
    conn = conectar()
    siguiente_numero(conn, 1, "factura")
    conn.rollback()                                  # la emisión falló
    assert siguiente_numero(conn, 1, "factura") == 1
    conn.close()
