# 🗂️ Ficha Técnica — Ecosistema Dist Coronel Sur

## 1. Servidor (infraestructura)

| Campo | Valor |
|---|---|
| Tipo | VPS Cloud (servidor virtual privado) |
| Proveedor | Hetzner Cloud |
| Modelo | CX23 (Shared vCPU, línea Intel/AMD x86) |
| CPU | 2 vCPU x86 |
| RAM | 4 GB |
| Disco | 40 GB SSD |
| Sistema operativo | Ubuntu 26.04 (Linux) |
| Ubicación | Nuremberg, Alemania |
| IP pública | 167.235.140.223 |
| Acceso | SSH (usuario root) |
| Costo | ~US$7/mes |

## 2. Stack tecnológico

| Capa | Tecnología |
|---|---|
| Lenguajes | Python 3.14 + Node.js 20 |
| Framework web/API | FastAPI + Uvicorn (Python) |
| WhatsApp (no oficial) | whatsapp-web.js (Node) + Chromium headless |
| IA / LLM | Claude API (Anthropic) — modelo claude-sonnet-4-6 |
| Transcripción de audio | faster-whisper (local, en el servidor) |
| Búsqueda web (Max) | Web search server-side de Anthropic |
| Base de datos | SQLite (modo WAL) |
| Proceso/arranque | systemd (servicios con auto-reinicio) |
| Entorno Python | virtualenv en /opt/fede/venv |
| Código | /opt/fede (repo git) |

## 3. Servicios corriendo (systemd) y puertos

| Servicio | Qué es | Puerto | Acceso |
|---|---|---|---|
| `eva-server` | Cerebro de Eva (vendedora) | 8003 | interno (127.0.0.1) |
| `eva-bridge` | WhatsApp de Eva | — | conexión saliente |
| `max-server` | Cerebro de Max (asistente personal) | 8002 | interno |
| `max-bridge` | WhatsApp de Max | — | conexión saliente |
| `coronel-sur` | Sistema de gestión (web) | 8000 | **público** (http://167.235.140.223:8000) |
| `vigilante` | Watchdog: vigila y alerta si algo cae | — | interno |

## 4. Flujo del sistema (arquitectura multi-agente)

### Flujo de un cliente comprando (Eva)
```
Cliente (WhatsApp)
   │  mensaje de texto o audio
   ▼
eva-bridge (Node / whatsapp-web.js)      ← límites anti-abuso, resuelve teléfono real
   │  HTTP POST /api/vendedor  (o /audio → transcribe con Whisper)
   ▼
eva-server (Python / FastAPI, puerto 8003)
   │  - carga inventario (negocio/inventario.csv, 1230 productos, 2 listas de precios)
   │  - arma el prompt (personalidad + info negocio) con prompt caching
   ▼
Claude API (Anthropic)                    ← razona, usa tools: buscar_producto / listar_categorias
   │  respuesta (texto + marcadores FOTO + posible PEDIDO_CONFIRMADO)
   ▼
eva-server: arma la secuencia (producto → su foto → producto → foto → alternativas)
   │
   ├─► eva-bridge → envía al cliente (texto e imágenes intercaladas)
   │
   └─► si hay PEDIDO_CONFIRMADO:
          ├─► WhatsApp a Malcom (vendedor humano)
          └─► HTTP a coronel-sur /api/agente/pedido → crea PRESUPUESTO + cliente en el CRM
```

### Flujo del asistente personal (Max)
```
Fede (WhatsApp)  →  max-bridge (Node)  →  max-server (Python 8002)
   →  Claude API + búsqueda web  →  investiga/compara  →  respuesta a Fede
```

### Sistema de gestión (Coronel Sur)
```
Navegador  →  http://167.235.140.223:8000  →  login (cookie firmada)
   →  coronel-sur (FastAPI 8000)  →  SQLite
   Módulos: Facturación · CRM (4180 clientes) · Inventario · Reportes · Agente (pedidos de Eva) · Tienda online
```

### Vigilancia (watchdog)
```
vigilante  →  cada 60s chequea: eva-server, max-server, coronel-sur (HTTP /health)
                              + eva-bridge, max-bridge (archivos de latido .alive)
   →  si algo cae/vuelve → alerta por WhatsApp al dueño (via el bridge vivo)
```

## 5. Datos y persistencia

| Dato | Dónde |
|---|---|
| Inventario (2 listas de precios) | /opt/fede/negocio/inventario.csv (export de FactuPyme) |
| Info del negocio (horarios, envíos, etc.) | /opt/fede/negocio/info.md |
| Ajustes por producto (bulto, grabable) | /opt/fede/negocio/productos_extra.csv |
| Base del sistema (facturas, CRM, pedidos) | /opt/fede/coronel-sur/backend/db/coronel_sur.db |
| Backups automáticos (14 días) | /opt/fede/coronel-sur/backend/db/backups/ |
| Sesiones de conversación (memoria) | /opt/fede/sesiones_eva.json, sesiones_max.json |
| Credenciales/config | /opt/fede/.env (API key, tokens, límites) |
| Sesión WhatsApp (para no re-escanear QR) | /opt/fede/*/.wwebjs_auth/ |

## 6. Integraciones externas

| Servicio | Uso | Estado |
|---|---|---|
| Anthropic (Claude API) | Cerebro de Eva y Max | ✅ activo |
| WhatsApp (no oficial, whatsapp-web.js) | Canal de Eva y Max | ✅ activo |
| FactuPyme | Origen del inventario (export CSV manual) | ✅ activo |
| Mercado Pago | Link de pago en pedidos | ⚙️ opcional (falta MP_ACCESS_TOKEN) |
| WhatsApp Cloud API (Meta oficial) | Migración futura de Eva | ⚙️ preparado, sin activar |
| Caddy (HTTPS) | Candadito verde con dominio | ⚙️ opcional (falta dominio) |
