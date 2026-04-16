"""
Hashing y verificación de passwords.

Estrategia de migración:
- Hashes nuevos → bcrypt (factor 12).
- Al login, si el hash guardado es MD5 legacy y matchea, se re-hashea
  con bcrypt y se actualiza en la DB. Transparente para el usuario.
"""
from __future__ import annotations

import hashlib
import re
import bcrypt

BCRYPT_ROUNDS = 12
_RE_BCRYPT = re.compile(r"^\$2[aby]\$\d{2}\$")


def es_hash_bcrypt(h: str) -> bool:
    """True si el hash está en formato bcrypt."""
    return bool(h and _RE_BCRYPT.match(h))


def hash_password(password: str) -> str:
    """Genera un hash bcrypt. Usar para passwords nuevas."""
    if not password:
        raise ValueError("Password vacía")
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(rounds=BCRYPT_ROUNDS),
    ).decode("utf-8")


def verify_password(password: str, stored_hash: str) -> bool:
    """
    Verifica una password contra el hash guardado.
    Soporta hashes bcrypt (actual) y MD5 (legacy, en migración).
    """
    if not stored_hash or not password:
        return False

    if es_hash_bcrypt(stored_hash):
        try:
            return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))
        except Exception:
            return False

    # Legacy: MD5 sin salt (formato viejo).
    md5_actual = hashlib.md5(password.encode("utf-8")).hexdigest()
    return md5_actual == stored_hash


def validar_fortaleza(password: str) -> tuple[bool, str]:
    """
    Política mínima de passwords.
    Devuelve (ok, motivo_si_falla).
    """
    if len(password) < 12:
        return False, "La contraseña debe tener al menos 12 caracteres"
    if password.lower() in {"password", "contraseña", "1234", "12345", "123456"}:
        return False, "Contraseña muy común, elegí una más robusta"
    clases = sum([
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(not c.isalnum() for c in password),
    ])
    if clases < 3:
        return False, "La contraseña debe combinar mayúsculas, minúsculas, números y símbolos (al menos 3 de los 4)"
    return True, ""
