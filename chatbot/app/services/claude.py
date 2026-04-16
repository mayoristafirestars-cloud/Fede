"""Cerebro IA: genera la respuesta usando Claude (Anthropic).

Usa prompt caching para no pagar la planilla completa en cada
mensaje: el system prompt + la planilla de precios se marcan
como `cache_control` y Anthropic los reusa por hasta 5 minutos.
"""
from __future__ import annotations

import logging
from typing import Optional

from anthropic import AsyncAnthropic

from ..config import get_settings
from . import sheets

log = logging.getLogger(__name__)


def _system_blocks(business_name: str, channel: str) -> list[dict]:
    """System prompt en bloques para aprovechar prompt caching."""
    instructions = f"""Sos el asistente de atención al cliente de {business_name}.
Respondés a clientes que escriben por {channel}.

REGLAS:
- Hablás en español rioplatense, tono cordial y directo, sin emojis salvo
  uno ocasional para saludar.
- Mensajes cortos (1 a 4 líneas). Si te piden lista, podés extender.
- Para precios, montos y stock SIEMPRE usás la "PLANILLA DE PRECIOS" que
  está más abajo. Si el producto no está, decilo de forma honesta y ofrecé
  pasar la consulta a un humano.
- NUNCA te inventes precios, stock ni códigos.
- Si te piden algo que no sea sobre productos, precios, pedidos o envíos,
  contestá brevemente y volvé al tema comercial.
- Si el cliente manda un audio, ya viene transcripto. Tratalo como texto.
- Cuando un cliente quiere comprar: pedí (en este orden y de a uno por
  mensaje si hace falta) producto + cantidad, datos de envío y forma de
  pago. Confirmá el total al final con los precios de la planilla.
"""

    price_table = sheets.render_price_table_for_prompt()
    price_block = (
        "PLANILLA DE PRECIOS (fuente de verdad, los datos vienen de la "
        "planilla de Google Sheets del negocio):\n\n" + price_table
    )

    return [
        {
            "type": "text",
            "text": instructions,
            "cache_control": {"type": "ephemeral"},
        },
        {
            "type": "text",
            "text": price_block,
            "cache_control": {"type": "ephemeral"},
        },
    ]


async def reply(
    channel: str, history: list[dict], user_message: str
) -> Optional[str]:
    """Genera la respuesta del asistente.

    `history` es una lista de {role, content} con los últimos turnos
    (sin incluir todavía el `user_message` actual).
    """
    s = get_settings()
    if not s.anthropic_api_key:
        log.warning("ANTHROPIC_API_KEY no configurada")
        return "Disculpá, ahora mismo no puedo responder. Te contestamos en un rato."

    client = AsyncAnthropic(api_key=s.anthropic_api_key)

    messages = list(history)
    messages.append({"role": "user", "content": user_message})

    try:
        resp = await client.messages.create(
            model=s.claude_model,
            max_tokens=600,
            system=_system_blocks(s.business_name, channel),
            messages=messages,
        )
    except Exception as e:  # noqa: BLE001
        log.exception("Error llamando a Claude: %s", e)
        return "Tuvimos un problema técnico. ¿Podés reescribirme en un rato?"

    # Tomar el primer bloque de texto.
    for block in resp.content:
        if getattr(block, "type", None) == "text":
            return block.text.strip()
    return None
