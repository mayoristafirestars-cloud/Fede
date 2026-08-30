# Guardrails — qué se puede perfilar y qué no

Destilado de `research/raw/05-ethics-legal.md`. Marco: Argentina, PyME, uso comercial.

---

## 🔴 ROJO — rechazar siempre

Sin excepción, sin flag de configuración, sin "modo avanzado". **Estos campos no deben
existir en el esquema de salida.** Un campo que no existe no se puede alucinar.

| # | Regla | Fundamento |
|---|---|---|
| R1 | Nunca inferir origen racial o étnico, ni tono de piel como atributo de la persona | LPDP arts. 2 y 7.3; GDPR art. 9; Ley 23.592 |
| R2 | Nunca inferir religión ni convicciones filosóficas — tampoco por proxies (velo, cruz, altar) | LPDP art. 7.3 ("directa o indirectamente revele") |
| R3 | Nunca inferir opinión política, ideología ni afiliación sindical — tampoco por proxies | LPDP art. 7.3; GDPR art. 9 |
| R4 | Nunca inferir orientación sexual, identidad de género ni vida sexual | LPDP art. 7.3; TJUE C-184/20; caso Kosinski |
| R5 | Nunca inferir salud, discapacidad, embarazo, salud mental, adicciones ni consumo | LPDP art. 7.3; GDPR art. 9 |
| R6 | Nunca inferir antecedentes penales, "criminalidad", "confiabilidad" ni "peligrosidad" | LPDP art. 7.4; *Physiognomy's New Clothes* |
| R7 | Nunca inferir estatus migratorio ni nacionalidad de origen | LPDP art. 7; Ley 23.592 |
| R8 | **Nunca perfilar a quien parezca menor de 18.** Ante señal de minoridad: abortar y descartar todo | Ley 26.061 art. 22; GDPR art. 8 |
| R9 | Nunca hacer reconocimiento facial, embeddings de rostro, matching entre cuentas ni estimación de emoción desde la cara | Res. AAIP 4/2019 crit. 4; AI Act art. 5(1)(f); Clearview |
| R10 | Nunca descargar ni almacenar imágenes de personas identificables. Analizar en memoria; persistir solo texto derivado | CCyCN art. 53; Platform Terms |
| R11 | **Nunca perfilar a un particular por encargo de un tercero interesado en esa persona** — vigilancia, dossier, targeting individual, evaluación de empleo/crédito/alquiler | LPDP arts. 4.3 y 20; GDPR art. 22; Meta Platform Terms |
| R12 | Nunca scrapear con cuentas falsas, credenciales ajenas, evasión de CAPTCHA o acceso a contenido no público | LPDP art. 4.2 ("medios desleales"); Meta v. Voyager Labs |
| R13 | Nunca vender, ceder ni publicar la base de perfiles | LPDP art. 11; Automated Data Collection Terms |
| R14 | Nunca estimar ingresos, patrimonio ni solvencia individual desde la estética de las fotos | LPDP arts. 4.1/4.3 |
| R15 | **Nunca emitir juicios sobre el cuerpo, el atractivo, el peso, la edad exacta o la apariencia de una persona** | CCyCN art. 52 (dignidad); AoIR IRE 3.0 |
| R16 | Nunca presentar una inferencia como hecho verificado, ni omitir la incertidumbre | LPDP art. 4.4 (exactitud); Res. AAIP 4/2019 crit. 2 |
| R21 | **"Perfilame a esta persona" es rechazo, siempre** | Consecuencia de R11 |

---

## 🟡 ÁMBAR — solo con evidencia citada, incertidumbre explícita y revisión humana

Cada afirmación ámbar sale con: **(a)** la evidencia concreta (post + fecha + qué se
vio), **(b)** confianza calibrada, **(c)** la hipótesis alternativa, **(d)** marca
visible de "no verificado".

| # | Inferencia |
|---|---|
| A1 | Rubro, categoría y surtido probable, desde productos visibles y captions |
| A2 | Tamaño y madurez aproximados del negocio — siempre en rangos, nunca en cifras |
| A3 | Ubicación de la **operación comercial**, solo si el negocio la publica. Nunca domicilio particular ni geolocalización de una persona |
| A4 | Posicionamiento de precio del comercio, desde precios publicados o marcas exhibidas. Nunca extrapolado a la persona dueña |
| A5 | Estilo visual y tono de marca, como descripción, no como juicio sobre la persona |
| A6 | Estacionalidad y calendario comercial |
| A7 | Canales y modalidad de venta declarados |
| A8 | Señales de intención de compra B2B ("buscamos proveedor", "reponemos stock") |
| A9 | Idioma y registro de comunicación |
| A10 | Rango etario amplio del público al que apunta el **comercio** — nunca de personas, nunca desde rostros |

> **Regla transversal:** si para sostener la inferencia hay que mirar el cuerpo o la
> cara de alguien, no es ámbar. Es rojo.

---

## 🟢 VERDE — libre

Datos publicados explícitamente por la propia cuenta con fines comerciales, y métricas
objetivas de la API oficial.

| # | Dato |
|---|---|
| G1 | Handle, nombre público, categoría declarada, bio literal, link en bio |
| G2 | Métricas públicas: seguidores, cantidad de posts, likes, comentarios, timestamp |
| G3 | Texto literal de captions y hashtags |
| G4 | Contacto **comercial** publicado por el negocio: teléfono, email, dirección del local, web |
| G5 | Frecuencia de publicación, horarios, ratio de formatos |
| G6 | Productos, precios y promociones explícitamente publicados |
| G7 | Marcas, proveedores y colaboraciones que la cuenta menciona o taggea |
| G8 | Permalinks y embeds oficiales |
| G9 | Métricas y contenido de **la propia cuenta** del usuario |
| G10 | Agregados estadísticos disociados sobre un conjunto de cuentas, sin identificadores |

---

## Reglas de proceso

**Fuente y acceso**
1. Jerarquía: API oficial de Meta → oEmbed → observación manual asistida → **nada**. No hay opción 5.
2. Solo cuentas profesionales. Si Business Discovery no la devuelve porque es personal, **eso es la respuesta**.
3. Respetar rate limits y toda señal de exclusión.

**Objeto**
4. Preferir la **cuenta/marca** sobre la **persona**. El sujeto legítimo es la unidad comercial.
5. Clasificador de tipo de cuenta al inicio, umbral conservador. Ante duda: `personal`, y frenar.

**Evidencia**
6. Toda afirmación no-verde lleva cita: permalink, fecha, qué se observó. Sin evidencia citable, no se emite.
7. Confianza en tres niveles con significado operativo:
   - *alta* (>80%): varios posts independientes y recientes lo sostienen
   - *media* (50–80%): evidencia parcial, admite otra lectura
   - *baja* (<50%): solo si el operador la pidió, y con la alternativa explicitada
8. Prohibida la precisión falsa.

**Minimización**
9. Recolectar solo lo que alimenta una decisión concreta. Si no se sabe qué decisión alimenta un campo, no se recolecta.
10. Retención: perfiles 90 días desde la última interacción comercial; **imágenes 0 días**; logs 12 meses. Purga automática.
11. Sin enriquecimiento cruzado con otras fuentes. La agregación es la que crea el daño.

**Derechos**
12. Canal de derechos con SLA legal: acceso 10 días corridos (art. 14), rectificación/supresión 5 días hábiles (art. 16), opt-out publicitario inmediato (art. 27).
13. Revisión humana obligatoria antes de cualquier acción con efecto sobre una persona o un negocio. Ningún perfil puede ser el único fundamento de una valoración (LPDP art. 20).

> **Matiz importante, y contraintuitivo.** La revisión humana es obligatoria sobre la
> **decisión**, no sobre la **estimación**. Medido: el humano corrigiendo la salida del
> modelo empeora la exactitud (g = −0,27; g = −0,54 cuando el modelo ya era mejor). O sea:
> la persona decide qué hacer con el análisis y responde por eso — pero "el modelo dijo
> 0,4 y a mí me parece 0,7" no es supervisión, es ruido con firma. Si el número está mal,
> se arregla el método o se suprime la dimensión; no se lo pisa a ojo.

---

## Checklist PyME argentina

- [ ] Perfilar **cuentas comerciales**, no personas físicas privadas
- [ ] Usar API oficial; nada de scraping automatizado ni cuentas falsas
- [ ] **No almacenar imágenes**; solo texto derivado y permalinks
- [ ] **Cero campos sensibles en el esquema** — no basta con no mostrarlos
- [ ] Encuadrar en el art. 27 LPDP (fines comerciales, fuente accesible al público) con opt-out funcionando
- [ ] Inscribir la base en el RNBD de la AAIP (art. 21)
- [ ] Política de privacidad conforme al art. 6 LPDP
- [ ] Retención y purga automática documentadas
- [ ] Revisión humana antes de todo contacto comercial
- [ ] Identificarse en cada comunicación, informar el origen de los datos, ofrecer baja
- [ ] Documentar el análisis de proporcionalidad — es la defensa si la AAIP pregunta

---

## Guion de rechazo

1. Negarse explícitamente, breve, sin sermón.
2. Nombrar la norma: *"el art. 7.3 de la Ley 25.326 prohíbe formar archivos que directa
   o indirectamente revelen datos sensibles"*.
3. Explicar el riesgo real — daño a la persona, multa AAIP, y sobre todo **la exactitud
   inexistente**: un perfil equivocado sobre el que se actúa es peor que ninguno.
4. **Ofrecer la alternativa legítima.**

El punto 4 no es cortesía. Un rechazo sin alternativa empuja al operador hacia una
herramienta que no le va a poner ninguno de estos límites.
