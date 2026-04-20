# Stack Técnico — Pipeline de Agentes SEO

> Derivada de: [Empresa 01 — Agencia de Contenido SEO](./README.md)
> Objetivo: especificación técnica para construir el pipeline de 6 agentes + humano.

---

## Arquitectura general

```
                    ┌─────────────────────────────────────┐
                    │  Orquestador (Claude Agent SDK)     │
                    │  - Estado del post (JSON en Airtable)│
                    │  - Retries, fallbacks, logs          │
                    └─────────────────────────────────────┘
                                    │
   ┌────────────┬────────────┬──────┴──────┬─────────────┬────────────┐
   ▼            ▼            ▼             ▼             ▼            ▼
[1 KW Res] [2 Outline] [3 Drafter] [4 Fact-Check] [5 SEO Opt] [6 Publisher]
   │            │            │             │             │            │
   └── DataForSEO└── Claude Opus└── Claude Son.└── Web Search└── Claude Son.└── CMS API
```

### Principios de diseño

1. **Cada agente es reemplazable**: contrato I/O estable (JSON), lógica interna puede cambiar.
2. **Estado persistente entre pasos**: Airtable guarda el post completo con todos los campos que van acumulando los agentes.
3. **Failover humano**: si un agente falla 2 veces, se escala al editor.
4. **Tracing obligatorio**: cada llamada LLM se loggea (tokens, costo, latencia, output) a un bucket.
5. **Prompts versionados**: `v1.0`, `v1.1`... en un repo, para poder hacer rollback.

---

## Stack base

| Capa | Herramienta | Razón |
|------|-------------|-------|
| Orquestación | Claude Agent SDK (sub-agentes) | Paraleliza, maneja contexto, built-in tool use |
| Modelo principal | Claude Sonnet 4.6 | Balance costo/calidad para drafting |
| Modelo crítico | Claude Opus 4.7 | Outlines y fact-checking donde calidad > costo |
| Modelo barato | Claude Haiku 4.5 | Clasificación, dedup, tareas simples |
| Estado | Airtable | UI lista para operar + API buena |
| Keyword/SERP | DataForSEO | US$ 0.003-0.05 por query, cubre todo |
| Web search | Brave Search API o Exa | Para fact-checking |
| CMS | WordPress REST / Webflow / HubSpot / Ghost | Depende del cliente |
| Tracking | Google Search Console API | Gratis, datos oficiales |
| Logs/observability | Helicone o Langfuse | Monitoreo LLM calls |
| Infra | Railway o Fly.io | Deploy del orquestador |

---

## Agente 1 — Keyword Researcher

**Propósito**: dado un tema o página semilla, producir un cluster de keywords con intención, volumen y dificultad.

### I/O

**Input**:
```json
{
  "client_id": "acme-saas",
  "domain": "acme.com",
  "seed_topic": "customer onboarding automation",
  "target_audience": "SaaS CSMs",
  "existing_posts": ["url1", "url2"]
}
```

**Output**:
```json
{
  "cluster_name": "customer onboarding automation",
  "primary_kw": "customer onboarding software",
  "secondary_kws": [
    {"kw": "saas onboarding checklist", "vol": 720, "kd": 22, "intent": "informational"},
    ...
  ],
  "paa_questions": ["How long should SaaS onboarding take?", ...],
  "competitor_urls": ["competitor1.com/blog/...", ...],
  "content_gap_notes": "Competitors miss enterprise segment"
}
```

### Herramientas que usa

- `dataforseo.keyword_suggestions(seed)` → lista de 50-200 keywords
- `dataforseo.serp(kw)` → top 10 resultados + PAA + featured snippets
- `dataforseo.keyword_difficulty(kw)`

### Prompt (esqueleto)

```
Sos un SEO strategist. Dado un seed topic y un dominio cliente, tu tarea es:

1. Expandir a 50 keywords relevantes usando dataforseo.keyword_suggestions
2. Para cada keyword: obtener volumen, KD, intención, PAA
3. Filtrar:
   - Eliminar las que el cliente ya cubrió (revisar existing_posts)
   - Priorizar KD < 40 si dominio es joven (DR < 30)
   - Agrupar por intención de búsqueda (informational / commercial / transactional)
4. Elegir 1 primary (volumen > 300, KD viable) y 5-10 secondary

Output: JSON con schema exacto del contrato.
```

### Modelo y costo

- **Modelo**: Claude Sonnet 4.6
- **Tokens estimados**: 8-15k entrada / 3-5k salida
- **Costo LLM**: ~US$ 0.05-0.10
- **Costo APIs externas**: ~US$ 0.30 (DataForSEO)

### Criterio de éxito

- ≥ 80% de keywords en output tienen volumen real > 100/mes (verificable)
- Primary KW tiene al menos 1 PAA identificado
- Zero duplicados con posts existentes del cliente

---

## Agente 2 — Outline Writer

**Propósito**: dado un cluster de keywords, diseñar la estructura del artículo (H2/H3) optimizada para rankear.

### I/O

**Input**: output del Agente 1 + `target_word_count`, `tone_guide`.

**Output**:
```json
{
  "title": "The SaaS Customer Onboarding Checklist (2026 Edition)",
  "meta_description": "...",
  "outline": [
    {
      "h2": "Why onboarding makes or breaks retention",
      "word_target": 250,
      "key_points": ["retention stat", "cost of bad onboarding"],
      "entities": ["Gainsight", "Totango"],
      "internal_link_opportunity": "/blog/retention-metrics"
    },
    ...
  ],
  "faq_block": [{"q": "...", "a_outline": "..."}],
  "estimated_total_words": 2400
}
```

### Herramientas

- Scraping de top 3 SERP results (via DataForSEO o Playwright headless)
- `claude.analyze(competitor_outlines)` para encontrar gaps

### Prompt (esqueleto)

```
Sos un editor SEO senior. Vas a diseñar un outline que combine:

1. Cobertura exhaustiva del cluster de keywords (primary + todas las secondary)
2. Mejor estructura que los top 3 competidores (te los paso)
3. Preguntas PAA como H3 o FAQ
4. Sugerencias de entidades (empresas, herramientas, expertos) para EEAT
5. Internal links al catálogo del cliente (te paso lista)

Reglas:
- Title ≤ 60 chars, incluir primary KW
- Meta description ≤ 155 chars, CTR-friendly
- H2 count: 5-9 para posts de 2000-3000 palabras
- Cada H2 debe tener un word_target que sume al total
```

### Modelo

- **Modelo**: Claude **Opus 4.7** (calidad > costo acá, es la decisión estructural)
- **Tokens**: 15-25k entrada (incluye competitor content) / 2-4k salida
- **Costo**: ~US$ 0.40-0.60

---

## Agente 3 — Drafter

**Propósito**: escribir el borrador completo siguiendo el outline, el tono del cliente y el brand voice.

### I/O

**Input**: outline del Agente 2 + `brand_voice_profile` del cliente + ejemplos de posts anteriores aprobados.

**Output**: Markdown con frontmatter completo listo para publicar.

```markdown
---
title: "..."
slug: "..."
meta_description: "..."
tags: [...]
cover_image_prompt: "..."
---

# H1

## H2
...
```

### Prompt (esqueleto)

```
Sos un writer técnico B2B. Vas a escribir el post completo siguiendo:

1. El outline EXACTO (no agregues ni saques H2)
2. El brand voice del cliente (te paso 3 ejemplos de posts anteriores)
3. Word count por sección (desviación máx. 15%)
4. Densidad KW: primary 3-5 veces naturalmente, secondary 1-2 veces cada una
5. Nunca alucinar datos: si necesitás un stat y no lo tenés, escribí [STAT_NEEDED: descripción]
   para que el Fact-Checker lo llene
6. Estilo:
   - Oraciones cortas y activas
   - 1-2 ejemplos concretos por H2
   - Código/ejemplos cuando el tema lo pida
   - Cero palabras vacías tipo "in today's fast-paced world"
```

### Modelo y costo

- **Modelo**: Claude Sonnet 4.6
- **Tokens**: 10-15k entrada / 6-10k salida
- **Costo**: ~US$ 0.30-0.50

### Criterio de éxito

- Word count dentro de ±10% del target
- Zero placeholders sin resolver al salir del pipeline
- Legibilidad Flesch ≥ 50

---

## Agente 4 — Fact-Checker

**Propósito**: resolver placeholders `[STAT_NEEDED: ...]`, validar todas las afirmaciones numéricas/fácticas, agregar citas con fuentes reales.

### I/O

**Input**: Markdown del Agente 3.

**Output**: Markdown con:
- Todos los `[STAT_NEEDED]` resueltos o removidos
- Links inline a fuentes (Nielsen, Gartner, McKinsey, reportes oficiales)
- Una sección final `<!-- sources -->` con lista completa
- Campo `fact_check_confidence`: 0-1

### Herramientas

- Brave Search / Exa para buscar sources
- Validador de URL (que devuelva 200)
- Opcional: Wikipedia API para entidades

### Prompt (esqueleto)

```
Sos un fact-checker periodístico. Recibís un borrador con placeholders y afirmaciones.

Para cada [STAT_NEEDED] y cada afirmación numérica:
1. Buscar en fuentes primarias (reportes oficiales, papers, empresas mencionadas)
2. Si encontrás stat → insertar con link a la fuente
3. Si NO encontrás → reescribir la oración para que no dependa del dato
4. NUNCA inventar. Mejor oración más débil que dato falso.

Para cada entidad mencionada (empresa, persona, producto):
- Validar que existe y el nombre está escrito correctamente
- Si la info del contexto está desactualizada → actualizar con search

Output: Markdown limpio + confidence score + lista de fuentes consultadas.
```

### Modelo

- **Modelo**: Claude **Opus 4.7** (acá no podés fallar)
- **Tokens**: 15-20k entrada (draft + search results) / 6-10k salida
- **Costo**: ~US$ 0.50-0.80
- **Nota**: el costo justifica usar Opus — un error factual publicado mata la reputación.

---

## Agente 5 — SEO Optimizer

**Propósito**: pulido final on-page. No toca el contenido sustantivo, solo elementos SEO.

### I/O

**Input**: Markdown del Agente 4.

**Output**: mismo Markdown + campos nuevos en frontmatter:
```yaml
schema_type: "Article"
schema_json: "..."
internal_links_added: ["/blog/post-1", "/blog/post-2"]
external_links_validated: true
image_alt_texts: [...]
reading_time_min: 9
```

### Tareas concretas

1. **Meta tags**: validar que title y description estén optimizados
2. **Schema.org**: generar JSON-LD para `Article` o `HowTo` según corresponda
3. **Internal links**: insertar 3-5 links a posts existentes del cliente (recibe lista)
4. **External links**: validar que todos sean live + nofollow donde corresponda
5. **Alt text**: generar para cada imagen sugerida
6. **Table of contents**: si post > 1500 palabras
7. **CTA al final**: según el stage del funnel del post

### Modelo

- **Modelo**: Claude Sonnet 4.6
- **Tokens**: 10-15k / 2-4k
- **Costo**: ~US$ 0.15-0.25

---

## Agente 6 — Publisher

**Propósito**: tomar el post final ya editado por humano y publicarlo al CMS del cliente.

### I/O

**Input**:
```json
{
  "client_id": "acme-saas",
  "post_md": "...",
  "frontmatter": {...},
  "publish_mode": "draft" | "scheduled" | "publish_now",
  "scheduled_at": "2026-04-25T10:00:00Z"
}
```

**Output**:
```json
{
  "status": "success",
  "cms_url": "https://acme.com/blog/customer-onboarding-software",
  "cms_post_id": "1234",
  "published_at": "..."
}
```

### Implementación por CMS

| CMS | Método | Notas |
|-----|--------|-------|
| WordPress | REST API `/wp-json/wp/v2/posts` | App password auth, el más común |
| Webflow | CMS API v2 | Paga plan CMS, schemas custom por cliente |
| HubSpot | Blog Posts API | OAuth, rate limits manejables |
| Ghost | Admin API | JWT auth, muy limpio |

### No es un agente LLM

Es un módulo determinístico (Python con `requests` o similar). Cero riesgo de alucinación.

### Criterio de éxito

- Publica como draft por default (safer)
- Retry automático 3 veces con backoff
- Notifica a Slack cuando publica (con link)

---

## Layer humano (estratega/editor)

Entre Agente 5 y Agente 6 va el humano. SLA: **15 minutos por post**.

### Checklist del editor

1. Leer intro y conclusión (¿convence?)
2. Spot-check de 2 claims factuales (¿las fuentes existen?)
3. Verificar tono vs cliente
4. Aprobar title y meta
5. Click "Publish" → dispara Agente 6

### UI del editor

Airtable vista custom:
- Columnas: Cliente | Título | Keyword | Word count | Fact-check score | Preview
- Acciones: Aprobar / Pedir revisión / Rechazar + comentario
- Integraciones: preview en mobile, diff con versión anterior

---

## Observabilidad y costos agregados

### Dashboard mínimo (Looker Studio o Metabase)

- **Costo por post**: promedio, mediana, outliers
- **Tiempo por post**: desde intake hasta publish
- **Tasa de fallo por agente**: ¿cuál rompe más?
- **Edición humana**: ¿cuántos posts necesitan re-run de algún agente?
- **ROI por cliente**: costo de producción vs precio cobrado

### Costo target por post

| Componente | Target | Stretch |
|------------|--------|---------|
| LLM (todos los agentes) | US$ 1.50 | US$ 1.00 |
| APIs externas | US$ 0.50 | US$ 0.30 |
| Humano (15 min @ US$ 30/h) | US$ 7.50 | US$ 5.00 |
| **Total COGS** | **US$ 9.50** | **US$ 6.30** |

Con precio promedio US$ 80-100/post → margen bruto 88-94%.

---

## Roadmap técnico (primeros 60 días)

### Semana 1: fundación
- [ ] Repo monorepo con estructura de agentes
- [ ] Airtable base con schema de posts
- [ ] Cuenta DataForSEO con US$ 50 de crédito
- [ ] Helicone/Langfuse para tracing LLM

### Semana 2-3: agentes 1-3 (happy path)
- [ ] Keyword Researcher funcional end-to-end
- [ ] Outline Writer
- [ ] Drafter
- [ ] Test: 3 posts completos generados (sin fact-check ni SEO)

### Semana 4: agentes 4-5 + humano
- [ ] Fact-Checker con Brave Search
- [ ] SEO Optimizer
- [ ] Vista Airtable para editor humano
- [ ] Test: 5 posts completos listos para publicar

### Semana 5: Publisher (WordPress)
- [ ] Conector WordPress REST
- [ ] Modo draft + scheduled
- [ ] Slack notifications

### Semana 6-8: producción real en blog propio
- [ ] 20 posts publicados en blog demo
- [ ] Medir: costo real, tiempo real, primeros rankings
- [ ] Ajustar prompts según learnings

### Semana 9-10: multi-cliente
- [ ] Abstracción "cliente" (brand voice, keywords, internal links)
- [ ] 2 CMS connectors más (Webflow + HubSpot)

### Semana 11-12: hardening
- [ ] Retries, fallbacks, alertas
- [ ] Documentación de SOPs
- [ ] Primer cliente pago onboarded

---

## Decisiones abiertas (pendientes de resolver)

1. **¿Multi-tenant desde día 1 o single-tenant y extraer después?**
   Recomendación: single-tenant (blog propio) → abstracción cuando llegue cliente #2.

2. **¿Orquestador propio o usar framework?**
   Recomendación: Claude Agent SDK (viene con sub-agentes, contexto manejado).

3. **¿Generación de imágenes incluida?**
   V1: no. V2: integrar con Flux o Recraft cuando validemos pricing.

4. **¿SEO audit como lead magnet?**
   Sí — usar mismo stack: el Keyword Researcher + un reporte-writer pequeño.
