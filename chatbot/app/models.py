"""Modelos de dominio compartidos entre canales."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional


Channel = Literal["whatsapp", "instagram"]
MessageKind = Literal["text", "audio", "image", "unsupported"]


@dataclass
class IncomingMessage:
    """Mensaje normalizado, independiente del canal."""

    channel: Channel
    # ID estable del usuario en ese canal (wa_id o IGSID).
    user_id: str
    # ID del mensaje en la plataforma (para no procesarlo dos veces).
    message_id: str
    kind: MessageKind
    # Texto del mensaje (vacío si era audio sin transcribir).
    text: str = ""
    # ID de media en Meta (audio/imagen). Para descarga posterior.
    media_id: Optional[str] = None
    # URL directa cuando viene de Instagram (que adjunta URL).
    media_url: Optional[str] = None
    # Nombre/handle si lo trae el webhook.
    sender_name: str = ""
    raw: dict = field(default_factory=dict)
