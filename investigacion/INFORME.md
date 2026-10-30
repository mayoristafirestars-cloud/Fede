# Negocios digitales con APIs en Argentina: investigación completa

Informe consolidado, 30/10/2026. Parte del PDF *Negocios digitales con APIs: oportunidades y validación* (29/10/2026) y lo profundiza para Argentina y LatAm. Seis agentes de investigación trabajaron en paralelo sobre fuentes públicas consultadas el 29 y 30/10/2026. Cada informe de detalle (carpeta `detalle/`) tiene fuentes numeradas con URL y marca cada dato como verificado, secundario, estimación o no encontrado.

> No es asesoramiento legal, contable ni de inversión. Los precios y las normas cambian. Las cifras económicas son supuestos para ordenar decisiones, no pronósticos.

---

## 1. Conclusión en una página

**El PDF está bien hecho, pero su orden de prioridades no se traslada tal cual a Argentina.**

- Los datos del PDF se verificaron y casi todos son correctos (precios, cambios de Google Ads, dato de Tiendanube). Las cuentas del modelo económico no tienen errores aritméticos.
- Lo que falla son los **supuestos para Argentina**. Con abonos que paguen pymes argentinas (USD 150 a 250), CAC de USD 500 y baja mensual del 6%, el escenario "documentos" del PDF da contribución **negativa**. Solo cierra si la revisión humana baja a 3 h por cliente o menos, si se cobra por transferencia y si el volumen incluido es acotado.
- **El hallazgo que cambia la decisión:** en Argentina las facturas electrónicas recibidas ya están estructuradas en ARCA ("Mis Comprobantes", y desde 11/2025 la precarga de compras en IVA Simple). Tango, Xubio, Colppy y otros ya las importan, y varios ya leen PDF con IA. Leer facturas fiscales con OCR, la primera apuesta del PDF, vale poco acá.
- **El costo de la IA no es la variable.** Un LLM barato cuesta unos USD 2 por 10 M de tokens de entrada (OpenAI, Anthropic o Google por igual). Lo que define el margen son las horas humanas, el canal de venta y el precio que acepta la pyme.
- **La defensa posible** es la integración local (ARCA, Mercado Libre, Mercado Pago, Tango, Tiendanube, Andreani/OCA), la operación de las excepciones y un canal de confianza (contadores, agencias, despachantes).

### Ranking revisado para Argentina

| # | Oportunidad (cuña concreta) | Por qué | Riesgo principal |
|---|---|---|---|
| **1** | **Rentabilidad real y conciliación para vendedores de Mercado Libre / Mercado Pago** (une las oportunidades 3 y 7 del PDF) | Hueco claro: los conectores globales no cubren Mercado Libre y no se encontró un producto pyme que cruce ML + MP + ARCA + banco. Las APIs (facturación por orden de ML, Product Ads, reportes de liberaciones de MP) alcanzan y son de solo lectura | Competencia barata para el vendedor suelto (Jaguar Sheet, ARS 25–30 mil/mes). Vender a agencias y consultoras de ML y a estudios contables, no al vendedor solo |
| **2** | **Documentos que ARCA no cubre:** costeo de importaciones (facturas del exterior, despacho, flete, prorrateo por SKU → Tango/Xubio/planilla) vendido por despachantes y estudios | Documentos sin CAE, multilingües, con cálculo propio. Hay 33 mil importadoras nuevas desde 2023 (CEPA). No se encontró competencia específica | Competencia no investigada a fondo; volumen por cliente variable |
| **3** | **Soporte "¿dónde está mi pedido?" y cambios** para tiendas de indumentaria en Tiendanube con Andreani/OCA | La API de órdenes de Tiendanube trae el seguimiento; OCA tiene web service público; las herramientas globales no integran transportistas argentinos | Andreani da credenciales solo a clientes; WhatsApp ahora cobra mensajes de servicio |
| **4** | **"No perdés pedidos fuera de horario"** (voz + WhatsApp) para urgencias del hogar y servicio técnico en AMBA | La tecnología cuesta USD 0,09–0,14/min, menos que el supuesto del PDF | **Demanda:** en Argentina se escribe más de lo que se llama y Meta ya ofrece agentes de texto en WhatsApp |

**No conviene empezar por:** reporting genérico de agencias (commodity, USD 15–20 por cliente), OCR de facturas fiscales, ventas por WhatsApp genérico (Meta y Tiendanube ya lo hacen), un CRM nuevo (sí un módulo sobre Tokko o similares) ni localización de video.

---

## 2. Qué dice el PDF y qué se confirmó

| Afirmación del PDF | Estado (30/10/2026) |
|---|---|
| Smith.ai, AgencyAnalytics USD 20, Pipedrive USD 14, Gorgias, Textract, Document AI, Vapi USD 82–129 por 1.000 min, Twilio AR USD 0,0107/min y USD 8/mes | Confirmado. AgencyAnalytics declara hoy 90+ integraciones, no 85+ |
| HeyGen USD 200 M ARR (25/06/2026) | Confirmado (autodeclarado) |
| Precios GPT-6 Luna (USD 2) y GPT-6.1 Sol (USD 40) en el ejemplo | Confirmado. Omite gpt-6.1-terra (USD 20). Claude Haiku 5.5 y Gemini 2.5 Flash-Lite (USD 1,80) están en el mismo rango bajo |
| Google Ads retiró los developer tokens el 09/09/2026 | Confirmado |
| 71,5% del ecosistema Tiendanube vende por WhatsApp | Confirmado como dato de emprendedores argentinos (60,3% en grandes marcas); vía fuente secundaria |
| Vapi: licencia no sublicenciable | **Más restrictivo:** §2(d)(14) prohíbe crear productos o plantillas para terceros. Retell tiene programa de partners que permite "sell or bundle", en tensión con su §10.1(f). Hoy Retell parece la vía más clara, con confirmación escrita |
| WhatsApp: confirmar tarifa vigente | **Cambió:** desde el 01/10/2026 Meta cobra los mensajes de servicio después de 1.000 gratis por número y mes. En Argentina, USD 0,026 por mensaje de servicio y USD 0,0618 de marketing (tabla oficial de Meta). Embedded Signup v2 y v3 dejaron de funcionar el 15/10/2026; hay que usar v4 |

### Lo que el PDF no considera

1. ARCA ya entrega estructuradas las facturas recibidas (ver arriba).
2. Los sistemas incorporan IA: Tango (Delta) importa PDF con IA, Xubio también; Gorgias incluye agente de IA; Tiendanube y Meta lanzaron Chat Nube; Meta ofrece su propio agente en WhatsApp.
3. Los laboratorios de IA venden directo a pymes: Anthropic lanzó *Claude for Small Business* (13/05/2026), por ahora centrado en EE.UU. y QuickBooks. Eso empuja la barrera hacia la integración local.
4. Tipo de cambio (techo de la banda ≈ 29% arriba del mayorista), inflación (1,9% mensual y 33,4% interanual a septiembre 2026), IVA e Ingresos Brutos sobre servicios pagados en USD, y percepción del 30% con tarjeta.
5. Contracción de la demanda: el número de empleadores formales cayó (−2,6% interanual a febrero 2026).

---

## 3. Modelo económico recalculado para Argentina

Supuestos alternativos (hipótesis, no pronósticos): abonos de USD 150 / 250 / 99–149, CAC USD 500 (300 en reportes), baja mensual 6%, cobro por Mercado Pago a 10 días con IVA (≈ 5,3%) o por transferencia (0%), hora propia USD 20 o delegada USD 12, fijos USD 1.100.

| Escenario (USD por cliente y mes) | Contribución | Clientes para equilibrio | LTV/CAC |
|---|---|---|---|
| PDF documentos / voz / reportes | 122 / 112 / 69 | 10 / 10 / 17 | ≈ 10× |
| AR-A documentos (150, 5 h propias) | **−13** | no hay | 0,6 |
| AR-A voz (250, 1.000 min) | 1,7 | 640 | 1,1 |
| AR-A reportes (99) | 10,7 | 103 | 1,6 |
| AR-B documentos (150, 3 h delegadas a USD 12) | 51 | 22 | 2,7 |
| AR-B voz (250, 500 min, delegada) | 93 | 12 | 4,1 |
| AR-C documentos (199, 3 h propias, transferencia) | 84 | 14 | 3,8 |
| AR-C voz (299, 500 min, transferencia) | 139 | 8 | 5,6 |
| AR-C reportes (149, transferencia) | 66 | 17 | 4,7 |

**Reglas que salen de la tabla:** limitar las horas de revisión por cliente (≤ 3 h), cobrar por transferencia contra factura, acotar el volumen incluido y cobrar el excedente, no bajar a USD 99. El mercado alcanza: el equilibrio es 0,01–0,03% de las ≈ 78.000 empresas de 10 a 100 empleados. **La restricción es la distribución, no el tamaño del mercado.**

**Referencia de precio local:** los estudios contables pagan ARS 40–52 mil por mes por herramientas de carga de comprobantes; Xubio/Colppy cuestan entre 18 y 75 veces menos que USD 299. Botmaker vende callbots desde USD 149. Cobrar más exige vender un resultado medido (horas ahorradas, plata recuperada), no software.

---

## 4. Detalle por oportunidad

### 4.1 Rentabilidad y conciliación Mercado Libre / Mercado Pago (opciones 3 + 7)
- **APIs:** facturación de ML con cargos por orden (comisión, envío, publicidad); Product Ads con métricas por campaña y anuncio; Mercado Pago con reportes de liberaciones y liquidaciones, OAuth de solo lectura y gestión de contracargos (el token de renovación rota en cada uso). ML no publica sus límites de uso.
- **Competencia:** Porter Metrics, Supermetrics, AgencyAnalytics, Reportei y Metricool no cubren ML. Solo Kondado (Brasil, ≈ USD 19/mes) y Jaguar Sheet (AR, planilla para el vendedor). Colppy no funciona con Checkout Pro y su facturación es manual; Xubio sumó conciliación de extractos con IA; Simetrik apunta a empresas grandes.
- **Bancos:** no hay Open Finance operativo en 2026 (el Decreto 353/2025 creó el sistema, pero sin estándares del BCRA). Hay que trabajar con extractos.
- **Retenciones:** IVA y Ganancias sobre ML/MP se derogaron en 2024 (RG 5554/2024); Ingresos Brutos sigue y varía por provincia. El producto debe **mostrar** retenciones, no interpretarlas.
- **Producto mínimo:** informe semanal de rentabilidad real por producto (precio − comisión − envío − Ads − costo de mercadería − retenciones) y conciliación de lo vendido contra lo liberado por MP, con diferencias visibles. Segundo módulo: Tiendanube (programa de agencias desde mayo de 2026).
- **Regla legal:** es de solo lectura. Nunca tocar el dinero del cliente; custodiar, cobrar u ordenar pagos convierte el negocio en proveedor de servicios de pago (PSP) registrado ante el BCRA, y solo puede hacerlo una sociedad.

### 4.2 Documentos verticales
- **Validación casi gratis sin IA:** el QR de la factura (RG 4892) trae CUIT, punto de venta, tipo, número, importe, moneda y CAE; con el web service WSCDC de ARCA se constata el comprobante; se completa con la constancia de inscripción (A5 está deprecado), la base APOC y el control de duplicados. "Mis Comprobantes" no tiene web service oficial: solo exportación CSV.
- **APIs de gestión:** Alegra y DUX tienen API REST pública; Tango Delta tiene APIs por proceso con token; Holistor importa Excel; no se encontró documentación vigente de Xubio, Colppy y Contabilium.
- **Costo de IA:** USD 0,35–3 por 1.000 páginas con LLM barato; Textract AnalyzeExpense y Azure ≈ USD 10; Document AI USD 0,10 por documento. Irrelevante frente a las horas de revisión.
- **Competencia genérica:** al menos 8 actores locales (FacturAI, Sourced, CargaFacturas, PortalContador, XPyME, Contapilot, FORJA, Xtract).
- **Demanda:** en la encuesta Thomson Reuters/CPCECABA 2025, la barrera principal para usar IA es "no sé cómo implementarlo" (39%). Eso favorece un servicio asistido.
- **Cuña recomendada:** costeo de importaciones para pymes importadoras nuevas, por despachantes y estudios. Plan B: administración de consorcios en CABA (deben publicar comprobantes de cada gasto; ya existe CONSO con lectura por IA).

### 4.3 Soporte ecommerce, ventas por WhatsApp y CRM vertical (opciones 5, 6 y 4)
- **WhatsApp en Argentina:** USD 0,026 por mensaje de servicio después de 1.000 gratis/mes por número; USD 0,0618 marketing. Una pyme con 1.500 conversaciones/mes paga ≈ USD 556/mes a Meta (estimación). Conviene que el cliente pague a Meta con su tarjeta (modelo Tech Provider) y cobrarle el software o el resultado.
- **Política de IA de Meta (cláusula 4.7, 23/09/2026):** prohíbe proveedores donde la IA es el producto principal y el entrenamiento con datos de WhatsApp. Un asistente sectorial secundario al servicio del comercio está permitido, sin aprobación automática.
- **Mercado:** el ecommerce argentino facturó ARS 34,03 billones en 2025 (CACE, +55% nominal); en el primer semestre de 2026 creció 28% nominal, casi cero en términos reales.
- **Soporte ecommerce:** Gorgias, Zendesk y Freshdesk cobran USD 0,49–2 por consulta resuelta con IA y no integran transportistas argentinos. Cuña: "¿dónde está mi pedido?" y cambios para indumentaria en Tiendanube con Andreani/OCA.
- **Ventas por WhatsApp:** solo vertical, por ejemplo presupuestador para corralones, ferreterías, repuestos o mayoristas, entregando un borrador de presupuesto que aprueba el vendedor.
- **CRM:** como módulo, no como CRM nuevo. Tokko Broker (API en planes Profesional y Corporativo) y KiteProp en inmobiliarias, Tecnom en concesionarias. Hipótesis sin competencia verificada: renovaciones para productores de seguros.

### 4.4 Voz entrante con IA (opción 2)
- **Telefonía:** números locales por API en Twilio (USD 8/mes + USD 0,0107/min, con registro comercial y domicilio en el área) y Telnyx (precio publicado contradictorio). Plivo no admite entrantes en AR; Vonage no tiene autoservicio. Anura ofrece troncal SIP, geográficos y 0800/0810 con portabilidad. ENACOM asigna numeración solo a prestadores registrados: hay que alquilar.
- **Costo total:** USD 0,09–0,14 por minuto con Vapi o Retell + LLM chico + voz estándar + Twilio AR. Se va a USD 0,30+ con el modelo realtime completo de OpenAI, voces premium, 0800 (USD 0,258/min) o transferencias a celular (USD 0,353/min).
- **WhatsApp Calling:** llamadas iniciadas por el usuario gratis, funciona en AR y admite SIP. Exige Cloud API y límite de al menos 2.000 destinatarios por día.
- **Legal:** avisar grabación y finalidad (Ley 25.326); no hay norma que obligue a avisar que atiende una IA, pero conviene; la Res. SCI 1033/2021 exige opción humana pero exceptúa a mipymes (confirmar vigencia); "No Llame" solo aplica a salientes de venta.
- **Diseño:** números geográficos, no 0800; en vez de transferir al celular, devolución de llamada con resumen por WhatsApp. Plan de entrada a probar: USD 99–199 por 300–500 min.

---

## 5. Marco legal, fiscal y de cobro (resumen)

| Tema | Qué hacer |
|---|---|
| Forma jurídica | Arrancar en **monotributo** (escala desde el 01/08/2026: categoría A hasta ARS 12,0 M/año, K hasta ARS 126,6 M). Las facturas E probablemente suman al tope: computarlas. Pasar a SAS con tracción |
| Cobros del exterior | Persona física: según la Com. "A" 8481 (14/09/2026) no hay obligación de pasarlos a pesos si entran a una cuenta en USD propia en un banco local. Una SAS sí debe liquidar en 20 días hábiles, salvo la excepción de Economía del Conocimiento (solo para sueldos) |
| Plataformas | Payoneer (ACH gratis, retiro USD 1,50), Wise, Deel, LLC con Stripe Atlas (USD 500 + costos anuales). Cripto: zona gris |
| Pagar APIs en USD | Percepción del 30% con tarjeta (RG 5617) salvo que se pague el saldo en USD con dólares propios; IVA 21% sobre servicios digitales e IIBB según provincia. En monotributo, el IVA es costo |
| Precios a clientes | USD pagaderos en ARS al BNA vendedor, o ARS con ajuste mensual por IPC; consumo de API aparte |
| Datos personales | Ley 25.326: Federico es encargado de tratamiento; contrato con cada cliente; transferencia a EE.UU. con cláusulas modelo AAIP (Res. 198/2023). Proyecto de reforma 3397-D-2026 en Diputados |
| IA | No hay ley de IA; guía orientativa de la AAIP |
| BCRA | Conciliación de solo lectura no requiere registro como PSP. Cobrar o custodiar dinero de terceros, sí |
| Apoyos | Economía del Conocimiento exige persona jurídica; para micro de menos de 3 años alcanza acreditar la actividad; bono de 70–80% de cargas sociales, hasta 60% menos de Ganancias, exención de derechos de exportación |

Checklist completo en `detalle/05-legal-fiscal.md`, sección 9.

---

## 6. Salida al mercado desde cero

- **Universo:** 525.538 empresas empleadoras (SIPA, abril 2025): 84% con menos de 10 empleados, ≈ 68.000 de 10 a 50, ≈ 10.500 de 51 a 100. La cifra de "606.000 mipymes" que circula es de 2019.
- **Canales por oportunidad:**
  - Mercado Libre: agencias y consultoras de ML, estudios contables con clientes de ecommerce, comunidades de vendedores.
  - Documentos: consejos profesionales de ciencias económicas (jornadas de IA en Santa Fe y Córdoba en 2026), partners de Tango (Axoft fue adquirida por Vela LatAm), despachantes de aduana, un contador "campeón" por zona con comisión recurrente.
  - Ecommerce: partners y agencias de Tiendanube, eCommerce Day (CACE).
  - Voz: cámaras de oficios, proveedores de telefonía, agencias locales.
- **Outreach:** con benchmarks globales (3,4% de respuesta en correo frío, 7,2% en LinkedIn), 15 entrevistas exigen ≈ 900 correos o ≈ 1.600 invitaciones. Mejor: diagnóstico gratuito de 30 minutos con datos reales del cliente (ej. "te muestro cuánto te cobró de verdad ML por cada producto el mes pasado").

---

## 7. Plan de 90 días recomendado

Aplica el método del PDF (entrevistas, pilotos pagos, métricas) a la cuña #1, con la #2 como alternativa.

**Días 1–30: problema y comprador**
- 12–15 entrevistas con agencias/consultoras de Mercado Libre y estudios contables con clientes que venden en ML. Preguntar por el último cierre de mes: cuánto tardaron en conciliar ML/MP y qué diferencias quedaron sin explicar.
- Prototipo con la cuenta de un vendedor que autorice el acceso (OAuth de solo lectura en ML y MP): rentabilidad por producto y conciliación vendido vs. liberado.
- Ofrecer 5 pilotos pagos en pesos (equivalente USD 100–200), con criterio de éxito escrito. Meta: 2 pagos.
- En paralelo: monotributo, cuenta en USD, contrato de servicio + acuerdo de encargado de tratamiento.

**Días 31–60: pilotos**
- 2–3 pilotos. Medir horas por cliente (objetivo ≤ 3 h/mes), diferencias encontradas, plata recuperada (cargos mal cobrados, liberaciones faltantes) y uso del informe.

**Días 61–90: repetir y cobrar**
- 3–5 clientes y al menos 2 renovaciones. Precio objetivo a validar: USD 150–200 por cuenta, cobrado por transferencia. Repetir una implementación sin rehacer el producto.
- **Frenar** si nadie paga, si la revisión supera 3 h por cliente o si cada cliente pide un producto distinto. Pasar a la cuña #2 (costeo de importaciones) con el mismo método.

---

## 8. Datos que no se pudieron confirmar

Se agotó el cupo de búsquedas web compartido entre los agentes. Quedaron pendientes:
- Cuota de mercado de los sistemas contables, total nacional de contadores, volumen anual de comprobantes, cantidad de agencias digitales y de partners de Tango.
- Competidores en costeo de importaciones; precios oficiales de Xubio, Colppy, Nubimetrics, Real Trends, Tokko, Treble, Darwin AI, Blip, Yalo, Gupshup, Aivo, Cliengo.
- Tarifa por minuto de Telnyx en AR, precios de Anura/IPLAN/Telecentro, desvío de llamadas en operadoras móviles, dato argentino de preferencia teléfono vs. WhatsApp.
- API de Correo Argentino y de envíos de ML para tiendas propias.
- Derechos de exportación sobre servicios hoy, costo total de una SAS, alícuotas 2026 de IIBB en CABA y PBA, tarifa 2026 de PayPal, si EE.UU. fue reconocido como país adecuado.

---

## Archivos de detalle

| Archivo | Tema | Fuentes |
|---|---|---|
| `detalle/01-documentos.md` | Documentos verticales, ARCA, sistemas de gestión | con URL y fecha |
| `detalle/02-voz.md` | Voz entrante, telefonía, costos por minuto | 42 |
| `detalle/03-reporting-conciliacion.md` | Reporting de agencias y conciliación ML/MP | 41 |
| `detalle/04-whatsapp-ecommerce-crm.md` | WhatsApp, soporte ecommerce, CRM | 40 |
| `detalle/05-legal-fiscal.md` | Legal, fiscal, cambiario, checklist | 52 |
| `detalle/06-verificacion-gtm.md` | Verificación del PDF, modelo AR, salida al mercado | 58 |
