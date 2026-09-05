# GUÍA ÚNICA DE PROYECTO — CASA DE UNA PLANTA EN SANTA ROSA, LA PAMPA

> **Qué es este documento.** El que se abre cuando entra un encargo de casa y se sigue de punta a punta.
> No explica teoría: **decide**. Cada decisión trae el número que la sostiene y de qué documento sale.
> Cuando este documento y el informe geotécnico, la ficha urbanística oficial o la norma vigente digan
> cosas distintas, **mandan esos, no este**.

## Cómo se lee

| Marca | Significado |
|---|---|
| **[V]** | Dato verificado en fuente primaria (norma, ordenanza transcripta, estadística oficial) |
| **[PD]** | Predimensionado / criterio de oficina. Sirve para dibujar y presupuestar, **no para construir** |
| **[FIRMA]** | Lo define y lo firma un matriculado con incumbencia (estructuralista, geotécnico, gasista) |
| **[VERIFICAR]** | **No está confirmado.** No se cotiza, no se compromete y no se firma con esto |

## Documentos fuente (todo número de esta guía sale de acá)

| Ref. corta | Documento |
|---|---|
| `marco` | [`docs/00-marco/marco-local-santa-rosa.md`](../00-marco/marco-local-santa-rosa.md) |
| `urb` | [`urbanismo-y-tramite-santa-rosa.md`](urbanismo-y-tramite-santa-rosa.md) |
| `suelo` | [`suelo-y-fundacion-santa-rosa.md`](suelo-y-fundacion-santa-rosa.md) |
| `viento` | [`viento-santa-rosa.md`](viento-santa-rosa.md) |
| `envolvente` | [`envolvente-casa-santa-rosa.md`](envolvente-casa-santa-rosa.md) |
| `gas` | [`gas-camuzzi-santa-rosa.md`](gas-camuzzi-santa-rosa.md) |
| `ante` | [`docs/01-anteproyecto/anteproyecto.md`](../01-anteproyecto/anteproyecto.md) |
| `proy` | [`docs/02-proyecto/proyecto-ejecutivo.md`](../02-proyecto/proyecto-ejecutivo.md) |
| `int` | [`docs/07-interiorismo/interiorismo.md`](../07-interiorismo/interiorismo.md) |
| `hon` | [`docs/08-gestion/servicios-y-honorarios.md`](../08-gestion/servicios-y-honorarios.md) |

---

## ÍNDICE

- [Los diez números que hay que saber de memoria](#los-diez-números-que-hay-que-saber-de-memoria)
- [FASE 0 — Antes de aceptar el encargo](#fase-0--antes-de-aceptar-el-encargo)
- [FASE 1 — El lote](#fase-1--el-lote)
- [FASE 2 — El partido](#fase-2--el-partido)
- [FASE 3 — Las decisiones técnicas que se toman en anteproyecto](#fase-3--las-decisiones-técnicas-que-se-toman-en-anteproyecto-y-no-después)
- [FASE 4 — El proyecto](#fase-4--el-proyecto)
- [FASE 5 — Trámites](#fase-5--trámites)
- [FASE 6 — Obra](#fase-6--obra)
- [ANEXO A — Checklist de una carilla](#anexo-a--checklist-de-una-carilla-para-la-primera-reunión)
- [ANEXO B — Los 10 errores que arruinan una casa en Santa Rosa](#anexo-b--los-10-errores-que-arruinan-una-casa-en-santa-rosa)
- [ANEXO C — Lo que falta verificar](#anexo-c--lo-que-falta-verificar-tabla-consolidada)

---

## Los diez números que hay que saber de memoria

| # | Número | Qué gobierna | Fuente |
|---|---|---|---|
| 1 | **TDMN −6,0 °C · TDMX 38,8 °C · GD18 1.394** | Todo el dimensionado térmico. Zona **IVc** | `marco` §4.1 · `envolvente` §0 |
| 2 | **K muro ≤ 0,30 · K techo ≤ 0,19** (Nivel A) | La envolvente. En techo **manda siempre el verano** | `envolvente` §1.7 |
| 3 | **Viento del N 34 % del tiempo · del S 18 % · 71 % de la carga en el eje N-S** | El partido entero | `viento` §3.3 y §3.6 |
| 4 | **V = 50 m/s** (CIRSOC 102-2005, Fig. 1B) | La succión de cubierta | `marco` §5.1 · `viento` §2.1 |
| 5 | **Zona sísmica 0** — el viento, no el sismo, es la acción horizontal | Estructura | `marco` §5.1 |
| 6 | **Manto eólico suelto de 0,20 a 2,00 m sobre tosca** | La fundación de una casa baja cae justo ahí | `suelo` §2.1 |
| 7 | **La napa pasó de ~25 m (1990) a menos de 5 m (2017)** en el centro | Todo antecedente anterior a 2015 no sirve | `suelo` §3.1 |
| 8 | **FOS 0,6 · C.A.S. 0,20** en R2/R3/R3e/R4 (el tejido más común) | Superficie construible | `urb` §2.1 |
| 9 | **Retiro de fondo en PB: 3 m si la profundidad ≥ 26 m**, solo dependencias de servicio | La huella | `urb` §2.1 |
| 10 | **5 m³/h** = techo de la matrícula de gasista de 3ª categoría | Qué instalador se puede contratar | `gas` §2.2 |

---

# FASE 0 — Antes de aceptar el encargo

## 0.1 La primera llamada: seis preguntas que se hacen antes de agendar la reunión

| # | Pregunta | Por qué decide si hay encargo |
|---|---|---|
| 1 | **¿Dónde está el lote? Dirección o nomenclatura catastral** | Define distrito, posición en la cuenca de Don Tomás, napa esperable y si hay red de gas (`suelo` §2.4 · `gas` §3.0) |
| 2 | **¿El lote está escriturado o hay boleto?** | Sin titularidad acreditable no hay Permiso de Obra: el municipio exige *"acreditarse la titularidad o posesión legítima del inmueble"* (`urb` §5.2) |
| 3 | **¿Tiene agua, cloaca, gas y luz en la cuadra?** | Sin cloaca cambia el partido (pozo + séptica, distancias); sin gas puede haber **años** de espera de extensión de red (`urb` §6.2 · `gas` §3.6) |
| 4 | **¿Qué presupuesto de obra tiene?** | Es el dato que más condiciona el diseño. Preguntarlo de frente (`ante` §2.1) |
| 5 | **¿Para cuándo lo necesita?** | El plazo del estudio para una casa de 120–200 m² es **6 semanas de anteproyecto** desde que el cliente entregó todo (`ante` §1.7.1) |
| 6 | **¿Quién decide? ¿Van a estar todos en la reunión?** | Reunión con la mitad de los decisores = anteproyecto rehecho (`ante` §2.1) |

**Y una pregunta que casi nadie hace y define la fundación:** *¿va a haber pileta?* Si la respuesta es sí,
hay que saberlo **en el anteproyecto**: una pileta es un depósito de decenas de m³ de agua enterrado, exige
**≥ 5,00 m [PD]** al perímetro de fundación y puede cambiar el tipo de fundación (`suelo` §8.7).

## 0.2 Datos del lote que se piden por escrito antes de la visita

| Documento | Quién lo tiene | Para qué |
|---|---|---|
| Escritura o boleto de compraventa | Cliente / escribano | Titularidad, superficie, servidumbres (`ante` §3.1) |
| **Plano de mensura** | Cliente / catastro | Medidas y ángulos reales — **no confiar en la escritura** (`marco` §7) |
| **Ficha / certificado urbanístico de la parcela** | Dirección de Planeamiento Urbano | **El documento más importante de todos.** Distrito, FOS, altura, retiros, densidad, C.A.S. oficiales de ESE lote (`marco` §Estado de la normativa) |
| Datos de parcela del **Portal Ciudadano** (`santarosa.gob.ar` → Trámites On Line) | El profesional | Ángulos y distancias a esquina. **El croquis de ubicación ya no se emite** (`urb` §5.0) |
| Libre de deuda catastral | Propietario | Deudas de tasas y multas bloquean el trámite (`urb` §5.0) |
| Planos aprobados anteriores (si hay preexistencia) | Cliente / archivo municipal | Punto de partida y estado de regularización (`marco` §7) |

> **[R] Regla de hierro:** no se dibuja una sola línea antes de tener el informe de zonificación por escrito.
> Lo que dice el mostrador verbalmente no vale; lo que dice el papel, sí (`ante` §3.1).

## 0.3 Señales de encargo problemático

Cuando aparecen **tres o más**, se cotiza alto o no se toma (`ante` §2.8):

| Señal | Qué significa |
|---|---|
| No quiere decir el presupuesto | O no lo tiene, o va a comparar precio de estudio en vez de proyecto |
| "Es un trabajito sencillo" | Subestima el encargo; va a discutir cada honorario |
| **Ya tiene los planos y quiere que "se los firmes"** | **Firma de complacencia: no se hace.** Falta ética grave y responsabilidad civil y penal |
| Trae un render de Pinterest y quiere "exactamente eso" | Compró una imagen, no un servicio de proyecto |
| Cambió de arquitecto dos veces | Escuchar por qué; muchas veces es el patrón |
| El que decide no vino a la reunión | Todo lo acordado se va a revisar |
| Plazo imposible | La presión de plazo se traslada a errores |
| **No tiene el terreno escriturado ni boleto** | Riesgo de trabajar sobre algo que no se compra |
| "Después vemos los honorarios" | Nunca se ven |
| Quiere empezar la obra sin proyecto, "sobre la marcha" | Sobrecostos, conflictos y responsabilidad profesional |

**Señales propias de Santa Rosa que se agregan a esa lista:**

- **"El vecino construyó sin estudio de suelos y no le pasó nada."** Las casas de los '80 se construyeron sobre otra ciudad: la napa subió del orden de 20 m en tres décadas (`suelo` §3.1). El argumento no aplica.
- **"Ya tengo el gasista."** Antes de aceptarlo hay que ver la categoría de matrícula contra el caudal del proyecto: con caldera, el de 3ª categoría queda fuera de alcance (`gas` §2.3).
- **Lote en loteo nuevo del ejido sin red de gas.** Hay antecedentes de barrios de Santa Rosa que esperaron más de 15 años (`gas` §3.6). **Verificarlo antes de firmar el contrato de proyecto.**
- **Lote en el sector bajo (SO, entorno de Don Tomás / Bajo Giuliani).** Napa somera, anegamiento, pozo absorbente que no absorbe (`suelo` §3.3).

## 0.4 Qué se cobra por el relevamiento y qué no

| Concepto | Criterio |
|---|---|
| **Visita al terreno + verificación de medidas + nivelación respecto del cordón** | Está dentro del anteproyecto en obra nueva. **En reforma se cotiza aparte: es trabajo real, no cortesía** (`hon` §6.1) |
| **Mensura, deslinde, amojonamiento y verificación de ángulos** | **Agrimensor matriculado**, ítem aparte (`ante` §3.2.1) |
| **Relevamiento planialtimétrico profesional** | **Obligatorio si** el desnivel supera **1,00 m** en cualquier dirección, hay subsuelo, o el terreno supera 1.000 m² (`ante` §3.2.1) |
| **Estudio de suelos** | Ítem aparte, siempre a cargo del comitente. Orden de magnitud: **0,3–0,8 % del costo de la obra** (`suelo` §6.7) |
| **Anteproyecto** | Se cobra siempre. Hasta el anteproyecto avanzado se devengó el **40 %** del honorario total de proyecto + dirección (`ante` §1.7.2). Cobro sugerido: **40 % a la firma, 30 % contra A1, 30 % contra A2 y acta** (`ante` §1.7.3) |

**Los costos que el comitente no tiene en la cabeza y se listan por escrito en la primera reunión** (`ante` §2.6.4):
honorarios de proyecto y dirección **8–12 %** del costo de obra · cálculo estructural **0,8–1,5 %** ·
proyecto de instalaciones **1–2,5 %** · amoblamiento fijo **6–12 %** · aberturas **8–15 %** ·
paisajismo y cercos **2–6 %** · derechos y tasas municipales **[VERIFICAR en Santa Rosa; suelen ser 0,5–2 %]** ·
**imprevistos 10 % mínimo, sin excepción**.

> **La frase para el cliente:** *"Al número de la obra hay que sumarle entre un 25 y un 35 por ciento de cosas
> que no son ladrillos. Si no lo contamos ahora, aparece igual, pero cuando ya no hay plata."* (`ante` §2.6.4)

**Y la frase que salva la casa:** *"El estudio de suelos es el único ítem del presupuesto que, si lo sacamos,
no se puede volver a poner después."* (`suelo` §6.7)

## 0.5 Qué se firma antes de dibujar

1. **Contrato / Orden de Trabajo** con alcance incluido **y excluido**, entregables enumerados, plazos, cantidad de revisiones (recomendado: **2 ciclos de ajuste** sobre el partido aprobado) y forma de pago por hitos (`hon` §3.3 y §6.3).
2. **Programa de necesidades por escrito, confirmado por mail dentro de las 48 h** de la entrevista. Ese mail es el documento de base del encargo (`ante` §2.1).
3. Declaración expresa de que **cambio de partido = nuevo anteproyecto**, no una revisión (`hon` §3.3).
4. Declaración de que el anteproyecto **no garantiza aprobación municipal** (`hon` §3.3).

---

# FASE 1 — El lote

## 1.1 Ficha urbanística: los cuatro números que importan en una casa

En una casa de una planta **la altura nunca es el condicionante**: los techos de los distritos residenciales
van de 6 a 9 m y una casa baja no los toca (`urb` §2). Lo que manda es esto:

| Indicador | **R2** | **R2a** | **R2e** | **R3** | **R3e** | **R4** | **R5** | **R6** |
|---|---|---|---|---|---|---|---|---|
| **FOS** | 0,6 | 0,6 | 0,6 | 0,6 | 0,6 | 0,6 (**0,8** en interés social ≤200 m²) | **0,5** | **0,5** |
| **Retiro de frente** | — | **Sí** (jardín) | **Sí** (jardín) | — | — | — | **4 m** | **4 m** |
| **Retiro de fondo en PB** (si prof. ≥ 26 m) | 3 m | 3 m | 3 m | 3 m | 3 m | 3 m | 3 m | 3 m |
| **Retiro lateral** | — | — | — | — | — | — | 3 m de un lateral si frente ≥ 20 m | **3 m de un lateral** |
| **C.A.S.** | **0,20** | **0,15** | **0,15** | **0,20** | **0,20** | **0,20** | **0,25** | **0,30** |
| **Cochera** | 1 espacio | **Obligatoria, 1 módulo/vivienda** | **Obligatoria, 1 módulo/vivienda** | 1 espacio | 1 espacio | 1 espacio | 1 espacio | 1 espacio |
| Densidad | 0,08 hab/m² | 0,04 hab/m² | **1 viv./parcela** | 0,02 hab/m² | 0,02 hab/m² | 0,03 hab/m² | **1 viv./parcela** | **1 viv./parcela** |
| Altura máx. | PB+2 ó 9 m | PB+2 ó 9 m | 9 m | PB+1 ó 6 m | PB+1 ó 6 m | PB+1 ó 6 m | PB+1 ó 6 m | PB+1 ó 6 m |
| Subdivisión mín. | 12 m / 300 m² | 15 m / 450 m² | 15 m / 450 m² | 12 m / 300 m² | 12 m / 300 m² | 10 m / 300 m² | 15 m / 600 m² | 20 m / 1.000 m² |

*Transcripto del Código Urbano Ambiental, Ord. 6976/2023, Título 5, Secciones 5.4 a 5.11 —* `urb` §2.1.
**Los indicadores de la Ord. 3274/2005 están derogados** (art. 2º de la 6976/23): el retiro de fondo de pisos
superiores se **unificó en (n−20)/2** y las densidades de R2e, R3, R3e y R4 **bajaron** (`urb` §2.2).

### Los cuatro que definen el proyecto de una casa

1. **FOS** — computa la **envolvente total, cubierta y semicubierta**, sobre el nivel +1,50 m, excluidos solo balcones de vuelo ≤1,20 m no continuos (art. 1.4.3.2). **Y la nota municipal agrega que los ALEROS computan** al 100 % (`urb` §3.1 punto 2).
2. **Retiro de fondo en PB** — mínimo **3 m** si la profundidad ≥ 26 m, ocupable **solo con dependencias de servicio** (cochera, quincho, baulera, sanitarios, natatorio) **en una sola planta de hasta 4,50 m**. El estar-comedor no puede ir ahí.
3. **C.A.S. (Coeficiente de Absorción del Suelo)** — indicador nuevo. *"Porción mínima de la superficie total de una parcela que debe quedar libre de cualquier construcción que impida la permeabilidad del terreno natural, sean locales cubiertos, semicubiertos o **veredas exteriores**"* (art. 1.4.1.15). **Los solados del patio computan en contra.**
4. **Cochera** — **⚠ contradicción normativa:** el Código de Edificación (art. 3.4.4.3) fija 12 m² y lado 2,60 m (**14 m², lado 2,90 m, altura 2,40 m** si además es acceso peatonal); el CUA fija **15 m² con lado ≥ 2,50 m**. **Criterio del estudio: adoptar lo más exigente de cada parámetro** → 15 m², lado 2,90 m, altura 2,40 m. **Computa en el FOS, sin bonus** (`urb` §4.10 y §8).

### Trampas de distrito que hay que chequear en el Plano P1 antes de dibujar

| Situación | Consecuencia | Fuente |
|---|---|---|
| **R3VII** | La cota de piso interior de PB debe estar **≥ 1,20 m sobre el cordón**. Cambia acceso, rampa vehicular y accesibilidad: con 10 % de pendiente máxima son **12 m de desarrollo de rampa** más descansos | `urb` §2.3 y §4.7 |
| **R2eIII y R2eIV** | Conjuntos en propiedad horizontal: **la planilla de usos no admite vivienda individual nueva** | `urb` §2.3 |
| **R2eII (Barrio Fitte)** | Interés de conjunto; requiere estudio particular de la Autoridad de Aplicación y vista de la Comisión de Patrimonio | `urb` §2.3 |
| **Lote frentista a corredor comercial (Plano P2)** | Mandan los indicadores del corredor y su tramo (CC1 a CC13, con tramos A/B/C/D). **Para una casa no aporta nada —el FOS residencial sigue en 0,6— pero puede quitar**: cambia subdivisión y retiros | `urb` §2.5 |
| **Lote en zona de influencia del aeropuerto (Plano P4)** | Altura admisible; trámite ANAC si corresponde | `urb` §5.0 |
| **Lote en esquina** | Frente y fondo = **lado menor** (art. 4.3.1.1); por criterio proyectual se puede definir el lado mayor como fondo. Si un lado supera 26 m, el retiro de fondo se cumple sobre el lado menor (art. 4.3.1.5) | `urb` §2.1 |
| **Lote ≤ 200 m²** | El FOS puede ser **0,80** (art. 4.3.1.6) | `urb` §2.1 |
| **Lote atípico** | Se pueden usar indicadores de zonas análogas para el FOS, variar el retiro de frente y **prescindir del retiro lateral** (art. 4.3.2.3) | `urb` §2.1 |

## 1.2 Cálculo de la superficie realmente construible — método

1. Ubicar el lote en el **Plano P1** (distrito) y en el **Plano P2** (¿corredor?).
2. **Superficie máxima por FOS** = superficie × FOS.
3. **Huella real** = superficie menos retiro de frente, laterales y **retiro de fondo de PB**.
4. **Superficie construible = el MENOR entre FOS y huella real.**
5. **C.A.S.** = superficie × coeficiente → m² que quedan **sin construcción y sin solado**. Se descuentan del patio, no del FOS.
6. **Densidad** → dormitorios admitidos (hab ÷ 1,5). En R2e, R5 y R6: **una vivienda por parcela**.
7. **Restar cochera + galería + aleros** del FOS.
8. Verificar **visuales a linderos** y **patios** (§1.3).
9. Si hay duda de interpretación: **trámite de Factibilidad** (`urb` §3.1).

### Ejemplo resuelto — el lote más típico de Santa Rosa: 12 × 30 m en R3 (360 m²)

Lote entre medianeras, intermedio, sin corredor, **no** en R3VII (`urb` §3.2):

| Paso | Cálculo | Resultado |
|---|---|---|
| Superficie del lote | 12 × 30 | **360 m²** |
| FOS 0,6 | 360 × 0,6 | **216 m² ocupables** |
| Retiro de frente | R3 no exige | 0 m |
| Retiro lateral | R3 no exige | 0 m |
| Retiro de fondo en PB (30 ≥ 26 m) | Franja de 3 m, **solo dependencias de servicio**, una planta ≤ 4,50 m | 12 × 3 = 36 m² |
| Huella para el uso principal | 12 × 27 | 324 m² |
| **Superficie construible** | menor entre 216 y 324 | **216 m² — manda el FOS** |
| **C.A.S. 0,20** | 360 × 0,20 | **72 m² permeables obligatorios** |
| Descubierto resultante | 360 − 216 = 144 m² | de los cuales **72 m² sin solado** |
| Densidad | 360 × 0,02 = 7,2 hab ÷ 1,5 | **4 dormitorios** (4,8 → 4; **criterio de redondeo [VERIFICAR]**) |
| Cochera (incluida en FOS) | −15 m² | |
| Galería + aleros computables | −12 m² y −8 m² aprox. | |
| **Queda realmente para la casa** | 216 − 15 − 12 − 8 | **≈ 180 m²** |

> **Lo que enseña el ejemplo:** en el lote típico entran cómodamente una casa de 3 dormitorios de ~150 m²,
> galería, cochera y aleros, **y todavía sobra FOS**. El indicador que primero se agota **no es el FOS: es el
> C.A.S.**, porque los 72 m² permeables obligan a no solar todo el patio; y la franja de fondo de 3 m ya no se
> puede sumar al estar. **El partido natural es casa al frente, patio en el medio, y quincho/lavadero/cochera
> contra el fondo** (`urb` §3.2).

**Los otros dos casos, para tener el orden de magnitud** (mismo lote de 15 × 40 m = 600 m², `urb` §3.3 y §3.4):

| | **R2a** | **R5** |
|---|---|---|
| FOS | 0,6 → **360 m²** | 0,5 → **300 m²** |
| Retiro de frente | Jardín (3 m si fondo >30 m; avanzable hasta LM en el **50 % del ancho**) | **4 m** |
| Retiro lateral | — | 3 m **solo si frente ≥ 20 m** → acá no |
| C.A.S. | 0,15 → **90 m²** | 0,25 → **150 m²** |
| Cochera | **Obligatoria** | 1 espacio |
| Queda para la casa | ≈ **308 m²** | **300 m²** menos cochera, galería y aleros |

> **El mismo lote pierde 60 m² de superficie construible solo por pasar de R2a a R5, y obliga a 150 m² de
> tierra. Por eso la primera pregunta de la primera reunión es el distrito, no el programa** (`urb` §3.4).

## 1.3 Reglas del Código de Edificación que condicionan la planta desde el primer croquis

| Regla | Valor | Artículo |
|---|---|---|
| **Vistas a linderos** | **Ninguna abertura enfrentada al eje divisorio a menos de 3,00 m.** Si no se cumple: elemento fijo opaco o traslúcido de **h ≥ 1,60 m**. Abertura en paramento **perpendicular** al eje divisorio: **≥ 0,50 m** | CE 3.8.1 |
| **Vanos en muro divisorio** | Solo iluminación suplementaria, con antepecho **> 1,60 m** y paño fijo no transparente | CE 3.8.2 |
| **Patio de 1ª categoría** (dormitorio, estar, comedor, cocina > 15 m²) | **lado ≥ 3,00 m y área ≥ 12,00 m²** | CE 3.4.7 |
| **Patio de 2ª categoría** (baño, cocina ≤ 15 m², lavadero, circulación) | **lado ≥ 2,00 m y área ≥ 8,00 m²** | CE 3.4.7 |
| **Ventanas enfrentadas de distintas unidades** | **6 m libres** | CUA 4.3.4.b |
| **Cocina** | *"Toda unidad de vivienda debe contar con un **local independiente destinado a cocina**"* → **la cocina integrada es una interpretación a consultar por escrito** | CE 5.8.2 |
| **Baño** | Independiente de locales de permanencia, comunicado por **compartimiento intermedio o paso**, con puerta que impida la visión | CE 5.2.4 |
| **Circulaciones** | Ancho libre **≥ 1,00 m** | CE 3.5.1 |
| **Rampa** | Pendiente **≤ 10 %**, solado antideslizante, descansos | CE 3.5.4 |
| **Escalera principal** (si hay altillo o acceso a azotea) | Ancho ≥ 1,00 m · paso ≥ 2,10 m · **2a + p = 0,60 a 0,63** · a ≤ 0,18 · p ≥ 0,26 · máx. 21 alzadas por tramo | CE 3.5.2 |
| **Medios de salida** | ***"Estas exigencias no son de aplicación en la vivienda individual"*** — no se dimensionan ni se computa número de ocupantes | CE 3.6.1 |
| **Clasificación de locales** | Cocina **de más de 15 m² pasa a 1ª clase** y necesita patio de 1ª categoría. *"El uso de cada local es el que resulta de su ubicación y dimensiones, no el que arbitrariamente pueda estar consignado en planos"* | CE 3.4.1 / 3.4.2 |
| **Parapeto de azotea** | 1,00 m general · **1,40 m ciego** si es tendedero · **1,60 m ciego** si está sobre el eje medianero o a menos de 3,00 m de él | CE 4.9 |
| **Desagües pluviales** | **Prohibida** la caída a la vía pública, a predios linderos o sobre muros divisorios | CE 4.9 / 5.3.2 |
| **Cercos entre predios** | Altura mínima **1,80 m** (mampostería o premoldeados); se puede acordar otra cosa **por escrito** con el lindero | CE 3.2.1 |
| **Cotas de nivel** | NT ≥ NR + 3 % del ancho de vereda · **NPB ≥ NR + 0,10 m + 3 %** · NP ≥ NR + 0,05 m + 3 %. *(Vereda de 2,00 m: NPB ≥ NR + 0,16 m.)* **El piso terminado nunca va al nivel del cordón** | CE 3.1.2 |
| **Vereda** | Ancho mínimo **1,40 m** con 2 cazoletas de arbolado (Acta de Inicio); pendiente transversal **1 a 3 %**; juntas cada 10 m; rampa vehicular con desarrollo máximo **1,40 m** desde el cordón; **no se permiten escalones**. **Sin acera no hay alta de obra** | CE 3.2.2 / Ord. 3428/2006 |
| **Superficie total > 300 m²** | Pasa a **"trámite especial"**: intervención de Secretaría de Gobierno y **doble inspección** (fundación/capa aisladora y fin de estructura) | `urb` §5.5 |

⚠ **Lo que este documento NO puede fijar:** superficie mínima, lado mínimo y **altura libre mínima** de los
locales (Cuadros 3.4.4.a/b/c) y la planilla de **iluminación y ventilación** (Cuadro 3.4.5.1). **No se
consiguieron.** Ver [Anexo C](#anexo-c--lo-que-falta-verificar-tabla-consolidada). Lo único que el Código fija
indirectamente es que el fondo de una viga aparente no puede bajar de **2,30 m** del solado y que no puede
ocupar más de 1/3 del cielorraso (CE 3.4.3).

## 1.4 Orientación y relevamiento de viento en el lote

**Lo que se releva en la visita** (`ante` §3.2.2):

- Medidas de los cuatro lados **y de las diagonales** (la escuadría casi nunca es exacta) y ángulos.
- **Cota del cordón en el eje del terreno** = cota de referencia ±0,00 municipal; cota de vereda en ambos extremos del frente; cota del terreno natural en las cuatro esquinas y el centro; cota del terreno del vecino junto a la medianera.
- **Dirección natural de escurrimiento del agua de lluvia** y si el lote recibe escorrentía del vecino.
- **Cota de la boca de registro de cloaca** → define si la casa desagota por gravedad o necesita bombeo. *"La cota de cloaca decide más plantas bajas que el sol"* (`ante` §3.2.2).
- Accesos vehiculares de los vecinos (condicionan dónde se puede poner el propio), árboles de vereda, postes, cámaras.
- **Posición del lote en la cuenca centrípeta de Don Tomás** (`suelo` §2.4): sector alto E/N (cotas 195–200 msnm) · casco céntrico (175–179) · **sector bajo SO (167 y menos)**.

**Lo que se releva de viento — y no hace falta anemómetro:** la rosa de los vientos ya está resuelta
(`viento` §3.3, SMN Santa Rosa Aero 2011-2020):

| Dirección | Frecuencia | Velocidad media | Índice de exposición (∝ frec. × v²) |
|---|---|---|---|
| **N** | **34,1 %** | **18 km/h** | **46,3 %** |
| **S** | **18,2 %** | **18 km/h** | **24,7 %** |
| W | 12,0 % | 8 km/h | 3,2 % |
| E | 9,0 % | 13 km/h | 6,4 % |
| NE | 8,1 % | 15 km/h | 7,6 % |
| SW | 6,8 % | 13 km/h | 4,8 % |
| SE | 5,6 % | 15 km/h | 5,3 % |
| NW | 5,1 % | 9 km/h | 1,7 % |
| **Calma** | **1,2 %** | — | — |

Lo que **sí** se releva en el lote:

- **Categoría de exposición CIRSOC.** Exposición B exige rugosidad urbana continua **> 450 m a barlovento**; si el lote da al **norte sobre campo, calle ancha, plaza, cancha, canal, Ruta 5 o Circunvalación**, es **C**. La diferencia B→C es **+21 % de presión dinámica** en el método analítico (Kz 0,72 → 0,87). **Criterio del estudio: ante la duda, C** (`viento` §2.5).
- **Obstáculos y barreras existentes**: altura, longitud y porosidad de cercos, medianeras y arbolado vecino, sobre todo al N. Ojo: el arbolado de vereda de Santa Rosa está dominado por **fresno (57,3 %)**, que es caduco y **en invierno aporta solo el 15 % de su área frontal** como obstrucción efectiva. **No se puede contar con el arbolado de vereda como barrera** (`viento` §5.4 y §2.5).
- **Kzt = 1,00** en llanura; **revisarlo** solo en lotes sobre el borde de los bajos (Bajo Giuliani, Valle Argentino) (`viento` §2.6).

**Contexto que hay que tener presente al proyectar el exterior** (`viento` §3.8): **156 días de viento fuerte
por año** (uno de cada 2,3 días), con máximos en **diciembre (17,8), noviembre (17,6), enero (16,9) y octubre
(16,1)** — justo la temporada de uso del patio; **37 días de tempestad de polvo o arena**; 54 de tormenta;
3 de granizo. Y los **máximos absolutos no vienen del sector dominante**: el récord de la serie es
**143 km/h del SE (12/02/2014)**, y los máximos mensuales vienen del S (5 meses), SE (2), W (2), SW y NE.

> **Consecuencia de primer orden: la barrera que hace confortable el patio (contra el N) NO es la que salva
> la estructura (que se rompe con vientos del S, SE y W). La estructura se calcula omnidireccional; el confort
> se resuelve direccional. No se pueden intercambiar** (`viento` §3.7).

## 1.5 Servicios disponibles

| Servicio | Prestador | Qué hay que averiguar |
|---|---|---|
| **Agua potable y cloaca** | **La propia Municipalidad de Santa Rosa** (Ord. 6278/2019 ratifica el convenio de 1980). No hay cooperativa ni empresa provincial | ¿Hay red en la cuadra? El plano lleva **nota obligatoria**: *"LA FINCA CUENTA (o NO) CON LOS SERVICIOS DE PROVISIÓN DE AGUA CORRIENTE Y CLOACA"*. **[VERIFICAR circuito, requisitos y costo de conexión en la Dirección de Agua y Saneamiento]** (`urb` §6.1) |
| **Electricidad** | **CPE — Cooperativa Popular de Electricidad de Santa Rosa Ltda.**, Raúl B. Díaz 218, tel. 412222, `cpe.coop.ar` sección "Solicitud de factibilidad" | Factibilidad y derecho de conexión **[VERIFICAR]**. La instalación interna se rige por **AEA 90364**, que el propio Código de Edificación adopta (art. 1.1.5) (`urb` §6.3) |
| **Gas natural** | **Camuzzi Gas Pampeana**. Consulta de factibilidad por dirección: **0810-555-3698** · WhatsApp 11 3931-1234 | **¿Hay red en la cuadra?** Y **¿la red es de baja o media presión?** — define si hace falta regulador domiciliario en el nicho, que **paga e instala el cliente**. Camuzzi no publica el mapa de presiones: **exigir el dato en la respuesta al Formulario 3.4 A** (`gas` §3.0 y §5.1) |
| **Pluvial** | Municipal | La ciudad es **cuenca endorreica**: el agua que cae en Santa Rosa se queda en Santa Rosa (`suelo` §2.4) |

**Si no hay cloaca** (CE 5.2.5, 5.3.3 a 5.3.5, transcripto en `urb` §4.17):

- **Perforación** para captación de agua potable: **≥ 1,00 m del eje divisorio**.
- **Cámara séptica de dos secciones iguales**, 200 l/persona hasta 10 personas, **mínimo absoluto 1.000 l por sección**. *(Vivienda de 5 personas → 2 secciones de 1.000 l = **2.000 l**.)* Ventilación de conducto **Ø ≥ 0,10 m**.
- **Pozo negro**: **≥ 1,50 m del eje divisorio** y **≥ 20,00 m de la perforación**; si el lote no lo permite, extremos opuestos del predio y **nunca menos de 10,00 m**. Bóveda de albañilería de 0,30 m u H°A° de 0,10 m.
- **Prohibidos los pozos negros en zonas con red cloacal.**
- **Criterio geotécnico que la norma no fija** (`suelo` §8.5): el pozo absorbente va **lo más lejos posible y nunca a menos de 5,00 m [PD] de cualquier elemento de fundación**, **aguas abajo** de la casa. *"Un pozo ciego a 3 m de una base en loess es una bomba de tiempo."* **Si el lote no permite 5 m, el pozo absorbente no es una solución aceptable en este suelo.**
- **[VERIFICAR en la APA, Villegas 194, Santa Rosa]** si una perforación domiciliaria de vivienda unifamiliar requiere permiso, registro del perforista y/o estudio hidrogeológico.

## 1.6 Encargo del estudio de suelos

### ¿Hace falta? Sí.

**El municipio no lo exige** en una casa: el art. 4.4.2 del Código de Edificación solo lo obliga en obras de
**más de 3 pisos y/o más de 10,00 m de altura y/o sótanos de más de 3,00 m** (`urb` §4.15). **Es una exención
administrativa, no técnica**, y no traslada la responsabilidad profesional **[FIRMA]**.

Los cinco argumentos con los que se lo omite y por qué no valen acá (`suelo` §6.1):

| Argumento | Por qué no vale en Santa Rosa |
|---|---|
| "Es una casa liviana" | **El colapso del loess lo dispara el agua, no la carga.** La casa baja funda a 0,80–1,20 m, **exactamente en la capa que se moja**, y tiene ~0,40 m de perímetro por m² cubierto contra 0,17 de un edificio |
| "Toda la cuadra está construida y no pasa nada" | La napa subió ~20 m en 30 años: las casas de los '80 se construyeron en otro suelo |
| "Ya sé cómo es el suelo de la zona" | **No hay banco de datos geotécnicos publicado de Santa Rosa**, y la tosca varía **dentro del mismo lote** |
| "El estudio sale caro" | 0,3–0,8 % del costo de obra, contra **15–40 %** que cuesta recalzar |
| "El municipio no lo pide" | No lo hace innecesario **[FIRMA]** |

### Exploración mínima exigible

| Requisito | Valor | Fuente |
|---|---|---|
| Cantidad de prospecciones | **2** (Clase C-1) / **3 recomendado** (Clase C-2). **Criterio del estudio: 3**, porque la C-1 exige "condiciones geotécnicas conocidas" y con napa en ascenso y tosca errática eso no se sostiene | CIRSOC 401 Tabla 3.1 |
| Profundidad de investigación | **≥ 6,00 m** | CIRSOC 401 art. 3.5.6.2 |
| **Método por encima de la napa** | **Calicatas y pozos a cielo abierto, con muestreo en damas de lado mínimo 0,25 m.** El SPT es *"poco representativo"* y *"tiende a sobrestimar la compacidad relativa"* | CIRSOC 401 art. 3.6.7 y C 3.6.7 |

> **Recomendación de oficina [PD]:** no es "calicata **o** SPT", es **las dos cosas** — 2 a 3 calicatas de
> 1,50–2,50 m con dama de ≥0,25 m bajo la impronta de la casa, **más** 1 sondeo con SPT hasta 6 m para
> completar la profundidad reglamentaria y **medir la napa estabilizada** (`suelo` §6.3).

### Pliego del estudio — lo que hay que pedir sí o sí

Texto completo para copiar y pegar en `suelo` §6.4. Lo que **no puede faltar**:

1. **3 calicatas** de 1,50 m mínimo, o hasta el techo de tosca sana **más 0,50 m de penetración en ella**, dentro de la impronta y acotadas en plano.
2. **Muestreo inalterado en damas de lado ≥ 0,25 m** de cada estrato representativo sobre la napa.
3. **1 sondeo SPT hasta 6,00 m**, o hasta atravesar la tosca **y reconocer el estrato inmediato inferior**.
4. **Nivel freático medido, estabilizado a 24 h, con fecha y hora**, más **opinión escrita sobre variación estacional y tendencia**.
5. **Doble ensayo edométrico** (probeta a humedad natural y probeta saturada) sobre muestra inalterada → **potencial de colapso PC** y **presión de fluencia saturada σ_F.SAT**. Clasificación como **no colapsable / potencialmente colapsable / autocolapsable**.
6. **σ_adm indicada por separado a humedad natural Y en condición saturada**, con tipo de fundación supuesto, ancho B, profundidad Df y factor de seguridad.
7. **Cota del techo de tosca en cada punto, su espesor, qué hay debajo, y opinión expresa sobre continuidad lateral bajo la impronta.**
8. **Análisis químico** (sulfatos, cloruros, sales solubles totales, pH, materia orgánica) + **clase de exposición CIRSOC 201** y tipo de cemento. *Es el ensayo más barato y el más olvidado, y después de hormigonar no hay reparación posible.*
9. **Módulo de balasto** con su ancho de referencia si se recomienda platea.
10. **Asentamiento total y diferencial estimado en ambas condiciones de humedad.**
11. **Recomendación explícita de tipo y cota de fundación** y de tratamiento del suelo (sustitución, espesor, densidad Proctor). **Firma de matriculado con incumbencia en geotecnia [FIRMA]**.
12. **Reunión previa:** el geotécnico recibe el anteproyecto **antes** de ejecutar los trabajos.

### Cómo se lee el informe (no empezar por la tensión admisible)

Orden: plano de ubicación → fecha → napa y su fecha de lectura → perfil y **dónde está la tosca en cada punto**
→ ¿hay doble edométrico? → σ_adm ¿a qué humedad, para qué B y Df? → asentamientos → química → firma
(`suelo` §6.5).

**Señales de alarma:** una sola perforación · sin doble edométrico en suelo limoso · σ_adm sin aclarar
condición de humedad · *"se recomienda fundar a 1,00 m con 1,5 kg/cm²"* y nada más · sin análisis químico ·
perfil "tipo" que no corresponde a los pozos · napa "no detectada" sin decir hasta qué profundidad.

**La pregunta que se hace siempre, por escrito:** *"¿Esta tensión admisible es a humedad natural o en condición
saturada? ¿Cuál me recomienda adoptar para una casa que va a tener riego y jardín alrededor?"* Para una casa
baja **el valor que gobierna es el saturado** (`suelo` §5.2 y §6.6).

---

# FASE 2 — El partido

## 2.1 El conflicto central: en Santa Rosa el sol y el viento vienen del mismo lado

> **En el hemisferio sur el sol viene del NORTE. En Santa Rosa el viento también viene del NORTE.**
> **La orientación óptima de asoleamiento y la de máxima exposición al viento son la misma. Este es EL
> problema de proyecto de una casa en Santa Rosa y todo lo demás se deriva de acá** (`viento` §4.1).

| | **NORTE** | **SUR** |
|---|---|---|
| Asoleamiento | Sol todo el año. Altura al mediodía: **76,9 °** el 21/12, **30,0 °** el 21/06 | **Sin sol directo en invierno** |
| Viento | **34 % del tiempo, 18 km/h, 46 % de la carga acumulada** | **18 % del tiempo, 18 km/h, 25 % de la carga** |
| Temperatura del viento | Cálido y seco (norte pampeano) | **Frío** (Pampero y entradas del S) |
| En verano | Sol alto → **fácil de sombrear con alero**; viento = **recurso** de ventilación | Viento fresco = **recurso** |
| En invierno | Sol bajo → **ganancia solar deseada**; viento = molestia moderada | Viento frío = **problema**, pérdidas |

### La estrategia, en cuatro reglas

| Orientación | Regla | Por qué |
|---|---|---|
| **NORTE** | **FILTRAR, no bloquear** | El viento N es cálido y coincide con el sol; **no es el que rompe cosas**. Una barrera opaca al N mata el asoleamiento de invierno y no hace falta |
| **SUR** | **CERRAR** | Fachada compacta, aberturas mínimas, locales de servicio, **la mejor aislación y el mejor sellado de la casa** |
| **ESTE / NORESTE** | **EXPANDIR** | 9 % del tiempo a 13 km/h. Sol de la mañana sin sobrecalentamiento. **La mejor orientación para el patio de uso y para los dormitorios** |
| **OESTE / NOROESTE** | **EL LADO TRANQUILO — pero el sol peor** | Menos del **10 %** de la carga de viento acumulada. Es el sol de la tarde de verano: quincho con parral o pérgola caduca |

### Dónde va cada cosa

| Espacio | Ubicación | Fundamento |
|---|---|---|
| **Galería principal / expansión del estar** | **NORTE**, acotada lateralmente y con filtro en el borde N | Única orientación con sol de invierno (`viento` §4.2) |
| **Patio de estar / parrilla / pileta** | **NE o E**, con la casa cerrando el S y barrera porosa al N | Menor exposición entre las orientaciones con sol útil |
| **Quincho / parrilla cerrada** | **W o NW**, adosado, con parral o pérgola caduca | Sector de menor carga de viento (3,2 % + 1,7 %); el sobrecalentamiento lo resuelve la vegetación |
| **Tendedero** | **N o NE, expuesto** | **El único caso donde la exposición al viento es un activo**: 156 días de viento fuerte secan ropa |
| **Cochera, depósito, tanque, lavadero** | **SUR o SW** | Amortiguan la fachada fría y no requieren confort |
| **Dormitorios** | **E y NE** | Sol de mañana, viento moderado, ventilación cruzada al S |

### Configuraciones de planta

| Configuración | Veredicto | Motivo |
|---|---|---|
| **Barra E-O con galería al N, cerrada en los testeros E y O** | ✓ **Muy buena** | Fachada N larga con sol; los testeros cortan el flujo lateral; fachada S ciega |
| **"L" con el brazo N-S sobre el lado O del lote** | ✓ **Muy buena** | Genera **patio NE protegido por dos lados**; el brazo O protege además del sol de la tarde |
| **"C" abierta al E o NE** | ✓ Buena | Tres lados de reparo, abertura hacia el sector de menor carga |
| **"U" abierta al N** | ✗ **Mala** | **Efecto embudo:** acelera el viento dominante justo donde se quiere estar. Peor que sin brazos |
| **Barra N-S** | ✗ Mala | Máxima superficie al E y al O, mínima al N |
| **Casa exenta en el centro del lote** | ✗ Regular | Sin lado protegido: obliga a barreras en todo el perímetro |
| **Patio claustro** | ✓ Térmicamente excelente / ✗ costoso | En lote urbano estándar de Santa Rosa suele no entrar |

*(`viento` §4.3)*

### Los seis errores que generan túnel de viento (`viento` §4.4)

1. **Pasillos entre medianera y casa de menos de 1,5 m** → efecto Venturi. O se ensancha, o se cierra con portón macizo del lado de barlovento.
2. **Pasajes bajo la casa o bajo la galería** (pilotis parciales). Si hay desnivel, cerrar el zócalo.
3. **Aberturas enfrentadas N-S sin control.** Excelentes para ventilar, inutilizables sin regulación fina.
4. **Patio embudo** entre dos volúmenes que convergen hacia sotavento.
5. **Barreras opacas altas y cortas.** La longitud mínima útil de una barrera es **10 veces su altura**.
6. **Aleros continuos sin interrupción en el frente de barlovento**, que trabajan como ala.

## 2.2 La galería: el dispositivo que resuelve el conflicto

**No es nostalgia: es un dispositivo bioclimático de precisión** (`envolvente` §8.6).

```
Sol de invierno (30°) bajo la galería:   P = h × 1,732
    h = 2,60 m  →  entra 4,50 m adentro del local
    h = 2,80 m  →  entra 4,85 m
    h = 3,20 m  →  entra 5,54 m

Sombra completa en verano (77°):  basta profundidad ≥ h / 4,289
    h = 2,80 m  →  profundidad ≥ 0,65 m   (cualquier galería real lo cumple)
```

> **La galería sombrea totalmente en verano con cualquier profundidad razonable y deja entrar el sol de
> invierno hasta 5 m si tiene altura suficiente. LA ALTURA DE LA GALERÍA IMPORTA MÁS QUE SU PROFUNDIDAD.
> Una galería baja (2,40 m) al norte bloquea el sol de invierno y es un error térmico.**

| Regla | Valor |
|---|---|
| **Galería al NORTE** | **Altura 2,80–3,20 m · profundidad 2,50–3,00 m** |
| **Galería al OESTE** | Profunda **y con el testero oeste cerrado** con celosía o vegetación: el sol de las 17 h entra horizontal por el lateral |
| **Piso de la galería** | Material **claro**; un piso oscuro se calienta y reirradia hacia el interior |
| **Estructura** | **Independiente de la del muro**, o con el vínculo aislado: una losa de galería continua con la estructura del muro es un puente térmico de primer orden |
| **Techo de la galería** | No es envolvente y no hace falta aislarlo, pero **claro o ventilado**: una chapa oscura a 2,80 m vuelve la galería inhabitable en enero |

### El borde norte de la galería — el detalle más rentable del proyecto

Con altura solar de **30 °** al mediodía de invierno, un parapeto de altura `h_p` proyecta `1,73 × h_p` de
sombra hacia adentro (`viento` §4.2):

| Altura del parapeto | Sombra al mediodía de invierno | Efecto sobre el viento a 1,0 m del suelo |
|---|---|---|
| 0,90 m | 1,56 m | Reparo parcial del cuerpo sentado |
| **1,00–1,10 m** | **1,73–1,90 m** | **Buen reparo sentado, con sol sobre el torso** |
| 1,50 m | 2,60 m | Reparo de pie, pero sombrea toda la profundidad útil en invierno |

> **Solución recomendada:** **parapeto macizo de 1,00–1,10 m + pantalla porosa (40–50 % de vacíos) de
> 0,80–1,00 m encima**, hasta 1,80–2,10 m de altura total. El macizo protege al ocupante sentado; la porosa
> evita la turbulencia de una barrera opaca alta y deja pasar sol filtrado (`viento` §4.2 y §5.5).

## 2.3 Barreras de viento: la porosidad manda

**Lo que determina el tamaño y la calidad de la zona de calma no es cuánto se opone la barrera, sino cuánto
la deja pasar** (`viento` §5.1).

| Tipo | Porosidad | Comportamiento |
|---|---|---|
| Densa | < 15 % | Reducción máxima (85 %) **inmediatamente detrás**, y después turbulencia y recirculación. **Zona protegida corta** |
| **Semipermeable** | **15–45 %** | **Reducción alta sobre una zona larga y sin turbulencia. Es la correcta para una casa** |
| Permeable | > 45–50 % | Reducción moderada pero muy extendida |

**Dimensionado en un lote urbano** — barrera semipermeable, R₁ de Peri (1998), `viento` §5.3:

| Altura **H** | Máxima protección (**4 H**, R₁ ≈ 75 %) | Fin de zona protegida (**15 H**) | Uso típico |
|---|---|---|---|
| **1,8 m** (cerco / seto bajo) | 7,2 m | 27 m | Reparo de una galería adyacente |
| **2,2 m** (medianera con celosía) | 8,8 m | 33 m | Patio pegado a la casa |
| **3,0 m** (seto formado / panel) | 12 m | 45 m | Patio + pileta |
| **5,0 m** (árboles de 5–8 años) | 20 m | 75 m | Fondo del lote completo |

**Cómo se usa en el proyecto:**

1. Marcar **dónde se va a estar** (galería, parrilla, mesa, pileta).
2. Medir la distancia **D** desde ese punto al borde N del lote.
3. **H ≈ D / 4** para máxima protección; **H ≥ D / 10** para protección aceptable.
4. **Si la barrera está a menos de 1 H, no protege: turbulenta.**
5. **Longitud ≥ 10 H**, y en todo caso ≥ 3 veces el ancho del área a proteger. Para una galería de 6 m, la barrera N debe medir **10–12 m de largo, no 6**.
6. **Orientación perpendicular al N ± 45 °.** Fuera de ese sector la protección cae rápido. Una barrera E-O protege del N, NE y NW; una NE-SO no protege del N.
7. **Las brechas son peores que la ausencia de barrera** en la brecha misma.

**Estrategia recomendada — barrera compuesta** (`viento` §5.5):
`muro bajo macizo 1,00 m + celosía 40–50 % de 0,80–1,00 m + vegetación semipermeable detrás (3–5 m)`.
El muro protege desde el día 1; la celosía evita la turbulencia; la vegetación sube la altura efectiva de
2,0 a 5,0 m en 5–8 años y **multiplica por 2,5 la zona protegida**.

**Especies** (`viento` §5.4): *Cupressus sempervirens* y *Casuarina* spp. como barrera perenne (protegen
también en invierno); *Ligustrum* para seto formado de 2–3 m (**precaución: invasor y muy alergénico**);
fresno, morera sin fruto o parra para **filtro estacional al norte** (caducos: dan sombra en verano y sol en
invierno, **pero como barrera de viento en invierno no cuentan**). **No conviene** álamo, sauce ni paraíso en
lote chico: raíces agresivas cerca de fundaciones y cloacas, madera frágil.

> ⚠ **Y la restricción que viene del suelo, no del viento:** ningún árbol mediano a menos de **3,00–5,00 m**
> del perímetro de fundación, y los grandes o de raíz agresiva a **5,00–10,00 m [PD]** (`suelo` §8.6).
> Los dos criterios —barrera y fundación— se resuelven juntos o se contradicen.

## 2.4 Zonificación día / noche / servicio

| Zona | Orientación | Contenido | Criterio |
|---|---|---|---|
| **DÍA** | **N** (estar-comedor) con expansión al **NE/E** | Estar, comedor, cocina | Ganancia solar directa de invierno + alero calculado. Es donde va el **55–65 % de toda la superficie vidriada de la casa** |
| **NOCHE** | **E / NE** | Dormitorios | Sol de mañana, viento moderado, ventilación cruzada hacia el S. Las ventanas se ubican respetando los **3,00 m al eje divisorio** (CE 3.8.1) |
| **SERVICIO** | **S / SW / W ciego** | Cochera, lavadero, depósito, baños, despensa, sala de caldera | Amortiguan la fachada fría; **no abrir al oeste** es la única solución perfecta al problema de verano y **es gratis si se toma en el anteproyecto** |

**Distribución de la superficie vidriada** (`envolvente` §5.7). La IRAM 11603 recomienda para Zona IV una
relación vidriado/opaco **≤ 15 %**, *"pero eso es sobre el TOTAL, no sobre cada fachada. Ahí está la salida de
proyecto: no se distribuye parejo, se concentra al norte"*:

| Fachada | % de la superficie vidriada total | Por qué |
|---|---|---|
| **NORTE** | **55–65 %** | Única orientación donde el vidrio gana más de lo que pierde en el balance invernal |
| **ESTE** | 15–20 % | Sol de mañana, agradable en invierno y tolerable en verano |
| **OESTE** | **5–10 %, y protegido** | Cada m² sin protección es una carga de refrigeración enorme |
| **SUR** | **10–15 %, lo indispensable** | Solo pierde. Se abre lo necesario para ventilación cruzada e iluminación de servicios |

**Cuatro recursos para tener luz sin superficie vidriada:** ventanas altas (clerestorios) al norte —una franja
de 40–60 cm bajo el techo ilumina hasta 2,5 veces su altura hacia adentro—; **locales pasantes N-S** (doble
iluminación con la mitad de vidrio por lado, y ventilación cruzada de regalo); colores interiores claros y
techo blanco; y la galería al norte.

> **El argumento contra el ventanal grande "porque da al jardín":** un ventanal de 12 m² con la mejor ventana
> disponible (K = 2,13) pierde **25,6 W/K**, lo mismo que **88 m² del muro recomendado** (K = 0,29) — en una
> casa de 130 m², toda la fachada. El equilibrio: superficie razonable (8 m², no 12), el mejor vidrio,
> **persiana o cortina pesada que se cierre de noche** (−0,3 a −0,5 W/m²K) y **masa térmica en el piso frente
> al ventanal** para acumular la ganancia (`envolvente` §5.7).

## 2.5 Ventilación: en Santa Rosa el problema no es conseguirla, es controlarla

Con **1,2 % de calmas anuales** (0,8 % en verano), **16,8 km/h de media en enero** y el eje dominante N-S
coincidiendo con el eje óptimo de la casa, **la ventilación cruzada funciona sola**. Con **1 m² de abertura
efectiva y viento medio se alcanzan 24 renovaciones por hora** en una casa de 120 m² (`viento` §10.2).

Y para la **ventilación nocturna de verano** —la estrategia de refrigeración de mayor rendimiento por peso
invertido, con 14,4 K de amplitud térmica estival y mínimas medias de 15–16,5 °C— **bastan menos de 0,2 m² de
abertura efectiva: dos banderolas de 0,40 × 0,30 m opuestas** (`viento` §10.3 · `envolvente` §8.3).

> **Regla de oro: en Santa Rosa la ventilación natural no se dimensiona por caudal, se dimensiona por
> control.** El caudal está garantizado por el clima; lo que hay que proyectar son los dispositivos que
> permiten graduarlo (`viento` §10.5).

**Lo que hay que resolver en el partido para que funcione:**

- **Toda abertura N y S necesita al menos tres posiciones de apertura, no dos.** Una corredera abierta 10 cm ya ventila una habitación entera.
- **Banderolas altas, celosías regulables y ventilaciones altas** antes que abrir la hoja principal: dan control fino y no meten polvo a la altura de la mesa.
- **Banderolas nocturnas con reja fija, mosquitero y alero** que permita dejarlas abiertas con lluvia (54 días de tormenta y 37 de polvo al año).
- **Recorrido de aire libre**: puertas interiores con paso inferior o superior; si el aire entra al norte y la puerta del dormitorio está cerrada, no hay barrido.
- **Masa térmica accesible al aire:** losa vista o cielorraso aplicado, **no colgado**; piso sin alfombra. *Si no hay a qué enfriar, la ventilación nocturna no sirve.* Es el argumento decisivo a favor de la cubierta pesada.
- **Amortiguar la entrada:** que el aire entre por una abertura no orientada directamente al N, o que atraviese primero un espacio de transición (galería, hall, patio protegido).

## 2.6 La cochera

| Decisión | Criterio |
|---|---|
| **¿Es obligatoria?** | **Sí en R2a y R2e** ("obligatoria en todo el distrito, 1 módulo mínimo por vivienda"). En el resto: **1 espacio guarda-auto** (`urb` §2.1) |
| **Medida** | **15 m² (CUA) · lado 2,90 m y altura 2,40 m (CE)** si además sirve de acceso peatonal — el caso normal entre medianeras. **Adoptar lo más exigente** (`urb` §4.10 y §8) |
| **¿Computa FOS?** | **Sí, sin bonus.** Se resta de los 216 m² del ejemplo (`urb` §3.1 punto 6) |
| **¿Dónde va?** | Preferentemente **al SUR o al SW**, o en la franja de fondo (es "dependencia de servicio" admitida en el retiro de 3 m, en una sola planta ≤ 4,50 m). **Nunca al norte si se puede evitar** |
| **El portón es un elemento estructural** | Si el portón cede en una tormenta, la casa pasa de cerrada a parcialmente cerrada (GC_pi de ±0,18 a ±0,55) y **la succión sobre TODO el techo aumenta un 45 %**. No falla el techo: falla una abertura y después falla el techo. Sobre un portón de 2,50 × 2,20 m actúan **≈ 12 kN mayorados** (`viento` §8.9 y §9.1) |
| **Alternativas de proyecto** | Separar el garaje del volumen habitable, o **ventilarlo permanentemente** para que no pueda presurizar la casa, con puerta interior estanca entre garaje y vivienda. Si el garaje da al **norte** (34 % del tiempo), el problema se agrava |
| **Muro divisorio con la cochera no calefaccionada** | Se trata como envolvente; el piso computa al **50 %** en ese tramo (`envolvente` §6.9, puente térmico n.º 10) |

## 2.7 Dónde va el C.A.S. sin poner agua contra la fundación

Este es el cruce más delicado del partido en Santa Rosa: **el C.A.S. empuja a infiltrar agua en el lote,
justo donde el loess colapsa al saturarse** (`marco` §2.1).

**El principio (`suelo` §8.1):** *"En loess colapsable, el manejo del agua es un asunto estructural. Una
fundación correctamente calculada, ejecutada sobre un manejo del agua incorrecto, falla igual."*

**Las tres franjas del lote, de adentro hacia afuera:**

```
        ┌──────────────────────── LOTE ─────────────────────────┐
        │  CASA  │ VEREDA PERIMETRAL │  JARDÍN / C.A.S.          │
        │        │ 1,20–1,50 m       │  suelo permeable          │
        │        │ IMPERMEABLE       │  riego, canteros, árboles │
        │        │ pendiente ≥2 %    │                           │
        │        │ junta elástica    │  pozo absorbente ≥5,00 m  │
        │        │ sellada           │  pileta ≥5,00 m           │
        └────────┴───────────────────┴───────────────────────────┘
                 └─ el jardín empieza acá, no antes ─┘
```

| Elemento | Distancia mínima al perímetro de fundación | Origen |
|---|---|---|
| **Vereda perimetral impermeable (ancho)** | **1,20 m mínimo / 1,50 m recomendado**, pendiente **≥ 2 %** hacia afuera (3 % si recibe descarga de cubierta) | Verificado, bibliografía de loess |
| **Descarga de pluviales** | **≥ 3,00 m** | Verificado |
| **Cantero, césped o superficie regada** | **≥ 1,20 m** (borde exterior de la vereda) | [PD] |
| **Aspersor de riego** | **≥ 2,00 m**, orientado hacia afuera | [PD] |
| Arbusto / árbol pequeño (<5 m) | ≥ 2,00 m | [PD] |
| Árbol mediano (5–10 m) | 3,00 – 5,00 m | [PD] |
| **Árbol grande / raíz agresiva** (eucalipto, álamo, sauce, ficus, paraíso, mora) | **5,00 – 10,00 m**, idealmente ≥ 1 vez la altura adulta | [PD] |
| **Pozo absorbente** | **≥ 5,00 m** — y si no entra, **cambiar de sistema** | [PD] |
| **Pileta de natación** | **≥ 5,00 m**, aguas abajo de la casa | [PD] |
| Cañería enterrada paralela al muro | ≥ 1,00 m, envainada | [PD] |

*(Tabla maestra completa en `suelo` §8.8)*

**Cómo se resuelve el C.A.S. en la práctica:**

1. **El suelo absorbente va en el patio, más allá de la vereda perimetral, y preferentemente aguas abajo de la casa.** Nunca como cantero contra el muro (`marco` §2.1).
2. **La vereda perimetral no es negociable y no computa como C.A.S.** (es solado impermeable). Se dibuja y se presupuesta.
3. En el ejemplo del lote de 12 × 30 m en R3: 72 m² permeables sobre 144 m² de descubierto. Descontando la vereda perimetral (≈ 12 m de perímetro libre × 1,50 m ≈ 18 m² del lado del patio) **queda margen**, pero hay que dibujarlo, no suponerlo.
4. **El plano municipal exige graficar el "límite de solado, terreno absorbente"** (`urb` §5.4, lámina 1).
5. **[VERIFICAR en Planeamiento]** si un piso permeable (adoquín con junta abierta, grava, césped reforzado) computa como suelo absorbente o solo la tierra desnuda (`urb` §8, punto 6).

**Nivelación general del lote:** pendiente que **aleja el agua superficial de la construcción en todas las
direcciones**. Si el lote recibe escorrentía del vecino, se resuelve con **cuneta perimetral conducida antes de
empezar la obra** (`suelo` §8.3).

> **La consigna que se le dice al comitente desde la primera reunión: el jardín empieza a 1,50 m de la casa**
> (`suelo` §8.6).

## 2.8 Módulo polivalente: la carta que conviene tener sobre la mesa

El CUA (art. 4.3.1.3) permite en **todos los distritos urbanos** un **módulo habitable polivalente** de
**superficie útil mínima 30 m²**, en planta baja, de un solo ambiente más baño, **admitiéndose cocina
integrada**. Un único módulo por parcela. Si va en el fondo, **no puede ampliarse ni anexársele locales**;
si se vincula a la vivienda, hay que preservar un espacio descubierto de **4 m de lado mínimo** entre ambas
construcciones, y debe estar **separado 3 m del eje divisorio** (`urb` §2.3).

**Lectura del estudio:** es la vía legal para el "departamento del fondo", el consultorio, el taller o el
estudio. Vale ofrecerlo en la primera reunión, **diciendo con claridad que es uno solo y que no se puede
ampliar**. **[VERIFICAR en Planeamiento]** si computa FOS, si computa densidad y si exige cochera propia
(`urb` §8, punto 8).

---

# FASE 3 — Las decisiones técnicas que se toman en anteproyecto y no después

> Las ocho decisiones de este capítulo **cuestan casi nada mientras el proyecto es un croquis y son
> irrecuperables después**. La aislación perimetral del piso, por ejemplo, **se hace o no se hace nunca**:
> no se puede aislar el perímetro de una casa terminada sin romper la vereda y el contrapiso
> (`envolvente` §9.3).

## 3.1 Fundación — **platea de hormigón armado con vigas de borde**

> ### **Platea de H°A° con vigas perimetrales y nervios de rigidización bajo muros portantes, apoyada sobre manto de suelo seleccionado compactado, con la cota de fundación por debajo de la capa activa** (`suelo` §7.3)

### Por qué

1. **Es la respuesta correcta al problema real, que es la heterogeneidad.** El riesgo dominante en Santa Rosa no es que el suelo no aguante: es que **aguante distinto en cada punto** (tosca errática, relleno urbano, humedecimiento local). La platea **promedia** esa heterogeneidad.
2. **Convierte fisura en desnivel.** Con una casa liviana de mampostería, la diferencia entre fundación rígida y flexible es la diferencia entre una casa que se inclina 1 cm y una casa rajada de punta a punta.
3. **Es literalmente la receta publicada para este suelo:** *"suele dar mejor resultado la adopción de medidas de diseño que minimicen el riesgo de ingreso de agua al terreno, o mejoras en el terreno mediante sustitución de suelo combinados con plateas que disminuyan significativamente las presiones en el suelo"* (Rocca–Redolfi–Terzariol).
4. **Baja la presión de contacto por debajo de la presión de fluencia saturada.** Ese es el objetivo mecánico concreto: `σ_actuante < σ_F.SAT` **con el suelo mojado**.
5. **Tolera napa somera** (con barrera de vapor), que es el escenario probable de los próximos 30 años.
6. **Su sobrecosto neto es modesto**, porque reemplaza contrapiso y carpeta: costo relativo 1,6–2,2 sobre una zapata corrida, que baja a **~1,3–1,6 [PD]** una vez descontado eso.

### Predimensionado orientativo [PD] — se calcula y se firma con el informe en la mano [FIRMA]

| Ítem | Valor orientativo | Lo define |
|---|---|---|
| Espesor de losa | **0,15 – 0,20 m** | Cálculo con módulo de balasto del informe |
| Armadura | Mallas en ambas caras y direcciones, con refuerzos bajo muros | Cálculo |
| **Viga perimetral** | **0,25 – 0,30 m de ancho × 0,40 – 0,50 m de altura** | Cálculo + cota de fundación |
| Nervios interiores bajo muros portantes | 0,20 × 0,30–0,40 m | Cálculo |
| **Cota de fondo de viga perimetral** | **≥ 0,80 m bajo terreno natural** | Informe geotécnico |
| Manto de suelo seleccionado compactado | **0,30 – 0,60 m**, en capas de ≤ 0,20 m, **≥ 95 % Proctor estándar** | **[VERIFICAR con estudio de suelos]** |
| Film de polietileno | **200 μm**, continuo, solapes ≥ 0,20 m sellados, subiendo por los bordes | — |
| Hormigón | Según **clase de exposición CIRSOC 201** del análisis químico | Informe químico |
| Tensión de contacto resultante | **0,25 – 0,50 kg/cm²** | **Verificar contra σ_adm SATURADA** |

### Profundidad de fundación: tres criterios simultáneos, manda el más profundo (`suelo` §7.1)

1. **Salir del suelo vegetal y del relleno antrópico** (típicamente 0,30–0,80 m en lote urbano).
2. **Salir de la capa activa** (variación estacional de humedad, desecación, raíces): **[PD] 0,80–1,00 m**.
3. **Alcanzar el estrato de apoyo recomendado.**

> **Criterio de oficina [PD]: no fundar por encima de 0,80 m del terreno natural**, salvo que el informe lo
> justifique **por escrito**.

### Cuándo NO es la platea

| Situación | Alternativa |
|---|---|
| **Tosca sana, continua y somera verificada bajo TODA la casa** (p. ej. 0,60–1,00 m en todos los puntos) | **Viga de fundación con base ensanchada apoyada en tosca**: más barata y perfectamente adecuada. Y si la tosca es madura, continua y sin crotovinas, la solución más limpia es **remover íntegramente el manto eólico bajo la casa y apoyar la platea sobre la tosca limpia**, con hormigón de limpieza inmediato |
| **Suelo autocolapsable** identificado por el informe | **Ninguna fundación directa sirve.** Tratamiento de suelo o fundación profunda con diseño por punta y fricción negativa **[FIRMA]** |
| Relleno profundo (> 1,5 m) no removible | Pilotines a tosca, o sustitución total del relleno |
| Terreno con mucha pendiente o desniveles internos | Platea escalonada o combinación, caso por caso |
| Napa prácticamente aflorante | Platea **con** verificación de subpresión y barrera hidráulica **[FIRMA]** |

### Las dos advertencias que hay que grabarse

> **1. Apoyo mixto = asentamiento diferencial garantizado.** Apoyar media zapata sobre tosca y media sobre
> limo suelto es la receta exacta. **Si la tosca es errática bajo la casa, la respuesta correcta no es "seguir
> la tosca": es no apoyarse en ella** y resolver con platea sobre manto compactado uniforme (`suelo` §7.1).
>
> **2. Ninguna fundación resuelve el colapso por sí sola.** Ni la zapata, ni la viga, ni la platea, ni los
> pilotines. El colapso se evita con el **manejo del agua** de §2.7 y §6.3 (`suelo` §7.2).

**Y sobre los pilotines "por las dudas":** *"existen numerosos casos donde este tipo de solución no ha sido
satisfactoria [...] aún estructuras fundadas sobre pilotes han sufrido daños de importancia al colapsar el
suelo que las rodea"*, por pérdida de fricción lateral y fricción negativa. Además, la casa queda quieta
mientras el terreno de alrededor baja: se rompen veredas, contrapisos, cañerías y escalones (`suelo` §7.2).

### Decisiones asociadas que se toman acá

- **Sin subsuelo.** Recomendación por defecto en Santa Rosa: con napa a 5 m, un sótano de 2,5 m está seco hoy y puede no estarlo en 15 años. Subpresión `u = γw·h` = **10 kPa por cada metro de columna**. Si se hace: recinto estanco + verificación de flotación **[FIRMA]** (`suelo` §3.4).
- **Encadenar la mampostería**, aunque el sismo no lo exija: el factor R de la Tabla 5.1 del CIRSOC 103 pasa de **1,5 sin encadenados a 3,0 o más** con ellos. **En La Pampa encadenar es la mejor protección contra el asentamiento diferencial por colapso del loess** (`marco` §5.1).
- **Capa aisladora horizontal Y vertical**, continua, sin discontinuidades (`suelo` §7.5).
- **Ninguna cañería con empalmes bajo la platea ni bajo muros portantes.** Los empalmes van en cámaras accesibles (`suelo` §8.4).

## 3.2 Muro — **hueco 18 + SATE de EPS 100 mm**

> ### **M4 — Ladrillo cerámico hueco 18 revocado + SATE de EPS de 100 mm · K = 0,29 W/m²K · Nivel A de IRAM 11605** (`envolvente` §2.5)

**Composición (de interior a exterior), espesor total 31,8 cm:**

```
Revoque fino a la cal 5 mm + revoque grueso 20 mm
LADRILLO CERÁMICO HUECO 18×18×33, junta de mortero 1:1:4
Mortero adhesivo cementicio del sistema SATE, 5 mm (cordón perimetral + pelladas)
PLACA DE EPS 20 kg/m³, 100 mm, a junta trabada
Fijación mecánica con espigas plásticas de expansión larga (para ladrillo hueco),
  cantidad y longitud según manual del fabricante y zona de viento CIRSOC 102 [VERIFICAR],
  cabeza rehundida y tapada con tapón de EPS
Capa base 3–5 mm con MALLA DE FIBRA DE VIDRIO ANTIÁLCALI embebida
  + refuerzo diagonal de 30×50 cm a 45° en cada esquina de vano
Segunda capa 2–3 mm + imprimación
Revestimiento acrílico/siliconado texturado 1,5–3 mm, PERMEABLE AL VAPOR, color claro
```

### Por qué esta y no otra

| Criterio | Por qué gana |
|---|---|
| **Verifica Nivel A** | 0,29 ≤ 0,30. No "casi": verifica |
| **Resuelve TODOS los puentes térmicos de la envolvente vertical** | El aislante pasa continuo por delante de columnas, encadenados, dinteles y antepechos. **Es la única familia de soluciones que permite cumplir K_pt ≤ 1,5 × K_muro**, que con K_muro 0,29 exige **K_pt ≤ 0,45** — imposible con aislación interior o en cámara. *(El encadenado desnudo tiene K = 2,92: excede 6,5 veces el admisible.)* |
| **Deja la masa del lado correcto** | Los ~250 kg/m² quedan en contacto térmico con el aire interior: con **14,4 K de amplitud estival**, la inercia vale tanto como el aislante |
| **Estanqueidad al aire** | La capa base continua de mortero armado con malla **es** la barrera al aire de la fachada. Con viento medio de 10–12,5 km/h, esto pesa tanto como el K |
| **No pierde superficie útil** | El espesor crece hacia afuera |
| **Escalable** | El mismo detalle sirve para 60, 100 o 150 mm: si el presupuesto aprieta se arranca en 60 (Nivel B, K 0,43) **sin cambiar ningún otro detalle de obra** |

### Alternativas admitidas

| Situación | Solución |
|---|---|
| El comitente quiere **ladrillo visto** | **M6**: muro doble con hoja exterior de ladrillo visto y EPS 100 en la cámara (K ≈ 0,28), **cámara ventilada y drenada**. Cuesta ~30 % más y 8 cm más de espesor |
| Se quiere **ahorrar estructura** | **M7b**: cerámico **portante** 18 + SATE EPS 100 (K = 0,29). Menos hormigón, menos puentes de origen |
| **Bajo peso sobre fundación en loess** | **M9c**: HCCA 20 + SATE EPS 60 (K = 0,28, 27 cm) |
| **Presupuesto ajustado, se acepta Nivel B** | **M3**: SATE EPS 60 (K = 0,43). **Nunca por debajo de 30 mm de EPS** |

### Lo que NO se acepta en un proyecto del estudio

- **Hueco 18 revocado sin aislante** (K = 1,58: **no verifica ni Nivel C**, y es el muro del 90 % del parque construido).
- Bloque de hormigón revocado sin aislante (K = 2,36).
- **Muro doble con cámara de aire vacía** (K = 0,86: con la TDMN correcta **ya no verifica Nivel B**).
- **"Aislación: manta reflectiva de 10 mm" como único aislante.** Un reflectivo no tiene λ útil: aporta como máximo **0,21 m²K/W = 7 mm de EPS**, y solo con cámara de aire y superficie limpia, cosa que la propia IRAM 11601 dice que no puede asegurarse en obra.

### Piso: el ítem más ignorado y el más barato

**IRAM 11605 no tabula K para pisos en contacto con el terreno; la norma que se usa es la 11604, Tabla 2**
(`envolvente` §1.8):

| Zona III y IV | Sin aislación | **Aislación perimetral** | **Aislación total** |
|---|---|---|---|
| Pérdida Pp (W/m de perímetro) | 1,38 | **1,08** | **0,93** |

- **Aislación perimetral:** capa de **R = 0,7 m²K/W**, ancho mínimo **50 cm**, densidad 25–120 kg/m³, vertical u horizontal → **30 mm de XPS**.
- **Criterio del estudio: perimetral como mínimo; total cuando hay losa radiante.** Es exactamente lo que recomienda la Nota 9 de la norma para suelos húmedos o con napa cercana — el caso de Santa Rosa.
- En una casa de una planta **todo el piso está en contacto con el terreno**, y con envolvente Nivel A el piso representa el **31 % de la pérdida por conducción**. **El espesor que pide la norma es sorprendentemente chico: 30 mm de XPS.** No hay excusa para omitirlo.

## 3.3 Techo — **losa + EPS 120-140 mm + membrana clara**, y por qué manda el verano

> ### **T9/T2c — Losa de viguetas con bovedilla de EPS + EPS 120–140 mm sobre la losa + contrapiso de pendiente + membrana de terminación CLARA · K verano = 0,21–0,23 W/m²K · Nivel A con α < 0,6** (`envolvente` §3.6)

### Por qué manda el verano — la tabla que cierra la discusión

| Nivel | K adm **invierno** (TDMN −6,0) | K adm **verano** (zona III/IV) | Manda | Verano con cubierta clara (α<0,6, +30 %) | ¿Sigue mandando el verano? |
|---|---|---|---|---|---|
| **A** | 0,26 | **0,19** | verano | **0,247** | **Sí** (0,247 < 0,26) |
| Sustentable | 0,47 | 0,34 | verano | 0,442 | Sí |
| **B** | 0,67 | **0,48** | verano | **0,624** | **Sí** (0,624 < 0,67) |
| C | 1,00 | 0,76 | verano | 0,988 | Sí |

> **No hay ningún caso en Santa Rosa, con ningún color, en que el invierno mande en la cubierta. La cubierta
> se dimensiona SIEMPRE por verano.** Y el verano se verifica con **flujo descendente, Rsi = 0,17** (no 0,10).

**Y la razón física:** en verano la cubierta recibe **900 W/m² de radiación de diseño** contra **400 W/m² de
los muros**. En la casa de referencia (130 m², 16 × 8 m) el techo es **130 m² contra 106,8 m² de muro neto**:
**el 41 % de toda la envolvente**. *"En una casa de una planta, el techo es la envolvente."*

**Composición completa (de interior a exterior):**

```
Cielorraso: revoque a la cal 15 mm, o placa de roca de yeso
LOSA DE VIGUETAS PRETENSADAS CON BOVEDILLA DE EPS h=17 cm + capa de compresión 5 cm con malla
                                                              [Rt = 0,63 — aislante gratis]
BARRERA DE VAPOR: film de polietileno 200 μ solapado 15 cm y sellado   ← VA ACÁ, DEL LADO CÁLIDO
EPS 25 kg/m³, 120–140 mm, placas a junta trabada
Film separador
CONTRAPISO DE PENDIENTE, espesor mínimo, pendiente ≥ 1,5 %
CARPETA HIDRÓFUGA 20 mm fratasada
MEMBRANA ASFÁLTICA 4 mm CON FOIL DE ALUMINIO   ← α < 0,6, SIN PINTAR
  (alternativa: membrana geotextil + pintura acrílica reflectiva blanca,
   con repintado cada 4–6 años consignado en el manual de uso)
```

### Por qué esta

- **Verifica Nivel A de verano con cubierta clara** (0,227 ≤ 0,247) y de invierno con muchísimo margen.
- **Masa del lado interior.** La losa (~300 kg/m²) queda por dentro del aislante: **es el volante de inercia de la casa**, y con 14,4 K de amplitud estival + ventilación nocturna es lo que evita usar el aire acondicionado.
- **La bovedilla de EPS es aislante gratis:** Rt 0,63 contra 0,19 de la cerámica. **0,44 m²K/W sin cambiar un solo paso de obra ni un peso de mano de obra**, solo especificando otra bovedilla.
- **El espesor va sobre la losa: no roba altura útil.**
- **Es la cubierta que hace cualquier contratista de Santa Rosa.** Lo único distinto es la bovedilla, el EPS y la exigencia de terminación clara.

### El color de la cubierta: la decisión gratuita de mayor impacto

**α < 0,6 da +30 % de K admisible → ahorra 40 mm de EPS en toda la cubierta**, y baja la temperatura
superficial de ~70 °C a ~45 °C `[VERIFICAR con medición]` (`envolvente` §8.7).

> ⚠ **Y el mantenimiento es parte de la especificación:** con viento y tierra, la cubierta clara pierde
> reflectancia en 3–5 años. **Consignar el repintado o lavado cada 4–6 años en el manual de uso. Si el
> proyecto no puede garantizar ese mantenimiento, calcular con α medio (0,7) y no con α < 0,6.**

### Alternativas admitidas

| Situación | Solución |
|---|---|
| Azotea accesible o mantenimiento difícil | **T3, cubierta invertida** con XPS 140 mm y lastre calculado por succión de viento. La membrana dura el doble |
| Techo inclinado con cielorraso plano | **T8: teja o chapa + ático ventilado + 150 mm de lana de vidrio sobre el cielorraso.** La mejor relación costo/prestación del capítulo |
| Machimbre a la vista | **T7** con **100 mm de EPS mínimo** (80 mm solo si la teja es clara). Verificar el α de la teja |
| Verano crítico (mucho techo al oeste) | **T4, doble techo ventilado.** La mejor cubierta de verano posible; cuesta más |
| Obra rápida y presupuesto acotado | **T6, panel sándwich 100 mm.** Compensar la masa con contrapiso pesado y tabiques de mampostería |

### Lo que NO se acepta

- **Losa sin aislante** (K = 1,83: **2,4 veces por encima del Nivel C**).
- Chapa con solo manta reflectiva de 10 mm.
- **Cubierta oscura** (membrana negra sin pintar, teja roja oscura, chapa prepintada oscura) sin haber recalculado con la corrección de **−20 %**.
- **Lana de vidrio sin barrera de vapor del lado cálido** en cubierta de chapa o de teja. Lana comprimida por las correas.

## 3.4 Cubierta liviana vs. pesada frente a la succión de viento

**En una casa baja el viento no es un problema de estabilidad lateral: es un problema de SUCCIÓN VERTICAL
sobre la cubierta** (`viento` §7.1). Tres razones: el flujo se separa en el borde de barlovento y genera
vórtices cónicos en las esquinas (succiones locales de 3 a 4 veces la presión dinámica); la cubierta es
**≈ 50 % de la envolvente** de una casa de una planta; y el peso propio de una cubierta liviana es
despreciable frente a la succión.

> **La casa no se vuelca: el techo vuela.** Verificación del vuelco global de la casa tipo: momento de vuelco
> ≈ 152 kNm contra momento estabilizante ≈ 2.150 kNm → **factor 14**. **La casa no se vuelca. La casa se
> destecha** (`viento` §8.5).

### El cálculo que decide — casa tipo 10 × 12 m, CIRSOC 102-2005, combinación `0,9 D + 1,6 W` (`viento` §8.4)

| Cubierta | Peso propio | Exposición | `0,9 D` | `1,6 W↑` | **Resultado** |
|---|---|---|---|---|---|
| **A** — chapa sin cielorraso | 0,23 kN/m² | C | 26,5 kN | 177,1 kN | **VUELA. Tracción neta 150,6 kN** |
| **B** — chapa con cielorraso de yeso | 0,38 kN/m² | C | 43,7 kN | 177,1 kN | **VUELA. Tracción neta 133,4 kN** |
| **C** — losa cerámica + teja | 3,20 kN/m² | C | 367,7 kN | 177,1 kN | ✓ Estable, **factor 2,08** |
| **D** — losa H°A° 12 cm + teja | 4,00 kN/m² | C | 459,7 kN | 177,1 kN | ✓ Estable, **factor 2,60** |

> ### **Una cubierta liviana de chapa en Santa Rosa recibe una succión mayorada 4 a 6 veces mayor que su peso estabilizante. El anclaje NO es opcional, NO es un detalle de obra y NO se resuelve "con unos tacos".**
> **Una cubierta pesada se estabiliza sola con factor de seguridad global de 2 a 2,6**, y el problema queda
> reducido a los elementos locales (tejas, cumbrera, borde).

### Criterio del estudio

| Decisión | Consecuencia |
|---|---|
| **Cubierta PESADA** | El viento deja de ser problema global y queda como problema local. **Y sinergiza con la ventilación nocturna** (masa térmica accesible), que es la estrategia de refrigeración de Santa Rosa |
| **Cubierta LIVIANA** | El anclaje pasa a ser **un cálculo estructural con números**, con la cadena de transmisión explícita y **cada eslabón dimensionado** |
| **Híbrido recomendado y frecuente** | **Losa plana de H°A°** (masa térmica, ruido, estabilidad, acústica) **+ cubierta liviana de chapa por encima** para escurrimiento. La chapa se calcula como componente y revestimiento sobre un sustrato que ya es estable. **Es la solución de menor riesgo** |

**Y dos factores no térmicos que pesan en Santa Rosa:** el **ruido** de la chapa con viento y lluvia, con
**156 días de viento fuerte al año**, es un problema de habitabilidad real; y con **3 días de granizo al año**
hay que descartar policarbonato fino y chapas ultralivianas y exigir espesor razonable (`viento` §7.4 y §3.8).

### Si la cubierta es liviana: la cadena de anclaje que hay que dibujar

**Demanda calculada [PD]** (cubierta B, exposición C, cabios cada 0,60 m — `viento` §8.5):

| Zona | Tracción neta de diseño | Por cabio | Solución |
|---|---|---|---|
| **Interior** (10 m centrales) | **5,1 kN/m** | ≈ 3,1 kN (310 kgf) | 1 fleje/zuncho metálico por cabio, anclado al encadenado |
| **Extremos** (2 m en cada una de las 4 esquinas) | **7,8 kN/m (+53 %)** | ≈ 4,7 kN (470 kgf) | **2 flejes por cabio o fleje reforzado**, más 1 barra roscada Ø10 pasante cada 1,2 m |

```
chapa
  ↓ tornillo autoperforante con arandela METÁLICA + EPDM   ← el modo de falla es el pull-through
clavadera
  ↓ tornillo o clavo HELICOIDAL (nunca clavo liso)
cabio / cercha
  ↓ FLEJE / ZUNCHO METÁLICO ← el eslabón que falta en el 90 % de las obras
viga de borde o solera
  ↓ barra roscada / anclaje químico
ENCADENADO SUPERIOR DE H°A° (continuo, sin interrupciones)
  ↓ muro portante  ↓ cimiento
```

**Los cinco puntos donde falla en la realidad:** el fleje no existe · **el encadenado está interrumpido** en el
dintel de una abertura grande (el anclaje ancla a nada) · el clavo es liso · el anclaje se hace con taco de
expansión en hormigón mal ejecutado · **los 2 m de los extremos se tratan igual que el centro**, que es
exactamente donde la demanda es 53 % mayor.

**Fijación de la chapa por zona** (`viento` §7.5): zona 1 (interior) 1 fijación cada 2–3 ondas · **zona 2**
(faja de 1 m en alero, hastial y cumbrera) **1 fijación en cada onda** · **zona 3** (cuadrados de esquina)
1 en cada onda **+ clavadera intermedia** · **alero volado** 1 en cada onda **+ fleje continuo de borde**.
Fijar **en la cresta de la onda, no en el valle**; no sobreapretar; **[VERIFICAR con el fabricante]** la
capacidad de arranque por perforación (*pull-through*) de la chapa especificada.

### Aleros: el punto de mayor succión de toda la casa

El alero recibe presión negativa arriba **y** positiva abajo; por eso sus GC_p (−2,2 en zona 2, **−3,7 en zona
3**) son mucho mayores que los del faldón. Succión mayorada en la esquina de alero: **6,7 kN/m² (684 kgf/m²)**
en exposición C — sobre un alero de 0,60 m son **4,0 kN por metro lineal** intentando arrancarlo
(`viento` §7.6 y §9.2).

**Detalle constructivo obligatorio:**

1. **Cerrar el sofito del alero con tapajuntas continuo.** Un sofito abierto deja que el viento se meta en la cámara del techo y la presurice: es el mecanismo por el que se levantan techos enteros desde el alero.
2. **El alero no puede ser un voladizo de la chapa: el cabio tiene que volar, no la chapa.**
3. **Anclar el voladizo a tracción.** El momento de la succión invierte el esfuerzo respecto del peso propio: la clavija/fleje del apoyo trabaja al revés de lo que sugiere la intuición.

### Si la cubierta es plana

- **Un parapeto de altura ≥ 1 m elimina la zona de esquina**: la Zona 3 se trata como Zona 2, y el GC_p pasa de **−2,8 a −1,8** → **−34 % de presión de diseño en todo el perímetro**. Un antepecho de 1 m no es estética: es economía estructural (`viento` §7.3, Nota 5 de la Fig. 5B).
- **La membrana asfáltica pegada no resiste succión por adherencia:** en el perímetro se **fija mecánicamente** con perfil de borde y luego se sella.
- **Grava suelta como protección: prohibida en Santa Rosa.** Con 156 días de viento fuerte se vuela y se convierte en proyectil, y como la casa es baja, contra los vidrios propios y del vecino. Usar baldosas fijadas o membrana autoprotegida.
- **Los equipos en cubierta (condensadoras, termotanque solar, tanque) se anclan, no se apoyan.**

### La galería independiente NO es parte de la casa

Es una **"cubierta aislada"** con su propio anexo del CIRSOC 102 y coeficientes mucho más severos
(`viento` §9.3). Ejemplo resuelto — galería de 3,00 × 6,00 m, vertiente única a 10°, exposición C:
tracción neta **20,1 kN repartida en 6 columnas = 3,4 kN por columna**.

> **Las columnas de una galería trabajan a TRACCIÓN. No se apoyan: se anclan.** Hacen falta placa de base con
> pernos calculados y un dado de fundación cuyo **peso** equilibre la tracción: **≥ 0,14 m³ de hormigón por
> columna** más coeficiente → un dado de 0,50 × 0,50 × 0,70 m. Y en la faja de borde, fijaciones en cada onda
> en todo el perímetro. **La cenefa/canaleta frontal es de los primeros elementos en irse** (C_pn = 1,3).

### Y la medianera, que es la falla más visible después de cada tormenta

Medianera de mampostería de **2,20 m**, exposición C: demanda **4,5 kNm/m** contra **0,55 kNm/m** de capacidad
por peso propio → **factor 8 en contra**. *"Una medianera de 2,20 m sin pilastras y sin fundación adecuada no
'puede caerse': se cae"* (`viento` §9.4).

**Solución:** pilastras de H°A° cada 3,00 m (momento en la base **13,4 kNm**, columna ≥ 0,20 × 0,20 m
**[VERIFICAR con diagrama de interacción]**, base de al menos 0,80 m de ancho) **+ viga de encadenado de
coronamiento**. **Alternativa mucho mejor de proyecto:** cerco de 2,20 m con la parte superior calada
(30–50 % de vacíos): **33 % menos de carga**, zona protegida más larga y sin turbulencia. *(Ojo: con menos de
30 % de vacíos el reglamento lo calcula como muro macizo.)*

---

## 3.5 Carpinterías y superficie vidriada

### Objetivo de proyecto (`envolvente` §1.7 y §5.6)

| | **Objetivo** | **Piso contractual** |
|---|---|---|
| **K de la ventana completa** | **≤ 2,13** (RPT + DVH low-E) → categoría **K4/K3** IRAM 11507-4 | ≤ 2,82 (RPT + DVH) → **K4** |
| **Infiltración de aire** | **IRAM A2** o mejor (A3 en fachada sur y aberturas grandes del norte) | IRAM A1 |
| **Superficie vidriada / opaca** | **≤ 15 %** sobre el total, concentrada al norte | — |

### K de ventanas completas — IRAM 11507-4, Tabla A.1 (`envolvente` §5.3)

| Tipología | Vidrio simple 6 mm | DVH 6-12-6 | **DVH Low-E 6-12-6** | DVH Low-E c/argón |
|---|---|---|---|---|
| Aluminio **SIN** ruptor de puente térmico | **5,86** | 3,82 | 3,14 | 2,80 |
| Aluminio **CON** ruptor (RPT) | 4,86 | **2,82** | **2,13** | 1,79 |
| Doble ventana con RPT | 1,99 | 1,25 | 0,97 | 0,83 |
| Doble ventana **con cortina de enrollar cerrada** | 1,52 | 1,05 | 0,84 | 0,74 |

> **Una ventana de aluminio sin RPT con vidrio simple NO ES CLASIFICABLE según IRAM 11507-4** (la norma exige
> K < 4,0). No tiene una categoría baja: **está fuera de norma.** Y es la ventana que lleva el 90 % del parque
> construido de Santa Rosa.
>
> **El orden correcto: el RPT primero, el low-E después.** Si hay que elegir entre (a) DVH low-E con marco sin
> RPT (K 3,14) y (b) DVH simple con marco CON RPT (K 2,82), **se elige (b)**: mejor K y, sobre todo,
> **desaparece la condensación sobre el marco**, que es el origen del deterioro.

**Por qué el DVH se justifica siempre en locales de permanencia, y no principalmente por el repago:**

1. **Condensación.** Con vidrio simple (K 5,80), interior a 20 °C y exterior a −6 °C, la cara interior queda a **≈ −5,7 °C**; el rocío interior a 20 °C y 70 % HR es **14,4 °C**. **Condensa masivamente todas las mañanas de invierno.** Con DVH simple la cara interior sube a 7,6 °C; **con DVH low-E, a 12,1 °C**, y con HR interior de 60 % (rocío 12,0 °C) ya no condensa. **El DVH low-E es lo que elimina el problema, no el DVH simple.**
2. **Asimetría radiante.** Sentado a 1 m de un vidrio a −5,7 °C se siente frío aunque el termómetro marque 21 °C, y el usuario sube la calefacción: **la casa con vidrio simple se calefacciona a 23 °C para sentirse a 20**. Ese sobreconsumo no aparece en ningún cálculo de repago.
3. **IRAM 11507-4 exige K < 4,0.** No es una opción de proyecto: es un incumplimiento.

### Vidrio por orientación (`envolvente` §5.2)

| Orientación | Qué se busca | Vidrio | Protección solar |
|---|---|---|---|
| **NORTE** | K bajo **+ factor solar ALTO** | **DVH con low-E de ALTA ganancia solar.** NO control solar | **Alero calculado** (§3.5.1) |
| **OESTE** | K bajo **+ factor solar BAJO** | DVH con **control solar** exterior + low-E interior | **Protección móvil EXTERIOR obligatoria** |
| **ESTE** | Intermedio | DVH incoloro o low-E | Persiana o parasol vertical |
| **SUR** | **Solo importa el K** | **DVH low-E siempre. Superficie mínima** | No hace falta |
| Claraboya | Factor solar bajo obligatorio | Control solar + laminado de seguridad | **Exterior.** Un vidriado horizontal recibe 900 W/m² en verano |

`[VERIFICAR]` El **factor solar (g), coeficiente de sombra y transmisión luminosa (TL)** de cada composición se
piden al proveedor en planilla y se archivan con el legajo: no están verificados en el repo (`envolvente` §11.2).

### El alero del norte: la regla

Latitud 36,57° S. Altura solar al mediodía: **76,9 °** el 21/12 · 53,4 ° en los equinoccios · **30,0 °** el
21/06 (`envolvente` §8.2).

> ### **Alero de 0,55 a 0,70 m de proyección, colocado 0,30 a 0,40 m POR ENCIMA del dintel.**
> **21/12 al mediodía: sombra completa** sobre toda la abertura. **21/06 al mediodía: sol pleno** sobre toda
> la abertura, ganancia solar invernal íntegra. Equinoccios: sombreado el tercio superior.
>
> **Elevar el alero por encima del dintel es el truco que casi nadie usa y que resuelve la contradicción
> "quiero sombra en verano y sol en invierno". Cuesta nada: es la altura del antepecho de cubierta o del canto
> de la losa.**

**La limitación, dicha con honestidad:** un alero fijo es simétrico respecto del solsticio y el desfase térmico
del año no lo es (el mes más caluroso es enero-febrero, no diciembre). Si el proyecto lo justifica: **parral o
pérgola con vid o glicina al norte** —la planta tiene el mismo desfase que el clima—, toldo retráctil, o
alero + persiana para el ajuste fino.

**Y el alero computa FOS** (nota municipal de "Elementos que componen el plano": *"el total de las superficies
y proyecciones de todas las plantas y aleros sobre el suelo, computadas al 100 %"*) — `urb` §3.1.

### El oeste no se resuelve ni con aislante ni con alero

Un muro oeste con SATE de 100 mm (K 0,29) a las 17 h del 21/12 "ve" una temperatura sol-aire de **58,8 °C**,
no 38,8: el Δt efectivo pasa de 13,8 K a **33,8 K**. Y el sol de las 17 h está a **26 ° de altura y
prácticamente al oeste**: un alero horizontal necesitaría **4,30 m de proyección** para sombrear una ventana de
2,10 m. **La fachada oeste no se protege con alero. Punto** (`envolvente` §8.5).

| Solución para el oeste, por eficacia | Costo |
|---|---|
| **1. NO ABRIR AL OESTE.** Poner ahí el garaje, el depósito, el lavadero, un muro ciego | **Cero — es una decisión de partido, y es gratis si se toma en el anteproyecto** |
| 2. Parasoles **VERTICALES** orientables en el plano de la fachada (los horizontales no sirven acá) | Alto |
| **3. Postigón exterior ciego u orientable.** Además elimina el cajón de persiana y da seguridad | **Medio — la mejor relación eficacia/costo** |
| 4. Persiana de enrollar exterior, bajada de 15 a 20 h | Medio |
| 5. Vegetación caduca a 3–6 m de la fachada (**y a la distancia que exige el suelo, §2.7**) | Bajo, tarda 5–10 años |
| 6. Galería o pérgola profunda **con el testero oeste cerrado** | Medio-alto |
| 7. Vidrio de control solar | Medio — **complemento, no sustituto** |
| 8. **Muro claro (α < 0,6)** — baja la sol-aire de 58,8 a ~50 °C, y la norma premia con +20 % de K admisible | **Cero** |
| ✗ Cortina o persiana **interior** | **Baja eficacia: la radiación ya entró.** **Toda protección solar eficaz es EXTERIOR** |

### El cajón de persiana

*"Es simultáneamente el peor puente térmico, el peor puente acústico y el mayor punto de infiltración de aire
de una vivienda argentina. Y está en cada ventana"* (`envolvente` §5.5). Se resuelve con **cajón exterior
aislado**, o **compacto con 40 mm de EPS + burletes**, con el SATE pasando por delante y **retorno del
aislante 20–30 mm sobre el marco**; o **se elimina** yendo a postigón exterior.

### Estanqueidad al aire: en Santa Rosa vale tanto como el aislante

| Clase IRAM 11507-1 | Caudal admisible a 100 Pa |
|---|---|
| A1 (normal) | > 4,01 hasta 6,00 m³/(h·m de junta) |
| **A2 (mejorada)** | > 2,01 hasta 4,00 m³/(h·m) |
| **A3 (reforzada)** | hasta 2,00 m³/(h·m) |

`[VERIFICAR contra el texto de IRAM 11507-1, cap. 4.6]` — los valores vienen de fuentes secundarias.

> **A1 es el mínimo legal en jurisdicciones que adoptan el criterio bonaerense, y es insuficiente para Santa
> Rosa.** Con 60 m lineales de junta perimetral, A1 admite hasta **360 m³/h a 100 Pa** solo por las ventanas =
> **2,4 kW** a ΔT 20 K. Con A3, 120 m³/h = 0,8 kW. **La diferencia entre A1 y A3 es un aire acondicionado
> entero de consumo permanente en invierno** (`viento` §6.2).

**Pero la clasificación mide la ventana, no la obra.** En obra el aire entra por (`viento` §6.3):

| Punto de fuga | Solución |
|---|---|
| **Junta marco-muro (el principal)** | Espuma de PU de baja expansión + **cinta o sellador elástico continuo** por dentro (barrera de aire) y por fuera (barrera de agua/viento). **No confiar en el revoque**: el mortero fisura y se abre |
| **Encuentro muro-cubierta** | Sellado continuo del plano de aire; no dejar la cámara del techo comunicada con el interior |
| Cajas de persiana | Cajón aislado y estanco, o persiana exterior sin caja interior |
| Pasos de instalaciones | Pasamuros con collarín sellado, **cada uno** |
| Cajas de electricidad en muro exterior | Cajas estancas o sellado del conducto |
| Puerta de acceso y de garaje | Burlete perimetral de 3 lados + burlete de umbral |
| Chimenea / hogar sin cierre | Registro de tiro con cierre efectivo |

> **Detalle de proyecto obligatorio en Santa Rosa: dibujar el PLANO DE ESTANQUEIDAD AL AIRE en el corte
> constructivo** — una línea continua que recorre toda la envolvente, sin interrupciones, con el material de
> cada tramo declarado en el pliego. **Si la línea se corta en el dibujo, se corta en la obra.**

**Y la carpintería tiene que resistir, no solo sellar.** Presiones de diseño mayoradas, exposición C
(`viento` §6.4): ventana en zona central **≈ 2,0 / −2,2 kN/m²** · ventana en zona de borde (a menos de 1 m de
la esquina) **≈ 2,0 / −2,6 kN/m²** · portón de garaje de 2,50 × 2,20 m **≈ 12 kN totales (~1.200 kgf)**.
**Exigir en el pliego que la carpintería declare resistencia a la carga de viento**, no solo estanqueidad.

### Puentes térmicos: en una casa de una planta hay 150 a 200 m lineales

Sobre 106,8 m² de muro. **Es una densidad altísima, muy superior a la de un edificio en altura, porque la casa
es toda perímetro** (`envolvente` §6.9). **Las tres decisiones que resuelven el 90 %:**

1. **Aislación exterior continua (SATE)** — resuelve encuentro muro-cubierta, encadenados, columnas embebidas, dinteles, jambas, antepechos, esquinas, tabiques que sobresalen y losas de galería.
2. **Continuidad de la aislación en los dos encuentros extremos** —muro-cubierta arriba y muro-piso abajo—, que es donde el SATE tiene que cerrarse con las otras dos aislaciones.
3. **Resolver el cajón de persiana, o eliminarlo.**

Y la verificación que **no es opcional**: con Santa Rosa en subzona **IVc**, la propia IRAM 11603 prescribe
*"se verificará el riesgo de condensación, controlando los puentes térmicos"*. Objetivo: **fRsi ≥ 0,80** en
todo encuentro (`envolvente` §1.7 y §7).

## 3.6 Gabinete de gas en línea municipal

**Se dibuja en el anteproyecto, no después** (`gas` §4.1). Reglas de NAG-200 3.2.1 y 3.2.2:

| Regla | Consecuencia de proyecto |
|---|---|
| **Acceso libre y permanente para la Prestadora** | Va **sobre la línea municipal, accesible desde la vereda** — no dentro del cerco ni pasando por un portón con llave |
| Lo más cerca posible de la válvula de corte de línea municipal | Se define junto con el acceso peatonal y el vehicular |
| **Base ≥ 0,10 m sobre piso terminado · cara superior ≤ 1,90 m** | Franja de fachada entre ~0,10 y 1,90 m: coordinar con zócalo, revestimiento y despiece |
| **1,00 m libre al frente de la puerta**, altura mínima 2,50 m, con apertura total | **No poner cantero, columna, medidor de agua ni tablero eléctrico enfrentado a 1 m** |
| **≥ 0,50 m a instalaciones eléctricas con riesgo de chispa** (0,30 m si ventila al exterior) | **El pilar de luz y el nicho de gas NO son un solo mueble.** *Es el error más repetido en fachadas de casas* |
| **≥ 1,00 m de toda toma de aire forzado y de todo sombrerete de evacuación de gases** | Condiciona dónde puede salir el terminal de tiro balanceado en la misma fachada |
| **≥ 0,50 m de cualquier abertura de ventilación** | Ídem respecto de rejillas |
| **Prohibido** debajo o delante de ventanas usables como salida, debajo de escaleras, en sótano bajo | Descarta el nicho "bajo la ventana del estar" |
| **Medida interior mínima para medidor ≤ 10 m³/h: 0,45 (alto) × 0,35 (ancho) × 0,25 m (profundidad)** | **Con muro de 0,20 m, un nicho de 0,25 m de profundidad NO entra empotrado:** obliga a engrosar el muro, a un pilar independiente o a un nicho semi-saliente. **Se define en el anteproyecto** |
| Construcción | **Ignífugo**, rígidamente amurado, **piso con pendiente hacia el frente**, estanco si está empotrado en muro de vivienda, conjunto puerta-marco **NAG-237 con la palabra "GAS"**, orificio en el piso para la vaina |
| Ventilación (nicho en espacio abierto) | Puerta con **aberturas superior e inferior de ≥ 10 cm² cada una** |
| **Si la red es de media presión** | El **regulador domiciliario** va en el gabinete aguas arriba del medidor, **lo paga y lo instala el cliente**, y **el nicho mínimo queda justo**: pedir a Camuzzi/matriculado la medida cuando lleva regulador |

**Además, del Código de Edificación de Santa Rosa (CE 5.8.5, mod. Ord. 3895/2009):** el local de medidores de
gas *"debe contar con fácil acceso, no contener tableros o medidores de electricidad, calderas, motores,
aparatos térmicos […] Al frente de los medidores debe dejarse un espacio de circulación de un ancho no
inferior a 1,00 m"* (`urb` §6.4).

**Y el gabinete de gas se dibuja en la lámina 1 del plano municipal**, que exige *"Gabinete de instalaciones
(gas, electricidad, agua, etc.)"* (`urb` §5.4).

## 3.7 Calefacción — y su impacto en la matrícula del gasista (el techo de 5 m³/h)

### La decisión de calefacción define el caudal, y el caudal define qué instalador se puede contratar

**Las tres categorías de matrícula** (prNAG-225, 5.1 — la matrícula **la da Camuzzi, no el CPITLP ni el
municipio**) — `gas` §2.1 y §2.2:

| Categoría | Alcance |
|---|---|
| **1ª** | Cualquier tipo de instalación, GN y GLP, envasado o a granel |
| **2ª — gasista domiciliario** | Hasta 4 bar de red, artefactos de **consumo individual ≤ 58,15 kW (50.000 kcal/h)**, presión interna ≤ 19 mbar. GLP envasado, **excepto a granel** |
| **3ª — gasista de unidades unifuncionales** | **Única instalación en el predio, un regulador y un medidor**, y **consumo total de la instalación ≤ 5 m³/h** |

### Los cuatro escenarios de una casa de Santa Rosa (`gas` §5.3)

| Escenario | Composición | **Suma directa** | Q_si | **¿Alcanza 3ª cat.?** |
|---|---|---|---|---|
| **A — "clásico pampeano"** | Cocina + termotanque 110 l + 4 calefactores TB | **3,58 m³/h** | 2,80 | **Sí** |
| **B** | Cocina + **caldera dual 30.000 kcal/h** (radiadores o losa) | **4,39 m³/h** | 4,39 | Sí, **al límite** |
| **C** *(el que piden muchos comitentes)* | Cocina + caldera 30.000 solo calefacción + **calefón 14 l** | **6,80 m³/h** | 6,22 | **NO — 2ª o 1ª** |
| **D — casa grande** | Cocina + caldera dual 40.000 + secarropas | **5,68 m³/h** | 5,57 | **NO — 2ª o 1ª** |

> ### **En cuanto el proyecto lleva caldera y algún artefacto más que la cocina, el instalador de 3ª categoría queda fuera de alcance.** Contratar al gasista antes de saber esto es el origen clásico del *"tengo que cambiar de matriculado a mitad de obra"*.

`[VERIFICAR con Camuzzi — matriculados@camuzzigas.com.ar, por escrito]` si el límite de 5 m³/h se mide sobre la
**suma directa** o sobre el **caudal de simultaneidad Q_si**. La norma dice *"consumo total de la instalación"*,
lo que sugiere suma directa, y **eso decide la categoría en los escenarios B y D**.

**Otros dos disparadores que sacan al de 3ª categoría:** que haya **más de un medidor** o que el predio tenga
**más de una instalación** (casa + quincho con artefactos + futura unidad de renta); y que el proyecto vaya a
**GLP a granel (zeppelin)**, que **solo puede firmar un instalador de 1ª categoría**.

**Mínimo de proyecto (NAG-200 4.6.2): 21,63 kW = 18.600 kcal/h → 2,00 m³/h.** Ninguna casa con calefacción
baja de ahí. **Y toda toma tapada suma:** la norma obliga a computar *"las tomas taponadas y potenciales
incrementos previstos en el proyecto"*. **Recomendación: proyectar y presentar con las tomas futuras incluidas**
(quincho, secarropas, segunda salida de cocina) — ampliar después implica nueva factibilidad, nuevo plano,
nueva inspección y potencialmente cambiar de categoría de matriculado.

### Elección del sistema (`gas` §6.1 y §6.2)

| Si el comitente… | Conviene | Consecuencias |
|---|---|---|
| Busca **presupuesto ajustado** y uso intermitente (casa vacía de día) | **Calefactores de tiro balanceado** — Escenario A | Menor inversión, menor caudal, **3ª categoría posible**. Pero: **un terminal visible en fachada por artefacto** y confort desigual |
| **Vive la casa todo el día** y prioriza confort | **Losa radiante** con caldera dual | La alta inercia es virtud, no defecto, con uso continuo. **Pero exige envolvente Nivel B verificada** (§3.7.1) |
| Quiere **control rápido por ambiente** | **Radiadores con válvulas termostáticas** | |
| Tiene **más de un baño** y quiere ACS abundante | **Caldera dual** (elimina el calefón) o termotanque de acumulación | La caldera dual **unifica ACS y calefacción en un artefacto y un solo conducto, y baja el caudal total**: comparar B (4,39) contra C (6,80) |

**Termotanque vs. calefón, en Santa Rosa concretamente:** el **calefón** de 14 l/min consume **2,41 m³/h** y
tiene caudal limitado con agua de entrada fría — y en invierno pampeano la temperatura de entrada de red es
baja, lo que aumenta la proporción de agua caliente en la mezcla **y castiga al calefón**. El **termotanque**
de 110 l consume **0,86 m³/h**, estable, y soporta dos puntos simultáneos, pero pierde por standby.

### Lo que la calefacción impone a la planta (NAG-200 5.9.2 — `gas` §4.3)

| Ambiente | Qué se admite |
|---|---|
| **DORMITORIOS** | **ÚNICAMENTE cámara estanca (Tipo C).** Prohibido todo otro artefacto a gas |
| **BAÑOS Y ANTEBAÑOS** | **ÚNICAMENTE cámara estanca (Tipo C)** |
| **PASOS A DORMITORIOS** | Tipo C, o cámara abierta con salida directa al exterior y remate a los cuatro vientos (Tipo B) |
| **COCINAS** | Con **volumen < 7 m³ no se admiten calentadores de cámara abierta** (calefón, termotanque ni caldera). Caldera de cámara abierta: **máx. 1,16 kW (1.000 kcal/h) por m³** → una caldera de 20.000 kcal/h exige **≥ 20 m³ de local** |

> ⚠ **La regla de puertas que sorprende (5.9.2.1):** *"La ausencia de puerta NO modifica el carácter o destino
> de un ambiente. Debe entenderse por ausencia de puerta al hueco, con o sin marco, cuyo ancho **no debe ser
> superior a 1 m**. Toda dimensión mayor de ese hueco califica al dormitorio como ambiente integrado o
> monoambiente."* **Un dormitorio abierto al estar por un vano de 1,20 m convierte todo el conjunto en
> monoambiente a los ojos de la norma**, y arrastra las reglas de monoambiente también a la cocina. En casas
> de programa abierto esto aparece más seguido de lo que se cree.

**Ventilaciones de ambientes con artefactos de cámara abierta:** **4 cm² por kW (4 cm² cada 860 kcal/h), con
mínimo absoluto de 100 cm²**, en **dos** aberturas: **inferior entre 0,30 y 0,50 m** del piso y **superior a no
menos de 1,80 m**. Es **superficie LIBRE DE PASAJE**, no la medida exterior de la rejilla (una rejilla de
20 × 20 cm al 60 % da 240 cm² libres): **especificar siempre el área libre en el pliego**.

> **Posición del estudio: en obra nueva en Santa Rosa, especificar cámara estanca (Tipo C) en todo lo que se
> pueda.** Elimina las rejillas permanentes —que en zona fría son un agujero térmico durante cinco meses—,
> elimina el riesgo de CO y libera el proyecto (permite calefactor en dormitorio y caldera o calefón en baño o
> lavadero) (`gas` §4.3).

**Conductos de evacuación:** chapa de acero galvanizada, aluminio o acero inoxidable, apto para más de 200 °C,
estanco, paredes internas lisas. **PROHIBIDOS: aluminio corrugado, PVC, polietileno y policarbonato.** *El
"flexible de aluminio corrugado" que se ve en tantas obras está expresamente prohibido* (`gas` §4.4).
`[VERIFICAR en NAG-200 §6.5 y §6.6 con el matriculado, ANTES de definir la fachada]` la **altura de remate
sobre cubierta** y las **distancias mínimas de los terminales de cámara estanca a ventanas, esquinas, aleros y
medianeras**: son visibles y su posición no es negociable después.

### Previsiones que, si no están en el anteproyecto, se pagan picando (`gas` §6.3)

- **Cada terminal de tiro balanceado dibujado en el alzado**, con sus separaciones (≥ 1,00 m al nicho de gas, ≥ 0,50 m a cualquier abertura de ventilación).
- **Espacio de caldera:** local o nicho ventilado, acceso frontal para service, desagüe de condensado si es de condensación, paso del conducto coaxial. **No en dormitorio ni en baño salvo cámara estanca.**
- **Colector de losa radiante:** gabinete empotrado (pasillo o lavadero) con espacio para los circuitos y purga accesible. **Desde ahí salen todos los caños hacia la losa.**
- **Nichos de calefactores TB en muros exteriores:** profundidad y ancho **según el modelo, que hay que definir antes de mandar a hacer los muros**.
- **Pases y vainas en losa, vigas y cimientos, ejecutados ANTES del hormigonado.**
- **Plano de cubierta con TODOS los remates** —sombreretes de gas + ventilaciones cloacales + extracciones + tanque— con cotas y separaciones. **En una casa de una planta la cubierta se ve desde el terreno vecino: es una decisión de proyecto, no de plomería.**
- **Alimentación eléctrica de la caldera o el termotanque: circuito dedicado.**

### 3.7.1 El error de asignación de presupuesto que hay que evitar

> **Comprar losa radiante en una casa sin aislar.** Con envolvente corriente la carga es de **170 W/m²** y la
> losa radiante emite **100 W/m² como máximo: no calienta.** Se gasta en el sistema y la casa sigue fría.
> **Aislar primero; la losa radiante solo con envolvente Nivel B verificada** (`envolvente` §9.3).

**El argumento completo para el comitente** (`envolvente` §9.4): una casa de 130 m² construida como se
construye habitualmente consume del orden de **3.400 m³ de gas/año** en calefacción; la misma casa en Nivel B,
**1.775 m³**; en Nivel A, **1.047 m³**. Y **la potencia instalada se divide por 3** (la carga baja de 22.146 W a
6.854 W): el equipo que se compra el primer día es más chico.

## 3.8 Previsión eléctrica e iluminación

**El punto de no retorno:** una vez que el electricista pasó los caños y se cerraron las paredes, **el proyecto
de iluminación está congelado**. Todo cambio posterior implica romper, y en el 90 % de los casos el cliente no
rompe: se conforma con algo peor (`int` §5.12).

```
Demolición ─► Replanteo ─► Instalaciones ─► Cerramiento ─► Yesería ─► Terminación
                  ▲              ▲                ▲
        El interiorismo    ÚLTIMO MOMENTO    YA ES TARDE
        DEBE estar acá     para mover una boca
```

### Quién define qué

| Define el PROYECTO (arquitectura / interiorismo) | Define el proyectista eléctrico / instalador |
|---|---|
| **Dónde va cada boca de luz** (coordenadas en planta) | Recorrido de cañerías |
| **Cuántas capas y cuántos circuitos** de iluminación | Sección de conductores |
| **Qué circuito comanda qué artefacto** | Cantidad y tipo de protecciones |
| **Dónde va cada tecla, a qué altura, cuántos módulos** | Distribución de circuitos en el tablero |
| **Dónde va cada tomacorriente y a qué altura** | Cálculo de demanda y grado de electrificación |
| **Bocas de datos, TV, timbre** | Cumplimiento de AEA 90364 |
| **Previsiones de fuerza motriz** (horno, anafe, aire, termotanque) | Verificación de la acometida |
| **Espacio y ventilación para drivers y fuentes** | Puesta a tierra, diferencial, térmicas |

**Marco normativo:** la instalación se rige por la **Reglamentación AEA 90364**, Parte 7 Sección 771 (viviendas),
que fija grados de electrificación, cantidad mínima de circuitos y bocas y las **zonas de protección en baños**.
**El Código de Edificación de Santa Rosa la adopta expresamente** (art. 1.1.5), junto con las *"Disposiciones
sobre el tablero para la protección de la alimentación y para la medición"* y la *"Reglamentación para la
derivación a usuarios"* **editadas por la CPE** (`urb` §4.15 y §6.3 · `int` §5.12).

### Previsiones mínimas que se dejan hechas (extracto operativo — completo en `int` §5.12 y Anexo C)

- **Todas las teclas a una sola altura** (110–120 cm al eje). **Ninguna detrás de una puerta abierta ni de un mueble** — verificar contra la planta amoblada y el sentido de apertura **real**.
- **Tomas generales cada 3–4 m de perímetro, nunca a más de 1,80 m de cualquier punto de un muro libre.**
- **Junto a la cama: mínimo 2 tomas por lado.** Sobre mesada de cocina: **4–6, en al menos 2 circuitos, a 110 cm.**
- **Circuitos exclusivos:** horno, anafe/inducción, lavarropas, lavavajillas, termotanque, aires acondicionados.
- **Espacio accesible y ventilado para todos los drivers.**
- **Alimentación en el dintel de cada ventana** para cortinas motorizadas futuras: *"es baratísimo dejarlo previsto y carísimo agregarlo después"*.
- **Toma alta detrás de la TV + datos + coaxil + conduit para pasar cables.** Router en posición central.
- Luz exterior: **acceso, sendero, galería, parrilla**, cochera. Balizamiento de pasillo nocturno.
- **Canalización troncal para carga de vehículo eléctrico**, si aplica.

### Iluminación: los niveles que se especifican (`int` §5.2)

| Local / tarea | **Em criterio del estudio (lux)** | Mín. IRAM-AADL J 20-06 | Ra mín. |
|---|---|---|---|
| Estar — ambiental | **100–200**, dimerizable a 20 | — | 90 |
| Estar — lectura | **300–500** (luz de tarea local) | — | 90 |
| Comedor — sobre la mesa | **200–300**, dimerizable a 50 | — | **90** |
| Cocina — general | **300** | 200 | 90 |
| **Cocina — mesada, bajo alacena, anafe, bacha** | **500–750** | 200 | **90, R9 ≥ 50** |
| Baño — general | **150–200** | **100** | 90 |
| **Baño — espejo (plano VERTICAL a 1,40–1,60 m)** | **300–500** | **200 (plano vertical)** | **90, R9 ≥ 50** |
| Dormitorio — general | **100–150**, dimerizable a 10 | 200 | 90 |
| Dormitorio — lectura en cama | **300–500**, con comando propio | 200 | 90 |
| Balizamiento nocturno | 1–5 lux, 2200–2700 K, con sensor | — | — |

*(En dormitorio el estudio usa menos que IRAM: la J 20-06 es de 1972 y no contempla el confort circadiano
nocturno; se compensa con luz de tarea localizada.)*

**La luz natural que ya está resuelta por el partido:** Santa Rosa tiene **cielos despejados frecuentes** y
excelente recurso solar invernal (`marco` §4). El clerestorio al norte, los locales pasantes N-S y los colores
interiores claros hacen más por la luz que agregar metros de vidrio — y no pagan la penalización térmica
(`envolvente` §5.7).

---

# FASE 4 — El proyecto

## 4.1 Lista de planos y escalas — para una casa, no para un edificio

**Escala de referencia en vivienda: 1:50** para plantas, cortes y vistas (el 1:100 es escala de edificio y de
legajo municipal). Detalles a **1:20 / 1:10 / 1:5**. Formato de lámina: **A2 / A3** con plegado a A4 según
IRAM 4504. **Evitar escalas raras (1:75, 1:30, 1:15): si un dibujo no entra, se cambia el formato de lámina,
no la escala** (`proy` §2.2).

| Grupo | Vivienda 120–200 m² | Contenido crítico |
|---|---|---|
| Carátula, índice, notas, simbología | **1** | Leyenda de materiales, referencias de carpinterías, **convención de cotas declarada** (a eje de muro o a paramento terminado) |
| Ubicación, mensura, implantación | **1** | Retiros acotados a los cuatro linderos, cotas de terreno natural y de proyecto, accesos, **entrada de servicios**, desagües pluviales de terreno |
| Plantas de arquitectura | **2–3** | Ver §4.1.1 |
| Cortes (mínimo 2: uno longitudinal y uno transversal) | **1–2** | Alturas de local, antepecho, dintel, cielorraso; espesores de losa y contrapiso; **cotas acumuladas desde ±0,00**; corte de terreno natural y modificado; **cordón cuneta y límites de terreno** |
| Vistas / fachadas | **1–2** | Materiales señalizados, carpinterías codificadas, **terminales de tiro balanceado**, nicho de gas, pilar eléctrico |
| Planta de techos | **1** | Pendientes con % y sentido, embudos y desagües con diámetro, canaletas, babetas, **TODOS los sombreretes y ventilaciones**, anclajes |
| Albañilería / dimensionado | **1–2** | Espesores reales terminados, vanos con altura de antepecho y dintel, huecos y pases, nichos |
| **Replanteos** | **2–3** | Terreno y linderos · **fundaciones (cotas de fondo de excavación)** · plantas · núcleo húmedo 1:25 |
| Terminaciones y solados | **1–2** | Despiece y **arranque de junta** (los cortes nunca contra la puerta de acceso) |
| Cielorrasos (RCP) | **1** | Donde se cierra la coordinación con instalaciones |
| Planilla de locales | **1** | La **fuente de verdad** de terminaciones |
| Planilla de carpinterías | **2–3** | Ficha gráfica por tipo, con **vano de albañilería Y carpintería terminada** |
| Planillas de herrería y equipamiento | **1–2** | |
| **Detalles constructivos** | **4–8** (ver §4.2: en esta casa el mínimo real es mayor) | |
| **Subtotal ARQUITECTURA** | **20–33 láminas** | |
| Estructura (fundaciones, encofrados, armaduras, detalles) | **5–7** | |
| Sanitaria **2–3** · Gas **1** · Eléctrica **2–3** · Termomecánica **0–1** | **5–9** | |
| **TOTAL LEGAJO EJECUTIVO** | **30–50 láminas** | |
| **Legajo municipal (subconjunto)** | **3–6 láminas** | Ver §5.2 |

*(`proy` §2.3 y §2.11)*

### 4.1.1 Lo que lleva siempre una planta de ejecutivo (`proy` §2.3.1)

Ejes estructurales numerados coincidentes con estructura · **tres líneas de cota perimetrales** (total, entre
ejes/aberturas, parciales de macizos y vanos) · cotas interiores y superficie de cada local · nombre y número
de local coincidente con la planilla · cota de nivel en cada cambio · códigos de carpintería con sentido de
apertura dibujado · artefactos, mesadas y muebles fijos a escala real · huecos, pases y buñas · **espesores de
muro reales terminados** (un hueco 18 con revoque a dos caras se dibuja 0,23–0,25 — **y con SATE de 100 mm,
0,318**) · líneas de corte · norte.

> **Convención crítica a declarar en la carátula: si las cotas son a eje de muro o a paramento terminado.
> Mezclar ambas es una de las causas más frecuentes de error de replanteo** (`proy` §2.3.2).

## 4.2 Detalles constructivos que en ESTA casa hay que dibujar sí o sí

Un legajo con 4 detalles no es un ejecutivo. En una vivienda de nivel medio son **15 a 30 detalles**
(`proy` §2.5). **Los que no pueden faltar en una casa de Santa Rosa:**

| # | Detalle | Escala | Qué tiene que resolver explícitamente | Fuente |
|---|---|---|---|---|
| **1** | **Encuentro MURO–CUBIERTA** (el puente térmico más importante de todos, 48 m lineales) | 1:10 / 1:5 | **El EPS del muro y el aislante de la cubierta DEBEN TOCARSE, por encima del encadenado.** El punto donde el encadenado queda "en el medio" es donde aparece la mancha de moho en el ángulo techo-pared. Con parapeto: **envolverlo por sus tres caras**. Con cubierta inclinada: **bafle o deflector rígido** obligatorio para que la lana no tape la entrada de aire del alero | `envolvente` §6.1 |
| **2** | **ALERO** — corte por el borde de cubierta | 1:10 / 1:5 | **Sofito cerrado con tapajuntas continuo** (si está abierto, el viento presuriza la cámara del techo y levanta el techo desde el alero); **el cabio vuela, no la chapa**; **fleje continuo de borde fijado mecánicamente**; anclaje a tracción; proyección **0,55–0,70 m** elevada **0,30–0,40 m sobre el dintel**; goterón y canaleta con su sujeción | `viento` §7.6 · `envolvente` §8.2 |
| **3** | **Arranque del SATE en ZÓCALO** y encuentro con la aislación perimetral del piso | 1:10 / 1:5 | El aislante del muro **baja 50–60 cm bajo NPT**; **por debajo del terreno XPS, nunca EPS**; **perfil de arranque de aluminio con goterón ≥ 30 cm sobre el terreno**; **la faja perimetral del piso y el XPS del muro se tocan** (si no, queda un puente lineal continuo de 48 m); **zócalo de mayor resistencia mecánica hasta 1,50–2,00 m** (el SATE en PB recibe golpes: bicicletas, herramientas, cortadora, granizo rebotado); **vereda perimetral con pendiente 2 %** | `envolvente` §6.6 |
| **4** | **JAMBA de vano** (y su gemelo, el **dintel con cajón de persiana**) | 1:5 | **Retorno del aislante 20–30 mm sobre el marco**; refuerzo de malla en diagonal 30 × 50 cm a 45° en cada esquina de vano; cajón compacto aislado con 40 mm de EPS + burletes, o cajón exterior; **premarco alineado con el plano del aislante, no con la mampostería** | `envolvente` §6.4 y §10.4 |
| **5** | **ANTEPECHO y alféizar** | 1:10 / 1:5 | Pendiente mínima 2 % y **goterón**; **prolongación lateral de 3 cm**; membrana bajo el alféizar **subiendo por las jambas**; sellado perimetral; **drenajes del marco no tapados** | `proy` §2.5 (D-02) · `envolvente` §6.5 |
| **6** | **PLATEA PERIMETRAL** — corte por viga de borde | 1:20 / 1:10 | Cota de fondo de viga **≥ 0,80 m bajo terreno natural**; hormigón de limpieza; armaduras y recubrimiento; **manto de suelo seleccionado compactado con espesor y densidad especificados**; **film de polietileno 200 μ subiendo por los bordes**; **capa aisladora horizontal Y vertical continua**; encuentro con la vereda perimetral y su **junta elástica sellada** | `suelo` §7.4 y §7.5 |
| **7** | **VEREDA PERIMETRAL** (es un detalle estructural, no de paisajismo) | 1:10 | **Ancho 1,20 m mínimo / 1,50 m recomendado**, **pendiente ≥ 2 % alejándose** (3 % si recibe descarga de cubierta), **junta elástica sellada contra el muro** (no mortero rígido), **juntas de contracción cada 2,00–3,00 m selladas**, superficie **impermeable**, nivel por debajo del piso interior (≥ 0,15 m) y por encima del terreno circundante | `suelo` §8.2 |
| **8** | **Baño completo** (planta + cortes + 1:5) | 1:20 / 1:5 | Alturas de bocas de agua y desagüe; pendiente a rejilla; arranque del despiece; **aislación hidrófuga del box subiendo 20 cm sobre el solado y 180 cm en pared** | `proy` §2.5 (D-04) |
| **9** | **Cocina** (planta + vistas) | 1:20 / 1:5 | Altura y profundidad de mesada; bocas eléctricas sobre mesada; **campana y su conducto**; **pase de gas**; tomas de electrodomésticos | `proy` §2.5 (D-05) |
| **10** | **Umbral de puerta exterior y encuentro con vereda** | 1:10 / 1:5 | Cota interior vs. vereda (**NPB ≥ NR + 0,10 m + 3 % del ancho de vereda**), corte de capilaridad, resolución accesible | `proy` §2.5 (D-10) · `urb` §4.12 |
| **11** | **Detalle de canaleta de desagüe sobre L.M. y eje divisorio** | 1:20 | **Exigido por el municipio** en el plano | `urb` §5.4 |
| **12** | **Detalle de encadenado** | 1:20 | **Exigido por el municipio**: sección de hormigón y hierro | `urb` §5.4 |

**Y si la cubierta es liviana, dos más:** el **detalle de anclaje cabio–encadenado** (fleje, y su versión
reforzada de las 4 esquinas) y el **detalle de fijación de chapa por zona** (`viento` §8.5).

## 4.3 Pliego mínimo

El pliego es **el contrato técnico**: los planos dicen *dónde y cuánto*; el pliego dice *qué, de qué, cómo, con
qué tolerancia y cómo se recibe* (`proy` §4.1).

### La cláusula que evita que cada contradicción del legajo sea un adicional

> *"En caso de discrepancia entre documentos, el orden de prelación será: 1) Contrata y anexos; 2) Circulares
> aclaratorias, en orden inverso a su fecha; 3) Pliego de Condiciones Particulares; 4) Pliego de Condiciones
> Generales; 5) Especificaciones Técnicas Particulares; 6) Especificaciones Técnicas Generales; 7) Planillas;
> 8) Planos de detalle de mayor escala; 9) Planos generales. Entre planos de distinta escala prevalece el de
> mayor escala. Entre cota numérica y medición gráfica, prevalece la cota numérica. Toda discrepancia deberá
> ser consultada al Director de Obra antes de la ejecución; su ejecución sin consulta será por cuenta y riesgo
> del Contratista."*

### Los seis bloques de todo ítem — si falta uno, el ítem genera adicional (`proy` §4.2)

| Bloque | Pregunta que responde |
|---|---|
| **1. Unidad y alcance de la medición** | ¿Cómo se mide y se paga? ¿Qué está incluido en el precio unitario? |
| **2. Materiales** | ¿Con qué se hace? (por norma, por prestación y/o marca de referencia) |
| **3. Ejecución** | ¿Cómo se hace? Procedimiento, secuencia, curado, protección |
| **4. Tolerancias** | ¿Cuándo está mal? |
| **5. Ensayos y controles** | ¿Cómo se comprueba? ¿Quién paga? |
| **6. Recepción** | ¿Cuándo se paga? Criterio de aprobación, motivos de rechazo, garantía |

### Cláusulas generales que no pueden faltar

Objeto y alcance con **cláusula de completitud** · **normas aplicables** (CIRSOC 101/102/201/401, IRAM 11601,
11603, 11604, 11605, 11507, 11625/11630, AEA 90364, NAG-200 y NAG-225, **Código de Edificación Ord. 1581/95 y
CUA Ord. 6976/23**, Dec. 911/96 y Ley 19.587) · conocimiento del lugar · **replanteo con verificación de
medidas en obra** · **muestras aprobadas por escrito con 15 días de antelación, conservadas en obra como patrón
de recepción** · **tramos de muestra** para revoques, revestimientos, pintura y juntas · ensayos (cuáles, con
qué frecuencia, quién los paga, laboratorio habilitado) · **ayuda de gremios definida con precisión** *(una de
las tres fuentes principales de conflicto en obra)* · protección de trabajos terminados · limpieza periódica y
final · documentación a entregar por el contratista (**conforme a obra**, garantías, manuales, protocolos) ·
seguridad e higiene · plazo, plan de trabajos y penalidades · recepción provisoria, fondo de reparo y recepción
definitiva · **adicionales y economías con autorización previa por escrito** (`proy` §4.1).

### Los ítems que en Santa Rosa hay que redactar con especial cuidado

| Ítem | Qué tiene que decir el pliego |
|---|---|
| **Movimiento de suelos y fondo de excavación** | **Hormigón de limpieza el mismo día**; prohibición de dejar la excavación abierta con pronóstico de lluvia; **densidad del manto compactado MEDIDA, no estimada** (≥ 95 % Proctor estándar, en capas ≤ 0,20 m) |
| **Hormigón de fundación** | **Clase de exposición CIRSOC 201 y tipo de cemento según el análisis químico del informe geotécnico**; curado obligatorio **≥ 7 días**; hormigonar temprano en verano |
| **SATE** | Sistema completo de un único fabricante; **espigas para ladrillo hueco, cantidad y longitud según manual del fabricante y zona de viento CIRSOC 102** `[VERIFICAR]`; malla antiálcali embebida; **refuerzo diagonal en esquinas de vano**; **revestimiento permeable al vapor y de color claro** con el índice de reflectancia mínimo que exija el fabricante `[VERIFICAR IR ≥ 20–25]`; **XPS bajo el perfil de arranque** |
| **Aislación de cubierta** | Espesor **por número**, no "aislación térmica"; **barrera de vapor del lado cálido, solapada 15 cm y sellada en cada perforación**; **terminación con α < 0,6** declarada; prohibición de grava suelta como protección |
| **Carpinterías** | **Clasificación IRAM 11507-1 de infiltración (A2 mínimo)**, K de ventana completa por IRAM 11507-4 (**objetivo 2,13; piso 2,82**), **resistencia declarada a la carga de viento**, composición de vidrio con **K, g y TL** de planilla del proveedor, **sellado perimetral con fondo de junta + espuma PU + sellador elástico continuo interior y exterior** |
| **Cubierta liviana (si la hay)** | **Anclaje calculado por zona** (interior / extremos de 2 m en las 4 esquinas); tornillos con **arandela metálica + EPDM**, fijación **en la cresta**; **clavo helicoidal o tornillo, nunca clavo liso**; capacidad de *pull-through* declarada por el fabricante |
| **Pluviales y vereda perimetral** | Cañería enterrada **estanca** con pendiente ≥ 1 % y **cámaras de inspección**, descarga **≥ 3,00 m** del perímetro; vereda perimetral con su ancho, pendiente, juntas y **sellado elástico** — **en planos y en cómputo, no "de palabra"** |
| **Instalaciones enterradas** | Toda cañería **en vaina**, con cámara de inspección testigo; **ningún empalme bajo la platea ni bajo muros portantes**; **prueba de estanqueidad antes de tapar, documentada con fotos** |

## 4.4 Cómputo por rubro

**Estructura de rubros para vivienda unifamiliar** (`proy` §5.2) — 20 rubros:

`01` Trabajos preliminares · `02` Movimiento de suelos · `03` **Estructura de H°A°** · `04` Mampostería ·
`05` **Aislaciones** · `06` Cubierta · `07` Revoques · `08` Contrapisos y carpetas · `09` Solados y
revestimientos · `10` Cielorrasos · `11` **Carpinterías** · `12` Herrería · `13` Instalación sanitaria ·
`14` Instalación de gas · `15` Instalación eléctrica · `16` Termomecánica · `17` Pintura · `18` Equipamiento ·
`19` **Obras exteriores** (vereda, cordón, **vereda perimetral**, cerco, parquización, pileta) · `20` Varios y
limpieza final.

**Incidencia porcentual de referencia — vivienda unifamiliar de nivel medio** (`proy` §5.5). *Son rangos de
práctica profesional, no una fuente única: el método correcto es que cada estudio construya su base con sus
obras reales.*

| Rubro | Incidencia | Rubro | Incidencia |
|---|---|---|---|
| Preliminares y obrador | 1–2 % | Cielorrasos | 2–4 % |
| Demolición y movimiento de suelos | 1–3 % | **Carpinterías y vidrios** | **8–14 %** |
| **Estructura de H°A°** | **12–18 %** | Herrería | 1–3 % |
| Mampostería y tabiques | 7–11 % | **Sanitaria** | **5–8 %** |
| **Aislaciones** | **2–4 %** *(se subestima siempre)* | Gas | 1–2 % |
| **Cubierta** | **4–8 %** *(alto en vivienda)* | **Eléctrica y corrientes débiles** | **5–8 %** |
| Revoques | 5–8 % | Termomecánica | 2–6 % |
| Contrapisos y carpetas | 3–5 % | Pintura | 3–5 % |
| **Solados y revestimientos** | **7–12 %** | Equipamiento fijo | 3–7 % |
| | | Obras exteriores y parquización | 2–6 % |

**Agrupamientos para conversar con el comitente:** obra gruesa **35–45 %** · obra húmeda y terminaciones
**25–32 %** · instalaciones **15–22 %** · carpinterías, herrería y equipamiento **12–20 %**.

**Uso práctico:** con estas incidencias se puede (a) presupuestar por analogía sobre un costo por m² total,
(b) **detectar una oferta desbalanceada** —un contratista que carga 30 % en la estructura y 3 % en
terminaciones se está financiando con el anticipo— y (c) construir la curva de inversión.

**Cómo se computa la superficie para presupuestar** (`ante` §2.6.3):
**superficie equivalente = cubiertos × 1,00 + semicubiertos × 0,50 + descubiertos accesibles × 0,30.**
*Presupuestar sobre superficie cubierta a secas subestima sistemáticamente las obras con mucha galería, que en
La Pampa son casi todas.* Incidencias relativas: galería/semicubierto **0,45–0,60 ×** el m² cubierto · terraza
descubierta accesible **0,20–0,35 ×** · **movimiento de suelos y fundaciones especiales pueden sumar 5–15 % al
total si el suelo es malo**.

**Base de honorarios en La Pampa:** valor de referencia del m² del **CALP**, actualizado por promedio de
índices **CAMARCO e INDEC** como máximo cada 2 meses. La última resolución obtenida es la **N° 09/2024:
$ 913.336/m² desde el 1/4/2024, sobre vivienda unifamiliar tipo de 120 m² cubiertos, con aporte mínimo
profesional de $ 8.100** — **dato de abril de 2024, desactualizado por inflación: pedir la resolución vigente
antes de cotizar** (`marco` §6).

## 4.5 Documentación térmica que se produce aunque nadie la pida

**No hay ley provincial de La Pampa de acondicionamiento térmico** análoga a la Ley 13.059 bonaerense
`[VERIFICAR en el Digesto provincial y en el CALP]`, y el Código de Edificación municipal no la exige. *"La
ausencia de exigencia municipal no es un permiso: es una responsabilidad profesional trasladada al
proyectista"* (`envolvente` §1.9).

- [ ] **Planilla de cálculo de K por elemento** (IRAM 11601), con capas, λ, Rt y **las resistencias superficiales correctas por estación** (verano en cubierta: **Rsi = 0,17**, flujo descendente).
- [ ] **Planilla de verificación de K máximo admisible** (IRAM 11605) **invierno Y verano**, con la corrección por α.
- [ ] **Planilla de verificación de condensación** superficial e intersticial (IRAM 11625 / 11630) — **no es opcional en subzona IVc**.
- [ ] **Planilla de coeficiente G** (IRAM 11604), con **G_cal ≤ G_adm**. *(Casa de referencia de 338 m³: G_adm ≈ 1,57 W/m³K; objetivo del estudio: G_cal ≤ 0,80 × G_adm.)*
- [ ] **Planilla de carpinterías** con K de ventana completa, clasificación IRAM 11507-1 y -4, y composición de vidrio con g y TL.
- [ ] **Memoria técnica** con el nivel de IRAM 11605 adoptado y su justificación.
- [ ] **Detalles a 1:5 / 1:10** de los encuentros de §4.2.
- [ ] **Etiqueta de eficiencia energética (IRAM 11900 / PRONEV)** — **La Pampa está adherida al PRONEV**, aunque el etiquetado no es obligatorio sin ley provincial. Es un diferencial comercial y una verificación externa gratuita `[VERIFICAR el registro de certificadores habilitados en La Pampa]`.

---

# FASE 5 — Trámites

## 5.1 El circuito completo, en orden

```
0. PORTAL CIUDADANO: datos de parcela  →  Plano P1 (distrito) + P2 (corredor) + P4 (aeropuerto)
1. [opcional pero recomendado] FACTIBILIDAD → acto administrativo aprobando/rechazando el proyecto
2. LIBRE DE DEUDA CATASTRAL (digital, con plano)
3. Orden de Trabajo + documentación → VISADO PREVIO en CALP (MiCALP) + aportes Caja de Previsión
4. PERMISO DE OBRA (digital, con plano visado + acreditación de titularidad)
      └─ liquidación de Derechos de Construcción → PAGO → acto administrativo
5. ACTA DE INICIO DE OBRA (propietario + Director Técnico + instaladores, DDJJ)
6. Cartel de obra al frente + copia del plano aprobado y del Permiso en obra
7. EJECUCIÓN. Presencia obligatoria del profesional en los hormigonados
      └─ si la obra supera 300 m²: doble inspección (fundación/capa aisladora y fin de estructura)
8. Ejecución de la VEREDA (reglamentaria, o provisoria de 1,20 m) — condición para el alta
9. FINAL DE OBRA / ALTA DE OBRA (digital, plano visado) → inspección → firma digital del plano
      └─ plazo: dentro de los 60 días corridos de terminada la obra
```

*(`urb` §5.9. Fuente: Manual de Procedimientos de la Dirección de Planeamiento Urbano y Obras Particulares,
vigente desde el 01/03/2026, y Código de Edificación arts. 2.1.1 a 2.1.12.)*

> **Cambio de fondo:** *"Los trámites serán recepcionados **únicamente de manera digital**, a través de la
> plataforma existente en la página web oficial de la Municipalidad: www.santarosa.gob.ar."* **Ya no se
> presentan copias en papel ni se cuentan juegos de planos: el municipio firma digitalmente el plano.**
> `[VERIFICAR formato de archivo, tamaño y nomenclatura que acepta la plataforma.]`
>
> **Y el croquis de ubicación ya no se emite:** los ángulos y distancias a la esquina se obtienen del
> **Portal Ciudadano → "Trámites On Line"**.

### El trámite optativo que conviene hacer: FACTIBILIDAD

*"Trámite optativo por el cual se solicita el análisis de viabilidad de una obra a realizarse, de acuerdo al
código urbano ambiental y el código de edificación."* Se presenta la propuesta *"con la mayor cantidad de
información técnica posible (ejemplo renders)"* y **el municipio emite un acto administrativo aprobando o
rechazando el proyecto** (`urb` §5.0).

> **Es la herramienta correcta para blindar cualquier interpretación dudosa —cocina integrada, cochera, R3VII,
> sistema constructivo alternativo— ANTES de desarrollar el ejecutivo.** Es optativa y probablemente gratuita,
> pero devuelve un acto administrativo. **Vale el tiempo.**

**Las preguntas que conviene meter dentro de una Factibilidad** (`urb` §8): cochera (12/14 m² del CE vs. 15 m²
del CUA) · **cocina integrada** · umbral del retiro de fondo en PB (26 o 28 m) · redondeo de la densidad ·
**cómo se computa y se acredita el C.A.S.** · módulo polivalente (¿computa FOS? ¿densidad?) · sistemas
constructivos alternativos (¿basta el CAT o hace falta además la aprobación expresa del art. 4.5.2?).

## 5.2 Visado previo del CALP — es obligatorio y es previo al municipio

**CE art. 2.1.2 (texto según Ord. 6445/2020):** *"Previo a la ejecución de cualquier tarea […] que requiera
Permiso de Obra, deberá efectuarse la correspondiente tramitación ante la Municipalidad con: **Planos
debidamente intervenidos por los Colegios y Consejos de Profesionales cumplimentando con el visado Previo**"*
(`urb` §5.1).

| Dato | Valor |
|---|---|
| **Sede Santa Rosa** | **Don Bosco 243** — lunes a viernes de 8 a 13 h |
| Teléfono / WhatsApp | **2954-412858** · Área Técnica (02954) 271045 · Adm. Contable (02954) 271011 |
| Mail Área Técnica | `tecnica@colegioarqlapampa.org.ar` |
| **Plataforma de visado** | **MiCALP** — `micalp.colegioarqlapampa.org.ar` |
| Marco legal | Leyes provinciales **2.878** (creación del CALP) y **2.881** (visado previo y aportes) |
| Documentación | **Orden de Trabajo / Contrato** firmada por propietario y profesional, planimetría con el rol declarado en la carátula, planilla de liquidación de gastos, comprobante de aporte a la Caja de Previsión |
| **Importe vigente del valor de referencia y del aporte** | **[VERIFICAR — CALP, Área Contable (02954) 271011 / `adm@colegioarqlapampa.org.ar`]** |

> **Un arquitecto visa en el CALP.** Las instalaciones de gas, eléctricas y sanitarias las visa el **CPITLP**
> (Urquiza 564, Santa Rosa · (02954) 42-9781 · `santarosa@cpitlp.org.ar`) cuando las firma un instalador
> matriculado allí.

## 5.3 Permiso de Obra: qué debe contener el plano municipal

**Las 11 láminas/planillas exigidas por "Elementos que componen el plano"** (`urb` §5.4):

| # | Lámina | Escala |
|---|---|---|
| 1 | **Plantas de arquitectura** (con **espacio de estacionamiento**, **límite de solado y terreno absorbente**, **gabinete de instalaciones**, **pozo absorbente y perforación si no hay red**, cercos, retiros y distancia a cercos, **vereda con niveles tomando el lomo del cordón cuneta como ±0,00**) | 1:100 |
| 2 | Esquema de estructura (base, columnas, vigas, **encadenados**, losas, conductos, sentido de pendiente, tanque y su base, canaletas) | 1:100 |
| 3 | **Cortes: dos como mínimo, uno longitudinal y otro transversal**, incluyendo **cordón cuneta y límites de terreno**, y **profundidad de cimientos y sus dimensiones** | 1:100 |
| 4 | Frente (fachada) | 1:100 |
| 5 | Cerco Línea Municipal | 1:100 |
| 6 | Detalle de escalera (si hay) | 1:50 / corte 1:20 |
| 7 | **Detalle de canaleta de desagüe sobre L.M. y E.D.** | 1:20 |
| 8 | **Detalle de encadenado** (sección de H° y hierro) | 1:20 |
| 9 | Planillas de estructura | — |
| 10 | **Planillas de iluminación y ventilación** | ⚠ **requiere los Cuadros 3.4.5.1 y 3.4.5.2, que NO se consiguieron** — ver [Anexo C](#anexo-c--lo-que-falta-verificar-tabla-consolidada) |
| 11 | Silueta de superficies y cuadro de superficies | — |

**Notas obligatorias en el plano:**

- ***"LA FINCA CUENTA (o NO) CON LOS SERVICIOS DE PROVISIÓN DE AGUA CORRIENTE Y CLOACA".***
- ***"SUPERFICIE TOTAL AL 100 %"***: el total de superficies y proyecciones de todas las plantas **y aleros**, computadas al 100 %, para el cálculo del FOS.
- **Croquis de instalaciones sanitarias** (Disposición 131/2025, art. 2): agua (tanque, cisterna, caja de medición, línea principal y distancia a ejes), cloaca (cámara de inspección, distancia a ejes y tapada, o pozo absorbente), y pluviales (cámara de inspección o boca de acceso).
- **Carátula municipal oficial** (PDF y DWG publicados por el CPITLP).

> **Una vivienda unifamiliar NO presenta plano sanitario específico:** alcanza con el croquis en el plano de
> arquitectura. El plano sanitario solo se exige en edificios > 500 m², multifamiliares de más de 6 unidades y
> usos especiales (Disposición 131/2025, art. 3).

**Si el proyecto se aparta de alguna norma**, se adjunta **nota y memoria descriptiva de justificación
técnica**; el Manual trae un **modelo (Anexo I)** que declara bajo juramento que la desviación no afecta
derechos de terceros, no compromete seguridad, salubridad ni habitabilidad, no altera la morfología urbana y
se mantiene en parámetros proporcionados.

**Derechos de Construcción:** *"Es condición indispensable, para obtener el Permiso de Obra, abonar con
anterioridad los Derechos de Construcción"* (CE 2.1.5). **[VERIFICAR el importe en la Ordenanza
Fiscal/Tarifaria vigente — Dirección de Rentas o Planeamiento.] No hay ningún valor municipal verificado.**

**Validez del permiso:** ⚠ el art. 2.1.10 (texto 6445/2020) **se contradice internamente**: dice que a los tres
años sin inicio "deberá ratificarse" y también que "caducará automáticamente". **[VERIFICAR la lectura oficial
en Obras Particulares.] Criterio prudente: tratarlo como caduco a los 3 años sin inicio.**

## 5.4 Gas con Camuzzi

**Antes que nada: ¿hay red en la cuadra?** Llamar al **0810-555-3698** o WhatsApp **11 3931-1234** y consultar
factibilidad **por dirección**, antes de cerrar la implantación. Si no hay red, el camino es una **extensión de
red** (obra colectiva con los vecinos, empresa extensionista habilitada, habilitación municipal y transferencia
de la obra a Camuzzi por Ley 24.076): **agrega meses y un costo que no está en el cuadro de tasas**
(`gas` §3.0 y §3.6).

**Secuencia oficial de 12 pasos con red existente** (`gas` §3.1):

| # | Paso | Quién |
|---|---|---|
| 1 | Contratar un **gasista matriculado** (de la categoría que corresponda al caudal — §3.7) | Comitente / estudio |
| 2 | Presentar el **Formulario 3.4 A — Pedido de Factibilidad**, con planos catastrales y de obra | Instalador |
| 3 | Camuzzi analiza la solicitud | Camuzzi |
| 4 | Comienza la ejecución de la instalación interna | Instalador |
| 5 | Presentar el **Formulario 3.5 Parcial** | Instalador |
| 6 | **Inspección parcial de seguridad — cañería a la vista, ANTES de tapar** | Camuzzi |
| 7 | Instalación de los artefactos | Instalador |
| 8 | Presentar el **Formulario 3.5 Final** | Instalador |
| 9 | **Inspección final de seguridad**, con artefactos conectados | Camuzzi |
| 10 | **Solicitar el alta del servicio** — recién acá, no antes | **El titular** |
| 11 | Colocación del medidor | Camuzzi |
| 12 | Habilitación / alta | Camuzzi |

El canal real hoy es el **Portal de Matriculados** (`matriculados.camuzzigas.com.ar/ingreso`), donde el
instalador sigue el estado del expediente y **el cliente puede seguirlo y aprobar los formularios**.

**Documentación del alta (la firma el titular, no el profesional):** **escritura**, o **boleto de compraventa
con firmas certificadas ante escribano**, o contrato de alquiler con membrete, sello y firma; **DNI original**;
**poder certificado** si el solicitante no es el titular.

> ### ⚠ La trampa del 31 de marzo
> La matrícula del instalador **se renueva del 2 de enero al 31 de marzo**. *"Vencido dicho plazo, la
> Licenciataria no debe aceptar la presentación de ningún nuevo pedido de gas hasta tanto se haya efectivizado
> la renovación."* **Si se presenta la factibilidad en abril o mayo con un matriculado que no renovó, Camuzzi
> rechaza la presentación sin analizarla.** **Pedir constancia de matrícula vigente del año en curso antes de
> la primera presentación** — y cruzar **los dos padrones**: el buscador de Camuzzi (acredita la matrícula de
> gas) y el del CPITLP (acredita la matrícula profesional provincial) (`gas` §2.5).

**Costos:** los conceptos son estables y los importes los fija ENARGAS en el anexo *"Importes máximos de tasas y
cargos"*. Una vivienda unifamiliar cae en **"servicio completo sin zanjeo y tapada (≤ 1")"** + **"zanjeo y
tapada"** + **"rotura y reparación de vereda"** si la vereda está ejecutada, más **"colocación de medidor
≤ 10 m³/h"**. **No aparecen cargos separados por aprobación de plano ni por inspección** `[confirmar con
Camuzzi]`. **Los importes de junio 2024 que figuran en `gas` §3.4 están desactualizados: descargar el cuadro
tarifario vigente antes de cotizar.**

**Plazos: NO VERIFICADOS.** Camuzzi no publica plazos de análisis de factibilidad, aprobación, turno de
inspección ni colocación de medidor. **Planificar el cronograma de obra con holgura, porque la inspección
parcial condiciona el tapado de cañerías y por lo tanto contrapisos y revoques** (`gas` §3.5).

## 5.5 Agua, cloaca y electricidad

| Servicio | Quién | Estado del dato |
|---|---|---|
| **Agua potable y cloaca** | **Municipalidad de Santa Rosa — Dirección de Agua y Saneamiento / Saneamiento Urbano**, dependiente de la Secretaría de Obras y Servicios Públicos | **[VERIFICAR el circuito exacto, requisitos y costo.]** Preguntar concretamente: ¿se pide junto con el Permiso de Obra o después? ¿es trámite digital? ¿quién ejecuta la conexión a la red y quién la paga? ¿hay derecho de conexión por diámetro? |
| **Electricidad** | **CPE**, Raúl B. Díaz 218 · tel. 412222 · `cpe.coop.ar` sección **"Solicitud de factibilidad"** | **[VERIFICAR]** circuito y costo del derecho de conexión, y si exige certificado de instalación firmado por matriculado antes del suministro definitivo. La instalación interna se rige por **AEA 90364**; existe un **Certificado de Ejecución de Instalaciones Eléctricas en Inmuebles** publicado por CALP y CPITLP |
| **Perforación (lotes sin red de agua)** | **Administración Provincial del Agua (APA)**, Villegas 194, Santa Rosa · `apa.lapampa.gob.ar` | **[VERIFICAR]** si una perforación domiciliaria de vivienda unifamiliar requiere permiso, registro del perforista y/o estudio hidrogeológico (Código de Aguas, Ley 2581 y Dec. 2468/2011) |

## 5.6 Quién firma qué

| Documento | Lo firma |
|---|---|
| **Plano de arquitectura / Permiso de Obra municipal** | **Arquitecto matriculado en el CALP**, con visado previo. *"El proyecto, la dirección y la ejecución […] estarán a cargo de un profesional matriculado"* (CE 2.2.3) |
| **Acta de Inicio de Obra** | **Propietario + Director Técnico**, en carácter de **Declaración Jurada**, con **matrícula municipal**, **domicilio especial electrónico** y **listado de instaladores intervinientes** (nombre, tarea, teléfono, firma) |
| **Cálculo estructural y plano de fundaciones** | **Estructuralista [FIRMA].** *"El cálculo de las estructuras resistentes debe formar parte de la documentación que se presenta ante la Municipalidad para solicitar el Permiso de Obra"* (CE 4.5.2) |
| **Informe geotécnico** | **Profesional con incumbencia en geotecnia [FIRMA].** El arquitecto especifica, coordina y controla — **no adopta tensiones admisibles por su cuenta** |
| **Formulario 3.4 A, plano de gas, Formularios 3.5 Parcial y Final, conforme a obra de gas** | **Instalador matriculado por Camuzzi**, de la categoría que corresponda al caudal |
| **Solicitud de alta del servicio de gas** | **El titular** (propietario o quien acredite el domicilio) |
| **Instalación eléctrica** | Instalador matriculado; **Certificado de Ejecución de Instalaciones Eléctricas en Inmuebles** |
| **Instalaciones sanitarias y de gas ante el colegio** | Visado del **CPITLP** cuando las firma un instalador matriculado allí |
| **Final de Obra / Alta de Obra** | **El profesional responsable**, dentro de los **60 días corridos** de finalizados los trabajos (CE 2.1.9) |

**Un arquitecto SIN matrícula de instalador de gas no puede proyectar, firmar, presentar ni dirigir la
instalación de gas: ni el plano, ni la factibilidad, ni el pedido de inspección.** Con matrícula puede acceder
a la **1ª categoría "profesional"** (NAG-225 5.3.2), pero con limitaciones: hasta 4 bar de red, potencia
individual ≤ 175 kW, **sin acceso a la matrícula de Sistemas de Combustión**, y limitado a instalaciones dentro
de los límites municipales de los predios abastecidos. `[VERIFICAR — aparente inconsistencia: el inciso b) fija
16 mbar de presión interna para el arquitecto, mientras la 2ª categoría admite 19 mbar y NAG-200 exige ≥ 19 mbar
en el artefacto. Preguntar por escrito a Camuzzi y a ENARGAS antes de iniciar el trámite de matrícula.]`

**El rol real del arquitecto en el gas, que es grande** (`gas` §2.4.3): contratar (o hacer contratar) al
matriculado **en etapa de anteproyecto**; definir con él **la posición del nicho, los conductos, los pases y
las rejillas antes de cerrar plantas y fachadas**; coordinar el plano de gas con arquitectura, sanitarias y
eléctrica; **verificar en obra que se pida la inspección parcial antes de tapar**; y **exigir el plano conforme
a obra** para el legajo del comitente.

---

# FASE 6 — Obra

## 6.1 Puntos de detención críticos en esta casa

**"Punto de detención" (*hold point*): tarea que NO puede continuar sin la aprobación escrita de la Dirección
de Obra. Debe estar listada en el pliego. Es la herramienta más eficaz de control de calidad, porque obliga a
que la DO sea convocada** (`proy` §9.5).

| # | Momento | Control | Quién | Documento |
|---|---|---|---|---|
| 1 | **Replanteo** | Ejes, niveles y **retiros** verificados contra la ficha urbanística | DO | **Acta de replanteo** |
| **2** | **Fondo de excavación** | **Cota y estado del fondo.** En loess: **hormigón de limpieza el MISMO DÍA**; si no se puede, cubrir con film y prever desagote. **Nunca dejar la excavación abierta un fin de semana con pronóstico de lluvia** — una lluvia sobre el fondo satura el suelo de apoyo antes de que exista la casa | DO (+ geotécnico si hay duda) | Orden de servicio |
| **3** | **Manto compactado bajo platea** | **Densidad MEDIDA in situ**, no "a ojo": ≥ 95 % Proctor estándar, en capas ≤ 0,20 m | Laboratorio | **Protocolo de densidad** |
| **4** | **Armadura de la platea** | Diámetros, separaciones, **recubrimientos**, empalmes, separadores; **continuidad total de vigas de borde y nervios, sin interrupciones**; refuerzos sobre y bajo aberturas | DO | **Aprobación escrita — no se hormigona sin ella** |
| 5 | Encofrados | Aplome, nivel, estanqueidad, apuntalamiento | DO | Aprobación escrita |
| 6 | **Hormigonado** | **Presencia obligatoria del profesional responsable durante las tareas de hormigonado** (CE 2.3.4). Cono por camión; probetas a 7 y 28 días. **Curado de la platea ≥ 7 días**; hormigonar temprano en verano | DO + laboratorio | Remito, planilla y protocolo |
| **7** | **Film de polietileno 200 μ y capa aisladora** | Continuidad y solape ≥ 20 cm; **capa aisladora horizontal Y vertical** sin discontinuidades | DO | **Aprobación escrita — antes de tapar** |
| **8** | **Faja perimetral de XPS del piso** | **Colocada y tocándose con el XPS del muro.** Es irrecuperable después | DO | Aprobación escrita — **antes del contrapiso** |
| **9** | **Instalaciones enterradas, antes de tapar** | **Prueba hidráulica de desagües · prueba de presión de agua.** Cañerías **envainadas**, cámaras **estancas**, **ningún empalme bajo la platea** | Contratista ante DO | **Acta de prueba + fotos** |
| **10** | **Instalación de gas** | **Prueba de hermeticidad** e **INSPECCIÓN PARCIAL DE CAMUZZI APROBADA, con la cañería a la vista.** **Tapar antes obliga a abrir contrapisos y revoques: es el error más caro de la lista** | Gasista matriculado ante la distribuidora | Acta + constancia de inspección |
| 11 | Premarcos | A plomo, escuadra y **en el plano correcto: alineados con el aislante, no con la mampostería** | DO | Aprobación escrita |
| **12** | **Barrera de vapor de cubierta** | **Continua, solapada 15 cm y sellada en CADA perforación.** En cubierta ventilada: **lana no comprimida y bafles del alero colocados** | DO | **Aprobación escrita — antes de cerrar la cubierta** |
| **13** | **Encuentro muro–cubierta** | **El EPS del muro y el de la cubierta se tocan**; el parapeto está envuelto por sus tres caras | DO | Aprobación escrita |
| **14** | **ANCLAJE DE CUBIERTA** (si es liviana) | Fleje por cabio en zona interior; **doble fleje o fleje reforzado en los 2 m de cada una de las 4 esquinas**; **encadenado superior continuo, sin interrupciones en dinteles**; clavo helicoidal o tornillo; anclaje químico o barra embebida (no taco de expansión); fijación de chapa **en la cresta**, en cada onda en bordes y esquinas | DO + estructuralista | **Aprobación escrita — antes de colocar la chapa** |
| **15** | **Cubierta terminada** | **Prueba de estanqueidad por inundación 24–48 h** | Contratista ante DO | **Acta — antes de la protección y del cielorraso** |
| **16** | **SATE** | **Doble malla a 45° en las esquinas de vano**; **retorno del aislante sobre el marco**; **cabezas de espiga rehundidas y tapadas**; **XPS (no EPS) por debajo del perfil de arranque**, hasta 50–60 cm bajo NPT | DO | Aprobación escrita |
| **17** | **Colocación de carpinterías** | **Fondo de junta colocado**, espuma de PU en toda la holgura, sellador neutro en relación 2:1, **drenajes del marco NO tapados** | DO | Aprobación escrita |
| 18 | Instalación eléctrica | Continuidad, aislación, **medición de puesta a tierra**, funcionamiento de diferenciales | Electricista + DO | Protocolo |
| 19 | **Replanteo eléctrico** (previo a pasar caños) | Se recorre **en obra, con el electricista, con el plano amoblado en la mano, marcando con fibrón**. Ver checklist en `int` Anexo C | DO / interiorismo | **Acta de replanteo firmada** |
| 20 | Revoques, solados y pintura | **Paño de muestra aprobado antes de continuar**; despiece aprobado | DO | Aprobación escrita |
| **21** | **ANTES DE TAPAR CUALQUIER COSA** | **Fotografiar todo**: fundaciones e instalaciones enterradas, faja perimetral, barrera de vapor, encuentro muro-cubierta, retorno del aislante en los vanos, **todas las paredes abiertas con las cañerías a la vista**. **Es la única prueba de que se hizo, y es la documentación que salva la próxima reforma** | DO | **Archivo del legajo y entrega al comitente** |

**Y dos obligaciones formales que se controlan desde el día uno** (`urb` §5.5):

- **Documentación en obra:** copia del **plano municipal aprobado** y del **Permiso de Obra** (CE 2.3.3).
- **Cartel de obra al frente**, con nombre, título, matrícula y domicilio de los profesionales, la tarea de cada uno, y **número de Permiso de Obra y fecha de otorgamiento** (CE 4.1.6).
- **Obra paralizada**: se considera tal a los **4 meses consecutivos** sin trabajos, y hay obligación de comunicarlo antes de cumplirse el plazo (CE 2.1.7).
- **Cambio de profesional**: *"la obra deberá ser inmediatamente paralizada hasta la designación de un nuevo Profesional"* (CE 2.2.5).

## 6.2 Los diez controles de envolvente que no se saltean

Versión corta para llevar a la obra (`envolvente` §10.4):

1. **Antes del contrapiso:** faja perimetral de XPS colocada y **tocándose** con el XPS del muro.
2. **Antes del contrapiso:** film de polietileno 200 μ continuo, solapado 20 cm.
3. **Con la mampostería levantada:** premarcos a plomo, escuadra **y en el plano del aislante**.
4. **Antes de cerrar la cubierta:** barrera de vapor continua, solapada 15 cm, **sellada en cada perforación**.
5. **Antes de cerrar la cubierta:** lana **no comprimida** y bafles del alero colocados.
6. **Durante el SATE:** doble malla a 45° en esquinas de vano; retorno del aislante sobre el marco; espigas rehundidas y tapadas.
7. **Durante el SATE:** **XPS, no EPS**, por debajo del perfil de arranque.
8. **Encuentro muro-cubierta:** los dos aislantes se tocan; parapeto envuelto por sus tres caras.
9. **Carpinterías:** fondo de junta, espuma en toda la holgura, sellador 2:1, **drenajes libres**.
10. **Antes de tapar: fotografiar todo.**

## 6.3 El manual de uso que se le entrega al comitente

**Se entrega por escrito con la documentación final de obra, en una carilla y en lenguaje llano.** No es un
gesto de cortesía: **es la última pieza del proyecto estructural**, porque siete de los ocho disparadores del
colapso del loess son decisiones cotidianas del usuario (`suelo` §8.9 · `proy` §9.9).

> ### SU CASA ESTÁ CONSTRUIDA SOBRE SUELO LOÉSSICO
> **Es un suelo firme mientras está seco, y pierde resistencia cuando se moja de forma prolongada. Estas seis
> cosas mantienen su casa sana:**
>
> **1. No plante ni riegue contra las paredes.** La vereda perimetral está para eso. **El jardín empieza más
> allá.**
>
> **2. No modifique el nivel del terreno junto a la casa.** Si trae tierra para el jardín, que nunca quede
> más alta que la vereda ni tape la capa aisladora.
>
> **3. Mantenga selladas las juntas de la vereda perimetral.** Revíselas una vez por año y reponga el
> sellador. **Es media hora de trabajo y es lo más importante de esta lista.** Una vereda fisurada sin sellar
> es un embudo dirigido a la fundación.
>
> **4. Si se rompe un caño, arréglelo enseguida.** Una pérdida enterrada durante meses es lo único que puede
> dañar seriamente la estructura. Señales: consumo de agua alto sin motivo, mancha húmeda que no seca,
> hundimiento localizado del piso o de la vereda.
>
> **5. Limpie las canaletas y no cambie las descargas pluviales.** Nada de bajadas que descarguen al pie de la
> pared: **las descargas van a 3 metros o más de la casa**.
>
> **6. Si aparece una fisura nueva que crece, avísenos y no la tape.** Fotografíela con una regla al lado y
> con fecha. Una fisura tapada sin diagnóstico vuelve a aparecer.
>
> **Si va a hacer una pileta, un quincho, una ampliación o plantar árboles: consúltenos antes.**

**Y la parte térmica del mismo manual** (`envolvente` §10.3):

- **Cerrar las persianas de noche en invierno.** Reduce el K de la ventana entre **0,3 y 0,5 W/m²K**: es aislación gratis, ~7 W/K sobre 18 m² de aberturas.
- **Régimen de ventilación por estación:** en verano, **cerrar la casa al mediodía** (persianas + carpinterías cerradas) y **ventilar intensamente de noche** con las banderolas altas. En invierno, solo ventilación higiénica controlada.
- **Bajar la protección solar del oeste entre las 15 y las 20 h** en verano.
- **Repintar o lavar la cubierta clara cada 4–6 años**: con viento y tierra pierde reflectancia en 3–5 años, y con ella el +30 % de K admisible.
- **Limpieza de canaletas** y mantenimiento del revestimiento del SATE.

**Lo que va en la carpeta que se entrega, además del manual:** planos conforme a obra (**incluidos los de
instalaciones enterradas, con cotas**), **informe geotécnico y planos de fundación**, plano conforme a obra de
gas, actas de prueba (hidráulica, presión, hermeticidad de gas, inundación de cubierta), protocolo de puesta a
tierra, **el archivo fotográfico de todo lo que se tapó**, manuales y certificados de artefactos, y las
garantías (`suelo` §10.F · `gas` §8.3 · `int` §5.12).

## 6.4 Si aparecen fisuras: el protocolo

**En orden, y el orden importa** (`suelo` §9.3):

1. **No tapar.** Un revoque nuevo sobre una fisura viva borra la evidencia y retrasa el diagnóstico.
2. **Documentar:** fotos con **regla y fecha**, croquis de planta y alzados con todas las fisuras, y **relevamiento de niveles de piso en grilla** (manguera o láser).
3. **Instalar testigos** —mejor **fisurómetros** graduados y numerados—, con **lectura cada 15 días durante 3 meses**. Es la única forma de saber si el movimiento está activo.
4. **Buscar la fuente de agua** en el sector afectado: cantero, bajada pluvial, pozo absorbente, pileta, cañería. Verificar consumo con todas las canillas cerradas.
5. **Cortar la fuente inmediatamente.** En muchos casos el movimiento se detiene solo cuando el suelo deja de recibir agua.
6. **Convocar al estructuralista [FIRMA]**, con los testigos leídos, el relevamiento de niveles y el informe geotécnico original en la mano.
7. **Decidir con datos.** Si el movimiento se detuvo y no hay pérdida de nivel importante: reparar. Si sigue activo: recalce.

> **[FIRMA] Recalzar sin haber cortado la fuente de agua es tirar el dinero.** Primero se elimina la causa, se
> verifica con testigos que el movimiento se detuvo, y **recién entonces** se decide si hace falta recalce.
> El orden inverso es el error más caro que se comete con estas patologías.

**Cómo se distingue un asentamiento de una retracción** (`suelo` §9.2). En una casa de una planta no existe el
chequeo del edificio (fisura repetida en la misma vertical en todas las plantas); los sustitutos son cuatro
preguntas:

1. **¿Se ve por dentro y por fuera en el mismo lugar?** → estructural.
2. **¿Hay desnivel de piso medible?** → asentamiento.
3. **¿La vereda perimetral y el solado exterior también están rotos ahí?** → es el terreno.
4. **¿Hay una fuente de agua en ese sector?** → ya tenés el diagnóstico.

**Ubicación esperable en Santa Rosa: perimetral y de esquina** —del lado donde está el cantero regado, la
bajada pluvial, el pozo absorbente o la pileta—, porque **la platea y el solado impermeabilizan el suelo bajo
la casa y el agua que entra por el perímetro queda debajo, sin poder evaporar**. *Antes de peritar la casa,
caminar el perímetro y mirar el agua* (`suelo` §4.4 y §9.1).

---

# ANEXO A — Checklist de una carilla (para la primera reunión)

> Imprimir una por parcela. **Ninguna línea se dibuja hasta que esta hoja esté llena.**

```
OBRA: ..................................................  FECHA: ................
COMITENTE: ............................................  TEL: ..................
DIRECCIÓN / NOMENCLATURA CATASTRAL: ....................................................

A — LA PARCELA
[ ] Superficie ......... m²   Frente ......... m   Fondo ......... m   Ángulos verificados
[ ] ¿Intermedia o EN ESQUINA?  Si es esquina: frente/fondo definidos (CUA 4.3.1.1)
[ ] Ancho de vereda ......... m  →  3 % = ......... m
        NT ≥ NR + 3 % .........   NPB ≥ NR + 0,10 + 3 % .........   NP ≥ NR + 0,05 + 3 % .........
[ ] ¿Tiene cordón cuneta? SÍ / NO      [ ] ¿Tiene vereda reglamentaria? SÍ / NO
[ ] Escritura / boleto        [ ] Plano de mensura        [ ] Libre de deuda

B — RÉGIMEN URBANÍSTICO (Plano P1 + ficha oficial de Planeamiento)
[ ] DISTRITO: ............ (con numeral romano: R3I ≠ R3VII)
[ ] ¿R3VII? → PB a ≥ 1,20 m sobre el cordón (rampa de 12 m de desarrollo)
[ ] ¿R2eIII / R2eIV? → NO admiten vivienda individual nueva
[ ] ¿Frentista a CORREDOR (Plano P2)? → mandan los indicadores del corredor
[ ] ¿Zona de influencia del aeropuerto (Plano P4)?   [ ] ¿Protección patrimonial?
        FOS ......  Retiro frente ......  Retiro fondo PB ......  Retiro lateral ......
        C.A.S. ......  Densidad ......  Altura máx. ......  Cochera: obligatoria SÍ / NO

C — CÁLCULO PREVIO
[ ] Superficie × FOS = ......... m²
[ ] Huella real (menos retiros) = ......... m²      →  CONSTRUIBLE = el menor: ......... m²
[ ] C.A.S. = superficie × ...... = ......... m² PERMEABLES, y DÓNDE VAN: ................
[ ] Dormitorios por densidad = sup. × ...... ÷ 1,5 = ......   (o "1 vivienda por parcela")
[ ] Cochera 15 m², lado 2,90 m, altura 2,40 m  →  COMPUTA FOS
[ ] Casa + cochera + galería + ALEROS ≤ FOS ?
[ ] ¿Supera 300 m²? → trámite especial + doble inspección

D — SITIO
[ ] Posición en la cuenca: ALTO (E/N) / CASCO / BAJO (SO)  → napa esperable
[ ] Escurrimiento natural: ¿el lote recibe agua del vecino?
[ ] Cota de la boca de registro de cloaca → ¿desagota por gravedad?
[ ] Norte marcado. Barreras existentes al N (altura, largo, porosidad, caduco/perenne)
[ ] Exposición CIRSOC: B / C   (ante la duda, C. ¿Hay 450 m de tejido al N?)
[ ] Árboles existentes y su distancia al futuro perímetro

E — SERVICIOS
[ ] Agua de red SÍ / NO      [ ] Cloaca SÍ / NO   → si no: séptica 2×1.000 L + pozo (§1.5)
[ ] GAS EN LA CUADRA SÍ / NO   ¿baja o media presión? (0810-555-3698)
[ ] Electricidad: factibilidad CPE

F — PROGRAMA Y PLATA
[ ] Quiénes viven, cuántos dormitorios, cómo usan la casa (guion de 60 preguntas, ante §2.2)
[ ] ¿PILETA? SÍ / NO   ¿QUINCHO? ¿AMPLIACIÓN FUTURA?   → cambian fundación y caudal de gas
[ ] Escenario de CALEFACCIÓN: TB / caldera+radiadores / losa radiante  → define la matrícula
[ ] Presupuesto objetivo $ ................  ÷ $/m² del nivel = ......... m² posibles
[ ] Listados por escrito los costos que no son ladrillos (+25 a 35 %) e imprevistos 10 %

G — ENCARGO
[ ] ¿Están todos los que deciden?      [ ] Señales de alarma detectadas: ......
[ ] ESTUDIO DE SUELOS encargado (3 calicatas + 1 SPT 6 m + doble edométrico + química)
[ ] Programa por escrito enviado dentro de 48 h        [ ] Contrato / Orden de Trabajo
```

---

# ANEXO B — Los 10 errores que arruinan una casa en Santa Rosa

| # | Error | Por qué arruina la casa | Fuente |
|---|---|---|---|
| **1** | **Regar o poner un cantero contra la pared** | Es **la causa n.º 1 de colapso localizado** en vivienda. El loess mantiene su capacidad mientras está seco y **pierde volumen bruscamente al saturarse**: `σ_adm` cae de 1,0–1,5 a **0,3–0,8 kg/cm²** o menos, con descensos locales de 2 a 10 cm. Y como la platea impermeabiliza el suelo de abajo, **el agua que entra por el perímetro no puede evaporar**: por eso las fisuras son perimetrales y de esquina. Se evita con **vereda perimetral impermeable de 1,20–1,50 m con pendiente ≥ 2 % y junta elástica sellada** | `suelo` §4, §8.2 y §8.6 |
| **2** | **Bajada pluvial que descarga al pie de la fundación** | Ni "a la vereda perimetral", ni "sobre una piedra", ni a un caño corto que termina a 50 cm del muro. La descarga va **≥ 3,00 m** del perímetro, por cañería enterrada **estanca** con cámaras de inspección. Además, el Código **prohíbe** la caída de pluviales a la vía pública, a linderos o sobre muros divisorios | `suelo` §8.3 · CE 4.9 |
| **3** | **Saltearse el estudio de suelos porque "el municipio no lo pide"** | Es cierto que no lo pide (CE 4.4.2 solo lo exige en obras de más de 3 pisos), **pero es una exención administrativa, no técnica, y no traslada la responsabilidad profesional**. El estudio cuesta **0,3–0,8 %** del costo de obra; recalzar cuesta **15–40 %** — y la reparación **nunca deja la casa como estaba** | `urb` §4.15 · `suelo` §6.1 y §6.7 |
| **4** | **Fundar con apoyo mixto: media zapata sobre tosca, media sobre limo suelto** | Es **la receta exacta del asentamiento diferencial**, y el mecanismo n.º 1 de patología en vivienda pampeana. La tosca **no es continua**: puede estar a 0,60 m en un extremo del lote y a 2,50 m en el otro, tiene **crotovinas de tamaño métrico** (cavidades) y **rizolitos rellenos de arena** que conducen agua. **Si la tosca es errática, la respuesta no es "seguir la tosca": es no apoyarse en ella** y resolver con platea sobre manto compactado uniforme | `suelo` §2.3 y §7.1 |
| **5** | **Aislar el techo poco (o nada) y gastar en DVH** | En una casa de una planta **el techo es el 41 % de la envolvente** y recibe **900 W/m² de radiación de diseño** contra 400 de los muros. Aislar la cubierta ahorra **8.147 kWh/año**; el DVH, **1.830**. **Con el mismo dinero se compra 4,5 veces más ahorro en el techo** — y se hace porque el DVH se ve y el aislante del techo no. Una **losa sin aislante tiene K = 1,83: 2,4 veces por encima del Nivel C** | `envolvente` §3 y §9.3 |
| **6** | **Dimensionar la cubierta por invierno, o ponerla oscura** | **En Santa Rosa manda SIEMPRE el verano en cubierta, con cualquier color** (0,19 de verano contra 0,26 de invierno en Nivel A; con cubierta clara, 0,247 contra 0,26). Y el color no es estética: **α < 0,6 da +30 % de K admisible = 40 mm menos de EPS en toda la cubierta**, y baja la temperatura superficial de ~70 a ~45 °C. Una cubierta oscura sin recalcular con la corrección de **−20 %** es un error de proyecto | `envolvente` §1.7 y §3.1 |
| **7** | **Aislar por dentro (o con cámara de aire vacía) en vez de por fuera** | Con K_muro objetivo 0,29, la norma exige **K_pt ≤ 0,45** en los puentes térmicos — **imposible con aislación interior o en cámara**: el encadenado desnudo tiene **K = 2,92**, seis veces y media el admisible. Además la aislación interior **deja la masa del lado equivocado**, y con 14,4 K de amplitud estival la inercia vale tanto como el aislante. En una casa de una planta hay **150 a 200 m lineales de puente térmico** sobre 106,8 m² de muro. **El SATE resuelve el 90 % de ellos de un saque** | `envolvente` §2.5 y §6.9 |
| **8** | **No anclar la cubierta liviana (o anclar igual las esquinas que el centro)** | Una cubierta de chapa recibe una **succión mayorada 4 a 6 veces mayor que su peso estabilizante**: 177 kN de succión contra 44 kN de peso. Y en los **2 m de cada una de las 4 esquinas la demanda es 53 % mayor** que en el centro (7,8 contra 5,1 kN/m). El eslabón que falta en el 90 % de las obras es **el fleje entre cabio y encadenado**, y el segundo error es **el encadenado interrumpido en el dintel de una abertura grande**: el anclaje ancla a nada. **La casa no se vuelca: se destecha** | `viento` §8.4 y §8.5 |
| **9** | **Abrir al oeste, y hacer la galería baja** | El muro oeste a las 17 h del 21/12 "ve" una temperatura sol-aire de **58,8 °C**, y **ningún alero lo detiene**: el sol está a 26° de altura y haría falta una proyección de **4,30 m**. **No abrir al oeste es la única solución perfecta, y es gratis si se toma en el anteproyecto.** Del otro lado, **una galería norte de 2,40 m de altura bloquea el sol de invierno**: con 2,80–3,20 m el sol de junio entra **4,85 a 5,54 m** adentro del local. **La altura de la galería importa más que su profundidad** | `envolvente` §8.5 y §8.6 |
| **10** | **Contratar al gasista sin haber decidido la calefacción** | El techo de la **3ª categoría es 5 m³/h**. Los escenarios con **caldera + calefón (6,80 m³/h)** o **caldera dual de 40.000 kcal/h + secarropas (5,68 m³/h)** lo superan, y el instalador queda fuera de alcance a mitad de obra. Se suma la **trampa del 31 de marzo**: con la matrícula sin renovar, **Camuzzi rechaza la presentación sin analizarla**. Y el error más caro de la obra: **tapar la cañería antes de la inspección parcial**, que obliga a abrir contrapisos y revoques | `gas` §2.3, §2.5 y §8.1 |

**Menciones de honor** (errores que no matan la casa pero cuestan plata): pegar el **nicho de gas al pilar
eléctrico** (mínimo 0,50 m, NAG-200 3.2.1: *el error más repetido en fachadas de casas*) · **abrir una ventana
a menos de 3,00 m del eje divisorio** enfrentada a él (CE 3.8.1) · **olvidar que los aleros computan FOS** ·
**pavimentar todo el patio** y descubrir el C.A.S. cuando el plano vuelve observado · **medianera de 2,20 m sin
pilastras** (factor 8 en contra: se cae) · **grava suelta en cubierta plana** (se vuela y rompe vidrios) ·
**cerrar las paredes antes del replanteo eléctrico** (el proyecto de iluminación queda congelado).

---

# ANEXO C — Lo que falta verificar (tabla consolidada)

> **Regla del repositorio: preferimos un hueco señalado a un número inventado.** Nada de esta tabla se usa para
> cotizar, comprometer plazos ni firmar documentación hasta que esté resuelto. **Cada ítem resuelto se
> documenta y se archiva por parcela.**

## C.1 🔴 Bloqueantes — sin esto no se puede firmar un plano

| # | Qué pedir, con nombre exacto | Dónde / a quién | Para qué |
|---|---|---|---|
| **1** | **CUADRO 3.4.4.a, CUADRO 3.4.4.b y CUADRO 3.4.4.c — "Dimensiones mínimas de los locales"** del Código de Edificación (Ord. 1581/95). El Código remite literalmente a *"TEMAS DE INTERÉS – Sector: CUADROS CÓDIGO DE EDIFICACIÓN"* del sitio del Concejo Deliberante, que está detrás de un desafío de **Cloudflare** (HTTP 403) y **no tiene copia en Wayback** | **Dirección de Planeamiento Urbano y Obras Particulares**, Municipalidad de Santa Rosa · o **Concejo Deliberante**, mesa de entradas · o **CALP** Área Técnica, `tecnica@colegioarqlapampa.org.ar` | **Fijar superficie mínima, lado mínimo y ALTURA LIBRE MÍNIMA de dormitorio, estar, comedor, cocina, baño y lavadero. Sin esto no se puede validar ninguna planta.** Hoy el Código solo fija indirectamente que el fondo de una viga aparente no baja de 2,30 m del solado |
| **2** | **CUADRO 3.4.5.1 — "Iluminación y ventilación natural"** (valores de **X** y relación **K/I**) **y GRÁFICO 3.4.5** (salientes, alturas de vanos, profundidad de locales) | ídem | **Completar la Planilla de Iluminación y Ventilación, obligatoria en el plano municipal (lámina 10).** Se conoce la estructura de la fórmula (I = A/X, con K derivado de I) pero **no los valores**. **Es el hueco más urgente de todo el corpus** |
| **3** | **CUADRO 3.4.5.2 — "Ventilación natural por conducto"** | ídem | Baños y cocinas sin vano al exterior; secciones de conducto |
| **4** | **Ordenanza Fiscal / Tarifaria vigente**, capítulo de **Derechos de Construcción** | **Dirección de Rentas** o **Planeamiento Urbano y Obras Particulares** | **Cotizar el trámite. Hoy no hay ningún importe municipal verificado** |
| **5** | **Resolución vigente del CALP** con el **valor de referencia del m² y el aporte mínimo profesional** | **CALP**, Don Bosco 243 · Adm. Contable **(02954) 271011** · `adm@colegioarqlapampa.org.ar` | Cotizar visado y aportes. Se actualiza como máximo cada 2 meses. *(La última obtenida es la Res. 09/2024: $ 913.336/m² desde el 1/4/2024, aporte mínimo $ 8.100 — **desactualizada**)* |

## C.2 🟠 Importantes — evitan retrabajo

| # | Qué pedir | Dónde / a quién | Para qué |
|---|---|---|---|
| 6 | **Requisitos técnicos de la presentación digital**: formatos de archivo, tamaño máximo, nomenclatura, PDF vectorial o rasterizado, cómo se firma digitalmente | Planeamiento Urbano y Obras Particulares · mesa de entradas digital de `santarosa.gob.ar` | El Manual dice "únicamente digital" pero no especifica formato |
| 7 | **Número exacto y fecha de la Disposición** que aprueba el Manual de Procedimientos (el CPITLP la publica como "N° 16"; la copia escaneada no se lee) | Planeamiento Urbano y Obras Particulares | Citarla correctamente en notas y memorias |
| 8 | **Circuito de solicitud de conexión de AGUA y de CLOACA** para obra nueva: formulario, requisitos, plazo, costo, quién ejecuta la conexión a la red | **Dirección de Agua y Saneamiento**, Municipalidad | Programar la obra y cotizar |
| 9 | **Solicitud de factibilidad eléctrica** y requisitos de conexión definitiva; reglamento de tablero y de derivación a usuarios | **CPE**, Raúl B. Díaz 218 · `cpe.coop.ar` | Dimensionar el gabinete de medidores y la acometida en el plano |
| 10 | **Régimen de perforaciones domiciliarias** (¿permiso? ¿perforista registrado? ¿estudio hidrogeológico?) | **APA**, Villegas 194 · `apaconsultas@lapampa.gob.ar` | Obligatorio en lotes sin red de agua |
| 11 | **Confirmación escrita del distrito de la parcela** | Planeamiento Urbano | El Plano P1 es de 2021/2022: puede haber ordenanzas de excepción posteriores sobre parcelas puntuales |
| **12** | **Profundidad de la napa registrada en el entorno del lote y serie histórica.** Pedir el trabajo *"Registros y análisis del comportamiento piezométrico de las aguas subterráneas del subsuelo de la Ciudad de Santa Rosa"* (censo de **148 perforaciones urbanas de la APA + 21 domiciliarias**) | **APA de La Pampa** · ficha en la biblioteca del **CFI** | **No hay mapa público de isoprofundidades de napa de la ciudad.** Es el documento a pedir |
| **13** | **Si el límite de 5 m³/h de la 3ª categoría se mide por SUMA DIRECTA o por Q_si** | **Camuzzi**, `matriculados@camuzzigas.com.ar` — **por escrito** | **Decide la categoría de matrícula en los escenarios B y D** |
| **14** | **Presión de la red en la cuadra (baja o media), caudal disponible y tamaño de medidor asignado** | **Camuzzi**, 0810-555-3698 + **exigirlo en la respuesta al Form. 3.4 A** | Define si hace falta **regulador domiciliario en el nicho** (lo paga el cliente) y el tamaño del gabinete |
| **15** | **NAG-200 §6.5 y §6.6, edición vigente:** altura de remate de conductos sobre cubierta y **distancias mínimas de terminales de cámara estanca a ventanas, esquinas, aleros y medianeras** | Instalador matriculado + ENARGAS | **Se define ANTES de cerrar la fachada**: los terminales son visibles y su posición no es negociable después |
| 16 | **Profundidad mínima de enterrado** de la cañería de gas, vainas y **separaciones a agua, cloaca y electricidad** | Instalador matriculado + NAG-200 vigente | No inventar un número |
| 17 | **Edición vigente de NAG-200**, su numeración de apartados, y si **prNAG-225 (2019)** ya es norma definitiva | ENARGAS | **Antes de firmar cualquier plano de gas** |
| 18 | **Alcance real del arquitecto matriculado en gas** — contradicción **16 mbar (NAG-225 5.3.2.1.b) vs. 19 mbar** de la 2ª categoría y de NAG-200 | Camuzzi + ENARGAS | Antes de que un arquitecto del estudio inicie el trámite de matrícula |
| 19 | **Si el plano de gas requiere visado previo del CPITLP** y su arancel | **CPITLP Santa Rosa**, Urquiza 564 · (02954) 42-9781 | Los T&C del Portal de Matriculados obligan a *"presentar los visados requeridos por los colegios profesionales"* |
| **20** | **Qué edición de CIRSOC exige hoy el visado de estructuras en Santa Rosa** (102-2005 con **1,6 W**, o la 3ª generación 2025 con **1,0 W**) | Municipalidad + CPITLP / CALP | ⚠ **Mezclar generaciones produce un error de ~60 % en la acción lateral**, y puede caer para cualquiera de los dos lados. Mientras no haya respuesta: resolver con **102-2005 + 1,6 W** y verificar contra 102-25 |
| 21 | **Texto vigente del Código de Edificación** en versión legible y **si incorpora exigencias de acondicionamiento térmico**, IRAM 11601/11605 o etiquetado | Concejo Deliberante / CPITLP | Puede haber exigencias térmicas municipales no relevadas |
| 22 | **Ley provincial de La Pampa de acondicionamiento térmico** (análoga a la 13.059 PBA) o de **obligatoriedad del etiquetado**; y el **registro de certificadores PRONEV habilitados** en la provincia | **Digesto de la Provincia de La Pampa** + **CALP** | No se encontró ninguna. La Pampa **sí está adherida al PRONEV**, pero la obligatoriedad la fija cada provincia por ley propia |

## C.3 🟡 Deseables y datos de producto

| # | Qué pedir | Dónde | Para qué |
|---|---|---|---|
| 23 | **Ordenanzas modificatorias del CUA posteriores a noviembre de 2023** | Concejo Deliberante | Cambios de delimitación o de indicadores |
| 24 | **Ordenanza 6445/2020** en versión legible (la disponible es un escaneo de baja calidad) | Concejo Deliberante | Precisar arts. 2.1.2, 2.1.9, **2.1.10 (la contradicción de validez del permiso)** y 2.1.12 |
| 25 | **Ordenanzas 783/90, 643/89 y 936/91** (patrimonio) | Concejo Deliberante | Solo si el lote está en R2eII o hay preexistencia inventariada |
| 26 | **Criterio oficial sobre el redondeo de la densidad** y sobre **cómo se computa y se acredita el C.A.S.** (¿un piso permeable computa, o solo la tierra desnuda? ¿hay que graficarlo y acotarlo?) | Planeamiento Urbano | Ver las 9 ambigüedades de `urb` §8 |
| 27 | **Ordenanza de arbolado**: distancias obligatorias y especies permitidas/prohibidas en vereda y en lote | Municipalidad | Coordina barrera de viento con distancias a fundación |
| 28 | **Distancias de pozo absorbente** exigidas por el Código de Edificación y la APA en Santa Rosa | Municipalidad + APA | Las distancias citadas (1,50 m a eje divisorio, 2,00 m a otro pozo, 10,00 m a captación) **son de otras jurisdicciones**, dadas como orden de magnitud |
| 29 | **Coeficiente de absorción solar α** de la teja, membrana o chapa **efectivamente especificadas** | Ficha técnica del producto | **Decide 20–40 mm de aislante en toda la cubierta** |
| 30 | **Factor solar (g), coeficiente de sombra y TL** de cada composición de vidrio ofertada | Planilla del proveedor (VASA/Blindex y equivalentes) | **Decide la estrategia de vidrio por orientación** |
| 31 | **Espesor máximo de EPS admitido por el sistema SATE**, cantidad y longitud de fijaciones **para la zona de viento de La Pampa**, índice de reflectancia mínimo del revestimiento y clasificación de reacción al fuego | Manual del fabricante del sistema + CIRSOC 102 | **Alto para la ejecución** |
| 32 | **Capacidad de arranque por perforación (*pull-through*)** de la chapa especificada, para su espesor y tipo de arandela | Fabricante de la chapa | **Es el dato que gobierna el anclaje y ningún catálogo argentino lo da por defecto: hay que pedirlo** |
| 33 | **λ del XPS** (no figura en IRAM 11601; se usó 0,033) y **Rt de bloques de hormigón huecos** y del hueco cerámico de 8 cm | IRAM 11601 Tablas A.2/A.3 + ficha técnica con ensayo | Afecta aislaciones enterradas y algunas soluciones de muro |
| 34 | **Factores de resistencia a la difusión de vapor μ** de los materiales usados en la verificación de condensación | IRAM 11601 y fichas técnicas | Las conclusiones cualitativas son robustas; los números exactos no |
| 35 | **Valores ψ de puentes térmicos lineales** (ISO 14683) y verificación 2D de los detalles concretos | Cálculo con THERM / Flixo / HTflux | Medio |
| 36 | **Umbral exacto de "viento fuerte"** del SMN y si "viento máximo diario" es ráfaga instantánea o promedio de intervalo | Glosario del SMN | Si fuera promedio de 1 o 10 minutos, el valor comparable con el CIRSOC sería **aún mayor** |
| 37 | **Valores de GC_p de las Figuras 5B y 5B (cont.)** del CIRSOC 102-2005 en zonas 2 y 3 para pendientes intermedias | Lectura directa de las figuras impresas | Fueron **leídos de curvas**, no de una tabla. **Confirmar antes de firmar** |
| 38 | **Costos relativos y precios reales** de corralones y contratistas de Santa Rosa; **tarifa de gas y poder calorífico**; **cotización de carpinterías** | Relevamiento de mercado local + distribuidora | **Es el único dato que falta para cerrar el análisis económico** de las tablas de prioridad de inversión |
| 39 | **Disponibilidad local en Santa Rosa** de: HCCA, sistemas SATE completos, **bovedillas de EPS**, XPS, carpintería con RPT y ensayo *Blower Door* | Relevamiento de mercado | **Alto para la viabilidad**: varias soluciones recomendadas dependen de que el producto exista en plaza |
| 40 | **A qué subzona pertenece Santa Rosa** (La Pampa Norte o La Pampa Sur) y los rangos de m³/año de las categorías R1 a R4 | Camuzzi / ENARGAS | Informar tarifa al comitente |

## C.4 Advertencias de método sobre las fuentes ya obtenidas

| Advertencia | Consecuencia |
|---|---|
| **El cuerpo del Código Urbano Ambiental (Ord. 6976/2023) es un escaneo sin capa de texto; todo lo transcripto proviene de un OCR** | **Antes de firmar un plano hay que verificar cada número contra la página del PDF.** El Código de Edificación, en cambio, tiene capa de texto real: sus transcripciones son fieles |
| **La ficha urbanística de la parcela se pide SIEMPRE en Planeamiento** | Puede haber ordenanzas modificatorias posteriores a 2023 y particularidades del lote que ninguna tabla general recoge |
| **La rosa de los vientos del SMN es de una serie de 10 años (2011-2020), no de 30** | Es lo mejor homogéneo disponible y alcanza para decidir, **pero no se presenta como "normal climatológica de 30 años"** |
| **Los parámetros geotécnicos de referencia NO son de Santa Rosa**: son del loess pampeano en general | Sirven **solo para dimensionar el anteproyecto y para detectar un informe absurdo**. **No hay banco de datos geotécnicos publicado de la ciudad**: quien ofrezca un número "de la zona" sin ensayo, está adivinando |
| **Cualquier antecedente de napa anterior a ~2015 es inservible** | *"Un vecino que te diga 'acá nunca hubo agua' está describiendo una ciudad que ya no existe"* |
| **El valor de referencia del m² del CALP y todo importe monetario llevan fecha** | Si la fecha está vieja, **el dato está mal** |

---

*Guía de proyecto del estudio, destilada de los documentos verificados del repositorio. **No sustituye a la
ficha urbanística oficial de la parcela, al informe geotécnico del lote, al cálculo estructural firmado ni a la
norma vigente.** Todo valor marcado **[PD]** es orden de magnitud para anteproyecto; todo valor marcado
**[VERIFICAR]** no está confirmado y no debe usarse para cotizar, comprometer plazos ni firmar documentación.
Cuando esta guía y el informe geotécnico, la ficha oficial o la norma digan cosas distintas, **mandan esos**.*
