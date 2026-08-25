# Límites de exactitud — los números que ordenan todo lo demás

Destilado de `research/raw/01-personality-images.md` (§0, §10) y `02-wellbeing-context-critiques.md`.

---

## Cuatro distinciones antes de leer cualquier número

Casi todo titular de este campo se cae cuando se ignora una de estas.

**1. Autoinformado vs. atribuido.** Predecir el puntaje que una persona **se pone a sí
misma** en un cuestionario es un problema. Predecir el puntaje que **desconocidos le
asignan** después de mirar sus fotos es otro, y es 2 a 3 veces más fácil — porque los
jueces solo vieron las imágenes, así que las imágenes *causan* la etiqueta. El mismo
estudio, sobre los mismos datos, obtuvo **r ≈ 0,26 autoinformado vs. r ≈ 0,68
atribuido**. Cualquier paper que reporte r > 0,5 desde imágenes solas casi con
seguridad está prediciendo percepción, no personalidad.

**2. Ground truth por encuesta vs. inferido de texto.** Varios estudios grandes etiquetan
con un modelo de texto en vez de con un cuestionario. Eso mide la concordancia entre dos
modelos, no con la persona.

**3. Tamaño de muestra.** Efectos de r ≈ 0,15–0,25 con n = 100–320 no son estimables con
precisión. La mitad de la literatura de Instagram está en ese régimen.

**4. Testeo múltiple.** 23 features × 5 rasgos = 115 tests. 85 features × 5 = 425. Solo
tres estudios del corpus corrigen por comparaciones múltiples.

---

## El techo, para autoinforme desde fotos

| Cota | Valor | Fuente |
|---|---|---|
| Techo meta-analítico, *todas* las huellas digitales combinadas | r = 0,29–0,40 | Azucar et al. 2018 |
| Validez convergente meta-analítica, toda la predicción computacional de personalidad | ρ = 0,30 | Hinds & Joinson |
| "Coeficiente de personalidad" — techo general de *cualquier* conducta prediciendo personalidad | r = 0,30–0,40 | Meyer et al. 2001; Roberts et al. 2007 |
| **Mejor resultado solo-imagen a n grande contra encuesta** | **r = 0,145–0,189** (una foto de perfil, n = 66.502) | Liu et al. 2016 |
| Mejor resultado solo-imagen, clasificación binaria, n = 11.736 | 55–56% (corte en la media), 60–62% (cuartiles extremos) | Segalin et al. 2017 (MM) |
| Mejor resultado solo-imagen, rasgos autoinformados, Flickr | r = 0,26 · 54% binario | Segalin et al. 2017 (TAC/CVIU) |
| **Observadores humanos juzgando una cuenta de Instagram entera** | **r = 0,25–0,44** | Osterholz et al. 2023 |
| Observadores humanos, una sola foto de perfil | 58–60% binario; α de Krippendorff = 0,26–0,34 | Segalin et al. 2017 (MM) |
| Máquina sobre las mismas 150 fotos | 68–69% binario | Segalin et al. 2017 (MM) |
| LLM zero-shot desde *texto* (cota superior de la modalidad) | r = 0,18–0,31 | Marengo 2025; Peters & Matz 2024 |
| **Likes de Facebook (no imágenes) — la marca real del campo** | **r = 0,56** (227 likes promedio); 0,66 (>500 likes) | Youyou et al. 2015 |
| Mejor VLM sobre rostros, MBTI percibido de 16 vías | 26,4% top-1, F1 = 18,0% | Chen et al. 2026 |

---

## Las siete conclusiones

1. **Una sola imagen da r ≈ 0,15–0,19 por rasgo** — 2 a 4% de la varianza. Es real
   (sobrevive a n = 66.502) y es casi inútil de a una.

2. **Una galería grande (100–300 imágenes) con features de contenido llega a r ≈
   0,25–0,30** contra etiquetas de encuesta, con RMSE aproximadamente igual al desvío
   estándar del propio rasgo. Todo valor publicado por encima de 0,40 viene de etiquetas
   inferidas de texto, de rasgos atribuidos, o de muestras menores a 200.

3. **El techo solo-imagen está *por debajo* del techo de huellas digitales.** El
   meta-análisis encontró que agregar imágenes **no** mejoró la predicción sobre otros
   tipos de huella. Las imágenes rinden menos que los likes (0,56), que el texto
   (0,29–0,35) y que las huellas combinadas (0,29–0,40).

4. **La personalidad atribuida es otro problema, mucho más fácil — r hasta 0,68 — y no
   es personalidad.** Es la impresión que genera la foto. Si el objetivo es gestión de
   impresión, estética o posicionamiento, ese techo es genuinamente alto y suficiente.
   Si el objetivo es saber cómo es alguien, no lo es.

5. **Las máquinas le ganan a los humanos individuales, pero apenas y solo en los rasgos
   fáciles.** 68–69% vs. 58–60% en extraversión/neuroticismo binarios desde una foto de
   perfil — y los jueces humanos coincidían *entre sí* a α = 0,26–0,34.

6. **El giro VLM/LLM de 2023–2026 no movió el techo del autoinforme.** Cada ganancia de
   titular vino de cambiar a un objetivo más fácil: rasgos percibidos, MBTI, primeras
   impresiones promediadas. Donde el objetivo siguió siendo "Big Five autoinformado",
   los LLM caen en r = 0,18–0,31 desde años de texto — exactamente donde estaban los
   modelos supervisados en 2013. Que los modelos coincidan *entre sí* a r = 0,58–0,83
   mientras coinciden con *la persona* a r = 0,18–0,31 es la evidencia más clara de que
   aprendieron un estereotipo estable, no a una persona.

7. **La asimetría entre rasgos es real y estable:** apertura y responsabilidad son
   recuperables; amabilidad y neuroticismo están cerca del ruido; extraversión es muy
   *perceptible* y poco *inferible*.

---

## Inferencias que la literatura NO sostiene

De `02-wellbeing-context-critiques.md` §8. Esta lista existe porque son exactamente las
que más se venden.

| Inferencia | Estado |
|---|---|
| **Salud y salud mental** | El paper insignia (fotos de Instagram → depresión) tiene problemas de muestreo, desbalance de clases y base rate. La demostración decisiva de validez externa mostró que el rendimiento se derrumba fuera de la muestra de entrenamiento. Un clasificador con 70% de exactitud sobre un rasgo de 5% de prevalencia es inservible |
| **Orientación sexual** | El caso Kosinski/Wang es el ejemplo canónico de sobreinterpretación fisiognómica |
| **Afiliación política** | No sostenida |
| **Religión** | No sostenida |
| **Raza / etnia** | Técnicamente inferible y éticamente prohibido. Las disparidades demográficas de los modelos desplegados son severas y están documentadas |
| **Emoción / estado afectivo interno desde la expresión facial** | La inferencia de estado interno desde la cara no está sostenida por la literatura de emoción |
| **Criminalidad, confiabilidad, personalidad desde la cara** | Fisiognomía con ropa nueva |
| **Ingreso o clase social individual desde fotos** | Los resultados que funcionan (autos → demografía, satélite → pobreza) son **agregados**, a nivel zona. A nivel individuo es mucho más débil |
| **Edad o género confiables desde una sola foto** | Las exactitudes de titular están infladas. La exactitud de grupo etario ronda el 60%, con sesgo demográfico documentado |

---

## Lo que sí es sólido

- **Las caras aumentan el engagement.** Las fotos con caras reciben más likes y comentarios — medido sobre corpus grandes de Instagram.
- **La disociación entre tipos de imagen comercial.** Los selfies de frente compran likes; las tomas en primera persona con el producto en la mano compran intención de compra. Los dos objetivos son visiblemente distintos en una grilla. Es una dissociación publicada sobre 258k posts, y es un diagnóstico que la mayoría de los dueños de cuenta no puede hacer sobre sí mismos.
- **El color estructural le gana al significado del tono.** "Azul = confianza" es folklore. "Menos tonos distintos ⇒ mayor status percibido, sobre 400.000 visuales" es evidencia. Medir amplitud de paleta, saturación y luminosidad; no narrar simbología de colores.
- **La calidad estética es una promesa, no un regalo.** Las imágenes profesionales levantan la demanda ~9%; pero prometer de más por imagen la destruye después vía reseñas.
- **Más imágenes → mejor estimación**, con saturación alrededor de 150–200. Una foto ya da señal; ~20–30 llegan a buena parte; por debajo de ~10 hay que reportar incertidumbre amplia y suprimir las afirmaciones finas.

---

## Regla de una línea

> Si la afirmación es sobre **lo que la cuenta comunica**, la evidencia probablemente la
> sostenga. Si es sobre **cómo es la persona detrás**, probablemente no — y el error va a
> ser invisible, porque va a sonar razonable.
