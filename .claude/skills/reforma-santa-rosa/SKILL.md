---
name: reforma-santa-rosa
description: Interpretar fotos o escaneos de planos de una vivienda y generar la reforma pedida - relevamiento del existente, propuesta de intervención, plano de demolición y obra nueva, verificación contra la normativa de Santa Rosa (La Pampa) y cómputo estimado. Usar SIEMPRE que el usuario mande imágenes de planos, croquis o plantas de una casa o departamento y pida reformar, ampliar, redistribuir, unir o dividir ambientes, mover baño o cocina, tirar un muro, cerrar una galería, agregar dormitorio o suite, o pregunte si algo "se puede hacer". También al pedir replanteo, redibujo a escala o cómputo de una reforma.
---

# Reformas a partir de fotos de planos — Santa Rosa, La Pampa

## Qué hace esta skill

Convierte **fotos de planos** en una **propuesta de reforma documentada**: qué se demuele, qué
se construye, si es legal, si es estructuralmente viable y cuánto sale aproximadamente.

## Paso 0 — Verificar que el material alcanza

**Antes de dibujar nada, revisar la imagen y confirmar estos cuatro puntos.** Si falta alguno,
pedirlo explícitamente y NO seguir adivinando:

| Necesario | Por qué | Si falta |
|---|---|---|
| **Al menos una cota conocida** (una acotación en el plano, o un dato del usuario tipo "el frente mide 8,20 m") | Sin escala, todo lo demás es decorativo | Pedirla. Si no hay, pedir que mida **una** pared larga con cinta |
| **La planta completa en el encuadre**, sin recortes | Un ambiente cortado se reconstruye mal | Pedir foto de la hoja entera, de frente, sin ángulo |
| **Norte** (el símbolo en el plano, o que el usuario diga hacia dónde da el frente) | En Santa Rosa el sol y el viento vienen del norte: sin orientación no se puede opinar sobre el partido | Preguntar "¿hacia dónde da el frente de la casa?" |
| **Espesor de muros** visible o declarado | Distingue muro portante (≥20-30 cm) de tabique (8-12 cm) | Pedir que mida el espesor en una puerta o ventana |

**Extras que mejoran mucho el resultado, pedirlos si el usuario los tiene:** fotos del interior
de los ambientes a reformar, foto del techo desde afuera, plano de instalaciones, año
aproximado de construcción, y si es departamento, el reglamento de copropiedad.

## Paso 1 — Relevar el existente

Leer la imagen y volcar a texto, **antes de proponer nada**:

1. **Planilla de locales**: nombre, dimensiones, superficie de cada ambiente.
2. **Superficie total cubierta** y semicubierta.
3. **Muros**: cuáles parecen portantes por espesor, continuidad y posición. **Marcar cada uno
   como "portante probable" o "tabique probable", nunca como certeza.**
4. **Dirección de la estructura de techo** si se puede inferir (viguetas, cabios, losa).
5. **Instalaciones visibles**: posición de baño, cocina, montantes, tablero, medidor de gas.
6. **Aberturas**: ubicación, medida aproximada, a qué orientación dan.

Entregar este relevamiento al usuario **y pedirle que confirme o corrija** antes de avanzar.
Un relevamiento mal leído propaga el error a todo lo que sigue.

## Paso 2 — Verificar la reforma pedida

Contra los documentos del repo. **Consultarlos, no responder de memoria:**

| Qué verificar | Dónde está |
|---|---|
| FOS, retiro de fondo, C.A.S., cochera, altura del distrito | `docs/00-marco/marco-local-santa-rosa.md` §2 y `docs/10-casa-santa-rosa/urbanismo-y-tramite-santa-rosa.md` |
| Si la ampliación supera el FOS o come el C.A.S. | ídem. **Recordar: el C.A.S. computa las veredas exteriores en contra** |
| Muro portante, apertura de vanos, refuerzos | `docs/03-estructuras/estructuras.md` (apertura de vanos, aplastamiento de apoyo) |
| Mover baño o cocina: pendientes, montantes, altura de contrapiso | `docs/04-instalaciones/instalaciones.md` y `docs/06-reformas/reformas-y-rehabilitacion.md` |
| Gas: caudal total y matrícula necesaria | `docs/10-casa-santa-rosa/gas-camuzzi-santa-rosa.md`. **Con caldera + otro artefacto se pasa de 5 m³/h y hace falta 2ª categoría** |
| Envolvente: si se toca muro o techo, aprovechar para aislar | `docs/10-casa-santa-rosa/envolvente-casa-santa-rosa.md`. Objetivos: muro K ≤ 0,80 (B) / 0,30 (A); techo K ≤ 0,48 / 0,19 |
| Cubierta y succión de viento si se agrega o modifica techo | `docs/10-casa-santa-rosa/viento-santa-rosa.md` |
| Ampliación que apoya en el terreno: fundación y manejo del agua | `docs/10-casa-santa-rosa/suelo-y-fundacion-santa-rosa.md` |
| Departamento: qué es parte común y qué mayoría hace falta | `docs/06-reformas/reformas-y-rehabilitacion.md` (arts. del CCyC transcriptos) |

**Decir explícitamente cuando algo NO se puede hacer, o cuando requiere cálculo y firma de un
estructuralista.** La lista de los 15 casos que exigen matriculado está en
`docs/06-reformas/reformas-y-rehabilitacion.md` §5.0.

## Paso 3 — Proponer

Entregar **2 o 3 variantes** cuando el problema lo admita, no una sola. Para cada una:

- Qué se demuele y qué se construye, en palabras.
- Superficies antes y después.
- Qué problemas resuelve y qué resigna.
- Costo relativo entre variantes (alto/medio/bajo), no en pesos salvo que se pida cómputo.
- Riesgos: estructurales, de trámite, de instalaciones.

## Paso 4 — Dibujar

Generar los planos **en SVG a escala**, escritos a archivo y enviados con `SendUserFile`.
El SVG abre en navegador, se importa a AutoCAD/Illustrator y es editable — no entregar imágenes
rasterizadas.

**Convención de colores obligatoria** (norma de uso corriente en Argentina):

| Color | Significa |
|---|---|
| **Negro / gris** | Existente que **permanece** |
| **Amarillo** | A **demoler** |
| **Rojo** | **Obra nueva** |

**Reglas de dibujo:**
- Escala real: definir `viewBox` en centímetros y trabajar 1 unidad = 1 cm. Indicar la escala
  nominal en el rótulo (1:50 o 1:100).
- Muros con dos líneas y espesor real, no una línea.
- Acotar: cotas parciales y totales en cada dirección.
- Nombre y superficie en cada local.
- Aberturas con su barrido de puerta.
- **Flecha de norte, siempre.**
- Rótulo con: obra, ubicación, contenido de la lámina, escala, fecha y la leyenda "PRELIMINAR —
  no apto para obra ni para trámite".
- Entregar **tres láminas**: existente, demolición (amarillo sobre gris) y obra nueva (rojo
  sobre gris).

## Paso 5 — Cerrar

- **Cómputo estimado por rubro** si el usuario lo pide, con la metodología de
  `docs/02-proyecto/proyecto-ejecutivo.md` §5. **Siempre con la fecha del precio y la
  advertencia de que se desactualiza.**
- **Qué hay que ir a verificar a obra** antes de ejecutar: espesores reales, si el muro es
  portante, estado de instalaciones, niveles.
- **Qué trámite corresponde** y quién firma.

## Límites — decirlos, no esquivarlos

1. **Un plano leído de una foto no es un relevamiento.** Las medidas salen de interpretar una
   imagen y hay que verificarlas en obra con cinta antes de ejecutar.
2. **No se puede determinar si un muro es portante desde una foto.** Se puede sospechar por
   espesor y continuidad. La confirmación es en obra, y si hay duda, la firma un estructuralista.
3. **No se entrega DWG.** Se entrega SVG a escala, que se importa a CAD.
4. **Nada de lo generado sirve para presentar en el municipio.** Es material de proyecto y de
   conversación con el cliente. El legajo municipal lo firma un matriculado.
5. **Si el plano es viejo, puede no reflejar lo construido.** Preguntar siempre si hubo
   modificaciones no documentadas.
