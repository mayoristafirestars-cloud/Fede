"""
Sesiones persistentes en la DB.

Reemplaza el diccionario en memoria SESIONES_ACTIVAS del módulo auth viejo.
Sobrevive reinicios del servidor, permite revocación real en logout, y
escala a múltiples instancias.
"""
from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar


# Vida útil de la sesión. Cada uso renueva la expiración.
DURACION_HORAS = 8
INACTIVIDAD_MAX_MINUTOS = 60


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _iso_en(minutos: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(minutes=minutos)).isoformat()


def crear_sesion(user_id: int, username: str, rol: str, nombre: str,
                 ip: str = "", user_agent: str = "") -> str:
    """
    Crea una sesión en la DB y devuelve el token.
    """
    token = secrets.token_urlsafe(48)
    expira = _iso_en(DURACION_HORAS * 60)

    conn = conectar()
    try:
        conn.execute(
            """INSERT INTO sesiones
               (token, user_id, username, rol, nombre, ip, user_agent,
                creado_en, expira_en, ultima_actividad)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (token, user_id, username, rol, nombre, ip, user_agent,
             _now_iso(), expira, _now_iso()),
        )
        conn.commit()
    finally:
        conn.close()
    return token


def validar_token(token: str) -> dict:
    """
    Valida token, actualiza última actividad, devuelve datos del usuario.
    Tira HTTPException(401) si no es válido o expiró.
    """
    if not token:
        raise HTTPException(status_code=401, detail="Token requerido")

    conn = conectar()
    try:
        row = conn.execute(
            "SELECT * FROM sesiones WHERE token = ?",
            (token,),
        ).fetchone()
        if not row:
            raise HTTPException(status_code=401, detail="Sesión inválida")

        data = dict(row)
        ahora = datetime.now(timezone.utc)

        # Expiración absoluta
        expira = datetime.fromisoformat(data["expira_en"])
        if expira < ahora:
            conn.execute("DELETE FROM sesiones WHERE token = ?", (token,))
            conn.commit()
            raise HTTPException(status_code=401, detail="Sesión expirada")

        # Inactividad
        ult = datetime.fromisoformat(data["ultima_actividad"])
        if (ahora - ult) > timedelta(minutes=INACTIVIDAD_MAX_MINUTOS):
            conn.execute("DELETE FROM sesiones WHERE token = ?", (token,))
            conn.commit()
            raise HTTPException(status_code=401, detail="Sesión expirada por inactividad")

        # Renovar actividad
        conn.execute(
            "UPDATE sesiones SET ultima_actividad = ? WHERE token = ?",
            (_now_iso(), token),
        )
        conn.commit()

        return {
            "id": data["user_id"],
            "username": data["username"],
            "nombre": data["nombre"],
            "rol": data["rol"],
            "token": token,
        }
    finally:
        conn.close()


def invalidar_token(token: str) -> None:
    """Borra la sesión (logout)."""
    if not token:
        return
    conn = conectar()
    try:
        conn.execute("DELETE FROM sesiones WHERE token = ?", (token,))
        conn.commit()
    finally:
        conn.close()


def invalidar_usuario(user_id: int) -> int:
    """Borra TODAS las sesiones de un usuario (cambio de password, etc.)."""
    conn = conectar()
    try:
        cur = conn.execute("DELETE FROM sesiones WHERE user_id = ?", (user_id,))
        conn.commit()
        return cur.rowcount if hasattr(cur, "rowcount") else 0
    finally:
        conn.close()


def limpiar_sesiones_expiradas() -> int:
    """
    Borra sesiones que ya no valen. Correr periódicamente.
    Devuelve cantidad borrada.
    """
    ahora = _now_iso()
    conn = conectar()
    try:
        conn.execute("DELETE FROM sesiones WHERE expira_en < ?", (ahora,))
        conn.commit()
        return 0
    finally:
        conn.close()
