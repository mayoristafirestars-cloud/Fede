# Oportunidad 2: voz entrante con IA en Argentina y LatAm

Investigación de mercado para Federico. Fuentes consultadas entre el 29 y el 30 de octubre de 2026.

**Cómo leer las marcas**

- **[V]**: dato verificado en la fuente citada.
- **[E]**: estimación propia hecha con datos verificados. Se muestra el cálculo.
- **[NV]**: conocimiento previo que no se verificó con una fuente en esta investigación. Hay que confirmarlo.
- **[NE]**: no se encontró información.

**Límite de esta investigación**: se agotó el cupo de búsquedas web antes de cubrir algunos puntos (Plivo y números, proveedores locales como Neotel u Ominira, precios de Cliengo). Esos huecos están marcados.

---

## 1. Resumen ejecutivo

1. **Se pueden conseguir números argentinos por API, con requisitos de documentación.** Twilio publica USD 8 por mes por un número local y USD 0,0107 por minuto entrante. Para un número local pide registro comercial y un domicilio dentro del área del prefijo. Telnyx vende números locales argentinos. Plivo indica que en Argentina **no admite llamadas entrantes**. Vonage no ofrece autoservicio para Argentina. [V] [1][2][3][6][9]
2. **El costo de uso entra en los USD 0,20 por minuto del PDF si se elige bien la combinación.** Con Vapi o Retell, un LLM barato, una voz estándar y Twilio como telefonía argentina, el uso cuesta entre **USD 0,09 y 0,14 por minuto** [E]. El supuesto se rompe con voces premium o con el speech-to-speech completo de OpenAI, de USD 0,23 a 0,45 por minuto [E]. También se rompe si se **transfiere la llamada a un celular**: Twilio cobra USD 0,3528 por minuto saliente a móviles argentinos [V][1].
3. **El mayor riesgo es de demanda, no técnico.** Los argentinos usan WhatsApp de forma masiva. No se encontró una encuesta argentina sólida sobre canal preferido. En Uruguay, en 2026, WhatsApp (42%) superó al teléfono (33%) como canal preferido para contactar empresas [V][20]. Meta lanzó en febrero de 2026 "Business AI", con agentes de texto en WhatsApp Business, y Argentina fue de los primeros países [V][18].
4. **Ya hay competencia local.** Botmaker, empresa argentina, vende "Callbots" de voz con IA desde USD 149 por mes [V][16]. Darwin AI, Aivo y otros incluyen voz en sus ofertas [V][22][23].
5. **El marco legal es manejable pero tiene puntos concretos.** La Res. SCI 1033/2021 prohíbe usar IA como medio *exclusivo* de atención y exige una opción humana, pero **exceptúa a las MiPyMEs** [V][28]. Grabar una llamada es tratar datos personales bajo la Ley 25.326 [V][31]. No se encontró una norma vigente que obligue a avisar que quien atiende es una IA [V][33], aunque conviene hacerlo igual.

---

## 2. Telefonía en Argentina

### 2.1 Proveedores con API

| Proveedor | Número local argentino | Precio del número | Minuto entrante | Requisitos | Fuente |
|---|---|---|---|---|---|
| **Twilio** | Sí (local y 0800 +54800) | Local USD 8/mes; toll-free USD 25/mes [V] | Local USD 0,0107; toll-free USD 0,2582; SIP/BYOC USD 0,0040 [V] | Local: registro comercial y número de registro, domicilio dentro del área del prefijo (no sirve casilla postal). 0800: domicilio en Argentina [V] | [1][2] |
| **Twilio (salientes y transferencias)** | n/a | n/a | Saliente a fijo USD 0,0604; **a móvil USD 0,3528** [V] | Twilio no permite llamadas a emergencias 911/933 [V] | [1][3] |
| **Telnyx** | Sí (locales). Inventario por área a confirmar en el portal | **Contradictorio**: una página dice "desde USD 1/mes" y otra "desde USD 6,75/mes" [V] | No se publica la tarifa argentina [NE]. Tarifa genérica de plataforma: USD 0,002/min más trunking [V] | Local: identidad (DNI o pasaporte, o constancia de inscripción societaria) y una dirección (sirve cualquier país) [V]. Menos exigente que Twilio | [4][5][6] |
| **Vonage** | Figura como país soportado | No publicado [NE] | No publicado [NE] | **Sin compra autoservicio para Argentina**: se pide por formulario o al gerente de cuenta, con revisión previa [V] | [7] |
| **Plivo** | No se pudo confirmar la venta de números [NE] | [NE] | **"Not Supported"** para entrantes locales, móviles y SIP en Argentina [V] | Solo publica salientes: fijo desde USD 0,016, móvil USD 0,303 [V] | [8] |
| **SignalWire** | No figura (la página solo muestra EE. UU. y Canadá) [V] | [NE] | [NE] | Agente IA a USD 0,16/min sin transporte [V] | [9] |
| **Revendedores de DID** (VoIPstudio, UnityVox, TollFreeForwarding) | Buenos Aires (11) | USD 13 a 16,21/mes, algunos con alta igual al abono [V, vía resumen de buscador] | [NE] | No se verificaron | [10] |
| **Genesys Cloud** (referencia) | Sí, para empresas con domicilio argentino | n/a | n/a | Para empresas extranjeras: sin salientes y con problemas de alcance desde Buenos Aires. Genesys afirma que "no hay portabilidad en Argentina" [V], lo que contradice la portabilidad fija vigente (ver 2.3) | [11] |

### 2.2 Proveedores locales (troncal SIP para conectar a Vapi o Retell)

| Proveedor | Qué ofrece | Precio | Fuente |
|---|---|---|---|
| **Anura** | Troncal IP (SIP, G.729), base de 10 canales. Numeración nueva **geográfica** (011, 0351, 0341, Mendoza, etc.) o **0800/0810**, contratable sin su central virtual. Hace la **portabilidad sin costo**, también de 0800/0810. Incluye API y webhooks, y grabaciones sin cargo extra [V] | No publica precios: hay que cotizar al 0800 220 0000 [V] | [12][13] |
| **IPLAN** | VoIP con troncal SIP y numeración pública. Variantes de 5/10, 15/50, 30/100 y 60/200 (llamadas simultáneas / números). El documento es de 2020, puede estar desactualizado [V] | [NE] | [14] |
| **Telecentro Empresas, Neotel, Ominira** | No se investigaron por falta de cupo de búsqueda [NE] | [NE] | n/a |

**Conclusión práctica [E]**: para un piloto, lo más rápido es **Twilio** (precio publicado e integración nativa con Vapi y Retell) o **Telnyx** (requisitos más laxos). Para clientes que ya tienen un número conocido, la vía es **portar ese número a un proveedor local con troncal SIP** (Anura, IPLAN) y conectarlo por SIP a la plataforma de IA. La alternativa más simple es que el cliente **desvíe sus llamadas** a un número nuevo. El desvío desde un celular tiene costos de la operadora móvil que no se investigaron [NE].

### 2.3 Regulación ENACOM y portabilidad

- **Portabilidad fija**: vigente desde el 21 o 22 de octubre de 2022, con un plazo máximo de 5 días. Se basa en las Res. 203 y 401 MM/2018 y la Res. 4950 ENACOM/2018 [V][15]. Anura confirma que porta números geográficos, 0800 y 0810 [V][12].
- **Numeración**: ENACOM no asigna números a usuarios finales. Los asigna a **prestadores TIC registrados**, en bloques de 10.000 números para 0800/0810 [V][15b]. Estar inscripto en el registro TIC (Res. 2483/2016, con 30 días sin observaciones) no garantiza obtener numeración [V][15b]. Una resolución de 2023 advierte **saturación de numeración geográfica** en varios indicativos [V][15b].
- **Implicancia**: Federico **no necesita ni le conviene** ser prestador TIC. Debe alquilar los números a un proveedor habilitado, a nombre del cliente o propio. Si revende telefonía (y no solo un servicio de software), conviene consultar con un abogado si eso lo convierte en prestador [NV].

### 2.4 WhatsApp Business Calling API como alternativa

| Punto | Dato | Fuente |
|---|---|---|
| Llamadas **iniciadas por el usuario** | **Gratis** para la empresa ("All user-initiated calls are free"). Página actualizada en 2026 [V] | [17] |
| Disponibilidad | Las llamadas iniciadas por el usuario funcionan en todos los países con Cloud API. Las iniciadas por la empresa, en todos salvo EE. UU., Canadá, Egipto, Vietnam y Nigeria. **Argentina queda incluida** [V] | [16b] |
| Requisitos | El número debe estar en **Cloud API**, no en la app WhatsApp Business. Hace falta un **límite de mensajería de al menos 2.000 destinatarios únicos por día** y activar la función de llamadas en el número [V] | [16b] |
| SIP | Admite SIP (TLS con WebRTC o SDES SRTP) y los códecs OPUS y G.711. **Se puede conectar técnicamente a Vapi, Retell o LiveKit** [V] | [16b] |
| Llamadas de la empresa al usuario | Se cobran por pulsos de 6 segundos según país y volumen. Desde el 1/4/2026 hay facturación en ARS. La tarifa argentina por minuto no apareció en el texto de la página [V]/[NE] | [17] |
| Ventana de mensajes | Una llamada del usuario, atendida o no, abre o renueva la ventana de atención de 24 horas [V] | [17] |
| Ofertas existentes | Botmaker anunció Callbots con alianza con Meta, desde USD 149 [V] | [16] |

**Lectura [E]**: WhatsApp Calling **elimina el costo de telefonía y del número** para llamadas entrantes. Encaja con la cultura WhatsApp argentina. Tiene dos límites:

- El requisito de 2.000 destinatarios por día deja afuera a muchas pymes chicas recién llegadas a la API.
- La empresa tiene que migrar su número a Cloud API.

Es un **canal complementario**, no un reemplazo del número telefónico. Antes de prometerlo hay que verificar si la app y la API pueden convivir en el mismo número [NV].

---

## 3. Plataformas de voz IA: precios, español rioplatense y latencia

### 3.1 Precios publicados (USD)

| Plataforma | Cargo propio | Componentes y notas | Fuente |
|---|---|---|---|
| **Vapi** | Hosting USD 0,05/min. Plan Core USD 29/mes (10 llamadas simultáneas, 5 números). Pro desde USD 999/mes [V] | Ejemplo propio: STT Deepgram 0,0095–0,0099; LLM 0,0077–0,0452; TTS ElevenLabs 0,0146–0,0238. Total **0,082–0,129/min** sin telefonía [V] | [19] |
| **Retell** | Voice infra USD 0,055/min. 20 llamadas simultáneas gratis, luego USD 8 por línea al mes [V] | LLM: GPT‑5 mini 0,008; GPT‑5.4 mini 0,024; Gemini 3.0 Flash 0,016; Claude 4.5 Haiku 0,025. TTS estándar 0,015; ElevenLabs 0,04–0,10. Base de conocimiento +0,005. Telefonía propia por SIP sin cargo [V]. **Argentina no está soportada en su telefonía administrada para salientes**: hace falta un troncal SIP propio (fuente: foro de la comunidad, no documentación oficial) [V] | [21][21b] |
| **ElevenLabs Agents** | USD 0,08 por minuto adicional; ráfagas USD 0,16 [V] | El LLM se cobra aparte en Realtime. Hay un caso de demostración "Che Voz" con acentos de Buenos Aires, Córdoba y Mendoza (vitrina del proveedor) [V] | [24][26] |
| **OpenAI Realtime** | gpt-realtime-2.1: audio de entrada USD 32 y de salida USD 64 por millón de tokens. Versión mini: USD 10 / 20 [V] | Una fuente secundaria estima **USD 0,30–0,45/min** para el modelo completo [V, estimación de terceros]. Transcripción: gpt‑4o‑mini‑transcribe USD 0,003/min [V] | [25][25b] |
| **Deepgram** | Voice Agent API estándar USD 0,075/min. Usando LLM y TTS propios, USD 0,050 [V] | STT Nova‑3 multilingüe USD 0,0092/min; monolingüe USD 0,0077/min [V] | [27] |
| **Bland** | Plan Start USD 0,14/min. Plan Build USD 0,12/min más USD 299/mes. Transferencia USD 0,04–0,05/min [V] | Telefonía aparte. Acepta Twilio o SIP propios [V] | [29] |
| **Synthflow** | Solo contrato anual empresarial, sin precio público [V] | Marca blanca dentro del contrato empresarial [V] | [30] |
| **Telnyx AI** | Voice engine USD 0,05/min (incluye STT y TTS). "Realista" alrededor de USD 0,06/min [V] | Redondea a 60 segundos por llamada. No menciona Argentina ni español [V] | [32] |
| **SignalWire AI** | USD 0,16/min; total de USD 0,163 a 0,168 [V] | No figura Argentina [V] | [9] |

### 3.2 Español rioplatense

- No se encontraron **evaluaciones independientes** de voseo, sheísmo o entonación porteña en ElevenLabs, Cartesia u otros motores [V: ausencia][26].
- Hay demostraciones y anuncios del propio proveedor: "Che Voz" en ElevenLabs y voces es‑AR de terceros [V][26]. Aivo afirma entender "modismos y regionalismos" (material promocional) [V][23].
- **Recomendación [E]**: armar un banco de prueba de 30 a 50 frases reales (direcciones porteñas, nombres de calles, patentes, "dale", "che", números de teléfono dictados) y medir la tasa de error del STT y la naturalidad con evaluadores argentinos. El PDF ya pide medir "errores de agenda y acento".

### 3.3 Latencia

- No hay un benchmark independiente que compare a todos con el mismo método [V][34].
- Un estudio de marzo de 2026 con 500 llamadas por plataforma ubica a **Retell con la menor mediana**, alrededor de 600–620 ms de punta a punta. Las cifras de Vapi (menos de 500 ms) son del propio proveedor [V, vía resumen][34]. Una regla práctica citada sitúa en unos 700 ms el punto en que el usuario empieza a notar la demora [V][34].
- **Riesgo para Argentina [E]**: los servidores de estas plataformas suelen estar en EE. UU. Con un número argentino, el audio cruza el continente y puede sumar latencia. Hay que medirlo en el piloto. No se encontraron datos específicos [NE].

---

## 4. Competidores en Argentina y LatAm

| Empresa | Origen | Oferta de voz | Precio publicado | Fuente |
|---|---|---|---|---|
| **Botmaker** | Argentina | "Callbots" de IA generativa: pedidos, ventas, preguntas frecuentes y derivación humana. Menú numérico y horario. Alianza con Meta (agosto de 2025) | Callbots **desde USD 149**. Planes de chat: USD 149 (3.000 conversaciones), 249 y 499 por mes. Alta de WhatsApp USD 99 [V] | [16][16c] |
| **Aivo** | Argentina (2012) | AgentBot con canal de voz telefónico 24/7. Clientes grandes (BBVA, Movistar, etc., según directorio de terceros) | [NE] | [23] |
| **Darwin AI** | Brasil (São Paulo, 2023). Reportada también como "startup argentina" | Agentes para pymes de LatAm en WhatsApp, Instagram y **llamadas**. Seed de USD 4,5 M (Base10, 2025). Más de USD 2 M de ingresos brutos anuales, según la propia empresa | [NE] | [22] |
| **Cliengo** | Argentina | Fuerte en chat y WhatsApp para inmobiliarias. No se encontró un producto de voz [NE] | [NE] | [35] |
| **Meta Business AI** | Global | Agentes de **texto** gratuitos o integrados en WhatsApp Business App (febrero de 2026, Argentina entre los primeros). No incluye voz [V] | No informado | [18] |
| **Yalo, Leadsales** | LatAm | No se investigaron por falta de cupo [NE] | [NE] | n/a |
| Referencias globales | CloudTalk desde €99 por 100 minutos; Aircall €0,99/min por el complemento de IA [V, resumen de buscador] | n/a | n/a | [36] |

**Lectura [E]**: la oferta local de voz con IA apunta a **empresas medianas y grandes** (Aivo) o se vende como **añadido de plataformas de chat** (Botmaker, Darwin). No se encontró un producto argentino de "recepcionista IA" vertical, con precio publicado, para oficios u hogar. Eso es un hueco posible, pero también puede indicar poca demanda.

---

## 5. Nichos y hábitos de canal

### 5.1 ¿El argentino llama o escribe?

| Dato | Alcance | Calidad | Fuente |
|---|---|---|---|
| El 99% de los encuestados argentinos usa WhatsApp; el 71% lo usa para comprar | Accenture con Facebook, 2020. Sin muestra publicada | Antiguo, sin metodología [V] | [37] |
| "8 de cada 10 argentinos prefieren WhatsApp" frente al teléfono, el email o los chatbots | Cronista, 2026 | **Sin estudio de origen identificado** [V: cita sin fuente] | [18] |
| WhatsApp 79%, Instagram 10%, **teléfono 6%**, email 4% | Treble.ai, más de 150 encuestas. País no aclarado | Muestra chica [V] | [38] |
| Uruguay 2026: canal preferido para contactar empresas, **WhatsApp 42%** (desde 4% en 2025) frente a **teléfono 33%** (desde 42%) | Opción Consultores para DavinciBot, 400 casos, marzo a mayo de 2026 | Sólido, pero **no es Argentina**. El salto de 4% a 42% es llamativo [V] | [20] |
| "El 80% de las consultas inmobiliarias en LatAm empiezan en WhatsApp" | Cliengo | Afirmación de un proveedor, sin fuente [V] | [35] |
| Datos de llamadas perdidas por pymes argentinas | n/a | **[NE]**. Solo hay datos de Reino Unido o España, de proveedores interesados | [39] |

**Conclusión [E]**: el teléfono sigue usándose (un tercio en Uruguay), pero en el Río de la Plata **WhatsApp es el canal dominante**. Un producto solo de voz ataca la porción menor de las consultas. La propuesta debería ser **"atendemos tu teléfono y tu WhatsApp con el mismo agente"**, o bien concentrarse en nichos donde la gente **sí llama**.

### 5.2 Nichos (hipótesis a validar en entrevistas)

| Nicho | Por qué una llamada perdida cuesta plata | Señal de que se llama | Riesgo |
|---|---|---|---|
| **Urgencias del hogar** (cerrajería, plomería, gas, destapaciones, electricistas) | La urgencia hace que el cliente llame al siguiente de la lista | En una emergencia se llama más que se escribe [E, sin dato AR] | El PDF excluye emergencias. Hay que fijar límites: **el gas es riesgo de vida**. Se toma el pedido y se deriva, sin diagnosticar |
| **Aire acondicionado** (instalación y service) | Picos estacionales con saturación de llamados en verano | [NE] | Estacionalidad del abono |
| **Inmobiliarias** | Cada consulta es un posible alquiler o venta. Los portales muestran teléfono | Cliengo dice que los portales empujan al teléfono pero el usuario prefiere chatear [V][35] | Competencia de Cliengo y Argenprop (CRM gratis) [V][40] |
| **Talleres mecánicos** | Turnos y presupuestos. La recepción se satura | Un proveedor afirma que el cliente prefiere WhatsApp [V, vendedor][41] | Ticket bajo |
| **Estudios jurídicos** | Admisión de casos (laboral, accidentes) | [NE] | Secreto profesional y datos sensibles |
| **Gimnasios, peluquerías y estética** | Turnos | Muy volcados a WhatsApp e Instagram [E] | Bajo valor por llamada. Mejor con chat |
| **Colegios** | Inscripciones con picos estacionales | [NE] | Datos de menores |

**Ranking tentativo [E]**: 1) urgencias del hogar y aire acondicionado, por **valor alto por llamada y fuera de horario**; 2) inmobiliarias, por **valor alto, aunque la competencia es de chat**; 3) talleres. Peluquerías y gimnasios quedan descartados para voz.

---

## 6. Marco legal argentino

| Tema | Situación | Fuente |
|---|---|---|
| **Res. SCI 1033/2021** (parámetros de atención a distancia, basada en el art. 8 bis de la Ley 24.240) | Derecho a ser atendido por una **persona humana**. **Prohíbe la IA, los bots o las grabaciones como medio *exclusivo***. En el primer nivel del menú debe haber una opción humana, con un máximo de 5 opciones. Espera de hasta 5 minutos. **Exceptúa a micro, pequeñas y medianas empresas** [V]. Vigente desde el 3/8/2022 (Res. 425/2022) [V]. No se confirmó si fue modificada en 2024–2026 [NE] | [28][28b] |
| **Ley 25.326** (datos personales) | La voz grabada y los datos del llamante son datos personales. La AAIP exige, para videollamadas grabadas, **informar antes, de forma explícita, la grabación y su finalidad** (aplicable por analogía) [V]. No hay un criterio específico de la AAIP para llamadas telefónicas [NE] | [31] |
| Transferencia internacional (servidores en EE. UU.) | El art. 12 de la Ley 25.326 restringe las transferencias a países sin protección adecuada. Suelen usarse cláusulas contractuales modelo de la AAIP. Registro de bases de datos ante la AAIP [NV] | Verificar con abogado |
| **Reforma de la Ley 25.326** | Exp. 3397‑D‑2026 (16/7/2026), que reproduce el proyecto del Ejecutivo de 2023 y derogaría las leyes 25.326 y 26.343. Otros proyectos parciales (4669‑D‑2026). **Sin tratamiento confirmado** [V] | [33b] |
| **Aviso de que atiende una IA** | **No hay una norma nacional vigente** que lo exija. Hay más de 10 proyectos de ley de IA en Diputados. En PBA hay una norma solo para el sector público [V]. En la UE, el art. 50 del AI Act rige desde el 2/8/2026 [V] | [33] |
| **Registro No Llame (Ley 26.951)** | Rige para contactos de **publicidad y venta** por teléfono. No afecta las llamadas entrantes. Excepción para quien tiene contrato vigente con el llamado, sobre ese objeto [V] | [42] |
| Ley 24.240 (trato digno, información) | Rige en general. El agente **no debe prometer** precios vinculantes ni plazos. Coincide con el PDF [E] | [28] |
| Impuestos sobre servicios digitales del exterior | IVA del 21% sobre servicios digitales (Ley 27.430) y percepciones sobre pagos con tarjeta en dólares. Hay que verificar el régimen vigente con un contador [NV] | n/a |

**Guion mínimo recomendado [E]**: "Hola, te atiende el asistente virtual de [empresa]. La llamada se graba para [finalidad]. Si preferís hablar con una persona, decí 'persona'". Además: una ruta humana real, política de borrado y un contrato de encargado de tratamiento con el cliente.

---

## 7. Costo por minuto completo en Argentina frente al PDF

Supuestos [E]:

- Llamada entrante a un número local de Twilio (USD 0,0107/min [1]).
- Precios publicados de cada plataforma.
- Sin impuestos argentinos.
- 1.000 minutos por cliente al mes, como en el PDF.

| Combinación | Plataforma | STT | LLM | TTS | Telefonía AR | **USD/min** | 1.000 min + número USD 8 (+ plan) |
|---|---|---|---|---|---|---|---|
| A‑bajo: Vapi, Deepgram, LLM barato y ElevenLabs Flash | 0,05 | 0,0077 | 0,0077 | 0,0146 | 0,0107 | **0,091** | ~USD 99 |
| A‑alto: Vapi con LLM mediano | 0,05 | 0,0092 | 0,0452 | 0,0238 | 0,0107 | **0,139** | ~USD 176 (con Core USD 29) |
| B‑bajo: Retell, Gemini 3.0 Flash y voz estándar | 0,055 | incl. | 0,016 | 0,015 | 0,0107 | **0,097** | ~USD 105 |
| B‑alto: Retell, GPT‑5.4 mini, ElevenLabs Flash y base de conocimiento | 0,055 | incl. | 0,024 | 0,040 | 0,0107 | **0,135** | ~USD 143 |
| B‑premium: Retell, GPT‑5.4, ElevenLabs v3 y base de conocimiento | 0,055 | incl. | 0,080 | 0,080 | 0,0107 | **0,231** | ~USD 239 |
| C: Deepgram Voice Agent estándar | 0,075 (todo) | | | | 0,0107 | **0,086** | ~USD 94 |
| D: OpenAI gpt‑realtime completo | estimación de terceros: 0,30–0,45 | | | | 0,0107 | **0,31–0,46** | USD 319–469 |
| E: SignalWire o Bland (si operan con números argentinos) | 0,12–0,168 | | | | 0,0107 | **0,13–0,18** | USD 140–190 |

**Costos que el PDF no considera [E]**:

- **Transferencia a un celular**: si el 10% de los minutos se deriva en vivo al celular del dueño, son 100 min × USD 0,3528 = **USD 35 más por mes** [1]. Es mejor transferir a un softphone o SIP (USD 0,004/min) o reemplazar la transferencia por una **devolución de llamada con resumen por WhatsApp**.
- **Minutos de entrada al 0800**: USD 0,2582/min [1]. Con un 0800, el costo de telefonía se multiplica por 24. Para este negocio conviene evitar el 0800 y usar números geográficos.
- Redondeo por llamada (Telnyx AI redondea a 60 segundos [32]), complementos de Retell (+0,005 a +0,01), control de calidad (USD 0,10/min después de los primeros 100 minutos en Retell [21]).
- Para minutos contados de punta a punta, IVA y percepciones argentinas [NV].

**Comparación con el PDF (USD 0,20/min más USD 15 fijos = USD 215 de costo técnico)**:

- Las combinaciones A, B‑bajo/alto y C quedan en **USD 95–180**. El supuesto del PDF es **conservador y razonable** [E].
- La sensibilidad del PDF de USD 0,35/min ocurre en la práctica con: speech-to-speech completo de OpenAI, voces premium más LLM grande, o muchas transferencias a celulares o entradas por 0800 [E].
- Con un costo de **USD 0,12/min**, la contribución del escenario del PDF subiría unos USD 80 por cliente, de USD 112 a alrededor de USD 192 [E: 215 − (120 + 15) = 80].

**Precio de venta frente al mercado local [E]**: el PDF propone un abono de USD 399 por 1.000 minutos (banda de USD 249 a 599). El competidor local más visible (Botmaker Callbots) **parte de USD 149** [16]. Para un cerrajero o un taller argentino, USD 399 por mes es mucho dinero. No se encontraron datos sobre su disposición a pagar [NE]. Probablemente haga falta un plan de entrada de **USD 99 a 199 con 300 a 500 minutos**, y reservar USD 399 o más para inmobiliarias o empresas con varias sucursales. Es una hipótesis que hay que validar en entrevistas.

---

## 8. Implicancias y recomendación para Federico

1. **La tecnología y el costo no son la traba.** Hay números locales por API (Twilio o Telnyx), portabilidad mediante proveedores locales, y un costo de uso de USD 0,09 a 0,14 por minuto, por debajo del supuesto del PDF. Eso vale con dos reglas de diseño: **no usar 0800** y **no transferir en vivo a celulares**.
2. **El riesgo real es de demanda y de canal.** En Argentina se escribe más de lo que se llama, y Meta ya regala agentes de texto en WhatsApp. **No conviene vender "recepcionista telefónica" sola.** Conviene vender **"no perdés ningún pedido fuera de horario, ni por teléfono ni por WhatsApp"**, con voz para el teléfono y el mismo cerebro para el chat. WhatsApp Calling (gratis para llamadas entrantes, con SIP) es la extensión natural cuando el cliente alcance el nivel de 2.000 destinatarios.
3. **Nicho sugerido para el piloto**: **urgencias del hogar y servicio técnico** (cerrajería, plomería, aire acondicionado, electricidad) en CABA y AMBA. Atender fuera de horario: tomar dirección, problema y franja horaria, y devolver un **resumen por WhatsApp** al técnico. Sin diagnósticos ni precios, y con un protocolo de "si huele a gas, llamá a la distribuidora" que remita al número oficial de emergencias. Segunda opción: **inmobiliarias** (atención de consultas desde portales).
4. **Pila técnica sugerida para el piloto**: Retell o Vapi con un número de Twilio Argentina (o Telnyx si Twilio pone trabas con la documentación), un LLM chico (Gemini Flash o GPT‑5.4 mini) y un TTS con buena prueba en rioplatense. Hay que medir latencia real desde Argentina y el error de STT en direcciones. Antes de ofrecer marca blanca, conviene revisar los términos de reventa de Vapi y Retell, que el PDF ya señala. Implementar en una **cuenta del cliente** reduce ese riesgo.
5. **Precio**: probar un plan de entrada de USD 99 a 199 frente al de USD 399, porque la referencia local es Botmaker desde USD 149. Cobrar la puesta en marcha aparte. Fijar un tope de minutos y un precio de excedente (por ejemplo, USD 0,25 a 0,30 por minuto) [E].
6. **Legal**: incluir un aviso de IA y de grabación al inicio, una opción humana, contrato de encargado de tratamiento y cláusulas para la transferencia internacional [NV]. Antes de vender a clientes grandes, hay que confirmar con un abogado la vigencia de la Res. 1033/2021, que exceptúa a las pymes.
7. **Pendiente de verificar** (no cubierto por falta de cupo de búsqueda):
   - tarifa argentina de Telnyx por minuto;
   - precios de Anura, IPLAN y Telecentro;
   - costo del desvío de llamadas en Personal, Claro y Movistar;
   - tarifa de WhatsApp Calling para llamadas de la empresa en Argentina (tabla en ARS);
   - precios de Aivo, Darwin, Cliengo, Yalo y Leadsales;
   - dato argentino de preferencia de canal y de llamadas perdidas por rubro.

---

## Fuentes (consultadas el 29 y 30 de octubre de 2026)

1. Twilio, Voice pricing Argentina (tabla de agosto de 2026): https://www.twilio.com/en-us/voice/pricing/ar
2. Twilio, Argentina regulatory guidelines: https://www.twilio.com/en-us/guidelines/ar/regulatory
3. Twilio, Argentina voice guidelines: https://www.twilio.com/en-us/guidelines/ar/voice
4. Telnyx, Argentina phone numbers (versión .md, "desde USD 6,75/mes"): https://telnyx.com/phone-numbers/argentina.md
5. Telnyx, Argentina DID requirements: https://support.telnyx.com/en/articles/3760805-argentina-did-requirements
6. Telnyx, números y precios ("desde USD 1/mes", resumen de buscador): https://telnyx.com/phone-numbers/argentina ; https://telnyx.com/pricing/numbers ; https://telnyx.com/pricing/voice-api
7. Vonage, Argentina Voice Features and Restrictions (vía resumen de buscador; la página dio 403): https://api.support.vonage.com/hc/en-us/articles/234653127-Argentina-Voice-Features-and-Restrictions
8. Plivo, Voice pricing Argentina (calculadora de mayo de 2026): https://www.plivo.com/voice/pricing/ar/
9. SignalWire, Voice pricing: https://signalwire.com/pricing/voice
10. Revendedores de DID (resumen de buscador): https://voipstudio.com/telephone-numbers/Argentina/usd ; https://unityvox.com/en/did-numbers-from-argentina/AR ; https://tollfreeforwarding.com/virtual-phone-number/argentina/
11. Genesys Cloud, Voice requirements Argentina: https://help.genesys.cloud/?p=263217
12. Anura, Troncal IP: https://www.anura.com.ar/soluciones/troncal-ip/
13. Anura, Precios: https://www.anura.com.ar/precios/
14. IPLAN, Descripción y alcance del servicio VoIP extendido: https://iplan.com.ar/sites/default/files/documentos/voip-descripcion_y_alcance_del_servicio_voip_extendido.pdf
15. Portabilidad fija: https://www.telesemana.com/blog/2022/11/25/hito-historico-llego-la-portabilidad-numerica-en-telefonia-fija-a-argentina/ ; https://telxp.cabase.org.ar/files/presentacion-enacom-portabilidad-fijos.pdf
15b. ENACOM, numeración y registro TIC: https://www.boletinoficial.gob.ar/detalleAviso/primera/296594/20231023?anexos=1 ; https://telxp.cabase.org.ar/notas/files/RESOL-2023-1369.pdf ; https://www.marval.com/Publicacion/registro-de-servicios-tic-para-la-prestacion-de-servicios-de-valor-agregado--acceso-a-internet-13111
16. DEF Online, Botmaker Callbots (22/8/2025): https://defonline.com.ar/ciencia-tecnologia/inteligencia-artificial-una-empresa-con-ingenieria-argentina-suma-agentes-de-ia-para-llamadas/
16b. Meta, WhatsApp Cloud API Calling: https://developers.facebook.com/docs/whatsapp/cloud-api/calling/
16c. Botmaker, Precios: https://botmaker.com/es/precios/
17. Meta, Calling API pricing (tarifas vigentes desde el 1/4/2026): https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/pricing/
18. El Cronista, Business AI en WhatsApp (febrero de 2026): https://www.cronista.com/infotechnology/it-business/asi-funciona-la-novedad-de-whatsapp-que-usan-las-pymes-para-vender-mas-sin-sumar-personal/
19. Vapi, Pricing: https://vapi.ai/pricing
20. El Observador (Uruguay), 23/7/2026, Observatorio de Conversación Digital 2026: https://www.elobservador.com.uy/ciencia-y-tecnologia/whatsapp-desplazo-al-telefono-como-el-canal-que-prefieren-los-uruguayos-hablar-empresas-n6051805
21. Retell AI, Pricing: https://www.retellai.com/pricing
21b. Retell Community, Argentina outbound: https://community.retellai.com/t/enable-outbound-calling-to-argentina-54-account-whitelist-request/2422
22. Darwin AI: https://latamlist.com/darwin-ai-raises-4-5m-seed-round-led-by-base10-partners/ ; https://www.itsitio.com/ar/inteligencia-artificial/startup-argentina-que-crea-trabajadores-de-ia-levanta-una-ronda-de-45-millones-de-dolares-en-silicon-valley/
23. Aivo (directorios y prensa): https://justcall.io/ai-agent-directory/aivo/ ; https://tiinside.com.br/en/21/03/2018/aivo-launches-AI-powered-voice-service-solution/
24. ElevenLabs, API pricing: https://elevenlabs.io/pricing/api
25. OpenAI, API pricing: https://developers.openai.com/api/docs/pricing
25b. Estimación de terceros por minuto para gpt-realtime-2: https://vantaige.io/blog/openai-gpt-realtime-2-voice-agent-setup-2026
26. Español rioplatense: https://showcase.elevenlabs.io/projects/p/che-voz ; https://speechgen.io/es/tts-spanish-argentina/ ; https://futureagi.com/blog/elevenlabs-vs-cartesia-tts-2026/
27. Deepgram, Pricing: https://deepgram.com/pricing
28. Res. SCI 1033/2021 (resumen): https://abogados.com.ar/resolucion-n-10332021-de-la-secretaria-de-comercio-interior-parametros-minimos-obligatorios-de-calidad-para-los-servicios-de-atencion-y-comunicacion-a-distancia/29244 ; https://www.argentina.gob.ar/noticias/nuevos-parametros-para-los-servicios-de-atencion-al-cliente-telefonica-y-web
28b. Res. 425/2022, vigencia: https://abogados.com.ar/un-respiro-para-las-empresas-se-modifico-la-entrada-en-vigencia-de-la-resolucion-sci-10332021/30415
29. Bland AI, Pricing: https://www.bland.ai/pricing
30. Synthflow, Pricing: https://synthflow.ai/pricing
31. AAIP, grabación de videollamadas: https://abogados.com.ar/proteccion-de-datos-personales-en-videollamadas-nuevas-recomendaciones-de-la-agencia-de-acceso-a-la-informacion-publica/28927
32. Telnyx, Conversational AI pricing: https://telnyx.com/pricing/conversational-ai
33. Ley de IA en Argentina: https://dplnews.com/?p=298984 ; https://www.iproup.com/innovacion/62508-ley-de-inteligencia-artificial-chatgpt-proyecto-debate-congreso-resiste-javier-milei ; https://www.cronista.com/economia-politica/kicillof-regula-el-uso-de-la-inteligencia-artificial-en-la-provincia-que-se-podra-hacer-y-que-queda-prohibido
33b. Reforma de la Ley 25.326: https://www.diariojudicial.com/news-99786-datos-personales-libro-y-debate-en-agenda ; https://digitalpolicyalert.org/change/21988-bill-amending-article-26-of-personal-data-protection-law-no-25326-on-retention-period-of-credit-information-bill-no-4669-d-2026
34. Latencia: https://www.morphllm.com/best-ai-voice-agent-platforms ; https://telnyx.com/resources/voice-ai-latency-benchmark ; https://dev.to/jays_tech/i-benchmarked-the-voice-ai-stack-in-may-2026-what-actually-holds-up-in-production-3fmn
35. Cliengo, leads inmobiliarios por WhatsApp: https://guiawabusiness.cliengo.com/captar-leads-inmobiliarios-whatsapp
36. Precios de referencia de agentes de voz: https://www.cloudtalk.io/es/precios-del-agente-de-voz-con-ia/ ; https://techsy.io/es/blog/precios-agente-voz-ia-2026
37. Mercado, Accenture con Facebook (17/9/2020): https://mercado.com.ar/marketing/71-de-los-consumidores-locales-usa-whatsapp
38. Portafolio, Treble.ai: https://www.portafolio.co/tecnologia/whatsapp-como-se-consolido-como-el-principal-medio-entre-empresas-y-clientes-601797
39. Llamadas perdidas (sin dato argentino): https://ainora.lt/md/es/blog/estadisticas-atencion-telefonica-llamadas-pymes-espana-2026.md
40. Portales inmobiliarios: https://roomix.ai/blog/mejores-portales-inmobiliarios-argentina
41. Talleres y WhatsApp (proveedor): https://www.aurorainbox.com/2026/02/18/chatbot-talleres-mecanicos/
42. Ley 26.951, Registro No Llame: https://www.argentina.gob.ar/normativa/nacional/norma-233066/texto
