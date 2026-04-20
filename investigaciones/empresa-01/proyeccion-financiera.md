# Proyección Financiera y Plan de Acción — Agencia SEO CaaS

> Derivada de: [Empresa 01](./README.md)
> Foco: modelo financiero con 3 escenarios + plan de acción a 24 meses

---

## 1. Supuestos del modelo

### Comerciales

| Variable | Valor base | Fuente |
|----------|-----------|--------|
| Ticket promedio inicial | US$ 1,800/mes | Mix 60% Starter + 40% Growth |
| Ticket promedio mes 12 | US$ 2,600/mes | Upsells a Growth y Scale |
| Tasa cierre de demos calificadas | 25% | Benchmark agencias SMB |
| Demos / mes (outbound) | 6-12 | 150 msjs/sem → 10% reply → 30% demo |
| Churn mensual | 6% | Contratos 3 meses + SLA reduce |
| Expansión MRR (upsell) | +3%/mes sobre base | Posts extra, newsletters |
| Ciclo de venta | 18 días | Desde primer contacto a cierre |
| CAC promedio | US$ 400 | Outbound propio, sin ads |

### Operativos

| Variable | Valor |
|----------|-------|
| COGS por post | US$ 9.50 |
| Posts promedio por cliente/mes | 18 |
| Tiempo humano por post | 15 min |
| Horas humano/mes por cliente | 4.5 h |
| Capacidad fundador (h/mes editando) | 40 h |
| Capacidad máx. fundador solo | 9 clientes |

### Costos fijos mensuales

| Ítem | Mes 1-6 | Mes 7-12 | Mes 13-24 |
|------|---------|----------|-----------|
| APIs (Claude, DataForSEO, etc.) base | US$ 200 | US$ 400 | US$ 800 |
| Tools (Airtable, Ahrefs, CRM, etc.) | US$ 300 | US$ 400 | US$ 500 |
| Dominio, legal, contabilidad | US$ 150 | US$ 200 | US$ 300 |
| Editor part-time | 0 | US$ 800 | US$ 1,500 |
| Account Manager | 0 | 0 | US$ 2,500 |
| Marketing/outbound tools | US$ 100 | US$ 200 | US$ 400 |
| **Total OpEx fijo** | **US$ 750** | **US$ 2,000** | **US$ 6,000** |

---

## 2. Escenarios a 24 meses

### Escenario Conservador (probabilidad ~30%)

Cierre 15%, churn 8%, ticket estancado en US$ 1,800.

| Mes | Clientes netos | MRR       | Ingresos mes | COGS+OpEx | Neto      | Acum.      |
|-----|----------------|-----------|--------------|-----------|-----------|------------|
| 3   | 1              | US$ 1.5k  | US$ 1.5k     | US$ 1.0k  | US$ 500   | -US$ 1.5k  |
| 6   | 3              | US$ 5.4k  | US$ 5.4k     | US$ 2.2k  | US$ 3.2k  | +US$ 2.0k  |
| 9   | 5              | US$ 9.0k  | US$ 9.0k     | US$ 3.4k  | US$ 5.6k  | +US$ 17.5k |
| 12  | 6              | US$ 10.8k | US$ 10.8k    | US$ 4.5k  | US$ 6.3k  | +US$ 37k   |
| 18  | 8              | US$ 14.4k | US$ 14.4k    | US$ 7.5k  | US$ 6.9k  | +US$ 78k   |
| 24  | 10             | US$ 18k   | US$ 18k      | US$ 9.5k  | US$ 8.5k  | +US$ 123k  |

**ARR mes 24**: US$ 216k (se llega a 6 cifras en mes ~15).

### Escenario Base (probabilidad ~50%)

Supuestos del cuadro principal. Cierre 25%, churn 6%.

| Mes | Clientes netos | MRR       | Ingresos mes | COGS+OpEx | Neto      | Acum.      |
|-----|----------------|-----------|--------------|-----------|-----------|------------|
| 3   | 2              | US$ 3.5k  | US$ 3.5k     | US$ 1.3k  | US$ 2.2k  | -US$ 0.5k  |
| 6   | 5              | US$ 11k   | US$ 11k      | US$ 3.0k  | US$ 8.0k  | +US$ 19k   |
| 9   | 8              | US$ 19k   | US$ 19k      | US$ 4.8k  | US$ 14.2k | +US$ 62k   |
| 12  | 10             | US$ 26k   | US$ 26k      | US$ 6.5k  | US$ 19.5k | +US$ 121k  |
| 18  | 14             | US$ 40k   | US$ 40k      | US$ 10k   | US$ 30k   | +US$ 275k  |
| 24  | 18             | US$ 54k   | US$ 54k      | US$ 14k   | US$ 40k   | +US$ 490k  |

**ARR mes 24**: US$ 648k. **Breakeven**: mes 4.

### Escenario Agresivo (probabilidad ~20%)

Cierre 35%, churn 4%, expansión 5%/mes, vertical nicheado rápido.

| Mes | Clientes netos | MRR        | Ingresos mes | COGS+OpEx | Neto       | Acum.      |
|-----|----------------|------------|--------------|-----------|------------|------------|
| 3   | 3              | US$ 5.4k   | US$ 5.4k     | US$ 1.6k  | US$ 3.8k   | +US$ 3k    |
| 6   | 7              | US$ 16k    | US$ 16k      | US$ 3.8k  | US$ 12.2k  | +US$ 36k   |
| 9   | 11             | US$ 28k    | US$ 28k      | US$ 6.2k  | US$ 21.8k  | +US$ 105k  |
| 12  | 15             | US$ 42k    | US$ 42k      | US$ 9k    | US$ 33k    | +US$ 220k  |
| 18  | 22             | US$ 68k    | US$ 68k      | US$ 15k   | US$ 53k    | +US$ 510k  |
| 24  | 30             | US$ 96k    | US$ 96k      | US$ 22k   | US$ 74k    | +US$ 890k  |

**ARR mes 24**: US$ 1.15M. **Breakeven**: mes 2-3.

---

## 3. Breakeven y cash flow

### Punto de equilibrio (escenario base)

- **Costos fijos mes 1-6**: US$ 750/mes
- **Margen de contribución por cliente**: US$ 1,800 − US$ 170 COGS = US$ 1,630
- **Clientes para breakeven**: ~1 cliente cubre costos fijos (mes 1-6)
- **En mes 7+ con editor**: necesita ~2 clientes activos

### Inversión inicial requerida (bootstrap)

| Ítem | Monto | Timing |
|------|-------|--------|
| Tiempo fundador pre-revenue | 0 (oportunidad) | Mes 0-2 |
| Registros, setup legal | US$ 500 | Mes 0 |
| APIs + tools primeros 3 meses | US$ 1,500 | Mes 0-3 |
| Blog demo (dominio, hosting, etc.) | US$ 300 | Mes 1 |
| **Capital inicial necesario** | **~US$ 2,500** | — |

No requiere inversión externa. Bootstrap viable.

### Cash flow acumulado escenario base

```
Mes 0:    -US$ 2,500  (setup)
Mes 3:    -US$ 500    (primeros clientes)
Mes 6:    +US$ 19k    (tracción clara)
Mes 12:   +US$ 121k   (6 cifras ARR)
Mes 24:   +US$ 490k
```

---

## 4. Análisis de cohortes y LTV

### LTV por plan (churn 6%/mes base)

| Plan    | Ticket | Vida media (meses) | Margen bruto/mes | LTV         |
|---------|--------|--------------------|--------------------|-------------|
| Starter | US$ 1,500 | 16.7 | US$ 1,330 | US$ 22,200  |
| Growth  | US$ 3,000 | 16.7 | US$ 2,700 | US$ 45,000  |
| Scale   | US$ 5,000 | 16.7 | US$ 4,500 | US$ 75,000  |

### Ratio LTV:CAC

- CAC blended: US$ 400
- LTV blended (mix 60/30/10): US$ 32,100
- **LTV:CAC = 80x** (excepcional; benchmark SaaS saludable es 3-5x)

El ratio tan alto indica margen para invertir más en adquisición (ads, contenido propio) después de mes 6.

---

## 5. Sensibilidad — qué variables mueven el negocio

Impacto sobre MRR mes 12 (escenario base = US$ 26k):

| Variable cambia | ΔMRR mes 12 | Lección |
|-----------------|-------------|---------|
| Cierre 25% → 35% | +US$ 11k (+42%) | **Mejorar demo es la palanca #1** |
| Cierre 25% → 15% | -US$ 10k (-39%) | Cuidar conversión desde mes 1 |
| Churn 6% → 3% | +US$ 7k (+27%) | Onboarding + SLA > adquirir |
| Churn 6% → 10% | -US$ 8k (-31%) | Churn alto mata el modelo |
| Ticket US$ 1,800 → US$ 2,500 | +US$ 10k (+38%) | Subir precio > buscar volumen |
| Volumen outbound 2x | +US$ 13k (+50%) | Pero limitado por tiempo humano |

**Conclusión**: las 3 palancas más fuertes son conversión de demo, churn y ticket. En ese orden.

---

## 6. Capacity planning

Limitante principal: **horas del editor humano**.

| Clientes | Posts/mes total | Horas humano/mes | Recurso |
|----------|-----------------|-------------------|---------|
| 1-3      | 20-60           | 5-15 h            | Solo fundador (2h/día) |
| 4-8      | 80-160          | 20-40 h           | Fundador full dedicación |
| 9-15     | 180-300         | 45-75 h           | Fundador + editor part-time |
| 16-25    | 320-500         | 80-125 h          | Fundador + editor full + AM |
| 26+      | 520+            | 130+ h            | Equipo de 3-5 personas |

**Trigger de contratación**: 70% de capacidad por 3 semanas consecutivas.

---

## 7. KPIs con metas mensuales

### Adquisición
- Mensajes outbound enviados: 600/mes
- Respuestas positivas: 60/mes (10%)
- Demos realizadas: 15/mes
- Clientes nuevos: 2-4/mes

### Producto
- Posts entregados vs comprometidos: ≥ 95%
- Costo COGS por post: ≤ US$ 10
- Tiempo humano por post: ≤ 15 min
- NPS trimestral: ≥ 40

### Financieros
- MRR growth MoM: ≥ 15% (meses 1-12), ≥ 10% (13-24)
- Churn mensual: ≤ 6%
- Margen bruto: ≥ 85%
- LTV:CAC: ≥ 10x

### Resultados cliente (externos, más importantes)
- Keywords en top 10 después de 90 días: ≥ 30% de posts publicados
- Tráfico orgánico MoM en blog cliente: ≥ 15% (meses 3-12)
- Retention: < 1 cancelación cada 6 clientes

---

## 8. Plan de acción — 24 meses

### Q1 (mes 1-3): Validación técnica + primer cliente

**Meta**: 2 clientes pagos + pipeline funcionando end-to-end.

- [ ] **Semana 1-2**: registro, stack setup, ICP definido
- [ ] **Semana 3-5**: agentes 1-3 construidos, blog demo lanzado
- [ ] **Semana 6-8**: agentes 4-6 + primer cliente cerrado (US$ 1,000 founding)
- [ ] **Semana 9-12**: segundo cliente + entrega fluida + SOPs documentados

**Go/no-go mes 3**: ¿se entregaron 30+ posts con costo real < US$ 10 y tiempo humano < 20 min?
- Sí → seguir. No → revisar pipeline antes de vender más.

### Q2 (mes 4-6): Tracción y validación comercial

**Meta**: 5 clientes, MRR US$ 11k, primer caso de estudio público.

- [ ] Documentar primer caso de estudio con rankings reales del cliente 1
- [ ] Subir precio base a US$ 1,500
- [ ] Sistema de outbound corriendo a 150 msjs/sem
- [ ] Editor part-time contratado en mes 6

**Go/no-go mes 6**: ¿MRR > US$ 10k + 2 clientes referidos?
- Sí → invertir más en adquisición. No → diagnosticar cierre/churn.

### Q3 (mes 7-9): Profesionalización

**Meta**: 8 clientes, MRR US$ 19k, primer vertical elegido.

- [ ] Elegir vertical #1 (probable: SaaS B2B)
- [ ] Landing vertical + content marketing propio
- [ ] Programa de referidos lanzado
- [ ] Dashboard de reportes para clientes automatizado

### Q4 (mes 10-12): Escala a 6 cifras ARR

**Meta**: 10 clientes, MRR US$ 26k, **ARR US$ 312k**.

- [ ] Contratar Account Manager en mes 11 (trigger: 8 clientes activos)
- [ ] Segundo CMS connector productivo
- [ ] Primer caso de estudio en Product Hunt / HN / LinkedIn viral
- [ ] Revisar pricing: testear plan Enterprise US$ 8k+

### Año 2 — Q5-Q8 (mes 13-24): Compound

**Meta**: 18-30 clientes, MRR US$ 54-96k.

- [ ] Segundo vertical validado
- [ ] Equipo: 1 editor full + 1 AM + 1 ops
- [ ] Newsletter propio con case studies (mini-producto: lead gen engine)
- [ ] Evaluación estratégica mes 18: ¿bootstrap indefinido / levantar / vender parcial?

---

## 9. Checkpoints de go/no-go

| Mes | Señal verde (continuar) | Señal roja (pivot o parar) |
|-----|-------------------------|-----------------------------|
| 3   | 2+ clientes pagos, pipeline end-to-end | 0 clientes después de 50+ demos |
| 6   | MRR ≥ US$ 8k, churn < 10% | MRR < US$ 5k o churn > 15% |
| 9   | Primer caso de estudio con ranking top 10 verificable | Ningún ranking top 20 después de 6 meses |
| 12  | ARR ≥ US$ 200k, ≥ 1 referido orgánico | ARR < US$ 120k o 100% outbound dependiente |
| 18  | Margen > 85%, NPS > 40 | Margen colapsando o NPS < 20 |

---

## 10. Riesgos financieros específicos

| Riesgo | Impacto $ | Mitigación concreta |
|--------|-----------|---------------------|
| Cliente grande (> 25% MRR) se va | -US$ 3-5k/mes | Cláusula de 60 días de aviso + cap de concentración |
| API Claude sube precio 2x | +US$ 300-600/mes COGS | Prompt caching agresivo + benchmarks con Haiku donde se pueda |
| Google penaliza AI content (update duro) | -30% clientes potencial | EEAT desde día 1: entrevistas a experts del cliente, autores humanos firmantes |
| Saturación outbound LinkedIn | -50% lead flow | Diversificar a email, Twitter, partnerships antes de mes 9 |
| Competidor copia modelo y baja precio | Compresión margen | Nichar por vertical + construir marca personal del fundador |

---

## 11. Resumen ejecutivo del modelo

- **Capital necesario**: US$ 2,500 (bootstrap viable)
- **Breakeven**: mes 4 (escenario base)
- **6 cifras ARR**: mes 12 (escenario base), mes 15 (conservador)
- **Limitante principal**: capacidad del editor humano (7-9 clientes por editor)
- **Palanca de crecimiento #1**: conversión de demo (25% → 35% = +42% MRR)
- **Margen bruto target**: 85-90%
- **LTV:CAC**: 80x (muy saludable; deja espacio para invertir en adquisición pagada después de mes 6)
- **Ventana de oportunidad**: 18-24 meses antes de que saturación baje márgenes. Hay que moverse rápido.
