"""
Registro de auditoría (sólo agregar).
Se escribe en la misma conexión y transacción que la acción auditada:
si la acción se deshace, el evento también. Nunca pasar contraseñas ni tokens.
"""

import json


def registrar(conn, accion: str, entidad: str = None, entidad_id=None, antes: dict = None,
              despues: dict = None, usuario=None, actor_texto: str = None, ip: str = None,
              empresa_id: int = None):
    if usuario is not None:
        empresa_id = usuario.empresa_id
        actor_texto = usuario.usuario
    conn.execute(
        """INSERT INTO evento_auditoria
               (empresa_id, actor_usuario_id, actor_texto, accion, entidad, entidad_id, antes, despues, ip)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (empresa_id, getattr(usuario, "id", None), actor_texto, accion, entidad,
         None if entidad_id is None else str(entidad_id),
         None if antes is None else json.dumps(antes, ensure_ascii=False),
         None if despues is None else json.dumps(despues, ensure_ascii=False), ip),
    )
