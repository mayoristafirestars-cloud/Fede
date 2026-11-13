# 04 — Panorama competitivo local (Argentina y Uruguay): software para mayoristas y distribuidoras

*Relevamiento: 20/10/2026. Los precios en ARS cambian cada 2–4 meses por inflación, y en septiembre de 2026 el IPC fue de 1,9% mensual y 33,4% interanual ([iProUP](https://www.iproup.com/finanzas/72300-indec-confirma-inflacion-de-19-en-septiembre-categorias-con-mayor-aumento)). Tómenlos como orden de magnitud. Casi todas las comparativas que se citan las publica un proveedor, así que tienen sesgo.*

---

## 0. Resumen ejecutivo

- El mercado está **fragmentado en tres capas que casi nunca se hablan entre sí**:
  1. **ERP/facturación:** Tango, Bejerman, Xubio, Colppy, Dux, Contabilium, FactuPyme.
  2. **Canal de pedidos B2B / catálogo:** Tiendanube mayorista, VentasxMayor, Commercy, Pedix, VentaClick.
  3. **Preventa / reparto en calle:** CHESS/Nextbyn, Cair, Líder, BCNSoft, Flexxus App.
- La suite que integra las tres capas es **CHESS (Nextbyn)**. Apunta a distribuidoras grandes de consumo masivo (clientes como AB InBev, Danone o Unilever), cotiza a medida y cuesta caro.
- Para la **PyME mayorista de 5 a 50 empleados** no hay un producto barato que haga lo siguiente sin integraciones caseras: catálogo privado con lista de precios por cliente, preventa offline, cuenta corriente y cobranzas, y factura ARCA.
- Los grandes jugadores (BEES/Quilmes, Juntos+ de Coca-Cola FEMSA, Mercado Libre Negocios) **digitalizan al almacenero para su propio portafolio**. Eso educa al comprador a pedir por app y deja expuesto al mayorista independiente, que hoy sigue con WhatsApp y PDF.

---

## 1. ERP / gestión / facturación para PyMEs

| Producto | Qué hace / target | Precio público (ARS/mes) | Fortalezas | Debilidades para mayoristas |
|---|---|---|---|---|
| **Tango Gestión / Tango Nube (Axoft)** | ERP líder en PyMEs medianas, mayoristas y distribuidoras | Tango Nube: Básica (2 puestos) $731.000 + IVA y Pro (5 puestos) $912.000 + IVA, con permanencia de 6 meses ([SpomSolutions, sep-2026](https://app.spomsolutions.com/blog/cuanto-cuesta-erp-argentina-2026)). Otra fuente: SaaS básico desde ~$180.000/mes y licencias perpetuas de $0,6M a $1,5M ([Develop Argentina](https://developargentina.com/blog/sistemas-gestion-comercial-argentina-2026)). Se vende por módulos y puestos concurrentes ([formulario Axoft](https://www.consejo.org.ar/storage/attachments/FORMULARIO%20TANGO%20SOFTWARE.pdf-jnmWYZsJBB.pdf)) | Estándar de facto; los contadores lo conocen; red de distribuidores | La preventa móvil y el B2B requieren módulos extra o desarrollos a medida ([Wynges](https://wynges.com/blog/top-7-programa-de-gestion-para-distribuidoras-optimiza-tu-logistica-y-facturacion-erp-distribuidoras-tango-softland-xubio-sap-odoo-oracle/)). Las instalaciones locales viejas sin API obligan a sincronizar por scripts o archivos planos ([búsqueda: ecommercemayorista.com](https://ecommercemayorista.com/integraciones/erp-softland-tango-b2b-argentina/)) |
| **Bejerman** | ERP administrativo-contable, muy usado por estudios contables | No publica precio | Fuerte en lo fiscal y administrativo | Poco foco en mostrador, preventa y armado de pedidos ([Wynges](https://wynges.com/blog/top-7-programa-de-gestion-para-distribuidoras-optimiza-tu-logistica-y-facturacion-erp-distribuidoras-tango-softland-xubio-sap-odoo-oracle/)) |
| **Xubio** | Gestión y contabilidad cloud | Básico $123.100, Estándar $198.700, Avanzado $268.300 y Pro $375.900, todos + IVA ([SpomSolutions](https://app.spomsolutions.com/blog/cuanto-cuesta-erp-argentina-2026)) | Cloud, multiempresa, apreciado por contadores | Sin canal B2B ni preventa propios |
| **Colppy** | Contable-administrativo cloud | $128.500 a $310.900 + IVA (mismo relevamiento) | Contabilidad, fácil para el estudio | Ídem |
| **Contabilium** | Gestión cloud PyME con integraciones e-commerce | $122.000 a $245.000 + IVA (mismo relevamiento) | Se integra con tiendas online y VentasxMayor | Sin preventa offline nativa |
| **Alegra** (Colombia) | Facturación y gestión simple | $19.999 a $79.999 + IVA (mismo relevamiento) | Barato | Adaptación a ARCA menos robusta que la de los locales (misma fuente) |
| **Dux Software** | SaaS PyME con presencia creciente en distribuidoras chicas | No publica precios; en el app store de Tiendanube figura ~$24.800/mes ([Tiendanube Apps](https://www.tiendanube.com/tienda-aplicaciones-nube/dux-software-erp)) | Varias listas de precios, precios en ARS o USD, factura automática ([Ayuda Tiendanube](https://ayuda.tiendanube.com/139131-aplicaciones-de-gestion-y-facturacion/como-integrar-dux-software-con-mi-tienda)) | Hay reseñas negativas sobre la sincronización de stock ([Software Advice](https://www.softwareadvice.com.au/software/489738/Dux-Software)) |
| **FactuPyme** (lo usa el equipo hoy) | Facturación ARCA con QR, stock, ventas, mesas/comandas, catálogo y tienda online. Target: almacenes, ferreterías, indumentaria, gastronomía, gimnasios | Plan PyME y Plan Negocio, con el primer mes gratis; el precio se informa por WhatsApp ([factupyme.com.ar](https://www.factupyme.com.ar)) | Simple, usuarios ilimitados, soporte por WhatsApp | **Orientado a retail y gastronomía**: no tiene preventa, listas por cliente ni cuenta corriente mayorista avanzada. Hoy es la base de la operación del equipo y a la vez su límite |
| **Flexxus** | ERP con vertical "Distribuidores y Mayoristas"; app de vendedores con hoja de ruta, pedidos, cobros y "no venta" | Cotiza; se ofrece en nube, alquiler o compra, con licencias concurrentes ([formulario Flexxus](https://www.consejo.org.ar/storage/attachments/FORMULARIO%20Flexxus.pdf-IFxGsckRKq.pdf), [App Store](https://apps.apple.com/ca/app/flexxus-app/id6746650391)) | Cubre preventa y ERP | La app depende del ERP completo; capacitación mínima de 8 h |
| **Líder Gestión (Wynges)** | ERP para distribuidoras: preventa offline, listas por cliente, multidepósito, ruteo, ARCA con percepciones, integración con WhatsApp, ML y Tiendanube | Licencia perpetua más mantenimiento; no publica monto ([Wynges](https://wynges.com/software-distribuidora-mayorista-sistema-pedidos-movil/)) | El paquete más parecido a "todo en uno PyME" | Modelo desktop y on-premise, interfaz tradicional |
| **BCNSoft** | POS, stock, compras, app de preventistas y ARCA | $199.900 mensual / $149.900 semestral / $84.900 anual + IVA, más un setup de $199.900, con 2 licencias ([bcnsoft](https://bcnsoft.com.ar/software-para-distribuidoras/)) | Precio público, foco en distribuidora y almacén | Instalación en Windows; **no tiene portal B2B de autopedido** |
| **SAP B1, Dynamics BC, Odoo, Calipso, Softland, Totvs, NetSuite** | Medianas y grandes | Odoo Enterprise desde USD 24,90 por usuario/mes más una implementación de USD 2.000 a 15.000 ([Develop Argentina](https://developargentina.com/blog/sistemas-gestion-comercial-argentina-2026)). Los ERP corporativos piden USD 30k a 150k iniciales ([Wynges](https://wynges.com/blog/top-7-programa-de-gestion-para-distribuidoras-optimiza-tu-logistica-y-facturacion-erp-distribuidoras-tango-softland-xubio-sap-odoo-oracle/)) | Escalan | Dependen de consultores; sobredimensionados para una PyME ([Norte en Línea](https://norteenlinea.com/erp-para-distribuidoras-que-opciones-existen-en-argentina/)) |
| Otros: Siigo AR, Gestix, Syscom | Siigo $29k–89k; Gestix desde $15k; Syscom (consumo masivo y rutas) ~$250k–800k por cotización ([Develop Argentina](https://developargentina.com/blog/sistemas-gestion-comercial-argentina-2026)) | | | |

No conseguí datos públicos de Holistor, Sistema Lince, Gestión Total, Calipso, Finnegans, Fénix, Zeus, Siasa ni Algoritmo; en general cotizan a medida.

**Lectura:**
- El **piso real** de un ERP cloud "serio" en Argentina hoy está en **$120.000–$200.000 + IVA por mes** (~USD 100–150).
- Las soluciones con preventa están en **$200.000–$900.000 por mes**.
- Eso deja espacio de precio para un producto vertical en la franja de USD 80–250 por mes.

---

## 2. Canal B2B: pedidos online y catálogo mayorista

| Producto | Qué hace | Precio | Comentario |
|---|---|---|---|
| **Tiendanube "ventas mayoristas"** | Tablas de precio por grupo de clientes, mínimos por monto o cantidad, catálogo visible solo tras login, checkout separado, stock compartido con minorista ([Tiendanube](https://www.tiendanube.com/soluciones/ventas-mayoristas)) | Incluido desde el plan Impulso (1 tabla), Escala (3) y Evolución (ilimitadas). Ajusta precios trimestralmente por inflación y cobra 0,7%–2% por transacción ([Ayuda Tiendanube](https://ayuda.tiendanube.com/123482-planes/como-se-ajusta-el-precio-de-los-planes-de-tiendanube)) | Es el competidor por default para el mayorista textil y de nicho. **No tiene preventa, cuenta corriente ni ruteo**, y la lógica es de e-commerce B2C adaptado |
| **VentasxMayor** (AR) | E-commerce B2B white-label: listas por cliente, descuentos por volumen, "Modo Pro" de catálogo en tabla, app de vendedor, IA vendedora (beta), API, integraciones con Dux, Contabilium y Dragonfish ([ventasxmayor.com](https://ventasxmayor.com/)) | Abono fijo, sin comisiones: "$150.000 fijos" ([Infonegocios, sep-2026](https://infonegocios.info/nota-principal/e-commerce-b2b-la-plataforma-argentina-que-facilita-las-ventas-mayoristas-150-000-fijos-y-sin-comisiones)); USD 99/mes en el sitio | **El competidor más directo de un portal B2B.** ~500 mayoristas, 8 países, 8 años en el mercado. Débil en preventa offline y en ARCA nativo (depende del ERP) |
| **Commercy** (AR) | POS, tienda online, canal B2B con código de invitación, listas por cliente, **cuenta corriente integrada**, factura A ARCA ([Commercy](https://commercy.com.ar/blog/plataforma-b2b-mayorista)) | B2B desde el plan Professional, USD 79/mes | Competidor directo "todo en uno liviano" |
| **VentaClick** (AR) | E-commerce B2B más SFA ("VendedorWeb"), sincronización con Tango, SAP B1 y Bejerman: stock, listas por cliente, cuentas corrientes ([G2](https://www.g2.com/products/ventaclick/discuss)) | No publica | Se monta sobre el ERP existente; apunta a medianas |
| **Open24, NexoSmart, Bitobee, agencias WooCommerce** | Portales B2B a medida o semi-SaaS integrados con Tango, Bejerman y Colppy ([Open24](https://open24.com.ar/ecommerce-b2b-argentina/), [NexoSmart](https://www.nexosmart.com.ar/soluciones/tienda-online-mayorista/), [Bitobee](https://bitobee.com/blog/ecommerce-b2b-mayorista-distribuidoras-latam)) | Por proyecto | Muestran que hay demanda; el servicio es costoso y poco escalable |
| **Pedix** | Catálogo y carrito que termina en un pedido por WhatsApp, para comercios de barrio | $19.000 / $25.500 / $35.000 por mes ([Pedix](https://info.pedix.app/)) | +3.000 tiendas en 6 países. Pensado para B2C; **no tiene listas por cliente ni cuenta corriente** |
| **Empretienda** | Tienda online barata, comprada por Ualá en 2022 ([Commercy](https://commercy.com.ar/blog/plataforma-b2b-mayorista)) | — | B2C |
| **WhatsApp Business (catálogo)** | Gratis | — | Es el "competidor" real: el status quo |
| **Mercado Shops** | Según reportes de 2024, Mercado Libre lo discontinuó; **no lo pude verificar en esta búsqueda** | — | Ver ML Negocios en la sección 4 |
| **Moda Avellaneda/Flores** | Modatex (marketplace de marcas mayoristas), Distrito Moda (carrito multimarca), "Avellaneda a un toque" (directorio viral). Muchos mayoristas usan Tiendanube ([Tiendanube blog](https://www.tiendanube.com/blog/proveedores-de-ropa/), [Cronista](https://www.cronista.com/informacion-gral/furor-por-la-app-que-muestra-los-mejores-locales-de-la-avenida-avellaneda-para-comprar-ropa-barata/)) | — | Vertical textil en crisis: la vacancia en la avenida subió 160% y compiten Temu y ML ([AméricaRetail](https://americaretail-malls.com/paises/argentina/como-mercado-libre-y-temu-desafian-al-comercio-tradicional-con-moda-barata/)) |

---

## 3. Preventa, fuerza de ventas y distribución en calle

| Producto | Qué hace | Precio | Comentario |
|---|---|---|---|
| **CHESS (Nextbyn)** | Suite vertical para distribuidoras de consumo masivo. Incluye CHESS ERP (ex "Distribuir"), **VENDO** (preventa), **ENTREGA** (reparto, cobranza y devoluciones), **MyB2B** (autopedido 24 h) y WMS (lotes y vencimientos), con trabajo offline ([Nextbyn](https://www.nextbyn.com/chess), [Norte en Línea](https://norteenlinea.com/erp-para-distribuidoras-que-opciones-existen-en-argentina/), [adquisición](https://blog.nextbyn.com/tecnologia-nextbyn-adquiere-chess)) | A medida | **El líder del vertical.** Clientes declarados: AB InBev, Quilmes, Danone, Unilever, Softys y BAT ([chess.com.ar](https://chess.com.ar/productos/)). Caro y de implementación pesada; no apunta al mayorista PyME multirrubro |
| **Cair** | App de preventa y reparto offline para distribuidoras de alimentos, con roles (preventista, repartidor, depósito), impresora térmica de 80 mm e import desde Excel o balanzas Kretz ([cair.com.ar](https://cair.com.ar/)) | **$50.000 por persona/mes** (de 1 a 25 personas); usuarios web gratis | Nuevo y ágil. **Todavía no tiene factura ARCA ni posnet** ("en desarrollo"). Muy buen benchmark de precio por usuario |
| **Preventa Fácil (NeoSistemas), Preventa (Galdon)** | Apps de preventa offline atadas a su propio ERP ([Google Play](https://play.google.com/store/apps/details?id=com.preventafacil&hl=en_US)) | Gratis para descargar; el precio está en el ERP | Nicho |
| **Flexxus App, Líder Móvil, BCNSoft** | Preventa dentro del ERP | Ver sección 1 | |
| **Syscom** | ERP para consumo masivo con rutas | ~$250k–800k/mes | |
| **SimpliRoute** (Chile) | Ruteo de última milla; +900 clientes, opera en Argentina ([SimpliRoute](https://simpliroute.com/about), [Crunchbase News](https://news.crunchbase.com/venture/simpliroute-plans-latin-american-expansion-following-3m-series-a/)) | Cotiza | Complemento, no sustituto |
| **Mercos** (Brasil) | Pedidos B2B y app de representantes ([B2B Stack](https://www.b2bstack.com.br/compare/vendasexternas-vs-mercos)) | Desde R$ 99/mes | **No encontré evidencia de que opere en Argentina.** Es el modelo a imitar ("Mercos argentino") |
| CPG Soft (UY) | Software de ventas y distribución de consumo masivo, con clientes mayormente en Argentina ([El Observador](https://www.elobservador.com.uy/nota/tras-20-anos-la-firma-cpg-soft-busca-ser-profeta-en-su-tierra-20132261780)) | — | Dato de 2013 |

No encontré información verificable de Moviltrack, Pedidos Móviles, Quinttos ni Alfasoft.

---

## 4. Grandes jugadores entrando al canal

- **BEES (Quilmes / AB InBev).** Es la app B2B para almacenes, kioscos y autoservicios. Vende el portafolio de Quilmes **más el de otras ~35 empresas** (yerba, snacks, café). Tiene más de 200–250 mil puntos de venta registrados, y los preventistas pasaron a ser "asesores" ([Infonegocios](https://infonegocios.info/plus/te-gustaria-que-tu-producto-tenga-la-misma-distribucion-que-quilmes-con-la-app-de-bees-ahora-es-posible), [Forbes AR](https://www.forbesargentina.com/lifestyle/quilmes-sigue-apostando-bees-su-app-ayudar-crecer-comerciantes-n8478)). **Es una amenaza directa al mayorista de almacén:** BEES actúa como "mayorista digital" del fabricante.
- **Juntos+ (Coca-Cola FEMSA).** Llegó a Argentina en octubre de 2025 con web, app y WhatsApp, pedidos 24 h, sugerencias con IA y programa de lealtad ([Mercado](https://mercado.com.ar/ruta-digital/coca-cola-femsa-introduce-juntos-app-en-argentina-para-digitalizar-la-gestion-de-comercios)).
- **Mercado Libre Negocios.** Es la unidad B2B de ML, en Argentina desde 2025, con 2,6 millones de productos mayoristas, descuentos de hasta 50%, factura B2B, roles de usuario, financiamiento de Mercado Pago y envíos ([Mercado](https://mercado.com.ar/negocios/mercado-libre-introduce-mercado-libre-negocios-plataforma-exclusiva-para-operaciones-b2b-en-argentina), [AméricaRetail](https://americaretail-malls.com/paises/brasil/mercado-libre-impulsa-el-comercio-mayorista-con-su-nueva-plataforma-b2b/)). Compite como **marketplace**, no como herramienta propia del mayorista.
- **Mercado Pago "Dinero Plus".** Créditos de hasta $10M a tasa 0 a 7–28 días para capital de trabajo de comercios ([NoticiasNQN](https://www.noticiasnqn.com.ar/noticias/2025/08/25/319241-mercado-pago-lanza-credito-a-tasa-cero-de-hasta-10-millones-para-comercios)). Financia al almacenero que le compra al mayorista, y ese financiamiento podría canalizarse desde la plataforma.
- **Ualá Bis.** Cobra 4,9% + IVA por cobro ([Ayuda Tiendanube](https://ayuda.tiendanube.com/uala-bis/preguntas-frecuentes-sobre-uala-bis)), compró Empretienda y Ceibo Créditos ([DPL News](https://dplnews.com/?p=164953)). Naranja X: sin datos específicos de B2B.
- **Scanntech** (origen uruguayo). Tiene datos de POS de autoservicios en 6 países, trabaja con más de 600 fabricantes, cerró una Serie F de USD 180M (oct-2026) y ofrece marketplace de promos financiadas por la industria ([DRNO](https://www.mrweb.com/drno/news40469.htm), [Scanntech Retail Day](https://cas.com.ar/wp-content/uploads/2022/08/Scanntech-Retail-Day-2022.pdf)). Puede ser socio (datos de sell-out) o competidor del lado del autoservicio.

---

## 5. Startups (2020–2026)

- **Centralo.** Marketplace mayorista móvil para kioscos y almacenes, con pago contra entrega, en etapa seed; en 2021 buscaba superar AR$4M en ventas ([Descubre VC](https://www.descubre.vc/centralo)).
- **Rintin.** Fundada por argentinos. Marketplace de comercios a fabricantes con crédito, logística e IA; levantó USD 6,2M liderada por Cometa (ago-2026). Opera en México y **evalúa Argentina** ([Cronista](https://www.cronista.com/infotechnology/entreprenerds/argentinos-crearon-un-marketplace-que-conecta-comercios-con-fabricantes-ya-levantaron-millones-de-dolares-para-expandirse/)).
- **MercadoMayor.** Marketplace B2B para kioscos, almacenes y autoservicios, sin comisión durante 2026 ([mercadomayor.com](https://mercadomayor.com/)).
- **EmprendeGO.** Conecta emprendedores con mayoristas verificados ([emprendego.com.ar](https://emprendego.com.ar/)).
- **Nilus.** Compras comunitarias de alimentos; reestructuró y transfirió su tecnología al PMA ([Descubre VC](https://www.descubre.vc/nilus)).
- **Cair, VentasxMayor y Commercy:** ver arriba.
- Logística de última milla (Moova, Treggo, SimpliRoute): son complementos de reparto, no de toma de pedido.

**Patrón:** la mayoría de las startups hace **marketplace** (se mete entre el mayorista y su cliente). Muy pocas hacen **SaaS que empodere al mayorista con su propia cartera**, que es justamente lo que el mayorista quiere para no perder margen ni cliente.

---

## 6. Uruguay

- **Memory**, comprada por Siigo (Colombia) ([Latin Lawyer](https://latinlawyer.com/article/colombian-software-provider-enters-uruguay)).
- **Zureo**: gestión retail desde 2007, con app "Zureo Móvil" para pedidos e integración con Shopify ([Shopify Apps](https://apps.shopify.com/zureo-integracion), [ComparaSoftware](https://www.comparasoftware.com/zureo)).
- **StockLink (Bit-A)**: automatización de ventas para distribuidores apoyada en WhatsApp y Excel ([Contra](https://contra.com/p/vWROEeN6-stock-link-landing-page)).
- Juntos+ también llega a Uruguay.

El mercado es chico (~3,5M habitantes) pero tiene factura electrónica madura (CFE) y menos inflación. Sirve como segundo mercado, no como prioridad.

---

## 7. Gaps: de qué se quejan los mayoristas

1. **Pedidos por WhatsApp, Excel y PDF.** El mayorista manda precios por WhatsApp, arma pedidos en Excel y lleva la cuenta corriente en otra planilla. El cliente que compra 180 artículos no puede buscarlos uno por uno ([Open24](https://open24.com.ar/ecommerce-b2b-argentina/), [Commercy](https://commercy.com.ar/blog/plataforma-b2b-mayorista)).
2. **Listas de precios que cambian todo el tiempo.** La inflación (1,9% mensual, con picos) hace que los proveedores manden listas nuevas. Hay casos de mayoristas que reciben listas con +6–8% y "no las validan" ([Cadena 3, CADAM](https://www.cadena3.com/noticia/informados-al-regreso/distribuidores-mayoristas-rechazan-listas-de-precios-con-aumentos-de-6-a-8_415725)). Remarcar a mano genera diferencias ([bcnsoft](https://bcnsoft.com.ar/software-para-distribuidoras/)). Se necesita **actualizar masivamente desde la lista del proveedor y propagar al instante** al catálogo y a los preventistas.
3. **Listas por cliente, escalas y descuentos** que se confirman a mano; y **precios expuestos a la competencia** si el catálogo es público ([Open24](https://open24.com.ar/ecommerce-b2b-argentina/)).
4. **Cuenta corriente y cobranzas.** El mayorista cobra a 30 días, por transferencia o contra factura, y "fía" sin control de vencimientos ni pagos parciales. Las tarjetas y los e-commerce B2C no encajan en ese modelo ([Open24](https://open24.com.ar/ecommerce-b2b-argentina/), [Commercy](https://commercy.com.ar/blog/plataforma-b2b-mayorista)).
5. **Preventistas en papel o con apps sin señal.** Hace falta trabajo offline, impresión de nota de pedido y registro de cobros en ruta (es la propuesta de Cair, CHESS y Líder).
6. **ARCA.** Exige factura A/B con percepciones provinciales y discriminación del IVA (RG 5614/2024). Desde el **1/12/2026 ARCA rechaza comprobantes sin la condición de IVA del receptor**, lo que afecta a los sistemas conectados por web services ([Blog del Contador](https://siap.blogdelcontador.com.ar/?p=90212), [Perfil](https://www.perfil.com/noticias/economia/factura-electronica-arca-que-cambia-cuando-debe-emitirse-y-cuales-son-los-nuevos-requisitos-a40.phtml)). Es un disparador de recambio de software a corto plazo.
7. **Integración con ERPs viejos.** Tango o Bejerman instalados en la PC del contador, sin API, sincronizados por archivos planos ([ecommercemayorista.com](https://ecommercemayorista.com/integraciones/erp-softland-tango-b2b-argentina/)).
8. **Comisiones por venta** de las plataformas (3% de $10M son $300k por año) frente a la preferencia por un **abono fijo** ([Open24](https://open24.com.ar/ecommerce-b2b-argentina/)).
9. **Stock y vencimientos:** faltantes, mermas y capital inmovilizado ([bcnsoft](https://bcnsoft.com.ar/software-para-distribuidoras/)).
10. **Miedo a migrar:** cargar artículos, clientes y listas de precios ([bcnsoft](https://bcnsoft.com.ar/software-para-distribuidoras/)).

---

## 8. Mapa de posicionamiento

Eje X: **amplitud funcional** (solo canal de pedidos → suite que incluye ERP, preventa y B2B).
Eje Y: **segmento** (micro y PyME chica, abono barato → mediana o grande, implementación a medida).

```
                Mediana / grande · a medida · caro
                          ▲
      VentaClick          │          CHESS/Nextbyn · SAP B1 · Dynamics
      Open24/Bitobee      │          Syscom · Tango + módulos · Flexxus
                          │          Líder Gestión (perpetua)
  ────────────────────────┼─────────────────────────────────────►
  Solo canal de pedidos   │                     Suite completa
      VentasxMayor        │          BCNSoft · Commercy · Dux
      Tiendanube mayorista│          Xubio/Colppy/Contabilium (sin preventa/B2B)
      Pedix · WhatsApp    │      Cair (preventa, sin ARCA)
                          │          FactuPyme (retail/gastro)
                          │      ★ HUECO: "Mercos argentino" PyME:
                          │        B2B + preventa offline + cta cte + ARCA,
                          │        USD 80–250/mes, onboarding en 1 día
                PyME chica · SaaS de abono fijo
```

Los marketplaces (ML Negocios, BEES, Juntos+, Centralo, MercadoMayor, Rintin) **quedan fuera del mapa**: le hablan al almacenero, no al mayorista, y le compiten por la relación con el cliente.

---

## 9. Dónde puede ganar un entrante

1. **Segmento:** mayoristas y distribuidoras PyME multirrubro (almacén, limpieza, bebidas, golosinas, ferretería, bazar, textil) con 1 a 30 vendedores o preventistas. Son demasiado grandes para WhatsApp y Pedix y demasiado chicos para CHESS o SAP.
2. **Producto núcleo**, la "cuña" de tres piezas, con salida a ARCA nativa:
   - **Portal B2B privado:** listas por cliente, pedido rápido en tabla, "repetir pedido", mínimos, catálogo PDF y WhatsApp generado automáticamente.
   - **App de preventista offline:** pedido, cobro, no venta, ruta.
   - **Cuenta corriente con cobranzas:** saldo visible para el cliente, recordatorios por WhatsApp, link de pago o transferencia con conciliación.
3. **Diferenciadores para la economía argentina:**
   - Motor de **actualización masiva de precios** desde listas de proveedor (Excel o PDF, con IA para mapear SKUs), con versión y vigencia, y aviso automático a los clientes.
   - Precios en USD o ARS con tipo de cambio configurable.
   - Percepciones IIBB por jurisdicción.
   - Aprovechar la fecha del **1/12/2026 de ARCA** como gancho comercial.
4. **WhatsApp-first, no WhatsApp-against.** El cliente pide por un link o bot que alimenta el sistema; no se le pide que "baje otra app". BEES y Juntos+ ya combinan app y WhatsApp.
5. **Precio:** abono fijo sin comisión, por debajo de BCNSoft ($200k) y de Tango Nube ($731k), y competitivo con VentasxMayor (~$150k) y Cair ($50k por usuario). Ejemplo: base de ~$90–150k más ~$20–30k por preventista.
6. **Integración en lugar de reemplazo:**
   - Conectores con Tango, Bejerman, Dux, Contabilium y **FactuPyme**, para entrar sin exigir migrar el ERP.
   - Que el ERP propio sea un plan superior.
   - La experiencia del equipo usando FactuPyme sirve para conocer el dolor de primera mano y como posible alianza o canal.
7. **Moats posibles:**
   - Datos de pedidos y cobranzas para habilitar **crédito al comprador** con socios (Mercado Pago, fintech o el propio mayorista).
   - Red: los clientes del mayorista piden a varios mayoristas desde una misma interfaz. Hay que hacerlo con cuidado para no convertirse en marketplace y que el mayorista no lo vea como amenaza.
8. **Amenazas a vigilar:**
   - VentasxMayor y Commercy (los competidores directos más maduros).
   - Tiendanube, si profundiza en B2B.
   - Que CHESS/Nextbyn baje al segmento PyME.
   - ML Negocios y BEES desintermediando al mayorista de almacén.
   - Rintin, si entra en Argentina.
