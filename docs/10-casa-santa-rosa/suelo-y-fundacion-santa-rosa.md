# Suelo y fundación en SANTA ROSA (La Pampa) — casa de una planta

**Documento técnico de proyecto. Estudio de arquitectura — Santa Rosa, La Pampa.**
Alcance: vivienda unifamiliar de **planta baja únicamente**, en el ejido urbano de Santa Rosa.

> **Relación con el resto de la biblioteca.** La teoría general del loess colapsable argentino
> (mineralogía, mecanismo, doble edométrico, autocolapsables, las tres estrategias de Rocca–Redolfi–Terzariol)
> está en [`docs/03-estructuras/estructuras.md` §3.5](../03-estructuras/estructuras.md).
> **Este documento no la repite: la aplica a Santa Rosa y a una casa baja.** Leer aquel primero.

## Convenciones de confianza del dato

| Marca | Significado |
|---|---|
| **(verificado)** | Dato textual de fuente citada al pie. Se puede usar en memoria de cálculo citando la fuente. |
| **[PD]** | Predimensionado / criterio profesional de oficina. Orienta el anteproyecto. **No reemplaza cálculo ni estudio.** |
| **[VER]** | No verificado en fuente primaria. Confirmar antes de usar. |
| **[VERIFICAR con estudio de suelos]** | **Dato que sólo puede salir del estudio geotécnico del lote.** No hay valor de tabla que lo sustituya. |
| **[FIRMA]** | Requiere firma de profesional matriculado (estructuralista y/o geotécnico). Responsabilidad indelegable. |

---

## Índice

1. [Resumen ejecutivo — las 12 cosas que hay que saber](#1-resumen-ejecutivo--las-12-cosas-que-hay-que-saber)
2. [Marco geológico de Santa Rosa](#2-marco-geológico-de-santa-rosa)
   - 2.1 Situación regional y génesis
   - 2.2 Columna estratigráfica de la ciudad
   - 2.3 La tosca (calcrete): qué es, dónde está, cuánto mide
   - 2.4 Topografía urbana: la cuenca centrípeta de Don Tomás
   - 2.5 Qué significa todo esto para tu lote
3. [Napa freática en Santa Rosa — el dato que cambió la ciudad](#3-napa-freática-en-santa-rosa--el-dato-que-cambió-la-ciudad)
   - 3.1 La cronología del ascenso
   - 3.2 Por qué sube
   - 3.3 Zonas de la ciudad
   - 3.4 Consecuencias directas sobre el proyecto
   - 3.5 Qué preguntar y a quién
4. [Loess colapsable aplicado a una casa de una planta](#4-loess-colapsable-aplicado-a-una-casa-de-una-planta)
   - 4.1 La paradoja de la casa liviana
   - 4.2 El mecanismo, aplicado a esta obra
   - 4.3 Los ocho disparadores reales
   - 4.4 Por qué la casa baja es el peor caso de exposición
5. [Parámetros geotécnicos de referencia para Santa Rosa](#5-parámetros-geotécnicos-de-referencia-para-santa-rosa)
   - 5.1 Declaración honesta sobre el estado del dato publicado
   - 5.2 Órdenes de magnitud utilizables (y de dónde salen)
   - 5.3 El SPT miente en loess sobre napa — lo dice el CIRSOC 401
   - 5.4 Tabla de parámetros a exigir al informe
6. [Estudio de suelos para una casa de una planta](#6-estudio-de-suelos-para-una-casa-de-una-planta)
   - 6.1 ¿Hace falta? Respuesta honesta
   - 6.2 Lo que exige el CIRSOC 401 (verificado)
   - 6.3 Calicata vs. SPT en Santa Rosa
   - 6.4 Pliego del estudio — texto para copiar y pegar
   - 6.5 Cómo se lee el informe
   - 6.6 Diez preguntas al geotécnico
   - 6.7 Costo relativo del estudio vs. costo de reparar
7. [Soluciones de fundación para casa de una planta](#7-soluciones-de-fundación-para-casa-de-una-planta)
   - 7.1 Profundidad mínima de fundación
   - 7.2 Comparativa de las cuatro soluciones
   - 7.3 Recomendación por defecto en Santa Rosa
   - 7.4 Predimensionado orientativo
   - 7.5 Detalles constructivos que deciden el resultado
8. [Mitigación no estructural — el capítulo que salva la casa](#8-mitigación-no-estructural--el-capítulo-que-salva-la-casa)
   - 8.1 El principio
   - 8.2 Vereda perimetral
   - 8.3 Pluviales
   - 8.4 Instalaciones enterradas
   - 8.5 Pozo absorbente y cámara séptica
   - 8.6 Jardín, riego y árboles
   - 8.7 Pileta de natación
   - 8.8 Tabla maestra de distancias
   - 8.9 Manual del usuario para el comitente
9. [Patologías locales — leer las fisuras](#9-patologías-locales--leer-las-fisuras)
10. [Checklist de suelo y fundación del proyecto](#10-checklist-de-suelo-y-fundación-del-proyecto)
11. [Fuentes](#11-fuentes)

---

## 1. Resumen ejecutivo — las 12 cosas que hay que saber

1. **Santa Rosa está fundada sobre un manto eólico cuaternario que apoya sobre la Formación Cerro Azul** (limos arenosos / limolitas del Mioceno superior). El basamento granítico se alcanzó **a 144 m de profundidad** en la ciudad (verificado). Todo lo que le importa a una casa está en los primeros 3 m.
2. **La tosca (calcrete) es el rasgo determinante de la fundación en La Pampa.** En el entorno Santa Rosa–Anguil los suelos dominantes tienen **tosca entre 0,50 y 1,50 m**, y otros con tosca **por debajo de 1,50 m** (INTA, verificado). En sectores erosionados de la ciudad **aflora en superficie**. Su profundidad **varía dentro de un mismo lote**.
3. **La napa freática de Santa Rosa subió del orden de 20 m en tres décadas.** Del orden de **25 m en el centro a comienzos de los '90** a **menos de 5 m** hacia 2017 (verificado, Viglizzo); **~6 m en el entorno de la plaza San Martín** hacia 2014 (verificado, Fábregas). Cualquier dato de napa anterior a 2015 **no sirve**.
4. **El proyecto no puede apoyarse en la napa "histórica" del barrio.** Hay que medirla, con fecha, en el lote, y pedir la tendencia. **[VERIFICAR con estudio de suelos]**
5. **Una casa de una planta es un caso delicado, no un caso menor.** Poca carga → no se "prueba" el suelo; fundación superficial → dentro de la capa activa; mucho perímetro por m² → máxima exposición al agua de lluvia y riego. El colapso del loess **no lo dispara la carga: lo dispara el agua.**
6. **No existe publicado un banco de datos geotécnicos de Santa Rosa con tensiones admisibles por zona.** Quien te ofrezca un número "de la zona" sin ensayo, está adivinando. Ver §5.1.
7. **El CIRSOC 401 obliga, en suelos colapsables por encima de la napa, a explorar con calicatas y pozos a cielo abierto, con muestreo en damas de lado mínimo 0,25 m** (verificado, art. 3.6.7). Y advierte que **el SPT es poco representativo** en esa condición (verificado, C 3.6.7).
8. **Cantidad mínima de prospecciones para tu casa: 2** (Clase C‑1) o **3** (Clase C‑2), y **profundidad mínima de investigación: 6 m** (verificado, CIRSOC 401, Tabla 3.1 y art. 3.5.6.2).
9. **Solución por defecto en Santa Rosa para casa de una planta: platea de hormigón armado sobre manto compactado, con vigas de borde y de rigidización.** Ver §7.3 para la fundamentación y las excepciones.
10. **La profundidad mínima de fundación es una decisión de proyecto, no un dato de catálogo:** por debajo de la capa activa de humedad y raíces. Orden de magnitud **[PD] 0,80–1,00 m** bajo terreno natural para fundación directa; el número final sale del informe. **[VERIFICAR con estudio de suelos]**
11. **El capítulo 8 vale más que el capítulo 7.** En loess, la fundación bien calculada sobre un manejo del agua malo se rompe igual. Vereda perimetral, pluviales alejados, cañerías estancas, pozo absorbente lejos, nada de canteros contra el muro.
12. **Firmas:** el estudio geotécnico lo firma un profesional con incumbencia en geotecnia; el cálculo y el plano de fundaciones los firma el estructuralista. **[FIRMA]** El arquitecto especifica, coordina y controla — no adopta tensiones admisibles por su cuenta.

---

## 2. Marco geológico de Santa Rosa

### 2.1 Situación regional y génesis

Santa Rosa está en el centro‑este de La Pampa, en el borde occidental de la llanura pampeana y en el corazón de la geografía loéssica argentina: al oeste el "Mar de Arena" (arenas eólicas), al este el loess pampeano típico (ver `estructuras.md` §3.5.1). El material que se pisa en la ciudad es **sedimento eólico cuaternario** — arenas y limos transportados por vientos del S‑SO — depositado sobre una plataforma sedimentaria neógena.

La secuencia, de abajo hacia arriba (verificado, Giai & Tullio, UNLPam / Dirección de Aguas de La Pampa):

- **Basamento cristalino.** En Santa Rosa se alcanzó, y es **de carácter granítico, a 144 m de profundidad**. Hacia el este se profundiza por un sistema de fracturas (en Uriburu y hacia el este se infiere a 4–5 km, dentro de la cuenca de Macachín).
- **Formación Macachín** (arcilitas verdes, Mioceno), donde está presente, bajo Cerro Azul.
- **Formación Cerro Azul** (Mioceno superior): limos arenosos, limolitas y areniscas muy finas. Es la unidad que aloja el acuífero. **Espesor máximo del orden de 190 m.** Entre **50 y 130 m de profundidad** (≈ 70–90 msnm) suele encontrarse una **intercalación arcillosa** que secciona hidráulicamente el acuífero: por debajo el agua es salada, por arriba dulce.
- **Arenas eólicas** por encima: cubren casi toda el área con espesores disímiles; **los máximos son del orden de los 10 m**. Los médanos de la región alcanzan, en acumulaciones equivalentes, **espesores desde decímetros hasta 32 m**, asignados al Pleistoceno final y Holoceno.

Composición de la Fm. Cerro Azul, según su análisis litoestratigráfico (verificado, Rev. Asoc. Geol. Argentina): **alternancia de limolitas y areniscas, que constituye el 92 % de la sucesión**, con intercalaciones de arcilitas en los estratos basales (**7 %**); hacia el techo se desarrollan **calcretes que coronan la sucesión (1 %)**.

> **Traducción para el proyecto:** la casa se funda en el **techo** de todo esto — en los primeros 1 a 3 m, es decir, en el manto eólico y/o en el calcrete que corona la Cerro Azul. Los 144 m de abajo son irrelevantes para la fundación de una vivienda; sí importan para entender la napa.

### 2.2 Columna estratigráfica típica de la ciudad

**Perfil de referencia — orden de magnitud, no dato de proyecto:**

| Prof. aprox. | Unidad | Descripción esperable | Relevancia para la casa |
|---|---|---|---|
| 0,00 – 0,30 m | Suelo vegetal / relleno antrópico | Materia orgánica, escombro, restos de obra. En lotes urbanos casi siempre hay relleno no controlado | **Se retira siempre.** Nunca fundar sobre él |
| 0,30 – 1,50 m *(muy variable)* | Manto eólico limo‑arenoso (loess / sedimento loessoide) | Limo arenoso fino, castaño claro, poroso, poco denso, seco y aparentemente "firme" | **Es el estrato de apoyo típico de una casa baja. Es el estrato colapsable.** |
| Variable, entre ~0,50 m y varios metros | **Tosca / calcrete** (banco o nódulos) | Carbonato de calcio, desde nódulos dispersos hasta banco continuo muy consolidado | Si aparece continua y sana: **excelente apoyo**. Si es discontinua: **fuente de asentamiento diferencial** |
| Por debajo | Fm. Cerro Azul | Limolitas y areniscas muy finas, con nódulos y bancos de carbonato | Sólo relevante para pozos/pilotines profundos |

**[VERIFICAR con estudio de suelos]** — Esta columna es un marco de lectura, **no un perfil de proyecto**. En Santa Rosa la variabilidad lateral es alta a escala de lote: la tosca puede estar a 0,60 m en un extremo del terreno y a 2,50 m en el otro, o aparecer y desaparecer.

### 2.3 La tosca (calcrete): qué es, dónde está, cuánto mide

**Qué es.** Costra calcárea (calcrete) formada por precipitación y recristalización de carbonato de calcio en el perfil, bajo clima semiárido. En el loess pampeano su origen está ligado a la abundancia de vidrio volcánico y a reacciones puzolánicas que cementan el sedimento (ver `estructuras.md` §3.5.1). No es una roca de fundación uniforme: es un horizonte con estructura interna.

**Estructura interna típica de un banco de calcrete** (verificado, estudio de los calcretes del sudeste de La Pampa — Rev. Asoc. Geol. Argentina). De abajo hacia arriba:

1. **Sector de transición** — material hospedador invadido por carbonato que lo brecha parcialmente y forma tabiques irregulares en todas direcciones.
2. **Sector laminado** — muy consolidado, láminas subparalelas de **0,1 a 1 cm** de espesor; en partes brechado y recementado.
3. **Sector pisolítico** — bien consolidado, cuerpos elipsoidales **de hasta 6 cm**, aspecto botroidal muy irregular.

**Espesores medidos en el sudeste provincial** (verificado, misma fuente — **atención: no es Santa Rosa**, sirve como orden de magnitud del rasgo geológico):

| Nivel | Cota | Espesor |
|---|---|---|
| Calcrete I (el más antiguo) | 225 msnm | máximo **2 m**, mínimo **1,10 m** |
| Calcrete II | 130 msnm | máximo **1 m**, mínimo **0,70 m** |
| Calcrete III | 70 msnm | **0,5 m** promedio |

La misma fuente aclara que **"sus espesores no son constantes lateralmente"** y que los calcretes **"están parcialmente cubiertos por depósitos eólicos del Pleistoceno‑Holoceno"** — exactamente la situación de un lote en Santa Rosa.

**Profundidad de la tosca en el entorno de Santa Rosa – Anguil** (verificado, INTA EEA Anguil, descripción de zonas y subzonas agroecológicas RIAP):

| Suelo dominante | Profundidad de la tosca |
|---|---|
| Haplustol éntico, familia franca gruesa, mixta térmica | **tosca entre 0,50 y 1,50 m** |
| Haplustol éntico, familia franca, mixta térmica | **tosca por debajo de 1,50 m** |

La misma fuente describe perfiles de secuencia **A‑AC‑C‑Tosca** o **A‑B‑C‑Tosca**, desarrollados sobre "una capa bien consolidada de carbonato de calcio (tosca) que limita su profundidad, y que a veces puede aflorar". En la ciudad de Santa Rosa, la erosión deja la tosca **al descubierto en amplios manchones** [VER — descripción geográfica de divulgación, confirmar en campo].

> **Regla de oficina.** En Santa Rosa hay que ir a la obra suponiendo que **la tosca aparece entre 0,5 y 2,5 m**, que **no es continua**, y que **su profundidad varía dentro del lote**. Esa es exactamente la razón por la que el estudio de suelos con **dos o tres puntos** (no uno) es indispensable: un solo pozo que "pega tosca a 0,80 m" puede llevarte a fundar media casa sobre tosca y media sobre limo suelto. **Ese es el mecanismo n.º 1 de asentamiento diferencial en vivienda pampeana.** [PD]

**Riesgos específicos de la tosca:**

| Riesgo | Descripción | Qué hacer |
|---|---|---|
| **Apoyo mixto** | Parte de la fundación sobre tosca, parte sobre limo suelto | **Nunca.** O se baja todo a tosca, o se aísla todo de la tosca sobre manto compactado uniforme |
| **Banco delgado sobre suelo blando** | Costra de 0,30–0,60 m con limo flojo debajo: "suena" firme y punzona | Verificar **espesor y qué hay debajo** con calicata que la atraviese |
| **Excavabilidad** | Tosca sana requiere martillo neumático / retro con pica. Encarece pozos y zapatas profundas | Preverlo en el cómputo y en el pliego de movimiento de suelos |
| **Falsa seguridad** | "Pegamos tosca, ya está" | La tosca sana es buen apoyo, pero **no exime del manejo del agua** ni de verificar continuidad |

### 2.4 Topografía urbana: la cuenca centrípeta de Don Tomás

Santa Rosa ocupa una **cuenca centrípeta (endorreica)** cuyo nivel de base es la **laguna Don Tomás**, que recibe el agua pluvial del área circundante. La ciudad no drena a ningún río: **el agua que cae en Santa Rosa se queda en Santa Rosa**, se infiltra o se evapora.

Cotas de referencia (verificado en fuente de divulgación geográfica; **[VER]** contra cartografía municipal o IGN antes de usar en proyecto):

| Sector | Cota aprox. |
|---|---|
| Mesetas del este | **200 msnm** |
| Alturas del norte | **195 msnm** |
| Cota media de la ciudad | **175 – 179 msnm** |
| Sector sudoeste (el más bajo) | **167 msnm** |
| Laguna Don Tomás | **~165 msnm** |

Hay pendientes que en algunos sectores **superan el 3 %**, con descenso pronunciado hacia el oeste y el sur.

> **Consecuencia de proyecto.** La posición del lote dentro de esta cuenca **cambia el problema**:
> - **Sector alto (E y N):** napa más profunda, mayor probabilidad de tosca somera o aflorante, mayor pendiente → el riesgo es la **escorrentía** que entra al lote desde arriba y el **apoyo mixto sobre tosca**.
> - **Sector bajo (SO, entorno de Don Tomás y del Bajo Giuliani):** napa somera, posible saturación estacional, riesgo de **subpresión y anegamiento**, pozos absorbentes que no absorben.
> **Lo primero que hay que mirar de un lote en Santa Rosa es dónde está en la cuenca.** [PD]

### 2.5 Qué significa todo esto para tu lote

| Hecho geológico | Consecuencia directa sobre el proyecto |
|---|---|
| Manto eólico limo‑arenoso poco denso en superficie | Suelo **potencialmente colapsable** en la cota de fundación de una casa baja |
| Tosca a profundidad variable, discontinua | Riesgo alto de **asentamiento diferencial por apoyo heterogéneo** |
| Clima semiárido, 686–753 mm/año de lluvia | El suelo está **naturalmente seco**: por eso es firme, y por eso colapsa cuando se moja |
| Cuenca endorreica sin salida | Todo excedente de agua **queda en el subsuelo urbano** |
| Napa en ascenso sostenido | El escenario de humedad futuro es **peor** que el del día del sondeo |

---

## 3. Napa freática en Santa Rosa — el dato que cambió la ciudad

### 3.1 La cronología del ascenso

Este es, junto con la tosca, **el dato local determinante**. Santa Rosa pasó, en tres décadas, de tener la napa como una curiosidad hidrogeológica a tenerla como un problema de ingeniería civil.

| Momento | Profundidad de la napa | Fuente |
|---|---|---|
| Década de 1970 | "Mucho más profunda, no generaba problemas de ingeniería" | Fábregas, geólogo, docente de Geotecnia UNLPam (verificado) |
| Fines '90 / época de sobreexplotación | **hasta 45 m en el área urbana**, "consecuencia de la sobreexplotación" | Giai & Tullio, UNLPam / Dirección de Aguas de La Pampa (verificado) |
| Comienzos de la década de 1990 (centro) | **~25 m** | Viglizzo (verificado) |
| ~2014 (entorno plaza San Martín) | **~6 m** | Fábregas (verificado) |
| 2017 (centro) | **menos de 5 m** | Viglizzo (verificado) |
| Hoy | **[VERIFICAR con estudio de suelos / consulta a la Administración Provincial del Agua (APA)]** | — |

Fuera del casco urbano, para el mismo acuífero Toay–Santa Rosa–Anguil–Catriló, los niveles estáticos regionales se ubicaban **entre 6,5 y 11 m cerca de Anguil**, y **entre 4 y 6 m hacia el este** (verificado, Giai & Tullio).

> **La conclusión operativa es brutal y simple:** en Santa Rosa, **cualquier antecedente de napa anterior a ~2015 es inservible para proyectar**. Un vecino que te diga "acá nunca hubo agua" está describiendo una ciudad que ya no existe. Y la tendencia registrada es de **ascenso**, no de estabilidad.

### 3.2 Por qué sube — el balance hídrico urbano

El diagnóstico publicado (verificado, Viglizzo, 2017) es un desbalance hídrico urbano:

```
ENTRADAS  ≈ 1.400 mm/año   =   ~700 mm de lluvia  +  ~700 mm importados por acueductos
SALIDAS   ≈ 1.000 mm/año   =   evaporación + evapotranspiración
                              ─────────────────────────────────
EXCEDENTE ≈   400 mm/año   →   se acumula en el subsuelo, año tras año
```

Los factores concurrentes identificados en las fuentes (verificado):

| Factor | Efecto |
|---|---|
| **Fin del bombeo local** (se eliminaron los bombeadores domiciliarios) | Dejó de extraerse agua del acuífero bajo la ciudad |
| **Acueducto de Anguil y acueducto del Río Colorado** | Se importa agua de fuera de la cuenca: entra volumen que antes no entraba |
| **Pérdidas de las redes** de agua y cloaca | Infiltración permanente, distribuida, invisible |
| **Impermeabilización urbana** (pavimento, cubiertas, solados) | Reduce la evapotranspiración, concentra el escurrimiento |
| **Cuenca endorreica** | No hay salida superficial: el excedente sólo puede infiltrarse o evaporarse |

Como testigo de superficie del mismo proceso: la laguna del **Bajo Giuliani pasó de ~550 ha en 1985 a ~1.300 ha en 2015** (verificado, Viglizzo).

### 3.3 Zonas de la ciudad

**No hay publicado un mapa de isoprofundidades de napa de la ciudad de acceso libre.** Existe el antecedente institucional del trabajo *"Registros y análisis del comportamiento piezométrico de las aguas subterráneas del subsuelo de la Ciudad de Santa Rosa"*, que reporta el censo de niveles de **148 perforaciones en el radio urbano realizadas por la Administración Provincial del Agua (APA)** más **21 perforaciones domiciliarias** (verificado en la ficha bibliográfica del Consejo Federal de Inversiones). **Ese es el documento a pedir.** Ver §3.5.

Criterio de lectura del lote mientras tanto, en función de la topografía de §2.4 **[PD]**:

| Posición en la ciudad | Expectativa de napa | Riesgo dominante |
|---|---|---|
| Sector **este / noreste** (cota 195–200) | Más profunda | Tosca somera / apoyo mixto; escorrentía que baja hacia el lote |
| **Casco céntrico** (cota ~175–179) | Somera — antecedente de **~5–6 m** | Subsuelos y cocheras hundidas; filtraciones |
| **Sudoeste**, entorno de Don Tomás y bajos (cota 167 y menos) | **Muy somera / estacionalmente aflorante** | Anegamiento, subpresión, pozo absorbente inoperante, colapso por saturación |
| Barrios sobre bajos rellenados | **Impredecible** | Relleno no controlado + napa: el peor combinado |

Signos publicados del fenómeno en los sectores bajos (verificado): *"afloramientos de agua en superficie", "cloacas que revientan, pavimentos destruidos, sótanos anegados, pisos embebidos, paredes deterioradas"*. Y en el centro, filtraciones en edificios de los años '70 **cuyas fundaciones están a 7 m** (verificado, Fábregas).

### 3.4 Consecuencias directas sobre el proyecto de una casa baja

| Consecuencia | Detalle | Decisión de proyecto |
|---|---|---|
| **Colapso del loess por ascenso** | El ascenso de napa satura el manto y lo colapsa. Ver `estructuras.md` §3.5.7: *"te asienta cuando sube y te asienta cuando baja"* | Diseñar suponiendo que el suelo **se va a mojar** durante la vida útil |
| **Subsuelo / sótano / cochera hundida** | Con napa a 5 m, un sótano de 2,5 m está "seco" hoy y puede no estarlo en 15 años. Subpresión `u = γw·h` = 10 kPa por cada metro de columna | **Recomendación por defecto: no hacer subsuelo en Santa Rosa.** Si se hace: recinto estanco + verificación de flotación + servidumbre de mantenimiento **[FIRMA]** |
| **Pozo absorbente** | Un pozo absorbente sólo funciona con zona no saturada suficiente por debajo. Con napa somera **deja de absorber y se convierte en un pozo de recarga contaminante** | Verificar cota de napa **antes** de proyectar el sistema; evaluar cloaca de red o planta compacta |
| **Contrapiso y piso** | Ascenso capilar sobre la platea/contrapiso | Barrera de vapor bajo contrapiso + capa aisladora horizontal y vertical, siempre |
| **Agresividad química** | El agua freática y el suelo pueden traer sulfatos y cloruros — el loess pampeano tiene **sales solubles de Ca y Na 0,4–1,2 %, con aniones dominantes sulfatos y cloruros** (verificado, ver `estructuras.md` §3.5.2) | **Pedir análisis químico de suelo y agua** y clase de exposición CIRSOC 201. Es el ensayo más barato y el más olvidado |
| **Excavación** | Fundación profunda que llega a napa: pozo inundado, paredes que se derrumban | Replantear el tipo de fundación antes que bombear |

### 3.5 Qué preguntar y a quién

1. **Administración Provincial del Agua (APA) de La Pampa** — organismo que ejecutó el censo de 148 perforaciones urbanas. Pedir: **profundidad de napa registrada en el entorno del lote y serie histórica**.
2. **Al geotécnico, en el pliego:** cota de napa medida, **con fecha y hora de lectura**, medida **estabilizada a 24 h** (no la lectura inmediata en la perforación), y **opinión escrita sobre la variación estacional y la tendencia**.
3. **A los vecinos y a la obra lindera:** ¿pozo absorbente que rebalsa? ¿piso que se humedece? ¿tuvieron que rellenar? ¿hay bomba de achique en alguna cochera?
4. **Al municipio:** ¿el lote está en zona con cloaca de red? ¿hay antecedentes de anegamiento en la manzana?

> **[FIRMA]** La cota de napa adoptada para el proyecto y sus consecuencias (subpresión, tipo de fundación, sistema de efluentes) son responsabilidad del profesional que firma el cálculo. El arquitecto **exige el dato**; no lo estima.

---

## 4. Loess colapsable aplicado a una casa de una planta

La teoría está en `estructuras.md` §3.5. Acá va **sólo lo que cambia cuando la obra es una casa baja**.

### 4.1 La paradoja de la casa liviana

La intuición dice: *"es una casa de una planta, pesa poco, cualquier suelo la aguanta"*. En loess, esa intuición es exactamente al revés. Cuatro razones:

**1. La carga no es el problema — el agua es el problema.**
El colapso del loess no lo dispara la tensión de contacto: lo dispara el **humedecimiento**. En el caso extremo, el loess **autocolapsable** *"colapsa espontáneamente al humedecerse, sin necesidad de carga exterior"* — literalmente, **el propio peso del suelo alcanza** (verificado, ver `estructuras.md` §3.5.3 y §3.5.4). Una casa que pesa poco no está protegida: está igual de expuesta, y con menos margen para verificar.

**2. La fundación superficial está dentro de la capa activa.**
Un edificio en altura funda a 3–6 m, por debajo de la zona de variación de humedad. Una casa baja funda a 0,80–1,20 m: **exactamente en el estrato que se moja con la lluvia, el riego, el pozo absorbente y la rotura de un caño.** Es la peor cota posible en cuanto a exposición.

**3. La relación perímetro/superficie es máxima.**
Una casa de 120 m² tiene del orden de 45–50 m de perímetro: **~0,4 m de borde por cada m² cubierto**. Un edificio de 600 m² de planta tiene ~0,17 m/m². La casa baja es, geométricamente, la construcción **más expuesta al agua de su propio contorno** — canteros, veredas, bajadas pluviales, riego.

**4. La estructura no tiene reservas.**
Un pórtico de hormigón de un edificio redistribuye esfuerzos ante un asentamiento diferencial. Una casa de **mampostería portante** no redistribuye nada: **fisura**. Y las patologías se ven, porque la casa es la vivienda de alguien y sus paredes están a la vista todos los días.

| | Casa PB 120 m² | Edificio PB+9 |
|---|---|---|
| Tensión de contacto típica **[PD]** | 0,3 – 0,8 kg/cm² | 2 – 4 kg/cm² |
| Cota de fundación típica | 0,8 – 1,2 m | 3 – 8 m |
| Perímetro / m² cubierto **[PD]** | ~0,40 m/m² | ~0,17 m/m² |
| ¿Estudio de suelos habitual? | **A menudo se omite** ← el problema | Siempre |
| ¿Estructura redundante? | No (mampostería portante) | Sí (pórticos) |
| Exposición al agua de superficie | **Máxima** | Baja |

> **Conclusión:** la casa de una planta tiene **el menor beneficio de la carga y la máxima exposición al agua**. Por eso es un caso delicado. Y por eso, en Santa Rosa, **el proyecto de la fundación de una casa baja es más un problema de hidráulica de superficie que de mecánica de suelos.**

### 4.2 El mecanismo, aplicado a esta obra

```
DÍA 0 — Entrega de obra                          AÑO 3 — Cantero regado contra el muro sur
                                                  o bajada pluvial que descarga al pie
 Loess seco: ω ≈ 10-15 %                          Loess saturado local: ω → 25-30 %
 γd ≈ 12-14 kN/m³, e ≈ 1,0                        Se disuelven los puentes de arcilla y sales
 σadm "a humedad natural" 1,0-1,5 kg/cm²          σadm real cae a 0,3-0,8 kg/cm² (o menos)
 Todo firme, ninguna fisura                       ΔH/H = 3 a 10 % del espesor humedecido
                                                  → asentamiento LOCAL de 2 a 10 cm
                                                  → NO uniforme → distorsión angular
                                                  → fisura a 45° arrancando del dintel

                        La casa no se hundió: se DESNIVELÓ EN UN SECTOR.
```

Valores de referencia del loess argentino en `estructuras.md` §3.5.2 y §3.4 (verificados de Rocca–Redolfi–Terzariol y Núñez et al.). El dato que hay que tener grabado: en ensayo de placa, **al saturarse se observan descensos de 10 a 20 veces** el asiento a humedad natural (verificado).

### 4.3 Los ocho disparadores reales en una vivienda

Ordenados por frecuencia observada en la práctica **[PD]**, todos evitables desde el proyecto:

| # | Disparador | Dónde se origina | Capítulo que lo resuelve |
|---|---|---|---|
| 1 | **Cantero / césped regado contra el muro** | Paisajismo | §8.6 |
| 2 | **Bajada pluvial que descarga al pie de la fundación** | Proyecto de desagües | §8.3 |
| 3 | **Vereda perimetral inexistente, angosta, con pendiente hacia la casa o fisurada** | Proyecto y ejecución | §8.2 |
| 4 | **Pérdida de cañería enterrada** (agua o cloaca) sin detección | Instalaciones | §8.4 |
| 5 | **Pozo absorbente demasiado cerca** | Instalaciones | §8.5 |
| 6 | **Pileta con pérdida o desborde** | Proyecto exterior | §8.7 |
| 7 | **Ascenso de napa** | Fuera del control del proyecto | §3, §7 |
| 8 | **Terreno con contrapendiente hacia la casa** / lote que recibe escorrentía del vecino | Nivelación general | §8.2, §8.3 |

> Siete de los ocho son **decisiones de arquitectura, no de cálculo estructural.** Esa es la tesis de este documento.

### 4.4 Por qué la casa baja es el peor caso de exposición

Un detalle contraintuitivo que conviene tener claro para discutir con el cliente: **la platea y el solado que la cubre impermeabilizan el suelo bajo la casa**. El agua de riego y lluvia que entra por el perímetro no puede evaporar hacia arriba — queda debajo. Ese es el "efecto invernadero" de la fundación: la humedad se acumula justo bajo el borde de la construcción. Por eso las patologías de colapso en vivienda son **perimetrales y de esquina**, no centrales. **[PD]**

---

## 5. Parámetros geotécnicos de referencia para Santa Rosa

### 5.1 Declaración honesta sobre el estado del dato publicado

**No se localizó ningún banco de datos geotécnicos publicado y de acceso libre para la ciudad de Santa Rosa** que dé tensiones admisibles, perfiles de N‑SPT o índices de colapso por zona o por barrio. Se buscó específicamente en: repositorio de la UNLPam, SEGEMAR, INTA Anguil, Administración Provincial del Agua, Consejo Federal de Inversiones y literatura geotécnica argentina.

Lo que **sí** existe y está verificado:

| Existe | No existe (públicamente) |
|---|---|
| Cartografía geológica regional (SEGEMAR, Hojas 3763‑I Santa Rosa y 3763‑III Darregueira) | Mapa de tensiones admisibles de la ciudad |
| Estratigrafía e hidrogeología del acuífero (UNLPam / Dirección de Aguas) | Perfiles de N‑SPT publicados por barrio |
| Profundidad de tosca a escala agronómica (INTA Anguil) | Perfiles de colapsabilidad (σ₀ vs. σ_F.SAT) de la ciudad |
| Caracterización general del loess argentino (Rocca–Redolfi–Terzariol) | Base de datos de estudios de suelos urbanos |
| Registro piezométrico urbano de la APA (148 perforaciones) — **existe, hay que pedirlo** | Publicación abierta de ese registro |

> **[FIRMA] Por eso el estudio de suelos es obligatorio igual — de hecho, *más* obligatorio.**
> Precisamente porque **no hay dato local publicado**, no existe la alternativa de "usar la experiencia de la zona". La única fuente legítima de la tensión admisible de tu lote es el ensayo en tu lote.
> **Si alguien te da una tensión admisible para Santa Rosa sin haber ensayado el terreno, ese número no tiene respaldo y no debe usarse.**
> Y hay una segunda razón, específica de acá: la variabilidad local es alta (tosca discontinua a profundidad variable + napa en ascenso). Un "valor típico de la zona" sería inútil aunque existiera.

### 5.2 Órdenes de magnitud utilizables — y de dónde salen

Los valores que siguen **no son de Santa Rosa**: son del loess pampeano en general y sirven **sólo para dimensionar el anteproyecto y para detectar un informe absurdo**. Están tomados de `estructuras.md` §3.4 y §3.5.2, verificados de Rocca–Redolfi–Terzariol (2006) y Bolognesi (1975).

**Propiedades índice esperables en el manto eólico superficial [PD, no local]:**

| Propiedad | Rango del loess reciente argentino | Comentario para Santa Rosa |
|---|---|---|
| Clasificación SUCS | **ML ó CL‑ML** | Limo de baja plasticidad |
| Granulometría | Arena 5–15 %, limo 40–60 %, arcilla 20–35 % | En Santa Rosa el manto es más arenoso: **franco arenoso muy fino, ~16 % arcilla y hasta ~32 % limo** (verificado, INTA, horizonte agronómico) |
| Humedad natural ω | **8,0 – 25,0 %** | En clima semiárido, esperable el extremo bajo |
| Peso unitario seco γd | **11,0 – 14,0 kN/m³** | γd < 14 kN/m³ en un limo → **sospechar colapsabilidad** |
| Límite líquido ωL | 22 – 30 % | |
| Índice plástico IP | 4 – 7 % | IP bajo con e alto → sospechar |
| φ′ (triaxial drenado, saturado) | ≈ **24°** | |
| Sales solubles Ca y Na | 0,4 – 1,2 %; aniones dominantes sulfatos y cloruros | **Exigir análisis químico** |

**Tensión admisible — rangos generales del loess [PD, no local]** (de `estructuras.md` §3.4):

| Condición | σ_adm (kg/cm²) |
|---|---|
| Loess a humedad natural, no colapsable | 1,0 – 2,0 |
| Loess colapsable, **a humedad natural** | 0,8 – 1,5 *aparente* |
| Loess colapsable, **saturado** | **0,3 – 0,8 (o menos)** |
| Loess **autocolapsable** | **NO APTO para fundación directa** |

> **Cómo se usa esta tabla: para hacer UNA pregunta.**
> Cuando llegue el informe con, por ejemplo, σ_adm = 1,2 kg/cm², preguntar:
> **"¿Este valor es a humedad natural o en condición saturada?"**
> Si la respuesta es "a humedad natural" y no hay análisis de colapsabilidad, **el estudio está incompleto** y no sirve para proyectar en Santa Rosa. Para una casa baja, **el valor que gobierna es el saturado**, porque el suelo bajo el borde de la casa se va a mojar (§4.4).

**N‑SPT esperable:** **[VERIFICAR con estudio de suelos]** — y ver la advertencia de §5.3, que es la razón por la que no se dan valores aquí.

**Índice / potencial de colapso (PC):** **[VERIFICAR con estudio de suelos]**, mediante doble edométrico sobre muestra inalterada. Escala de severidad de Jennings y Knight en `estructuras.md` §3.5.5 (0–1 % no problemático; 1–5 % moderado; 5–10 % problema; 10–20 % severo; >20 % muy severo).

**Profundidad del estrato apto para fundar:** **[VERIFICAR con estudio de suelos]**. En Santa Rosa las dos hipótesis realistas son (a) **manto eólico mejorado/compactado** en el primer metro, o (b) **techo de tosca sana** entre ~0,5 y ~2,5 m. Cuál de las dos, y a qué cota exacta, es lo que el estudio tiene que decir.

### 5.3 El SPT miente en loess sobre napa — lo dice el CIRSOC 401

Este es probablemente el dato técnico más útil de todo el documento a la hora de contratar el estudio.

**CIRSOC 401 (Reglamento Argentino de Estudios Geotécnicos), Comentario C 3.6.7 — Suelos colapsables (texto verificado):**

> *"a) **Por encima del nivel freático.** Los ensayos de penetración estándar son **poco representativos**. Tienden a **sobrestimar la compacidad relativa** debido a la alta fricción lateral.*
> *b) **Por debajo del nivel freático.** En esta situación son representativos los ensayos de penetración estándar, estática y dinámica‑estática."*
>
> *"En aquellos suelos en los que por su granulometría o por su baja cohesión no se puedan obtener muestras de calidad suficiente como para realizar los ensayos de laboratorio necesarios [...] se podrá ejecutar el **ensayo de placa en condición saturada**."*

Y el **artículo 3.6.7** del propio Reglamento (texto verificado) fija el método de exploración:

> *"La exploración de los suelos colapsables depende de su posición relativa con respecto al nivel freático:*
> *(a) **por encima del nivel freático** y hasta la profundidad en que pueda ser ejecutado de manera segura: **calicatas y pozos excavados a cielo abierto**. El **muestreo se realizará mediante la obtención de damas de lado mínimo 0,25 m**, de donde se tallarán los especímenes necesarios.*
> *(b) por debajo del nivel freático: perforaciones por avance a percusión o rotación con la utilización de sacatestigos."*

> **Consecuencia directa para tu casa.** El manto de apoyo de una vivienda de una planta en Santa Rosa está **por encima de la napa**. Por lo tanto:
> - **El método de exploración reglamentario es la calicata con muestreo en dama (bloque) de al menos 25 cm de lado**, no el SPT.
> - Un informe basado sólo en N‑SPT, en ese estrato, **sobrestima la compacidad** y por lo tanto **da una tensión admisible optimista**.
> - Ese es el mecanismo por el cual un informe formalmente correcto conduce a una fundación insuficiente. **[FIRMA]**

### 5.4 Tabla de parámetros a exigir al informe

| Parámetro | Unidad | ¿Quién lo da? | Estado |
|---|---|---|---|
| Perfil estratigráfico con clasificación SUCS por estrato | — | Geotécnico | [VERIFICAR con estudio de suelos] |
| **Cota del techo de tosca en cada punto de exploración** | m | Geotécnico | **[VERIFICAR — dato crítico en Santa Rosa]** |
| **Espesor de la tosca y qué hay debajo** | m | Geotécnico | **[VERIFICAR — crítico]** |
| Peso unitario natural γ y seco γd por estrato | kN/m³ | Laboratorio | [VERIFICAR] |
| Humedad natural ω por estrato | % | Laboratorio | [VERIFICAR] |
| Límites de Atterberg (ωL, ωP, IP) | % | Laboratorio | [VERIFICAR] |
| N‑SPT por metro (si se hace SPT) | golpes/30 cm | Campo | [VERIFICAR] + leer §5.3 |
| **Potencial de colapso PC (doble edométrico, muestra inalterada)** | % | Laboratorio | **[VERIFICAR — innegociable en Santa Rosa]** |
| **Presión de fluencia saturada σ_F.SAT vs. presión de tapada σ₀** | kPa | Laboratorio | **[VERIFICAR — define si es autocolapsable]** |
| **σ_adm a humedad natural Y en condición saturada**, con Df y B de referencia | kg/cm² | Geotécnico | **[VERIFICAR — pedir las dos]** |
| Asentamiento total y diferencial estimado para la carga prevista | mm | Geotécnico | [VERIFICAR] |
| Módulo de balasto k (con ancho de referencia) — si va platea | kg/cm³ | Geotécnico | [VERIFICAR] |
| **Nivel freático medido, con fecha, estabilizado a 24 h** | m | Campo | **[VERIFICAR — crítico]** |
| Sulfatos, cloruros, sales solubles totales, pH, materia orgánica + clase de exposición CIRSOC 201 | ppm / % | Laboratorio | [VERIFICAR] |
| Recomendación explícita de tipo y cota de fundación | — | Geotécnico | [VERIFICAR] **[FIRMA]** |

---

## 6. Estudio de suelos para una casa de una planta

### 6.1 ¿Hace falta? Respuesta honesta

**Sí. En Santa Rosa, para una casa de una planta, hace falta.** La respuesta honesta y fundada, sin marketing:

**Argumentos por los que a veces se omite (y por qué no aplican acá):**

| Argumento habitual | Por qué no vale en Santa Rosa |
|---|---|
| "Es una casa liviana" | El colapso lo dispara el agua, no la carga (§4.1) |
| "Toda la cuadra está construida y no pasa nada" | La napa subió ~20 m en 30 años: las casas de los '80 se construyeron en otro suelo (§3.1) |
| "Ya sé cómo es el suelo de la zona" | No hay dato local publicado, y la tosca varía dentro del mismo lote (§2.3, §5.1) |
| "El estudio sale caro" | Es el ítem más barato del proyecto y el único irreversible (§6.7) |
| "El municipio no lo pide" | Que no lo pida el municipio no lo hace innecesario, y **no traslada la responsabilidad profesional** **[FIRMA]** |

**El único caso en que se puede discutir** es un lote en zona alta, con antecedentes ciertos y documentados de la manzana, tosca aflorante confirmada y sin napa somera — y aun así **lo que se ahorra no es el estudio, es el SPT**: la calicata sigue siendo obligatoria (§6.3). En un lote con relleno, en zona baja, cerca de bajos o sin antecedentes, **no hay discusión posible**.

### 6.2 Lo que exige el CIRSOC 401 (verificado)

**Cantidad mínima de prospecciones — Tabla 3.1 del CIRSOC 401** (texto verificado):

| Clase | Descripción de la tipología estructural | Cantidad mínima de prospecciones | Coeficiente α |
|---|---|---|---|
| **C‑1** | **Viviendas unifamiliares de dos plantas con una superficie máxima en planta de 250 m² en condiciones geotécnicas conocidas** | **2** | 1,0 |
| **C‑2** | **Edificios para vivienda o industriales hasta 2 plantas** | **3** | 1,0 |
| C‑3 | Edificios para vivienda o industriales de hasta 4 plantas sin muros de carga | 3 | 1,0 |
| C‑7 | Construcciones complementarias con área de fundación menor a 50 m² | 1 | 1,0 |

**Distancia máxima entre prospecciones:** `l = α · l₀`

**Tabla 3.2 del CIRSOC 401 — distancias máximas según tipo de terreno** (texto verificado):

| Grupo | Distancia l₀ | Ejemplo dado por el Reglamento |
|---|---|---|
| **T‑1: variabilidad baja** | **l₀ = 30 a 40 m** | **"Grandes llanuras loésicas"** ← es literalmente nuestro caso |
| T‑2: variabilidad media | l₀ = 20 a 30 m | Coladas basálticas |
| T‑3: variabilidad alta | l₀ = 20 m | Antiguas llanuras de inundación de ríos divagantes |

**Profundidad de investigación — art. 3.5.6.2** (texto verificado). Será **mayor o igual al máximo entre**:

- **seis metros (6 m)**;
- la profundidad del plano de fundación **más 2 veces el ancho de la mayor zapata individual** o del grupo de pilotes, o **10 veces el diámetro** del pilote aislado;
- la profundidad a la que el incremento de tensión efectiva vertical sea igual al **10 % de la presión efectiva de tapada, en suelos cohesivos**;
- la profundidad a la que ese incremento sea igual al **20 % de la presión efectiva de tapada, en suelos granulares**.

El Reglamento agrega (verificado): *"Cuando la profundidad de investigación atraviese estratos de características geotécnicas conocidas y favorables [...] la profundidad de investigación se podrá limitar a la detección fehaciente del contacto entre el estrato competente y el inmediato superior."*

Y los **Comentarios** al art. 3.5.5 ilustran, para predios cuadrados y rectangulares, **N_mín = 3** puntos de exploración (con ejemplos de 5, 6, 8 y 9 según la forma y la presencia de zonas problemáticas) (verificado).

> **Lectura para tu casa en Santa Rosa [PD]:**
> - Casa de PB en lote urbano típico (10 × 30 a 15 × 40): **mínimo 2 prospecciones, recomendable 3**, distribuidas en las esquinas del área cargada.
> - **Profundidad mínima: 6 m.** Si aparece tosca sana antes, se aplica la excepción del art. 3.5.6.2 — **pero hay que atravesarla y demostrar el contacto con lo que hay debajo**, no detenerse al primer rebote.
> - La distancia máxima entre puntos (30–40 m) casi nunca gobierna en un lote urbano: **lo que gobierna es la cantidad mínima**.
> - La Clase C‑1 exige "condiciones geotécnicas **conocidas**". En Santa Rosa, con napa en ascenso y tosca errática, **es difícil sostener que las condiciones son conocidas**: por eso el criterio de oficina es adoptar C‑2 → **3 prospecciones**.

### 6.3 Calicata vs. SPT en Santa Rosa

| | **Calicata** | **SPT (perforación con penetración estándar)** |
|---|---|---|
| Qué da | Perfil visual continuo, **espesor real y contacto de la tosca**, **muestra inalterada en dama** (imprescindible para el doble edométrico), estado de humedad real | N por metro, perfil hasta gran profundidad, detección de napa profunda |
| Profundidad práctica | Hasta ~2,5–3,0 m (límite de seguridad y de equipo) | 6 m o más, sin límite práctico |
| En loess sobre napa | **Método exigido por CIRSOC 401 art. 3.6.7** | **"Poco representativo", "sobrestima la compacidad"** (C 3.6.7) |
| Ve la tosca | **Sí, la ve y la mide** | La detecta como rechazo, pero **no distingue banco sano de nódulo** |
| Costo relativo | Bajo | Medio |
| Riesgo | Excavación de más de 1,20 m: **entibado / talud obligatorio** — no bajar a una calicata sin protección **[FIRMA]** | — |

> **Recomendación de oficina para una casa de una planta en Santa Rosa [PD]:**
> **Combinar los dos.** No es "calicata *o* SPT": es
> - **2 a 3 calicatas** de 1,50–2,50 m, ubicadas bajo el área de la casa, **con muestreo en dama de ≥ 0,25 m de lado** para doble edométrico y densidad; y
> - **1 sondeo con SPT hasta 6 m** (o hasta atravesar la tosca y reconocer lo que hay debajo), para completar la profundidad reglamentaria y **medir la napa estabilizada**.
>
> El sobrecosto respecto de "sólo dos calicatas" es marginal frente al costo del proyecto, y es lo que separa un informe que responde a las preguntas correctas de uno que no.

### 6.4 Pliego del estudio — texto para copiar y pegar

> **PLIEGO DE ESTUDIO GEOTÉCNICO — Vivienda unifamiliar de planta baja, Santa Rosa (La Pampa)**
>
> **1. Alcance.** Estudio geotécnico para proyecto, conforme al Reglamento CIRSOC 401. Obra: vivienda unifamiliar de planta baja, superficie cubierta aproximada ____ m², estructura de mampostería portante / hormigón armado (tachar lo que no corresponda), sin subsuelo.
>
> **2. Antecedentes a entregar por el comitente.** Plano de mensura, plano de anteproyecto con implantación acotada y niveles, relevamiento planialtimétrico del lote, fotografías del estado actual y de las construcciones linderas.
>
> **3. Exploración mínima requerida.**
> - **Tres (3) calicatas** de 1,50 m mínimo de profundidad, o hasta el techo de tosca sana **más 0,50 m de penetración en ella**, ubicadas dentro de la impronta de la construcción y acotadas en plano.
> - **Muestreo inalterado en damas de lado mínimo 0,25 m**, conforme art. 3.6.7 del CIRSOC 401, de cada estrato representativo por encima del nivel freático.
> - **Un (1) sondeo con ensayo de penetración estándar (SPT)** hasta **6,00 m** de profundidad como mínimo (art. 3.5.6.2), o hasta atravesar el banco de tosca y reconocer fehacientemente el estrato inmediato inferior.
> - Registro de **nivel freático**, con lectura **estabilizada a 24 horas**, **fecha y hora**.
>
> **4. Ensayos de laboratorio mínimos.** Granulometría y límites de Atterberg por estrato; humedad natural; peso unitario natural y seco; **doble ensayo edométrico (probeta a humedad natural y probeta saturada) sobre muestra inalterada de cada estrato de apoyo potencial**; determinación de **potencial de colapso PC** y de **presión de fluencia saturada σ_F.SAT**; análisis químico de suelo (**sulfatos, cloruros, sales solubles totales, pH, materia orgánica**) y del agua freática si se la alcanza.
>
> **5. Contenido mínimo del informe.**
> a) Plano de ubicación acotada de calicatas y sondeo, con cotas referidas al nivel de vereda.
> b) Perfiles individuales y **perfil geotécnico interpretado entre puntos**.
> c) **Cota del techo de tosca en cada punto, su espesor y descripción del estrato subyacente.** Opinión expresa sobre **continuidad lateral de la tosca bajo la impronta de la casa**.
> d) **Perfil de colapsabilidad**: σ₀ y σ_F.SAT en profundidad, con y sin el incremento de presión de la obra. Clasificación del suelo como **no colapsable / potencialmente colapsable / autocolapsable**.
> e) **Tensión admisible recomendada, indicada por separado a humedad natural y en condición saturada**, con indicación del tipo de fundación supuesto, ancho B y profundidad Df de referencia y factor de seguridad adoptado.
> f) **Estimación de asentamientos totales y diferenciales** para la carga prevista, en ambas condiciones de humedad.
> g) **Módulo de balasto** con su ancho de referencia, si se recomienda platea.
> h) **Recomendación explícita de tipo de fundación y cota de fundación**, y de tratamiento del suelo (sustitución, compactación, espesor y densidad exigida) si corresponde.
> i) Nivel freático medido, **evolución estacional estimada y opinión sobre la tendencia de ascenso en el sector**.
> j) Clase de exposición del hormigón según CIRSOC 201 y tipo de cemento recomendado.
> k) Recomendaciones de excavación: taludes estables, entibado, drenaje.
> l) **Firma de profesional matriculado con incumbencia en geotecnia.**
>
> **6. Reunión previa.** El profesional geotécnico recibirá el anteproyecto **antes** de ejecutar los trabajos y podrá proponer ajustes a la ubicación de las prospecciones.

### 6.5 Cómo se lee el informe

Orden de lectura recomendado — **no** empezar por la tensión admisible:

1. **El plano de ubicación.** ¿Los puntos están **bajo la casa** o los hicieron donde entraba la máquina? Si están todos sobre un eje, no hay información transversal.
2. **La fecha.** Un informe de hace 5 años en Santa Rosa **tiene la napa mal** (§3.1).
3. **El nivel freático y su fecha de lectura.** Si dice "no se detectó napa hasta la profundidad explorada", verificar **hasta qué profundidad exploró**. "No hay napa a 3 m" no es "no hay napa".
4. **El perfil: dónde está la tosca en cada punto.** Comparar los puntos entre sí. **Si difieren mucho, ahí está el problema del proyecto.**
5. **¿Hay doble edométrico?** Si no lo hay, **el informe no responde la pregunta central en loess** y hay que pedirlo.
6. **La tensión admisible: ¿a qué humedad, para qué B y qué Df?** Una σ_adm sin B y Df de referencia es un número sin significado.
7. **Los asentamientos estimados.** Es el número que realmente gobierna el diseño de una casa de mampostería, más que la rotura del suelo.
8. **El análisis químico y la clase de exposición.** Si falta, hay que pedirlo **antes de hormigonar**: después no hay reparación posible.
9. **La firma y la matrícula.**

**Señales de alarma en un informe:**

| Señal | Qué significa |
|---|---|
| Una sola perforación | Incumple CIRSOC 401 Tabla 3.1 para vivienda |
| Sin doble edométrico en suelo limoso | No evaluó colapsabilidad. Inservible acá |
| σ_adm sin aclarar condición de humedad | Ver §5.2. Preguntar |
| "Se recomienda fundar a 1,00 m con 1,5 kg/cm²" y nada más | Informe de trámite, no de proyecto |
| Sin análisis químico | Falta el ensayo más barato y más olvidado |
| Perfil "tipo" que no corresponde a los pozos reales | Copiado de otro trabajo |
| Napa "no detectada" sin decir hasta qué profundidad | Ambiguo por omisión |

### 6.6 Diez preguntas al geotécnico

1. **¿Esta tensión admisible es a humedad natural o en condición saturada?** ¿Cuál me recomienda adoptar para una casa que va a tener riego y jardín alrededor?
2. **¿El suelo de apoyo es potencialmente colapsable o autocolapsable?** ¿Con qué ensayo lo determinó?
3. **¿Cuánto vale el potencial de colapso PC y a qué presión lo midió?**
4. **¿A qué cota está la tosca en cada punto, y es continua bajo toda la casa?** ¿Qué hay debajo de ella?
5. **¿Cuál es la profundidad mínima de fundación que recomienda para quedar por debajo de la capa activa de humedad?**
6. **¿Platea o zapata corrida? ¿Por qué?** ¿Recomienda sustitución de suelo? ¿Qué espesor y a qué densidad Proctor?
7. **¿Qué asentamiento total y diferencial estima si el suelo se satura localmente?**
8. **¿A qué profundidad midió la napa, en qué fecha, y qué tendencia le atribuye en este sector de la ciudad?**
9. **¿Hay riesgo de agresividad química? ¿Qué clase de exposición CIRSOC 201 y qué cemento?**
10. **Si tuviera que poner un pozo absorbente en este lote, ¿dónde lo pondría y a qué distancia mínima de la casa?**

> Estas preguntas se hacen **por escrito** y las respuestas se archivan con el expediente. No son una desconfianza hacia el profesional: son la forma de que el informe sea útil para proyectar. Un buen geotécnico las agradece.

### 6.7 Costo relativo del estudio vs. costo de reparar

No se dan valores en pesos (se desactualizan en semanas). Se da la **relación**, que es estable:

| Concepto | Orden de magnitud relativo **[PD]** |
|---|---|
| **Estudio geotécnico completo** (3 calicatas + 1 SPT + laboratorio con doble edométrico + química) | **~0,3 – 0,8 % del costo de la obra** |
| Sobrecosto de pasar de zapata corrida a **platea** bien resuelta | ~2 – 5 % del costo de la obra |
| Sobrecosto de **sustitución de suelo** de 0,60–1,00 m bajo la platea | ~1 – 3 % del costo de la obra |
| **Recalce** de una vivienda con asentamiento diferencial (pilotines, inyecciones, apuntalamiento, reparación de mampostería, revoques, pisos, aberturas, mudanza) | **~15 – 40 % del costo de la obra**, y a veces más |
| Peritaje, honorarios legales y tiempo si el caso va a juicio | No acotable |

> **La aritmética.** El estudio cuesta del orden de **1/40 a 1/100 de lo que cuesta reparar el problema que evita.** Y la reparación **nunca deja la casa como estaba**: quedan las fisuras selladas, el piso desnivelado y el valor de reventa afectado.
>
> **La frase para el cliente:** *"El estudio de suelos es el único ítem del presupuesto que, si lo sacamos, no se puede volver a poner después."*

---
