"""
Configuración común de pruebas.
Cada prueba usa una base SQLite temporal: nunca la base real.
"""

import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "backend"))


@pytest.fixture
def db_temporal(tmp_path, monkeypatch):
    """Apunta DB_PATH a una base nueva dentro de tmp_path."""
    ruta = tmp_path / "prueba.db"
    monkeypatch.setenv("DB_PATH", str(ruta))
    return ruta


@pytest.fixture
def cliente(db_temporal):
    """Cliente HTTP de la app con la base temporal ya inicializada."""
    from fastapi.testclient import TestClient
    from main import app
    with TestClient(app) as c:
        yield c


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
