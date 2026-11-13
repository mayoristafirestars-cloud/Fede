import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.environ.get("CORONEL_DB_PATH", os.path.join(BASE_DIR, "db", "coronel_sur.db"))
SCHEMA   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")


def conectar() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row          # devuelve dicts en vez de tuplas
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL") # mejor rendimiento concurrente
    return conn


def inicializar_db():
    """Crea las tablas si no existen."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(SCHEMA, "r", encoding="utf-8") as f:
        sql = f.read()
    conn = conectar()
    conn.executescript(sql)
    # Additive migration: preserve existing catalog, prices, stock and receipts.
    columns = {r[1] for r in conn.execute("PRAGMA table_info(productos)")}
    for name, definition in {
        "unidad_venta": "TEXT NOT NULL DEFAULT 'kg'",
        "variedad": "TEXT NOT NULL DEFAULT ''",
        "calidad": "TEXT NOT NULL DEFAULT ''",
        "presentacion": "TEXT NOT NULL DEFAULT ''",
        "foto": "TEXT NOT NULL DEFAULT ''",
        "venta_exacta": "TEXT",
        "reposicion_exacta": "TEXT",
        "promedio_exacto": "TEXT",
    }.items():
        if name not in columns:
            conn.execute(f"ALTER TABLE productos ADD COLUMN {name} {definition}")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS configuracion_negocio (
            id INTEGER PRIMARY KEY CHECK(id = 1),
            datos TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS identificadores_producto (
            clave TEXT PRIMARY KEY,
            producto_id INTEGER NOT NULL REFERENCES productos(id),
            tipo TEXT NOT NULL,
            valor TEXT NOT NULL
        );
    """)
    conn.commit()
    with open(os.path.join(os.path.dirname(SCHEMA), 'compras.sql'), encoding='utf-8') as f:
        conn.executescript(f.read())
    with open(os.path.join(os.path.dirname(SCHEMA), 'inventario.sql'), encoding='utf-8') as f:
        conn.executescript(f.read())
    import stock
    with conn:
        stock.initialize(conn)
    with open(os.path.join(os.path.dirname(SCHEMA), 'mostrador.sql'), encoding='utf-8') as f:
        conn.executescript(f.read())
    with open(os.path.join(os.path.dirname(SCHEMA), 'tienda.sql'), encoding='utf-8') as f:
        conn.executescript(f.read())
    web_columns = {r[1] for r in conn.execute('PRAGMA table_info(pedidos_web)')}
    for name, definition in {
        'presupuesto': 'TEXT', 'franja_id': 'INTEGER REFERENCES franjas_web(id)',
        'vence_reserva': 'REAL', 'costos_base': 'TEXT', 'cobro': 'TEXT', 'entregado_en': 'TEXT'
    }.items():
        if name not in web_columns:
            conn.execute(f'ALTER TABLE pedidos_web ADD COLUMN {name} {definition}')
    for table in ('comprobante_items','lineas_pos'):
        columns={r[1] for r in conn.execute(f'PRAGMA table_info({table})')}
        if 'foto' not in columns:
            conn.execute(f'ALTER TABLE {table} ADD COLUMN foto TEXT')
    conn.execute("""CREATE TABLE IF NOT EXISTS fotos_documento(
        id INTEGER PRIMARY KEY,origen TEXT NOT NULL,item_id INTEGER NOT NULL,
        foto TEXT NOT NULL,responsable TEXT NOT NULL,motivo TEXT NOT NULL,
        creado TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now'))
    )""")
    conn.commit()
    conn.close()
    print(f"✅ Base de datos lista en: {DB_PATH}")


if __name__ == "__main__":
    inicializar_db()
