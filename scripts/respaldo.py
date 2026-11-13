"""Consistent SQLite snapshot and immutable product photos in one private archive."""
import argparse
import os
from pathlib import Path
import sqlite3
import tarfile
import tempfile
from datetime import datetime, timezone


def backup(db, media, output):
    db, media, output = Path(db).resolve(), Path(media).resolve(), Path(output).resolve()
    if not db.is_file() or not media.is_dir():
        raise ValueError('Falta la base de datos o la carpeta de fotos')
    if output == db or media == output or media in output.parents:
        raise ValueError('Guardá el respaldo fuera de la carpeta de fotos y de la base')
    # Exclusive output prevents accidental replacement. Private permissions include credentials.
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, 'wb') as destination, tempfile.TemporaryDirectory() as temporary:
            snapshot = Path(temporary) / 'nativa.db'
            with sqlite3.connect(f'{db.as_uri()}?mode=ro', uri=True) as source, sqlite3.connect(snapshot) as target:
                source.backup(target)
                if target.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                    raise ValueError('El respaldo no supera la verificación de integridad')
            with tarfile.open(fileobj=destination, mode='w:gz') as archive:
                archive.add(snapshot, arcname='nativa.db')
                archive.add(media, arcname='uploads')
    except BaseException:
        output.unlink(missing_ok=True)
        raise
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destino', help='Archivo .tar.gz nuevo; guardar una copia fuera del servidor')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    print(backup(os.environ.get('CORONEL_DB_PATH', root / 'backend/db/coronel_sur.db'),
                 os.environ.get('CORONEL_MEDIA_DIR', root / 'backend/uploads'), args.destino))
