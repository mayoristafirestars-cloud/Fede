"""
Dependencias FastAPI para autenticación y autorización.

Uso en routers:

    from security import require_admin, usuario_actual

    @router.post("/algo", dependencies=[Depends(require_admin)])
    def algo():
        ...

    @router.get("/perfil")
    def perfil(u: dict = Depends(usuario_actual)):
        return u
"""
from __future__ import annotations

from typing import Optional

from fastapi import Depends, Header, HTTPException, Request

from .sessions import validar_token


def _extraer_token(authorization: Optional[str]) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Token requerido")
    # Tolerante: acepta "Bearer xxx" o "xxx"
    if authorization.lower().startswith("bearer "):
        return authorization[7:].strip()
    return authorization.strip()


def usuario_actual(authorization: Optional[str] = Header(None)) -> dict:
    """Devuelve los datos del usuario autenticado o 401."""
    token = _extraer_token(authorization)
    return validar_token(token)


def require_auth(authorization: Optional[str] = Header(None)) -> dict:
    """Alias explícito: sólo requiere que haya sesión válida."""
    return usuario_actual(authorization)


def require_admin(authorization: Optional[str] = Header(None)) -> dict:
    """Requiere rol admin."""
    u = usuario_actual(authorization)
    if u["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Requiere rol administrador")
    return u


def require_role(*roles: str):
    """Factory: devuelve una dependencia que exige uno de los roles."""
    roles_set = set(roles)

    def _dep(authorization: Optional[str] = Header(None)) -> dict:
        u = usuario_actual(authorization)
        if u["rol"] not in roles_set:
            raise HTTPException(
                status_code=403,
                detail=f"Requiere uno de los roles: {sorted(roles_set)}",
            )
        return u

    return _dep
