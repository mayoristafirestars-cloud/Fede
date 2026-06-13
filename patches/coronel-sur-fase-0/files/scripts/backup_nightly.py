"""
Backup nocturno de la DB a Google Drive, encriptado con Fernet.

Uso (manual):
    python scripts/backup_nightly.py

Uso automático (Render Cron Job):
    1. Crear un Cron Job en Render (gratis).
    2. Command: cd /opt/render/project/src && python scripts/backup_nightly.py
    3. Schedule: 0 3 * * *   (todos los días 3 AM UTC = 00:00 AR)
    4. Environment variables (mismo proyecto):
       - BACKUP_ENCRYPTION_KEY (clave Fernet, 44 chars base64)
       - BACKUP_DRIVE_FOLDER_ID (id de la carpeta de Drive)
       - GOOGLE_SERVICE_ACCOUNT_FILE=/etc/secrets/google-service-account.json
       - DB_PATH=/data/coronel_sur.db

Política de retención:
    Mantiene los últimos 30 backups en Drive. Los más viejos los borra
    (siempre que sean archivos creados por esta misma service account).

Seguridad:
    - El archivo sube YA encriptado. Sólo con BACKUP_ENCRYPTION_KEY se
      puede descifrar. Ni Google ni nadie con acceso a Drive lo ve.
    - Si perdés la key, los backups son chatarra. Guardala en un password
      manager (1Password, Bitwarden) aparte de Render.
"""
from __future__ import annotations

import datetime as dt
import os
import sys
from pathlib import Path

from cryptography.fernet import Fernet


# ─── Configuración desde env ────────────────────────────────

DB_PATH = os.environ.get("DB_PATH", "/data/coronel_sur.db")
ENCRYPTION_KEY = os.environ.get("BACKUP_ENCRYPTION_KEY", "").strip()
DRIVE_FOLDER_ID = os.environ.get("BACKUP_DRIVE_FOLDER_ID", "").strip()
SERVICE_ACCOUNT_FILE = os.environ.get(
    "GOOGLE_SERVICE_ACCOUNT_FILE", "/etc/secrets/google-service-account.json"
)
RETENCION_DIAS = int(os.environ.get("BACKUP_RETENCION_DIAS", "30"))


def _die(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def _checkear_config():
    if not ENCRYPTION_KEY:
        _die("Falta BACKUP_ENCRYPTION_KEY (generá una con Fernet.generate_key())")
    if not DRIVE_FOLDER_ID:
        _die("Falta BACKUP_DRIVE_FOLDER_ID")
    if not Path(SERVICE_ACCOUNT_FILE).exists():
        _die(f"No encuentro el JSON de la service account en {SERVICE_ACCOUNT_FILE}")
    if not Path(DB_PATH).exists():
        _die(f"No encuentro la DB en {DB_PATH}")


def _hacer_dump_sqlite() -> Path:
    """Crea un .sql consistente usando sqlite3 .backup (snapshot atómico)."""
    import sqlite3

    tmp_db = Path(f"/tmp/coronel_sur_backup_{dt.datetime.utcnow():%Y%m%d_%H%M%S}.db")
    src = sqlite3.connect(DB_PATH)
    dst = sqlite3.connect(tmp_db)
    with dst:
        src.backup(dst)
    src.close()
    dst.close()
    return tmp_db


def _encriptar(origen: Path) -> Path:
    f = Fernet(ENCRYPTION_KEY.encode())
    datos = origen.read_bytes()
    cifrado = f.encrypt(datos)
    destino = origen.with_suffix(origen.suffix + ".enc")
    destino.write_bytes(cifrado)
    return destino


def _drive_service():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/drive.file"],
    )
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def _subir_a_drive(path_encriptado: Path) -> str:
    from googleapiclient.http import MediaFileUpload

    service = _drive_service()
    file_metadata = {
        "name": path_encriptado.name,
        "parents": [DRIVE_FOLDER_ID],
        "description": "Backup encriptado del CRM Coronel Sur",
    }
    media = MediaFileUpload(str(path_encriptado), mimetype="application/octet-stream")
    resultado = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id,name,createdTime,size")
        .execute()
    )
    return resultado["id"]


def _podar_backups_viejos():
    """
    Borra backups más viejos que RETENCION_DIAS (solo los creados por
    esta misma service account y dentro de la carpeta destino).
    """
    service = _drive_service()
    corte = (dt.datetime.utcnow() - dt.timedelta(days=RETENCION_DIAS)).isoformat() + "Z"
    query = (
        f"'{DRIVE_FOLDER_ID}' in parents and trashed = false "
        f"and createdTime < '{corte}' "
        f"and name contains 'coronel_sur_backup'"
    )
    resp = service.files().list(q=query, fields="files(id,name,createdTime)").execute()
    borrados = 0
    for f in resp.get("files", []):
        try:
            service.files().delete(fileId=f["id"]).execute()
            borrados += 1
        except Exception as e:
            print(f"Aviso: no pude borrar {f['name']}: {e}")
    if borrados:
        print(f"Limpieza: {borrados} backups viejos borrados.")


def main():
    _checkear_config()

    ahora = dt.datetime.utcnow()
    print(f"[{ahora:%Y-%m-%d %H:%M:%S UTC}] Iniciando backup de {DB_PATH}")

    dump = _hacer_dump_sqlite()
    print(f"  Dump creado: {dump} ({dump.stat().st_size} bytes)")

    cifrado = _encriptar(dump)
    print(f"  Encriptado:  {cifrado} ({cifrado.stat().st_size} bytes)")

    file_id = _subir_a_drive(cifrado)
    print(f"  Subido a Drive: {file_id}")

    # Limpieza
    try:
        dump.unlink()
        cifrado.unlink()
    except Exception:
        pass

    try:
        _podar_backups_viejos()
    except Exception as e:
        print(f"Aviso: limpieza de viejos falló: {e}")

    print("✓ Backup completado")


if __name__ == "__main__":
    main()
