import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "db", "coronel_sur.db")   # ruta por defecto


def ruta_db() -> str:
    """Ruta de la base: variable de entorno DB_PATH o la ruta por defecto."""
    return os.environ.get("DB_PATH", DB_PATH)


def conectar() -> sqlite3.Connection:
    conn = sqlite3.connect(ruta_db())
    conn.row_factory = sqlite3.Row          # devuelve dicts en vez de tuplas
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL") # mejor rendimiento concurrente
    return conn


def inicializar_db():
    """Aplica las migraciones pendientes (crea las tablas si la base es nueva)."""
    from db.migrador import aplicar_migraciones
    aplicar_migraciones()
    print(f"✅ Base de datos lista en: {ruta_db()}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, BASE_DIR)   # permite ejecutar este archivo directamente
    inicializar_db()
