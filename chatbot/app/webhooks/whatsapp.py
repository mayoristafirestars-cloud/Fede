"""Webhook de WhatsApp Cloud API."""
from __future__ import annotations

import logging

from fastapi import APIRouter, Request, Response

from ..config import get_settings
from ..core import handler
from ..models import IncomingMessage

log = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook/whatsapp", tags=["whatsapp"])


@router.get("")
async def verify(request: Request) -> Response:
    """Handshake inicial: Meta verifica el endpoint."""
    s = get_settings()
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge", "")
    if mode == "subscribe" and token == s.meta_verify_token:
        return Response(content=challenge, media_type="text/plain")
    return Response(status_code=403)


@router.post("")
async def receive(request: Request) -> dict:
    payload = await request.json()
    log.debug("WA payload: %s", payload)

    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            contacts = {c["wa_id"]: c.get("profile", {}).get("name", "")
                        for c in value.get("contacts", [])}
            for m in value.get("messages", []):
                msg = _parse(m, contacts)
                if msg:
                    await handler.handle(msg)
    # Meta exige 200 rápido o reentrega.
    return {"status": "ok"}


def _parse(m: dict, contacts: dict[str, str]) -> IncomingMessage | None:
    wa_id = m.get("from")
    msg_id = m.get("id")
    if not wa_id or not msg_id:
        return None

    mtype = m.get("type")
    common = dict(
        channel="whatsapp",
        user_id=wa_id,
        message_id=msg_id,
        sender_name=contacts.get(wa_id, ""),
        raw=m,
    )

    if mtype == "text":
        return IncomingMessage(kind="text", text=m["text"]["body"], **common)
    if mtype in ("audio", "voice"):
        media_id = m.get(mtype, {}).get("id")
        return IncomingMessage(kind="audio", media_id=media_id, **common)
    if mtype == "image":
        media_id = m.get("image", {}).get("id")
        return IncomingMessage(kind="image", media_id=media_id, **common)
    return IncomingMessage(kind="unsupported", **common)
