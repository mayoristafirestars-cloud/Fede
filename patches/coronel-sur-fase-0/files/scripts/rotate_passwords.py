"""
Crea o actualiza las passwords de los 3 usuarios iniciales con bcrypt.

ÚSALO UNA SOLA VEZ después de deployar Fase 0, para:
  1. Migrar los hashes MD5 de "1234" (comprometidos al estar commiteados
     antes del filter-repo) a bcrypt con passwords nuevas fuertes.
  2. Invalidar todas las sesiones activas.

Uso:
    python scripts/rotate_passwords.py

El script pide las passwords por stdin (no quedan en historial de shell).

Después de correrlo, cada usuario puede entrar con su nueva password.
El flag `debe_cambiar_password` queda en 1, así el frontend los fuerza
a elegir su propia password en el primer login.
"""
from __future__ import annotations

import getpass
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from db.database import conectar, inicializar_db  # noqa: E402
from security.passwords import hash_password, validar_fortaleza  # noqa: E402


USUARIOS_INICIALES = [
    ("fede",    "Fede",     "admin"),
    ("malcolm", "Malcolm",  "facturacion"),
    ("anamar",  "Ana Mar",  "crm"),
]


def _pedir_password(prompt: str) -> str:
    while True:
        p1 = getpass.getpass(f"{prompt}: ")
        ok, motivo = validar_fortaleza(p1)
        if not ok:
            print(f"  ✗ {motivo}")
            continue
        p2 = getpass.getpass(f"{prompt} (repetir): ")
        if p1 != p2:
            print("  ✗ No coinciden, reintentá")
            continue
        return p1


def main():
    print("=" * 60)
    print("Rotación de passwords — Coronel Sur")
    print("=" * 60)
    print("Política: mínimo 12 caracteres, 3 de 4 clases (may/min/num/sym).")
    print()

    inicializar_db()

    nuevos = []
    for username, nombre, rol in USUARIOS_INICIALES:
        pwd = _pedir_password(f"Nueva password para {username} ({nombre}, {rol})")
        nuevos.append((username, nombre, rol, hash_password(pwd)))

    print()
    print("Aplicando a la DB…")
    conn = conectar()
    try:
        for username, nombre, rol, hash_ in nuevos:
            existe = conn.execute(
                "SELECT id FROM usuarios WHERE username = ?", (username,)
            ).fetchone()
            if existe:
                conn.execute(
                    """UPDATE usuarios
                       SET password_hash = ?, nombre = ?, rol = ?,
                           activo = 1, debe_cambiar_password = 1
                       WHERE username = ?""",
                    (hash_, nombre, rol, username),
                )
                print(f"  ✓ {username} actualizado")
            else:
                conn.execute(
                    """INSERT INTO usuarios
                       (username, nombre, password_hash, rol, activo, debe_cambiar_password)
                       VALUES (?, ?, ?, ?, 1, 1)""",
                    (username, nombre, hash_, rol),
                )
                print(f"  ✓ {username} creado")

        # Invalidar TODAS las sesiones — se acaban de cambiar las pass.
        borradas = conn.execute("DELETE FROM sesiones").rowcount if hasattr(
            conn.execute("SELECT COUNT(*) FROM sesiones").fetchone(), "__getitem__"
        ) else 0
        conn.commit()
    finally:
        conn.close()

    print()
    print("✓ Listo. Los 3 usuarios ya pueden iniciar sesión con sus nuevas passwords.")
    print("  El sistema les va a pedir elegir la suya propia en el primer login")
    print("  (flag debe_cambiar_password = 1).")


if __name__ == "__main__":
    main()
