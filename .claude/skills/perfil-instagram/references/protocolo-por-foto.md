# Protocolo por foto — esquema, anclas y patrones de prompting

Destilado de `research/raw/04-methods-pipeline.md` (§4, §6, §7).

---

## La regla de arquitectura

> **Calificar cada foto por separado en un esquema estructurado; agregar las fichas con
> estadística común; después escribir el perfil en un pase de texto sobre la tabla
> agregada. Nunca pedirle a un modelo de visión que mire 100 fotos y resuma.**

Por qué: los VLM actuales se comportan esencialmente como modelos de una sola imagen. La
atención entre imágenes se diluye en las capas profundas, y la exactitud sobre
información distribuida cae de 79,0% a 66,5% con distractores. **La degradación arranca
a las 2–3 imágenes.**

Beneficio lateral: es la única arquitectura auditable. Cada afirmación del perfil final
rastrea a filas concretas de la tabla.

---

## Ficha por foto

```json
{
  "post_id": "...",
  "fecha": "AAAA-MM-DD",
  "procedencia": {
    "balde": "original | reposteo_placa | ambiguo",
    "texto_superpuesto": 0.0,
    "duplicado_de": null
  },
  "escena": {
    "interior_exterior": "...",
    "tipo_lugar": "...",
    "contexto": "..."
  },
  "sujeto": {
    "tipo": "producto | local | persona | placa_texto | paisaje | otro",
    "cantidad_personas": 0,
    "producto_visible": true,
    "precio_visible": false
  },
  "captura": {
    "encuadre": "...",
    "distancia": "...",
    "calidad_produccion": "..."
  },
  "color": {
    "tonos_dominantes": ["..."],
    "cantidad_tonos": 0,
    "saturacion": "...",
    "luminosidad": "..."
  },
  "comercial": {
    "tipo_imagen": "selfie_marca | producto_en_uso | packshot | ambiente | otro",
    "cta_presente": false,
    "tipo_cta": null
  },
  "observaciones": ["...", "...", "..."],
  "señales": { "dimension": [0, 2] },
  "calificaciones": { "dimension": { "nivel": "...", "confianza": "..." } },
  "abstenciones": ["dimension_x"]
}
```

**Campos que no deben existir:** nada de raza, etnia, tono de piel, religión, política,
orientación sexual, salud, edad exacta, atractivo, peso, estado emocional inferido desde
la cara, ingreso individual. Un campo que no existe no se puede alucinar.

---

## Orden obligatorio: observar → citar → calificar

```
Devolver JSON con estos campos, EN ESTE ORDEN:

1. "observaciones": 3 a 6 afirmaciones literales y verificables sobre lo que se ve.
   Cada una debe ser algo en lo que dos personas mirando esta imagen coincidirían.
   Prohibido: cualquier adjetivo sobre el carácter, el ánimo o la intención
   de quien la publicó.

2. "señales": para cada dimensión, el índice o los índices de las observaciones
   que la sostienen, o null si ninguna la sostiene.

3. "calificaciones": para cada dimensión, uno de los niveles anclados.
   Si "señales" para esa dimensión es null, la calificación DEBE ser
   "evidencia_insuficiente".
```

La restricción del punto 3 es todo el método. Un benchmark de VLM sobre inferencia
psicológica midió una tasa de prejuicio de ~51% — calificaciones emitidas sin evidencia
visual que las sostenga. La restricción convierte esa propiedad invisible en una salida
rechazada.

**El orden importa.** Pedir la calificación primero y la justificación después produce
racionalización post-hoc, con tasa de confabulación ≈ 52%.

Las observaciones, por ser literales, se pueden verificar por separado. Un desacuerdo
entre lo que el modelo dice haber observado y un detector determinístico (conteo de
caras, interior/exterior) es una alarma de alucinación de alta precisión.

---

## Anclas ordinales

Nada de escalas numéricas libres. Niveles discretos con anclas escritas, y **cada ancla
definida por algo observable, no por una inferencia**. "Multitud" es observable.
"Sociable" no.

```
Para ESTA imagen, elegir exactamente una etiqueta para "densidad social":
  ninguna        — no hay personas visibles
  sola           — exactamente una persona
  par            — dos personas
  grupo_chico    — 3 a 5
  multitud       — 6 o más
```

```
Para ESTA imagen, elegir exactamente una etiqueta para "tipo de imagen comercial":
  packshot           — producto aislado, fondo neutro o de estudio
  producto_en_uso    — producto en mano o en contexto de uso, punto de vista propio
  selfie_marca       — persona de frente mirando a cámara, producto secundario
  ambiente           — local, vidriera, espacio, sin producto protagonista
  placa_texto        — la imagen es mayormente texto o gráfica
  otro
```

```
Para ESTA imagen, elegir exactamente una etiqueta para "nivel de producción":
  captura_rapida     — luz disponible, encuadre casual, fondo sin preparar
  cuidada            — luz elegida o fondo ordenado, encuadre deliberado
  producida          — iluminación controlada, set o flat-lay armado, post-proceso visible
  evidencia_insuficiente
```

---

## Anti-sesgo y anti-adulación

- **Tercera persona.** Juzgar "la cuenta que publicó estas fotos", nunca "vos" ni "el
  usuario". El encuadre en tercera persona reduce la adulación hasta un 63,8%.
- **No re-preguntar ante desacuerdo.** Entre el 40% y el 75% de las respuestas
  inicialmente correctas de un VLM se dan vuelta bajo alguna forma de presión social. Si
  hace falta una segunda opinión, que venga de una muestra independiente, no de un turno
  de seguimiento.
- **Sacar el contexto que filtra identidad** del prompt de juicio: handle, bio, caption,
  conclusiones previas. Todo eso entra recién en el pase de escritura.
- **Nunca incluir la autodescripción del sujeto ni un perfil previo** en el prompt de
  juicio. En el pase final, marcar acuerdo o desacuerdo — no resolverlo.

---

## Agregación

Por fuera del modelo, siempre.

**Por balde de procedencia** (originales / reposteos y placas / ambiguos) **y por tercio
temporal.** Nunca promediar los tres baldes juntos: un agregado que incluye contenido
reposteado del proveedor mide la estética del proveedor.

**Estadísticos:** promedio, desvío, mediana, p10/p90, conteos.

El desvío no es un adorno. La saturación media describe la paleta; su **varianza** dice
si la cuenta sostiene un look o va a los tumbos — y esa es la señal más estable de las
dos.

**Temporales:** posts/semana · irregularidad (coeficiente de variación de los intervalos
entre posts) · mayor silencio · histograma horario · **deriva**: cuánto cambió el mundo
visual entre el primer tercio y el último.

**No cortar por representatividad.** El hallazgo del benchmark de agregadores: los
métodos **más débiles** son justamente los que toman decisiones duras de excluir parte
del conjunto. Si hay que submuestrear por costo, muestrear al azar o estratificado —
nunca elegir "las fotos más representativas".

**Incertidumbre por remuestreo:** volver a agregar sobre remuestreos del propio conjunto
de fotos y reportar el rango. **Si el rango de una dimensión abarca más de un nivel,
no mostrar un valor puntual.** Convierte "¿cuántas fotos alcanzan?" de conjetura en
medición.

---

## Cuántas fotos

Medido directamente en un solo lugar del corpus: el rendimiento sube con el tamaño del
conjunto y **satura alrededor de las 150–200 imágenes**.

| Cantidad | Qué se puede decir |
|---|---|
| 1 | Hay señal, y es casi inútil sola |
| < 10 | Incertidumbre amplia; suprimir toda afirmación fina |
| ~20–30 | Buena parte del camino |
| 30–60 | Mínimo real para un perfil |
| 60–90 | Rango recomendado |
| 150–200 | Saturación |

---

## Procedencia: originales, reposteos y placas

Nada de la literatura clásica maneja esto, y es una amenaza seria a la validez.

1. **Duplicados y reposteos** — la señal más fuerte es que la misma imagen aparezca en
   cuentas no relacionadas.
2. **Placas y memes** — proxies baratos: fracción de área con texto superpuesto,
   proporciones que no son de cámara, ausencia de metadatos de captura.
3. **Metadatos como procedencia** — la presencia de marca, modelo, lente o ISO es
   evidencia fuerte de captura original; su ausencia es evidencia débil de reposteo,
   porque las plataformas los borran.
4. **Rutear, no borrar.** Los reposteos y las placas informan sobre gusto y sobre qué
   señaliza la cuenta — simplemente no sobre su producción propia. Tres baldes, agregado
   separado, y que cada afirmación diga sobre cuál se apoya.

---

## Chequeo de sesgo como rutina

Mantener la escena constante y variar la región que porta rasgos demográficos: las
calificaciones deberían quedar invariantes. Reportar la diferencia por dimensión.

Y el hallazgo que conviene tener presente: **más fidelidad a la evidencia no garantiza
menos sesgo.** Anclaje y equidad se auditan por separado.
