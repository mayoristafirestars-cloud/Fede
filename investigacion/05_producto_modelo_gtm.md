# 05 — Producto, modelo de negocio y go-to-market para una plataforma B2B para mayoristas y distribuidores (Argentina)

*Investigación al 20/10/2026. Punto de partida: "Coronel Sur" (FastAPI + SQLite, importa stock, ventas y presupuestos desde FactuPyme, ~4.180 clientes de tipo minorista, mayorista o institucional). Las cifras de terceros que no son oficiales se marcan como "referencial".*

---

## 0. Tesis en una línea

Construir **"el sistema operativo comercial del distribuidor pyme argentino"**: tomar pedidos por cualquier canal (WhatsApp, portal, preventista), ordenarlos con IA y cerrar el ciclo con cuenta corriente, cobranza y factura. Se monetiza primero con **SaaS en pesos indexado** y después con **pagos y financiamiento**. Es el camino que recorrieron Choco, Pepper y Toast.

---

## 1. Benchmark: qué nos enseñan los referentes

| Referente | Qué hace | Lección para nosotros |
|---|---|---|
| **Choco** (EE.UU./UE) | Arrancó como app para restaurantes y pivoteó a "AI partner for distributors". Su OrderAgent (2023) toma voicemails, SMS y emails y los carga en el ERP "en segundos". Declara más de 10.000 proveedores. ([choco.com](https://choco.com/us/stories/suppliers/from-restaurant-app-to-ai-partner-for-distributors-the-evolution-of-choco), [Choco AI](https://choco.com/uk/stories/suppliers/choco-ai)) | El que paga es el **distribuidor**, no el comprador. Cuando lo entendieron, la IA de captura de pedidos pasó a ser la cuña de entrada. |
| **Pepper** (EE.UU.) | E-commerce para distribuidores independientes de foodservice, con pagos, marketing y analítica. Su IA ingiere pedidos desde email, voicemail, texto, fotos, planillas y PDF hacia el ERP. Se integra con más de 70 ERPs. Levantó USD 30M (Serie B, 2024) y USD 50M (Serie C, 2026). ([Digital Commerce 360](https://www.digitalcommerce360.com/2026/02/24/pepper-raises-50-million-funding-ecommerce-tools/), [AgFunder](https://agfundernews.com/inside-peppers-push-to-digitize-foodservices-long-tail-armed-with-50m-and-agentic-ai)) | Ganó por **integrarse con el ERP existente** en lugar de reemplazarlo, y después sumó pagos y ads (data/trade marketing). |
| **Ordermentum** (Australia) | Gratis para el comprador ("core free forever") y pago para el proveedor. Hay referencias de ~USD 200/mes hasta 150 clientes con setup de USD 399, y ~USD 1.050/mes hasta 700 clientes (referencial). Cobra antes del despacho vía Zai. ([pricing](https://www.ordermentum.com/pricing), [Enterprise DNA](https://enterprisedna.co/omni/instead-of/ordermentum)) | El precio se escala **por cantidad de clientes activos del distribuidor**. Al comprador nunca se le cobra lo básico, para no frenar la red. |
| **Mercos** (Brasil) | App de pedidos para representantes y portal B2B para industrias y distribuidoras. ([B2B Stack](https://www.b2bstack.com.br/compare/fast-channel-vs-mercos)) | El preventista offline y el portal B2B son el núcleo del mercado LatAm. |
| **Toast** (vertical SaaS + pagos) | Según análisis secundarios, los servicios financieros generan varias veces lo que genera la suscripción. La secuencia fue pagos → préstamos (Toast Capital, que se repagan con un % de las ventas) → resto. ([Apideck](https://www.apideck.com/blog/embedded-finance-vertical-saas), [análisis Toast](https://alexandre.substack.com/p/toast-a-lesson-on-expanding-your)) | El SaaS es la **plataforma de datos** que después habilita el fintech. |

**Competencia local.** El mercado está fragmentado:

- **VentaClick**: e-commerce B2B y SFA, integra Tango y Bejerman, listas por cliente y cuenta corriente ([G2](https://www.g2.com/products/ventaclick/discuss)).
- **Centralo**: marketplace de kioscos y almacenes con mayoristas ([Descubre](https://www.descubre.vc/centralo)).
- **Mercado Libre Negocios**: B2B mayorista. Declara más de 500.000 usuarios mayoristas en Argentina ([America Retail](https://americaretail-malls.com/paises/brasil/mercado-libre-impulsa-el-comercio-mayorista-con-su-nueva-plataforma-b2b/)).
- **Tiendanube**: tiene tablas de precios mayoristas desde el plan Impulso, hasta 3 en Escala e ilimitadas en Evolución ([ayuda Tiendanube](https://ayuda.tiendanube.com/es_AR/ventas-mayoristas/que-es-y-como-configurar-la-funcion-de-ventas-mayoristas-y-minoristas-de-tiendanube)).
- ERPs: **Tango Gestión** (SaaS desde ~ARS 180.000/mes), **Siigo** (ARS 29.000–89.000/mes) y **Odoo** ([Develop Argentina](https://developargentina.com/blog/sistemas-gestion-comercial-argentina-2026)).

**Hueco detectado.** Nadie combina bien estas cuatro cosas:

1. Captura de pedidos por WhatsApp con IA (texto, audio y foto).
2. Integración liviana con el ERP o facturador que ya tiene el mayorista, como FactuPyme o Tango.
3. Actualización masiva de precios por inflación.
4. Cuenta corriente y cobranza con Mercado Pago.

Todo eso a un precio pyme y sin "implementación de ERP".

---

## 2. Producto: MVP y orden de construcción

### Principios

1. **No reemplazar el ERP o facturador al principio; montarse encima.** El mayorista ya factura con FactuPyme, Tango u otro sistema. Pedirle que migre mata la venta. Coronel Sur ya demuestra el patrón: importar desde FactuPyme.
2. **WhatsApp es el canal real de pedidos en Argentina.** El portal B2B es el complemento, no el reemplazo.
3. **La inflación es una feature.** Hay que poder actualizar listas en segundos y fijar la vigencia de precios en presupuestos y pedidos.

### Orden recomendado de módulos

| Fase | Módulo | Por qué en este orden |
|---|---|---|
| **MVP-0 (mes 0–3)** | **Catálogo y listas de precios por cliente o segmento** (minorista, mayorista, institucional, como ya clasifica Coronel Sur) + **actualización masiva** (% por rubro, proveedor o marca; importación de la lista del proveedor por Excel o PDF) | Es el dolor diario n.º 1 con inflación. Reutiliza el modelo de datos existente. |
| MVP-0 | **Importador ERP** (CSV/Excel de FactuPyme y Tango; luego API): stock, clientes, saldos | Sin datos no hay producto. Es "time-to-value" de un día. |
| MVP-0 | **Portal B2B / catálogo online** (PWA) con login por cliente, precios propios, carrito, "repetir último pedido" y estado del pedido | Es lo que el mayorista puede mostrarle a sus clientes. Es la base de la red. |
| **MVP-1 (mes 3–6)** | **Pedidos por WhatsApp con IA**: el cliente manda texto, audio o foto de una lista manuscrita → transcripción → LLM extrae ítems → *product matching* contra el catálogo del cliente (sinónimos, marcas, presentaciones) → borrador de pedido que un humano confirma con un clic | Es la cuña diferencial ("aha moment"). Choco y Pepper validan que la IA de captura vende sola. |
| MVP-1 | **Cuenta corriente y cobranzas**: saldo por cliente, antigüedad de deuda, recordatorios por WhatsApp (plantillas utility), link de pago Mercado Pago, imputación de pagos | El mayorista financia al almacén. Este módulo es la puerta al fintech. |
| **V1 (mes 6–9)** | **App de preventista offline-first** (PWA con IndexedDB/sync o React Native): ruta del día, cartera, toma de pedido sin señal, cobranza en campo, geolocalización de visita | Es crítica en consumo masivo y en distribuidoras con fuerza de venta en calle. Se cobra por usuario. |
| V1 | **Facturación electrónica ARCA** vía proveedor (AFIP SDK o TusFacturas) para los clientes que no tienen ERP o quieren facturar desde el pedido | Opcional. Sirve para facturar desde la plataforma sin reemplazar al ERP. |
| V1 | **Stock multi-depósito liviano** y reserva de stock al confirmar pedido | Al principio alcanza con sincronizar el stock del ERP. |
| **V2 (mes 9–12)** | **Reportes e IA predictiva**: reposición sugerida por cliente ("este almacén suele pedir X cada 10 días y no pidió"), clientes en riesgo, rentabilidad por rubro y vendedor, chatbot de catálogo ("¿tenés lavandina de 5 L y a cuánto?") | Retención y upsell. Usa los datos ya acumulados. |
| V2 | **Pagos integrados (split Mercado Pago)** y piloto de **financiamiento** | Es la monetización de segunda capa (ver §3). |

### IA realista en 2026 (y su costo)

- **Captura de pedidos multimodal.** El flujo es audio → transcripción → LLM con salida estructurada (JSON de ítems) → *matching* contra el catálogo por embeddings, alias aprendidos por cliente e historial de compras. La foto de una lista manuscrita también se procesa con un LLM con visión.
  - **Clave del producto:** un humano siempre confirma. La IA prepara el borrador y el sistema aprende de cada corrección (tabla de alias por cliente).
  - **Meta:** ≥85 % de líneas correctas sin edición en el mes 3 de cada cliente.
  - **Costo:** del orden de centavos de USD por pedido, despreciable frente al ticket.
- **Reposición sugerida:** heurísticas (frecuencia y cantidad histórica por SKU y cliente) antes que ML complejo. Se puede enviar como plantilla de WhatsApp "¿te armo tu pedido habitual?".
- **Chatbot de catálogo:** RAG sobre catálogo, precios del cliente y stock. Contesta disponibilidad y precio y deriva a un humano.
- **Actualización de listas:** se lee el PDF o Excel del proveedor con un LLM, se mapea a SKUs propios y se propone el nuevo precio con margen objetivo.

### WhatsApp Business Platform (Cloud API): reglas y costos

Fuente: [Meta, pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing).

- **Cobro por mensaje** desde el 1/7/2025, por categoría (marketing, utility, authentication, service) y por país del destinatario. Los mensajes entrantes del usuario no se cobran.
- **Servicio:** cada número tiene **1.000 mensajes de servicio gratis por mes**. **Desde el 1/10/2026** se cobran los mensajes de servicio que superen ese cupo y también los mensajes *utility* enviados dentro de la ventana abierta de 24 h. Esto cambia el modelo de costos: hay que **trasladar el costo de WhatsApp al cliente** (cupo incluido por plan y excedente con margen).
- **Argentina** es mercado propio. Meta bajó las tarifas de utility y authentication el 1/10/2025. **Se puede facturar en ARS desde el 1/4/2026.**
- **Tarifas de referencia (no oficiales):** marketing ≈ USD 0,03–0,06 y utility ≈ USD 0,01–0,03 por mensaje ([sent.dm](https://docs.sent.dm/docs/guides/whatsapp-pricing), [Chattigo](https://blog.chattigo.com/whatsapp-business/cuáles-son-las-tarifas-comunes-para-usar-un-chatbot-con-la-api-de-whatsapp-business)). Hay que verificar la *rate card* ARS vigente.
- Los anuncios **Click-to-WhatsApp** abren una ventana gratis de 7 días.
- **Reglas operativas:**
  - Opt-in del cliente.
  - Plantillas aprobadas para iniciar conversación.
  - Un número por mayorista (registrado en su WABA, con nuestra app como *Tech Provider* o vía un BSP).
  - Hay riesgo de *quality rating* si se abusa del marketing.

### Facturación electrónica e integraciones

- **AFIP SDK** ([afipsdk.com/pricing](https://afipsdk.com/pricing)):
  - Free: 1 CUIT y 1.000 requests.
  - Pro: USD 25/mes con 10 CUITs.
  - Growth: USD 80/mes con 100 CUITs.
  - Startup: USD 250/mes con 1.000 CUITs.
  - Para un SaaS multi-CUIT el costo marginal queda por debajo de **USD 1 por cliente**. Es la opción recomendada.
- **TusFacturas API:** alternativa con SDKs ([docs](https://developers.tusfacturas.app/como-empiezo/api-factura-electronica-afip-plugins-y-sdks)).
- **Librerías open source** de WSFEv1, como `arca-sdk-php`: más control y cero costo, pero más mantenimiento.
- **ERPs:**
  - Primero, conectores por archivo (CSV/Excel programado, carpeta compartida o email entrante).
  - Después, API donde exista: Tango tiene API REST en su versión Nube/Delta.
  - FactuPyme: replicar el importador de Coronel Sur.

---

## 3. Modelo de negocio

### Opciones evaluadas

| Modelo | Pros | Contras en Argentina | Veredicto |
|---|---|---|---|
| **SaaS por suscripción con tiers** | Ingreso predecible y fácil de vender | Inflación: hay que indexar | **Núcleo** |
| **Por usuario (preventista)** | Escala con el tamaño del cliente | Fricción si es caro | **Add-on** |
| **% del GMV o take rate sobre pedidos** | Se alinea con el valor | Los mayoristas operan con márgenes del 8–15 % y desconfían de "comisiones por mis propias ventas". Además es difícil de auditar fuera de la plataforma | **No** como modelo principal |
| **Pagos (split de Mercado Pago)** | Ingreso por transacción. `marketplace_fee` o `application_fee` en el checkout ([MP docs](https://www.mercadopago.com.ar/developers/es/docs/split-payments/split-1-1/integration-configuration/integrate-marketplace)) | El MDR de MP ya es alto (~6,29 % + IVA con acreditación inmediata; ~1,49–3,49 % + IVA con 30–35 días, referencial, [Shopify](https://www.shopify.com/es/blog/mercado-pago-metodos-de-pago)). En B2B domina la transferencia y el efectivo | **Fase 2**: fee chico (0,3–0,8 %) o un fijo por cobro |
| **Finanzas embebidas** (crédito a almacenes, factoring de la cuenta corriente del mayorista) | Es el mayor potencial, según la lección de Toast | Riesgo de crédito y regulación. Hay que hacerlo con un *partner* (fintech o SGR) y solo cobrar *revenue share* | **Fase 3** (mes 12+) |
| **Datos y trade marketing para marcas (CPG)** | Alto margen, como Pepper con ads | Requiere escala (miles de almacenes) y consentimiento | **Fase 3+** |

### Recomendación: **SaaS en pesos indexado + add-ons por uso, con opcionalidad fintech**

Precio de lista en USD como referencia interna y cobro en ARS ajustado trimestralmente por IPC o dólar MEP, con débito automático por Mercado Pago. Plan anual con descuento.

| Plan | Para quién | Incluye | Precio sugerido |
|---|---|---|---|
| **Inicial** | Mayorista chico (<150 clientes activos) | Catálogo, 3 listas de precios, portal B2B, importador ERP, 1 número de WhatsApp con pedidos IA (300 pedidos IA/mes), 2 usuarios internos | **USD 59–79/mes** (~ARS equivalente) |
| **Profesional** | 150–700 clientes | Listas ilimitadas, cuenta corriente y cobranzas, recordatorios, reportes, 1.000 pedidos IA/mes, 5 usuarios | **USD 149–199/mes** |
| **Distribuidora** | Más de 700 clientes o con fuerza de venta | Todo lo anterior, app de preventista, multi-depósito, API, soporte prioritario | **USD 349+/mes** |
| Add-ons | — | Preventista: **USD 15–20 por usuario al mes**. Excedente de mensajes de WhatsApp a costo de Meta + 30 %. Facturación ARCA: USD 10/mes. Setup u onboarding asistido: USD 150–400 una vez | — |

**Justificación.** Ordermentum cobra ~USD 200 con el mismo eje de "clientes activos". Tango cuesta ~ARS 180.000/mes solo en ventas y stock, y nosotros lo complementamos en vez de competir. Siigo y Gestix muestran que la pyme argentina paga ARS 15.000–90.000 por herramientas simples. El precio se ancla en el **ahorro**: si se elimina 1 administrativo dedicado a cargar pedidos de WhatsApp, eso vale más de ARS 1M/mes en costo laboral. **El comprador (almacén o minorista) nunca paga** por el portal ni la app, para proteger la red.

### Métricas objetivo (vertical SaaS para SMB)

- **Churn mensual:** el rango típico SMB es 3–5 %, y por debajo de 2 % es muy bueno. Los productos que capturan transacciones diarias (pedidos y cobranzas) tienden a churn bajo porque son "system of record" ([Stealth Agents](https://stealthagents.com/research/saas-startup-metrics-statistics-2026), [Prospeo](https://prospeo.io/s/saas-industry-benchmarks)). **Meta: <2,5 % mensual de logos y NRR >100 %** gracias a preventistas y pagos.
- **CAC payback:** el benchmark SMB es 8–15 meses ([Prospeo](https://prospeo.io/s/cac-payback)). Con ventas lideradas por los fundadores y referidos, la meta es **<9 meses**.
- **LTV/CAC:** ≥3:1 ([Stealth Agents](https://stealthagents.com/research/smb-customer-lifetime-value-benchmarks-2026)). Ejemplo de cálculo:
  - ARPA de USD 150 con margen bruto del 80 % = USD 120/mes.
  - Con churn del 2,5 %, la vida media es de 40 meses → LTV ≈ USD 4.800.
  - CAC tolerable: ≤ USD 1.600.

---

## 4. Go-to-market en Argentina

### 4.1 Vertical inicial (elegir 1–2)

| Candidato | Pros | Contras |
|---|---|---|
| **Distribuidoras de consumo masivo, almacén y limpieza/perfumería** | Enorme base: CADAM habla de **~140.000 almacenes** abastecidos por mayoristas ([El Litoral](https://www.ellitoral.com/politica/distribuidores-mayoristas-reclaman-medidas-urgentes-economia-argentina_0_tPqMWoIsnh.html)). Pedidos por WhatsApp muy frecuentes, preventistas y cuenta corriente. Recurrencia semanal → datos para reposición sugerida y crédito | Margen bajo y sensibilidad al precio |
| **Rubro de Coronel Sur** (a confirmar: si es ferretería, materiales eléctricos, sanitarios o similar, con clientes minoristas, mayoristas e institucionales) | Hay caso real, datos y conocimiento del dominio. Catálogos grandes con alias y códigos → la IA de *matching* es muy valiosa. Tickets más altos | Ciclo de pedido menos frecuente |
| Bebidas, golosinas, kioscos | Altísima frecuencia | Más competencia de distribuidores oficiales con SFA de las marcas |
| Foodservice (gastronomía) | Es el playbook de Choco y Pepper | Restaurantes golpeados por el consumo en 2026 |

**Recomendación:**

- **Vertical 1 = el rubro de Coronel Sur.** Se tiene caso de éxito, datos reales, lenguaje del rubro y referencias inmediatas en su red de proveedores y colegas.
- **Vertical 2 = distribuidoras de consumo masivo, limpieza y perfumería** (escala y fintech futuro). Se entra con el módulo de pedidos por WhatsApp con IA y preventistas.

### 4.2 Motor de ventas

1. **Ventas lideradas por los fundadores (meses 0–9):** los fundadores venden y hacen el onboarding de los primeros 20–30 clientes. Objetivos:
   - Demo con **los datos del prospecto**: importar su lista de precios y convertir un audio real de WhatsApp en pedido en vivo.
   - Piloto de 30 días con un éxito definido (por ejemplo, ≥50 % de los pedidos de WhatsApp pasan por el sistema).
2. **Coronel Sur como design partner y caso de estudio.** Precio preferencial a cambio de:
   - Métricas publicables: horas ahorradas, pedidos por día, reducción de errores, DSO de cobranzas.
   - Video testimonial.
   - Presentaciones a sus proveedores (que también son mayoristas).
   - Acceso para iterar el producto semanalmente.
3. **Referidos desde abajo (flywheel).**
   - Cada mayorista invita a sus clientes al portal o app: con ~4.180 clientes de Coronel Sur hay un piloto de adopción del lado minorista.
   - Cuando un almacén ya usa la app con un mayorista, se le permite **agregar a otros proveedores**. Así el minorista termina invitando a su otro mayorista, el loop de Ordermentum y Choco.
   - Incentivo: un mes gratis para el mayorista que refiere y para el referido.
4. **Canales y partners:**
   - **Contadores y estudios contables**, que asesoran a pymes y recomiendan sistemas: comisión recurrente del 15–20 % durante 12 meses.
   - **Revendedores y consultores de Tango y FactuPyme**: nos posicionamos como complemento ("le agregás pedidos con IA a tu Tango"), no como competencia.
   - **Cámaras**:
     - **CADAM**: tiene eventos como la Black Week Mayorista con más de 150 sucursales ([C5N](https://www.c5n.com/economia/ultimos-dias-aprovechar-black-week-nacional-mayorista-organizada-cadam-n181868/amp)) y el congreso CONAL ([America Retail](https://americaretail-malls.com/paises/argentina/conal-2025-un-encuentro-clave-para-los-distribuidores-mayoristas-en-el-sheraton-pilar/)).
     - **CAME** y cámaras regionales de comercio.
     - Cámaras del rubro elegido, por ejemplo ferreteras.
     - Beneficio para socios y charlas.
   - **Proveedores y marcas**: las marcas quieren que sus distribuidores se digitalicen y pueden cofinanciar licencias. Esto es la semilla del negocio de datos y trade marketing.
5. **Contenido y performance:**
   - **LinkedIn** del fundador con casos y números.
   - **YouTube y TikTok** cortos: "cómo actualizo 5.000 precios en 1 minuto" y "audio de WhatsApp → pedido".
   - **Meta Ads Click-to-WhatsApp**: la ventana gratis de 7 días es ideal para hacer la demo por WhatsApp.
   - **Plantillas gratuitas** como lead magnet: Excel de actualización de listas por inflación y calculadora de costo de cuenta corriente.
   - **Comunidad de WhatsApp** de dueños de distribuidoras.
6. **Precio de entrada:** sin setup para los primeros 20 clientes ("Fundadores") a cambio de feedback y testimonio. Plan anual con 2 meses gratis.

---

## 5. Arquitectura técnica (evolución desde Coronel Sur)

- **Base:** mantener **FastAPI** (Python), que ya conoce el equipo y tiene muy buen ecosistema para LLMs.
- **Migración SQLite → PostgreSQL** (gestionado):
  - **Multi-tenant** con *shared schema*: columna `tenant_id` en todas las tablas + **Row-Level Security** de Postgres como defensa en profundidad.
  - A futuro, esquema o base dedicada para clientes grandes.
  - Migraciones con Alembic.
  - El código de Coronel Sur pasa a ser el **tenant #1**.
- **Capas:**
  1. API core: catálogo, precios, clientes, pedidos, cuenta corriente.
  2. **Workers asíncronos** (Celery/RQ o Arq + Redis) para importaciones, LLM, webhooks de WhatsApp y Mercado Pago, y facturación.
  3. **Conectores** como plugins: FactuPyme, Tango, CSV genérico, AFIP SDK, Mercado Pago OAuth.
  4. **Capa IA**: servicio de extracción de pedidos con prompts versionados, embeddings del catálogo en **pgvector** y tabla de alias por tenant y cliente. Proveedor LLM detrás de una interfaz para cambiar de modelo. Logging para evaluación (*evals* de precisión del *matching*).
- **Frontend:**
  - **PWA** (React/Next o SvelteKit) para el backoffice y el portal B2B: una sola base de código, instalable y sin pasar por las tiendas de apps.
  - **App de preventista**: PWA offline-first (Service Worker + IndexedDB + cola de sincronización con resolución de conflictos "último gana" por línea y validación de precio y stock en el servidor). Si se necesitan GPS en segundo plano, impresión Bluetooth o mucho volumen offline, pasar a **React Native/Expo** con SQLite local.
  - Recomendación: arrancar con PWA y migrar solo si los preventistas lo exigen.
- **Seguridad y cumplimiento:**
  - Certificados de ARCA por tenant cifrados (KMS o secret manager).
  - Ley 25.326 de datos personales.
  - Backups diarios con PITR (recuperación a un punto en el tiempo).
  - Auditoría de cambios de precios.
- **Hosting (estimado mensual):**
  - Etapa 0–50 clientes: VPS o Render/Fly/Railway + Postgres gestionado ~USD 50–150; Redis ~USD 10–30; storage de objetos y CDN ~USD 10.
  - LLM y transcripción: ~USD 0,01–0,05 por pedido IA.
  - AFIP SDK Growth: USD 80.
  - **Total de infraestructura: ~USD 200–400/mes** hasta ~50 clientes (<5 % del MRR objetivo).
  - Con más de 200 clientes conviene AWS o GCP en São Paulo por latencia, o seguir en un PaaS.

---

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| **Inflación y tipo de cambio** erosionan el precio en ARS | Precio indexado trimestral, débito automático y planes anuales en USD-MEP para clientes grandes |
| **Cambios de Meta en WhatsApp** (cobro de servicio desde 10/2026, *quality rating*, baneos) | Trasladar el costo por excedentes, usar la ventana de servicio, opt-in, y el portal y la app como canal alternativo. Monitorear el calendario trimestral de precios de Meta |
| **Errores de la IA** en pedidos (producto o cantidad equivocados) | Siempre con confirmación humana, mostrar el nivel de confianza por línea, aprender alias y medir con *evals* |
| **Competencia** (Mercado Libre Negocios, Tiendanube B2B, ERPs que agregan módulos) | Foco vertical, integración con el ERP existente, IA de WhatsApp y cuenta corriente, servicio cercano. No competir en marketplace abierto al principio |
| **Integraciones frágiles** con ERPs legacy | Empezar por archivos, con conectores robustos e idempotentes y monitoreo de sincronización |
| **Concentración en el design partner** (el producto queda "a medida" de Coronel Sur) | Toda feature nueva tiene que pedirla al menos 3 clientes y se implementa como configuración por tenant |
| **Churn SMB** (cierre de comercios en contexto recesivo, como reclama CADAM en 2026) | Valor ligado al ahorro de costos, plan "Inicial" barato para bajar en lugar de cancelar, y *health score* de uso |
| **Fintech y regulación** (BCRA, UIF, riesgo de crédito) | Solo como *partner* referidor con revenue share. No prestar con balance propio |
| **Equipo chico y deuda técnica** | Migración disciplinada a Postgres y multi-tenant antes de sumar al cliente #3. CI/CD y tests |

---

## 7. Roadmap a 12 meses, KPIs y presupuesto

| Trimestre | Hitos | KPIs |
|---|---|---|
| **T1 (meses 1–3)** | Postgres multi-tenant. Coronel Sur migrado como tenant #1. Catálogo, listas y actualización masiva. Importador FactuPyme/CSV. Portal B2B PWA. Entrevistas a 30 mayoristas | 3 design partners activos, 10 % de los clientes de Coronel Sur pidiendo por el portal, NPS ≥40 |
| **T2 (meses 4–6)** | Pedidos por WhatsApp con IA (texto, audio, foto). Cuenta corriente y recordatorios. Link de pago MP. Pricing lanzado. Caso de estudio publicado | **10 clientes pagos**, MRR ≥ USD 1.500, ≥80 % de líneas IA sin edición, tiempo de carga de pedido −50 % |
| **T3 (meses 7–9)** | App de preventista offline. Facturación ARCA vía AFIP SDK. Conector Tango. Programa de contadores y revendedores. Convenio con una cámara | **25–30 clientes**, MRR ≥ USD 5.000, churn <3 %, 30 % de las altas por canal o referido |
| **T4 (meses 10–12)** | Reposición sugerida, chatbot de catálogo, reportes. Split MP en cobranzas. Piloto de financiamiento con un partner. Multi-proveedor para minoristas (beta) | **50–60 clientes**, MRR USD 8.000–12.000 (ARR ~USD 100–140k), NRR >100 %, payback <9 meses, ≥2.000 minoristas activos en la red |

### Equipo y presupuesto (12 meses, orden de magnitud)

| Rol | Dedicación | Costo aprox. (USD/mes) |
|---|---|---|
| Fundador 1: producto y ventas | 100 % | Equity o sueldo mínimo |
| Fundador 2: tech lead backend e IA | 100 % | Equity o sueldo mínimo |
| Desarrollador full-stack (PWA y offline) | 100 %, desde el mes 3 | 1.800–2.800 |
| Onboarding y soporte / customer success (perfil comercial con conocimiento del rubro) | 100 %, desde el mes 5 | 1.000–1.500 |
| Diseño UX freelance | Parcial | 300–500 |
| Infraestructura, LLM, AFIP SDK, WhatsApp | — | 200–500 |
| Marketing (ads Click-to-WhatsApp, contenido, eventos de cámaras) | — | 500–1.500 |
| Legal y contable (SAS, términos, datos personales) | — | 200–300 |

- **Burn estimado:** ~USD 5.000–8.000/mes, es decir **~USD 60.000–90.000 en el año** sin sueldos de mercado para los fundadores.
- **Breakeven operativo:** alrededor de 50–60 clientes con ARPA de USD 150.
- **Financiamiento:** alcanza con *bootstrapping* más clientes "Fundadores" con pago anual adelantado. Recién con tracción en T3/T4 tiene sentido una ronda pre-seed (USD 300–500k) para acelerar el vertical 2 y el fintech.

---

## 8. Conclusión

El producto ganador para el mayorista argentino en 2026 tiene cinco piezas:

- **Pedidos por WhatsApp con IA** como cuña de entrada.
- **Listas de precios con actualización masiva** para sobrevivir a la inflación.
- **Cuenta corriente y cobranza** como sistema de registro diario.
- **Integración** con el facturador o ERP existente.
- Un **portal y una app gratuitos para los minoristas**, que construyen la red.

El modelo es **SaaS indexado por tamaño del cliente + add-on por preventista**, con pagos y financiamiento como segunda y tercera capa (el playbook de Toast, Choco y Pepper, adaptado a Mercado Pago). El GTM es **ventas lideradas por los fundadores en un vertical**, con Coronel Sur como caso de estudio, más contadores, revendedores de ERP y cámaras como canales de escala.
