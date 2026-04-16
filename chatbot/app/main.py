"""Servidor FastAPI del chatbot multicanal."""
from __future__ import annotations

import logging

from fastapi import FastAPI

from .config import get_settings
from .services import conversation, sheets
from .webhooks import instagram, whatsapp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
)
log = logging.getLogger(__name__)


app = FastAPI(title="Chatbot Multicanal", version="0.1.0")
app.include_router(whatsapp.router)
app.include_router(instagram.router)


@app.on_event("startup")
def _startup() -> None:
    s = get_settings()
    conversation.init_db()
    # Pre-cargar la planilla en memoria (no falla si todavía no
    # tenemos credenciales; reintenta al primer mensaje).
    try:
        sheets.get_price_rows(force=True)
    except Exception as e:  # noqa: BLE001
        log.warning("Planilla no cargada al arranque: %s", e)
    log.info("Chatbot listo (negocio=%s)", s.business_name)


@app.get("/")
def root() -> dict:
    return {"status": "ok", "service": "chatbot-multicanal"}


@app.get("/health")
def health() -> dict:
    s = get_settings()
    rows = sheets.get_price_rows()
    return {
        "ok": True,
        "business": s.business_name,
        "whatsapp_configured": bool(s.whatsapp_phone_number_id and s.meta_access_token),
        "instagram_configured": bool(s.instagram_account_id and s.meta_access_token),
        "claude_configured": bool(s.anthropic_api_key),
        "whisper_configured": bool(s.openai_api_key),
        "sheet_configured": bool(s.google_sheet_id),
        "sheet_rows": len(rows),
    }
