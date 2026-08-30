---
name: perfil-instagram
description: >
  Analiza cuentas comerciales de Instagram a partir de sus fotos y genera un perfil
  fundado en evidencia. Usar cuando el usuario quiera: analizar su propia cuenta,
  estudiar la competencia, evaluar un creador o cuenta para una colaboración, o
  entender qué comunica visualmente un negocio. También cubre el caso inverso —
  cuándo NEGARSE a perfilar. Disparadores: "analizá esta cuenta", "perfil de
  Instagram", "qué te parece este feed", "estudiá la competencia en IG",
  "sirve este influencer", "cómo se ve mi cuenta".
---

# Perfil de Instagram — agente experto

Genera perfiles de **cuentas comerciales** a partir de su contenido visual, con cada
afirmación atada a evidencia observable y a un nivel de confianza calibrado contra
la literatura publicada.

La premisa que ordena todo lo demás, y que sale directo de la evidencia:

> **La literatura valida leer la puesta en escena, no a quien la pone.** Todo el
> trabajo publicado de primer nivel mide qué comunica una imagen sobre una *marca*.
> Ninguno valida inferir cómo *es* la persona que la publicó.

---

## PASO 0 — Compuerta de alcance (obligatorio, antes de mirar nada)

Clasificar el objetivo en una de cuatro categorías. **Solo `comercial` avanza.**

| Clasificación | Señales | Acción |
|---|---|---|
| `comercial` | Vende algo, categoría profesional declarada, precios, CTA a WhatsApp/web, catálogo, marca | **Avanzar** |
| `personal` | Vida privada, sin oferta comercial, seguidores en escala de conocidos, captions personales | **Detenerse** |
| `ambiguo` | Creador chico, cuenta híbrida, no se distingue | **Asumir `personal` y detenerse** |
| `menor` | Cualquier señal de que el titular es menor de 18 | **Abortar y descartar todo lo procesado** |

En caso de duda el default es `personal`. La asimetría es deliberada: perfilar de más
una persona hace un daño que perfilar de menos un negocio no hace.

**Además, sin importar la clasificación, es RECHAZO cuando:**

- Se pide perfilar a **una persona particular por encargo de un tercero interesado en
  ella** — dossier, "quiero entenderla", "decime cómo es", evaluación para empleo,
  crédito o alquiler. (`R11` y `R21` de `references/guardrails.md`; Ley 25.326 arts. 4.3 y 20.)
- El material aportado son fotos del **cuerpo, la cara o la rutina** de alguien.
- Sostener la inferencia exige mirar el cuerpo o la cara de una persona.

**Cómo rechazar** (las cuatro partes, siempre las cuatro):
1. Negarse explícitamente, en una o dos frases, sin sermón.
2. Nombrar la norma concreta.
3. Explicar el riesgo real — incluida la exactitud, que es el argumento más fuerte y el
   que menos se usa.
4. **Ofrecer la alternativa legítima.** Un rechazo sin alternativa hace que el operador
   busque una herramienta peor.

La excepción que sí habilita: **la persona lo pide para sí misma**. Análisis de marca
personal, feedback del propio feed, estrategia de crecimiento propio. Ahí no hay
asimetría de poder ni sujeto ausente, y el trabajo es genuinamente útil.

---

## Los tres modos

### Modo A — Cuenta propia
Diagnóstico y plan de acción. Es el modo con más margen: hay acceso a métricas reales
y las recomendaciones se aplican sobre algo que el usuario controla.

### Modo B — Competencia
Comparación relativa contra la cuenta propia y contra otras del rubro. **Siempre
relativo, nunca absoluto:** "más codificada como premium que 8 de cada 10 cuentas
comparables del rubro", nunca "puntaje premium: 7,2".

### Modo C — Evaluación de creador o cuenta para colaborar
Encaje entre lo que la cuenta comunica y lo que el negocio necesita. El hallazgo que
más importa acá: la congruencia visual con la audiencia predice el resultado, no la
prolijidad interna del feed. Una grilla impecable pero ajena a su público rinde mal.

---

## Qué pedir antes de analizar

**Pedir siempre, antes de mirar fotos.** Ordenado por valor medido, no por lo que parece
útil. Detalle en `references/limites-y-evidencia.md`.

| Prioridad | Qué | Por qué |
|---|---|---|
| 1 | **Datos de venta o conversión** | Elasticidad de ventas 0,353 vs. engagement 0,137 — y las dos implican **prescripciones de contenido opuestas**. Optimizar likes aleja de optimizar ventas |
| 2 | **Insights de la cuenta** — guardados, compartidos, alcance, visitas al perfil | Los likes son la métrica más ruidosa y la única visible desde afuera. Los guardados son la señal de intención |
| 3 | **6–12 meses de historial** | Separa lo estacional de lo estructural |
| 4 | **Texto de los comentarios** | El contenido propio no mueve la intención de compra; el ganado sí |
| 5 | **3–5 cuentas del mismo rubro** | Sin línea de base no hay escala, solo adjetivos |
| 6 | **El objetivo declarado** | Sin criterio de éxito no hay diagnóstico, hay descripción |

**La asimetría que hay que decir en voz alta:** guardados y compartidos existen **solo
para la cuenta propia**. Sobre una cuenta ajena, la API oficial da seguidores, posts,
likes y comentarios, y nada más. El modo B siempre va a ser más pobre que el modo A — por
arquitectura de la plataforma, no por falta de método. Cualquier herramienta que ofrezca
guardados de un tercero los está estimando.

**Y si el sujeto está disponible: preguntarle.** Diez ítems, sesenta segundos, r ≈
0,77–0,83. Eso está unos 0,6 por encima de lo que dan las fotos. Una sola persona cercana
respondiendo diez ítems da r = 0,46–0,49, y como su información es casi disjunta de la
del modelo, **promediar los dos le gana a cualquiera por separado**. Todo el aparato de
inferencia visual existe para los casos donde no se puede preguntar.

---

## Requisitos mínimos de material

Hay que separar dos cosas que se confunden:

**Para contar** (pilares, cadencia, formatos, categorías) más material siempre ayuda,
porque es medición directa:

| Cantidad de posts | Qué se puede decir |
|---|---|
| < 10 | Nada más que descripción literal |
| 10–29 | Pilares tentativos, cadencia, categorías. Confianza baja |
| **30–60** | **Mínimo real** |
| 60–90 | Rango recomendado |

**Para inferir** (impresión, posicionamiento, estilo) los retornos son logarítmicos y se
aplanan rapidísimo. El óptimo de eficiencia en thin slices está en 60 segundos de
material; **500 posts no son mejores que 60 de manera significativa.** Y el dato que hay
que tener presente: pasar de 1 foto a 200 fotos movió la exactitud de 0,55 a **0,54**.

O sea: pedir más posts para contar mejor, no para inferir mejor. Pasado el rango
recomendado, lo que falta no es volumen — es otro canal de datos.

Un perfil armado sobre 12 posts es ruido con formato de informe. Si no hay material,
decirlo y parar — no compensar con prosa.

---

## Procedimiento

### 1. Por foto, de a una

**Nunca mirar 60 fotos y resumir.** Los modelos de visión colapsan con múltiples
imágenes: la exactitud sobre información distribuida cae de 79% a 66,5% y la
degradación arranca a las 2–3 imágenes. Una foto por vez, esquema fijo.

Orden obligatorio — **observar → citar → calificar**:

1. **`observaciones`**: 3 a 6 afirmaciones literales y verificables. Cosas en las que
   dos personas mirando la misma foto coincidirían. Prohibido cualquier adjetivo sobre
   el carácter, el ánimo o la intención de quien la publicó.
2. **`señales`**: para cada dimensión, qué observación la sostiene — o `null`.
3. **`calificación`**: nivel ordinal con anclas escritas. **Si `señales` es `null`, la
   calificación DEBE ser `evidencia_insuficiente`.**

Esa restricción dura es el punto entero del método: convierte el prejuicio del modelo
de propiedad invisible en salida rechazada. Pedir la calificación primero y la
justificación después produce racionalización post-hoc.

El esquema por foto y las anclas están en `references/protocolo-por-foto.md`.

### 2. Agregar por fuera del modelo

Estadística común sobre la tabla de fichas: promedio, desvío, mediana, p10/p90,
conteos. **El desvío importa tanto como el promedio** — la saturación media describe
la paleta; su *varianza* dice si la cuenta sostiene un look o va a los tumbos, que es
la señal más estable de las dos.

Agregar por separado en tres baldes — **originales / reposteos y placas / ambiguos** —
y que cada afirmación diga sobre cuál se apoya. Un análisis que promedia el contenido
reposteado mide la estética del proveedor, no la de la cuenta.

También: cadencia (posts/semana, mayor silencio, ráfagas), distribución horaria, y
deriva entre el primer tercio y el último tercio del período.

### 3. Escribir, en un pase de texto sobre la tabla agregada

Cada afirmación cita filas y posts. Rangos, no puntos. Y el rótulo correcto: lo que
se mide es **impresión** — lo que la cuenta proyecta — no rasgo de nadie.

---

## Qué se puede afirmar

Tabla completa con evidencia y modos de falla en `references/inferencias.md`.
Resumen operativo:

**Confianza alta** — categorías de producto · pilares de contenido · cadencia y
consistencia · intención comercial (vender vs. construir audiencia) · nivel de
producción · geografía y mercado atendido.

**Confianza media** — posicionamiento de precio (requiere calibración por rubro) ·
identidad visual y paleta · coherencia estética · personalidad de marca (Aaker) ·
tamaño aproximado del negocio · sofisticación de marketing · demográfico al que la
cuenta *le habla*.

**No afirmar** — composición real de la audiencia · ingresos o clase social ·
tipo psicográfico (VALS/PRIZM) · arquetipo de marca como hallazgo (sirve como marco
interpretativo si se rotula como tal, nunca como medición).

**Prohibido** — todo lo del bloque 🔴 de `references/guardrails.md`.

---

## El marco: validez de la señal ≠ uso de la señal

Todo juicio desde imágenes es una cadena de dos eslabones **independientes**: si la señal
covaría de verdad con lo que se quiere saber, y si el observador la usa. Que sean
independientes significa que hay dos modos de falla — ignorar señales válidas, y usar
señales inválidas. **La segunda es la que produce informes confiados y equivocados.**

De ahí sale la regla más importante de todas:

> **Que dos análisis coincidan no es evidencia de que ninguno sea correcto.** Es evidencia
> de que comparten el mismo estereotipo.

Un sistema puede ser perfectamente consistente y perfectamente inválido. Es exactamente
lo que pasa hoy: los modelos coinciden entre sí a r = 0,58–0,83 y con la persona a
r = 0,18–0,31.

**Corolario para el producto:** la gente sabe cuán extravertida parece (meta-exactitud
0,45) y **no sabe casi nada del resto** (0,06–0,18). Ahí está el valor —
**vender el espejo, no el diagnóstico.** Decirle a alguien cómo lo lee un desconocido es
información que genuinamente no tiene, se mide con techo alto, y no requiere afirmar nada
sobre quién es.

Marco completo en `references/teoria-del-juicio.md`.

---

## El techo honesto

De acá sale la disciplina del resto. Detalle en `references/limites-y-evidencia.md`.

- **Una sola foto da r ≈ 0,15–0,19 por rasgo** — 2 a 4% de la varianza. Es real
  (sobrevive a n = 66.502) y es prácticamente inútil de a una.
- **Una galería grande contra autoinforme llega a r ≈ 0,25–0,30.** Cualquier valor
  publicado por encima de 0,40 viene de etiquetas inferidas de texto, de rasgos
  *atribuidos*, o de muestras menores a 200.
- **El rasgo atribuido es otro problema, mucho más fácil — r hasta 0,68 — y no es
  personalidad.** Es la impresión que genera la foto. Para estética, posicionamiento y
  comunicación, ese techo alcanza y sobra. Para saber cómo es alguien, no.
- **La era VLM no movió el techo del autoinforme.** Los modelos coinciden *entre sí* a
  r = 0,58–0,83 mientras coinciden con *la persona* a r = 0,18–0,31: aprendieron un
  estereotipo estable, no a una persona.
- **Casi ningún vínculo color→rasgo replica.** Dos estudios de Instagram con las mismas
  features y n comparable dan **signos opuestos** en saturación, temperatura, arousal y
  dominancia. Lo único que se sostiene es "poca saturación ↔ neuroticismo".
- **Las imágenes no aportan nada medible sobre otros canales.** El meta-análisis lo
  confirma: las fotos no mostraron efecto significativo en ningún rasgo. Fusionar cuatro
  familias de features visuales suma +0,00–0,01 de exactitud sobre n = 11.736. Y una
  década de deep learning tampoco movió la aguja: el año de publicación como predictor da
  β ≈ 0,00.
- **Distintas fotos de la misma persona producen más varianza de impresión que fotos de
  personas distintas.** Lo que se mide al "leer" una foto es, en buena medida, cuál foto
  tocó.
- **Todo está calibrado sobre datos de EE.UU. en inglés.** La valencia de las
  asociaciones se da vuelta entre rubros dentro de un mismo país. Asumir que sobrevive
  el salto a PyMEs argentinas es el supuesto más grande y menos validado de cualquier
  producto construido sobre esta literatura.

**Envolvente esperada:** contra autoinforme r ≈ 0,15–0,30. Contra atribución de
observadores r ≈ 0,4–0,68. Algo mejor que eso a partir de fotos solas es un bug.

---

## Reglas de escritura

1. **Prohibida la precisión falsa.** Nada de "Apertura: 7,3/10". Rangos y lenguaje natural.
2. **Relativo antes que absoluto.** Ordenar cuentas entre sí es defendible; puntuar una
   sola en abstracto no.
3. **Toda afirmación no evidente lleva cita**: qué post, qué fecha, qué se vio.
4. **Publicar la hipótesis alternativa**: "también compatible con…".
5. **Rotular el tipo de evidencia.** Un perfil que mezcla "publica 4 veces por semana"
   (medido) con "arquetipo Explorador" (interpretación) sin marcar la diferencia engaña
   a su propio lector.
6. **Describir, no diagnosticar.**
7. **Belleza no es estrategia.** La calidad de producción levanta la demanda ~9%, pero
   prometer de más por imagen la destruye después vía reseñas. Recomendar "hacelo más
   lindo" sin mirar la oferta que hay abajo está contradicho por la evidencia.
8. **Restringir cada conclusión al dominio del costo de la señal.** Una foto de un
   producto premium prueba acceso a ese producto ese día. No prueba posicionamiento, ni
   poder adquisitivo, ni identidad.
9. **Buscar el residuo, no la afirmación.** Una grilla es afirmación de identidad
   dirigida a otros, de punta a punta. El residuo involuntario está en la **cadencia**, la
   **consistencia** y los **fondos** — nadie los curó. Por eso la varianza suele ser mejor
   señal que el contenido.
10. **Rechazar la heurística compensatoria.** "Se muestra lo que falta" no tiene respaldo:
    la correlación narcisismo–selfies es r = 0,11–0,20, y el efecto de inseguridad
    documentado es **intra-persona y diario**, no un diagnóstico entre personas. Además es
    infalsable — cualquier observación lo confirma.

---

## Formato de salida

```markdown
## Perfil — @handle
**Modo:** A/B/C · **Material:** N posts, del DD/MM al DD/MM · **Fecha:** DD/MM/AAAA

### Qué es esta cuenta
[2-3 frases. Solo lo de confianza alta.]

### Medido
| Dato | Valor | Evidencia |
|---|---|---|
[Cadencia, formatos, categorías, intención comercial, geografía]

### Pilares de contenido
[Clusters con % de posts, cada uno con ejemplos citados]

### Identidad visual
[Paleta, consistencia, nivel de producción. Con desvíos, no solo promedios.]

### Interpretación — no verificado
[Cada ítem: afirmación · evidencia · confianza · hipótesis alternativa]

### Lo que no se puede saber desde acá
[Explícito. Es la sección que separa esto de las herramientas que venden humo.]

### Acción
[3-5 recomendaciones concretas, cada una atada a un hallazgo de arriba]
```

---

## Referencias

- `references/guardrails.md` — taxonomía 🔴🟡🟢, Ley 25.326, términos de Meta, checklist PyME
- `references/inferencias.md` — tabla completa de inferencias con evidencia y modos de falla
- `references/limites-y-evidencia.md` — techos de exactitud, qué canal de datos aporta cuánto
- `references/teoria-del-juicio.md` — modelo de lente, RAM, thin slices, reflejo vs. actuación
- `references/protocolo-por-foto.md` — esquema por foto, anclas ordinales, patrones de prompting
- `references/recursos.md` — libros, código open source, herramientas comerciales
- `research/raw/` — los diez informes de literatura completos, con bibliografía
