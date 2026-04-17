import os
import sqlite3

BACKEND = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT    = os.path.dirname(BACKEND)
DATA    = os.path.join(ROOT, "data")
DB_PATH = os.path.join(DATA, "medico.db")
SCHEMA  = os.path.join(BACKEND, "db", "schema.sql")


def conectar():
    os.makedirs(DATA, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def inicializar_db():
    os.makedirs(DATA, exist_ok=True)
    with open(SCHEMA, "r", encoding="utf-8") as f:
        sql = f.read()
    conn = conectar()
    try:
        conn.executescript(sql)
        conn.commit()
    finally:
        conn.close()
