# En qué gastan las grandes empresas de IA (2023–2025)

**Empresas analizadas:** Google (Alphabet/DeepMind), OpenAI (ChatGPT), Anthropic (Claude), Microsoft y Meta
**Período:** 2023, 2024, 2025 (con guías y datos hasta principios de 2026)
**Fecha del informe:** Junio 2026

---

## Resumen ejecutivo

Durante 2023–2025, el gasto de las grandes empresas de IA estuvo **dominado abrumadoramente por la infraestructura de cómputo**: data centers, chips/GPUs y nube. Esta es, por lejos, la mayor categoría de costos — entre el **54% y 62% del costo total** según el análisis de Epoch AI sobre empresas con datos granulares — muy por encima del gasto en personal/talento, que pese a los salarios récord del sector representa **menos del 25%**.

Las conclusiones centrales:

1. **El cómputo le gana al talento.** Aunque los titulares se los llevan los fichajes de $100M, la realidad es que por cada dólar en sueldos se gastan varios dólares en GPUs, data centers y nube.
2. **El capex de los hiperscalers se disparó.** Alphabet, Microsoft, Meta y Amazon, combinados, se proyectan cerca de **~$700 mil millones de capex para 2026**, partiendo de cifras mucho menores en 2023–2024.
3. **OpenAI triplicó todo cada año.** Cómputo, ingresos y compromisos de gasto crecieron ~3x anual. Comprometió **~$1.15 billones (trillion)** en hardware y nube para 2025–2035.
4. **Anthropic creció a un ritmo "loco" (80x).** Gastó ~$4.1B en entrenar modelos y ~$2.7B en inferencia en 2025, con ingresos a un run-rate de $30B en 2026.

---

## 1. La estructura de gasto: cómputo por encima de todo

| Categoría de gasto | % del costo total | Fuente |
|---|---|---|
| **Cómputo** (entrenamiento + inferencia + I+D de cómputo) | **54% – 62%** | Epoch AI |
| **Personal / talento** | **< 25%** | Epoch AI |
| Otros costos (operación, marketing, G&A) | Resto | Epoch AI |

> Epoch AI: *"I+D e inferencia de cómputo juntos representan entre el 54% y 62% de los costos"* y *"pese a que los laboratorios de IA ofrecen algunos de los salarios más altos del sector tecnológico, el gasto en personal es menos del 25% del total"*. La infraestructura resultó más cara que el personal **en todos los casos analizados**.

⚠️ *Caveat clave:* las tres empresas con desglose granular en este análisis son **Anthropic, Minimax y Z.ai**. Solo Anthropic coincide con las empresas objetivo. Para Google y Microsoft no existe un desglose interno público de I+D vs. cómputo vs. salarios — solo cifras agregadas de capex.

---

## 2. Tabla comparativa de gastos por empresa y año

> Cifras en miles de millones de USD. **Capex = capital expenditure total** (predominante pero no exclusivamente IA). Las cifras de OpenAI y Anthropic son estimaciones (Epoch AI / documentos filtrados), no cifras auditadas GAAP.

| Empresa | 2023 | 2024 | 2025 | 2026 (guía) | Qué tipo de gasto |
|---|---|---|---|---|---|
| **Meta** | ~$28B capex | ~$39B capex | $60–65B capex *(luego elevado a $64–72B)* | hasta $125–145B | Data centers, 1.3M+ GPUs, cómputo IA |
| **Alphabet (Google)** | ~$32B capex | ~$52B capex | ~$91B capex | $175–185B *(luego $180–190B)* | Data centers, TPUs propios, nube |
| **Microsoft** | (no desglosado) | (en alza) | (en alza) | $120B+ (año fiscal 2026) | Azure, data centers IA |
| **Amazon** | (no objetivo directo) | — | $131.8B capex | ~$200B | Data centers, chips, robótica, Kuiper |
| **OpenAI** | ~$2B ARR / 200MW | ~$5B cómputo I+D ($3B train + $1.8B inferencia + $1B research) | $20B+ ARR / 1.9GW | — | Cómputo (entrenamiento + inferencia + nube) |
| **Anthropic** | — | — | ~$4.1B entrenamiento + ~$2.7B inferencia | run-rate $30B ingresos | Cómputo de entrenamiento e inferencia |

**Capex combinado hiperscalers (Alphabet + Microsoft + Meta + Amazon):** se proyecta **cerca de $700 mil millones para 2026** (Bloomberg estimó ~$650B).

---

## 3. Desglose por empresa

### 🔵 Meta (Llama)
- **Capex 2024:** ~$39.2B (oficial).
- **Capex 2025:** guía inicial de **$60–65B**, luego elevada a **$64–72B**. Es uno de los mayores saltos interanuales del sector.
- **Hardware:** planeó cerrar 2025 con **más de 1.3 millones de GPUs** (mezcla de Nvidia + silicio propio MTIA) y ~1GW de cómputo en línea.
- **Mega data centers:** construyó instalaciones de **más de 2GW** (Zuckerberg dijo que una cubriría parte significativa de Manhattan), y luego reveló clusters aún mayores de **5GW** (Hyperion y Prometheus).
- **Talento:** lideró la guerra de fichajes (ver sección 4).

### 🔴 Alphabet / Google (DeepMind, Gemini)
- **Capex:** ~$32B (2023) → ~$52B (2024) → ~$91B (2025) → guía **$175–185B para 2026** (literalmente el doble), luego elevada a $180–190B.
- **Gasto principal:** data centers, sus chips propios **TPU** y capacidad de nube (Google Cloud).
- ⚠️ No hay desglose público de I+D vs. cómputo vs. salarios para DeepMind/Google específicamente.

### 🟢 Microsoft
- **Guía capex año fiscal 2026:** **$120B+**, mayormente data centers e infraestructura de IA (Azure).
- **Vínculo con OpenAI:** contrató con OpenAI la venta de **$250B incrementales en servicios Azure** (2025–2030 est.).
- ⚠️ Sin desglose interno público de la composición del gasto.

### 🟣 OpenAI (ChatGPT)
- **Cómputo triplicado cada año:** 200MW (2023) → 600MW (2024) → **1.9GW (fin de 2025)** — un aumento de 9.5x en dos años.
- **Ingresos (ARR) ~10x:** $2B (2023) → $6B (2024) → **$20B+ (2025)**.
- **Desglose de cómputo 2024:** ~$3B entrenamiento + ~$1.8B inferencia + ~$1B investigación amortizada = ~$5B I+D de cómputo.
- **Compromisos a 10 años (~$1.15 billones / trillion, 2025–2035):**

  | Proveedor | Compromiso | Tipo |
  |---|---|---|
  | Broadcom | $350B | Co-desarrollo de chips |
  | Oracle | $300B | Nube (~$60B/año, 2027–2031) |
  | Microsoft (Azure) | $250B | Nube |
  | Nvidia | hasta $100B | Carta de intención **no vinculante** |
  | AMD | $90B | Atado a warrants/objetivos |
  | Amazon AWS | $38B | Nube |
  | CoreWeave | $22B | Nube |

  ⚠️ *Caveat:* "comprometido" exagera lo vinculante. Críticos (WSJ, Yale) señalan **financiamiento circular** y desproporción con sus ingresos (~$13–20B). La escasez de cómputo, según la CFO Sarah Friar, **limitó la monetización**: con más cómputo habrían crecido más rápido.

### 🟠 Anthropic (Claude)
- **Gasto de cómputo 2025:** ~**$4.1B en entrenamiento** + ~**$2.7B en inferencia** (estimación basada en ~40% de margen bruto sobre ~$4.5B de ingresos).
- **Crecimiento de ingresos:** run-rate de ~$9B (fin 2025) → **$30B (2026)**, un crecimiento de **80x anualizado** que Dario Amodei calificó de *"crazy"*, impulsado por demanda empresarial (1,000+ clientes pagando >$1M/año).
- ⚠️ El run-rate de $30B **no es ingreso GAAP auditado**; OpenAI argumentó internamente que está sobreestimado ~$8B por reportar ingresos de nube en bruto vs. neto.

---

## 4. La guerra del talento (real, pero secundaria)

Aunque el gasto en personal es <25% del total, la competencia por talento alcanzó cifras récord en 2025, liderada por **Meta**:

- **$200M+** a Ruoming Pang (ex jefe de modelos fundacionales de Apple).
- Una oferta de **$18M rechazada** por un investigador.
- Supuestos **bonos de fichaje de $100M**, según afirmó Sam Altman en un podcast (cifra disputada por Meta).
- Paquetes multimillonarios para hacer *poaching* de OpenAI.

👉 **Conclusión:** estas cifras son llamativas pero **ilustrativas de individuos**, no la nómina total. El verdadero peso del gasto sigue siendo el cómputo.

---

## 5. Advertencias metodológicas (leer antes de citar)

1. **Granularidad desigual:** el único desglose porcentual por categoría viene de Epoch AI y cubre Anthropic/Minimax/Z.ai — **no** Google/Microsoft/Meta directamente. Para estos solo hay capex agregado.
2. **Capex ≠ solo IA:** las cifras de capex de los hiperscalers son **totales** (incluyen robótica, satélites Kuiper, infraestructura general), predominante pero no exclusivamente IA.
3. **Guías superadas:** varias guías 2025/2026 fueron revisadas al alza después (Meta 2025: $60–65B→$64–72B; Alphabet 2026: $175–185B→$180–190B).
4. **Estimaciones vs. auditado:** las cifras de OpenAI y Anthropic son estimaciones de Epoch AI sobre documentos filtrados, no cifras auditadas. Los run-rates (ARR) no son ingresos GAAP.
5. **Compromisos no vinculantes:** el "$1.15 billones" de OpenAI mezcla contratos firmes con cartas de intención y acuerdos atados a warrants.
6. **Datos 2023 escasos:** las fuentes son fuertes para 2024–2026 pero más débiles en cifras concretas de 2023.

---

## 6. Preguntas abiertas (lo que NO se pudo determinar con certeza)

- ¿Cuál es el desglose interno (I+D vs. cómputo vs. salarios vs. marketing) **específico de Google/DeepMind y Microsoft**? Solo hay capex agregado.
- ¿Cuánto gastan exactamente en **marketing y costos operativos (G&A)**? Apenas aparece en las fuentes, dominadas por cómputo.
- ¿Cuál fue el **gasto real ejecutado en 2023** por empresa? Datos escasos.
- ¿Cuál es el **gasto total agregado en talento en dólares** (no solo % ni anécdotas)?

---

## Fuentes principales (verificadas)

- **Epoch AI** — *Company spending breakdown* (desglose de costos): https://epoch.ai/data-insights/company-spending-breakdown — *(fuente primaria)*
- **DataCenterDynamics** — OpenAI CFO: 1.9GW de cómputo a fin de 2025: https://www.datacenterdynamics.com/en/news/openai-cfo-says-company-ended-2025-with-19gw-of-compute-scaled-revenue-at-same-speed/
- **Tom's Hardware** — Meta: data center 2GW, 1.3M GPUs, $65B en 2025: https://www.tomshardware.com/tech-industry/artificial-intelligence/meta-to-build-2gw-data-center-with-over-1-3-million-nvidia-ai-gpus-invest-usd65b-in-ai-in-2025
- **CNBC** — Capex combinado de Google/Microsoft/Meta/Amazon: https://www.cnbc.com/2026/02/06/google-microsoft-meta-amazon-ai-cash.html
- **VentureBeat** — Anthropic: run-rate de $30B, crecimiento 80x: https://venturebeat.com/technology/anthropic-says-it-hit-a-30-billion-revenue-run-rate-after-crazy-80x-growth
- **Tomasz Tunguz** — Compromisos de hardware de OpenAI 2025–2035: https://tomtunguz.com/openai-hardware-spending-2025-2035/ *(blog, corroborado por CNBC y otros)*
- **TechCrunch** — Guerra de talento de Meta: https://techcrunch.com/2025/06/27/meta-is-offering-multimillion-dollar-pay-for-ai-researchers-but-not-100m-signing-bonuses/
- **Fortune** — $200M a Ruoming Pang: https://fortune.com/2025/07/11/how-much-ai-salary-meta-zuckerberg-200-million-compensation/

---

*Informe generado mediante investigación multi-fuente con verificación adversarial: 6 ángulos de búsqueda, 24 fuentes consultadas, 36 afirmaciones extraídas, 25 verificadas con votación 3-vías (25 confirmadas, 0 refutadas).*
