"""
Respaldo y restauración de la base SQLite.
Usa la API backup de sqlite3: copia consistente aunque haya conexiones abiertas.
"""

import os
import sqlite3
from datetime import datetime

from db.database import BASE_DIR, ruta_db


def dir_respaldos() -> str:
    """Carpeta de respaldos: variable BACKUP_DIR o backend/db/respaldos."""
    return os.environ.get("BACKUP_DIR", os.path.join(BASE_DIR, "db", "respaldos"))


def _copiar(origen: str, destino: str):
    src = sqlite3.connect(origen)
    dst = sqlite3.connect(destino)
    try:
        src.backup(dst)
    finally:
        dst.close()
        src.close()


def verificar_integridad(ruta: str) -> bool:
    """True si el archivo es una base SQLite sana."""
    if not os.path.isfile(ruta):
        return False
    try:
        conn = sqlite3.connect(f"file:{ruta}?mode=ro", uri=True)
        try:
            return conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        finally:
            conn.close()
    except sqlite3.DatabaseError:
        return False


def respaldar(ruta: str = None, motivo: str = "manual") -> str:
    """Copia la base a un archivo fechado y devuelve su ruta."""
    ruta = ruta or ruta_db()
    if not os.path.isfile(ruta):
        raise FileNotFoundError(f"No existe la base: {ruta}")
    os.makedirs(dir_respaldos(), exist_ok=True)
    sello = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    nombre = f"{os.path.splitext(os.path.basename(ruta))[0]}_{sello}_{motivo}.db"
    destino = os.path.join(dir_respaldos(), nombre)
    _copiar(ruta, destino)
    return destino


def restaurar(ruta_respaldo: str, ruta: str = None) -> str:
    """
    Reemplaza la base por el respaldo indicado.
    Antes respalda la base actual (si existe) y devuelve la ruta de ese respaldo previo.
    """
    ruta = ruta or ruta_db()
    if not verificar_integridad(ruta_respaldo):
        raise ValueError(f"El respaldo no es una base válida: {ruta_respaldo}")
    previo = respaldar(ruta, motivo="pre_restauracion") if os.path.isfile(ruta) else ""
    os.makedirs(os.path.dirname(os.path.abspath(ruta)), exist_ok=True)
    _copiar(ruta_respaldo, ruta)
    return previo
