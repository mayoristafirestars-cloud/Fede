# 06 · Verificación de hechos, modelo económico para Argentina y go-to-market

Revisión crítica del informe "Negocios digitales con APIs: oportunidades y validación" (29/10/2026).
Fuentes consultadas el 29 y 30/10/2026. Los números entre corchetes remiten a la lista de fuentes del final.

**Límites de esta revisión**
- Se agotó el cupo de búsquedas web de la sesión (200 consultas compartidas entre agentes). Por eso quedaron sin buscar dos temas: los requisitos regulatorios para obtener un número local de Twilio en Argentina y la cantidad de usuarios de LinkedIn en Argentina.
- Algunas páginas oficiales bloquearon la descarga directa (error 403): openai.com/policies, pipedrive.com, mercadopago.com.ar/ayuda. En esos casos se usó el texto que muestran los buscadores o una copia del mismo documento en otro sitio, y así se indica en cada caso.

---

## A. Verificación de hechos

### A.1 Precios y datos de proveedores

| # | Afirmación del PDF | Estado | Valor actual / matiz | Fuente |
|---|---|---|---|---|
| 1 | Smith.ai: recepción con IA desde USD 150/mes por 75 llamadas; Enterprise USD 500 por 300 | **Confirmado** | Pro USD 150: 75, 150 o 300 llamadas (USD 2,00 / 1,80 / 1,67 por llamada; excedente USD 2,50 / 2,30 / 2,17). Enterprise USD 500: 300 llamadas, con escalones de 500 y 1.000+. Existe un plan Free de 25 llamadas. | [1] |
| 2 | Smith.ai: más de 5.000 negocios y 20 millones de llamadas | **Confirmado con matiz** | La página dice "5,000+ businesses" y "20 million calls … in the past 10 years". Ese acumulado de 10 años incluye la época de recepcionistas humanos, así que no mide la demanda de IA. | [1] |
| 3 | AgencyAnalytics: USD 20 por cliente al mes con pago anual; más de 85 integraciones | **Precio confirmado; integraciones distinto** | Plan Core: USD 20 por cliente al mes con pago anual (ahorro de 20%). Hoy declara **90+** integraciones, no 85+. Para 25 clientes o más hay precio por volumen a cotizar. | [2] |
| 4 | Pipedrive: más de 100.000 equipos; desde USD 14 por asiento con pago anual | **Confirmado** | Lite: USD 14 por asiento con pago anual, sin IVA. La cifra de "más de 100.000 empresas" aparece en un comunicado de abril de 2026. La propia empresa dice "empresas", no "equipos". | [3][4] |
| 5 | Gorgias: USD 10 por 50 tickets y USD 60 por 300; automatización aparte | **Confirmado** | Starter: USD 10, 50 tickets. Basic: USD 60 mensual o USD 50 con pago anual, 300 tickets. Excedente: USD 0,40 por ticket. El agente de IA está incluido en todos los planes, pero cada interacción cuesta USD 0,90 (anual) o 1,00 (mensual) y cuenta como ticket. | [5] |
| 6 | Textract (Oregon): 1.000 páginas de OCR USD 1,50; formularios y tablas USD 65 | **Confirmado** | DetectDocumentText cuesta USD 0,0015 por página. Los USD 65 por 1.000 páginas suman formularios (USD 0,05) y tablas (USD 0,015) por página. No es un precio único publicado. | [6] |
| 7 | Document AI Invoice Parser: USD 0,10 por documento de 1 a 10 páginas | **Confirmado** | USD 0,10 por unidad de hasta 10 páginas. Las solicitudes síncronas aceptan como máximo 10 páginas; por lote, hasta 200. Hay descuento a USD 0,09–0,08 con un plan de ahorro de 3 años. | [7] |
| 8 | Vapi: hosting USD 0,05/min; 1.000 minutos = USD 82 a 129 | **Confirmado** | Hosting USD 50 + Deepgram USD 10 + LLM USD 8–45 + ElevenLabs USD 15–24 + transporte USD 0. Aparte se cobran paquetes de soporte: Core USD 29/mes; Pro 10% del hosting con mínimo de USD 999/mes. | [8] |
| 9 | Twilio Argentina: entrada local USD 0,0107/min; número USD 8/mes | **Confirmado** (tabla de agosto de 2026) | Número gratuito (0800): USD 0,2582/min + USD 25/mes. Salientes a celular: USD 0,3528/min. No se pudo verificar si hay números locales disponibles ni qué requisitos regulatorios piden (se agotó el cupo de búsquedas). | [9] |
| 10 | HeyGen API de traducción: audio USD 0,57/min; lip sync rápido 0,81; preciso 1,50 | **Confirmado con reservas** | El centro de ayuda de HeyGen publica esos valores para uso por API. G2 y un revendedor muestran tarifas por segundo distintas (≈ USD 2–4/min). La página de precios redirige a la consola y no se pudo leer. | [10][11] |
| 11 | HeyGen anunció USD 200 millones de ARR en junio de 2026 | **Confirmado** | Anuncio del 25/06/2026: duplicó el ARR en 8 meses, desde USD 100 M. Es una cifra declarada por la empresa, sin auditar. | [12][13] |
| 12 | OpenAI: 10 M tokens de entrada + 2 M de salida = USD 2 con "GPT 6 Luna" y USD 40 con "GPT 6.1 Sol" | **Confirmado** | gpt-6-luna: USD 0,10 entrada / 0,50 salida, así que 1 + 1 = USD 2. gpt-6.1-sol: USD 2 / 10, así que 20 + 20 = USD 40. El PDF omite **gpt-6.1-terra** (USD 1 / 5, es decir USD 20 en el mismo ejemplo). gpt-6-astra cuesta USD 10 / 50 (USD 200). | [14] |
| 13 | Google Ads cambió el acceso en septiembre de 2026 hacia proyecto Cloud y OAuth | **Confirmado** | Los developer tokens se retiraron el 09/09/2026. El nivel de acceso ahora depende del proyecto Cloud de las credenciales OAuth y el encabezado del token se ignora. Hay un error conocido (AUTHORIZATION_ERROR) en proyectos que subieron de nivel después del 09/09. Según una fuente secundaria, Basic y Standard ahora exigen verificación de marca. | [15][16] |
| 14 | Tiendanube: 71,5% del ecosistema relevado vendió por WhatsApp en 2025 | **Confirmado con matiz** | Tiendanube cita su reporte NubeCommerce 2026: "71,5% de los emprendedores en **Argentina** usó WhatsApp como canal de venta en 2025", segundo canal después de Instagram. La misma página lo presenta también como "% de tiendas". Otros países: México 68%, Chile 60,1%, Colombia 84,1%. No se encontró el reporte original. | [17] |

### A.2 Términos contractuales sobre reventa

| Plataforma | Afirmación del PDF | Estado | Detalle |
|---|---|---|---|
| OpenAI | Permite integrar el servicio en aplicaciones, pero no revender cuentas | **Confirmado** (el documento se leyó a través de una copia indexada; openai.com devolvió 403) | §2.2: se puede integrar en aplicaciones propias para usuarios finales. §3.1: prohíbe revender o alquilar el acceso a la cuenta. §3.3: prohíbe comprar, vender o transferir claves de API. [18] |
| Vapi | Licencia no sublicenciable para uso propio, modificable por acuerdo | **Confirmado, y es más restrictivo de lo que dice el PDF** | §2(a): licencia "non-exclusive, non-transferable, non-assignable, non-sublicensable, revocable". §2(d)(1): solo "your own use"; prohíbe licenciar, vender o alquilar. §2(d)(14) **prohíbe usar el servicio para desarrollar "templates or products for third-party"**. Actualizado el 14/09/2026. Tiene un programa de Solution Partners sin condiciones públicas de reventa. [19][20] |
| Retell | Restringe ciertas reventas o capas intermediarias | **Confirmado, con una contradicción** | §10.1(e) prohíbe revender la voz generada como producto aislado. §10.1(f) prohíbe construir una "intermediary layer on top of the Services". Actualizado el 25/10/2026. Sin embargo, su **programa de partners** dice que los partners pueden "sell or bundle" Retell para sus clientes y lista partners de marca blanca. Esto se resuelve pidiendo confirmación por escrito. [21][22] |
| Windsor.ai | Licencia interna e intransferible; aprobación escrita para incorporarlo en otro sitio | **Confirmado** | §6: uso "limited to your internal business purposes, non-transferable"; ítem 5: no se puede "frame, mirror or otherwise incorporate" el servicio en otro sitio sin autorización escrita. [23] |

### A.3 Precios de LLM para comparar (el ejemplo del PDF: 10 M tokens de entrada + 2 M de salida, tarifa estándar)

| Proveedor / modelo | USD por millón de tokens (entrada / salida) | Costo del ejemplo | Fuente |
|---|---|---|---|
| Gemini 2.5 Flash-Lite | 0,10 / 0,40 | **USD 1,80** | [25] |
| Claude Haiku 5.5 (prompts ≤100k) | 0,10 / 0,50 | **USD 2,00** | [24] |
| OpenAI gpt-6-luna | 0,10 / 0,50 | USD 2,00 | [14] |
| Gemini 3.1 Flash-Lite | 0,25 / 1,50 | USD 5,50 | [25] |
| Gemini 3.6 / 3.8 Flash (promoción hasta el 31/12/2026) | 0,75 / 3,75 | USD 15 (USD 30 desde el 01/01/2027) | [25] |
| OpenAI gpt-6.1-terra | 1 / 5 | USD 20 | [14] |
| Claude Sonnet 5.5 / Sonnet 5 | 2 / 10 | USD 40 | [24] |
| OpenAI gpt-6.1-sol | 2 / 10 | USD 40 | [14] |
| Gemini 4 Argon (hasta el 30/11/2026) | 2 / 10 | USD 40 (USD 80 desde el 01/12/2026) | [25] |
| Claude Opus 5.5 | 4 / 20 | USD 80 | [24] |
| OpenAI gpt-6-astra | 10 / 50 | USD 200 | [14] |

Notas:
- Anthropic aplica 50% de descuento en la Batch API y cobra las lecturas de caché a 0,05–0,1× el precio de entrada.
- Los modelos Claude 4.7 en adelante usan un tokenizador que genera alrededor de **30% más tokens** para el mismo texto [24]. Por eso el precio por token no se puede comparar directamente con el de otros proveedores.
- Dos precios de Gemini **suben** en diciembre de 2026 y enero de 2027.
- **Conclusión:** el costo de inferencia de gama baja ya es casi nulo en los tres proveedores (alrededor de USD 2 en el ejemplo). La IA no es la variable relevante del margen; sí lo son las horas humanas, la telefonía y las licencias de conectores. Lo mismo que vuelve barata la IA quita la barrera técnica para entrar (ver la sección D).

---

## B. Revisión del modelo económico (páginas 7 y 8)

### B.1 Las cuentas del PDF están bien hechas

| | Documentos | Voz | Reportes |
|---|---|---|---|
| Contribución = abono − técnico − horas − cobro − reposición | 299 − 50 − 100 − 14,95 − 12 = **122,05** ✓ | 399 − 215 − 40 − 19,95 − 12 = **112,05** ✓ | 149 − 25 − 40 − 7,45 − 8 = **68,55** ✓ |
| Equilibrio = 1.100 / contribución, redondeado hacia arriba | 9,01 → 10 ✓ | 9,82 → 10 ✓ | 16,05 → 17 ✓ |
| Horas en equilibrio (clientes × h + 40 de administración) | 50 + 40 = 90 ✓ | 20 + 40 = 60 ✓ | 34 + 40 = 74 ✓ |
| Sensibilidad | 10 h: 22,05 → 50 clientes, 540 h ✓ | USD 0,35/min: −37,95 ✓ | USD 99: 21,05 → 53 clientes, 146 h ✓ |

No hay errores aritméticos. Los problemas están en los **supuestos**:

1. **Abonos en dólares de mercado estadounidense.** USD 299/mes equivale a unos ARS 452.000 al mayorista de ~1.513 (19/10/2026) [26]. Como referencia, Xubio y Colppy, los sistemas contables pyme locales, rondan ARS 6.000–25.000/mes según una guía de terceros (≈ USD 4–17) [27]. Un abono de USD 299 es entre 18 y 75 veces el software contable del mismo cliente. El dato de esa guía no está confirmado en las páginas oficiales.
2. **CAC de USD 300 con 4% de baja mensual implica una relación LTV/CAC de alrededor de 10×**, muy optimista. Stripe ubica el CAC de SaaS B2B para pymes y empresas medianas entre USD 300 y 5.000 [28]: el PDF usa el piso. No se encontró un benchmark de CAC específico para Latinoamérica; el único dato regional es un período de recupero del CAC 32% menor que en EE. UU. (State of SaaS LatAm 2024) [29].
3. **Baja de clientes (churn) del 4%.** Los benchmarks globales para pymes van de 3% a 5% mensual [30], con una mediana de 4,7% en el primer trimestre de 2026 [31]. No se encontró un dato para Latinoamérica. En Argentina pesa además la mortalidad de empresas: el número de empleadores cayó 2,6% interanual en febrero de 2026, con 17 meses seguidos de baja [32]. Es razonable estresar el modelo con 6%.
4. **Comisión de cobro del 5%.** El link de pago de Mercado Pago Argentina cobra 6,29% con acreditación al instante, 4,39% a 10 días, 3,39% a 18 días y 1,49% a 35 días. La página aclara que no incluye impuestos ni retenciones y que el costo varía por provincia [33]; un blog de terceros dice "+ IVA" [34]. Con IVA, 4,39% a 10 días da ≈ 5,3%. El 5% del PDF es razonable con Mercado Pago, pero en B2B argentino es habitual cobrar por **transferencia contra factura**, con costo cercano a cero (a cambio, más gestión de cobranza).
5. **USD 20/h** está en línea con el mercado freelance argentino: Workana muestra full stack concentrado entre USD 20 y 30/h; Freelancer.com, USD 25–40/h; Upwork, USD 5–15/h (Infotechnology) [35]. Como costo de contratar operación, un sueldo de full stack de USD 1.800 brutos/mes (Coderhouse, 2026 [36]) equivale a ≈ USD 11/h. La revisión de documentos no requiere un desarrollador, así que USD 12/h es una alternativa razonable para operación delegada; no se encontró un dato de sueldo administrativo.
6. **Lo que no incluye el modelo** (lo reconoce en parte): IVA, Ingresos Brutos (alícuota provincial, no verificada aquí), impuestos y percepciones por pagar servicios en USD desde Argentina (no verificado), y el riesgo de cobrar en pesos con costos en dólares. Inflación de septiembre de 2026: 1,9% mensual y 33,4% interanual (INDEC según la prensa) [37]. Banda cambiaria: techo de ≈ ARS 1.951 en octubre, ≈ 29% por encima del mayorista de mediados de mes [26].

### B.2 Supuestos alternativos para Argentina (todos son hipótesis, no pronósticos)

| Supuesto | PDF | Alternativa AR | Base |
|---|---|---|---|
| Abono documentos / voz / reportes | 299 / 399 / 149 | 150–199 / 250–299 / 99–149 | Bandas inferiores del propio PDF, ajustadas a la referencia de precios del software local [27] |
| Costo técnico de documentos | 50 (Document AI) | 25 | Un LLM barato (≈ USD 0,10/0,50 por millón [14][24][25]) más infraestructura. Además, ARCA "Mis Comprobantes" entrega gratis los datos de las facturas electrónicas recibidas [38] |
| Costo técnico de voz | 0,20/min + 15 | 0,15/min + 15 | Vapi USD 0,082–0,129 [8] + Twilio AR USD 0,0107 [9] + margen |
| Volumen de voz | 1.000 min | 500 min | Volumen más realista para una pyme (supuesto propio) |
| Hora de operación | 20 | 20 (propia) o 12 (delegada) | [35][36] |
| Comisión de cobro | 5% | 5,3% (Mercado Pago a 10 días + IVA) o 0% (transferencia) | [33][34] |
| Churn mensual | 4% | 6% | [30][31][32] |
| CAC | 300 / 200 | 500 / 300 | Piso de Stripe [28] más ciclo de confianza con contadores (supuesto propio) |
| Costos fijos | 1.100 | 1.100 | Sin cambio |

### B.3 Escenarios recalculados para Argentina (USD por cliente y por mes)

| Escenario | Abono | Técnico | Horas | Cobro | Reposición | **Contribución** | **Equilibrio** | Horas/mes en equilibrio | LTV/CAC |
|---|---|---|---|---|---|---|---|---|---|
| PDF Documentos | 299 | 50 | 5h×20 | 5% | 300×4% | **122,05** | 10 | 90 | 11,2 |
| PDF Voz | 399 | 215 | 2h×20 | 5% | 300×4% | **112,05** | 10 | 60 | 10,3 |
| PDF Reportes | 149 | 25 | 2h×20 | 5% | 200×4% | **68,55** | 17 | 74 | 9,6 |
| **AR-A Documentos** (precio AR, horas propias) | 150 | 25 | 5h×20 | 5,3% | 500×6% | **−12,97** | no hay | — | 0,6 |
| **AR-A Voz** (1.000 min) | 250 | 165 | 2h×20 | 5,3% | 500×6% | **1,72** | 640 | 1.320 | 1,1 |
| **AR-A Reportes** | 99 | 25 | 2h×20 | 5,3% | 300×6% | **10,74** | 103 | 246 | 1,6 |
| **AR-B Documentos** (3 h delegadas a 12) | 150 | 25 | 3h×12 | 5,3% | 500×6% | **51,03** | 22 | 106 | 2,7 |
| **AR-B Voz** (500 min, delegada a 12) | 250 | 90 | 2h×12 | 5,3% | 500×6% | **92,72** | 12 | 64 | 4,1 |
| **AR-B Reportes** (precio 149, delegada a 12) | 149 | 25 | 2h×12 | 5,3% | 300×6% | **74,09** | 15 | 70 | 5,1 |
| **AR-C Documentos** (199, 3 h propias, transferencia) | 199 | 25 | 3h×20 | 0% | 500×6% | **84,00** | 14 | 82 | 3,8 |
| **AR-C Voz** (299, 500 min, transferencia) | 299 | 90 | 2h×20 | 0% | 500×6% | **139,00** | 8 | 56 | 5,6 |
| **AR-C Reportes** (149, transferencia) | 149 | 25 | 2h×20 | 0% | 300×6% | **66,00** | 17 | 74 | 4,7 |

LTV/CAC = (abono − técnico − horas − cobro) / churn / CAC.

**Lectura**
- Con precios argentinos y 5 horas de revisión por cliente, **documentos no cierra** (contribución negativa). Solo es viable si baja el tiempo de revisión (≤3 h) y si el precio se acerca a USD 200 o la operación se delega.
- **Voz con 1.000 minutos a USD 250 no deja margen.** Hay que limitar el volumen incluido (500 min) o cobrar el exceso por minuto.
- **Reportes a USD 99 no es viable** (103 clientes).
- En los escenarios AR-B y AR-C, la relación LTV/CAC queda entre 2,7× y 5,6×. Es más realista que el 10× del PDF, pero todavía depende de que el CAC sea de USD 300–500, cosa que no está medida.

---

## C. Go-to-market en Argentina desde cero

### C.1 Tamaño del universo (empresas con empleados registrados)

| Dato | Valor | Fuente / fecha |
|---|---|---|
| Empresas empleadoras registradas (SIPA) | **525.538** (abril de 2025) | UCEMA, set. 2025 [39] |
| Con menos de 10 empleados | 84% ≈ 441.000 | [39] |
| Pequeñas (10–50) | 13% ≈ 68.000 | [39] |
| De 51 a 100 | 2% ≈ 10.500 | [39] |
| Con más de 100 | ≈ 9.939 | [39] |
| Empleadores según la SRT | 512.357 (nov. 2023) → 26.448 menos a marzo de 2026 (≈ 485.909 implícito) | CEPA, vía prensa [40] |
| Caída interanual de empleadores | −13.163 (−2,6%) entre febrero de 2025 y febrero de 2026 | Fundar/SRT en Bloomberg Línea, 23/05/2026 [32] |
| Matriculados en el CPCE de CABA | ≈ 76.000 (62.000 habilitados), dato de 2022 | El Cronista [41] |

- **Advertencia:** la cifra de "606.000 mipymes" del GPS de Empresas que circula en notas fechadas en 2026 proviene de un artículo de **julio de 2019** [42]. Está desactualizada.
- No se encontró la cantidad de estudios contables ni de partners de Tango.
- **Implicancia:** el equilibrio requiere entre 8 y 22 clientes, lo que equivale a 0,01–0,03% de las ≈ 78.000 empresas de 10 a 100 empleados. **El tamaño del mercado no es la restricción; la restricción es la distribución y la confianza.**

### C.2 Canales concretos (de mayor a menor encaje para documentos)

| Canal | Por qué | Evidencia / acción concreta |
|---|---|---|
| **Consejos profesionales de Ciencias Económicas** | Los contadores son quienes cargan comprobantes y los que recomiendan herramientas | En 2026 hubo jornadas con sesiones de IA aplicada: CPCE Santa Fe, Sur (Cañada de Gómez, 30/10/2026); Jóvenes Profesionales (Rosario, 08/08/2026); CPCE Córdoba, pre-congreso en Villa María (07/10/2026) [43][44]. Acción: proponerse como disertante o hacer una demostración en comisiones de "tecnología" o "jóvenes", que suelen ser el acceso más barato |
| **Implementadores y partners de ERP (Tango y otros)** | Tienen la relación con el cliente y la integración | Axoft (Tango) fue adquirida por Vela LatAm; tiene más de 300 empleados y fuerte presencia en pymes y estudios contables [45]. Hay demanda directa: un pedido en Workana busca leer facturas con ChatGPT y cargarlas en Tango [46]. No se encontró el número de partners. Acción: ofrecerse como subcontratista "marca blanca del partner" con un reparto de ingresos (20–30%, supuesto propio) |
| **Sistemas contables en la nube (Colppy, Xubio, Dux, SOS Contador)** | Pueden ser socios o competidores | Todos importan "Mis Comprobantes" de ARCA [38], y Xubio ya tiene importación de comprobantes con IA desde 2025 [47]. Acción: apuntar a los documentos que ARCA **no** cubre (remitos, órdenes de compra, extractos, recibos, comprobantes del exterior) |
| **Cámaras sectoriales** | Acceso a verticales | eCommerce Day Argentina (CACE, 27/08/2026) [48]; IAB Argentina, comisión directiva 2026–28 e IAB Now (agosto) [49]. Interact y AAP reúnen agencias (cifras de socios desactualizadas o sin verificar) [49]. No se buscaron datos de cámaras como CAME o de sectores puntuales (se agotó el cupo) |
| **Comunidades de agencias** (para reportes) | Las agencias boutique son el comprador | IAB, Interact, AAP [49]. Partners de Tiendanube: la alianza con Meta para ventas automatizadas por WhatsApp [50] también es competencia |
| **LinkedIn y correo en frío** | Escala, con baja conversión | Benchmarks globales, sin datos para Latinoamérica: correo en frío 3,43% de respuesta promedio (Instantly 2026), mediana 1,5% (Woodpecker), 0,45% (Belkins) [51]. LinkedIn: 26% de aceptación y 7,2% de respuesta entre quienes aceptan [52]. Cálculo con esas tasas y un supuesto propio de 50% de respuestas que pasan a reunión: 15 entrevistas exigen ≈ 900 correos o ≈ 1.600 invitaciones |
| **Grupos de WhatsApp profesionales y referidos** | La confianza pesa mucho en Argentina | No hay benchmark. Acción: un contador "campeón" por zona que refiera clientes a cambio de una comisión recurrente |

### C.3 Tácticas de outreach B2B en Argentina (recomendaciones, no verificadas con datos locales)
- **Diagnóstico gratuito de 30 minutos con datos del propio cliente**, por ejemplo: "te muestro cuántos comprobantes de Mis Comprobantes no están cargados en tu sistema". Es lo opuesto a una demo con datos ficticios.
- **Precio en pesos, ajustable cada trimestre por IPC**, con un piso en USD para la parte tecnológica. Cobro por transferencia contra factura.
- **Piloto pago en pesos de bajo monto** (equivalente a USD 100–200), con criterio de éxito por escrito, tal como propone el PDF.
- **Secuencias de varios toques** (correo, LinkedIn y llamada): los seguimientos explican el 42% de las respuestas [53].

---

## D. Lo que el PDF no considera y debería

1. **En Argentina, el OCR de facturas fiscales vale menos.** Las facturas electrónicas recibidas ya están en ARCA "Mis Comprobantes" (Excel/CSV, identificadas por CAE) y Colppy, Dux, SOS Contador y YoFacturo las importan [38]. El caso de uso "Nanonets → facturas" del PDF es estadounidense. En Argentina el valor está en la conciliación (lo informado a ARCA contra lo cargado y lo pagado), en los documentos no fiscales y en la imputación a cuentas o centros de costo.
2. **Los propios sistemas ya incorporan IA.** Xubio (de Visma) importa comprobantes con IA [47]. Gorgias incluye un agente de IA en todos sus planes [5]. Tiendanube y Meta lanzaron venta automatizada por WhatsApp [50]. HeyGen vende su API directamente [10]. No se encontró un anuncio de IA de Axoft/Tango.
3. **Los agentes de los propios laboratorios de IA.** Anthropic lanzó *Claude for Small Business* el 13/05/2026: 15 flujos con conectores a QuickBooks, PayPal, HubSpot y otros, incluidos el cierre de mes, el seguimiento de facturas impagas y el flujo de caja, sin cargo extra sobre la licencia [54]. Hoy se enfoca en QuickBooks y EE. UU., pero desplaza la barrera hacia la integración local (ARCA, Tango, Mercado Pago). Esa es justamente la defensa posible.
4. **Commoditización del costo técnico.** La inferencia barata cuesta alrededor de USD 2 en el ejemplo del PDF con OpenAI, Anthropic o Google (sección A.3). Cualquier competidor replica el componente de IA; la defensa es la operación, la integración local y la distribución por canal.
5. **Tipo de cambio e impuestos.** No hay escenario de devaluación: el techo de la banda está ≈ 29% arriba del mayorista [26]. Faltan IVA, Ingresos Brutos, la elección entre monotributo y responsable inscripto, y el costo de pagar servicios en USD desde Argentina. Los tres últimos no se verificaron en esta revisión.
6. **Los términos de Vapi son más restrictivos de lo que dice el PDF.** La cláusula §2(d)(14) prohíbe crear productos o plantillas para terceros [19]. Retell, en cambio, tiene un programa de partners que permite "sell or bundle" [22], en tensión con su §10.1(f) [21]. Es un dato práctico: hoy Retell parece la vía más clara para un servicio de agencia, siempre con confirmación escrita.
7. **WhatsApp en Argentina.** Desde abril de 2026 Meta factura en pesos en Argentina, según un proveedor de soluciones de WhatsApp (BSP) [55]. Las tarifas por mensaje varían entre fuentes (marketing ≈ USD 0,027–0,066) [55]. Hay versiones no confirmadas de un cambio desde el 01/10/2026 que haría pagas las respuestas [56]. Esto refuerza la advertencia del PDF.
8. **Marco legal de voz en Argentina.** Rige el registro "No Llame" (Ley 26.951), y hay proyectos para imponer un prefijo obligatorio a las llamadas comerciales (3218-D-2025) [57]. Las grabaciones se rigen por interpretación judicial, sin ley expresa, según una fuente secundaria [58]. Se aplica la Ley 25.326 de datos personales.
9. **Contexto de demanda en contracción.** El número de empleadores formales viene bajando: −26.448 entre noviembre de 2023 y marzo de 2026 [40]. La pyme argentina tiene menos presupuesto, pero también más presión para reemplazar horas administrativas. Este doble efecto no aparece en el PDF.
10. **Supuestos del PDF que no se pudieron contrastar:** usuarios de LinkedIn en Argentina, condiciones de número local de Twilio, tarifa de suscripciones de Mercado Pago, cantidad de partners de Tango y de estudios contables.

---

## Fuentes (consultadas el 29 y 30/10/2026)

1. Smith.ai, AI Receptionist pricing — https://smith.ai/pricing/ai-receptionist
2. AgencyAnalytics, Pricing — https://agencyanalytics.com/pricing
3. Pipedrive, Pricing (vía snippet de búsqueda; la página devolvió 403) — https://www.pipedrive.com/en/pricing
4. Pipedrive Newsroom (comunicado de abril de 2026) — https://www.pipedrive.com/newsroom ; ver también https://automationatlas.io/tools/pipedrive/
5. Gorgias, Pricing — https://www.gorgias.com/pricing
6. AWS, Amazon Textract pricing — https://aws.amazon.com/textract/pricing/
7. Google Cloud, Document AI pricing — https://cloud.google.com/products/document-ai/pricing
8. Vapi, Pricing — https://vapi.ai/pricing
9. Twilio, Voice pricing Argentina (tabla de agosto de 2026) — https://www.twilio.com/en-us/voice/pricing/ar
10. HeyGen Help Center, Premium credits (tabla de API) — https://help.heygen.com/en/articles/10060327-heygen-premium-credits-explained
11. G2, HeyGen API pricing — https://www.g2.com/articles/heygen-api-pricing
12. HeyGen Blog, "HeyGen surpasses $200M ARR" (25/06/2026) — https://www.heygen.com/blog/heygen-surpasses-200m-arr
13. Upstarts Media, "HeyGen's AI Video Reaches $200M in ARR" — https://www.upstartsmedia.com/p/exclusive-heygen-200m-arr-without-burn
14. OpenAI, API pricing — https://developers.openai.com/api/docs/pricing
15. Google Ads API, API policy (retiro de developer tokens el 09/09/2026) — https://developers.google.com/google-ads/api/docs/api-policy
16. PPC Land, "Google drops developer tokens from Ads API access decisions" — https://ppc.land/google-drops-developer-tokens-from-ads-api-access-decisions/
17. Tiendanube Blog, "Cómo vender por WhatsApp en 2026" — https://www.tiendanube.com/blog/como-vender-por-whatsapp/ ; https://www.tiendanube.com/blog/whatsapp-business/
18. OpenAI Services Agreement (copia en PDF) — https://cdn.openai.com/osa/openai-services-agreement.pdf ; https://openai.com/policies/services-agreement/
19. Vapi, Terms of Service (14/09/2026) — https://vapi.ai/terms-of-service
20. Vapi, Partnerships — https://vapi.ai/partnerships
21. Retell AI, Terms of Service (25/10/2026) — https://www.retellai.com/terms-of-service
22. Retell AI, Partners Program — https://www.retellai.com/partners-program ; https://docs.retellai.com/ecosystem/partner-program
23. Windsor.ai, Terms of Service §6 — https://windsor.ai/terms-of-service/
24. Anthropic, Claude pricing — https://platform.claude.com/docs/en/about-claude/pricing
25. Google, Gemini API pricing — https://ai.google.dev/gemini-api/docs/pricing
26. Economis (mayorista $1.513, 19/10/2026) — https://economis.com.ar/dolar-mayorista-cerro-semana-por-encima-de-los-1-500/ ; iProUP (techo de banda) — https://www.iproup.com/economia-digital/71536-el-dolar-mayorista-marca-su-mayor-distancia-del-techo-oficial-en-16-meses
27. Guía de Software, facturación electrónica en Argentina (precios de Xubio y Colppy, terceros) — https://www.guiadesoftware.com/blog/mejor-software-facturacion-argentina
28. Stripe, "CAC in SaaS" — https://stripe.com/ie/resources/more/cac-in-saas
29. Nasdaq, "LatAm Tech Weekly: State of SaaS LatAm 2024" — https://www.nasdaq.com/articles/latam-tech-weekly:-state-of-saas-latam-2024
30. Fungies, SaaS Market Statistics 2026 (datos de Optifai) — https://fungies.io/saas-market-statistics-2026/
31. Visionary Marketing, SaaS churn benchmarks 2026 — https://visionary-marketing.co.uk/blog/saas-churn-benchmarks-2026
32. Bloomberg Línea (23/05/2026), datos de la SRT vía Fundar — https://www.bloomberglinea.com/latinoamerica/argentina/hay-mas-o-menos-empresas-argentinas-en-2026-esto-revelan-los-datos-oficiales/
33. Mercado Pago Argentina, Link de pago — https://www.mercadopago.com.ar/herramientas-para-vender/link-de-pago
34. YoFacturo, "Link de pago Mercado Pago (2026)" — https://yo-facturo.com/blog/link-de-pago-mercado-pago/
35. El Cronista/Infotechnology, freelancers en Argentina — https://www.cronista.com/infotechnology/actualidad/freelancers-en-argentina-cuanto-ganan-por-hora-y-que-profesiones-son-las-mejores-y-peores-pagas
36. Coderhouse, sueldo de desarrollador full stack en Argentina — https://www.coderhouse.com/ar/sueldos/sueldo-desarrollador-full-stack-argentina-2025
37. Finanzas Digital, inflación de septiembre de 2026 — https://finanzasdigital.com/inflacion-argentina-septiembre-2026-indec-ipc-acumulada/ ; iProUP — https://www.iproup.com/finanzas/72300-indec-confirma-inflacion-de-19-en-septiembre-categorias-con-mayor-aumento
38. Importación de ARCA "Mis Comprobantes": Colppy — https://intercom.help/Colppy/es/articles/3181130-importar-tus-facturas-desde-mis-comprobantes-recibidos-afip ; Dux — https://intercom.help/duxsoftware/es/articles/8489755-como-importar-compras-de-arca ; SOS Contador — https://contadoresenred.com/sos-contador-ya-permite-la-importacion-de-mis-comprobantes-emitidos-y-recibidos/ ; YoFacturo — https://yo-facturo.com/docs/accounting/received-invoices/
39. UCEMA, Indicadores PyMEs (set. 2025, datos SIPA a abril de 2025) — https://ucema.edu.ar/sites/default/files/2025-09/IndicadoresUCEMA_PyMEs092025_0.pdf
40. CEPA vía Análisis Digital (16/06/2026) — https://www.analisisdigital.com.ar/economia/2026/06/16/informe-de-cepa-desde-la-asuncion-de-milei-se-perdieron-mas-de-370-mil-empleos-registrados-en-el-pais ; Perfil — https://www.perfil.com/noticias/cordoba/empleo-y-empresas-la-gestion-de-milei-acumula-la-perdida-de-30600-empleadores-y-411000-trabajadores.phtml
41. El Cronista, reelección en el CPCECABA (76.000 matriculados) — https://www.cronista.com/informacion-gral/gabriela-russo-fue-reelecta-como-presidenta-del-consejo-profesional-de-ciencias-economicas
42. Sitio Andino (artículo del 04/07/2019, GPS de Empresas) — https://www.sitioandino.com.ar/n/297904-2-de-cada-3-trabajadores-se-emplea-en-una-mipyme
43. CPCE Santa Fe, 24ª Jornada del Sur de Santa Fe — https://www.consejo.org.ar/noticias/2026/participa-de-la-24a-jornada-de-profesionales-en-ciencias-economicas-del-sur-de-santa-fe ; 23ª Jornada de Jóvenes Profesionales — https://consejo.org.ar/noticias/2026/participa-de-las-230-jornada-provincial-de-jovenes-profesionales-en-ciencias-economicas
44. CPCE Córdoba, pre-congreso en Villa María — https://web.cpcecba.org.ar/?p=70043
45. Bruchou & Funes de Rioja, adquisición de Axoft por Vela LatAm — https://bruchoufunes.com/en/we-advised-on-vela-latams-acquisition-of-axoft-argentina/
46. Workana, "API para Tango Software" — https://www.workana.com/es/job/appi-para-tango-sofware
47. Descubre.vc, Xubio (IA para importar comprobantes; adquisición por Visma) — https://www.descubre.vc/xubio-saas
48. Ecosistema Startup, eCommerce Day Argentina 2026 — https://ecosistemastartup.com/ecommerce-day-argentina-2026-ia-y-comercio-unificado-lideran-el-ecosistema/
49. Mercado, comisión directiva de IAB Argentina 2026–2028 — https://mercado.com.ar/talento-y-liderazgo/iab-argentina-definio-su-consejo-directivo-2026-2028-con-mariano-filarent-como-presidente ; Cancillería, Directorio Argentina Creativa — https://cancilleria.gob.ar/es/directorios-argentina-creativa/marketing-publicidad-y-comunicacion
50. Mercado, "Tiendanube, protagonista de 2025" (alianza con Meta para WhatsApp) — https://mercado.com.ar/protagonistas/tiendanube-protagonista-de-2025-sus-tiendas-facturaron-casi-2-billones
51. Webtonic, estadísticas de correo en frío en B2B SaaS — https://www.webtonic.io/blog/b2b-saas-and-tech-cold-email-outbound-statistics
52. Founder Reports, benchmarks de ventas outbound (datos de Belkins) — https://founderreports.com/outbound-sales-benchmarks/
53. Martal, estadísticas de correo en frío B2B — https://martal.ca/b2b-cold-email-statistics/
54. SiliconANGLE / Technobezz, lanzamiento de Claude for Small Business (13/05/2026) — https://siliconangle.com/?p=754848 ; https://www.technobezz.com/news/anthropic-launches-claude-for-small-business-with-15-ready-to-run-agentic-workflows
55. Chattigo, cuánto cobra WhatsApp Business por mensaje — https://blog.chattigo.com/whatsapp-business/cuanto-cobra-whatsapp-business-por-mensaje ; Meta, precios — https://developers.facebook.com/docs/whatsapp/pricing
56. Mercately (cambio del 01/10/2026, no confirmado) — https://blog.mercately.com/?p=30248
57. HCDN, proyecto 3218-D-2025 — https://www4.hcdn.gob.ar/dependencias/dsecretaria/Periodo2025/PDF2025/TP2025/3218-D-2025.pdf
58. RecordingLaw, leyes de grabación en Argentina — https://www.recordinglaw.com/es/world-laws/world-recording-laws/argentina-recording-laws/
