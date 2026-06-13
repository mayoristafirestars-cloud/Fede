# Fase 2 — Bot multicanal integrado al CRM

Este paquete agrega el bot de WhatsApp + Instagram al CRM Coronel Sur
como un router nativo. Comparte DB, deploy y seguridad con el resto
del sistema.

## ⚠️ Pre-requisito

**Fase 0 debe estar aplicada y mergeada a `main`** (reutilizamos
`backend/security/` para proteger endpoints internos y la tabla
`sesiones` persistente). Si todavía no aplicaste Fase 0, hacelo primero.

## Contenido

- **`files/MIGRATION_FASE_2.md`** — guía paso a paso (leelo primero).
- **`files/backend/bot/`** — módulo nuevo completo:
  - `__init__.py`
  - `productos.py` — queries a DB con filtro de rol bot
  - `conversaciones.py` — memoria corta por sesión en la DB
  - `prompts.py` — system prompts + render del catálogo
  - `claude.py` — cliente Anthropic con prompt caching
  - `meta.py` — verificación de webhook + firma HMAC + envío a
    WhatsApp/Instagram + bajar media
  - `transcribe.py` — Whisper opcional para audios
- **`files/backend/routers/bot.py`** — webhooks Meta + endpoints admin.
- **`files/backend/db/database.py`** — tablas nuevas:
  `bot_sesiones`, `bot_conversaciones`, `bot_mensajes_procesados`.
- **`files/backend/main.py`** — `include_router(router_bot)`.
- **`files/requirements.txt`** — +anthropic, +openai.

## Resumen ejecutivo

### El bot:
- Recibe mensajes de WhatsApp Cloud API y Instagram Messaging.
- Valida la firma HMAC de Meta en cada POST.
- Dedupe de eventos repetidos.
- Transcribe audios de WhatsApp con Whisper (opcional).
- Lee productos con filtro de privacidad hardcoded:
  - **SÍ** ve: código, descripción, rubro, precio_venta, disponibilidad.
  - **NO** ve: precio_costo, precio_mayorista, proveedor, margen.
- Recuerda últimos 8 turnos por cliente; reset automático tras 24h sin
  actividad.
- Usa Claude Haiku 4.5 + prompt caching (~90% ahorro tras el primer
  mensaje). Cambiable a Sonnet 4.6 por env var.

### Endpoints expuestos:

Públicos (Meta los llama):
- `GET  /webhooks/meta` — handshake de verificación
- `POST /webhooks/meta` — recepción de mensajes

Internos (requieren token admin):
- `GET  /api/bot/stats` — métricas
- `POST /api/bot/probar` — simular un mensaje sin pasar por Meta

### Secrets que tenés que setear en Render:

Obligatorios:
- `ANTHROPIC_API_KEY`
- `META_VERIFY_TOKEN` (lo inventás vos, también lo pegás en Meta)
- `META_APP_SECRET`
- `WHATSAPP_PHONE_NUMBER_ID`
- `WHATSAPP_ACCESS_TOKEN`

Opcionales:
- `INSTAGRAM_ACCESS_TOKEN`, `INSTAGRAM_ACCOUNT_ID` (si querés IG)
- `OPENAI_API_KEY` (para transcripción de audios)
- `BOT_MODEL=claude-sonnet-4-6` (para mejor calidad)
- `BOT_STOCK_FORMATO=numerico` (para mostrar stock exacto)

## Cómo aplicar

Mismo procedimiento que Fase 0: copiás los archivos al clon local de
tu repo privado `Coronel-Sur`, commit, push, PR, merge, deploy.

Ver `files/MIGRATION_FASE_2.md` para el paso a paso completo, incluyendo
cómo configurar el webhook en Meta for Developers.

## Testing en seco antes de configurar Meta

El endpoint `POST /api/bot/probar` te deja mandarle mensajes al bot sin
necesidad de WhatsApp/Instagram. Solo con `ANTHROPIC_API_KEY` seteada:

```bash
curl -X POST https://coronel-sur.onrender.com/api/bot/probar \
  -H "Authorization: Bearer $TOKEN_ADMIN" \
  -H "Content-Type: application/json" \
  -d '{"texto":"tenes farolitos LED?","sesion_id":"test:1","canal":"whatsapp"}'
```

Respuesta: la respuesta del bot usando tu inventario real.

## Orden recomendado

1. Aplicar Fase 0 (ver `patches/coronel-sur-fase-0/`).
2. Rotar passwords + configurar Render con disco persistente.
3. Aplicar Fase 2 (este paquete).
4. Setear `ANTHROPIC_API_KEY` en Render.
5. Probar con `/api/bot/probar` — **este es el momento "ahá"**: ves al
   bot respondiendo sobre tu inventario sin necesidad de Meta todavía.
6. Si te conforma cómo responde, configurar webhook en Meta y pasar a
   producción.

## Qué falta para el producto completo

Pendiente para fases siguientes (o Fase 2.5 si lo priorizás):

- **Tools / function calling**: que el bot pueda llamar
  `buscar_producto(q)` como herramienta en vez de depender de la
  muestra cacheada. Más preciso para consultas específicas.
- **Entregar presupuestos**: generar un PDF desde el bot.
- **Rate limit del bot**: límite por número/IP para controlar gastos.
- **Dashboard de conversaciones**: vista admin con todas las
  conversaciones, filtros, marcado como "atendida", takeover humano.
- **Handoff a humano**: comando tipo "quiero hablar con un humano"
  que pausa el bot y crea un ticket.

Cuando quieras priorizar alguna de estas, me decís.
