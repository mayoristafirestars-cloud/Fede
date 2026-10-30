# G2. Automatización documental y back-office a nivel mundial

Investigación del 30/10/2026 para Federico. Continúa el PDF *Negocios digitales con APIs* (29/10/2026) y el informe argentino (`investigacion/INFORME.md`). Todas las fuentes se consultaron el 30/10/2026; la fecha que figura al lado de cada una es la del dato, cuando se conoce.

**Marcas:** [V] verificado en fuente primaria (página del proveedor, organismo o comunicado propio) · [S] fuente secundaria (prensa, agregador, blog de un proveedor sobre otro) · [E] estimación propia · [NE] no encontrado o no confirmado.

> No es asesoramiento legal ni fiscal. Los calendarios de facturación electrónica cambian seguido; antes de decidir hay que confirmarlos en la web del organismo fiscal de cada país.

---

## 0. Conclusión en 8 puntos

1. **El hallazgo argentino se repite en el mundo.** Donde la factura electrónica estructurada se vuelve obligatoria (Bélgica 2026, Polonia 2026, Francia 2026–27, Alemania 2027–28, España 2027–28, Emiratos 2027), la factura recibida llega como XML y **leer facturas fiscales con OCR pierde valor**. El valor se corre a la conversión, la validación, la integración con ERPs chicos y a los documentos que siguen sin estructura: facturas del exterior, fletes, aduana, remitos y documentos de seguros o construcción. [E, basado en 2.1]
2. **La extracción ya es commodity y barata.** LlamaParse cobra desde USD 0,00125 por página en el parseo básico; Reducto, USD 10 cada 1.000 páginas (parse) y USD 20 (extract). Veryfi cobra USD 0,16 por factura, con un mínimo de USD 500 por mes. Rossum arranca en USD 18.000 por año. [V, 1.2] Nadie gana por "leer el PDF".
3. **El tamaño del mercado IDP no sirve para decidir.** Según la consultora, el mercado va de USD 1.400 M a 10.000 M en 2025 y el crecimiento anual, del 10% al 33%. [S, 1.1]
4. **Las cuñas verticales que tienen financiamiento** (logística, construcción, aduanas, seguros) están ocupadas por startups con USD 3 a 95 M levantados y apuntan a empresas medianas y grandes. En seguros, ACORD regala su propio extractor a sus miembros desde 06/2026. [V/S, 3]
5. **Los marketplaces contables cambiaron las reglas.** Xero eliminó la comisión del 15% y desde 03/2026 cobra por conexiones y por GB de datos, y publicar en su App Store exige el plan Plus (AUD 245 por mes). Intuit cobra por las llamadas de lectura "CorePlus" (Builder es gratis hasta 500 mil; Silver USD 300 por mes). [V/S, 4]
6. **Costo de importación (landed cost):** existe a nivel global, pero en dos formas que no son la del hallazgo argentino. Una es el cálculo de aranceles en el checkout del comercio electrónico transfronterizo (Zonos). La otra son módulos de prorrateo dentro de sistemas de inventario o apps chicas (Landara, desde USD 49 por mes con 10 cálculos). No se encontró un producto que **lea los documentos** (factura del proveedor extranjero, despacho o entrada aduanera, factura de flete) y deje el prorrateo por SKU asentado en Xero o QuickBooks. [S/NE, 5]
7. **La facturación electrónica es una ola real, pero la dominan proveedores grandes** (Sovos, Vertex/ecosio, Avalara, Comarch, Quadient, Storecove). En Francia hay unas 150 plataformas aprobadas que cobran de 0 a 40 € por mes a la micro y pequeña empresa. Para un integrador chico desde Argentina la puerta es estrecha: conectores con ERPs locales, en el idioma del país y con soporte local. [S, 2]
8. **Recomendación:** probar una app de **costeo de importaciones a partir de documentos** para pymes importadoras que usan QuickBooks Online o Xero (EE.UU., Reino Unido y Australia), aprovechando lo aprendido en Argentina. Como alternativa, una **mesa de excepciones de cuentas a pagar (AP) en horario de EE.UU.** para un vertical (construcción o administración de propiedades) en QuickBooks. Detalle en la sección 7.

---

## 1. Mercado de Intelligent Document Processing (IDP)

### 1.1 Tamaño y crecimiento

| Fuente | Tamaño | Crecimiento anual compuesto | Marca |
|---|---|---|---|
| Grand View Research | USD 12.350 M en 2030 | 33,1% (2025–2030) | [S] [1] |
| IMARC | USD 3.300 M (2025) → 48.800 M (2034) | 33,8% (2026–2034) | [S] [1] |
| 360iResearch | USD 1.680 M (2024) → 5.420 M (2030) | 20,3% | [S] [1] |
| Knowledge Sourcing | USD 3.840 M (2025) → 6.400 M (2030) | 10,75% | [S] [1] |
| Meticulous Research | USD 9.180 M en 2032 | 25,8% | [S] [1] |

**Lectura:** las cifras varían hasta 7 veces según cómo cada consultora define el mercado; sirven solo para decir que crece. No se abrieron los informes pagos (vistos en fragmentos o resúmenes). [S]

**Señal de capital:** Reducto levantó USD 24,5 M (Serie A, 04/2025, liderada por Benchmark) y USD 75 M (Serie B, 14/10/2025, liderada por a16z), USD 108 M en total. Declara que su volumen mensual creció más de 6 veces desde la Serie A. [S] [2] El dinero va a la capa de infraestructura (parseo para equipos de IA), no a la pyme.

### 1.2 Competidores y precios publicados

| Proveedor | Modelo / precio publicado | Público | Marca |
|---|---|---|---|
| **LlamaParse** (LlamaIndex) | Gratis 10 mil créditos por mes; Starter USD 50 por mes (40 mil créditos); Pro USD 500 por mes (400 mil créditos); 1.000 créditos = USD 1,25; parseo básico "desde 1 crédito por página" | Desarrolladores | [V] [3] |
| **Reducto** | USD 150 de crédito gratis; cada 1.000 páginas: Parse USD 10, Extract USD 20, Deep Extract USD 40, Classify USD 7,50; Growth y Enterprise a medida | Desarrolladores y empresas | [V] [4] |
| **Mindee** | Starter 44 por mes, Pro 116 por mes (la tabla no indica moneda; el FAQ habla de dólares); 1 página = 1 crédito; excedente +20%. El FAQ contradice la tabla de créditos | Desarrolladores y pymes | [V] [5] |
| **Veryfi** | Gratis hasta 100 documentos por mes; Starter con mínimo de USD 500 por mes: factura USD 0,16, recibo USD 0,08, extracto bancario USD 0,25 | Fintech y apps de gastos | [V] [6] |
| **Nanonets** | Gratis con USD 50 de crédito; después USD 100 por mes por 100 créditos; cobra por bloque ejecutado (USD 0,02 / 0,10 / 0,30); una factura típica usa 4 a 6 bloques | Pymes y mercado medio | [V] [7] |
| **Docsumo** | Prueba de 14 días con 1.000 páginas; Business y Enterprise con cotización, más cargo de implementación | Mercado medio (préstamos, seguros) | [V] [8] |
| **Rossum** | Starter "desde USD 18.000 por año", contrato mínimo de 1 año | Empresas (AP, logística) | [V] [9] |
| Hyperscience, Klippa, Affinda, Extend | Sin precio verificado (la página de Klippa dio error 404) | — | [NE] |

**Costo de extracción por factura de 2 páginas [E]:** LlamaParse ≈ USD 0,003–0,03; Reducto Extract ≈ USD 0,04; Veryfi USD 0,16; Nanonets ≈ USD 0,40–1,80 (4–6 bloques). La extracción no es lo que define el margen; lo definen la revisión humana y la integración, igual que en el modelo argentino.

---

## 2. Facturación electrónica obligatoria como motor de demanda

### 2.1 Calendario (estado a octubre de 2026)

Fuente principal: lista cronológica de VATupdate actualizada al 28/10/2026 [10], cruzada con otras fuentes.

| País / bloque | Fecha | Alcance | Marca |
|---|---|---|---|
| **Alemania** | 01/01/2025 | Todas las empresas deben poder **recibir** facturas electrónicas | [S] [11][12] |
| | 01/01/2027 | **Emitir**, si la facturación del año anterior superó 800.000 € | [S] [10][12] |
| | 01/01/2028 | Emitir: todas las empresas B2B nacionales | [S] [10] |
| | 2030 | Reporte de operaciones dentro de la UE (ViDA) y posible reporte B2B nacional | [S] [10] |
| **Francia** | 01/09/2026 | Recibir: todas las empresas. Emitir y reportar: grandes e intermedias, a través de plataformas aprobadas | [S] [10][13] |
| | 01/09/2027 | Emitir y reportar: pymes y microempresas | [S] [10] |
| **Bélgica** | 01/01/2026 | B2B obligatorio por Peppol. Tolerancia de enero a marzo de 2026, sin extensión; se aplica desde el 01/04/2026. Multas de 1.500 / 3.000 / 5.000 € | [S] [14] |
| | 2026 | Las pequeñas empresas deducen el 120% del costo del software o del Access Point (períodos fiscales 2024–2027) | [S] [14] |
| | 01/01/2028 | Reporte B2B casi en tiempo real (proyecto de ley) | [S] [10] |
| **Polonia (KSeF)** | 02/2026 y 04/2026 | Grandes contribuyentes, después el resto | [S] [11] |
| | 01/01/2027 | Grupo transitorio más chico (micro); hay un proyecto para pasar las multas a 2028 | [S] [10] |
| **España** | 01/01/2027 y 01/07/2027 | VERI*FACTU: sociedades y luego autónomos (RDL 15/2025). Se anunció otra postergación, todavía no sancionada | [S] [10][11] |
| | 06/10/2027 y 06/10/2028 | Factura electrónica B2B (Ley Crea y Crece): empresas de más de 8 M €, después el resto | [S] [10] |
| **Grecia** | 02/11/2026 → 02/2027 | Fase B del B2B para empresas de hasta 1 M € | [S] [10] |
| **Croacia** | 01/01/2027 | Fiscalización 2.0, fase 2 | [S] [10] |
| **UE (ViDA)** | 01/07/2030 | Reporte digital por transacción de las operaciones B2B dentro de la UE (adoptado) | [S] [10] |
| **Emiratos** | 01/01/2027 · 01/07/2027 | Fase 1 (facturación de 50 M AED o más; debían designar proveedor acreditado hasta el 30/10/2026); fase 2 para el resto | [S] [10] |
| **Arabia Saudita** | 01/02/2027 | Ola 25 de la fase 2 de ZATCA | [S] [10] |
| **Singapur** | 04/2028 → 04/2030 | InvoiceNow (GST) por tramos de facturación | [S] [10] |
| **Malasia** | 31/12/2027 | Termina la flexibilización para el tramo de 3 a 5 M de ringgit | [S] [10] |
| **Brasil** | 11/2026 – 12/2026 | NFS-e nacional para Simples Nacional; olas de documentos IBS/CBS (reforma tributaria) | [S] [10] |
| **Chile** | 01/11/2026 | Datos de trazabilidad adicionales en facturas y guías de despacho | [S] [10] |
| **EE.UU.** | — | Sin obligación federal. La red DBNAlliance (arquitectura tipo Peppol) es voluntaria. Declaración conjunta UE-EE.UU. sobre interoperabilidad del 05/04/2024 | [S] [15] |
| México, Colombia | Ya operan modelos de autorización previa (CFDI, DIAN) | Sin cambios relevantes en la fuente | [NE] |

**Evidencia de que las pymes no están listas (Alemania):** la ZDH (federación de oficios) encuestó a 1.926 empresas entre enero y febrero de 2026. Concluye que recibir y enviar facturas electrónicas "no funciona sin problemas" y que sin más medidas oficiales no es posible una aplicación segura desde 2027. [V] [12] Quadient (04/2026, proveedor): el 75% factura digitalmente, pero solo el 6% cumple todos los requisitos. Sage (11/2025): solo el 4% de las pymes había implementado la factura electrónica. [S] [12]

### 2.2 Quién compite y a qué precio

| Actor | Rol | Precio / dato | Marca |
|---|---|---|---|
| **Sovos** | Cumplimiento global; compra regionales (APAC de IRIS, 08/2025) | Cotización | [S] [16] |
| **Vertex** | Compró ecosio (Austria, EDI y factura electrónica) por USD 180 M | — | [S] [16] |
| **Pagero** | Red global de factura electrónica; vinculada a una adquisición que no se pudo confirmar | — | [NE] [16] |
| **Avalara** | Producto de factura electrónica y reporte en vivo (lanzado para clientes de Workday) | Cotización | [S] [16] |
| **Comarch, Quadient** | Líderes en IDC MarketScape 2026; Quadient compró Serensia (Francia, 2025) | — | [S] [16] |
| **Storecove** | Access Point Peppol y DBNAlliance vía API | Según agregadores, desde 495 € por mes; un usuario informó 52 € por mes por 50 facturas y 300 € por 5.000 [no oficial] | [S] [17] |
| **Plataformas aprobadas en Francia** | 146 a 156 plataformas según la fecha de la lista de la DGFiP | Micro y pequeña empresa: 0 a 40 € por mes; Pennylane desde 14 €, Tiime desde 17,99 €, Sage desde 39 € | [S] [13] |

### 2.3 Oportunidades para un integrador pequeño [E]

- **Sí, en teoría:** conectar ERPs o sistemas de facturación chicos y locales con un Access Point Peppol a través de una API de mayorista (Storecove u otro). También validar XRechnung, ZUGFeRD o Factur-X, mostrar el XML recibido en forma legible y asentarlo en el sistema contable, o resolver la autofacturación (en Bélgica tuvo tolerancia hasta el 30/06/2026 porque el software no estaba listo [14]).
- **Problema para Federico:** es un trabajo **local**, en el idioma del país, vendido por contadores y proveedores de ERP de ese país, con muchos competidores baratos (en Francia, casi 150 plataformas). Desde Argentina, sin red en Europa, no conviene que sea la primera cuña.
- **Efecto de segundo orden más interesante:** cuando la factura fiscal pasa a ser estructurada, los documentos **que no la acompañan** (extracto del proveedor extranjero, documento de transporte, entrada aduanera, comprobante de entrega) se convierten en el cuello de botella de la conciliación. Es el mismo patrón que en Argentina con ARCA.

---

## 3. Verticales con dolor documental fuerte

| Vertical | Documentos | Evidencia de demanda y competidores | Lectura [E] | Marca |
|---|---|---|---|---|
| **Logística / fletes** | Conocimientos de embarque (B/L), comprobantes de entrega (POD), facturas de transportistas | Loop: Serie C de USD 95 M (04/2026), dice que automatiza más del 99% de las facturas sin intervención. Pallet: USD 50 M en total. 5U AI (Múnich): USD 3,2 M (07/2026). Opereit (Barcelona): USD 2,5 M pre-seed (2026, auditoría de fletes y reclamos). Freightmate: USD 5 M (01/2025, más de 30 documentos por embarque). Expedock: USD 13,5 M (2022) | Muy financiado y concentrado en transportistas, forwarders y cargadores grandes. Hueco posible: brokers y forwarders chicos en QuickBooks | [S] [18] |
| **Construcción** | AP con subcontratistas, renuncias de privilegio de cobro (lien waivers), avisos preliminares | Handle: Serie B de USD 27 M (2026, liderada por Marbruck); más de USD 160.000 M en facturas procesadas; ARR contratado casi duplicado en 6 meses. Adaptive: Serie A de USD 19 M (2024, IA de AP que imputa a obra). Built: renuncias gratis (10/2025). CrewCost: AP con IA (09/2025) | Mercado probado en EE.UU. con normas estatales; hay competidores, pero apuntan a proveedores de materiales y contratistas generales medianos | [V] Handle [19]; [S] resto [19] |
| **Seguros** | Formularios ACORD (25, 125, 126, 130), detalle de riesgos (SOV), historial de siniestros (loss runs), denuncias de siniestro (FNOL) | **ACORD hace gratis su Transcriber para miembros (02/06/2026)**, con más del 98% de precisión declarada; American Integrity lo usa (01/2026). FurtherAI, Nomad Data, Docsumo, Reducto y Outmarket ya extraen formularios ACORD | Se volvió commodity por arriba (el propio estándar regala la extracción). No recomendado | [V] [20] |
| **Comercio exterior / aduanas** | Factura comercial, lista de empaque, clasificación arancelaria, entrada aduanera | Amari AI: seed de USD 4,5 M (02/2026, más de 30 despachantes clientes). Alchemize (YC primavera 2026). Nabu: 3 M € (Maersk Growth). Digicust: 2,3 M € (12/2025). iCustoms: USD 2,2 M. Caspian: USD 5,4 M (reintegro de aranceles) | Hay capital y startups para despachantes en EE.UU. y la UE. Riesgo regulatorio: se mencionó un fallo de CBP (16/01/2026) contra plataformas que precargan entradas sin licencia; no confirmado | [S] [21]; [NE] fallo CBP |
| **Administración de propiedades** | Facturas de proveedores por propiedad o unidad | Yardi (Payscan; Smart AP gratis en Breeze Premier), AppFolio (ingesta con IA), AvidXchange integrado en AppFolio (03/2026). Wrk: servicio administrado en AppFolio, Buildium y Yardi, **USD 1.000 de implementación + USD 250 por mes**. PredictAP, Vic.ai | Las plataformas grandes absorben la función. El precio de Wrk sirve de referencia para un servicio asistido | [S] [22] |
| **Contabilidad pyme en EE.UU. (QuickBooks / Xero)** | Recibos, facturas de compra, extractos | Dext: Business ≈ USD 30 por mes; en el Reino Unido, 12 a 36 £ por mes. AutoEntry cobra por crédito. Datamolino: 17 a 55 £ por mes. Xero llama "Smart Document Capture" a su captura incluida (EE.UU., 07/2026); hay versiones contradictorias sobre si Hubdoc sigue vendiéndose | Muy saturado, y la captura viene incluida en el sistema contable. No recomendado | [S] [23] |

---

## 4. Ecosistemas de apps contables

| Ecosistema | Cómo se distribuye y cuánto cuesta | Marca |
|---|---|---|
| **Xero App Store** | El 04/12/2025 Xero anunció que deja la comisión del 15% sobre suscripciones (XASS). Desde el 02/03/2026 cobra por conexiones y por datos que salen de Xero. Los pagos de XASS terminaron a fines de 06/2026. Planes en AUD sin impuestos: Starter gratis (5 conexiones), Core AUD 35 (50 conexiones, 10 GB), **Plus AUD 245 (1.000 conexiones, 50 GB, permite publicar en el App Store)**, Advanced AUD 1.445 (10.000 conexiones), Enterprise a medida (publicación obligatoria). Excedente AUD 2,40 por GB; la entrada de datos es gratis. En USD: 25 / 145 / 895. Los nuevos términos **prohíben usar datos de la API para entrenar modelos de IA o aprendizaje automático**. Hubo fuerte rechazo de contadores y desarrolladores | [V] [24]; [S] [25][26] |
| **QuickBooks (Intuit App Partner Program)** | Lanzado el 28/07/2025, con 4 niveles. Builder: gratis, llamadas Core ilimitadas y 500 mil llamadas CorePlus por mes (las de lectura); al superarlas, la API da error. Silver USD 300 por mes; Gold USD 1.700 (500 o más conexiones activas); Platinum USD 4.500 (3.000 o más). Las llamadas de escritura son gratis. Cobros variables desde el 01/11/2025. Solo QuickBooks Online. No se encontró comisión sobre ventas en el App Store | [S] [26][27]; FAQ oficial no legible [NE] |
| **NetSuite (SuiteApps)** | Membresía SDN de USD 3.000 por año (otra página regional muestra USD 10.000, posiblemente un nivel superior). La certificación "Built for NetSuite" exige revisión de arquitectura y seguridad. Conectarse por API no tiene costo | [V] [28]; [S] [26] |
| **Sage Intacct** | Marketplace Partner Program: USD 2.500 por año, con ≈ 66.666 llamadas por mes incluidas (USD 0,015 por llamada) | [S] [26] |
| **Otros (referencia)** | Odoo: 30% sobre ventas de apps. Fortnox: 25%. Dynamics 365 BC: 3% vía Marketplace. Exact Online: 15 € por mes. DATEV: 1.500 € por única vez | [S] [26] |

**Implicancia [E]:** el marketplace dejó de cobrar comisión (Xero) o la reemplazó por cobro por uso (Intuit). Con eso cae una barrera de margen, pero la distribución sigue sin ser gratuita: publicar en Xero cuesta AUD 245 por mes y, en las apps que leen mucho (conciliación, reportes), el cobro por datos penaliza. **Una app que sobre todo *escribe* en el sistema contable** (crear facturas de compra, asientos, ajustes de costo) es la que mejor se acomoda a los dos esquemas: en Intuit la escritura es gratis y en Xero la entrada de datos es ilimitada.

---

## 5. Comparación con el hallazgo argentino: costeo de importaciones (landed cost)

| Tipo de solución | Ejemplos | Qué hace / precio | Marca |
|---|---|---|---|
| Cálculo de aranceles en el comercio electrónico transfronterizo | Zonos Landed Cost | Calcula aranceles, impuestos y cargos en el checkout. Freemium; según FitGap, desde USD 250. Pocas reseñas | [S] [29] |
| Calculadoras de aranceles para importadores chicos | TariffCenter.ai, LandedHQ (Reino Unido, datos de HMRC) | Estimación; TariffCenter Starter USD 49 por mes | [S] [29][30] |
| Prorrateo contable sobre Xero o QuickBooks | **Landara** | Calcula flete, aranceles y tipo de cambio y asienta el costo de ventas en Xero o QuickBooks. **Desde USD 49 por mes con 10 cálculos**; el plan ilimitado cuesta más | [S] [30] |
| Función nativa | QuickBooks Online Plus/Advanced (fuentes contradictorias); Xero no la tiene (pedido abierto en su foro de ideas) | — | [S] [30] |
| Sistemas de inventario y ERP | Cin7, Unleashed, Katana, NetSuite | Tienen módulos de costo de importación, pero no se verificaron en esta búsqueda | [NE] |

**Conclusión [E]:** el problema existe y alguien lo resuelve, pero lo que se ofrece es *cálculo* (el usuario carga los montos a mano) o *módulos de ERP o inventario*. **No se encontró un producto pyme que extraiga de los documentos** (factura del proveedor en chino o inglés, factura del forwarder, entrada aduanera CBP 7501 o equivalente, factura del despachante) y genere el prorrateo por SKU con asiento contable. Los aranceles de EE.UU. de 2025–2026 hacen el dolor más visible: blogs y calculadoras de 2025–2026 hablan de cómo registrar aranceles en QuickBooks [30]. Las startups de aduana financiadas (sección 3) venden al despachante, no al importador pyme y su contador.

---

## 6. Riesgos

- **Plataformas que absorben la función:** captura incluida en Xero, Yardi y AppFolio; ACORD regala la extracción; los laboratorios de IA venden directo a pymes (ver informe argentino). [S]
- **Términos de las APIs:** Xero prohíbe entrenar modelos con datos de su API [25]. Intuit cobra las lecturas; un producto con muchas lecturas puede perder margen. [S]
- **Regulación aduanera:** si una herramienta precarga datos de una entrada aduanera, puede considerarse actividad de despachante (fallo de CBP no confirmado [21]). El costeo después de la importación (lectura y prorrateo contable) no presenta ese riesgo [E].
- **Dispersión de datos de mercado:** no usar ninguna cifra de "mercado IDP" en una presentación sin aclarar la fuente. [S]

---

## 7. Implicancias para Federico

**Cuña global 1 (recomendada): "Costo de importación desde documentos" para pymes importadoras en QuickBooks Online / Xero (EE.UU., Reino Unido, Australia).**
- **Qué hace:** el cliente o su contador sube la factura del proveedor extranjero, la del flete o forwarder y la entrada aduanera o la factura del despachante. El sistema extrae, concilia contra la orden de compra, prorratea flete, seguro y aranceles por SKU (por valor, peso o cantidad) y *escribe* en el sistema contable (factura de compra, ajuste de inventario o asiento). Las excepciones pasan por una cola de revisión. Es el hallazgo argentino n.º 2 llevado a ecosistemas con API abierta y marketplace.
- **Por qué:** competidor directo débil (Landara cobra USD 49 por mes por 10 cálculos manuales). Xero no lo trae de forma nativa. La extracción cuesta centavos (Reducto o LlamaParse). Las cuentas de escritura son baratas en ambos ecosistemas. Lo que se aprenda en Argentina (despachos, multimoneda) se puede reutilizar.
- **Precio hipotético [E]:** USD 99–249 por mes según la cantidad de embarques, o un cargo por embarque. Canal: contadores y bookkeepers de pymes que venden en Amazon o Shopify con importación directa, y consultores de QuickBooks o Xero. Empezar con Builder (Intuit, gratis) y Starter o Core (Xero) y publicar en el App Store recién con tracción (Plus, AUD 245 por mes).
- **Validación barata:** 15 entrevistas a contadores de e-commerce importador en EE.UU. y 3 pilotos pagos procesando sus embarques reales de 2026, antes de escribir la integración.

**Cuña global 2 (alternativa): mesa de excepciones AP en horario de EE.UU., vertical construcción o administración de propiedades en QuickBooks.**
- Servicio asistido con IA y revisión humana desde Argentina, que comparte horario con EE.UU. Precio de referencia de mercado: Wrk cobra USD 1.000 de implementación más USD 250 por mes [22], mucho más de lo que paga una pyme argentina, y eso arregla la economía unitaria que en el informe argentino dio negativa.
- Riesgo: Handle, Adaptive, AvidXchange y las funciones nativas de Yardi y AppFolio cubren a los clientes medianos. Hay que apuntar a subcontratistas o administradores chicos que usan QuickBooks y no esas plataformas.

**No conviene empezar por:** OCR genérico de facturas, extracción ACORD, conversores de factura electrónica europeos sin presencia local, ni captura de recibos para QuickBooks o Xero.

---

## Fuentes (consultadas el 30/10/2026)

1. Resultados agregados de informes IDP (Grand View en marketresearch.com, IMARC, 360iResearch, Knowledge Sourcing, Meticulous, TechSci): https://marketresearch.com/Grand-View-Research-v4060/Intelligent-Document-Processing-Size-Share-39035723 · https://www.imarcgroup.com/report/en/intelligent-document-processing-market · https://www.knowledge-sourcing.com/report/intelligent-document-processing-idp-market · https://www.meticulousresearch.com/product/intelligent-document-processing-market-5774 · https://www.gii.co.jp/report/ires1608134-intelligent-document-processing-market-by.html
2. Reducto, Serie B (14/10/2025): https://gazette.com/2025/10/14/reducto-raises-75m-series-b-to-define-the-future-of-ai-document-intelligence/ · Serie A: https://www.fortune.com/2025/04/25/exclusive-reducto-ai-document-parsing-startup-raises-24-5-million-series-a-led-by-benchmark
3. LlamaIndex, precios: https://www.llamaindex.ai/pricing
4. Reducto, precios: https://reducto.ai/pricing
5. Mindee, precios: https://www.mindee.com/pricing
6. Veryfi, precios: https://www.veryfi.com/pricing/
7. Nanonets, precios: https://nanonets.com/pricing
8. Docsumo, precios: https://www.docsumo.com/pricing
9. Rossum, precios: https://rossum.ai/pricing/
10. VATupdate, "Worldwide upcoming e-invoicing mandates" (actualizado al 28/10/2026): https://www.vatupdate.com/2026/10/28/worldwide-upcoming-e-invoicing-mandates-implementations-and-changes-chronological-2-2-2-2-2/
11. Calendarios UE: https://www.e-invoice.app/insights/busiest-einvoicing-year-2026 · https://www.jaggaer.com/blog/e-invoicing-compliance-france-spain-2026 · https://comarch.com/trade-and-services/data-management/news/e-invoicing-delays-france-poland-belgium-spain · https://www.vertexinc.com/resources/resource-library/navigating-urgent-e-invoicing-mandates-november-2025-regulatory-alert
12. Alemania, preparación de las pymes: ZDH https://www.zdh.de/ueber-uns/fachbereich-steuern-und-finanzen/umsatzsteuer/umfrageergebnisse-e-rechnung/ · Quadient https://www.quadient.com/en-gb/blog/e-invoicing-from-2027-are-german-businesses-really-ready · Sage (11/2025) https://www.sage.com/de-de/news/pressemitteilungen/2025/11/deutsche-kmu-e-rechnung/ · ecosio https://ecosio.com/de/blog/e-invoicing-e-rechnungspflicht/
13. Francia, plataformas aprobadas y tarifas: https://www.legifiscal.fr/actualites-fiscales/4536-facturation-electronique-137-plateformes-agreees.html · https://www.comparatif-facture-electronique.fr/cout-tarif-plateforme-facturation-electronique/ · https://blog.tiime.fr/cout-facturation-electronique-2026 · https://ma-facture-electronique.org/facture-electronique-definition/inconvenients/
14. Bélgica, tolerancia y multas: https://www.bdo.be/en-gb/insights/news-alerts/2025/mandatory-e-invoicing-in-2026-in-belgium-three-month-tolerance-period · https://fintua.com/blog/belgium-mandatory-einvoicing-enforcement/ · https://www.deloitte.com/be/en/services/tax/blogs/tax-legal-pulse/belgium-peppol-mandate-what-changes-for-smes.html · https://innovatetax.com/blog/belgian-einvoicing-penalties/
15. EE.UU. y DBNAlliance: https://www.storecove.com/blog/en/what-is-the-dbnalliance/ · https://econnect.eu/en/docs/knowledge/regulations/united-states · https://tradeshift.com/?p=72026
16. Consolidación del sector: https://www.itpro.com/business/acquisition/vertex-snaps-up-e-invoicing-specialist-ecosio-for-180-million · https://www.vatupdate.com/2025/08/13/sovos-acquires-iris-apac-tax-tech-business-expands-global-einvoicing-and-tax-compliance-reach · https://sovos.com/press-releases/sovos-named-a-leader-in-idc-marketscape-worldwide-compliant-e-invoicing-solutions-2026-vendor-assessment/ · https://briefglance.com/articles/quadient-named-e-invoicing-leader-amidst-global-regulatory-shift
17. Storecove, precios (secundarios): https://www.capterra.com/p/204604/Storecove/reviews/ · https://forum.invoiceninja.com/t/e-invoicing-without-invoiceninja-proxy-integration/23415 · https://www.e-invoice.app/vendors/storecove
18. Logística: https://freightwaves.com/news/freightmate-ai-raises-5m-highlights-need-for-flexible-freight-forwarding-tech · https://yespress.io/loop.md · https://yespress.io/pallet/pallet-ai-agents-for-logistics · https://www.cbinsights.com/company/opereit · https://www.pymnts.com/?p=1373395
19. Construcción: https://www.handle.com/series-b/ · https://news.yahoo.com/news/adaptive-builds-automation-tools-speed-130000462.html · https://getbuilt.com/blog/lien-waiver-automation/ · https://www.mannpublications.com/mannreport/2025/09/23/crewcost-launches-ai-powered-accounts-payable-for-general-contractors/
20. Seguros / ACORD: https://www.acord.org/news-detail/2026/06/02/acord-advances-industry-digitalization-by-providing-member-community-with-free-access-to-ai-driven-data-extraction · https://www.acord.org/news-detail/2026/01/27/american-integrity-automates-submissions-data-intake-via-acord-transcriber · https://www.furtherai.com/blog/best-ai-acord-form-data-extraction
21. Aduanas: https://www.caplight.com/company/amari · https://ycombinator.com/companies/alchemize · https://www.pulse.bot/supply-chain/news/nabu-raises-3m-to-scale-digital-customs-in-europe-e3edf5ed-4f74-40b2-b0cf-bdb564a85431/ · https://www.vestbee.com/insights/articles/digicust-secures-2-3-m · https://www.multimodal.org.uk/article/icustoms-raises-2-2-million-to-revolutionise-trade-compliance-with-ai · https://techintelpro.com/news/finance/investment/caspian-secures-54m-for-ai-driven-trade-advisory-platform
22. Administración de propiedades: https://www.wrk.com/blog/8-best-accounts-payable-automation-software-for-property-management · https://www.buildium.com/blog/best-ai-property-management-tools/ · https://www.pulse.bot/saas/news/avidxchange-expands-appfolio-partnership-with-embedded-ap-automation-solution-for-property-managemen-7564076f-6f06-4334-bb5d-2866ca6ec563
23. Captura para pymes: https://datamolino.com/blog/pricing-and-features-autoentry-vs-hubdoc-vs-dext-vs-datamolino-in-2026 · https://marcandrews.com/dext-vs-hubdoc-2026-best-receipt-scanner-for-uk-firms/ · https://receiptor.ai/blog/best-hubdoc-alternatives-for-xero-users
24. Xero, precios para desarrolladores: https://developer.xero.com/pricing
25. Xero, cambio de modelo: https://developer.xero.com/faq/pricing-and-policy-updates · https://www.theregister.com/2025/12/04/xero_api_fees_change/ · https://www.accountingtoday.com/news/xero-shifts-to-tiered-pricing-model-for-developers
26. Apideck, guía de precios de APIs contables (revisada el 11–16/10/2026): https://www.apideck.com/accounting-api-pricing
27. Intuit App Partner Program: https://investors.intuit.com/_assets/_08ee5483ec4c057568cc8774f3fd6aad/intuit/news/2025-07-28_Intuit_Launches_New_App_Partner_Program_to_Drive_1261.pdf · https://www.apideck.com/blog/quickbooks-api-pricing-and-the-intuit-app-partner-program · https://developer.intuit.com/app/developer/qbo/docs/get-started/partner-faq (no se pudo leer)
28. NetSuite SDN: https://netsuite.com/portal/developers/sdn.shtml · https://www.zoneandco.com/glossary/suitecloud-developer-network-sdn
29. Zonos: https://www.capterra.com/p/235321/Zonos-Landed-Cost/ · https://us.fitgap.com/search/global-trade-management-software/free · https://www.tariffcenter.ai/
30. Costo de importación en QuickBooks y Xero: https://www.g2.com/sellers/landara · https://pickyourapp.com/collections/store-management-finances-accounting/products/landara-landed-costs · https://invoicedataextraction.com/blog/quickbooks-online-landed-cost-allocation · https://productideas.xero.com/forums/967139-purchase-orders-bills-inventory/suggestions/48529637-inventory-landed-cost-allocation · https://www.cleverence.com/articles/business-blogs/trump-tariffs-quickbooks-3974/ · https://www.capterra.co.uk/software/1103101/Landedhq
