"""
Configuración común de pruebas.
Cada prueba usa una base SQLite temporal: nunca la base real.
"""

import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "backend"))

CONTRASENA = "clave-de-prueba-123"


@pytest.fixture(autouse=True)
def entorno_de_prueba(monkeypatch, tmp_path):
    """Entorno aislado: desarrollo, clave fija de prueba y respaldos en tmp."""
    monkeypatch.setenv("ENTORNO", "desarrollo")
    monkeypatch.setenv("SECRET_KEY", "clave-secreta-solo-para-pruebas-0123456789")
    monkeypatch.setenv("BACKUP_DIR", str(tmp_path / "respaldos"))


@pytest.fixture
def db_temporal(tmp_path, monkeypatch):
    """Apunta DB_PATH a una base nueva dentro de tmp_path."""
    ruta = tmp_path / "prueba.db"
    monkeypatch.setenv("DB_PATH", str(ruta))
    return ruta


def crear_usuario(usuario, roles, empresa_id=1, nombre=None):
    from db.database import conectar
    import seguridad
    conn = conectar()
    uid = seguridad.crear_usuario(conn, usuario, nombre or usuario.title(), CONTRASENA, set(roles), empresa_id)
    conn.commit()
    conn.close()
    return uid


def login(c, usuario, contrasena=CONTRASENA):
    """Inicia sesión y deja el token CSRF como encabezado por defecto del cliente."""
    r = c.post("/api/auth/login", json={"usuario": usuario, "contrasena": contrasena})
    assert r.status_code == 200, r.text
    c.headers["X-CSRF-Token"] = c.cookies.get("cs_csrf")
    return r


@pytest.fixture
def cliente_anonimo(db_temporal):
    """Cliente HTTP sin sesión, con la base temporal ya inicializada."""
    from fastapi.testclient import TestClient
    from main import app
    with TestClient(app) as c:
        yield c


@pytest.fixture
def cliente(cliente_anonimo):
    """Cliente con sesión de administrador (para las pruebas de comportamiento)."""
    crear_usuario("admin", {"admin"})
    login(cliente_anonimo, "admin")
    return cliente_anonimo


@pytest.fixture
def cargar_producto(cliente):
    """Inserta un producto directo en la base y devuelve su id."""
    from db.database import conectar

    def _cargar(codigo="P1", descripcion="Yerba 1kg", stock=10, precio_venta=1000.0, precio_costo=600.0, rubro="Almacen"):
        conn = conectar()
        cur = conn.execute(
            "INSERT INTO productos (codigo, descripcion, rubro, stock, precio_venta, precio_costo) VALUES (?,?,?,?,?,?)",
            (codigo, descripcion, rubro, stock, precio_venta, precio_costo),
        )
        conn.commit()
        pid = cur.lastrowid
        conn.close()
        return pid

    return _cargar


def stock_de(producto_id):
    from db.database import conectar
    conn = conectar()
    valor = conn.execute("SELECT stock FROM productos WHERE id = ?", (producto_id,)).fetchone()[0]
    conn.close()
    return valor
