"""
Bot multicanal — agente conversacional para WhatsApp e Instagram.

Arquitectura:
- `productos`       lee la DB aplicando el filtro de rol "bot"
                    (no ve precio_costo, precio_mayorista, proveedor,
                    ni datos de ventas).
- `conversaciones`  mantiene memoria corta por sesión en la tabla
                    bot_conversaciones.
- `prompts`         arma el system prompt + renderiza el catálogo.
- `claude`          cliente Anthropic con prompt caching del inventario.
- `meta`            firma HMAC de webhooks + envío de mensajes a
                    WhatsApp/Instagram.
- `transcribe`      Whisper opcional para mensajes de audio.

El router vive en `backend/routers/bot.py`.
"""

__all__ = []
