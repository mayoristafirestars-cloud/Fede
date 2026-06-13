"""
Sistema de migraciones ligero para SQLite.

Cada migración es una función con un nombre único y un SQL.
Se ejecutan en orden y se registran en la tabla `schema_migrations`.
Si una migración ya corrió, se saltea. Idempotente.

Para agregar una migración:
  1. Agregá un tuple (nombre_unico, sql) a la lista MIGRATIONS.
  2. Deployá. Al siguiente startup, se ejecuta automáticamente.
  3. No borres migraciones viejas (sirven de historial).

Mucho más simple que Alembic para un proyecto single-dev con SQLite.
Cuando migren a Postgres, podemos pasar a Alembic si hace falta.
"""
from __future__ import annotations

import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db.database import conectar, USE_PG

log = logging.getLogger("migrations")


# (nombre_unico, sql_a_ejecutar)
# El nombre debe ser descriptivo y NUNCA cambiar después de deployado.
MIGRATIONS: list[tuple[str, str]] = [
    (
        "001_crear_tabla_schema_migrations",
        """CREATE TABLE IF NOT EXISTS schema_migrations (
            name TEXT PRIMARY KEY,
            applied_at TEXT DEFAULT (datetime('now','localtime'))
        )""",
    ),
    (
        "002_agregar_debe_cambiar_password",
        """ALTER TABLE usuarios ADD COLUMN debe_cambiar_password INTEGER DEFAULT 0""",
    ),
    (
        "003_crear_tabla_sesiones",
        """CREATE TABLE IF NOT EXISTS sesiones (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL, rol TEXT NOT NULL, nombre TEXT NOT NULL,
            ip TEXT DEFAULT '', user_agent TEXT DEFAULT '',
            creado_en TEXT NOT NULL, expira_en TEXT NOT NULL,
            ultima_actividad TEXT NOT NULL
        )""",
    ),
    (
        "004_crear_tabla_auditoria",
        """CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT DEFAULT (datetime('now','localtime')),
            user_id INTEGER, username TEXT, rol TEXT,
            accion TEXT NOT NULL, recurso TEXT, detalle TEXT,
            ip TEXT, exito INTEGER DEFAULT 1
        )""",
    ),
    (
        "005_indices_sesiones_auditoria",
        """CREATE INDEX IF NOT EXISTS idx_sesiones_user ON sesiones(user_id);
           CREATE INDEX IF NOT EXISTS idx_sesiones_expira ON sesiones(expira_en);
           CREATE INDEX IF NOT EXISTS idx_auditoria_fecha ON auditoria(fecha);
           CREATE INDEX IF NOT EXISTS idx_auditoria_user ON auditoria(user_id)""",
    ),
    (
        "006_crear_tablas_bot",
        """CREATE TABLE IF NOT EXISTS bot_sesiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            canal TEXT NOT NULL, sesion_id TEXT NOT NULL,
            telefono TEXT DEFAULT '', nombre_cliente TEXT DEFAULT '',
            cliente_id INTEGER,
            iniciada_en TEXT NOT NULL, ultima_actividad TEXT NOT NULL,
            UNIQUE(canal, sesion_id)
        );
        CREATE TABLE IF NOT EXISTS bot_conversaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sesion_id INTEGER NOT NULL,
            fecha TEXT NOT NULL, rol TEXT NOT NULL,
            contenido TEXT NOT NULL, metadata TEXT
        );
        CREATE TABLE IF NOT EXISTS bot_mensajes_procesados (
            message_id TEXT PRIMARY KEY,
            procesado_en TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_bot_sesiones_canal ON bot_sesiones(canal, sesion_id);
        CREATE INDEX IF NOT EXISTS idx_bot_sesiones_cliente ON bot_sesiones(cliente_id);
        CREATE INDEX IF NOT EXISTS idx_bot_conv_sesion ON bot_conversaciones(sesion_id, fecha)""",
    ),
]


def _ya_aplicada(conn, nombre: str) -> bool:
    try:
        row = conn.execute(
            "SELECT 1 FROM schema_migrations WHERE name = ?", (nombre,)
        ).fetchone()
        return row is not None
    except Exception:
        return False


def _registrar(conn, nombre: str):
    try:
        conn.execute(
            "INSERT OR IGNORE INTO schema_migrations (name) VALUES (?)",
            (nombre,),
        )
    except Exception:
        pass


def ejecutar_migraciones() -> int:
    """
    Ejecuta todas las migraciones pendientes en orden.
    Devuelve la cantidad de migraciones aplicadas.
    """
    if USE_PG:
        log.info("Migraciones: modo PostgreSQL, salteo (usar schema_pg.sql)")
        return 0

    conn = conectar()
    aplicadas = 0
    try:
        for nombre, sql in MIGRATIONS:
            if nombre == "001_crear_tabla_schema_migrations":
                # La primera siempre corre (crea la tabla de control)
                try:
                    conn.execute(sql)
                    conn.commit()
                    _registrar(conn, nombre)
                    conn.commit()
                except Exception:
                    pass
                continue

            if _ya_aplicada(conn, nombre):
                continue

            log.info("Aplicando migración: %s", nombre)
            try:
                for stmt in sql.split(";"):
                    s = stmt.strip()
                    if s:
                        conn.execute(s)
                conn.commit()
                _registrar(conn, nombre)
                conn.commit()
                aplicadas += 1
                log.info("  OK  %s", nombre)
            except Exception as e:
                # ALTER TABLE falla si la columna ya existe — no es grave.
                log.warning("  SKIP %s: %s", nombre, e)
                try:
                    conn.rollback()
                except Exception:
                    pass
                _registrar(conn, nombre)
                try:
                    conn.commit()
                except Exception:
                    pass
    finally:
        conn.close()

    if aplicadas:
        log.info("Migraciones: %d aplicadas", aplicadas)
    else:
        log.info("Migraciones: todo al día")
    return aplicadas
