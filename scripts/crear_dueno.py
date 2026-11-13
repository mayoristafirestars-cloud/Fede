"""Run on the host before exposing the service. No password in arguments/logs."""
import getpass
import secrets
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from db.database import inicializar_db
from routers.preparacion import database
from routers.comercial import Credentials, password_hash

if __name__ == '__main__':
    inicializar_db()
    with database() as conn:
        if conn.execute('SELECT COUNT(*) FROM responsables').fetchone()[0]:
            raise SystemExit('Ya existe un responsable. Usá la sesión del dueño para agregar usuarios.')
    nombre = input('Nombre del dueño: ').strip()
    clave = getpass.getpass('Clave (8–128 caracteres): ')
    if clave != getpass.getpass('Repetir clave: '):
        raise SystemExit('Las claves no coinciden')
    data = Credentials(nombre=nombre, clave=clave)
    with database() as conn:
        conn.execute('BEGIN IMMEDIATE')
        if conn.execute('SELECT COUNT(*) FROM responsables').fetchone()[0]:
            raise SystemExit('Ya existe un responsable')
        salt = secrets.token_hex(16)
        conn.execute('INSERT INTO responsables(nombre,rol,sal,clave_hash) VALUES(?,?,?,?)',
                     (data.nombre, 'dueno', salt, password_hash(clave, salt)))
    print('Dueño creado. Ya podés ingresar con tu nombre y clave.')
