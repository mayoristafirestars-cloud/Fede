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


def _public_columns(all_cols: list[str]) -> list[str]:
    """Devuelve la lista de columnas visibles para el cliente.

    Si SHEET_PUBLIC_COLUMNS está vacío, devuelve todas. Si no, devuelve
    las que estén en el whitelist *y* existan en la planilla, en el
    orden del whitelist.
    """
    s = get_settings()
    whitelist = [c.strip() for c in s.sheet_public_columns.split(",") if c.strip()]
    if not whitelist:
        return all_cols
    available = {c.lower(): c for c in all_cols}
    return [available[c.lower()] for c in whitelist if c.lower() in available]


def render_price_table_for_prompt(max_rows: int = 800) -> str:
    """Devuelve la planilla filtrada y en TSV para mandarle a Claude.

    Filtra las columnas sensibles (precio costo, utilidades, etc.)
    según SHEET_PUBLIC_COLUMNS antes de mandarle nada al modelo.
    Filas con stock 0 o vacío van al final, así Claude prioriza las
    disponibles cuando se acerca al límite del prompt.
    """
    rows = get_price_rows()
    if not rows:
        return "(La planilla de precios todavía no está disponible.)"

    all_cols = list(rows[0].keys())
    cols = _public_columns(all_cols)

    def _stock(r: dict) -> int:
        for k in ("Cantidad", "cantidad", "Stock", "stock"):
            if k in r:
                try:
                    return int(float(str(r[k]).replace(",", ".") or 0))
                except (ValueError, TypeError):
                    return 0
        return 0

    # Productos con stock primero (Claude verá los disponibles aunque
    # se trunquen las últimas filas).
    rows_sorted = sorted(rows, key=lambda r: _stock(r) <= 0)

    lines = ["\t".join(cols)]
    for row in rows_sorted[:max_rows]:
        lines.append("\t".join(str(row.get(c, "")) for c in cols))
    if len(rows_sorted) > max_rows:
        lines.append(f"... ({len(rows_sorted) - max_rows} filas más omitidas)")
    return "\n".join(lines)
