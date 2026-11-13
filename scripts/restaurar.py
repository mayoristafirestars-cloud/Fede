"""
Restaura la base de datos desde un respaldo.
Uso: python scripts/restaurar.py RUTA_DEL_RESPALDO [--si]

IMPORTANTE: detené el servidor antes de restaurar.
Antes de reemplazar la base, se guarda un respaldo de la base actual.
"""

import json
import sys

import _ruta  # noqa: F401
from db import respaldos
from db.database import conectar, ruta_db


def _auditar(origen: str, previo: str):
    conn = conectar()
    try:
        existe = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='evento_auditoria'").fetchone()
        if existe:
            conn.execute(
                "INSERT INTO evento_auditoria (empresa_id, actor_texto, accion, entidad, despues) VALUES (NULL, 'consola', 'respaldo.restaurar', 'base', ?)",
                (json.dumps({"desde": origen, "respaldo_previo": previo}),),
            )
            conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--si"]
    if len(args) != 1:
        print(__doc__)
        sys.exit(1)
    origen = args[0]
    print(f"Base actual:  {ruta_db()}")
    print(f"Se restaura:  {origen}")
    if "--si" not in sys.argv and input("Escribí RESTAURAR para confirmar: ").strip() != "RESTAURAR":
        print("Cancelado.")
        sys.exit(1)
    previo = respaldos.restaurar(origen)
    _auditar(origen, previo)
    print(f"✅ Restaurado. Respaldo de la base anterior: {previo or '(no había base)'}")
