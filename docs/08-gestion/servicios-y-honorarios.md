# Los tres servicios: anteproyecto, proyecto e interiorismo

> Define qué se vende, qué se entrega, dónde termina cada etapa y cómo se le explica al cliente.
> El desarrollo técnico de cada etapa está en los documentos correspondientes; acá está el
> **alcance comercial y contractual**.

---

## 1. El problema que resuelve esta estructura

La mayoría de los conflictos de un estudio no son técnicos: son de **alcance**. El cliente
creyó que "el proyecto" incluía elegir los pisos; el estudio creyó que "el anteproyecto"
incluía dos revisiones y va por la novena. Los tres servicios separados existen para que cada
parte sepa exactamente **dónde termina lo que pagó**.

Regla que ordena todo: **cada servicio se cierra con un entregable y una aprobación firmada.
Sin aprobación de la etapa anterior no arranca la siguiente.**

---

## 2. Cuadro comparativo de los tres servicios

| | **1 · ANTEPROYECTO** | **2 · PROYECTO** | **3 · INTERIORISMO** |
|---|---|---|---|
| **Qué es** | La idea general resuelta | La idea llevada a documentación construible | El diseño interior integral |
| **Pregunta que responde** | "¿Cómo va a ser?" | "¿Cómo se construye?" | "¿Cómo se ve, se siente y con qué se equipa?" |
| **Contenido** | Distribución de espacios, funcionalidad, fachada, imágenes 3D | Todo lo anterior + desarrollo técnico y planos de obra: estructura, instalaciones, detalles, pliego, cómputo | Materiales, colores, iluminación, mobiliario, equipamiento, decoración |
| **Escala de trabajo** | 1:100 / 1:200 | 1:100, 1:50, 1:20, 1:10, 1:5 | 1:50, 1:20, 1:10 + planillas |
| **Con qué se cierra** | Carpeta de anteproyecto aprobada y firmada | Legajo técnico completo | Carpeta de interiorismo + planilla FF&E |
| **Se puede vender solo** | Sí | No sin anteproyecto aprobado (propio o de terceros, con reservas) | Sí, incluso sobre obra existente terminada |
| **Documento técnico** | `docs/01-anteproyecto/` | `docs/02-proyecto/`, `03-estructuras/`, `04-instalaciones/`, `05-construccion/` | `docs/07-interiorismo/` |

---

## 3. Servicio 1 — ANTEPROYECTO

### 3.1 Alcance

Se trabaja **la idea general**: distribución de los espacios, funcionalidad y fachada. Se
incluyen **imágenes 3D** para que el cliente visualice los espacios antes de decidir.

**Incluye:**
- Entrevista y armado del programa de necesidades
- Análisis del sitio y verificación de indicadores urbanísticos (envolvente máxima admisible)
- Partido arquitectónico y zonificación funcional
- Plantas, cortes y vistas de anteproyecto
- Diseño de fachada
- Imágenes 3D de exterior y de espacios principales
- Estimación preliminar de superficie y de orden de magnitud de costo
- Presentación al cliente y ciclo de ajustes acordado

**No incluye** (y hay que decirlo explícitamente en la propuesta):
- Planos de estructura ni de instalaciones
- Detalles constructivos
- Pliego de especificaciones ni cómputo y presupuesto detallado
- Trámite municipal ni visado
- Elección de materiales de terminación, colores, mobiliario o iluminación (eso es interiorismo)
- Dirección de obra

### 3.2 Entregables

| # | Entregable | Formato |
|---|---|---|
| 1 | Programa de necesidades acordado | Documento |
| 2 | Ficha urbanística y envolvente máxima | Documento + esquema |
| 3 | Plantas de anteproyecto amobladas | PDF 1:100 |
| 4 | Cortes (mínimo 2) y vistas / fachadas | PDF 1:100 |
| 5 | Planta de techos e implantación | PDF |
| 6 | Imágenes 3D exteriores | Cantidad a definir en propuesta |
| 7 | Imágenes 3D interiores de espacios principales | Cantidad a definir en propuesta |
| 8 | Planilla de superficies | Documento |
| 9 | Carpeta de presentación | PDF único |

### 3.3 Cláusulas que evitan el 90 % de los problemas

- **Número de revisiones incluidas** explícito (recomendado: 2 ciclos de ajuste sobre el partido
  aprobado). A partir de ahí, se cotiza aparte.
- **Cambio de partido** = nuevo anteproyecto, no una revisión. Definirlo por escrito.
- **La cantidad de imágenes 3D es cerrada.** Las imágenes son el ítem que más se desborda.
- **La aprobación del anteproyecto es por escrito** y congela la distribución. Cambios
  posteriores durante el proyecto se cotizan como adicional.
- El anteproyecto **no garantiza aprobación municipal**: se ajusta a la normativa vigente
  relevada, pero el criterio de la Autoridad de Aplicación puede exigir modificaciones.

---

## 4. Servicio 2 — PROYECTO

### 4.1 Alcance

Incluye todo el anteproyecto y además se desarrolla **toda la parte técnica y los planos
necesarios para llevarlo a obra**: estructura, instalaciones, detalles constructivos y
documentación.

**Incluye** (además de lo del anteproyecto):
- Planos de arquitectura de obra: replanteo, albañilería, plantas, cortes, vistas, techos
- Planillas de locales y de carpinterías
- Detalles constructivos (1:20 / 1:10 / 1:5)
- Proyecto de **estructura**: fundaciones, encofrado por nivel, armaduras, planillas
- Proyecto de **instalaciones**: sanitaria (agua fría/caliente, cloacal, pluvial), gas,
  eléctrica y corrientes débiles, incendio, termomecánica según corresponda
- Coordinación de las tres disciplinas (pases, interferencias, alturas de cielorraso)
- Pliego de especificaciones técnicas
- Cómputo métrico y presupuesto
- Documentación para trámite municipal y visado profesional

**Definir en propuesta, caso por caso:**
- Si el cálculo estructural y las instalaciones los firma el estudio o profesionales asociados
  (y si sus honorarios están dentro o fuera de la propuesta) — **esto se aclara siempre**
- Si incluye la **gestión** del trámite o solo la documentación para tramitarlo
- Si incluye **dirección de obra** (es una tarea profesional distinta, ver 4.3)

### 4.2 Entregables

El listado completo de planos, escalas y contenido está en
`docs/02-proyecto/proyecto-ejecutivo.md`. En la propuesta al cliente conviene entregarlo como
**índice de legajo**, con cantidad estimada de láminas: es lo que hace tangible la diferencia
de precio contra el anteproyecto.

### 4.3 Dirección de obra: es otro servicio

**Proyecto ≠ dirección de obra.** Son tareas profesionales distintas, con honorarios distintos
y responsabilidades distintas. Un proyecto sin dirección de obra se construye igual, pero el
estudio no controla cómo. Ofrecerla siempre como ítem separado, y si el cliente no la toma,
dejar asentado por escrito que el estudio no responde por la ejecución.

---

## 5. Servicio 3 — INTERIORISMO

### 5.1 Alcance

Trabajar específicamente el **diseño interior**: materiales, colores, iluminación, mobiliario,
equipamiento y decoración, **para que todo el espacio tenga una misma estética**.

**Incluye:**
- Briefing de estilo, uso y presupuesto
- Concepto y moodboard por ambiente
- Paleta de materiales y colores especificada (con códigos, no con adjetivos)
- Proyecto de iluminación: niveles, temperatura de color, artefactos, ubicación y comandos
- Diseño de mobiliario a medida y selección de mobiliario de catálogo
- Equipamiento y decoración
- Planos de interiorismo (solados, cielorrasos e iluminación, vistas interiores, detalles de
  carpintería)
- **Planilla FF&E**: cada ítem con proveedor, medida, cantidad, precio y plazo

**Modalidades de venta** (elegir una y dejarla escrita):

| Modalidad | Qué hace el estudio | Cuándo conviene |
|---|---|---|
| **Asesoramiento** | Reuniones y recomendaciones; el cliente ejecuta y compra | Presupuesto acotado, cliente con tiempo |
| **Proyecto de interiorismo** | Diseño completo + documentación + planilla FF&E; el cliente compra y coordina | El estándar |
| **Proyecto + gestión** | Además compra, coordina proveedores, montaje y styling final | Cliente sin tiempo, obra llave en mano |

**Transparencia con proveedores:** si el estudio recibe comisiones de proveedores, se declara
por escrito al inicio. No hacerlo es la forma más rápida de perder un cliente y su recomendación.

### 5.2 El punto de coordinación crítico

**El interiorismo tiene que empezar antes de que se ejecute la instalación eléctrica.** La
ubicación de cada boca de luz, cada tecla, cada toma y cada circuito de escena se define en el
proyecto de iluminación. Si el interiorismo entra después de la instalación, todo se resuelve
con soluciones de segunda: artefactos donde hay boca, no donde va la luz.

Lo mismo con: pendientes y desagües en baños, refuerzos en tabiques para colgar, previsión de
nichos, alturas de mesada, ventilación de campana, y estructura para cielorrasos técnicos.

**Consecuencia comercial:** cuando se vende proyecto, ofrecer interiorismo **en el mismo momento**
y explicar por qué contratarlo después cuesta más y rinde menos.

---

## 6. Cómo se combinan y se venden

### 6.1 Los tres caminos típicos

| Caso | Camino | Nota |
|---|---|---|
| Obra nueva, cliente que quiere todo resuelto | Anteproyecto → Proyecto → Interiorismo → Dirección de obra | El más rentable y el de mejor resultado |
| Obra nueva, cliente que quiere ver antes de comprometerse | Anteproyecto → decide → Proyecto | El anteproyecto funciona como prueba de la relación |
| Departamento o casa a estrenar / existente | Solo Interiorismo | No requiere las etapas previas |
| Reforma | Relevamiento + Anteproyecto de reforma → Proyecto → Interiorismo | El relevamiento se cotiza aparte: en reforma es trabajo real, no cortesía |

### 6.2 Escalonar el cobro

Cobrar por hitos, contra entregable, y no arrancar la etapa siguiente con la anterior impaga.
Estructura habitual: anticipo a la firma, pagos contra cada entregable de etapa, saldo contra
entrega final de la etapa. El detalle de porcentajes, aranceles y la base de cálculo de
honorarios está en `docs/02-proyecto/proyecto-ejecutivo.md` §8.

**Base de cálculo en La Pampa:** el Colegio de Arquitectos publica un **valor de referencia del
m² de construcción** que se actualiza por promedio de índices CAMARCO e INDEC. Es el punto de
partida para presupuestar honorarios. **Pedir siempre la resolución vigente** — ver
`docs/00-marco/marco-local-santa-rosa.md` §6.

### 6.3 Qué poner sí o sí en toda propuesta

- [ ] Alcance **incluido** e **items expresamente excluidos**
- [ ] Entregables enumerados, con formato y cantidad
- [ ] Plazos por etapa y qué los suspende (falta de definición del cliente, de datos, de pagos)
- [ ] Cantidad de revisiones incluidas y precio de las adicionales
- [ ] Forma de pago por hitos y actualización en contexto inflacionario
- [ ] Quién firma cada especialidad y si sus honorarios están incluidos
- [ ] Si incluye gestión de trámites y visados, o solo la documentación
- [ ] Propiedad intelectual del proyecto y uso de imágenes para difusión del estudio
- [ ] Vigencia de la propuesta (en Argentina: corta)

---

## 7. Documentos relacionados

| Tema | Documento |
|---|---|
| Indicadores urbanos, clima, suelo y marco profesional de Santa Rosa | `docs/00-marco/marco-local-santa-rosa.md` |
| Método de anteproyecto, entrevista, programa, fachada, 3D | `docs/01-anteproyecto/anteproyecto.md` |
| Legajo, pliego, cómputo, trámites, honorarios, dirección de obra | `docs/02-proyecto/proyecto-ejecutivo.md` |
| Método de interiorismo, iluminación, FF&E | `docs/07-interiorismo/interiorismo.md` |
| Relevamiento y cotización de reformas | `docs/06-reformas/reformas-y-rehabilitacion.md` |
