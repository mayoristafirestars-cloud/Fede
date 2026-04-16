"""Lector de la planilla de precios alojada en Google Sheets.

Cachea el contenido en memoria por SHEET_CACHE_SECONDS para no
pegarle a Google en cada mensaje.
"""
from __future__ import annotations

import json
import logging
import threading
import time
from typing import Optional

import gspread
from google.oauth2.service_account import Credentials

from ..config import get_settings

log = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


class _Cache:
    def __init__(self) -> None:
        self.rows: list[dict] = []
        self.fetched_at: float = 0.0
        self.lock = threading.Lock()


_cache = _Cache()


def _credentials() -> Optional[Credentials]:
    s = get_settings()
    if s.google_service_account_json:
        info = json.loads(s.google_service_account_json)
        return Credentials.from_service_account_info(info, scopes=SCOPES)
    if s.google_service_account_file:
        return Credentials.from_service_account_file(
            s.google_service_account_file, scopes=SCOPES
        )
    return None


def _fetch_now() -> list[dict]:
    s = get_settings()
    creds = _credentials()
    if not creds or not s.google_sheet_id:
        log.warning("Google Sheets sin credenciales o sin SHEET_ID configurado")
        return []
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(s.google_sheet_id)
    ws = sh.worksheet(s.google_sheet_tab)
    # get_all_records usa la primera fila como encabezados.
    return ws.get_all_records()


def get_price_rows(force: bool = False) -> list[dict]:
    """Devuelve la planilla como lista de dicts (encabezado → valor)."""
    s = get_settings()
    with _cache.lock:
        fresh = (time.time() - _cache.fetched_at) < s.sheet_cache_seconds
        if _cache.rows and fresh and not force:
            return _cache.rows
        try:
            _cache.rows = _fetch_now()
            _cache.fetched_at = time.time()
        except Exception as e:  # noqa: BLE001
            log.exception("No se pudo leer Google Sheets: %s", e)
            # Si tenemos algo viejo en cache, lo seguimos usando.
        return _cache.rows


def render_price_table_for_prompt(max_rows: int = 500) -> str:
    """Devuelve la planilla en texto plano para mandarle a Claude."""
    rows = get_price_rows()
    if not rows:
        return "(La planilla de precios todavía no está disponible.)"
    cols = list(rows[0].keys())
    lines = ["\t".join(cols)]
    for row in rows[:max_rows]:
        lines.append("\t".join(str(row.get(c, "")) for c in cols))
    if len(rows) > max_rows:
        lines.append(f"... ({len(rows) - max_rows} filas más omitidas)")
    return "\n".join(lines)
