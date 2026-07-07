# Agentes de IA

Dos agentes construidos con Python y la API de Claude (Anthropic):

| Agente | Archivo | Qué hace |
|---|---|---|
| **Sofi** | `agente.py` + `server.py` | Soporte al cliente para e-commerce (demo: tienda Trama). Widget web flotante, memoria, FAQs, catálogo, tools de pedidos/stock. |
| **Max** | `asistente.py` | Asistente ejecutivo personal. Investiga en internet, compara opciones, arma rankings y redacta mensajes de contacto/negociación. |

## Setup

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Crear tu archivo de credenciales:
   ```bash
   cp .env.example .env
   ```

3. Editar `.env` y pegar tu API key de Anthropic (https://console.anthropic.com).

4. Para Max: habilitar la búsqueda web en
   https://console.anthropic.com/settings/privacy → "Permitir búsqueda web".

## Correr

**Max (asistente personal, por consola):**
```bash
python3 asistente.py
```

**Sofi (bot de soporte, consola):**
```bash
python3 agente.py
```

**Sofi (widget web):**
```bash
uvicorn server:app --reload --port 8000
# abrir http://localhost:8000
```

## Estructura

- `asistente.py` — Max: agente personal con búsqueda web (server-side de Anthropic)
- `agente.py` — Sofi: agente de soporte con memoria + tools
- `server.py` — API HTTP (FastAPI) + widget web para Sofi
- `static/index.html` — widget de chat flotante tipo Intercom
- `prompts/` — personalidades de los agentes
- `data/` — base de conocimiento de Sofi (FAQs, catálogo)
- `tools/db.py` — datos simulados de pedidos y stock (reemplazar por API real)
- `.env` — credenciales (NUNCA se sube a git)

## Pendientes

- Integración de WhatsApp vía Twilio (webhook)
- Deploy a VPS para correr 24/7
