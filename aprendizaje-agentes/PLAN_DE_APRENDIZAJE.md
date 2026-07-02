# 🤖 Plan de Aprendizaje: Programar Agentes de IA

**Para:** Fede
**Punto de partida:** Ya tenés un sistema en Python (FastAPI + SQLite, "Coronel Sur"), así que sabés lo básico de Python. Este plan arranca desde ahí.
**Meta final:** Construir un agente de IA que trabaje para tu negocio mayorista — que consulte tus ventas, responda preguntas sobre stock, y automatice tareas.

---

## ¿Qué es un agente? (la idea en 3 líneas)

Un **agente** es un modelo de IA (como Claude) metido dentro de un **bucle** (loop) y con acceso a **herramientas** (tools):

```
Agente = Modelo de IA + Bucle + Herramientas
```

1. Le das una tarea ("¿cuánto vendimos este mes?")
2. El modelo decide qué herramienta usar (ej: `consultar_ventas`)
3. Tu código ejecuta la herramienta y le devuelve el resultado
4. El modelo sigue pensando y usando herramientas hasta terminar
5. Te da la respuesta final

Eso es todo. Todo lo demás son detalles sobre cómo hacerlo bien.

---

## 📅 El plan: 6 fases (aprox. 6-8 semanas a ritmo tranquilo)

### ✅ Fase 0 — Preparación (1 día)

**Objetivo:** Tener todo instalado y funcionando.

1. Crear una cuenta en [platform.claude.com](https://platform.claude.com) y generar una **API key**
2. Cargar unos pocos dólares de crédito (con USD 5 te sobra para aprender)
3. Instalar el SDK de Python:
   ```bash
   pip install anthropic
   ```
4. Guardar la API key como variable de entorno (¡nunca en el código!):
   ```bash
   # Windows (PowerShell)
   setx ANTHROPIC_API_KEY "tu-clave-aqui"

   # Linux/Mac
   export ANTHROPIC_API_KEY="tu-clave-aqui"
   ```

**Checkpoint:** correr `ejemplos/01_primer_mensaje.py` y que responda.

---

### 📗 Fase 1 — Tu primera llamada a la API (semana 1)

**Objetivo:** Entender cómo hablarle a Claude desde Python.

Conceptos clave:
- **`messages.create()`** — la llamada básica: le mandás mensajes, te devuelve una respuesta
- **`model`** — qué modelo usar (ver tabla de modelos abajo)
- **`max_tokens`** — límite de largo de la respuesta
- **`system`** — el "prompt de sistema": las instrucciones permanentes que definen cómo se comporta ("Sos un asistente para un negocio mayorista argentino...")
- **Conversaciones multi-turno** — la API no tiene memoria: le mandás TODA la conversación en cada llamada

Ejercicios:
1. Correr `ejemplos/01_primer_mensaje.py` y modificar la pregunta
2. Agregarle un `system` prompt que lo haga hablar como argentino
3. Hacer un mini-chat en la terminal: un `while True` que lee tu input, lo agrega a la lista `messages`, llama a la API, imprime la respuesta y la agrega también a `messages`

**Checkpoint:** tenés un chat funcionando en la terminal que recuerda la conversación.

---

### 📘 Fase 2 — Herramientas (tool use): el corazón de los agentes (semanas 2-3)

**Objetivo:** Que Claude pueda EJECUTAR cosas, no solo hablar. Esta es LA fase más importante.

Conceptos clave:
- **Definir una herramienta** — nombre + descripción + esquema de parámetros (JSON Schema)
- **El bucle agéntico** — Claude pide usar una herramienta (`stop_reason == "tool_use"`), tu código la ejecuta, le devolvés el resultado (`tool_result`), y repetís hasta que Claude termina (`stop_reason == "end_turn"`)
- **El Tool Runner** — el SDK tiene un atajo (`@beta_tool` + `client.beta.messages.tool_runner()`) que maneja el bucle por vos

La versión con decorador (la más fácil):

```python
from anthropic import beta_tool
import anthropic

client = anthropic.Anthropic()

@beta_tool
def sumar(a: int, b: int) -> str:
    """Suma dos números enteros.

    Args:
        a: Primer número.
        b: Segundo número.
    """
    return str(a + b)

runner = client.beta.messages.tool_runner(
    model="claude-opus-4-8",
    max_tokens=1024,
    tools=[sumar],
    messages=[{"role": "user", "content": "¿Cuánto es 1234 + 5678?"}],
)
for mensaje in runner:
    print(mensaje)
```

Ejercicios:
1. Correr `ejemplos/02_agente_con_herramientas.py`
2. Escribir el bucle **a mano** una vez (sin tool runner) para entender qué pasa por dentro — está explicado en el ejemplo
3. Crear 2-3 herramientas propias: `obtener_fecha_hoy()`, `calcular_precio_con_iva(precio)`, `leer_archivo(ruta)`

**Checkpoint:** entendés el ciclo `tool_use → ejecutar → tool_result → repetir` y podés explicarlo con tus palabras.

---

### 📙 Fase 3 — Tu primer agente REAL: conectado a tu negocio (semanas 3-4)

**Objetivo:** Un agente que responde preguntas sobre TU base de datos (como la de Coronel Sur).

La idea: le das a Claude herramientas para consultar tu SQLite:
- `consultar_ventas(desde, hasta)` — total de ventas en un rango de fechas
- `buscar_producto(nombre)` — busca productos por nombre
- `stock_bajo(limite)` — productos con poco stock

Y le podés preguntar en lenguaje natural:
> "¿Cuáles fueron los 5 productos más vendidos el mes pasado?"
> "¿Qué productos tienen menos de 10 unidades de stock?"

Ejercicios:
1. Estudiar `ejemplos/03_agente_ventas.py` (ya viene armado con una base de datos de ejemplo)
2. Adaptarlo a tu base real de Coronel Sur (`coronel_sur.db`) — cambiar las consultas SQL a tus tablas (`productos`, `clientes`, `ventas_historicas`)
3. **Regla de oro de seguridad:** las herramientas ejecutan SQL que VOS escribiste con parámetros — nunca dejes que el modelo escriba SQL libre contra tu base de producción

**Checkpoint:** le preguntás a tu agente algo sobre tus ventas reales y te responde bien.

---

### 📕 Fase 4 — Hacerlo bien: los conceptos de calidad (semanas 4-5)

**Objetivo:** Pasar de "funciona" a "funciona bien y no gasta de más".

| Concepto | Qué es | Cuándo lo usás |
|---|---|---|
| **Streaming** | Ver la respuesta palabra por palabra en vez de esperar todo junto | Siempre que un humano esté mirando |
| **Structured outputs** | Forzar que la respuesta sea JSON válido con un esquema exacto (`client.messages.parse()` + Pydantic) | Cuando otro programa consume la respuesta |
| **Prompt caching** | Cachear el prefijo del prompt (system + tools) para pagar ~10% en llamadas repetidas | Agentes con system prompts largos |
| **Thinking adaptativo** | `thinking={"type": "adaptive"}` — Claude decide cuánto razonar | Tareas complejas |
| **Effort** | `output_config={"effort": "low/medium/high"}` — controla cuánto piensa/gasta | Para balancear costo vs calidad |
| **Manejo de errores** | `except anthropic.RateLimitError`, reintentos, `is_error=True` en tool results | Siempre en producción |

Ejercicios:
1. Agregar streaming a tu chat de la Fase 1 (`client.messages.stream()`)
2. Hacer que el agente de ventas devuelva un reporte como JSON estructurado con Pydantic
3. Agregar `cache_control` al system prompt y verificar en `response.usage.cache_read_input_tokens` que el cache funciona

**Checkpoint:** tu agente streamea, devuelve datos estructurados y cachea el prompt.

---

### 📓 Fase 5 — Temas avanzados (semanas 6+, a demanda)

Ya con la base sólida, elegí según lo que necesites:

- **Memoria entre sesiones** — que el agente recuerde cosas de conversaciones anteriores (memory tool: archivos en un directorio `/memories`)
- **Herramientas del servidor** — web search, code execution: Anthropic las ejecuta por vos, solo las declarás
- **MCP (Model Context Protocol)** — el estándar para conectar agentes a servicios externos (GitHub, Google Drive, etc.) sin escribir cada integración a mano
- **Managed Agents** — Anthropic corre el bucle Y el sandbox por vos: creás un "Agent" persistente y abrís "Sessions"; ideal para agentes que corren solos con cron (ej: "todos los lunes generá el reporte semanal de ventas")
- **Sub-agentes** — un agente coordinador que delega tareas a agentes especializados
- **Compaction / context editing** — para conversaciones larguísimas que superan la ventana de contexto

---

### 🏆 Proyecto final: "El asistente de Firestars"

Combiná todo en un agente para tu negocio:

1. **Herramientas de datos:** consultar ventas, stock, clientes desde tu SQLite
2. **Herramienta de reportes:** generar un resumen semanal (structured output → lo formateás lindo)
3. **Interfaz:** un endpoint nuevo en tu FastAPI (`POST /api/asistente`) que recibe la pregunta y devuelve la respuesta del agente — así lo integrás a la web que ya tenés
4. **Bonus:** programarlo para que corra solo cada lunes y te mande el reporte

---

## 💰 Modelos y costos (para que no te sorprenda la factura)

| Modelo | ID | Para qué | Costo (entrada/salida por millón de tokens) |
|---|---|---|---|
| Claude Opus 4.8 | `claude-opus-4-8` | El recomendado por defecto: el mejor para agentes | $5 / $25 |
| Claude Sonnet 5 | `claude-sonnet-5` | Alto volumen en producción, casi tan bueno | $3 / $15 |
| Claude Haiku 4.5 | `claude-haiku-4-5` | Tareas simples y rápidas (clasificar, extraer) | $1 / $5 |

Para aprender: una conversación típica cuesta centavos. Con USD 5 hacés cientos de pruebas.

**Tips para gastar menos:** usá `max_tokens` razonables, prompt caching para prompts largos, y `effort: "low"` para tareas simples.

---

## ⚠️ Errores típicos de principiante (para que no pierdas horas)

1. **Hardcodear la API key en el código** → usá siempre la variable de entorno `ANTHROPIC_API_KEY`
2. **Olvidarse de mandar el historial completo** → la API no tiene memoria; cada llamada lleva toda la conversación
3. **No devolver un `tool_result` por cada `tool_use`** → la API rechaza la llamada si falta uno (tienen que coincidir por `tool_use_id`)
4. **Descripciones vagas en las herramientas** → Claude decide qué herramienta usar leyendo la descripción; escribí CUÁNDO usarla, no solo qué hace
5. **Dejar que el modelo escriba SQL libre** → las herramientas ejecutan código TUYO con parámetros validados
6. **No chequear `stop_reason`** → siempre mirá por qué paró: `end_turn` (terminó), `tool_use` (quiere herramienta), `max_tokens` (se quedó corto)

---

## 📚 Recursos

- **Documentación oficial:** [platform.claude.com/docs](https://platform.claude.com/docs) — la guía de tool use es la lectura clave
- **SDK de Python:** [github.com/anthropics/anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python) — la carpeta `examples/` tiene código listo
- **Claude Code:** lo que estás usando ahora mismo — pedile que te explique cualquier concepto de este plan, que revise tu código, o que programe con vos

## 🗂️ Los ejemplos de este repo

| Archivo | Fase | Qué hace |
|---|---|---|
| `ejemplos/01_primer_mensaje.py` | 1 | Tu primera llamada a la API + mini chat |
| `ejemplos/02_agente_con_herramientas.py` | 2 | El bucle agéntico explicado paso a paso |
| `ejemplos/03_agente_ventas.py` | 3 | Agente conectado a una base SQLite como la tuya |

Para correrlos:
```bash
pip install anthropic
python ejemplos/01_primer_mensaje.py
```

---

**Consejo final:** no leas todo y después programes — programá desde el día 1. El bucle de aprender agentes es igual al de los agentes: probar → ver el error → corregir → repetir. 🚀
