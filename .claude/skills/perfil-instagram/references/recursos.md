# Recursos — libros, código y herramientas

Destilado de `research/raw/06-github-ecosystem.md`, `07-libros.md` y `10-herramientas-comerciales.md`.

---

## Los cinco libros que cambian cómo se hace este trabajo

1. **Todorov, *Face Value*** (Princeton UP, 2017). Las impresiones de rasgos a partir de
   caras son rápidas, consensuadas y en gran medida **inválidas**: mapean los
   estereotipos del que mira. Su hallazgo decisivo: **distintas fotos de la misma persona
   producen más varianza de impresión que fotos de personas distintas.** Es la
   justificación empírica de separar "¿qué comunica esta imagen?" de "¿cómo es esta
   persona?".

2. **Goffman, *Gender Advertisements*** (1979). El mejor ejemplo trabajado de leer poses
   sistemáticamente, cincuenta años antes del machine learning. Seis familias
   codificables: tamaño relativo, toque femenino, ranking funcional, familia,
   ritualización de la subordinación, retiro autorizado. No es estadístico y elige sus
   ejemplos — pero el esquema es codificable entre evaluadores en una tarde. Y da el
   encuadre correcto: **las imágenes son ritualizaciones, no muestras de conducta.**

3. **Manovich, *Instagram and Contemporary Image*** (2017, gratis, hay traducción al
   español de 2020). 16 millones de fotos, 17 ciudades. Aporta la tipología
   **casual / profesional / diseñado**, y tratar el **feed** como unidad de análisis en
   vez del post. Para método, su *Cultural Analytics* (MIT, 2020).

4. **Crawford, *Atlas of AI*, cap. 5 "Affect"** (Yale, 2021). La demolición de inferir
   estados internos desde la cara. Es la cita para **rechazar** un pedido. El cap. 4,
   sobre clasificación, casi tan útil.

5. **Rose, *Visual Methodologies*, 5ª ed.** (SAGE, 2022). Cuatro sitios —
   producción / imagen / circulación / audiencia — por tres modalidades. Hace visible el
   error estándar del campo: **hacer una pregunta del sitio de producción con evidencia
   del sitio de la imagen.** Es exactamente el error de "dime lo que ostentas".

**Casi entran:** Funder, *Personality Judgment* (1999) — el RAM predice *a priori* qué
rasgos son legibles · Hersh, *Hacking the Electorate* (CUP, 2015) — el "votante
percibido", que traslada directo: *perfilás un avatar de datos, no a una persona* ·
Bell, cap. 2 del *Handbook of Visual Analysis* — cómo hacer análisis de contenido de
imágenes con un coeficiente de confiabilidad real.

**Sobrevenden, sin vueltas:** Wylie *Mindf\*ck* y Kaiser *Targeted* — los dos necesitan
que el targeting de Cambridge Analytica haya funcionado; el regulador británico concluyó
que la analítica "no era tan sofisticada como se afirmó" y el meta-análisis de persuasión
en elecciones generales da cerca de cero. Matz, *Mindmasters* (2025) es el mejor
informado de los libros de divulgación y **igual infla**: generaliza desde diferencias de
clicks en avisos pareados a "predecir y cambiar la conducta humana".

**En español/LATAM** (flaco pero rescatable): Sibilia, *La intimidad como espectáculo*
(FCE, 2008) · Manovich traducido · Rivera Cusicanqui, *Sociología de la imagen* (Tinta
Limón) · Villafañe, grilla de análisis de la imagen · el informe gratuito de la AAIP
(2023) sobre el proyecto que reemplaza a la Ley 25.326.

---

## Código

**La respuesta a "¿hay algo en GitHub?": mucho sobre cada paso, nada sobre el conjunto.**

### Sirve — infraestructura sana

| Repo | Para qué |
|---|---|
| `IQA-PyTorch` (3.381★, activo) | Calidad y estética de imagen. **Reemplaza a `idealo/image-quality-assessment`, que está archivado** |
| `open_clip` | Embeddings y sondeo de atributos zero-shot |
| `imagededup` | Duplicados y near-duplicates |
| `fiftyone` | Manejo y exploración de sets de imágenes |
| `instructor`, `outlines` | Forzar salida JSON con esquema fijo. **`lmql` está muerto** |
| `VLMEvalKit` | Evaluación de modelos de visión |

### Casi nada — personalidad desde imágenes

Buscar "automatic personality recognition" devuelve 12 repos, ninguno arriba de 2★.
Existen dos artefactos reales:

- `liaorongfan/DeepPersonality` (70★, MIT, último commit 2024-10) — 18 modelos sobre
  ChaLearn FI, pero orientado a video y dormido.
- `aimclub/OCEANAI` (65★, BSD-3, activo, instalable con pip) — **pensado para ranking
  automatizado de candidatos, que es alto riesgo bajo el AI Act.** Ojo con el encuadre.

Los ganadores del challenge ChaLearn nunca publicaron código. De Segalin queda un
extractor de features en Matlab de 2017 (7★). De Ferwerda, nada. **Los extractores de
features de Datta y Machajdik no existen: cero repos.**

### Vacío total

Marketing visual: "Visual Listening In" → 0 repos, 0 resultados en búsqueda de código.
Detección de logos para análisis de marca → 0. Los 40 repos de analítica de influencers
son dashboards de Power BI sobre un CSV de Kaggle — **ninguno mira una imagen.**

Auditoría de sesgo: `fairface` no tiene archivo de licencia. No existe ningún harness de
sesgo contrafáctico para imágenes. No existe awesome-list del área.

### Recolección de datos

La API oficial es un desierto de wrappers (el mejor en Python tiene 8★ — conviene HTTP
crudo). `instaloader` (13.258★, MIT, activo) es el scraper más limpio y **igual viola los
términos**; `instagrapi` usa la API privada y tiene riesgo real de baneo.

---

## Herramientas comerciales

### El techo lo pone Meta

Toda herramienta de terceros es un envoltorio sobre la Graph API. Y la asimetría es dura:

**Para tu propia cuenta** — reach, views, **saves, shares**, profile_views, y demografía
de seguidores (mínimo 100 seguidores, corte en los top 45 segmentos, ~90 días de
retención, ~48 h de latencia).

**Para una cuenta ajena** — solo `business_discovery`: seguidores, cantidad de posts,
likes, comentarios, caption, media_url. **Guardados y compartidos, que son las señales de
intención más fuertes, son estructuralmente inaccesibles.** Todo lo demás que una
herramienta afirme sobre un tercero es estimación.

### Recomendación para una PyME argentina

| Capa | Herramienta |
|---|---|
| Métricas propias | **Insights de Meta** — gratis, y es la fuente de verdad |
| Analítica y competencia | **Metricool** — español nativo, plan Free real, Starter ~USD 20–25, hasta 100 competidores |
| Línea de base | **Panel propio de 15–30 cuentas comparables.** No existe benchmark público con muestra argentina; la mediana global de 0,30% no describe a una PyME del interior |
| Vetting de creadores | Pedirle los Insights al creador + Creator Marketplace |
| Análisis visual | Google Vision por uso — objetos, escenas, OCR, logos |

Multiplicar precios en USD por ~1,3–1,6 (percepción + IVA).

### Rechazar

**Audiense** (USD 12.000–28.750/año) — construyó su psicografía sobre IBM Watson
Personality Insights, que **IBM apagó en 2021**, y su material comercial lo sigue citando
cinco años después sin decir qué lo reemplazó.

**Crystal Knows y Humantic AI** — refutados por auditoría independiente publicada (Rhea
et al. 2022, arXiv:2201.09151): "cannot be considered valid testing instruments". Crystal
le cambia el puntaje al mismo CV según venga en PDF o en texto plano.

**Toda API de emoción o género facial.** Los propios fabricantes ya se retiraron: Google
sacó las etiquetas de género de Cloud Vision (19/2/2020, "gender cannot be inferred by
appearance"); Microsoft retiró emoción, género y edad de Azure Face (21/6/2022); AWS
desaconseja por escrito usar sus predicciones de género y emoción. El AI Act prohíbe
reconocimiento de emociones en ámbito laboral y educativo desde el 2/2/2025.

**PimEyes y el mercado OSINT de búsqueda por rostro** — la autoridad de datos de Hamburgo
lo declaró ilegal bajo GDPR. Es el extremo cautelar, no el modelo.

### Sobre detección de seguidores falsos

Es la única inferencia comercial con base técnica plausible, y aun así: HypeAuditor
declara 95,5% "sobre actividad fraudulenta conocida" — autoetiquetada — y **nadie publica
tasa de falsos positivos**. No hay estudio independiente comparando vendors. Las
estimaciones de prevalencia van de 5–15% a 37,2%: un factor de 7.

**El contraejemplo honesto del mercado es SparkToro**, que publica sus límites y dice
explícitamente que es direccional, no censo. Ese es el estándar de comunicación a imitar.
