"""
Crea el primer usuario administrador (o cualquier usuario).
Uso: python scripts/crear_admin.py
La contraseña se pide por consola y no se muestra. No hay usuarios por defecto.
"""

import getpass
import json
import sys

import _ruta  # noqa: F401  (agrega backend/ al path y carga .env)
import seguridad
from db.database import conectar, inicializar_db


def crear(usuario: str, nombre: str, contrasena: str, roles: set) -> int:
    conn = conectar()
    try:
        uid = seguridad.crear_usuario(conn, usuario, nombre, contrasena, roles)
        conn.commit()
        return uid
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    inicializar_db()
    print("\nCrear usuario de Coronel Sur")
    usuario = input("Usuario (ej: fede): ").strip()
    nombre = input("Nombre para mostrar: ").strip()
    roles_txt = input(f"Roles separados por coma [{', '.join(sorted(seguridad.ROLES))}] (Enter = admin): ").strip()
    roles = {r.strip() for r in roles_txt.split(",") if r.strip()} or {"admin"}
    c1 = getpass.getpass(f"Contraseña (mínimo {seguridad.LARGO_MINIMO} caracteres): ")
    c2 = getpass.getpass("Repetir contraseña: ")
    if c1 != c2:
        print("❌ Las contraseñas no coinciden.")
        sys.exit(1)
    try:
        uid = crear(usuario, nombre, c1, roles)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    print(f"✅ Usuario creado (id {uid}) con roles: {json.dumps(sorted(roles))}")
