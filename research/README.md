# Investigación — perfilado a partir de imágenes de Instagram

Revisión de literatura hecha por diez agentes en dos tandas, cada uno sobre un cuerpo
distinto de trabajo publicado. Es el material del que sale la skill
`.claude/skills/perfil-instagram/`.

| Informe | Contenido |
|---|---|
| `raw/01-personality-images.md` | Personalidad (Big Five) desde imágenes: Segalin (IEEE TAC 2017), Ferwerda, Skowron, Liu, Guntuku, meta-análisis de Azucar 2018, era VLM 2022-2026. Incluye la tabla feature→rasgo completa y el techo de exactitud |
| `raw/02-wellbeing-context-critiques.md` | Estado y contexto: Reece & Danforth y sus críticas, inferencia de nivel socioeconómico, edad y género con sus sesgos, engagement. Y la lista de inferencias que la literatura no sostiene |
| `raw/03-marketing-profiling.md` | Marketing y consumo: Visual Listening In (Marketing Science), Li & Xie (JMR 2020), The Power of Brand Selfies, perfilado de creadores. Con auditoría de evidencia sobre los marcos de práctica (arquetipos, psicología del color, VALS) |
| `raw/04-methods-pipeline.md` | Métodos: estética computacional clásica, features profundas, VLM, agregación de N fotos a un perfil, evaluación, patrones de prompting |
| `raw/05-ethics-legal.md` | Ley 25.326, AAIP, derecho a la imagen, GDPR, términos de Meta, crítica fisiognómica, sesgo demográfico. Taxonomía 🔴🟡🟢 y checklist PyME |
| `raw/06-github-ecosystem.md` | Qué existe en GitHub para cada paso del pipeline: reproducciones de los papers (abandonadas), recolección de datos y su estado frente a los términos, infraestructura de estética y CLIP (sana), analítica visual de marketing (vacía), auditoría de sesgo |
| `raw/07-libros.md` | 40 libros: teoría de la autopresentación, estudios de redes visuales, primeras impresiones, huellas digitales, sesgo algorítmico, métodos visuales. Con lista rankeada y sección de lo que sobrevende |
| `raw/08-que-datos-mejoran.md` | Ranking cuantificado de canales de datos por aporte medido, incluidos los resultados negativos verificados |
| `raw/09-teoria-del-juicio.md` | Modelo de lente de Brunswik, RAM de Funder, thin slices, reflejo vs. actuación, afirmación de identidad vs. residuo conductual |
| `raw/10-herramientas-comerciales.md` | Qué expone realmente la Graph API, el mercado de analítica y benchmark, detección de seguidores falsos, auditoría de evidencia de los vendors psicográficos |

## Los hallazgos que ordenan la skill

1. **La literatura valida leer la puesta en escena, no a quien la pone.** Todo el
   trabajo de primer nivel mide qué comunica una imagen sobre una marca. Ninguno valida
   inferir cómo es la persona que la publicó.

2. **El techo real es bajo y está bien medido.** Una foto da r ≈ 0,15–0,19 por rasgo.
   Una galería grande contra autoinforme llega a r ≈ 0,25–0,30. Los números publicados
   por encima de 0,40 vienen de rasgos *atribuidos* — que son la impresión que genera la
   foto, no la persona.

3. **La era VLM no movió ese techo.** Los modelos coinciden entre sí a r = 0,58–0,83 y
   con la persona a r = 0,18–0,31: aprendieron un estereotipo estable.

4. **El hallazgo comercialmente más útil del corpus** es la disociación entre tipos de
   imagen: los selfies de frente compran likes, las tomas del producto en la mano compran
   intención de compra. Medido sobre 258k posts. Es un diagnóstico que la mayoría de los
   dueños de cuenta no puede hacer sobre sí mismos.

5. **Todo está calibrado sobre datos de EE.UU. en inglés**, y la valencia de las
   asociaciones se da vuelta entre rubros dentro de un mismo país. Asumir que sobrevive
   el salto a PyMEs argentinas es el supuesto más grande y menos validado de cualquier
   cosa construida sobre esta literatura.

6. **Las fotos son el canal más débil que se puede elegir.** El meta-análisis confirma que
   no aportan efecto significativo sobre otras huellas digitales. De 1 a 200 fotos, la
   exactitud fue de 0,55 a 0,54. Lo que sí aporta: preguntarle al sujeto (r ≈ 0,77–0,83),
   preguntarle a alguien cercano (0,46–0,49), los likes (0,56–0,66), el historial musical.

7. **Consistencia no es validez.** El modelo de lente de Brunswik las separa formalmente:
   un sistema puede ser perfectamente consistente y perfectamente inválido. Por eso los
   modelos coinciden entre sí a r = 0,58–0,83 y con la persona a 0,18–0,31.

8. **No existe nada end-to-end en open source.** Hay infraestructura excelente para cada
   paso y cero pegamento. La parte que falta es exactamente la que escribimos: agregación
   a nivel cuenta, esquema, calibración, vínculo con la evidencia y compuerta de rechazo.
