# Chatbot multicanal (WhatsApp + Instagram)

Asistente automático para responder a clientes en **WhatsApp** e **Instagram**,
con precios cargados desde una planilla de **Google Sheets** en tu Drive y
transcripción de **audios** (Whisper).

Stack:

- **FastAPI** + Uvicorn como servidor de webhooks.
- **Meta Cloud API** (WhatsApp Business + Instagram Messaging) para mandar y
  recibir mensajes.
- **Anthropic Claude** como cerebro de las respuestas (con *prompt caching* de
  la planilla, así no se paga la lista entera en cada turno).
- **OpenAI Whisper** sólo para transcribir audios → texto.
- **gspread** para leer la planilla de Google Sheets.
- **SQLite** local para guardar el historial de conversación e idempotencia.

## Estructura

```
chatbot/
├── app/
│   ├── main.py              ← FastAPI + endpoints / y /health
│   ├── config.py            ← variables de entorno
│   ├── models.py            ← IncomingMessage normalizado
│   ├── core/handler.py      ← orquesta: recibir → transcribir → IA → enviar
│   ├── webhooks/
│   │   ├── whatsapp.py      ← GET verify + POST recibir
│   │   └── instagram.py     ← GET verify + POST recibir
│   └── services/
│       ├── meta_api.py      ← enviar WA/IG, descargar media
│       ├── sheets.py        ← leer planilla con caché
│       ├── transcribe.py    ← audio → texto (Whisper)
│       ├── claude.py        ← genera la respuesta (Anthropic)
│       └── conversation.py  ← historial + idempotencia (SQLite)
├── data/                    ← SQLite local (se crea solo)
├── requirements.txt
├── render.yaml              ← deploy en Render
└── .env.example
```

## Variables de entorno

Copiá `.env.example` a `.env` y completá los valores. Resumen rápido:

| Variable | Para qué sirve |
| --- | --- |
| `META_ACCESS_TOKEN` | Token de la app de Meta (WhatsApp + Instagram). |
| `META_VERIFY_TOKEN` | String que vos inventás para el handshake del webhook. |
| `META_APP_SECRET` | App Secret de la app de Meta. |
| `WHATSAPP_PHONE_NUMBER_ID` | ID del número de WhatsApp Business. |
| `INSTAGRAM_ACCOUNT_ID` | ID de la cuenta profesional de Instagram. |
| `ANTHROPIC_API_KEY` | API key de Claude. |
| `CLAUDE_MODEL` | Modelo (default `claude-sonnet-4-5`). |
| `OPENAI_API_KEY` | API key de OpenAI (sólo para Whisper). |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | JSON entero de la service account. |
| `GOOGLE_SHEET_ID` | ID del Sheet (lo sacás de la URL). |
| `GOOGLE_SHEET_TAB` | Nombre de la pestaña con los precios. |
| `BUSINESS_NAME` | Cómo se llama tu negocio (lo usa Claude). |

## Setup paso a paso

### 1. Cuenta de Meta para WhatsApp + Instagram

1. Entrá a <https://developers.facebook.com>, creá una **App** tipo *Business*.
2. Agregá los productos **WhatsApp** y **Messenger** (este último es el que
   maneja Instagram DMs).
3. En **WhatsApp → API Setup**:
   - Anotá el **Phone Number ID** → `WHATSAPP_PHONE_NUMBER_ID`.
   - Generá un **Permanent Access Token** (con un *system user* en Business
     Manager) → `META_ACCESS_TOKEN`.
4. En **App settings → Basic** copiá **App Secret** → `META_APP_SECRET`.
5. En **Instagram → API Setup**: conectá tu cuenta profesional de IG con la
   página de Facebook. Anotá el **IG User ID** → `INSTAGRAM_ACCOUNT_ID`.
6. Configurá los webhooks (después de desplegar el servidor):
   - **WhatsApp** → URL: `https://TU-DOMINIO/webhook/whatsapp`,
     verify token: el mismo que pongas en `META_VERIFY_TOKEN`,
     suscribite a `messages`.
   - **Instagram** → URL: `https://TU-DOMINIO/webhook/instagram`,
     mismo verify token, suscribite a `messages`.

### 2. Anthropic (Claude)

1. <https://console.anthropic.com> → crear API key → `ANTHROPIC_API_KEY`.
2. Cargá saldo. Una conversación promedio (planilla cacheada) cuesta unos
   centavos.

### 3. OpenAI (sólo Whisper)

1. <https://platform.openai.com> → API key → `OPENAI_API_KEY`.
2. Whisper cuesta ~ USD 0,006 por minuto de audio.

### 4. Google Sheets (planilla de inventario)

#### 4.a. Subir el inventario de FactuPyme a Drive

El bot espera el formato exacto de exportación de FactuPyme
(`Inventario_Articulos_*.csv`), que tiene estas columnas:

```
Codigo | Descripción | Cod SubRubro | SubRubro | Cod Rubro | Rubro |
Cod Marca | Marca | Cod Provedor | Proveedor | Temporada |
Fecha Alta | Fecha Modif | Precio Costo | Precio Venta |
Utilidad 1 | Utilidad 2 | Cantidad | Stock Min | Vencimiento |
Reponer | imagenes
```

Pasos (flujo recomendado, se usa un archivo permanente tipo
`Base Bot Coronel Sur`):

1. Creá una vez un Google Sheet en Drive llamado **`Base Bot Coronel Sur`**
   (o como quieras). Ese ID es el que va en `GOOGLE_SHEET_ID` y no cambia
   nunca.
2. Cada vez que actualizás precios:
   - Exportá el CSV desde FactuPyme.
   - Abrí `Base Bot Coronel Sur` en Drive.
   - **Importá** el CSV (Archivo → Importar → Subir → Reemplazar hoja
     actual, o "Reemplazar datos en la celda seleccionada").
   - O, más simple: borrá la pestaña vieja y arrastrá el nuevo CSV dentro
     del mismo Sheet.
3. La pestaña va a quedar con un nombre tipo
   `Inventario_Articulos_2026-04-16.csv` (FactuPyme le pone la fecha).
   **No hay que renombrarla** — el bot por defecto lee la **primera
   pestaña**, así que funciona igual.
4. Si preferís fijar un nombre de pestaña específico, poné ese nombre en
   `GOOGLE_SHEET_TAB`. Si el nombre configurado no existe, el bot igual
   cae a la primera pestaña y loguea un warning.
5. Verificá que la primera fila sean los encabezados originales tal cual
   los exporta FactuPyme. NO los renombres ni traduzcas.

#### 4.b. Qué ve y qué NO ve el cliente

El bot **filtra antes de mandarle nada a Claude**. Por defecto, sólo
expone estas columnas (vía `SHEET_PUBLIC_COLUMNS` en `.env`):

```
Codigo, Descripción, Rubro, SubRubro, Marca, Proveedor, Precio Venta, Cantidad
```

Las siguientes quedan **ocultas** (Claude nunca las recibe):

```
Precio Costo, Utilidad 1, Utilidad 2, Stock Min, Cod Provedor,
Cod Marca, Cod Rubro, Cod SubRubro, Fecha Alta, Fecha Modif,
Vencimiento, Reponer, Temporada, imagenes
```

Si querés cambiar la lista, editá `SHEET_PUBLIC_COLUMNS` con las
columnas separadas por coma. Vacío = todas (NO recomendado).

#### 4.c. Service account de Google Cloud

1. Andá a <https://console.cloud.google.com>:
   - Creá un proyecto.
   - Habilitá **Google Sheets API** y **Google Drive API**.
   - Creá una **Service Account** y descargá la *key* en JSON.
2. Pegá **el contenido entero** del JSON en la variable
   `GOOGLE_SERVICE_ACCOUNT_JSON` (en una sola línea, escapando comillas si lo
   ponés en un `.env`). Alternativa: subí el archivo y poné la ruta en
   `GOOGLE_SERVICE_ACCOUNT_FILE`.
3. **MUY IMPORTANTE**: andá al Sheet y **compartilo con el email de la service
   account** (algo como `chatbot@tu-proyecto.iam.gserviceaccount.com`) con
   permiso de **Lector**.
4. Copiá el ID del Sheet de la URL (`/d/AQUI_VA_EL_ID/edit`) →
   `GOOGLE_SHEET_ID`.

#### 4.d. Refrescar después de actualizar precios

Cuando exportes un nuevo CSV de FactuPyme, lo reemplazás en Drive y el
bot lo lee solo en hasta `SHEET_CACHE_SECONDS` segundos (5 min por
defecto). Para forzar refresco inmediato podés reiniciar el servicio
en Render.

## Correr en local

```bash
cd chatbot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # editá los valores
uvicorn app.main:app --reload --port 8000
```

Verificá:

```bash
curl http://localhost:8000/health
```

Para que Meta pueda llegar a tu local, exponé el puerto con **ngrok**:

```bash
ngrok http 8000
```

Y usá la URL `https://...ngrok.io/webhook/whatsapp` en el panel de Meta.

## Deploy en Render

El `render.yaml` ya está listo. Pasos:

1. Subí el repo a GitHub.
2. En <https://render.com> → **New → Blueprint** → seleccioná el repo.
3. Render detecta `chatbot/render.yaml`.
4. En **Environment** del servicio, cargá todas las variables del `.env`.
5. Tomá la URL pública (ej: `https://chatbot-multicanal.onrender.com`) y
   ponela en los webhooks de Meta:
   - `https://...onrender.com/webhook/whatsapp`
   - `https://...onrender.com/webhook/instagram`

## Cómo funciona internamente

```
WhatsApp/IG  ──POST──▶  /webhook/{wa,ig}
                              │
                              ▼
                    parse → IncomingMessage
                              │
                              ▼
                        core/handler.py
                              │
                  ┌───────────┼───────────┐
                  ▼           ▼           ▼
             si es audio  historial    planilla
             → Whisper    (SQLite)     (Sheets,
                                        cacheada)
                  │           │           │
                  └─────► Claude ◄────────┘
                              │
                              ▼
                       respuesta texto
                              │
                              ▼
                  meta_api.send_{wa,ig}_text
```

- La planilla se cachea en memoria por `SHEET_CACHE_SECONDS` (default 5 min).
  Si modificás un precio en el Sheet, en ≤ 5 min ya responde con el nuevo.
- El system prompt + planilla van marcados con `cache_control` de Anthropic,
  así pagás los tokens de la lista una sola vez cada 5 minutos.
- Cada `message_id` se guarda en `processed` para no contestar dos veces si
  Meta reenvía el webhook.

## Próximos pasos (a pedido)

- Validar firma `X-Hub-Signature-256` con `META_APP_SECRET` para rechazar
  webhooks falsos.
- Botones / quick replies para acelerar pedidos comunes.
- Integrar con la base de Coronel Sur para registrar pedidos directamente.
- Handoff a humano (palabra clave "agente" → silenciar al bot N horas).
