"""Transcripción de audios con OpenAI Whisper."""
from __future__ import annotations

import io
import logging
from typing import Optional

from openai import AsyncOpenAI

from ..config import get_settings

log = logging.getLogger(__name__)


async def transcribe_audio(audio_bytes: bytes, filename: str = "audio.ogg") -> Optional[str]:
    """Devuelve el texto del audio o None si falla."""
    s = get_settings()
    if not s.openai_api_key:
        log.warning("OPENAI_API_KEY no configurada; no se transcribe")
        return None

    client = AsyncOpenAI(api_key=s.openai_api_key)
    buf = io.BytesIO(audio_bytes)
    buf.name = filename  # Whisper usa la extensión para detectar formato.

    try:
        resp = await client.audio.transcriptions.create(
            model=s.whisper_model,
            file=buf,
        )
        return (resp.text or "").strip()
    except Exception as e:  # noqa: BLE001
        log.exception("Error transcribiendo audio: %s", e)
        return None
