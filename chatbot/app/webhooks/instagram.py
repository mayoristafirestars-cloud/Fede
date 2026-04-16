"""Webhook de Instagram Messaging (Messenger Platform sobre IG)."""
from __future__ import annotations

import logging

from fastapi import APIRouter, Request, Response

from ..config import get_settings
from ..core import handler
from ..models import IncomingMessage

log = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook/instagram", tags=["instagram"])


@router.get("")
async def verify(request: Request) -> Response:
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
    log.debug("IG payload: %s", payload)

    for entry in payload.get("entry", []):
        for ev in entry.get("messaging", []):
            msg = _parse(ev)
            if msg:
                await handler.handle(msg)
    return {"status": "ok"}


def _parse(ev: dict) -> IncomingMessage | None:
    sender_id = ev.get("sender", {}).get("id")
    message = ev.get("message", {})
    if not sender_id or not message:
        return None
    # Filtrar echos (mensajes enviados por nosotros que IG nos repite).
    if message.get("is_echo"):
        return None

    msg_id = message.get("mid", "")
    text = message.get("text", "")

    common = dict(
        channel="instagram",
        user_id=sender_id,
        message_id=msg_id,
        raw=ev,
    )

    if text:
        return IncomingMessage(kind="text", text=text, **common)

    # Audio viene como attachment con type='audio' y URL en payload.url
    for att in message.get("attachments", []):
        atype = att.get("type")
        url = att.get("payload", {}).get("url")
        if atype == "audio" and url:
            return IncomingMessage(kind="audio", media_url=url, **common)
        if atype == "image" and url:
            return IncomingMessage(kind="image", media_url=url, **common)

    return IncomingMessage(kind="unsupported", **common)
