"""Cliente para la Graph API de Meta (WhatsApp Cloud + Instagram Messaging)."""
from __future__ import annotations

import logging
from typing import Optional

import httpx

from ..config import get_settings

log = logging.getLogger(__name__)

GRAPH_VERSION = "v21.0"
GRAPH_BASE = f"https://graph.facebook.com/{GRAPH_VERSION}"


class MetaAPIError(Exception):
    pass


async def send_whatsapp_text(to_wa_id: str, text: str) -> dict:
    """Envía un mensaje de texto a un WhatsApp dado."""
    s = get_settings()
    if not s.whatsapp_phone_number_id or not s.meta_access_token:
        raise MetaAPIError("Faltan WHATSAPP_PHONE_NUMBER_ID o META_ACCESS_TOKEN")

    url = f"{GRAPH_BASE}/{s.whatsapp_phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_wa_id,
        "type": "text",
        "text": {"body": text[:4096]},
    }
    headers = {"Authorization": f"Bearer {s.meta_access_token}"}

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, json=payload, headers=headers)
        if r.status_code >= 300:
            log.error("WhatsApp send error %s: %s", r.status_code, r.text)
            raise MetaAPIError(f"WhatsApp {r.status_code}: {r.text}")
        return r.json()


async def send_instagram_text(to_igsid: str, text: str) -> dict:
    """Envía un mensaje DM por Instagram al usuario IGSID dado."""
    s = get_settings()
    if not s.instagram_account_id or not s.meta_access_token:
        raise MetaAPIError("Faltan INSTAGRAM_ACCOUNT_ID o META_ACCESS_TOKEN")

    url = f"{GRAPH_BASE}/{s.instagram_account_id}/messages"
    payload = {
        "recipient": {"id": to_igsid},
        "message": {"text": text[:1000]},
    }
    headers = {"Authorization": f"Bearer {s.meta_access_token}"}

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, json=payload, headers=headers)
        if r.status_code >= 300:
            log.error("Instagram send error %s: %s", r.status_code, r.text)
            raise MetaAPIError(f"Instagram {r.status_code}: {r.text}")
        return r.json()


async def get_whatsapp_media_url(media_id: str) -> Optional[str]:
    """Resuelve el media_id de WhatsApp a una URL temporal de descarga."""
    s = get_settings()
    url = f"{GRAPH_BASE}/{media_id}"
    headers = {"Authorization": f"Bearer {s.meta_access_token}"}
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url, headers=headers)
        if r.status_code >= 300:
            log.error("Media URL fetch error %s: %s", r.status_code, r.text)
            return None
        return r.json().get("url")


async def download_media(url: str) -> Optional[bytes]:
    """Descarga el contenido de una URL (con bearer si es de Meta)."""
    s = get_settings()
    headers = {}
    if "facebook.com" in url or "fbcdn.net" in url:
        headers = {"Authorization": f"Bearer {s.meta_access_token}"}
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.get(url, headers=headers, follow_redirects=True)
        if r.status_code >= 300:
            log.error("Media download error %s", r.status_code)
            return None
        return r.content
