# Oportunidad 1: Documentos verticales en Argentina

**Para:** Federico Coronel · **Investigación hecha entre el 29 y el 30 de octubre de 2026** · Profundiza la Oportunidad 1 del informe "Negocios digitales con APIs".

> **Cómo leer este documento.** Las etiquetas indican qué tan firme es cada afirmación:
> - **[V]**: verificado en la fuente oficial o primaria citada.
> - **[P]**: lo dice el propio proveedor, en marketing o en una nota de prensa. No fue auditado.
> - **[T]**: viene de un tercero (blog, comparador o agregador) y no se confirmó en la fuente original.
> - **[E]**: estimación o cálculo propio.
>
> Si un dato no se encontró, el texto lo dice. Durante el trabajo se agotó el cupo de búsquedas web, así que algunos huecos quedaron sin cubrir. Están listados en la sección 9.

---

## 0. Resumen ejecutivo

1. **Lo central del documento argentino ya es digital y verificable.** Toda factura electrónica trae un QR con un JSON en Base64: CUIT, punto de venta, tipo, número, fecha, importe, moneda y CAE/CAEA [V][13]. Con esos mismos campos se consulta el web service oficial **WSCDC (Constatación de Comprobantes)**, que devuelve A (aprobado) o R (rechazado) [V][11][12]. Para validar el encabezado no hace falta IA: alcanza con decodificar el QR y consultar a ARCA.
2. **ARCA ya precarga las compras para el IVA.** Con **IVA Simple** (F.2051), obligatorio desde el período noviembre de 2025, los comprobantes recibidos llegan automáticamente [T][16][17]. Vender "cargar facturas para el libro IVA" es vender algo que el Estado ya resuelve. El valor que queda está en otros lugares: **imputación contable y detalle de ítems, documentos que no son facturas electrónicas, conciliación entre ARCA y el sistema de gestión, y procesos operativos** (orden de compra, remito y factura; costeo; rendiciones).
3. **El segmento genérico de facturas de proveedor ya está ocupado.** Tango (Delta) [V][5] y Xubio [V][7] incorporaron la lectura de PDF con IA. Hay al menos 8 jugadores locales: FacturAI, Sourced, CargaFacturas, PortalContador, XPyME, Contapilot, FORJA y Xtract. Xtract proyecta USD 7,5 millones de ingresos para 2027 [P][22].
4. **La demanda existe, pero el canal todavía está en etapa temprana.** En una encuesta a 561 profesionales, el 16% de los que usan IA la aplican a la carga de comprobantes. Entre quienes todavía no la usan, el 30% querría usarla para eso. La principal barrera es "no sé cómo implementarlo" (39%) [V][19].
5. **Cuña recomendada (hipótesis a validar): el costeo documental de importaciones** para las pymes que empezaron a importar desde 2024. Según CEPA, son unas 33.000 firmas nuevas [T][27]. Se venderían a través de despachantes y estudios contables, con salida a Tango, Xubio o una planilla. La alternativa es **administración de consorcios en CABA** [T][28], aunque ese nicho ya tiene un competidor con IA (CONSO) [T][29].

---

## 1. Sistemas de gestión y contables: cuota, API e importación

**Cuota de uso:** no se encontró ninguna encuesta con cuota de mercado de software contable entre pymes o estudios argentinos.
- Lo más cercano es una tesis de la UNCuyo con una muestra de estudiantes, que menciona a "Tiempo, Tango y Bejerman" como los más usados. No sirve para estimar cuota [T][1].
- Xubio declaraba unas 40.000 empresas gestionadas hacia 2020 y casi 50.000 clientes en AR, CO y MX en octubre de 2021 [P][2][3].
- Para Colppy, el último dato público de usuarios encontrado es de 2014, así que no es utilizable.

| Sistema | Perfil | API o integración (estado verificado) | Importación sin API | Precio de referencia |
|---|---|---|---|---|
| **Tango Gestión (Axoft)** | Pymes medianas. Muy presente en estudios [T][4] | Compras ya hace "importación automática de comprobantes en PDF […] utilizando inteligencia artificial" y "compara información obtenida de Mis Comprobantes ARCA" [V][5]. Las APIs son por proceso en la plataforma Delta, con token de desarrollador, más la REST de Tango Tiendas (que pide licencia Full) [T][6]. Hay una API oficial de comprobantes en JSON solo para ventas con CAE [V][GitHub TangoSoftware/ApiClientes] | Transferencias entre bases y Excel de proveedores [V][5] | Desde ~ARS 528.000/mes más implementación, a junio de 2026 [T][4] |
| **Xubio** | Monotributistas, pymes y estudios | "Importación de comprobantes con Inteligencia Artificial" dentro del módulo contable [V][7]. Hay un SDK no oficial en PHP (2021) con CLIENT_ID y SECRET [T][8]. No se encontraron documentos oficiales públicos de una API de compras | Excel | Planes de ARS 123.100 a 375.900 + IVA por mes, con 300 a 10.000 comprobantes, a septiembre de 2026 [T][9]. Gratis 6 meses para matriculados del CPCECABA [V][7] |
| **Colppy** | Pymes y estudios | Existió una API, según una gema Ruby de 2016 con wiki en Atlassian [T][10]. Para acceso a la API, el soporte deriva a ventas [T] | **Importador masivo de facturas de compra** (Proveedores > Importar > Facturas) e importación desde Mis Comprobantes Recibidos [V][intercom Colppy] | No publicado en lo encontrado |
| **Contabilium** | Pymes y e-commerce | No se encontró documentación pública. Un hilo de Make/Pipedrive dice que el botón "API" lleva a un registro [T] | Conectores de marketplaces | No encontrado |
| **Alegra** | Pymes LatAm | **API REST pública** con *bills* (facturas de proveedor) y operaciones CRUD. Autenticación Basic con email y token [T][Apideck] | CSV | No relevado |
| **Bejerman (Thomson Reuters)** | Estudios y medianas | Anunció "carga inteligente de documentos" con IA en octubre de 2024. El acceso a la API depende de versión y licencia [T][6] | No relevado | Se cotiza a través de agentes [T][4] |
| **Holistor** | Estudios contables | No se encontró API | IVA Registración: "Importar datos de otros sistemas" desde Excel o .prn. El documento es de 2009 y hay que confirmar si sigue vigente [T][Holistor PDF] | No relevado |
| **DUX** | Pymes comerciales | REST pública en planes PRO y FULL. No tiene webhooks. Límite de 1 request cada 5 s. No maneja asientos [T][6] | — | — |
| **Onvio, Nubox, Siigo** | — | No se relevó Onvio. Nubox (Chile) declara que puede incorporar hasta 800 documentos de clientes con propuesta de cuentas [P][Nubox blog]. Siigo es de Colombia | — | — |

**Marketplaces de partners:** no se encontró un marketplace público de apps para Tango, Xubio ni Colppy. Tango tiene una red de partners o distribuidores (consultoras implementadoras) que funciona como canal [T][6].

**Lectura:** los dos destinos con más volumen (Tango y Xubio) **ya incluyen extracción de PDF con IA de forma nativa**. Un producto externo tiene que aportar algo más: reglas del vertical, validación fiscal y operativa, documentos no estándar, multi-cliente para el estudio o integración con otros sistemas.

---

## 2. APIs de ARCA: qué se puede validar automáticamente

| Servicio | Qué hace | Estado |
|---|---|---|
| **WSAA** | Autenticación. Con un certificado X.509 se obtiene un *token* y un *sign* válidos por 12 h | [V][14] y [T] para el plazo |
| **WSFEv1 / WSFEX / WSMTXCA** | **Emisión** de factura electrónica (mercado interno, exportación y con detalle de ítems). Sirve para emitir, no para validar facturas recibidas | [V][15] |
| **WSCDC (Constatación de Comprobantes)** | "Verificar en forma dinámica si los comprobantes **recibidos** se encuentran autorizados por ARCA". El método `ComprobanteConstatar` recibe CbteModo (CAE, CAEA o CAI), CuitEmisor, PtoVta, CbteTipo, CbteNro, CbteFch, ImpTotal, CodAutorizacion y, en forma opcional, el documento del receptor. Devuelve `Resultado` A o R con observaciones. Endpoint de producción: `servicios1.arca.gob.ar/WSCDC/service.asmx`. El manual v0.4 es del 01/12/2025 | [V][11][12] |
| **Padrón: Constancia de Inscripción, A4, A10, A13, A100** | Datos del CUIT: condición frente al IVA, impuestos y actividades. **El A5 está deprecado** y lo reemplaza `ws_sr_constancia_inscripcion` | [V][11] |
| **Consulta de contribuyentes apócrifos (APOC)** | Indica si un CUIT figura como emisor de facturas apócrifas | [V][11] |
| **WSCPE (Carta de Porte Electrónica)** y remitos electrónicos cárnico, harinero y azúcar | Documentos de transporte que ya nacen electrónicos | [V][11] |
| **"Mis Comprobantes" (recibidos)** | **No figura en el catálogo de web services** [V][11]. YoFacturo afirma que "ARCA no ofrece un servicio web para consultarlos" y que la vía es exportar el CSV o Excel [P][18]. PortalContador dice que consulta Mis Comprobantes "directamente", seguramente con la clave fiscal del cliente; no se verificó el método [P][20] | Sin API oficial |
| **QR de factura (RG 4892/2020)** | El texto es `https://www.arca.gob.ar/fe/qr/?p={JSON en Base64}` con los campos ver, fecha, cuit, ptoVta, tipoCmp, nroCmp, importe, moneda, ctz, tipoDocRec, nroDocRec, tipoCodAut (E=CAE, A=CAEA) y codAut | [V][13] |

**Validaciones automáticas posibles en una factura argentina (diseño propuesto, [E]):**
1. Decodificar el QR y obtener los campos del encabezado sin OCR. Si no hay QR, se extraen con OCR o un LLM.
2. Constatar con WSCDC si el comprobante existe y el CAE coincide con importe y fecha.
3. Consultar el padrón del emisor para ver la condición de IVA y comprobar que corresponde al tipo de comprobante (A, B, C o M).
4. Consultar APOC para el emisor.
5. Buscar duplicados por la clave (CUIT, tipo, punto de venta, número).
6. Verificar la coherencia aritmética: neto + IVA por alícuota + percepciones = total.
7. Confirmar que el CUIT receptor sea el del cliente.
8. Validaciones de negocio, como el cruce con orden de compra o remito y los límites por proveedor.

**Requisitos para usar los web services:**
- Clave fiscal y un certificado digital que se genera en "Administrador de Certificados Digitales". En homologación se usa WSASS [V][14].
- Asociar el servicio en "Administrador de Relaciones de Clave Fiscal" [V][14].
- **Delegación:** el contribuyente puede autorizar a otro CUIT (el del proveedor del servicio) a operar el web service en su nombre. Eso evita manejar un certificado por cliente [T][14].
- El nivel 3 de clave fiscal lo mencionan terceros, no la página oficial.

---

## 3. Competidores en Argentina y LatAm

| Jugador | Qué hace | Destinos | Validación ARCA | Precio publicado |
|---|---|---|---|---|
| **Tango Delta (nativo)** | Importa PDF con IA en Compras y compara con Mis Comprobantes | Tango | Sí, padrón y Mis Comprobantes | Incluido en la licencia [V][5] |
| **Xubio (nativo)** | Importa comprobantes con IA y concilia bancos con IA (oct-2026) | Xubio | No detallado | Incluido en el plan [V][7] |
| **FacturAI** | OCR "98%", alertas de precio, foco en gastronomía | Siigo, Tango, Contabilium, Excel | CAE, CUIT, APOC y duplicados | 0 / 9 / 29 / 59 / 149 por mes para 30 / 100 / 400 / 900 / 3.000 facturas. **La moneda no se indica** [P][21] |
| **Sourced (gosourced.ai)** | Cuentas a pagar: OCR, revisión de campos dudosos y matching con OC | Tango | CAE/CAI, CUIT, tipo y número, importes | No publicado. Demo [P][23] |
| **CargaFacturas** | OCR + LLM "entrenado en facturas AR". A, B, C y NC | Calipso, Dynamics, Odoo | No detallado | En ARS, no visible [P][24] |
| **PortalContador** | Para estudios: bancos, tarjetas, Mis Comprobantes, Portal IVA, APOC e imputación con IA | Excel listo para Xubio | APOC y constancia | Packs de ARS 11.500 a 58.000; **ARS 52.000/mes ilimitado** [P][20] |
| **XPyME** | ERP con módulo de lectura de facturas de compra con IA | XPyME | No | Abono mensual, sin precio publicado [P][25] |
| **Xtract** (fundada en 2020) | Automatización financiera "determinística, sin LLM genérico". Clientes: Arcos Dorados y MODO (9.300 facturas en MODO). Más de 50 ERP. Más de 36 empleados. Sin inversión externa | SAP, Oracle, NetSuite, Dynamics | — | No publicado. Proyecta USD 7,5 M para 2027 [P][22] |
| **Contapilot, FORJA, CONTADOR-IA** | Contabilidad con IA para pymes y estudios | — | — | FORJA USD 200/mes; CONTADOR-IA ARS 40.000/mes (200 interacciones). Ambos vistos solo en extractos de búsqueda [T] |
| **CONSO** (consorcios) | Liquidación de expensas y facturas de proveedores leídas con IA que pasan a la liquidación | Propio | — | "Desde ARS 2.950", con precio por unidad. Ficha de Capterra probablemente desactualizada [T][29] |
| **Clara** | Gastos corporativos y reintegros por WhatsApp con IA (llegó a AR) | — | — | No público [T] |
| **Nanonets / Mindee (globales)** | APIs de extracción | API | No | Ver sección 4 |

**No se pudo relevar:** precios de Rindegastos (la búsqueda no los devolvió), Bind ERP ni Expensify LatAm.

---

## 4. Calidad y costo de OCR/IA para facturas argentinas

**Calidad:**
- No se encontró ningún benchmark independiente sobre facturas argentinas. Las precisiones publicadas son de cada proveedor: FacturAI 98%, Sourced más de 95%, CargaFacturas 96,4% y Xtract 98% [P].
- Xtract critica que los LLM generativos pueden dar resultados distintos sobre la misma factura ("en contabilidad, casi bien es mal") [P][22].
- Los integradores locales (Nexosmart, NetOne) dicen que el OCR genérico falla con los formatos variables de Argentina [P].
- **Cómo atenuar el problema [E]:** usar el QR y WSCDC para el encabezado, que es determinístico, y dejar el modelo solo para ítems, imputación y documentos sin QR, con una cola de revisión. Así el riesgo queda acotado a los campos que no se pueden verificar contra ARCA.

**Precios de lista consultados el 29/10/2026:**

| Servicio | Precio | Equivalente por 1.000 páginas | Etiqueta |
|---|---|---|---|
| AWS Textract AnalyzeExpense (Oregon) | USD 0,01 por página (0,008 después de 1 M) | USD 10 | [V][30] |
| AWS Textract Detect Text | USD 0,0015 por página | USD 1,50 | [V][30] |
| Google Document AI Invoice Parser | USD 0,10 por documento de 1 a 10 páginas | ~USD 100 por 1.000 facturas | Informe base [32]. No se pudo reverificar porque la página no cargó |
| Azure Document Intelligence prebuilt (invoice) | ~USD 10 por 1.000 páginas; Read USD 1,50 | USD 10 | [T][31]. La página oficial mostraba los precios vacíos |
| Mindee | Desde ~USD 0,05 por crédito (página) + 20% de excedente. Starter 44/mes | ~USD 44–60 | [P][32]. La página tiene inconsistencias internas |
| Nanonets | USD 0,30 por ejecución de bloque "complejo" de IA; el flujo típico de factura "menos de USD 2 por factura" | USD 300 a 2.000 | [P][33] |
| **Gemini 2.5 Flash-Lite** | USD 0,10 por 1M de tokens de entrada y 0,40 por 1M de salida. **258 tokens por página de PDF** | **~USD 0,35** [E]* | [V][34][35] |
| Gemini 3.8 Flash | USD 0,75 de entrada y 3,75 de salida por 1M de tokens. El precio se duplica el 01/01/2027 | **~USD 3** [E]* | [V][34] |

\* Supuesto propio: unos 1.000 tokens de entrada por página (258 de la imagen más el prompt) y unos 600 de salida (JSON). Las imágenes JPG pueden consumir otra cantidad de tokens. Sin batch.

**Conclusión de costos [E]:** con un LLM multimodal económico, la extracción cuesta menos de USD 0,005 por página. Es entre 20 y 300 veces menos que los parsers especializados. **El costo técnico es irrelevante frente a los minutos humanos de revisión.** Coincide con la advertencia del informe base: el margen depende de las excepciones.

---

## 5. Tamaño del canal

| Indicador | Dato | Fecha | Etiqueta |
|---|---|---|---|
| Matriculados del CPCECABA (solo CABA, incluye todas las profesiones de ciencias económicas) | 76.000, de los cuales 62.000 estaban habilitados para votar | Junio 2022 | [T][36]. El sitio TRIVIA menciona "más de 70/80 mil", sin fecha ni verificación |
| Contadores matriculados en todo el país (FACPCE) | **No encontrado** | — | — |
| Empresas empleadoras privadas | **477.463**, con una caída de 3,3% interanual | Mayo 2026 (SRT) | [T][37] |
| Monotributistas | Más de 4,5 millones | 2024–2025 | [T][Cronista] |
| Firmas importadoras | Se duplicaron frente a 2023, con **33.108 empresas nuevas**. El 80% del monto lo siguen aportando las que ya importaban | 1er semestre 2026 (CEPA) | [T][27] |
| Comprobantes electrónicos emitidos por año en AR | **No encontrado** (solo hay datos de Perú) | — | — |
| Cartas de porte | ~5,2 millones de viajes de granos por año | Estimación BCR 2019 | [T][38] |
| Adopción de IA en estudios | 36% la usa; 16% de quienes la usan, para carga de comprobantes; 30% de los indecisos querría usarla para eso; 54% planea invertir en tecnología en 2025 | Encuesta de TR y CPCECABA con n=561, 2025 | [V][19] |

---

## 6. Nichos verticales con dolor documental

| Nicho | Documentos | ¿Ya está digital en ARCA? | Competencia vista | Evaluación [E] |
|---|---|---|---|---|
| **Agro / cartas de porte** | CPE, liquidaciones de granos (WSLPG) | **Sí.** CPE y LPG nacen electrónicos [V][11] | ERPs agro (no relevados) | Poco OCR. El valor está en la conciliación. **Mala cuña para OCR** |
| **Logística / remitos** | Remitos en papel con firma, COT y guías | Remito electrónico solo para cárnicos, harinas y azúcar [V][11] | No relevada | Dolor real (prueba de entrega), pero son fotos manuscritas de baja calidad. Tiene más que ver con operaciones que con contabilidad |
| **Construcción** | Certificados de obra, facturas de corralón, partes diarios | Facturas sí; certificados no | XPyME menciona corralones [P][25] | Fragmentado, con formatos propios en cada empresa |
| **Consorcios (CABA)** | Facturas de monotributistas (C), tickets, recibos, servicios, sueldos de encargados | Parcial | **CONSO con IA** [T][29] | **Obligación regulatoria:** desde el 01/08/2024 la liquidación debe incluir QR o link con los comprobantes escaneados de cada gasto [T][28]. El dolor es claro y el comprador es identificable (administradores), pero ya hay un software vertical con IA |
| **Importadores pymes** | Factura comercial del exterior (inglés o chino), packing list, B/L o AWB, despacho, liquidación del despachante, gastos de terminal y flete | **No** como factura electrónica estándar; la factura del exterior no tiene CAE | Ningún competidor específico encontrado (sin búsqueda dedicada por falta de cupo) | **Mejor cuña candidata.** Base nueva y grande (33 mil firmas nuevas), documentos heterogéneos que la IA nativa de Tango o Xubio no resuelve, necesidad de **costeo** con prorrateo de flete, seguro, derechos, tasa y percepciones, y canal concentrado en despachantes |
| Estudios contables (genérico) | Facturas y tickets que llegan por WhatsApp | Encabezado precargado | Saturado (más de 8 jugadores más los nativos) | Solo con un ángulo multi-cliente y barato. Riesgo de pelear por precio |

---

## 7. Señales de demanda y disposición a pagar

- **Estudios:** PortalContador cobra **ARS 52.000/mes** por uso ilimitado [P][20]. CONTADOR-IA cobra ARS 40.000/mes [T]. Si FacturAI cobra en USD, son USD 0,05–0,09 por factura [P][21] y [E]. Xubio cobra a las empresas entre ARS 123 mil y 376 mil por mes [T][9]. Es un ancla de cuánto paga una pyme por todo su sistema.
- **Medianas y grandes:** Xtract tiene más de 36 empleados y proyecta USD 7,5 millones con clientes corporativos, lo que muestra que se paga por automatizar cuentas a pagar con garantía de exactitud [P][22]. Nanonets estima "menos de USD 2 por factura" de punta a punta [P][33].
- **Implementación:** Nexosmart ofrece pilotos con 50–100 facturas en 4–6 semanas [P]. Es un formato de venta similar al que propone el informe base.
- **Brecha de la banda del informe base:** el informe proponía USD 149–399/mes. Para un estudio pequeño, ARS 40–52 mil/mes es la referencia local, mucho menos que esa banda. **USD 149–399 solo parece defendible para pymes con proceso operativo (costeo, matching) o para administradores con muchas unidades**, no para un estudio que busca "cargar facturas" [E].

---

## 8. Implicancias y recomendación para Federico

**Qué cambia respecto del informe genérico:**
1. **No conviene construir otro "lector de facturas de proveedor".** El encabezado se resuelve gratis con el QR y WSCDC, el IVA ya viene precargado por ARCA y Tango y Xubio ya incorporaron la IA. Un producto así compite con funciones incluidas en la licencia que el cliente ya paga.
2. **El activo técnico diferencial es barato y determinístico:** el pipeline QR → WSCDC → padrón → APOC → duplicados, más un LLM económico (menos de USD 0,005 por página) para lo que no tiene QR. El costo real es la revisión humana, así que hay que elegir documentos donde las reglas atrapen la mayoría de los errores.
3. **Conviene apuntar a documentos que ARCA no tiene y que los ERP no entienden.**

**Cuña recomendada (hipótesis, sin validar): "Costeo de importaciones listo para el sistema" para pymes importadoras nuevas.**
- **Quién paga:** pymes que empezaron a importar desde 2024 (comercio, indumentaria, juguetes, electrónica) y sus estudios contables.
- **Canal a probar:** **despachantes de aduana**, que concentran decenas de importadores cada uno, y estudios con cartera importadora.
- **Qué entrega:** se reciben la factura comercial del exterior, el packing list, el B/L, el despacho, la liquidación del despachante y los gastos locales (flete, terminal, depósito). El servicio extrae, valida (CUIT y CAE de los gastos locales vía WSCDC, coherencia de montos y tipo de cambio), **prorratea el costo por SKU** y exporta a Tango, Xubio o una planilla de costos, con una cola de excepciones.
- **Por qué esta cuña:**
  - Son documentos multilingües y heterogéneos, sin CAE en la factura de origen.
  - El resultado (costo unitario real) tiene valor económico directo para fijar precios.
  - La base de clientes crece.
  - No se encontró un competidor específico, aunque no hubo búsqueda dedicada.
- **Precio a testear [E]:** puesta en marcha de USD 300–600, más USD 15–40 por operación de importación costeada, o un abono de USD 149–299 con cupo de despachos.
- **Riesgos:**
  - Ciclo de importaciones volátil, sujeto a la política macro.
  - Hace falta conocer los conceptos aduaneros (derechos, tasa estadística, percepciones) y validarlos con un despachante.
  - El volumen por cliente es bajo: decenas de despachos por mes, no miles de facturas.

**Plan B: administradores de consorcios en CABA.** Hay una obligación concreta desde agosto de 2024 de publicar los comprobantes de cada gasto, y el comprador es identificable. El producto sería **armado y validación del legajo de comprobantes por liquidación**: CAE, APOC y duplicados entre consorcios. Antes de invertir hay que confirmar la disposición vigente y competir o integrarse con CONSO u otros softwares de expensas.

**Próximos pasos concretos (días 1 a 30):**
1. Hacer 8 entrevistas con despachantes y 6 con importadores pymes, preguntando por el último despacho y cómo calcularon el costo.
2. Construir un prototipo del pipeline QR → WSCDC en homologación (certificado de testing vía WSASS) y procesar 20 documentos reales con permiso.
3. Confirmar con Axoft y Xubio cómo importar compras con costo por ítem (API Delta o Excel) antes de prometer integración.
4. Ofrecer 3 pilotos pagos de costeo para 5 despachos cada uno.

---

## 9. Huecos de información (no encontrados o no verificados)

- Cuota de mercado de los sistemas contables en Argentina.
- Cantidad nacional de contadores matriculados (FACPCE).
- Volumen anual de comprobantes electrónicos.
- Documentación oficial de las APIs de Xubio, Contabilium y Colppy (actual).
- Precios de Rindegastos, Bind y Expensify LatAm.
- Competidores específicos de costeo de importaciones.
- Cantidad de consorcios en CABA y número de la disposición de 2024.
- Precio oficial actual de Google Document AI y Azure.

Se agotó el cupo de búsqueda web de la sesión. Estos puntos se pueden completar en una ronda siguiente.

---

## Fuentes (consultadas entre el 29 y el 30/10/2026)

1. UNCuyo, "La revolución tecnológica en la contabilidad": https://bdigital.uncu.edu.ar/objetos_digitales/19398/la-revolucin-tecnolgica-en-la-contabilidad.pdf
2. Cronista, nota sobre Xubio (~2020): https://www.cronista.com/infotechnology/entreprenerds/este-argentino-ayuda-a-los-comercios-que-evita-el-contacto-fisico-y-tarjetas-planea-facturar-us-2-m
3. Forbes Argentina, oct. 2021: https://www.forbesargentina.com/negocios/prepandemia-tenian-30-empleados-hoy-son-70-hacen-apuntan-pymes-n8839
4. Wynges, ranking de software de gestión 2026 (act. 11/09/2026): https://wynges.com/blog/top-10-software-zeus-flexus-softland-xubio-tango-bejerman-contagram-colppy-nubox/
5. Axoft, Tango Compras: https://www.axoft.com/tango/software-de-gestion/soluciones/compras.php
6. Duotach, "Integrar IA con Tango, Bejerman, DUX" (19/07/2026): https://duotach.com/en/blog/integrar-ia-tango-bejerman-dux
7. Propuesta Xubio para matriculados del CPCECABA 2025: https://consejo.org.ar/storage/attachments/Propuesta%20XUBIO%20-%20MPE%202025_v2.pdf-x6vEHIulUo.pdf
8. SDK no oficial de Xubio (Packagist): https://packagist.org/packages/xubio/sdk
9. SpomSolutions, alternativas a Xubio (precios a sep-2026): https://app.spomsolutions.com/comparar/alternativas-a-xubio
10. Gema Ruby de Colppy: https://rubygems.org/gems/colppy · Ayuda de Colppy sobre facturas de compra: https://intercom.help/Colppy/es/articles/3207270-factura-de-compra-proveedores · Importar desde Mis Comprobantes: https://intercom.help/Colppy/es/articles/3181130-importar-tus-facturas-desde-mis-comprobantes-recibidos-afip
11. ARCA, catálogo de web services: https://www.arca.gob.ar/ws/documentacion/catalogo.asp
12. ARCA, manual del desarrollador WSCDC v0.4 (01/12/2025): https://www.afip.gob.ar/ws/WSCDCV1/WSCDC-manual-desarrollador-v4.pdf
13. ARCA, especificaciones del QR: https://www.afip.gob.ar/fe/qr/documentos/QRespecificaciones.pdf · RG 4892/2020: https://biblioteca.afip.gob.ar/dcp/REAG01004892_2020_12_22
14. ARCA, WSAA y certificados: https://arca.gob.ar/ws/documentacion/wsaa.asp · https://www.arca.gob.ar/ws/programadores/certificados-digitales.asp · https://arca.gob.ar/ws/documentacion/certificados.asp · YoFacturo, delegación: https://yo-facturo.com/dev/arca/webservice-afip-sin-certificado/
15. ARCA, manuales de web services de factura electrónica: https://www.arca.gob.ar/fe/ayuda/webservice.asp
16. Cronista, IVA Simple (03/06/2025): https://www.cronista.com/economia-politica/iva-simple-el-gobierno-lo-festeja-pero-las-grandes-empresas-deberan-mirar-con-lupa
17. iProfesional, preguntas frecuentes sobre IVA Simple (18/09/2025): https://www.iprofesional.com/impuestos/437665-respuestas-arca-iva-simple-web-preguntas-frecuentes
18. YoFacturo, comprobantes recibidos: https://yo-facturo.com/docs/accounting/received-invoices/
19. Thomson Reuters y CPCECABA, "IA en los estudios contables en Argentina 2025": https://www.thomsonreuters.com.ar/content/dam/ewp-m/documents/argentina/es/pdf/white-papers/informe-inteligencia-artificial-en-la-contabilidad-en-argentina-2025.pdf
20. PortalContador: https://portalcontador.com.ar/
21. FacturAI: https://facturai.com.ar/
22. Norte en Línea, sobre Xtract (26/10/2026): https://norteenlinea.com/en-contabilidad-casi-bien-es-mal-la-startup-argentina-que-le-enseno-a-leer-facturas-a-arcos-dorados-y-modo-sin-depender-de-openai-o-antropic/
23. Sourced, carga de facturas en Tango: https://www.gosourced.ai/es/tango-gestion-carga-de-facturas
24. CargaFacturas: https://cargafacturas.com/ar
25. XPyME: https://xpyme.com.ar/automatiza-la-gestion-de-facturas-de-compra-con-ia
26. Otros vistos solo en extractos de búsqueda: Nexosmart https://www.nexosmart.com.ar/soluciones/procesamiento-facturas-ocr-ia/ · NetOne https://netone.com.ar/automatizacion-de-facturas-con-ia-ocr-netone--news--7-1106 · FORJA https://forja.tech/ · CONTADOR-IA https://contador-ia.com/ · Contapilot https://contapilot.com.ar/ · Clara https://www.iproup.com/startups/72595-fintech-que-usa-ia-y-whatsapp-para-controlar-gastos-llega-a-argentina · Apideck/Alegra https://developers.apideck.com/apis/accounting/alegra/configuration · Holistor (2009) https://guia.ispcube.com/wp-content/uploads/2017/05/IVAImportaciondatosExcel-HOLISTOR.pdf · Nubox https://blog.nubox.com/contadores/haz-que-tu-contabilidad-vuele-con-lo-nuevo-de-nubox · Tango GitHub https://github.com/TangoSoftware/ApiClientes
27. El Economista, importaciones récord con datos de CEPA (2026): https://eleconomista.com.ar/economia/importaciones-record-argentina-cuales-son-productos-extranjeros-mas-crecieron-ganaron-mercado-n97464
28. Derecho en Zapatillas, comprobantes junto con las expensas (01/08/2024): https://www.derechoenzapatillas.com/2024/los-administradores-de-consorcios-deberan-mandar-a-partir-de-hoy-los-comprobantes-de-los-gastos-junto-con-las-expensas/
29. CONSO en Capterra: https://www.capterra.es/software/1111352/CONSO
30. AWS Textract, precios: https://aws.amazon.com/textract/pricing/
31. ERP Research, precios de Azure Document Intelligence 2026: https://erpresearch.com/erp-add-ons/ocr/azure-document-intelligence/pricing · Oficial (precios no visibles): https://azure.microsoft.com/en-us/pricing/details/ai-document-intelligence/
32. Mindee, precios: https://www.mindee.com/pricing
33. Nanonets, precios: https://nanonets.com/pricing
34. Gemini API, precios (act. 28/10/2026): https://ai.google.dev/gemini-api/docs/pricing
35. Gemini API, procesamiento de documentos (258 tokens por página): https://ai.google.dev/gemini-api/docs/document-processing
36. Cronista, elecciones en el CPCECABA (09/06/2022): https://www.cronista.com/informacion-gral/gabriela-russo-fue-reelecta-como-presidenta-del-consejo-profesional-de-ciencias-economicas
37. DolarHoy, datos de la SRT (mayo 2026, publicado en agosto 2026): https://dolarhoy.com/economia/sector-privado-sufre-caida-del-3-3-en-empresas-empleadoras-y-acumula-27-meses-de-retroceso-2026818105952
38. BCR, sobre cartas de porte: https://bichosdecampo.com/se-usan-casi-21-millones-de-hojas-de-papel-para-imprimir-las-cartas-de-porte-la-bolsa-de-rosario-sugiere-pasar-a-digital
- Informe base, Document AI USD 0,10 por documento: referencia [32] del PDF "Negocios digitales con APIs".
