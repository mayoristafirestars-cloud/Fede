"""Login, sesiones, CSRF, bloqueo por intentos y permisos por rol."""

import sqlite3
from datetime import timedelta

import pytest

from conftest import CONTRASENA, crear_usuario, login

ITEM = {"producto_desc": "Item", "cantidad": 1, "precio_unitario": 100.0}


def _emitir(c, headers=None):
    return c.post("/api/facturacion/nuevo", json={"tipo": "factura", "items": [ITEM]}, headers=headers)


# ─── Sin sesión no se accede a nada ────────────────────────

@pytest.mark.parametrize("metodo,ruta", [
    ("get", "/api/estado"), ("get", "/api/productos"), ("get", "/api/rubros"),
    ("get", "/api/facturacion/historial"), ("get", "/api/facturacion/1"),
    ("get", "/api/facturacion/buscar-producto?q=a"), ("post", "/api/facturacion/nuevo"),
    ("post", "/api/facturacion/1/anular"), ("get", "/api/auth/yo"), ("get", "/api/ruta-que-no-existe"),
])
def test_api_sin_sesion_da_401(cliente_anonimo, metodo, ruta):
    assert getattr(cliente_anonimo, metodo)(ruta).status_code == 401


def test_pagina_principal_sin_sesion_redirige_al_login(cliente_anonimo):
    r = cliente_anonimo.get("/", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/login"
    assert "Ingresar" in cliente_anonimo.get("/login").text


def test_salud_es_publica_y_no_expone_datos(cliente_anonimo):
    r = cliente_anonimo.get("/salud")
    assert r.status_code == 200 and r.json() == {"estado": "ok"}


# ─── Login ─────────────────────────────────────────────────

def test_login_correcto_crea_sesion_con_cookies_seguras(cliente_anonimo):
    crear_usuario("fede", {"admin"}, nombre="Fede")
    r = login(cliente_anonimo, "FEDE ")                     # sin distinguir mayúsculas ni espacios
    cookies = r.headers.get_list("set-cookie")
    sesion = next(c for c in cookies if c.startswith("cs_sesion="))
    assert "HttpOnly" in sesion and "SameSite=lax" in sesion
    yo = cliente_anonimo.get("/api/auth/yo").json()
    assert yo == {"usuario": "fede", "nombre": "Fede", "roles": ["admin"]}
    assert cliente_anonimo.get("/").status_code == 200


def test_cookie_secure_en_produccion(cliente_anonimo, monkeypatch):
    crear_usuario("fede", {"admin"})
    monkeypatch.setenv("ENTORNO", "produccion")
    r = cliente_anonimo.post("/api/auth/login", json={"usuario": "fede", "contrasena": CONTRASENA})
    assert all("Secure" in c for c in r.headers.get_list("set-cookie"))


def test_login_incorrecto_y_usuario_inexistente_dan_el_mismo_error(cliente_anonimo):
    crear_usuario("fede", {"admin"})
    malo = cliente_anonimo.post("/api/auth/login", json={"usuario": "fede", "contrasena": "otra-clave-123"})
    nadie = cliente_anonimo.post("/api/auth/login", json={"usuario": "nadie", "contrasena": "otra-clave-123"})
    assert malo.status_code == nadie.status_code == 401
    assert malo.json() == nadie.json()


def test_bloqueo_despues_de_cinco_intentos(cliente_anonimo):
    from db.database import conectar
    import seguridad
    crear_usuario("fede", {"admin"})
    for _ in range(5):
        cliente_anonimo.post("/api/auth/login", json={"usuario": "fede", "contrasena": "mala-mala-mala"})
    # aun con la contraseña correcta, queda bloqueado
    r = cliente_anonimo.post("/api/auth/login", json={"usuario": "fede", "contrasena": CONTRASENA})
    assert r.status_code == 401
    # pasado el bloqueo, vuelve a entrar
    conn = conectar()
    conn.execute("UPDATE usuario SET bloqueado_hasta = ? WHERE usuario = 'fede'",
                 ((seguridad.ahora() - timedelta(minutes=1)).isoformat(),))
    conn.commit()
    conn.close()
    login(cliente_anonimo, "fede")


def test_usuario_inactivo_no_entra(cliente_anonimo):
    from db.database import conectar
    crear_usuario("fede", {"admin"})
    conn = conectar()
    conn.execute("UPDATE usuario SET activo = 0")
    conn.commit()
    conn.close()
    r = cliente_anonimo.post("/api/auth/login", json={"usuario": "fede", "contrasena": CONTRASENA})
    assert r.status_code == 401


def test_desactivar_usuario_corta_sesiones_abiertas(cliente):
    from db.database import conectar
    conn = conectar()
    conn.execute("UPDATE usuario SET activo = 0")
    conn.commit()
    conn.close()
    assert cliente.get("/api/estado").status_code == 401


def test_sesion_vencida_no_sirve(cliente):
    from db.database import conectar
    conn = conectar()
    conn.execute("UPDATE sesion SET expira_en = '2000-01-01T00:00:00+00:00'")
    conn.commit()
    conn.close()
    assert cliente.get("/api/estado").status_code == 401


def test_logout_revoca_la_sesion(cliente):
    token = cliente.cookies.get("cs_sesion")
    assert cliente.post("/api/auth/logout").status_code == 200
    cliente.cookies.set("cs_sesion", token)          # aunque se reuse el token viejo
    assert cliente.get("/api/estado").status_code == 401


def test_token_no_se_guarda_en_claro(cliente, db_temporal):
    token = cliente.cookies.get("cs_sesion")
    conn = sqlite3.connect(db_temporal)
    guardados = [r[0] for r in conn.execute("SELECT token_hmac FROM sesion")]
    hashes = [r[0] for r in conn.execute("SELECT hash_contrasena FROM usuario")]
    conn.close()
    assert token not in guardados
    assert all(h.startswith("$argon2") and CONTRASENA not in h for h in hashes)


# ─── CSRF ──────────────────────────────────────────────────

def test_post_sin_token_csrf_da_403(cliente):
    del cliente.headers["X-CSRF-Token"]
    assert _emitir(cliente).status_code == 403
    assert _emitir(cliente, headers={"X-CSRF-Token": "falso"}).status_code == 403


# ─── Permisos por rol ──────────────────────────────────────

@pytest.mark.parametrize("rol,puede_emitir,puede_anular", [
    ("admin", True, True),
    ("responsable_cobranza", True, False),
    ("cobrador", False, False),
    ("consulta", False, False),
])
def test_permisos_de_facturacion_por_rol(cliente_anonimo, rol, puede_emitir, puede_anular):
    crear_usuario("jefe", {"admin"})
    login(cliente_anonimo, "jefe")
    cid = _emitir(cliente_anonimo).json()["comprobante_id"]
    cliente_anonimo.post("/api/auth/logout")

    crear_usuario("persona", {rol})
    login(cliente_anonimo, "persona")
    assert cliente_anonimo.get("/api/facturacion/historial").status_code == 200   # todos leen
    assert (_emitir(cliente_anonimo).status_code == 200) == puede_emitir
    r = cliente_anonimo.post(f"/api/facturacion/{cid}/anular")
    assert (r.status_code == 200) == puede_anular
    if not puede_anular:
        assert r.status_code == 403


def test_crear_usuario_valida_datos(db_temporal):
    from db.migrador import aplicar_migraciones
    from db.database import conectar
    import seguridad
    aplicar_migraciones()
    conn = conectar()
    with pytest.raises(ValueError):
        seguridad.crear_usuario(conn, "a", "A", "corta", {"admin"})
    with pytest.raises(ValueError):
        seguridad.crear_usuario(conn, "a", "A", CONTRASENA, {"rol_inventado"})
    seguridad.crear_usuario(conn, "a", "A", CONTRASENA, {"admin"})
    with pytest.raises(ValueError):
        seguridad.crear_usuario(conn, "A", "Otro", CONTRASENA, {"admin"})   # duplicado
    conn.close()


def test_produccion_sin_secret_key_no_arranca(db_temporal, monkeypatch):
    from fastapi.testclient import TestClient
    from main import app
    monkeypatch.setenv("ENTORNO", "produccion")
    monkeypatch.delenv("SECRET_KEY")
    with pytest.raises(RuntimeError):
        with TestClient(app):
            pass
