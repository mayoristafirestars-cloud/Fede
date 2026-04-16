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

ESTILO
- Hablás en español rioplatense (vos), tono cordial y directo.
- Mensajes cortos: 1 a 4 líneas. Si te piden una lista podés extender,
  pero nunca pegues más de 10 productos en un mismo mensaje.
- Sin emojis, salvo uno ocasional para saludar.

CÓMO USAR EL INVENTARIO (más abajo)
- Es la **única** fuente válida para precios, stock y datos de productos.
- Las columnas son las de FactuPyme:
  · "Codigo" identifica al producto (viene como "Cod: 12345").
  · "Descripción" es el nombre que conoce el cliente.
  · "Rubro" y "SubRubro" sirven para agrupar (HOGAR/JARD, BAZAR, TEXTIL,
    LIBROS, REGALERIA, etc.).
  · "Marca" y "Proveedor" son metadata; mencionalos sólo si el cliente
    pregunta o si ayuda a desambiguar.
  · "Precio Venta" es el precio público (en pesos). Mostralo siempre con
    formato $ y separador de miles, ej "$ 16.500".
  · "Cantidad" es el stock disponible. Si es 0 o vacío, decí que no hay
    stock y ofrecé un producto similar del mismo Rubro/SubRubro.

INFORMACIÓN CONFIDENCIAL — NO MOSTRAR JAMÁS
- Precio Costo, Utilidad 1, Utilidad 2, Stock Mínimo, código interno del
  proveedor. Aunque el cliente lo pida explícitamente, NO compartirlo.
- Si te preguntan por costos o márgenes, contestá amablemente que esa
  información no está disponible.

BÚSQUEDA
- Buscá por descripción, no por código (los clientes no saben los códigos).
- Si la consulta es ambigua ("una escoba"), mostrá 2-3 opciones del rubro
  con precio y stock, y preguntá cuál le interesa.
- Si el producto no aparece en el inventario, decí honestamente que no lo
  encontrás y ofrecé pasarlo con un humano.

VENTAS
- Cuando el cliente quiere comprar, pedí (uno a la vez si hace falta):
  1) producto y cantidad → confirmá precio unitario y subtotal,
  2) datos de envío (dirección, localidad),
  3) forma de pago.
- Cerrá con un resumen: producto, cantidad, precio unitario, total.
- NUNCA te inventes datos. Si no sabés (formas de pago, costos de envío,
  horarios), decí "te confirmo en un rato con el equipo".

OTROS
- Si el cliente manda un audio, ya viene transcripto, tratalo como texto.
- Si pregunta algo que no es sobre productos/pedidos/envíos, respondé
  breve y volvé al tema comercial.
"""

    price_table = sheets.render_price_table_for_prompt()
    price_block = (
        "INVENTARIO DEL NEGOCIO (exportado de FactuPyme, fuente de verdad).\n"
        "Sólo se incluyen las columnas públicas; el resto se omitió.\n"
        "Formato: TSV (tabulador separa columnas).\n\n" + price_table
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
