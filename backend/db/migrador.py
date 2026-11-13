"""
Migraciones versionadas.
Cada archivo backend/db/migraciones/NNNN_nombre.sql se aplica una sola vez,
en orden y dentro de una transacción. Antes de aplicar, se respalda la base.
"""

import hashlib
import json
import os
import re
import sqlite3
from datetime import datetime

from db.database import ruta_db
from db import respaldos

DIR_MIGRACIONES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "migraciones")
PATRON = re.compile(r"^(\d{4})_([\w-]+)\.sql$")


def listar_migraciones(directorio: str = None) -> list[tuple[int, str, str]]:
    """Devuelve [(version, nombre, ruta)] ordenado por versión."""
    directorio = directorio or DIR_MIGRACIONES
    salida = []
    for archivo in sorted(os.listdir(directorio)):
        m = PATRON.match(archivo)
        if m:
            salida.append((int(m.group(1)), m.group(2), os.path.join(directorio, archivo)))
    versiones = [v for v, _, _ in salida]
    if len(versiones) != len(set(versiones)):
        raise RuntimeError("Hay dos migraciones con el mismo número")
    return salida


def _sentencias(sql: str) -> list[str]:
    """Parte un script SQL en sentencias completas (respeta triggers BEGIN...END)."""
    sentencias, actual = [], ""
    for linea in sql.splitlines(keepends=True):
        if not actual and (not linea.strip() or linea.strip().startswith("--")):
            continue
        actual += linea
        if sqlite3.complete_statement(actual):
            sentencias.append(actual.strip())
            actual = ""
    if actual.strip():
        raise ValueError("La migración termina con una sentencia incompleta")
    return sentencias


def _checksum(ruta: str) -> str:
    with open(ruta, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _crear_tabla_control(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_migraciones (
            version     INTEGER PRIMARY KEY,
            nombre      TEXT NOT NULL,
            checksum    TEXT NOT NULL,
            aplicada_en TEXT NOT NULL
        )
    """)


def _tiene_tablas(conn) -> bool:
    fila = conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name != 'schema_migraciones'"
    ).fetchone()
    return fila[0] > 0


def aplicar_migraciones(ruta: str = None, directorio: str = None, respaldar: bool = True) -> list[int]:
    """Aplica las migraciones pendientes. Devuelve las versiones aplicadas."""
    ruta = ruta or ruta_db()
    os.makedirs(os.path.dirname(os.path.abspath(ruta)), exist_ok=True)
    conn = sqlite3.connect(ruta, isolation_level=None)   # transacciones manuales
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        _crear_tabla_control(conn)
        aplicadas = {v: c for v, c in conn.execute("SELECT version, checksum FROM schema_migraciones")}
        todas = listar_migraciones(directorio)

        for version, nombre, archivo in todas:
            if version in aplicadas and aplicadas[version] != _checksum(archivo):
                print(f"⚠️  La migración {version:04d}_{nombre} cambió después de aplicarse. No se vuelve a aplicar.")

        pendientes = [m for m in todas if m[0] not in aplicadas]
        if not pendientes:
            return []

        if respaldar and _tiene_tablas(conn):
            destino = respaldos.respaldar(ruta, motivo=f"pre_migracion_{pendientes[0][0]:04d}")
            print(f"💾 Respaldo previo a migrar: {destino}")

        hechas = []
        for version, nombre, archivo in pendientes:
            with open(archivo, "r", encoding="utf-8") as f:
                sql = f.read()
            conn.execute("BEGIN")
            try:
                for sentencia in _sentencias(sql):
                    conn.execute(sentencia)
                conn.execute(
                    "INSERT INTO schema_migraciones (version, nombre, checksum, aplicada_en) VALUES (?,?,?,?)",
                    (version, nombre, _checksum(archivo), datetime.now().isoformat(timespec="seconds")),
                )
                conn.execute("COMMIT")
            except Exception:
                conn.execute("ROLLBACK")
                raise
            hechas.append(version)
            print(f"✅ Migración aplicada: {version:04d}_{nombre}")

        _auditar(conn, [(v, n) for v, n, _ in pendientes if v in hechas])
        return hechas
    finally:
        conn.close()


def _auditar(conn, hechas):
    """Registra las migraciones en la auditoría, si la tabla ya existe."""
    existe = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='evento_auditoria'"
    ).fetchone()
    if not existe or not hechas:
        return
    conn.execute("BEGIN")
    for version, nombre in hechas:
        conn.execute(
            "INSERT INTO evento_auditoria (empresa_id, actor_texto, accion, entidad, entidad_id, despues) VALUES (NULL, 'sistema', 'migracion.aplicar', 'schema_migraciones', ?, ?)",
            (str(version), json.dumps({"nombre": nombre})),
        )
    conn.execute("COMMIT")
