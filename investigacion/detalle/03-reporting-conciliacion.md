# Oportunidades 3 (Reporting de agencias) y 7 (Conciliación de lectura) en Argentina / LatAm

Investigación de escritorio al 29/10/2026. Todas las fuentes se consultaron ese día; la fecha que aparece entre paréntesis es la de publicación o actualización de la página, cuando se pudo ver.
Convenciones: **[V]** = verificado en fuente oficial o primaria. **[S]** = fuente secundaria (prensa, comparador o competidor; puede tener sesgo). **[E]** = estimación o inferencia propia. **[NE]** = no encontrado.

---

## 1. Resumen ejecutivo

- **El reporting genérico de agencias (Meta + Google + GA4 en Looker Studio) está resuelto y es barato.** Porter Metrics, que es latinoamericano, cobra desde unos USD 15 por cuenta conectada al mes. AgencyAnalytics cobra unos USD 20 por cliente al mes. Reportei, Metricool y Master Metrics tienen versión en español o portugués. Entrar ahí sin un ángulo vertical es competir por precio [1][2][3].
- **El hueco está en Mercado Libre.** Mercado Libre publica APIs de Product Ads (métricas por campaña y por anuncio) y de facturación (cargos por orden: comisión, envío, publicidad), pero los grandes conectores de agencias no lo cubren [V/S][10][17][18]. Hoy lo cubren jugadores chicos: Jaguar Sheet, un complemento argentino para Google Sheets que cuesta ARS 25.000–30.000 por mes, y Kondado, un conector brasileño para Looker Studio [S][10][31].
- **La conciliación para pymes y estudios contables es un dolor real pero fragmentado.** Los ERP locales (Colppy, Xubio) traen conciliación bancaria y una integración parcial con Mercado Pago. Colppy no funciona con Checkout Pro y su facturación es manual [V][33]. Simetrik apunta a empresas grandes [S][35]. No encontré un producto específico que concilie ventas de Mercado Libre, liquidación de Mercado Pago, comprobantes de ARCA y banco para el segmento pyme o estudio contable [NE].
- **Open Finance en Argentina todavía no funciona en 2026.** El Decreto 353/2025 creó el sistema, pero el BCRA no publicó estándares ni cronograma [S][36]. Para datos bancarios hay que usar extractos en PDF/CSV o la conexión que ofrece cada ERP. Mercado Pago, en cambio, sí tiene APIs de reportes con OAuth [V][24][25].
- **La cuña recomendada:** un informe de rentabilidad real por SKU y por mes para vendedores de Mercado Libre, opcionalmente con Tiendanube. Cruza órdenes, cargos de facturación (comisión, envío, Ads), liberaciones de Mercado Pago y costo de mercadería. Se vende a la agencia o consultora que gestiona la cuenta, o al contador del vendedor. Une las oportunidades 3 y 7 sobre una misma integración.

---

## 2. Oportunidad 3: Reporting de agencias

### 2.1 Mercado de agencias en Argentina y LatAm

| Dato | Valor | Tipo | Fuente |
|---|---|---|---|
| Cantidad total de agencias de marketing digital en Argentina | **No hay una cifra pública actualizada.** | [NE] | — |
| Censo de agencias digitales (Interact + UBA) | Primer censo, con datos de 2013: más de $1.000 M de facturación y más de 2.000 empleados, sobre 53 agencias socias. Está muy desactualizado. | [S] | [12] |
| IAB Argentina | Reúne editores, anunciantes, agencias y empresas de tecnología. No encontré un conteo de agencias. | [NE] | [12] |
| AAMD | No encontré cantidad de socios. | [NE] | — |
| Tamaño típico (Clutch, categoría "digital marketing" en Argentina) | La mayoría de las fichas visibles declaran entre 10 y 49 empleados; algunas entre 50 y 249. Tarifas de menos de USD 25 hasta USD 199 por hora. Es una muestra sesgada hacia agencias que exportan servicios. | [S] | [13] |
| Inversión en medios, 1.er semestre 2025 (CAAM) | Digital: USD 298 M, contra USD 175 M en el 1.er semestre de 2024. Medios en total: +103% interanual en pesos. | [S] | [14] |
| Mercado Ads Agency Partners 2025 | Primera edición en Argentina y México. Publicis y Omnicom recibieron el nivel Platinum. Confirma que existe un canal de agencias de "retail media" sobre Mercado Libre. | [S] | [15] |
| Tiendanube Partners Program – Agencies | Nuevo esquema de 5 niveles desde mayo de 2026, con certificación en Partners Academy y comisiones por tiendas nuevas. Es un canal de agencias identificable para salir a prospectar. | [V] | [16] |

**Estimación [E]:** el segmento útil para Federico no es "todas las agencias", sino las boutiques de entre 2 y 30 personas que gestionan Ads y e-commerce de pymes. Se pueden ubicar en los directorios de Partners de Tiendanube, en Clutch y en el Partner Center de Mercado Libre. No hay datos que permitan dimensionar ese segmento: hay que contarlo a mano desde esos directorios.

### 2.2 Herramientas de reporting y precios (USD salvo indicación)

| Herramienta | Origen | Modelo y precio | ¿Mercado Libre? | Tipo | Fuente |
|---|---|---|---|---|---|
| Looker Studio | Google | Gratis; Pro USD 9 por usuario al mes | Sin conector nativo | [S] | [2] |
| Porter Metrics | Colombia (Manizales) | Desde unos USD 15 por cuenta al mes, bajando hasta USD 2 con más de 400 conexiones. Plan "Agencias" USD 83,33 al mes (20 cuentas) y "Agencias Pro" USD 150 (40 cuentas), según un fragmento de su web. Dice tener más de 1.200 clientes y más de USD 500k de facturación anual (Forbes Colombia). | No lo encontré en sus listas | [S] | [1][2][11] |
| Supermetrics | Finlandia | Starter unos USD 29–37 al mes (3 fuentes, 1 destino); Growth unos USD 159–222. Cada destino adicional se cobra aparte. | No | [S] | [2][5] |
| Windsor.ai | — | Basic unos USD 19–23 al mes; Standard unos USD 99–118 al mes. Cobra por fuentes y por filas. | No figura entre los conectores populares | [S] | [7] |
| Dataslayer | España | Precios nuevos desde febrero de 2026: Starter unos USD 35, Advanced USD 115, Pro USD 345 (según terceros). | No | [V estructura / S precios] | [6] |
| AgencyAnalytics | Canadá | Plan "Core" de unos USD 20 por cliente al mes (anual) o unos USD 25 (mensual), sin cargo base. | No | [S] | [3] |
| DashThis | Canadá | Desde el 30/03/2026 cobra según fuentes y dashboards. Tiers listados: USD 49, 149 y 289 (pueden ser anteriores al cambio). | No | [V cambio / S precios] | [4] |
| Reportei | Brasil | Planes Starter, Pro y Premium; unos USD 24, 39 y 79 al mes según Capterra/G2. Un competidor cita R$ 74,90 como entrada. Tiene versión en español. | No figura entre sus 14 integraciones visibles | [S] | [2][8] |
| Metricool | España | Starter unos €16–20 al mes (5 marcas); Advanced unos €43 o más (15 marcas). | No | [S] | [2][9] |
| Master Metrics | LatAm | Conectores desde unos USD 30 al mes; dashboards desde unos USD 69 al mes. | No verificado | [S] | [2] |
| **Kondado** | Brasil | 19 pipelines de Mercado Livre (Orders, Ads, Payments, Shipments) con plantilla de Looker Studio que muestra ACOS y ROAS. Desde unos USD 19 al mes según su web. | **Sí** | [S, del propio proveedor] | [10] |
| **Jaguar Sheet** | Argentina | Complemento de Google Sheets. ARS 30.000 al mes (ARS 25.000 en plan anual); multicuenta ARS 62.000 (ARS 51.700 anual). Sincroniza cada hora ventas (44 columnas, con comisiones, envíos y retenciones de la API de facturación), publicaciones y Product Ads. | **Sí** | [S, del propio proveedor] | [31] |
| Nubimetrics / Real Trends | Argentina | Inteligencia de mercado y competencia (Nubimetrics) y gestión operativa (Real Trends, certificado por Mercado Libre, "más de 15 mil vendedores"). Sin precio público verificado. Según Jaguar Sheet, Nubimetrics no sincroniza la facturación ni los Ads propios del vendedor. | Sí (otro foco) | [S] | [31][32] |

**Lectura:** el reporting de Meta + Google ya cuesta entre USD 15 y 25 por cliente o cuenta y es una commodity. En Mercado Libre la oferta es chica y el foco es el vendedor, no la agencia: Jaguar Sheet es una planilla y Kondado es un conector genérico. No encontré un producto de reporting **para agencias** que combine Mercado Ads, facturación de Mercado Libre y Meta/Google con margen [NE].

### 2.3 Fuentes de datos: qué permite cada API

| Fuente | Qué permite (lectura) | Requisitos y límites | Tipo | Fuente |
|---|---|---|---|---|
| **Mercado Libre: Órdenes y Facturación** | `/billing/monthly/periods` (últimos 12 períodos), `/documents`, `/summary`, `/details`. Cargos por orden o pack en `/billing/integration/group/ML/order/details`. Tipos de cargo como CV (cobro por venta) y PADS (publicidad). Parámetro `group` = ML o MP. Paginación de hasta 1.000. | OAuth del vendedor. El rate limit se controla por Client ID y por endpoint; los números concretos no son públicos y difieren según la fuente (1.500 rpm frente a 240 rpm, ambos de terceros). | [V] | [18][19] |
| **Mercado Libre: Product Ads (Mercado Ads)** | Anunciante, campañas, anuncios y keywords. Métricas por campaña y por anuncio (`/advertising/product_ads/...`). `product_id` PADS, DISPLAY o BADS. | Para usar Product Ads, el vendedor necesita reputación amarilla o mejor, 15 días o más desde el registro, ventas mínimas y no tener facturas vencidas. Desde el 17/06/2026, algunos Brand Ads migraron a PAds y devuelven 204 en los endpoints viejos. | [S de doc oficial] | [17] |
| **Mercado Libre: Developer Partner Program** | Certificación y medallas para aparecer en el Partner Center. | Exige GMV mensual mínimo de los vendedores que usan la app: desde USD 100k (Perú) hasta USD 2,5M (Brasil). Requiere OAuth server-side y chequeo de vulnerabilidades. No es necesario para operar con pocos clientes. | [S de doc oficial] | [19] |
| **Mercado Pago: Reportes** | Reporte de Liberaciones (`/v1/account/release_report/config`) y Reporte de Conciliación/Liquidaciones (`/v1/account/settlement_report/config`). Columnas configurables (ej. SOURCE_ID, EXTERNAL_REFERENCE), frecuencia diaria, semanal o mensual, envío por SFTP. Muestra bloqueos y desbloqueos y cuotas liquidadas frente a pendientes. | OAuth con scopes `read`, `write` y `offline_access`. El refresh token dura unos 180 días y rota en cada uso. Los reportes no dan acceso a las cuentas bancarias del vendedor. | [V] | [24][25][41] |
| **Mercado Pago: Contracargos** | Notificación y gestión de disputas por API. El dinero queda retenido durante la disputa. | Igual que arriba. | [V] | [26] |
| **Tiendanube / Nuvemshop** | Admin API REST: órdenes, productos, clientes. | OAuth. Leaky bucket de 40 solicitudes con 2 por segundo, por tienda y por app; ×10 en planes Next/Evolución. Las apps públicas pasan homologación. Según la documentación, desde el **30/10/2026** empieza la deprecación de scripts que no usan NubeSDK. Afecta a apps que inyectan código en la tienda, no a la lectura por API [S, no confirmado en la página]. | [V rate limit / S resto] | [20][40] |
| Tiendanube: tamaño | La empresa declara más de 180.000 tiendas activas en LatAm. StoreLeads cuenta 176.933 (marzo 2026). API2Cart atribuye un 28,1% a Argentina, lo que sería unas 47.000 [E]. | — | [S] | [21] |
| Shopify / WooCommerce en Argentina | Unas 10.100 tiendas Shopify (StoreCensus, 01/09/2026) y unas 1.389 WooCommerce (mayo 2026). Las cifras de WooCommerce de los trackers parecen subestimadas: TechnologyChecker pone a WooCommerce primero en Argentina. | — | [S] | [21][22] |
| VTEX | OMS `/oms/pvt/orders` con paginación de unos 100 por página. Límites por créditos de ráfaga y error 429 con Retry-After. Apunta a cuentas grandes y no a pymes. | — | [S] | [23] |
| **Google Ads API** | Reporting completo con GAQL. | **Los developer tokens se retiraron el 09/09/2026**: el nivel de acceso ahora depende del proyecto de Google Cloud que genera el OAuth. Las solicitudes Basic pendientes se cerraron. Según terceros, las solicitudes nuevas exigen verificación de marca. | [V fecha / S detalles] | [27] |
| **Meta Marketing API** | Insights de campañas. | Para cuentas de terceros hace falta **Advanced Access** a `ads_read` (App Review) y la Business Verification de la empresa dueña de la app. Toma de días a semanas. | [V/S] | [28] |
| **TikTok Marketing API** | Campañas y reporting. | App en el portal de desarrolladores, revisión de scopes y data-security antes de pasar a producción. De 1 a 2 semanas según terceros. | [S] | [29] |

**Implicancia técnica [E]:** para un piloto con 3 a 5 clientes no hace falta certificar en Mercado Libre ni homologar en Tiendanube: alcanza con una app privada u OAuth por cliente. El cuello de botella son Meta (Advanced Access) y Google (proyecto Cloud con nivel de acceso). Alternativa: al principio, delegar Meta y Google a un conector existente como Porter o Windsor y construir propio **solo** Mercado Libre y Mercado Pago. Cuidado: Windsor exige aprobación escrita para incorporar sus datos en un producto de terceros (informe original, fuente [17] del PDF).

---

## 3. Oportunidad 7: Conciliación de lectura (pedidos, cobros y facturas)

### 3.1 El dolor en Argentina

| Componente | Qué complica | Tipo | Fuente |
|---|---|---|---|
| Liberación de Mercado Pago | El dinero se libera en distintas fechas según el medio y las cuotas; los reclamos y contracargos bloquean fondos. El reporte de liberaciones existe para conciliar el saldo disponible por fecha. | [V] | [24][26][41] |
| Cargos de Mercado Libre | Comisión variable por categoría, costo fijo por unidad (pesa mucho en tickets bajos), envío a cargo del vendedor y Product Ads. Todo llega en una factura mensual aparte, no en la orden. | [V/S] | [18][31] |
| Retenciones y percepciones | La RG 5554/2024 derogó las retenciones de IVA y Ganancias sobre cobros electrónicos desde el 01/09/2024. Siguen las retenciones de **Ingresos Brutos** (SIRCREB, SIRCUPA y regímenes provinciales), que varían por jurisdicción. Algunos blogs de 2026 hablan de percepciones de IVA por la RG 5319/2023: **hay contradicción entre fuentes; verificar con ARCA o un contador.** | [S] | [37] |
| Contracargos | El monto queda retenido hasta que se resuelve la disputa; si se pierde, se debita. Genera diferencias entre lo vendido y lo cobrado. | [V] | [26] |
| ARCA / comprobantes | "Mis Comprobantes" (emitidos y recibidos) se consulta con clave fiscal. **No encontré un web service oficial de descarga masiva**: integradores como yo-facturo importan el CSV exportado del portal. Hay repositorios open source que cruzan ese CSV con Mercado Pago, lo que muestra que el problema existe. | [S/NE] | [38] |
| Facturar cobros de Mercado Pago | Mercado Pago no emite factura electrónica. Hay un nicho de apps (TutiFactura, Gestorando, Facturita) que facturan a partir de cobros de Mercado Pago. | [S] | [39] |
| Escala del problema | Mercado Libre declara más de 3,5 M de pymes y emprendedores en su ecosistema en 2025 (incluye Mercado Pago) y unos 42.000 vendedores nuevos en el año. Es un dato autorreportado. | [S] | [30] |
| Fuga de ingresos | Simetrik describe el dolor como "dinero que la empresa cree tener y no aparece": diferencias chicas y repetidas entre plataforma, procesador y banco. | [S] | [35] |

### 3.2 Herramientas existentes

| Herramienta | Qué hace en conciliación | Precio | Tipo | Fuente |
|---|---|---|---|---|
| **Colppy** | Conciliación bancaria con conexión al banco (movimientos del día anterior, con 24–48 h hábiles de demora) en los planes Platinum, Full y Enterprise. Integración con Mercado Pago (QR, link de pago, transferencias) solo en Full y Enterprise. **No funciona con Checkout Pro**, la facturación es manual, se usa una empresa por cuenta de Mercado Pago y depende de webhooks (actualizado el 03/02/2026). | Plan Full de unos ARS 216.900 al mes (lista, marzo 2026, según un competidor) | [V funcionalidad / S precio] | [33] |
| **Xubio** | Importación de extractos en PDF con IA y conciliación sugerida que confirma una persona (función reciente, octubre de 2026). Se integra con Mercado Libre, Mercado Pago, Tiendanube y WooCommerce (sin detalle). | Básico ARS 123.100 + IVA; Estándar ARS 198.700; Avanzado ARS 268.300; Pro ARS 375.900 por mes (lista, septiembre 2026, según un competidor) | [S] | [34] |
| SpomBridge | ERP con integración nativa a Mercado Libre. Conciliación bancaria automática en el plan Empresa. | Base ARS 49.999 al mes; Empresa desde ARS 250.000 | [S, autodeclarado] | [34] |
| Contabilium | Cobra aparte cada cuenta adicional de Mercado Libre o Tiendanube. | Sin precio verificado | [S] | [34] |
| **Simetrik** | Plataforma de conciliación para empresas grandes (Mercado Libre, Nubank, Rappi). Más de 200 clientes, unos 50 países, US$ 85 M levantados. Lanzó "Simetrik Agent" con IA (08/2026). No apunta a pymes. | Sin precio público | [S] | [35] |
| Jaguar Sheet | Trae comisiones, envíos y retenciones por venta de Mercado Libre a Sheets. Sirve para rentabilidad, pero no concilia contra banco ni ARCA. | ARS 25.000–30.000 al mes | [S] | [31] |
| Bind / Pulpo | Las mencioné en el pedido; **no encontré información relevante sobre ellas para este caso en Argentina.** | — | [NE] | — |

### 3.3 Open Finance y APIs bancarias en Argentina (estado 2026)

- El **Sistema de Finanzas Abiertas** fue creado por el Decreto 353/2025, con el BCRA, ARCA, CNV, SSN y ANSES como autoridades. En 2026 **no está operativo**: no hay estándares técnicos, mecanismos de consentimiento ni cronograma publicados; hay grupos técnicos de trabajo [S][36].
- APIs públicas del BCRA ya activas: indicadores, Central de Deudores y Régimen de Transparencia (11/03/2026). **No dan movimientos de cuentas de clientes** [V][36].
- **Consecuencia [E]:** para conciliar bancos hay que trabajar con extractos (PDF/CSV, como hace Xubio con IA) o con la conexión bancaria del ERP del cliente. Mercado Pago es la única "cuenta" con una API de reportes madura y autorizable por OAuth.

---

## 4. ¿Qué combinación vertical funciona mejor como cuña?

| Candidata | A favor | En contra | Evaluación [E] |
|---|---|---|---|
| **A. Rentabilidad real para vendedores de Mercado Libre (Ads + comisiones + envíos + liberación de Mercado Pago + costo de mercadería), vendida a agencias y consultoras de Mercado Libre o a contadores** | Las APIs de facturación y Product Ads existen y son autorizables por el vendedor [18][17]. Los conectores globales no cubren Mercado Libre [1–9]. El dolor de margen es concreto (comisión variable, costo fijo, Ads) [31]. Une las oportunidades 3 y 7 sobre una sola integración. Hay un canal de agencias de Mercado Ads en formación [15]. | Jaguar Sheet ya cubre buena parte para el vendedor a ARS 25–30k al mes, que es un ancla de precio baja [31]. El rate limit por app no es público [19]. La dependencia de una sola plataforma es un riesgo. | **La mejor cuña.** Diferenciarse de Jaguar Sheet con conciliación (orden → cargo → liberación → acreditación), multicliente para agencias o estudios y alertas de excepciones (cargos inesperados, contracargos, retenciones de IIBB). |
| B. Agencias que gestionan tiendas Tiendanube (Meta/Google + órdenes Tiendanube + Mercado Pago) | Canal identificable (Partners Program Agencies, mayo 2026) [16]. API simple con rate limit documentado [20]. Unas 47k tiendas en Argentina [E][21]. | Meta y Google exigen Advanced Access y proyecto Cloud [27][28]. Porter, Windsor y AgencyAnalytics ya conectan Meta/Google + Shopify y es fácil que sumen Tiendanube. Diferenciación más débil. | Buena como **segundo módulo** una vez validada A. |
| C. Conciliación pura para estudios contables (Mercado Pago + banco + ARCA) | Dolor fuerte y recurrente. Los ERP solo cubren parcialmente Mercado Pago y no cubren Checkout Pro [33]. | Sin Open Finance, el banco llega por extractos [36]. ARCA no tiene API de descarga de recibidos [38]. La confianza exigida es alta y compite con funciones de ERP que mejoran (IA de Xubio) [34]. | Viable como **servicio asistido** para pocos estudios. Más difícil de escalar como SaaS. |
| D. Reporting genérico de agencias en español | Fácil de construir. | Commodity a USD 15–25 por cliente, con un competidor latinoamericano fuerte (Porter) [1][2][3]. | **Evitar.** |

---

## 5. Implicancias y recomendación para Federico

1. **No entrar en "reporting de agencias" genérico.** El precio de mercado ya está en USD 15–25 por cuenta o cliente y hay jugadores latinoamericanos establecidos como Porter Metrics [1][2][11]. Cualquier reporte de Meta y Google se compara contra eso.
2. **Elegir la cuña A: "P&L real por SKU y conciliación para cuentas de Mercado Libre".** Producto mínimo:
   - Órdenes de Mercado Libre + detalle de facturación por orden (CV, envío, PADS) + métricas de Product Ads + reporte de liberaciones de Mercado Pago + costo de mercadería que carga el cliente.
   - Salida: margen neto por SKU y por campaña; cuánto se vendió frente a cuánto se liberó y se acreditó; lista de excepciones (cargos sin orden, contracargos, retenciones de IIBB, liberaciones atrasadas).
   - Comprador principal: **agencias o consultoras que gestionan cuentas de Mercado Libre y Mercado Ads** (venta multicliente). Comprador secundario: **estudios contables con clientes vendedores de Mercado Libre**.
3. **Precio de referencia [E]:** el vendedor individual ya tiene Jaguar Sheet a ARS 25–30k al mes [31]. Para no competir ahí, vender **a la agencia o al estudio por cuenta gestionada**, más una puesta en marcha cobrada, en línea con el informe base. El precio por cuenta lo tienen que validar los pilotos; no hay dato que lo respalde.
4. **Técnica y permisos:**
   - Empezar con OAuth por cliente en Mercado Libre y Mercado Pago, solo en lectura (scopes `read` + `offline_access`) [25]. No buscar la certificación de Partner de Mercado Libre hasta superar sus umbrales de GMV [19].
   - Manejar el refresh token de Mercado Pago, que rota en cada uso [25], y hacer backoff ante errores 429 [19].
   - Dejar Meta y Google para una segunda etapa. Si la agencia los pide, usar sus propios exports o un conector con licencia que permita incorporarlo; el informe base advierte sobre los términos de Windsor.
5. **Validación en 30 días (alineada con el plan del informe):**
   - Hacer 12 a 15 entrevistas con agencias o consultoras de Mercado Libre (Partner Center de Mercado Libre, directorio de Tiendanube Partners, LinkedIn) y con 5 estudios contables que tengan vendedores de Mercado Libre.
   - Pregunta clave: "¿cómo calculaste el margen real y la diferencia entre vendido y cobrado del último mes, y cuántas horas te llevó?".
   - Llevar una demo con datos ficticios del reporte de facturación de Mercado Libre.
6. **Riesgos a vigilar:**
   - Cambios de API de Mercado Libre: por ejemplo, la migración de Brand Ads a PAds en junio de 2026 [17].
   - Dependencia de una sola plataforma.
   - Normativa de retenciones cambiante, con fuentes contradictorias [37]: el producto debe **mostrar** las retenciones, no interpretarlas fiscalmente.
   - Mantenerse en **lectura**: no custodiar ni iniciar pagos, para no entrar en categorías de PSP del BCRA (informe base).
7. **Datos que no encontré y conviene conseguir en las entrevistas:** cantidad real de agencias que gestionan Mercado Libre o Tiendanube en Argentina; precios oficiales vigentes de Xubio, Colppy, Nubimetrics y Real Trends; rate limits reales de Mercado Libre para una app chica; si existe un web service de ARCA para comprobantes recibidos.

---

## 6. Fuentes (consultadas el 29/10/2026)

1. Porter Metrics, Planes. https://portermetrics.com/es/planes/ (fragmento de búsqueda; la página no cargó completa)
2. Furia Reports, "Las mejores herramientas de informes de publicidad para agencias (2026)", 04/07/2026. https://furiareports.com/blog/mejores-herramientas-informes-agencias-2026 (escrito por un competidor)
3. Swydo, "AgencyAnalytics Pricing Explained" (junio 2026). https://www.swydo.com/blog/agencyanalytics-pricing/ ; Coupler.io, "AgencyAnalytics Pricing in 2026". https://blog.coupler.io/?p=85540
4. DashThis, "We're Updating Our Pricing" (2026). https://dashthis.com/blog/new-pricing-2026/ ; Capterra. https://www.capterra.com/p/163170/DashThis/pricing/
5. Coupler.io, "Supermetrics pricing" (2026). https://blog.coupler.io/supermetrics-pricing/ ; Swydo, alternativas. https://www.swydo.com/blog/best-supermetrics-alternatives/
6. Dataslayer Support, nueva estructura de precios (febrero 2026). https://support.dataslayer.ai/dataslayer-new-pricing-structure-transitioning-to-user-and-connector-based-plans-in-february-2026 ; PricingSaaS. https://pricingsaas.com/companies/dataslayer
7. CostBench, Windsor.ai Pricing 2026. https://costbench.com/software/marketing-attribution/windsor-ai/ ; MetricNexus. https://metricnexus.ai/blog/windsor-ai-pricing
8. Reportei KB, Planos. https://reportei.com/kb/planos/ ; 1ClickReport (competidor). https://www.1clickreport.com/blog/reportei-alternativa-analista-ia-agencias
9. SocialKit, guía de precios de Metricool (junio 2026). https://socialk.it/es/pricing/metricool
10. Kondado, reportes de Mercado Libre para Looker Studio. https://kondado.io/en/pre-built-reports/mercado-livre.html ; https://kondado.io/es/reports/dashboard-mercadolivre-looker-studio.html
11. Forbes Colombia, Porter Metrics. https://forbes.co/emprendedores/esta-startup-de-automatizacion-de-datos-de-manizales-factura-mas-de-us500-000-al-ano ; Latka. https://getlatka.com/companies/portermetrics.com
12. InfoNegocios, "Las Agencias Digitales tuvieron su primer censo" (Interact/UBA). https://infonegocios.info/infopublicidad/las-agencias-digitales-tuvieron-su-primer-censo
13. Clutch, Top Digital Marketing Agencies in Argentina. https://clutch.co/ar/agencies/digital-marketing
14. El Cronista, inversión publicitaria, 1.er semestre 2025 (CAAM). https://www.cronista.com/negocios/la-inversion-publicitaria-crecio-63-puntos-por-encima-de-la-inflacion-en-la-primera-mitad-de-2025
15. Mercado, "Mercado Ads reconoce a Publicis Groupe y Omnicom… Agency Partners 2025" (diciembre 2025). https://mercado.com.ar/marketing/mercado-ads-reconoce-a-publicis-groupe-y-omnicom-media-group-en-agency-partners-2025
16. Tiendanube Ayuda, niveles del Partners Program Agencies (actualizado el 13/07/2026). https://ayuda.tiendanube.com/es_AR/socios-comerciales/cuales-son-los-nuevos-niveles-del-partners-program-agencies-de-tiendanube
17. Mercado Libre Developers, Product Ads (lectura) (actualizado el 18/02/2026). https://developers.mercadolibre.com.ar/pads-read ; Brand Ads (09/06/2026). https://developers.mercadolibre.com.ar/ads-bads
18. Mercado Libre Developers, Buenas prácticas de reportes de facturación (febrero 2026). https://developers.mercadolibre.com.ar/buenas-practicas-para-el-consumo-de-las-apis-de-reportes-de-facturacion ; Reporte de pagos (mayo 2025). https://developers.mercadolibre.com.ar/reportes-pagos
19. Mercado Libre Developers, Rate limit 429. https://developers.mercadolibre.com.ar/rate-limit-error-429 ; Developer Partner Program. https://developers.mercadolibre.com.ar/developer-partner-program
20. Tiendanube API documentation, intro / rate limits. https://tiendanube.github.io/api-documentation/intro
21. StoreLeads, Tiendanube report. https://storeleads.app/reports/tiendanube ; TechnologyChecker. https://technologychecker.io/technology/tiendanube ; API2Cart. https://api2cart.com/api-technology/tiendanube-api/
22. StoreCensus, tiendas en Argentina (Shopify, 01/09/2026). https://api.storecensus.com/stores/country/argentina ; WooCommerce (28/05/2026). https://www.storecensus.com/woocommerce-stores/country/argentina
23. VTEX Community, List orders per_page. https://community.vtex.com/t/list-orders-is-there-a-max-per-page/25362
24. Mercado Pago Developers, Reporte de dinero liberado vía API. https://www.mercadopago.com/developers/es/docs/mp-point/additional-content/reports/released-money/api ; Referencia releases-report. https://www.mercadopago.com/developers/en/reference/releases-report/create-new-configuration/post
25. Mercado Pago Developers, OAuth token. https://www.mercadopago.com/developers/en/reference/oauth/_oauth_token/post ; https://www.mercadopago.com.ar/developers/en/docs/security/oauth
26. Mercado Pago Developers Argentina, Contracargos. https://www.mercadopago.com.ar/developers/es/docs/checkout-api-orders/chargebacks
27. Google Ads API, Deprecations (retiro de developer tokens, 09/09/2026). https://developers.google.com/google-ads/api/docs/deprecations ; PPC Land. https://ppc.land/google-drops-developer-tokens-from-ads-api-access-decisions/ ; Relevant Audience. https://www.relevantaudience.com/google-ads-en/google-ads-api-developer-tokens-sunset-cloud-project-access/
28. Meta for Developers, Marketing API Authorization / Access. https://developers.facebook.com/docs/marketing-api/get-started/authorization
29. Unified.to, "How to get your TikTok Ads API key". https://unified.to/blog/how_to_get_your_tiktok_ads_api_key ; Treasure Data, guía TikTok Marketing API. https://docs.treasure.ai/int/guides-for-creating-tiktok-marketing-api-developer-account-and-application
30. Mercado, "El ecosistema de Mercado Libre aportó US$ 5.400 millones…" (Efecto MELI 2025). https://mercado.com.ar/negocios/el-ecosistema-de-mercado-libre-aporto-us-5-400-millones-a-la-economia-argentina-en-2025
31. Jaguar Sheet, "Jaguar Sheet vs Nubimetrics". https://jaguarsheet.com/es/blog/jaguar-sheet-vs-nubimetrics ; "Herramientas para vendedores de Mercado Libre 2026" (27/03/2026). https://jaguarsheet.com/es/blog/herramientas-vendedores-mercado-libre (contenido del propio proveedor)
32. Argentina.gob.ar, ficha de Real Trends. https://www.argentina.gob.ar/node/222220 ; Algoritmo Digital. https://algoritmodigital.com.ar/news/potencial-imparable-como-la-alianza-de-mercadolibre-y-real-trends-puede-revolucionar-el-e-commerce-en-latam/
33. Colppy Ayuda, Integración con Mercado Pago (03/02/2026). https://intercom.help/Colppy/es/articles/9842451-integracion-con-mercado-pago ; Conciliación bancaria, conectá tu banco. https://intercom.help/Colppy/es/articles/4044358-conciliacion-bancaria-conecta-tu-banco ; SpomBridge vs Colppy (precios a marzo 2026). https://app.spomsolutions.com/comparar/spombridge-vs-colppy
34. SpomBridge, Alternativas a Xubio (precios a septiembre 2026; escrito por un competidor). https://app.spomsolutions.com/comparar/alternativas-a-xubio ; Blog del Contador, Xubio conciliación con IA. https://blogdelcontador.com.ar/news-46525-xubio-conciliacion-bancaria-ia-extractos-pdf
35. Forbes Argentina, Simetrik (14/10/2026). https://www.forbesargentina.com/negocios/la-fintech-controla-cuentas-mercado-libre-nubank-apuesta-ia-detectar-dinero-llega-n100245
36. Fiskil, Open Finance tracker Argentina. https://www.fiskil.com/es/open-finance-tracker/argentina ; BCRA, API Régimen de Transparencia. https://www.bcra.gob.ar/noticias/el-bcra-lanza-la-api-de-regimen-de-transparencia-para-facilitar-el-acceso-a-informacion-financiera/ ; Marval. https://www.marval.com/publicacion/el-bcra-da-un-paso-mas-hacia-el-open-finance-en-la-argentina-16825?lang=en
37. LM Neuquén, Mercado Pago deja de aplicar retenciones de IVA y Ganancias (RG 5554/2024). https://www.lmneuquen.com/pais/mercado-pago-dejara-aplicar-retenciones-iva-y-ganancias-cobros-online-como-impactara-los-usuarios-n1140148 ; Contablix 2026. https://contablix.ar/blog/retenciones-percepciones-ecommerce-argentina-2026 ; Jaguar Sheet, retenciones. https://jaguarsheet.com/es/blog/retenciones-mercado-libre
38. yo-facturo, recursos de facturación (importación CSV de Mis Comprobantes). https://yo-facturo.com/dev/resources/facturacion/ ; GitHub reconciliacionARCA. https://github.com/meshi6/reconciliacionARCA
39. Noticias Argentinas, app de facturas Mercado Libre/ARCA (TutiFactura). https://noticiasargentinas.com/economia/tiene-22-anos-y-creo-la-app-que-resuelve-el-drama-de-las-facturas-de-mercado-libre-y-arca_a684732f2d66463bf23c07464 ; Gestorando. https://gestorando.com/facturar-ventas-mercado-pago/
40. Nuvemshop/Tiendanube Developers, overview y NubeSDK (fragmento de búsqueda; la página redirige a https://nuvemshop.dev/en-US/overview, que no muestra las fechas). https://dev.tiendanube.com/en/docs/applications/overview
41. Mercado Pago, Reporte de dinero liberado (fuente [10] del informe base) y documentación de liberaciones. https://www.mercadopago.com.br/developers/es/docs/salesforce-commerce-cloud/additional-content/reports/released-money
