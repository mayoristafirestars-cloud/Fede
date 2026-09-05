# Casa de una planta en Santa Rosa (La Pampa) — normativa urbana y trámite municipal

> **Documento operativo del estudio.** Cubre todo lo que hay que resolver *antes de dibujar* y
> todo lo que hay que hacer *después de dibujar* para una vivienda unifamiliar de planta baja
> en Santa Rosa. Reemplaza, para el caso "casa de una planta", los indicadores del Código
> Urbanístico derogado que figuran en `docs/00-marco/marco-local-santa-rosa.md`.

---

## Índice

- [0. Estado de las fuentes — qué se consiguió y qué no](#0-estado-de-las-fuentes--qué-se-consiguió-y-qué-no)
- [1. Marco normativo vigente](#1-marco-normativo-vigente)
- [2. Dónde se puede hacer una casa de una planta — distritos e indicadores](#2-dónde-se-puede-hacer-una-casa-de-una-planta--distritos-e-indicadores)
  - [2.1 Tabla maestra de indicadores residenciales](#21-tabla-maestra-de-indicadores-residenciales)
  - [2.2 Qué cambió respecto del código viejo](#22-qué-cambió-respecto-del-código-viejo-ord-32742005)
  - [2.3 Restricciones tipológicas distrito por distrito](#23-restricciones-tipológicas-distrito-por-distrito)
  - [2.4 Qué distrito conviene](#24-qué-distrito-conviene)
  - [2.5 Corredores comerciales](#25-corredores-comerciales--el-lote-frentista-cambia-de-reglas)
- [3. Cálculo de la superficie construible](#3-cálculo-de-la-superficie-construible)
  - [3.1 Método, en orden fijo](#31-método-en-orden-fijo)
  - [3.2 Ejemplo A — lote 12 × 30 m en R3](#32-ejemplo-a--lote-12--30-m-en-r3-360-m)
  - [3.3 Ejemplo B — lote 15 × 40 m en R2a](#33-ejemplo-b--lote-15--40-m-en-r2a-600-m)
  - [3.4 Ejemplo C — lote 15 × 40 m en R5](#34-ejemplo-c--lote-15--40-m-en-r5-600-m-el-caso-que-más-se-recorta)
- [4. Código de Edificación aplicado a una vivienda](#4-código-de-edificación-aplicado-a-una-vivienda)
- [5. Trámite municipal, paso a paso](#5-trámite-municipal-paso-a-paso)
- [6. Servicios: agua, cloaca, electricidad, gas](#6-servicios-agua-cloaca-electricidad-gas)
- [7. Checklist de verificación urbana antes de dibujar](#7-checklist-de-verificación-urbana-antes-de-dibujar)
- [8. Ambigüedades y contradicciones detectadas](#8-ambigüedades-y-contradicciones-detectadas-preguntas-para-planeamiento)
- [9. LO QUE HAY QUE IR A BUSCAR PERSONALMENTE](#9-lo-que-hay-que-ir-a-buscar-personalmente)
- [Anexo — fuentes y archivos descargados](#anexo--fuentes-y-archivos-descargados)

---

## 0. Estado de las fuentes — qué se consiguió y qué no

### ✅ CONSEGUIDO

| Documento | Estado | Vía |
|---|---|---|
| **Ordenanza 6976/2023 — Código Urbano Ambiental (CUA)**, texto completo, 134 pp. + planillas de usos + planos | **Obtenido.** PDF descargado y transcripto por OCR | Enlace de Google Drive publicado por el CPITLP en `cpitlp.org.ar/nuevocdigourbanoambiental`, resuelto vía `drive.google.com/uc?export=download&id=1WZucUvH9wsi4HXQA2zd5zQLiMNKFGbDV` |
| **Plano P1 — Zonificación (Distritos)** | Obtenido (PDF) | ídem, id `1c9t__k28a83RjZ1dEMNdJk--7Cs1e5MR` |
| **Plano P2 — Corredores Comerciales** | Obtenido (PDF) | ídem, id `1hcn4vgp8UEkjPhRUfqtzDeaG_cg2xMxr` |
| **Ordenanza 1581/1995 — Código de Edificación**, texto consolidado 86 pp. (rotulado por el CPITLP como *actualizado al 16/02/2022*) | **Obtenido, con texto seleccionable** | `noticias.cpitlp.org.ar/storage/articulos/formularios/codigo edificacion santa rosa v20201230.pdf` |
| **Ordenanza 6445/2020** (modificatoria del Código de Edificación) | Obtenida (escaneada, OCR parcial) | `cpitlp.org.ar/modificacionCodigoEdificacion` |
| **Manual de Procedimientos de la Dirección de Planeamiento Urbano y Obras Particulares** (vigente desde 01/03/2026) | **Obtenido.** Es la descripción oficial del trámite | CPITLP → Formularios → Santa Rosa |
| **Disposición 131/2025 SOySP** — planos sanitarios | Obtenida | ídem |
| **Acta de Inicio de Obra** (formulario municipal) | Obtenida | ídem |
| **"Elementos que componen el plano municipal"** (qué debe contener cada lámina) | Obtenido | ídem |
| **Carátula municipal de Santa Rosa** (PDF y DWG) | Obtenida | ídem |

### ❌ NO CONSEGUIDO

| Falta | Por qué | Impacto |
|---|---|---|
| **CUADRO 3.4.4.a / 3.4.4.b / 3.4.4.c del Código de Edificación** — superficies y lados mínimos de locales por clase, y **altura mínima de local** | El texto del Código remite literalmente a *"TEMAS DE INTERES – Sector: CUADROS CODIGO DE EDIFICACION"* del sitio del Concejo Deliberante. `concejosantarosa.gob.ar` está detrás de un **desafío de Cloudflare** (`cf-mitigated: challenge`, HTTP 403) que bloquea todo acceso automatizado; tampoco hay copias en Wayback Machine ni en repositorios alternativos | **Alto.** Sin esos cuadros no se pueden fijar por norma el lado y la superficie mínima de un dormitorio, estar, cocina o baño, ni la altura libre mínima |
| **CUADRO 3.4.5.1** — área mínima de vano de iluminación (I) y de ventilación (K) en función del área del local (A) y del factor X según ubicación del vano — y **GRÁFICO 3.4.5** (salientes, altura de vanos, profundidad de locales) | ídem | **Alto.** Es la planilla de iluminación y ventilación que hay que presentar firmada |
| **CUADRO 3.4.5.2** — ventilación natural por conducto | ídem | Medio (baños y cocinas sin vano exterior) |
| **CUADRO 5.2.2** — cantidad de artefactos sanitarios | ídem | Bajo en vivienda unifamiliar |
| **CUADRO 3.6.2** — número de ocupantes | ídem | Nulo en vivienda unifamiliar (ver §4) |
| **Ordenanza Fiscal / Tarifaria vigente** — importe de los Derechos de Construcción | No publicada en fuentes accesibles | **Alto para cotizar.** No hay ningún número de costo municipal verificado en este documento |
| **Aportes y valor de referencia del m² del CALP** (Resolución vigente) | El sitio del CALP publica la Resolución 22/2023 pero el valor actualizado está en una carpeta de Drive renderizada por JavaScript que no se pudo listar | **Alto para cotizar** |
| **Planillas municipales del CALP por localidad** (carpeta Drive `1I-fO4p4hZLSL_WqmFrHBmDJTGwaYZALA`) | Carpeta de Drive no listable sin navegador | Medio |

> ⚠ **Advertencia de método.** El cuerpo del Código Urbano Ambiental (páginas 1 a 134 del PDF)
> es un **escaneo sin capa de texto**. Todo lo transcripto de él en este documento proviene de
> un **OCR** (Tesseract, español) del PDF original, guardado en
> `fuentes/codigo-urbano-ambiental-ord6976-23-OCR.txt`. La lectura es buena, pero **antes de
> firmar un plano hay que verificar cada número contra la página del PDF**. El Código de
> Edificación, en cambio, tiene capa de texto real: sus transcripciones son fieles.

---

## 1. Marco normativo vigente

**Transcripción literal — Ordenanza 6976/23, Santa Rosa (L.P.), 09 de noviembre de 2023:**

> *"Artículo 1º.- Apruébase el Código Urbano Ambiental de la ciudad de Santa Rosa que como
> Anexo I forma parte integrante de la presente.*
> *Artículo 2º.- Derógase la Ordenanza Nº 3274/2005 y toda otra disposición que se oponga a
> las previsiones establecidas en el Código que se aprueba en el Artículo 1º de la presente,
> incluso las definiciones técnicas incorporadas a normas anteriores y que no se ajusten a los
> términos de las enunciadas en el Código Urbano Ambiental."*
>
> Expte. Nº 351/2004 - 4, 5 y 6 (CD) y Expte. Nº 9864/1994/1-12 (DE) y Expte Nº 927/2020/1-1 (DE).

**Consecuencia directa y correctiva:** el código urbanístico anterior era la **Ordenanza
3274/2005**, no la 1582/95. Está **derogado**. Los indicadores de la tabla del documento
`marco-local-santa-rosa.md` (retiros de fondo `(n−20)/3`, `/4`, `/5`, densidades de R3 y R2e,
subdivisión mínima de R6) **ya no rigen**. Ver §2.2.

| Norma | Objeto | Estado |
|---|---|---|
| **Ordenanza 6976/2023** — Código Urbano Ambiental | Zonificación, usos, tejido (FOS, alturas, retiros, densidad, CAS), estacionamiento, subdivisión | **Vigente** desde su promulgación |
| **Ordenanza 1581/1995** — Código de Edificación | Trámite, locales, patios, circulaciones, medios de salida, ejecución de obra, instalaciones | **Vigente**, con modificatorias |
| Ordenanzas modificatorias del Código de Edificación identificadas en el texto consolidado | 3216/2004 (número de ocupantes), 3428/2006 (veredas), 3667/2007 (medidores eléctricos y SET), 3895/2009 (medidores de gas), 4860/2013 (cercos), **6445/2020** (alcances, objetivos, tramitación, final de obra, validez del permiso, clasificación de obras, construcciones transitorias en calzada) | Vigentes |
| **Ordenanza 6278/2019** | Ratifica el convenio de 1980 por el cual la Provincia transfiere a la Municipalidad los servicios de agua potable y desagües cloacales del ejido | Vigente |
| **Ordenanza 6273/2019** | Deroga la Ordenanza 69/1983 (normas de Obras Sanitarias de la Nación) | Vigente |
| **Disposición 131/2025** (Secretaría de Obras y Servicios Públicos) | Suprime el plano sanitario específico para obras comunes; define el croquis sanitario obligatorio en el plano | Vigente desde 03/11/2025 |
| **Manual de Procedimientos de la Dirección de Planeamiento Urbano y Obras Particulares** | Circuito administrativo de todos los trámites de obra | Vigente desde 01/03/2026 |
| Ordenanza 7021/2024 + Resolución 317/2024 | Organigrama municipal del que depende Planeamiento | Vigente |

**Autoridad de aplicación (transcripto del Manual de Procedimientos):** Secretaría de Obras y
Servicios Públicos → **Dirección de Planeamiento Urbano y Obras Particulares**.

---

## 2. Dónde se puede hacer una casa de una planta — distritos e indicadores

**Respuesta corta: en casi toda la ciudad.** La planilla de usos del CUA (Anexo 2.1) marca
"1.1.1 Vivienda Individual" como uso admitido en CR1a, CR1b, CR1, CR2a-b, CR3, R2, **R2e (con
la salvedad "No R2e III y IV")**, R2a, R3 (I a IX), R3e, R4, R5, R6, y varios distritos E, I1,
PI, ISP, ISe, PU, RU y PE. Es decir: **el problema de una casa de una planta en Santa Rosa
nunca es "si se puede", es cuánto y con qué recortes.**

Los distritos donde el producto "casa" es el uso natural del tejido son
**R2, R2a, R2e, R3, R3e, R4, R5 y R6**, con alturas de 6 a 9 m. Una vivienda de planta baja
jamás toca el techo de altura de ninguno de ellos: **la altura no es un condicionante en este
proyecto.** Lo que manda es el **FOS**, el **retiro de fondo en planta baja**, el
**CAS (suelo absorbente)** y, en algunos distritos, el **retiro de frente**.

### 2.1 Tabla maestra de indicadores residenciales

Transcripta del Código Urbano Ambiental (Ord. 6976/2023), Título 5, Secciones 5.4 a 5.11.
Se agrega CR3 como referencia de borde del área central.

| Indicador | **R2** | **R2a** | **R2e** | **R3** | **R3e** | **R4** | **R5** | **R6** | *CR3 (ref.)* |
|---|---|---|---|---|---|---|---|---|---|
| **FOS** | 0,6 | 0,6 | 0,6 | 0,6 | 0,6 | 0,6 (hasta **0,8** en barrios de interés social con lotes ≤200 m², solo uso residencial) | 0,5 | 0,5 | 0,6 resid. / 0,8 no resid. en PB |
| **Retiro de frente** | — no exige | **Sí** (jardín). Sugerido: 3 m si fondo >30 m · 2 m si 20–30 m · 1,5 m si ≤20 m. Se puede avanzar hasta LM en el **50 % del ancho** | ídem R2a | — no exige | — no exige | — no exige | **4 m** intermedias · esquina: 4 m lado menor + 2 m lado mayor | **4 m** intermedias · esquina: 4 m / 2 m | Sin retiro |
| **Retiro de fondo — PLANTA BAJA** (solo si profundidad ≥ 26 m) | Mínimo **3 m**, ocupable con dependencias de servicio (cocheras, quinchos, bauleras, locales sanitarios, natatorios), **en una sola planta de 4,50 m de altura**, sin superar el FOS | ídem | Se admite ocupar el fondo con dependencias de servicio en una sola planta cumpliendo el FOS | ídem R2 | ídem R2 | ídem R2 | ídem R2 | ídem R2 | ídem R2 |
| **Retiro de fondo — PISOS SUPERIORES** | **(n−20)/2** | **(n−20)/2** | **(n−20)/2** | **(n−20)/2** | **(n−20)/2** | **(n−20)/2** | **(n−20)/2** | **(n−20)/2** | (n−20)/2 en 1º y 2º piso · **(n−20)/1,5** desde el 3º |
| **Retiro lateral** | — | — | — | — | — | — | **3 m de un lateral** si el frente ≥ 20 m | **3 m de un lateral** (sin condición de frente) | No se exige entre medianeras |
| **Subdivisión mínima** | 12 m / 300 m² | 15 m / 450 m² | 15 m / 450 m² | 12 m / 300 m² | 12 m / 300 m² | 10 m / 300 m² | 15 m / 600 m² | **20 m / 1.000 m²** | 12 m / 300 m² |
| **Altura máxima** | PB + 2 pisos ó 9 m | PB + 2 pisos ó 9 m | 9 m | PB + 1 piso ó 6 m | PB + 1 piso ó 6 m | PB + 1 piso ó 6 m | PB + 1 piso ó 6 m | Vivienda individual: PB+1 (6 m) · multifamiliar en parcelas >5.000 m²: PB+2 (9 m) | PB + 6 pisos ó 21 m |
| **Densidad** | 800 hab/ha · **0,08 hab/m²** | 400 hab/ha · **0,04 hab/m²** | **200 hab/ha** · **1 vivienda por parcela** (hasta 2 UF del mismo grupo familiar, sin tipología repetitiva) | **200 hab/ha** · **0,02 hab/m²** | **200 hab/ha** · **0,02 hab/m²** | **300 hab/ha** · **0,03 hab/m²** | **60 hab/ha** · **1 vivienda por parcela** (hasta 2 UF del mismo grupo familiar) | **60 hab/ha** · **1 vivienda por parcela** (ídem) | 0,1 hab/m² |
| **C.A.S.** (Coeficiente de Absorción del Suelo) | **0,20** | **0,15** | **0,15** | **0,20** | **0,20** | **0,20** | **0,25** | **0,30** | 0,20 resid. |
| **Cochera exigida** | 1 espacio guarda-auto (cuadro Título 7) | **Obligatoria en todo el distrito, 1 módulo mínimo por vivienda** | **Obligatoria en todo el distrito, 1 módulo mínimo por vivienda** | 1 espacio guarda-auto | 1 espacio guarda-auto | 1 espacio guarda-auto | 1 espacio guarda-auto | 1 espacio guarda-auto | 1 espacio guarda-auto |

**Notas de lectura (todas transcriptas del CUA):**

- `n` = profundidad del lote en metros. Para aplicar la densidad: **1,5 hab/dormitorio
  (3 habitantes cada 2 dormitorios)**.
- **FOS (art. 1.4.3.2):** *"Proporción máxima de la superficie total de una parcela que puede
  ser ocupada con edificios sobre el nivel +1,50 m respecto de la cota ±0,00, considerando la
  envolvente total del edificio, cubierta y semicubierta, excluidos solamente los balcones como
  salientes de vuelo menor o igual a 1,20 m, excluyendo los de configuración continua."*
- **C.A.S. — "Suelo Absorbente" (art. 1.4.1.15):** *"Porción mínima de la superficie total de
  una parcela que debe quedar libre de cualquier construcción que impida la permeabilidad del
  terreno natural, sean locales cubiertos, semicubiertos o **veredas exteriores**."*
  → **Es indicador nuevo y es una restricción de proyecto real:** los solados exteriores del
  patio computan en contra. En R2a/R2e (CAS 0,15) sobre 600 m² hay que dejar 90 m² de tierra
  o piso permeable, sin contar los 240 m² que quedan libres de FOS.
- **Lotes ≤ 200 m² (art. 4.3.1.6):** *"En lotes iguales o menores a 200 m2, el Factor de
  Ocupación del Suelo -FOS-, podrá ser igual al 80% de la superficie de aquellos."*
- **Lotes atípicos (art. 4.3.2.3):** *"En los lotes preexistentes cuyas dimensiones difieran
  considerablemente del parcelamiento típico del distrito podrán utilizarse indicadores de
  zonas análogas en el indicador de FOS, pudiendo variar el ancho mínimo de los retiros de
  frente sin coincidir totalmente con la línea municipal y prescindir del retiro lateral."*
- **Lotes en esquina (art. 4.3.1.1):** *"se considerará al lado de menor longitud como frente y
  como fondo, siendo el lado de mayor longitud considerado como el eje divisorio y frente
  lateral. Por consideraciones proyectuales podrá definirse el lado mayor como fondo."*
- **Uso de fondo en esquina (art. 4.3.1.5):** *"Las parcelas en esquinas que tengan uno de sus
  lados mayor a 26 m deberán cumplimentar el retiro de fondo correspondiente al Distrito sobre
  el lado menor, tanto para planta baja como pisos superiores, pudiendo optar por una
  distribución de las superficies en ambos ejes divisorios o la totalidad de la misma sobre el
  lado mayor."*
- **Retiro de frente compensable (art. 4.3.2.4):** *"Los retiros de frente podrán ser inferiores
  a lo establecido para cada Distrito siempre que existan razones ambientales o técnicas que
  así lo justifiquen, en cuyo caso se deberá compensar a lo largo del frente de la parcela la
  superficie teórica requerida. El criterio de compensación no aplica para eximir total o
  parcialmente el retiro, es decir que no se admitirá construcción sobre línea municipal, aun
  cuando ofrezca compensación. Tampoco se admitirá una compensación tal que por su geometría o
  por su condición espacial pueda asimilarse a un patio interior."*
- **Sistemas constructivos (art. 4.3.1.4):** *"En todos los Distritos se admite la ejecución de
  construcciones mediante sistemas constructivos tradicionales y alternativos y, en este último
  caso, deberán contar con el Certificado de Aptitud Técnica (CAT) emitido por el organismo
  competente."*

### 2.2 Qué cambió respecto del código viejo (Ord. 3274/2005)

Esto es lo que hay que desaprender. Si se proyecta con la tabla vieja se comete un error de
superficie y de partido.

| Tema | Código viejo (3274/2005, texto 2018) | **CUA vigente (6976/2023)** |
|---|---|---|
| Retiro de fondo, pisos superiores | Coeficiente por distrito: R2 `/3`, R2a `/5`, R2e `/5`, R3 `/4`, R4 `/4`, R5 `/4`, R6 `/4` | **Unificado en `(n−20)/2` para todos los distritos R.** Es el retiro **más exigente**, no el más laxo |
| Densidad R3 y R3e | 400 hab/ha · 0,04 hab/m² | **200 hab/ha · 0,02 hab/m²** (la mitad) |
| Densidad R2e | 400 hab/ha | **200 hab/ha** |
| Densidad R4 | 400 hab/ha | **300 hab/ha · 0,03 hab/m²** |
| Densidad R5 / R6 | "1 vivienda por parcela" | **60 hab/ha** + 1 vivienda por parcela (hasta 2 UF del mismo grupo familiar); multifamiliar solo en parcelas ≥ 5.000 m² con 3 lados a calle, 100 hab/ha |
| Subdivisión mínima R6 | 25 m / 1.000 m² | **20 m / 1.000 m²** |
| Suelo absorbente | No existía como indicador | **C.A.S. obligatorio en todos los distritos** |
| Corredores comerciales | Tipos 1 a 8, "+3 m sobre la altura del distrito" | **CC1 a CC13, con tramos A/B/C/D**, cada uno con su propio FOS, altura y retiros expresos |
| Módulo de estacionamiento | 12,5 m² genérico | 12,5 m² general · **15 m² con lado ≥ 2,50 m en vivienda unifamiliar** · 18 m² accesible · 4 m² moto |
| Módulo polivalente | No existía | **Nuevo: se admite un módulo habitable de 30 m² mínimo en el fondo de la parcela** (ver §2.3) |

### 2.3 Restricciones tipológicas distrito por distrito

**R2** — el más permisivo del tejido residencial. Densidad media, admite vivienda individual y
colectiva. Sin retiro de frente ni lateral. Sin restricción tipológica particular.
En conjuntos multifamiliares horizontales tipo viviendas adosadas, el estacionamiento debe
proyectarse **como área cubierta desde la aprobación del proyecto**.

**R2a** — transcripto (art. 5.5.7.f, "Tipología Constructiva"):

> *"Si bien se permite vivienda multifamiliar, la misma conservará ciertas características de la
> vivienda individual. Por tal motivo, **no se admitirán viviendas superpuestas**. Los accesos
> deberán resolverse a partir del nivel 0,00 y todas las unidades tendrán relación con un patio
> de uso privado cuyo lado mínimo respetará lo establecido en el Código de Edificación para
> patios de 1ra categoría. **No se admitirán unidades de 1 solo ambiente. Las viviendas serán de
> 2 -dos- dormitorios como mínimo**, y en caso de que exista posibilidad de crecimiento, el
> mismo no se hará a expensas de los espacios destinados a cocheras, ni podrá superar el factor
> de ocupación del suelo máximo admitido en ese sector urbano. En el Distrito R2aII, en caso de
> unificaciones parcelarias que resulten en lotes de más de 600 m2. se permitirá vivienda
> multifamiliar con los indicadores que corresponden para tal destino en el Distrito R2. […]
> Las parcelas frentistas a los Corredores Comerciales -Ameghino y Sgo. Marzo- se regirán por
> los indicadores urbanísticos que corresponden a los mismos."*

**R2e** — resguardo de calidad y homogeneidad edilicia. Densidad (art. 5.6.7.d):

> *"Densidad neta máxima: 200 Hab./ha. **Se admitirá solo una unidad de vivienda por parcela de
> hasta dos unidades funcionales del mismo grupo familiar sin tipología repetitiva.**"*

**R2eII es el Barrio Fitte**, declarado de interés de conjunto; los inmuebles incluidos en el
Inventario de Bienes Patrimoniales (Ord. 936/91) requieren **estudio particular de la Autoridad
de Aplicación** y vista consultiva de la Comisión Honoraria de Defensa del Patrimonio
(Ord. 643/89). **R2eIII y R2eIV son conjuntos ya sometidos a propiedad horizontal**: no aplica
subdivisión, el FOS máximo es la superficie cubierta original de los bloques, toda intervención
debe ser autorizada por el Consorcio según el Reglamento de Copropiedad, **y la planilla de usos
no admite en ellos vivienda individual nueva**.

**R3 / R3e** — el tejido residencial de baja densidad en compactación; probablemente el caso más
frecuente del estudio. Sin retiros de frente ni laterales. Una particularidad importante:

> *"f) Nota: En la tipología constructiva en **R3VII** y para todos los usos admitidos, la cota
> de nivel interior de planta baja deberá ser de igual o mayor a **1,20 m** del nivel de
> referencia del cordón de la vereda, o el equivalente de la rasante superior del mismo si no lo
> hubiera, pudiendo excluirse de esta condición, a criterio del proyectista, únicamente los
> locales de servicio o complementarios."*

→ **En el sector R3VII la casa va elevada 1,20 m sobre el cordón.** Es una zona con problema
hídrico. Cambia el partido, el acceso, la rampa vehicular y la accesibilidad. **Verificar en el
Plano P1 si el lote cae en R3VII antes de dibujar nada.** La planilla de usos además restringe
varios rubros comerciales con la leyenda "NO R3VII".

**R4** — residencial de baja densidad en recuperación. Único distrito con FOS 0,8 admitido, y
solo *"en los barrios de viviendas de interés social con terrenos de hasta 200 m2 de superficie
[…] para usos residenciales únicamente"*.

**R5 y R6** — baja densidad, tipología aislada:

> *"En parcelas de cualquier superficie se admite vivienda individual **aislada o de
> semiperímetro libre**."*
> *"Se admitirá sólo una vivienda por parcela de hasta dos unidades funcionales del mismo grupo
> familiar sin tipología repetitiva."*
> *"Los conjuntos de vivienda que no cuenten con servicios de agua potable de red pública deberán
> resolver el servicio en forma colectiva mediante sistemas alternativos no individuales. El
> servicio de cloaca se podrá resolver individualmente mediante sistema séptico o
> biodigestores."*

Son los distritos con **retiro de frente (4 m) y retiro lateral (3 m)** obligatorios, y con el
**CAS más alto (0,25 y 0,30)**. Es donde el lote se recorta más.

**Módulo polivalente — regla nueva y útil (art. 4.3.1.3), transcripta:**

> *"En todos los Distritos urbanos se permitirá, como uso principal o complementario, la
> construcción de un **módulo habitable polivalente** para cualquiera de los usos permitidos en
> los respectivos distritos […]. Estará ubicado en planta baja exclusivamente y podrá ser un
> espacio de un solo ambiente más el espacio destinado a baño, admitiéndose la cocina integrada
> si la tuviere, **cuya superficie útil mínima será de 30 m2** […]. Se admitirá un único módulo
> por parcela, pudiendo contar o no con proyecto de vivienda. Cuando el mismo se ubique en el
> fondo de la parcela, **no podrá ser ampliado ni anexársele locales para transformarlo en
> vivienda principal**. Si en la parcela existe o se proyecta una vivienda, el módulo polivalente
> podrá vincularse a ésta a través de un apéndice, pero preservando un espacio descubierto con
> una **distancia mínima entre ambas construcciones de cuatro (4) metros de lado mínimo**, por el
> ancho de casi la totalidad de la parcela. Se mantendrá como unidad complementaria o deberá
> estar **separado tres (3) metros del eje divisorio** desde su ejecución para preservar el
> pulmón de manzana."*

→ **Lectura del estudio (inferido):** es la vía legal para el "departamento del fondo", el
consultorio, el taller o el estudio de 30 m² en una parcela con casa, en cualquier distrito
residencial. Vale la pena ofrecerlo como opción en la primera reunión con el comitente, pero
hay que decir con claridad que es **un único módulo por parcela y que no se puede ampliar**.

### 2.4 Qué distrito conviene

**Lectura del estudio (inferido a partir de los indicadores transcriptos):**

1. **R2 es el mejor distrito para una casa de una planta.** FOS 0,6, sin retiro de frente ni
   lateral, CAS 0,20, altura sobrada, densidad holgada. Todo el FOS se puede volcar a la casa.
2. **R3 / R3e son casi tan buenos** (mismos retiros, mismo FOS, mismo CAS) y son el tejido más
   extendido. La única diferencia real frente a R2 es la densidad, que en una casa unifamiliar
   no ata. **Salvo que el lote caiga en R3VII, donde hay que elevar la planta baja 1,20 m.**
3. **R4 es equivalente a R3**, con el bonus de FOS 0,8 en lotes de interés social ≤ 200 m².
4. **R2a y R2e cuestan superficie**: el retiro de frente para jardín consume una franja de 1,5 a
   3 m en todo el ancho (compensable hasta el 50 % del ancho), el CAS baja a 0,15 y la cochera
   es obligatoria desde el proyecto. A cambio se compra vecindad de mejor calidad edilicia y
   parcelas más grandes (450 m²).
5. **R5 y R6 son los más caros en suelo**: 4 m de retiro de frente + 3 m de retiro lateral + CAS
   0,25/0,30 + FOS 0,5. Sobre 600 m² el FOS ya baja a 300 m², y hay que dejar 150 m² de suelo
   absorbente. Son distritos de casa aislada con jardín, no de casa que aprovecha el lote.
6. **CR1, CR2 y CR3 admiten vivienda individual, pero no tiene sentido económico**: se está
   pagando suelo de área central con FOS 0,6 y altura de 21 a 48 m sin usarla.

### 2.5 Corredores comerciales — el lote frentista cambia de reglas

**Transcripto (art. 4.3.3.2):** *"Los parámetros de Corredores Comerciales aplican para todas
las parcelas frentistas a las calles asignadas como corredores por el presente Código
urbanístico, incluyendo a aquellas parcelas cuya calle que las delimita no es un corredor, pero
se ubican adyacentemente y por su condición geométrica en la trama lo componen
volumétricamente."*

**Transcripto (art. 4.3.3.3):** *"En Corredores Comerciales no aplica retiro de frente, excepto
en los específicamente dispuestos."*

El CUA define **13 corredores (CC1 a CC13)**, varios de ellos partidos en tramos A, B, C y D,
**cada uno con FOS, altura, retiros y subdivisión propios**. Ya no existe la regla general
"+3 m sobre la altura del distrito". Ejemplo transcripto del **CC1 tramo A** (Av. Circunvalación
Santiago Marzo, desde la rotonda de acceso Norte hasta S. López / Camino del Centenario):

> *"c) FOS: 0,8 en Planta Baja para usos no residenciales cuando éstos ocupen el 50 % de la
> superficie como mínimo · 0,6 en Planta Baja para usos residenciales · 0,6 en Pisos superiores
> para todos los usos · 0,9 en parcelas de superficie inferior a 200 m2, en Planta Baja y los 2
> pisos superiores. d) Altura: PB y 3 pisos — 12 mts. e) Retiros: Frente: sin retiro. Fondo: PB:
> 3 mts. Para usos complementarios sin retiro. Pisos Superiores: (n−20)/2 […] Lateral: sin
> retiro. f) Subdivisión del Suelo: Área: 600 m2 · Frente Mínimo: 15 mts."*

→ **Para una casa de una planta un corredor no aporta nada** (el FOS residencial sigue siendo
0,6) **pero puede quitar**: cambia la subdivisión mínima y puede imponer retiros distintos.
**Chequear siempre el Plano P2 antes de asumir los indicadores del distrito.**

---

## 3. Cálculo de la superficie construible

### 3.1 Método, en orden fijo

1. **Ubicar el lote en el Plano P1** (distrito) **y en el Plano P2** (¿es frentista a un
   corredor?). Si es frentista a corredor, mandan los indicadores del corredor.
2. **Superficie máxima ocupable = superficie del lote × FOS.** Recordar qué computa: envolvente
   total, cubierta **y semicubierta**, excluidos solo balcones de vuelo ≤ 1,20 m. Y recordar la
   nota municipal de "Elementos que componen el plano": *"el total de las superficies y
   proyecciones de todas las plantas **y aleros** sobre el suelo, computadas al 100 %, necesarias
   para el cálculo del FOS"*. **Los aleros computan.**
3. **Dibujar la huella real:** restar retiro de frente (si el distrito lo exige), retiros
   laterales (R5/R6) y el **retiro de fondo de planta baja** (mínimo 3 m si la profundidad ≥ 26 m,
   ocupable solo con dependencias de servicio en una sola planta de hasta 4,50 m).
   **La superficie construible es el MENOR entre el FOS y la huella real.**
4. **Verificar el CAS:** superficie del lote × CAS = m² de suelo que deben quedar permeables,
   **sin construcción y sin solado**. Descontarlos del patio, no del FOS.
5. **Verificar la densidad:** superficie del lote × indicador parcelario = habitantes admitidos;
   dividir por 1,5 = dormitorios admitidos. En R2e, R5 y R6 el límite no es aritmético: es
   **una vivienda por parcela**.
6. **Ubicar la cochera:** 1 espacio guarda-auto en todos los casos. En vivienda unifamiliar,
   **15 m² con lado ≥ 2,50 m**, y **el FOS ya la incluye** (no hay bonus del 20 %).
7. **Verificar las visuales a linderos** (Código de Edificación 3.8.1): ninguna abertura
   enfrentada al eje divisorio a menos de 3,00 m. Esto define dónde pueden ir las ventanas de
   los dormitorios.
8. **Verificar los patios** (Código de Edificación 3.4.7): 1ª categoría, lado ≥ 3,00 m y área
   ≥ 12,00 m² para locales habitables; 2ª categoría, lado ≥ 2,00 m y área ≥ 8,00 m² para baños,
   cocinas chicas, lavaderos y circulaciones.
9. **Cerrar con el trámite de Factibilidad** (§5) si hay cualquier duda de interpretación.

### 3.2 Ejemplo A — lote 12 × 30 m en R3 (360 m²)

Lote entre medianeras, intermedio, sin corredor, **no** en R3VII.

| Paso | Cálculo | Resultado |
|---|---|---|
| Superficie del lote | 12 × 30 | **360 m²** |
| FOS 0,6 | 360 × 0,6 | **216 m² ocupables** |
| Retiro de frente | R3 no exige | **0 m** |
| Retiro lateral | R3 no exige | **0 m** |
| Retiro de fondo en PB (prof. 30 ≥ 26 m) | Mínimo **3 m**, ocupable con dependencias de servicio en una sola planta ≤ 4,50 m | franja de 12 × 3 = 36 m² |
| Huella disponible para el uso principal | 12 × (30 − 3) = 12 × 27 | **324 m²** |
| **Superficie construible** | menor entre FOS (216) y huella (324) | **216 m² — manda el FOS** |
| C.A.S. 0,20 | 360 × 0,20 | **72 m² de suelo permeable obligatorio** |
| Superficie descubierta resultante | 360 − 216 | 144 m², de los cuales **72 m² sin solado** |
| Densidad | 360 × 0,02 hab/m² = 7,2 hab ÷ 1,5 hab/dorm | **4 dormitorios** admitidos (4,8 → 4; criterio de redondeo a verificar) |
| Cochera | 1 espacio guarda-auto, 15 m², lado ≥ 2,50 m, **incluido en el FOS** | −15 m² |
| **Queda realmente para la casa** | 216 − 15 (cochera) − ~12 (galería) − ~8 (aleros computables) | **≈ 180 m² de casa** |

**Lectura:** en el lote más típico de Santa Rosa entran cómodamente una casa de 3 dormitorios
de ~150 m², galería, cochera y aleros, y todavía sobra FOS. **El indicador que primero se agota
no es el FOS: es el CAS**, porque los 72 m² permeables obligan a no solar todo el patio, y la
franja de fondo de 3 m ya no se puede sumar al estar-comedor (solo admite dependencias de
servicio). El partido natural es **casa al frente sobre línea municipal o con jardín corto,
patio en el medio, y quincho/lavadero/cochera contra el fondo**.

### 3.3 Ejemplo B — lote 15 × 40 m en R2a (600 m²)

| Paso | Cálculo | Resultado |
|---|---|---|
| Superficie del lote | 15 × 40 | **600 m²** |
| FOS 0,6 | 600 × 0,6 | **360 m² ocupables** |
| Retiro de frente (jardín obligatorio) | Fondo del lote 40 m > 30 m → sugerido **3 m**. Se puede avanzar hasta LM en el 50 % del ancho, es decir en 7,50 m de los 15 m | franja de 15 × 3 = 45 m²; hasta 22,5 m² recuperables sobre LM |
| Retiro lateral | R2a no exige | **0 m** |
| Retiro de fondo en PB (prof. 40 ≥ 26 m) | Mínimo **3 m**, ocupable solo con dependencias de servicio | franja de 15 × 3 = 45 m² |
| Retiro de fondo en pisos superiores | (40 − 20)/2 = **10 m** — *no aplica: la casa es de una planta* | — |
| Huella disponible para el uso principal | 15 × (40 − 3 − 3) = 15 × 34 | **510 m²** |
| **Superficie construible** | menor entre FOS (360) y huella (510) | **360 m² — manda el FOS** |
| C.A.S. 0,15 | 600 × 0,15 | **90 m² de suelo permeable obligatorio** |
| Superficie descubierta resultante | 600 − 360 | 240 m², de los cuales **90 m² sin solado** |
| Densidad | 600 × 0,04 hab/m² = 24 hab ÷ 1,5 | 16 dormitorios — **no ata** |
| Cochera | **Obligatoria en R2a**, 1 módulo mínimo por vivienda, 15 m², incluida en el FOS | −15 m² |
| **Queda realmente para la casa** | 360 − 15 (cochera) − ~25 (galería) − ~12 (aleros) | **≈ 308 m² de casa** |

**Lectura:** en R2a el FOS es tan generoso para una casa que **el proyecto lo define el programa,
no la norma**. Lo que sí condiciona el partido es el **retiro de frente**: hay que resolver un
jardín de 3 m en el 50 % del ancho como mínimo, y el Código recomienda *"mantener el Retiro de
Frente en los locales de máxima permanencia -Estar, comedor, Dormitorios-"* y *"mantener la
correspondencia entre los Retiros y/o áreas construidas linderas"*. Con 40 m de fondo y solo
3 m de retiro de fondo exigido, hay margen para una casa en dos crujías con patio central.

### 3.4 Ejemplo C — lote 15 × 40 m en R5 (600 m²): el caso que más se recorta

Mismo lote, distrito R5, para mostrar el contraste.

| Paso | Cálculo | Resultado |
|---|---|---|
| FOS 0,5 | 600 × 0,5 | **300 m²** |
| Retiro de frente | 4 m (parcela intermedia) | 15 × 4 = 60 m² |
| Retiro lateral | frente 15 m < 20 m → **no se exige** | 0 m |
| Retiro de fondo en PB | mínimo 3 m | 15 × 3 = 45 m² |
| Huella disponible | 15 × (40 − 4 − 3) = 15 × 33 | 495 m² |
| **Superficie construible** | menor entre 300 y 495 | **300 m²** |
| C.A.S. 0,25 | 600 × 0,25 | **150 m² permeables** |
| Descubierto | 600 − 300 = 300 m², **la mitad sin solado** | |
| Densidad | 1 vivienda por parcela (hasta 2 UF del mismo grupo familiar) | |

**Lectura:** el mismo lote pierde **60 m² de superficie construible** solo por cambiar de R2a a
R5, y obliga a 150 m² de tierra. Si el frente hubiera sido de 20 m o más, además se sumaría un
retiro lateral de 3 m. **La diferencia entre distritos, en un lote idéntico, es de un dormitorio
y medio.** Por eso la primera pregunta de la primera reunión es el distrito, no el programa.

---

## 4. Código de Edificación aplicado a una vivienda

Todo lo que sigue está **transcripto literalmente** de la Ordenanza 1581/1995, texto consolidado
(archivo `fuentes/codigo-edificacion-ord1581-95-santa-rosa.pdf`), salvo donde se indique.

### 4.1 Clasificación de locales (art. 3.4.2) — TRANSCRIPTO

> **Primera Clase:** *Dormitorio, sala de estar, comedor, comedor diario, escritorio, biblioteca,
> estudio, dormitorio de servicio, sala de juegos, oficina, consultorio, **cocina de más de
> 15,00 m² de superficie**, cuarto de plancha o de costura de más de 6,00 m² de superficie, y
> todo otro local habitable no clasificado de otro modo por este Código.*
>
> **Segunda Clase:** *Cocina hasta 15 m² de superficie, **baño, lavadero**, cuarto de plancha o de
> costura de hasta 6 m² de superficie.*
>
> **Tercera Clase:** *Local para comercio y trabajo, depósito comercial e industrial, vestuario
> colectivo, local para la práctica deportiva, comedor colectivo, cocina de restaurant, casa de
> comida, hotel o comedor colectivo.*
>
> **Cuarta Clase:** *Vestíbulo, pasillo, corredor, sala de espera anexa a oficina o consultorio,
> vestidor anexo a dormitorio, despensa, depósito familiar, depósito no comercial […]*
>
> **Quinta Clase:** *Locales auxiliares para servicios generales de un edificio como sala de
> máquinas, dependencias del personal de servicio, baulera, depósito de utensilios, sala común de
> juegos infantiles, salón de usos múltiples, sala común de estar, administración y portería […]*

Además (art. 3.4.1): *"El uso de cada local es el que resulta de su ubicación y dimensiones, y
no el que arbitrariamente pueda estar consignado en planos, siendo atribución de la
Municipalidad presumir el destino de los locales a su exclusivo criterio."*

→ **Consecuencia práctica:** rotular un local como "escritorio" para escaparle a la exigencia de
dormitorio no funciona. Y **una cocina de más de 15 m² deja de ser local de 2ª clase y pasa a
1ª**, con lo que necesita patio de 1ª categoría (lado ≥ 3 m, área ≥ 12 m²), no de 2ª.

### 4.2 Definiciones dimensionales (art. 3.4.3) — TRANSCRIPTO

> *"**Altura libre mínima de un local:** Es la distancia comprendida entre el solado y el
> cielorraso terminado. Cuando haya vigas aparentes, el fondo de estas deberá distar **no menos
> de 2,30 m** del solado y **no ocuparán más de 1/3 de la superficie del cielorraso**.*
> ***Distancia mínima entre solados:** Comprende la altura libre de un local más el espesor del
> entrepiso superior.*
> ***Área mínima de un local:** Es la superficie mínima de un local **incluyendo los armarios o
> roperos empotrados**.*
> ***Lado mínimo de un local:** Es el lado mínimo libre **excluyendo los armarios o roperos
> empotrados**, en caso de dormitorios se considerará 0,60 m de espacio de un ropero."*

### 4.3 ❌ Superficies, lados y altura mínimos de locales — NO SE CONSIGUIÓ

**Transcripción exacta de lo que dice el Código en ese punto (art. 3.4.4):**

> *"CUADRO 3.4.4 DIMENSIONES MINIMAS DE LOS LOCALES. 1. Generalidades: Cada local tendrá las
> dimensiones mínimas que se especifican de acuerdo a su clase y uso al que está destinado, según
> lo indicado en los CUADRO 3.4.4.a, CUADRO 3.4.4.b y CUADRO 3.4.4.c. **Los presentes cuadros por
> razones de programación deben consultarse en -TEMAS DE INTERES - Sector: CUADROS CODIGO DE
> EDIFICACION**: CUADRO 3.4.4.a VER EN TEMAS DE INTERES · CUADRO 3.4.4.b VER EN TEMAS DE INTERES
> · CUADRO 3.4.4.c VER EN TEMAS DE INTERES"*

**No se pudo obtener el contenido de esos tres cuadros.** El sitio del Concejo Deliberante
(`concejosantarosa.gob.ar`) está protegido por Cloudflare y devuelve 403 a todo acceso
automatizado; no hay copias en Wayback Machine ni en repositorios alternativos, ni en la
Ordenanza 6445/2020, ni en los materiales que el CPITLP publica.

**Por lo tanto, este documento NO fija:**

- superficie mínima ni lado mínimo de dormitorio, estar, comedor, cocina, baño y lavadero;
- **altura libre mínima de local habitable** (el Código solo fija, indirectamente, que el fondo
  de una viga aparente no puede bajar de 2,30 m del solado, y que un entrepiso comercial tiene
  altura libre mínima de 2,10 m — **ninguno de los dos es la altura mínima de un local**);
- profundidad máxima de local en relación con el vano.

**Lo que hay que pedir, con nombre exacto:** *Cuadros 3.4.4.a, 3.4.4.b y 3.4.4.c del Código de
Edificación (Ordenanza 1581/95)* — ver §9.

### 4.4 ❌ Iluminación y ventilación natural — NO SE CONSIGUIÓ el cuadro

**Transcripto (art. 3.4.5):**

> *"1. Iluminación y ventilación natural: Todos los locales de un edificio deberán contar con
> iluminación y ventilación natural, de acuerdo a su clase y al uso al que están destinados,
> salvo aquellos casos que se encuentre específicamente exceptuados por este Código. Las
> dimensiones de los vanos son las que se detallan en el **CUADRO 3.4.5.1**, y las dimensiones
> máximas o mínimas de salientes, alturas de vanos y profundidad de locales son las que se
> indican en el **gráfico 3.4.5**.*
> *2. Ventilación natural por conducto: La ventilación natural por conducto de los locales que se
> detallan, se realizará según las dimensiones y características que establecen el **CUADRO
> 3.4.5.2**.*
>
> ***CUADRO 3.4.5.1 — ILUMINACION Y VENTILACION NATURAL. REFERENCIAS: I = Área mínima de vano
> para iluminación · A = Área total de la planta del local · X = Valor dependiente de la ubicación
> del vano · K = Área mínima de vano para ventilación. LOCALES DE PRIMERA CLASE EN VIVIENDA: Los
> presentes cuadros por razones de programación deben consultarse en -TEMAS DE INTERES-"***

→ **Se conoce la estructura de la fórmula (I = A/X, con K derivado de I) pero no los valores de
X ni la proporción de K.** Sin eso no se puede completar la **Planilla de Iluminación y
Ventilación** que el municipio exige en el plano (ver §5.4, ítem 10). **Es el hueco más urgente
de todo este documento.**

### 4.5 ✅ Patios (art. 3.4.7) — TRANSCRIPTO COMPLETO

> *"**a- Patios de Primera Categoría:** sirven para proporcionar iluminación y ventilación a
> locales de primera, tercera y quinta categoría, sus dimensiones mínimas serán **hasta 13,00 m
> de altura sus lados mínimos serán 3,00 m y área de 12,00 m²**; superando los 13,00 m de altura,
> sus dimensiones mínimas serán de **3,00 m de lado mínimo y 18,00 m² de área**.*
> ***b- Patios de Segunda Categoría:** sirven para proporcionar iluminación y ventilación a
> locales de segunda y cuarta categoría, sus dimensiones mínimas serán **2,00 m de lado y 8,00 m²
> de área**.*
> *2- División de Patios con Cercas: Un patio de cualquier categoría puede en su base ser dividido
> por cercas interiores, siempre que entre paramentos próximos quede un **paso libre no inferior
> a 1,00 m**.*
> *3- Acceso a Patios: Todo patio contará con un acceso practicable para su limpieza.*
> *4- Prohibición de cubrir Patios: No se podrá cubrir patios en edificios existentes no
> construidos de acuerdo a éste Código, mediante cubierta alguna aunque se trate de claraboyas
> corredizas con armadura vidriada, salvo cuando el patio resulte innecesario según las
> prescripciones vigentes, se permitirá la instalación de toldos."*

**Para una casa de una planta esto es directamente aplicable y no tiene ambigüedad:**
un patio al que ventilen dormitorios, estar o comedor debe tener **3,00 m de lado y 12,00 m² de
área**. Un patio de servicio al que solo ventilen baño, cocina ≤ 15 m² y lavadero: **2,00 m de
lado y 8,00 m²**.

El CUA agrega (art. 4.3.4.b) para todos los distritos: *"En todos los casos se deberá dejar 3 m
libres en patios que sirvan a la iluminación y ventilación de locales de primera categoría.
Cuando las ventanas de distintas unidades habitacionales en distintas parcelas o en la misma se
enfrenten, la distancia mínima será de 6 m libres."*

### 4.6 ✅ Espacio exterior propio — TRANSCRIPTO (CUA art. 4.3.4.b)

> *"Toda vivienda debe contar con un espacio exterior propio, sea este abierto o semicubierto
> (patio, balcón, terraza). […] Los espacios exteriores propios de tipo balcón o terraza serán
> considerados como tales cuando cumplan con las condiciones mínimas de **3,60 m² de superficie y
> lado no inferior a 1,20 m**."*

Y la exención que interesa a una casa (CUA art. 4.3.4.a): *"Quedan exceptuadas de la obligación
[de ventilar exclusivamente al frente o al corazón de manzana] las construcciones destinadas a
**vivienda unifamiliar** o aquellos conjuntos multifamiliares desarrollados en 3 niveles (PB y
2P), así como las unidades de vivienda que tengan 3 o más dormitorios, pudiendo iluminar y
ventilar estos últimos hacia espacios abiertos de 18 m² y 3 m de lado mínimo."*

### 4.7 ✅ Circulaciones y escaleras (arts. 3.5.1 a 3.5.4) — TRANSCRIPTO

> *"**Entradas y pasajes generales:** Un pasaje general y la entrada al mismo deben tener en
> cualquier dirección un **ancho libre no inferior a 1,00 m**, salvo en aquellos casos que el
> presente Código determine otra medida.*
>
> ***Escaleras Principales:** Son aquellas que dan acceso a locales de primera y tercera clase, a
> las circulaciones generales o comunes de un edificio, y a los locales habitables y de trabajo
> clasificados en cuarta y quinta clase. El **ancho libre de una escalera principal medido entre
> zócalos no será inferior a 1,00 m** […]. La **altura de paso** medida en cualquier punto de la
> escalera **no puede ser inferior a 2,10 m**. Las pedadas y los descansos de la escalera se miden
> sobre la línea de huella, entendiendo como tal la línea paralela al limón interior a 0,50 m de
> distancia de éste. Todos los escalones de un mismo tramo deben tener la misma dimensión medida
> sobre la línea de huella, y **cada tramo entre rellanos o descansos no puede tener más de 21
> alzadas corridas**. Las dimensiones responderán a las siguientes fórmulas:*
> ***2a + p = 0,60 m a 0,63** · **a ≤ 0,18 m** · **p ≥ 0,26 m** · **l ≥ 0,13 m** · **d ≥ 1,00 m**
> · **r ≥ 0,25 m***
> *donde a = alzada, p = pedada en la línea de huella, l = pedada junto al limón interior,
> d = descanso en la línea de huella, r = radio de la proyección horizontal del limón interior.*
>
> ***Escaleras secundarias:** Son aquellas que dan acceso a locales de segunda clase, a locales no
> habitables de cuarta y quinta clase, y a azoteas transitables, y las escaleras auxiliares
> exteriores de un edificio. El **ancho libre […] no será inferior a 0,70 m** […]. La altura de
> paso […] **no puede ser inferior a 2,00 m**. Un tramo […] tendrá un máximo de **25 alzadas
> corridas**. Las dimensiones responderán a: **a ≤ 0,20 m · p ≥ 0,23 m · l ≥ 0,10 m · d ≥ 0,50 m ·
> r ≥ 0,15 m**.*
>
> ***Rampas:** Una rampa puede reemplazar a una escalera, debiendo tener el ancho mínimo exigido
> para éstas […]. Su **pendiente será como máximo del 10 %**, su solado antideslizante y tendrá
> partes horizontales a manera de descansos en los accesos y en los sitios donde la rampa cambia
> de dirección."*

→ En una casa de una planta esto se aplica a la **escalera de acceso a la azotea o al entrepiso
de guardado**, y a la **rampa de acceso** cuando la planta baja va elevada (obligatorio en
R3VII, donde el nivel interior debe estar ≥ 1,20 m sobre el cordón — con 10 % de pendiente máxima
eso son **12 m de desarrollo de rampa** más descansos; hay que preverlo en el partido).

### 4.8 ✅ Medios de salida — la exención que importa (art. 3.6.1) — TRANSCRIPTO

> *"Todo edificio o unidad de uso independiente debe contar con los medios de salida diseñados y
> dimensionados de acuerdo a la cantidad de personas que alberga […]. **Estas exigencias no son
> de aplicación en la vivienda individual.**"*

→ **En una casa unifamiliar no se dimensionan medios de salida ni número de ocupantes.** Por eso
la falta del CUADRO 3.6.2 no afecta a este proyecto.

### 4.9 ✅ Cocina, baño y servicios sanitarios — TRANSCRIPTO

> *"**5.8.2 LOCAL PARA COCINAR:** Toda unidad de uso independiente, cualquiera sea su destino, de
> superficie mayor a 100,00 m², **así como toda unidad de vivienda, cualquiera sea su superficie,
> deben contar con un local independiente destinado a cocina**, con las dimensiones que se
> determinan en el Artículo 3.4.4."*

→ **Ojo con la cocina integrada.** El Código exige *local independiente destinado a cocina* en
toda vivienda. La única figura del CUA que admite expresamente cocina integrada es el **módulo
polivalente** (*"admitiéndose la cocina integrada si la tuviere"*). **Un estar-comedor-cocina
único en una vivienda es una interpretación que hay que consultar por escrito antes de
dibujarlo** (ver §8).

> *"**5.2.1 SERVICIO SANITARIO MINIMO:** En todo predio, edificado o no, donde se habite, trabaje
> o realice alguna actividad, existirán por lo menos los siguientes servicios sanitarios:
> a- Un retrete de albañilería u hormigón, con paramentos y solado revestidos de material
> resistente, liso e impermeable, dotado de inodoro. b- Una pileta de cocina o pileta de lavar o
> lavatorio. c- Instalaciones de provisión de agua y desagües cloacales en un todo de acuerdo a
> las normativas vigentes en la materia."*
>
> *"**5.2.4 INDEPENDENCIA DE LOS LOCALES SANITARIOS:** Los locales de los servicios sanitarios
> serán independientes de los locales de trabajo, habitación y permanencia, **comunicándose con
> éstos por medio de compartimientos intermedios o pasos, y provistos de puertas o elementos fijos
> que impidan la visión del interior de los servicios**."*

> *"**4.7.2 REVESTIMIENTOS** […] La altura mínima del revestimiento impermeable será de 2,00 m
> medidos desde el solado […]"* y *"El solado de un local destinado a baño, retrete o tocador se
> ejecutará con solado impermeable de mármol, mosaico, baldosas plásticas o cerámicas."*

### 4.10 ✅ Cocheras (art. 3.4.4, punto 3) — TRANSCRIPTO

> *"Un espacio o local para la guarda de un automóvil particular deberá tener una **superficie
> mínima de 12 m², un lado mínimo de 2,60 m y una altura no inferior a 2,00 m**. **Si ese espacio,
> además, sirve de acceso peatonal a la vivienda la superficie mínima será de 14,00 m², su lado
> mínimo de 2,90 m y su altura no inferior a 2,40 m.** En las cocheras colectivas, el espacio
> destinado al estacionamiento de cada vehículo tendrá una superficie mínima de 12,50 m², un lado
> mínimo de 2,50 m y una altura libre no inferior a 2,20 m entre el solado y el fondo de vigas.
> A ésta superficie deberá adicionarse la requerida para la circulación y maniobras de los
> vehículos."*

**⚠ Contradicción con el CUA**, que dice: *"En viviendas unifamiliares se preverá un espacio de
15 m², cuyo lado mínimo será igual o mayor a 2,50 m."*

**Criterio del estudio (inferido):** adoptar **lo más exigente de cada parámetro** —
**15 m² de superficie** (CUA), **lado 2,90 m** y **altura 2,40 m** (Código de Edificación) cuando
la cochera sirve además de acceso peatonal a la casa, que es el caso normal en una vivienda
entre medianeras. Consultar por escrito (ver §8).

### 4.11 ✅ Vistas a linderos — la regla que define dónde van las ventanas (art. 3.8) — TRANSCRIPTO

> *"**3.8.1. VISTAS A PREDIOS LINDEROS:** **No se permiten vistas a predios linderos ni a unidades
> de uso independiente dentro del mismo predio, aunque sean del mismo dueño, desde aberturas
> enfrentadas al Eje Divisorio del predio o unidad de uso, si la distancia entre el muro que
> contiene el vano y dicho eje es inferior a 3,00 m.** Cuando se proyecten aberturas que no
> cumplan con la distancia exigida, se debe impedir la vista al predio o unidad de uso lindera
> utilizando **elementos fijos, sean opacos o traslúcidos, con una altura no inferior a 1,60 m**
> medidos desde el solado correspondiente. **Una abertura ubicada en un paramento perpendicular al
> Eje Divisorio, debe distar de éste un mínimo de 0,50 m.**"*
>
> *"**3.8.2. VANOS EN MUROS DIVISORIOS:** Para proporcionar a un local iluminación suplementaria a
> la exigida por éste Código pueden abrirse vanos en Muro Divisorio, o en muro privativo contiguo
> a Eje Divisorio hacia predios o unidades linderas, siempre que **el antepecho de la abertura se
> ubique a más de 1,60 m del solado del local y se cierre con un paño fijo no transparente**."*
>
> *"**3.8.3. INSTALACIONES QUE AFECTEN A LINDEROS:** Queda prohibido instalar o construir sobre
> muros separativos de predios o de unidades de uso independiente, cualquier instalación o
> elemento que pudiera generar molestias al vecino, sean éstas producidas por golpes, choques,
> ruidos, vibraciones, calor, frío o humedad."*

→ **En una casa entre medianeras esto es el condicionante de planta número uno**, más que el FOS.
Una ventana perpendicular al eje divisorio (típica en un patio lateral angosto) necesita 0,50 m;
una ventana enfrentada al eje divisorio necesita 3,00 m o se convierte en paño fijo con antepecho
a 1,60 m. Es el motivo por el cual **el patio de 3,00 m de lado del art. 3.4.7 y los 3,00 m de
este artículo coinciden y hay que respetar la cifra sin excepción.**

### 4.12 ✅ Línea, nivel y cotas (arts. 3.1.1 y 3.1.2) — TRANSCRIPTO

> *"**Cota de Nivel Referencial -NR-:** Denomínase así el nivel más alto del cordón del pavimento
> existente o futuro al frente de la parcela.*
> ***Cota de Nivel del terreno -NT-:** El nivel del terreno de un predio **no puede ser inferior a
> la Cota de Nivel Referencial más el 3 % del ancho de la vereda** medido entre la Línea Municipal
> y el cordón del pavimento existente o futuro.*
> ***Cota de Nivel en Planta Baja -NPB-:** La cota de nivel de piso en locales ubicados en la
> planta baja de un edificio, **no podrá ser inferior a la Cota de Nivel Referencial más 0,10 m
> más el 3 % del ancho de la vereda**.*
> ***Cota de Nivel de Patios en Planta Baja -NP-:** La cota de nivel de los patios ubicados en
> planta baja, **no será inferior a la Cota de Nivel Referencial más 0,05 m más el 3 % del ancho
> de la vereda**."*

**Ejemplo resuelto (inferido del texto):** vereda de 2,00 m de ancho → 3 % = 0,06 m.
NT ≥ NR + 0,06 · NPB ≥ NR + 0,16 · NP ≥ NR + 0,11. **Son cotas mínimas absolutas: el piso
terminado de la casa nunca va al mismo nivel que el cordón.**

### 4.13 ✅ Cercos y veredas (arts. 3.2.1 y 3.2.2) — TRANSCRIPTO

> *"**Cercos de frente en predio baldío:** Todo propietario de un predio baldío está obligado a
> construir un cerco en el frente de su parcela […] con una **altura no inferior a 1,80 m**
> medidos desde el nivel del solado de la vereda. El cerco debe ser ejecutado con mampostería o
> piezas premoldeadas de cemento u hormigón […]*
> ***Cercos entre predios:** Los cercos que delimitan los predios entre sí, tendrán una **altura
> mínima de 1,80 m** medidos desde la Cota de Nivel del Terreno, ejecutados en mampostería o
> piezas premoldeadas de cemento u hormigón.*
> ***Acuerdo entre linderos:** Los propietarios de dos o más parcelas linderas podrán acordar la
> eliminación del cerco entre sus parcelas, la construcción del mismo con otros materiales […],
> la modificación de su altura o su reemplazo por un cerco vivo. El acuerdo deberá realizarse por
> escrito, debiendo cada uno de los firmantes poseer una copia."*
>
> **Veredas (texto dado por Ordenanza 3428/2006):** *"a- La superficie del solado será plana,
> antideslizante y sin excesiva rugosidad. […] d- Se dejarán juntas de dilatación tanto en el
> contrapiso como en el solado, ubicadas junto al cordón del pavimento, en los límites entre las
> propiedades y **cada 10,00 m del largo de vereda** […] f- La **pendiente en sentido transversal
> podrá variar entre 1 % y 3 %**. g- Deberán dejar libre los espacios necesarios para la
> plantación de árboles, con una **distancia no mayor de 5,00 m entre ellos, en cuadrados de
> 0,80 × 0,80 m en las veredas de más de 2,00 m de ancho, y de 0,60 × 0,60 m en las veredas cuyo
> ancho se encuentre entre 1,20 m y 2,00 m**. h- Las **rampas para entrada y salida de vehículos**
> no deberán generar desniveles que afecten a la comodidad y seguridad de los peatones, con un
> **desarrollo máximo de 1,40 m medidos desde el cordón del pavimento**, y el contrapiso será
> reforzado […] j- **No se permitirá la construcción de escalones**, en casos que no existiera
> otra solución posible, deberá gestionarse su expresa autorización ante la Municipalidad."*

**Y del Acta de Inicio de Obra municipal (transcripto):** *"El propietario, en conocimiento de la
existencia del cordón vereda, tiene como obligatoriedad la ejecución de la Acera Reglamentaria.
Se compromete a su ejecución, la cual contará con un **ancho mínimo de 1,40 m y 2 cazoletas para
arbolado permitido**, pendiente reglamentaria, y rampa vehicular sin obstaculizar el tránsito
peatonal, garantizando accesibilidad."*

**De "Elementos que componen el plano":** *"Si la finca no contase con vereda reglamentaria
materializada se deberá indicar (con línea continua), especificar (**y construir, condición
necesaria para el "alta de obra"**) una 'provisoria' cuyo **ancho mínimo es 1,20** y la
'Reglamentaria, según código de edificación' a construir, con línea de trazo."*

→ **La vereda no es un detalle: sin acera reglamentaria no hay alta de obra.**

### 4.14 ✅ Techos, desagües y azoteas (art. 4.9) — TRANSCRIPTO

> *"**Techo transitable:** Un techo transitable y/o de fácil acceso debe estar cercado con
> parapetos o baranda de una **altura mínima de 1,00 m** medida desde el solado […]. Si la azotea
> es utilizada como tendedero, el **parapeto será ciego y su altura no podrá ser inferior a
> 1,40 m**. **Cuando el parapeto se ubique sobre el eje medianero o a menos de 3,00 m de él, la
> altura mínima será de 1,60 m, debiendo ser completamente ciego.** Cuando el parapeto separe
> terrazas pertenecientes a dos unidades de uso independiente, tendrá una altura no inferior a
> 1,80 m medidos desde el solado más alto.*
> ***Desagües:** Las aguas pluviales que caen sobre los techos deben escurrir fácilmente hacia los
> desagües, quedando **prohibida su caída a la vía pública, los predios linderos, las otras
> unidades de uso independiente o sobre Muros Divisorios**."*

Y del art. 5.3.2: *"El agua de lluvia o la proveniente del lavado de pisos, tanto desde edificios
como desde terrenos, debe escurrir hacia la vía pública a través de canalizaciones, no pudiendo
en ningún caso caer libremente hacia la vía pública ni hacia predios linderos."*

### 4.15 ✅ Estructura y estudio de suelos (arts. 4.4 y 4.5) — TRANSCRIPTO

> *"**4.4.2. ESTUDIO DE SUELOS:** Cuando se ejecuten obras de **más de 3 pisos y/o de más de
> 10,00 m de altura y/o con sótanos de más de 3,00 m de profundidad**, será obligatoria la
> presentación ante la Municipalidad del estudio de suelos."*

→ **Una casa de una planta NO tiene obligación municipal de estudio de suelos.**
**Lectura del estudio (inferido):** en suelo loéssico pampeano eso es una exención administrativa,
no técnica. Encadenar la mampostería sigue siendo la mejor protección contra el asentamiento
diferencial (ver `docs/03-estructuras/estructuras.md`). La ausencia de exigencia municipal no es
un permiso para no hacerlo.

> *"**4.5.1. GENERALIDADES:** La estructura resistente no debe ejecutarse fuera de los límites del
> predio, a excepción del muro divisorio y su cimiento, el que puede asentarse en ambos predios
> linderos."*
> *"**4.5.2. MATERIALES PARA ESTRUCTURAS:** […] pueden utilizarse los siguientes materiales:
> albañilería de ladrillos, albañilería de piedra, sillería de piedra, hormigón simple, hormigón
> armado y acero estructural. **No está permitida, para la ejecución de estructuras resistentes, la
> utilización de materiales combustibles. La madera solo podrá ser utilizada en la ejecución de
> vigas y tirantería de techos**, siempre que la cubierta sea de materiales incombustibles y que la
> madera esté protegida contra la putrefacción. […] La utilización de otros materiales […] deberá
> ser expresamente aprobada por la Municipalidad."*
> *"**El cálculo de las estructuras resistentes debe formar parte de la documentación que se
> presenta ante la Municipalidad para solicitar el Permiso de Obra.**"*

⚠ **Atención al proyectar en madera.** El art. 4.5.2 limita la madera a vigas y tirantería de
techos. Una construcción de entramado de madera (*wood frame*) requiere **aprobación expresa de
la Municipalidad**, más el **Certificado de Aptitud Técnica (CAT)** que exige el CUA art. 4.3.1.4
para sistemas constructivos alternativos.

**Normas referenciales complementarias que el Código adopta (art. 1.1.5) — TRANSCRIPTO
(extracto):** reglamentos CIRSOC (101 cargas y sobrecargas, 102 acción del viento, y siguientes);
Reglamentación AEA para instalaciones eléctricas en inmuebles; *"Disposiciones sobre el tablero
para la protección de la alimentación y para la medición"* y *"Reglamentación para la derivación
a usuarios"*, ambas **editadas por la Cooperativa Popular de Electricidad de Santa Rosa Ltda.**;
normas de Gas del Estado para instalaciones domiciliarias de gas; Ley 19.587 y Decreto 351/79
Cap. 18 y Anexo VII para incendio.

### 4.16 ✅ Subdivisión de locales con tabiques (art. 3.7.1) — TRANSCRIPTO

> *"Un local puede ser subdividido en dos o más partes aisladas con tabiques, muebles o mamparas,
> si la **altura del elemento divisor no supera los 2,20 m** medidos desde el solado, y deja entre
> sí y el cielorraso una **abertura de altura no inferior a 0,40 m**, debiendo éste elemento ser
> traslúcido en caso que fuera necesario para conservar las condiciones mínimas de iluminación.
> Esta condición no será exigible en caso que cada una de las partes que resulten de tal
> subdivisión cumpliera con todas las condiciones de iluminación y ventilación exigidas por este
> Código."*

### 4.17 ✅ Zonas sin redes: cámara séptica y pozo negro (arts. 5.2.5, 5.3.3 a 5.3.5) — TRANSCRIPTO

> *"**5.2.5 ZONAS QUE CARECEN DE REDES:** Un predio, edificado o no, donde se habite, trabaje o
> realice alguna actividad, ubicado en una zona que carezca de redes de servicio de agua corriente
> y desagües cloacales, **debe contar con instalación sanitaria con perforación para captación de
> agua potable, y desagüe a cámara séptica y pozo negro**. Queda prohibido lanzar a la vía pública
> o a otros predios los líquidos cloacales y las aguas servidas."*
>
> *"**5.3.3 PERFORACION PARA LA CAPTACION DE AGUA:** La perforación […] debe **distar no menos de
> 1,00 m del Eje Divisorio** entre predios, y debe tener la profundidad adecuada para extraer agua
> que sea potable."*
>
> *"**5.3.4 CAMARAS SEPTICAS:** Una cámara séptica **debe constar de por lo menos dos secciones
> iguales**, para que no se interrumpa su funcionamiento durante la reparación o limpieza de una de
> ellas. La capacidad se determinará en función del caudal de desagüe diario, según las siguientes
> relaciones:*
> | Cantidad de personas | Capacidad de cada sección |
> |---|---|
> | Hasta 10 | **200 litros/persona** |
> | Más de 10 y hasta 50 | 175 litros/persona |
> | Más de 50 | 150 litros/persona |
>
> *Estos valores determinan la capacidad de cada sección de cámaras sépticas que sirven a edificios
> destinados a viviendas. Para otros usos, la capacidad mínima exigida será la mitad de la
> requerida para vivienda. **En ningún caso, cada sección de una cámara séptica tendrá una
> capacidad inferior a 1000 litros.** La cámara llevará interiormente revoque impermeable que
> impida la filtración de líquidos al exterior. **La ventilación de la cámara se realizará por un
> conducto de diámetro no inferior a 0,10 m** […]"*
>
> *"**5.3.5 POZOS NEGROS:** Un pozo negro debe ubicarse a una **distancia no inferior a 1,50 m del
> Eje Divisorio** entre predios, y a **20,00 m de una perforación para la captación de agua**. Si
> por las dimensiones de la parcela, esta última distancia fuera imposible de cumplir, el pozo
> negro y la perforación para captación de agua deben ubicarse en los extremos opuestos del predio,
> pero **nunca podrán distar entre sí menos de 10,00 m**. La profundidad del pozo debe asegurar que
> no se ha de contaminar la napa de la cual se extrae el agua. El pozo debe contar en su parte
> superior con una **bóveda o cierre de albañilería de 0,30 m o de hormigón armado de 0,10 m de
> espesor**. El conducto de descarga al interior del pozo terminará con un codo a 90° ubicado en el
> centro del pozo y con la boca hacia abajo. […] **No se permite la ejecución de pozos negros en
> las zonas de la ciudad que cuentan con redes de desagües cloacales.**"*

**Cálculo resuelto (inferido):** vivienda para 5 personas → 5 × 200 = 1.000 litros por sección,
que además es el mínimo absoluto. **Cámara séptica de 2 secciones de 1.000 L cada una = 2.000 L
totales.** En un lote de 12 m de frente, la exigencia de 20 m entre pozo negro y perforación
obliga casi siempre a la excepción: perforación al frente y pozo al fondo, **nunca a menos de
10 m entre sí**.

---

## 5. Trámite municipal, paso a paso

Fuente: **Manual de Procedimientos de la Dirección de Planeamiento Urbano y Obras Particulares**
(Anexo I de la Disposición del Secretario de Obras y Servicios Públicos, **vigente desde el
01/03/2026**), Código de Edificación arts. 2.1.1 a 2.1.12, Disposición 131/2025, y los
formularios municipales publicados.

> ⚠ **El número de la Disposición que aprueba el Manual no se lee con certeza en la copia
> escaneada.** El CPITLP publica el archivo bajo el nombre *"DISPOSICIÓN N° 16 APROBANDO MANUAL DE
> PROCEDIMIENTOS ADMINISTRATIVOS DE LA DIRECCIÓN DE PLANEAMIENTO URBANO"*.
> **[VERIFICAR el número exacto en la Dirección de Planeamiento Urbano y Obras Particulares.]**

**Cambio de fondo respecto de años anteriores, transcripto del Manual:**

> *"Los trámites serán recepcionados **únicamente de manera digital**, a través de la plataforma
> existente en la página web oficial de la Municipalidad de Santa Rosa: www.santarosa.gob.ar."*

→ **Ya no se presentan copias en papel ni se cuentan juegos de planos.** La pregunta "cuántas
copias" dejó de tener respuesta: **se sube documentación digital y el municipio firma
digitalmente el plano.** **[VERIFICAR el formato exacto de archivo, tamaño y nomenclatura que
acepta la plataforma — Dirección de Planeamiento Urbano.]**

Y el **croquis de ubicación ya no se emite**, transcripto:

> *"El trámite de solicitud de croquis de ubicación **no se expedirá más**, en virtud que la
> información respecto de los ángulos y las distancias de las parcelas a las esquinas se
> encontrará disponible y accesible desde **portal ciudadano** al que se ingresa desde la página
> web de la Municipalidad de Santa Rosa, en **"Trámites On Line"**."*

### 5.0 Paso 0 — Datos de la parcela (antes de dibujar)

| Qué | Dónde | Quién | Para qué |
|---|---|---|---|
| Ángulos, distancias a esquina y datos catastrales de la parcela | **Portal Ciudadano / "Trámites On Line"**, `santarosa.gob.ar` | El profesional | Reemplaza al croquis de ubicación |
| **Distrito** del lote | Plano P1 del CUA (`fuentes/plano-P1-zonificacion-distritos.pdf`) + confirmación en Planeamiento | El profesional | FOS, retiros, altura, densidad, CAS |
| ¿Es frentista a **corredor comercial**? | Plano P2 (`fuentes/plano-P2-corredores-comerciales.pdf`) | El profesional | Cambia los indicadores |
| ¿Cae en **zona de influencia del aeropuerto**? | Plano P4 del CUA | El profesional | Altura máxima admisible; trámite ante ANAC si corresponde |
| **Libre de deuda catastral** | Plataforma digital `santarosa.gob.ar`, adjuntando el plano | Propietario / profesional | Acredita ausencia de deudas (tasas, derechos de construcción, multas). Se deriva a inspección, liquidación y notificación |
| **Factibilidad** (OPTATIVO pero recomendado) | Plataforma digital | El profesional | *"trámite optativo por el cual se solicita el análisis de viabilidad de una obra a realizarse, de acuerdo al código urbano ambiental y el código de edificación"*. Se presenta la propuesta *"con la mayor cantidad de información técnica posible (ejemplo renders)"*; el municipio emite **acto administrativo aprobando o rechazando el proyecto** |

> **Lectura del estudio (inferido):** la Factibilidad es la herramienta correcta para blindar
> cualquier interpretación dudosa (cocina integrada, cochera, R3VII, sistema constructivo
> alternativo) **antes** de desarrollar el ejecutivo. Es optativa y probablemente gratuita, pero
> devuelve un acto administrativo. Vale el tiempo.

### 5.1 Paso 1 — Visado previo del Colegio profesional

**Es obligatorio y es previo al municipio.** Transcripto del Código de Edificación art. 2.1.2
(texto según Ordenanza 6445/2020):

> *"Previo a la ejecución de cualquier tarea comprendida por este Código, que requiera Permiso de
> Obra, deberá efectuarse la correspondiente tramitación ante la Municipalidad con: **Planos
> debidamente intervenidos por los Colegios y Consejos de Profesionales cumplimentando con el
> visado Previo**, no pudiendo dar inicio a los trabajos hasta tanto: - Se haya finalizado el
> trámite y autorizado los planos de obra. - Abonando los derechos municipales que en cada caso
> correspondieran. - Suscripto el acta de inicio de obra, con la firma del Propietario, el Director
> Técnico de la obra, con el visado correspondiente de los Colegios o Consejos Profesionales y
> Declaraciones Juradas de los profesionales o las inspecciones municipales que correspondan."*

Y art. 2.2.3: *"El proyecto, la dirección y la ejecución de tareas que, según este Código,
requieran Permiso de Obra, estarán a cargo de un profesional matriculado en el Consejo Profesional
de Ingeniería y Arquitectura de la Provincia de La Pampa, supeditado a las categorías,
incumbencias y alcances que dicho Consejo determina para cada título profesional."*

> **Nota de vigencia:** el texto de 1995 nombra al *"Consejo Profesional de Ingeniería y
> Arquitectura de la Provincia de La Pampa"*, entidad que hoy está desdoblada en el
> **CALP (Colegio de Arquitectos de La Pampa, Ley provincial 2.878)** y el **CPITLP (Colegio
> Profesional de la Ingeniería y la Técnica de La Pampa)**. La Ordenanza 6445/2020 actualiza la
> redacción a *"los Colegios y Consejos de Profesionales"*, en plural.
> → **Un arquitecto visa en el CALP.**

**Dónde y cómo (CALP):**

| Dato | Valor |
|---|---|
| Sede Santa Rosa | **Don Bosco 243, Santa Rosa** — lunes a viernes de 8 a 13 h |
| Teléfono / WhatsApp Santa Rosa | **2954-412858** · Área Técnica (02954) 271045 · Adm. Contable (02954) 271011 |
| Mail Área Técnica | `tecnica@colegioarqlapampa.org.ar` |
| Plataforma de visado | **MiCALP** — `micalp.colegioarqlapampa.org.ar` |
| Marco legal | Ley provincial **2.878** (creación del CALP) y Ley provincial **2.881** (Visado Previo y Aportes por Tareas Profesionales de Arquitectos) |
| Documentación de visado | **Orden de Trabajo / Contrato** firmada por propietario y profesional (PDF descargable del sitio), planimetría con el rol del profesional declarado en la carátula (Proyecto / Dirección de Obra / etc.), planilla de liquidación de gastos y comprobante de aporte a la Caja de Previsión |
| Base de cálculo de aportes | Valor de referencia del costo unitario de construcción (\$/m²) **para una vivienda unifamiliar tipo**, fijado por Resolución del Directorio y actualizado como máximo cada 2 meses por variación del índice CAMARCO y del IPC Nivel General del INDEC (Resoluciones 03/2016, 10/2023 y 22/2023) |
| **Importe vigente del valor de referencia y del aporte** | **[VERIFICAR en el CALP, Área Contable (02954) 271011 o `adm@colegioarqlapampa.org.ar`]** — la Resolución vigente no se pudo obtener |

**Instaladores:** el acta de inicio municipal exige declarar los **instaladores intervinientes**
(nombre, tarea, teléfono, firma). Las instalaciones de gas, eléctricas y sanitarias las visa el
**CPITLP** cuando las firma un instalador matriculado allí
(Urquiza 564, Santa Rosa · (02954) 42-9781 · `santarosa@cpitlp.org.ar`).
El CALP publica además un **Certificado de Ejecución de Instalaciones Eléctricas en Inmuebles**.

### 5.2 Paso 2 — Permiso de Obra (P.O.)

**Cuándo corresponde (Código de Edificación art. 2.1.1) — TRANSCRIPTO:**

> *"Se deberá solicitar **Permiso de Obra** cuando se realicen las siguientes tareas: - **Construir
> nuevos edificios.** - Ampliar, refaccionar o transformar los ya construidos. - Cerrar, abrir o
> modificar vanos en la fachada principal. - Cambiar o modificar estructuras de techos. -
> **Desmontar y excavar terrenos.** - Efectuar demoliciones. - Efectuar instalaciones mecánicas,
> eléctricas, térmicas y de inflamables […] - Instalar carteles […] - Instalar marquesinas […] -
> Construir en el Cementerio […]. Todas estas tareas requieren la intervención de un profesional
> matriculado […]"*

**Cómo se hace (Manual de Procedimientos) — TRANSCRIPTO:**

> *"Se entiende para la administración municipal por permiso de obra, en adelante P.O., a la
> autorización que se requiere, previo al inicio de cualquier tipo de obra o construcción. Los
> trámites serán recepcionados **únicamente de manera digital** […]. El P.O. se solicitará, **con
> el plano visado por el colegio y/o consejo profesional correspondiente, debiendo acreditarse la
> titularidad o posesión legítima del inmueble**. En aquellos casos que el proyecto no cumpla con
> alguna normativa deberá adjuntarse **nota y memoria descriptiva del profesional**, por la cual
> justifique que se encuentran dentro de los límites técnicos de flexibilidad. Ingresado el P.O.,
> el trámite se derivará para su liquidación de acuerdo a los datos presentados por el profesional
> y posteriormente se dictará el acto administrativo correspondiente, notificándose al interesado
> al domicilio electrónico constituido."*

**El Manual incluye un MODELO DE NOTA DE JUSTIFICACIÓN TÉCNICA** (Anexo I) para el caso de
apartamientos menores de la norma, que declara bajo juramento que la desviación:
*"1. No afecta derechos de terceros ni genera perjuicio a linderos. 2. No compromete condiciones
de seguridad, salubridad ni habitabilidad. 3. No altera sustancialmente la morfología urbana ni el
carácter del sector. 4. Se mantiene dentro de parámetros razonables y proporcionados en relación
con la superficie total del proyecto."* → **Copiar el modelo del PDF guardado en `fuentes/`.**

**Derechos de Construcción (art. 2.1.5) — TRANSCRIPTO:**

> *"Por la realización de cada tarea que, según el presente Código, requiera Permiso de Obra,
> deberán abonarse los Derechos de Construcción que establezca en cada caso la **Ordenanza
> Fiscal**. Es condición indispensable, para obtener el Permiso de Obra, **abonar con anterioridad
> los Derechos de Construcción**."*

**[VERIFICAR el importe en la Ordenanza Fiscal/Tarifaria vigente — Dirección de Rentas o
Planeamiento Urbano y Obras Particulares.]** No hay ningún valor publicado accesible.

**Validez del Permiso (art. 2.1.10, texto según Ordenanza 6445/2020) — TRANSCRIPTO:**

> *"Transcurridos **tres años** desde el otorgamiento de un permiso de obra, sin que los trabajos
> de ejecución hayan dado comienzo, **o no se superara el cinco por ciento de avance de obra**, el
> permiso deberá ratificarse adaptando el proyecto a las normas vigentes al momento de su
> ratificación, abonando los derechos de aprobación y construcción si correspondiere. Transcurridos
> tres años desde el otorgamiento de un permiso de obra, y sin que los trabajos de ejecución hayan
> dado comienzo, **el permiso y los derechos caducarán automáticamente perdiendo toda validez**."*

> ⚠ **Contradicción interna del propio artículo:** el primer párrafo dice que a los tres años
> "deberá ratificarse" y el segundo, con el mismo plazo de tres años, dice que "caducará
> automáticamente". El texto anterior a la 6445/2020 tenía 3 años para ratificar y **5** para
> caducar. **[VERIFICAR la lectura oficial en Obras Particulares.]** Criterio prudente: tratar el
> permiso como **caduco a los 3 años sin inicio**.

### 5.3 Paso 3 — Acta de Inicio de Obra

Formulario municipal (`fuentes/acta-inicio-de-obra-santa-rosa.pdf`), firmado por **propietario y
Director Técnico**, en carácter de **Declaración Jurada**. Contenido:

- Datos de propietario y profesional, **matrícula municipal**, y **domicilio especial electrónico**
  constituido bajo el art. 75 del Código Civil y Comercial;
- designación expresa del **Director/a Técnico/a**;
- declaración del estado de la obra: *A) no tuvo principio de ejecución · B) avance ≤ 10 % ·
  C) avance de …% · D) la parcela cuenta con cordón cuneta SÍ/NO*;
- **listado de instaladores intervinientes** (nombre, tarea, teléfono, firma);
- compromiso de ejecutar la **acera reglamentaria** (ancho mínimo 1,40 m, 2 cazoletas de arbolado,
  pendiente reglamentaria, rampa vehicular accesible);
- advertencia: *"Cualquier modificación del proyecto previa o durante su ejecución deberá ser
  informada, aprobada y autorizada por la autoridad municipal competente, caso contrario serán
  susceptibles de las multas correspondientes."*

### 5.4 Qué debe contener el plano — "Elementos que componen el plano municipal" (TRANSCRIPTO)

Documento municipal completo en `fuentes/elementos-que-componen-el-plano-municipal.pdf`. Resumen
de las láminas exigidas:

| # | Lámina | Escala | Contenido exigido (extracto literal) |
|---|---|---|---|
| 1 | **Plantas de arquitectura** | 1:100 | *"Cada piso con cotas interiores de locales y patios, espesores de muros y tabiques; niveles, designación (destino/uso) y numeración. Carpinterías correctamente indicadas. Mobiliario fijo: artefactos de baño, cocina y lavadero, mesadas y placares. Vacíos. Barandas. Conductos y plenos de ventilación y su sección. […] Aleros y proyecciones de plantas superiores (en línea de trazo). Indicar desniveles, rampas y escaleras. **Espacio estacionamiento auto.** […] En exterior: indicar cercos, cotas parciales y totales exteriores de la construcción, **retiros y distancia a cercos**. Barrido/aperturas de puertas y portones. Límite de solado, **terreno absorbente**. **Pozo negro o absorbente y bomba, si no contase con agua de red y de cloaca.** Cotas y ángulos del terreno. Ejes Divisorios y Línea Municipal […]. Gabinete de instalaciones (gas, electricidad, agua, etc.). Ubicación de pozo absorbente y perforación. **Vereda:** elementos (rampas, alarmas, marquesinas, bordes de solados, canteros, vegetación), cotas y niveles **tomando el lomo del Cordón Cuneta como nivel ±0,00 m**"* |
| 2 | **Esquema/s de estructura** | 1:100 | *"Distribución de la estructura y cada una de sus partes con sus correspondientes denominaciones (base, columnas, vigas, **encadenados**, losas, conductos de ventilación y sus secciones, sentido de la pendiente del techo). Tanque de reserva y su base de apoyo, canaletas."* |
| 3 | **Cortes** | 1:100 | *"**Dos como mínimo, uno longitudinal y otro transversal**, mostrando el total del proyecto, incluyendo Cordón Cuneta y límites de terreno. Altura libre locales, espesores losas, cielorrasos, contrapisos, profundidad de cimientos y sus dimensiones. Niveles, materiales, cercos, aberturas y su apertura y mano."* |
| 4 | **Frente (fachada)** | 1:100 | *"Descripción real de los materiales dando una idea exacta de su construcción […], cotas alturas, niveles referenciados al C.C. Aberturas y su apertura y mano."* |
| 5 | **Cerco Línea Municipal** | 1:100 | *"Dibujar cerco L.M. y postes, verjas, rampas y todos los elementos con sus alturas y especificando materiales, aperturas. Niveles y alturas."* |
| 6 | **Detalle escalera** | 1:50 (corte 1:20) | *"Planta de escaleras, su desarrollo, línea de huella con sentido de ascenso, numeración de escalones, niveles, cotas, proyecciones, barandas (acotar hueco de escalera). Corte de tres escalones (mínimamente), indicando alzada, huella, nariz, baranda y materiales."* |
| 7 | **Detalle canaleta desagüe** | 1:20 | *"Detalle canaletas desagües sobre L.M. y E.D. indicando claramente su construcción."* |
| 8 | **Detalle encadenado** | 1:20 | *"Indicando sección H° y hierro."* |
| 9 | **Planillas de estructura** | — | *"Planillas reglamentarias de estructura (base, columnas, vigas, losas) y losas prefabricadas según marca."* |
| 10 | **Planillas de iluminación y ventilación** | — | ⚠ requiere los cuadros 3.4.5.1 y 3.4.5.2 que **no se consiguieron** |
| 11 | **Silueta (polígonos) de superficies y cuadro de superficies** | — | *"Polígonos acotados claramente, numerados, con rayados reglamentarios. En cuadro discriminar superficies según sean 'con permiso', 'a construir', …; y cubierta o semicubierta."* |

**Notas obligatorias en el plano (transcriptas):**

> *"**'LA FINCA CUENTA (o NO) CON LOS SERVICIOS DE PROVISIÓN DE AGUA CORRIENTE Y CLOACA'.**"*
> *"EN CARÁTULA. PLANO DE: además del tipo de plano (ej: 'OBRA NUEVA') se deberá especificar si es
> plano de arquitectura, electricidad, estructura… y numerado, si fuere más de uno."*
> *"**SUPERFICIES.** Especificar al final del resto, como 'SUPERFICIE TOTAL AL 100 %', el total de
> las superficies y proyecciones de todas las plantas **y aleros** sobre el suelo, computadas al
> 100 %, necesarias para el cálculo del FOS."*
> *"La municipalidad se reserva el derecho de exigir detalles, plantas, cortes, vistas y planillas
> según lo requiera el proyecto, para su mejor interpretación."*

**Croquis de instalaciones sanitarias (Disposición 131/2025, art. 2) — TRANSCRIPTO:**

> *"Los interesados y/o profesionales que tramiten proyectos de obras particulares deberán incluir
> al tiempo de la presentación de los planos de construcción […] **un croquis de instalaciones
> sanitarias**, con la siguiente información para su aprobación:*
> ***A) Servicios de Agua Potable:** Tanque elevado y cisterna (ubicación y capacidad). Ubicación
> de conexión de agua, incorporando caja de medición, línea principal interna y distancia a ejes
> medianeros.*
> ***B) Servicios de Desagües Cloacales:** Cámara de inspección, boca de acceso o de inspección que
> permita efectuar la limpieza y desobstrucción en caso de ser necesario. Distancia a ejes
> medianeros de conexión cloacal y tapada (cuando exista conexión a red). Distancia a ejes
> medianeros de pozo absorbente (cuando exista).*
> ***C) Servicios de Desagües Pluviales:** Ubicación de cámara de inspección, boca de acceso o de
> inspección que permita efectuar la limpieza y desobstrucción en caso de ser necesario."*

Y el art. 3 de la misma Disposición: **el plano sanitario específico solo se exige** en edificios
>500 m², viviendas multifamiliares de más de 6 unidades, y una lista de usos especiales
(hospitales, laboratorios, carnicerías, lavaderos, estaciones de servicio, panaderías,
restaurantes, hoteles, soderías, industrias, edificios públicos, establecimientos educativos y
dependencias de fuerzas de seguridad). → **Una vivienda unifamiliar NO presenta plano sanitario
específico: alcanza con el croquis en el plano de arquitectura.**

**Carátula:** usar la carátula municipal oficial (`fuentes/caratula-municipal-santa-rosa.pdf`; el
CPITLP publica también el DWG).

### 5.5 Paso 4 — Policía de obra e inspecciones

**Transcripto del Código de Edificación:**

> *"**2.3.3. DOCUMENTACION EN LA OBRA:** Es obligatorio tener permanentemente en obra […] **una
> copia del Plano Municipal aprobado, el Permiso de Obra otorgado** y/o constancia del Aviso de
> Obra presentado."*
> *"**2.3.4. PRESENCIA DEL PROFESIONAL EN OBRA:** **Es obligatoria la presencia del profesional
> responsable de una obra durante las tareas de hormigonado.** La Inspección Municipal podrá citar
> al Profesional en la obra, mediante notificación cursada en forma, conviniendo día y hora con una
> **anticipación no menor de tres días hábiles**. Un Profesional puede solicitar por escrito la
> presencia de la Inspección Municipal en una obra a su cargo […]"*
> *"**4.1.6. CARTEL DE OBRA:** En toda obra comprendida por este Código, **es obligatorio colocar al
> frente un cartel** conteniendo como mínimo la siguiente información: Nombre, Apellido, Título,
> Matrícula y Domicilio del/los profesional/es responsables de la misma con indicación de la tarea
> que realizan cada uno de ellos, **número de Permiso de Obra y fecha de su otorgamiento**."*

**Inspecciones en obra (Manual de Procedimientos, Capítulo VI — TRÁMITES ESPECIALES):**

> *"Se considerarán **trámites especiales aquellos que tengan una superficie de más de 300 m²**.
> Los que deberán tener especificadas las etapas del proyecto. En esos casos, al ingresar el
> trámite se derivará a la Secretaría de Gobierno para su toma de conocimiento. En el caso de que
> el trámite especial sea por un P.O., una vez otorgado el mismo, se realizará un **doble control,
> con una inspección en la etapa de fundación/capa aisladora y otra inspección posterior al
> finalizar la estructura**. En caso de detectar incumplimientos se determinará la sanción a
> aplicar pudiendo ser la multa, paralización de la obra, adecuación o demolición […]"*

→ **Lectura del estudio (inferido):** una vivienda unifamiliar de menos de 300 m² **no** cae en
"trámite especial" y, por lo tanto, **no tiene el régimen de doble inspección obligatoria**;
la inspección llega en el Final de Obra. Por encima de 300 m² sí, y además el expediente pasa por
Secretaría de Gobierno. **Es un umbral de diseño a tener presente al cerrar el programa.**

**Obras paralizadas (art. 2.1.7) — TRANSCRIPTO:** *"Una obra se considerará paralizada cuando no
se ejecuten trabajos constructivos y/o de instalaciones durante **cuatro meses consecutivos**.
Antes de cumplirse dicho plazo, el Propietario y el Profesional están obligados a comunicar dicha
circunstancia a la Municipalidad […]"* — y la reanudación después de **3 años** obliga a verificar
el proyecto contra las normas vigentes al momento de reanudar.

**Cambio de profesional (art. 2.2.5) — TRANSCRIPTO:** *"En ambos casos, la obra deberá ser
inmediatamente paralizada hasta la designación de un nuevo Profesional. El profesional es
responsable de la obra hasta el día en que él o el Propietario comuniquen oficialmente a la
Municipalidad su desligamiento."*

### 5.6 Paso 5 — Final de Obra / Alta de Obra

**Transcripto del Código de Edificación art. 2.1.9 (texto según Ordenanza 6445/2020):**

> *"Todo profesional responsable de una obra, al terminar la misma, **está obligado a tramitar el
> Final de Obra**, el que será presentado ante la Municipalidad **dentro de los sesenta días
> corridos de la finalización de los trabajos**. El Municipio podrá otorgar **altas parciales o
> totales** y la habilitación del inmueble."*

**Transcripto del Manual de Procedimientos:**

> *"**V.d) FINAL DE OBRA/ALTA DE OBRA:** se entiende por final de obra y/o alta de obra al acto
> administrativo que declara por finalizado el P.O. autorizado. **Trámite:** será recepcionado
> únicamente de manera digital […] **adjuntando el plano visado correspondiente**. Previo al dictado
> del acto administrativo, **la Dirección de Obras realizará la inspección correspondiente**. Se
> liquidarán los derechos y multas de corresponder. **Se firmará digitalmente el plano** y se
> notificará el acto administrativo dictado al efecto. […] En caso que existan diferencias y se
> encuentren en contravención a la normativa vigente, se evaluará la envergadura del incumplimiento
> y si afecta a la estructura de la edificación o a terceros, aplicando las sanciones
> correspondientes (multa, adecuación o demolición)."*

Y del Acta de Inicio: *"Se podrá solicitar el final de obra / parcial o total si se garantizan las
condiciones mínimas de habitabilidad."*

**Condición previa (de "Elementos que componen el plano"):** ejecutar la **vereda** —
reglamentaria, o provisoria de 1,20 m de ancho mínimo — *"condición necesaria para el 'alta de
obra'"*.

### 5.7 Paso 6 — Plano Conforme a Obra (regularización)

**Transcripto del Manual:**

> *"**V.e) PLANO CONFORME A OBRA:** Se entiende por Plano Conforme a obra, la presentación efectuada
> por la cual se pretende **regularizar una construcción sin P.O.** Trámite: será recepcionado
> únicamente de manera digital […] adjuntando el plano visado correspondiente. Iniciado el trámite,
> la Dirección de Obras realizará una inspección. Se liquidarán los derechos y multas de
> corresponder. Se firmará digitalmente el plano y se notificará el acto administrativo […]"*

**Clasificación de obras (Código de Edificación art. 2.1.12, incorporado por Ord. 6445/2020) —
TRANSCRIPTO:**

> *"a) **Obra Clase A:** son aquellas obras mayoritariamente autorizadas de acuerdo a la normativa
> vigente, previas a su ejecución. Designadas como Construcción Clase A - Autorizada.*
> *b) **Obra Clase B:** son aquellas mayoritariamente ejecutadas sin autorización municipal,
> aceptadas para regularizar el catastro, encuadradas a la normativa vigente. Designadas como
> Construcción Clase B - Conformada.*
> *c) **Obra Clase C:** son aquellas mayoritariamente proyectadas y ejecutadas sin autorización
> municipal en contraposición a la normativa vigente, que para ser aceptada su regularización debe
> ejecutarse la adecuación parcial o total a la normativa vigente. Designadas como Construcción
> Clase C - Conformada con adecuación.*
> *d) **Obras Clase D:** son aquellas mayoritariamente ejecutadas sin autorización municipal, en
> contraposición a la normativa vigente, con discrepancias menores que pueden aceptarse
> condicionalmente, y que de constatarse perjuicios a terceros, se deberá proceder a su adecuación.
> Designadas como Construcciones Clase D - Conformada - Aceptada condicionalmente.*
> *Podrá modificarse su clase y el municipio certificarlo cuando modificaciones o nuevas
> construcciones la encuadren mayoritariamente en la clase correspondiente."*

### 5.8 Otros trámites del catálogo (Manual, Capítulo V)

| Trámite | Cuándo se usa | Plataforma |
|---|---|---|
| **Aviso de Obra** | Terraplenar/rellenar terrenos · cercar el frente · ejecutar aceras y refaccionar cordones · refaccionar, revocar, pintar o limpiar fachadas cuando se requieran estructuras · instalar toldos sobre veredas · cualquier obra que requiera ocupación temporal del espacio público. **Autorización automática si el municipio no objeta en 10 días hábiles.** *"Todas las acciones no enumeradas aquí requieren permiso de obra."* | `santarosa.gob.ar` |
| **Uso de Suelo y Aptitud Técnica** | Viabilidad de una **actividad comercial** en un inmueble. Se adjunta el último plano aprobado conforme a obra | **`munidigital.com/citizenv2/santarosalapampa/login`** (plataforma distinta) |
| **Cambio de titularidad** | Registrar nuevo titular. Se adjunta libre de deuda + escritura | `santarosa.gob.ar` |
| **Mensuras** | Plano de mensura **visado por el Consejo Profesional**. Los loteos de más de una manzana se presentan **presencialmente** en la mesa de entradas de la Dirección | `santarosa.gob.ar` / presencial |
| **Duplicado de plano** | Abonando la tasa correspondiente | `santarosa.gob.ar` |

### 5.9 Resumen del circuito, en orden

```
0. Portal Ciudadano: datos de parcela  →  Plano P1 (distrito) + P2 (corredor) + P4 (aeropuerto)
1. [opcional pero recomendado] FACTIBILIDAD  →  acto administrativo aprobando/rechazando el proyecto
2. Libre de deuda catastral (digital, con plano)
3. Orden de Trabajo + documentación  →  VISADO PREVIO en CALP (MiCALP) + aportes Caja de Previsión
4. PERMISO DE OBRA (digital, con plano visado + acreditación de titularidad)
       └─ liquidación de Derechos de Construcción  →  PAGO  →  acto administrativo
5. ACTA DE INICIO DE OBRA (propietario + Director Técnico + instaladores, DDJJ)
6. Cartel de obra al frente + copia del plano aprobado y del Permiso en obra
7. Ejecución. Presencia obligatoria del profesional en los hormigonados.
       └─ si la obra supera 300 m²: doble inspección (fundación/capa aisladora y fin de estructura)
8. Ejecución de la VEREDA (reglamentaria o provisoria de 1,20 m) — condición para el alta
9. FINAL DE OBRA / ALTA DE OBRA (digital, plano visado)  →  inspección  →  firma digital del plano
       └─ plazo: dentro de los 60 días corridos de terminada la obra
```

---

## 6. Servicios: agua, cloaca, electricidad, gas

### 6.1 Agua potable y cloaca — los presta **la propia Municipalidad**

**Transcripto de los considerandos de la Disposición 131/2025:**

> *"Que, por Ordenanza N.º 6278/2019 se ratificó lo actuado por la Municipalidad de Santa Rosa en
> cuanto al Convenio suscripto con fecha 1º de agosto de 1980 con el Ministerio de Obras Públicas
> de la Provincia de La Pampa, por el cual se transfieren al Municipio los servicios de provisión de
> agua potable y desagües cloacales ubicados dentro del ejido municipal, **siendo la Municipalidad
> quien administra, opera y mantiene los sistemas de agua potable y desagües cloacales de la
> ciudad**."*

→ **En Santa Rosa NO hay cooperativa ni empresa provincial de agua: es el municipio.** El área es
la **Dirección de Agua y Saneamiento / Dirección de Saneamiento Urbano**, dependiente de la
Secretaría de Obras y Servicios Públicos.

| Qué | Cómo |
|---|---|
| Declarar el estado de servicios | **Nota obligatoria en el plano:** *"LA FINCA CUENTA (o NO) CON LOS SERVICIOS DE PROVISIÓN DE AGUA CORRIENTE Y CLOACA"* |
| Croquis sanitario en el plano | Obligatorio según Disposición 131/2025 art. 2 (ver §5.4) |
| Plano sanitario específico | **No se exige** en vivienda unifamiliar (solo >500 m², multifamiliares >6 unidades y usos especiales) |
| **Solicitud de conexión de agua y/o cloaca** | **[VERIFICAR el circuito exacto, requisitos y costo en la Dirección de Agua y Saneamiento, Municipalidad de Santa Rosa.]** Preguntar concretamente: ¿se pide junto con el Permiso de Obra o después? ¿es un trámite digital de `santarosa.gob.ar`? ¿quién ejecuta la conexión a la red y quién la paga? ¿hay derecho de conexión por diámetro? |

### 6.2 Zonas sin cloaca

Se aplica el Código de Edificación art. 5.2.5 + 5.3.4 + 5.3.5, transcripto íntegro en §4.17:
**perforación para captación de agua potable + cámara séptica de dos secciones + pozo negro**, con
las distancias de 1,00 m (perforación al eje divisorio), 1,50 m (pozo negro al eje divisorio) y
20,00 m entre pozo y perforación (10,00 m como mínimo absoluto si la parcela no lo permite).

**El CUA agrega, para R5 y R6 (transcripto):** *"Los conjuntos de vivienda que no cuenten con
servicios de agua potable de red pública deberán resolver el servicio en forma colectiva mediante
sistemas alternativos no individuales. El servicio de cloaca se podrá resolver individualmente
mediante **sistema séptico o biodigestores**."*

**Administración Provincial del Agua (APA) / Secretaría de Recursos Hídricos.** El propio CUA
remite, para la extracción de agua, al *"Código de Aguas de la Provincia de La Pampa, **Ley
Provincial N.º 2581** y su **Decreto Reglamentario N.º 2468/2011** y **Resolución N.º 11/2013** de
la Secretaría de Recursos Hídricos de la Provincia"*.

→ **Lectura del estudio (inferido, a confirmar):** una perforación domiciliaria para uso doméstico
del propietario en una vivienda unifamiliar suele estar exceptuada del permiso de explotación, pero
**la excepción y sus condiciones las fija la reglamentación**.
**[VERIFICAR en la Administración Provincial del Agua — Villegas 194, Santa Rosa]** si una
perforación domiciliaria de vivienda unifamiliar requiere permiso, registro del perforador ante el
Registro de Consultores y Perforistas, y/o presentación de estudio hidrogeológico.

### 6.3 Electricidad — **Cooperativa Popular de Electricidad (CPE) de Santa Rosa Ltda.**

Confirmado por el propio Código de Edificación, que adopta como normas referenciales
complementarias (art. 1.1.5) *"Disposiciones sobre el tablero para la protección de la
alimentación y para la medición, editado por la **Cooperativa Popular de Electricidad, Obras y
Otros Servicios Públicos de Santa Rosa Ltda.**"* y *"Reglamentación para la derivación a usuarios,
editados por la Cooperativa Popular de Electricidad […]"*.

| Dato | Valor |
|---|---|
| Distribuidora | **CPE — Cooperativa Popular de Electricidad, Obras y Servicios Públicos de Santa Rosa Ltda.** (fundada 1930; distribución domiciliaria y alumbrado público en Santa Rosa y Toay) |
| Sitio | `cpe.coop.ar` — sección **"Solicitud de factibilidad"**, con formularios diferenciados para conexión estándar, loteos y rurales |
| Oficina | Raúl B. Díaz 218, Santa Rosa |
| Teléfono Energía | 412222 |
| Reglamento aplicable a la instalación interna | **AEA — Reglamentación para la Ejecución de Instalaciones Eléctricas en Inmuebles** (el Código de Edificación la adopta expresamente) |
| Certificado | **Certificado de Ejecución de Instalaciones Eléctricas en Inmuebles**, formularios publicados por CALP y por CPITLP |
| Local para medidores (CE 5.8.4.1, texto Ord. 3667/2007) | *"Debe contar con un fácil acceso, no contener instalaciones de gas ni comunicarse con locales que los contengan, debiendo **cumplir con las disposiciones del concesionario del Servicio Eléctrico**."* |

**[VERIFICAR en la CPE]** el circuito y el costo del **derecho de conexión / factibilidad** para una
vivienda nueva, y si exige el certificado de instalación firmado por profesional matriculado antes
de dar el suministro definitivo.

### 6.4 Gas natural

Distribuidora en toda la provincia de La Pampa: **Camuzzi Gas Pampeana S.A.**
Normativa adoptada por el Código de Edificación (art. 1.1.5): *"Disposiciones y normas mínimas
para la ejecución de instalaciones domiciliarias de gas, editado por la empresa Gas del Estado en
1984"* — hoy sustituidas por las **NAG y disposiciones de ENARGAS**.
Local para medidores de gas (CE 5.8.5, mod. Ord. 3895/2009): *"Deben contar con fácil acceso, no
contener tableros o medidores de electricidad, calderas, motores, aparatos térmicos […] Al frente
de los medidores debe dejarse un espacio para circulación de un ancho no inferior a 1,00 m,
cumpliendo además todas las disposiciones del ente o empresa prestataria del servicio."*
**[VERIFICAR requisitos y plazos de conexión en Camuzzi Gas Pampeana, delegación La Pampa.]**

---

## 7. Checklist de verificación urbana antes de dibujar

Imprimir y completar una por parcela. Ninguna línea se dibuja hasta que esta hoja esté llena.

**A — Identificación de la parcela**

- [ ] Nomenclatura catastral y referencia municipal (Portal Ciudadano / Trámites On Line)
- [ ] Medidas reales de frente y fondo, y **ángulos** (Portal Ciudadano; el croquis de ubicación
      ya no se emite)
- [ ] Superficie de la parcela
- [ ] ¿Intermedia o **en esquina**? Si es esquina: definir cuál es frente y cuál fondo
      (CUA 4.3.1.1) y verificar si algún lado supera 26 m (CUA 4.3.1.5)
- [ ] Ancho de la vereda y **cota del cordón** (existente o futuro) → NT, NPB y NP mínimos
      (CE 3.1.2)
- [ ] ¿Tiene cordón cuneta? (dato exigido en el Acta de Inicio)
- [ ] ¿Tiene vereda reglamentaria? Si no, prever provisoria de 1,20 m + reglamentaria a construir

**B — Régimen urbanístico**

- [ ] **Distrito** en el Plano P1 — y sub-distrito con numeral romano (R3I ≠ R3VII)
- [ ] ¿**R3VII**? → planta baja a **≥ 1,20 m** sobre el cordón
- [ ] ¿**R2eIII o R2eIV**? → no admiten vivienda individual nueva; son PH con FOS congelado
- [ ] ¿Frentista a **corredor comercial** (Plano P2)? → mandan los indicadores del corredor y tramo
- [ ] ¿Dentro de la **zona de influencia del aeropuerto** (Plano P4)? → verificar altura admisible
- [ ] ¿Inmueble o entorno con **protección patrimonial** (Ord. 783/90, 643/89, 936/91)?
- [ ] FOS · Retiro de frente · Retiro de fondo en PB · Retiro lateral · Altura máxima · Densidad ·
      **C.A.S.** — anotados uno por uno con el artículo del CUA que los respalda

**C — Cálculo previo**

- [ ] Superficie máxima por FOS = superficie × FOS
- [ ] Huella real descontando retiros
- [ ] **La menor de las dos** es la superficie construible
- [ ] m² de **suelo absorbente** obligatorios (superficie × CAS) y dónde van a estar
- [ ] Dormitorios admitidos por densidad (superficie × indicador ÷ 1,5) — o "1 vivienda por
      parcela" en R2e, R5 y R6
- [ ] Cochera: **15 m², lado ≥ 2,50 m** (CUA) / **14 m², lado 2,90 m, altura 2,40 m** si además es
      acceso peatonal (CE) → adoptar lo más exigente. **Computa en el FOS.**
- [ ] Verificar que la suma casa + cochera + galería + **aleros** no supere el FOS
- [ ] ¿La superficie total supera **300 m²**? → trámite especial, doble inspección, paso por
      Secretaría de Gobierno

**D — Verificación del Código de Edificación**

- [ ] Ninguna abertura enfrentada al eje divisorio a menos de **3,00 m** (o paño fijo con antepecho
      a 1,60 m); aberturas perpendiculares al eje divisorio a **≥ 0,50 m**
- [ ] Patios de 1ª categoría (dormitorios, estar, comedor, cocina >15 m²): **lado ≥ 3,00 m,
      área ≥ 12,00 m²**
- [ ] Patios de 2ª categoría (baño, cocina ≤15 m², lavadero, circulaciones): **lado ≥ 2,00 m,
      área ≥ 8,00 m²**
- [ ] **Local independiente destinado a cocina** (CE 5.8.2) — si el partido es cocina integrada,
      consultar por escrito primero
- [ ] Baño con **compartimiento intermedio o paso** y puerta que impida la visión (CE 5.2.4)
- [ ] Pasajes y circulaciones ≥ **1,00 m** de ancho libre
- [ ] Escalera (si hay): ancho ≥ 1,00 m, paso ≥ 2,10 m, 2a+p = 0,60–0,63, a ≤ 0,18, p ≥ 0,26,
      ≤ 21 alzadas por tramo. Rampa: pendiente ≤ 10 %
- [ ] Parapetos de azotea: 1,00 m general · 1,40 m si es tendedero · **1,60 m ciego si está sobre
      el eje medianero o a menos de 3,00 m de él**
- [ ] Desagües pluviales: **prohibida** la caída a vía pública, linderos o muros divisorios
- [ ] Cercos entre predios: 1,80 m de altura mínima
- [ ] Superficies mínimas y **altura libre mínima de local**: ⚠ **PENDIENTE — falta el Cuadro
      3.4.4** (ver §9)
- [ ] Planilla de iluminación y ventilación: ⚠ **PENDIENTE — falta el Cuadro 3.4.5.1** (ver §9)

**E — Servicios**

- [ ] ¿La finca cuenta con **agua corriente** de red? (nota obligatoria en el plano)
- [ ] ¿La finca cuenta con **cloaca** de red? (nota obligatoria en el plano)
- [ ] Si no hay cloaca: cámara séptica de 2 secciones (mín. 1.000 L c/u) + pozo negro a ≥ 1,50 m
      del eje divisorio y ≥ 20,00 m (o ≥ 10,00 m excepcional) de la perforación
- [ ] Si no hay agua de red: perforación a ≥ 1,00 m del eje divisorio + consulta a la APA
- [ ] Croquis de instalaciones sanitarias (agua / cloaca / pluviales) según Disposición 131/2025
- [ ] Solicitud de factibilidad eléctrica a la **CPE**; gabinete de medidores según su reglamento
- [ ] Gabinete de gas separado del eléctrico, 1,00 m libre al frente de los medidores

**F — Antes de presentar**

- [ ] Carátula municipal oficial completa
- [ ] "SUPERFICIE TOTAL AL 100 %" incluyendo proyecciones y **aleros**
- [ ] Las 11 láminas/planillas de "Elementos que componen el plano" que correspondan
- [ ] Visado previo del **CALP** con Orden de Trabajo y aportes pagos
- [ ] Acreditación de titularidad o posesión legítima del inmueble
- [ ] Si hay apartamiento normativo: **nota y memoria descriptiva de justificación técnica**
      (modelo en el Anexo I del Manual de Procedimientos)

---

## 8. Ambigüedades y contradicciones detectadas (preguntas para Planeamiento)

Hacerlas **por escrito**, idealmente dentro de un trámite de **Factibilidad**, para que vuelvan
como acto administrativo.

1. **Cochera: 12/14 m² del Código de Edificación vs. 15 m² del CUA.** El CE 3.4.4.3 fija 12 m² y
   lado 2,60 m (14 m² y lado 2,90 m si sirve de acceso peatonal, altura 2,40 m); el CUA Sección 7.1
   fija *"En viviendas unifamiliares se preverá un espacio de 15 m², cuyo lado mínimo será igual o
   mayor a 2,50 m"*. **¿Cuál rige y cómo se combinan superficie, lado y altura?**
2. **Cocina integrada.** El CE 5.8.2 exige *"un local independiente destinado a cocina"* en toda
   unidad de vivienda. El CUA solo admite expresamente cocina integrada en el módulo polivalente.
   **¿Se admite el estar-comedor-cocina único en una vivienda unifamiliar? ¿Bajo qué condición
   (superficie, ventilación, campana)?**
3. **Retiro de fondo en planta baja: 26 m o 28 m.** El CUA art. 4.3.1.2 dice, en la misma página,
   *"a excepción de las parcelas de longitud menor a 28 m que no aplica la restricción del uso"* y
   *"Para parcelas de longitud mayor a 26 m se deberá aplicar retiro de fondo en planta baja"*,
   mientras que cada distrito dice *"Se aplicará cuando el lote sea de una profundidad mayor o igual
   a 26 mts."*. **¿Cuál es el umbral y qué se puede ocupar en la franja de fondo entre 26 y 28 m?**
4. **Validez del Permiso de Obra: 3 años para ratificar y 3 años para caducar** (CE 2.1.10, texto
   6445/2020). **¿Cómo se lee la contradicción?**
5. **Densidad y redondeo.** En R3, 360 m² × 0,02 = 7,2 habitantes ÷ 1,5 = 4,8 dormitorios.
   **¿Se redondea hacia abajo (4) o hacia arriba (5)?** El CUA solo fija el redondeo hacia arriba
   para los módulos de estacionamiento.
6. **C.A.S.: cómo se computa y cómo se acredita.** ¿Un piso permeable (adoquín con junta abierta,
   grava, césped reforzado) computa como suelo absorbente o solo la tierra desnuda? ¿Hay que
   graficarlo y acotarlo en el plano (la nota municipal habla de *"límite de solado, terreno
   absorbente"*)?
7. **Definición de Planta Baja (CUA 1.4.1.20)** — el texto dice que Planta Baja es la construcción
   *"cuyo nivel de piso terminado se encuentra por encima de 1,5 m de la cota o nivel ±0,00"*,
   mientras que el FOS computa lo construido *"sobre el nivel +1,50 m respecto de la cota ±0,00"*.
   **¿Una construcción con piso terminado por debajo de +1,50 m no computa FOS?** La lectura literal
   es absurda; puede ser un error de redacción o de OCR. **Verificar contra el PDF y preguntar.**
8. **Módulo polivalente:** ¿computa FOS? ¿computa densidad? ¿exige cochera propia? ¿se puede
   habilitar comercialmente en cualquier distrito R?
9. **Sistemas constructivos alternativos:** el CE 4.5.2 no admite madera como estructura resistente
   salvo vigas y tirantería de techos; el CUA 4.3.1.4 admite sistemas alternativos con CAT.
   **¿Basta el CAT para un wood frame o hace falta además la aprobación expresa del art. 4.5.2?**

---

## 9. LO QUE HAY QUE IR A BUSCAR PERSONALMENTE

Ordenado por urgencia. Cada ítem dice **dónde**, **a quién** y **para qué**.

### 🔴 Bloqueantes — sin esto no se puede firmar un plano

| # | Qué pedir, con nombre exacto | Dónde / a quién | Para qué sirve |
|---|---|---|---|
| 1 | **CUADRO 3.4.4.a, CUADRO 3.4.4.b y CUADRO 3.4.4.c — "Dimensiones mínimas de los locales"** del Código de Edificación (Ord. 1581/95). El Código remite a *"TEMAS DE INTERÉS – Sector: CUADROS CÓDIGO DE EDIFICACIÓN"* del sitio del Concejo Deliberante | **Dirección de Planeamiento Urbano y Obras Particulares**, Municipalidad de Santa Rosa · o **Concejo Deliberante de Santa Rosa**, mesa de entradas · o **CALP**, Área Técnica, `tecnica@colegioarqlapampa.org.ar` | Fijar superficie mínima, lado mínimo y **altura libre mínima** de dormitorio, estar, comedor, cocina, baño y lavadero. **Sin esto no se puede validar ninguna planta.** |
| 2 | **CUADRO 3.4.5.1 — "Iluminación y ventilación natural"** (valores de X y relación K/I) **y GRÁFICO 3.4.5** (salientes, alturas de vanos, profundidad de locales) | ídem | Completar la **Planilla de Iluminación y Ventilación** obligatoria en el plano (lámina 10) |
| 3 | **CUADRO 3.4.5.2 — "Ventilación natural por conducto"** | ídem | Baños y cocinas sin vano al exterior; secciones de conducto |
| 4 | **Ordenanza Fiscal / Tarifaria vigente**, capítulo de **Derechos de Construcción** | **Dirección de Rentas** o **Planeamiento Urbano y Obras Particulares**, Municipalidad de Santa Rosa | Cotizar el trámite. Hoy no hay ningún importe municipal verificado |
| 5 | **Resolución vigente del CALP** con el **valor de referencia del costo de construcción (\$/m²) y el aporte mínimo profesional** | **CALP**, Don Bosco 243, Santa Rosa · Adm. Contable (02954) 271011 · `adm@colegioarqlapampa.org.ar` | Cotizar visado y aportes. Se actualiza como máximo cada 2 meses |

### 🟠 Importantes — evitan retrabajo

| # | Qué pedir | Dónde / a quién | Para qué |
|---|---|---|---|
| 6 | **Requisitos técnicos de la presentación digital**: formatos de archivo admitidos, tamaño máximo, nomenclatura, si el plano va en PDF vectorial o rasterizado, cómo se firma digitalmente | Dirección de Planeamiento Urbano y Obras Particulares · mesa de entradas digital de `santarosa.gob.ar` | El Manual dice "únicamente digital" pero no especifica formato |
| 7 | **Número exacto y fecha de la Disposición** que aprueba el Manual de Procedimientos (el CPITLP la publica como "N° 16"; la copia escaneada no se lee) | Dirección de Planeamiento Urbano y Obras Particulares | Citarla correctamente en notas y memorias |
| 8 | **Circuito de solicitud de conexión de agua y de cloaca** para obra nueva: formulario, requisitos, plazo, costo, quién ejecuta la conexión a la red | **Dirección de Agua y Saneamiento**, Municipalidad de Santa Rosa | Programar la obra y cotizar |
| 9 | **Solicitud de factibilidad eléctrica** y requisitos de conexión definitiva; reglamento de tablero y de derivación a usuarios de la CPE | **CPE**, Raúl B. Díaz 218, Santa Rosa · `cpe.coop.ar` sección "Solicitud de factibilidad" | Dimensionar el gabinete de medidores y la acometida en el plano |
| 10 | **Régimen de perforaciones domiciliarias**: si una vivienda unifamiliar necesita permiso, si el perforista debe estar en el Registro de Consultores y Perforistas, si hace falta estudio hidrogeológico | **Administración Provincial del Agua (APA)**, Villegas 194, Santa Rosa · `apa.lapampa.gob.ar` · `apaconsultas@lapampa.gob.ar` | Obligatorio en lotes sin red de agua |
| 11 | **Carpeta "Documentación por localidades" del CALP** (planillas municipales de Santa Rosa) | CALP → menú Ejercicio Profesional → Documentación por localidades (carpeta de Google Drive) | Planillas y formularios actualizados |
| 12 | **Confirmación del distrito de la parcela** con constancia escrita | Dirección de Planeamiento Urbano | El Plano P1 es de 2021/2022; puede haber ordenanzas de excepción posteriores sobre parcelas puntuales |

### 🟡 Deseables

| # | Qué pedir | Dónde | Para qué |
|---|---|---|---|
| 13 | **Ordenanzas modificatorias del CUA posteriores a noviembre de 2023** (se detectaron ordenanzas de excepción puntuales por inmueble y por uso) | Concejo Deliberante de Santa Rosa | Verificar que no haya cambios de delimitación o de indicadores |
| 14 | **Texto de la Ordenanza 6445/2020** en versión legible (la copia disponible es un escaneo de baja calidad) | Concejo Deliberante | Precisar la redacción de los artículos 2.1.2, 2.1.9, 2.1.10 y 2.1.12 |
| 15 | **Ordenanzas 783/90, 643/89 y 936/91** (patrimonio) | Concejo Deliberante | Solo si el lote está en R2eII (Barrio Fitte) o hay preexistencia inventariada |
| 16 | **Criterio oficial sobre el redondeo de la densidad** y sobre el cómputo del C.A.S. | Planeamiento Urbano | Ver §8 |

---

## Anexo — fuentes y archivos descargados

Todos los archivos quedaron guardados en `docs/10-casa-santa-rosa/fuentes/`.

| Archivo | Qué es | Origen |
|---|---|---|
| `codigo-edificacion-ord1581-95-santa-rosa.pdf` | Código de Edificación, Ordenanza 1581/1995, texto consolidado, 86 pp., **con capa de texto** | `noticias.cpitlp.org.ar/storage/articulos/formularios/codigo edificacion santa rosa v20201230.pdf` |
| `codigo-edificacion-ord1581-95-TEXTO.txt` | Texto plano extraído del anterior | extracción propia |
| `codigo-urbano-ambiental-ord6976-23-OCR.txt` | **Transcripción por OCR** del Código Urbano Ambiental (Ord. 6976/2023), 165 pp. | OCR propio del PDF de Drive |
| `plano-P1-zonificacion-distritos.pdf` | Plano P1 — Distritos y zonificación | Drive id `1c9t__k28a83RjZ1dEMNdJk--7Cs1e5MR` |
| `plano-P2-corredores-comerciales.pdf` | Plano P2 — Corredores comerciales | Drive id `1hcn4vgp8UEkjPhRUfqtzDeaG_cg2xMxr` |
| `manual-procedimientos-planeamiento-urbano-2026.pdf` | Manual de Procedimientos de la Dirección de Planeamiento Urbano y Obras Particulares, vigente 01/03/2026, con el modelo de nota de justificación técnica | CPITLP → Formularios → Santa Rosa |
| `disposicion-131-2025-planos-sanitarios.pdf` | Disposición 131/2025 SOySP — croquis sanitario y casos que exigen plano sanitario | ídem |
| `acta-inicio-de-obra-santa-rosa.pdf` | Formulario municipal de Acta de Inicio de Obra | ídem |
| `elementos-que-componen-el-plano-municipal.pdf` | Qué debe contener cada lámina del plano municipal | ídem |
| `caratula-municipal-santa-rosa.pdf` | Carátula oficial | ídem (el DWG está en la misma página del CPITLP) |
| `ordenanza-6445-2020-modif-codigo-edificacion.pdf` | Modificatoria del Código de Edificación (escaneo) | `cpitlp.org.ar/modificacionCodigoEdificacion` |

**PDF del Código Urbano Ambiental completo (44 MB, escaneado):** no se guardó en el repositorio por
tamaño. Se descarga con
`https://drive.google.com/uc?export=download&id=1WZucUvH9wsi4HXQA2zd5zQLiMNKFGbDV`
(enlace publicado por el CPITLP en `cpitlp.org.ar/nuevocdigourbanoambiental`).

**Portales:**
`santarosa.gob.ar` (trámites de obra, libre deuda, mensuras, portal ciudadano) ·
`munidigital.com/citizenv2/santarosalapampa` (uso de suelo y aptitud técnica) ·
`micalp.colegioarqlapampa.org.ar` (visado CALP) ·
`cpe.coop.ar` (factibilidad eléctrica) ·
`apa.lapampa.gob.ar` (agua) ·
`cpitlp.org.ar` (formularios y normativa municipal republicada).

---

*Documento elaborado a partir de fuentes primarias descargadas y transcriptas. Todo lo marcado como
transcripción es literal de la norma; todo lo marcado como "lectura del estudio (inferido)" es
interpretación propia y debe validarse. Todo lo marcado `[VERIFICAR]` no está verificado y no debe
usarse para cotizar, comprometer plazos ni firmar documentación.*
