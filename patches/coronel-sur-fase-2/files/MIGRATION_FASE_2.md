# Migración Fase 2 — Bot multicanal integrado al CRM

Esta fase agrega el bot de WhatsApp + Instagram como un router más
dentro del CRM Coronel Sur, compartiendo la misma DB y el mismo deploy.

**Requisito**: Fase 0 (seguridad crítica) debe estar aplicada y
mergeada en `main` ANTES de aplicar esta fase. El bot reutiliza
`backend/security/` para proteger los endpoints internos.

## Qué hace el bot

- Recibe mensajes por WhatsApp e Instagram (webhook de Meta).
- Valida la firma HMAC de Meta (no procesa nada sin firma válida).
- Transcribe audios con Whisper de OpenAI (opcional).
- Responde con Claude Haiku 4.5 (barato, rápido) o Sonnet 4.6
  (premium, setear `BOT_MODEL=claude-sonnet-4-6`).
- Lee productos directamente de la DB con filtro "rol bot":
  - SÍ ve: código, descripción, rubro, precio_venta, disponibilidad.
  - NO ve: precio_costo, precio_mayorista, proveedor, margen, ventas
    históricas.
- Recuerda los últimos 8 turnos por cliente (configurable).
- Si pasan más de 24hs sin mensajes, arranca una conversación nueva.
- Dedupe automático de mensajes por `message_id` (Meta reintenta).

## Arquitectura: archivos nuevos/modificados

### Nuevos

```
backend/bot/
├── __init__.py
├── claude.py          — cliente Anthropic con prompt caching
├── conversaciones.py  — memoria por sesión en DB
├── meta.py            — firma HMAC + envío de WhatsApp/IG
├── productos.py       — queries con filtro rol bot
├── prompts.py         — system prompts + render de catálogo
└── transcribe.py      — Whisper (opcional)

backend/routers/bot.py — webhooks + endpoints admin
```

### Modificados

| Archivo | Cambio |
|---|---|
| `backend/db/database.py` | +tablas `bot_sesiones`, `bot_conversaciones`, `bot_mensajes_procesados` |
| `backend/main.py` | `app.include_router(router_bot)` |
| `requirements.txt` | +anthropic==0.39.0, +openai==1.54.3 |

## Orden de pasos

### Paso 1 — Aplicar el patch al repo privado

Igual que Fase 0: en tu clon local de `Coronel-Sur`, desde la branch
`main` (con Fase 0 ya mergeada):

```bash
git checkout main
git pull origin main
git checkout -b fase-2-bot
git apply --3way /ruta/a/Fede/patches/coronel-sur-fase-2/fase-2-bot.patch
```

Si `git apply` falla, usá la carpeta `files/` como fallback (copiá los
archivos uno por uno).

### Paso 2 — Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 3 — Probar local (sin Meta todavía)

El endpoint `POST /api/bot/probar` te deja simular un mensaje sin
pasar por WhatsApp. Necesita sólo `ANTHROPIC_API_KEY` seteada.

```bash
# Asumiendo que el servidor está corriendo con tu API key configurada:
export ANTHROPIC_API_KEY="sk-ant-..."
cd backend && python main.py &

# Loguearse como admin primero para obtener token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"fede","password":"tu-password"}' | jq -r .token)

# Simular un mensaje de cliente
curl -X POST http://localhost:8000/api/bot/probar \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"texto":"Hola, tenés farolitos LED?","sesion_id":"test:1","canal":"whatsapp"}'
```

La primera vez tarda unos segundos (carga el inventario en cache).
Las siguientes son rápidas y baratas (prompt caching).

### Paso 4 — Commit + push + PR + merge

```bash
git add -A
git commit -m "Fase 2: bot multicanal integrado como router del CRM"
git push origin fase-2-bot
```

PR en GitHub → review → merge.

### Paso 5 — Configurar secrets en Render

En Dashboard > `coronel-sur` > Environment, agregar:

| Variable | Valor | Obligatoria |
|---|---|---|
| `ANTHROPIC_API_KEY` | tu key de Anthropic | ✅ sí |
| `META_VERIFY_TOKEN` | cualquier string random (vos lo elegís, después lo usás en Meta para verificar) | ✅ sí |
| `META_APP_SECRET` | de Meta Developers > Basic Settings > App Secret | ✅ sí |
| `WHATSAPP_PHONE_NUMBER_ID` | de Meta > WhatsApp > API Setup | ✅ sí |
| `WHATSAPP_ACCESS_TOKEN` | token de acceso permanente | ✅ sí |
| `INSTAGRAM_ACCESS_TOKEN` | ídem IG Graph | ◇ solo si usás IG |
| `INSTAGRAM_ACCOUNT_ID` | ID de la cuenta IG Business | ◇ solo si usás IG |
| `OPENAI_API_KEY` | para Whisper | ◇ solo si querés transcripción de audios |
| `BOT_MODEL` | `claude-haiku-4-5-20251001` (default) o `claude-sonnet-4-6` | ◇ opcional |

Render redeployea automático.

### Paso 6 — Configurar webhook en Meta for Developers

1. Ir a https://developers.facebook.com → tu app.
2. **WhatsApp > Configuration > Webhook**:
   - Callback URL: `https://coronel-sur.onrender.com/webhooks/meta`
   - Verify Token: el mismo string que pusiste en `META_VERIFY_TOKEN`.
   - Click en **Verify and Save**. Si todo está bien, te da check verde.
3. **Webhook fields** (suscribirse a):
   - `messages` ← esencial
4. Para Instagram, mismo procedimiento en **Instagram > Webhook**.

### Paso 7 — Probar el flujo real

Mandate un WhatsApp a vos mismo desde otro número:

```
"Hola, cuánto sale el farolito LED?"
```

El bot tendría que responder algo tipo:

```
Hola! Tenemos farolitos LED a $ 16.500 con stock disponible 🙂
¿Te interesa?
```

### Paso 8 — Monitoreo

Endpoint de métricas:

```bash
curl -s https://coronel-sur.onrender.com/api/bot/stats \
  -H "Authorization: Bearer $TOKEN"
```

Devuelve:
```json
{
  "sesiones_totales": 5,
  "mensajes_totales": 23,
  "mensajes_procesados": 12,
  "sesiones_por_canal": {"whatsapp": 4, "instagram": 1}
}
```

## Costos estimados

Con Claude Haiku 4.5 + prompt caching:
- **Primer mensaje de una conversación**: ~$0.002 (carga caché).
- **Siguientes mensajes** (cache hit): ~$0.0003 cada uno.
- **Un día con 100 mensajes**: ~$0.05.
- **Un mes con 3000 mensajes**: ~$1.5.

Si ves que Haiku responde mal, cambiá a Sonnet 4.6 (5x más caro pero
mucho más capaz).

## Reglas de privacidad que aplica el bot

Ver `backend/bot/productos.py` — el filtro es hardcoded y no cambia
por URL ni por ningún parámetro. Los campos que se exponen están en la
constante `CAMPOS_PUBLICOS`.

Si querés que muestre el stock numérico exacto (ahora muestra sólo
`disponible: true/false`), seteá `BOT_STOCK_FORMATO=numerico`.

## Troubleshooting

### El webhook devuelve 401 "Firma inválida"
Problema: `META_APP_SECRET` mal configurado. Meta firma cada POST con
HMAC-SHA256 y nuestra verificación rechaza si no matchea.

### El bot responde "Tuve un problema técnico"
Ver logs en Render. Casi seguro es `ANTHROPIC_API_KEY` no seteada o
límite de créditos en Anthropic.

### El bot responde con info equivocada sobre productos
Dos causas posibles:
1. El inventario cacheado en memoria está desactualizado — se refresca
   cada 5 minutos (`BOT_INVENTARIO_TTL_SEG=300`). Bajalo si querés.
2. El producto no está en la muestra del snapshot (150 productos más
   vendidos). Para mejorar, podemos exponerle al bot una herramienta
   de búsqueda en vivo — Fase 2.5 si hace falta.

### El bot responde muy lento (>10s)
1. Primera consulta después de reinicio: carga el inventario. Normal.
2. Si es consistente: cambiar a `BOT_MODEL=claude-haiku-4-5-20251001`
   (más rápido que Sonnet).

### Los audios de WhatsApp no se transcriben
Revisar que `OPENAI_API_KEY` esté seteada. Si no, el bot va a pedir al
cliente que escriba en texto — comportamiento aceptable.

## Qué NO hace todavía (y está pensado para fases siguientes)

- **No llama funciones/tools** (ej: "buscar_producto", "crear_pedido").
  Hoy sólo responde con la info del snapshot. Si se necesita, Fase 2.5.
- **No emite facturas ni presupuestos** desde el bot. Eso es Fase 3+,
  y requiere que el cliente confirme por otro canal.
- **No procesa pagos**. No toca Mercado Pago.
- **No cachea respuestas propias** (cada Claude request es fresh). No
  es problema al volumen actual.
- **No tiene rate limit propio** — depende del rate limit general
  (Fase 1). Un cliente que manda 100 mensajes/minuto genera gasto de
  Claude sin control. Para mitigar: poner un `Spending Limit` mensual
  en la consola de Anthropic.

---

## Rollback

El bot se puede desactivar rápido sin tocar código: en Render,
Environment, **borrá `ANTHROPIC_API_KEY`**. El router seguirá cargado
pero cada mensaje fallará con un error claro en los logs.

Para eliminarlo totalmente, comentá la línea `app.include_router(router_bot)`
en `backend/main.py` y redeployá. Las tablas quedan (no estorban).
