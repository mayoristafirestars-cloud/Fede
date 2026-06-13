"""
Transcripción de audios con Whisper (OpenAI).

Opcional: si OPENAI_API_KEY no está seteada, devuelve None y el bot
responde con un mensaje pidiendo que escriban en texto.
"""
from __future__ import annotations

import io
import os
from typing import Optional


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "whisper-1")


def transcribir(audio_bytes: bytes, formato_hint: str = "ogg") -> Optional[str]:
    """
    Transcribe audio a texto. Devuelve None si falla o no hay API key.
    `formato_hint`: extensión del archivo (ogg, mp3, m4a, wav). Por
    default WhatsApp manda ogg/opus.
    """
    if not audio_bytes or not OPENAI_API_KEY:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        buf = io.BytesIO(audio_bytes)
        buf.name = f"audio.{formato_hint}"
        resp = client.audio.transcriptions.create(
            model=WHISPER_MODEL,
            file=buf,
            response_format="text",
            language="es",
        )
        # SDK devuelve string si response_format="text"
        return (resp or "").strip() if isinstance(resp, str) else str(resp).strip()
    except Exception:
        return None
