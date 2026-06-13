"""Lógica central: recibe un IncomingMessage y manda una respuesta."""
from __future__ import annotations

import logging

from ..models import IncomingMessage
from ..services import claude, conversation, meta_api, transcribe

log = logging.getLogger(__name__)


async def handle(msg: IncomingMessage) -> None:
    # Idempotencia: Meta puede reentregar el mismo webhook.
    if conversation.already_processed(msg.message_id):
        log.info("Mensaje %s ya procesado, ignoro", msg.message_id)
        return

    user_text = await _extract_text(msg)
    if not user_text:
        await _send(msg, "No pude leer tu mensaje. ¿Me lo reenviás como texto?")
        return

    history = conversation.get_history(msg.channel, msg.user_id, limit=20)
    answer = await claude.reply(msg.channel, history, user_text)
    if not answer:
        answer = "Tuvimos un problema técnico. Probá de nuevo en un rato."

    conversation.append_message(msg.channel, msg.user_id, "user", user_text)
    conversation.append_message(msg.channel, msg.user_id, "assistant", answer)

    await _send(msg, answer)


async def _extract_text(msg: IncomingMessage) -> str:
    if msg.kind == "text":
        return msg.text.strip()

    if msg.kind == "audio":
        audio_bytes = await _download_audio(msg)
        if not audio_bytes:
            return ""
        text = await transcribe.transcribe_audio(audio_bytes)
        if text:
            log.info("Audio transcripto (%s chars)", len(text))
            return text
        return ""

    # imagen u otro tipo no soportado todavía
    return ""


async def _download_audio(msg: IncomingMessage) -> bytes | None:
    if msg.media_url:
        return await meta_api.download_media(msg.media_url)
    if msg.media_id:
        url = await meta_api.get_whatsapp_media_url(msg.media_id)
        if not url:
            return None
        return await meta_api.download_media(url)
    return None


async def _send(msg: IncomingMessage, text: str) -> None:
    try:
        if msg.channel == "whatsapp":
            await meta_api.send_whatsapp_text(msg.user_id, text)
        elif msg.channel == "instagram":
            await meta_api.send_instagram_text(msg.user_id, text)
    except meta_api.MetaAPIError as e:
        log.error("No se pudo enviar respuesta: %s", e)
