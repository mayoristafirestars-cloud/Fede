"""
Respalda la base de datos.
Uso: python scripts/respaldar.py
La ruta de la base sale de DB_PATH y la carpeta de respaldos de BACKUP_DIR.
"""

import _ruta  # noqa: F401  (agrega backend/ al path y carga .env)
from db import respaldos


if __name__ == "__main__":
    destino = respaldos.respaldar(motivo="manual")
    print(f"💾 Respaldo creado: {destino}")
