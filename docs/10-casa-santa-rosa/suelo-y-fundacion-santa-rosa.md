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

1. **Santa Rosa se funda sobre un manto eólico suelto (Fm. Meaucó) de 0,20 a 2 m de espesor, que cubre una costra calcárea (tosca) que a su vez corona la Formación Cerro Azul** (verificado, SEGEMAR, Hoja 3763‑I Santa Rosa, 2023). El basamento granítico está a **144 m**. **Todo lo que le importa a una casa está en los primeros 2 m — y ese manto es también donde se aloja la napa freática.**
2. **La tosca (calcrete) es el rasgo determinante de la fundación en La Pampa.** En el entorno Santa Rosa–Anguil los suelos dominantes tienen **tosca entre 0,50 y 1,50 m**, y otros con tosca **por debajo de 1,50 m** (INTA, verificado). El *hardpan* puede llegar a **1 m de espesor**, pero **hacia el este del área los calcretes son inmaduros y suelen carecer de él** (verificado, SEGEMAR). Su profundidad y calidad **varían dentro de un mismo lote**.
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

La secuencia, de abajo hacia arriba (verificado — SEGEMAR, *Hojas Geológicas 3763‑I Santa Rosa y 3763‑III Darregueira*, 2023; y Giai & Tullio, UNLPam / Dirección de Aguas de La Pampa):

- **Basamento cristalino.** En Santa Rosa se alcanzó, y es **de carácter granítico, a 144 m de profundidad**. Hacia el este se profundiza por un sistema de fracturas (en Uriburu y hacia el este se infiere a 4–5 km, dentro de la cuenca de Macachín).
- **Formación Macachín** (arcilitas verdes, Mioceno), donde está presente, bajo Cerro Azul. Comportamiento hidrogeológico **acuícludo a acuitardo**.
- **Formación Cerro Azul** (Mioceno superior): limos arenosos, limolitas y areniscas muy finas. Es la unidad que aloja el acuífero de abastecimiento. **Espesor máximo del orden de 190 m.** Entre **50 y 130 m de profundidad** (≈ 70–90 msnm) suele encontrarse una **intercalación arcillosa** que secciona hidráulicamente el acuífero: por debajo el agua es salada, por arriba dulce. Es la **"roca almacén de un acuífero multicapa"**, con comportamiento **acuífero‑acuitardo**, que alberga el **Acuífero Toay–Santa Rosa–Anguil–Catriló** (verificado, SEGEMAR).
- **Calcrete (tosca)** — corona la Formación Cerro Azul **"conformando la parte superior de una planicie estructural"**. En la Hoja Santa Rosa esa planicie va de **cota 230 m en el límite occidental** y desciende hacia el este con un **gradiente de 1,10 m/km** hasta **cota 120 m**, *"hundiéndose finalmente bajo el campo de dunas que caracteriza el sector oriental"* (verificado, SEGEMAR). Hidrogeológicamente es **una planicie calcárea de baja permeabilidad que reduce la infiltración**.
- **Formación Meaucó** (Pleistoceno–Holoceno) — los **depósitos eólicos** que forman la superficie actual. Se reconoce *"prácticamente en toda la superficie de las hojas Santa Rosa y Darregueira, ya sea como un manto continuo que cubre al calcrete de la planicie estructural, o en los flancos de los valles transversales o bajos, cubriendo a la Formación Cerro Azul, **con espesores variables entre 0,20 a 2 metros**"* (verificado, SEGEMAR). En los valles transversales y en el campo de dunas, en cambio, alcanza *"espesores que oscilan entre **3 y 30 m** sobre el nivel topográfico"*.

**Litología del manto eólico superficial — el suelo de fundación de tu casa** (verificado, SEGEMAR): *"material eólico areno‑limoso o limo‑arenoso, **suelto**, color castaño, con tintes rojizos o gris parduzcos a negros"*. Granulometría de la facies eólica de manto: **arena muy fina 34 %**, arena fina 16 %, limos medianos 14 %, limos gruesos 13 %, resto 23 %.

Composición de la Fm. Cerro Azul, según su análisis litoestratigráfico (verificado, Rev. Asoc. Geol. Argentina): **alternancia de limolitas y areniscas, que constituye el 92 % de la sucesión**, con intercalaciones de arcilitas en los estratos basales (**7 %**); hacia el techo se desarrollan **calcretes que coronan la sucesión (1 %)**.

> **Traducción para el proyecto — y es el dato que ordena todo el documento:**
> **La casa se funda en un manto eólico suelto de arena muy fina y limo, de 0,20 a 2 m de espesor, apoyado sobre una costra calcárea.**
> Es decir: la cota de fundación de una casa de una planta (0,80–1,20 m) cae **exactamente en el rango de espesor de ese manto suelto** — o justo en el contacto con la tosca. Los 144 m de abajo son irrelevantes para la fundación de una vivienda; sí importan para entender la napa.

**Y un dato hidrogeológico que cambia el diagnóstico:** la Unidad Hidroestratigráfica I del SEGEMAR — los depósitos eólicos de la Fm. Meaucó — tiene *"elevada permeabilidad", constituye "zonas de recarga excepcionales"*, y **"en esta unidad se aloja el acuífero freático"** (verificado). Es decir: **el mismo manto eólico suelto en el que apoya la casa es el que aloja la napa freática y el que infiltra el agua de lluvia y de riego.** No hay ninguna barrera entre el agua de superficie y el suelo de fundación.

### 2.2 Columna estratigráfica típica de la ciudad

**Perfil de referencia — orden de magnitud, no dato de proyecto:**

| Prof. aprox. | Unidad | Descripción esperable | Relevancia para la casa |
|---|---|---|---|
| 0,00 – 0,30 m | Suelo vegetal / relleno antrópico | Materia orgánica, escombro, restos de obra. En lotes urbanos casi siempre hay relleno no controlado | **Se retira siempre.** Nunca fundar sobre él |
| **0,20 – 2,00 m** *(espesor verificado del manto, SEGEMAR)* | **Fm. Meaucó — manto eólico** | Material areno‑limoso o limo‑arenoso, **suelto**, castaño. Arena muy fina dominante (34 %) | **Es el estrato de apoyo típico de una casa baja. Es el estrato problemático.** Y es donde se aloja la napa freática |
| Variable, desde ~0,50 m | **Tosca / calcrete** | De nódulos dispersos a **hardpan de hasta 1 m** de espesor. Perfil interno: hospedante → pulverulento → nodular → laminar → macizo | Si aparece continua y madura: **excelente apoyo**. Si es discontinua o inmadura: **fuente de asentamiento diferencial** |
| Por debajo | Fm. Cerro Azul | Limolitas y areniscas muy finas, con nódulos y bancos de carbonato | Sólo relevante para pozos/pilotines profundos |

**En valles transversales y campo de dunas** (sector oriental y nordeste de la Hoja Santa Rosa) el manto eólico pasa a **3 – 30 m de espesor** (verificado, SEGEMAR) y **desaparece el apoyo en tosca**: escenario completamente distinto, y mucho más exigente.

**[VERIFICAR con estudio de suelos]** — Esta columna es un marco de lectura, **no un perfil de proyecto**. En Santa Rosa la variabilidad lateral es alta a escala de lote: la tosca puede estar a 0,60 m en un extremo del terreno y a 2,50 m en el otro, o aparecer y desaparecer.

### 2.3 La tosca (calcrete): qué es, dónde está, cuánto mide

**Qué es.** Costra calcárea (calcrete) — *"acumulaciones de carbonato cálcico"* — formada por **procesos pedogenéticos** bajo clima semiárido: infiltración, precipitación y recristalización de carbonato en el perfil de suelo, con participación de raíces y microorganismos (verificado, SEGEMAR, citando a Calmels y Carballo 2006). **No es una roca de fundación uniforme: es un horizonte de suelo endurecido, con estructura interna y con grados de madurez.**

**Perfil típico del calcrete en la Hoja Santa Rosa** (verificado, SEGEMAR, 2023). De abajo hacia arriba:

1. **Horizonte basal hospedador** — areno‑limoso, grisáceo rosado, con **carbonato pulverulento** (sin consolidar).
2. **Horizonte prismático transicional** — con **nódulos arenosos calcificados, elongados verticalmente, de hasta 20 cm de longitud y 1 a 5 cm de diámetro**; hacia arriba pasan a forma irregular.
3. **Lentes y láminas subhorizontales** de carbonato de calcio, de **1 a 10 cm de potencia**.
4. **Rizolitos** — tubitos de **1 a 2 cm de diámetro** revestidos de carbonato y **rellenos de arena fina a mediana**, dispuestos vertical u horizontalmente.
5. **Crotovinas** (paleomadrigueras) — *"de forma circular y **tamaño métrico**"*.
6. **Horizonte macizo de caliza impura (*hardpan*)** — corona el perfil y *"puede llegar a tener **1 m de espesor**"*. Textura bandeada, pisolítica y oolítica; pisolitas de 0,2 a 1 cm.

> **Tres consecuencias de fundación que salen directamente de ese perfil [PD]:**
> - **Los rizolitos y las láminas son planos de debilidad y vías de agua.** Una tosca "sana" al golpe puede tener conductos rellenos de arena fina que conducen agua directamente hacia abajo.
> - **Las crotovinas de tamaño métrico son cavidades.** Una oquedad de escala métrica bajo una zapata es una falla local sin aviso. **Es una razón adicional para preferir fundación rígida y repartida (platea) antes que zapatas puntuales.**
> - **El horizonte pulverulento de la base no es apoyo**: es carbonato sin consolidar. Apoyar sobre "tosca" sin identificar en qué horizonte del calcrete se está apoyando es un error frecuente.

**Grado de madurez — y por qué importa para Santa Rosa** (verificado, SEGEMAR): los calcretes **más desarrollados están en el sector occidental** de las hojas (estadio IV–V de Machette), *"mientras que hacia el este las exposiciones son menores y **en general carecen del horizonte cuspidal duro o hardpan y/o del horizonte laminar**"* (estadio II–III). Es decir: **hacia el este la tosca es más pobre y menos apta como estrato de apoyo.** Santa Rosa está en el sector centro‑oriental de su hoja, con el campo de dunas inmediatamente al este.

**Espesores medidos en el sudeste provincial** (verificado, Rev. Asoc. Geol. Argentina — **atención: no es Santa Rosa**, sirve como orden de magnitud del rasgo geológico):

| Nivel | Cota | Espesor |
|---|---|---|
| Calcrete I (el más antiguo) | 225 msnm | máximo **2 m**, mínimo **1,10 m** |
| Calcrete II | 130 msnm | máximo **1 m**, mínimo **0,70 m** |
| Calcrete III | 70 msnm | **0,5 m** promedio |

La misma fuente aclara que **"sus espesores no son constantes lateralmente"** y que los calcretes **"están parcialmente cubiertos por depósitos eólicos del Pleistoceno‑Holoceno"**; el SEGEMAR coincide: *"en general las exposiciones son parciales y lateralmente presentan variaciones"*. Exactamente la situación de un lote en Santa Rosa.

**Dato local adicional (verificado, SEGEMAR):** el relevamiento de canteras de tosca de la hoja registra **catorce indicios**, con frentes de explotación *"generalmente en los bordes de la planicie estructural"* y labores **"en las áreas urbanas y suburbanas de Santa Rosa y Toay"**. Es decir: **hay tosca explotable dentro y alrededor del ejido urbano** — confirmación cartográfica oficial de que el rasgo está presente a poca profundidad en la ciudad. El SEGEMAR aclara además que *"si bien los afloramientos de tosca son muy abundantes en toda la región, sólo algunos de ellos pueden ser considerados como yacimientos"*: **abundante no significa uniforme.**

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
| **Crotovinas y rizolitos** | Cavidades **de tamaño métrico** y conductos rellenos de arena dentro del calcrete (verificado, SEGEMAR) | Argumento a favor de **fundación rígida y repartida**; verificar en calicata |
| **Apoyo en horizonte pulverulento** | La base del calcrete es carbonato **sin consolidar**: no es apoyo | Exigir que el informe **identifique el horizonte** de apoyo, no sólo "tosca" |
| **Calcrete inmaduro** | Hacia el este del área faltan el *hardpan* y el horizonte laminar (verificado, SEGEMAR) | No suponer resistencia por el solo hecho de "encontrar tosca" |
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
| Manto eólico **suelto**, areno‑limoso, de 0,20 a 2 m (verificado, SEGEMAR) | Suelo **potencialmente colapsable** justo en la cota de fundación de una casa baja |
| Ese mismo manto es de **elevada permeabilidad, zona de recarga excepcional, y aloja el acuífero freático** (verificado, SEGEMAR) | **No hay barrera entre el agua de superficie y el suelo de fundación.** Todo lo que se riega o se derrama llega abajo |
| Tosca a profundidad variable, discontinua, con crotovinas métricas | Riesgo alto de **asentamiento diferencial por apoyo heterogéneo** y de cavidades locales |
| Hacia el este/nordeste, manto eólico de **3 a 30 m** sin tosca | Escenario distinto: **no hay estrato competente somero** |
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
| Cartografía geológica oficial con descripción litológica y de espesores (SEGEMAR, Hojas 3763‑I Santa Rosa y 3763‑III Darregueira, 2023) | Mapa de tensiones admisibles de la ciudad |
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

## 7. Soluciones de fundación para casa de una planta

> **[FIRMA] Todo este capítulo es material de anteproyecto y de discusión con el estructuralista.**
> El dimensionamiento definitivo, la armadura y la cota de fundación se calculan con los parámetros del informe geotécnico del lote y los firma el profesional matriculado. Los predimensionados que siguen están marcados **[PD]** y sirven para presupuestar y para dibujar el anteproyecto, no para construir.

### 7.1 Profundidad mínima de fundación

La cota de fundación de una casa baja en loess se decide por **tres criterios simultáneos**, y manda el más profundo:

| Criterio | Qué exige | Valor orientativo |
|---|---|---|
| **1. Salir del suelo vegetal y del relleno antrópico** | Apoyar en suelo natural inalterado | **[VERIFICAR con estudio de suelos]** — típicamente el relleno urbano llega a 0,30–0,80 m |
| **2. Salir de la "capa activa"** — zona afectada por variación estacional de humedad, desecación, raíces de césped y arbustos | Que el suelo de apoyo no cambie de humedad con las estaciones | **[PD] 0,80 – 1,00 m** bajo terreno natural. **[VERIFICAR con estudio de suelos]**: el geotécnico debe indicar el espesor real de la capa activa en el lote |
| **3. Alcanzar el estrato de apoyo recomendado** | Manto natural competente, manto mejorado, o techo de tosca sana | **[VERIFICAR con estudio de suelos]** |

**Criterio de oficina [PD]:** en Santa Rosa, para casa de una planta, **no fundar por encima de 0,80 m** de la cota de terreno natural, salvo que el informe geotécnico lo justifique expresamente por escrito. Y si se llega a tosca sana antes, **limpiar bien el asiento y apoyar sobre ella**, verificando que sea continua bajo todo el elemento.

> **Un dato que juega a favor en Santa Rosa.** Como el manto eólico tiene **0,20 a 2 m de espesor sobre el calcrete** en el sector de planicie estructural (verificado, SEGEMAR — §2.1), en muchos lotes **la cota de fundación de una casa baja cae en el contacto o muy cerca de él**. Cuando el estudio confirma que **la tosca es madura (con *hardpan*), continua bajo toda la impronta y sin crotovinas**, la solución más limpia es **remover íntegramente el manto eólico bajo la casa y apoyar la platea directamente sobre la tosca limpia**, con un hormigón de limpieza inmediato. Eso elimina el estrato colapsable de la ecuación en lugar de convivir con él. **[VERIFICAR con estudio de suelos]** — la palabra clave es *continua*: si no lo es, esta solución se convierte en el peor caso (apoyo mixto).

**Una advertencia sobre la tosca:** apoyar **la mitad de una zapata corrida sobre tosca y la otra mitad sobre limo** es la receta exacta del asentamiento diferencial. Si la tosca es errática bajo la casa, **la respuesta correcta no es "seguir la tosca": es no apoyarse en ella** y resolver con platea sobre manto compactado uniforme (§7.3).

### 7.2 Comparativa de las cuatro soluciones

#### A) Zapata corrida (cimiento corrido de hormigón simple/ciclópeo o armado)

| | |
|---|---|
| **Cuándo corresponde** | Suelo homogéneo, no colapsable o de colapsabilidad baja verificada, sin napa somera, con tosca continua o manto firme parejo. Casa de mampostería portante regular |
| **Ventajas** | La más económica en materiales; ejecución simple y conocida por cualquier contratista local; poco movimiento de suelo |
| **Riesgos en loess** | **Muy alta.** Ancho pequeño → tensión de contacto concentrada; **rigidez longitudinal casi nula** si no está armada; **cualquier humedecimiento local produce descenso local y la mampostería lo copia fisurando**. No tolera apoyo heterogéneo |
| **Predimensionado [PD]** | Ancho B ≥ 2× espesor del muro y **B ≥ 0,40 m**; altura del cimiento ≥ B/2; Df ≥ 0,80 m. Con **σ_adm saturada de 0,5 kg/cm²**, un muro que baja 4 t/m necesita **B ≈ 0,80 m** — y ahí ya conviene otra solución |
| **Costo relativo** | **1,0** (base de comparación) |
| **Veredicto en Santa Rosa** | **Sólo con estudio de suelos que descarte colapsabilidad, y siempre con encadenado inferior armado continuo.** Nunca "cimiento corrido de cascote" sin viga |

#### B) Viga de fundación con base ensanchada (zapata corrida armada + viga de encadenado)

| | |
|---|---|
| **Cuándo corresponde** | La evolución natural de la anterior. Suelo de capacidad media, colapsabilidad baja a moderada, casa de mampostería portante con planta razonablemente regular |
| **Ventajas** | **Rigidiza la fundación en su plano**: convierte muros y bases en un anillo que se asienta más como un todo; distribuye cargas concentradas; es la medida estructural que recomienda la bibliografía para convivir con el colapso (*"encadenado de las fundaciones y muros"*, ver `estructuras.md` §3.5.6); costo moderado |
| **Riesgos en loess** | Rigidiza, pero **no reduce la presión de contacto** ni impide el colapso: si se moja un sector, el anillo se deforma igual, sólo que fisura menos y más repartido. **No sirve si el suelo es autocolapsable** |
| **Predimensionado [PD]** | Base ensanchada 0,50–0,80 m de ancho; viga de 0,20 × 0,40 m sobre la base, armada arriba y abajo (típicamente 4 Ø12 + estribos Ø6 c/20, **a verificar por cálculo**); **continuidad en todo el perímetro y en los muros interiores portantes, sin interrupciones**; empalmes en las esquinas resueltos con barras dobladas, no yuxtapuestas |
| **Costo relativo** | **1,3 – 1,6** |
| **Veredicto en Santa Rosa** | **Mínimo aceptable** para una casa de una planta con suelo verificado bueno. Por debajo de esto no se baja |

#### C) Platea de hormigón armado

| | |
|---|---|
| **Cuándo corresponde** | **Loess potencialmente colapsable; suelo heterogéneo; tosca discontinua; napa somera; lote con relleno; planta irregular.** Es decir: el escenario típico de Santa Rosa |
| **Ventajas** | **1)** Baja drásticamente la presión de contacto (reparte sobre toda la superficie). **2)** Es **una sola pieza rígida**: ante un humedecimiento local, la casa se inclina levemente en lugar de partirse — el mecanismo de daño pasa de "fisura" a "desnivel". **3)** Resuelve simultáneamente contrapiso, capa aisladora y base del piso. **4)** Tolera napa somera (con barrera de vapor). **5)** Es la solución que la bibliografía recomienda explícitamente combinada con sustitución de suelo (`estructuras.md` §3.5.6). **6)** Menos excavación → menos exposición del suelo a la intemperie durante la obra |
| **Riesgos en loess** | Si el colapso es **generalizado y grande**, la platea **acompaña** el descenso: no lo impide, lo uniformiza. **No sirve sobre suelo autocolapsable.** Requiere **buen control de ejecución** (nivelación, densidad del manto, recubrimientos, curado): una platea mal hecha es peor que una zapata bien hecha. Encarece si el proyecto tiene desniveles internos |
| **Predimensionado [PD]** | Losa de **0,15 – 0,20 m** de espesor, malla superior e inferior (p. ej. Ø8 c/15 en ambas direcciones y ambas caras, **a verificar por cálculo**); **vigas de borde perimetrales invertidas o hacia abajo de 0,25 × 0,40–0,50 m**, más nervios de rigidización bajo los muros portantes interiores; sobre **manto de suelo seleccionado compactado** de 0,30–0,60 m (mín. 95 % Proctor, **[VERIFICAR: espesor y densidad los fija el geotécnico]**); film de polietileno 200 μm como barrera de vapor; hormigón según clase de exposición del informe químico |
| **Costo relativo** | **1,6 – 2,2** (pero **absorbe el costo del contrapiso y de la carpeta**, así que el sobrecosto neto real es menor de lo que parece: **[PD] ~1,3 – 1,6** una vez descontado eso) |
| **Veredicto en Santa Rosa** | **La opción por defecto.** Ver §7.3 |

#### D) Pozos / pilotines hasta tosca (fundación indirecta)

| | |
|---|---|
| **Cuándo corresponde** | Manto superficial malo o de espesor conocido y acotado, con **tosca sana, continua y verificada** a profundidad alcanzable (típicamente 1,5–3,5 m); o lote con relleno profundo; o recalce de una casa existente |
| **Ventajas** | Transfiere la carga por debajo de la capa activa y del manto colapsable; poco movimiento de suelo; ejecutable con equipo liviano; el **pilotín helicoidal** es una alternativa industrializada apta para cargas bajas de vivienda |
| **Riesgos en loess** | **Los más contraintuitivos, y están documentados.** Cita verificada (`estructuras.md` §3.5.6): *"existen numerosos casos donde este tipo de solución **no ha sido satisfactoria** [...] aún estructuras fundadas sobre pilotes han sufrido daños de importancia al colapsar el suelo que las rodea"*, por **pérdida de fricción lateral** y **fricción negativa**. Además: la casa queda quieta mientras **el terreno de alrededor baja** → se rompen veredas, contrapisos, cañerías y escalones de acceso; y **la tosca discontinua da longitudes de pilote dispares** |
| **Predimensionado [PD]** | Pozos Ø0,30–0,40 m u hormigonados in situ, separados 1,50–2,50 m bajo vigas de fundación armadas continuas; empotramiento en tosca sana **≥ 0,30–0,50 m** verificado en obra pozo por pozo. **No computar fricción lateral en el manto colapsable**; diseñar **por punta** y **sumar la fricción negativa** como carga descendente **[FIRMA]** |
| **Costo relativo** | **1,8 – 3,0** (muy sensible a la dureza de la tosca y a la profundidad) |
| **Veredicto en Santa Rosa** | **Buena solución cuando la tosca está verificada y continua.** Mala idea "por las dudas": si el manto es colapsable y no se controla el agua, los pilotines **no salvan la casa, sólo cambian el modo de falla** |

#### Cuadro resumen

| | Zapata corrida | Viga con base ensanchada | **Platea** | Pozos/pilotines a tosca |
|---|---|---|---|---|
| Reduce presión de contacto | No | Poco | **Sí, mucho** | Concentra en la punta |
| Rigidiza el conjunto | No | Sí | **Sí, mucho** | Sí (con vigas) |
| Tolera suelo heterogéneo | No | Poco | **Sí** | Sólo si la tosca es continua |
| Tolera napa somera | Regular | Regular | **Sí** | Difícil de ejecutar |
| Sensible a mala ejecución | Media | Media | **Alta** | Alta |
| Vulnerable a fricción negativa | — | — | — | **Sí** |
| Resuelve el colapso por sí sola | **No** | **No** | **No** | **No** |
| Costo relativo | 1,0 | 1,3–1,6 | 1,6–2,2 | 1,8–3,0 |

> **La fila que importa es la anteúltima: ninguna resuelve el colapso por sí sola.** El colapso se evita con el capítulo 8.

### 7.3 Recomendación por defecto en Santa Rosa

> ## **Platea de hormigón armado, con vigas perimetrales y nervios de rigidización bajo muros portantes, apoyada sobre manto de suelo seleccionado compactado, con la cota de fundación por debajo de la capa activa.**

**Por qué es la opción por defecto para una casa de una planta en Santa Rosa [PD, fundado]:**

1. **Es la respuesta correcta al problema real, que es la heterogeneidad.** El riesgo dominante acá no es que el suelo no aguante: es que **aguante distinto en cada punto** (tosca errática, relleno urbano, humedecimiento local). La platea **promedia** esa heterogeneidad.
2. **Convierte fisura en desnivel.** Con una casa liviana de mampostería, la diferencia entre una fundación rígida y una flexible es la diferencia entre una casa que se inclina 1 cm y una casa rajada de punta a punta. La bibliografía es explícita: *"la cimentación en losa, sobre todo si tiene rigidez y resistencia holgadas, puede amortiguar mucho los efectos de un fallo local del terreno, evitando el efecto de asiento diferencial"* (verificado, De Miguel).
3. **Es literalmente la receta publicada para este suelo.** Rocca–Redolfi–Terzariol, sobre edificaciones arquitectónicas en loess colapsable (texto verificado, ver `estructuras.md` §3.5.6): *"suele dar mejor resultado la adopción de medidas de diseño que minimicen el riesgo de ingreso de agua al terreno, **o mejoras en el terreno mediante sustitución de suelo combinados con plateas** que disminuyan significativamente las presiones en el suelo."*
4. **Baja la presión de contacto por debajo de la presión de fluencia saturada.** Ése es el objetivo mecánico concreto: mantener `σ_actuante < σ_F.SAT` incluso con el suelo mojado. Con una casa liviana repartida en toda la planta, es alcanzable.
5. **Tolera el escenario de napa en ascenso**, que es el escenario probable de los próximos 30 años (§3.1).
6. **Su sobrecosto neto es modesto**, porque reemplaza contrapiso y carpeta.

**Cuándo NO es la opción por defecto:**

| Situación | Alternativa |
|---|---|
| **Tosca sana, continua y somera verificada bajo toda la casa** (p. ej. a 0,60–1,00 m en todos los puntos) | **Viga de fundación con base ensanchada apoyada en tosca**, más barata y perfectamente adecuada |
| **Suelo autocolapsable** identificado por el informe | **Ninguna fundación directa sirve.** Tratamiento de suelo o fundación profunda con diseño por punta y fricción negativa **[FIRMA]** |
| **Relleno profundo (> 1,5 m) o material heterogéneo no removible** | Pilotines a tosca, o sustitución total del relleno |
| Casa con desniveles internos importantes o terreno con mucha pendiente | Platea escalonada o combinación; evaluar caso por caso |
| Napa prácticamente aflorante | Platea **con** verificación de subpresión y barrera hidráulica **[FIRMA]** |

### 7.4 Predimensionado orientativo de la platea **[PD]**

Para una casa de una planta, mampostería portante, cubierta liviana o losa cerámica, sin sobrecargas especiales:

| Ítem | Valor orientativo **[PD]** | Se define finalmente por |
|---|---|---|
| Espesor de losa | **0,15 – 0,20 m** | Cálculo con módulo de balasto del informe **[FIRMA]** |
| Armadura | Mallas en ambas caras y direcciones; refuerzos bajo muros | Cálculo **[FIRMA]** |
| Viga perimetral | **0,25 – 0,30 m de ancho × 0,40 – 0,50 m de altura** | Cálculo + cota de fundación |
| Nervios interiores bajo muros portantes | 0,20 × 0,30–0,40 m | Cálculo |
| Cota de fondo de viga perimetral | **≥ 0,80 m bajo terreno natural** | Informe geotécnico |
| Manto de suelo seleccionado compactado bajo platea | **0,30 – 0,60 m**, en capas de ≤ 0,20 m, **≥ 95 % Proctor estándar** | **[VERIFICAR con estudio de suelos]** |
| Film de polietileno | **200 μm**, continuo, solapes ≥ 0,20 m sellados, subiendo por los bordes | — |
| Hormigón | Según **clase de exposición** del análisis químico (CIRSOC 201) | Informe químico |
| Tensión de contacto resultante estimada | **0,25 – 0,50 kg/cm²** para casa liviana sobre platea de toda la planta | Verificar contra σ_adm **saturada** |

> **El chequeo que hay que hacer siempre:** tensión de contacto de la platea **contra la tensión admisible en condición SATURADA**, no contra la de humedad natural. Si no verifica, la respuesta es aumentar la superficie de apoyo o mejorar el suelo — **no** adoptar el valor a humedad natural "porque va a estar seco".

### 7.5 Detalles constructivos que deciden el resultado

| Detalle | Por qué | Qué hacer |
|---|---|---|
| **El fondo de excavación no puede quedar abierto y expuesto** | Una lluvia sobre el fondo de excavación **satura el suelo de apoyo antes de hormigonar** — el colapso empieza antes de que exista la casa | Hormigón de limpieza el mismo día; si no se puede, cubrir con film y prever desagote. **Nunca dejar la excavación abierta un fin de semana con pronóstico de lluvia** |
| **Compactación del fondo** | El "escarificado y compactado" que nadie controla | Exigir densidad medida, no "a ojo" |
| **Continuidad de encadenados** | Un encadenado interrumpido en una abertura no rigidiza | Continuidad total; refuerzos sobre y bajo aberturas |
| **Juntas de trabajo en la platea** | Una junta mal resuelta es la primera fisura | Planificar el hormigonado en una sola etapa si es posible |
| **Curado** | La platea es una superficie enorme expuesta al sol y al viento pampeano | Curado obligatorio ≥ 7 días; hormigonar temprano en verano |
| **Capa aisladora** | Con napa somera y ascenso capilar | Horizontal **y vertical**, sin discontinuidades |
| **Cañerías que atraviesan la platea** | Cada pasaje es un punto de entrada de agua y una rotura futura | Pasantes con vaina, sellados; **evitar empalmes bajo la platea** |
| **Nivelación del terreno terminado** | El detalle más barato y el más olvidado | Ver §8 completo |

---

## 8. Mitigación no estructural — el capítulo que salva la casa

### 8.1 El principio

> **En loess colapsable, el manejo del agua es un asunto estructural.**
> Una fundación correctamente calculada, ejecutada sobre un manejo del agua incorrecto, **falla igual**. Una fundación modesta con un manejo del agua impecable, **no falla**.
> Esto no es una recomendación de mantenimiento: es **parte del proyecto estructural**, y se dibuja, se especifica y se presupuesta.

Las tres reglas, en orden de importancia:

1. **Que el agua no entre.** Alejar toda descarga y toda infiltración del perímetro.
2. **Que si entra, se vea.** Instalaciones inspeccionables: una pérdida oculta durante dos años es lo que rompe la casa.
3. **Que si entra y se ve, no importe.** Fundación rígida y suelo mejorado que toleren un evento local.

### 8.2 Vereda perimetral

Es la medida más barata y más eficaz del documento.

| Parámetro | Especificación **[PD, criterio de oficina; el ancho mínimo de 1,20 m surge de `estructuras.md` §3.5.6]** |
|---|---|
| **Ancho** | **Mínimo 1,20 m. Recomendado 1,50 m.** Debe cubrir toda la zona donde el agua de escurrimiento podría infiltrar junto a la fundación |
| **Pendiente** | **≥ 2 % alejándose de la casa** (2 cm por metro). En loess conviene **3 %** si el sector recibe descarga de cubierta |
| **Continuidad** | **Perimetral completa, sin interrupciones.** El sector "que no se ve" del contrafrente es donde falla |
| **Junta contra el muro** | **Junta elástica sellada** (sellador poliuretánico o similar), no mortero rígido. Reponer el sellado es mantenimiento previsto |
| **Juntas de contracción** | Cada 2,00–3,00 m, selladas. Una vereda fisurada sin sellar **es un embudo dirigido a la fundación** |
| **Terminación** | Superficie impermeable (hormigón, baldosón sobre contrapiso con carpeta). **No** solado permeable, **no** piedra suelta, **no** deck sobre tierra pegado al muro |
| **Cordón / babeta exterior** | Cordón bajo en el borde exterior sólo si conduce a un desagüe; si no, obstaculiza y embalsa |
| **Nivel** | Vereda **por debajo** del nivel de piso terminado interior (≥ 0,15 m) y **por encima** del terreno natural circundante |

> **Error clásico local:** vereda de 0,60 m con pendiente hacia la casa (porque el terreno bajaba hacia allá), fisurada y sin sellar. Es un **canal de recarga localizada** sobre la fundación. En loess, ese detalle solo puede producir la patología.

### 8.3 Pluviales

| Medida | Especificación |
|---|---|
| **Prohibición absoluta** | **Ninguna bajada pluvial descarga junto a la fundación.** Ni "a la vereda perimetral", ni "sobre una piedra", ni a un caño corto que termina a 50 cm del muro |
| **Descarga mínima alejada del perímetro** | **≥ 3,00 m** del perímetro de la construcción (criterio de `estructuras.md` §3.5.6 — verificado como recomendación de la bibliografía de loess). Preferible: conducir a cordón cuneta / red pluvial |
| **Conducción** | Cañería enterrada **estanca**, con pendiente ≥ 1 %, **con cámaras de inspección**, hasta la vía pública o hasta un punto de descarga controlado y alejado |
| **Nunca** | Bajada pluvial a **pozo absorbente**, ni compartida con cloacal, ni descargando en el jardín contra la casa |
| **Canaletas** | Con pendiente y limpieza accesible. Una canaleta tapada **rebalsa exactamente sobre el perímetro** |
| **Techos sin canaleta** | Si el partido arquitectónico no lleva canaletas (cubierta con goterón libre), **es obligatorio** proyectar una **canaleta de piso** con pendiente y desagüe conducido bajo la línea de goteo, o ensanchar la vereda perimetral más allá del goterón |
| **Nivelación general del lote** | Pendiente que **aleje el agua superficial de la construcción** en todas las direcciones. Si el lote recibe escurrimiento del vecino, resolverlo con cuneta perimetral conducida **antes** de empezar la obra |

### 8.4 Instalaciones enterradas

**El principio: toda pérdida oculta es un colapso en formación.**

| Medida | Especificación |
|---|---|
| **Cañerías enterradas dentro del predio** | Toda cañería de agua o cloaca enterrada **dentro de vaina, con pendiente y cámara de inspección testigo**, de modo que una pérdida **se vea y se drene**, no se infiltre (criterio verificado, `estructuras.md` §3.5.6) |
| **Empalmes** | **Ninguno bajo la platea ni bajo muros portantes.** Los empalmes van en cámaras accesibles |
| **Cámaras** | **Estancas**, con tapa hermética, base y paredes impermeabilizadas. Una cámara de inspección que filtra es un pozo absorbente clandestino junto a la fundación |
| **Cañería de agua fría de entrada** | Recorrido conocido y registrable; llave de paso general accesible |
| **Prueba hidráulica** | Prueba de estanqueidad **antes** de tapar. Documentarla con fotos |
| **Tendido paralelo al muro** | Evitar cañerías enterradas **paralelas y adyacentes** a la fundación. Si es inevitable, separar ≥ 1,00 m **[PD]** y envainar |
| **Riego automático enterrado** | Si lo hay: **no** contra la casa, con llave de corte sectorizada y **caudalímetro o control de consumo** para detectar una pérdida |

### 8.5 Pozo absorbente y cámara séptica

Este es el punto donde la reglamentación disponible **no alcanza** y hay que aplicar criterio.

**Lo que sí está normado (verificado, ordenanzas municipales argentinas de referencia — Bahía Blanca, Colonia Caroya):** el pozo distará **no menos de 1,50 m de la línea divisoria entre predios y de la línea municipal**, **no menos de 2,00 m de cualquier otro pozo absorbente**, y **no menos de 10 m de cualquier pozo o perforación de captación de agua** propio o del predio vecino.

> **[VER] Verificar el Código de Edificación y el reglamento de instalaciones sanitarias vigentes de la Municipalidad de Santa Rosa y de la Administración Provincial del Agua antes de proyectar.** Las distancias citadas arriba son de otras jurisdicciones y se dan como orden de magnitud.

**Lo que la reglamentación NO fija y hay que resolver por criterio geotécnico [PD]:**

| Cuestión | Criterio de oficina |
|---|---|
| **Distancia mínima del pozo absorbente a la fundación** | **Lo más lejos posible dentro del lote, y nunca menos de 5,00 m** de cualquier elemento de fundación. Si el lote no permite 5 m, **el pozo absorbente no es una solución aceptable en este suelo** y hay que ir a red cloacal o a un sistema estanco con retiro. Referencia de la bibliografía de loess: *"Un pozo ciego a 3 m de una base en loess es una bomba de tiempo"* (verificado, `estructuras.md` §3.5.6) |
| **Posición relativa** | **Aguas abajo** de la casa según la pendiente del terreno, nunca aguas arriba |
| **Napa** | **Verificar cota de napa antes de proyectarlo.** Con napa somera el pozo no absorbe: se llena, rebalsa y satura el entorno. Y contamina el acuífero (§3.4) |
| **Cámara séptica** | **Estanca, verificada con prueba hidráulica.** Una séptica que filtra es peor que un pozo absorbente, porque nadie la sospecha |
| **Alternativa preferible** | **Conexión a red cloacal** siempre que exista. Es el mejor dinero que se gasta en una casa en loess |
| **Doble pozo** | Si se ejecutan dos pozos alternados, **ambos** cumplen la distancia mínima a la fundación |

### 8.6 Jardín, riego y árboles

> **Es la causa n.º 1 de colapso localizado en vivienda** (criterio verificado en la bibliografía de loess, `estructuras.md` §3.5.6). Y es una decisión que se toma en el proyecto de paisajismo, cuando la estructura ya está calculada y nadie la vuelve a mirar.

| Elemento | Regla | Distancia mínima al perímetro de la casa |
|---|---|---|
| **Cantero regado / césped regado** | **Prohibido contra el muro.** Entre la casa y cualquier superficie regada va la **vereda perimetral impermeable** | **≥ 1,20 m (ancho de la vereda); recomendado 1,50 m** |
| **Riego por aspersión** | Ningún aspersor debe mojar la franja perimetral ni el muro | **[PD] ≥ 2,00 m**, y orientado hacia afuera |
| **Riego por goteo** | Aceptable más allá de la vereda; nunca sobre ella ni bajo ella | **[PD] ≥ 1,50 m** |
| **Cantero elevado contra el muro** | Prohibido. Es un depósito de agua permanente contra la fundación | — |
| **Arbustos y árboles pequeños (< 5 m)** | Alejados del perímetro | **[PD] ≥ 2,00 m** (referencia general de bibliografía europea, no local) |
| **Árboles medianos (5 – 10 m)** | Alejados del perímetro | **[PD] 3,00 – 5,00 m** |
| **Árboles grandes o de raíz agresiva** (eucaliptos, pinos, álamos, sauces, ficus, paraísos, moras) | **No plantar cerca de la casa.** En La Pampa el eucalipto y el álamo son de uso corriente en cortinas: mantenerlos fuera del entorno inmediato | **[PD] 5,00 – 10,00 m como mínimo**, idealmente ≥ 1 vez la altura adulta |
| **Árbol existente muy próximo** | **No talarlo sin consultar.** La eliminación de un árbol grande cambia bruscamente el régimen de humedad del suelo, y el efecto puede ser tan dañino como su presencia | Consultar a estructuralista **[FIRMA]** |
| **Pozo de árbol en vereda perimetral** | Prohibido. Es un embudo | — |

> **Dos mecanismos distintos, no confundirlos:**
> - **Riego contra el muro → humedece el loess → colapso → la casa BAJA en ese sector.** Éste es el mecanismo dominante en Santa Rosa.
> - **Raíces → desecan el suelo → retracción; y la tala posterior → rehumedecimiento → hinchamiento.** Este mecanismo es propio de suelos arcillosos expansivos, mucho menos relevante en el loess pampeano de baja plasticidad, **pero las raíces sí levantan veredas y rompen cañerías**, y una cañería rota **sí** dispara el colapso.

**Qué sí se puede hacer en el jardín:** todo, más allá de la franja perimetral protegida. Especies de bajo requerimiento hídrico (el clima es semiárido: 686–753 mm/año), gramíneas nativas, cubresuelos xerófitos, riego eficiente y sectorizado. **La consigna para el cliente: el jardín empieza a 1,50 m de la casa.**

### 8.7 Pileta de natación

Una pileta es **un depósito de decenas de m³ de agua enterrado junto a la casa**. En loess colapsable es el mayor riesgo puntual que se puede introducir en un lote.

| Medida | Especificación |
|---|---|
| **Distancia a la fundación de la casa** | **[PD] ≥ 5,00 m** entre el paramento exterior del vaso y cualquier elemento de fundación. Si el lote no lo permite: **[FIRMA]** el estructuralista debe verificar expresamente la interacción, y probablemente haga falta fundación profunda o tratamiento del suelo |
| **Cota relativa** | La pileta, **aguas abajo** de la casa. Nunca en el sector alto del lote descargando hacia la construcción |
| **Estanqueidad del vaso** | **Impermeabilización verificada con prueba de estanqueidad documentada** antes de terminar el entorno |
| **Detección de pérdida** | **Cañería de recirculación registrable** (no embutida en el terreno sin acceso) y **control de nivel**: una pérdida lenta de pileta puede pasar meses inadvertida disfrazada de "evaporación" |
| **Vaciado y retrolavado del filtro** | **Conducidos a desagüe alejado**, nunca al terreno junto a la casa ni al pozo absorbente. Un retrolavado semanal descargando al jardín es un ensayo de hidrocompactación |
| **Vereda perimetral de la pileta** | Igual criterio que la de la casa: ancho, pendiente hacia afuera, juntas selladas |
| **Excavación** | La excavación de la pileta **descomprime y expone el suelo** junto a la casa. Coordinar con el estructuralista si es posterior a la construcción **[FIRMA]** |
| **Subpresión** | Con napa somera, verificar **flotación del vaso vacío**. Ver `estructuras.md` §3.6.2 |

> **Si el cliente quiere pileta, hay que saberlo en el anteproyecto**, no cuando la casa está terminada. Cambia la implantación y puede cambiar el tipo de fundación.

### 8.8 Tabla maestra de distancias

Resumen operativo. Los valores **[PD]** son criterio de oficina; los **(verificado)** provienen de las fuentes citadas.

| Elemento | Distancia mínima al perímetro de fundación | Origen |
|---|---|---|
| Vereda perimetral impermeable (**ancho**) | **1,20 m mínimo / 1,50 m recomendado**, pendiente ≥ 2 % hacia afuera | (verificado, bibliografía de loess) |
| Descarga de pluviales | **≥ 3,00 m** | (verificado, bibliografía de loess) |
| Cantero, césped o superficie regada | **≥ 1,20 m** (borde exterior de la vereda) | [PD] |
| Aspersor de riego | **≥ 2,00 m** | [PD] |
| Arbusto / árbol pequeño | **≥ 2,00 m** | [PD, referencia no local] |
| Árbol mediano (5–10 m) | **3,00 – 5,00 m** | [PD, referencia no local] |
| Árbol grande / raíz agresiva | **5,00 – 10,00 m** | [PD, referencia no local] |
| **Pozo absorbente** | **≥ 5,00 m** (y si no entra, cambiar de sistema) | [PD] |
| Pozo absorbente a línea divisoria / línea municipal | ≥ 1,50 m | (verificado, otras jurisdicciones) **[VER Santa Rosa]** |
| Pozo absorbente a otro pozo absorbente | ≥ 2,00 m | (verificado, otras jurisdicciones) **[VER Santa Rosa]** |
| Pozo absorbente a captación de agua | ≥ 10,00 m | (verificado, otras jurisdicciones) **[VER Santa Rosa]** |
| **Pileta de natación** | **≥ 5,00 m** | [PD] |
| Cañería enterrada paralela al muro | ≥ 1,00 m, envainada | [PD] |

### 8.9 Manual del usuario para el comitente

**Entregar por escrito con la documentación final de obra.** Una página, en lenguaje llano:

> **Su casa está construida sobre suelo loéssico. Es un suelo firme mientras está seco, y pierde resistencia cuando se moja de forma prolongada. Estas seis cosas mantienen su casa sana:**
>
> 1. **No plante ni riegue contra las paredes.** La vereda perimetral está para eso. El jardín empieza más allá.
> 2. **No modifique el nivel del terreno junto a la casa.** Si trae tierra para el jardín, que nunca quede más alta que la vereda ni tape la capa aisladora.
> 3. **Mantenga selladas las juntas de la vereda perimetral.** Reviselas una vez por año y reponga el sellador. Es media hora de trabajo y es lo más importante de esta lista.
> 4. **Si se rompe un caño, arréglelo enseguida.** Una pérdida enterrada durante meses es lo único que puede dañar seriamente la estructura. Señales: consumo de agua alto sin motivo, mancha húmeda que no seca, hundimiento localizado del piso o de la vereda.
> 5. **Limpie las canaletas y no cambie las descargas pluviales.** Nada de bajadas que descarguen al pie de la pared.
> 6. **Si aparece una fisura nueva que crece, avísenos y no la tape.** Fotografíela con una regla al lado y con fecha. Una fisura tapada sin diagnóstico vuelve a aparecer.
>
> **Si va a hacer una pileta, un quincho, una ampliación o plantar árboles: consúltenos antes.**

---

## 9. Patologías locales — leer las fisuras

### 9.1 Cómo se ve un asentamiento diferencial en una casa de una planta

**Patrón característico** (verificado, De Miguel, *Fisuras y grietas*): fisuras **inclinadas** en los paños alrededor del punto que asienta, **apuntando hacia él**. En una casa de planta baja hay que buscar además:

| Síntoma | Descripción |
|---|---|
| **Fisura diagonal desde el ángulo de una abertura** | Arranca en el vértice superior o inferior de una ventana o puerta y sube/baja a ~45°. Es el sitio más débil del paño |
| **Fisura vertical en el encuentro de dos muros** (esquina) | Típica del sector perimetral que baja: la esquina se "despega" |
| **Fisura que atraviesa el dintel y sigue en el antepecho** | Indica movimiento del apoyo, no del dintel |
| **Aberturas que dejan de cerrar / marcos desescuadrados** | Es la confirmación de que hay distorsión, no sólo fisura superficial |
| **Piso interior desnivelado**, zócalos que se separan | Buscarlo con nivel de manguera o láser. Es el dato más objetivo |
| **Rotura de solados y de la vereda perimetral en el mismo sector** | Confirma que el movimiento es del terreno |
| **Fisuras que se abren más arriba que abajo, o al revés** | Indica el sentido del giro y ayuda a ubicar el punto que cede |
| **La fisura se ve por dentro y por fuera, en el mismo lugar** | Atraviesa el muro: es estructural, no de revoque |

**Ubicación esperable en Santa Rosa [PD]:** **perimetral y de esquina**, del lado donde está el cantero regado, la bajada pluvial, el pozo absorbente o la pileta (§4.4). Antes de peritar la casa, **caminar el perímetro y mirar el agua**.

### 9.2 Asentamiento vs. retracción vs. otras causas

| | **Asentamiento diferencial** | **Retracción (hormigón / revoque / mortero)** | **Expansión / hinchamiento** | **Dilatación térmica** |
|---|---|---|---|---|
| **Trazado** | **Inclinado, apuntando al punto que baja**; diagonal desde ángulos de aberturas | **Mapeada** (piel de cocodrilo) en revoques; **a mitad de la luz** en dinteles; siguiendo la geometría del elemento | Inclinado **de trazado contrario** al de asentamiento (verificado, De Miguel) | Vertical u horizontal, cerca de encuentros de materiales distintos |
| **Profundidad** | **Atraviesa el muro**: se ve por dentro y por fuera en el mismo punto | Superficial, sólo en el revoque o sólo en el elemento afectado | Atraviesa | Suele ser superficial |
| **Involucra otros elementos** | Sí: pisos, zócalos, veredas, aberturas | **No**: *"las fisuras de retracción [...] no involucran necesariamente a los demás elementos constructivos"* (verificado) | Sí | Poco |
| **Evolución** | **Progresiva** mientras dura la causa; se estabiliza cuando ésta cesa | Aparece temprano (semanas/meses) y **se detiene** | Progresiva y estacional | **Cíclica**: abre y cierra con las estaciones |
| **Relación con el agua** | Aparece o empeora **después de lluvias intensas, de una pérdida o del riego** | Aparece en **secado** rápido: verano, viento, curado deficiente | Aparece con **humedecimiento** | Con cambios de temperatura |
| **Ancho típico** | Crece con el tiempo; puede superar 1–2 mm y llegar a grieta | Fina, generalmente < 0,3 mm y estable | Variable | Fina y estable |
| **Qué hacer** | **Diagnóstico geotécnico. No sellar y olvidar** | Reparación de terminación | Diagnóstico | Junta de dilatación |

> **La prueba decisiva en una casa de una planta.** En un edificio, De Miguel usa el criterio de que la fisura por asiento se repite **en la misma vertical en todas las plantas** (verificado). En una casa de PB **no hay ese chequeo**. Los sustitutos son:
> 1. **¿Se ve por dentro y por fuera en el mismo lugar?** Si sí → estructural.
> 2. **¿Hay desnivel de piso medible?** Si sí → asentamiento.
> 3. **¿La vereda perimetral y el solado exterior también están rotos ahí?** Si sí → es el terreno.
> 4. **¿Hay una fuente de agua en ese sector?** Si sí → ya tenés el diagnóstico.

### 9.3 Qué hacer cuando aparecen

**Protocolo, en orden:**

1. **No tapar.** Un revoque nuevo sobre una fisura viva sólo borra la evidencia y retrasa el diagnóstico.
2. **Documentar.** Fotografías con **regla y fecha** en cada fisura, croquis de planta y alzados con la ubicación de todas ellas, y **relevamiento de niveles de piso** (manguera o láser) en una grilla.
3. **Instalar testigos.** Testigos de yeso, o mejor **fisurómetros** (testigos graduados) numerados, con lectura y fecha. **Leer al menos cada 15 días durante 3 meses.** Es la única forma de saber si el movimiento está activo.
4. **Buscar la fuente de agua** en el sector afectado: cantero, bajada pluvial, pozo absorbente, pileta, cañería. Verificar consumo de agua con todas las canillas cerradas.
5. **Cortar la fuente inmediatamente** si se identifica. En muchos casos el movimiento se detiene solo cuando el suelo deja de recibir agua.
6. **Convocar al estructuralista.** **[FIRMA]** Con los testigos leídos, el relevamiento de niveles y el informe geotécnico original en la mano.
7. **Decidir con datos.** Si el movimiento **se detuvo** y no hay pérdida de nivel importante: reparar (sellar, restituir revoques, reponer maniobrabilidad de aberturas). Si **sigue activo**: recalce. Dato verificado (De Miguel): *"Si el fenómeno se estabiliza, y no ha habido alteraciones geométricas importantes, bastará restañar las fisuras [...] Si el fenómeno prosigue incesantemente, es, en general, imparable"* — pero también: *"la propia dinámica de los acontecimientos hace que, en general, la situación acabe encajando en otro punto, encontrando de nuevo el equilibrio, aunque los daños hayan podido ser severos."*

**Sobre el recalce.** El asentamiento *"es en general, no subsanable, aunque sí se puede detener su progreso, mediante intervenciones de recalce"* (verificado, De Miguel). En vivienda baja sobre loess, la alternativa más difundida son los **pilotines** (incluidos los helicoidales), que se adaptan a las bajas cargas de obras de pequeña escala **[VER — verificar profundidad del estrato competente en cada caso; no adoptar profundidades "típicas"]**. Pero:

> **[FIRMA] Recalzar sin haber cortado la fuente de agua es tirar el dinero.** Primero se elimina la causa, se verifica con testigos que el movimiento se detuvo, y recién entonces se decide si hace falta recalce. El orden inverso es el error más caro que se comete con estas patologías.

---

## 10. Checklist de suelo y fundación del proyecto

### A. Antes de comprar / de aceptar el encargo

- [ ] Ubicación del lote **dentro de la cuenca centrípeta** de Santa Rosa (sector alto E/N, casco, sector bajo SO). §2.4
- [ ] Relevamiento planialtimétrico del lote y de los linderos. ¿El lote recibe escorrentía de arriba?
- [ ] ¿Hay **relleno**? Preguntar historia del lote (¿era un bajo? ¿hubo excavación previa? ¿hubo demolición?)
- [ ] Recorrer la manzana: **fisuras en construcciones vecinas**, veredas rotas, hundimientos de pavimento, bombas de achique
- [ ] Consulta a la **APA** por profundidad de napa registrada en el sector
- [ ] ¿Hay **red cloacal** en la cuadra? (cambia todo el capítulo 8.5)
- [ ] ¿Hay **árboles grandes** existentes y dónde?

### B. Estudio de suelos

- [ ] Contratado **antes** del proyecto ejecutivo, con el anteproyecto en la mano del geotécnico. §6.4
- [ ] **Mínimo 2 prospecciones (Clase C‑1) — recomendado 3 (Clase C‑2)**, CIRSOC 401 Tabla 3.1. §6.2
- [ ] **Profundidad mínima 6,00 m**, art. 3.5.6.2. §6.2
- [ ] **Calicatas con muestreo en damas de ≥ 0,25 m de lado**, art. 3.6.7. §5.3
- [ ] **Doble ensayo edométrico** y **potencial de colapso** solicitados explícitamente. §6.4
- [ ] **σ_adm pedida a humedad natural Y saturada**. §5.2
- [ ] **Cota y espesor de tosca en cada punto** + opinión sobre continuidad. §2.3
- [ ] **Napa medida, estabilizada a 24 h, con fecha** + opinión sobre tendencia. §3.5
- [ ] **Análisis químico** (sulfatos, cloruros, sales, pH, MO) + clase de exposición CIRSOC 201. §5.4
- [ ] Informe **firmado por matriculado con incumbencia en geotecnia**. **[FIRMA]**
- [ ] Las **10 preguntas** hechas y respondidas por escrito. §6.6

### C. Proyecto de fundación

- [ ] Tipo de fundación **decidido con el informe en la mano**, no antes. §7.2
- [ ] Verificación de la tensión de contacto **contra σ_adm SATURADA**. §7.4 **[FIRMA]**
- [ ] Cota de fundación **por debajo de la capa activa** (orientativo ≥ 0,80 m). §7.1
- [ ] **Ningún elemento con apoyo mixto tosca / suelo suelto**. §7.1
- [ ] **Encadenado / rigidización continua** en todo el perímetro y bajo muros portantes. §7.2
- [ ] Espesor y densidad del **manto de suelo compactado** especificados por el geotécnico. §7.4
- [ ] Clase de exposición y tipo de cemento del hormigón según análisis químico. §5.4
- [ ] Plano de fundaciones con **cota de fondo, tensión admisible adoptada, cota del estrato resistente y hormigón de limpieza**. **[FIRMA]**
- [ ] **Sin subsuelo** — o, si lo hay, verificación de subpresión y estanqueidad. §3.4 **[FIRMA]**

### D. Manejo del agua (dibujado y presupuestado, no "de palabra")

- [ ] **Vereda perimetral continua ≥ 1,20 m (mejor 1,50 m), pendiente ≥ 2 % hacia afuera, junta elástica contra el muro**, en planos y en cómputo. §8.2
- [ ] Pluviales conducidos y con **descarga a ≥ 3,00 m** del perímetro. §8.3
- [ ] **Ninguna bajada pluvial** descarga al pie de la fundación. §8.3
- [ ] Cañerías enterradas **envainadas**, con cámaras de inspección **estancas**, sin empalmes bajo platea. §8.4
- [ ] **Pozo absorbente a ≥ 5,00 m** de la fundación, aguas abajo, con napa verificada. §8.5
- [ ] Nivelación general del terreno alejando el agua de la casa. §8.3
- [ ] **Paisajismo coordinado**: nada regado dentro de la franja perimetral, árboles a distancia. §8.6
- [ ] Pileta (si la hay) a ≥ 5,00 m, con vaciado y retrolavado conducidos. §8.7

### E. Obra

- [ ] Excavación **no abierta bajo lluvia**; hormigón de limpieza el mismo día. §7.5
- [ ] **Densidad del manto compactado medida**, no estimada. §7.5
- [ ] **Prueba de estanqueidad** de cañerías y cámaras antes de tapar. §8.4
- [ ] Curado de la platea ≥ 7 días. §7.5
- [ ] Capa aisladora horizontal **y vertical** continua. §7.5
- [ ] Registro fotográfico de fundaciones e instalaciones **antes de tapar** (documentación para el futuro). 

### F. Entrega

- [ ] **Manual del usuario** entregado y explicado al comitente. §8.9
- [ ] Planos conforme a obra de instalaciones enterradas, con cotas.
- [ ] Informe geotécnico y planos de fundación archivados y entregados al propietario.

---

## 11. Fuentes

**Geología y suelos de la zona**

- **Giai, S. B. y Tullio, J. O.** — *Características de los principales acuíferos de la provincia de La Pampa.* Facultad de Ciencias Humanas UNLPam y Dirección de Aguas de La Pampa. [chadileuvu.org.ar/pdf/acuiferos.pdf](https://chadileuvu.org.ar/pdf/acuiferos.pdf) — *(basamento granítico a 144 m en Santa Rosa; Fm. Cerro Azul hasta ~190 m; intercalación arcillosa entre 50 y 130 m; arenas eólicas de espesores máximos del orden de 10 m; niveles estáticos históricos; recarga 20–120 mm/año, media ~60 mm/año; superficie del acuífero 841 km²).*
- **Servicio Geológico Minero Argentino (SEGEMAR)** — *Hojas Geológicas 3763‑I y 3763‑III, Santa Rosa y Darregueira, provincias de La Pampa y Buenos Aires*, Boletín, 2023. [repositorio.segemar.gov.ar/handle/308849217/4394](https://repositorio.segemar.gov.ar/handle/308849217/4394) — **cartografía geológica oficial de la ciudad. Fuente principal del §2.** *(Fm. Meaucó, manto eólico suelto areno‑limoso de 0,20 a 2 m sobre el calcrete y de 3 a 30 m en valles y dunas; granulometría de la facies de manto; perfil del calcrete con horizontes hospedante, pulverulento, nodular, laminar y hardpan de hasta 1 m; nódulos de hasta 20 cm, láminas de 1 a 10 cm, rizolitos de 1–2 cm, crotovinas de tamaño métrico; grados de madurez IV–V al oeste y II–III al este; planicie estructural de cota 230 m al oeste a 120 m al este con gradiente 1,10 m/km; unidades hidroestratigráficas I a VII, con el acuífero freático alojado en la Fm. Meaucó; catorce indicios de canteras de tosca, con labores en áreas urbanas y suburbanas de Santa Rosa y Toay).* El mapa geológico 3763‑I está disponible por separado en el mismo repositorio.
- **Análisis litoestratigráfico de la Formación Cerro Azul** — Revista de la Asociación Geológica Argentina. [scielo.org.ar/img/revistas/raga/v67n2/html/v67n2a09.htm](https://www.scielo.org.ar/img/revistas/raga/v67n2/html/v67n2a09.htm) — *(limolitas y areniscas 92 % de la sucesión; arcilitas basales 7 %; calcretes al techo 1 %).*
- **Los calcretes del sudeste de la provincia de La Pampa: caracterización y origen** — Revista de la Asociación Geológica Argentina. [revista.geologica.org.ar/raga/article/download/438/484/1412](https://revista.geologica.org.ar/raga/article/download/438/484/1412) — *(espesores de calcrete 0,5 a 2 m; estructura transición/laminado/pisolítico; cobertura eólica pleistocena‑holocena; **datos del SE provincial, no de Santa Rosa**).*
- **INTA EEA Anguil** — *Descripción de las zonas y subzonas agroecológicas RIAP, área de influencia de la EEA Anguil* — *(Haplustoles énticos con tosca entre 0,50 y 1,50 m, y con tosca por debajo de 1,50 m; textura franco arenosa muy fina, ~16 % arcilla, hasta ~32 % limo).*

**Napa freática de Santa Rosa**

- **Viglizzo, E. F.** — *"¿Cayó Santa Rosa en una trampa hídrica?"*, La Arena, 13/06/2017. [laarena.com.ar](https://www.laarena.com.ar/la-ciudad/2017-6-13-0-50-11--cayo-santa-rosa-en-una-trampa-hidrica) — *(napa ~25 m en el centro a comienzos de los '90 → menos de 5 m en 2017; balance hídrico 1.400 mm entrada / 1.000 mm salida; Bajo Giuliani 550 ha en 1985 → 1.300 ha en 2015).*
- **Fábregas, G.** (geólogo, docente de Geotecnia, UNLPam) — *"La napa, a seis metros en el centro"*, La Arena, 02/08/2014. [laarena.com.ar](https://www.laarena.com.ar/la-ciudad/2014-8-2-4-36-14-la-napa-a-seis-metros-en-el-centro) — *(napa a ~6 m en el entorno de la plaza San Martín; filtraciones en edificios de los '70 fundados a 7 m; causas: fin del bombeo local, acueductos de Anguil y del Río Colorado, pérdidas de red).*
- **Consejo Federal de Inversiones** — *Registros y análisis del comportamiento piezométrico de las aguas subterráneas del subsuelo de la Ciudad de Santa Rosa, provincia de La Pampa.* [biblioteca.cfi.org.ar](http://biblioteca.cfi.org.ar/documento/registros-y-analisis-del-comportamiento-piezometrico-de-las-aguas-subterraneas-del-subsuelo-de-la-ciudad-de-santa-rosa-provincia-de-la-pamp/) — *(censo de 148 perforaciones de la APA en el radio urbano + 21 domiciliarias).* **Documento a solicitar.**
- **Administración Provincial del Agua (APA) de La Pampa** — organismo de consulta obligada para el dato de napa del sector.

**Reglamentación**

- **CIRSOC 401 — Reglamento Argentino de Estudios Geotécnicos** (INTI‑CIRSOC). Arts. 3.5.2, 3.5.4, 3.5.6.2, 3.6.7; Tablas 3.1 y 3.2. [contenidos.inpres.gob.ar/docs/Reglamentos/CIRSOC-401-Reglamento.pdf](http://contenidos.inpres.gob.ar/docs/Reglamentos/CIRSOC-401-Reglamento.pdf)
- **CIRSOC 401 — Comentarios.** C 3.5.5 y C 3.6.7 (suelos colapsables). [contenidos.inpres.gob.ar/docs/Reglamentos/CIRSOC-401-Comentarios.pdf](http://contenidos.inpres.gob.ar/docs/Reglamentos/CIRSOC-401-Comentarios.pdf)
- **CIRSOC 201** — clases de exposición del hormigón (agresividad química del suelo y del agua).
- **[VER]** Código de Edificación y reglamento de instalaciones sanitarias de la **Municipalidad de Santa Rosa**; normativa de la APA para pozos absorbentes. **Verificar antes de proyectar el sistema de efluentes.**

**Geotecnia del loess**

- **Rocca, R. J., Redolfi, E. R. y Terzariol, R. E.** — *Características geotécnicas de los loess de Argentina.* Rev. Int. de Desastres Naturales, Accidentes e Infraestructura Civil, Vol. 6(2). [fceia.unr.edu.ar/geologiaygeotecnia/Loess Rocca_Redolfi_Terzariol.pdf](https://www.fceia.unr.edu.ar/geologiaygeotecnia/Loess%20Rocca_Redolfi_Terzariol.pdf) — **fuente principal del §3.5 de `estructuras.md`.**
- **Redolfi, E. R.** — *Suelos colapsables.* Área Geotecnia, FCEFyN, Universidad Nacional de Córdoba, 2007. [fceia.unr.edu.ar/geologiaygeotecnia/Redolfi_2007_Suelos Colapsables.pdf](https://www.fceia.unr.edu.ar/geologiaygeotecnia/Redolfi_2007_Suelos%20Colapsables.pdf) — *(métodos de mejoramiento; densidades de 1,70–1,80 t/m³ suficientes para evitar el colapso por peso propio y aptas como manto de fundación; criterios de presión inicial de colapso).*

**Patología**

- **De Miguel, J. L.** — *Fisuras y grietas*, 2015. — *(patrones de fisuración por asiento, expansividad y retracción; criterio de la repetición en la misma vertical; efecto amortiguador de la cimentación en losa).*

**Documento interno relacionado**

- [`docs/03-estructuras/estructuras.md`](../03-estructuras/estructuras.md) — §3.1 a §3.7 (estudio de suelos, ensayos, correlaciones, loess colapsable, napa freática, contenido mínimo del informe geotécnico) y §4 (fundaciones).

---

> **Nota final sobre el alcance de este documento.** Es material de proyecto y de discusión profesional del estudio. **No sustituye al informe geotécnico del lote ni al cálculo estructural firmado.** Todos los valores marcados **[PD]** son órdenes de magnitud para anteproyecto; todos los marcados **[VERIFICAR con estudio de suelos]** sólo pueden salir del ensayo. **Cuando este documento y el informe geotécnico del lote digan cosas distintas, manda el informe.**
