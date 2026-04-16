"""
Cliente Anthropic (Claude) con prompt caching.

Diseño del prompt:
- System = [reglas cacheadas 1h] + [inventario cacheado 5min]
- Messages = historial breve de la conversación + último mensaje del user

Prompt caching ahorra ~90% del costo después del primer mensaje, porque
los bloques grandes (reglas + inventario) no se re-tokenizan.
"""
from __future__ import annotations

import os
from typing import Iterable

from anthropic import Anthropic


ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Modelo por defecto. Haiku 4.5 es rápido y barato, suficiente para este
# caso. Si notás que responde mal a consultas complejas, subí a Sonnet 4.6
# con BOT_MODEL=claude-sonnet-4-6.
MODEL = os.environ.get("BOT_MODEL", "claude-haiku-4-5-20251001")

MAX_TOKENS = int(os.environ.get("BOT_MAX_TOKENS", "400"))


_client = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        if not ANTHROPIC_API_KEY:
            raise RuntimeError(
                "ANTHROPIC_API_KEY no está seteada. Configurala en "
                "Render > Environment (Settings > Environment Variables)."
            )
        _client = Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def responder(
    system_reglas: str,
    inventario_texto: str,
    historial: list[dict],
    mensaje_usuario: str,
) -> str:
    """
    Llama a Claude y devuelve la respuesta como string.

    historial: [{"rol": "user"|"assistant", "contenido": "..."}]
    mensaje_usuario: el último mensaje, que se agrega al final.
    """
    client = _get_client()

    # System con 2 bloques cacheables.
    system = [
        {
            "type": "text",
            "text": system_reglas,
            "cache_control": {"type": "ephemeral", "ttl": "1h"},
        },
        {
            "type": "text",
            "text": inventario_texto,
            "cache_control": {"type": "ephemeral"},  # default 5min
        },
    ]

    # Historial reciente (sin tool calls, sin system; sólo user/assistant).
    messages = []
    for m in historial:
        rol = m.get("rol", "user")
        if rol not in ("user", "assistant"):
            continue
        texto = (m.get("contenido") or "").strip()
        if not texto:
            continue
        messages.append({"role": rol, "content": texto})

    # Mensaje actual del cliente.
    messages.append({"role": "user", "content": mensaje_usuario})

    resp = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=messages,
    )

    # Extraer texto plano de la respuesta.
    partes = []
    for bloque in resp.content:
        if getattr(bloque, "type", None) == "text":
            partes.append(bloque.text)
    texto = "".join(partes).strip()

    if not texto:
        # Fallback defensivo. No debería pasar salvo modelo loco.
        texto = "Disculpá, no pude procesar eso. ¿Podés repetirlo?"

    return texto
