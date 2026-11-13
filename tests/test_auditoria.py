"""Auditoría: qué se registra, que no se pueda modificar y que no guarde secretos."""

import json
import sqlite3

import pytest

from conftest import CONTRASENA, crear_usuario, login

ITEM = {"producto_desc": "Item", "cantidad": 1, "precio_unitario": 100.0}


def _eventos(db, accion=None):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    sql, params = "SELECT * FROM evento_auditoria", ()
    if accion:
        sql, params = sql + " WHERE accion = ?", (accion,)
    filas = [dict(f) for f in conn.execute(sql + " ORDER BY id", params)]
    conn.close()
    return filas


def test_migraciones_quedan_auditadas(cliente_anonimo, db_temporal):
    versiones = {e["entidad_id"] for e in _eventos(db_temporal, "migracion.aplicar")}
    assert {"1", "2", "3", "4", "5"} <= versiones


def test_login_logout_emision_y_anulacion(cliente, db_temporal):
    cid = cliente.post("/api/facturacion/nuevo", json={"tipo": "factura", "cliente_nombre": "Kiosco Sol", "items": [ITEM]}).json()["comprobante_id"]
    cliente.post(f"/api/facturacion/{cid}/anular")
    cliente.post("/api/auth/logout")

    acciones = [e["accion"] for e in _eventos(db_temporal) if not e["accion"].startswith("migracion")]
    assert acciones == ["login", "comprobante.emitir", "comprobante.anular", "logout"]

    emitir = _eventos(db_temporal, "comprobante.emitir")[0]
    assert emitir["actor_texto"] == "admin" and emitir["empresa_id"] == 1 and emitir["actor_usuario_id"]
    assert json.loads(emitir["despues"])["numero"] == "F-000001"
    anular = _eventos(db_temporal, "comprobante.anular")[0]
    assert json.loads(anular["antes"])["estado"] == "activo"
    assert json.loads(anular["despues"])["estado"] == "anulado"
    assert anular["ip"]


def test_login_fallido_registra_motivo_sin_guardar_lo_tecleado(cliente_anonimo, db_temporal):
    crear_usuario("fede", {"admin"})
    cliente_anonimo.post("/api/auth/login", json={"usuario": "fede", "contrasena": "mala-mala-mala"})
    cliente_anonimo.post("/api/auth/login", json={"usuario": "MiClaveSecreta!", "contrasena": "x"})
    fallidos = _eventos(db_temporal, "login.fallido")
    assert [json.loads(e["despues"])["motivo"] for e in fallidos] == ["contrasena", "inexistente"]
    assert fallidos[0]["actor_texto"] == "fede"
    assert fallidos[1]["actor_texto"] == "(usuario inexistente)"
    volcado = json.dumps(_eventos(db_temporal))
    assert "MiClaveSecreta" not in volcado and "mala-mala-mala" not in volcado


def test_no_quedan_contrasenas_ni_tokens_en_la_auditoria(cliente, db_temporal):
    token = cliente.cookies.get("cs_sesion")
    volcado = json.dumps(_eventos(db_temporal))
    assert CONTRASENA not in volcado and token not in volcado


def test_emision_fallida_no_deja_evento(cliente, db_temporal):
    r = cliente.post("/api/facturacion/nuevo", json={"tipo": "factura", "items": []})
    assert r.status_code == 400
    assert _eventos(db_temporal, "comprobante.emitir") == []


@pytest.mark.parametrize("sql", [
    "UPDATE evento_auditoria SET accion = 'otra'",
    "DELETE FROM evento_auditoria",
])
def test_la_auditoria_no_se_puede_modificar_ni_borrar(cliente, db_temporal, sql):
    conn = sqlite3.connect(db_temporal)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(sql)
    conn.close()


def test_crear_usuario_por_consola_queda_auditado(cliente_anonimo, db_temporal):
    import importlib.util, os
    from conftest import RAIZ
    import sys
    sys.path.insert(0, os.path.join(RAIZ, "scripts"))
    spec = importlib.util.spec_from_file_location("crear_admin", os.path.join(RAIZ, "scripts", "crear_admin.py"))
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    uid = modulo.crear("Fede", "Fede", CONTRASENA, {"admin"})
    evento = _eventos(db_temporal, "usuario.crear")[0]
    assert evento["entidad_id"] == str(uid) and evento["actor_texto"] == "consola"
    assert json.loads(evento["despues"])["roles"] == ["admin"]
    assert CONTRASENA not in json.dumps(evento)


def test_restaurar_por_consola_queda_auditado(cliente_anonimo, db_temporal):
    import importlib.util, os
    from conftest import RAIZ
    from db import respaldos
    copia = respaldos.respaldar(motivo="prueba")
    spec = importlib.util.spec_from_file_location("restaurar", os.path.join(RAIZ, "scripts", "restaurar.py"))
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    previo = respaldos.restaurar(copia)
    modulo._auditar(copia, previo)
    assert len(_eventos(db_temporal, "respaldo.restaurar")) == 1
