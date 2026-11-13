"""
Login, logout y datos del usuario actual.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
import seguridad
from db.database import conectar
from db.auditoria import registrar

router = APIRouter(prefix="/api/auth", tags=["auth"])


class Credenciales(BaseModel):
    usuario:    str
    contrasena: str


def _poner_cookies(response: Response, token: str, csrf: str):
    edad = config.sesion_horas() * 3600
    seguro = config.es_produccion()
    response.set_cookie(seguridad.COOKIE_SESION, token, max_age=edad, httponly=True,
                        secure=seguro, samesite="lax", path="/")
    # La cookie CSRF la lee el frontend para mandarla en el encabezado X-CSRF-Token.
    response.set_cookie(seguridad.COOKIE_CSRF, csrf, max_age=edad, httponly=False,
                        secure=seguro, samesite="strict", path="/")


def _borrar_cookies(response: Response):
    response.delete_cookie(seguridad.COOKIE_SESION, path="/")
    response.delete_cookie(seguridad.COOKIE_CSRF, path="/")


@router.post("/login")
def login(data: Credenciales, request: Request, response: Response):
    """Inicia sesión. Responde siempre el mismo error para no revelar si el usuario existe."""
    conn = conectar()
    try:
        ip = seguridad.ip_de(request)
        fila, motivo = seguridad.autenticar(conn, data.usuario, data.contrasena)
        if not fila:
            # Si el usuario no existe no se guarda lo tecleado: podría ser una contraseña.
            existente = conn.execute("SELECT id, empresa_id, usuario FROM usuario WHERE usuario = ?",
                                     (data.usuario.strip().lower(),)).fetchone()
            registrar(conn, "login.fallido", entidad="usuario",
                      entidad_id=existente["id"] if existente else None,
                      despues={"motivo": motivo},
                      actor_texto=existente["usuario"] if existente else "(usuario inexistente)",
                      empresa_id=existente["empresa_id"] if existente else None, ip=ip)
            conn.commit()     # guarda el contador de intentos / bloqueo y el evento
            raise HTTPException(status_code=401, detail=seguridad.MENSAJE_LOGIN)
        token, csrf = seguridad.crear_sesion(conn, fila["id"], fila["empresa_id"], ip)
        registrar(conn, "login", entidad="usuario", entidad_id=fila["id"],
                  actor_texto=fila["usuario"], empresa_id=fila["empresa_id"], ip=ip)
        conn.commit()
    finally:
        conn.close()
    _poner_cookies(response, token, csrf)
    return {"ok": True, "usuario": fila["usuario"], "nombre": fila["nombre"]}


@router.post("/logout")
def logout(request: Request, response: Response):
    token = request.cookies.get(seguridad.COOKIE_SESION)
    conn = conectar()
    try:
        if token:
            seguridad.revocar_sesion(conn, token)
        usuario = getattr(request.state, "usuario", None)
        if usuario:
            registrar(conn, "logout", entidad="usuario", entidad_id=usuario.id,
                      usuario=usuario, ip=seguridad.ip_de(request))
        conn.commit()
    finally:
        conn.close()
    _borrar_cookies(response)
    return {"ok": True}


@router.get("/yo")
def yo(usuario: seguridad.Usuario = Depends(seguridad.requiere("producto.ver"))):
    return {"usuario": usuario.usuario, "nombre": usuario.nombre, "roles": sorted(usuario.roles)}
