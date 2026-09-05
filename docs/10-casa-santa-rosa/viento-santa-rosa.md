# EL VIENTO EN SANTA ROSA, LA PAMPA
## Documento técnico aplicado al proyecto de una vivienda unifamiliar de una planta

> **Estado:** documento de trabajo del estudio. Complementa y profundiza `docs/03-estructuras/estructuras.md` §2.5 (que verificó V = 50,0 m/s para Santa Rosa según CIRSOC 102-2005, Fig. 1B). Acá no se repite la tabla de ciudades ni las tablas generales del reglamento: se va a lo que cambia el proyecto de una casa baja.
>
> **Convenciones de trazabilidad usadas en todo el documento:**
> - **[V]** dato verificado contra la fuente primaria (PDF del reglamento, PDF del SMN, paper).
> - **[VERIFICAR en …]** dato que no pude confirmar contra fuente primaria; hay que chequearlo antes de firmar.
> - **[SUP]** supuesto de proyecto propio del ejemplo (peso de materiales, geometría), no dato de norma.

---

## ÍNDICE

1. [Cómo leer este documento: dos datos que no son lo mismo](#1-cómo-leer-este-documento-dos-datos-que-no-son-lo-mismo)
2. [Dato normativo: velocidad básica del viento en Santa Rosa](#2-dato-normativo-velocidad-básica-del-viento-en-santa-rosa)
   - 2.1 CIRSOC 102-2005
   - 2.2 CIRSOC 102-25: los tres valores nuevos
   - 2.3 Por qué 61,2 m/s NO es "más viento" que 50 m/s
   - 2.4 Cuál usar hoy en Santa Rosa
   - 2.5 Categoría de exposición de un lote urbano de Santa Rosa
   - 2.6 Los demás factores: Kzt, Kd, I, Ke
3. [Dato climático real: estadísticas SMN Santa Rosa Aero](#3-dato-climático-real-estadísticas-smn-santa-rosa-aero)
   - 3.1 La estación y los límites de la serie
   - 3.2 Velocidad media mensual
   - 3.3 Rosa de los vientos anual
   - 3.4 Rosa de los vientos mes a mes
   - 3.5 Rosa de los vientos por estación del año
   - 3.6 Índice de exposición direccional: de dónde viene la carga
   - 3.7 Vientos máximos y ráfagas
   - 3.8 Días con viento fuerte, tormenta, granizo y polvo
   - 3.9 Síntesis del dato climático
4. [Implantación, orientación y expansiones](#4-implantación-orientación-y-expansiones)
   - 4.1 El conflicto central del proyecto en Santa Rosa
   - 4.2 Dónde va la galería, el quincho y el patio
   - 4.3 Configuraciones de planta que funcionan y que no
   - 4.4 Errores que generan túnel de viento
5. [Barreras de viento: vegetales y construidas](#5-barreras-de-viento-vegetales-y-construidas)
   - 5.1 Física de la barrera: la porosidad manda
   - 5.2 Datos de investigación (reducción vs. porosidad vs. distancia)
   - 5.3 Dimensionado en un lote urbano
   - 5.4 Especies
   - 5.5 Barreras construidas: muros, pantallas, celosías
6. [Cerramientos: infiltración de aire y estanqueidad](#6-cerramientos-infiltración-de-aire-y-estanqueidad)
7. [CUBIERTA: el punto crítico de una casa baja](#7-cubierta-el-punto-crítico-de-una-casa-baja)
8. [Cálculo resuelto: casa tipo 10 × 12 m en Santa Rosa](#8-cálculo-resuelto-casa-tipo-10--12-m-en-santa-rosa)
9. [Elementos que fallan primero](#9-elementos-que-fallan-primero)
10. [Ventilación natural: cuándo el viento es recurso](#10-ventilación-natural-cuándo-el-viento-es-recurso)
11. [Checklist de verificación de viento en el proyecto](#11-checklist-de-verificación-de-viento-en-el-proyecto)
12. [Fuentes](#12-fuentes)

---

## 1. Cómo leer este documento: dos datos que no son lo mismo

En Santa Rosa se confunden permanentemente dos cosas. Hay que tenerlas separadas en la cabeza porque sirven para decisiones distintas y no se pueden comparar directamente.

| | **DATO NORMATIVO (CIRSOC 102)** | **DATO CLIMÁTICO (SMN)** |
|---|---|---|
| Qué es | Velocidad básica del viento **V** | Estadística de la serie observada |
| Magnitud en Santa Rosa | **50,0 m/s = 180 km/h** (102-2005) | **velocidad media anual 14,7 km/h** |
| Definición | Ráfaga de **3 segundos**, a 10 m, **exposición C**, probabilidad anual 0,02 (recurrencia 50 años) | Promedio de las observaciones sinópticas, a la altura del anemómetro de la estación |
| Para qué sirve | **Dimensionar la estructura**: no se cae, no vuela el techo | **Orientar el proyecto**: dónde poner la galería, de dónde reparar, cuándo ventilar |
| Frecuencia del evento | Una vez cada 50 años (o cada 700, según edición) | Todos los días |
| Error típico | "El viento acá es de 180 km/h" — no, ese es el valor de diseño con recurrencia 50 años | "Acá el viento es de 15 km/h, no hace falta calcular" — no, eso es el promedio |

**Regla:** el dato normativo no dice de qué dirección viene el viento (asume que puede venir de cualquiera). El dato climático no sirve para dimensionar. **Hacen falta los dos y para cosas distintas.**

---

## 2. Dato normativo: velocidad básica del viento en Santa Rosa

### 2.1 CIRSOC 102-2005

**[V] V = 50,0 m/s = 180 km/h** — Figura 1B "Velocidades básicas del viento en ciudades", CIRSOC 102 (julio 2005).

Definición textual de la figura: *"velocidad de ráfaga de 3 segundos en m/s a 10 m sobre el terreno para Categoría de Exposición C y están asociadas con una probabilidad anual de 0,02"* → **recurrencia 50 años**.

Este valor se usa **con factor de carga 1,6 W** en las combinaciones de resistencia del CIRSOC 201-2005 (o 1,5 W en CIRSOC 301-05 para acero).

### 2.2 CIRSOC 102-25: los tres valores nuevos

El CIRSOC 102-25 (3.ª generación, puesto en vigencia para obra pública nacional por Resolución 11/2026) **cambia el formato**: ya no hay un mapa único, hay **tres mapas según Categoría de Riesgo** y el Factor de Importancia desaparece de la expresión de la presión dinámica (queda incorporado en la velocidad).

**[V] Tabla del Comentario C 1.5, CIRSOC 102-25 — velocidades básicas en ciudades (m/s):**

| Ciudad | Cat. Riesgo **I** | Cat. Riesgo **II** | Cat. Riesgo **III y IV** |
|---|---|---|---|
| **SANTA ROSA** | **57,1** | **61,2** | **65,7** |
| Bahía Blanca | 62,8 | 67,4 | 72,2 |
| Rosario | 57,1 | 61,2 | 65,7 |
| Buenos Aires | 51,4 | 55,1 | 59,1 |
| Córdoba | 51,4 | 55,1 | 59,1 |
| Neuquén | 54,8 | 58,8 | 63,0 |
| Mendoza | 44,6 | 47,8 | 51,2 |
| Comodoro Rivadavia | 77,1 | 82,7 | 88,7 |
| Viedma / Rawson / Río Gallegos / Ushuaia | 68,5 | 73,5 | 78,8 |
| Mar del Plata | 58,3 | 62,5 | 67,0 |
| Santa Fe | 58,3 | 62,5 | 67,0 |
| Paraná | 59,4 | 63,7 | 68,3 |
| Salta | 40,0 | 42,9 | 46,0 |

**Una vivienda unifamiliar es Categoría de Riesgo II → V = 61,2 m/s = 220 km/h.**

Recurrencias asociadas [V, C 1.5]: **300 años (Cat. I), 700 años (Cat. II), 1700 años (Cat. III-IV)**.

### 2.3 Por qué 61,2 m/s NO es "más viento" que 50 m/s

Esto es lo más importante de esta sección y es lo que más se malinterpreta en obra.

**[V] El propio Comentario del CIRSOC 102-25 da la fórmula con la que construyó los mapas nuevos:**

```
V_T = √( 1,5 · (V₅₀)² · I )                        (C 1.5-6.1)
```

donde `V₅₀` es la velocidad básica del **mapa de CIRSOC 102-2005** e `I` es el viejo Factor de Importancia (0,87 / 1,00 / 1,15).

Verificación numérica para Santa Rosa (V₅₀ = 50 m/s):

| Categoría | I | V_T calculada | V_T tabulada 102-25 | ✓ |
|---|---|---|---|---|
| I | 0,87 | √(1,5 × 2500 × 0,87) = √3262,5 = **57,12** | 57,1 | ✓ |
| II | 1,00 | √(1,5 × 2500 × 1,00) = √3750 = **61,24** | 61,2 | ✓ |
| III–IV | 1,15 | √(1,5 × 2500 × 1,15) = √4312,5 = **65,67** | 65,7 | ✓ |

**El mapa de 2025 en Santa Rosa es literalmente el mapa de 2005 multiplicado por √1,5.** No hay nueva estadística meteorológica detrás (el Comentario lo dice: *"esta situación se tornará abstracta cuando los futuros mapas, en proceso de elaboración, provengan del ajuste de las series estadísticas para cada estación meteorológica"*).

**Consecuencia numérica sobre la carga de diseño mayorada:**

```
102-2005:  1,6 × q(V=50)              = 1,6 × 0,613·K·Kd·(50²)·I
102-25:    1,0 × q(V=61,2) · Ke       = 1,0 × 0,613·K·Kd·(1,5·50²·I)·Ke

Relación = 1,5 · Ke / 1,6 = 0,9375 · Ke
```

Con Ke para Santa Rosa (altitud ≈ 190 m, ver §2.6): Ke = 0,978 → **relación = 0,917**.

> ### ⚠️ Conclusión que hay que tener clara
> **Pasar de CIRSOC 102-2005 a CIRSOC 102-25 en Santa Rosa NO aumenta la carga de viento de diseño: la baja aproximadamente un 8 %.** La velocidad "sube" de 50 a 61,2 m/s pero el factor de carga baja de 1,6 a 1,0, y el neto es levemente favorable.
>
> **Lo que sí es un error de 60 %:** mezclar las dos ediciones. Usar V = 61,2 m/s con factor 1,6 W sobredimensiona un 60 %. Usar V = 50 m/s con factor 1,0 W subdimensiona un 37 %. **Elegí una edición y usala completa, incluidas sus combinaciones de carga.**

### 2.4 Cuál usar hoy en Santa Rosa

| Situación | Edición | Factor de carga |
|---|---|---|
| Obra pública nacional (a partir de la vigencia de la Res. 11/2026) | **102-25** con CIRSOC 201-2025 | 1,0 W |
| Obra privada en Santa Rosa | La que **adopte la ordenanza municipal / el Colegio** | Coherente con la edición |
| Ante la duda / transición | Verificar por **ambas**; adoptar la envolvente | — |

**[VERIFICAR en la Municipalidad de Santa Rosa y en el CPIA La Pampa]** qué edición exige hoy el visado de estructuras. Mientras la respuesta no esté, el ejemplo del §8 se resuelve con **102-2005 + 1,6 W** (que es la práctica instalada y, según §2.3, la envolvente conservadora) y se verifica contra 102-25 en §8.8.

### 2.5 Categoría de exposición de un lote urbano de Santa Rosa

Este es el factor que más plata mueve en una casa baja, y el que más se resuelve "de memoria".

**[V] CIRSOC 102-25, art. 1.7.3 — regla cuantitativa para edificios bajos:**

> *"Exposición B: **para edificios con una altura media de cubierta menor o igual que 10 m**, se debe aplicar Exposición B donde la rugosidad superficial del terreno, tal como se la define en rugosidad superficial B, prevalece en la dirección a barlovento **en una distancia mayor que 450 m**."*
>
> *"Exposición C: se debe aplicar en todos aquellos casos en los que las Exposiciones B o D no son aplicables."*

Y la definición de rugosidad B: *"áreas urbanas y suburbanas, áreas boscosas u otros terrenos con obstrucciones numerosas y poco espaciadas entre sí que tengan el tamaño de una vivienda unifamiliar o mayor"*.

**[V] Además, el Comentario da un ejemplo calibrado que es exactamente nuestro caso:**

> *"si el fetch a barlovento consiste primordialmente en casas unifamiliares con altura típica H_ob = 6 m, un área frontal vertical (incluyendo algunos árboles en cada lote) de 100 m² y un área de terreno por cada casa de 1000 m², entonces z₀ = 0,5 × 6 × 100/1000 = 0,3 m"* → **Exposición B**.

**[V] Otro dato del mismo Comentario, útil para las barreras (§5):** *"Para coníferas y otros árboles de hojas perennes no se puede tomar más del **50 %** de su área frontal bruta que sea efectiva en obstruir el viento. Para árboles y arbustos de hojas caducas no se puede tomar más del **15 %**."* Es decir: **el arbolado caduco de Santa Rosa (fresnos, mayoría del arbolado urbano) prácticamente no cuenta como rugosidad en invierno.**

**Decisión para el proyecto — hay que verificar los 450 m en las direcciones que importan (N y S, ver §3):**

| Situación del lote | Exposición | Justificación |
|---|---|---|
| Macrocentro / barrio consolidado, tejido continuo de casas y árboles > 450 m en todas las direcciones relevantes | **B** | Cumple art. 1.7.3 |
| Loteo nuevo, casas dispersas, frente a campo, borde de ciudad | **C** | No hay 450 m de rugosidad B |
| **Lote con frente al N sobre campo, calle ancha, plaza, cancha, canal o la Ruta 5 / Circunvalación** | **C** | La exposición se evalúa **por dirección**, en sectores de ±45° (art. 1.7.1). Basta que falle al N. |
| Barrio consolidado pero con arbolado **caduco** y lotes grandes | **C, o justificar B con el cálculo de z₀** | El 15 % de área efectiva del caduco baja mucho z₀ |
| Frente sobre el **Bajo Giuliani / lagunas / bordes de valle** | **C**, y revisar Kzt | Superficie de agua y posible escarpa |

> **La diferencia entre B y C en una casa baja es del 21 % en la presión dinámica** (Kz de 0,72 a 0,87 en el rango de alturas de una vivienda, Caso 1 de la Tabla 5). En el método simplificado el multiplicador tabulado B→C es **1,40** [V, notas Tablas 2 y 3] porque esas tablas están construidas a h = 10 m. **No son inconsistentes: son dos bases distintas.** Si usás el método analítico usá 0,87/0,72; si usás el simplificado usá 1,40.
>
> **Criterio del estudio: en Santa Rosa, ante la duda, C.** El sobrecosto de rigidez y anclaje en una casa de una planta es marginal (unos flejes y unos anclajes más); el costo de un techo volado es total.

### 2.6 Los demás factores: Kzt, Kd, I, Ke

| Factor | Valor para una casa en Santa Rosa | Fuente / justificación |
|---|---|---|
| **Kzt** (topográfico) | **1,00** | [V] Terreno de llanura suavemente ondulada. Kzt = (1+K₁K₂K₃)². Solo distinto de 1 si hay loma o escarpa aislada que sobresale abruptamente. **Revisar** en lotes sobre el borde de los bajos (Bajo Giuliani, Valle Argentino). |
| **Kd** (direccionalidad) | **0,85** | [V] Tabla 6 (102-05) / Tabla 1.6-1 (102-25), edificios, SPRFV y C&R. Solo válido si se usan las combinaciones del Apéndice B (o del reglamento de aplicación). Si no aplicás Kd, el CIRSOC 201 permite 1,3 W en lugar de 1,6 W. |
| **I** (importancia, solo 102-05) | **1,00** | [V] Categoría II — "todas las no incluidas en I, III y IV", incluye vivienda. |
| **Ke** (altitud, solo 102-25) | **0,978 ≈ 0,98** | [V] Tabla 1.12-1: Ke = e^(−0,000119·z_g). Santa Rosa Aero: **190 m s.n.m.** [V, SMN] → e^(−0,02261) = 0,9776. Se permite tomar 1,00 (conservador). |
| **G** (efecto de ráfaga) | **0,85** | Edificio rígido (n₁ ≥ 1 Hz). Una casa de mampostería de una planta es trivialmente rígida. En el método de edificios de baja altura (Fig. 4) el efecto de ráfaga ya está **incluido** en los GC_pf y no se multiplica aparte. |
| **GC_pi** (presión interna) | **±0,18** cerrado / **±0,55** parcialmente cerrado | [V] Tabla 7 (102-05) / Tabla 1.11-1 (102-25). Ver §9.1 — es la variable que hace volar techos. |

**[V] Novedad del 102-25 que conviene conocer:** aparece una cuarta clase de cerramiento, **"edificio parcialmente abierto"** (el que no califica como cerrado, parcialmente cerrado ni abierto), con GC_pi = ±0,18, y los criterios de clasificación pasan a ser cuantitativos:

| Clasificación (102-25) | Criterio | GC_pi |
|---|---|---|
| Abierto | A₀ ≥ 0,8 A_g | 0,00 |
| Parcialmente cerrado | A₀ > 1,10 A₀ᵢ **y** A₀ > 0,4 m² ó > 0,01A_g (el menor) **y** A₀ᵢ/A_gᵢ ≤ 0,20 | **±0,55** |
| Cerrado | A₀ ≤ 0,01 A_g, ó 0,4 m² (el menor) | ±0,18 |
| Parcialmente abierto | El que no cumple ninguna de las anteriores | ±0,18 |

---

## 3. Dato climático real: estadísticas SMN Santa Rosa Aero

Fuente única de esta sección: **SMN, "Estadísticas Climatológicas Normales — República Argentina, período 1991-2020"** (ISSN 2953-5549), ficha **Santa Rosa Aero**, páginas 448-455 de la publicación. **Todos los valores de §3 son [V]** — extraídos directamente del PDF oficial.

### 3.1 La estación y los límites de la serie

| | |
|---|---|
| Estación | **SANTA ROSA AERO**, La Pampa |
| Identificador WIGOS | 0-20000-0-87623 |
| Latitud / Longitud | 36,59311° S / 64,27988° O |
| Altura campo de observación | **190 m** |
| Régimen de observación | **24 horas** (no figura marcada con "X" de tres observaciones diarias en el Cuadro 1) |
| Período de las normales | 1991-2020 (30 años) |
| **Período de las estadísticas de VIENTO** | **2011-2020 (10 años)** |

> ### ⚠️ Advertencia metodológica del propio SMN [V]
> *"Al analizar la velocidad del viento para el período 1991-2020, en la mayoría de las estaciones meteorológicas, se encontraron importantes diferencias de velocidad entre subperíodos dentro de la serie completa. Se infiere que esta disparidad pudo ser provocada por el cambio de instrumental... Por tal motivo, se decidió publicar únicamente los valores medios, extremos y la tabla de frecuencias y velocidades por dirección **sólo del período 2011-2020**."*
>
> **Es decir: la rosa de los vientos y las velocidades son de una serie de 10 años, no de 30.** Es lo mejor homogéneo disponible y es suficiente para decisiones de proyecto, pero no hay que presentarlo como "normal climatológica de 30 años". El resto de los parámetros (temperatura, precipitación, heladas, tormentas, granizo) sí son 1991-2020.
>
> A favor: Santa Rosa Aero es estación de **24 h**, así que sus máximos y frecuencias **no** están subestimados como sí ocurre en las estaciones de 3 observaciones diarias.

### 3.2 Velocidad media mensual del viento (km/h), 2011-2020

| | Ene | Feb | Mar | Abr | May | Jun | Jul | Ago | Sep | Oct | Nov | Dic | **Anual** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Promedio** | **16,8** | 15,0 | 15,1 | 13,5 | 12,3 | **11,8** | 12,9 | 14,4 | 15,9 | 16,1 | 16,6 | 16,4 | **14,7** |
| Máx. valor promedio | 18,5 | 17,6 | 18,0 | 15,9 | 14,4 | 14,4 | 15,6 | 16,7 | 19,6 | 17,8 | 17,8 | 19,6 | 16,1 |
| Mín. valor promedio | 14,8 | 12,0 | 12,8 | 11,3 | 10,7 | 9,8 | 9,6 | 12,6 | 13,3 | 14,8 | 14,6 | 14,3 | 13,6 |

**Lectura:**
- **Máximo en enero (16,8 km/h) y mínimo en junio (11,8 km/h).** El máximo es **verano-primavera**, no invierno. Esto contradice la intuición de "el viento es cosa del invierno" y tiene consecuencias directas: **la galería y el patio se usan justo en la temporada más ventosa.**
- La amplitud anual es baja: la relación mes más ventoso / mes menos ventoso es apenas **1,42**. **En Santa Rosa hay viento todo el año.**
- 14,7 km/h de media anual = **4,1 m/s**. La velocidad básica de diseño (50 m/s) es **12 veces** ese valor. Son escalas distintas: una es el promedio, la otra la ráfaga cincuentenaria.

### 3.3 Rosa de los vientos anual (frecuencia ‰ y velocidad media km/h), 2011-2020

| Dirección | Frecuencia (‰) | % del tiempo | Velocidad media (km/h) |
|---|---|---|---|
| **N** | **341** | **34,1 %** | **18** |
| **S** | **182** | **18,2 %** | **18** |
| W | 120 | 12,0 % | 8 |
| E | 90 | 9,0 % | 13 |
| NE | 81 | 8,1 % | 15 |
| SW | 68 | 6,8 % | 13 |
| SE | 56 | 5,6 % | 15 |
| NW | 51 | 5,1 % | 9 |
| **Calma** | **12** | **1,2 %** | — |

> ### 🔑 El dato central del documento
> **En Santa Rosa el viento viene del NORTE el 34 % del tiempo y del SUR el 18 %. Entre los dos suman más de la mitad del año. Son además los dos sectores más veloces (18 km/h de media cada uno).**
>
> **El sector menos ventoso es el NW-W (51 y 120 ‰, a sólo 9 y 8 km/h).**
>
> **Las calmas son el 1,2 % del año.** Santa Rosa prácticamente nunca está quieta. Cualquier expansión exterior sin reparo va a ser inutilizable buena parte del tiempo, y cualquier estrategia de ventilación natural tiene recurso de sobra.

### 3.4 Rosa de los vientos mes a mes

**Frecuencia (‰):**

| Dir | Ene | Feb | Mar | Abr | May | Jun | Jul | Ago | Sep | Oct | Nov | Dic | Anual |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **N** | 406 | 401 | **460** | 320 | 321 | 291 | 315 | 318 | 294 | 281 | 328 | 353 | **341** |
| NE | 102 | 101 | 92 | 79 | 87 | 36 | 56 | 69 | 91 | 100 | 79 | 77 | 81 |
| E | 102 | 95 | 82 | 104 | 84 | 37 | 55 | 64 | 111 | **144** | 112 | 95 | 90 |
| SE | 52 | 66 | 59 | 60 | 50 | 39 | 40 | 44 | 58 | 76 | 70 | 57 | 56 |
| **S** | 155 | 153 | 143 | 187 | 182 | 157 | 195 | 208 | **235** | 202 | 184 | 181 | **182** |
| SW | 53 | 46 | 39 | 68 | 56 | **106** | 86 | 83 | 62 | 66 | 74 | 72 | 68 |
| W | 76 | 76 | 76 | 112 | 139 | **220** | 171 | 153 | 112 | 94 | 108 | 103 | 120 |
| NW | 48 | 48 | 40 | 52 | 58 | **86** | 68 | 49 | 32 | 29 | 40 | 58 | 51 |
| **Calma** | 6 | 13 | 9 | 19 | 23 | **28** | 13 | 13 | 7 | 7 | 5 | 4 | 12 |

**Velocidad media por dirección (km/h):**

| Dir | Ene | Feb | Mar | Abr | May | Jun | Jul | Ago | Sep | Oct | Nov | Dic | Anual |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **N** | **20** | 18 | 18 | 17 | 15 | 16 | 16 | 19 | **20** | **20** | **20** | **20** | **18** |
| NE | 16 | 14 | 14 | 14 | 13 | 11 | 12 | 13 | 15 | 18 | 16 | 14 | 15 |
| E | 15 | 13 | 12 | 12 | 11 | 9 | 11 | 11 | 14 | 15 | 14 | 13 | 13 |
| SE | 17 | 16 | 15 | 13 | 12 | 11 | 13 | 14 | 16 | 16 | 17 | 16 | 15 |
| **S** | **19** | 18 | 18 | 16 | 16 | 15 | 16 | 18 | 18 | 18 | **19** | **19** | **18** |
| SW | 13 | 10 | 11 | 12 | 11 | 12 | 12 | 14 | 13 | 12 | 13 | 14 | 13 |
| **W** | 9 | 8 | 8 | 8 | **7** | 8 | **7** | 8 | 8 | 8 | 9 | 10 | **8** |
| NW | 10 | 10 | 10 | 9 | 8 | 9 | 9 | 9 | 9 | 8 | 10 | 11 | 9 |

**Observaciones:**
- El **N domina todos los meses del año sin excepción** (mínimo 281 ‰ en octubre, máximo 460 ‰ en marzo).
- El **S es el segundo sector en todos los meses**, con pico en **septiembre (235 ‰)**.
- El **W es un fenómeno de invierno**: salta de 76 ‰ en verano a **220 ‰ en junio** — pero es el más lento del año (7-8 km/h). Es viento de estabilidad invernal, no viento de tormenta.
- El **E tiene un pico de primavera** (144 ‰ en octubre), asociado al ciclo de las bajas del NO y las entradas del Atlántico.
- Las **calmas se concentran en otoño-invierno** (28 ‰ en junio, 23 ‰ en mayo) y desaparecen en primavera-verano (4-7 ‰ de octubre a enero).

### 3.5 Rosa de los vientos por estación del año

Promedios de las frecuencias mensuales (‰) y de las velocidades (km/h):

| Dir | **VERANO** (D-E-F) | **OTOÑO** (M-A-M) | **INVIERNO** (J-J-A) | **PRIMAVERA** (S-O-N) |
|---|---|---|---|---|
| **N** | **387 ‰ @ 19 km/h** | **367 ‰ @ 17** | **308 ‰ @ 17** | **301 ‰ @ 20** |
| NE | 93 @ 15 | 86 @ 14 | 54 @ 12 | 90 @ 16 |
| E | 97 @ 14 | 90 @ 12 | 52 @ 10 | 122 @ 14 |
| SE | 58 @ 16 | 56 @ 13 | 41 @ 13 | 68 @ 16 |
| **S** | **163 @ 19** | **171 @ 17** | **187 @ 16** | **207 @ 18** |
| SW | 57 @ 12 | 54 @ 11 | 92 @ 13 | 67 @ 13 |
| W | 85 @ 9 | 109 @ 8 | **181 @ 8** | 105 @ 8 |
| NW | 51 @ 10 | 50 @ 9 | 68 @ 9 | 34 @ 9 |
| Calma | 8 | 17 | 18 | 6 |

**Traducción a proyecto, estación por estación:**

- **VERANO** — el N sopla el 39 % del tiempo a 19 km/h, más S 16 % a 19 km/h. **Eje N-S = 55 % del tiempo, a velocidad alta.** Sólo 0,8 % de calmas. Una galería al N abierta es un corredor de viento. Pero también: **el recurso de ventilación cruzada N-S en verano es prácticamente permanente.**
- **PRIMAVERA** — la estación más ventosa en conjunto (N 20 km/h + S 18 km/h + E 122 ‰). Menos calmas del año (0,6 %). Es la estación de las tormentas de polvo (§3.8).
- **INVIERNO** — el N baja a 31 % y el W sube a 18 % pero débil. **El SW aparece (9 %) y es el viento frío del Pampero.** Las mayores calmas del año.
- **OTOÑO** — transición, con N todavía dominante (37 %) y W creciendo.

### 3.6 Índice de exposición direccional: de dónde viene la carga

La frecuencia sola engaña: un viento frecuente pero lento molesta poco. La carga mecánica y el enfriamiento convectivo escalan con **v²**. Índice propuesto (elaboración propia sobre datos SMN):

```
IE(dirección) = frecuencia(‰) × velocidad_media(km/h)²
```

normalizado a 100 %. Es proporcional a la presión dinámica acumulada en el tiempo por sector.

| Dirección | **Anual** | **Verano** | **Invierno** |
|---|---|---|---|
| **N** | **46,3 %** | **52,2 %** | **47,0 %** |
| **S** | **24,7 %** | **20,7 %** | **26,2 %** |
| NE | 7,6 % | 7,3 % | 4,1 % |
| E | 6,4 % | 6,6 % | 2,9 % |
| SE | 5,3 % | 5,6 % | 3,5 % |
| SW | 4,8 % | 3,1 % | 7,8 % |
| W | 3,2 % | 2,5 % | 5,7 % |
| NW | 1,7 % | 2,0 % | 2,9 % |

> ### 🔑 El 71 % de la carga de viento acumulada de Santa Rosa viene del eje N-S.
> El cuadrante **W-NW-SW aporta menos del 10 %**. Ese cuadrante es el **lado protegido natural** del lote — pero es también el lado del sol de la tarde de verano. Ver §4.1.

### 3.7 Vientos máximos y ráfagas

**Viento máximo diario registrado (km/h) con su dirección y fecha, 2011-2020:**

| Mes | Dir | km/h | Fecha |
|---|---|---|---|
| Ene | N | 98 | 17/01/2014 |
| **Feb** | **SE** | **143** | **12/02/2014** |
| Mar | S | 87 | 14/03/2018 |
| Abr | SW | 94 | 08/04/2014 |
| May | SE | 70 | 22/05/2017 |
| Jun | W | 96 | 17/06/2017 |
| Jul | S | 80 | 14/07/2014 |
| Ago | S | 85 | 01/08/2019 |
| Sep | S | 89 | 28/09/2013 |
| Oct | NE | 83 | 04/10/2014 |
| Nov | S | 93 | 26/11/2017 |
| Dic | W | 109 | 18/12/2020 |
| **ANUAL** | **SE** | **143** | **12/02/2014** |

**Lecturas críticas:**

1. **Los máximos NO vienen del sector dominante.** El N domina en frecuencia pero sólo produce un máximo mensual (98 km/h en enero). **Los extremos vienen del S (5 meses), SE (2), W (2), SW (1), NE (1).** Son eventos convectivos y frentes fríos, no el flujo medio.
   > **Consecuencia de proyecto de primer orden:** la barrera que hace confortable el patio (contra el N) **no es** la que salva la estructura (que se rompe con vientos del S/SE/W). **La estructura se calcula omnidireccional; el confort se resuelve direccional.** No se pueden intercambiar.
2. **El máximo registrado en 10 años, 143 km/h = 39,7 m/s**, corresponde a una presión dinámica ≈ 0,613 × 39,7² ≈ **966 N/m²** a 10 m en exposición C. La presión de diseño con V = 50 m/s es del orden de **1133 N/m²** (ver §8). Es decir: **en 10 años se alcanzó el 85 % de la presión de diseño.** El valor normativo no es una exageración; es un evento perfectamente plausible en la vida de la casa.
3. **[VERIFICAR en el glosario del SMN]** si "viento máximo diario" corresponde a ráfaga instantánea o a un promedio de intervalo. La velocidad V del CIRSOC está definida como ráfaga de **3 segundos**; si el registro del SMN fuera un promedio de 1 o 10 minutos, el valor comparable sería aún mayor. Santa Rosa Aero es estación de 24 h, así que el registro no está truncado por falta de observador.

### 3.8 Días con viento fuerte, tormenta, granizo y polvo

| Fenómeno | Ene | Feb | Mar | Abr | May | Jun | Jul | Ago | Sep | Oct | Nov | Dic | **Anual** | Período |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Viento fuerte** | 16,9 | 13,5 | 13,6 | 10,5 | 6,6 | 7,1 | 7,8 | 13,4 | 15,3 | 16,1 | 17,6 | **17,8** | **156,2** | 2011-2020 |
| Tormenta | 9,4 | 7,6 | 6,7 | 3,0 | 1,2 | 0,3 | 0,5 | 0,8 | 2,3 | 5,6 | 7,6 | 8,9 | **54,0** | 1991-2020 |
| Tempestad de polvo o arena | 4,1 | 2,5 | 2,1 | 1,2 | 1,0 | 1,4 | 1,7 | 4,5 | 4,9 | 3,4 | 5,1 | 5,0 | **36,8** | 1995-2020 |
| Granizo | 0,5 | 0,3 | 0,2 | <0,1 | 0,1 | 0,1 | 0,1 | 0,1 | 0,3 | 0,5 | 0,4 | 0,4 | **3,0** | 1991-2020 |
| Niebla | 0,4 | 1,2 | 1,9 | 2,9 | 5,5 | 6,1 | 4,7 | 2,9 | 1,6 | 1,5 | 0,6 | 0,3 | 29,7 | 1991-2020 |
| Helada | 0,0 | 0,0 | 0,0 | 0,4 | 2,9 | 6,6 | 9,8 | 7,0 | 2,6 | 0,3 | 0,1 | 0,0 | 29,7 | 1991-2020 |

Extremos registrados de días con viento fuerte: **máximo 218 días (2017), mínimo 89 días (2012)**.

> ### 🔑 **156 días de viento fuerte por año. Uno de cada 2,3 días.**
> Con máximos en **diciembre (17,8), noviembre (17,6), enero (16,9) y octubre (16,1)** — exactamente la temporada de uso del exterior. En mayo el mínimo es 6,6.
>
> **[VERIFICAR en el glosario del SMN]** el umbral exacto de "viento fuerte". La publicación no lo define; el SMN utiliza la escala de Beaufort modificada por Simpson. Históricamente el umbral se ubica en el orden de los **43 km/h (fuerza 6-7)**. Aun con la incertidumbre del umbral, el patrón estacional y la magnitud (156 días) son inequívocos.

**37 días al año de tempestad de polvo o arena**, con máximo en noviembre (5,1) y septiembre (4,9). Esto es un argumento de proyecto por sí solo: **sellado de carpinterías, filtros, cámara de aire ventilada con protección, no dejar juntas abiertas a barlovento.** El polvo entra por donde entra el aire.

**3 días de granizo al año.** Bajo, pero suficiente para descartar policarbonato fino y chapas ultralivianas en galerías y para exigir espesor de chapa razonable en cubiertas.

### 3.9 Síntesis del dato climático

| Pregunta | Respuesta con dato |
|---|---|
| ¿De dónde viene el viento? | **Del N (34 % del tiempo) y del S (18 %)**. El eje N-S concentra el 71 % de la carga acumulada. |
| ¿Con qué intensidad? | **18 km/h de media** en ambos sectores dominantes; 14,7 km/h de media anual global. |
| ¿Cuándo es peor? | **Primavera y verano** (dic-ene y oct-nov-dic para viento fuerte). Mínimo en mayo-junio. |
| ¿Hay calmas? | **1,2 % del año.** Prácticamente no. |
| ¿De dónde vienen los golpes? | **S, SE y W** — ráfagas de 87 a 143 km/h. **No** del sector dominante. |
| ¿Cuál es el lado protegido? | **W-NW-SW**: menos del 10 % de la carga acumulada. |
| ¿Cuántos días molesta? | **156 días de viento fuerte + 37 de tempestad de polvo**. |

---

## 4. Implantación, orientación y expansiones

### 4.1 El conflicto central del proyecto en Santa Rosa

> **En el hemisferio sur el sol viene del NORTE. En Santa Rosa el viento también viene del NORTE.**
>
> **La orientación óptima de asoleamiento y la orientación de máxima exposición al viento son la misma. Este es EL problema de proyecto de una casa en Santa Rosa y todo lo demás se deriva de acá.**

Datos que definen el conflicto:

| | Norte | Sur |
|---|---|---|
| Asoleamiento | Sol todo el año. Altura solar mediodía: **77°** en solsticio de verano, **30°** en solsticio de invierno (latitud 36,6° S) | Sin sol directo en invierno |
| Viento | **34 % del tiempo, 18 km/h, 46 % de la carga acumulada** | **18 % del tiempo, 18 km/h, 25 % de la carga** |
| Temperatura del viento | Cálido/seco (norte pampeano) | Frío (Pampero, entradas del S) |
| Rol en verano | Sol alto → fácil de sombrear con alero; viento = **recurso** de ventilación | Viento fresco = **recurso** |
| Rol en invierno | Sol bajo → ganancia solar deseada; viento = molestia moderada | Viento frío = **problema**, pérdidas |

**Las dos direcciones no son simétricas y hay que tratarlas distinto:**

- **NORTE = filtrar, no bloquear.** El viento N es cálido y coincide con el sol. Hay que **frenarlo parcialmente sin perder el sol**: parapetos bajos, pantallas porosas, vegetación caduca de porte medio. Una barrera opaca al N mata el asoleamiento de invierno y no hace falta: el viento N no es el que rompe cosas.
- **SUR = cerrar.** El viento S es frío, trae los máximos y no aporta sol. **Fachada sur compacta, aberturas mínimas, locales de servicio, la mejor aislación y el mejor sellado de la casa.**
- **OESTE/NOROESTE = el lado tranquilo.** Menos del 10 % de la carga. Pero es el sol de la tarde de verano (el peor). Es el lugar ideal para **expansiones protegidas del viento que necesiten protección solar activa** (parral caduco, pérgola, toldo).
- **ESTE = el compromiso.** 9 % del tiempo a 13 km/h, sol de la mañana, sin sobrecalentamiento. **Es la mejor orientación para un patio de uso matutino y para dormitorios.**

### 4.2 Dónde va la galería, el quincho y el patio

| Espacio | Ubicación recomendada | Por qué |
|---|---|---|
| **Galería principal / expansión del estar** | **Al NORTE, pero acotada lateralmente y con filtro en el borde N** | Es la única orientación con sol de invierno. El viento se filtra, no se bloquea (§4.1). |
| **Patio de estar / parrilla / pileta** | **Al NE o al E**, con la casa cerrando el S y una barrera porosa al N | El E es el sector de menor exposición entre los que reciben sol útil |
| **Quincho / parrilla cerrada** | **Al W o NW**, adosado, con parral o pérgola | Es el sector de menor carga de viento (3,2 % + 1,7 %); el sobrecalentamiento se resuelve con vegetación caduca |
| **Tendedero / lavadero exterior** | **Al N o NE, expuesto** | El viento acá es recurso: 156 días de viento fuerte secan ropa. Único caso donde la exposición es un activo |
| **Cocheras, depósitos, tanques** | **Al SUR o SW** | Amortiguan la fachada fría y no requieren confort |
| **Dormitorios** | E y NE | Sol de mañana, viento moderado, ventilación cruzada al S |

**Regla de la galería al norte (dimensional):**

Con altura solar mediodía **30° en invierno**, un parapeto de altura `h_p` proyecta una sombra de `h_p / tan(30°) = 1,73 · h_p` hacia adentro de la galería.

| Altura del parapeto/pantalla | Sombra al mediodía de invierno | Efecto sobre el viento a 1,0 m del suelo |
|---|---|---|
| 0,90 m | 1,56 m | Reparo del cuerpo sentado; parcial |
| **1,10 m** | **1,90 m** | **Buen reparo sentado; sol sobre el torso** |
| 1,50 m | 2,60 m | Reparo de pie; sombrea toda la profundidad útil de la galería en invierno |

**Recomendación:** parapeto macizo de **1,00-1,10 m** + **pantalla porosa (40-50 % de vacíos) de 0,80-1,00 m encima**, hasta 1,80-2,10 m. El macizo protege al ocupante sentado; la porosa evita la turbulencia de una barrera opaca alta (§5.1) y deja pasar sol filtrado. Este es el detalle más rentable de todo el proyecto.

### 4.3 Configuraciones de planta que funcionan y que no

```
                                N (viento 34% + sol)
                          ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

   ✗ MAL: "U" abierta al N        ✓ BIEN: "L" con brazo al O
   ┌────┐        ┌────┐            ┌───────────────┐
   │    │ PATIO  │    │            │               │
   │    │ ←túnel │    │            │   CASA        │
   │    │        │    │            │               │
   └────┴────────┴────┘            └───┬───────────┘
   El patio embudo acelera             │  PATIO NE
   el viento N entre los brazos.       │  (protegido del S por
   Peor que sin brazos.                │   la casa, del O por
                                       │   el brazo, del N por
   ✗ MAL: galería corrida N            │   barrera porosa)
   sin cierre lateral E y O            └── barrera porosa ────
   → corredor E-O y colador N
```

| Configuración | Veredicto | Motivo |
|---|---|---|
| **Barra E-O con galería al N, cerrada en los extremos E y O** | ✓ Muy buena | Fachada N larga con sol; los testeros cortan el flujo lateral; fachada S ciega |
| **"L" con el brazo N-S sobre el lado O del lote** | ✓ Muy buena | Genera patio NE protegido por dos lados; el brazo O protege del sol de la tarde también |
| **"C" abierta al E o NE** | ✓ Buena | Tres lados de reparo; abertura hacia el sector de menor carga |
| **"U" abierta al N** | ✗ Mala | Efecto embudo: acelera el viento dominante justo donde se quiere estar |
| **Barra N-S** | ✗ Mala | Máxima superficie a los sectores E y O (poco sol útil, mucho sol de tarde) y mínima al N |
| **Casa exenta en el centro del lote** | ✗ Regular | Sin lado protegido; todos los frentes expuestos; obliga a barreras en todo el perímetro |
| **Patio interior / claustro** | ✓ Excelente térmicamente, ✗ costoso | Reparo total; pero en lote urbano estándar de Santa Rosa suele no entrar |

### 4.4 Errores que generan túnel de viento

1. **Pasillos entre medianera y casa de menos de 1,5 m.** El estrechamiento acelera el flujo (efecto Venturi). Si hay que dejar un paso lateral, o se ensancha o se cierra con portón macizo en el extremo de barlovento.
2. **Pasajes bajo la casa / bajo galería (pilotis parciales).** Concentran el flujo bajo el volumen. Si hay desnivel, cerrar el zócalo.
3. **Aberturas enfrentadas N-S sin control.** Excelente para ventilación cruzada (§10), inutilizable si no hay una regulación fina. **Toda abertura N y S necesita al menos tres posiciones de apertura, no dos.**
4. **Patio embudo entre dos volúmenes convergentes.** Cualquier planta que estreche hacia sotavento acelera.
5. **Barreras opacas altas y cortas.** Una medianera de 2,2 m de sólo 6 m de largo genera más turbulencia de la que quita: el viento la flanquea y "invade" la zona de calma (§5.1). La longitud mínima útil de una barrera es **10 veces su altura** [V, Ramilo/UNLP].
6. **Aleros continuos sin interrupción sobre el frente de barlovento**, que actúan como ala. Ver §7.6.

---

## 5. Barreras de viento: vegetales y construidas

### 5.1 Física de la barrera: la porosidad manda

Cuando el viento encuentra una barrera se acumula a barlovento (sobrepresión), una parte la atraviesa y otra asciende. **Lo que determina el tamaño y la calidad de la zona de calma no es cuánto se opone la barrera, sino cuánto la deja pasar.**

| Tipo de barrera | Porosidad óptica | Comportamiento |
|---|---|---|
| **Densa / impermeable** | **< 15 %** | Casi todo el viento asciende. Reducción máxima muy alta (85 %) pero **inmediatamente detrás**, y luego el flujo desciende bruscamente generando **turbulencia y recirculación**. Zona protegida corta. |
| **Semipermeable** | **15-45 %** (algunas fuentes: 25-50 %) | Parte del flujo atraviesa a velocidad reducida, lo que "empuja" hacia sotavento el descenso del flujo superior. **Reducción alta sobre una zona larga y sin turbulencia.** |
| **Permeable / porosa** | **> 45-50 %** | Reducción moderada pero muy extendida. |

> **Para una casa, la barrera correcta es la SEMIPERMEABLE.** La densa produce, a 2-4 alturas, una zona de remolinos que es peor que el viento laminar: es la razón por la que un muro macizo de 2,2 m no hace confortable el patio que está detrás.

### 5.2 Datos de investigación: reducción vs. porosidad vs. distancia

**[V] Peri, P. L. (1998), "Efectos de parámetros estructurales de cortinas forestales en la reducción del viento en la provincia de Santa Cruz, Argentina", *Quebracho* N° 6, pp. 20-27.** Mediciones de campo con anemómetros a 1,50 m, viento testigo entre 20 y 80 km/h, cortinas de 100 m de longitud orientadas perpendiculares al viento dominante.

**Reducción relativa de la velocidad del viento, R₁ = (u₀ − u_s)/u₀, en %:**

| Distancia a sotavento | **Densa** (<15 %) | **Semipermeable** (15-45 %) | **Permeable** (>45 %) |
|---|---|---|---|
| 0,5 Ht | 60 % | 40 % | 35 % |
| **1 Ht** | **85 %** ← máx. | 50 % | 40 % |
| 2 Ht | 70 % | 55 % | **45 %** ← máx. |
| **4 Ht** | 60 % | **75 %** ← máx. | 42 % |
| 5 Ht | 55 % | 70 % | 40 % |
| 7 Ht | 50 % | 60 % | 38 % |
| 10 Ht | 30 % | 40 % | 35 % |
| 15 Ht | — | 30 % | 35 % |
| 18 Ht | — | — | 30 % |
| **Longitud de zona protegida** | **10 Ht** | **15 Ht** | **18 Ht** |

*(Ht = altura total de la barrera. Criterio de fin de protección: cuando se recupera el 70 % de la velocidad testigo a 1,50 m de altura.)*

**[V] Datos complementarios de la misma línea de investigación:**
- **Ramilo, D. (2021), cap. 4 "Cortinas forestales", en *Sistemas Agroforestales en Argentina*, FCAyF-UNLP:** cortina densa (<15 %) → máxima reducción a **3-4 H**, zona útil hasta **10 H**; cortina semipermeable (25-50 %) → zona protegida hasta **20 H**, máxima reducción entre **5 y 10 H**.
- **Guyot y Elejabeitia (1970), citados por Peri:** la acción de las cortinas semipermeables alcanza **20 H**; las impermeables, sólo **11 H**.
- **FAO (1962), obs. en Suiza, citado por Peri:** una cortina muy densa reduce la velocidad al **15 % de la inicial a 1 H**, pero el viento **recupera su velocidad inicial a 24 H**.
- **[V] Efecto del ángulo de incidencia:** dentro de un sector de **±45°** respecto de la perpendicular, el efecto de la dirección sobre la reducción es despreciable (Konstantinov y Struzer, 1969, citado por Peri). **Fuera de ±45° la protección cae rápido.**
- **[V] Efecto de la velocidad:** en el rango 20-80 km/h la reducción relativa R₁ es **estable** (variación máxima 4 %). Es decir, **el porcentaje de reducción no depende de la intensidad del viento** — la barrera funciona igual con 20 que con 80 km/h. Por debajo de 18 km/h, R₁ es errática.
- **[V] Vientos > 50 km/h deforman la copa** (flexión de ramas y reorientación del follaje), **aumentan la porosidad efectiva y reducen el efecto protector** (Gardiner et al., 2016, citado por Ramilo). **Una cortina vegetal protege el confort, no la estructura.**
- **[V] Longitud mínima:** el largo ininterrumpido debe ser **≥ 10 H**. Los bordes son flanqueados y el área protegida en planta es trapezoidal, no rectangular.
- **[V] Las brechas son peores que la ausencia de barrera** en la brecha misma: el viento se acelera al pasar por la constricción.

### 5.3 Dimensionado en un lote urbano de Santa Rosa

En un lote de 10-12 × 30-40 m no hay lugar para cortinas de 20 m de altura ni de 200 m de largo. Hay que **escalar el problema**: lo que importa es la relación distancia/altura, y en un lote urbano las alturas útiles están entre **1,8 y 6 m**.

**Tabla de diseño — barrera semipermeable (porosidad 30-45 %), aplicando R₁ de Peri (1998):**

| Altura de la barrera **H** | Zona de máxima protección (**4 H**, R₁ ≈ 75 %) | Fin de la zona protegida (**15 H**, R₁ ≈ 30 %) | Uso típico |
|---|---|---|---|
| **1,8 m** (cerco / seto bajo) | 7,2 m | 27 m | Reparo de una galería adyacente |
| **2,2 m** (medianera con celosía) | 8,8 m | 33 m | Patio pegado a la casa |
| **3,0 m** (seto formado / panel) | 12 m | 45 m | Patio + pileta |
| **5,0 m** (árboles jóvenes, 5-8 años) | 20 m | 75 m | Fondo del lote completo |
| **8,0 m** (árboles adultos) | 32 m | 120 m | Lote entero + vecinos |

**Cómo usar la tabla en el proyecto:**

1. **Marcar dónde se va a estar** (galería, parrilla, mesa exterior, pileta). Ese es el punto que hay que proteger.
2. **Medir la distancia D desde ese punto hasta el borde N del lote** (el sector dominante).
3. **Altura necesaria: H ≈ D / 4** para máxima protección, o **H ≥ D / 10** para protección aceptable (R₁ ≈ 40 %).
   - Ejemplo: galería a 6 m del cerco norte → **H = 1,5 m para máximo, con 6 m ya se está a 4H de un cerco de 1,5 m**. Un cerco de 1,8-2,0 m al N a 6-8 m de la galería es el punto óptimo.
   - Ejemplo: mesa exterior a 12 m del fondo → H ≈ 3,0 m.
4. **Si la barrera está muy cerca (< 1 H), no protege: turbulenta.** Distancia mínima útil de una barrera: **1 H**.
5. **Longitud: ≥ 10 H, y en todo caso ≥ 3 veces el ancho del área a proteger.** Para una galería de 6 m, la barrera N debe tener al menos 10-12 m de largo, no 6.
6. **Orientación: perpendicular al N ± 45°.** Es decir, una barrera E-O protege del N, NE y NW. Una barrera orientada NE-SO no protege del N.

### 5.4 Especies

**[V] Especies usadas en cortinas forestales en la Región Pampeana** (Ramilo, 2021, Tabla 6):
*Casuarina* spp.; *Eucalyptus camaldulensis*; *E. tereticornis*; clones de *Populus deltoides* y *P. × euroamericana*; *Cupressus sempervirens*, *C. macrocarpa*, *C. × leylandii*.

**[V] Espaciamientos de plantación por especie y porosidad buscada** (Ramilo, 2021):

| Especie | Cortina **semipermeable** | Cortina **densa/poco permeable** | Cortina **permeable** |
|---|---|---|---|
| *Casuarina* spp. | **2,0-2,5 m** entre plantas | 1,2-1,5 m | — |
| *Eucalyptus* spp. | 2,0-3,0 m | — | — |
| *Populus* fastigiado (álamo criollo) | **1,2-1,5 m** | — | **2,0-2,5 m** |
| *Salix* (sauce) | — | 1,0 m (doble hilera) | **3,0 m** |
| *Cupressus macrocarpa* / *C. × leylandii* | — | **≥ 4,0 m** (copa muy extendida) | — |

**[V] Diseño:** de **1 a 3 hileras** (excepcionalmente 4); con 2 hileras, disposición **al tresbolillo** (desfase 50 %), separación entre hileras 1,5-3,0 m.

**Adaptación al caso urbano de Santa Rosa — criterio del estudio:**

| Rol | Especie | Observación |
|---|---|---|
| **Barrera perenne de fondo de lote (5-8 m)** | *Cupressus sempervirens* (ciprés piramidal) | Perenne (protege también en invierno), copa columnar, poco ancho. Distanciamiento 1,5-2,0 m para semipermeable. **[VERIFICAR en vivero local]** su comportamiento en suelo pampeano y régimen de 750 mm/año |
| **Barrera perenne compacta** | *Casuarina* spp. | Alta tolerancia a viento y sequía; muy usada en la región pampeana. Copa fina, buena porosidad natural |
| **Barrera media / seto formado (2-3 m)** | *Ligustrum* (ligustro/ligustrina) | Ya presente masivamente en Santa Rosa (11,3 % del arbolado del barrio relevado). Perenne, se poda a la altura buscada. **Precaución: es invasora y muy alergénica** |
| **Sombra + filtro estacional al N** | *Fraxinus* (fresno), *Morus alba* sin fruto, parra | **Caducos**: sombra en verano, sol en invierno. **Pero [V, CIRSOC 102-25]: un caduco aporta sólo el 15 % de su área frontal como obstrucción efectiva.** Como barrera de viento, en invierno no cuentan |
| **Lo que NO conviene** | *Populus* (álamo), *Salix* (sauce), *Melia azedarach* (paraíso) en lote chico | Raíces agresivas cerca de fundaciones y cloacas; álamo y paraíso de madera frágil, rompen con viento fuerte |

> **[V] Contexto local:** el arbolado de alineación de Santa Rosa está fuertemente dominado por **fresno (57,3 % en el barrio Santa María de las Pampas)**, seguido de ligustro (11,3 %), arce (5,2 %) y paraíso (5,2 %); es un arbolado joven, de baja diversidad y con sobreuso del fresno. Hay **2.525 ejemplares en estado malo a muy malo** que deberían reemplazarse a corto plazo (Semiárida, UNLPam). **No se puede contar con el arbolado de vereda como barrera: es caduco, es joven, y en la mitad del año no está.**

**Restricción crítica de plantación:** verificar distancia mínima a fundaciones, cloacas y medianera. **[VERIFICAR en el Código de Edificación / Ordenanza de Arbolado de la Municipalidad de Santa Rosa]** distancias obligatorias y especies permitidas/prohibidas en vereda y en lote.

### 5.5 Barreras construidas: muros, pantallas, celosías

**La regla es la misma que para la vegetación: 30-50 % de vacíos.** Un muro macizo es la peor barrera posible para el confort.

| Solución | Porosidad | Cuándo usarla | Precaución estructural |
|---|---|---|---|
| **Muro macizo bajo (0,90-1,10 m) + celosía encima** | 0 % abajo, 40-50 % arriba | **La mejor solución para el borde N de la galería** | El macizo bajo no tiene problema de vuelco; la celosía sí carga: ver §9.4 |
| **Ladrillo hueco colocado con vacíos a la vista (celosía cerámica)** | 30-40 % | Cerramientos de patio, medianeras altas | Es una pared: necesita pilastras. **Además la porosidad reduce el Cf de la barrera** |
| **Listones de madera / metal verticales u horizontales, luz = ancho del listón** | 50 % | Pantallas móviles, cierres de galería | Fijaciones: la vibración afloja tornillos. Usar arandelas elásticas |
| **Panel de chapa perforada** | 30-40 % | Estética contemporánea, bajo mantenimiento | Chapa perforada + viento = **ruido**. Verificar |
| **Vidrio / policarbonato ciego** | 0 % | Sólo si se necesita ver a través Y no se puede filtrar | Barrera densa: turbulencia a sotavento. Y carga total de viento sobre la fijación |
| **Media sombra / malla textil** | 20-50 % según densidad | Provisorio, mientras crece la vegetación | **Se rompe**. En Santa Rosa dura 1-2 temporadas. No es solución permanente |

> **Estrategia recomendada para Santa Rosa: barrera compuesta.**
> `muro bajo macizo (1,00 m) + celosía 40-50 % (0,80-1,00 m) + vegetación semipermeable detrás (3-5 m)`.
> El muro protege al ocupante sentado desde el día 1; la celosía evita la turbulencia; la vegetación toma el relevo en 5-8 años y sube la altura efectiva de 2,0 a 5,0 m, multiplicando por 2,5 la zona protegida.

---

## 6. Cerramientos: infiltración de aire y estanqueidad

### 6.1 Por qué en zona ventosa la infiltración se come la aislación

La pérdida de calor de una vivienda tiene dos componentes: **transmisión** (por los cerramientos, gobernada por K y por el espesor de aislante) e **infiltración/renovación** (por el aire que entra y sale, gobernada por la estanqueidad y **por la presión de viento**).

El punto es que **la infiltración depende del viento y la transmisión no**. Con 156 días de viento fuerte al año, en Santa Rosa la infiltración es la componente variable dominante.

**Estimación de la presión que empuja el aire a través de las juntas:**

| Velocidad del viento | Presión dinámica q = 0,613·v² (Pa) | Δp aprox. entre barlovento y sotavento (≈ 1,3 q) |
|---|---|---|
| 15 km/h (4,2 m/s) — media anual | 11 Pa | 14 Pa |
| 30 km/h (8,3 m/s) | 42 Pa | 55 Pa |
| **43 km/h (12 m/s) — "viento fuerte"** | **88 Pa** | **115 Pa** |
| 60 km/h (16,7 m/s) | 171 Pa | 222 Pa |
| 100 km/h (27,8 m/s) | 474 Pa | 616 Pa |

**El ensayo de infiltración de la IRAM 11507-1 se hace a 100 Pa.** Esa presión corresponde a un viento del orden de **46 km/h**, es decir, **la condición de "viento fuerte" que en Santa Rosa ocurre 156 días al año**. No es una condición extrema de laboratorio: es un martes cualquiera de noviembre.

**El aire que entra por infiltración hay que calentarlo entero.** Energía por renovación:

```
Q_inf [W] = 0,34 · V_aire [m³/h] · ΔT [K]
```

Con un ΔT de invierno de 20 K (interior 20 °C, exterior 0 °C — Santa Rosa tiene **29,7 días de helada al año**):

| Caudal infiltrado | Pérdida a ΔT = 20 K | Equivalente en superficie de muro K=0,5 |
|---|---|---|
| 100 m³/h | 680 W | **68 m² de muro bien aislado** |
| 200 m³/h | 1360 W | 136 m² |
| 500 m³/h | 3400 W | 340 m² |

> **Traducción brutal:** una casa con carpinterías mediocres y sin sellado perimetral puede perder por infiltración **más que por todos sus muros aislados juntos**. Poner 10 cm de EPS y una carpintería sin ruptura de puente térmico ni burlete es tirar la plata. **En Santa Rosa el sellado precede a la aislación en orden de prioridad.**

### 6.2 IRAM 11507-1 — clasificación de estanqueidad

**IRAM 11507-1** — *"Carpintería de obra. Ventanas exteriores. Requisitos básicos y clasificación"*. Establece los requisitos básicos que deben cumplir las ventanas exteriores y puertas-ventana de edificios (incluidos vidrios, accesorios y herrajes) y permite clasificarlas por infiltración de aire y estanqueidad al agua.

**Clasificación de infiltración de aire (cap. 4.6), medida a 100 Pa:**

| Clase | Denominación | Caudal admisible |
|---|---|---|
| **IRAM A1** | Normal | > 4,01 hasta 6,00 m³/(h·m de junta) |
| **IRAM A2** | Mejorada | > 2,01 hasta 4,00 m³/(h·m) |
| **IRAM A3** | Reforzada | hasta 2,00 m³/(h·m) |

**[VERIFICAR contra el texto de la norma IRAM 11507-1, cap. 4.6]** — los valores numéricos de la tabla provienen de fuentes secundarias, no del texto normativo. Lo que **sí está [V]** en fuente oficial (Decreto 1030/2010 de la Provincia de Buenos Aires, reglamentario de la Ley 13.059, art. 2.7.1) es la **exigencia**:

> *"Infiltración de aire según el capítulo 4.6 de la norma IRAM N° 11507-1, cumpliendo la **Clasificación IRAM A1** para carpinterías colocadas en edificios de **hasta 10 m de altura** sobre el nivel del terreno (medida hasta el dintel de la ventana) y la **Clasificación IRAM A2** para las colocadas por encima de ese nivel."*

> ### ⚠️ Criterio del estudio para Santa Rosa
> **A1 es el mínimo legal de una casa de una planta en jurisdicciones que adoptan ese criterio, y es insuficiente para Santa Rosa.**
>
> Razonamiento: A1 admite hasta **6 m³/h por metro lineal de junta**. Una casa de una planta con, digamos, 60 m lineales de junta perimetral de carpintería puede llegar a **360 m³/h a 100 Pa** sólo por las ventanas, sin contar puertas ni el sellado ventana-muro. A ΔT = 20 K eso son **2,4 kW**. Con A3 (2 m³/h·m) el mismo perímetro da 120 m³/h → 0,8 kW. **La diferencia entre A1 y A3 es del orden de un aire acondicionado entero de consumo permanente en invierno.**
>
> **Exigir A2 como mínimo y A3 donde el presupuesto lo permita**, particularmente en la fachada SUR (viento frío) y en las aberturas grandes del NORTE.

**[VERIFICAR en IRAM 11507-1]** la clasificación de **estanqueidad al agua** (clases E, con presiones de ensayo en Pa) y sus exigencias. Es igual de relevante: en Santa Rosa la lluvia rara vez cae vertical.

**Otras partes de la serie que conviene tener a mano:**
- IRAM 11507-4: requisitos complementarios de **aislación térmica** de ventanas exteriores.
- IRAM 11507-5: metodología de los ensayos, orden cronológico y criterios.
- IRAM 11507-6: **etiquetado de eficiencia energética** de ventanas — permite comparar productos del mercado.

### 6.3 Sellado perimetral: dónde entra realmente el aire

**La clasificación IRAM mide la ventana, no la obra.** En obra el aire entra por otro lado:

| Punto de fuga | Magnitud relativa | Solución |
|---|---|---|
| **Junta marco-muro (perímetro de la abertura)** | **La principal**. En obra tradicional argentina se rellena con mortero y se revoca encima; el mortero fisura y se abre | Espuma de poliuretano de baja expansión + **cinta o sellador elástico continuo** por el lado interior (barrera de aire) y por el exterior (barrera de agua/viento). No confiar en el revoque |
| **Encuentro muro-cubierta** (coronamiento) | Muy alta en cubierta liviana. Es también el punto donde el viento genera más succión | Sellado continuo del plano de aire; no dejar la cámara del techo comunicada con el interior |
| **Cajas de persianas** | Alta. Una caja de persiana sin aislar y sin sellar es un agujero permanente | Cajón aislado y estanco, con acceso sellado. O persiana exterior sin caja interior |
| **Pasos de instalaciones** (caños, cables, campana, salidas de aire) | Media, pero acumulativa | Pasamuros con collarín sellado, cada uno |
| **Cajas de electricidad en muro exterior** | Baja pero múltiple | Cajas estancas o sellado del conducto |
| **Puerta de acceso y de garaje** | Alta. Ver §9.1 | Burlete perimetral de 3 lados + burlete de umbral |
| **Chimenea / hogar a leña sin cierre** | Muy alta cuando no está en uso | Registro de tiro con cierre efectivo |

**Detalle de proyecto obligatorio en Santa Rosa: definir el PLANO DE ESTANQUEIDAD AL AIRE** en el corte constructivo — una línea continua que recorre toda la envolvente, sin interrupciones, y decir en el pliego con qué material se resuelve en cada tramo y en cada encuentro. Si la línea se corta en el dibujo, se corta en la obra.

### 6.4 Presión de viento sobre las carpinterías (componentes y revestimientos)

Las carpinterías no sólo tienen que ser estancas: tienen que **resistir** la presión. Ver el cálculo en §8.7. Valores de referencia para la casa tipo del §8, exposición C, **mayorados (1,6 W)**:

| Elemento | Presión de diseño (kN/m²) | Equivalente (kgf/m²) |
|---|---|---|
| Ventana en zona central de fachada | ≈ **2,0 / −2,2** | 200 / −220 |
| Ventana en **zona de borde** (a menos de 1 m de la esquina de la casa) | ≈ **2,0 / −2,6** | 200 / −265 |
| **Portón de garaje 2,50 × 2,20 m** | ≈ **2,0 / −2,1** → **~12 kN totales** | ~1.200 kgf sobre el portón |

**Exigir en el pliego que la carpintería declare resistencia a la carga de viento**, no sólo estanqueidad. **[VERIFICAR en IRAM 11507-1 y 11507-3]** la clasificación de resistencia a la carga de viento (clases V o similares) y sus presiones de ensayo.

---

## 7. CUBIERTA: el punto crítico de una casa baja

### 7.1 Por qué la cubierta es el problema y no los muros

En un edificio en altura, el viento es un problema de **estabilidad lateral**: vuelco, corte basal, deriva. En una casa de una planta eso desaparece: el corte por viento es una fracción trivial del peso.

**En una casa baja el viento es un problema de SUCCIÓN VERTICAL sobre la cubierta.** Tres razones:

1. **El flujo se separa en el borde de barlovento y genera vórtices cónicos** en las esquinas del techo. Ahí las succiones locales son de 3 a 4 veces la presión dinámica de referencia.
2. **La superficie de cubierta es la mayor de la casa** (en una casa de una planta, la cubierta es ≈ 50 % de la superficie de envolvente, contra ≈ 15 % en un edificio de 10 pisos).
3. **El peso propio de una cubierta liviana es despreciable frente a la succión.** En el ejemplo del §8: succión mayorada 5,0 kN/m² en esquina contra 0,05 kN/m² de peso de la chapa. **Relación 100:1.**

> **La casa no se vuelca. El techo vuela. Y cuando el techo vuela, la casa queda destechada y con el interior presurizado, y después se caen los muros.**

### 7.2 Zonas de la cubierta: la dimensión `a`

**[V] CIRSOC 102-2005, notas de las Figuras 4 y 5:**

```
a = el MENOR de:  0,10 × (menor dimensión horizontal del edificio)
                  0,40 × h                                (h = altura media de cubierta)

pero NO menor que el MAYOR de:  0,04 × (menor dimensión horizontal)
                                1,00 m
```

Para la casa tipo del §8 (10 × 12 m, h = 3,61 m): **a = 1,00 m**.

Las zonas de succión agravada son fajas de ancho `a` en los bordes y cuadrados de `a × a` (o `2a`) en las esquinas y a lo largo de la cumbrera. **En una casa chica `a` es sólo 1 metro, y por eso todo el mundo lo ignora. Es justo donde arranca el desprendimiento.**

| Zona | Ubicación en una cubierta a dos aguas |
|---|---|
| **1** | Interior de cada faldón |
| **2** | Fajas de ancho `a` a lo largo de los aleros, de los hastiales y de la cumbrera |
| **3** | Cuadrados de esquina — encuentro alero/hastial, y extremos de la cumbrera |
| **Alero** | La parte volada, con coeficientes propios que **ya incluyen la presión de la cara inferior** |

### 7.3 Coeficientes de presión externa para la cubierta

**A) Para el SPRFV (sistema principal): Figura 4 de CIRSOC 102-2005, GC_pf, edificios de baja altura h ≤ 20 m** — [V] transcripción completa de la tabla:

**CASO A (viento normal a la cumbrera):**

| θ (grados) | 1 | 2 | 3 | 4 | 1E | 2E | 3E | 4E |
|---|---|---|---|---|---|---|---|---|
| 0 – 5 | 0,40 | −0,69 | −0,37 | −0,29 | 0,61 | −1,07 | −0,53 | −0,43 |
| **20** | **0,53** | **−0,69** | **−0,48** | **−0,43** | **0,80** | **−1,07** | **−0,69** | **−0,64** |
| 30 – 45 | 0,56 | 0,21 | −0,43 | −0,37 | 0,69 | 0,27 | −0,53 | −0,48 |
| 90 | 0,56 | 0,56 | −0,37 | −0,37 | 0,69 | 0,69 | −0,48 | −0,48 |

**CASO B (viento paralelo a la cumbrera):**

| θ | 1 | 2 | 3 | 4 | 5 | 6 | 1E | 2E | 3E | 4E | 5E | 6E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 – 90 | −0,45 | −0,69 | −0,37 | −0,45 | 0,40 | −0,29 | −0,48 | −1,07 | −0,53 | −0,48 | 0,61 | −0,43 |

*(Superficies: 1 = pared a barlovento, 2 = cubierta a barlovento, 3 = cubierta a sotavento, 4 = pared a sotavento; en Caso B, 5 y 6 son las paredes de hastial. Sufijo E = zonas de extremo, de ancho 2a.)*

**[V] Notas críticas de la Figura 4, que casi nadie aplica:**
- *Nota 2:* "el edificio se debe rotar en incrementos de 90° de manera tal que **cada esquina a su turno sea esquina de barlovento**". **Hay que correr 4 (Caso A) + 4 (Caso B) = 8 hipótesis, no 2.**
- *Nota 4b:* "Excepto para pórticos resistentes a flexión, **el corte horizontal total no debe ser menor que el determinado al despreciar las fuerzas del viento sobre las superficies de la cubierta**." → En una cubierta inclinada la succión del faldón de barlovento **descarga** horizontalmente y esta nota lo impide. Ver §8.6: **la nota gobierna**.
- *Nota 4a:* el GC_pf negativo de zona 2 se aplica desde el borde hasta **0,5 × (dimensión horizontal perpendicular al alero)** o **2,5 h**, el menor; más allá, hasta la cumbrera, se usa el coeficiente de zona 3.
- *Nota 5:* hay que combinar con las presiones internas de la Tabla 7 en la forma más severa.

**B) Para componentes y revestimientos (chapa, tejas, correas, cabios, fijaciones): Figura 5B de CIRSOC 102-2005, GC_p, h ≤ 20 m.**

Los valores dependen del **área de viento efectiva** de cada elemento (escala logarítmica, de 0,1 a 100 m²).

**Cubierta a dos aguas 10° < θ ≤ 30° (Figura 5B cont.):**

| Zona | GC_p (A ≈ 1 m²) | GC_p (A ≈ 10 m²) |
|---|---|---|
| 1 (interior) | **+0,5 / −0,9** | +0,3 / −0,8 |
| 2 (bordes, cumbrera) | −1,7 | −1,2 |
| 3 (esquinas) | −2,6 | −2,0 |
| **Alero zona 2** | **−2,2** | −2,2 |
| **Alero zona 3** | **−3,7** | −2,5 |

**Cubierta plana o de poca pendiente θ ≤ 10° (Figura 5B):**

| Zona | GC_p (A ≈ 1 m²) | GC_p (A ≈ 50-100 m²) |
|---|---|---|
| 1 (interior) | +0,3 / −1,0 | +0,2 / −0,9 |
| 2 (bordes) | −1,8 | −1,1 |
| 3 (esquinas) | **−2,8** | −1,1 |
| Alero zona 2 | −1,7 | — |
| Alero zona 3 | −2,8 | — |

> **[VERIFICAR contra la lectura directa de las Figuras 5B y 5B (cont.) impresas.** Los valores de las curvas los extraje del PDF del reglamento y los verifiqué por consistencia con las etiquetas de los gráficos, pero son valores leídos de curvas, no de una tabla. Los valores de zona 1 y de alero son los que estoy más seguro; los de zonas 2 y 3 en pendientes intermedias hay que confirmarlos en el gráfico impreso antes de firmar.**

**[V] Nota 5 de la Figura 5B — una herramienta de proyecto que vale plata:**

> *"Si existe un **parapeto de altura igual o mayor que 1 m** alrededor del perímetro de una cubierta con pendiente θ ≤ 10°, **la Zona 3 se debe tratar como Zona 2**."*

**En una cubierta plana, un parapeto de 1,00 m elimina la zona de esquina.** El GC_p pasa de −2,8 a −1,8: **una reducción del 34 % en la presión de diseño de todo el perímetro.** Un antepecho de 1 m no es sólo estética: es economía estructural y es la diferencia entre una membrana que se despega y una que no.

**[V] Nota 6:** *"Los valores de GC_p para **aleros incluyen las contribuciones de las presiones de las superficies superior e inferior**."* → para el alero se usa `p = q_h · GC_p` **sin sumar GC_pi** (no hay interior debajo del alero).

**[V] Nota 5 de la Figura 5A (paredes):** *"Los valores de GC_p para paredes se deben reducir en un 10 % cuando θ ≤ 10°."*

### 7.4 Cubierta pesada vs. cubierta liviana en zona ventosa

| | **LIVIANA** (chapa sobre estructura de madera o steel) | **PESADA** (losa cerámica o de H°A° + teja) |
|---|---|---|
| Peso propio típico **[SUP]** | 0,25 – 0,45 kN/m² | 2,7 – 4,0 kN/m² |
| Succión de diseño (§8, exp. C, mayorada) | ≈ 1,5 kN/m² promedio, hasta 5,0 en esquina | idem |
| **Estabilidad global al vuelo** | **NO se estabiliza sola. Requiere anclaje calculado en toda la línea de apoyo.** | Se estabiliza con holgura (factor > 2,5) |
| Problema local | La chapa se desprende de la fijación (arranque por perforación de la arandela) | La teja se levanta individualmente; la losa no |
| Inercia térmica | Nula. Requiere masa interior (contrapiso, muros) para la ventilación nocturna (§10.3) | Alta. **Sinergia directa con la ventilación nocturna de verano de Santa Rosa** |
| Comportamiento con granizo (3 días/año) | Abolladura; con chapa fina, perforación | Rotura de tejas aisladas, reparable |
| Ruido con viento y lluvia | **Alto**. Con 156 días de viento fuerte es un problema de habitabilidad real | Nulo |
| Costo | Menor | Mayor (20-40 % del costo de la cubierta) |
| Riesgo de falla catastrófica | **Alto si el anclaje no está calculado** | Bajo |

> ### Criterio del estudio para Santa Rosa
> **Ambas son válidas; no son intercambiables sin cambiar el proyecto estructural.**
>
> - Si la cubierta es **pesada**, el viento deja de ser un problema global y queda como problema local (tejas, cumbrera, borde) + el problema de las carpinterías.
> - Si la cubierta es **liviana** (que suele ser la decisión económica correcta), **el anclaje deja de ser un detalle de obra y pasa a ser un cálculo estructural con números**, con una cadena de transmisión explícita: chapa → clavadera → cabio → viga/encadenado → muro → fundación. **Cada eslabón se dimensiona.** Ver §8.5.
> - **Híbrido recomendado y frecuente en Santa Rosa:** losa plana de H°A° (que resuelve masa térmica, ruido, estabilidad y aislación acústica) con cubierta liviana de chapa sobre ella para escurrimiento. La chapa se calcula como componente y revestimiento sobre un sustrato que ya es estable. Es la solución de menor riesgo.

### 7.5 Fijaciones de una cubierta de chapa

**El modo de falla de una cubierta de chapa NO es la rotura de la chapa ni el arrancamiento del tornillo: es la PERFORACIÓN DE LA CHAPA ALREDEDOR DE LA ARANDELA** (*pull-through*). La chapa se rasga en el agujero y se va, dejando los tornillos puestos.

**Reglas de fijación derivadas del cálculo (§8.7):**

| Zona | Separación de fijaciones | Justificación |
|---|---|---|
| **Zona 1** (interior del faldón) | 1 fijación cada 2-3 ondas (≈ 0,20-0,30 m) en cada clavadera | Demanda ≈ 0,7 kN por tornillo |
| **Zona 2** (bordes: alero, hastial, cumbrera — faja de 1 m) | **1 fijación en CADA onda** | Demanda ≈ 1,3 kN por tornillo con separación normal |
| **Zona 3** (esquinas — cuadrados de 1 × 1 m) | **1 fijación en cada onda + clavadera intermedia** | Demanda ≈ 1,8 kN por tornillo con separación normal — al límite |
| **Alero volado** | **1 fijación en cada onda + fleje continuo de borde** | Demanda ≈ 2,4 kN por tornillo. **Es el punto de mayor succión de toda la casa** |

**Reglas de obra:**
- **Fijar en la CRESTA de la onda, no en el valle** (el valle es donde corre el agua; la cresta trabaja mejor a arranque porque la chapa está apoyada, no en voladizo).
- Tornillos autoperforantes con **arandela metálica + EPDM**. La arandela metálica es la que reparte la carga y evita el *pull-through*. Sin arandela metálica el número de arriba no se cumple.
- **No sobre-apretar**: la arandela deformada pierde capacidad y estanqueidad.
- **La cumbrera y las cenefas de borde son lo primero que se va.** Solapes generosos, fijación en cada onda, y babeta/fleje de borde continuo mecánicamente fijado al alero, no sólo pegado.
- **[VERIFICAR con el fabricante]** la capacidad de arranque por perforación (*pull-through*) de la chapa especificada, para el espesor y el tipo de arandela. Es el dato que gobierna y ningún catálogo argentino lo da por defecto: hay que pedirlo.

### 7.6 Aleros y voladizos: dónde arranca la falla

**El alero es simultáneamente el punto de mayor succión de la casa y el elemento peor anclado.** Recibe presión negativa arriba (flujo separado) **y** presión positiva abajo (el viento se mete debajo y empuja hacia arriba). Por eso los GC_p de alero (−2,2 y −3,7) son mucho mayores que los del faldón (−1,7 y −2,6): **el reglamento ya combinó las dos caras.**

| Decisión | Efecto sobre el viento | Efecto sobre el sol |
|---|---|---|
| **Sin alero** | El mejor comportamiento a viento | Pierde la protección solar del muro N y la protección de la lluvia sobre la carpintería |
| **Alero de 0,40-0,60 m** | Manejable con anclaje correcto | **Insuficiente para sombrear la ventana N en verano** (con altura solar 77°, un alero de 0,60 m sombrea 2,6 m de altura de muro — en realidad suficiente) |
| **Alero de 0,80-1,20 m** | Requiere anclaje explícito del voladizo; el fleje de borde es estructural | Buen control solar, protege carpinterías de la lluvia |
| **Alero corrido en el frente NORTE** | Es el frente de mayor incidencia (34 % del tiempo). Hay que anclarlo de verdad | Es donde más sirve |

**Detalle constructivo obligatorio:**
- **Cerrar el sofito del alero (tapajuntas continuo).** Un alero con el sofito abierto deja que el viento se meta en la cámara del techo y presurice desde adentro. Es el mecanismo por el que se levantan techos enteros desde el alero.
- **El alero no puede ser un voladizo de la chapa.** El cabio tiene que volar, no la chapa.
- **Anclar el voladizo a tracción**: el momento de la succión del alero se transmite al apoyo como una tracción en la fibra superior del cabio y una compresión abajo, invirtiendo el esfuerzo respecto del peso propio. La clavija/fleje del apoyo trabaja al revés de lo que sugiere la intuición.

### 7.7 El caso de la cubierta plana o de poca pendiente

Frecuente en la casa contemporánea. Consideraciones específicas:

- **[V] Método 1 (simplificado) del CIRSOC 102-2005 sólo es aplicable si la pendiente < 10° y h ≤ 10 m** (art. 4.1). Una casa de losa plana **sí** califica; una casa de dos aguas a 20° **no**.
- **[V] En CIRSOC 102-25 el método simplificado se restringió a pendientes de hasta 7°** para mantener consistencia con las nuevas figuras de coeficientes.
- La **zona 3 con GC_p = −2,8** es brutal, pero **el parapeto de 1 m la elimina** (§7.3). Aprovecharlo.
- **La membrana asfáltica pegada no resiste succión por adherencia**: en el perímetro hay que **fijarla mecánicamente** con perfil de borde y luego sellar. La membrana suelta que se ve flamear en una tormenta ya está perdida.
- **Losa de H°A° con membrana + protección**: el peso resuelve todo. **Grava suelta como protección: prohibida en Santa Rosa** — con 156 días de viento fuerte la grava se vuela y se convierte en proyectil (y como la casa es baja, contra los vidrios propios y del vecino). Usar baldosas fijadas o membrana con terminación autoprotegida.
- **Equipos en cubierta plana** (unidades exteriores de aire, termotanques solares, tanque de agua): **son estructuras sobre azoteas** y tienen su propio capítulo (Cap. 4 en 102-25). Se anclan, no se apoyan.

---

## 8. Cálculo resuelto: casa tipo 10 × 12 m en Santa Rosa

### 8.1 Geometría, hipótesis y parámetros

**Geometría [SUP] — casa de referencia del estudio:**

| Parámetro | Valor |
|---|---|
| Planta | **10,00 m × 12,00 m** (120 m²), rectangular, regular |
| Cumbrera | Paralela al lado de 12 m (luz de la cubierta: 10 m) |
| Altura de alero | **2,70 m** |
| Pendiente de cubierta θ | **20°** |
| Flecha de cubierta | 5,00 × tan 20° = 5,00 × 0,36397 = **1,82 m** |
| Altura de cumbrera | 2,70 + 1,82 = **4,52 m** |
| **Altura media de cubierta h** | (2,70 + 4,52)/2 = **3,61 m** |
| Longitud de faldón | 5,00 / cos 20° = 5,00 / 0,93969 = **5,32 m** |
| Superficie de cubierta (sin aleros) | 2 × 5,32 × 12,00 = **127,7 m²** |
| Aleros | 0,60 m en los cuatro lados |
| Cerramiento | **Cerrado** (GC_pi = ±0,18) — se verifica el caso "parcialmente cerrado" en §8.9 |
| Sistema | Muros portantes de mampostería + encadenado + estructura de cubierta liviana |

**Verificación de aplicabilidad de método:**

| Método | ¿Aplica? | Por qué |
|---|---|---|
| Método 1 — Simplificado (Cap. 4) | **NO** | [V] art. 4.1.2: "la pendiente de la cubierta del edificio es **menor que 10°**". Con θ = 20° queda fuera |
| Método 2 — Analítico, **edificios de baja altura (Figura 4)** | **SÍ** | [V] Definición Cap. 2: h ≤ 20 m **y** h ≤ menor dimensión horizontal. h = 3,61 ≤ 10 ✓ |
| Método 2 — Todas las alturas (Figura 3) | Aplicable pero innecesario | Más trabajo, resultado similar |

**→ Se usa el Método 2 con la Figura 4 (GC_pf) para el SPRFV y la Figura 5A/5B (GC_p) para componentes y revestimientos.**

**Parámetros de viento (CIRSOC 102-2005):**

| Parámetro | Valor | Fuente |
|---|---|---|
| V | **50,0 m/s** | [V] Fig. 1B — Santa Rosa |
| I | **1,00** | [V] Tabla 1 — Categoría II (vivienda) |
| K_d | **0,85** | [V] Tabla 6 — edificios, SPRFV y C&R |
| K_zt | **1,00** | Terreno plano |
| **K_h (exposición B)** | **0,72** | [V] Tabla 5, **Caso 1** (SPRFV de edificio de baja altura con Fig. 4, y todos los C&R), z ≤ 5 m. La observación de la nota 2 fija que en exposición B, Caso 1, no se tome z < 10 m; a 10 m también vale 0,72 |
| **K_h (exposición C)** | **0,87** | [V] Tabla 5, Caso 1, z ≤ 5 m (h = 3,61 m < 5 m) |
| GC_pi | **±0,18** | [V] Tabla 7 — edificio cerrado |
| **a** (dimensión de zona) | **1,00 m** | min(0,10 × 10 ; 0,40 × 3,61) = min(1,00 ; 1,44) = 1,00; ≥ max(0,04 × 10 ; 1,00) = 1,00 ✓ |
| 2a | **2,00 m** | Ancho de las zonas de extremo (E) |

### 8.2 Presión dinámica q_h

```
q_h = 0,613 · K_h · K_zt · K_d · V² · I         [N/m²]
```

**Exposición B:**
```
q_h = 0,613 × 0,72 × 1,00 × 0,85 × 50² × 1,00
    = 0,613 × 0,72 = 0,44136
    × 0,85 = 0,375156
    × 2500 = 937,9  →  q_h = 938 N/m² = 0,94 kN/m²
```

**Exposición C:**
```
q_h = 0,613 × 0,87 × 1,00 × 0,85 × 2500 × 1,00
    = 0,613 × 0,87 = 0,53331
    × 0,85 = 0,4533135
    × 2500 = 1133,3  →  q_h = 1133 N/m² = 1,13 kN/m²
```

**Relación C/B = 1133/938 = 1,208** → pasar de exposición B a C **aumenta todas las presiones un 21 %**.

> Nota de coherencia: el multiplicador 1,40 de las Tablas 2 y 3 (método simplificado) corresponde a otra base — esas tablas están construidas a h = 10 m, donde K_z(B) = 0,72 y K_z(C) = 1,00 → 1,39 ≈ 1,40. [V, confirmado en el Comentario del 102-25: "Se han utilizado los siguientes valores en la preparación de las Tablas: h = 10 m, Exposición B, Kz = 0,71"]. **Los dos números son correctos en su propio método. No mezclar.**

### 8.3 Presiones de diseño sobre el SPRFV — Figura 4, Caso A (viento normal a la cumbrera)

```
p = q_h · [ GC_pf − (GC_pi) ]
```

**Coeficientes para θ = 20°, Caso A [V]:** 1 = +0,53 | 2 = −0,69 | 3 = −0,48 | 4 = −0,43 | 1E = +0,80 | 2E = −1,07 | 3E = −0,69 | 4E = −0,64

**Presiones netas (N/m²), exposición B (q_h = 938) y exposición C (q_h = 1133):**

| Superficie | GC_pf | GC_pi crítico | (GC_pf − GC_pi) | **p exp. B** | **p exp. C** |
|---|---|---|---|---|---|
| **1** Pared barlovento (máx. hacia adentro) | +0,53 | −0,18 | +0,71 | **+666** | **+804** |
| **1E** Pared barlovento, extremo | +0,80 | −0,18 | +0,98 | **+919** | **+1.110** |
| **2** Cubierta barlovento (máx. succión) | −0,69 | +0,18 | −0,87 | **−816** | **−986** |
| **2E** Cubierta barlovento, extremo | −1,07 | +0,18 | −1,25 | **−1.173** | **−1.417** |
| **3** Cubierta sotavento | −0,48 | +0,18 | −0,66 | **−619** | **−748** |
| **3E** Cubierta sotavento, extremo | −0,69 | +0,18 | −0,87 | **−816** | **−986** |
| **4** Pared sotavento (succión) | −0,43 | +0,18 | −0,61 | **−572** | **−691** |
| **4E** Pared sotavento, extremo | −0,64 | +0,18 | −0,82 | **−769** | **−929** |

*(Signo + = hacia la superficie; − = alejándose de la superficie. Son valores **nominales** de servicio; para resistencia hay que mayorar por 1,6.)*

### 8.4 SUCCIÓN TOTAL SOBRE LA CUBIERTA vs. PESO PROPIO

**Áreas en proyección horizontal** (el componente vertical de una presión normal al faldón sobre el área del faldón equivale a la presión por el área proyectada):

| Zona | Extensión | Área proyectada |
|---|---|---|
| 2E | 5,00 m (semiluz) × 2,00 m (2a) | 10,0 m² |
| 2 | 5,00 × 10,00 | 50,0 m² |
| 3E | 5,00 × 2,00 | 10,0 m² |
| 3 | 5,00 × 10,00 | 50,0 m² |
| **Total** | | **120,0 m²** |

*(Verificación de la nota 4a: el GC_pf negativo de zona 2 se extiende desde el alero una distancia de min(0,5 × 10 ; 2,5 × 3,61) = min(5,00 ; 9,03) = 5,00 m = todo el faldón. No hay que subdividir.)*

**FUERZA VERTICAL ASCENDENTE TOTAL SOBRE LA CUBIERTA:**

**Exposición B:**
```
F↑ = 1.173 × 10,0  +  816 × 50,0  +  816 × 10,0  +  619 × 50,0
   =    11.730     +    40.800    +     8.160    +   30.950
   = 91.640 N  =  91,6 kN     (nominal, sin mayorar)
```

**Exposición C:**  F↑ = 91,6 × 1,208 = **110,7 kN**

**Succión media sobre la planta:** 91,6 kN / 120 m² = **0,76 kN/m²** (exp. B) — **0,92 kN/m²** (exp. C).

**PESO PROPIO DE LA CUBIERTA [SUP] — hipótesis del estudio, a ajustar con el cómputo real:**

| Solución | Composición | Peso (kN/m² sobre faldón) | Peso total (127,7 m²) |
|---|---|---|---|
| **A — Chapa, sin cielorraso suspendido** | Chapa C25 (0,05) + clavaderas y cabios de madera (0,15) + aislación lana de vidrio 100 mm (0,03) | **0,23** | **29,4 kN** |
| **B — Chapa con cielorraso de placa de yeso colgado** | A + perfilería y placa 12,5 mm (0,15) | **0,38** | **48,5 kN** |
| **C — Losa cerámica inclinada + teja** | Viguetas + ladrillo hueco + capa de compresión (2,3) + carpeta (0,4) + teja cerámica (0,5) | **3,20** | **408,6 kN** |
| **D — Losa H°A° 12 cm + contrapiso + teja** | 0,12 × 25 (3,0) + contrapiso/carpeta (0,5) + teja (0,5) | **4,00** | **510,8 kN** |

**COMBINACIÓN CRÍTICA — CIRSOC 201-2005, combinación (6): `0,9 D + 1,6 W`** [V, ver `estructuras.md` §2.2]

| Cubierta | Exposición | `0,9 D` (kN) | `1,6 W↑` (kN) | **Resultado** |
|---|---|---|---|---|
| **A** chapa sin cielorraso | B | 26,5 | 146,6 | **VUELA. Tracción neta 120,1 kN** |
| **A** | **C** | 26,5 | **177,1** | **VUELA. Tracción neta 150,6 kN** |
| **B** chapa con cielorraso | B | 43,7 | 146,6 | **VUELA. Tracción neta 102,9 kN** |
| **B** | **C** | 43,7 | **177,1** | **VUELA. Tracción neta 133,4 kN** |
| **C** losa cerámica | C | 367,7 | 177,1 | ✓ Estable. Margen 190,6 kN (factor 2,08) |
| **D** losa H°A° | C | 459,7 | 177,1 | ✓ Estable. Margen 282,6 kN (factor 2,60) |

> ### 🔑 RESULTADO CENTRAL DEL CÁLCULO
> **Una cubierta liviana de chapa en Santa Rosa recibe una succión mayorada 4 a 6 veces mayor que su peso estabilizante. El anclaje NO es opcional, NO es un detalle de obra y NO se resuelve "con unos tacos".**
>
> **Una cubierta pesada (losa) se estabiliza sola con un factor de seguridad global de 2 a 2,6**, y el problema queda reducido a los elementos locales (tejas, cumbrera, borde).

### 8.5 Anclaje: cuánto, dónde y cómo

**Distribución del anclaje.** La cubierta a dos aguas apoya en los **dos muros de alero de 12 m** → **24 m lineales de línea de apoyo**.

**Cubierta B (chapa con cielorraso, 0,38 kN/m²), exposición C:**

Reparto a lo largo de los 12 m de cumbrera: **10 m con coeficientes de zona interior + 2 m con coeficientes de zona de extremo (E)**, en el extremo de barlovento. Como la hipótesis se rota 90° cuatro veces (nota 2 de la Fig. 4), **los 2 m de extremo se dan en las dos puntas de los dos aleros**: hay que anclar reforzado en las **cuatro esquinas**.

| Zona a lo largo de la cumbrera | Succión mayorada `1,6 W↑` por metro de alero | Peso estabilizante `0,9 D` | **Tracción neta de diseño** |
|---|---|---|---|
| **Zona interior** (10 m centrales) | 6,94 kN/m | 1,82 kN/m | **≈ 5,1 kN/m** |
| **Zonas de extremo** (2 m en cada esquina) | 9,61 kN/m | 1,82 kN/m | **≈ 7,8 kN/m** |

*Verificación del cálculo (exp. C, q_h = 1.133 N/m²):*
```
Zona interior, por metro de cumbrera:
  F↑ = 986 N/m² × 5,00 m  +  748 N/m² × 5,00 m  =  8.670 N/m
  repartido en los dos aleros:  4.335 N/m por alero
  × 1,6 = 6.936 N/m
  Peso: 0,38 kN/m² × 10,64 m = 4,04 kN/m ; por alero 2,02 ; × 0,9 = 1,82 kN/m
  TRACCIÓN NETA = 6,94 − 1,82 = 5,12 kN/m

Zona de extremo, por metro de cumbrera:
  F↑ = 1.417 × 5,00 + 986 × 5,00 = 12.015 N/m ; por alero 6.008 N/m ; × 1,6 = 9,61 kN/m
  TRACCIÓN NETA = 9,61 − 1,82 = 7,79 kN/m

Comprobación contra el total del §8.4:
  5,12 × 10 m × 2 aleros  +  7,79 × 2 m × 2 aleros  =  102,4 + 31,2 = 133,6 kN  ✓
  (§8.4 daba 133,4 kN de tracción neta para la cubierta B en exposición C)
```

**→ Demanda de anclaje: 5,1 kN/m en zona interior, 7,8 kN/m en los 2 m de cada esquina (+53 %).**

**Traducción a obra, con cabios cada 0,60 m:**

| | Zona interior | Zonas de extremo (2 m en las 4 esquinas) |
|---|---|---|
| Tracción por cabio | **≈ 3,1 kN (310 kgf)** | **≈ 4,7 kN (470 kgf)** |
| Solución | 1 fleje/zuncho metálico por cabio, anclado al encadenado | **2 flejes por cabio o fleje reforzado**, anclado al encadenado, más 1 barra roscada Ø10 pasante cada 1,2 m |

**Cadena de transmisión que hay que dibujar y verificar eslabón por eslabón:**

```
chapa
  ↓ tornillo autoperforante c/arandela metálica + EPDM  ← §7.5 (pull-through)
clavadera
  ↓ tornillo o clavo helicoidal (NO clavo liso)
cabio / cercha
  ↓ FLEJE / ZUNCHO METÁLICO — este es el eslabón que falta en el 90 % de las obras
viga de borde o solera
  ↓ barra roscada / anclaje químico al encadenado de H°A°
ENCADENADO SUPERIOR DE H°A° (continuo, sin interrupciones)
  ↓ armadura vertical de los muros / el propio peso de la mampostería
muro portante
  ↓
cimiento
```

**Puntos donde falla en la realidad:**
1. **El fleje no existe** — el cabio simplemente apoya sobre la solera. Falla instantánea.
2. **El encadenado está interrumpido** en el dintel de una abertura grande o en un encuentro. El anclaje ancla a nada.
3. **El clavo es liso.** Un clavo liso a extracción tiene una capacidad ridícula. **Clavo helicoidal o tornillo, siempre.**
4. **El anclaje al encadenado se hace con taco de expansión en hormigón fresco o mal ejecutado.** Anclaje químico o barra embebida en el hormigonado.
5. **Los 2 m de los extremos se tratan igual que el centro.** Es exactamente donde la demanda es 60 % mayor.

**Verificación de vuelco/deslizamiento global de la casa:** no gobierna. Peso de la superestructura **[SUP]**: muros perimetrales 44 m × 2,70 m × ≈ 2,7 kN/m² ≈ 321 kN, + tabiques interiores ≈ 60 kN, + cubierta 48,5 kN ≈ **430 kN**. Momento de vuelco (§8.6) ≈ 50,5 × 3 = 152 kNm contra un momento estabilizante ≈ 430 × 5 = 2.150 kNm → **factor 14**. **La casa no se vuelca. La casa se destecha.**

### 8.6 Corte horizontal — y por qué la nota 4b gobierna

**Viento normal a la cumbrera (Caso A), sobre la fachada de 12 m:**

Cálculo directo con coeficientes de la Figura 4, aplicando cada GC_pf a la superficie **proyectada verticalmente**:

| Contribución | Coeficiente × altura proyectada | Sentido |
|---|---|---|
| Pared barlovento | +0,53 × 2,70 = 1,431 | + |
| Pared sotavento | +0,43 × 2,70 = 1,161 | + |
| Faldón barlovento (succión, normal apuntando a barlovento) | −0,69 × 1,82 = −1,256 | **−** |
| Faldón sotavento (succión, normal apuntando a sotavento) | +0,48 × 1,82 = 0,874 | + |
| **Suma** | **2,210** | |

Corte incluyendo la cubierta (exp. B) = 938 × 2,210 × 12 = **24,9 kN**.

**Pero [V] nota 4b de la Figura 4:** *"el corte horizontal total no debe ser menor que el determinado al **despreciar las fuerzas del viento sobre las superficies de la cubierta**"*:

| | Coeficiente × altura |
|---|---|
| Pared barlovento zona 1 | 0,53 × 2,70 = 1,431 |
| Pared sotavento zona 4 | 0,43 × 2,70 = 1,161 |
| **Suma (zonas interiores)** | **2,592** |
| Zonas de extremo 1E + 4E | (0,80 + 0,64) × 2,70 = 3,888 |

```
V = q_h · [ 2,592 × 10 m  +  3,888 × 2 m ]
  = 938 × [ 25,92 + 7,776 ] = 938 × 33,70 = 31.610 N  ≈ 31,6 kN   (exp. B, nominal)
```

**El valor con cubierta (24,9 kN) es 21 % MENOR. Gobierna la nota 4b: V = 31,6 kN.**

| | Exposición B | Exposición C |
|---|---|---|
| Corte nominal, viento ⊥ cumbrera | 31,6 kN | 38,2 kN |
| **Corte mayorado (1,6 W)** | **50,6 kN** | **61,1 kN** |
| Corte nominal, viento ∥ cumbrera (Caso B) | 25,7 kN | 31,1 kN |
| **Corte mayorado** | **41,2 kN** | **49,7 kN** |

**Consecuencia de proyecto:** 61 kN es el corte que debe tomar el conjunto de muros transversales. Con muros de mampostería es trivial **siempre que haya muros transversales continuos y encadenados**. **Deja de ser trivial si la fachada norte es todo vidrio.** Una casa con el frente N enteramente abierto tiene que resolver la rigidez lateral en esa dirección con pórticos o tabiques, y hay que dibujarlo.

### 8.7 Componentes y revestimientos — Figura 5B (10° < θ ≤ 30°)

```
p = q_h · [ GC_p − (GC_pi) ]       (cubierta y paredes)
p = q_h · GC_p                     (aleros — el GC_p ya incluye ambas caras)
```

**Presiones de succión, área efectiva ≈ 1 m² (el caso de una chapa entre clavaderas o un tramo de teja):**

| Zona | GC_p | **Exp. B nominal** | **Exp. C nominal** | **Exp. C mayorada (×1,6)** | En kgf/m² |
|---|---|---|---|---|---|
| **1** Interior del faldón | −0,9 | −1.013 N/m² | −1.224 N/m² | **−1.958 N/m²** | 200 |
| **2** Bordes y cumbrera | −1,7 | −1.763 | −2.130 | **−3.408** | 348 |
| **3** Esquinas | −2,6 | −2.608 | −3.151 | **−5.042** | **514** |
| **Alero zona 2** | −2,2 | −2.064 | −2.493 | **−3.989** | 407 |
| **Alero zona 3** | **−3,7** | −3.471 | −4.192 | **−6.707** | **684** |

> **684 kgf/m² de succión en la esquina de un alero. La chapa C25 pesa 5 kgf/m². Relación 137 : 1.**

**Verificación de las fijaciones — chapa sinusoidal, onda de 100 mm, clavaderas cada 1,20 m:**

| Esquema de fijación | Área tributaria por tornillo | **Zona 1** | **Zona 3** | **Alero zona 3** |
|---|---|---|---|---|
| 1 tornillo cada 3 ondas (0,30 m) | 0,36 m² | 705 N | **1.815 N** | **2.415 N** |
| 1 tornillo cada 2 ondas (0,20 m) | 0,24 m² | 470 N | 1.210 N | 1.610 N |
| **1 tornillo en cada onda (0,10 m)** | **0,12 m²** | 235 N | **605 N** | **805 N** |

**[VERIFICAR con el fabricante de la chapa]** la resistencia característica al **arranque por perforación** (*pull-through*) para el espesor especificado y el diámetro de arandela. Orden de magnitud típico para chapa de 0,5 mm con arandela de 19 mm: **1,5 a 2,5 kN**, sin coeficiente de minoración.

**Conclusión operativa:** con separación normal (cada 3 ondas), **las zonas de esquina y alero quedan al límite o por encima de la capacidad de la fijación**. Con fijación en cada onda quedan holgadas. **Por eso la regla del §7.5: fijación en cada onda en zonas 2, 3 y aleros.** Cuesta unos pesos en tornillos y evita la falla.

**Paredes (Figura 5A), área efectiva ≈ 5 m² (una ventana o un portón):**

| Zona | GC_p [VERIFICAR lectura de la Fig. 5A] | Exp. C mayorada |
|---|---|---|
| **4** Interior de pared | ≈ +0,9 / −1,0 | +1,96 / −2,14 kN/m² |
| **5** Bordes de pared (faja de 1 m en las esquinas) | ≈ +0,9 / −1,2 | +1,96 / −2,50 kN/m² |

### 8.8 Verificación cruzada con CIRSOC 102-25

Mismo edificio, edición 2025, exposición B, categoría de riesgo II:

| Parámetro | Valor | Fuente |
|---|---|---|
| V | **61,2 m/s** | [V] Comentario C 1.5, Santa Rosa, Cat. II |
| K_h | **0,72** | [V] El Comentario C 1.13 aclara que los valores de K_z se mantuvieron sin cambios donde diferían menos de 0,01, y que eso cubre **"alturas de hasta 9 m en exposición B, 37 m en exposición C"**. Nuestro h = 3,61 m entra de lleno |
| K_d | 0,85 | [V] Tabla 1.6-1 |
| K_zt | 1,00 | — |
| **K_e** | **0,978** | [V] Tabla 1.12-1, K_e = e^(−0,000119 × 190) |
| Factor de importancia | **no existe** (incorporado en V) | [V] |

```
q_h = 0,613 × 0,72 × 1,00 × 0,85 × 0,978 × 61,2²
    = 0,375156 × 0,978 = 0,366903
    × 3.745,44 = 1.374,3  →  q_h = 1.374 N/m²
```

**Comparación de la presión de diseño MAYORADA:**

| Edición | q_h (N/m²) | Factor de carga | **Presión mayorada de referencia** |
|---|---|---|---|
| **CIRSOC 102-2005** | 938 | **1,6 W** | **1.501 N/m²** |
| **CIRSOC 102-25** | 1.374 | **1,0 W** | **1.374 N/m²** |
| | | | **Relación: 0,915 → la edición 2025 da un 8,5 % MENOS** |

Coincide con el cálculo analítico del §2.3: `1,5 × K_e / 1,6 = 1,5 × 0,978 / 1,6 = 0,917`.

> **Verificado: en Santa Rosa, la edición 2025 no encarece la estructura. La abarata marginalmente.** Y si se toma K_e = 1,00 (permitido), la relación es 0,938 — todavía favorable.
>
> **Lo que sí cambia y hay que revisar:** los coeficientes de presión de las figuras del 102-25 **no son los mismos** que los de la Fig. 4 y 5B de 2005 (el propio Comentario lo dice: *"las figuras de donde se extraen los coeficientes de carga... son diferentes en esta revisión"*). **La comparación de q_h de arriba es válida; la comparación de las presiones finales requiere rehacer el cálculo con las figuras nuevas.** **[VERIFICAR: rehacer §8.3 a §8.7 con las Figuras 2.4-x y 5.3-x del CIRSOC 102-25 antes de presentar el cálculo para visado bajo esa edición.]**

### 8.9 El efecto del portón de garaje que se rompe

Escenario: el portón de garaje (2,50 × 2,20 m = 5,5 m²) cede en una tormenta con viento de frente. La casa pasa de **cerrada** a **parcialmente cerrada**: GC_pi de ±0,18 a ±0,55.

**Verificación del criterio [V, Tabla 1.11-1 del 102-25]:** A₀ = 5,5 m² > 0,4 m² ✓, y es dominante frente a las demás aberturas ✓ → **parcialmente cerrado**.

**Recálculo de la succión total en la cubierta (exp. B):**

| Zona | (GC_pf − 0,55) | p (N/m²) | Área proy. | F↑ |
|---|---|---|---|---|
| 2E | −1,62 | −1.520 | 10 m² | 15.200 N |
| 2 | −1,24 | −1.163 | 50 m² | 58.150 N |
| 3E | −1,24 | −1.163 | 10 m² | 11.630 N |
| 3 | −1,03 | −966 | 50 m² | 48.300 N |
| **Total** | | | | **133.280 N = 133,3 kN** |

| | Cerrado | **Parcialmente cerrado** | Aumento |
|---|---|---|---|
| Succión total, exp. B | 91,6 kN | **133,3 kN** | **+45 %** |
| Succión total, exp. C | 110,7 kN | **161,0 kN** | **+45 %** |

> ### 🔑 **El portón de garaje que se rompe aumenta la succión sobre TODO el techo un 45 %.**
> No es que "entra viento por el garaje". Es que **la casa se presuriza y el techo se levanta desde adentro**, sumando la presión interna a la succión externa. Este es el mecanismo real por el que se pierden techos en la Pampa: no falla el techo, falla una abertura, y después falla el techo.
>
> **Decisiones de proyecto que se derivan:**
> 1. **El portón de garaje y las aberturas grandes son elementos ESTRUCTURALES.** Especificar resistencia a carga de viento, no sólo dimensión y color. Ver §8.7: el portón de 5,5 m² recibe ≈ **12 kN** mayorados.
> 2. **Si el garaje está en el frente NORTE** (el sector dominante, 34 % del tiempo), el problema se agrava.
> 3. **Alternativa de proyecto:** separar el garaje del volumen habitable, o **ventilarlo permanentemente** de modo que no pueda presurizar la casa (un garaje intencionalmente permeable no genera presión interna sobre la vivienda), con una puerta interior estanca entre garaje y casa.
> 4. **Alternativa de cálculo:** si el proyecto tiene aberturas grandes en una sola fachada y no se puede garantizar su integridad, **calcular directamente como parcialmente cerrado** y anclar para 133 kN en vez de 91,6 kN. El sobrecosto es de flejes; el ahorro es un techo.

---

## 9. Elementos que fallan primero

Ordenados por frecuencia real de falla, de mayor a menor.

### 9.1 Portones y puertas de garaje
Ya tratado en §8.9. **Es el elemento nº 1.** Resumen: falla → GC_pi ±0,18 → ±0,55 → succión de cubierta +45 % → se pierde el techo. Demanda sobre el portón mismo: **≈ 12 kN mayorados** en un portón de 5,5 m². Especificar clasificación de resistencia a viento, refuerzos y guías ancladas al muro (no al marco de chapa).

### 9.2 Aleros y voladizos
Ya tratado en §7.6. **Es el elemento nº 2.** Succión mayorada en la esquina de alero: **6,7 kN/m² (684 kgf/m²)** en exposición C. Sobre un alero de 0,60 m eso es **4,0 kN por metro lineal de alero** intentando arrancarlo. Sofito cerrado, cabio volado (no chapa volada), fleje continuo de borde fijado mecánicamente.

### 9.3 Galerías, pérgolas y parasoles — el Anexo I del CIRSOC 102
**Una galería con techo independiente NO es parte de la casa: es una "cubierta aislada" y tiene su propio anexo, con coeficientes mucho más severos.**

**[V] CIRSOC 102-2005, Anexo I:** `p = q_h · G · C_pn`, con **G = 0,85** y C_pn de las Tablas I.1 (vertiente única) e I.2 (dos aguas), que **contemplan el efecto combinado del viento sobre la superficie superior y la inferior, para todas las direcciones de viento**.

**[V] Tabla I.1 — cubierta aislada de vertiente única, ζ = 0 (sin obstrucciones debajo):**

| θ | Coef. **global** máx / mín | Local **A** | Local **B** | Local **C** |
|---|---|---|---|---|
| 0° | +0,2 / −0,5 | +0,5 / −0,6 | +1,8 / −1,3 | +1,1 / −1,4 |
| 5° | +0,4 / −0,7 | +0,8 / −1,1 | +2,1 / −1,7 | +1,3 / −1,8 |
| **10°** | **+0,5 / −0,9** | **+1,2 / −1,5** | **+2,4 / −2,0** | **+1,6 / −2,1** |
| 15° | +0,7 / −1,1 | +1,4 / −1,8 | +2,7 / −2,4 | +1,8 / −2,5 |
| 20° | +0,8 / −1,3 | +1,7 / −2,2 | +2,9 / −2,8 | +2,1 / −2,9 |
| 30° | +1,2 / −1,8 | +2,2 / −3,0 | +3,2 / −3,8 | +2,4 / −3,6 |

**[V] Otras disposiciones del Anexo I que valen oro para una galería:**
- **ζ (relación de bloqueo)** = altura de las obstrucciones bajo la cubierta / altura del alero a sotavento. ζ = 0 sin obstrucciones, ζ = 1 totalmente bloqueada. **Cerrar el fondo de una galería con un muro cambia radicalmente los coeficientes.** Se interpola.
- **[V] Cenefas y tímpanos:** *"habrá cargas horizontales sobre la misma debidas a las presiones de viento actuando sobre cualquier cenefa en los aleros... usando un coeficiente de presión neta de **C_pn = 1,3 sobre las cenefas y/o tímpanos a barlovento y C_pn = 0,6** sobre los de sotavento."* → **la cenefa/canaleta frontal de una galería es de los primeros elementos en irse.**
- Coeficientes **globales** para dimensionar las columnas y las vigas; **locales** (A, B, C, en las fajas de borde) para dimensionar la cubierta y las fijaciones.
- Se debe verificar además **un faldón cargado y el otro descargado** en cubiertas a dos aguas — hipótesis antimétrica que carga las columnas de un solo lado.

**Ejemplo de dimensionado — galería independiente de 3,00 × 6,00 m, vertiente única a 10°, ζ = 0, exposición C (q_h = 1.133 N/m²):**

```
Global (mínimo):   p = 1.133 × 0,85 × (−0,9) = −867 N/m²
F↑ total = 867 × 18 m² = 15,6 kN  (nominal)  →  ×1,6 = 25,0 kN mayorados
Peso propio [SUP] chapa + estructura ≈ 0,30 kN/m² × 18 = 5,4 kN  →  ×0,9 = 4,9 kN
TRACCIÓN NETA = 25,0 − 4,9 = 20,1 kN,  repartida en 6 columnas = 3,4 kN por columna
```

> ### 🔑 **Las columnas de una galería trabajan a TRACCIÓN. No se apoyan: se anclan.**
> 3,4 kN de tracción por columna. Una columna de perfil tubular simplemente apoyada sobre una base de hormigón se levanta. Hace falta **placa de base con pernos de anclaje calculados** y un dado de fundación cuyo **peso** (no su capacidad portante) equilibre la tracción: 3,4 kN / 24 kN/m³ = **0,14 m³ de hormigón por columna como mínimo**, más coeficiente. Un dado de 0,50 × 0,50 × 0,70 m.
>
> Y localmente: p = 1.133 × 0,85 × (−2,1) = **−2.023 N/m²** en la faja de borde C, mayorado **3,2 kN/m²**. Fijaciones en cada onda en todo el perímetro de la galería.

**Pérgolas y parasoles (estructuras abiertas, sin cubierta continua):** se calculan con la **Tabla 12** del 102-2005, coeficientes de fuerza C_f según la relación de área sólida ε = A_f/A_total:

| ε (área sólida / área total) | C_f elementos de caras planas |
|---|---|
| < 0,1 | **2,0** |
| 0,1 a 0,29 | 1,8 |
| 0,3 a 0,7 | 1,6 |

**Contraintuitivo pero verificado:** una pérgola **muy calada** (ε < 0,1) tiene el **mayor** coeficiente de fuerza (2,0) porque cada listón trabaja aislado con su propia estela. La fuerza total es menor porque el área sólida es menor, pero **cada listón individual y su fijación reciben más**. Los listones sueltos de una pérgola se van de a uno.

### 9.4 Medianeras y cercos altos — cálculo resuelto
**Es la falla más visible y más frecuente después de cada tormenta en Santa Rosa.**

**[V] CIRSOC 102-2005, Tabla 11 — paredes libres llenas y carteles llenos:**

| ν = altura/ancho (a nivel del terreno) | C_f |
|---|---|
| ≤ 3 | **1,2** |
| 5 | 1,3 |
| 10 | 1,5 |
| 20 | 1,75 |
| ≥ 40 | 2,0 |

**[V] Nota 2:** *"Los carteles con aberturas que abarquen menos del 30 % del área total se deben considerar como carteles llenos."* → **una medianera con menos de 30 % de vacíos calcula como maciza.** Otro argumento a favor de la celosía: por encima del 30 % de vacíos, cambia el método de cálculo (Tabla 12).

**Cálculo — medianera de mampostería de 2,20 m de altura, 20 m de largo, exposición C:**

```
ν = 2,20 / 20 = 0,11 ≤ 3          →  C_f = 1,2
K_z (Tabla 5, CASO 2 — "otras estructuras", z ≤ 5 m, exp. C) = 0,87
K_d (carteles llenos) = 0,85
q_z = 0,613 × 0,87 × 1,00 × 0,85 × 2500 × 1,00 = 1.133 N/m²
p   = q_z · G · C_f = 1.133 × 0,85 × 1,2 = 1.156 N/m²   (nominal)
p_u = 1,6 × 1.156 = 1.850 N/m²                          (mayorada)
```

**Momento de vuelco en la base, por metro lineal de muro (si el muro es un voladizo puro):**
```
M = 1.850 × 2,20² / 2 = 1.850 × 2,42 = 4.477 Nm/m  ≈  4,5 kNm/m
```

**Momento estabilizante del peso propio** (muro de 0,20 m, ≈ 2,5 kN/m²):
```
W = 2,5 × 2,20 = 5,5 kN/m ;  brazo = 0,20/2 = 0,10 m  →  M_est = 0,55 kNm/m
```

> ### 🔑 **4,5 kNm/m de demanda contra 0,55 kNm/m de capacidad por peso propio. Factor 8 en contra.**
> **Una medianera de 2,20 m de mampostería sin pilastras y sin fundación adecuada se cae. No "puede caerse": se cae.** Y es una de las causas más frecuentes de daño a terceros después de una tormenta en La Pampa.
>
> **Solución dimensionada — pilastras de H°A° cada 3,00 m:**
> ```
> Momento en la base de cada pilastra = 1.850 N/m² × 3,00 m × 2,20²/2 = 13.430 Nm ≈ 13,4 kNm
> ```
> Requiere una columna de al menos 0,20 × 0,20 m con armadura adecuada **[VERIFICAR con diagrama de interacción]**, y una **base cuyo peso y ancho resistan el vuelco**: con un peso propio de tramo de muro ≈ 16,5 kN por pilastra, hace falta una base de al menos 0,80 m de ancho para que la resultante caiga dentro del núcleo central.
>
> **Y en el remate del muro:** un muro libre en su borde superior se comporta peor que uno con encadenado de coronamiento. **Poner viga de encadenado superior**, que además reparte la carga entre pilastras y convierte el muro en una losa apoyada en cuatro bordes en vez de un voladizo.

**Alternativa de proyecto mucho mejor:** cerco de **2,20 m con la parte superior calada** (30-50 % de vacíos). Baja la carga, mejora el confort a sotavento (§5.1) y sale más barato. Si los vacíos superan el 30 %, se calcula con la Tabla 12, que da C_f = 1,6 sobre el **área sólida solamente**: para ε = 0,5 la fuerza total es 1,6 × 0,5 = 0,8 veces la de un muro macizo con C_f = 1,2 → **33 % menos de carga**, con una zona protegida más larga y sin turbulencia.

### 9.5 Paneles solares en cubierta
Cada vez más frecuentes en Santa Rosa (buen recurso solar: heliofanía efectiva anual **7,0 h/día**, con **9,9 h en enero** [V, SMN]).

**[V] CIRSOC 102-25 incorpora tratamiento específico:** el Capítulo 4 cubre "accesorios de edificios (estructuras sobre azoteas y equipamiento sobre azoteas)" y la **Figura 4.5-7** define la geometría de los paneles solares en cubierta con parámetros propios: `h₁` (altura del borde inferior del panel sobre la cubierta), `h₂` (borde superior), `L_p` (longitud de la cuerda del panel), `L_b` (longitud normalizada del edificio), `d₀` (distancia normal entre el borde del panel y el borde del edificio), `d₁` (distancia al conjunto adyacente). **CIRSOC 102-2005 no lo trata: hay que usar 102-25 o bibliografía específica.**

**Reglas de proyecto:**
1. **Nunca en zona 3 (esquinas) ni en zona 2 (fajas de borde de 1 m).** Las succiones ahí son 3 veces las del interior, y el panel actúa como ala. **Retirar los paneles al menos `a` (1 m en nuestra casa), preferentemente 1,5 a 2 m del borde.**
2. **Cuanto más bajo y más paralelo a la cubierta, mejor.** Un panel a 15° sobre una cubierta plana es un perfil aerodinámico con sustentación. Un panel coplanar apenas altera el flujo.
3. **Nunca lastrado en Santa Rosa.** Los sistemas "sin perforar" que se lastran con bloques de hormigón están calibrados para regiones de viento moderado. Con 156 días de viento fuerte y ráfagas de 143 km/h, **anclaje mecánico pasante y sellado**.
4. **El anclaje del panel se suma a la succión de la cubierta**, no la sustituye. Los cabios bajo los paneles reciben la carga del panel además de la propia.
5. **Termotanque solar:** peor que el panel fotovoltaico, porque además lleva el peso del tanque arriba. Anclarlo y verificar la estructura de apoyo. **[VERIFICAR según Cap. 4 del 102-25.]**

### 9.6 Otros elementos, en orden de fragilidad

| Elemento | Modo de falla | Prevención |
|---|---|---|
| **Cumbrera y cenefas de borde de chapa** | Se levantan antes que la chapa. Solape insuficiente y fijación cada dos ondas | Solape ≥ 200 mm, fijación en cada onda, fleje de borde continuo |
| **Canaletas y bajadas** | Arrancadas por el viento (C_pn = 1,3 en cenefa a barlovento, Anexo I) | Ménsulas cada 0,60 m, no cada 1,20 |
| **Tejas cerámicas o de hormigón sueltas en el perímetro** | Se levantan de a una, en las 2 primeras hiladas de alero y las 2 últimas de cumbrera y en los bordes de hastial | **Fijar mecánicamente (clavo/gancho) todas las tejas de las zonas 2 y 3**; en el interior el peso alcanza |
| **Tanque de agua elevado** | Vuelco de la estructura de apoyo | Se calcula con la Tabla 10 del 102-2005 (C_f según h/D y rugosidad) y se ancla |
| **Antenas, chimeneas metálicas, extractores** | Vuelco y arranque | Riendas o anclaje calculado |
| **Toldos y velas de sombra** | Rotura de la tela o del anclaje | Recogibles. Especificar velocidad máxima de operación. **En Santa Rosa un toldo fijo no sobrevive** |
| **Vidrios grandes** | Impacto de proyectiles (37 días/año de tempestad de polvo, grava suelta de terrazas y patios) | No usar grava suelta a la vista. Vidrio laminado en aberturas grandes de barlovento |
| **Media sombra, mallas, cañizo** | Se rompe en 1-2 temporadas | Considerarlo consumible, o no usarlo |

---

## 10. Ventilación natural: cuándo el viento es recurso

### 10.1 El recurso disponible

Santa Rosa tiene, para ventilación natural, un recurso **excepcional**:

| Dato | Valor | [V] |
|---|---|---|
| Calmas anuales | **1,2 % del tiempo** | SMN |
| Calmas en verano (D-E-F) | **0,8 %** | SMN |
| Velocidad media enero | **16,8 km/h = 4,7 m/s** | SMN |
| Dirección dominante en verano | **N (39 %) y S (16 %)** — eje limpio N-S | SMN |
| Amplitud térmica media de enero | **31,5 °C máx − 16,5 °C mín = 15,0 K** | SMN |
| Humedad relativa media de enero | **57,1 %** (baja) | SMN |
| Temperatura mínima media de enero | **16,5 °C** | SMN |

> **Las tres condiciones que hacen viable la ventilación natural como estrategia principal de refrigeración están todas presentes: viento casi permanente, amplitud térmica de 15 K y humedad baja.**

### 10.2 Ventilación cruzada: el eje N-S es un regalo

**El eje de viento dominante (N-S) coincide con el eje de mejor orientación de una casa** (fachada larga al N para el sol, fachada corta al S). En Santa Rosa la ventilación cruzada N-S funciona sola.

**Estimación de caudal** (fórmula estándar de ventilación cruzada por acción del viento):
```
Q = C_v · A · v
```
donde `C_v ≈ 0,5-0,6` con viento perpendicular a la abertura, `A` = la menor de las áreas efectivas de entrada o salida, `v` = velocidad del viento exterior.

| Área efectiva de entrada | Viento a 15 km/h (4,2 m/s) | Viento a 25 km/h (6,9 m/s) |
|---|---|---|
| 0,5 m² | 3.780 m³/h | 6.210 m³/h |
| **1,0 m²** | **7.560 m³/h** | **12.420 m³/h** |
| 2,0 m² | 15.120 m³/h | 24.840 m³/h |

Una casa de 120 m² con 2,60 m de altura libre tiene un volumen de **312 m³**. Con 1,0 m² de abertura efectiva y viento medio: **7.560 / 312 = 24 renovaciones por hora.**

> ### 🔑 **El problema en Santa Rosa NO es conseguir ventilación. Es CONTROLARLA.**
> Con **1 m² de abertura efectiva alcanzan 24 renovaciones por hora** — muchísimo más de lo necesario. **Toda la inteligencia del proyecto está en la regulación fina, no en el tamaño de los huecos.**
>
> **Consecuencias de proyecto:**
> 1. **Toda abertura de ventilación necesita al menos tres posiciones**, no dos. Una hoja de corredera abierta 10 cm ya ventila una habitación entera.
> 2. **Banderolas, celosías regulables y ventilaciones altas** son mejores que abrir la hoja principal: dan control fino y no dejan entrar el polvo a la altura de la mesa.
> 3. **Mosquitero + tela metálica reducen el área efectiva un 30-50 %** [VERIFICAR según el tipo de malla]. Con el recurso que hay, sigue sobrando.
> 4. **Una ventilación mal dimensionada en Santa Rosa no es un espacio mal ventilado: es un espacio inhabitable por corriente de aire.** Papeles que vuelan, puertas que golpean, cortinas horizontales.
> 5. **Amortiguar la entrada:** que el aire entre por una abertura no orientada directamente al N, o que atraviese primero un espacio de transición (galería, hall, patio protegido). Se gana confort sin perder caudal.

### 10.3 Ventilación nocturna de verano: la estrategia principal

Con **15 K de amplitud térmica** en enero y mínimas medias de 16,5 °C, **la ventilación nocturna es la estrategia de refrigeración de mayor rendimiento por peso invertido en Santa Rosa.** El mecanismo: durante la noche se hace pasar aire exterior frío por la masa térmica interior (contrapiso, losa, muros), que se enfría; durante el día la casa se cierra y esa masa absorbe la carga térmica.

**Estimación de dimensionado [SUP, orden de magnitud]:**

Enfriar 100 m² de losa de 0,12 m de H°A° (masa 100 × 0,12 × 2.400 = **28.800 kg**, calor específico ≈ 1,0 kJ/kg·K) en **3 K** requiere:
```
E = 28.800 × 1,0 × 3 = 86.400 kJ
```
Aire a ΔT = 8 K (interior 26 °C, exterior 18 °C — coherente con la mínima media de 16,5 °C en enero):
```
energía por m³ de aire = 1,2 kg/m³ × 1,0 kJ/kg·K × 8 K = 9,6 kJ/m³
volumen necesario = 86.400 / 9,6 = 9.000 m³
en 8 horas de noche = 1.125 m³/h = 0,31 m³/s
```
Área de abertura necesaria con viento nocturno de 3 m/s (conservador):
```
A = 0,31 / (0,55 × 3) = 0,19 m²
```

> **Menos de 0,2 m² de abertura efectiva bastan para purgar térmicamente la casa cada noche.** Es decir: **dos banderolas de 0,4 × 0,3 m opuestas.** El recurso sobra por un orden de magnitud.

**Lo que hay que resolver para que funcione (y es lo que suele faltar):**

| Requisito | Por qué |
|---|---|
| **Masa térmica accesible al aire** | Si la losa tiene cielorraso suspendido y el piso tiene alfombra, no hay a qué enfriar. **Losa vista o cielorraso aplicado, no colgado.** Es el argumento decisivo a favor de la cubierta pesada (§7.4) |
| **Aberturas nocturnas seguras** | Nadie duerme con la ventana abierta si no tiene reja. **Banderolas altas con reja fija, celosías de seguridad, o ventilación en cámara** |
| **Aberturas nocturnas a prueba de lluvia y polvo** | 54 días de tormenta y 37 de tempestad de polvo al año. Las banderolas deben poder quedar abiertas con lluvia (voladizo/alero) |
| **Aberturas nocturnas sin insectos** | Mosquitero fijo en la banderola |
| **Recorrido de aire libre** | Puertas interiores abiertas o con paso inferior/superior. Si el aire entra al norte y la puerta del dormitorio está cerrada, no hay barrido |
| **Cierre efectivo de día** | La estrategia sólo funciona si la casa se cierra al mediodía. Persianas + carpinterías A2/A3 |

### 10.4 Efecto chimenea (ventilación por diferencia de temperatura)

En Santa Rosa el efecto chimenea es un **recurso secundario**, porque el recurso de viento es tan abundante que casi siempre domina. Pero es **esencial en el 1,2 % de calmas y en las noches de verano sin viento**, que son justamente las peores.

```
Q = C_d · A · √( 2 · g · Δh · (T_i − T_e) / T_i )
```
Con `Δh` = altura entre la abertura de entrada y la de salida, `T` en Kelvin.

| Δh (altura útil) | ΔT = 5 K | ΔT = 10 K |
|---|---|---|
| 2,0 m | 0,40 m/s | 0,57 m/s |
| **3,5 m** (cumbrera de la casa tipo) | **0,53 m/s** | **0,75 m/s** |
| 6,0 m | 0,70 m/s | 0,99 m/s |

*(Velocidad teórica de la corriente; el caudal es `≈ 0,6 · A · v`.)*

**En la casa tipo (2,70 m de alero, 4,52 m de cumbrera) hay 1,82 m de altura aprovechable en el volumen del techo.** Es poco pero no es nada.

**Recursos de proyecto para amplificar el efecto chimenea en una casa de una planta:**
1. **Cubierta a dos aguas con la cumbrera aprovechada:** ventilación alta en el hastial o en un lucernario de cumbrera. Con la habitación abierta al volumen del techo (techo inclinado a la vista) se ganan 1,8 m de Δh gratis.
2. **Patio interior o lucernario con abertura cenital.** El clásico.
3. **Chimenea solar** en la fachada norte: un conducto vertical con la cara al sol, que se sobrecalienta y aumenta ΔT. Con la heliofanía de Santa Rosa (9,9 h/día en enero) funciona muy bien. **Cuidado: es también un elemento expuesto que hay que anclar.**
4. **Doble altura en el estar** con banderola alta al S y entrada baja al N.

### 10.5 Cuándo el viento es recurso y cuándo es problema — la tabla de decisión

| Situación | Velocidad del viento | Viento como… | Estrategia |
|---|---|---|---|
| Verano, día, casa cerrada, interior 26 °C | Cualquiera | **Problema** (arrastra calor exterior) | Cerrar. Carpintería A2/A3, persianas, alero |
| Verano, día, uso de la galería | > 15 km/h del N | **Problema** (confort) | Barrera semipermeable a 4H (§5) |
| **Verano, noche, purga térmica** | **> 3 km/h** | **RECURSO PRINCIPAL** | Banderolas altas abiertas, barrido cruzado (§10.3) |
| Verano, día, sensación de bochorno interior | 10-20 km/h | **Recurso** | Ventilación cruzada controlada; el aire en movimiento sube la temperatura de confort ~2-3 K |
| Media estación (abr-may, sep-oct) | 12-16 km/h | **Recurso** | Ventilación libre casi todo el día |
| **Invierno, cualquier hora** | Cualquiera | **PROBLEMA** (infiltración) | Estanqueidad (§6). Sólo ventilación higiénica controlada |
| Invierno, día soleado, ganancia solar N | Del S o SW | **Problema** (enfría la fachada) | Fachada S compacta y muy aislada |
| Tempestad de polvo (37 días/año) | Alta | **PROBLEMA** | Cerrar todo. El sellado es lo que decide si hay que limpiar la casa entera |
| **Tendido de ropa** | Cualquiera | **RECURSO** | Tendedero expuesto al N |

**Regla de oro:** **en Santa Rosa la ventilación natural no se dimensiona por caudal, se dimensiona por control.** El caudal está garantizado por el clima. Lo que hay que proyectar son los dispositivos que permiten graduarlo: banderolas, celosías, persianas de lamas orientables, esclusas, patios intermedios.

---

## 11. Checklist de verificación de viento en el proyecto

### A. Datos de partida (antes de dibujar)

- [ ] **Verificar qué edición del CIRSOC 102 exige el visado** (Municipalidad de Santa Rosa / CPIA La Pampa). **[VERIFICAR]**
- [ ] Fijar **V** según esa edición: 50,0 m/s (102-2005) o **61,2 m/s** (102-25, Cat. Riesgo II).
- [ ] **Elegir el factor de carga coherente con la edición: 1,6 W (2005) o 1,0 W (2025). NO MEZCLAR.**
- [ ] **Determinar la categoría de exposición verificando 450 m de rugosidad B a barlovento, POR DIRECCIÓN (sectores de ±45°), especialmente al N y al S.** Ante la duda, **C**.
- [ ] Verificar K_zt = 1,00 (revisar si el lote está sobre un borde de bajo o valle).
- [ ] Confirmar K_e (102-25): 0,978 para 190 m s.n.m., o 1,00 conservador.
- [ ] Clasificar el cerramiento: **cerrado (±0,18)** o **parcialmente cerrado (±0,55)**. Si hay portón de garaje o ventanal grande en una sola fachada, decidir explícitamente (§8.9).

### B. Implantación y partido (croquis)

- [ ] **Dibujar la rosa de los vientos de Santa Rosa sobre el plano de implantación** (N 34 % @ 18 km/h; S 18 % @ 18 km/h; W-NW el sector protegido).
- [ ] Verificar que el partido **no genere embudo** al N (nada de "U" abierta al norte).
- [ ] Ubicar la galería/expansión principal al **N** con filtro (parapeto 1,00-1,10 m + celosía) o al **NE/E**.
- [ ] Ubicar el quincho / parrilla en el sector protegido **W-NW**.
- [ ] Fachada **S**: compacta, aberturas mínimas, locales de servicio, máximo sellado y aislación.
- [ ] Verificar que ningún paso lateral tenga menos de 1,50 m de ancho.
- [ ] Ubicar el tendedero **expuesto** (único caso donde conviene).
- [ ] Si el garaje está en el frente N: decidir si se separa, se ventila o se calcula la casa como parcialmente cerrada.

### C. Barreras

- [ ] Definir la **altura H** de cada barrera en función de la distancia D al punto a proteger: **H ≈ D/4** (máxima protección) o **H ≥ D/10** (aceptable).
- [ ] Porosidad objetivo: **30-45 %**. Nada de muros macizos altos como barrera de confort.
- [ ] Longitud mínima: **10 H**, y ≥ 3 veces el ancho del área protegida.
- [ ] Sin brechas ni interrupciones (o resolverlas con solapes/mangas).
- [ ] Orientación perpendicular al N ± 45°.
- [ ] Especies: **perennes** (una barrera caduca no existe en invierno: 15 % de área efectiva).
- [ ] **[VERIFICAR]** distancias mínimas de plantación a fundaciones, cloacas y medianera en la ordenanza municipal.
- [ ] Toda barrera construida > 1,5 m: **verificar estructuralmente** (§9.4). Pilastras + encadenado de coronamiento + base dimensionada al vuelco.

### D. Cubierta (lo crítico)

- [ ] Calcular **a** = min(0,10·b ; 0,40·h), ≥ max(0,04·b ; 1,00 m). **Dibujar las zonas 1, 2 y 3 en el plano de techos.**
- [ ] Calcular q_h con K_h de **Caso 1** de la Tabla 5.
- [ ] SPRFV con **Figura 4 (GC_pf)**, corriendo las **8 hipótesis** (4 rotaciones × Caso A y B).
- [ ] Aplicar la **nota 4b**: el corte horizontal no puede ser menor que el que resulta de despreciar la cubierta.
- [ ] **Calcular la succión total sobre la cubierta y compararla con `0,9 D`.**
- [ ] Si `1,6 W↑ > 0,9 D` → **diseñar el anclaje**, con la demanda en kN por metro de alero y por cabio, **diferenciando las zonas de extremo (2 m en cada una de las 4 esquinas) donde la demanda es ~50 % mayor**.
- [ ] **Dibujar la cadena de anclaje completa** en el corte constructivo: chapa → clavadera → cabio → **fleje** → encadenado → muro → cimiento. Verificar que **ningún eslabón falte**.
- [ ] Verificar que el **encadenado superior sea continuo** (sin interrupciones en dinteles).
- [ ] C&R con **Figura 5B**: presiones por zona y por área efectiva. **Especificar la separación de fijaciones POR ZONA en el plano**, no una sola separación para todo el techo.
- [ ] **[VERIFICAR con el fabricante]** la resistencia al arranque por perforación (*pull-through*) de la chapa.
- [ ] Alero: cabio volado (no chapa volada), sofito cerrado, fleje de borde continuo fijado mecánicamente.
- [ ] Cumbrera y cenefas: solape ≥ 200 mm, fijación en cada onda.
- [ ] Si la cubierta es plana: considerar **parapeto ≥ 1,00 m** para convertir la zona 3 en zona 2 (−34 % de presión). Membrana fijada mecánicamente en el perímetro. **Prohibida la grava suelta.**
- [ ] Tejas: fijar mecánicamente todas las de las zonas 2 y 3.

### E. Cerramientos

- [ ] **Dibujar el plano de estanqueidad al aire** como una línea continua en el corte. Si se interrumpe en el dibujo, se interrumpe en la obra.
- [ ] Especificar carpinterías con clasificación **IRAM A2 mínimo**, A3 en fachada S y aberturas grandes del N.
- [ ] Especificar **resistencia a carga de viento** de las carpinterías, no sólo estanqueidad. **[VERIFICAR clasificación en IRAM 11507]**
- [ ] Sellado perimetral marco-muro: espuma PU + sellador elástico continuo interior y exterior. **No confiar en el revoque.**
- [ ] Cajas de persiana: aisladas y estancas.
- [ ] Portón de garaje: especificar resistencia a viento y anclaje de guías al muro.
- [ ] Pasos de instalaciones: pasamuros sellados uno por uno.

### F. Elementos secundarios

- [ ] Galería/quincho con cubierta independiente: **calcular con el Anexo I** (cubiertas aisladas, coeficientes mucho más severos). **Columnas ancladas a tracción, con dado de fundación dimensionado por peso.**
- [ ] Cenefa frontal de galería: C_pn = 1,3. Anclar.
- [ ] Pérgolas: Tabla 12 (C_f = 1,6-2,0 según ε). **Cada listón y su fijación.**
- [ ] Medianeras y cercos > 1,8 m: cálculo de vuelco con Tabla 11 (C_f = 1,2). Pilastras + base.
- [ ] Paneles solares: retirar ≥ 1,5 m de los bordes; anclaje mecánico pasante; **nunca lastrados**.
- [ ] Tanque de agua, equipos de aire, chimeneas: anclados y calculados.
- [ ] Toldos: recogibles.
- [ ] **Nada de grava suelta** en terrazas ni patios.

### G. Ventilación

- [ ] Verificar que exista **ventilación cruzada N-S efectiva** en cada local principal.
- [ ] **Toda abertura de ventilación con al menos 3 posiciones de apertura**, no 2.
- [ ] **Banderolas altas con reja y mosquitero fijos** para ventilación nocturna de verano segura.
- [ ] **Masa térmica accesible al aire**: evitar cielorraso suspendido continuo en los locales principales.
- [ ] Recorrido de aire libre entre locales (paso bajo puertas o banderolas interiores).
- [ ] Recurso de efecto chimenea: aprovechar la altura de cumbrera (1,8 m adicionales) o un lucernario.
- [ ] Verificar que la entrada de aire principal **no dé directamente al N sin amortiguación** (espacio de transición).

---

## 12. Fuentes

**Normativa (verificada contra el PDF original):**
1. **CIRSOC 102 — Reglamento Argentino de Acción del Viento sobre las Construcciones**, INTI-CIRSOC, julio 2005. 124 pp. Capítulos 1-6, Figuras 1B, 2, 3, 4, 5A, 5B, 5B(cont.), 5C; Tablas 1 a 13; Apéndices A y B; Anexos I a VI. — `http://contenidos.inpres.gob.ar/docs/Reglamentos/CIRSOC-102-Reglamento.pdf`
2. **CIRSOC 102-25 — Reglamento Argentino de Acción del Viento sobre las Construcciones**, INTI-CIRSOC, 2025. 292 pp. Capítulos 1-6 con Comentarios. Tabla de velocidades en ciudades (Comentario C 1.5), Tabla 1.6-1 (K_d), art. 1.7 y Tablas C 1.7-1/C 1.7-2 (exposición y rugosidad), Tabla 1.11-1 (GC_pi), Tabla 1.12-1 (K_e), art. 1.13 (K_z). — `https://icomunicacion.inti.gob.ar/2025/cirsoc/Reglamento-CIRSOC-102-25.pdf`
3. Resolución 11/2026, Secretaría de Obras Públicas de la Nación — puesta en vigencia de la 3.ª generación de Reglamentos CIRSOC. **[VERIFICAR alcance y fechas]**
4. **IRAM 11507-1** — Carpintería de obra. Ventanas exteriores. Requisitos básicos y clasificación. **[VERIFICAR valores numéricos del cap. 4.6]**
5. Decreto 1030/2010, Provincia de Buenos Aires (reglamentario de la Ley 13.059), art. 2.7.1 — exigencia de clasificación IRAM A1/A2. Citado como referencia de criterio; **no rige en La Pampa**. **[VERIFICAR si La Pampa o Santa Rosa tienen norma equivalente.]**

**Datos climáticos (verificados contra el PDF original):**
6. **Servicio Meteorológico Nacional (2023), "Estadísticas Climatológicas Normales — República Argentina, período 1991-2020"**, ISSN 2953-5549, 853 pp. **Ficha SANTA ROSA AERO, La Pampa (ID WIGOS 0-20000-0-87623), pp. 448-455.** Estadísticas de viento correspondientes al subperíodo **2011-2020**. — `https://repositorio.smn.gob.ar/handle/20.500.12160/2506`

**Investigación sobre barreras de viento:**
7. **Peri, P. L. (1998), "Efectos de parámetros estructurales de cortinas forestales en la reducción del viento en la provincia de Santa Cruz, Argentina"**, *Quebracho* N° 6, pp. 20-27, FCF-UNSE. Tabla 2 (R₁ por porosidad y distancia). — `https://fcf.unse.edu.ar/archivos/quebracho/q6_02.pdf`
8. **Ramilo, D. (2021), "Cortinas forestales", cap. 4 de Sharry, Stevani y Galarco (coord.), *Sistemas Agroforestales en Argentina*, FCAyF-UNLP, pp. 87-133.** Porosidades, espaciamientos, especies por región, longitud mínima. — `http://sedici.unlp.edu.ar/handle/10915/132081`
9. Peri, P. L. — *Cortinas forestales cortaviento*, INTA EEA Santa Cruz, Producción Forestal, oct. 2003.

**Arbolado urbano local:**
10. *Evaluación del arbolado urbano de alineación en la zona céntrica de Santa Rosa, La Pampa*, revista **Semiárida** (UNLPam), 2022. — `https://cerac.unlpam.edu.ar/index.php/semiarida/`
11. *Relevamiento del arbolado urbano del barrio Santa María de las Pampas, Santa Rosa, La Pampa*, revista **Semiárida** (UNLPam).

**Documentación interna del estudio:**
12. `docs/03-estructuras/estructuras.md` §2.2 (combinaciones de carga), §2.5 (viento, tablas generales del CIRSOC 102), §2.6 (sismo / exención en zona 0).
13. `docs/00-marco/marco-local-santa-rosa.md`.

---

## Pendientes para cerrar el documento

| # | Qué falta | Dónde | Prioridad |
|---|---|---|---|
| 1 | Confirmar qué edición del CIRSOC 102 exige el visado en Santa Rosa | Municipalidad / CPIA La Pampa | **Alta** |
| 2 | Verificar la lectura de los GC_p de las Figuras 5A y 5B (cont.) en el reglamento impreso | CIRSOC 102-2005 | **Alta** |
| 3 | Rehacer §8.3-§8.7 con las figuras del 102-25 si esa es la edición aplicable | CIRSOC 102-25, Figs. 2.4-x y 5.3-x | **Alta** |
| 4 | Valores numéricos exactos de la clasificación IRAM A1/A2/A3 y de estanqueidad al agua | IRAM 11507-1, cap. 4.6 | Media |
| 5 | Umbral de "viento fuerte" del SMN | Glosario SMN | Media |
| 6 | Si el "viento máximo diario" del SMN es ráfaga instantánea o promedio de intervalo | SMN | Media |
| 7 | Capacidad de *pull-through* de la chapa que se especifique | Fabricante | Media (obra) |
| 8 | Distancias de plantación y especies permitidas | Ordenanza de arbolado, Municipalidad de Santa Rosa | Media |
| 9 | Comportamiento de *Cupressus sempervirens* y *Casuarina* en suelo y régimen pluviométrico de Santa Rosa (753 mm/año) | Vivero local / INTA Anguil | Baja |
| 10 | Verificar los pesos propios [SUP] del §8.4 contra el cómputo real del proyecto | Proyecto | **Alta** al momento de calcular |
