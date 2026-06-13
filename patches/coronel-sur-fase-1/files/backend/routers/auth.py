"""
Módulo Auth — Usuarios, roles y sesiones.

Roles: admin (Fede) | facturacion (Malcolm) | crm (Ana Mar)

Cambios respecto a la versión MD5 anterior:
- Passwords nuevas se guardan con bcrypt (factor 12).
- Passwords viejas MD5 siguen funcionando pero se re-hashean con bcrypt
  al primer login exitoso (migración transparente).
- Sesiones persistentes en la DB (tabla `sesiones`), no en memoria.
- Cambiar password ahora invalida TODAS las sesiones del usuario.
- Flag `debe_cambiar_password` fuerza al frontend a redirigir al cambio
  al próximo login (seteado a 1 para los 3 usuarios iniciales con "1234").
"""
from __future__ import annotations

import os
import sys
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import conectar
from rate_limit import limiter
from security import (
    crear_sesion,
    hash_password,
    invalidar_token,
    require_admin,
    usuario_actual,
    verify_password,
)
from security.passwords import es_hash_bcrypt, validar_fortaleza
from security.sessions import invalidar_usuario


router = APIRouter(prefix="/api/auth", tags=["auth"])


# ─── Modelos ───────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class NuevoUsuario(BaseModel):
    username: str
    nombre: str
    password: str
    rol: str = "facturacion"


class CambiarPassword(BaseModel):
    password_actual: str
    password_nueva: str


# ─── Helpers internos ──────────────────────────────────────

def _ip_del_request(request: Request) -> str:
    # Respeta X-Forwarded-For si viene (Render lo pone).
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else ""


def _migrar_hash_si_hace_falta(user_id: int, hash_guardado: str, password_plana: str) -> None:
    """Si el hash guardado es MD5 legacy, reemplazarlo por bcrypt."""
    if es_hash_bcrypt(hash_guardado):
        return
    nuevo = hash_password(password_plana)
    conn = conectar()
    try:
        conn.execute(
            "UPDATE usuarios SET password_hash = ? WHERE id = ?",
            (nuevo, user_id),
        )
        conn.commit()
    finally:
        conn.close()


# ─── Endpoints ─────────────────────────────────────────────

@router.post("/login")
@limiter.limit("10/minute")
def login(data: LoginRequest, request: Request):
    """Inicia sesión y devuelve un token. Rate limited: 10/min por IP."""
    conn = conectar()
    try:
        user = conn.execute(
            "SELECT * FROM usuarios WHERE username = ? AND activo = 1",
            (data.username.lower().strip(),),
        ).fetchone()

        if not user:
            # Respuesta genérica para no dar pistas al atacante.
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        u = dict(user)
        if not verify_password(data.password, u["password_hash"]):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        # Migrar hash legacy → bcrypt si corresponde
        _migrar_hash_si_hace_falta(u["id"], u["password_hash"], data.password)

        # Crear sesión persistente
        token = crear_sesion(
            user_id=u["id"],
            username=u["username"],
            rol=u["rol"],
            nombre=u["nombre"],
            ip=_ip_del_request(request),
            user_agent=request.headers.get("user-agent", "")[:200],
        )

        debe_cambiar = bool(u.get("debe_cambiar_password", 0))

        return {
            "ok": True,
            "token": token,
            "nombre": u["nombre"],
            "rol": u["rol"],
            "username": u["username"],
            "debe_cambiar_password": debe_cambiar,
        }
    finally:
        conn.close()


@router.post("/logout")
def logout(authorization: Optional[str] = Header(None)):
    """Cierra la sesión actual."""
    if authorization:
        token = authorization.replace("Bearer ", "").strip()
        invalidar_token(token)
    return {"ok": True}


@router.get("/me")
def me(u: dict = Depends(usuario_actual)):
    """Devuelve el usuario actual."""
    return {"ok": True, "usuario": {k: v for k, v in u.items() if k != "token"}}


@router.get("/usuarios")
def listar_usuarios(u: dict = Depends(require_admin)):
    """Lista usuarios (solo admin)."""
    conn = conectar()
    try:
        filas = conn.execute(
            "SELECT id, username, nombre, rol, activo, debe_cambiar_password, creado_en "
            "FROM usuarios ORDER BY id"
        ).fetchall()
        return [dict(f) for f in filas]
    finally:
        conn.close()


@router.post("/usuarios")
def crear_usuario(data: NuevoUsuario, u: dict = Depends(require_admin)):
    """Crea un usuario nuevo (solo admin)."""
    roles_validos = {"admin", "facturacion", "crm", "bot"}
    if data.rol not in roles_validos:
        raise HTTPException(
            status_code=400,
            detail=f"Rol inválido. Opciones: {sorted(roles_validos)}",
        )

    ok, motivo = validar_fortaleza(data.password)
    if not ok:
        raise HTTPException(status_code=400, detail=motivo)

    conn = conectar()
    try:
        existe = conn.execute(
            "SELECT id FROM usuarios WHERE username = ?",
            (data.username.lower(),),
        ).fetchone()
        if existe:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe el usuario '{data.username}'",
            )

        conn.execute(
            """INSERT INTO usuarios
               (username, nombre, password_hash, rol, debe_cambiar_password)
               VALUES (?, ?, ?, ?, 0)""",
            (
                data.username.lower(),
                data.nombre,
                hash_password(data.password),
                data.rol,
            ),
        )
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()


@router.put("/usuarios/{user_id}/password")
def cambiar_password(
    user_id: int,
    data: CambiarPassword,
    u: dict = Depends(usuario_actual),
):
    """
    Cambia la contraseña de un usuario.
    - Admin puede cambiar la de cualquiera (y no se le pide password actual).
    - Cualquier usuario puede cambiar la suya, confirmando la actual.
    """
    if u["rol"] != "admin" and u["id"] != user_id:
        raise HTTPException(status_code=403, detail="Sin permiso")

    ok, motivo = validar_fortaleza(data.password_nueva)
    if not ok:
        raise HTTPException(status_code=400, detail=motivo)

    conn = conectar()
    try:
        user = conn.execute(
            "SELECT * FROM usuarios WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Usuario no-admin cambiando la suya debe confirmar la password actual
        if u["rol"] != "admin":
            if not verify_password(data.password_actual, dict(user)["password_hash"]):
                raise HTTPException(
                    status_code=401,
                    detail="Contraseña actual incorrecta",
                )

        conn.execute(
            """UPDATE usuarios
               SET password_hash = ?, debe_cambiar_password = 0
               WHERE id = ?""",
            (hash_password(data.password_nueva), user_id),
        )
        conn.commit()

        # Invalidar todas las sesiones del usuario — fuerza re-login en
        # otros dispositivos para evitar persistencia tras cambio de pass.
        invalidar_usuario(user_id)

        return {"ok": True}
    finally:
        conn.close()


@router.put("/usuarios/{user_id}/toggle")
def toggle_usuario(user_id: int, u: dict = Depends(require_admin)):
    """Activa/desactiva un usuario (solo admin)."""
    if u["id"] == user_id:
        raise HTTPException(status_code=400, detail="No podés desactivarte a vos mismo")

    conn = conectar()
    try:
        conn.execute(
            "UPDATE usuarios SET activo = CASE WHEN activo=1 THEN 0 ELSE 1 END "
            "WHERE id = ?",
            (user_id,),
        )
        conn.commit()
        # Si se desactivó, invalidar sus sesiones
        invalidar_usuario(user_id)
        return {"ok": True}
    finally:
        conn.close()
