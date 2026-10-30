# G1 · Panorama global: economía de APIs e IA aplicada para pymes (2025–2026)

Investigación al 30/10/2026 para Federico. Complementa el PDF *Negocios digitales con APIs* (29/10/2026) y `investigacion/INFORME.md` (Argentina); no repite lo local.

**Marcas:** [V] verificado en fuente primaria · [S] fuente secundaria (prensa, agregadores, trackers) · [E] estimación o cálculo propio · [NE] no encontrado.
**Pronóstico ≠ dato:** se aclara en cada cifra. Las cifras de ARR de startups privadas casi siempre son autodeclaradas o estimadas por terceros.

---

## 1. Resumen en 8 puntos

1. **El dinero existe y crece rápido, pero se concentra arriba.** El gasto empresarial en IA generativa fue de USD 37.000 M en 2025 (3,2× 2024), con USD 19.000 M en aplicaciones [V, dato de encuesta, 1]. Gartner proyecta USD 2,6–2,7 billones de gasto total en IA para 2026, en su mayoría infraestructura [S, pronóstico, 2][3].
2. **Las aplicaciones verticales son la categoría que más crece**: USD 3.500 M en 2025, casi 3× (salud USD 1.500 M, legal USD 650 M) [V, 1]. Las startups capturan el 63% del gasto en aplicaciones, y el 91% en finanzas y operaciones [V, 1].
3. **El soporte al cliente con agentes es donde hoy se ve ARR grande y rápido**: Sierra USD 100 M ARR (11/2025) [V, 8] y ~USD 200 M (05/2026) [S, 9]; Decagon >USD 100 M (08/2026) [S, 10]; Fin (Intercom) cerca de USD 100 M [S, 12]. En legal, Harvey supera los USD 200 M [S, 13].
4. **El precio por resultado ya es estándar en soporte**: Fin cobra USD 0,99 por resultado, con un mínimo de 50 por mes [V, 11]. Sierra cobra por trabajo completado [V, 8].
5. **Los laboratorios entraron directo a la pyme**: Claude for Small Business (13/05/2026) [S, 15], ChatGPT Small Business Program con *ChatGPT Work* (21/07/2026) [S, 16] y MCP como estándar de conectores, hoy bajo la Linux Foundation [S, 17]. Lo genérico y horizontal para pymes estadounidenses quedó absorbido.
6. **La inferencia es barata y sigue bajando, pero también puede subir**: la gama baja cuesta ~USD 2 por 10 M de tokens de entrada + 2 M de salida en OpenAI, Anthropic y Google [V, 21–23]. Google anunció **aumentos** para Gemini 4 Argon (01/12/2026) y Gemini 3.x Flash (01/01/2027) [V, 23].
7. **Los márgenes y la retención son el problema estructural**: las empresas nativas de IA tienen un margen bruto de ~45–53% contra 75–85% del SaaS [S, 25]. La retención bruta (GRR) es de 40% y la neta (NRR) de 48%, aunque sobre USD 250/mes se iguala al B2B SaaS (GRR 70%, NRR 85%) [V, 26].
8. **Para alguien chico, lo defendible es lo vertical, integrado y con operación de excepciones**, cobrado por resultado. Los grandes están absorbiendo los *wrappers* finos, los agregadores de modelos y los asistentes horizontales [V, 28].

---

## 2. Tamaño y crecimiento del mercado

### 2.1 Gasto total en IA y en IA generativa

| Métrica | Valor | Tipo | Fuente |
|---|---|---|---|
| Gasto empresarial en IA generativa, 2025 (EE.UU., encuesta a 495 decisores) | USD 37.000 M (2024: 11.500 M; 2023: 1.700 M) | Dato estimado por encuesta | [V] [1] Menlo Ventures, 09/12/2025 |
| Capa de aplicaciones, 2025 | USD 19.000 M (>50% del total) | Dato estimado | [V] [1] |
| Capa de infraestructura, 2025 (de la cual APIs de modelos: USD 12.500 M) | USD 18.000 M | Dato estimado | [V] [1] |
| Comprar vs. construir | 76% comprado en 2025 (53% en 2024) | Dato de encuesta | [V] [1] |
| Gasto mundial en IA, 2026 (Gartner, 05/2026) | USD 2,59 billones (+47%) | **Pronóstico** | [S] [3] CIO Dive, 19/05/2026 |
| Gasto mundial en IA, 2026 (Gartner, 16/09/2026) | ≈ USD 2,7 billones (+49,5%); modelos de IA generativa USD 28.300 M (+117%) | **Pronóstico** | [S] [2]. Comunicado de Gartner con 403; cifra vía prensa |
| Modelos de IA, 2027 (Gartner, mayo) | ≈ USD 60.000 M | **Pronóstico** | [S] [3] |

**Lectura:** la mayor parte de los "billones" de Gartner es infraestructura (servidores, centros de datos). Para un emprendedor, lo relevante es la capa de aplicaciones de Menlo (USD 19.000 M en 2025), donde las startups ya ganan participación.

### 2.2 Gasto en aplicaciones por categoría (Menlo, 2025) [V] [1]

| Categoría | 2025 | Comentario |
|---|---|---|
| Horizontal (copilotos, plataformas de agentes) | USD 8.400 M (×5,3) | Copilotos USD 7.200 M (86%); **plataformas de agentes solo USD 750 M** (10%) |
| Departamental | USD 7.300 M (×4,1) | Código USD 4.000 M (55%); IT ~700 M; marketing ~660 M; **atención al cliente ~630 M**; diseño 7%; RR.HH. 5% |
| Vertical | USD 3.500 M (×~3) | **Salud ~1.500 M** (escribas clínicos 600 M); **legal 650 M**; herramientas para creadores 360 M; gobierno 350 M |

Participación de startups vs. incumbentes en aplicaciones: 63% startups (36% el año anterior). Por área: ventas 78%, finanzas y operaciones 91% [V] [1].

### 2.3 Agentes de IA, API management y voz (pronósticos de consultoras)

| Mercado | Cifra | Tipo | Fuente |
|---|---|---|---|
| Agentes de IA, 2026 | USD 10.000–15.000 M según la consultora (Grand View 10.900 M; GMI 10.200 M; MarkNtel 10.900 M; Roots 15.000 M) | Pronóstico con definiciones dispares | [S] [4] |
| Proyectos de IA agéntica cancelados antes de fin de 2027 | >40% | Predicción de Gartner (06/2025) | [S] [4] |
| API management, 2030 | USD 20.000–24.000 M (base 2024 ≈ 7.700 M; TCAC 12–18%) | Pronóstico | [S] [5] |
| Agentes de voz con IA | USD 2.540 M (2025) → 35.240 M (2033), Grand View | Pronóstico | [S] [6] |
| IDC sobre agentes | — | [NE] | — |
| Automatización con IA específica para pymes (tamaño global) | — | [NE]: no se halló una cifra seria | — |

**Advertencia:** los "mercados de agentes" de consultoras miden cosas distintas. La cifra de Menlo de plataformas de agentes (USD 750 M en 2025) es mucho menor y sale de gasto declarado. Eso sugiere que buena parte del "mercado de agentes" se compra embebido en productos verticales o de soporte, no como plataforma.

### 2.4 Inversión de riesgo

| Dato | Valor | Fuente |
|---|---|---|
| Venture capital global, 3T 2026 (Crunchbase) | USD 159.000 M; **IA: USD 102.000 M (64%)**. 1T 2026 ≈ 80%; 2T >70% | [S] [7] |
| Acumulado 2026 a septiembre | USD 679.000 M (récord) | [S] [7] |
| Rondas de USD 1.000 M o más en el 3T 2026 | 27 (16 en el 2T) | [S] [7] |
| Desglose por vertical (soporte, legal, salud) | [NE] en fuentes abiertas | — |

---

## 3. Dónde se genera dinero de verdad: startups verticales y de agentes

| Empresa (categoría) | ARR / ingresos | Fecha | Valuación / ronda | Marca | Fuente |
|---|---|---|---|---|---|
| **Sierra** (agentes de soporte, enterprise) | USD 100 M ARR | 21/11/2025 | USD 10.000 M (09/2025) | [V] | [8] TechCrunch |
| Sierra | USD 150 M (02/2026) → ~USD 200 M (05/2026) | 2026 | Serie E de USD 950 M a USD 15.800 M (04/05/2026) | [S] | [9] |
| **Decagon** (agentes de soporte) | >USD 100 M anualizado (Sacra estimaba ~44 M a fines de 2025) | 08/2026 | USD 4.500 M (01/2026) | [S] | [10] |
| **Fin / Intercom** (agente de soporte, precio por resultado) | Fin cerca de USD 100 M ARR; Intercom total ~USD 400 M (est. Sacra) | 08/2026 | Se reporta un acuerdo de compra de Salesforce por ~USD 3.600 M (06/2026) | [S], la compra **no verificada** | [12] |
| **Harvey** (legal) | "Bastante por encima de USD 200 M" (CEO, 03/2026); estimaciones de 300–400 M | 2026 | ~USD 11.000–16.000 M según la ronda | [S] | [13] |
| **EvenUp** (legal, lesiones personales) | ~USD 100 M ARR (estimación de tracker) | 07/2026 | ~USD 2.000 M | [S] débil | [13] |
| **Abridge** (escriba clínico) | ARR [NE]; valuación USD 5.300 M | — | — | [S]/[NE] | [10] |
| **ElevenLabs** (voz) | ~USD 330–350 M a fines de 2025; >USD 500 M a inicios de 2026 | 2026 | Serie D de USD 500 M a USD 11.000 M (02/2026) | [S] | [6] |
| HeyGen (video) | USD 200 M ARR | 25/06/2026 | — | ya verificado en el PDF | PDF |

**Patrones:**
- El ARR grande y rápido se concentra en **atención al cliente** (Sierra, Decagon, Fin), **legal** (Harvey, EvenUp), **salud** (Abridge, escribas) y **voz** (ElevenLabs). Coincide con las categorías de Menlo.
- Los ganadores venden a **empresas medianas y grandes** con contratos de seis o siete cifras y precio por resultado. A la pyme se llega por suites (Fin con mínimo de USD 49,50/mes) o por la vía de los laboratorios.
- Múltiplos de ~80–100× ARR (Sierra) [V/S, 8, 9]: hay exceso de capital y riesgo de corrección.

---

## 4. Tendencias que cambian el juego

### 4.1 MCP y marketplaces de conectores
- Anthropic donó MCP a la **Agentic AI Foundation** (Linux Foundation) en 12/2025, cofundada con Block y OpenAI. Se reporta que A2A, el protocolo de Google, se sumó después [S] [17].
- Adopción: ~97 M de descargas mensuales de los SDK (03/2026, según Anthropic vía terceros); 9.652 registros en el registro oficial (05/2026); registro verificado con auditorías previsto para el 4T 2026 [S] [17]. Las cifras se informan con poca precisión y miden cosas distintas.
- **Implicancia:** el conector genérico (Gmail, QuickBooks, HubSpot, Stripe) ya es infraestructura gratuita. El valor está en conectores a sistemas **no cubiertos** (ERP locales, marketplaces regionales) y en la lógica de negocio encima.

### 4.2 Los laboratorios venden directo a la pyme

| Lanzamiento | Fecha | Qué incluye | Alcance | Fuente |
|---|---|---|---|---|
| **Claude for Small Business** (Anthropic) | 13/05/2026 | ~15 flujos agénticos y 15 *skills* en finanzas, operaciones, ventas, marketing, RR.HH. y atención al cliente. Conectores: QuickBooks, PayPal, HubSpot, Google Workspace, Microsoft 365, DocuSign, Slack, Canva, Square y Stripe. Aprobación humana antes de actuar. Sin costo extra sobre la suscripción | **Inglés, optimizado para EE.UU.** | [S] [15] |
| **ChatGPT Small Business Program** (OpenAI) | 21/07/2026 | *ChatGPT Work* (agente de tareas de varios pasos sobre apps y archivos, desplegado desde el 09/07), GPT-5.6, academias, socios (Intuit, Shopify, Slack, Dropbox, Atlassian, Wix) con *skills* | EE.UU. al inicio. Precio en conflicto (sin costo extra vs. desde USD 20/mes) | [S] [16]. Página de OpenAI con 403 |
| Google (Gemini / Workspace para pymes) | — | — | [NE] en esta ronda | — |

Encuesta citada por Anthropic: el 50% de los dueños de pymes menciona la seguridad de datos como la principal traba para adoptar IA [S] [15].

### 4.3 "Service-as-software" y precio por resultado
- Sequoia ("Services: The New Software", 03/2026): por cada dólar que se gasta en software se gastan seis en servicios. Los proveedores que venden resultados apuntan a ese presupuesto [S] [19].
- General Catalyst destinó USD 1.500 M a comprar empresas de servicios y transformarlas con IA (*roll-ups*) [S] [19].
- Precio por resultado:
  - **Fin**: USD 0,99 por resolución, derivación por procedimiento, descalificación o enrutamiento; USD 9,99 por lead calificado; mínimo de 50 resultados por mes; no se cobra si se deriva sin resultado [V] [11].
  - **Sierra**: cobra por trabajo completado [V] [8].
  - **Crescendo**: cobra por ticket resuelto [S] [19].
- Sacra estima que con el precio por resultado la NRR de Fin pasó de 112% a 146% [S] [12].

### 4.4 Infraestructura y frontera
- La IA ya no es la variable de costo dominante para un caso pyme (ver §5). Pero los proveedores **pueden subir precios**, como hace Google en 12/2026 y 01/2027 [V] [23].
- Los modelos de Anthropic desde la versión 4.7 usan un tokenizador que genera ~30% más tokens para el mismo texto. Por eso, un precio por token igual no implica el mismo costo por tarea [V] [22].

---

## 5. Precios de LLM por millón de tokens (consultados el 30/10/2026)

Tarifa estándar, contexto corto, sin batch. **Costo de referencia** = 10 M de tokens de entrada + 2 M de salida (mismo ejemplo que el PDF) [E: cálculo propio].

### Gama baja (clasificación, extracción, rutas, chat simple)

| Proveedor · modelo | Entrada | Salida | Costo de referencia | Fuente |
|---|---|---|---|---|
| OpenAI gpt-6-luna | 0,10 | 0,50 | **USD 2,00** | [V] [21] |
| Anthropic Claude Haiku 5.5 (≤100k de *prompt*) | 0,10 | 0,50 | **USD 2,00** (+~30% de tokens por tokenizador) | [V] [22] |
| Google Gemini 2.5 Flash-Lite | 0,10 | 0,40 | USD 1,80 | [V] [23] |
| Google Gemini 3.1 Flash-Lite | 0,25 | 1,50 | USD 5,50 | [V] [23] |
| DeepSeek flash (V4.1, fuera de hora pico / pico) | 0,15 / 0,30 | 0,60 / 1,20 | USD 2,70 / 5,40 | [V] [24] |
| Groq gpt-oss-120b | 0,15 | 0,60 | USD 2,70 | [S] [27] |
| Groq Llama 3.1 8B | 0,05 | 0,08 | USD 0,66 | [S] [27] |
| Together Qwen3.8 Flash / gpt-oss-120B | 0,15 | 0,47 / 0,60 | USD 2,44 / 2,70 | [V] [24b] |

### Gama media (agentes con herramientas, documentos complejos)

| Proveedor · modelo | Entrada | Salida | Costo de referencia | Fuente |
|---|---|---|---|---|
| OpenAI gpt-6.1-terra | 1,00 | 5,00 | USD 20 | [V] [21] |
| Anthropic Claude Sonnet 5.5 | 2,00 | 10,00 | USD 40 | [V] [22] |
| Google Gemini 3.8 Flash (hasta el 31/12/2026 → desde el 01/01/2027) | 0,75 → 1,50 | 3,75 → 7,50 | USD 15 → **30** | [V] [23] |
| DeepSeek v4-pro (fuera de hora pico / pico) | 0,66 / 1,32 | 1,98 / 3,96 | USD 10,6 / 21,1 | [V] [24] |
| Mistral Large | 0,50 | 1,50 | USD 8 | [V] [24c] |
| Together GLM-5.3 | 1,40 | 4,40 | USD 22,8 | [V] [24b] |

### Gama alta (razonamiento de frontera)

| Proveedor · modelo | Entrada | Salida | Costo de referencia | Fuente |
|---|---|---|---|---|
| OpenAI gpt-6.1-sol | 2,00 | 10,00 | USD 40 | [V] [21] |
| OpenAI gpt-6-astra | 10,00 | 50,00 | USD 200 | [V] [21] |
| Anthropic Claude Opus 5.5 | 4,00 | 20,00 | USD 80 | [V] [22] |
| Anthropic Claude Fable 5.1 | 10,00 | 50,00 | USD 200 | [V] [22] |
| Google Gemini 4 Argon (hasta el 30/11 → desde el 01/12/2026) | 2,00 → 4,00 | 10,00 → 20,00 | USD 40 → **80** | [V] [23] |
| Together Kimi K3 (pesos abiertos) | 3,00 | 15,00 | USD 60 | [V] [24b] |

**Notas:**
- La caché reduce mucho el costo de los *prompts* repetidos. En Claude Sonnet y Opus 5.5 la lectura de caché cuesta 0,05× el precio de entrada; en DeepSeek, ~2%. El batch da un 50% de descuento en Mistral, Groq y otros [V] [22][24][24c].
- El PDF llama "alta" a gpt-6.1-sol (USD 40). Existe gpt-6-astra, cinco veces más cara; para la gama de un negocio pyme, sol funciona como gama media-alta [E].
- Los pesos abiertos vía Groq y Together **no son mucho más baratos** que la gama baja de los laboratorios. Su ventaja es la portabilidad: si un proveedor sube precios o cierra la cuenta, se cambia de host [E].

---

## 6. Riesgos estructurales

| Riesgo | Evidencia | Fuente |
|---|---|---|
| **Margen bruto bajo** | Nativas de IA ~45% (2025) → 53% proyectado (2026), contra 75–85% del SaaS (ICONIQ). La inferencia equivale al 23% de los ingresos en empresas B2B en etapa de escala. Las startups más rápidas (USD 100 M en ~18 meses) tuvieron ~25% de margen bruto; las más eficientes, ~60% (Bessemer) | [S] [25] |
| Contrapunto | Benchmarkit 2026: la mediana de margen del software sigue por encima del 80%. La presión se concentra en las nativas de IA | [S] [25] |
| **Retención baja (B2B)** | Nativas de IA: GRR 40% y NRR 48% (B2B SaaS NRR mediana: 82%). Con precio **<USD 50/mes**: GRR 23%, NRR 32%. **De USD 50 a 249**: GRR 45%, NRR 61%. **>USD 250/mes**: GRR 70%, NRR 85%, igual que el B2B SaaS. Unas 200 empresas nativas de IA analizadas, con al menos USD 250 k de ARR | [V] [26] ChartMogul, 10/12/2025 |
| **Retención baja (apps de consumo)** | Suscriptores que siguen al año: 21,1% en apps de IA vs. 30,7% en el resto (RevenueCat 2026). Las apps de IA monetizan ~41% más por usuario | [S] [26b] |
| **Absorción por plataformas** | Google (D. Mowry, 21/02/2026): los *wrappers* finos y los agregadores de modelos tienen "la luz de check-engine encendida"; "Stay out of the aggregator business". Casos anecdóticos: la hoja de cálculo con IA quedó desplazada por el análisis de datos de ChatGPT, y el *computer use* pasó a ser función de plataforma | [V] [28]; [S] [29] |
| **Dependencia de plataforma (precios y términos)** | Google duplica precios de Gemini 4 Argon y 3.x Flash en 12/2026 y 01/2027. Los términos de Vapi prohíben productos para terceros (ver INFORME AR). Los laboratorios lanzan funciones encima de sus clientes de API | [V] [23]; INFORME |
| **Burbuja de valuación** | Múltiplos de ~79–100× ARR (Sierra); 64% del VC global va a IA | [V/S] [8][9][7] |
| **Proyectos de agentes que fracasan** | Gartner: más del 40% de los proyectos de IA agéntica en riesgo de cancelación antes de fin de 2027 | [S] [4] |

---

## 7. Qué es defendible para un emprendedor chico y qué está siendo absorbido

| Categoría | Estado | Por qué | Marca |
|---|---|---|---|
| Chatbot o asistente genérico, "ChatGPT para X" sin datos ni integración | **Absorbido** | Claude for Small Business, ChatGPT Work y Meta/WhatsApp lo dan sin costo extra | [S] [15][16]; [V] [28] |
| Agregadores o ruteadores de modelos | **Absorbido / presionado** | Advertencia explícita de Google | [V] [28] |
| Conectores genéricos (Gmail, QuickBooks, Stripe) | **Commodity** | MCP abierto, más de 9.000 servidores, conectores nativos de los laboratorios | [S] [17] |
| Copilotos horizontales de productividad | **De incumbentes** | USD 7.200 M en copilotos dominados por Microsoft, Google y OpenAI | [V] [1] |
| Soporte al cliente para pymes de EE.UU. y Europa | **Saturado arriba** | Fin a USD 0,99, Sierra, Decagon y Gorgias con IA; capital masivo | [V] [11]; [S] [9][10] |
| **Flujos verticales de nicho con integración a sistemas locales o no cubiertos** | **Defendible** | Las startups capturan el 91% del gasto en finanzas y operaciones; los laboratorios cubren primero EE.UU., en inglés, con QuickBooks | [V] [1]; [S] [15] |
| **Servicio con IA cobrado por resultado** (*service-as-software*: operar excepciones, revisión humana, SLA) | **Defendible si se controla el costo humano** | Presupuesto de servicios 6× mayor que el de software; el resultado no lo vende un laboratorio | [S] [19] |
| **Productos verticales de ticket medio (>USD 250/mes)** | **Retención comparable al SaaS** | La retención mejora fuerte con el precio | [V] [26] |
| Herramientas pyme baratas (<USD 50/mes) | **Riesgo alto** | GRR 23% | [V] [26] |
| Voz para pymes (recepcionista) | **En disputa** | Mucho capital (ElevenLabs, Newo), sin líder con más del 10% de participación; las plataformas de voz bajan precios | [S] [6] |

Fuera de la evidencia [E]: la defensa para alguien chico no es el modelo ni el conector. Es (a) datos y reglas de un nicho; (b) integración con sistemas que los grandes no priorizan (idioma, país, ERP local); (c) operar las excepciones con responsabilidad; (d) canal de confianza.

---

## 8. Implicancias para Federico

1. **Confirmación global de la tesis del INFORME:** el mundo paga por resultados verticales, no por "IA". Los ganadores de 2025–2026 (Sierra, Harvey, Abridge, EvenUp) son verticales o de soporte con precio por resultado. Ninguno es un *wrapper* horizontal.
2. **No competir donde ya llegaron los laboratorios.** Claude for Small Business y ChatGPT Work cubren flujos genéricos de pymes estadounidenses con QuickBooks, Stripe, HubSpot y Google. Tienen poca o nula cobertura de español, ARCA, Mercado Libre, Mercado Pago, Tango o Tiendanube. Esa brecha de 12–24 meses es la ventana [E].
3. **Construir *sobre* MCP, no contra MCP.** Publicar los conectores propios (por ejemplo, ML/MP + ARCA) como servidor MCP permite usarlos desde Claude o ChatGPT. Pasa de competir con el agente del laboratorio a ser su conector vertical [E].
4. **Precio:** evitar la franja de menos de USD 50/mes, donde la retención anual es catastrófica [V, 26]. Apuntar a más de USD 150–250/mes vía canal (contadores, agencias), con un componente por resultado al estilo Fin (USD 0,99) [V, 11] cuando el resultado se pueda medir.
5. **Costo de IA:** con la gama baja (~USD 2 por cada 10 M + 2 M tokens), la IA no define el margen. Hay que presupuestar subas: Google duplica precios a fines de 2026. Conviene diseñar desde el día 1 para cambiar de proveedor, con una capa de abstracción y un modelo de pesos abiertos como respaldo vía Groq o Together [V, 21–24][E].
6. **El margen real lo come el humano**, no el token. El margen bruto de las nativas de IA ronda el 50%, y una operación chica con revisión manual puede quedar por debajo [S, 25]. Limitar las horas de excepción por cliente, como ya concluyó el INFORME.
7. **Señal de riesgo:** el 64% del VC global va a IA y las valuaciones son extremas. Si hay corrección, los competidores financiados quiebran o bajan precios de golpe. Un negocio chico, rentable desde el piloto, es más resistente que uno que depende de levantar capital [E].

---

## Fuentes (consultadas el 29–30/10/2026)

1. Menlo Ventures, "2025: The State of Generative AI in the Enterprise", 09/12/2025. https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/ [V]
2. Gartner, "Gartner Forecasts Worldwide AI Spending to Grow 49.5% in 2026", 16/09/2026. https://gartner.com/en/newsroom/press-releases/2026-09-16-gartner-forecasts-worldwide-ai-spending-to-grow-49-point-5-percent-in-2026 (403); cifras vía https://techstrong.ai/features/gartner-global-ai-spending-to-hit-2-7-trillion-in-2026/ [S]
3. CIO Dive, sobre el pronóstico de Gartner de USD 2,59 billones, 19/05/2026. https://www.ciodive.com/news/global-AI-spend-2026/820656/ [S]
4. Resúmenes de pronósticos de agentes (Grand View, GMI, MarkNtel, Roots; Gartner 40%). https://www.raftlabs.com/blog/ai-agents-statistics ; https://gminsights.com/industry-analysis/ai-agents-market ; https://www.marknteladvisors.com/research-library/ai-agent-market.html ; https://www.rootsanalysis.com/ai-agents-market [S]
5. API management: QKS Group https://prnewswire.co.uk/news-releases/api-management-market-disruptions-the-20-28-billion-opportunity-vendors-cant-afford-to-miss-302425651.html ; TechSci https://www.techsciresearch.com/report/api-management-market/3894.html ; GIA https://www.marketresearch.com/Global-Industry-Analysts-v1039/API-Management-33700410 [S]
6. ElevenLabs y voz: https://sacra.com/c/elevenlabs/ ; https://www.cxodigitalpulse.com/?p=53213 ; https://www.softwareseni.com/where-voice-ai-money-is-going-and-what-it-actually-returns [S]
7. Crunchbase, 3T 2026 (vía secundarias): https://fourweekmba.com/ai-crunchbase-q3-2026-159b-venture-27-billion-dollar-rounds-ai/ ; https://aiweekly.co/alerts/crunchbase-logs-27-billion-dollar-rounds-in-q3-2026-as-ai-grabs-102b-or-64-of [S]
8. TechCrunch, "Bret Taylor's Sierra reaches $100M ARR in under two years", 21/11/2025. https://techcrunch.com/2025/11/21/bret-taylors-sierra-reaches-100m-arr-in-under-two-years/ [V: reporte de la compañía en medio primario]
9. Sierra USD 200 M y Serie E: https://cryptobriefing.com/sierra-200m-annualized-revenue-may/ ; https://doolpa.com/news/sierra-950m-series-e-15-8b-valuation-bret-taylor-may-4-2026 [S]
10. Decagon: https://www.revenuememo.com/p/decagon-funding ; https://valueaddvc.com/pulse/company/decagon [S]
11. Fin, precios oficiales. https://fin.ai/pricing (consultado el 30/10/2026) [V]
12. Fin/Intercom ARR y NRR: https://enterprisedna.co/resources/ai-pulse/ai-pulse-2026-08-02-intercom-s-fin-ai-agent-is-nearing-100m-arr-roughly-half-of ; https://sacra.com/research/intercom [S]
13. Harvey / EvenUp: https://newmarketpitch.com/blogs/news/legal-ai-top-revenue ; https://sacra.com/research/harvey-at-150m-arr/ ; https://www.arr.club/evenup [S]
15. Claude for Small Business: https://www.axios.com/2026/05/13/anthropic-claude-small-business-smb ; https://aibusiness.com/generative-ai/anthropic-targets-small-businesses-latest-claude-release ; https://pasqualepillitteri.it/es/news/2526/claude-for-small-business-anthropic-pymes-2026 [S]
16. ChatGPT Small Business Program: https://openai.com/index/introducing-chatgpt-small-business-program (403); https://shellypalmer.com/2026/07/openai-joins-the-race-for-smbs/ ; https://www.shopifreaks.com/openai-launches-a-chatgpt-for-small-business-program-with-training-academies-guides-and-partner-skills-from-shopify-and-intuit/ [S]
17. MCP 2026: https://serpapi.com/blog/the-state-of-mcp-everything-that-changed-in-h1-2026/ ; https://workos.com/blog/everything-your-team-needs-to-know-about-mcp-in-2026 ; https://algeriatech.news/mcp-97-million-installs-2026/ [S]
19. *Service-as-software*: https://www.generalcatalyst.com/stories/the-future-of-services ; https://www.vccafe.com/ai-startups-attacking-the-4-trillion-services-sector/ ; https://trends.vc/service-as-software-solo-operator-pattern-the-61-ratio-liability-as-a-service/ [S]
21. OpenAI API pricing. https://developers.openai.com/api/docs/pricing (30/10/2026) [V]
22. Anthropic pricing. https://platform.claude.com/docs/en/about-claude/pricing (30/10/2026) [V]
23. Google Gemini API pricing. https://ai.google.dev/gemini-api/docs/pricing (30/10/2026) [V]
24. DeepSeek pricing. https://api-docs.deepseek.com/quick_start/pricing/ (30/10/2026) [V]
24b. Together AI pricing. https://www.together.ai/pricing (30/10/2026) [V]
24c. Mistral pricing. https://mistral.ai/pricing (30/10/2026) [V]. Solo publica Mistral Large; Medium y Small [NE]
25. Márgenes de IA (ICONIQ, Bessemer, Benchmarkit vía secundarias): https://www.softwareseni.com/why-ai-gross-margins-are-so-much-lower-than-saas-and-what-that-means-for-your-business/ ; https://enterprisedna.co/resources/ai-pulse/ai-pulse-2026-07-31-ai-native-saas-gross-margins-are-still-running-20-40-points ; https://www.getmonetizely.com/articles/the-economics-of-ai-first-b2b-saas-in-2026-margins-pricing-models-and-profitability [S]
26. ChartMogul / Kyle Poyar, "The SaaS Retention Report: The AI churn wave", 10/12/2025. https://chartmogul.com/reports/saas-retention-the-ai-churn-wave/ [V]
26b. RevenueCat 2026 (vía TechCrunch). https://techcrunch.com/2026/03/10/ai-powered-apps-struggle-with-long-term-retention-new-report-shows [S]
27. Groq (página oficial no legible; precios vía trackers). https://www.morphllm.com/groq-pricing ; https://www.aipricing.guru/groq-pricing/ [S]
28. TechCrunch, "Google VP warns that two types of AI startups may not survive", 21/02/2026. https://techcrunch.com/2026/02/21/google-vp-warns-that-two-types-of-ai-startups-may-not-survive [V: declaración citada]
29. Absorción de *wrappers* (anecdótico): https://startupfortune.com/?p=7352 ; https://dev.to/isahilkapoor/2026-prediction-foundation-models-are-becoming-a-black-hole-for-ai-startups-o52 [S, opinión]

*Numeración con huecos (14, 18 y 20) por fuentes descartadas en la edición.*
