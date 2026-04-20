# Empresa 01 — Agencia de Contenido SEO "Content-as-a-Service"

- **Modelo**: Agencia de contenido SEO operada por agentes IA + humano estratega
- **Sector**: MarTech / Content Marketing / SEO
- **Ticket objetivo**: US$ 1.5k - 5k mensual por cliente
- **Objetivo de facturación**: 6 cifras anuales con 6-10 clientes activos
- **Tiempo humano requerido**: 1-2 horas/día (estrategia + edición final)

---

## 1. Tesis del negocio

Las PYMEs B2B y SaaS early-stage necesitan contenido SEO constante (20-60 posts/mes) pero no pueden pagar agencias tradicionales (US$ 300-800 por post = US$ 6k-48k/mes). La brecha entre "contenido barato de baja calidad" (Fiverr, content mills) y "agencias premium caras" es el nicho.

Con un pipeline de agentes IA especializados + revisión humana al final, se puede ofrecer **volumen de agencia premium al 20-40% del costo**, manteniendo calidad editorial y resultados de ranking reales.

**Diferencial clave**: no se vende "contenido IA barato". Se vende **resultados de SEO medibles** (rankings, tráfico orgánico, leads) con contenido humano-editado.

---

## 2. Análisis de mercado

### Tamaño y tendencia

- Mercado global de content marketing: ~US$ 600B (2024), crece ~16% anual.
- 70% de marketers B2B invierten activamente en SEO.
- Post-actualizaciones de Google (Helpful Content Update 2023-2024): penalización a contenido 100% IA sin edición → ventaja para modelos híbridos.
- SMBs gastan en promedio US$ 2-5k/mes en contenido externalizado.

### Cliente ideal (ICP)

- **Tamaño**: 10-200 empleados
- **Tipo**: SaaS B2B, e-commerce nicho, consultoras, agencias legales/salud/finanzas
- **Señales de compra**:
  - Blog activo pero con frecuencia < 4 posts/mes
  - Tienen equipo de marketing de 1-3 personas
  - Usan HubSpot, Webflow, WordPress o Ghost
  - Ya invierten en Google Ads (validan intención SEO)
- **Dolor que paga**: "sabemos que el SEO funciona pero no tenemos tiempo/equipo para producir consistentemente"

### Competencia

| Competidor | Modelo | Precio | Debilidad que explotamos |
|------------|--------|--------|---------------------------|
| Verblio, Crowd Content, ContentFly | Freelancers humanos | US$ 100-400/post | Lento, inconsistente, sin estrategia |
| Jasper, Copy.ai, Writesonic | DIY tools | US$ 50-500/mes | El cliente tiene que operarlo |
| Byword, Koala, Cuppa AI | AI content automático | US$ 30-200/mes | Calidad baja, Google penaliza |
| Agencias tradicionales (Animalz, Grow&Convert) | Humano premium | US$ 8k-30k/mes | Inaccesible para SMB |
| **Nosotros** | **Híbrido IA+humano con pipeline** | **US$ 1.5-5k/mes** | — |

---

## 3. Arquitectura del producto

### Pipeline de agentes

```
Cliente → [Intake: dominio, tono, audiencia, temas semilla]
   ↓
1. Keyword Researcher      → clusters de keywords + intención + dificultad
   ↓
2. Outline Writer          → estructura H2/H3, entidades, preguntas PAA
   ↓
3. Drafter                 → borrador completo según outline + estilo
   ↓
4. Fact-Checker            → valida stats, citas, links, fechas
   ↓
5. SEO Optimizer           → meta tags, schema, links internos, CTR
   ↓
[HUMANO: estratega/editor — 10-15 min/post]
   ↓
6. Publisher               → CMS API (WordPress, Webflow, HubSpot, Ghost)
```

### Stack técnico sugerido

- **Orquestación**: Claude Agent SDK (sub-agentes especializados) o LangGraph
- **Modelo primario**: Claude Sonnet 4.6 para drafting, Opus 4.7 para outlines y fact-checking crítico
- **Keyword data**: DataForSEO API, Ahrefs API, o SerpAPI
- **Fact-checking**: búsqueda web + Claude con citas obligatorias
- **CMS publishing**: WordPress REST API, Webflow API, HubSpot API, Ghost Admin API
- **Tracking**: Google Search Console API + Looker Studio dashboards por cliente
- **Operaciones**: Airtable o Notion como CRM/kanban de posts

### Unit economics por post

| Concepto | Costo |
|----------|-------|
| API LLM (Claude, ~30-50k tokens/post) | US$ 0.50 - 1.50 |
| Keyword + SERP API | US$ 0.20 - 0.50 |
| Tiempo humano edición (12 min @ US$ 30/h) | US$ 6 |
| **Costo total por post** | **US$ 7 - 8** |
| Precio promedio cobrado al cliente | US$ 50 - 150 |
| **Margen bruto** | **~90%** |

---

## 4. Comercialización (Go-to-market)

### Fase 1: Outbound + casos de estudio (meses 1-3)

1. **Construir 2-3 casos propios**: crear blogs nicho, rankearlos en 60-90 días, documentar resultados. Esto es el "lead magnet" más potente.
2. **Outbound LinkedIn**:
   - Target: Head of Marketing / CMO / Founder en SaaS B2B 10-100 empleados
   - Señales: postean sobre contenido, blog subactivo, rondas Seed/Series A recientes
   - Volumen: 30-50 conexiones/día, 10-15 mensajes personalizados/día
   - Copy: abrir con auditoría SEO gratuita (automatizable con el mismo pipeline)
3. **Oferta irresistible**: "Te publico 10 artículos en 30 días. Si no veo señales de ranking en 90, te devuelvo el último mes."

### Fase 2: Inbound + partnerships (meses 4-9)

- Blog propio mostrando el método (meta, irónico, efectivo).
- Partnerships con agencias de diseño/desarrollo que no ofrecen contenido.
- YouTube/LinkedIn personal del fundador mostrando resultados reales.
- Programa de referidos 15% recurrente.

### Fase 3: Escala (mes 10+)

- Contratar un Account Manager cuando se superen 8 clientes.
- Subir ticket promedio con paquetes premium (video scripts, LinkedIn posts, newsletters).
- Verticalizar: "contenido SEO para fintech", "contenido SEO para healthtech".

---

## 5. Monetización y proyecciones

### Paquetes

| Plan       | Posts/mes | Precio/mes | Margen bruto (~90%) |
|------------|-----------|------------|---------------------|
| Starter    | 10        | US$ 1,500  | US$ 1,350           |
| Growth     | 25        | US$ 3,000  | US$ 2,700           |
| Scale      | 50        | US$ 5,000  | US$ 4,500           |
| Enterprise | 60+       | Custom     | —                   |

### Proyección de 12 meses (escenario base)

| Mes | Clientes | MRR        | Notas                          |
|-----|----------|------------|--------------------------------|
| 1   | 0        | US$ 0      | Build + casos propios          |
| 2   | 1        | US$ 1.5k   | Primer cliente (descuento)     |
| 3   | 2        | US$ 3.5k   |                                |
| 4   | 3        | US$ 6k     |                                |
| 6   | 5        | US$ 12k    | Primer Growth plan             |
| 9   | 8        | US$ 22k    | Necesidad de contratar AM      |
| 12  | 10       | US$ 30k    | **ARR ~US$ 360k = 6 cifras**   |

### Supuestos críticos

- Tasa de cierre outbound: 2-4% de conversaciones calificadas.
- Churn mensual: < 8% (contratos de 3 meses mínimo ayuda).
- CAC objetivo: < US$ 500 (outbound propio sin ads).
- LTV esperado: US$ 15-40k (retención 10-12 meses promedio).

---

## 6. Riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Google cambia algoritmo y penaliza IA | Media | Alto | Edición humana obligatoria, EEAT signals, entrevistas a expertos del cliente |
| Cliente pide "solo IA" para pagar menos | Alta | Medio | Mantener posicionamiento premium, no competir por precio |
| Saturación del nicho | Media | Medio | Verticalizar rápido + construir marca personal del fundador |
| Un cliente grande = >30% ingresos | Alta inicial | Alto | Capear clientes al 20% del MRR, diversificar desde mes 6 |
| Falla técnica del pipeline | Baja | Alto | Fallbacks en cada agente + revisión humana bloqueante |
| Alucinaciones / errores factuales | Alta | Alto | Fact-Checker + citas obligatorias + editor humano |

---

## 7. KPIs operativos

**Producto**:
- Posts publicados / mes
- Tiempo humano por post (objetivo: < 15 min)
- Costo COGS por post (objetivo: < US$ 10)

**Cliente**:
- Keywords en top 10 / top 3 (por cliente, mensual)
- Tráfico orgánico mes vs mes
- Posts publicados vs comprometidos (SLA > 95%)
- NPS trimestral

**Negocio**:
- MRR, churn, CAC, LTV
- Conversaciones outbound → demos → cierres

---

## 8. Plan de acción (90 días)

### Semana 1-2: Fundación
- [ ] Registrar marca y dominio
- [ ] Definir ICP final (1 vertical + 1 tamaño)
- [ ] Crear pricing page + one-pager de ventas
- [ ] Abrir cuentas: Claude API, DataForSEO, Ahrefs trial, CMS de prueba
- [ ] Setup Airtable como CRM de posts + clientes

### Semana 3-4: MVP del pipeline
- [ ] Construir agente Keyword Researcher (input: dominio + tema → output: cluster)
- [ ] Construir agente Outline Writer
- [ ] Construir agente Drafter con estilo configurable por cliente
- [ ] Test end-to-end: producir 5 posts propios para blog demo

### Semana 5-6: Pipeline completo + caso propio
- [ ] Agregar Fact-Checker + SEO Optimizer
- [ ] Integrar Publisher (empezar por WordPress API)
- [ ] Lanzar blog demo propio en nicho con baja competencia
- [ ] Publicar 20 posts en 2 semanas, empezar a medir ranking

### Semana 7-8: Primer cliente
- [ ] Armar secuencia outbound LinkedIn (3 mensajes)
- [ ] Target: 500 prospectos calificados en lista
- [ ] Enviar 150 mensajes, meta 3-5 demos
- [ ] Cerrar primer cliente a US$ 1,000/mes (descuento founding)
- [ ] Onboarding: brief de marca + 30 keywords semilla

### Semana 9-10: Entrega + refinamiento
- [ ] Publicar primeros 10 posts del cliente
- [ ] Setup dashboard Search Console compartido
- [ ] Documentar SOPs de cada agente
- [ ] Pedir testimonial inicial ("contenido entregado a tiempo")

### Semana 11-12: Segundo y tercer cliente
- [ ] Retomar outbound con caso real en mano
- [ ] Subir precio a US$ 1,500 base
- [ ] Cerrar 2 clientes más
- [ ] Revisar pipeline: qué agente rompe más, optimizar prompts

### Mes 4-6: Escala a US$ 10k MRR
- [ ] Contratar editor part-time (US$ 500-800/mes)
- [ ] Lanzar programa de referidos
- [ ] Primer caso de estudio público con métricas reales
- [ ] Empezar a testear inbound (LinkedIn posts del fundador 3x/semana)

### Mes 7-12: Escala a US$ 30k MRR
- [ ] Contratar Account Manager
- [ ] Segundo vertical
- [ ] Upsell a clientes existentes (newsletter, LinkedIn ghost-writing)
- [ ] Evaluar si conviene levantar capital o seguir bootstrap

---

## 9. Próximas investigaciones derivadas

- [ ] `analisis-competencia-detallado.md` — Deep dive en Animalz, Byword, Koala
- [ ] `stack-tecnico-agentes.md` — Especificación técnica de cada agente
- [ ] `playbook-outbound-linkedin.md` — Copys, cadencias, herramientas
- [ ] `casos-estudio-propios.md` — Plan para construir los 2-3 blogs demo
- [ ] `pricing-y-contratos.md` — Modelos de contrato, SLAs, cláusulas
- [ ] `vertical-saas-b2b.md` — Investigación específica del primer nicho
