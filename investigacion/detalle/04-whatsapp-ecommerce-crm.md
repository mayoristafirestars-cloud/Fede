# Hallazgos 04: Ventas por WhatsApp (Op. 6), Soporte ecommerce (Op. 5) y CRM vertical (Op. 4) en Argentina/LatAm

Investigación hecha el 29 y 30/10/2026 para profundizar el informe "Negocios digitales con APIs" (que no menciona país).
Convenciones:
- **[V]** = dato verificado en la fuente primaria (página oficial del proveedor o de la cámara), con la fecha de consulta o de publicación.
- **[S]** = dato tomado de una fuente secundaria (prensa, blog o competidor) y no contrastado con la primaria.
- **[E]** = estimación o cálculo propio. No es un dato publicado.
- **[NE]** = no encontrado o no verificable con las herramientas disponibles.

Limitación: el cupo de búsquedas web de esta sesión se agotó a mitad del trabajo. La parte de logística (Correo Argentino, Mercado Envíos) y los CRM verticales de seguros y educación quedaron con menos verificación. Se indica en cada caso.

---

## 1. Resumen ejecutivo

1. **Meta cambió las reglas el 01/10/2026.** Los mensajes de servicio (respuestas libres dentro de la ventana de 24 h) ahora se cobran. Cada número tiene 1.000 gratis por mes; desde el 1.001 se paga. En Argentina cada mensaje de servicio cuesta **USD 0,026**. Lo mismo pasa con las plantillas *utility* enviadas dentro de la ventana [V][1][2]. Esto encarece de forma directa cualquier bot de ventas o soporte "charlatán" en Argentina, donde la tarifa de servicio y utility es la más alta de la región después de Perú.
2. **Las respuestas largas de IA sólo están prohibidas para "AI Providers".** La sección 4.7 de los términos de WhatsApp Business Platform prohíbe a los proveedores de IA usar la plataforma cuando la IA es la oferta principal. También prohíbe usar los datos para entrenar modelos, salvo el *fine-tuning* de uso exclusivo [V][3]. Un asistente sectorial de ventas o soporte para un comercio está permitido, siempre que la IA sea incidental al servicio del negocio [S][4].
3. **Meta compite directamente.** La categoría "Meta Business Agent" cobra USD 2 por millón de tokens, unos USD 0,04 a 0,05 por mensaje según Meta [V][1]. Tiendanube ya vende ventas automatizadas por WhatsApp con Chat Nube, desde ARS 190 hasta ARS 400 por conversación [V][7][8]. Un "bot de ventas genérico para tiendas" no tiene espacio.
4. **El mercado existe.** El ecommerce argentino facturó ARS 34,03 billones en 2025 (+55 % nominal), según la CACE [V][9]. En el primer semestre de 2026 facturó ARS 19,53 billones (+28 % nominal), lo que implica un crecimiento real cercano a cero o negativo [S][10][11]. Según Tiendanube, el 71,5 % de los emprendedores y el 60,3 % de las grandes marcas de su plataforma venden por WhatsApp [S][12].
5. **Las cuñas con más defensa** combinan WhatsApp con un sistema concreto que el generalista no integra bien:
   - "dónde está mi pedido" (WISMO) integrado con transportistas argentinos (Andreani y OCA tienen API de trazas [V][19][20]);
   - presupuestación sectorial con aprobación humana;
   - CRM vertical sobre nichos con software débil.

---

## 2. Oportunidad 6: Ventas por WhatsApp

### 2.1 Modelo de precios de WhatsApp Business Platform (vigente desde el 01/10/2026)

Fuente primaria: Meta Developers, "Pricing on the WhatsApp Business Platform", página actualizada el 30/09/2026, y las tarifas oficiales en USD "effective October 1, 2026" (XLSX descargado el 29/10/2026) [V][1][2].

**Reglas clave [V][1]:**
- **Cobro por mensaje entregado**, vigente desde el 01/07/2025. Los mensajes del usuario a la empresa son gratis.
- **Cinco categorías:**
  - plantillas *marketing*, *utility* y *authentication*, que pueden enviarse en cualquier momento;
  - mensajes no-plantilla *service*, sólo dentro de la ventana de 24 h, que se abre o renueva con cada mensaje del usuario;
  - mensajes no-plantilla *Meta Business Agent*, cuando los genera el agente de IA propio de Meta.
- **Cambio del 01/10/2026:** se vuelven a cobrar los mensajes de servicio y las plantillas *utility* enviadas dentro de la ventana, que eran gratis desde julio de 2025. Hay un **tramo gratis de 1.000 mensajes de servicio por mes y por número**, que no se acumula. Si la cuenta no tiene medio de pago, Meta deja de entregar mensajes de servicio una vez agotado el tramo gratis.
- **Ventana de punto de entrada gratuito (FEP):** cuando el usuario llega desde un anuncio *Click to WhatsApp* y la empresa responde dentro de la ventana, se abre una ventana "de hasta 7 días" en la que marketing, utility, authentication y service son gratis. Los mensajes de Meta Business Agent se siguen cobrando. *Nota:* respond.io habla de 72 h [S][4b]. Prevalece el texto oficial.
- **Descuentos por volumen** sólo para utility y authentication. En Argentina: tarifa de lista hasta 100.000 utility por mes, −5 % entre 100.001 y 1.000.000, y −10 % entre 1.000.001 y 4.500.000 [V][2].
- **Meta Business Agent:** USD 2,00 por millón de tokens. Según Meta, "un mensaje consume típicamente 20.000–25.000 tokens ≈ 4–5 centavos USD". No tiene tramos ni gratuidad [V][1].
- **Moneda local:** se puede facturar en ARS desde el 01/04/2026 [V][1].

**Tarifas por mensaje en USD, vigentes desde el 01/10/2026 [V][2]**

| Mercado | Marketing | Utility | Authentication | Service (desde el mensaje 1.001 del mes) |
|---|---|---|---|---|
| **Argentina** | **0,0618** | **0,0260** | **0,0260** | **0,0260** |
| Brasil | 0,0625 | 0,0068 | 0,0068 | 0,0068 |
| Chile | 0,0889 | 0,0200 | 0,0200 | 0,0200 |
| Colombia | 0,0125 | 0,0008 | 0,0008 | 0,0008 |
| México | 0,0397 | 0,0085 | 0,0085 | 0,0085 |
| Perú | 0,0703 | 0,0300 | 0,0300 | 0,0300 |
| Resto de Latinoamérica | 0,0740 | 0,0113 | 0,0113 | 0,0113 |

En ARS, Argentina paga 89,56 por marketing y 37,68 por utility, authentication o service [V][2]. El tipo de cambio implícito en la tarifa es de unos 1.449 ARS/USD [E].

**Cambios recientes:** el 01/10/2025 Meta bajó utility y authentication en Argentina. El 01/10/2026 subió marketing en México y utility y authentication en Perú [V][1].

**Ejemplo de costo para una pyme argentina [E]** (supuestos propios, no son datos):
- 1.500 conversaciones por mes iniciadas por el cliente;
- 6 respuestas de la empresa por conversación, o sea 9.000 mensajes de servicio;
- 1.500 confirmaciones de pedido (utility);
- 1 campaña de 5.000 marketing.

| Concepto | Cálculo | USD/mes |
|---|---|---|
| Service | (9.000 − 1.000) × 0,026 | 208 |
| Utility | 1.500 × 0,026 | 39 |
| Marketing | 5.000 × 0,0618 | 309 |
| **Total Meta, sin BSP ni IA** | | **≈ 556** |
| Alternativa: los 9.000 mensajes con Meta Business Agent | 9.000 × 0,04 a 0,05 | 360–450 |

Implicancias de diseño [E]:
- Conviene agrupar respuestas: menos mensajes por conversación implica menos costo.
- Conviene empujar el tráfico vía anuncios *Click to WhatsApp* para entrar en la ventana FEP.
- Hay que medir el costo por conversación cerrada.
- El informe original ya advertía no vender consumo ilimitado. Ahora el riesgo es mayor, porque el servicio dejó de ser gratis.

### 2.2 Alta de terceros: Tech Provider, Solution Partner y Embedded Signup

- **Tech Provider [V][5]** (Meta Developers, consultado el 29/10/2026). Pasos:
  - verificar la empresa ante Meta;
  - pasar *App Review* con video del envío de un mensaje y de la creación de una plantilla, para obtener acceso avanzado a `whatsapp_business_messaging` y `whatsapp_business_management`.

  Los clientes incorporados **deben cargar su propia tarjeta** en su cuenta. La página no menciona límites de cantidad de clientes ni niveles del programa [NE].
- **Solution Partner (BSP) [V][6]:** necesita una línea de crédito con Meta y compartirla con los clientes durante el alta. El BSP factura el consumo y por eso puede revenderlo con margen. Ejemplo: Botmaker declara "costo WhatsApp + 20 %" en las notificaciones [V][14].
- **Embedded Signup [V][6]:**
  - Es el flujo de alta integrada con Facebook Login for Business y devuelve `waba_id`, `phone_number_id` y un token.
  - **Las versiones v2 y v3 se dejaron de admitir el 15/10/2026.** Hay que integrar la v4.
  - Admite **"coexistence"**: incorporar un número que ya usa la app WhatsApp Business sin migrarlo. Es clave para pymes argentinas que ya venden desde la app.
- **Ruta práctica para Federico [E]:**
  1. Arrancar como Tech Provider, o sobre un BSP con una cuenta propiedad del cliente.
  2. Cobrar sólo su software y servicio, y que el cliente pague a Meta con su tarjeta.

  Así no financia consumo variable ni asume el riesgo cambiario.

### 2.3 Política de IA (sección 4.7 de los términos de WhatsApp Business Platform)

- Texto vigente: "Last Modified: September 23, 2026" [V][3]. Los "AI Providers" (proveedores de IA o ML, según los define Meta) "are strictly prohibited from accessing or using the WhatsApp Business Platform, whether directly or indirectly" cuando esas tecnologías son la oferta principal y no algo incidental.
- **Entrenamiento:** está prohibido usar los datos de la plataforma "to create, develop, train, or improve any machine learning or artificial intelligence systems", incluso agregados o anonimizados. Excepción: se permite el *fine-tuning* de un modelo **de uso exclusivo** del negocio [V][3].
- **Cronología [S][4]:** rige para cuentas nuevas desde el 15/10/2025 y para existentes desde el 15/01/2026. Afectó a ChatGPT, Perplexity, Luzia y Copilot. Meta dijo a TechCrunch que no apunta a empresas que usan IA para atención al cliente [S][4c]. Hubo investigaciones antimonopolio en la UE, Italia y Brasil [S][4c].
- **Qué implica para un asistente sectorial [E]:**
  - Debe presentarse y operar como el canal del comercio (catálogo, stock, presupuesto, estado de pedido), nunca como "un ChatGPT por WhatsApp".
  - No puede reutilizar las conversaciones de un cliente para mejorar un modelo compartido entre clientes. Esto limita el *moat* basado en datos agregados de conversaciones.
  - La aprobación no es automática: Meta decide qué es "incidental".

### 2.4 Competencia: plataformas y BSP en LatAm con precios

| Proveedor (origen) | Precio publicado | Modelo y observaciones | Fuente |
|---|---|---|---|
| **Chat Nube, Tiendanube (AR/BR)** | Por conversación de IA (24 h), según plan: Inicial ARS 400, Esencial 320, Impulso 260, Escala 210, Evolución 190. Sin abono fijo. Prueba de 15 días | Arma el carrito, envía el link de pago (Pago Nube) y deriva a un humano. WhatsApp e Instagram. **La página no menciona estado de pedido ni seguimiento.** No aclara si incluye los cargos de Meta. Equivale a ~USD 0,13–0,28 por conversación [E] | [V][8] (act. 17/07/2026); [V][7] |
| **Botmaker (AR)** | USD 149/mes (3.000 conversaciones), 249 (5.000), 499 (10.000); excedente USD 0,05–0,07. Alta WhatsApp USD 99 | Notificaciones a "costo WhatsApp + 20 %". **Su página todavía dice que las respuestas dentro de las 24 h son gratis, algo desactualizado desde el 01/10/2026** | [V][14] (29/10/2026) |
| **Cliengo (AR)** | Premium USD 119/mes; Business USD 259; Starter y Corporate sin precio publicado | Conversación = sesión de 24 h. Cargos de Meta aparte. WhatsApp API "con costo adicional" en Premium | [V][15] (29/10/2026) |
| **Kommo (ex amoCRM)** | USD 25 / 35 / 45 por usuario/mes, mínimo 6 meses, sin pago mensual | CRM con WhatsApp y créditos de IA por usuario. Cargos de Meta aparte, aparentemente [S] | [V][16] |
| **respond.io (MY)** | USD 79 / 159 / 279 por mes con pago anual (99 / 199 / 349 con pago mensual) | Cargos de WhatsApp no incluidos, se recargan en la plataforma | [V][17] |
| **Wati (IN)** | USD 59 / 119 / 279 por mes con pago anual | IA "Astra" como complemento aparte; número extra USD 29 | [V][18] |
| **Leadsales (MX)** | USD 97 / 133 / 247 por mes (−20 % anual) | "Lead Agent" de IA entre USD 87 y 793 por mes, además del plan | [V][21] |
| **Zenvia (BR)** | Specialist USD 130 (104 con promoción), Expert 390, Professional 845 | Alta de WhatsApp USD 137 en Starter; paquetes de saldo desde USD 20. Ya informa los 1.000 mensajes de servicio gratis | [V][22] |
| **Jelou (EC)** | Free, Builder USD 25, Growth USD 299 | USD 0,009 por ejecución; mensajes de Meta "billed separately" (cambio de jul–oct 2026) | [S][23] |
| **Treble (CO)** | No publica precios; plan gratis de 5 conversaciones | Estimación de terceros: USD 200–500/mes [S, no verificado] | [S][24] |
| **Darwin AI (AR/BR/MX)** | No publica precios; cobra *setup* más un cargo por conversación | Venta asistida | [S][25] |
| **Gupshup, Blip, Yalo** | No se encontraron precios públicos | Orientados a enterprise | [NE] |

**Lectura [E]:** el piso de precio de una plataforma horizontal es USD 60–150/mes más los cargos de Meta. Una cuña nueva no puede competir en "inbox + bot". Tiene que cobrar por un resultado: borrador de venta válido, presupuesto aprobado o reclamo resuelto.

### 2.5 Uso de WhatsApp para vender en Argentina

- **Tiendanube, NubeCommerce:** el 71,5 % de los emprendedores y el 60,3 % de las grandes marcas venden por WhatsApp, además de su tienda. Instagram queda primero, con 82,6 % y 68,2 % [S][12]. La tabla se cita en Noujau (05/10/2026) y no se pudo ubicar en la página oficial del informe. Mide el **porcentaje de comercios**, no de facturación. En el mismo informe, Colombia tiene 84,1 % de uso de WhatsApp [V][13].
- **Atención con IA:** en Argentina, el 60,8 % de las consultas de tiendas Tiendanube se resolvieron con IA sin intervención humana [V][13] (informe del 03/08/2026). Chat Nube declaraba 7 de cada 10 consultas automatizadas en diciembre de 2025 [V][7].
- **Tamaño de Tiendanube AR:** más de 65.000 marcas facturaron cerca de ARS 2 billones en 2025 (+73 %), con unos 22 millones de órdenes y un ticket de ARS 90.396 [S][26] (Mercado, 12/06/2026).
- **CACE, estudio anual 2025** (publicado el 19/03/2026, Kantar) [V][9]:
  - Facturación de ARS 34.033.238 millones (+55 %), 253 millones de órdenes (+3 %), 645 millones de unidades (+28 %) y un ticket de ARS 134.519.
  - 25,1 millones de compradores. El 37 % de las entregas llegó en menos de 24 h.
  - El 62 % de las empresas ya usa IA.
  - El artículo no trae datos de WhatsApp [NE].
- **CACE, Mid Term del primer semestre de 2026** (agosto de 2026) [S][10][11]:
  - ARS 19.533.815 millones (+28 % nominal), 181,5 millones de órdenes (+21 %) y un ticket de ARS 107.597.
  - Con una inflación de alrededor de 32–33 %, el crecimiento real queda cerca de cero o es levemente negativo [S][11].
  - Según Noujau, las entregas de 2025 fueron 58 % a domicilio y 29 % con retiro en el local [S][12].
- **Meta:** no se encontró un dato oficial de Meta sobre uso de WhatsApp para comprar en Argentina [NE].

### 2.6 Cuña vertical posible para Argentina (Op. 6)

**"Presupuestador por WhatsApp para corralones y ferreterías / materiales de construcción" [E]**

*Hipótesis a validar.* Herramientas y construcción figura entre los rubros que más facturaron en el Mid Term 2026 [S][10].

Por qué funciona como cuña:
- El pedido típico es una lista de materiales (texto, foto o audio) que hay que convertir en un presupuesto con stock, precio vigente (lista con alta rotación por inflación), flete por zona y forma de pago.
- Chat Nube y los bots horizontales resuelven catálogos de tienda online, no listas de obra con equivalencias de producto ni cálculo de cantidades.
- El entregable cobrable es un **borrador de presupuesto válido** que el vendedor aprueba y envía, y que se registra en el sistema de gestión o en una planilla.

Alternativas del mismo patrón: repuestos de autos y motos (por modelo y año), distribuidoras mayoristas con listas de precios, ópticas.

---

## 3. Oportunidad 5: Soporte ecommerce

### 3.1 Herramientas globales (precios publicados, consultados el 29/10/2026)

| Herramienta | Precio | IA | WhatsApp | Fuente |
|---|---|---|---|---|
| **Gorgias** | Starter USD 10 (50 tickets), Basic 60 (300), Pro 360 (2.000), Advanced 900 (5.000) con pago mensual; excedente USD 0,36–0,40 por ticket | AI Agent USD 0,90–1,00 por interacción automatizada (1,50 fuera del plan) | La página no lo lista entre los canales | [V][27] (la página tiene un segundo bloque de precios distinto, así que hay que confirmar) |
| **Zendesk Suite** | Team USD 55 y Professional USD 115 por agente/mes con pago anual (69 y 149 con pago mensual) | Resolución automatizada USD 1,50 comprometida o 2,00 a demanda; incluye 5 o 10 por agente | Incluido en Suite, "additional fees apply" | [V][28] |
| **Freshdesk** | Growth USD 19, Pro 55, Enterprise 89 por agente/mes con pago anual | Freddy AI Agent: 500 sesiones gratis una sola vez y luego USD 49 cada 100 sesiones | La página no lo menciona | [V][29] |

**Lectura [E]:**
- Estas herramientas cobran entre USD 0,49 y 2,00 por resolución de IA. Es una referencia de disposición a pagar por resolución en el segmento que ya las usa.
- Ninguna trae integración nativa con transportistas argentinos, ni con WhatsApp como canal principal a precio pyme. Ahí está el hueco.
- Localmente, Chat Nube cubre la preventa en tiendas Tiendanube, pero su página de ayuda no menciona estado de pedido ni seguimiento [V][8].

### 3.2 Logística local: APIs útiles para "¿dónde está mi pedido?"

| Operador | API de seguimiento | Acceso | Fuente |
|---|---|---|---|
| **Andreani** | Sí: "API trazas" para obtener los estados del envío, además de APIs de pedidos, recepción, stock y localidades. Módulos para VTEX, Tiendanube y Magento | **Hay que ser cliente.** Las credenciales de QA y producción se gestionan con el ejecutivo comercial | [V][19] (developers.andreani.com, 29/10/2026) |
| **OCA (ePak)** | Sí: web service SOAP público con `Tracking_Pieza`, `Tracking_PiezaExtendido`, `Tracking_PiezaNumeroEnvio`, `GetEnvioEstadoActual`, más etiquetas y sucursales. Portal developers.oca.com.ar con "notificaciones y comunicaciones" | Algunas operaciones requieren cuenta y credenciales de cliente [E] | [V][20] |
| **Correo Argentino** | Existe "MiCorreo" para pymes y seguimiento web. **No se pudo verificar una API pública documentada de seguimiento** | — | [NE][30] |
| **Mercado Envíos** | La API de Mercado Libre expone envíos (shipments) para ventas en Mercado Libre. La documentación devolvió 403 desde aquí | Sólo para órdenes de Mercado Libre y con OAuth del vendedor [E, no verificado] | [NE] |
| **Envíopack** | Fulfillment, última milla en AMBA y "API DOC" para desarrolladores. Integraciones (por logos) con Tiendanube, Shopify, WooCommerce, VTEX y Mercado Libre | Precio a consultar | [V][31] |
| **Zipnova (ex Zippin)** | Agregador de más de 100 transportes, con API, seguimiento en tiempo real e integraciones con Mercado Libre, Tiendanube, VTEX, WooCommerce y Shopify | Registro gratis; precios no publicados | [V][32] (zippin.com.ar redirige a zipnova.com/ar) |
| **Tiendanube (plataforma)** | La API de órdenes expone `shipping_status` (unpacked, shipped, delivered, etc.) y *fulfillment orders* con `tracking_info{url, code}` | OAuth y app revisada para distribución pública (ver el informe original) | [V][33] |

**Lectura [E]:**
- Resolver WISMO por WhatsApp es técnicamente viable:
  1. leer la orden desde Tiendanube o Shopify;
  2. tomar el código de seguimiento;
  3. consultar Andreani, OCA o un agregador (Zipnova, Envíopack);
  4. responder con una plantilla *utility* o dentro de la ventana de servicio.
- La fricción está en el acceso: Andreani exige ser cliente y pasar por su ejecutivo, y cada transportista tiene su propio formato de estados.
- Usar un agregador reduce las integraciones, pero agrega dependencia.
- Las acciones sobre pedidos (reembolsos, cambios) siguen siendo el riesgo que señalaba el informe. Conviene empezar en sólo lectura con traspaso a un humano.

### 3.3 Cuña vertical posible para Argentina (Op. 5)

**"WISMO + cambios para tiendas de indumentaria y calzado en Tiendanube que envían por Andreani u OCA" [E]**

- Indumentaria tiene alta tasa de consultas por talle y cambio (hipótesis a validar con tiendas reales).
- El producto contesta por WhatsApp "dónde está mi pedido" con el estado normalizado del transportista.
- Avisa en forma proactiva los envíos demorados con una plantilla utility de USD 0,026.
- Gestiona la solicitud de cambio (talle o color) hasta generar el borrador de logística inversa, que un humano aprueba.
- Se cobra por pedido resuelto, como referencia frente a los USD 0,90–2,00 por resolución de Gorgias o Zendesk, y siempre por encima del costo de Meta.

---

## 4. Oportunidad 4: CRM vertical

### 4.1 CRM horizontales (precios consultados el 29/10/2026)

| CRM | Precio publicado | WhatsApp | Fuente |
|---|---|---|---|
| **HubSpot Sales Hub** | Free (2 usuarios); Starter USD 20 por puesto/mes (7 con pago anual, según la interpretación de la página); Professional USD 100 (90 anual) más USD 1.500 de alta; Enterprise USD 150 más USD 3.500 | No mencionado en la página de precios | [V][34] |
| **Pipedrive** | Lite USD 14, Growth 39, Premium 59, Ultimate 79 por puesto/mes con pago anual, sin IVA | No mencionado (marketplace de más de 500 apps) | [V][35] |
| **Kommo** | USD 25–45 por usuario/mes, mínimo 6 meses | Nativo, es su diferencial en LatAm | [V][16] |
| **Clientify (ES)** | 39 €/USD por mes con pago anual o 65 con pago mensual; usuarios y contactos "ilimitados" | Bandeja de WhatsApp multiusuario incluida | [V][36] |
| **Zoho CRM** | Free hasta 3 usuarios; CRM Plus desde USD 20 por usuario/mes; el resto de los precios no se pudo leer | No mencionado | [V][37] |

### 4.2 CRM de nicho en Argentina

| Nicho | Jugador | Qué se verificó | Fuente |
|---|---|---|---|
| **Inmobiliarias** | **Tokko Broker** | Planes Personal (1 usuario, 15 propiedades), Inicial (2/40), Equipo (4/90), Profesional (10/200, API incluida) y Corporativo (15/300). Difusión a Zonaprop, Mercado Libre y Argenprop (los portales se pagan aparte). WhatsApp "¡Nuevo!" con precio a consultar. **Los montos no se leen en la página** | [V][38] |
| Inmobiliarias | **KiteProp** | Se presenta como "CRM inmobiliario líder" en Argentina | [V][39] (sólo el título del sitio) |
| **Concesionarias** | **Tecnom** | "CRM automotriz con IA que usan más de 400 concesionarios en LATAM" (autodeclarado) | [V][40] (sólo el título del sitio) |
| Seguros (productores asesores) | — | No se pudo investigar por falta de cupo de búsqueda | [NE] |
| Educación (institutos o academias) | — | No se pudo investigar | [NE] |

**Lectura [E]:**
- En inmobiliarias y concesionarias ya hay CRM verticales con integraciones a portales. Competir como "otro CRM" es inviable, tal como advierte el informe.
- La oportunidad está en un **módulo de flujo** sobre el CRM existente (Tokko tiene API en los planes Profesional y Corporativo) o sobre Kommo o HubSpot, que resuelva una tarea que el CRM no automatiza:
  - calificar consultas de portales que llegan por WhatsApp;
  - coordinar visitas;
  - seguimientos aprobados;
  - en seguros, renovaciones y cotizaciones multiaseguradora.

### 4.3 Cuña vertical posible para Argentina (Op. 4)

**"Seguimiento y renovaciones para productores asesores de seguros (PAS) por WhatsApp" [E, hipótesis]**

Supuestos:
- La cartera de pólizas tiene vencimientos conocidos.
- Cada renovación necesita una cotización, la aprobación del productor y el envío al cliente.

Propuesta:
- Plantilla utility de recordatorio (USD 0,026).
- Recolección de datos (vehículo, cambios) dentro de la ventana de servicio.
- Borrador de renovación que el PAS aprueba.
- Registro en su CRM o planilla.

Barreras:
- El acceso a los cotizadores de aseguradoras, que puede no tener API.
- Los datos personales sensibles.

**No se verificó** la competencia local (software de gestión para PAS) ni el tamaño del nicho. Es lo primero que hay que investigar.

Alternativa más verificada: **inmobiliarias con Tokko**.
- Un asistente que toma la consulta del portal o de WhatsApp, la cruza con la ficha vía la API de Tokko, propone horarios de visita y deja la oportunidad cargada.
- Requiere confirmar los términos de uso de la API de Tokko para terceros. No verificado [NE].

---

## 5. Comparación de las tres oportunidades para Argentina

| | Op. 6 Ventas WhatsApp | Op. 5 Soporte ecommerce | Op. 4 CRM vertical |
|---|---|---|---|
| Competencia directa | Muy alta: Tiendanube Chat Nube, Meta Business Agent, más de 10 BSP | Media: Gorgias, Zendesk y Freshdesk son caros o poco locales; Chat Nube cubre la preventa | Alta en inmobiliarias (Tokko, KiteProp) y autos (Tecnom); desconocida en seguros |
| Precio de referencia | USD 60–500/mes más Meta; Chat Nube ARS 190–400 por conversación | USD 0,49–2,00 por resolución de IA (globales) | USD 14–45 por usuario/mes (horizontales) |
| Costo variable clave | Meta: service y utility a USD 0,026 en Argentina desde el mensaje 1.001 | Meta (avisos utility) más APIs de transportistas | Meta (recordatorios) |
| Barrera técnica o regulatoria | Alta de Tech Provider, App Review, Embedded Signup v4, sección 4.7 de IA | Credenciales de cada transportista (Andreani exige ser cliente) y OAuth de Tiendanube | API del CRM de nicho y permisos para terceros |
| Defensa posible | Catálogo y reglas sectoriales (presupuesto) | Integración logística local y flujo de cambios | Flujo específico encima del CRM existente |

---

## 6. Implicancias y recomendación para Federico

1. **Recalcular todo presupuesto de WhatsApp con las tarifas del 01/10/2026.**
   - En Argentina cada respuesta del bot cuesta USD 0,026 a partir del mensaje 1.001 del mes.
   - No hay que vender conversaciones ilimitadas. Conviene que el cliente pague a Meta con su propia tarjeta (modelo Tech Provider) y cobrarle sólo el software o el resultado.
   - El informe original decía "confirmar la tarifa vigente". Ya está confirmada [1][2].
2. **No construir un "bot de ventas para tiendas".** Tiendanube (Chat Nube, con alianza oficial con Meta) y Meta (Business Agent) ya ocupan ese espacio, a precios por conversación que una pyme puede comparar fácil.
3. **La cuña más prometedora y verificable es la Op. 5: WISMO + cambios para tiendas Tiendanube con Andreani u OCA.** Motivos:
   - Hay APIs de trazas reales y verificadas.
   - Hay un hueco: Chat Nube no menciona seguimiento, y las herramientas globales no integran transportistas argentinos.
   - El valor es medible en tickets evitados.
   - Se puede arrancar en sólo lectura, lo que reduce el riesgo de "acciones sobre pedidos".

   Primer paso: conseguir 3 a 5 tiendas de indumentaria y medir qué parte de sus mensajes son "¿dónde está mi pedido?" y cambios.
4. **La Op. 6 conviene sólo en forma vertical, como presupuestador:** corralones, repuestos o mayoristas con listas de precios. Lo cobrable es el "borrador de presupuesto válido". Hay que diseñar el asistente para cumplir la sección 4.7: la IA como función incidental del comercio y sin entrenar modelos compartidos con datos de WhatsApp.
5. **La Op. 4 conviene como módulo, no como CRM.** Antes de invertir:
   - validar si Tokko permite integraciones de terceros por API (inmobiliarias);
   - investigar el software existente para productores de seguros, que es el nicho con menos información en esta investigación.
6. **Pendientes de verificación**, por el agotamiento del cupo de búsquedas:
   - API de seguimiento de Correo Argentino;
   - alcance de la API de envíos de Mercado Libre para tiendas propias;
   - precios de Tokko, Treble, Darwin AI, Blip, Yalo y Gupshup;
   - competencia en software para productores de seguros y para educación;
   - fuente primaria del 71,5 % de Tiendanube.

---

## 7. Fuentes

| # | Fuente | URL | Fecha |
|---|---|---|---|
| 1 | Meta Developers, "Pricing on the WhatsApp Business Platform" | https://developers.facebook.com/docs/whatsapp/pricing | Actualizada el 30/09/2026; consultada el 29/10/2026 |
| 2 | Meta, tarifas en USD y ARS y tramos por volumen, "effective October 1, 2026" (XLSX enlazado desde [1]) | Enlaces CSV en https://developers.facebook.com/docs/whatsapp/pricing#rate-cards | Descargado el 29/10/2026 |
| 3 | Meta, "Meta Terms for WhatsApp Business Platform", sección 4.7 | https://www.facebook.com/legal/Meta-Terms-for-WhatsApp-Business-Platform | Last Modified 23/09/2026; consultada el 29/10/2026 |
| 4 | respond.io, "WhatsApp general purpose chatbots ban" | https://respond.io/blog/whatsapp-general-purpose-chatbots-ban | 27/10/2025 |
| 4b | respond.io, "WhatsApp pricing change 2026" | https://respond.io/blog/whatsapp-pricing-change-2026 | 03/09/2026 (modificada el 06/10/2026) |
| 4c | TechCrunch, "WhatsApp changes its terms to bar general-purpose chatbots" | https://techcrunch.com/2025/10/18/whatssapp-changes-its-terms-to-bar-general-purpose-chatbots-from-its-platform | 18/10/2025 |
| 5 | Meta Developers, "Become a Tech Provider" | https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/get-started-for-tech-providers | Consultada el 29/10/2026 |
| 6 | Meta Developers, "Embedded Signup overview" | https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/overview/ | Consultada el 30/10/2026 |
| 7 | Revista Mercado, "Tiendanube y Meta habilitan ventas automatizadas por WhatsApp en Argentina" | https://mercado.com.ar/innovacion/tiendanube-y-meta-habilitan-ventas-automatizadas-por-whatsapp-en-argentina-por-primera-vez | 08/12/2025 |
| 8 | Tiendanube, ayuda, "Preguntas frecuentes sobre Chat Nube" | https://ayuda.tiendanube.com/es_AR/activar-chat-nube/preguntas-frecuentes-sobre-chat-nube | Actualizada el 17/07/2026 |
| 9 | Revista Mercado, "Comercio electrónico: el estudio anual de CACE midió $34.033.238 millones en 2025" | https://mercado.com.ar/tendencias/comercio-electronico-el-estudio-anual-de-cace-midio-34-033-238-millones-en-2025 | 19/03/2026 |
| 10 | Revista Mercado, "CACE: el comercio electrónico facturó $19.533.815 millones en el primer semestre" | https://mercado.com.ar/tendencias/cace-el-comercio-electronico-facturo-19-533-815-millones-en-el-primer-semestre | Agosto de 2026 (según el buscador) |
| 11 | El Economista, "Ecommerce Argentina crece 28%, pero..." | https://eleconomista.com.ar/economia/ecommerce-argentina-crece-28-pero-siempre-significa-ganar-mas-n98420 | Agosto de 2026 (según el buscador) |
| 12 | Noujau, "Comercio electrónico en Argentina: qué dicen las cifras de 2025 y 2026" (tabla atribuida a Tiendanube) | https://noujau.com.ar/blog/comercio-electronico-en-argentina-cifras | 05/10/2026 (act. 12/10/2026) |
| 13 | Tiendanube, "NubeCommerce 2026: el mapa estratégico para escalar tu marca" | https://www.tiendanube.com/blog/ecommerce-informe/ | 03/08/2026 |
| 14 | Botmaker, precios | https://www.botmaker.com/es/precios | Consultada el 29/10/2026 |
| 15 | Cliengo, precios | https://www.cliengo.com/pricing | Consultada el 29/10/2026 |
| 16 | Kommo, precios | https://www.kommo.com/pricing/ | Consultada el 29/10/2026 |
| 17 | respond.io, precios | https://respond.io/pricing | Consultada el 29/10/2026 |
| 18 | Wati, precios | https://www.wati.io/pricing/ | Consultada el 29/10/2026 |
| 19 | Andreani Developers | https://developers.andreani.com/ | Consultada el 30/10/2026 |
| 20 | OCA Developers y web service ePak Tracking | https://developers.oca.com.ar/ ; https://webservice.oca.com.ar/ePak_tracking/Oep_TrackEPak.asmx | Consultadas el 30/10/2026 |
| 21 | Leadsales, precios | https://www.leadsales.io/precios | Consultada el 29/10/2026 |
| 22 | Zenvia, precios | https://www.zenvia.com/es/precios/ | Consultada el 29/10/2026 (promoción hasta el 31/10/2026) |
| 23 | PricingSaaS, cambios de precios de Jelou | https://pricingsaas.com/companies/jelou/diffs/2026W30 | Julio a octubre de 2026 |
| 24 | Hackceleration y Dupple, precios de Treble | https://www.hackceleration.com/labs/treble-pricing ; https://dupple.com/tools/trebleai | Junio a agosto de 2026 |
| 25 | Aurora Inbox (competidor), "Aurora vs Darwin AI"; Spotsaas | https://www.aurorainbox.com/aurora-vs-darwin-ai/ ; https://www.spotsaas.com/product/darwinai/pricing | 2026 |
| 26 | Revista Mercado, "Tiendanube, protagonista de 2025" | https://mercado.com.ar/protagonistas/tiendanube-protagonista-de-2025-sus-tiendas-facturaron-casi-2-billones | 12/06/2026 |
| 27 | Gorgias, precios | https://www.gorgias.com/pricing | Consultada el 29/10/2026 |
| 28 | Zendesk, precios | https://www.zendesk.com/pricing/ | Modificada el 09/10/2026 |
| 29 | Freshdesk, precios | https://www.freshworks.com/freshdesk/pricing/ | Consultada el 29/10/2026 |
| 30 | Correo Argentino, MiCorreo | https://www.correoargentino.com.ar/MiCorreo/public/ | Consultada el 30/10/2026 (sin documentación de API visible) |
| 31 | Envíopack Argentina | https://www.enviopack.com.ar/ | Consultada el 30/10/2026 |
| 32 | Zipnova (ex Zippin) | https://zipnova.com/ar/ | Consultada el 30/10/2026 |
| 33 | Tiendanube API, recurso Order | https://tiendanube.github.io/api-documentation/resources/order | Consultada el 30/10/2026 |
| 34 | HubSpot, precios de Sales Hub | https://www.hubspot.com/pricing/sales | Consultada el 30/10/2026 |
| 35 | Pipedrive, precios (ES) | https://www.pipedrive.com/es/pricing | Consultada el 30/10/2026 |
| 36 | Clientify, precios | https://clientify.com/precios | Consultada el 30/10/2026 |
| 37 | Zoho CRM, precios | https://www.zoho.com/crm/zohocrm-pricing.html | Consultada el 30/10/2026 |
| 38 | Tokko Broker, planes Argentina | https://www.tokkobroker.com/es-ar/planes | Consultada el 30/10/2026 |
| 39 | KiteProp | https://www.kiteprop.com/ar | Consultada el 30/10/2026 (sólo título y descripción) |
| 40 | Tecnom | https://tecnom.ai/ | Consultada el 30/10/2026 (sólo título y descripción) |
