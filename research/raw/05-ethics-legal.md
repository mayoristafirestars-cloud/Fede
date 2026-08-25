# 05 — Guardrails éticos, legales y metodológicos para un sistema de perfilado a partir de fotos de Instagram

**Alcance:** sistema automatizado que analiza imágenes públicas de Instagram para construir un perfil de una cuenta o persona, con uso comercial legítimo (prospección B2B, calificación de leads, análisis de marca) desde **Argentina**.
**Fecha del relevamiento:** agosto 2026.
**Regla de oro que atraviesa todo el documento:** *lo público no equivale a consentido, y la exactitud declarada de la inferencia casi nunca es la exactitud real.*

---

## 1. DERECHO ARGENTINO

### 1.1 Ley 25.326 de Protección de los Datos Personales (LPDP)

Texto vigente: https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm
Decreto reglamentario 1558/2001: https://servicios.infoleg.gob.ar/infolegInternet/anexos/70000-74999/70368/norma.htm

**Art. 1 — Objeto.** Protección integral de los datos personales asentados en archivos, registros, bancos de datos "u otros medios técnicos de tratamiento de datos", públicos o privados destinados a dar informes, "para garantizar el derecho al honor y a la intimidad de las personas".
→ Una base de perfiles construida por scraping **es** un banco de datos alcanzado por la ley.

**Art. 2 — Definiciones clave.**
- *Datos personales*: "Información de cualquier tipo referida a personas físicas o de existencia ideal determinadas o determinables." Una foto de rostro + handle de IG es dato personal.
- *Datos sensibles*: "Datos personales que revelan **origen racial y étnico, opiniones políticas, convicciones religiosas, filosóficas o morales, afiliación sindical e información referente a la salud o a la vida sexual**."
- *Tratamiento de datos*: incluye recolección, conservación, almacenamiento, relacionamiento y **"evaluación"** — es decir, el scoring/perfilado está expresamente cubierto.
- *Disociación de datos*: tratamiento tal que la información no pueda asociarse a persona determinada o determinable.

**Art. 4 — Calidad de los datos** (principio de finalidad y minimización, en versión argentina):
- 4.1 Los datos deben ser "ciertos, adecuados, pertinentes y **no excesivos** en relación al ámbito y finalidad para los que se hubieren obtenido".
- 4.2 "La recolección **no puede efectuarse por medios desleales, fraudulentos o en forma contraria a las disposiciones de la presente ley**." → Este inciso es el que muerde al scraping que evade barreras técnicas, usa cuentas falsas o viola términos de servicio: es "medio desleal".
- 4.3 Prohibición de uso para "finalidades distintas o incompatibles" con las que motivaron la obtención. → La foto se publicó para socializar/promocionar; usarla para scoring psicométrico es un cambio de finalidad difícil de justificar.
- 4.4/4.5 Exactitud y obligación de suprimir/rectificar lo inexacto.
- 4.7 "Los datos deben ser **destruidos cuando hayan dejado de ser necesarios o pertinentes**." → obliga a una política de retención.

**Art. 5 — Consentimiento.** Regla: "libre, expreso e informado", por escrito o medio equiparable. Es un régimen **opt-in**, más estricto que el GDPR en cuanto a que Argentina *no tiene una base autónoma de "interés legítimo"*.
Excepciones del art. 5.2, las únicas usables aquí:
- **5.2.a) datos obtenidos de "fuentes de acceso público irrestricto"**;
- 5.2.c) listados limitados a nombre, DNI, CUIT/CUIL, ocupación, fecha de nacimiento y domicilio;
- 5.2.d) datos que deriven de una relación contractual, científica o profesional del titular.

⚠️ **Zona gris crítica**: si un perfil de Instagram abierto es o no "fuente de acceso público irrestricto". La postura defendible y conservadora: la excepción puede alcanzar la *recolección* del dato tal como fue publicado (nombre comercial, rubro, ubicación del local, contacto), pero **no** habilita ni el enriquecimiento inferencial (deducir atributos que el titular nunca publicó) ni la formación de datos sensibles. El art. 5.2 exime del consentimiento, **no** exime de los arts. 4 (finalidad/proporcionalidad), 6 (información), 7 (sensibles), 14/16 (derechos) ni 21 (registro).

**Art. 6 — Deber de información.** Al recabar hay que informar finalidad y destinatarios, existencia del banco de datos e identidad/domicilio del responsable, carácter facultativo, consecuencias, y "la posibilidad del interesado de ejercer los derechos de acceso, rectificación y supresión". En scraping esto se traduce en una **política de privacidad pública y accesible** que describa el tratamiento y un canal de contacto.

**Art. 7 — Datos sensibles.** Es la norma más dura del sistema argentino:
- 7.1 "Ninguna persona puede ser obligada a proporcionar datos sensibles."
- 7.2 Sólo pueden recolectarse "cuando medien razones de interés general autorizadas por ley" o con finalidades estadísticas/científicas **sin identificar titulares**.
- 7.3 "**Queda prohibida la formación de archivos, bancos o registros que almacenen información que directa o indirectamente revele datos sensibles**" (salvo iglesias, partidos y sindicatos respecto de sus miembros).
- 7.4 Antecedentes penales/contravencionales: sólo autoridades públicas competentes.

→ **Consecuencia operativa:** una base de perfiles que guarde campos como "probablemente LGBT", "aparenta ser judío/musulmán", "milita en X", "parece tener una discapacidad o enfermedad", "origen étnico: …" es **ilícita per se en Argentina**, aunque el dato sea una *inferencia* y aunque la foto fuera pública. La expresión "directa o **indirectamente** revele" cubre las proxies (bandera, símbolo religioso, marcha, silla de ruedas, etc.).

**Art. 11 — Cesión.** Sólo para fines directamente relacionados con el interés legítimo de cedente y cesionario **y con consentimiento previo** del titular, salvo excepciones (entre ellas las del art. 5.2 y la disociación total). → No vender ni compartir la base de perfiles.

**Art. 14 — Derecho de acceso.** Respuesta en **10 días corridos** desde la intimación fehaciente; gratuito a intervalos no menores a 6 meses.
**Art. 16 — Rectificación, actualización y supresión.** Plazo máximo **5 días hábiles**; obligación de notificar al cesionario dentro del 5º día hábil; bloqueo del registro mientras dure la verificación.
→ El sistema debe poder **buscar por handle, exportar el perfil completo, corregirlo y borrarlo** en esos plazos. Si no puede, no cumple.

**Art. 20 — Impugnación de valoraciones personales.** "Las decisiones judiciales o los actos administrativos que impliquen apreciación o valoración de conductas humanas **no podrán tener como único fundamento el resultado del tratamiento informatizado de datos personales que suministren una definición del perfil o personalidad del interesado**. Los actos que resulten contrarios a la disposición precedente serán **insanablemente nulos**."
→ Es el equivalente argentino (más acotado, apunta a actos estatales/judiciales) del art. 22 GDPR. Doctrinariamente se lo lee como principio general de que un perfil algorítmico no puede ser el único fundamento de una valoración de conducta. **Regla práctica: siempre human-in-the-loop antes de cualquier decisión con efecto sobre la persona.**

**Art. 21 — Registro de bases de datos.** Todo archivo privado "destinado a proporcionar informes" debe inscribirse en el Registro Nacional de Bases de Datos (RNBD) de la AAIP, vía TAD. Además: "Ningún usuario de datos podrá poseer datos personales de naturaleza distinta a los declarados en el registro."
Guía oficial de obligaciones: https://www.argentina.gob.ar/aaip/datospersonales/responsables/obligaciones

**Art. 27 — Archivos con fines de publicidad (la base legal más útil para uso comercial).** Permite tratar datos "aptos para establecer perfiles determinados con fines promocionales, comerciales o publicitarios" o hábitos de consumo, **cuando figuren en documentos accesibles al público o hayan sido facilitados por los propios titulares u obtenidos con su consentimiento**. El titular puede en cualquier momento **solicitar el retiro o bloqueo** de su nombre de la base (opt-out), y el decreto 1558/2001 lo reglamenta exigiendo que en cada comunicación se informe quién es el responsable y el derecho a retirarse.
→ **Este es el carril legal del prospecting comercial en Argentina.** Su límite: sólo datos *aptos para fines promocionales* y *de fuente accesible al público*; nunca sensibles; siempre con opt-out operativo.

**Arts. 31/32 — Sanciones.** Art. 31: apercibimiento, suspensión, multa, clausura o cancelación del archivo. Los montos originales fueron actualizados por las Resoluciones **AAIP 240/2022** (clasificación de infracciones en leves, graves y muy graves) y **244/2022** (topes de multa: ~$3M leves, $10M graves, $15M muy graves, valores 2022). Art. 32 incorpora al Código Penal los arts. **117 bis** (insertar datos falsos en archivo de datos personales) y **157 bis** (acceso ilegítimo a banco de datos personales y revelación indebida) — prisión de 1 mes a 2 años, agravada para funcionarios.
**Arts. 33-43 — Habeas data.** Acción constitucional (art. 43 CN) para conocer, rectificar, suprimir o someter a confidencialidad los datos.

### 1.2 AAIP — Agencia de Acceso a la Información Pública

Autoridad de control desde 2017 (Ley 27.275). Portal: https://www.argentina.gob.ar/aaip/datospersonales

**Resolución AAIP 4/2019** — "Criterios orientadores e indicadores de mejores prácticas en la aplicación de la Ley 25.326" (Anexo I).
Norma: https://servicios.infoleg.gob.ar/infolegInternet/anexos/315000-319999/318874/norma.htm · Anexo: https://servicios.infoleg.gob.ar/infolegInternet/anexos/315000-319999/318874/res4AAIP.pdf
Criterios relevantes:
- **Criterio 2 — Tratamiento automatizado de datos:** cuando una decisión automatizada produce efectos jurídicos o negativos significativos, el responsable debe poder **explicar la lógica aplicada**.
- **Criterio 3 — Disociación:** no hay dato personal si la re-identificación exige medidas o plazos desproporcionados o inviables.
- **Criterio 4 — Datos biométricos:** "datos personales obtenidos a partir de un tratamiento técnico específico, relativos a las características físicas, fisiológicas o conductuales de una persona humana" que permiten o confirman su identificación única. **Son sensibles cuando identifican unívocamente y además revelan información cuyo uso pueda ser potencialmente discriminatorio** (origen étnico, salud, etc.).
- **Criterio 5 — Consentimiento:** el responsable debe validar que quien presta el consentimiento sea efectivamente el titular.

→ **Consecuencia directa para un sistema de fotos:** correr *face embeddings* / reconocimiento facial sobre fotos de IG convierte el pipeline en tratamiento de **datos biométricos**, y si además se usa para inferir etnia, salud u orientación, en **datos sensibles prohibidos por el art. 7.3**. Evitar por completo la identificación facial y el matching de rostros entre cuentas.

**Resolución AAIP 255/2022** (datos genéticos como sensibles): https://www.boletinoficial.gob.ar/detalleAviso/primera/277889/20221216

**Resolución AAIP 161/2023** — crea el *Programa Nacional de Transparencia y Protección de Datos Personales en el uso de la Inteligencia Artificial*: https://www.argentina.gob.ar/programa-nacional-de-transparencia-y-proteccion-de-datos-personales-en-el-uso-de-la-inteligencia

**Guía AAIP para una IA responsable** (junio 2024) — "Guía para entidades públicas y privadas en materia de transparencia y protección de datos personales para una inteligencia artificial responsable": https://www.argentina.gob.ar/aaip/documentos-de-inteligencia-artificial · nota oficial: https://www.argentina.gob.ar/noticias/guia-de-la-aaip-para-usar-la-inteligencia-artificial-de-manera-responsable
Ejes: transparencia algorítmica y protección de datos a lo largo de todo el ciclo de vida del sistema (diseño, implementación, mantenimiento); evaluación de impacto; explicabilidad; supervisión humana; trazabilidad de las fuentes de datos.

### 1.3 Derecho a la imagen — art. 53 Código Civil y Comercial

> **Art. 53 CCyCN.** "Para captar o reproducir la imagen o la voz de una persona, de cualquier modo que se haga, **es necesario su consentimiento**, excepto en los siguientes casos: a) que la persona participe en actos públicos; b) que exista un interés científico, cultural o educacional prioritario, y se tomen las precauciones suficientes para evitar un daño innecesario; c) que se trate del ejercicio regular del derecho de informar sobre acontecimientos de interés general."

Doctrina consolidada: la autorización para **captar** no implica autorización para **reproducir**; son consentimientos independientes. Que alguien haya publicado su foto en Instagram **no** es consentimiento para que un tercero la descargue, almacene y reutilice comercialmente.
Referencia: https://leyes-ar.com/codigo_civil_y_comercial/53.htm
Concordantes: art. 51 (inviolabilidad de la persona humana), art. 52 (afectaciones a la dignidad, intimidad, honra, imagen e identidad → indemnización), art. 1770 CCyCN (protección de la vida privada).

→ **Consecuencia operativa:** no almacenar imágenes descargadas. Trabajar sobre **URLs/embeds oficiales** y sobre **descripciones textuales derivadas**, borrando el binario tras el análisis. No reproducir públicamente la foto de una persona en reportes, dashboards o presentaciones sin su consentimiento.

### 1.4 Menores — Ley 26.061

**Art. 22 (Derecho a la dignidad).** "Las niñas, niños y adolescentes tienen derecho a ser respetados en su dignidad, reputación y propia imagen. **Se prohíbe exponer, difundir o divulgar datos, informaciones o imágenes que permitan identificar, directa o indirectamente**, a los sujetos de esta ley, a través de cualquier medio de comunicación o publicación, en contra de su voluntad y la de sus padres o representantes legales, cuando se lesione su dignidad o reputación o constituyan injerencias arbitrarias o ilegales en su vida privada."
Texto: https://servicios.infoleg.gob.ar/infolegInternet/anexos/110000-114999/110778/norma.htm

→ **Regla dura: nunca perfilar menores, nunca almacenar sus imágenes, y descartar la cuenta entera si el sistema detecta señales de que el titular es menor de 18.**

### 1.5 Otras normas argentinas concurrentes

- **Ley 23.592 (actos discriminatorios).** Obliga a cesar y reparar actos que arbitrariamente restrinjan derechos por raza, religión, nacionalidad, ideología, opinión política o gremial, sexo, posición económica, condición social o caracteres físicos. Un perfilado que segmente por esos ejes puede ser fuente de responsabilidad civil autónoma.
- **Ley 24.240 de Defensa del Consumidor, art. 8 bis** (trato digno y no discriminatorio) y **art. 4** (información). Relevante si el perfil se usa para diferenciar precios o condiciones.
- **Ley 26.522 de Servicios de Comunicación Audiovisual.** Poco relevante para perfilado en redes: regula servicios audiovisuales, no plataformas. Sus arts. 70 (prohibición de contenidos discriminatorios) y 71 (obligación de respetar la Ley 26.061 en programación y publicidad) son útiles sólo como **estándar de contenido** si el output del sistema alimenta piezas publicitarias. No es la norma aplicable a la recolección de datos.
- **Art. 43 Constitución Nacional** — habeas data como garantía constitucional.

### 1.6 El proyecto de nueva ley de protección de datos

La Ley 25.326 tiene más de 25 años y no contempla profiling, IA, portabilidad, DPO, notificación de brechas ni evaluaciones de impacto. Estado a agosto 2026:
- El **anteproyecto elaborado por la AAIP** (mensaje 2023) **perdió estado parlamentario** a fines de 2024. Ficha oficial: https://www.argentina.gob.ar/aaip/datospersonales/proyecto-ley-datos-personales
- Hay al menos **tres proyectos vivos**: **644-S-2025** (Doñate) y **1948-D-2025** (Carro), ambos inspirados en el anteproyecto de la AAIP y con enfoque de derechos fundamentales; y el **1751-D-2026** del diputado **Martín Yeza** (72 artículos, 13 títulos, deroga expresamente la 25.326 y su reglamentación), con enfoque pro-innovación/tecnología. Sitio del proyecto Yeza: https://leydedatospersonales.tech/
- Análisis: https://iapp.org/news/a/se-impulsa-un-nuevo-proyecto-de-reforma-del-r-gimen-de-protecci-n-de-datos-en-argentina · https://www.marval.com/publicacion/nuevos-proyectos-de-ley-de-datos-personales-en-argentina-17289?lang=en

→ **Todos** los proyectos incorporan figuras tipo GDPR: interés legítimo como base autónoma, derecho a no ser objeto de decisiones automatizadas, evaluaciones de impacto, notificación de brechas. **Diseñar hoy contra el estándar GDPR es la apuesta correcta**: es a la vez el techo probable de la ley futura y el requisito para conservar la adecuación.

### 1.7 Adecuación ante la Unión Europea

Argentina está reconocida como país con nivel adecuado de protección desde la **Decisión 2003/490/CE** de la Comisión Europea (30/6/2003): https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32003D0490

El **15 de enero de 2024** la Comisión publicó el informe de la primera revisión de las 11 decisiones de adecuación adoptadas bajo la Directiva 95/46/CE (Andorra, **Argentina**, Canadá, Islas Feroe, Guernsey, Isla de Man, Israel, Jersey, Nueva Zelanda, Suiza y **Uruguay**) y concluyó que **todas siguen ofreciendo un nivel adecuado**; ninguna se retira ni modifica por ahora. Se valoró positivamente el fortalecimiento de la independencia de la autoridad de control tras la creación de la AAIP.
Cobertura: https://iapp.org/news/a/european-commission-upholds-11-adequacy-decisions · https://www.insideprivacy.com/cross-border-transfers/european-commission-retains-adequacy-decisions-for-data-transfers-to-eleven-countries/
Carta del EDPB (5/12/2024): https://www.edpb.europa.eu/system/files/documents/2024-12/edpb_letter_20241205_european-commission-review-of-11-existing-adequacy-decisions_en.pdf

→ **Práctico:** los datos pueden fluir UE→Argentina sin salvaguardas adicionales. Pero la adecuación es **revisable**; y la contracara es que un tratamiento argentino abusivo sobre datos de europeos es exactamente el tipo de práctica que erosiona la adecuación. No es sólo riesgo propio, es riesgo país.

---

## 2. GDPR — QUÉ APLICA SI HAY ALGÚN TITULAR EN LA UE

Aplicabilidad extraterritorial: **art. 3(2) GDPR** — aplica a responsables fuera de la UE cuando (a) ofrecen bienes/servicios a personas en la UE o (b) **monitorean su comportamiento**. El perfilado de cuentas es el caso de manual del inciso (b). Confirmado en *ICO v Clearview AI* (ver 2.5).

### 2.1 Art. 4(4) — Definición de perfilado
> "toda forma de tratamiento automatizado de datos personales consistente en utilizar datos personales para **evaluar determinados aspectos personales** de una persona física, en particular para analizar o predecir aspectos relativos al rendimiento profesional, situación económica, salud, **preferencias personales, intereses, fiabilidad, comportamiento, ubicación o movimientos** de dicha persona física."
https://gdpr-info.eu/art-4-gdpr/

Analizar fotos para inferir estilo de vida, poder adquisitivo o personalidad **es perfilado** por definición.

### 2.2 Art. 9 — Categorías especiales
Prohibido tratar datos que revelen **origen racial o étnico, opiniones políticas, convicciones religiosas o filosóficas, afiliación sindical**, datos genéticos, **datos biométricos dirigidos a identificar de manera unívoca a una persona**, datos relativos a la **salud** o a la **vida sexual u orientación sexual**, salvo alguna de las excepciones del art. 9(2).
https://gdpr-info.eu/art-9-gdpr/

Clave: **la inferencia también cuenta.** TJUE, **C-184/20, *OT v Vyriausioji tarnybinės etikos komisija*** (1/8/2022): la publicación de datos que permiten **deducir indirectamente** la orientación sexual de una persona constituye tratamiento de categorías especiales. Es decir, no hace falta que el dato esté etiquetado como sensible: basta que el tratamiento permita revelarlo.
Excepción práctica única y estrecha: **art. 9(2)(e)**, datos "manifiestamente hechos públicos por el interesado" — interpretado restrictivamente (TJUE C-136/17, *GC y otros*: exige un acto deliberado e inequívoco del propio titular de hacer público *ese* dato sensible). Una foto no es una declaración manifiesta de religión, salud ni orientación.

### 2.3 Art. 22 — Decisiones automatizadas
> **22(1)** "Todo interesado tendrá derecho a no ser objeto de una decisión basada únicamente en el tratamiento automatizado, incluida la elaboración de perfiles, que produzca efectos jurídicos en él o le afecte significativamente de modo similar."
> **22(2)** Excepciones: necesaria para un contrato; autorizada por Derecho de la Unión o del Estado miembro con salvaguardas; consentimiento explícito.
> **22(3)** Salvaguardas mínimas: **derecho a obtener intervención humana, a expresar su punto de vista y a impugnar la decisión.**
> **22(4)** No puede basarse en categorías especiales del art. 9 salvo 9(2)(a) o (g) con medidas adecuadas.
https://gdpr-info.eu/art-22-gdpr/

Guía interpretativa: **WP29, Guidelines on Automated individual decision-making and Profiling, WP251rev.01**, adoptadas el 6/2/2018 y **endosadas por el EDPB**: https://ec.europa.eu/newsroom/article29/items/612053/en
Ampliado por TJUE **C-634/21, *SCHUFA*** (7/12/2023): el mero *scoring* puede ser ya la "decisión" del art. 22 si un tercero lo usa de forma determinante.

### 2.4 Interés legítimo — art. 6(1)(f) y el balancing test
**EDPB Guidelines 1/2024** sobre el art. 6(1)(f): tres condiciones **acumulativas** — (i) interés legítimo lícito, claramente articulado, real y presente (no especulativo); (ii) **necesidad** del tratamiento (¿no hay medio menos intrusivo?); (iii) **ponderación** frente a derechos y libertades del interesado, incluyendo sus **expectativas razonables**.
**EDPB Opinion 28/2024** sobre modelos de IA y protección de datos.
**EDPB Guidelines 03/2026 sobre web scraping en el contexto de la IA generativa**, adoptadas en el plenario del **7-8 de julio de 2026**, en consulta pública hasta el **30 de octubre de 2026**: https://www.edpb.europa.eu/news/edpb-sheds-light-on-anonymisation-and-web-scraping-for-generative-ai-and-adopts-final-version_en
Puntos operativos de esa guía:
- El scraping es tratamiento (recolección, almacenamiento, organización, recuperación) y el GDPR aplica plenamente.
- **El consentimiento no es base viable a escala**; el interés legítimo es la única base realista, y sólo si se supera el test triple.
- Deben respetarse **limitación de la finalidad** y **transparencia**; la información individual puede omitirse sólo si es imposible o exige un esfuerzo desproporcionado (**art. 14(5)(b)**), lo que **no** exime de publicar información general.
- Categorías especiales: **prohibición en principio**; se necesita base del art. 6 **y** excepción del art. 9(2).
- Medidas de mitigación esperadas: obtener datos de **fuentes fiables**, registrar *timestamp*, validar antes de usar, **excluir sitios sensibles**, respetar señales de exclusión, filtrar y borrar datos sensibles capturados incidentalmente, y aplicar minimización real.

**ICO (Reino Unido).** Serie de consultas sobre IA generativa (enero 2024 – informe de resultados 13/12/2024). Capítulo 1: *"The lawful basis for web scraping to train generative AI models"* — el ICO mantiene que **el interés legítimo es la única base disponible**, y sólo si se supera el test de tres partes, en particular el de **necesidad**: https://ico.org.uk/about-the-ico/what-we-do/our-work-on-artificial-intelligence/response-to-the-consultation-series-on-generative-ai/the-lawful-basis-for-web-scraping-to-train-generative-ai-models/

**Garante (Italia).** *Provvedimento n. 329 del 20/5/2024*, "Nota informativa su web scraping e intelligenza artificiale generativa" (G.U. n. 132 del 7/6/2024): https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10020316 — indica a titulares de sitios y plataformas contramedidas frente al scraping de terceros (áreas reservadas, cláusulas anti-scraping en los ToS, rate limiting, robots.txt, verificación de bots). Señal regulatoria: **el scraping masivo se presume incompatible con la finalidad original de publicación.**

### 2.5 Enforcement: la línea Clearview AI
Modelo de negocio idéntico en su estructura al de un perfilador de fotos de IG: scraping masivo de imágenes públicas → base biométrica → servicio comercial de identificación.

| Autoridad | Sanción / medida | Referencia |
|---|---|---|
| ICO (UK), 05/2022 | £7,5M + enforcement notice (borrado de datos de residentes UK) | https://ico.org.uk |
| CNIL (Francia), 10/2022 | €20M + apremio | |
| Garante (Italia), 02/2022 | €20M + prohibición de ulterior scraping en territorio italiano + orden de borrado de datos biométricos | https://noyb.eu/en/eu-20-mio-fine-clearview-ai-italy |
| HDPA (Grecia), 07/2022 | €20M | |
| AP (Países Bajos), 09/2024 | **€30,5M** — la mayor hasta la fecha; base de +30.000 millones de imágenes scrapeadas sin conocimiento ni consentimiento | https://www.techmonitor.ai/technology/cybersecurity/dutch-regulator-fines-clearview-ai-e30-5m-over-illegal-facial-recognition-data-collection |

**ICO v Clearview AI Inc (Privacy International interviniente), [2025] UKUT 319 (AAC)**, 7/10/2025: el Upper Tribunal revocó la decisión del First-tier Tribunal y confirmó que **el ICO sí tiene jurisdicción**: la actividad de Clearview cae en el ámbito territorial del UK GDPR por **art. 3(2)(b)** — monitoreo del comportamiento de personas en el Reino Unido — aunque el responsable esté en EE.UU. y sus clientes sean extranjeros.
https://www.gov.uk/administrative-appeals-tribunal-decisions/the-information-commissioners-office-v-clearview-ai-inc-privacy-international-intervening-2025-ukut-319-aac · https://ico.org.uk/about-the-ico/media-centre/news-and-blogs/2025/10/uk-upper-tribunal-hands-down-judgment-on-clearview-ai-inc/

→ **Lección:** "los datos ya eran públicos" y "estamos fuera de la UE" **no** son defensas.

### 2.6 EU AI Act — líneas rojas ya vigentes
Reglamento (UE) 2024/1689. Las **prohibiciones del art. 5 son aplicables desde el 2 de febrero de 2025**; la Comisión publicó guías interpretativas el 4/2/2025.
- **Art. 5(1)(f)** — prohibidos los sistemas de **reconocimiento de emociones** en el ámbito laboral y educativo.
- **Art. 5(1)(g)** — prohibidos los sistemas de **categorización biométrica** que clasifiquen individualmente a personas físicas **a partir de sus datos biométricos para deducir o inferir raza, opiniones políticas, afiliación sindical, convicciones religiosas o filosóficas, vida sexual u orientación sexual**.
Texto: https://artificialintelligenceact.eu/article/5/ · análisis: https://fpf.org/blog/red-lines-under-the-eu-ai-act-understanding-the-prohibition-of-biometric-categorization-for-certain-sensitive-characteristics/

→ Un módulo que mire una foto y devuelva "etnia probable" o "orientación probable" es, en la UE, una **práctica prohibida**, no un riesgo a gestionar. En Argentina es, además, la conducta descripta en el art. 7.3 LPDP.

---

## 3. TÉRMINOS DE PLATAFORMA: INSTAGRAM / META

### 3.1 Qué prohíben los términos

**Instagram Terms of Use** (https://help.instagram.com/581066165581870) y **Meta Terms of Service** (https://www.facebook.com/terms.php), sección "What you can't do / Lo que no podés hacer":
> "You may not access or collect data from our Products using **automated means** (without our prior permission) or attempt to access data you do not have permission to access, **regardless of whether such automated access or collection is undertaken while logged in to a Facebook account**."

La coletilla final ("logged in or not") fue **agregada tras el fallo Bright Data** y es aplicable desde el **1 de enero de 2025**: cierra expresamente el hueco de "yo scrapeo deslogueado, no soy usuario, no me obligan los ToS".

Edad mínima de uso de Instagram: **13 años** (más alta donde la ley local lo exija).

**Meta Automated Data Collection Terms** (efectivas 7/10/2024): https://www.facebook.com/legal/automated_data_collection_terms
- Exigen **permiso expreso por escrito** obtenido mediante el proceso formal de autorización de Meta; **aceptar los términos no equivale a tener permiso**.
- Prohíben "transferring, selling, licensing or sublicensing Collected Data and data derived from Collected Data to any third party".
- Limitan los usos autorizados a resultados de motores de búsqueda, previews de URL o fines expresamente autorizados.

**Meta Platform Terms** (https://developers.facebook.com/terms/) — para quien usa las APIs oficiales. Obligaciones duras:
- Prohibido procesar Platform Data para "**discriminate or encourage discrimination**" por características protegidas, ni para "**eligibility determinations about people, including for housing, employment, insurance, education**".
- Prohibido "**Processing Platform Data to perform, facilitate, or provide tools for surveillance**".
- Prohibido "**Selling, licensing, or purchasing Platform Data**".
- Prohibido construir o enriquecer perfiles de usuario **sin consentimiento válido** del usuario.
- **Borrado:** "Delete all Platform Data as soon as reasonably possible" cuando ya no sea necesaria, cuando cese el producto, cuando Meta lo pida, o cuando el usuario lo pida o cierre su cuenta; en la práctica **90 días** desde la revocación del acceso o baja de cuenta (Platform Terms §3(d)). Debe existir una vía "easily accessible and clearly marked" para pedir modificación o borrado.

### 3.2 Qué está legítimamente disponible hoy

- **Instagram Basic Display API: DESACTIVADA el 4 de diciembre de 2024.** Ya no existe. Reemplazo: **Instagram API with Instagram Login** (cuentas personales, business y creator), que sólo da acceso a los datos **de la propia cuenta que autoriza**. Overview oficial: https://developers.facebook.com/docs/instagram-platform/overview/
- **Instagram API with Facebook Login (ex Instagram Graph API)** — para cuentas profesionales vinculadas a una Página.
- **Business Discovery** — https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/business-discovery/
  - Es **el único camino oficial para leer datos públicos de *otra* cuenta**.
  - Requiere: tu propia **cuenta profesional** de Instagram, token de acceso, y **Facebook Login** (no funciona con Instagram Login).
  - Sólo alcanza **cuentas profesionales (Business/Creator)**, no cuentas personales.
  - Devuelve: `username`, `name`, `biography`, `website`, `profile_picture_url`, `followers_count`, `media_count`, y objetos `media` con `caption`, `media_url`, `permalink`, `timestamp`, `like_count`, `comments_count`.
  - Limitación expresa: "**Data about age-gated Instagram professional accounts will not be returned.**"
  - Rate limiting de plataforma (no el de Business Use Case).
- **oEmbed** (https://developers.facebook.com/docs/instagram-platform/oembed/) — devuelve el **código de embed** de un post o reel público. Sirve para **mostrar** contenido legítimamente, sin copiarlo ni almacenarlo. Requiere app con el feature `oEmbed Read`.
- **Hashtag Search**, **Mentions**, **Insights** — sobre la propia cuenta o hashtags.

→ **Traducción para una PyME:** con Business Discovery + oEmbed se puede construir legítimamente un análisis de **cuentas comerciales**: qué publican, con qué frecuencia, qué engagement tienen, qué productos muestran, qué estética usan. **No** se puede construir legítimamente una base de personas físicas con cuentas personales.

### 3.3 La línea jurisprudencial sobre scraping de datos públicos (EE.UU.) y sus límites

**hiQ Labs, Inc. v. LinkedIn Corp.** (9th Cir.) — https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn
- *hiQ I* (2019) y *hiQ II* (abril 2022, tras la devolución por *Van Buren v. United States*, 593 U.S. 374 (2021)): **el scraping de datos públicos no viola la CFAA**, porque no hay acceso "sin autorización" a un sitio abierto al público.
- **Pero**: noviembre 2022, el N.D. Cal. concedió a LinkedIn **summary judgment por incumplimiento de contrato**: hiQ violó el User Agreement al scrapear y al crear perfiles falsos. https://natlawreview.com/article/court-finds-hiq-breached-linkedin-s-terms-prohibiting-scraping-mixed-ruling-declines
- **Diciembre 2022: acuerdo confidencial con sentencia de US$500.000 contra hiQ**, reconocimiento de responsabilidad por *trespass to chattels* y *misappropriation* bajo derecho común de California, e **injunction permanente** que le impide volver a scrapear LinkedIn. hiQ cerró.

**Lectura correcta de hiQ:** no legaliza el scraping. Sólo dice que **la vía penal/CFAA no es el arma correcta**. Las armas que sí funcionan son **contrato (ToS), trespass to chattels, misappropriation, unjust enrichment** — y, en Europa/Argentina, **la ley de datos personales**, que hiQ nunca tuvo que enfrentar.

**Meta Platforms, Inc. v. Bright Data Ltd.**, N.D. Cal., Juez Edward M. Chen, **23/1/2024** — summary judgment a favor de Bright Data:
> "The Facebook and Instagram Terms do not bar logged-off scraping of public data; perforce it does not prohibit the sale of such public data."
Razonamiento: los ToS obligan a "usuarios"; Bright Data scrapeaba deslogueado; y la cláusula de "supervivencia" que pretendía prohibir el scraping a perpetuidad tras la baja de la cuenta se declaró **inejecutable**.
https://www.fbm.com/publications/major-decision-affects-law-of-scraping-and-online-data-collection-meta-platforms-v-bright-data/ · https://blog.ericgoldman.org/archives/2024/01/game-on-bright-data-scores-major-victory-in-web-scraping-dispute-with-meta-guest-blog-post.htm

⚠️ **Ese fallo ya está neutralizado en lo práctico**: Meta reescribió los ToS (cláusula "regardless of whether... logged in", vigente 1/1/2025) y publicó las Automated Data Collection Terms (7/10/2024). Además el fallo es de un district court de California y **no dice nada sobre derecho de datos personales argentino ni europeo**.

**Meta contra scrapers — historial de litigios:**
- **Meta v. BrandTotal / Unimania** (2020) — **acuerdo septiembre 2022**: prohibición permanente de usar y scrapear Facebook e Instagram; BrandTotal cerró.
- **Meta v. Octopus Data** (julio 2022) — uso de cuentas falsas en Instagram para recolectar datos de ~350.000 perfiles.
- **Meta v. Voyager Labs** (enero 2023) — Meta alegó **38.000 cuentas falsas** usadas para scrapear datos de **más de 600.000** usuarios y venderlos como servicio de vigilancia. **Acuerdo homologado** por la jueza Araceli Martínez-Olguín (N.D. Cal.): Voyager se obliga a **no volver a scrapear** Facebook e Instagram y a **borrar permanentemente** todos los datos obtenidos. https://www.cnbc.com/2023/01/12/meta-sues-voyager-labs-over-scraping-user-data.html

Nótese el patrón: los casos que Meta gana con contundencia son los que involucran **cuentas falsas** y **venta de datos para vigilancia**. Ese es exactamente el perfil de riesgo a evitar.

### 3.4 Qué puede y qué no puede hacer concretamente una PyME argentina

**✅ PUEDE**
1. Mirar cuentas públicas **manualmente** y tomar notas — eso es investigación de mercado normal, no tratamiento automatizado masivo.
2. Usar **Business Discovery** con su propia cuenta profesional para leer métricas y posts públicos de **otras cuentas profesionales** (proveedores, competidores, revendedores, marcas).
3. Usar **oEmbed** para mostrar posts públicos en su web o presentaciones.
4. Analizar **su propia** cuenta, sus insights, sus comentarios y sus DMs.
5. Construir perfiles **de cuentas comerciales** (rubro, surtido, precios exhibidos, frecuencia de publicación, estética, zona) con finalidad de prospección B2B — encuadrable en el **art. 27 LPDP** si la fuente es accesible al público y se ofrece opt-out.
6. Guardar **datos de contacto comercial** publicados por el propio negocio (teléfono comercial, dirección del local, email de contacto, sitio web).
7. Contactar comercialmente identificándose, informando el origen de los datos y ofreciendo baja inmediata (arts. 6 y 27 LPDP).

**❌ NO PUEDE**
1. Scrapear con **bots, cuentas falsas, cuentas de terceros, automatización de sesión o evasión de rate limits/CAPTCHAs**. Viola los ToS, las Automated Data Collection Terms, y en Argentina el **art. 4.2 LPDP** ("medios desleales").
2. **Descargar y almacenar imágenes** de personas — art. 53 CCyCN + art. 7 LPDP si de ellas se infiere algo sensible.
3. Correr **reconocimiento facial / face embeddings / matching de rostros** — datos biométricos (Res. AAIP 4/2019, criterio 4).
4. **Inferir y guardar** etnia, religión, ideología, afiliación sindical, salud, discapacidad, embarazo, orientación sexual o vida sexual — **art. 7.3 LPDP prohíbe la formación misma del archivo**, y art. 5(1)(g) AI Act si toca la UE.
5. Perfilar **menores de 18**.
6. **Vender, ceder o licenciar** la base de perfiles (art. 11 LPDP; Platform Terms; Automated Data Collection Terms).
7. Usar el perfil para **decisiones de elegibilidad** (crédito, condiciones de pago, empleo) sin intervención humana ni posibilidad de impugnación (art. 20 LPDP; art. 22 GDPR; Platform Terms).
8. Perfilar **personas físicas privadas** con fines de vigilancia, targeting personalizado o dossier.

---

## 4. ÉTICA DE LA INVESTIGACIÓN

### 4.1 AoIR — Internet Research: Ethical Guidelines 3.0
Franzke, A.S., Bechmann, A., Zimmer, M., Ess, C. y el AoIR Ethics Working Committee (2020). Aprobadas por unanimidad por la membresía de AoIR el **6 de octubre de 2019**.
PDF: https://aoir.org/reports/ethics3.pdf · Portal: https://aoir.org/ire30/

Principios operativos que se trasladan directamente al diseño del sistema:
- **Ética como proceso, no como checklist.** Las decisiones éticas se reevalúan en cada etapa del ciclo de vida (formulación, recolección, análisis, publicación, archivo, borrado), no una sola vez al inicio.
- **Casuística y contexto por encima de reglas universales.** La misma técnica es aceptable en un caso e inaceptable en otro según el contexto de publicación.
- **Proporcionalidad del daño.** "The greater the vulnerability of the community/author, the greater the obligation of the researcher to protect them."
- **Lo público-online no es un espacio sin expectativas de privacidad.** Se retoma la **integridad contextual** de Helen Nissenbaum: la información fluye según normas propias de cada contexto; extraerla de su contexto de origen es, en sí, la violación.
- **Consentimiento en Big Data:** IRE 3.0 dedica atención específica a la imposibilidad práctica del consentimiento informado en enfoques de datos masivos, y a las obligaciones sustitutas que eso genera (minimización, agregación, no republicación de identificadores).
- Novedad de la 3.0: protección **del propio investigador** y del equipo.

### 4.2 "Los datos ya son públicos" no es consentimiento
**Zimmer, M. (2010). "But the data is already public": on the ethics of research in Facebook.** *Ethics and Information Technology*, 12(4), 313-325.
https://link.springer.com/article/10.1007/s10676-010-9227-5 · PDF: https://www.sfu.ca/~palys/Zimmer-2010-EthicsOfResearchFromFacebook.pdf

Caso *Tastes, Ties, and Time* (T3): investigadores de Harvard scrapearon los perfiles de Facebook de toda la cohorte 2009 de una universidad, los cruzaron con datos académicos y de residencia provistos por la institución, y publicaron un dataset "anonimizado". Zimmer **re-identificó la institución en días** a partir de metadatos residuales (cantidad de alumnos, oferta de carreras, distribución de nacionalidades).

Argumentos centrales, todos aplicables a Instagram:
1. **La accesibilidad técnica no es una autorización moral.** Que un perfil no tenga barreras no significa que su titular haya consentido su agregación, análisis y almacenamiento por terceros.
2. **La agregación crea un dato nuevo.** Cada foto por separado es trivial; 300 fotos analizadas conjuntamente producen un perfil que el titular nunca publicó ni consintió.
3. **La anonimización de datos ricos y granulares falla.** Cuanto más rico el perfil, más fácil la re-identificación.
4. **Las expectativas de privacidad en redes son contextuales, no binarias.** La gente publica *para su audiencia imaginada*, no para el mundo.

Complemento: **boyd, d. & Crawford, K. (2012), "Critical Questions for Big Data"**, *Information, Communication & Society* 15(5) — "just because it is accessible does not make it ethical".

### 4.3 El caso Kosinski/Wang ("gaydar") y la crítica fisiognómica

**Wang, Y. & Kosinski, M. (2018). "Deep neural networks are more accurate than humans at detecting sexual orientation from facial images."** *Journal of Personality and Social Psychology*, 114(2), 246-257.
Preprint: https://www.gsb.stanford.edu/sites/gsb/files/publication-pdf/wang_kosinski.pdf
Afirmación: 81% de acierto distinguiendo hombres gay de heterosexuales con una sola foto (71% en mujeres); 91% y 83% con cinco fotos. Humanos: 61% y 54%.

**Crítica 1 — Agüera y Arcas, B., Mitchell, M. & Todorov, A. (2017). "Physiognomy's New Clothes."** Medium.
https://medium.com/@blaisea/physiognomys-new-clothes-f2d4b59fdd6a
- Reconstruye la genealogía: Lavater → Lombroso → Galton → "scientific racism". El deep learning está **reinstalando la fisiognomía** con vocabulario de ML.
- Demolición del paper de Wu & Zhang sobre "predecir criminalidad desde el rostro": el clasificador aprendió que los no-criminales **sonreían** en las fotos.
- Punto metodológico general: un clasificador con alta accuracy sobre un dataset sesgado no descubre una regularidad natural; **descubre el sesgo de construcción del dataset**.

**Crítica 2 — Agüera y Arcas, B., Todorov, A. & Mitchell, M. (2018). "Do algorithms reveal sexual orientation or just expose our stereotypes?"** Medium.
https://medium.com/@blaisea/do-algorithms-reveal-sexual-orientation-or-just-expose-our-stereotypes-d998fafdf477
- Replicaron gran parte del rendimiento del clasificador usando **sólo señales de auto-presentación**: uso de anteojos, vello facial, maquillaje, ángulo de la cámara, encuadre, tono de la imagen.
- Es decir: el modelo no detecta orientación sexual, detecta **decisiones de estilo y de plataforma** correlacionadas con la orientación **en ese corpus** (fotos de sitios de citas de EE.UU., mayoritariamente blancos).
- Corolario: se transporta mal a otra cultura, otra plataforma u otro año.

**Crítica 3 — el problema de la tasa base.** Gelman, A., Mattson, G. & Simpson, D., **"Gaydar and the fallacy of decontextualized measurement"**, *Sociological Science* 5: 270-280 (2018). https://sociologicalscience.com/download/vol-5/may/SocSci_v5_270to280.pdf
- Los experimentos usan corpus **balanceados 50/50**. En la población real la prevalencia ronda el 3-7%.
- Con 91% de sensibilidad y especificidad sobre una prevalencia del 5%, la mayoría de las alarmas positivas son **falsos positivos**. Se requerirían razones de verosimilitud del orden de 20:1 para que la clasificación sea pragmáticamente útil, y **ningún estudio las alcanza**.
- Un clasificador "muy preciso" en el laboratorio produce, desplegado, un aluvión de etiquetas erróneas sobre personas reales.

**Crítica 4 — Kate Crawford (AI Now):** el trabajo es "AI phrenology, and it's very, very dangerous". Ver también el estudio de caso de Data & Society: https://datasociety.net/wp-content/uploads/2018/09/AI-Systems-and-Research-Revealing-Sexual-Orientation_Case-Study_Final.pdf

**Crítica 5 — daño aun si funcionara.** El principal riesgo no es el error: es el **acierto**. Un clasificador que funcione es una herramienta de persecución en los ~60 países donde la homosexualidad es delito. El paper no tenía consentimiento de las personas fotografiadas.

### 4.4 Sesgo demográfico en visión por computadora

**Buolamwini, J. & Gebru, T. (2018). "Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification."** *Proceedings of Machine Learning Research* 81 (FAT* 2018), 77-91.
https://proceedings.mlr.press/v81/buolamwini18a.html · Proyecto: http://gendershades.org/
Auditoría de los clasificadores de género comerciales de Microsoft, IBM y Face++ sobre el benchmark PPB, estratificado por tono de piel (escala Fitzpatrick) y género:
- Hombres de piel clara: error **≤0,8%**.
- Mujeres de piel oscura: error de hasta **34,7%** (IBM), **~20,8%** (Microsoft).
- Brecha de hasta **34,4 puntos** entre el mejor y el peor subgrupo.
Lección central: **la accuracy agregada esconde la falla.** Un sistema "95% preciso" puede ser inservible y dañino para un subgrupo específico.
Seguimiento: Raji, I.D. & Buolamwini, J. (2019), "Actionable Auditing", AIES.
Contexto argentino: la población destinataria de un negocio en La Pampa o el conurbano **no** se parece a los benchmarks sobre los que se entrenaron esos modelos.

**Birhane, A. & Prabhu, V.U. (2021). "Large image datasets: A pyrrhic win for computer vision?"** WACV 2021.
https://arxiv.org/abs/2006.16923 · https://openaccess.thecvf.com/content/WACV2021/html/Birhane_Large_Image_Datasets_A_Pyrrhic_Win_for_Computer_Vision_WACV_2021_paper.html
Auditoría de ImageNet-ILSVRC-2012 y 80 Million Tiny Images:
- Categorías con **insultos raciales y misóginos** heredados de WordNet.
- **Imágenes pornográficas y no consentidas** dentro de datasets de uso general.
- Imágenes obtenidas por scraping **sin consentimiento** de las personas retratadas, con problemas de justicia distributiva (las personas retratadas no obtienen nada; los costos del error recaen sobre ellas).
- Consecuencia directa: MIT **retiró** 80 Million Tiny Images en 2020 e ImageNet purgó categorías de personas.
Corolario: **cualquier modelo de visión preentrenado que se use hereda estas patologías.** Un clasificador de "estilo de vida" o "nivel socioeconómico" sobre fotos está construido encima de ellas.

Complementos: Birhane, Prabhu & Kahembwe (2021) sobre LAION-400M (https://arxiv.org/abs/2110.01963); Buolamwini, *Unmasking AI* (2023); NIST FRVT Part 3, "Demographic Effects" (NISTIR 8280, 2019).

### 4.5 El daño específico de inferir atributos protegidos
1. **Outing involuntario** — orientación sexual, identidad de género, estatus de salud, estatus migratorio, condena previa.
2. **Codificación y amplificación del estereotipo** — el sistema aprende el prejuicio del corpus y lo devuelve con autoridad numérica; el número lava el prejuicio ("mathwashing").
3. **Asimetría de errores** — los falsos positivos y negativos no se reparten al azar: se concentran en los grupos ya marginados (Gender Shades).
4. **Falta de recurso** — la persona no sabe que fue perfilada, no sabe qué dice el perfil y no puede corregirlo. Choca con arts. 14/16 LPDP y arts. 15/16/21/22 GDPR.
5. **Efecto inhibitorio (chilling effect)** — la percepción de vigilancia altera lo que la gente publica.
6. **Riesgo de reuso y filtración** — una base construida "para marketing" puede ser subpoenada, hackeada, vendida en una quiebra, o repropósitada por un empleado. El único control robusto es **no crear el campo**.

---

## 5. EL ARGUMENTO DE LA EXACTITUD: POR QUÉ CORRESPONDE HUMILDAD

### 5.1 La brecha entre exactitud declarada y exactitud real
Cinco mecanismos sistemáticos que inflan la accuracy reportada:

1. **Corpus balanceados vs. tasas base reales.** (§4.3) Un AUC alto sobre 50/50 se derrumba con prevalencia del 5%.
2. **Confusión de correlato con causa.** El modelo aprende maquillaje, anteojos, ángulo de cámara, filtro, iluminación — no rasgos estables. (Agüera y Arcas et al.)
3. **Fuga y sobreajuste al dataset.** Fotos del mismo sitio de citas, misma cámara, mismo año, misma cultura. Deployment fuera de esa distribución = colapso.
4. **Accuracy agregada que oculta disparidad por subgrupo.** (Gender Shades: 0,8% vs 34,7%)
5. **Sesgo de publicación.** Se publican los resultados llamativos; las replicaciones fallidas rara vez se publican.

### 5.2 Lo que realmente se puede predecir de la personalidad
- **Meta-análisis** Azucar, Marengo & Settanni (2018), "Predicting the Big 5 personality traits from digital footprints on social media: A meta-analysis", *Personality and Individual Differences* 124: 150-159. https://www.sciencedirect.com/science/article/abs/pii/S0191886917307328
  Correlaciones entre predicción y auto-reporte: **r ≈ .29 (Amabilidad) a r ≈ .40 (Extraversión)**. En términos de varianza explicada: **8% a 16%**. Es decir, **84%-92% de la variación queda sin explicar**.
  Además: **sólo 4 de 28 estudios** incluían contenido de imagen, y **sólo uno** era específicamente sobre Instagram. La evidencia para "personalidad desde fotos de IG" es **fina**.
- Estudios sobre Instagram: los juicios de observadores humanos sobre perfiles de IG convergen con los rasgos reales entre **r = .25 (Responsabilidad)** y **r = .44 (Extraversión)** — mejor que el azar, lejos de ser diagnóstico.
- **Todorov, A. (2017). *Face Value: The Irresistible Influence of First Impressions.*** Princeton University Press. https://press.princeton.edu/books/hardcover/9780691167497/face-value
  Tesis central: "The character judgments we make from faces are **as inaccurate as they are irresistible**; in most situations, we would guess more accurately if we ignored faces." Los rostros no son un mapa de la personalidad ajena: **son un mapa de nuestros propios sesgos y estereotipos**. Y: "The judgments might be accurate here and now, but they're very, very lousy guides of what the person is like across time and situations."

### 5.3 El costo asimétrico de un perfil equivocado
- **Para el negocio:** un lead mal calificado cuesta un email desperdiciado. El error es barato y recuperable.
- **Para la persona:** ser etiquetada como "de bajo poder adquisitivo", "poco confiable", "conflictiva", "probablemente X" tiene consecuencias que no puede ver ni impugnar. El error es caro e invisible.
- **Esa asimetría es el argumento decisivo:** cuando el que se beneficia de la inferencia no es el que paga por el error, el umbral de confianza exigido debe subir drásticamente. Con r = .3 no se toman decisiones sobre personas; se generan hipótesis para verificar hablando con ellas.
- **Regla práctica derivada:** el sistema nunca debe emitir una etiqueta cuyo error, en manos de un operador humano apurado, produzca un trato peor a una persona real.

---

## 6. DISEÑO PRÁCTICO DE GUARDRAILS

### 6.1 Taxonomía RED / AMBER / GREEN

#### 🔴 RED — RECHAZAR SIEMPRE. Sin excepción, sin flag de configuración, sin "modo avanzado".
El agente debe negarse y explicar por qué. Estos campos **no deben existir en el esquema de datos**.

| # | Regla | Fundamento |
|---|---|---|
| R1 | **Nunca inferir ni almacenar origen racial o étnico, ni tono de piel como atributo de la persona.** | LPDP art. 2 y 7.3; GDPR art. 9; AI Act art. 5(1)(g); Ley 23.592 |
| R2 | **Nunca inferir ni almacenar religión o convicciones filosóficas** (ni por proxies: velo, kipá, cruz, altar, saludo religioso). | LPDP art. 7.3 ("directa o indirectamente revele") |
| R3 | **Nunca inferir ni almacenar opinión política, ideología ni afiliación sindical** (ni por proxies: marchas, banderas, colores partidarios, hashtags). | LPDP art. 7.3; GDPR art. 9; AI Act art. 5(1)(g) |
| R4 | **Nunca inferir ni almacenar orientación sexual, identidad de género ni vida sexual.** | LPDP art. 7.3; TJUE C-184/20; AI Act art. 5(1)(g); caso Kosinski |
| R5 | **Nunca inferir ni almacenar salud, discapacidad, embarazo, salud mental, adicciones ni uso de sustancias.** | LPDP art. 7.3; GDPR art. 9 |
| R6 | **Nunca inferir ni almacenar antecedentes penales, "criminalidad", "confiabilidad" ni "peligrosidad".** | LPDP art. 7.4; "Physiognomy's New Clothes" |
| R7 | **Nunca inferir estatus migratorio ni nacionalidad de origen.** | LPDP art. 7; Ley 23.592 |
| R8 | **Nunca perfilar personas que parezcan menores de 18.** Si hay señal de minoridad → abortar y descartar todo lo procesado de esa cuenta. | Ley 26.061 art. 22; GDPR art. 8; IG ToU (13 años) |
| R9 | **Nunca ejecutar reconocimiento facial, face embeddings, matching de rostros entre cuentas ni estimación de emociones a partir del rostro.** | Res. AAIP 4/2019 crit. 4; GDPR art. 9; AI Act art. 5(1)(f); Clearview |
| R10 | **Nunca descargar ni almacenar imágenes de personas identificables.** Analizar en memoria, persistir sólo texto derivado no sensible; para mostrar, usar oEmbed o permalink. | CCyCN art. 53; Platform Terms |
| R11 | **Nunca perfilar a un particular (cuenta personal, no comercial) para vigilancia, dossier, targeting individual, evaluación de empleo/crédito/alquiler, o por encargo de un tercero interesado en esa persona.** | LPDP arts. 4.3 y 20; GDPR art. 22; Meta Platform Terms (surveillance / eligibility) |
| R12 | **Nunca scrapear con cuentas falsas, sesiones automatizadas, credenciales ajenas, evasión de CAPTCHA/rate limit o acceso a contenido no público.** | LPDP art. 4.2 ("medios desleales"); IG ToU; Automated Data Collection Terms; Meta v. Voyager Labs / Octopus |
| R13 | **Nunca vender, ceder, licenciar ni publicar la base de perfiles ni los perfiles individuales.** | LPDP art. 11; Automated Data Collection Terms; Platform Terms |
| R14 | **Nunca inferir estimaciones de ingresos, patrimonio o solvencia individual a partir de la estética de las fotos.** | LPDP arts. 4.1/4.3; Platform Terms (eligibility determinations); §5 |
| R15 | **Nunca producir juicios de valor sobre el cuerpo, el atractivo, el peso, la edad exacta o la apariencia de una persona.** | CCyCN art. 52 (dignidad); AoIR IRE 3.0 |
| R16 | **Nunca presentar una inferencia como si fuera un hecho verificado, ni omitir la incertidumbre.** | LPDP art. 4.4 (exactitud); Res. AAIP 4/2019 crit. 2 |

#### 🟡 AMBER — PERMITIDO SÓLO CON EVIDENCIA CITADA, INCERTIDUMBRE EXPLÍCITA Y REVISIÓN HUMANA
Cada afirmación AMBER debe salir con: **(a)** la evidencia concreta que la sostiene (post + fecha + qué se vio), **(b)** un nivel de confianza calibrado, **(c)** la hipótesis alternativa, **(d)** marca visible de "no verificado".

| # | Inferencia permitida bajo condiciones |
|---|---|
| A1 | **Rubro, categoría de negocio y surtido probable** — a partir de productos visibles y captions. Ej.: "Probable venta de bazar y textil de hogar (confianza media): 7 de los últimos 20 posts muestran acolchados y juegos de sábanas". |
| A2 | **Tamaño y madurez aproximados del negocio** — a partir de seguidores, frecuencia de publicación, presencia de local físico visible, cantidad de empleados que aparecen. Siempre en rangos, nunca en cifras. |
| A3 | **Ubicación aproximada de la operación comercial** — sólo si el propio negocio la publica (dirección del local, tag de ciudad, mención en bio). **Nunca** inferir domicilio particular ni geolocalizar a una persona. |
| A4 | **Nivel de posicionamiento de precio del comercio** (económico / medio / premium) — a partir de precios efectivamente publicados o marcas exhibidas. Nunca extrapolado a la persona dueña. |
| A5 | **Estilo visual y tono de marca** (paleta, calidad de foto, formalidad del copy) — como observación descriptiva, no como juicio de calidad de la persona. |
| A6 | **Estacionalidad y calendario comercial** (qué promociona y cuándo). |
| A7 | **Canales y modalidad de venta declarados** (WhatsApp, envíos, retiro en local, MercadoLibre) — cuando figuran en bio o posts. |
| A8 | **Señales de intención de compra B2B** (publica "buscamos proveedor", "reponemos stock", "mayorista"). |
| A9 | **Idioma y registro de comunicación.** |
| A10 | **Rango etario amplio del público al que apunta el comercio** — sólo del *segmento comercial*, nunca de personas individuales, y nunca a partir de rostros. |

Regla transversal AMBER: **si para sostener la inferencia hay que mirar el cuerpo o la cara de alguien, no es AMBER: es RED.**

#### 🟢 GREEN — PERMITIDO LIBREMENTE
Datos **publicados explícitamente por la propia cuenta** para fines comerciales, y métricas objetivas provistas por la API oficial.

| # | Dato |
|---|---|
| G1 | Handle, nombre público, categoría declarada, bio literal, link en bio. |
| G2 | Métricas públicas de la API: `followers_count`, `media_count`, `like_count`, `comments_count`, `timestamp`. |
| G3 | Texto literal de captions y hashtags publicados por la cuenta. |
| G4 | Datos de contacto **comercial** publicados por el propio negocio: teléfono comercial, email de contacto, dirección del local, web. |
| G5 | Frecuencia de publicación, horarios habituales, ratio de formatos (feed/reel/carrusel). |
| G6 | Productos, precios y promociones **explícitamente publicados** en la imagen o el caption. |
| G7 | Marcas, proveedores y colaboraciones que la cuenta menciona o taggea. |
| G8 | Permalinks y embeds oficiales (oEmbed) para referenciar contenido sin copiarlo. |
| G9 | Métricas y contenido de **la propia cuenta** del usuario del sistema. |
| G10 | Agregados estadísticos **disociados** sobre un conjunto de cuentas (art. 2 y 28 LPDP), sin identificadores. |

### 6.2 Reglas de arquitectura y proceso

**Fuente y acceso**
1. **Jerarquía de fuentes:** (1) API oficial de Meta → (2) oEmbed → (3) observación manual asistida → (4) *nada*. No hay opción 5.
2. **Sólo cuentas profesionales** (Business/Creator). Si Business Discovery no devuelve la cuenta porque es personal, **eso es la respuesta**: no perfilar.
3. **Respetar rate limits, robots.txt y toda señal de exclusión.** Nunca autenticarse con credenciales de terceros ni con cuentas creadas para scrapear.

**Objeto del perfilado**
4. **Preferir la CUENTA/MARCA sobre la PERSONA.** El sujeto legítimo es la unidad comercial. Si el sistema no puede distinguir un negocio de una persona, debe asumir **persona** y detenerse.
5. **Clasificador de tipo de cuenta al inicio del pipeline**, con umbral conservador: `comercial | personal | ambiguo | menor`. Sólo `comercial` avanza.

**Evidencia y calibración**
6. **Toda afirmación no-GREEN lleva cita obligatoria:** `[permalink, fecha, qué se observó]`. Sin evidencia citable, la afirmación no se emite.
7. **Confianza calibrada y verbalizada**, en tres niveles con significado operativo:
   - *alta* (≈>80%): múltiples posts independientes y recientes lo sostienen.
   - *media* (≈50-80%): evidencia parcial, admite lectura alternativa.
   - *baja* (<50%): se emite **sólo** si el operador la pidió explícitamente, y con la alternativa explicitada.
8. **Publicar siempre la hipótesis alternativa** en AMBER: "También compatible con: …".
9. **Prohibida la precisión falsa.** Nada de "Extraversión: 7,3/10". Rangos y lenguaje natural.

**Minimización y retención**
10. **Minimización por diseño:** recolectar sólo los campos que una decisión comercial concreta requiere. Si no se sabe qué decisión alimenta un campo, no se recolecta (LPDP art. 4.1).
11. **Retención acotada:** perfiles derivados **90 días** desde la última interacción comercial, salvo relación contractual activa; imágenes **0 días** (nunca persistidas); logs de acceso 12 meses. Purga automática, no manual (LPDP art. 4.7; Platform Terms §3(d)).
12. **Sin enriquecimiento cruzado** con otras fuentes (padrones, filtraciones, brokers de datos). La agregación es la que crea el daño.

**Derechos y contestabilidad**
13. **Página pública de transparencia**: quién es el responsable, qué datos se tratan, con qué finalidad, de qué fuente, cuánto se conservan, cómo ejercer derechos (LPDP art. 6).
14. **Canal de derechos operativo** con SLA que cumpla la ley: **acceso 10 días corridos** (art. 14), **rectificación/supresión 5 días hábiles** (art. 16), **opt-out inmediato de la base publicitaria** (art. 27).
15. **Búsqueda por handle** que permita exportar, corregir y borrar un perfil completo en un solo paso. Si el sistema no puede hacerlo, no cumple la ley — es un requisito de arquitectura, no una feature.
16. **Human-in-the-loop obligatorio** antes de cualquier acción con efecto sobre la persona o el negocio (contacto, priorización, condiciones comerciales). Ningún perfil puede ser el **único** fundamento de una valoración (LPDP art. 20; GDPR art. 22(3)).
17. **Registro de la base ante el RNBD de la AAIP** (art. 21) y declaración veraz de la naturaleza de los datos tratados.

**Operación y auditoría**
18. **Log de decisiones**: para cada perfil, qué fuentes se consultaron, qué se infirió, con qué confianza y qué evidencia. Trazabilidad exigida por la Guía de IA de la AAIP.
19. **Lista de negación en el código**, no en el prompt: un filtro de salida que bloquee campos y vocabulario RED aunque el modelo los genere.
20. **Revisión periódica de deriva**: muestreo trimestral de perfiles verificados contra realidad; si la precisión de una categoría AMBER cae por debajo de lo declarado, se degrada o se elimina la categoría.
21. **No usar el sistema sobre un objetivo definido por un tercero interesado en esa persona.** Si alguien pide "perfilame a esta persona", es RED (R11).

### 6.3 Guion de rechazo para el agente
Cuando llegue un pedido RED, el agente debe: (1) negarse explícitamente; (2) nombrar la norma concreta (ej.: "el art. 7.3 de la Ley 25.326 prohíbe formar archivos que directa o indirectamente revelen datos sensibles"); (3) explicar el riesgo real (multa AAIP, nulidad, daño a la persona, exactitud inexistente); (4) **ofrecer la alternativa legítima** ("puedo analizar el rubro, el surtido y la frecuencia de publicación de la cuenta comercial, que es lo que sirve para decidir si es un buen prospecto"). El rechazo sin alternativa hace que el operador busque otra herramienta peor.

---

## 7. CHECKLIST DE CUMPLIMIENTO PARA UNA PyME ARGENTINA

- [ ] Perfilar **cuentas comerciales**, no personas físicas privadas.
- [ ] Usar **API oficial (Business Discovery + oEmbed)**; nada de scraping automatizado, nunca cuentas falsas.
- [ ] **No almacenar imágenes**; sólo texto derivado y permalinks.
- [ ] **Cero campos sensibles** en el esquema de la base (no basta con no mostrarlos: no deben existir).
- [ ] Encuadrar el tratamiento en el **art. 27 LPDP** (fines publicitarios/comerciales, fuente accesible al público) con **opt-out** funcionando.
- [ ] **Inscribir la base** en el RNBD de la AAIP.
- [ ] Publicar **política de privacidad** conforme al art. 6 LPDP con canal de derechos.
- [ ] Cumplir SLA: **10 días corridos** acceso, **5 días hábiles** rectificación/supresión.
- [ ] Política de **retención y purga automática** documentada.
- [ ] **Revisión humana** antes de todo contacto o decisión comercial.
- [ ] Identificarse en cada comunicación comercial, informar el origen de los datos y ofrecer baja.
- [ ] **Documentar el análisis de proporcionalidad**: qué se trata, para qué, por qué no hay medio menos intrusivo. Es la defensa si la AAIP pregunta.
- [ ] Si hay algún destinatario en la UE: aplicar el estándar GDPR completo (bases, DPIA, arts. 13-22).

---

## 8. FUENTES

**Argentina**
- Ley 25.326 (texto actualizado) — https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm
- Decreto 1558/2001 — https://servicios.infoleg.gob.ar/infolegInternet/anexos/70000-74999/70368/norma.htm
- Código Civil y Comercial, art. 53 — https://leyes-ar.com/codigo_civil_y_comercial/53.htm
- Ley 26.061, art. 22 — https://servicios.infoleg.gob.ar/infolegInternet/anexos/110000-114999/110778/norma.htm
- AAIP Res. 4/2019 (norma) — https://servicios.infoleg.gob.ar/infolegInternet/anexos/315000-319999/318874/norma.htm — (Anexo I) https://servicios.infoleg.gob.ar/infolegInternet/anexos/315000-319999/318874/res4AAIP.pdf
- AAIP Res. 255/2022 — https://www.boletinoficial.gob.ar/detalleAviso/primera/277889/20221216
- AAIP — Programa Nacional de Transparencia y PDP en IA (Res. 161/2023) — https://www.argentina.gob.ar/programa-nacional-de-transparencia-y-proteccion-de-datos-personales-en-el-uso-de-la-inteligencia
- AAIP — Documentos de Inteligencia Artificial / Guía IA responsable (2024) — https://www.argentina.gob.ar/aaip/documentos-de-inteligencia-artificial
- AAIP — Obligaciones de los responsables — https://www.argentina.gob.ar/aaip/datospersonales/responsables/obligaciones
- AAIP — Proyecto de Ley de PDP — https://www.argentina.gob.ar/aaip/datospersonales/proyecto-ley-datos-personales
- Proyecto 1751-D-2026 (Yeza) — https://leydedatospersonales.tech/
- Marval — Nuevos proyectos de ley de datos personales — https://www.marval.com/publicacion/nuevos-proyectos-de-ley-de-datos-personales-en-argentina-17289?lang=en
- IAPP — Reforma del régimen de PDP en Argentina — https://iapp.org/news/a/se-impulsa-un-nuevo-proyecto-de-reforma-del-r-gimen-de-protecci-n-de-datos-en-argentina

**Unión Europea / Reino Unido**
- Decisión 2003/490/CE (adecuación Argentina) — https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32003D0490
- Informe de revisión de adecuaciones (15/1/2024) — https://iapp.org/news/a/european-commission-upholds-11-adequacy-decisions
- Carta EDPB sobre la revisión (5/12/2024) — https://www.edpb.europa.eu/system/files/documents/2024-12/edpb_letter_20241205_european-commission-review-of-11-existing-adequacy-decisions_en.pdf
- GDPR art. 4 — https://gdpr-info.eu/art-4-gdpr/ · art. 9 — https://gdpr-info.eu/art-9-gdpr/ · art. 22 — https://gdpr-info.eu/art-22-gdpr/
- WP29 WP251rev.01 (profiling) — https://ec.europa.eu/newsroom/article29/items/612053/en
- EDPB Guidelines 03/2026 web scraping & IA generativa — https://www.edpb.europa.eu/news/edpb-sheds-light-on-anonymisation-and-web-scraping-for-generative-ai-and-adopts-final-version_en
- ICO — Lawful basis for web scraping to train genAI — https://ico.org.uk/about-the-ico/what-we-do/our-work-on-artificial-intelligence/response-to-the-consultation-series-on-generative-ai/the-lawful-basis-for-web-scraping-to-train-generative-ai-models/
- Garante — Provv. n. 329 del 20/5/2024, web scraping e IA generativa — https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10020316
- ICO v Clearview AI [2025] UKUT 319 (AAC) — https://www.gov.uk/administrative-appeals-tribunal-decisions/the-information-commissioners-office-v-clearview-ai-inc-privacy-international-intervening-2025-ukut-319-aac
- AP (NL) multa €30,5M a Clearview — https://www.techmonitor.ai/technology/cybersecurity/dutch-regulator-fines-clearview-ai-e30-5m-over-illegal-facial-recognition-data-collection
- Garante multa €20M a Clearview — https://noyb.eu/en/eu-20-mio-fine-clearview-ai-italy
- AI Act art. 5 — https://artificialintelligenceact.eu/article/5/ · FPF sobre 5(1)(g) — https://fpf.org/blog/red-lines-under-the-eu-ai-act-understanding-the-prohibition-of-biometric-categorization-for-certain-sensitive-characteristics/

**Plataforma y litigios**
- Instagram Terms of Use — https://help.instagram.com/581066165581870
- Meta Automated Data Collection Terms (7/10/2024) — https://www.facebook.com/legal/automated_data_collection_terms
- Meta Platform Terms — https://developers.facebook.com/terms/
- Instagram Platform overview — https://developers.facebook.com/docs/instagram-platform/overview/
- Business Discovery — https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/business-discovery/
- hiQ Labs v. LinkedIn — https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn · https://www.morganlewis.com/blogs/sourcingatmorganlewis/2022/12/linkedin-v-hiq-landmark-data-scraping-suit-provides-guidance-to-data-scrapers-and-web-operators
- Meta v. Bright Data (N.D. Cal., 23/1/2024) — https://www.fbm.com/publications/major-decision-affects-law-of-scraping-and-online-data-collection-meta-platforms-v-bright-data/
- Meta v. Voyager Labs — https://www.cnbc.com/2023/01/12/meta-sues-voyager-labs-over-scraping-user-data.html

**Ética e investigación**
- AoIR, Internet Research: Ethical Guidelines 3.0 — https://aoir.org/reports/ethics3.pdf · https://aoir.org/ire30/
- Zimmer, M. (2010), "But the data is already public" — https://link.springer.com/article/10.1007/s10676-010-9227-5 · https://www.sfu.ca/~palys/Zimmer-2010-EthicsOfResearchFromFacebook.pdf
- Wang & Kosinski (2018), JPSP 114(2):246-257 — https://www.gsb.stanford.edu/sites/gsb/files/publication-pdf/wang_kosinski.pdf
- Agüera y Arcas, Mitchell & Todorov (2017), "Physiognomy's New Clothes" — https://medium.com/@blaisea/physiognomys-new-clothes-f2d4b59fdd6a
- Agüera y Arcas, Todorov & Mitchell (2018), "Do algorithms reveal sexual orientation or just expose our stereotypes?" — https://medium.com/@blaisea/do-algorithms-reveal-sexual-orientation-or-just-expose-our-stereotypes-d998fafdf477
- Gelman, Mattson & Simpson (2018), *Sociological Science* 5:270-280 — https://sociologicalscience.com/download/vol-5/may/SocSci_v5_270to280.pdf
- Data & Society, case study sobre IA y orientación sexual — https://datasociety.net/wp-content/uploads/2018/09/AI-Systems-and-Research-Revealing-Sexual-Orientation_Case-Study_Final.pdf
- Buolamwini & Gebru (2018), "Gender Shades", PMLR 81:77-91 — https://proceedings.mlr.press/v81/buolamwini18a.html · http://gendershades.org/
- Birhane & Prabhu (2021), "Large image datasets: A pyrrhic win for computer vision?" WACV — https://arxiv.org/abs/2006.16923
- Azucar, Marengo & Settanni (2018), *Pers. Individ. Dif.* 124:150-159 — https://www.sciencedirect.com/science/article/abs/pii/S0191886917307328
- Todorov, A. (2017), *Face Value*, Princeton UP — https://press.princeton.edu/books/hardcover/9780691167497/face-value
