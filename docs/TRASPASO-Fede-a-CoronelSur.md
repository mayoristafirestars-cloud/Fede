# Documento de traspaso — de `Fede` a `Coronel-Sur`

**Para:** la sesión de Claude que trabaja el repo `mayoristafirestars-cloud/Coronel-Sur`.
**De:** la sesión que trabajó el repo `mayoristafirestars-cloud/Fede` (branch `claude/build-ai-agent-H9XwU`).
**Objetivo del dueño (Fede):** un solo **sistema del negocio** = *facturación + tienda + Eva sobre UNA base de datos* (la de facturación de Coronel-Sur). **Maxx** queda aparte como asistente personal.

Este documento describe TODO lo valioso construido en `Fede` para que lo integres a `Coronel-Sur`. El código real está en ese repo/branch; acá van las especificaciones, contratos de API, esquema de base y variables de entorno para que lo portes con precisión.

---

## 0. La idea clave que hace fácil el traspaso

**Eva ya está desacoplada del sistema de gestión por HTTP.** Eva son 2 procesos propios que hablan con el sistema SOLO por API REST (con un header `X-Token`):

- **Cerebro de Eva** — `vendedor_server.py` (FastAPI, puerto 8003). Usa la API de Claude, busca productos, arma pedidos, recalcula precios.
- **Puente oficial** — `eva_cloud_bridge.py` (FastAPI, puerto 8011). Webhook de WhatsApp Cloud API (Meta).

Eva NO lee la base directamente: le pega a `CORONEL_URL` (una variable de entorno). **Entonces, para conectar Eva a la base de Coronel-Sur, alcanza con:**

1. Que Coronel-Sur exponga los endpoints que Eva usa (listados abajo).
2. Que Coronel-Sur tenga las tablas nuevas (esquema abajo).
3. Apuntar `CORONEL_URL` de Eva al sistema Coronel-Sur.
4. Correr el sincronizador de inventario dentro de Coronel-Sur.

Los procesos de Eva (cerebro + puente) casi no cambian. **No hace falta reescribir Eva; hace falta que Coronel-Sur "hable su idioma".**

---

## 1. Eva oficial de Meta (WhatsApp Cloud API) — sin riesgo de ban

**Por qué importa:** el número no-oficial (whatsapp-web.js) hace que Meta pueda banear/suspender la cuenta. La versión oficial usa la Cloud API de Meta: número comercial verificado, cero riesgo de ban, gratis hasta ~1000 conversaciones/mes.

**Archivo:** `eva_cloud_bridge.py`. Puntos salientes ya implementados:
- **Webhook** `GET /webhook` (verifica `hub.verify_token`) y `POST /webhook`.
- **Validación de firma** HMAC `X-Hub-Signature-256` con el App Secret (`firma_valida`). **A prueba de fallas: rechaza si falta `WA_APP_SECRET`.**
- **Deduplicación** de mensajes reenviados por Meta (`OrderedDict`, últimos 500) → no responde/cobra dos veces.
- **Topes anti-abuso** con aviso al cliente ("mucha demanda", 1/hora) y alerta al dueño; nunca deja al cliente mudo.
- **Envío:** `enviar_texto`, `enviar_imagen` con **subida de media a Meta** (`subir_media`) para que las fotos lleguen siempre (Meta no puede leer los links de FactuPyme; el server las baja y las sube).
- **Audio:** `descargar_audio` + transcripción en el cerebro (faster-whisper).
- **Endpoint interno** `POST /notificar` (protegido por `X-Token`) para que el SISTEMA le pida a Eva mandar un WhatsApp (lo usa el webhook de pagos). Body: `{"a": "<numero>", "texto": "<mensaje>"}`.

**Variables de entorno (Meta):**
```
WA_TOKEN=            # token permanente de Meta (System User)
WA_PHONE_ID=         # Phone Number ID
WA_VERIFY_TOKEN=     # palabra secreta del webhook (la misma en Meta)
WA_APP_SECRET=       # App Secret de Meta (valida la firma del webhook)
VENDEDOR_HUMANO=     # número de Malcom (recibe los pedidos)
ALERTA_WHATSAPP=     # tu número (alertas y resumen)
AGENTE_TOKEN=        # token M2M compartido con el sistema (X-Token)
```

**Trámites de Meta ya hechos (no rehacer):** app de tipo Business, producto WhatsApp, número registrado y verificado, token permanente, webhook apuntado a `https://<dominio>/webhook` (ruteado a :8011 por Caddy), verificación de negocio en curso.

**Cómo portar:** el puente puede quedar tal cual. Solo asegurate de que `EVA_API` (dentro del puente) apunte al cerebro y que el cerebro tenga `CORONEL_URL` → Coronel-Sur.

---

## 2. Cerebro de Eva — anti-alucinación de precios

**Archivo:** `vendedor_server.py` (puerto 8003, endpoint `POST /api/vendedor` y `/api/vendedor/audio`).

**Lo importante que NO hay que perder:**
- **Precios recalculados en el servidor.** Cuando el modelo arma un pedido, `parsear_pedido()` + `_precio_real(codigo, tipo_cliente)` **recalculan cada precio desde el inventario real por código y lista** — nunca se confía en lo que "escribió" el modelo. (Evita que Eva facture un precio inventado.)
- **El costo/utilidad NUNCA llega al modelo.** El inventario público que ve Eva solo tiene Lista 1 y Lista 2; el costo se usa para calcular Lista 2 y se descarta.
- **Lista 2 (mayorista)** = `costo * (1 + Utilidad2/100)` (confirmado contra el reporte real de FactuPyme).
- **Fotos por código:** el modelo pide `FOTO: <código>` y el server resuelve la foto correcta (garantiza que la foto coincida con el producto).
- **Lock por número** (`_lock_sesion`): dos mensajes casi simultáneos del mismo cliente se procesan en orden y no corrompen el pareo `tool_use`/`tool_result` (que la API rechaza con 400).
- **Tools de Claude:** `buscar_producto`, `listar_categorias` (solo lectura — Eva no tiene tools de acción peligrosos).

**Registro al sistema (fire-and-forget, no bloquea):**
- `notificar_coronel(pedido)` → `POST {CORONEL_URL}/api/agente/pedido`. **Devuelve el número de pedido (`EVA-xxxxx`)**, que se usa como referencia del pago.
- `registrar_conversacion(...)` → `POST {CORONEL_URL}/api/agente/conversacion`.
- `registrar_busqueda(...)` → `POST {CORONEL_URL}/api/agente/busqueda` (inteligencia de demanda; ver §4).

**Variables:** `ANTHROPIC_API_KEY`, `CORONEL_URL`, `AGENTE_TOKEN`, `MODEL` (modelo de Claude), `MP_ACCESS_TOKEN` (para el link de pago; ver §3).

---

## 3. Pagos de Mercado Pago que cierran el pedido solos + enriquecen el CRM

**Por qué importa:** el cliente paga y el sistema se entera solo, marca el pedido **cobrado** y avisa. Además, cada pago **completa la ficha del cliente** con lo que trae MP (nombre, DNI, email) → el CRM crece solo con cada venta.

**Archivos:**
- `pagos.py` (lado Eva): `crear_link_pago(items, referencia)` crea la preferencia de Checkout Pro. Incluye `notification_url` (= `MP_NOTIF_URL`) y usa el **número de pedido como `external_reference`**.
- `coronel-sur/backend/routers/pagos.py` (**el webhook — portar entero**): `POST /api/pagos/webhook`.

**Flujo del webhook (clave de seguridad):**
1. MP notifica con el id del pago (varios formatos; `_extraer_payment_id` los cubre).
2. **Reconsulta el pago a MP** (`GET https://api.mercadopago.com/v1/payments/{id}` con `MP_ACCESS_TOKEN`) — **autoritativo**: un webhook falso no sirve.
3. Si `status == "approved"`: marca el comprobante (`origen='eva'`) como `cobrado`, **idempotente** por `pagos_mp.payment_id UNIQUE`.
4. **Enriquece el cliente** en el CRM: completa `dni`, `email`, `nombre` (solo lo que falta; no pisa datos cargados a mano) desde `pago.payer`.
5. **Avisa por WhatsApp** vía el puente (`POST http://127.0.0.1:8011/notificar` con `X-Token`): al dueño ("💰 pago acreditado, preparar") y al cliente ("recibimos tu pago ✅").

**Auth:** en `auth.py`, `/api/pagos/webhook` va en `ABIERTAS` (MP no puede autenticar; la seguridad está en reconsultar a MP).

**Variables:** `MP_ACCESS_TOKEN` (producción, `APP_USR-...`), `MP_NOTIF_URL` (default `https://coronelsur.com.ar/api/pagos/webhook`), `EVA_BRIDGE_URL` (`http://127.0.0.1:8011`), `AGENTE_TOKEN`.

> ⚠️ **Cumplimiento (del informe de riesgo):** validar la firma `x-signature` de MP además de reconsultar (defensa en profundidad). Y "facturación" legal requiere CAE de ARCA — no mostrar PDF de factura sin CAE.

---

## 4. Inteligencia de demanda — "qué comprar / qué reponer"

**Por qué importa:** cada búsqueda de producto de un cliente se registra. Las búsquedas **sin resultado** (piden y no tenés) o **sin stock** son un radar de qué comprar. Convierte a Eva de gasto en fuente de decisiones.

**Archivos:**
- `vendedor_server.py`: `registrar_busqueda()` enganchado dentro de `buscar_producto` (registra término + nº de resultados + si algún resultado tenía stock).
- `coronel-sur/backend/routers/agente.py`:
  - `POST /api/agente/busqueda` — registra (en `MAQUINA` de `auth.py`).
  - `GET /api/agente/demanda?dias=30` — devuelve `sin_resultado` (comprar), `sin_stock` (reponer), `mas_buscado`.
  - `resumen-diario` enriquecido con top "piden y no tengo" del día.
- `coronel-sur/frontend/templates/index.html`: sección **"🛒 Qué comprar"** en la pestaña Agente (`cargarDemanda()`).

---

## 5. Inventario de fuente única — tienda y Eva siempre iguales

**Por qué importa:** antes Eva leía el CSV en vivo (1230 productos) pero la tienda leía la tabla `productos` que solo se actualizaba a mano → mostraban precios/stock distintos.

**Archivo:** `coronel-sur/backend/sincronizador.py` (**portar entero**).
- Vuelca `negocio/inventario.csv` (export de FactuPyme) a la tabla `productos` con **la misma lógica de precios que Eva** (Lista 1 = Precio Venta; Lista 2 = `costo*(1+Utilidad2/100)`); upsert + baja lógica de faltantes.
- Se dispara en el arranque (`main.py` → `sincronizar()`) y, throttled, en cada request de la tienda (`tienda.py` → `sincronizar_si_cambio()`).
- Verificado: **1230 productos, 0 diferencias** de precio contra lo que cotiza Eva.

> El **parser de precios debe ser idéntico** entre Eva y el sincronizador (coma = miles). Es la garantía de que la web y Eva muestren lo mismo.

---

## 6. Robustez (arreglos de hoy — Fase 0)

- **Stock con dueño único (crítico):** `facturacion.py` **ya NO descuenta ni revierte stock**. Decisión del dueño: **FactuPyme es el único dueño del stock** (el CSV es la verdad); el sincronizador lo refleja. Antes, el sistema descontaba y el sync lo pisaba → números oscilaban. **Mantené este criterio en Coronel-Sur.**
- **Seguridad:** Coronel-Sur escucha solo en `127.0.0.1` (Caddy expone HTTPS); el webhook de Meta rechaza si falta `WA_APP_SECRET`.
- **`.gitignore`:** excluir `*.db` y backups (datos de clientes nunca al repo).

---

## 7. Esquema de base — tablas/columnas a agregar en Coronel-Sur

```sql
-- Inventario: columna Lista 2 (mayorista)
ALTER TABLE productos ADD COLUMN precio_mayorista REAL DEFAULT 0;

-- Conversaciones de Eva (si no existe)
CREATE TABLE IF NOT EXISTS conversaciones_eva (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session TEXT, telefono TEXT, mensaje TEXT, respuesta TEXT,
    es_audio INTEGER DEFAULT 0,
    creado_en TEXT DEFAULT (datetime('now','localtime'))
);

-- Búsquedas de Eva (inteligencia de demanda)
CREATE TABLE IF NOT EXISTS busquedas_eva (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    termino TEXT, termino_norm TEXT,
    resultados INTEGER DEFAULT 0, con_stock INTEGER DEFAULT 0,
    telefono TEXT,
    creado_en TEXT DEFAULT (datetime('now','localtime'))
);
CREATE INDEX IF NOT EXISTS idx_busq_norm ON busquedas_eva(termino_norm);
CREATE INDEX IF NOT EXISTS idx_busq_fecha ON busquedas_eva(creado_en);

-- Pagos de Mercado Pago (idempotencia del webhook)
CREATE TABLE IF NOT EXISTS pagos_mp (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_id TEXT UNIQUE, referencia TEXT,
    comprobante_id INTEGER REFERENCES comprobantes(id),
    monto REAL DEFAULT 0, estado TEXT,
    creado_en TEXT DEFAULT (datetime('now','localtime'))
);
```

Los pedidos de Eva se guardan como comprobantes con `origen='eva'` y número `EVA-xxxxx`; su estado se maneja con `activo | facturado | entregado | cancelado | cobrado`.

---

## 8. Contrato de los endpoints que Coronel-Sur debe exponer para Eva

Todos con header `X-Token: <AGENTE_TOKEN>` salvo el webhook de MP (abierto). Referencia: `coronel-sur/backend/routers/agente.py` y `routers/pagos.py` del repo `Fede`.

| Método | Ruta | Qué hace |
|---|---|---|
| POST | `/api/agente/pedido` | Crea presupuesto `EVA-xxxxx` desde un pedido de Eva. Devuelve `{numero}`. |
| POST | `/api/agente/conversacion` | Registra un intercambio cliente↔Eva. |
| POST | `/api/agente/busqueda` | Registra una búsqueda (demanda). |
| GET | `/api/agente/demanda?dias=30` | Reporte: piden-y-no-tengo / sin-stock / más-buscado. |
| GET | `/api/agente/pedidos` · `/conversaciones` · `/resumen-diario` | Vistas de la pestaña Agente. |
| POST | `/api/agente/pedido/{id}/estado` | Cambia estado del pedido. |
| POST | `/api/pagos/webhook` | Webhook de Mercado Pago (ver §3). |

Y el **puente de Eva** expone (para que el sistema le pida enviar WhatsApp):

| Método | Ruta | Body |
|---|---|---|
| POST | `/notificar` (en :8011, `X-Token`) | `{"a": "<numero>", "texto": "<mensaje>"}` |

---

## 9. Plan de integración sugerido (orden)

1. **Esquema:** agregar las tablas/columna de §7 al Coronel-Sur.
2. **Endpoints:** portar `routers/agente.py` (pedido/conversacion/busqueda/demanda/estado/resumen) y `routers/pagos.py` (webhook) desde `Fede`. Ajustar a los nombres de tabla de Coronel-Sur si difieren (mapear `comprobantes`, `clientes`, `productos`).
3. **Auth:** agregar `/api/agente/*` a rutas M2M (X-Token) y `/api/pagos/webhook` a rutas abiertas.
4. **Sincronizador:** portar `sincronizador.py`; llamarlo en el arranque y en la tienda.
5. **Frontend:** portar la sección "🛒 Qué comprar" (pestaña Agente) y los estados de pedido de Eva.
6. **Conectar Eva:** apuntar `CORONEL_URL` (cerebro de Eva) al Coronel-Sur, y `MP_NOTIF_URL` al dominio de Coronel-Sur.
7. **Un solo servicio de gestión:** dejar UNA sola app de gestión corriendo y UN solo Caddyfile (hoy `Fede` :8000 y `Coronel-Sur` :8010 se pisan; elegir Coronel-Sur y apagar/`mask` el otro para que no reviva).

---

## 10. Trampas conocidas (que ya nos pegaron)

- **`@lid` de WhatsApp:** WhatsApp ya no entrega el número, sino un ID interno `@lid`. Las listas de permitidos y la identificación de contactos deben comparar por dígitos del `@lid`, no por el número. (Ej. el dueño entra como `9152608919693@lid`.)
- **Ventana de 24 h de Meta:** un mensaje a Malcom/dueño puede rechazarse si él no escribió al número en 24 h. El pedido igual queda en el sistema.
- **Fotos:** Meta no puede leer los links de FactuPyme → hay que **subir el media a Meta** desde el server (ya implementado en `subir_media`).
- **Dos fuentes de inventario = divergencia.** Mantener el sincronizador como única vía.
- **SaaS multi-cliente (a futuro):** cada comercio necesita **su propia cuenta de WhatsApp aislada** (una WABA + número por cliente). Compartir número = un cliente que spamea banea a todos.

---

## 11. Dónde está el código real

Repo `mayoristafirestars-cloud/Fede`, branch `claude/build-ai-agent-H9XwU`. Commits relevantes (más nuevo primero):

- `8b42f6e` — Fase 0: stock dueño único + hardening + limpieza
- `b0162c9` — Eva cierra el pago con MP + enriquece CRM
- `b655652` — inteligencia de demanda
- `ce28a52` — inventario fuente única (sincronizador)
- `4b29a8d` — anti-ghosteo (fallback, topes, lock por sesión)
- `8f93414` — subida de fotos a Meta
- `7d0d614` — precios de pedidos server-side + seguridad del webhook

Archivos núcleo: `eva_cloud_bridge.py`, `vendedor_server.py`, `pagos.py`, `memoria.py`, y `coronel-sur/backend/{routers/agente.py, routers/pagos.py, routers/tienda.py, sincronizador.py, auth.py, main.py, db/schema.sql}`.
