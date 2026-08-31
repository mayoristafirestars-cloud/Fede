"""Configuración por variables de entorno (con soporte de archivo .env)."""
from __future__ import annotations

import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def cargar_env(ruta: Path | None = None) -> None:
    """Carga un .env simple sin dependencias externas.

    Ignora comentarios y líneas vacías, y no pisa variables ya exportadas
    en el entorno real (que siempre mandan sobre el archivo).
    """
    ruta = ruta or RAIZ / ".env"
    if not ruta.exists():
        return
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, _, valor = linea.partition("=")
        clave = clave.strip()
        valor = valor.strip().strip('"').strip("'")
        os.environ.setdefault(clave, valor)


def env(clave: str, defecto: str = "") -> str:
    return os.environ.get(clave, defecto).strip()


def env_float(clave: str, defecto: float) -> float:
    try:
        return float(os.environ[clave])
    except (KeyError, ValueError):
        return defecto


def env_int(clave: str, defecto: int) -> int:
    try:
        return int(os.environ[clave])
    except (KeyError, ValueError):
        return defecto


def env_bool(clave: str, defecto: bool = False) -> bool:
    valor = env(clave).lower()
    if not valor:
        return defecto
    return valor in {"1", "true", "si", "sí", "yes", "on"}


cargar_env()
