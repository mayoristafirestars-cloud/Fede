# 10 — El mercado de herramientas comerciales: analítica de Instagram, inteligencia de audiencia y perfilado por imagen

**Alcance:** relevamiento del mercado *comercial* (no académico) de herramientas que se venden para analizar cuentas de Instagram, auditar creadores, describir audiencias y analizar imágenes sociales. Se evalúa qué venden, qué prometen, qué es verificable, y qué de todo eso sirve y se puede pagar desde una **pyme argentina**.
**Fecha del relevamiento:** agosto 2026. Los precios de SaaS cambian seguido; tomarlos como orden de magnitud, no como cotización.
**Regla que atraviesa el documento:** hay que separar en cada producto lo **MEDIDO** (un contador que la plataforma reporta y que en principio se puede auditar) de lo **INFERIDO** (un modelo estadístico que produce una etiqueta que nadie validó contra un criterio externo). Casi todas las herramientas del mercado mezclan ambas cosas en la misma pantalla, con la misma tipografía y el mismo aire de certeza.

---

## 0. Marco de lectura: MEDIDO vs. INFERIDO vs. ESTIMADO

Antes del catálogo conviene fijar tres categorías, porque el marketing de estos productos las funde deliberadamente.

| Categoría | Qué significa | Ejemplos típicos | Cómo se verifica |
|---|---|---|---|
| **MEDIDO** | Un contador registrado por la plataforma dueña del dato y devuelto por su API oficial. | reach, views, likes, comments, saves, shares, profile_views, follower_count, seguidores por ciudad/edad/género declarados por Meta | Se contrasta con la app de Instagram. Si la herramienta y la app coinciden, está midiendo. |
| **ESTIMADO** | Un cálculo sobre datos públicos raspados, sin acceso al backend. No es fantasía, pero tiene error y sesgo de muestreo. | engagement rate de la competencia (likes+comments / seguidores), "mejor horario", % de audiencia por país de un influencer que no te dio acceso, alcance estimado de un post ajeno | Se valida sólo si conseguís el dato real de la cuenta analizada. Casi nunca pasa. |
| **INFERIDO** | Una etiqueta psicológica, de personalidad, de intención, de emoción o de identidad producida por un modelo. | "tu audiencia es Openness alta", "este seguidor es un bot", "esta cara expresa alegría", "perfil DISC: Dominante", segmentos psicográficos | Requiere validación externa publicada: correlación con un instrumento de referencia, tasa de falsos positivos, estabilidad test-retest. **La enorme mayoría de los vendors no publica ninguna.** |

La única inferencia de este mercado con base técnica razonable y verificable en principio es la **detección de seguidores falsos** (sección 4), porque tiene un criterio externo posible: la cuenta o existe o no, se compró o no, y las purgas de Instagram funcionan como ground truth parcial. Todo lo demás — personalidad, emoción, psicografía — carece de criterio externo accesible, y ahí es donde el mercado vende con más confianza.

---

## 1. LA FUENTE PRIMARIA: Instagram Insights y la Graph API

Cualquier herramienta de terceros que analice **tu propia** cuenta es, en el fondo, un envoltorio sobre la misma API de Meta. Entender qué expone esa API define el techo real de todo el mercado.

### 1.1 Requisitos de acceso

- Cuenta **profesional** (Business o Creator). Las cuentas personales no exponen insights. (Meta: "This API returns only data for media owned by Instagram professional accounts".)
- Token OAuth con `instagram_manage_insights` (más `instagram_basic`, `pages_read_engagement` según flujo).
- Se consulta **una sola cuenta por vez, la propia**. No existe endpoint para pedir los insights de una cuenta ajena. Este es el hecho estructural más importante de toda la sección de "análisis de competencia".

### 1.2 Métricas a nivel de cuenta (MEDIDO)

- `reach` (cuentas alcanzadas), `views` (vistas), `profile_views`, `accounts_engaged`, `total_interactions`, `website_clicks` / `profile_links_taps`, `follower_count`.
- **Demografía**: `follower_demographics`, `engaged_audience_demographics`, `reached_audience_demographics`, con `breakdown` por `age`, `gender`, `city`, `country`.
- Meta unificó la métrica de exposición en `views`, dejando `impressions` deprecada en versiones recientes de la API (v22+). Cualquier herramienta que todavía te muestre "impresiones" para Instagram está mostrando un dato heredado o reconstruido.

### 1.3 Métricas a nivel de publicación (MEDIDO)

`likes`, `comments`, `saved`, `shares`, `reach`, `views`, `total_interactions`, `profile_visits` y `follows` originados en el post, `navigation` para stories (exits, taps forward/back, replies).

**`saved` y `shares` son las dos métricas comercialmente más informativas y las que ninguna herramienta externa puede estimar sobre una cuenta ajena.** Son privadas: no aparecen en el HTML público del post. Esto tiene una consecuencia directa para cualquier sistema de perfilado por scraping: el guardado y el compartido, que son las señales de intención de compra más fuertes, son estructuralmente inaccesibles fuera de la cuenta propia.

### 1.4 Los límites, que son severos

| Límite | Detalle | Consecuencia práctica |
|---|---|---|
| **Mínimo de seguidores** | La demografía de seguidores no se devuelve por debajo de **100 seguidores**. | Un negocio chico recién arrancando no tiene demografía. Punto. |
| **Top 45 segmentos** | Cada breakdown demográfico se corta en los **45 segmentos principales** (top 45 ciudades, etc.). | La cola larga geográfica no existe. Para Argentina, se ven CABA, GBA y capitales; los pueblos desaparecen. |
| **Retención de datos** | Métricas de usuario ~**90 días**; métricas de media, más largas (del orden de 2 años, según integradores). | Cualquier serie histórica más larga que 90 días la tiene que acumular la herramienta de terceros, no Meta. Esto explica por qué "historial ilimitado" es un feature de pago: es almacenamiento propio del vendor. |
| **Latencia demográfica** | Hasta ~48 h de retraso en métricas demográficas. | No sirve para reaccionar en el día. |
| **Búsqueda por hashtag** | 30 hashtags únicos por ventana móvil de 7 días por cuenta. | Mata cualquier estrategia de monitoreo amplio de hashtags con un solo app token. |
| **Rate limits** | Presupuesto por hora por app/cuenta (`acc_id_util_pct`); a 80-90% hay que hacer backoff. | Un sistema que recorra muchas cuentas necesita colas y reintentos, no consultas ad hoc. |
| **Sin insights ajenos** | No hay endpoint. | Ver 1.5. |

### 1.5 Lo único que la API oficial da sobre cuentas ajenas: `business_discovery`

El endpoint `business_discovery` permite consultar, desde tu propia cuenta profesional, datos **públicos** de otra cuenta profesional: `followers_count`, `media_count`, y la lista de medios con `caption`, `like_count`, `comments_count`, `timestamp`, `media_url`, `permalink`.

Lo que **no** da: reach, saves, shares, profile views, demografía de la audiencia ajena, ni ninguna métrica privada. También hay cuotas y requiere app revisada por Meta.

**Traducción:** todo análisis de competencia legítimo se construye sobre cuatro números públicos —seguidores, cantidad de posts, likes, comentarios— más el contenido de la imagen y el texto. Todo lo demás que te muestre una herramienta sobre un competidor es **estimación**, no medición. Es el punto que ninguna landing page dice con esta claridad.

### 1.6 Herramientas gratuitas de Meta

- **Instagram Insights in-app / Professional Dashboard**: gratis, en español, cubre reach, views, interacciones, saves, shares, demografía de seguidores y de audiencia alcanzada. Es la fuente más exacta que existe para tu propia cuenta.
- **Meta Business Suite**: gratis, agrega planificación, bandeja unificada IG+FB, y comparación básica de "páginas en observación" (que en Facebook da algo de benchmark, en Instagram es más pobre).
- **Instagram Creator Marketplace**: desde 2024 disponible en Argentina y, según reportes de 2026, abierto globalmente sin lista de países. Permite a marcas buscar creadores y ver métricas **declaradas por el propio creador con su consentimiento** — es decir, datos MEDIDOS con permiso, el camino ético por excelencia para vetting.

> **Conclusión de la sección 1:** para una pyme argentina, el 70% del valor analítico está gratis, en español, dentro de la app. Lo que se paga a terceros es: (a) historial más largo que 90 días, (b) comparación con competencia, (c) reportes presentables, (d) programación de contenido. Nadie vende métricas propias mejores que las de Meta, porque nadie las tiene.

---

## 2. HERRAMIENTAS DE ANALÍTICA Y AUDITORÍA DE CUENTA (terceros)

Precios de referencia a agosto 2026, plan mensual salvo aclaración. Todos facturan en USD/EUR salvo indicación.

| Herramienta | Precio de entrada | Techo típico | Español | Qué agrega de verdad | Advertencias |
|---|---|---|---|---|---|
| **Metricool** (España) | **Free** real (1 marca, ~50 posts/mes, 30 días de histórico, 5 competidores) | Starter desde ~USD 20-25/mes; Advanced ~USD 53-67/mes | **Sí, nativo** (empresa española, soporte, blog y academia en español) | Historial ilimitado, hasta 100 competidores, informes PDF/PPT, conector Looker Studio, integración Canva, Ads de Google y Meta en el mismo panel | X/Twitter es add-on pago (~USD 10/mes desde jul-2026). El plan Free es el mejor del mercado para un negocio chico. |
| **Later** (Canadá/EEUU) | Starter USD 25/mes (USD 18,75 anual) | Scale USD 110/mes | Interfaz en inglés | Planificación visual, "best time to post", link-in-bio | **Análisis de competencia sólo desde el plan Scale (USD 110/mes, hasta 20 competidores)**. Los planes baratos no benchmarkean. Histórico: 3 meses en Starter. |
| **Iconosquare** (Francia) | Launch €33/mes | Excel €116/mes | Parcial | El más orientado a analítica pura. **Competitor tracking desde Scale (€69); "industry benchmarks" recién en Excel (€116)** | El benchmark de industria, que es lo que uno realmente quiere, está en el plan caro. Retención de datos escalonada (1 año / 2 años / ilimitado) como palanca de precio. |
| **Hootsuite** | Standard USD 99/usuario/mes | Advanced USD 399/usuario/mes | Sí, interfaz en español | Gestión multi-red, aprobaciones, bandeja social | Pasó a modelo **por asiento**: el precio escala con el equipo. Muy caro para el valor analítico que entrega a una pyme. |
| **Sprout Social** | ~USD 199-249/usuario/mes | Enterprise a cotizar | Sí | Reporting corporativo, listening como add-on caro | Fuera de escala para una pyme argentina por un orden de magnitud. |
| **Socialinsider** (Rumania) | ~USD 83-99/mes | Agency USD 199/mes | Inglés | **Especialista en benchmarking**: analítica de perfiles no propios, comparación cross-plataforma, análisis a nivel de post de competidores, benchmarks de industria | Es la herramienta cuyo producto principal es exactamente lo que la sección 3 exige. Precio de entrada alto para una pyme. |

### 2.1 Qué es MEDIDO y qué es ESTIMADO en estas herramientas

- **MEDIDO** (vía API, tu cuenta): reach, views, saves, shares, interacciones, demografía de seguidores, crecimiento. Todas coinciden entre sí porque leen la misma fuente. Si dos herramientas discrepan sobre tu propio reach, una está mal.
- **ESTIMADO** (competencia): engagement rate ajeno, frecuencia de publicación, "mejor horario del competidor", crecimiento de seguidores del competidor (por muestreo periódico del contador público). Razonable como orden de magnitud, no como número exacto.
- **INFERIDO y flojo**: "mejor momento para publicar" calculado sobre tu propio histórico con pocos datos (n chico, confundido con estacionalidad y con el propio algoritmo de distribución); "sentimiento" de los comentarios en español rioplatense, que en general funciona mal con ironía y modismos locales; puntajes compuestos tipo "health score" que suman métricas heterogéneas con pesos que nadie publica.

---

## 3. BENCHMARK Y ANÁLISIS RELATIVO — el requisito duro

La literatura sobre perfilado sostiene que un rasgo visual o métrico **sólo significa algo en relación a una línea de base de su categoría**: un feed con 60% de fotos de producto es normal en indumentaria y anómalo en gastronomía; un engagement de 1,2% es excelente en una marca grande y mediocre en un nano-negocio local. Sin una referencia de categoría, un perfil no es un diagnóstico sino una descripción.

Esto convierte a la fuente de benchmark en un **requisito de arquitectura**, no en un extra. Opciones reales:

### 3.1 Benchmarks publicados y gratuitos (la vía barata y honesta)

- **Rival IQ — Social Media Industry Benchmark Report** (anual, gratuito con registro). En la edición 2026 la mediana de engagement rate de Instagram por post sobre seguidores cae a **0,30%** (desde 0,36% el año anterior, ~17% de caída interanual), con cortes por 18 industrias (~150 marcas por industria). Ejemplos citados: servicios financieros 0,26%, educación superior 2,10%, ONGs 0,56%. Rival IQ opera hoy como subsidiaria bajo la marca Quid y sigue publicando su reporte.
- **Socialinsider**, **Metricool** y **Hootsuite** publican estudios anuales equivalentes con muestras propias.
- **Limitación grave para Argentina:** todas estas muestras son dominantemente norteamericanas y europeas, de marcas medianas y grandes. Un almacén, una distribuidora o un local de indumentaria de Santa Rosa no está en esa población. Usarlas como línea de base absoluta es un error de referencia.

### 3.2 Benchmark comprado (herramientas con benchmarking nativo)

- **Socialinsider** (~USD 99/mes): el más directo. Compara perfiles ajenos entre sí y contra promedios de industria.
- **Iconosquare Excel** (€116/mes): incluye "industry benchmarks".
- **Metricool** (desde el plan Starter, ~USD 20-25): hasta 100 competidores. No entrega un "promedio de industria" prearmado, pero permite **construirse el propio panel de referencia**, que para una pyme local es mejor: 15-25 cuentas comparables reales del mismo rubro y la misma región valen más que una mediana global.
- **Later Scale** (USD 110/mes): hasta 20 competidores.

### 3.3 La recomendación metodológica

Para un negocio argentino, la línea de base útil **no** es "el promedio mundial de retail". Es un **panel propio de 15-30 cuentas comparables** (mismo rubro, misma escala de seguidores, mismo país o región), medido con los cuatro números públicos disponibles (seguidores, posts, likes, comentarios) y actualizado periódicamente. Metricool en plan Starter alcanza para armarlo; hasta se puede hacer con `business_discovery` y una planilla.

**Regla de reporte:** todo indicador de un perfil debe expresarse como *percentil dentro del panel de referencia*, no como valor absoluto ni como adjetivo. "Engagement 1,8%, percentil 70 del panel de 22 cuentas de indumentaria pampeana" es un dato. "Buen engagement" no lo es.

---

## 4. VETTING DE INFLUENCERS Y CREADORES

Es el subsegmento más maduro y el único donde la inferencia tiene una base técnica defendible.

### 4.1 Los jugadores y sus precios

| Plataforma | Precio de entrada (2026) | Notas |
|---|---|---|
| **HypeAuditor** | Basic ~USD 299/mes anual; Pro ~USD 499/mes; Enterprise a cotizar | El más citado en fraude. Ofrece **herramientas gratuitas** de chequeo puntual (fake follower check, informe básico de una cuenta) que para una pyme suelen alcanzar. Tiene blog y contenidos en español, incluida una guía específica de herramientas para Argentina. |
| **Modash** | Essentials ~USD 99-120/mes; Performance ~USD 599/mes | Fuerte en descubrimiento con filtros de audiencia; scoring de autenticidad integrado al flujo de búsqueda. Menos transparente sobre metodología. |
| **Heepsy** | Free / Starter ~USD 49-69/mes; Plus USD 199; Advanced USD 299 | El más barato con profundidad real de descubrimiento. Interfaz y soporte en español (origen español). Bueno para nano/micro influencers LATAM. |
| **Influencity** | ~USD 348-2.108/mes | Español (España). Fuerte en LATAM, pero precio de entrada alto. |
| **Upfluence** | ~USD 478/mes por módulo; setup realista ~USD 1.200/mes, **contrato de 12 meses** | Fuera de escala para pyme. |
| **Favikon, Influencer Hero, Collabstr, IQfluence** | Free tiers y planes bajos | Capa de herramientas más nuevas y baratas; calidad de datos desigual. |

### 4.2 Qué miden realmente

**MEDIDO (si el creador conecta su cuenta o lo hace vía Creator Marketplace):** reach, views, saves, demografía real de seguidores. Este es el camino correcto y el que Meta habilitó justamente para eliminar la estimación.

**ESTIMADO (el caso normal, sin consentimiento del creador):**
- Engagement rate = (likes + comentarios) / seguidores, sobre una muestra de los últimos N posts. Fácil de calcular, fácil de manipular por el creador.
- Demografía de audiencia: se estima **muestreando seguidores públicos** e infiriendo país/idioma/edad/género de sus perfiles. Aquí se acumulan tres errores: sesgo de muestreo (los seguidores públicos y activos no son los seguidores), sesgo del clasificador de género/edad por nombre y foto, y el hecho de que muchos perfiles son marcas, no personas. Los vendors reportan estos porcentajes con un decimal y sin intervalo de confianza.
- Crecimiento histórico: por muestreo periódico del contador público.

**INFERIDO (con base técnica plausible): detección de seguidores falsos.**
La técnica es real y está en la literatura desde hace una década (Cresci et al., *Fame for sale: efficient detection of fake Twitter followers*, 2015, arXiv:1509.04098; y para Instagram, trabajos de detección de cuentas falsas y automatizadas como arXiv:1910.03090). Las señales usadas son razonables: relación seguidores/seguidos anómala, ausencia de foto o biografía, patrones de creación de cuenta en lotes, engagement inconsistente con el alcance, picos de crecimiento sin evento que los explique, comentarios genéricos repetidos, estructura del grafo de seguidores (comunidades densas de cuentas que se siguen entre sí = pods).

### 4.3 Lo declarado vs. lo verificado — la parte incómoda

- **HypeAuditor declara** detectar "más del 95%" de la actividad fraudulenta, incluidos follow/unfollow, pods de comentarios y sorteos en loop, y publica una cifra de **95,5% de detección sobre actividad fraudulenta conocida**. Ese "conocida" hace todo el trabajo: es una tasa de detección sobre un conjunto etiquetado por el propio vendor, no una precisión ni un recall sobre un ground truth independiente. **No hay tasa de falsos positivos publicada.** Un falso positivo es acusar a un creador honesto de comprar seguidores.
- **Influencer Hero declara 99% de exactitud** invocando un modelo académico de estudiantes de doctorado de ETH Zurich. Cifras de ese orden, sin paper, sin dataset y sin matriz de confusión, deben tratarse como marketing.
- **Modash** usa análisis de grafo sobre miles de millones de cuentas; es una aproximación defendible, con documentación metodológica escasa.
- **No encontré ningún estudio independiente y publicado que compare las salidas de estas herramientas sobre el mismo conjunto de cuentas.** Lo que sí es consenso en el sector (y lo admiten hasta los comparadores comerciales) es que **las herramientas discrepan entre sí de forma significativa** sobre las mismas cuentas, porque difieren en señales, umbrales y frecuencia de reentrenamiento. La recomendación que circula —correr dos vendors en paralelo y usar el desacuerdo como información— es un reconocimiento implícito de que ninguna es un oráculo.
- Las estimaciones de prevalencia también son inconsistentes: se citan rangos de 5-15% de seguidores falsos por cuenta, y también análisis de vendors que afirman 37,2% de seguidores con señales de inautenticidad sobre 100.000 cuentas. Esa dispersión (un factor de 3 a 7) es en sí misma la mejor prueba de que no hay una medición estandarizada.

### 4.4 Cómo usarlo bien

1. Correr el chequeo gratuito de HypeAuditor y/o Heepsy sobre el candidato.
2. Tratar el resultado como **una bandera, no como un veredicto**: 8% de seguidores sospechosos no es evidencia de fraude; 45% con un salto de crecimiento en una semana sí amerita conversación.
3. **Pedirle al creador capturas o acceso de sus Insights reales** (reach, saves, shares, demografía). Es gratis, es MEDIDO y es la única forma de salir de la estimación. Un creador serio las da; la negativa es en sí un dato.
4. Preferir el **Creator Marketplace** de Instagram, donde los datos vienen con consentimiento y de la fuente.

---

## 5. INTELIGENCIA DE AUDIENCIA Y PSICOGRAFÍA — el segmento que hay que interrogar

Aquí es donde la línea entre medición y adivinación se cruza con más elegancia visual.

### 5.1 El dato madre: IBM Watson Personality Insights fue DISCONTINUADO

Prácticamente todo el vocabulario comercial de "psicografía desde texto social" (Big Five / OCEAN inferido de posteos, "necesidades" y "valores" del consumidor) desciende de un solo producto: **IBM Watson Personality Insights**.

- **No se pudieron crear instancias nuevas desde el 1 de diciembre de 2020.**
- **Las instancias existentes dejaron de estar soportadas el 1 de diciembre de 2021.**
- **Razón declarada por IBM:** el servicio llevaba años congelado ("PI has been a frozen service for several years and for that reason, we have chosen to sunset it"). IBM no ofreció reemplazo directo; derivó a Watson Natural Language Understanding, que hace keywords, categorías, sentimiento y emoción — **no personalidad**.

Esto es extraordinariamente informativo. La empresa que más recursos había puesto en convertir la inferencia de personalidad desde texto en un producto de nube lo **apagó**, y no lo reemplazó por nada equivalente. El nicho no fue reemplazado por un producto mejor: fue abandonado. Cuando un vendor de 2026 vende "personalidad de tu audiencia", está vendiendo una categoría de producto que su principal proveedor tecnológico deprecó hace un lustro.

### 5.2 Audiense: el caso testigo

**Audiense Insights** construyó su propuesta de valor psicográfica **explícitamente sobre Watson Personality Insights**, con partnership y material de marketing dedicado ("Maximize the value of Watson Personality Insights from IBM"). Cinco años después de que IBM apagara el servicio, la documentación y el material comercial de Audiense **siguen refiriendo la integración con IBM Watson para perfilado psicográfico**. Sea porque migraron a un modelo propio sin cambiar el relato, sea porque el contenido quedó desactualizado, el efecto para el comprador es el mismo: **la promesa se sostiene sobre una lineage tecnológica que ya no existe, y nadie publicó qué la reemplazó ni con qué validación.**

Otros datos de Audiense:
- Su materia prima histórica es el grafo de **Twitter/X**. Con el cierre y encarecimiento del acceso a la API de X desde 2023, la base sobre la que se construyen los segmentos quedó comprometida en cobertura y frescura. Para audiencias **argentinas de Instagram**, X es una proxy pobre: distinta población, distinta escala.
- Precio: planes de Audience Intelligence del orden de **USD 12.000/año (Base) a USD 28.750/año (Unlimited)**; plan gratuito limitado a 3 reportes de muestra por mes sobre 10.000 miembros de audiencia y 3 segmentos.
- Audiense fue **adquirida por Buxton en marzo de 2025**.

**Veredicto:** inferencia no validada, con precio enterprise, sobre una fuente de datos que no es la red que le importa a un negocio argentino. No usar.

### 5.3 SparkToro: el contraejemplo honesto

SparkToro merece mención separada porque hace lo contrario.

- **Fuentes declaradas:** datos de *clickstream* de paneles grandes (vía Datos) más perfiles públicos de LinkedIn y perfiles sociales. No pretende leer mentes: describe **a qué le presta atención** una audiencia (sitios, podcasts, cuentas, subreddits, canales de YouTube).
- **Autolimitación explícita y publicada.** Literalmente en su FAQ de exactitud: *"it is directional rather than exact: it is excellent for spotting patterns, comparing options, and prioritizing where to focus, and it is not meant to be a precise census of every person"*; *"Results reflect the people represented in the clickstream panels and public profile data we use, so they approximate a real audience rather than capturing every individual in it"*. Reconoce que las audiencias nicho dan resultados más ruidosos y que la cobertura varía por tema, región y plataforma, y recomienda **validar las decisiones de alto riesgo contra datos propios de primera parte**.
- **Nunca describe individuos, sólo grupos.**

Ese es exactamente el estándar de honestidad que el resto del segmento no cumple. **Limitación para Argentina:** los paneles de clickstream tienen cobertura fuerte en EEUU y débil en el interior de Argentina; para un negocio local el output va a ser ruidoso o vacío.

### 5.4 Helixa (hoy TelmarHelixa)

- Fusiona un panel de Twitter con encuestas sindicadas establecidas (**MRI-Simmons**, GfK) y pondera cada persona construida para **reflejar la población de EEUU**.
- Esto es metodológicamente más serio que la mayoría: hay data fusion contra un panel de consumo con muestreo probabilístico conocido. Pero: (a) la ponderación es a población estadounidense, (b) sigue apoyándose en Twitter, (c) "psicografía" aquí significa afinidades e intereses agregados, no rasgos de personalidad medidos.
- Es enterprise, sin precio público, y **estructuralmente inaplicable a Argentina** porque su marco de referencia es el consumidor de EEUU.

### 5.5 Brandwatch Consumer Research

- Precio reportado por terceros: **desde ~USD 800/mes hasta USD 15.000+/mes**, siempre por cotización, contratos anuales, sin free tier. El costo escala con menciones monitoreadas, queries activas y usuarios.
- Lo que hace bien es MEDIDO/agregado: volumen de menciones, share of voice, picos temporales. Lo que hace mal o sin validar: "sentimiento" (especialmente en español rioplatense), "emoción", segmentos de personalidad.

### 5.6 El extremo del segmento: Crystal Knows y Humantic AI — y la auditoría que los desarma

Estas dos venden **perfiles de personalidad individuales** (marco DISC) inferidos del LinkedIn y otros rastros públicos de una persona concreta, para uso en ventas y reclutamiento. Es la versión más literal de "esta herramienta te dice la personalidad de alguien".

- **Lo declarado:** Crystal reporta ~**80% de exactitud** en perfiles predichos y ~97% en perfiles "verificados" (los que la propia persona completó con un test). Ambas cifras son **autoinformadas, no validadas por terceros**. Nótese además el truco: el 97% corresponde a los casos donde la persona hizo el test — o sea, donde no hubo predicción.
- **Lo verificado, y es demoledor:** Rhea, Markey, D'Arinzo, Schellmann, Sloane, Squires, Arif Khan y Stoyanovich (2022), *An External Stability Audit Framework to Test the Validity of Personality Prediction in AI Hiring* (arXiv:2201.09151; publicado también en *Data Mining and Knowledge Discovery*), auditaron externamente **Humantic AI y Crystal** y concluyeron que **ambos sistemas "show substantial instability with respect to key facets of measurement, and hence cannot be considered valid testing instruments"**. Un hallazgo concreto: Crystal produce con frecuencia **puntajes de personalidad distintos para el mismo CV según se entregue en PDF o en texto plano** — una variación completamente irrelevante para el constructo que dice medir. Si el formato del archivo mueve el resultado, no hay medición.

Este es el resultado más importante de toda la sección 5, porque es una **auditoría independiente, publicada y reproducible (los autores liberaron una librería open source)** sobre productos comerciales de inferencia de personalidad. La confiabilidad es condición necesaria de la validez; estos productos fallan la condición necesaria.

### 5.7 Síntesis de la sección 5

| Vendor | Qué vende | Evidencia publicada | Veredicto |
|---|---|---|---|
| SparkToro | Atención de audiencias agregadas | FAQ de exactitud explícita, fuentes declaradas, autolimitación fuerte | **Honesto.** Poco útil para Argentina profunda por cobertura de panel. |
| Helixa/TelmarHelixa | Personas y afinidades, fusión con MRI-Simmons | Metodología de fusión y ponderación declarada, validada a población EEUU | Serio pero irrelevante fuera de EEUU. Enterprise. |
| Brandwatch | Listening + segmentos + imagen | Volumen y menciones auditable; sentimiento/emoción sin validación publicada | Mixto. Caro. |
| Audiense | Segmentos + "personalidad" | **Ninguna.** Lineage en un producto de IBM discontinuado en 2021 | **Inferencia no validada con UI confiada.** Evitar. |
| Crystal Knows | Personalidad DISC individual | Autodeclarada 80%; **auditoría externa 2022: instrumento no válido** | **Refutado por evidencia independiente.** |
| Humantic AI | Personalidad individual para ventas | **Auditoría externa 2022: instrumento no válido** | **Refutado por evidencia independiente.** |

---

## 6. ANALÍTICA VISUAL: VISUAL LISTENING Y LOS BLOQUES DE CONSTRUCCIÓN

### 6.1 Productos de visual listening

| Producto | Qué detecta | Precio | Comentario |
|---|---|---|---|
| **Brandwatch Image Insights** | Logos (incluso en remeras, carteles, tatuajes), objetos, escenas y actividades en miles de millones de imágenes | Dentro de contratos Brandwatch (USD 800-15.000+/mes) | La capacidad más madura del mercado. Su claim verificable —menos spam y duplicados, más volumen de datos— es de *ingeniería de datos*, no psicológico. |
| **YouScan Visual Insights** | Logos, objetos, escenas, actividades, "demografía" y "clasificación de emoción" dentro de fotos y videos; biblioteca de miles de escenas | Desde ~USD 499/mes (Starter anual) | Fuerte en FMCG, moda y belleza. **Ojo con las capas de "demografía" y "emoción" en imagen: son exactamente las que los proveedores de infraestructura restringieron o retiraron (ver 6.3).** |
| **Talkwalker** | Reconocimiento de logos y "señales emocionales" en imagen y video | Enterprise | Mismo reparo sobre emoción. |
| **Pulsar TRAC** | Analítica multimodal texto/imagen/video/audio con agentes LLM | Enterprise | Más nuevo, menos trazable. |

**Ninguno de estos es realista para una pyme argentina por precio.** Se mencionan porque definen el estado del arte y porque muestran dónde el propio mercado enterprise puso la raya.

### 6.2 Los bloques de construcción (lo que sí es accesible)

Para un sistema propio, la vía viable es la API de visión por uso:

- **Google Cloud Vision**: `LABEL_DETECTION` (objetos, escenas), `LOGO_DETECTION`, `TEXT_DETECTION`/OCR, `IMAGE_PROPERTIES` (paleta de colores dominantes), `SafeSearch`. Pago por imagen, arranca en centavos de dólar por unidad, con cuota gratuita mensual. Es la opción más razonable en costo para procesar unos miles de imágenes.
- **AWS Rekognition**: `DetectLabels`, `DetectText`, `DetectModerationLabels`, y `DetectFaces` con atributos faciales.
- **Modelos abiertos locales** (CLIP y derivados, detectores de objetos): costo marginal cero después del hardware, sin envío de imágenes de terceros a un proveedor externo — lo que además reduce exposición legal.

**MEDIDO/objetivo en estos servicios:** presencia de objetos, texto (OCR), logos, paleta de color, composición. Verificable: uno mira la foto y confirma si hay o no una silla.
**INFERIDO y frágil:** todo lo demás.

### 6.3 Las restricciones que los propios proveedores impusieron — el dato más importante de la sección

Tres de los cuatro grandes proveedores de visión **retiraron o restringieron** justamente las inferencias que un sistema de perfilado se sentiría tentado de usar. No lo hicieron por moda: lo hicieron porque no podían defender la validez.

**Google Cloud Vision — retiró las etiquetas de género (19 de febrero de 2020).**
A partir de esa fecha, `LABEL_DETECTION` **dejó de devolver etiquetas de género** como "man" y "woman", reemplazándolas por "person". La razón declarada por Google: *"Given that a person's gender cannot be inferred by appearance, we have decided to remove these labels in order to align with the Artificial Intelligence Principles at Google, specifically Principle #2: Avoid creating or reinforcing unfair bias"*. La decisión presionó al resto del mercado.

**Microsoft Azure Face — retiró emoción, género, edad y otros atributos (anuncio del 21 de junio de 2022).**
Como parte de la alineación con su Responsible AI Standard, Microsoft decidió **no soportar un sistema de propósito general que pretenda inferir estados emocionales, género, edad, sonrisa, vello facial, cabello y maquillaje**. Cronograma: **sin acceso para clientes nuevos desde el 21 de junio de 2022; los clientes existentes tuvieron hasta el 30 de junio de 2023** para discontinuar el uso antes del retiro. La razón declarada por **Natasha Crampton**, Chief Responsible AI Officer de Microsoft: **falta de consenso científico sobre la definición misma de "emociones"**, y preocupación por la **sobregeneralización** en cómo los sistemas de IA interpretan esas emociones, con riesgo de estereotipación y discriminación.

**AWS Rekognition — no lo retiró, pero lo desautorizó por escrito en su documentación.**
La guía oficial de atributos faciales de AWS dice, textualmente:
> *"gender and emotion predictions are based on physical appearance and should not be used for determining actual gender identity or emotional state. A gender binary (male/female) prediction is based on the physical appearance of a face in a particular image. It doesn't indicate a person's gender identity, and you shouldn't use Rekognition to make such a determination. We don't recommend using gender binary predictions to make decisions that impact an individual's rights, privacy, or access to services. Similarly, a prediction of an emotional doesn't indicate a person's actual internal emotional state... A person pretending to have a happy face in a picture might look happy, but might not be experiencing happiness."*

AWS además recomienda umbral de confianza del 99% para casos sensibles y advierte que la API no debe usarse de forma que viole el **EU AI Act** u otras leyes aplicables.

**Y el regulador ya alcanzó a la industria.**
El **AI Act** europeo prohíbe en su **art. 5(1)(f)** los sistemas de IA que infieran emociones de una persona física **en el ámbito laboral y en instituciones educativas** a partir de datos biométricos, con excepciones médicas y de seguridad. Las prohibiciones del art. 5 son **aplicables desde el 2 de febrero de 2025**, con multas de hasta **35 millones de euros o el 7% de la facturación global anual**, lo que sea mayor. La Comisión vinculó la prohibición a la definición legal de "sistema de reconocimiento de emociones", limitándola a inferencias basadas en datos biométricos.

### 6.4 Qué se sigue de todo esto para un sistema responsable

Si Google no se anima a etiquetar género desde una foto, si Microsoft apagó la inferencia de emoción y edad citando la ausencia de consenso científico sobre qué es una emoción, y si AWS deja por escrito que su propia predicción de emoción no indica el estado emocional real de la persona, entonces:

1. **Un sistema de perfilado no debe inferir emoción, edad, género, etnia, orientación ni estado de ánimo desde rostros.** No es una posición ética blanda: es la posición técnica de los propios fabricantes.
2. **La detección de caras (cuántas personas hay, si el feed muestra personas o sólo producto) es MEDIDA y aceptable.** La *clasificación* de esas caras no lo es.
3. Lo que sí queda, y es mucho: **objetos, escenas, texto en imagen (OCR), logos, paleta de color, composición, consistencia visual, tipo de encuadre, presencia/ausencia de producto, de precio, de persona.** Todo eso es verificable a ojo por un humano y suficiente para caracterizar una cuenta comercial.

---

## 7. EL MERCADO OSINT / BÚSQUEDA DE PERSONAS POR FOTO — el extremo cautelar

Se incluye brevemente y **de forma crítica**: es el borde del mercado que define, por contraste, dónde está la línea. **No se dan instrucciones operativas.**

### 7.1 Qué se vende

Buscadores de reconocimiento facial de acceso público (**PimEyes** es el más conocido) que, a partir de una foto de una cara, devuelven otras apariciones de esa cara en la web abierta. Alrededor de ellos orbita un mercado de "people search" que promete consolidar identidad, domicilios, familiares y redes sociales de una persona a partir de un dato mínimo.

### 7.2 Su situación legal

- PimEyes rastrea la web continuamente para recolectar caras; su base contiene **miles de millones de imágenes**, construida **sin consentimiento** de las personas retratadas.
- La **autoridad de protección de datos de Hamburgo** considera que sus prácticas son **ilegales bajo el GDPR**, pero **no ha adoptado medidas de ejecución sustantivas por más de cuatro años**, aparentemente por estar la empresa radicada fuera de la UE (Dubái).
- En **2025 la ONG austríaca noyb demandó a la propia DPA de Hamburgo**, sosteniendo que la inacción del regulador es en sí misma ilegal y que la localización offshore de un operador no puede ser motivo para abandonar la aplicación del derecho europeo. Hubo una decisión de la DPA a fines de 2025; la ejecución sustantiva contra PimEyes seguía pendiente a mediados de 2026.
- El Parlamento Europeo trató el asunto en una pregunta parlamentaria formal (E-002586/2022) sobre las implicancias en derechos fundamentales del reconocimiento facial de uso privado.
- El precedente comparable es **Clearview AI**, sancionada con multas millonarias en varios Estados europeos (entre ellas órdenes de prohibición y multas de €20M) por el mismo modelo de negocio.

### 7.3 Por qué es la advertencia y no el modelo

1. **Ilegalidad reconocida sin sanción efectiva no es permiso; es riesgo diferido.** El hecho de que un servicio siga operando no significa que usarlo sea lícito para quien lo usa. En Argentina, la Ley 25.326 exige consentimiento y prohíbe la formación de bancos de datos que revelen datos sensibles; el rostro procesado biométricamente es dato personal y su tratamiento requiere base legal.
2. **Es el caso donde "público ≠ consentido" se ve sin ambigüedad.** Las fotos que indexa fueron publicadas para otra finalidad. El desvío de finalidad es el defecto estructural de todo el modelo.
3. **Define la línea del sistema propio:** un sistema que analiza *cuentas comerciales* para caracterizar *comunicación de marca* está en un lugar defendible. Un sistema que identifica *personas* a partir de rostros está en el lugar donde los reguladores europeos ya dijeron "ilegal". La diferencia no es de grado: es de objeto. **El objeto legítimo es la cuenta como emisor comercial, no la persona como individuo.**

---

## 8. LATAM Y ARGENTINA EN CONCRETO

### 8.1 La fricción de pagar software en dólares desde Argentina (2026)

Ninguna de estas herramientas cotiza en pesos. El costo real para un contribuyente argentino que paga con tarjeta en pesos:

- **Impuesto PAIS: derogado.** Caducó a fines de 2024 y sus remanentes normativos se ordenaron a comienzos de 2026. Ya no aplica.
- **Percepción del 30%** a cuenta de Ganancias / Bienes Personales sobre la conversión a pesos (sólo si se paga en pesos; recuperable en la declaración anual, o reintegrable vía CBU para quienes no son contribuyentes de esos impuestos).
- **IVA 21%** sobre servicios digitales del exterior, más eventuales percepciones de IIBB provinciales según jurisdicción.
- **Regla práctica:** multiplicar el precio de lista en USD por **~1,3 a ~1,6** para estimar el costo en pesos. Un plan de USD 99 es, en la práctica, USD 130-160 equivalentes; ese es el número que hay que comparar contra el valor.
- Alternativa habitual de las pymes: pagar con tarjeta en dólares (cuenta en USD) para evitar la percepción, o usar el plan anual para congelar precio.

### 8.2 Qué está realmente disponible en español

| Herramienta | Español | Origen | Adopción en Argentina |
|---|---|---|---|
| **Instagram Insights / Meta Business Suite** | Sí, completo | Meta | Universal, gratis. Es lo que efectivamente usa el 90% de las pymes. |
| **Metricool** | **Sí, nativo** (producto, soporte, academia, comunidad) | España | **Muy alta en LATAM.** Es el estándar de facto para community managers hispanohablantes independientes y pymes. |
| **Heepsy** | Sí | España | Media, en el nicho de influencer marketing con presupuesto chico. |
| **Influencity** | Sí | España | Media-alta en agencias. Caro para pyme. |
| **HypeAuditor** | Blog y contenidos en español, incluida guía específica para Argentina; producto en inglés | Chipre/global | Alta en agencias grandes. Sus **herramientas gratuitas** sí las usan negocios chicos. |
| **Hootsuite** | Sí | Canadá | Presente pero en retroceso por precio por asiento. |
| **Later, Iconosquare, Socialinsider, Sprout, Brandwatch, YouScan, SparkToro, Audiense, Helixa** | No o parcial | — | Baja a nula en pymes argentinas. |

### 8.3 Agencias y plataformas locales/regionales

- **FLUVIP** (regional, con trayectoria en Argentina; clientes como Subway, Sony, Xiaomi), **Story Talent** y varias agencias locales operan como intermediarios de influencer marketing. Venden *servicio*, no herramienta: el dato lo compran ellos a HypeAuditor/Influencity y lo revenden dentro de una campaña.
- **Referencias de precio del mercado argentino de influencers (2026):** nano (5.000-20.000 seguidores) ~ARS 30.000-80.000 por post en feed; micro (20.000-100.000) ~USD 150-600; macro (+100.000) desde USD 1.000 hasta USD 15.000+ por campaña. Sirve para dimensionar: **el chequeo de un influencer no puede costar más que el influencer.** Pagar USD 299/mes de HypeAuditor para contratar nano-influencers de ARS 50.000 es económicamente absurdo.
- **Gestión de redes en Argentina (servicio tercerizado):** rangos de referencia USD 80-300/mes (básico), USD 200-600 (estándar), USD 400-1.200 (premium). Es el competidor real de comprar herramientas: para muchos negocios chicos, contratar horas de una persona rinde más que licenciar software.

### 8.4 El problema del benchmark argentino

**No existe un reporte público de benchmarks de Instagram por industria para Argentina o LATAM con muestra local.** Los reportes de Rival IQ/Quid, Socialinsider y Metricool son de muestras principalmente anglosajonas y de marcas medianas/grandes. Para una pyme del interior argentino esto significa que **la línea de base hay que construirla**, no comprarla. Es un trabajo de una tarde con `business_discovery` o con el plan Starter de Metricool, y vale más que cualquier reporte importado.

---

## 9. TABLA DE RECOMENDACIÓN FINAL PARA UNA PYME ARGENTINA

### 9.1 Qué comprar, en orden

| Prioridad | Necesidad | Solución recomendada | Costo real estimado (con impuestos) | Por qué |
|---|---|---|---|---|
| **1** | Métricas propias exactas | **Instagram Insights + Meta Business Suite** | **$0** | Es la fuente. Nadie tiene mejores datos de tu cuenta. En español. Reach, views, saves, shares, demografía. |
| **2** | Historial >90 días, panel de competencia, informes | **Metricool** — empezar en **Free**, subir a **Starter** cuando el Free moleste | $0 → ~USD 25-35/mes efectivos | Español nativo, historial ilimitado, hasta 100 competidores, informes PDF. Mejor relación valor/precio del mercado para este caso. |
| **3** | Línea de base de categoría | **Panel propio de 15-30 cuentas comparables** (mismo rubro, misma región) construido en Metricool + Rival IQ/Quid como referencia secundaria | $0 adicional | La mediana global (IG ~0,30% en 2026) no describe a un negocio de Santa Rosa. El percentil dentro del panel propio sí. |
| **4** | Vetting de un creador antes de pagarle | **Pedirle sus Insights** (reach, saves, demografía) + **Creator Marketplace** + chequeo gratuito de **HypeAuditor/Heepsy** como segunda opinión | $0 | Datos MEDIDOS con consentimiento. La herramienta paga sólo estima lo que el creador te puede mostrar gratis. |
| **5** | Análisis visual del feed (propio o de competencia) | **Google Cloud Vision** (labels, logos, OCR, paleta) por uso, o **modelo abierto local** | Centavos de USD por imagen; free tier mensual | Objetos, texto, color y composición son MEDIDOS y verificables. Alcanza para caracterizar una cuenta comercial. |
| **6** | Sentimiento y contexto de comentarios | **Lectura humana** de una muestra + LLM sólo como asistente de resumen, nunca como puntaje | $0 a bajo | El sentiment automático en español rioplatense es malo. Una persona leyendo 100 comentarios sabe más. |

### 9.2 Qué NO comprar, y por qué

| Herramienta / categoría | Precio | Motivo del rechazo |
|---|---|---|
| **Hootsuite / Sprout Social** | USD 99-399+/usuario/mes | Precio por asiento desproporcionado. No aportan ningún dato que Metricool o Meta no den. |
| **Brandwatch / Talkwalker / Pulsar / YouScan** | USD 500-15.000+/mes | Escala enterprise. El volumen de menciones de una pyme argentina no justifica el listening. Además venden capas de emoción sin validar. |
| **Audiense** | USD 12.000-28.750/año | **Psicografía sin validación publicada, apoyada en el linaje de un producto de IBM discontinuado en 2021, sobre datos de Twitter/X que no representan a una audiencia argentina de Instagram.** |
| **Crystal Knows / Humantic AI** | Varios | **Auditoría externa publicada (Rhea et al., 2022) concluye que no son instrumentos de medición válidos: inestables ante variaciones irrelevantes del input.** |
| **Helixa / TelmarHelixa** | Enterprise | Metodológicamente serio pero ponderado a población de EEUU. Irrelevante para Argentina. |
| **Upfluence** | ~USD 1.200/mes, contrato 12 meses | Compromiso anual desproporcionado. |
| **HypeAuditor / Modash / Influencity de pago** | USD 99-500+/mes | Sólo si el volumen de campañas lo justifica (>10 creadores por mes). Con nano-influencers a ARS 50.000, la herramienta cuesta más que la campaña. |
| **PimEyes y buscadores faciales** | — | **Ilegalidad bajo GDPR reconocida por la DPA de Hamburgo. En Argentina, tratamiento biométrico sin base legal bajo Ley 25.326. Riesgo legal y reputacional desproporcionado. No usar.** |
| **Cualquier API de inferencia de emoción/género/edad desde rostro** | — | **Google retiró las etiquetas de género (feb-2020); Microsoft retiró emoción, género y edad (jun-2022 / jun-2023) por falta de consenso científico; AWS lo desaconseja por escrito; el AI Act lo prohíbe en ámbitos laboral y educativo desde feb-2025.** |

### 9.3 La regla de reporte que debería atravesar cualquier sistema propio

Cada afirmación del perfil tiene que venir etiquetada:

- **[MEDIDO]** — dato de la API de Meta o contador público verificable. Se cita el número y la fecha.
- **[ESTIMADO]** — cálculo sobre datos públicos, con el método y la muestra explícitos. Se expresa como rango o percentil dentro del panel de referencia, nunca como número puntual con decimales.
- **[INFERIDO]** — hipótesis del modelo. Se marca como hipótesis, se acompaña de la evidencia visual concreta que la motiva, y **no se usa como base única de ninguna decisión**.

Si el sistema no puede etiquetar una afirmación en una de las tres categorías, esa afirmación no debería salir.

---

## 10. LO QUE ESTE RELEVAMIENTO NO PUDO ESTABLECER

En favor de la honestidad del informe:

1. **No existe estudio independiente y publicado que compare la exactitud de HypeAuditor, Modash, Heepsy e Influencity sobre el mismo conjunto de cuentas.** Lo que hay son comparativas comerciales y el reconocimiento sectorial de que las herramientas discrepan.
2. **Ningún vendor de detección de fraude publica tasa de falsos positivos.** Todos publican "detección". Es la mitad de la matriz de confusión.
3. **No pude determinar qué reemplazó técnicamente a Watson Personality Insights dentro de Audiense.** El material comercial sigue nombrando la integración con IBM. La falta de respuesta a esa pregunta es, en sí, la respuesta relevante para un comprador.
4. **Los precios de SaaS varían por región, promoción y negociación.** Los números de este informe son de listas públicas de agosto 2026 y deben reverificarse antes de contratar.
5. **La normativa impositiva argentina sobre servicios del exterior cambia con frecuencia.** El esquema descrito (percepción 30% + IVA 21%, sin Impuesto PAIS) corresponde a 2026 y debe confirmarse con un contador antes de presupuestar.

---

## FUENTES

**Instagram / Meta**
- Instagram Platform — Insights: https://developers.facebook.com/docs/instagram-platform/insights
- Instagram Insights updates (Supermetrics): https://docs.supermetrics.com/docs/instagram-insights-updates
- Phyllo — Instagram API integration, rate limits: https://www.getphyllo.com/post/instagram-api-integration-101-for-developers-of-the-creator-economy
- Phyllo — Instagram audience demographics API: https://www.getphyllo.com/post/instagram-audience-demographics-for-influencer-marketing-platforms
- Instagram Creator Marketplace, expansión: https://www.socialmediatoday.com/news/instagram-expands-geographic-creator-marketplace/715865/ ; https://techcrunch.com/2024/05/13/instagram-expands-its-creator-marketplace-to-10-new-countries

**Analítica y precios**
- Metricool precios: https://metricool.com/pricing/
- Later precios: https://later.com/pricing/
- Iconosquare planes y precios: https://www.iconosquare.com/plans-and-pricing
- Hootsuite precios (análisis 2026): https://costbench.com/software/social-media-management/hootsuite/
- Socialinsider (perfil y precios): https://www.capterra.com/p/202776/Socialinsider/

**Benchmarks**
- Rival IQ / Quid — Social Media Industry Benchmark Report 2026 (vía análisis): https://apaya.com/blog/social-media-benchmarks-instagram

**Influencers y fraude**
- HypeAuditor — cómo funciona la detección de seguidores falsos: https://blog.hypeauditor.com/hypeauditor-fake-followers-detection/
- HypeAuditor — herramientas para Argentina (español): https://blog.hypeauditor.com/es/mejores-herramientas-de-marketing-de-influencers-en-argentina/
- HypeAuditor — costos: https://blog.hypeauditor.com/how-much-does-hypeauditor-cost-/
- Cresci et al. (2015), *Fame for sale: efficient detection of fake Twitter followers*: https://arxiv.org/pdf/1509.04098
- *Instagram Fake and Automated Account Detection*: https://arxiv.org/pdf/1910.03090
- *Computational Studies in Influencer Marketing: A Systematic Literature Review*: https://arxiv.org/pdf/2506.14602

**Psicografía e inteligencia de audiencia**
- IBM — deprecación de Watson Personality Insights (foro oficial): https://community.ibm.com/community/user/discussion/watson-pi-deprecated
- Humantic AI — "Welcoming IBM Watson Personality Insights API users": https://humanticai.medium.com/welcoming-ibm-watson-personality-insights-api-users-to-humantic-ai-677cdd1a30ce
- Audiense — material sobre Watson Personality Insights: https://resources.audiense.com/en/blog/getting-the-most-out-of-personality-insights-ibm-watson
- Audiense Insights (producto): https://www.audiense.com/products/audiense-insights/audiense-insights
- SparkToro — exactitud y sesgo (FAQ): https://sparktoro.com/support/faq/accuracy-and-bias
- SparkToro — cómo obtiene los datos: https://sparktoro.com/support/faq/how-sparktoro-finds-data
- TelmarHelixa — soluciones: https://telmarhelixa.com/audience-segmentation
- Crystal Knows — claim de exactitud: https://www.crystalknows.com/blog/crystal-accuracy
- **Rhea, Markey, D'Arinzo, Schellmann, Sloane, Squires, Arif Khan, Stoyanovich (2022), *An External Stability Audit Framework to Test the Validity of Personality Prediction in AI Hiring*: https://arxiv.org/abs/2201.09151**

**Visión e imagen**
- Brandwatch Image Insights: https://www.brandwatch.com/press/press-releases/brandwatch-image-insights-image-analytics-platform-track-every-logo/
- Brandwatch — reconocimiento de logos: https://www.brandwatch.com/guides/logo-recognition/
- YouScan Visual Insights: https://youscan.io/visual-insights/ ; precios: https://youscan.io/pricing/
- Talkwalker — análisis de imagen: https://www.talkwalker.com/blog/what-is-image-analysis
- AWS — Guidelines on face attributes: https://docs.aws.amazon.com/rekognition/latest/dg/guidance-face-attributes.html
- Microsoft Azure — Responsible AI investments and safeguards for facial recognition (21/06/2022): https://azure.microsoft.com/en-us/blog/responsible-ai-investments-and-safeguards-for-facial-recognition/
- Google Cloud Vision — retiro de etiquetas de género (19/02/2020): https://venturebeat.com/2020/02/20/google-cloud-ai-removes-gender-labels-from-cloud-vision-api-to-avoid-bias/ ; https://thenextweb.com/neural/2020/02/20/google-drops-gender-labels-from-image-recognition-to-reduce-bias/
- FPF — prohibición de reconocimiento de emociones bajo el AI Act: https://fpf.org/blog/red-lines-under-eu-ai-act-unpacking-the-prohibition-of-emotion-recognition-in-the-workplace-and-education-institutions/

**OSINT / búsqueda facial**
- noyb — demanda contra la DPA de Hamburgo por inacción frente a PimEyes: https://noyb.eu/en/no-action-taken-against-pimeyes-noyb-lawsuit-against-hamburg-dpa
- Cybernews — regulador alemán y PimEyes: https://cybernews.com/privacy/german-regulator-facial-recognition-pimeyes-billions-faces-privacy/
- Parlamento Europeo — pregunta E-002586/2022 sobre PimEyes: https://www.europarl.europa.eu/doceo/document/E-9-2022-002586_EN.html

**Argentina**
- Impuestos a consumos en el exterior 2026: https://www.global66.com/blog/como-afectan-los-impuestos-a-tus-gastos-digitales/ ; https://www.perfil.com/noticias/economia/sin-impuesto-pais-como-cambia-el-costo-real-de-pagar-con-tarjeta-en-el-exterior-en-2026.phtml
- Precios de manejo de redes en Argentina: https://www.estudiocreativo.agency/blog/manejo-redes-sociales-precios-argentina
- Plataformas de influencer marketing en Argentina: https://branch.com.co/marketing-digital/top-8-plataformas-de-marketing-de-influencers-en-argentina/
