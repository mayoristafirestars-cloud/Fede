"""
Cliente de Meta Graph API: verificación de webhook, firma HMAC y
envío de mensajes a WhatsApp e Instagram.
"""
from __future__ import annotations

import hashlib
import hmac
import os
from dataclasses import dataclass, field
from typing import Optional

import httpx


# ─── Config ────────────────────────────────────────────────

META_VERIFY_TOKEN = os.environ.get("META_VERIFY_TOKEN", "")
META_APP_SECRET = os.environ.get("META_APP_SECRET", "")

WHATSAPP_PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_ACCESS_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN", "")

INSTAGRAM_ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "")
INSTAGRAM_ACCOUNT_ID = os.environ.get("INSTAGRAM_ACCOUNT_ID", "")

GRAPH_VERSION = os.environ.get("META_GRAPH_VERSION", "v21.0")
GRAPH_BASE = f"https://graph.facebook.com/{GRAPH_VERSION}"


# ─── Modelos ───────────────────────────────────────────────

@dataclass
class MensajeEntrante:
    canal: str                       # "whatsapp" | "instagram"
    sesion_id: str                   # wa_id (WA) o IGSID (IG)
    message_id: str                  # wamid.xxx / mid
    texto: str = ""
    tipo: str = "text"               # text | audio | image | interactive | otro
    media_id: str = ""               # para audio/image — bajar luego con /media/{id}
    telefono: str = ""               # E.164 sin '+' si es WhatsApp
    nombre_cliente: str = ""
    timestamp: str = ""
    raw: dict = field(default_factory=dict)


# ─── Verificación GET /webhooks/meta ───────────────────────

def verificar_webhook(mode: str, token: str, challenge: str) -> Optional[str]:
    """
    Meta hace GET con mode=subscribe, hub.verify_token, hub.challenge
    cuando configurás el webhook. Si el token matchea, devolvemos el
    challenge tal cual; si no, None (el endpoint devuelve 403).
    """
    if mode == "subscribe" and token and META_VERIFY_TOKEN and token == META_VERIFY_TOKEN:
        return challenge
    return None


# ─── Firma HMAC de webhooks ────────────────────────────────

def validar_firma(body_bytes: bytes, signature_header: str) -> bool:
    """
    Meta manda X-Hub-Signature-256: sha256=<hex>
    Lo validamos con HMAC-SHA256 usando META_APP_SECRET.
    """
    if not META_APP_SECRET:
        # Si no está seteado, rechazamos (no se puede validar).
        return False
    if not signature_header or "=" not in signature_header:
        return False

    _, recibido = signature_header.split("=", 1)
    esperado = hmac.new(
        META_APP_SECRET.encode("utf-8"),
        body_bytes,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(recibido, esperado)


# ─── Parseo de payloads ────────────────────────────────────

def parsear_mensajes(payload: dict) -> list[MensajeEntrante]:
    """
    Parsea un payload genérico de Meta. Soporta WhatsApp Cloud API y
    Instagram Messaging. Devuelve lista de mensajes entrantes.
    """
    mensajes: list[MensajeEntrante] = []

    # Formato WhatsApp Cloud API
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            messaging_product = value.get("messaging_product")
            if messaging_product == "whatsapp":
                mensajes.extend(_parsear_whatsapp(value))
                continue

        # Formato Messenger/Instagram
        for msg_event in entry.get("messaging", []):
            m = _parsear_instagram(msg_event, entry.get("id", ""))
            if m:
                mensajes.append(m)

    return mensajes


def _parsear_whatsapp(value: dict) -> list[MensajeEntrante]:
    contactos = {c["wa_id"]: c for c in value.get("contacts", [])}
    out: list[MensajeEntrante] = []
    for msg in value.get("messages", []):
        wa_id = msg.get("from", "")
        tipo = msg.get("type", "text")
        texto = ""
        media_id = ""

        if tipo == "text":
            texto = (msg.get("text", {}) or {}).get("body", "")
        elif tipo == "audio":
            media_id = (msg.get("audio", {}) or {}).get("id", "")
        elif tipo == "image":
            media_id = (msg.get("image", {}) or {}).get("id", "")
            texto = (msg.get("image", {}) or {}).get("caption", "") or ""
        elif tipo == "interactive":
            interactive = msg.get("interactive", {}) or {}
            if interactive.get("type") == "button_reply":
                texto = (interactive.get("button_reply") or {}).get("title", "")
            elif interactive.get("type") == "list_reply":
                texto = (interactive.get("list_reply") or {}).get("title", "")

        nombre = ""
        contacto = contactos.get(wa_id)
        if contacto:
            nombre = (contacto.get("profile") or {}).get("name", "") or ""

        out.append(MensajeEntrante(
            canal="whatsapp",
            sesion_id=wa_id,
            message_id=msg.get("id", ""),
            texto=texto,
            tipo=tipo,
            media_id=media_id,
            telefono=wa_id,
            nombre_cliente=nombre,
            timestamp=msg.get("timestamp", ""),
            raw=msg,
        ))
    return out


def _parsear_instagram(event: dict, page_id: str) -> Optional[MensajeEntrante]:
    sender = (event.get("sender") or {}).get("id", "")
    if not sender:
        return None
    mensaje = event.get("message") or {}
    mid = mensaje.get("mid", "")
    texto = mensaje.get("text", "") or ""
    # Adjuntos (audio/image)
    media_id = ""
    tipo = "text"
    attachments = mensaje.get("attachments") or []
    if attachments:
        att = attachments[0]
        att_type = att.get("type", "")
        payload = att.get("payload") or {}
        if att_type in ("audio", "image", "video"):
            tipo = att_type
            media_id = payload.get("url", "") or ""  # IG suele mandar URL directa

    return MensajeEntrante(
        canal="instagram",
        sesion_id=sender,
        message_id=mid,
        texto=texto,
        tipo=tipo,
        media_id=media_id,
        timestamp=str(event.get("timestamp", "")),
        raw=event,
    )


# ─── Envío de mensajes ─────────────────────────────────────

def enviar_whatsapp(to: str, texto: str) -> dict:
    """Envía un mensaje de texto via WhatsApp Cloud API."""
    if not WHATSAPP_ACCESS_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
        raise RuntimeError(
            "Faltan WHATSAPP_ACCESS_TOKEN o WHATSAPP_PHONE_NUMBER_ID en env."
        )

    url = f"{GRAPH_BASE}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"preview_url": False, "body": texto[:4000]},
    }
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    with httpx.Client(timeout=20.0) as client:
        r = client.post(url, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()


def enviar_instagram(recipient_id: str, texto: str) -> dict:
    """Envía un mensaje de texto via Messenger/Instagram Messaging."""
    token = INSTAGRAM_ACCESS_TOKEN
    if not token or not INSTAGRAM_ACCOUNT_ID:
        raise RuntimeError(
            "Faltan INSTAGRAM_ACCESS_TOKEN o INSTAGRAM_ACCOUNT_ID en env."
        )
    url = f"{GRAPH_BASE}/{INSTAGRAM_ACCOUNT_ID}/messages"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": texto[:2000]},
        "messaging_type": "RESPONSE",
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    with httpx.Client(timeout=20.0) as client:
        r = client.post(url, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()


def enviar(canal: str, destino: str, texto: str) -> dict:
    """Fachada para enviar en cualquier canal."""
    if canal == "whatsapp":
        return enviar_whatsapp(destino, texto)
    elif canal == "instagram":
        return enviar_instagram(destino, texto)
    else:
        raise ValueError(f"Canal desconocido: {canal}")


# ─── Bajar media (audio/imagen) ────────────────────────────

def url_de_media_whatsapp(media_id: str) -> Optional[str]:
    """
    WhatsApp media API: se pide la URL en 2 pasos.
    1) GET /{media-id} con el token → devuelve { "url": "..." }
    2) GET esa URL con el token en Authorization → bytes del archivo.
    Esta función hace sólo el paso 1.
    """
    if not media_id or not WHATSAPP_ACCESS_TOKEN:
        return None
    url = f"{GRAPH_BASE}/{media_id}"
    headers = {"Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}"}
    with httpx.Client(timeout=20.0) as client:
        r = client.get(url, headers=headers)
        if r.status_code != 200:
            return None
        return (r.json() or {}).get("url")


def bajar_media_whatsapp(media_id: str) -> Optional[bytes]:
    """Devuelve los bytes del archivo de media de WhatsApp."""
    url = url_de_media_whatsapp(media_id)
    if not url:
        return None
    headers = {"Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}"}
    with httpx.Client(timeout=30.0) as client:
        r = client.get(url, headers=headers)
        if r.status_code != 200:
            return None
        return r.content
