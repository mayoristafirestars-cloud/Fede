"""Módulo de seguridad: passwords, sesiones, middleware de auth, headers."""

from .passwords import hash_password, verify_password, es_hash_bcrypt
from .sessions import (
    crear_sesion,
    validar_token,
    invalidar_token,
    limpiar_sesiones_expiradas,
)
from .dependencies import (
    require_auth,
    require_admin,
    require_role,
    usuario_actual,
)

__all__ = [
    "hash_password",
    "verify_password",
    "es_hash_bcrypt",
    "crear_sesion",
    "validar_token",
    "invalidar_token",
    "limpiar_sesiones_expiradas",
    "require_auth",
    "require_admin",
    "require_role",
    "usuario_actual",
]
