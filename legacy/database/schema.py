"""
Schema de base de datos — Coronel Sur
SQLite por ahora, migrable a PostgreSQL
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'coronel_sur.db')


def get_conexion():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acceder columnas por nombre
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def crear_tablas():
    conn = get_conexion()
    cur = conn.cursor()

    # ── PRODUCTOS ──────────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo          TEXT    UNIQUE NOT NULL,
            descripcion     TEXT    NOT NULL,
            rubro           TEXT,
            proveedor       TEXT,
            precio_venta    REAL    NOT NULL DEFAULT 0,
            precio_costo    REAL    NOT NULL DEFAULT 0,
            stock_actual    INTEGER NOT NULL DEFAULT 0,
            activo          INTEGER NOT NULL DEFAULT 1,   -- 1=activo, 0=inactivo
            fecha_ingreso   TEXT,                         -- Fecha Modificado del CSV
            fecha_creacion  TEXT    DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── CLIENTES ───────────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre          TEXT    NOT NULL,
            telefono        TEXT,
            email           TEXT,
            direccion       TEXT,
            tipo            TEXT    DEFAULT 'minorista',  -- minorista / mayorista
            activo          INTEGER NOT NULL DEFAULT 1,
            fecha_creacion  TEXT    DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── FACTURAS ───────────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS facturas (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            numero          TEXT    UNIQUE,               -- numero de factura
            tipo            TEXT    DEFAULT 'venta',      -- venta / presupuesto / nota_credito
            cliente_id      INTEGER REFERENCES clientes(id),
            cliente_nombre  TEXT,                         -- para clientes sin cuenta
            fecha           TEXT    NOT NULL,
            subtotal        REAL    NOT NULL DEFAULT 0,
            descuento       REAL    NOT NULL DEFAULT 0,
            total           REAL    NOT NULL DEFAULT 0,
            estado          TEXT    DEFAULT 'emitida',    -- emitida / cobrada / anulada
            origen          TEXT    DEFAULT 'sistema',    -- sistema / importado_factu
            fecha_creacion  TEXT    DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── ITEMS DE FACTURA ───────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS factura_items (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            factura_id      INTEGER NOT NULL REFERENCES facturas(id),
            producto_id     INTEGER REFERENCES productos(id),
            descripcion     TEXT    NOT NULL,             -- nombre al momento de venta
            cantidad        REAL    NOT NULL DEFAULT 1,
            precio_venta    REAL    NOT NULL DEFAULT 0,
            precio_costo    REAL    NOT NULL DEFAULT 0,
            subtotal        REAL    NOT NULL DEFAULT 0
        )
    """)

    # ── MOVIMIENTOS DE STOCK ───────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS movimientos_stock (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id     INTEGER NOT NULL REFERENCES productos(id),
            tipo            TEXT    NOT NULL,             -- entrada / salida / ajuste
            cantidad        INTEGER NOT NULL,
            motivo          TEXT,                         -- venta / compra / ajuste_manual
            referencia_id   INTEGER,                      -- factura_id si aplica
            fecha           TEXT    DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── LOG DE IMPORTACION ─────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS log_importacion (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            archivo         TEXT    NOT NULL,
            tipo            TEXT    NOT NULL,             -- inventario / ventas / presupuestos
            filas_totales   INTEGER,
            filas_ok        INTEGER,
            filas_error     INTEGER,
            errores         TEXT,                         -- JSON con detalle
            fecha           TEXT    DEFAULT (datetime('now','localtime'))
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Tablas creadas correctamente")


if __name__ == '__main__':
    crear_tablas()
