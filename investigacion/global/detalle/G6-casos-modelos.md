# G6 · Casos reales, modelos de negocio y lecciones a nivel mundial

Informe de detalle para Federico. Fecha de elaboración: 30/10/2026. Todas las fuentes web se consultaron el 30/10/2026. Base: PDF *Negocios digitales con APIs: oportunidades y validación* (29/10/2026) e `investigacion/INFORME.md` (30/10/2026).

**Marcas:** [V] verificado en fuente primaria · [S] fuente secundaria o dato agregado por terceros · [E] estimación o cálculo propio · [NE] no encontrado / no verificable. **Autodeclarado** = la cifra la publica la empresa o el fundador sin auditoría.

> Advertencia general: casi todas las métricas de negocios chicos son autodeclaradas o de terceros que se citan entre sí. Las únicas cifras de ingresos con algún control externo de este informe son las de TrustMRR (conexión directa a Stripe u otro procesador de pagos) y aun así muestran ingresos, no márgenes ni rentabilidad. Hay sesgo de supervivencia fuerte: se publican los casos que funcionan.

---

## 1. Resumen en 8 puntos

1. **Existen negocios chicos sobre IA que facturan de verdad**, pero la distribución es una cola larga: unos pocos superan USD 100 mil de MRR y la mayoría de los micro-SaaS de IA que se venden en marketplaces facturan cientos o pocos miles de dólares por mes [V/S, §2].
2. **Los que mejor aguantan no venden "IA"**: venden un resultado en un flujo concreto (atribución de ventas, prospección B2B, validación de datos, SEO como servicio). Varios de los más grandes del ranking verificado son agencias o servicios productizados, no software puro [V, §2.1].
3. **El "sherlocking" es real y sigue pasando en 2026**: Ryze AI (gestión de anuncios Meta/Google) vio caer su tasa de cierre de 70% a 20% cuando Claude y Manus sumaron conectores de Meta Ads (02/2026); Relay (automatización tipo Zapier, respaldada por a16z) cerró en 08/2026 [S, §3]. Esto pega de lleno en la oportunidad 3 del PDF (reporting de agencias).
4. **El precio bajo mata la retención en IA**: según ChartMogul (12/2025), los productos de IA de menos de USD 50/mes retienen 23% del ingreso al año; los de más de USD 250/mes retienen 70%, igual que el SaaS B2B clásico [V, §5]. Traducido: ≈11,5% vs ≈2,9% de baja mensual [E].
5. **El 6% de baja mensual que usó el INFORME para Argentina coincide con el dato mundial** para productos de IA de USD 50–249/mes (45% de retención bruta anual ≈ 6,4% mensual) [E sobre dato V]. No es un supuesto pesimista: es la mediana.
6. **Margen bruto de IA: 45–60%, no 80%**. ICONIQ midió 45% promedio en productos de IA en 2025; Bessemer, ≈60% en las startups de IA que crecen "como SaaS" y ≈25% en las de crecimiento explosivo [V/S, §4.2]. Para un negocio con horas humanas de revisión, el margen lo define el servicio, no el token.
7. **Cobrar por resultado todavía es raro** (5% de las empresas lo usa como modelo principal), pero el modelo híbrido (fijo + uso) pasó de 27% a 41% en un año [S, §4.1]. La propuesta del PDF —implementación de alcance fijo + mensualidad con volumen incluido + excedente— está alineada con lo que hace el mercado.
8. **Matriz de decisión (§7):** las mejor puntuadas son *implementación productizada de IA para estudios contables* (nueva), *rentabilidad multi-cuenta ML/MP para agencias y estudios* (nueva, une 3 y 7) y *conciliación de lectura* (7). Las peores: localización de video (8), ventas por WhatsApp (6) y reporting genérico (3).

---

## 2. Casos documentados con números (2023–2026)

### 2.1 Ingresos verificados por procesador de pagos (TrustMRR)

TrustMRR publica ingresos conectados a Stripe, RevenueCat, App Store y otros, y declara que actualiza cada hora [1]. Es la fuente más dura encontrada, pero: (a) es una foto, sin fecha de corte visible; (b) no muestra costos ni margen; (c) el fundador elige qué mostrar; (d) la clasificación "IA" sale de la descripción, no de una auditoría.

| Negocio | Qué hace | MRR mostrado | ¿IA? | Lección | Marca |
|---|---|---|---|---|---|
| GojiberryAI | Plataforma B2B de salida comercial (GTM) | USD 424.368 | Sí | IA aplicada a generar ventas para otros: se paga por pipeline, no por "IA" | [V] [1] |
| 1Lookup | API de validación de teléfono, email e IP | USD 270.373 | No declarado | Una API de validación "aburrida" factura más que casi todos los wrappers; está **en venta** | [V] [1] |
| Cometly | Atribución de marketing ("chateá con tus datos de anuncios") | USD 198.256 | Parcial | La atribución sobrevive donde el reporting genérico no: conecta gasto con ventas reales (oportunidad 3 del PDF, bien hecha) | [V] [1] |
| AEO Engine | **Agencia** de SEO para buscadores de IA | USD 178.519 | Sí | Servicio productizado sobre IA, no software: escala con equipo | [V] [1] |
| PROSP | Prospección en LinkedIn con IA | USD 128.005 | Sí | En venta; categoría que Ryze señaló como "en riesgo" de absorción | [V] [1] |
| LLM Gateway | Gateway open-source de APIs de LLM | USD 78.764 | Sí (infra) | Infraestructura para desarrolladores | [V] [1] |
| Vozexo | Atención telefónica para plomeros | USD 218 (7 suscripciones) | Parcial | Voz para oficios en EE.UU.: arranque lento aun en el mercado más maduro | [V] vía [2] |
| Yapper | Recepcionista telefónica para oficios | USD 29 | Sí | Idem | [S] [2] |

### 2.2 Casos con cifras autodeclaradas o estimadas por terceros

| Caso | Cifra | Fuente y fecha | Marca y confianza |
|---|---|---|---|
| **HeadshotPro** (Danny Postma, solo, fotos de perfil con IA) | USD 300.000 MRR al año del lanzamiento; ≈ USD 3,6 M/año | Blog Supabird, sin fecha clara [3] | [S] autodeclarado, una sola fuente secundaria. No usar como base |
| **TypingMind** (Tony Dinh, interfaz para ChatGPT/Claude) | ≈ USD 817 mil en 2024 (360 mil en 2023), equipo de 3 | Estimación de Latka [4] | [S] estimación de tercero |
| **Intercom Fin** (agente de soporte, USD 0,99 por resolución) | > USD 100 M ARR, ≈ 350% de crecimiento anual (04/2026) | Sacra [5] | [S]; Sacra se contradice entre páginas (400 vs 419 M total). Cifras de Intercom no confirmadas en fuente primaria |
| **Compound** (agencia no-code de automatización para tiendas Shopify, Reino Unido) | USD 17.500/mes | Starter Story [6] | [S] autodeclarado; sin fecha ni margen |
| **AYH Consulting** (automatización de tareas repetitivas) | USD 6.000/mes | Starter Story [7] | [S] autodeclarado |
| **Lancer** (agente que busca y oferta trabajos en Upwork) | USD 10.000/mes | Starter Story, 03/2026 [8] | [S] autodeclarado |
| Agencia n8n (caso de Reddit) | USD 25.000 MRR en 4 meses, USD 1.500 base por cliente | Blog de tercero que cita r/n8n [9] | [NE] no se pudo ver el post original |
| **LedgerBox** (extracción de documentos financieros, solo) | USD 250 → USD 1.000 MRR | Indie Hackers [10] | [S] autodeclarado. El fundador dice que lo difícil fue elegir LLM (precisión vs costo vs velocidad) |
| **Desktop AI for CAs** (contadores, modelos locales) | USD 1.800 ARR, 6 clientes, a la venta | Microns [11] | [S] autodeclarado. Caso típico: vertical contable, ingreso mínimo |
| **Broccoli AI** (IA para contratistas: plomería, HVAC) | Serie A USD 25 M, 800+ contratistas, ≈20× ingresos en 2025 | Yespress [12] | [S]. Financiado, no bootstrapped: muestra que en voz para oficios en EE.UU. compite capital de riesgo |
| Netic (IA para oficios) | > USD 40 M levantados | Implicator [13] | [S] |

### 2.3 América Latina y Argentina

| Caso | Dato | Fuente | Marca |
|---|---|---|---|
| **Facturitas** (AR): factura electrónica por WhatsApp para monotributistas, con agentes de IA para el alta | > 5.000 usuarios activos | iProUP / ITSitio [14][15] | [S] autodeclarado; sin ingresos |
| **Talentum** (AR): agente de reclutamiento "Sara" | > 50 empresas clientes en 6 meses | Cronista (resultado de búsqueda) [16] | [S] autodeclarado |
| **Prometheo** (AR): CRM para pymes operado por agentes | ≈ USD 50/mes | Cronista [16] | [S] precio, sin clientes ni ingresos |
| **Darwin AI** (AR): bots en WhatsApp | Sin datos financieros | Ecosistema Startup [17] | [NE] |
| **Pulpos** (MX): IA en WhatsApp para pymes | USD 5 M levantados | Cronista [16] | [S] |
| Meta Business AI en LatAm | Llegó a AR con otros 16 países; cobro de mensajes del agente desde 01/08/2026 | Blog Diego Ceredi [18] | [S]. Competidor directo de la oportunidad 6 |

**No se encontró** [NE] ningún caso argentino bootstrapped con ingresos publicados y verificables construido sobre APIs de IA. Los casos locales informan usuarios o clientes, no ingresos.

### 2.4 Mercado de compraventa (qué vale un micro-SaaS de IA)

| Fuente | Dato | Marca |
|---|---|---|
| TrustMRR, listados en venta (10/2026) | La columna "múltiplo" equivale a precio ÷ ingreso anualizado [E: Unnamed Company, USD 53 mil/mes y USD 1,2 M → 1,9×]. Rango observado 0,2×–5,7×. Ejemplos de IA: LipsyncX 1,7× (USD 874/mes, pide USD 18 mil), LinkPost 1,6× (USD 4 mil/mes, USD 79 mil), Knightvision 0,6× (USD 36 mil/mes, USD 250 mil) | [V] precios de lista, no de cierre [1] |
| Microns (newsletter) | Ventas de USD 2.500–7.000. PlanTripAI: 21 clientes, USD 226/año, vendida a USD 2.500 (11×); PixelBazaar 1,45× | [S] autopromoción de la plataforma [19] |
| Acquire.com | Mediana 4,3× ganancia anual (TTM) en el informe de 01/2024; desde 2024 el marketplace valúa por ganancia, no por ingreso | [S] [20]; no se pudo abrir el informe 2025 [NE] |
| SEG / Acquiry | Volumen de M&A SaaS +28% en 2025, récord; brecha de múltiplos entre SaaS con y sin IA "se amplió" | [S] [21] |

**Lectura [E]:** un micro-SaaS de IA chico se vende a 1–2× ingreso anual (≈ 2–4× ganancia). Para Federico, la salida por venta no es un plan: el valor está en el flujo de caja.

---

## 3. Fracasos y "sherlocking": quién murió y por qué

| Caso | Qué pasó | Datos | Lección para Federico | Marca |
|---|---|---|---|---|
| **Jasper** (redacción de marketing sobre GPT) | ChatGPT gratis replicó gran parte de la propuesta | Valuación interna −20% (a ≈ USD 1,2 B desde 1,5 B); previsión de ARR 2023 recortada ≥ 30%; despidos 07/2023; cofundadores salieron de la operación 09/2023. Ingresos 2024: cifras contradictorias (USD 35 M vs 55 M) | No vender "la IA" a quien puede usar la IA directamente. Jasper sobrevivió girando a empresas y flujos de marca | [S] [22]; ingresos 2024 [NE fiable] |
| **ChatPDF y wrappers de "chateá con tu PDF"** (11/2023) | ChatGPT sumó lectura de PDF nativa | "Many startups just died today" (A. Ker); ChatPDF cobraba ≈ USD 10/mes | Una función que el modelo base puede absorber no es negocio. **Aplica a la oportunidad 1 (OCR de facturas)**: además de ARCA, cualquier LLM ya lee PDF | [S] [23][24]; pérdidas de ChatPDF [NE] |
| **Ryze AI** (gestión automática de anuncios Google/Meta) | Claude y Manus lanzaron conectores de Meta Ads | Tasa de cierre de 70% → 20%; "cientos de clientes en dos meses" antes. Ya había girado a flujos para agencias multi-cuenta | **Oportunidad 3 (reporting/ads) es la más expuesta.** La fundadora señala que resisten las herramientas que guardan datos del cliente (CRM, bases) y que MCP puede hacer que la IA elija la herramienta por el usuario | [S] autodeclarado, nota del 25/02/2026 [25] |
| **Relay** (automatización tipo Zapier, a16z) | Cerró: acceso gratis hasta 15/08/2026, pago hasta 14/09/2026; el CEO pasó a Google Chrome | La nota atribuye el cierre a que Google Workspace, Copilot y OpenAI integraron automatización en productos que el usuario ya paga (análisis del medio, no del fundador) | El "pegamento genérico" entre apps queda dentro de las suites. Lo local (ML, MP, ARCA, Tango) no lo integran los grandes | [S] [26] |
| **Huxe** (podcasts generados por IA) | Cerró un día después de que Spotify lanzara una función similar | — | El riesgo no es solo OpenAI: es cualquier plataforma dueña del usuario (Spotify, Meta, Tiendanube, ML) | [S] [27] |
| Tendencia | Las adquisiciones "acqui-hire" (se contrata al equipo, se cierra el producto) fueron la salida más común de startups de IA en 2024–2025 | — | — | [S] [27] |

**Contrapunto honesto:** varios analistas consideraron exagerado el pánico por los PDF ("Jasper is fine", 2023) [24], y Stripe sostiene que llamarlas "wrappers" no explica su crecimiento [28]. El patrón que sí se repite: **muere la función genérica horizontal; sobrevive el flujo vertical con datos, integración y operación**.

---

## 4. Modelos de monetización comparados

### 4.1 Qué usa el mercado

| Modelo | Ejemplo con precio | Adopción / evidencia | Ventaja | Riesgo para Federico |
|---|---|---|---|---|
| Suscripción por asiento | Pipedrive USD 14/asiento (PDF) | Cae de 21% a 15% como modelo principal en 12 meses [S][29] | Simple | La IA reduce asientos; pyme argentina tiene pocos usuarios |
| Suscripción fija | Prometheo ≈ USD 50 [16] | 29% → 22% [S][29] | Predecible | Si el uso de IA crece, se come el margen |
| **Híbrido (fijo + uso)** | Gorgias USD 10/50 tickets + extras (PDF) | 27% → **41%** en 12 meses; 29% deja elegir modelo (2026) [S][29][30] | Protege margen | Explicarlo bien a la pyme |
| Por uso | Vapi USD 0,05/min; Textract; Fin desde 50 resoluciones mínimas | Estándar en infraestructura | Alineado al costo | Ingreso volátil; difícil en pesos con inflación |
| **Por resultado** | Intercom Fin USD 0,99 por resolución [5] | Solo 5% como modelo principal; 25% espera usarlo en 2028 [S][29] | Vende ROI | Hay que medir el resultado de forma indiscutible; Fin lo hace con escala que Federico no tiene |
| **Setup + retainer (servicio productizado)** | Agencias Starter Story USD 6–17,5 mil/mes [6][7]; caso n8n USD 1.500/cliente [9] | Predomina en agencias de automatización | Cobra desde el día 1; sirve para aprender | No escala sin gente; cada cliente pide algo distinto (el PDF ya lo advierte) |
| Revenue share con partners | Programa de agencias Tiendanube (INFORME); "contador campeón" con comisión recurrente (INFORME) | Sin datos públicos de % de comisión [NE] | Canal de confianza | Cede 15–30% del ingreso [E, rango habitual no verificado] |
| Marketplace / app store | Tiendanube apps, ML app store | Comisiones y conversión [NE] | Distribución | Dependencia total de la plataforma (riesgo Huxe) |

### 4.2 Margen bruto real

| Fuente | Dato | Marca |
|---|---|---|
| ICONIQ, State of AI 2025 (≈300 empresas) | Margen bruto promedio de productos de IA: 41% (2024) → 45% (2025); proyecta 53% (2026) y 59% (2027) | [S] vía [31][32] |
| Bessemer, State of AI 2025 (13/08/2025) | "Supernovas" (USD 40 M ARR en el año 1): ≈ 25%, a menudo negativo. "Shooting Stars": ≈ 60%. En mercados saturados de wrappers, márgenes "cerca de cero o negativos" | [V] [33] |
| Benchmarkit 2026 (vía CloudZero) | Software tradicional: mediana > 80% | [S] [34] |

**Lectura [E] aplicada al PDF:** en el escenario de documentos del PDF (abono 299, costo técnico 50, operación 100) el margen bruto es ≈ 50% si se cuenta la hora humana como costo de venta. En el escenario AR-A del INFORME es negativo. **La IA no es el costo dominante; la hora de revisión sí.** Esto coincide con la regla del INFORME de ≤ 3 h por cliente.

---

## 5. Benchmarks de métricas SaaS pyme 2025–2026

| Métrica | Dato | Fuente / fecha | Marca |
|---|---|---|---|
| **Retención de productos de IA por precio** (empresas ≥ USD 250 mil ARR, 2025) | < USD 50/mes: GRR 23%, NRR 32%. USD 50–249: GRR 45%, NRR 61%. > USD 250: GRR 70%, NRR 85% | ChartMogul / K. Poyar, 10/12/2025, ≈200 empresas de IA [35] | [V] (el autor lo llama "direccional") |
| Equivalente mensual [E] | < 50: ≈ 11,5% de baja mensual · 50–249: ≈ 6,4% · > 250: ≈ 2,9% | Cálculo propio: 1 − GRR^(1/12) | [E] |
| Retención mediana IA-nativa vs SaaS | IA: GRR 40%, NRR 48%. B2B SaaS: NRR 82% (cuartil superior 97%). B2C: NRR 49%. GRR de IA subió de 27% (01/2025) a 40% (09/2025) | ChartMogul [35] | [V] |
| Baja mensual por precio (SaaS general) | ARPA < USD 25: 6,1% mensual; ARPA > USD 500: 2,2% | ChartMogul, página de métricas (sin año visible) | [S] snippet [36]; la página actual (09/2026) dice que productos < USD 50 retienen > 20 p.p. peor y > USD 250 igual que B2B [V][36] |
| NRR mediana B2B privada | 101% NRR, 91% GRR (todas las empresas); contratos multianuales 103%/94% | SaaS Capital 2025 [37] | [S] (snippet del PDF primario; no se abrió la tabla por ACV) |
| ACV bootstrapped | Mediana USD 23.391 (empresas bootstrapped > USD 1 M ARR, datos 2024) | SaaS Capital [37] | [S]. Muy por encima de lo que paga una pyme argentina |
| **Repago de CAC** | Mediana 18 meses (datos 2024) → 16 meses (datos 2025, 198 empresas); cuartil superior ≤ 6 meses. Por ACV: < USD 5 mil ≈ 9–11 meses | Benchmarkit 2025 / Aleph × Benchmarkit 2026 [38] | [S] cifras contradictorias entre fuentes |
| Prueba gratis → pago | Opt-in (sin tarjeta) 18,2%; opt-out (con tarjeta) 48,8%; freemium 2,6% | FirstPageSage, 86 empresas, 2022–2025, vía agregador [39] | [S]. Otras fuentes: 8% (Userpilot), 15–20% (ProfitWell) |
| Velocidad de las empresas de IA | Top 100 de IA en Stripe llegaron a USD 5 M anualizados en ≈ 24 meses vs 37 de las top 100 SaaS (2018) | Carta de Stripe 2024, publicada 02/2025 [28] | [S] (dato propio de Stripe, sesgo al tope de la distribución) |

**Implicancias de los benchmarks para el modelo del INFORME [E]:**
- El supuesto de baja 6% mensual con abono de USD 150–250 **es la mediana mundial**, no un caso pesimista. Por debajo de USD 50 (precios tipo Jaguar Sheet o Xubio) la baja esperable se duplica.
- CAC USD 500 con contribución de USD 51–139 (escenarios AR-B/AR-C del INFORME) da repago de 4–10 meses: mejor que la mediana de 16–18 meses, **siempre que el CAC real no supere USD 500**, lo que en venta consultiva (entrevistas, diagnóstico, piloto) es optimista.
- Prueba gratis sin tarjeta convierte ≈ 18%: para servicios asistidos tiene más sentido el **piloto pago** del PDF que un trial.

---

## 6. Lecciones transversales

1. **Lo que se absorbe**: funciones horizontales que el modelo base o la suite ya tiene (leer PDF, redactar, automatizar entre apps de Google/Microsoft, operar anuncios de Meta). [S][23][25][26]
2. **Lo que resiste**: datos propios del cliente acumulados, integraciones locales que los grandes no priorizan, operación de excepciones y canal de confianza. Coincide con el INFORME (ARCA, ML, MP, Tango) y con la lectura de la fundadora de Ryze. [S][25]
3. **Precio ≥ USD 250/mes o no hay retención** en productos de IA; si la pyme argentina no paga eso, hay que vender a quien sí: estudios, agencias o despachantes que atienden varias cuentas (multi-cuenta) [V][35] + [E].
4. **Los ganadores verificados suelen estar a un paso del dinero del cliente**: atribución (Cometly), prospección (GojiberryAI), validación (1Lookup). Venden ingresos o ahorro medible [V][1].
5. **Los servicios productizados facturan antes que el SaaS** (AEO Engine, agencias Starter Story) [V/S], a costa de escalabilidad. Para un fundador solo en Argentina es la forma de financiar el producto.
6. **El riesgo de plataforma incluye a Meta, Spotify, Tiendanube y ML**, no solo a los laboratorios de IA [S][18][27].
7. **La salida por venta es modesta** (1–2× ingreso anual en micro-SaaS de IA) [V][1]: diseñar para caja, no para exit.

---

## 7. Marco de decisión: matriz de puntuación

**Escala 1–5, donde 5 siempre es mejor para Federico** (alta demanda, poca competencia, barrera baja para un fundador solo, bajo riesgo de plataforma, alto potencial de precio, fácil de vender desde Argentina). **Pesos [E]:** demanda 25%, riesgo de plataforma 20%, competencia 15%, barrera para fundador solo 15%, precio 15%, venta desde AR 10%. Los puntajes son juicio del analista [E] apoyado en la evidencia citada; cambiar los pesos puede cambiar el orden de las posiciones cercanas.

### 7.1 Oportunidades evaluadas

- **1–8**: las del PDF, tal como están planteadas (versión genérica).
- **N1 · Implementación productizada de IA para estudios contables** (nueva): setup fijo + retainer mensual para implementar y operar flujos (carga, conciliación, respuestas a clientes) sobre las herramientas que el estudio ya usa. Evidencia: 39% de los contadores dice "no sé cómo implementarlo" (INFORME, encuesta TR/CPCECABA 2025); agencias de automatización con USD 6–17,5 mil/mes autodeclarados [6][7]; AEO Engine verificado como agencia [1]. Cuando Claude o ChatGPT sacan una función nueva, el servicio la incorpora en lugar de morir.
- **N2 · Rentabilidad y conciliación multi-cuenta ML/MP para agencias y estudios** (nueva como forma de venta; une 3 y 7 y sigue la cuña 1 del INFORME): vender al intermediario que maneja muchas cuentas, como hizo Ryze al girar [25], y cobrar ≥ USD 250 por cartera para entrar en el tramo de buena retención [35].
- **N3 · API de validación fiscal argentina para software houses** (nueva): CUIT, constatación de comprobantes (WSCDC), padrón, APOC, duplicados, como API por uso. Análogo global: 1Lookup, USD 270 mil MRR verificado [1]. Competencia local probable (existen SDK comerciales de ARCA/AFIP) [E, no investigada → NE].

### 7.2 Matriz

| # | Oportunidad | Demanda (25%) | Competencia (15%) | Barrera solo (15%) | Riesgo plataforma (20%) | Precio (15%) | Venta desde AR (10%) | **Puntaje** |
|---|---|---|---|---|---|---|---|---|
| N1 | Implementación productizada para estudios contables | 4 | 3 | 4 | 4 | 3 | 4 | **3,70** |
| N2 | Rentabilidad multi-cuenta ML/MP para agencias/estudios | 4 | 4 | 3 | 3 | 3 | 4 | **3,50** |
| 7 | Conciliación de lectura (genérica) | 3 | 3 | 3 | 3 | 3 | 4 | **3,10** |
| 4 | CRM vertical (como módulo) | 3 | 2 | 3 | 3 | 3 | 3 | **2,85** |
| N3 | API de validación fiscal AR | 2 | 2 | 4 | 4 | 2 | 3 | **2,80** |
| 1 | Documentos verticales (OCR de facturas) | 3 | 2 | 3 | 2 | 2 | 4 | **2,60** |
| 5 | Soporte ecommerce | 3 | 2 | 3 | 2 | 2 | 4 | **2,60** |
| 2 | Voz entrante | 2 | 3 | 2 | 2 | 4 | 3 | **2,55** |
| 3 | Reporting de agencias (genérico) | 3 | 1 | 4 | 1 | 1 | 3 | **2,15** |
| 6 | Ventas por WhatsApp (genérico) | 3 | 1 | 3 | 1 | 2 | 3 | **2,15** |
| 8 | Localización de video | 2 | 1 | 3 | 1 | 2 | 3 | **1,90** |

### 7.3 Justificación de los puntajes clave

| # | Por qué | Evidencia |
|---|---|---|
| N1 | Demanda por falta de saber implementar; el servicio se adapta cuando la plataforma cambia; cobra desde el día 1. Pierde en precio (estudios pagan ARS 40–52 mil por herramientas) y en escalabilidad | INFORME §4.2; [6][7][1] |
| N2 | Hueco sin conectores globales; multi-cuenta permite precio ≥ USD 250; riesgo de que ML agregue reportes nativos de rentabilidad (3) | INFORME §4.1; [25][35] |
| 1 | ARCA ya estructura las facturas y los LLM leen PDF de forma nativa: caso ChatPDF | INFORME §1; [23] |
| 2 | Precio alto (Smith.ai USD 150–500) pero en AR se escribe más de lo que se llama; en EE.UU. compite capital de riesgo (Broccoli, Netic) y los bootstrapped arrancan en USD 29–218 MRR | PDF; [2][12][13] |
| 3 | El más expuesto: Claude/Manus absorbieron la gestión de Meta Ads (Ryze); precio commodity USD 15–20 por cliente. Solo se salva como atribución a ventas reales (Cometly) | [25][1]; PDF |
| 6 | Meta lanzó su propio agente en LatAm, cobra mensajes y su cláusula 4.7 restringe la IA como producto principal | [18]; INFORME §4.3 |
| 8 | HeyGen vende la API de traducción directo; categoría de redacción/medios con el patrón Jasper | PDF; [22] |

**Sensibilidad [E]:** si se sube el peso de "potencial de precio" a 25% (y se baja demanda a 15%), la voz (2) sube a ≈ 2,75 y supera a documentos, pero N1 y N2 siguen arriba. El orden de las tres primeras se mantiene bajo cualquier ponderación razonable porque ninguna puntúa bajo en riesgo de plataforma.

---

## 8. Datos que no se encontraron [NE]

- Informe 2025/2026 de Acquire.com con múltiplos específicos de IA (la página no cargó).
- Ingresos verificados de ChatPDF después de 11/2023 y de Jasper en 2024–2025 (fuentes contradictorias).
- MRR de PhotoAI (Pieter Levels) para 2025.
- Margen bruto real de agencias de automatización con IA (ninguna lo publica).
- Comisiones de revenue share en programas de partners de Tiendanube o Mercado Libre.
- Casos argentinos bootstrapped con ingresos publicados.
- Tabla de SaaS Capital por ACV para bootstrapped (está en el PDF primario, no se extrajo).

---

## 9. Implicancias para Federico

1. **No construyas un "wrapper" horizontal.** Cada caso de muerte documentado (Jasper, PDF chat, Ryze, Relay) es una función genérica que el modelo o la suite absorbió. Las oportunidades 3, 6 y 8 del PDF están en esa zona.
2. **Vendé al que maneja muchas cuentas** (estudios, agencias, despachantes), no al vendedor o la pyme suelta: es la única forma realista de cobrar ≥ USD 250/mes, el umbral donde la retención de productos de IA se parece a la del SaaS B2B (70% vs 23% bajo USD 50).
3. **Arrancá como servicio productizado** (setup fijo + retainer con volumen incluido, el esquema del PDF) y convertí en software solo lo que se repita en 3+ clientes. Es el patrón de los casos que facturan antes (agencias, AEO Engine) y reduce el riesgo de plataforma: si Claude o ChatGPT sacan una función, la integrás en el servicio.
4. **Tomá 6% de baja mensual como el caso base, no el pesimista**: es la mediana mundial para IA de USD 50–249. El modelo del INFORME ya lo usa; no lo "mejores" en la planilla sin datos propios.
5. **Calculá margen con horas, no con tokens**: el mercado de IA trabaja con 45–60% de margen bruto; tu límite es ≤ 3 h de revisión por cliente.
6. **Defensa = integración local + datos del cliente + operación de excepciones.** ML/MP/ARCA/Tango no los va a integrar OpenAI ni Anthropic a corto plazo; eso respalda la cuña #1 del INFORME (N2 en la matriz).
7. **Medí con piloto pago, no con prueba gratis**: el trial sin tarjeta convierte ≈ 18% en SaaS en general, y en servicio asistido el piloto pago filtra mejor la intención real.
8. **No planifiques una venta del negocio**: los micro-SaaS de IA se ofrecen a 1–2× el ingreso anual. Diseñá para caja mensual.

---

## Fuentes (consultadas el 30/10/2026)

1. TrustMRR, ranking por MRR y listados en venta (ingresos verificados vía Stripe/RevenueCat/App Store). https://trustmrr.com/
2. TrustMRR, Vozexo y fundador de Yapper (vía resultados de búsqueda). https://trustmrr.com/startup/vozexo-answering-service-for-plumbing-companies.md · https://trustmrr.com/founder/_jamesmck
3. Supabird, "The Solo Founder Who Built a $300K/Month AI Empire: Danny Postma HeadshotPro". https://supabird.io/articles/danny-postma-how-a-solo-hacker-built-an-ai-empire-from-bali
4. Latka, TypingMind. https://getlatka.com/companies/typingmind
5. Sacra, Intercom. https://sacra.com/research/intercom
6. Starter Story, Compound (agencia no-code de ecommerce). https://starterstory.herokuapp.com/stories/compound
7. Starter Story, AYH Consulting. https://starterstory.herokuapp.com/stories/ayh-consulting-ltd
8. Starter Story, "I Built a $10K/Month AI Agent" (03/2026). https://rosetta.to/u/starterstory/i-built-a-10k-month-ai-agent?t=0
9. BrowserAct blog, caso n8n USD 25 mil/mes (cita r/n8n). https://ab-admin.browseract.com/blog/best-high-income-case-analysis-how-to-achieve-25000-monthly-revenue-with-n8n
10. Indie Hackers, LedgerBox. https://www.indiehackers.com/product/ledgerbox
11. Microns, Desktop AI for Financial Document Extraction. https://www.microns.io/startup-listings/desktop-ai-for-financial-document-extraction
12. Yespress, Broccoli AI. https://yespress.io/broccoli-ai
13. Implicator, Netic. https://www.implicator.ai/netic-ais-got-this-the-smartest-plumber-doesnt-work-for-you-anymore.md
14. iProUP, Facturitas. https://www.iproup.com/startups/69692-app-monotributistas-iaemitir-facturas-whatsapp-mercado-pago-tienda-nube-facturitas
15. ITSitio, "Crearon una IA que emite facturas por WhatsApp". https://www.itsitio.com/ar/inteligencia-artificial/crearon-una-ia-que-emite-facturas-por-whatsapp-y-simplifica-la-vida-de-los-monotributistas/
16. El Cronista (Prometheo, Pulpos, Talentum; datos de titulares y extractos). https://www.cronista.com/colombia/finanzas-y-economia/el-asistente-de-ia-que-surgio-por-accidente-y-hoy-impulsa-a-pymes-latinas-cuesta-solo-50-dolares · https://www.cronista.com/mexico/finanzas-economia/pulpos-recauda-5-millones-de-dolares-para-revolucionar-pymes-mexicanas-con-ia-en-whatsapp
17. Ecosistema Startup, Darwin AI. https://ecosistemastartup.com/darwin-ai-la-startup-argentina-que-transforma-whatsapp-con-ia/
18. Diego Ceredi, "IA vende sola: WhatsApp Business Argentina". https://www.diegoceredi.com/blog/ia-vende-sola-whatsapp-business-argentina
19. Microns newsletter (archivo de ventas). https://newsletter.microns.io/archive · https://newsletter.microns.io/p/microns-in-june-9-startups-sold-worth
20. Acquire.com blog, informes de múltiplos (tag). https://blog.acquire.com/tag/acquire-coms-acquisition-multiples-report/ (no cargó; dato 01/2024 vía resumen secundario)
21. Acquiry, "SaaS M&A Hits Record Volume in 2025". https://www.acquiry.com/saas-ma-record-volume-2025/
22. Maginative, "Jasper Appoints New CEO and Cuts Internal Valuation as AI Growth Slows" (2023). https://www.maginative.com/article/jasper-cuts-internal-valuation-as-ai-growth-slows/
23. TechCrunch, "Get the PDF outta here" (06/11/2023). https://techcrunch.com/2023/11/06/get-the-pdf-outta-here
24. Business Insider India, "Founders who built on ChatGPT find out the hard way…" (11/2023). https://www.businessinsider.in/tech/news/bracing-for-the-impact-founders-who-built-on-chatgpt-find-out-the-hard-way-big-tech-can-torpedo-their-work/articleshow/104949320.cms · contrapunto: https://www.thealgorithmicbridge.com/p/openai-gpt-store-is-not-the-end-of
25. Free Press Journal, "'Claude AI Killed My Startup'" (25/02/2026). https://www.freepressjournal.in/tech/claude-ai-killed-my-startup-founder-explains-how-one-feature-made-her-business-obsolete
26. Value Add VC, cierre de Relay (17/08/2026). https://valueaddvc.com/pulse/relay-ai-startup-shutdown-google-chrome-2026
27. Pulse.bot, cierre de Huxe. https://www.pulse.bot/media/news/audio-generation-app-huxe-founded-by-former-notebooklm-developers-shuts-down-fcdd3975-3e8c-4326-8a5e-c507bd1f17e3/
28. TechCrunch, "Stripe CEO says AI startups are growing faster than SaaS ever did" (27/02/2025). https://techcrunch.com/2025/02/27/stripe-ceo-says-ai-startups-are-growing-faster-than-saas-ever-did-and-calling-them-wrappers-misses-the-point · Stripe, carta 2025: https://stripe.com/newsroom/news/stripe-2025-update
29. Kyle Poyar, "2025 State of B2B Monetization" (Growth Unhinged, encuesta 04–05/2025, 240+ empresas). https://www.growthunhinged.com/p/2025-state-of-b2b-monetization
30. Sequence, "What changed in SaaS pricing in the past 12 months". https://www.sequencehq.com/blog/what-changed-in-saas-pricing-in-the-past-12-months
31. Upstarts Media, "Startups Are Learning What AI Profits Look Like" (ICONIQ 2025). https://www.upstartsmedia.com/p/data-ai-startup-margins-rise
32. SaaStr, "10 metrics from ICONIQ's 2026 State of AI report". https://saastr.com/the-builders-economy-10-metrics-from-iconiqs-newest-2026-state-of-ai-report
33. Bessemer Venture Partners, "The State of AI 2025" (13/08/2025). https://www.bvp.com/atlas/the-state-of-ai-2025
34. CloudZero, "AI gross margin" (cita Benchmarkit 2026). https://www.cloudzero.com/blog/ai-gross-margin
35. ChartMogul / Kyle Poyar, "The SaaS Retention Report: The AI churn wave" (10/12/2025). https://chartmogul.com/reports/saas-retention-the-ai-churn-wave/
36. ChartMogul, Customer churn (actualizada 08/09/2026). https://chartmogul.com/saas-metrics/customer-churn/
37. SaaS Capital, "2025 B2B SaaS Retention Benchmarks" (PDF, 09/2025). https://www.saas-capital.com/wp-content/uploads/2025/09/RB32WS1-2025-B2B-SaaS-Retention-Benchmarks.pdf
38. Aleph, "CAC payback period SaaS 2026" (Aleph × Benchmarkit). https://www.getaleph.com/answers/cac-payback-period-saas-2026 · Maxio, 2025 B2B SaaS Benchmarks: https://www.maxio.com/?p=8708
39. Flint / agregadores que citan FirstPageSage Free Trial Benchmarks. https://www.flint.com/blog/b2b-saas-free-trial-conversion-rate-statistics
