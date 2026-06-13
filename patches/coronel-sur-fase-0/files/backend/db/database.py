"""
Base de datos — SQLite (local/Render disk) o PostgreSQL (via DATABASE_URL).

Cambios respecto a la versión anterior:
- SQLite detecta /data/ montado (Render Disk) y usa /data/coronel_sur.db
  si existe, así la DB sobrevive a los deploys.
- Nueva tabla sesiones (reemplaza SESIONES_ACTIVAS en memoria).
- Nueva tabla auditoria para log de acciones sensibles.
- Nueva columna debe_cambiar_password en usuarios.
- NO se insertan usuarios hardcodeados. La creación inicial la hace
  el script scripts/rotate_passwords.py o el endpoint /api/admin/crear-usuarios.
"""
from __future__ import annotations

import os
import sqlite3

DATABASE_URL = os.environ.get("DATABASE_URL", "")
USE_PG = DATABASE_URL.startswith("postgresql") or DATABASE_URL.startswith("postgres")


def _resolver_db_path() -> str:
    """
    Orden de preferencia:
      1. DB_PATH (variable de entorno explícita).
      2. /data/coronel_sur.db (Render Disk montado).
      3. backend/db/coronel_sur.db (local dev).
    """
    explicit = os.environ.get("DB_PATH", "").strip()
    if explicit:
        return explicit

    # Render Disk — si /data existe y es escribible, usarlo.
    data_dir = "/data"
    if os.path.isdir(data_dir) and os.access(data_dir, os.W_OK):
        return os.path.join(data_dir, "coronel_sur.db")

    # Local dev — backend/db/coronel_sur.db
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "db", "coronel_sur.db")


DB_PATH = _resolver_db_path()


if USE_PG:
    import psycopg2
    import psycopg2.extras


# ─── Wrapper PostgreSQL ──────────────────────────────────────

class PGConn:
    def __init__(self):
        self._c = psycopg2.connect(DATABASE_URL)
        self._c.autocommit = False

    def execute(self, sql, params=()):
        sql = _pg_sql(sql)
        cur = self._c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql, params or ())
        return PGCur(cur, self._c)

    def commit(self):
        self._c.commit()

    def rollback(self):
        self._c.rollback()

    def close(self):
        try:
            self._c.close()
        except Exception:
            pass


class PGCur:
    def __init__(self, cur, conn):
        self._cur = cur
        self._conn = conn
        self._lastrowid = None
        if cur.description and cur.description[0].name == "id":
            try:
                row = cur.fetchone()
                if row:
                    self._lastrowid = row["id"]
            except Exception:
                pass

    @property
    def lastrowid(self):
        return self._lastrowid

    @property
    def rowcount(self):
        return self._cur.rowcount

    def fetchone(self):
        row = self._cur.fetchone()
        return DictRow(row) if row else None

    def fetchall(self):
        return [DictRow(r) for r in (self._cur.fetchall() or [])]

    def __getitem__(self, key):
        return self.fetchone()[key]


class DictRow:
    def __init__(self, data):
        self._d = dict(data) if data else {}

    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self._d.values())[key]
        return self._d[key]

    def get(self, key, default=None):
        return self._d.get(key, default)

    def keys(self):
        return self._d.keys()

    def __iter__(self):
        return iter(self._d.values())


def _pg_sql(sql):
    """Convierte SQL SQLite → PostgreSQL."""
    import re
    sql = sql.replace("?", "%s")
    sql = re.sub(r"\bAUTOINCREMENT\b", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"datetime\('now'[^)]*\)", "NOW()::TEXT", sql)
    sql = re.sub(r"date\('now'[^)]*\)", "NOW()::TEXT", sql)
    sql = re.sub(r"\bINSERT OR IGNORE\b", "INSERT", sql, flags=re.IGNORECASE)
    s = sql.strip().upper()
    if s.startswith("INSERT") and "RETURNING" not in s and "ON CONFLICT" not in s:
        sql = sql.rstrip("; \n") + " RETURNING id"
    elif s.startswith("INSERT") and "ON CONFLICT" in s and "RETURNING" not in s:
        sql = sql.rstrip("; \n") + " RETURNING id"
    return sql


# ─── API pública ─────────────────────────────────────────────

def conectar():
    if USE_PG:
        return PGConn()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def inicializar_db():
    if USE_PG:
        _init_pg()
    else:
        _init_sqlite()


def _init_sqlite():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(_SCHEMA_SQLITE)
    conn.close()
    print(f"SQLite lista: {DB_PATH}")


def _init_pg():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    for stmt in _SCHEMA_PG.split(";"):
        s = stmt.strip()
        if not s:
            continue
        try:
            cur.execute(s)
            conn.commit()
        except Exception:
            conn.rollback()
    conn.close()
    print("PostgreSQL lista")


# ─── Schemas ─────────────────────────────────────────────────

_SCHEMA_SQLITE = """
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL, descripcion TEXT NOT NULL,
    rubro TEXT, proveedor TEXT, stock REAL DEFAULT 0,
    precio_venta REAL DEFAULT 0, precio_costo REAL DEFAULT 0,
    precio_mayorista REAL DEFAULT 0, fecha_ingreso TEXT,
    ean TEXT DEFAULT '', foto_url TEXT DEFAULT '',
    activo INTEGER DEFAULT 1,
    creado_en TEXT DEFAULT (datetime('now','localtime')),
    actualizado_en TEXT DEFAULT (datetime('now','localtime'))
);
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL, telefono TEXT, email TEXT, dni TEXT,
    direccion TEXT, tipo TEXT DEFAULT 'minorista', notas TEXT,
    creado_en TEXT DEFAULT (datetime('now','localtime')),
    actualizado_en TEXT DEFAULT (datetime('now','localtime'))
);
CREATE TABLE IF NOT EXISTS comprobantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL, numero TEXT,
    cliente_id INTEGER, cliente_nombre TEXT,
    fecha TEXT NOT NULL, subtotal REAL DEFAULT 0,
    descuento REAL DEFAULT 0, total REAL DEFAULT 0,
    estado TEXT DEFAULT 'activo', forma_pago TEXT DEFAULT 'efectivo',
    origen TEXT DEFAULT 'sistema',
    creado_en TEXT DEFAULT (datetime('now','localtime'))
);
CREATE TABLE IF NOT EXISTS comprobante_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comprobante_id INTEGER, producto_id INTEGER,
    producto_desc TEXT, cantidad REAL DEFAULT 1,
    precio_unitario REAL DEFAULT 0, precio_costo REAL DEFAULT 0,
    subtotal REAL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS ventas_historicas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT, codigo TEXT, producto TEXT, producto_desc TEXT,
    rubro TEXT, cantidad REAL DEFAULT 0, subtotal REAL DEFAULT 0,
    ganancia REAL DEFAULT 0, cliente TEXT, cliente_nombre TEXT,
    origen TEXT DEFAULT 'factupyme'
);
CREATE TABLE IF NOT EXISTS numeracion_afip (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT UNIQUE NOT NULL, punto_venta TEXT DEFAULT '0001',
    ultimo_num INTEGER DEFAULT 0
);
INSERT OR IGNORE INTO numeracion_afip (tipo,punto_venta,ultimo_num) VALUES ('factura','0001',0);
INSERT OR IGNORE INTO numeracion_afip (tipo,punto_venta,ultimo_num) VALUES ('presupuesto','0001',0);
INSERT OR IGNORE INTO numeracion_afip (tipo,punto_venta,ultimo_num) VALUES ('remito','0001',0);
INSERT OR IGNORE INTO numeracion_afip (tipo,punto_venta,ultimo_num) VALUES ('nota_credito','0001',0);
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL, nombre TEXT NOT NULL,
    password_hash TEXT NOT NULL, rol TEXT DEFAULT 'facturacion',
    activo INTEGER DEFAULT 1,
    debe_cambiar_password INTEGER DEFAULT 0,
    creado_en TEXT DEFAULT (datetime('now','localtime'))
);
CREATE TABLE IF NOT EXISTS sesiones (
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    rol TEXT NOT NULL,
    nombre TEXT NOT NULL,
    ip TEXT DEFAULT '',
    user_agent TEXT DEFAULT '',
    creado_en TEXT NOT NULL,
    expira_en TEXT NOT NULL,
    ultima_actividad TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sesiones_user ON sesiones(user_id);
CREATE INDEX IF NOT EXISTS idx_sesiones_expira ON sesiones(expira_en);
CREATE TABLE IF NOT EXISTS auditoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT DEFAULT (datetime('now','localtime')),
    user_id INTEGER,
    username TEXT,
    rol TEXT,
    accion TEXT NOT NULL,
    recurso TEXT,
    detalle TEXT,
    ip TEXT,
    exito INTEGER DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_auditoria_fecha ON auditoria(fecha);
CREATE INDEX IF NOT EXISTS idx_auditoria_user ON auditoria(user_id);
CREATE TABLE IF NOT EXISTS caja_sesiones (
    id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT NOT NULL,
    apertura TEXT, cierre TEXT, saldo_inicial REAL DEFAULT 0,
    saldo_final REAL, total_ingresos REAL DEFAULT 0,
    total_egresos REAL DEFAULT 0, estado TEXT DEFAULT 'abierta',
    creado_en TEXT DEFAULT (datetime('now','localtime'))
);
CREATE TABLE IF NOT EXISTS caja_movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT, sesion_id INTEGER,
    tipo TEXT NOT NULL, descripcion TEXT, monto REAL DEFAULT 0,
    comprobante_id INTEGER,
    creado_en TEXT DEFAULT (datetime('now','localtime'))
);
CREATE TABLE IF NOT EXISTS cuenta_corriente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER, cliente_nombre TEXT NOT NULL,
    comprobante_id INTEGER, tipo TEXT NOT NULL, concepto TEXT NOT NULL,
    monto REAL NOT NULL, saldo_post REAL NOT NULL,
    fecha TEXT, forma_cobro TEXT,
    creado_en TEXT DEFAULT (datetime('now','localtime'))
);
CREATE TABLE IF NOT EXISTS compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT, numero TEXT,
    proveedor TEXT NOT NULL, fecha TEXT, total REAL DEFAULT 0,
    estado TEXT DEFAULT 'pendiente', notas TEXT,
    creado_en TEXT DEFAULT (datetime('now','localtime'))
);
CREATE TABLE IF NOT EXISTS compra_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT, compra_id INTEGER,
    producto_id INTEGER, producto_desc TEXT,
    cantidad REAL, precio_costo REAL, subtotal REAL
);
CREATE TABLE IF NOT EXISTS pedidos_tienda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_cliente TEXT NOT NULL, telefono TEXT,
    tipo_entrega TEXT DEFAULT 'retiro', direccion TEXT,
    notas TEXT, subtotal REAL DEFAULT 0,
    estado TEXT DEFAULT 'pendiente',
    creado_en TEXT DEFAULT (datetime('now','localtime'))
);
CREATE TABLE IF NOT EXISTS pedidos_tienda_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT, pedido_id INTEGER,
    descripcion TEXT, cantidad REAL DEFAULT 1,
    precio REAL DEFAULT 0, subtotal REAL DEFAULT 0
);
"""

_SCHEMA_PG = """
CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY, codigo TEXT UNIQUE NOT NULL,
    descripcion TEXT NOT NULL, rubro TEXT, proveedor TEXT,
    stock REAL DEFAULT 0, precio_venta REAL DEFAULT 0,
    precio_costo REAL DEFAULT 0, precio_mayorista REAL DEFAULT 0,
    fecha_ingreso TEXT, ean TEXT DEFAULT '', foto_url TEXT DEFAULT '',
    activo INTEGER DEFAULT 1,
    creado_en TEXT DEFAULT NOW()::TEXT, actualizado_en TEXT DEFAULT NOW()::TEXT
);
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY, nombre TEXT NOT NULL, telefono TEXT,
    email TEXT, dni TEXT, direccion TEXT, tipo TEXT DEFAULT 'minorista',
    notas TEXT, creado_en TEXT DEFAULT NOW()::TEXT, actualizado_en TEXT DEFAULT NOW()::TEXT
);
CREATE TABLE IF NOT EXISTS comprobantes (
    id SERIAL PRIMARY KEY, tipo TEXT NOT NULL, numero TEXT,
    cliente_id INTEGER, cliente_nombre TEXT, fecha TEXT NOT NULL,
    subtotal REAL DEFAULT 0, descuento REAL DEFAULT 0, total REAL DEFAULT 0,
    estado TEXT DEFAULT 'activo', forma_pago TEXT DEFAULT 'efectivo',
    origen TEXT DEFAULT 'sistema', creado_en TEXT DEFAULT NOW()::TEXT
);
CREATE TABLE IF NOT EXISTS comprobante_items (
    id SERIAL PRIMARY KEY, comprobante_id INTEGER, producto_id INTEGER,
    producto_desc TEXT, cantidad REAL DEFAULT 1,
    precio_unitario REAL DEFAULT 0, precio_costo REAL DEFAULT 0, subtotal REAL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS ventas_historicas (
    id SERIAL PRIMARY KEY, fecha TEXT, codigo TEXT, producto TEXT,
    producto_desc TEXT, rubro TEXT, cantidad REAL DEFAULT 0,
    subtotal REAL DEFAULT 0, ganancia REAL DEFAULT 0,
    cliente TEXT, cliente_nombre TEXT, origen TEXT DEFAULT 'factupyme'
);
CREATE TABLE IF NOT EXISTS numeracion_afip (
    id SERIAL PRIMARY KEY, tipo TEXT UNIQUE NOT NULL,
    punto_venta TEXT DEFAULT '0001', ultimo_num INTEGER DEFAULT 0
);
INSERT INTO numeracion_afip (tipo,punto_venta,ultimo_num) VALUES ('factura','0001',0) ON CONFLICT (tipo) DO NOTHING;
INSERT INTO numeracion_afip (tipo,punto_venta,ultimo_num) VALUES ('presupuesto','0001',0) ON CONFLICT (tipo) DO NOTHING;
INSERT INTO numeracion_afip (tipo,punto_venta,ultimo_num) VALUES ('remito','0001',0) ON CONFLICT (tipo) DO NOTHING;
INSERT INTO numeracion_afip (tipo,punto_venta,ultimo_num) VALUES ('nota_credito','0001',0) ON CONFLICT (tipo) DO NOTHING;
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL, password_hash TEXT NOT NULL,
    rol TEXT DEFAULT 'facturacion', activo INTEGER DEFAULT 1,
    debe_cambiar_password INTEGER DEFAULT 0,
    creado_en TEXT DEFAULT NOW()::TEXT
);
CREATE TABLE IF NOT EXISTS sesiones (
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL, rol TEXT NOT NULL, nombre TEXT NOT NULL,
    ip TEXT DEFAULT '', user_agent TEXT DEFAULT '',
    creado_en TEXT NOT NULL, expira_en TEXT NOT NULL,
    ultima_actividad TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sesiones_user ON sesiones(user_id);
CREATE INDEX IF NOT EXISTS idx_sesiones_expira ON sesiones(expira_en);
CREATE TABLE IF NOT EXISTS auditoria (
    id SERIAL PRIMARY KEY, fecha TEXT DEFAULT NOW()::TEXT,
    user_id INTEGER, username TEXT, rol TEXT,
    accion TEXT NOT NULL, recurso TEXT, detalle TEXT,
    ip TEXT, exito INTEGER DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_auditoria_fecha ON auditoria(fecha);
CREATE INDEX IF NOT EXISTS idx_auditoria_user ON auditoria(user_id);
CREATE TABLE IF NOT EXISTS caja_sesiones (
    id SERIAL PRIMARY KEY, fecha TEXT NOT NULL, apertura TEXT,
    cierre TEXT, saldo_inicial REAL DEFAULT 0, saldo_final REAL,
    total_ingresos REAL DEFAULT 0, total_egresos REAL DEFAULT 0,
    estado TEXT DEFAULT 'abierta', creado_en TEXT DEFAULT NOW()::TEXT
);
CREATE TABLE IF NOT EXISTS caja_movimientos (
    id SERIAL PRIMARY KEY, sesion_id INTEGER, tipo TEXT NOT NULL,
    descripcion TEXT, monto REAL DEFAULT 0, comprobante_id INTEGER,
    creado_en TEXT DEFAULT NOW()::TEXT
);
CREATE TABLE IF NOT EXISTS cuenta_corriente (
    id SERIAL PRIMARY KEY, cliente_id INTEGER, cliente_nombre TEXT NOT NULL,
    comprobante_id INTEGER, tipo TEXT NOT NULL, concepto TEXT NOT NULL,
    monto REAL NOT NULL, saldo_post REAL NOT NULL, fecha TEXT,
    forma_cobro TEXT, creado_en TEXT DEFAULT NOW()::TEXT
);
CREATE TABLE IF NOT EXISTS compras (
    id SERIAL PRIMARY KEY, numero TEXT, proveedor TEXT NOT NULL,
    fecha TEXT, total REAL DEFAULT 0, estado TEXT DEFAULT 'pendiente',
    notas TEXT, creado_en TEXT DEFAULT NOW()::TEXT
);
CREATE TABLE IF NOT EXISTS compra_items (
    id SERIAL PRIMARY KEY, compra_id INTEGER, producto_id INTEGER,
    producto_desc TEXT, cantidad REAL, precio_costo REAL, subtotal REAL
);
CREATE TABLE IF NOT EXISTS pedidos_tienda (
    id SERIAL PRIMARY KEY, nombre_cliente TEXT NOT NULL, telefono TEXT,
    tipo_entrega TEXT DEFAULT 'retiro', direccion TEXT, notas TEXT,
    subtotal REAL DEFAULT 0, estado TEXT DEFAULT 'pendiente',
    creado_en TEXT DEFAULT NOW()::TEXT
);
CREATE TABLE IF NOT EXISTS pedidos_tienda_items (
    id SERIAL PRIMARY KEY, pedido_id INTEGER, descripcion TEXT,
    cantidad REAL DEFAULT 1, precio REAL DEFAULT 0, subtotal REAL DEFAULT 0
)
"""

if __name__ == "__main__":
    inicializar_db()
