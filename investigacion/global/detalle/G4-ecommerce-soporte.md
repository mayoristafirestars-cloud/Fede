# G4 · Comercio electrónico, marketplaces, mensajería y soporte: panorama global

Informe del agente G4, 30/10/2026. Continúa el PDF *Negocios digitales con APIs* (29/10/2026) y el informe argentino (`investigacion/INFORME.md`), donde la cuña #1 fue **rentabilidad real y conciliación para vendedores de Mercado Libre / Mercado Pago**. Acá se busca su equivalente a nivel mundial y se revisan las economías de las tiendas de apps, la mensajería y el soporte con IA.

**Marcas:** [V] verificado en fuente primaria (página oficial del proveedor o de la plataforma) · [S] fuente secundaria (prensa, blog de terceros, agregador) · [E] estimación o inferencia propia · [NE] no encontrado.
Todas las fuentes se consultaron el 30/10/2026 salvo otra indicación. Se hicieron 18 búsquedas web. Cuando un dato viene del informe argentino se lo indica como "(inv. AR)".

> No es asesoramiento legal, contable ni de inversión. Precios y normas cambian; confirmar antes de usar.

---

## 1. Conclusión en una página

1. **La categoría "profit analytics / conciliación para vendedores" está madura en el mundo anglosajón y barata.** Sellerboard cobra USD 19–79 por mes y declara más de 20.000 vendedores. A2X arranca en USD 29 por canal. TrueProfit cobra USD 35–200 y tiene 923 reseñas en Shopify. Triple Whale tiene decenas de millones de USD de ingresos estimados [V][1][2][4][S][5]. **Entrar ahí con Amazon US o Shopify US es entrar a una guerra de precios con productos de 5 a 7 años.**
2. **El hueco está en los marketplaces regionales y en el componente fiscal local.** Ninguno de los líderes globales consultados (Sellerboard, A2X, Link My Books, TrueProfit) menciona Mercado Libre. Tampoco cubren Allegro, Bol, Zalando ni Kaufland en sus páginas [V][1][2][3][4]. En esos mercados aparecen herramientas locales o módulos de ERP, sin un líder claro [S][12][13].
3. **Brasil ya está poblado. México parece el mejor "segundo país" para la cuña argentina.** En Brasil hay al menos cinco herramientas de conciliación o lucro para Mercado Livre/Shopee (GE Finance, Koncili, TrackCash, Letzee, UpSeller, GoSmarter) [S][10][11]. En México, desde el 01/01/2026 las plataformas retienen **IVA 8 % e ISR 2,5 %** a personas físicas (las tasas para personas morales varían según la fuente). Eso genera saldos a favor y una conciliación fiscal que hoy se hace en Excel [S][14][15]. Es el mismo patrón que hizo fuerte la cuña en Argentina: la API del marketplace sumada al fisco local.
4. **Las tiendas de apps son baratas de entrar.** Shopify no cobra comisión sobre el primer USD 1 M de ingresos de **toda la vida** del desarrollador (antes era anual) y 15 % arriba de eso [V][6]. Amazon **canceló** en mayo de 2026 el cargo anual de USD 1.400 y la tarifa por llamadas GET de SP-API [S][7]. El problema es otro: hay unas 17.500 apps en Shopify y el 1 % superior concentra alrededor del 72 % de los ingresos estimados [S][8].
5. **Mensajería:** desde el 01/10/2026 Meta cobra los mensajes de servicio después de 1.000 gratis por número y mes. La tarifa de servicio es igual a la de utility: India USD 0,0014, Brasil 0,0068, México 0,0085, Indonesia 0,025, España 0,020, Argentina 0,026 [V][16 vía inv. AR][S][17]. Los ganadores (respond.io con USD 35 M de ARR, Manychat, Wati, Gupshup) venden plataforma horizontal [S][18]. Un jugador chico no compite ahí: compite con un flujo vertical encima.
6. **Soporte con IA:** el precio por resultado se volvió estándar. Intercom Fin cobra USD 0,99 por resultado [V][19], Zendesk USD 1,50–2,00 por resolución automatizada (inv. AR) y Gorgias USD 0,90–1,00 por interacción (inv. AR). Siena cobra alrededor de USD 750 por mes más USD 0,90 por ticket [S][22]. Sierra vale unos USD 15.800 M y Decagon USD 4.500 M [S][20]. **La parte de arriba está tomada. El espacio chico es vertical, por idioma y por integración logística local.**
7. **Reporting de agencias:** es un commodity global, con AgencyAnalytics a unos USD 20 por cliente [S][23]. Para agencias de Amazon hay suites de USD 279 a 1.499 por mes [S][23]. No conviene como cuña genérica.

---

## 2. Profit analytics y conciliación para vendedores: el equivalente global de la cuña #1

### 2.1 Jugadores y precios

| Herramienta | Foco | Precio publicado | Canales | Tracción declarada | Marca / fuente |
|---|---|---|---|---|---|
| **Sellerboard** (DE/US) | Rentabilidad para Amazon | Standard USD 19, Professional 29, Business 39, Enterprise 79 por mes (con pago anual: 15/23/31/63). Límite de 3.000 a 50.000 pedidos por mes | "Todos los marketplaces de Amazon", Shopify y Walmart; eBay sin detalle. **No menciona TikTok ni Mercado Libre** | "20K+ Amazon sellers" | [V][1] |
| **A2X** (NZ) | Conciliación de liquidaciones hacia contabilidad | Desde USD 29 por mes por canal (Amazon, Shopify, TikTok Shop, Etsy, eBay, PayPal); Walmart desde USD 79 | QuickBooks Online, Xero y NetSuite. **No menciona Mercado Libre** | "10,000+ ecommerce businesses, accountants and bookkeepers" | [V][2] |
| **Link My Books** (UK) | Conciliación para Xero y QuickBooks | La página no muestra precios sin usar el calculador. Tramos de 200 a 250.000 pedidos por mes | Amazon, eBay, Etsy, Shopify, Walmart (solo US), TikTok Shop (UK y US), WooCommerce y Square. **Sin Zalando, Bol ni OnBuy** | "1,000 accountants" en su programa de socios; 510+ reseñas en Xero | [V][3] |
| **TrueProfit** (VN, opera como US) | Ganancia neta para Shopify | USD 35 (300 pedidos), 60 (600), 100 (1.500) y 200 (3.500) por mes, con cargo por pedido excedente | Shopify más gasto en anuncios (Meta, Google, TikTok, Amazon). Ofrece **MCP para Claude y ChatGPT** | 4,9 estrellas con 923 reseñas en Shopify; lanzada el 31/07/2019 | [V][4] |
| **Triple Whale** (US) | Atribución y analítica para marcas DTC | No relevado | Shopify y anuncios | Ingresos estimados entre USD 15 M y 63,6 M según la fuente. Unos USD 50–56 M de financiación con participación de Shopify. Compró Anteater (visibilidad en buscadores de IA) en 01/2026 | [S][5] |
| Helium 10 Profits, BeProfit, Lifetimely | Igual categoría | No relevado en esta ronda | — | — | [NE] |
| Shopkeeper (DE) | Rentabilidad multicanal con foco en Europa | No se pudo consultar: el dominio está bloqueado en la red de esta sesión | — | — | [NE] |

**Lectura [E]:** el precio de referencia global para el vendedor individual está entre USD 19 y 100 por mes. Hay MCP y conectores con IA incluso en apps de nicho (TrueProfit). Diferenciarse por "dashboard con IA" no alcanza.

### 2.2 Marketplaces regionales: dónde está el hueco

| Mercado | Qué se encontró | Lectura |
|---|---|---|
| **Mercado Livre y Shopee (Brasil)** | GE Finance, Koncili, TrackCash y Letzee (conciliación de repasses, panel financiero y Ads de ML), GoSmarter (servicio de conciliación, "+1.000 sellers" atendidos) y UpSeller (ERP con informe de ganancia por pedido para ML y Shopee, actualizado en 03/2026) [S][10][11]. Ninguno publica precios en las páginas vistas [NE]. Shopee cobra 20 % + R$ 4 a vendedores CNPJ en ítems de hasta R$ 79,99 desde 03/2026 [S][10] | **Poblado.** Entrar desde Argentina sin ventaja local es difícil [E] |
| **Mercado Libre y Amazon (México)** | UpSeller ofrece un informe de ganancia por pedido de ML que contempla IVA, ISR y retenciones [S][13]. Jaguar Sheet publica contenido en español neutro [S][13]. En Workana hay un pedido de software que conecte Amazon y ML México por API, señal de oferta escasa [S][13]. Plazos de liberación en ML MX: 2 a 6 días después de la entrega con Mercado Envíos; hasta 28 días sin él [S][13] | **Hueco relativo.** Hay competencia de ERP, pero no se vio un líder específico de rentabilidad más retenciones [E] |
| **Allegro (PL), Bol (NL/BE), Zalando y Kaufland (DE)** | FiveX (Bol, ganancia por SKU), Polar Analytics (P&L con Allegro), MarżoMat (calculadora para Allegro) y conectores de ERP (ECOSIRE para ERPNext y Odoo, que importan liquidaciones de Allegro, Zalando y Kaufland) [S][12]. La comisión de Zalando estaría entre 5 y 25 %, negociada por marca [S][12] | Fragmentado. Requiere idioma local, IVA de la UE y OSS; es lejano para Federico [E] |
| Falabella, Amazon MX (aparte de lo anterior), Shopee SEA | No relevado | [NE] |

### 2.3 México: el componente fiscal que replica la ventaja argentina

- Desde el **01/01/2026** las plataformas digitales retienen a personas físicas **ISR 2,5 %** (antes 1 %) e **IVA 8 %**, la mitad del 16 % [S][14] (blog de Mercado Pago México, más una guía de beancount.io del 09/09/2026).
- Para **personas morales** las fuentes no coinciden: unas hablan de 4 % de ISR y otras de 2,5 %. Sin RFC, la retención de ISR sube al 20 % [S][14][15]. **Hay que confirmarlo en el art. 113-A de la LISR y en la LIF 2026** [NE en fuente oficial SAT].
- La retención del 50 % del IVA suele superar el IVA neto a pagar y genera **saldos a favor** [S][15] (temario del curso "Plataformas Digitales 2026" de El Contribuyente). Las cámaras empresariales reclaman por el impacto en la liquidez de las mipymes [S][14].
- **Implicancia [E]:** el vendedor mexicano necesita cruzar ventas, comisiones, retenciones (CFDI de retenciones), liberaciones de Mercado Pago y depósitos, y después recuperar o compensar saldos. Es el mismo problema "API del marketplace más fisco" que en Argentina, con un contador como canal natural de venta. La API de Mercado Libre es la misma en todos los países, así que el núcleo técnico armado para Argentina se reutiliza.

---

## 3. Economía de las tiendas de apps y de las APIs de marketplaces

| Plataforma | Condición para desarrolladores 2025/2026 | Marca / fuente |
|---|---|---|
| **Shopify App Store** | 0 % de comisión sobre el **primer USD 1 M de ingresos de toda la vida** y 15 % arriba de ese monto. Rige desde el 16/06/2025 (changelog publicado el 24/04/2025). Las ganancias anteriores al 01/01/2025 no cuentan. Se suman los ingresos de todas las cuentas asociadas del partner | [V][6] |
| Shopify: tamaño | Unas 17.000 a 17.900 apps listadas en 2026. El 1 % superior (225 apps) se quedaría con cerca del 72 % de los ingresos estimados (estimación basada en precios públicos, no en facturación). Los pagos a desarrolladores tienen cifras contradictorias (USD 890 M por año, o "más de USD 1.300 M") | [S][8] |
| **Amazon SP-API** | El 03/11/2025 Amazon anunció un cargo anual de USD 1.400 (desde el 31/01/2026) y USD 0,40 por cada 1.000 llamadas GET (desde el 30/04/2026) para desarrolladores de terceros. El **12/05/2026 lo canceló**, según correos a desarrolladores citados por Novadata y Fivetran. La página oficial del anuncio devuelve 404 | [S][7] |
| **TikTok Shop Partner Center** | Hay una tienda de apps para sellers (conectores, atención al cliente). Un evento para desarrolladores menciona "zero commission" en compras dentro de la app, sin condiciones. Las apps pasan una revisión de "Data Security Compliance" | [S][9]; condiciones oficiales [NE] |
| **Mercado Libre / Mercado Livre Developer Partner Program** | Certifica apps con medallas Silver, Gold y Platinum. Exige cumplir "cambios obligatorios" en plazo (15 días en la versión chilena) bajo pena de perder la certificación. Global Selling pide una cuota de GMV mensual. Página en portugués actualizada el 03/03/2026 | [V][24] |
| Mercado Libre: contexto | GMV de Commerce +36 % interanual en el 2T 2026; Brasil +39 % | [S][24b] |

**Lectura [E]:** el costo de entrada a las tiendas es casi cero (Shopify y SP-API sin cargo hoy). La barrera es la distribución dentro de la tienda y las certificaciones, como el Developer Partner Program de ML. Amazon ya mostró que puede cobrar el acceso, así que hay riesgo de que vuelva a intentarlo ("at this time").

---

## 4. Mensajería conversacional global

### 4.1 Tarifas de WhatsApp Business desde el 01/10/2026 (USD por mensaje entregado)

| Mercado | Marketing | Utility / Authentication | Service (desde el mensaje 1.001 del mes) | Fuente |
|---|---|---|---|---|
| India | 0,0118 | 0,0014 | 0,0014 | [S][17] |
| Brasil | 0,0625 | 0,0068 | 0,0068 | [V][16] (inv. AR) / [S][17] coincide |
| México | 0,0397 (subió el 01/10/2026) | 0,0085 | 0,0085 | [V][16] (inv. AR) / [S][17] coincide |
| España | 0,0707 (subió el 01/07/2026) | 0,0200 | 0,0200 | [S][17]; cambio de marketing [V][16] |
| Indonesia | 0,0411 | 0,0250 | 0,0250 | [S][17] |
| EE. UU. | 0,0250 | 0,0034 | 0,0034 | [S][17] |
| Alemania | 0,1365 | 0,0550 | 0,0550 | [S][17] |
| Argentina (referencia) | 0,0618 | 0,0260 | 0,0260 | [V][16] (inv. AR) |

- **Reglas comunes [V][16]:** 1.000 mensajes de servicio gratis por número y mes, sin acumulación. La ventana de entrada gratuita (Click-to-WhatsApp) dura hasta 7 días y no cobra marketing, utility, authentication ni service. Meta Business Agent cobra aparte, USD 2 por millón de tokens según Meta (inv. AR). Brasil puede facturar en BRL desde el 01/07/2026.
- **Lectura [E]:** un bot de soporte con 6 respuestas por conversación cuesta en Meta unos USD 0,008 por conversación en India, 0,05 en México y 0,15 en Indonesia o Argentina. **México y Brasil son mercados baratos para soporte por WhatsApp.** En España, Indonesia y Argentina conviene agrupar respuestas.

### 4.2 Política 4.7 de Meta sobre IA

- La sección 4.7 de los términos de WhatsApp Business Platform (modificada el 23/09/2026) prohíbe a los "AI Providers" usar la plataforma cuando la IA es la oferta principal. También prohíbe entrenar modelos con los datos, salvo el ajuste fino de uso exclusivo del negocio [V][25] (inv. AR). Rige para cuentas nuevas desde el 15/10/2025 y para existentes desde el 15/01/2026. Meta dijo que no apunta a la atención al cliente con IA [S] (inv. AR, respond.io y TechCrunch).
- **Implicancia [E]:** un asistente de soporte o posventa de un comercio está permitido. No se puede construir un modelo compartido entrenado con las conversaciones de todos los clientes.

### 4.3 Quiénes ganan

| Empresa | Dato | Marca / fuente |
|---|---|---|
| **respond.io** (MY) | Serie B de USD 62,5 M (06/2026, liderada por Camber Partners). USD 35 M de ARR y +169 % interanual (autodeclarado). Precios de USD 79 a 279 por mes con pago anual | [S][18]; precios [V] (inv. AR) |
| **Manychat** (US) | USD 140 M de capital de crecimiento (Summit Partners), "ya rentable", sin fecha confirmada. Latka estima USD 34,6 M de ingresos y 1 M de clientes | [S][18] |
| **Wati** (IN) | Serie B con Peak XV (≈ 2022). Latka estima unos USD 9,7 M de ingresos (dato poco confiable). Precios de USD 59 a 279 por mes | [S][18]; precios [V] (inv. AR) |
| **Gupshup** (IN) | Latka muestra cifras contradictorias (USD 309–361 M de ingresos) | [S][18], no confiable |
| Yalo, Zoko, Interakt | No relevado en esta ronda | [NE] |

**Lectura [E]:** las plataformas horizontales ya tienen escala, capital y presencia en India, LatAm y el sudeste asiático. Un recién llegado no gana compitiendo como otra plataforma. Puede ganar como capa vertical (posventa con transportista local, cobranza, turnos) sobre la plataforma que el comercio ya usa o sobre la API directa como Tech Provider.

---

## 5. Soporte al cliente con IA

| Producto | Modelo de precio | Dato de tracción | Marca / fuente |
|---|---|---|---|
| **Intercom Fin** | USD 0,99 por resultado: resolución confirmada, cliente que deja de pedir ayuda o workflow completado, incluidas las derivaciones. Un cobro por conversación. Con un helpdesk que no sea Intercom (por ejemplo Salesforce) hay mínimo mensual de unos 50 resultados y no hay cargos por asiento ni por implementación. Asientos de Intercom: USD 19 (promo), 85 y 132 | "Thousands of businesses" (sin cifra) | [V][19] |
| **Zendesk** | Resolución automatizada a USD 1,50 comprometida o 2,00 a demanda; incluye 5 o 10 por agente | — | [V] (inv. AR, página del 09/10/2026) |
| **Gorgias** | AI Agent a USD 0,90–1,00 por interacción automatizada (1,50 fuera del plan). Helpdesk de USD 10 a 900 por mes | Objetivo declarado: automatizar 60 % o más | [V] (inv. AR); [S][22] |
| **Siena AI** (RO/US) | Unos USD 750 por mes más USD 0,90 por ticket automatizado; funciona sobre Gorgias, Zendesk e Intercom | Serie A de USD 17 M, total USD 29,7 M (2026) | [S][22] |
| **Sierra** | Por resultado; unos USD 1,50 por resolución según reportes de contratos | Valuación de unos USD 15.800 M (05/2026). ARR de más de USD 150 M a 02/2026 (autodeclarado) | [S][20] |
| **Decagon** | Por conversación o por resolución. Contratos reportados de unos USD 50.000 por año de plataforma más uso | Valuación de USD 4.500 M (01/2026); ARR no informado | [S][20] |

**Espacio para un jugador chico [E]:**
- El precio de referencia ya es USD 0,90–2,00 por resolución. Un jugador chico no puede cobrar más salvo que resuelva casos que los genéricos no resuelven.
- Esos casos son los que exigen **acción sobre sistemas locales**: transportistas (Estafeta, DHL MX, J&T, Correios, Andreani), cambios y devoluciones con logística inversa, el estado de envío de Mercado Envíos, facturación (CFDI o factura argentina) y pagos locales (OXXO, Pix, Mercado Pago).
- Fin y Siena integran helpdesks, no transportistas regionales. No se verificó la cobertura de transportistas de cada uno [NE].
- El idioma por sí solo no defiende: Fin y los otros son multilingües [E].

---

## 6. Reporting de agencias y CRM verticales

| Segmento | Dato | Marca / fuente |
|---|---|---|
| Reporting genérico | AgencyAnalytics a unos USD 20 por cliente y mes con pago anual. DashThis desde USD 44 por mes (cobra por fuente desde 03/2026). Databox desde USD 79 | [S][23] |
| Agencias de Amazon | Suites desde USD 279 hasta 1.499 por mes. Novadata cobra por cuenta de Amazon. Intentwise ofrece webinars sobre "the 2026 reporting stack for Amazon agencies". Las agencias de Amazon cobran entre USD 1.500 y 25.000 o más por mes a sus clientes | [S][23] |
| Agencias de TikTok Shop | Existe un programa de partners con agencias (por ejemplo TikTokWiz, 06/2026) | [S][9]; herramientas específicas [NE] |

**Lectura [E]:** el reporting de anuncios está saturado. El nicho defendible es el que la agencia no puede armar sola: **margen real neto de comisiones, retenciones y devoluciones por cuenta de cliente**. Así se vende la herramienta de rentabilidad a agencias de Mercado Libre o Amazon en México, que es la misma estrategia de canal que en Argentina.

---

## 7. Huecos y riesgos resumidos

| Hueco | Evidencia | Riesgo |
|---|---|---|
| Rentabilidad más retenciones para vendedores de ML y Amazon en **México** | Las herramientas globales no cubren ML; en México se ven sobre todo ERP (UpSeller) y planillas; retenciones nuevas desde 01/2026 [V][1–4][S][13–15] | Tasas fiscales en discusión; UpSeller u otros ERP pueden sumar la función; ML puede mejorar su propio reporte |
| Conciliación de marketplaces europeos | Fragmentación, módulos de ERP [S][12] | Idioma, IVA de la UE y distancia comercial |
| Posventa y WISMO con transportistas regionales en LatAm | Los generalistas cobran USD 0,90–2,00 por resolución; WhatsApp es barato en MX/BR [V][19][S][17] | Meta Business Agent, Chat Nube y otros jugadores nativos; acciones sobre pedidos reales |
| Profit analytics de Shopify o Amazon US | Saturado: Sellerboard USD 19, TrueProfit, Triple Whale [V][1][4] | No recomendado |

---

## 8. Implicancias para Federico

**Cuña global 1, recomendada: "Margen real y conciliación fiscal para vendedores de Mercado Libre (y Amazon) en México", vendida a despachos contables y agencias de ML.**
- *Por qué:* reutiliza casi todo el núcleo argentino, porque la API de Mercado Libre y Mercado Pago es la misma. Le suma el problema fiscal mexicano nuevo de 2026: retenciones de IVA 8 % e ISR 2,5 % o más, CFDI de retenciones y saldos a favor [S][14][15]. Los líderes globales (Sellerboard, A2X, Link My Books, TrueProfit) no cubren Mercado Libre [V][1–4].
- *Precio de referencia [E]:* el vendedor suelto ancla en USD 19–60 por mes. Por eso conviene vender al **despacho contable** por cartera (por ejemplo, por RFC conciliado por mes) o a la agencia por cuenta.
- *Validar antes de construir:*
  - la tasa vigente para personas morales en la LISR y la LIF 2026;
  - si ML México entrega por API el detalle de retenciones por orden [NE];
  - el precio y la cobertura real de UpSeller y de cualquier jugador local;
  - 10 entrevistas con contadores que atiendan vendedores de ML.
- *Expansión:* Amazon MX con SP-API, sin cargo hoy [S][7]; TikTok Shop MX si abre la API. Brasil solo con un socio local, porque está poblado [S][10][11].

**Cuña global 2, secundaria: "Posventa por WhatsApp con transportistas locales" en México y Brasil, cobrada por resolución.**
- *Por qué:* el mensaje de servicio cuesta USD 0,0085 en México y 0,0068 en Brasil, de 3 a 4 veces menos que en Argentina [V][16]. Los generalistas (Fin a USD 0,99, Zendesk a 1,50–2,00, Siena a USD 750 por mes más 0,90) no integran, hasta donde se vio, transportistas regionales ni Mercado Envíos [V][19][S][22][NE].
- *Precio [E]:* USD 0,40–0,70 por pedido resuelto, debajo de Fin, con tope mensual.
- *Riesgos:* que Meta Business Agent o el propio marketplace lo resuelvan; la política 4.7 (posicionarse como canal del comercio, sin entrenar un modelo compartido); las acciones sobre pedidos reales.
- Conviene arrancarla solo después de validar la cuña 1, porque comparte canal (agencias y tiendas) [E].

**No hacer:** profit analytics para Shopify o Amazon US, reporting genérico de agencias, ni otra plataforma horizontal de WhatsApp.

---

## 9. Fuentes

| # | Fuente | URL | Fecha |
|---|---|---|---|
| 1 | Sellerboard, página principal con precios | https://sellerboard.com/en/ | Consultada el 30/10/2026 |
| 2 | A2X, precios | https://www.a2xaccounting.com/pricing | Consultada el 30/10/2026 |
| 3 | Link My Books, precios | https://linkmybooks.com/pricing | Consultada el 30/10/2026 |
| 4 | Shopify App Store, TrueProfit | https://apps.shopify.com/trueprofit | Consultada el 30/10/2026 |
| 5 | Triple Whale: estimaciones de StartupHub, Caplight y ecommercefastlane | https://www.startuphub.ai/startups/triple-whale ; https://www.caplight.com/company/triple-whale ; https://ecommercefastlane.com/triple-whale-review/ | 2026 |
| 6 | Shopify.dev changelog, "Update to Shopify's app developer revenue share" | https://shopify.dev/changelog/update-to-shopifys-app-developer-revenue-share | Publicado el 24/04/2025; vigente desde el 16/06/2025 |
| 7 | Cancelación de las tarifas de SP-API: Novadata, Fivetran y PPC Land | https://novadata.io/resources/news/amazon-cancels-sp-api-fees-may-2026 ; https://www.fivetran.com/blog/no-walled-gardens-amazon-reversed-its-seller-partner-api-fees ; https://ppc.land/amazon-drops-sp-api-fees-after-developer-pushback | 05–07/2026 |
| 8 | Estadísticas de la Shopify App Store: AppJubilee, RevenueHunt y MageComp | https://www.appjubilee.io/shopify-app-store-report-2026 ; https://revenuehunt.com/state-of-the-shopify-app-economy/ ; https://magecomp.com/blog/shopify-app-store-statistics/ | 2026 |
| 9 | TikTok Shop developer events; TikTokWiz Partner Program | https://tiktokshopdeveloper.splashthat.com/TT4Drecap ; https://ipsnews.net/business/2026/06/10/tiktokwiz-joins-tiktok-shop-partner-program-following-record-year-of-member-sales-growth/ | 2026 |
| 10 | GoSmarter, "Conciliação financeira marketplace" | https://gosmarter.com.br/conciliacao-financeira-marketplace/ | Publicada el 25/02/2026; actualizada el 20/05/2026 |
| 11 | UpSeller, relatório de lucros Mercado Livre/Shopee | https://upseller.com/pt/help-doc-article-1544 | Actualizado en 03/2026 |
| 12 | FiveX (Bol), Polar Analytics (Allegro), ECOSIRE (comisiones en Alemania) | https://fivex.com/integrations/bol/ ; https://www.polaranalytics.com/integration-draft/allegro ; https://ecosire.com/ar/blog/german-marketplace-seller-fees-comparison | 2026 |
| 13 | UpSeller ES (ganancia ML México); Jaguar Sheet; Workana | https://www.upseller.com/es/help-doc-article-1394 ; https://jaguarsheet.com/es/blog/rentabilidad-mercado-libre ; https://www.workana.com/es/job/software-para-analizar-rentabilidad-de-tienda-de-amazon-y-mercado-libre | 2025–2026 |
| 14 | Mercado Pago MX, "Cambios fiscales 2026"; El Contribuyente; DPL News; IDC Online | https://www.mercadopago.com.mx/blog/cambios-fiscales-mexico ; https://www.elcontribuyente.mx/2025/11/en-2026-vender-en-plataformas-digitales-sera-mas-caro-habra-nuevas-retenciones/ ; https://dplnews.com/?p=328946 ; https://idconline.mx/fiscal-contable/2025/10/10/retenciones-a-personas-morales-por-plataformas-digitales-2026 | 10/2025–2026 |
| 15 | Temario "Plataformas Digitales 2026" (El Contribuyente); Siempre al Día; beancount.io | https://img.elcontribuyente.mx/cursos/Temario_Plataformas_Digitales_2026.pdf ; https://siemprealdia.co/mexico/fiscal/retencion-de-isr-en-plataformas-digitales/ ; https://beancount.io/es/blog/2026/09/09/mexico-digital-platform-vat-withholding-b2b-sellers-marketplace-guide | 2026 |
| 16 | Meta, "Pricing on the WhatsApp Business Platform" y rate cards en USD (descargadas el 29/10/2026 por la inv. AR) | https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md ; https://developers.facebook.com/docs/whatsapp/pricing#rate-cards | Consultada el 30/10/2026 |
| 17 | ChatMaxima, "WhatsApp Service Message Pricing from October 1, 2026" (tabla por país) | https://chatmaxima.com/blog/whatsapp-service-message-pricing-october-2026/ | 03/09/2026 |
| 18 | respond.io Serie B (Profit/Pakistan Today); Manychat (cxm.world); Wati (CB Insights); Latka | https://profit.pakistantoday.com.pk/2026/06/18/respondio-secures-dollar625-million-series-b-to-drive-global-expansion ; https://cxm.world/?p=130972 ; https://www.cbinsights.com/company/wati/financials ; https://getlatka.com/companies/industries/i-conversational-marketing-software | 06/2026 y s/f |
| 19 | Intercom, precios (Fin) | https://www.intercom.com/pricing | Consultada el 30/10/2026 |
| 20 | Sierra y Decagon: ai2.work, fin.ai, dragapp | https://ai2.work/blog/sierra-hits-15b-valuation-as-ai-agents-reach-production ; https://ai2.work/blog/decagon-hits-4-5b-valuation-as-ai-support-agents-scale-2026 ; https://www.dragapp.com/blog/decagon-vs-sierra/ | 2026 |
| 21 | Zendesk, Gorgias y Freshdesk, precios (inv. AR, detalle 04) | https://www.zendesk.com/pricing/ ; https://www.gorgias.com/pricing | 09–29/10/2026 |
| 22 | Siena AI: Pulse 2.0, Romania Insider, myaskai; Gorgias (Silicon UK) | https://pulse2.com/siena-raises-17-million-series-a-bringing-total-funding-to-29-7-million/ ; https://www.romania-insider.com/romanian-founded-ai-startup-siena-raises-usd-17-million ; https://myaskai.com/blog/siena-ai-complete-guide-2026 ; https://www.silicon.co.uk/press-release/gorgias-raises-29m-in-new-funding-to-lead-the-new-era-of-ai-powered-customer-experience-for-ecommerce | 2026 |
| 23 | Reporting de agencias: Coupler, Swydo, Sellersonar, Novadata, Intentwise | https://blog.coupler.io/?p=85540 ; https://www.swydo.com/blog/best-client-reporting-software/ ; https://sellersonar.com/blog/amazon-agency-software/ ; https://novadata.io/who-we-serve/agencies ; https://www.intentwise.com/webinars/the-2026-reporting-stack-for-amazon-agencies | 07/2026 |
| 24 | Mercado Livre, Developer Partner Program | https://developers.mercadolivre.com.br/pt-br/developer-partner-program | Actualizada el 03/03/2026 |
| 24b | GiroNews, resultados del 2T 2026 de Mercado Livre | https://gironews.com/varejo-digital/mercado-livre-supera-us-10-bilhoes-em-receita-no-2o-trimestre/ | 2026 |
| 25 | Meta Terms for WhatsApp Business Platform, §4.7 (inv. AR) | https://www.facebook.com/legal/Meta-Terms-for-WhatsApp-Business-Platform | Last Modified 23/09/2026 |

**Pendientes [NE]:**
- precios de Helium 10 Profits, BeProfit, Lifetimely, Shopkeeper (dominio bloqueado en esta sesión), Koncili, GE Finance y TrackCash;
- tarifas oficiales de Meta para India, Indonesia y España (solo fuente secundaria);
- condiciones oficiales del TikTok Shop Partner Center;
- tasa definitiva de ISR para personas morales en México;
- disponibilidad por API del detalle de retenciones en ML México.
