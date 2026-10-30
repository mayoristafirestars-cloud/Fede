# Negocios digitales con APIs en el mundo: investigación completa

Informe consolidado, 30/10/2026. Continúa la investigación argentina (`../INFORME.md`) y el PDF *Negocios digitales con APIs: oportunidades y validación*. Seis agentes investigaron en paralelo, con fuentes públicas consultadas el 30/10/2026. Cada informe de detalle (`detalle/G1` a `G6`) trae fuentes numeradas con URL y fecha, y marca cada dato como [V] verificado en fuente primaria, [S] secundaria, [E] estimación o [NE] no encontrado.

> No es asesoramiento legal, fiscal ni de inversión. Los tamaños de mercado de consultoras varían mucho entre sí y se usan solo como contexto.

---

## 1. Conclusión en una página

**Lo que se encontró en Argentina se repite en el mundo.**

1. **La IA es barata e igual para todos.** La gama baja cuesta USD 0,10 por millón de tokens de entrada y 0,50 de salida en OpenAI (gpt-6-luna) y Anthropic (Claude Haiku 5.5), y Google y DeepSeek están en el mismo rango [V]. Nadie gana por el modelo ni por la extracción: leer un PDF cuesta desde USD 0,00125 por página (LlamaParse) [V].
2. **La factura electrónica obligatoria le quita valor al OCR de facturas en todos lados.** Bélgica (04/2026), Polonia y Francia (2026–27), Alemania (2027–28), España (VERI*FACTU 2027) [S]. Lo que queda por resolver son los documentos sin estructura: facturas del exterior, fletes, aduana, comprobantes de entrega.
3. **La plata está en lo vertical y en el soporte cobrado por resultado.** Las empresas gastaron USD 37.000 M en IA generativa en 2025; USD 3.500 M en aplicaciones verticales, casi el triple que en 2024 [V, Menlo]. Sierra y Decagon superan los USD 100 M anuales; Intercom Fin cobra USD 0,99 por resolución [V/S].
4. **Los laboratorios ya venden directo a la pyme**, pero en inglés y con integraciones de EE.UU.: Claude for Small Business (13/05/2026) y el programa pyme de OpenAI con ChatGPT Work (21/07/2026) [S]. Lo genérico y horizontal se está muriendo: Jasper, los "chat con PDF", Relay (cerró en 08/2026), Ryze AI (su tasa de cierre cayó de 70% a 20% cuando Claude y Manus sumaron conectores de Meta Ads) [S].
5. **El precio decide la retención.** Los productos de IA de menos de USD 50/mes retienen 23% del ingreso al año; los de más de USD 250 retienen ≈ 70%, como el SaaS clásico [V, ChartMogul]. Margen bruto típico de productos de IA: 45–60%, contra 80% del software tradicional [S].
6. **La ventaja de Federico es doble:** conocer integraciones regionales que las herramientas globales ignoran (Mercado Libre, fiscos latinoamericanos) y tener costo argentino (USD 12–20 por hora) vendiendo a precios de EE.UU. o España, donde las agencias de IA cobran USD 500–4.500 por mes [S].

### Ranking global para Federico

| # | Oportunidad | Dónde | Por qué | Riesgo principal |
|---|---|---|---|---|
| **1** | **Margen real y conciliación fiscal para vendedores de marketplaces regionales**, vendido a estudios contables y agencias que manejan muchas cuentas | Argentina → **México** (Mercado Libre y Amazon MX) | Sellerboard, A2X, Link My Books y TrueProfit no cubren Mercado Libre, Allegro, Bol ni Zalando [V]. En México, desde 01/2026 las plataformas retienen IVA e ISR a personas físicas: mismo patrón "marketplace + fisco" que en Argentina [S] | Brasil ya está poblado (GE Finance, Koncili, TrackCash) [S]. Confirmar si la API de ML México entrega retenciones por orden [NE] |
| **2** | **Implementación productizada de IA para estudios contables**: puesta en marcha fija + abono mensual para operar flujos sobre las herramientas que el estudio ya usa | Argentina → pymes hispanas de EE.UU. y España | Mejor puntaje de la matriz (3,70/5). La principal barrera de los contadores es "no sé cómo implementarlo". Cuando Claude o ChatGPT sacan una función, el servicio la incorpora en lugar de morir | Es servicio, no software: escala con horas. Un operador solo consigue 3–6 clientes el primer año [S] |
| **3** | **Costeo de importaciones a partir de documentos**, asentado en QuickBooks o Xero | EE.UU., Reino Unido, Australia (y Argentina como piloto) | Existen calculadoras de aranceles (Zonos), calculadoras manuales (TariffCenter USD 49) y apps de prorrateo con carga manual (Landara USD 49/mes), pero nadie que lea los documentos y deje el costo por producto asentado en el sistema contable [V/NE] | QuickBooks cobra las lecturas de su API (Silver USD 300/mes) y Xero exige plan Plus (AUD 245/mes) para publicar en su tienda; conviene una app que sobre todo escriba [V/S] |
| **4** | **Servicio "hecho por vos" en horario de EE.UU.**: revisión de cuentas a pagar para construcción o administración de propiedades, o recepción IA para negocios hispanos | EE.UU. y España | Los precios de EE.UU. arreglan la economía que en Argentina daba negativa. En home services se pierde el 27% de las llamadas y menos del 3% deja mensaje [V, Invoca] | Recepción IA genérica ya cuesta USD 29–150 (Dialzara, Rosie, Goodcall, Smith.ai) y ya viene en español [V]. Hay que vender servicio y cumplimiento, no la herramienta |

**Evitar a nivel mundial:** conversores de factura electrónica en la UE (mercado de proveedores grandes que se compran entre sí y ≈ 150 plataformas aprobadas en Francia a 0–40 € por mes), recepcionista IA genérica en EE.UU., herramientas de rentabilidad para Amazon o Shopify de EE.UU. (Sellerboard USD 19–79 con 20.000+ vendedores), reporting genérico de agencias, WhatsApp genérico, localización de video y cualquier producto de menos de USD 50/mes.

---

## 2. Panorama global (G1)

| Dato | Valor | Marca |
|---|---|---|
| Gasto empresarial en IA generativa 2025 | USD 37.000 M (3,2× 2024); USD 19.000 M en aplicaciones; USD 3.500 M en verticales (salud 1.500 M, legal 650 M) | [V] Menlo, encuesta a 495 decisores de EE.UU. |
| Participación de startups | 63% del gasto en aplicaciones; 91% en finanzas y operaciones | [V] |
| Gasto total en IA 2026 (Gartner) | USD 2,59–2,7 billones, casi todo infraestructura | [S] |
| Agentes de IA 2026 / API management 2030 | USD 10–15 mil M / USD 20–24 mil M; definiciones distintas entre consultoras | [S] |
| Capital de riesgo hacia IA | 64% del total global | [S] |
| MCP | Bajo la Linux Foundation; registro oficial con 9.000+ servidores | [S] |

**Precios de modelos por millón de tokens (entrada/salida), 30/10/2026 [V]**

| Gama | Modelos | Precio |
|---|---|---|
| Baja | gpt-6-luna, Claude Haiku 5.5, Gemini Flash-Lite, DeepSeek flash | ≈ 0,10 / 0,50 |
| Media | gpt-6.1-terra / Claude Sonnet 5.5 | 1 / 5 – 2 / 10 |
| Alta | Claude Opus 5.5 / gpt-6-astra, Claude Fable 5.1 | 4 / 20 – 10 / 50 |

Google duplica el precio de Gemini 4 Argon el 01/12/2026 y de Gemini 3.x Flash el 01/01/2027 [V]. Conclusión: diseñar para poder cambiar de proveedor desde el primer día.

**Qué hacer con los grandes:** publicar los conectores propios (ARCA, Mercado Libre, Mercado Pago, Tango) como servidor MCP para que se usen desde Claude o ChatGPT, en vez de competir con ellos.

---

## 3. Documentos y back-office (G2)

- **Mercado IDP:** entre USD 1.400 M y 10.000 M en 2025 según la consultora; no sirve para decidir [S].
- **Precios de extracción:** LlamaParse desde USD 0,00125/página, Reducto USD 20 cada 1.000 páginas, Veryfi USD 0,16 por factura, Rossum desde USD 18 mil/año [V].
- **Factura electrónica:** Alemania obliga a emitir desde 01/2027 si se factura más de 800 mil € y a todas desde 2028; Francia, pymes desde 09/2027; Bélgica desde 04/2026 con multas de 1.500 a 5.000 €; España VERI*FACTU 2027; UE (ViDA) 07/2030; EE.UU. voluntario (DBNAlliance) [S, VATupdate 28/10/2026]. En Alemania la federación de oficios (ZDH, 1.926 empresas) dice que las pymes no llegan a 2027. Aun así es mal punto de entrada: Sovos, Vertex/ecosio, Avalara y Storecove dominan.
- **Verticales ya financiados:** logística (Loop, Serie C USD 95 M), construcción (Handle, USD 27 M), aduanas (Amari AI, USD 4,5 M), administración de propiedades (Wrk, USD 1.000 de implementación + USD 250/mes). En seguros, ACORD regala su extractor a sus miembros desde 06/2026 [V/S].
- **Tiendas de apps contables:** Xero eliminó la comisión del 15% y desde 03/2026 cobra por conexiones y datos que salen, exige plan Plus y prohíbe entrenar IA con datos de su API. QuickBooks cobra lecturas (Builder gratis hasta 500 mil; Silver USD 300/mes), no escrituras [V/S].

---

## 4. Voz con IA y agencias de automatización (G3)

- **Demanda medida por capital:** Avoca USD 1.000 M de valuación, HappyRobot USD 1.200 M, Netic USD 450 M, Slang.ai Serie B USD 36 M [V/S]. Las cifras de mercado (USD 2.700 M en 2025 según Market.us) varían varias veces entre consultoras [S].
- **Precios minoristas ya comprimidos:** Dialzara desde USD 29, Rosie 49, Goodcall 79, My AI Front Desk 99, Smith.ai 150 por 75 llamadas; ServiceTitan ≈ USD 2,75 por llamada [V/S].
- **Costo técnico:** USD 0,07–0,31/min en Retell, USD 0,045/min + LLM en HighLevel, USD 0,08/min en ElevenLabs [V].
- **Plataformas para agencias:** HighLevel USD 497/mes para revender + agente IA USD 50–97 por subcuenta; My AI Front Desk marca blanca desde USD 500/mes; Synthflow eliminó el plan de agencias; Vapi no publica marca blanca; Retell tiene partners pero no marca blanca [V].
- **"AI automation agency":** negocio real pero de servicios; 3–6 clientes el primer año para un operador solo, márgenes de menos del 30% en un caso; las cifras de éxito vienen de quienes venden cursos [S].
- **Regulación:** EE.UU. FCC 24-17 (TCPA aplica a voces IA, sobre todo salientes); California SB 1001 (el bot debe identificarse) y riesgo de demandas colectivas tras *Ambriz v. Google* (2025). UE: art. 50 del AI Act (avisar que es IA) rige desde el 02/08/2026. España: Ley 10/2025 exige opción humana desde el 28/12/2026 solo a grandes empresas y servicios básicos [V/S].

---

## 5. Ecommerce, mensajería y soporte (G4)

- **Rentabilidad para vendedores (EE.UU.):** Sellerboard USD 19–79/mes y 20.000+ vendedores; A2X desde USD 29 por canal; TrueProfit USD 35–200 [V]. Ninguna menciona Mercado Libre, Allegro, Bol, Zalando ni Kaufland.
- **Brasil:** GE Finance, Koncili, TrackCash, Letzee, UpSeller y GoSmarter ya cubren Mercado Livre y Shopee [S]. Entrar solo con socio local.
- **México:** retenciones de IVA 8% e ISR 2,5% a personas físicas desde 01/2026 → saldos a favor y conciliación en Excel [S; confirmar tasas en LISR/LIF 2026].
- **Tiendas de apps:** Shopify no cobra comisión sobre el primer USD 1 M acumulado de por vida y 15% después; ≈ 17.500 apps. Amazon canceló en 05/2026 el cargo anual de USD 1.400 y el cobro por llamadas de SP-API [V/S].
- **WhatsApp, mensaje de servicio desde 01/10/2026** (después de 1.000 gratis por número): India USD 0,0014, Brasil 0,0068, México 0,0085, España 0,020, Indonesia 0,025, Argentina 0,026 [V para BR/MX/AR; S para el resto]. La política 4.7 de Meta permite IA de soporte del propio comercio, no entrenar un modelo compartido.
- **Soporte por resultado:** Intercom Fin USD 0,99, Zendesk 1,50–2,00, Gorgias 0,90–1,00, Siena ≈ USD 750/mes + 0,90 por ticket. Sierra vale ≈ USD 15.800 M y Decagon 4.500 M [V/S]. El espacio chico: integrar transportistas y fiscos locales.
- **Cuña secundaria:** posventa por WhatsApp con transportistas locales en México y Brasil, a USD 0,40–0,70 por pedido resuelto [E], después de validar la principal.

---

## 6. Vender al mundo desde Argentina (G5)

**Orden de mercados sugerido:** EE.UU. (36,2 M de pymes; ≈ 496.000 empresas hispanas con empleados [V]) → España (3,31 M [V]) → México (≈ 7 M de establecimientos [S]) → Reino Unido (5,7 M [V]) → Chile, Colombia, Perú → Brasil al final. Para el producto de marketplaces (ranking #1), México va primero por el encaje con Mercado Libre.

| Tema | Recomendación |
|---|---|
| Cobrar servicios | Seguir en monotributo, Factura E, cobro por ACH/SEPA con Payoneer o Wise a cuenta en USD propia |
| Cobrar SaaS | **Paddle** como Merchant of Record (5% + USD 0,50; maneja IVA y sales tax). Que acepte vendedores argentinos sale de un ejemplo de su API [S]: confirmarlo por escrito. **Stripe no soporta Argentina** [V]; Lemon Squeezy migra a Stripe Managed Payments, que tampoco [V] |
| LLC en EE.UU. | Solo cuando un cliente o canal la exija: USD 500 (Atlas) + USD 100/año agente + USD 400/año Delaware; Form 5472 anual con multa de USD 25.000 si no se presenta; BOI ya no aplica a sociedades de EE.UU. (14/08/2026) [V] |
| Estonia / SL España | No convienen sin mudarse, por riesgo fiscal |
| Impuestos indirectos | UE: OSS desde el primer euro vendiendo a consumidores; EE.UU.: nexo típico USD 100.000 por estado [S]. Un Merchant of Record lo resuelve |
| GDPR | Argentina tiene adecuación: no hacen falta SCCs para recibir datos de la UE. Sí DPA y probablemente representante en la UE (art. 27) |
| AI Act | Art. 50 (avisar que es IA, marcar contenido generado) vigente desde 02/08/2026; el alto riesgo se postergó al 02/12/2027 [S] |
| EE.UU. privacidad / SOC 2 | 20 estados con ley de privacidad [S]. SOC 2 cuesta USD 25.000–60.000 el primer año: no antes de que un cliente lo pida [S] |
| Canales | Shopify (0% hasta USD 1 M), HubSpot (3 instalaciones activas para listar), Upwork (0–15%), AWS Marketplace (3%, no sirve para pymes) [V/S] |

---

## 7. Casos, modelos y métricas (G6)

- **Casos con ingresos verificados por procesador (TrustMRR):** GojiberryAI USD 424 mil MRR, 1Lookup (API de validación) 270 mil, Cometly (atribución) 198 mil, AEO Engine (agencia) 178 mil [V; sin márgenes]. Los micro-SaaS de IA que se venden en marketplaces facturan entre cientos y pocos miles de dólares por mes, y se venden a 1–2× el ingreso anual [S].
- **LatAm:** casos argentinos (Facturitas, Talentum, Prometheo) solo publican usuarios, no ingresos [NE].
- **Monetización:** el modelo híbrido (fijo + uso) pasó del 27% al 41% de las empresas en un año; solo el 5% cobra principalmente por resultado [S, Poyar 2025]. El esquema del PDF (puesta en marcha + abono con volumen) va en línea.
- **Benchmarks:** repago del CAC 16–18 meses de mediana; prueba gratis sin tarjeta convierte ≈ 18%, freemium ≈ 2,6%; retención neta mediana 101% [S]. El 6% de baja mensual usado para Argentina coincide con la mediana mundial del tramo USD 50–249.

### Matriz de decisión (escala 1–5; pesos: demanda 25%, riesgo de plataforma 20%, competencia 15%, barrera para un fundador solo 15%, precio 15%, venta desde Argentina 10%)

| Oportunidad | Puntaje |
|---|---|
| N1 · Implementación productizada de IA para estudios contables | **3,70** |
| N2 · Rentabilidad multi-cuenta ML/MP para agencias y estudios | **3,50** |
| 7 · Conciliación de lectura (genérica) | 3,10 |
| 4 · CRM vertical (como módulo) | 2,85 |
| N3 · API de validación fiscal argentina para software houses | 2,80 |
| 1 · Documentos verticales (OCR de facturas) | 2,60 |
| 5 · Soporte ecommerce | 2,60 |
| 2 · Voz entrante | 2,55 |
| 3 · Reporting de agencias (genérico) | 2,15 |
| 6 · Ventas por WhatsApp (genérico) | 2,15 |
| 8 · Localización de video | 1,90 |

Son juicios del analista sobre la evidencia, no una medición. Cambiando los pesos, las tres primeras siguen arriba.

---

## 8. Argentina vs. mundo

| Pregunta | Argentina | Mundo |
|---|---|---|
| ¿Leer facturas con IA? | No: ARCA ya las entrega estructuradas | No: la factura electrónica obligatoria hace lo mismo en la UE |
| ¿Dónde está el hueco? | Mercado Libre + Mercado Pago + ARCA + banco | Marketplaces y fiscos regionales que las herramientas globales ignoran (ML México, Allegro, Bol) |
| ¿Precio viable? | USD 150–250 apenas cierra | USD 250+ entra en el tramo de buena retención; servicios a USD 500–4.500 |
| ¿Voz con IA? | Demanda dudosa (se escribe más) | Demanda probada pero precio minorista comprimido |
| ¿Cómo cobrar? | Transferencia, ARS ajustado o USD al BNA | Factura E + Payoneer/Wise; Paddle para SaaS |
| Ventaja de Federico | Integraciones locales | Integraciones regionales + costo argentino con precios de EE.UU./España |

---

## 9. Estrategia recomendada: 6 meses

**Principios:** vender al intermediario que maneja muchas cuentas (estudios, agencias), cobrar ≥ USD 250 por mes, arrancar como servicio productizado y convertir en software solo lo que se repita en tres o más clientes, validar con pilotos pagos, diseñar para cambiar de modelo de IA.

**Meses 1–3: validar en Argentina (plan del informe argentino).** Rentabilidad y conciliación Mercado Libre / Mercado Pago para agencias y estudios. Construir los conectores con independencia del modelo y publicarlos también como servidor MCP.

**Meses 2–3, en paralelo: generar ingresos en USD.** 1–2 clientes de EE.UU. o España con un servicio productizado (implementación de IA para un estudio contable hispano, o revisión de cuentas a pagar en QuickBooks), conseguidos por referidos, LinkedIn o Upwork. Facturar con Factura E y cobrar por Payoneer/Wise.

**Meses 4–6: México.** Llevar el producto de marketplaces a ML y Amazon MX, con foco en las retenciones de IVA/ISR 2026, vendido a despachos contables y agencias. Antes: confirmar qué entrega la API de ML México por orden y las tasas de retención vigentes. Si Argentina no validó, probar el costeo de importaciones sobre QuickBooks/Xero.

**Frenar si:** nadie paga el piloto, la revisión humana supera 3 h por cliente y mes, o cada cliente pide un producto distinto.

---

## 10. Datos no confirmados

- Si Paddle acepta vendedores argentinos (confirmar por escrito).
- Si la API de Mercado Libre México entrega retenciones por orden, y las tasas de retención para empresas en México.
- Tarifas de los marketplaces de QuickBooks, Xero, Zapier, Make y GoHighLevel; precios de Doola y Firstbase.
- Tarifas de WhatsApp para India, Indonesia y España en fuente oficial; programa de partners de TikTok Shop.
- Precios de Klippa, Hyperscience, Extend, Podium, Ruby, Housecall Pro, Numa, Helium 10 Profits, BeProfit, Lifetimely, Koncili, GE Finance, TrackCash.
- Lista oficial de estados de EE.UU. con consentimiento de dos partes para grabar; texto del Omnibus 2026/1744 en el Diario Oficial de la UE.
- Informe 2025 de Acquire.com y márgenes publicados de agencias de automatización.

---

## Archivos de detalle

| Archivo | Tema | Fuentes |
|---|---|---|
| `detalle/G1-panorama.md` | Mercado global de IA y APIs, precios de modelos, riesgos | numeradas |
| `detalle/G2-documentos.md` | Documentos, factura electrónica, verticales, tiendas contables | 30 |
| `detalle/G3-voz-agencias.md` | Voz con IA, agencias, regulación EE.UU./UE | 36 |
| `detalle/G4-ecommerce-soporte.md` | Marketplaces, WhatsApp por país, soporte por resultado | numeradas |
| `detalle/G5-vender-al-mundo.md` | Mercados, estructura, cobro, cumplimiento, canales | 34 |
| `detalle/G6-casos-modelos.md` | Casos, monetización, métricas, matriz de decisión | 39 |
