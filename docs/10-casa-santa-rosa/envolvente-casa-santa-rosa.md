# ENVOLVENTE TÉRMICA DE UNA CASA DE UNA PLANTA EN SANTA ROSA, LA PAMPA
## Soluciones constructivas concretas, calculadas y comparadas
### Documento técnico de proyecto — estudio de arquitectura, Santa Rosa (LP)

> **Qué es este documento.** No repite el método de cálculo de K (eso está en `docs/05-construccion/tecnologia-constructiva.md`, cap. 4). Este documento **fija el objetivo numérico** para Santa Rosa, **resuelve la discrepancia de datos climáticos** que había entre los dos registros del repositorio, y entrega **soluciones de muro, techo, piso y carpintería con espesores, K calculado, verificación de nivel y costo relativo**, para el caso específico de una **vivienda unifamiliar de planta baja únicamente**.
>
> **Qué tiene de particular una casa de una planta.** La relación superficie de envolvente / volumen es la peor de todas las tipologías: **el techo es la mayor superficie de pérdida y de ganancia** (en una casa de 130 m² el techo es el 40–45 % de toda la envolvente opaca), **todo el piso está en contacto con el terreno**, y **no hay entrepisos que aporten masa**. Las conclusiones de un edificio en altura no se trasladan.

---

## ÍNDICE

**[0. Resumen ejecutivo — los ocho números del proyecto](#0-resumen-ejecutivo--los-ocho-números-del-proyecto)**

**[1. EL OBJETIVO NUMÉRICO](#1-el-objetivo-numérico)**
- [1.1 La discrepancia de TDMN: −2,7 vs −6,0 °C. Resolución](#11-la-discrepancia-de-tdmn-27-vs-60-c-resolución)
- [1.2 Datos climáticos de proyecto adoptados](#12-datos-climáticos-de-proyecto-adoptados)
- [1.3 Zona bioambiental: la segunda contradicción](#13-zona-bioambiental-la-segunda-contradicción)
- [1.4 K máximos admisibles de IRAM 11605 — invierno](#14-k-máximos-admisibles-de-iram-11605--invierno)
- [1.5 K máximos admisibles de IRAM 11605 — verano](#15-k-máximos-admisibles-de-iram-11605--verano)
- [1.6 Corrección por color: la decisión gratuita de mayor impacto](#16-corrección-por-color-la-decisión-gratuita-de-mayor-impacto)
- [1.7 TABLA MAESTRA: valores de proyecto para Santa Rosa](#17-tabla-maestra-valores-de-proyecto-para-santa-rosa)
- [1.8 Pisos: la norma que hay que usar es la 11604, no la 11605](#18-pisos-la-norma-que-hay-que-usar-es-la-11604-no-la-11605)
- [1.9 Exigencia normativa provincial y municipal en La Pampa](#19-exigencia-normativa-provincial-y-municipal-en-la-pampa)
- [1.10 Datos de entrada del cálculo (resistencias, λ, Rt)](#110-datos-de-entrada-del-cálculo-resistencias-λ-rt)

**[2. MUROS](#2-muros)**
- [2.1 Las doce soluciones calculadas](#21-las-doce-soluciones-calculadas)
- [2.2 Tabla comparativa general](#22-tabla-comparativa-general)
- [2.3 Espesor de aislante necesario por objetivo](#23-espesor-de-aislante-necesario-por-objetivo)
- [2.4 Costo relativo, mano de obra y disponibilidad en Santa Rosa](#24-costo-relativo-mano-de-obra-y-disponibilidad-en-santa-rosa)
- [2.5 LA RECOMENDACIÓN POR DEFECTO](#25-la-recomendación-por-defecto)

**[3. TECHO](#3-techo)**
- [3.1 Por qué en cubierta manda el verano](#31-por-qué-en-cubierta-manda-el-verano)
- [3.2 Las nueve soluciones calculadas](#32-las-nueve-soluciones-calculadas)
- [3.3 Tabla comparativa general de cubiertas](#33-tabla-comparativa-general-de-cubiertas)
- [3.4 Espesor de aislante necesario en cubierta](#34-espesor-de-aislante-necesario-en-cubierta)
- [3.5 Ventilación de cubierta y cámara de aire](#35-ventilación-de-cubierta-y-cámara-de-aire)
- [3.6 LA RECOMENDACIÓN POR DEFECTO](#36-la-recomendación-por-defecto)

**[4. PISO](#4-piso)**
- [4.1 Cómo se computa la pérdida por el piso](#41-cómo-se-computa-la-pérdida-por-el-piso)
- [4.2 Las tres situaciones de la norma y cómo se materializan](#42-las-tres-situaciones-de-la-norma-y-cómo-se-materializan)
- [4.3 Cuánto pesa el piso en una casa de una planta](#43-cuánto-pesa-el-piso-en-una-casa-de-una-planta)
- [4.4 Aislación perimetral: detalle constructivo](#44-aislación-perimetral-detalle-constructivo)
- [4.5 Piso y losa radiante](#45-piso-y-losa-radiante)

**[5. CARPINTERÍAS Y VIDRIOS](#5-carpinterías-y-vidrios)**
- [5.1 Perfilería comparada](#51-perfilería-comparada)
- [5.2 Vidrios: K y factor solar](#52-vidrios-k-y-factor-solar)
- [5.3 Ventana completa: la tabla que hay que usar](#53-ventana-completa-la-tabla-que-hay-que-usar)
- [5.4 ¿Se justifica el DVH en Santa Rosa? Análisis con supuestos explícitos](#54-se-justifica-el-dvh-en-santa-rosa-análisis-con-supuestos-explícitos)
- [5.5 Cajón de persiana](#55-cajón-de-persiana)
- [5.6 Sellado perimetral y estanqueidad al aire en zona ventosa](#56-sellado-perimetral-y-estanqueidad-al-aire-en-zona-ventosa)
- [5.7 Superficie vidriada máxima y cómo convive con querer luz y sol](#57-superficie-vidriada-máxima-y-cómo-convive-con-querer-luz-y-sol)

**[6. PUENTES TÉRMICOS DE UNA CASA DE UNA PLANTA](#6-puentes-térmicos-de-una-casa-de-una-planta)**

**[7. CONDENSACIÓN](#7-condensación)**

**[8. ESTRATEGIAS PASIVAS](#8-estrategias-pasivas)**

**[9. PRIORIDAD DE INVERSIÓN](#9-prioridad-de-inversión)**

**[10. CHECKLIST DE ENVOLVENTE](#10-checklist-de-envolvente-para-el-proyecto-de-una-casa)**

**[11. Fuentes y estado de verificación](#11-fuentes-y-estado-de-verificación)**

---

# 0. Resumen ejecutivo — los ocho números del proyecto

| # | Parámetro | Valor de proyecto | Origen |
|---|---|---|---|
| 1 | **TDMN — temperatura exterior de diseño mínima** | **−6,0 °C** | IRAM 11603:2011, Anexo, estación Santa Rosa (Aero), serie 1980-2009 |
| 2 | **TDMX — temperatura exterior de diseño máxima** | **38,8 °C** | ídem |
| 3 | **GD18 — grados-día base 18 °C** | **1.394 °C·día** | ídem |
| 4 | **K máx. admisible MUROS** | **0,30 (Nivel A) / 0,80 (Nivel B)** W/m²K | IRAM 11605, Tabla 1, invierno, con TDMN −6,0 |
| 5 | **K máx. admisible TECHOS** | **0,19 (Nivel A) / 0,48 (Nivel B)** W/m²K | IRAM 11605, Tabla 3, verano, zona III y IV |
| 6 | **Pérdida por piso en contacto con el terreno** | **1,38 / 1,08 / 0,93 W/m** de perímetro | IRAM 11604:2001, Tabla 2, zona III y IV |
| 7 | **Gadm — coeficiente volumétrico admisible** (casa de 338 m³) | **≈ 1,57 W/m³K** | IRAM 11604:2001, Tabla 1, interpolado |
| 8 | **Relación superficie vidriada / opaca recomendada** | **≤ 15 %** | IRAM 11603, recomendaciones Zona IV |

**Solución de muro recomendada por defecto:** ladrillo cerámico hueco 18 revocado + **SATE de EPS de 100 mm** (K = 0,29 W/m²K → **Nivel A**). Piso contractual: SATE de EPS de 60 mm (K = 0,43 → Nivel B con margen).

**Solución de techo recomendada por defecto:** losa de viguetas con bovedilla de EPS + **EPS de 120–140 mm sobre la losa** + contrapiso de pendiente + membrana con **terminación clara (α < 0,6)**, o cubierta invertida con XPS. K resultante 0,20–0,25 W/m²K.

---

# 1. EL OBJETIVO NUMÉRICO

## 1.1 La discrepancia de TDMN: −2,7 vs −6,0 °C. Resolución

En el repositorio conviven dos juegos de datos climáticos de Santa Rosa que no coinciden:

| Parámetro | `05-construccion/tecnologia-constructiva.md` (§0.1) | `04-instalaciones/instalaciones.md` (§6.1.1) |
|---|---|---|
| Fuente citada | Czajkowski & Gómez, *Diseño bioclimático y economía energética edilicia* (UNLP/SEDICI) | **IRAM 11603:2011, Anexo A**, estación Santa Rosa (Aero), serie 1980-2009 |
| TMED invierno | 8,2 °C | 9,77 °C |
| TMIN media invierno | 1,8 °C | 3,5 °C |
| **TDMN** | **−2,7 °C** | **−6,0 °C** |
| TMA (mínima absoluta) | no figura | −11,3 °C |
| TMAX media verano | 30,3 °C | 29,4 °C |
| **TDMX** | **33,8 °C** | **38,8 °C** |
| GD18 | 1.331 | 1.394 |

### La causa: dos métodos distintos de obtener la temperatura de diseño

**Definición formal de IRAM 11603:2011, apartado 3.3** (verificada en el texto de la norma):

> *"**temperatura de diseño.** Es el percentil del 1 % o del 99 % de las temperaturas mínimas o máximas diarias del período de invierno (mayo, junio, julio y agosto) o verano (diciembre, enero, febrero y marzo), respectivamente."*

**Regla simplificada** que circula en la bibliografía docente y que la propia norma admite como aproximación (verificada en el material de cátedra de Instalaciones/UNLP que reproduce las tablas de IRAM 11605):

> *"La temperatura mínima de diseño se obtiene, de manera simplificada, **restando 4,5° a la temperatura mínima media** de la localidad. Esto se corresponde a una frecuencia de 4 días de ocurrencia de cierta temperatura en 5 años."*
> *"La temperatura máxima de diseño se obtiene, de manera simplificada, **sumando 3,5° a la temperatura máxima media** de la localidad."*

**Aplicando la regla simplificada al juego de datos de Czajkowski:**

```
TDMN = TMIN − 4,5 = 1,8 − 4,5 = −2,7 °C     ← EXACTAMENTE el valor de tecnologia-constructiva.md
TDMX = TMAX + 3,5 = 30,3 + 3,5 = 33,8 °C    ← EXACTAMENTE el valor de tecnologia-constructiva.md
```

**Aplicando el percentil real del 1 % sobre la serie 1980-2009 (lo que hace el Anexo de IRAM 11603:2011):**

```
TDMN = −6,0 °C     (coherente con una mínima absoluta TMA de −11,3 °C)
TDMX = +38,8 °C    (coherente con una máxima absoluta TMA de +42,1 °C)
```

### VEREDICTO

> ### CON QUÉ NÚMEROS HAY QUE TRABAJAR
>
> **TDMN = −6,0 °C. TDMX = 38,8 °C. GD18 = 1.394 °C·día.**
>
> **Por tres razones, en orden de peso:**
>
> 1. **Son los valores tabulados en el Anexo de la norma.** IRAM 11605 se indexa sobre "la temperatura exterior de diseño de la localidad **obtenida de IRAM 11603**". Cuando la norma publica un valor para la estación, ese valor es el dato normativo; la regla simplificada es una aproximación para localidades **que no están tabuladas**. Santa Rosa (Aero) **sí está tabulada**. No hay margen de interpretación.
> 2. **La regla simplificada subestima sistemáticamente el frío pampeano.** Un TDMN de −2,7 °C es incompatible con una mínima absoluta registrada de −11,3 °C y con el hecho, de conocimiento local, de que en Santa Rosa hay varias mañanas por invierno bajo −5 °C. La regla "TMIN − 4,5" fue calibrada sobre climas de menor amplitud térmica; en un clima continental con amplitud invernal de 12,5 K la cola fría de la distribución es mucho más larga que 4,5 K.
> 3. **Es el criterio conservador, y es el criterio ya adoptado por el estudio** (`instalaciones.md` §6.1.2 y el criterio de encargo de este documento). Dimensionar con −6,0 °C cuesta, en muro, **20 mm más de EPS** que dimensionar con −2,7 °C. Dimensionar con −2,7 °C y que el invierno sea el real cuesta una casa fría durante 50 años.

### Cuánto cambia la exigencia

| Elemento y nivel | Con TDMN = −2,7 °C (interpolado) | Con **TDMN = −6,0 °C** | Endurecimiento |
|---|---|---|---|
| Muros — Nivel A | 0,336 → 0,34 | **0,30** | −12 % |
| Muros — Nivel B | 0,922 → 0,92 | **0,80** | −13 % |
| Techos — Nivel A invierno | 0,293 → 0,29 | **0,26** | −10 % |
| Techos — Nivel B invierno | 0,749 → 0,75 | **0,67** | −11 % |
| Techos — verano (no depende de TDMN) | 0,19 / 0,48 | 0,19 / 0,48 | sin cambio |

> **Acción sobre el repositorio:** la Tabla 0.1 y la Tabla 4.9 de `docs/05-construccion/tecnologia-constructiva.md` deben corregirse o, como mínimo, llevar una nota que remita a este apartado. Los K de la Tabla 4.10 de ese documento están bien calculados pero su **columna de verificación de nivel está evaluada contra los admisibles equivocados** (0,34/0,92 en vez de 0,30/0,80). Varias soluciones que allí figuran como "casi A" ahora no llegan.

---

## 1.2 Datos climáticos de proyecto adoptados

**Estación SANTA ROSA (AERO), La Pampa. Lat. −36,57° / Long. −64,27° / 191 m s.n.m. Serie 1980-2009.**
Fuente: **IRAM 11603:2011** (esquema 1, revisión de la edición 1996), Anexo de datos climáticos. Verificado sobre el texto de la norma.

### Tabla 1.1 — Invierno

| Parámetro | Símbolo | Valor |
|---|---|---|
| Temperatura media | TMED | 9,77 °C |
| Temperatura máxima media | TMÁX | 16,0 °C |
| Temperatura mínima media | TMÍN | 3,5 °C |
| **Temperatura mínima absoluta** | **TMA** | **−11,3 °C** |
| **Temperatura exterior de diseño mínima** | **TDMN** | **−6,0 °C** |
| Precipitación | PREC | 105 mm |
| **Humedad relativa** | **HR** | **73 %** |
| Heliofanía relativa | HELRE | 4,8 |
| Velocidad media del viento | VM | 10,1 |
| Grados-día base 16 | GD16 | 994 |
| **Grados-día base 18** | **GD18** | **1.394** |
| Grados-día base 20 | GD20 | 1.865 |
| Grados-día base 22 | GD22 | 2.409 |

### Tabla 1.2 — Verano

| Parámetro | Símbolo | Valor |
|---|---|---|
| Temperatura media | TMED | 22,21 °C |
| Temperatura máxima media | TMÁX | 29,4 °C |
| Temperatura mínima media | TMÍN | 15,0 °C |
| **Temperatura máxima absoluta** | **TMA** | **42,1 °C** |
| **Temperatura exterior de diseño máxima** | **TDMX** | **38,8 °C** |
| Precipitación | PREC | 380,0 mm |
| Humedad relativa | HR | 61,6 % |
| Heliofanía relativa | HELRE | 9,0 |
| Velocidad media del viento | VM | 12,5 |

### Tabla 1.3 — Indicadores derivados para el proyecto

| Indicador | Cálculo | Valor | Consecuencia de proyecto |
|---|---|---|---|
| Salto térmico de diseño **invernal** | 20 − (−6,0) | **26,0 K** | Es el Δt de todos los cálculos de carga y de condensación |
| Salto térmico de diseño **estival** (aire) | 38,8 − 25 | **13,8 K** | Muy inferior al invernal: **el problema de verano no es conducción, es radiación** |
| Amplitud térmica media **invierno** | 16,0 − 3,5 | **12,5 K** | Inercia térmica útil |
| Amplitud térmica media **verano** | 29,4 − 15,0 | **14,4 K** | **Enfriamiento nocturno pasivo plenamente viable** (mínima media de verano de 15,0 °C) |
| Relación GD18 / demanda de frío | 1.394 °C·día contra TMED verano 22,2 °C | — | **Domina ampliamente la calefacción**, pero con TDMX 38,8 y máxima absoluta 42,1 el verano no es despreciable |
| Rango térmico anual absoluto | 42,1 − (−11,3) | **53,4 K** | Todo material expuesto trabaja en ese rango: membranas, selladores, carpinterías |
| HR de invierno | — | **73 %** (IRAM 11603) / 76 % (dataset Czajkowski) | **El aire de invierno NO es seco. La verificación de condensación es obligatoria.** Se adopta el valor conservador **76 %** para exteriores y HR interior de diseño **70 %** |

> **Nota sobre la heliofanía relativa.** IRAM 11603 la publica como 4,8 (invierno) y 9,0 (verano) para Santa Rosa. La unidad de ese campo **no está aclarada en la tabla**: no puede ser un porcentaje (sería absurdamente bajo) y el orden de magnitud sugiere **horas medias diarias de sol efectivo**. `[VERIFICAR la definición del campo HELRE en el cuerpo de IRAM 11603 antes de usarlo en un cálculo solar.]` Para el diseño de aleros y de captación solar de este documento **no se usa este dato**: se usan ángulos solares geométricos, que no dependen de la nubosidad.

---

## 1.3 Zona bioambiental: la segunda contradicción

**Dato 1 — listado departamental de IRAM 11603:2011** (verificado en el texto): bajo **Zona III, subzona IIIa**, La Pampa figura con los departamentos *Atreucó, **Capital**, Catriló, Conhelo, Chapaleufú, Loventué, Maracó, Quemú Quemú, Rancul, Realicó, Toay, Trenel*. **Santa Rosa está en el Departamento Capital → IIIa.**

**Dato 2 — criterio de grados-día de la misma norma:** la Zona IV (templada fría) va de la isolínea de **1.170** a la de **1.950 GD18**. **Santa Rosa tiene 1.394 GD18 → Zona IV.**

**Dato 3 —** los departamentos pampeanos **Caleu Caleu, Caleucalen, Guatraché, Hucal y Lihuel-Calel** figuran en **IVc**, y *Curacó, Chalileo, Chical-Có, Limay Mahuida, Puelen y Utracán* en **IVb**. Es decir: la propia norma pone en zona IV a departamentos vecinos con clima muy parecido.

> ### RESOLUCIÓN
> **Proyectar con criterio de Zona IV, y verificar los K contra los valores que corresponden.** La contradicción es **prácticamente inocua para el dimensionamiento**, por dos razones verificadas:
>
> 1. **Invierno:** los K máx. admisibles de la Tabla 1 de IRAM 11605 **dependen de la TDMN, no de la zona**. Con TDMN = −6,0 el resultado es el mismo se llame la zona III o IV.
> 2. **Verano:** las Tablas 2 y 3 de IRAM 11605 **dan el mismo valor para zonas III y IV** (muros 0,50/1,25/2,00 y techos 0,19/0,48/0,76 para niveles A/B/C). Tampoco cambia nada.
>
> **Sólo afecta a las recomendaciones cualitativas de diseño bioclimático de IRAM 11603** (orientaciones, protección solar, ventilación), donde la Zona IV es más exigente. Se adoptan las de Zona IV, que son las que corresponden al clima real:
> - *"Muy buena aislación en toda la envolvente, sugiriendo **el doble de aislación en techos respecto de muros**"*;
> - *"La relación superficie vidriada / superficie opaca **no debería superar el 15 %**"*;
> - *"En las subzonas c y d **se verificará el riesgo de condensación**, controlando los puentes térmicos"*;
> - orientaciones favorables para latitud > 30°: **NO–N–NE–E**;
> - *"En las zonas IV, V y VI, **la protección contra el viento será de suma importancia**"*.
>
> `[VERIFICAR el encuadre departamental en la edición vigente de IRAM 11603 antes de firmar una verificación higrotérmica ante un organismo. La edición consultada (2011) es un esquema en discusión pública, revisión de la edición 1996.]`

---

## 1.4 K máximos admisibles de IRAM 11605 — invierno

Los valores dependen **exclusivamente de la TDMN**. Tabla verificada (reproducida idénticamente en el material de cátedra de la UNLP y en el capítulo 6 del manual ICPA):

### Tabla 1.4 — IRAM 11605, Tabla 1. K MÁX ADM, condición de INVIERNO [W/m²K]

| TDMN (°C) | A — Muros | A — Techos | **Sustentable — Muros** | **Sustentable — Techos** | B — Muros | B — Techos | C — Muros | C — Techos |
|---|---|---|---|---|---|---|---|---|
| −10 | 0,26 | 0,23 | 0,48 | 0,42 | 0,69 | 0,60 | 1,19 | 1,00 |
| −9 | 0,27 | 0,23 | 0,50 | 0,42 | 0,72 | 0,61 | 1,23 | 1,00 |
| −8 | 0,28 | 0,24 | 0,51 | 0,44 | 0,74 | 0,63 | 1,28 | 1,00 |
| −7 | 0,29 | 0,25 | 0,53 | 0,45 | 0,77 | 0,65 | 1,33 | 1,00 |
| **−6** | **0,30** | **0,26** | **0,55** | **0,47** | **0,80** | **0,67** | **1,39** | **1,00** |
| −5 | 0,31 | 0,27 | 0,57 | 0,48 | 0,83 | 0,69 | 1,45 | 1,00 |
| −4 | 0,32 | 0,28 | 0,60 | 0,50 | 0,87 | 0,72 | 1,52 | 1,00 |
| −3 | 0,33 | 0,29 | 0,62 | 0,52 | 0,91 | 0,74 | 1,59 | 1,00 |
| −2 | 0,35 | 0,30 | 0,65 | 0,54 | 0,95 | 0,77 | 1,67 | 1,00 |
| −1 | 0,36 | 0,31 | 0,68 | 0,56 | 0,99 | 0,80 | 1,75 | 1,00 |
| ≥ 0 | 0,38 | 0,32 | 0,69 | 0,58 | 1,00 | 0,83 | 1,85 | 1,00 |

*Para valores intermedios de TDMN, interpolar linealmente. **Santa Rosa cae exactamente en la línea de −6,0: no hay que interpolar.***

**Qué significa cada nivel** (criterio de la norma, verificado): los niveles se definen por el **salto máximo admisible entre la temperatura superficial interior del cerramiento y la temperatura del aire interior**, medida a 1,50 m del piso en el centro del local:

| Nivel | Temperatura interior de confort | Δθ máximo superficie-aire | Lectura |
|---|---|---|---|
| **A — Recomendado** | 22 °C | **1,0 K** | La pared "no se siente". No hay asimetría radiante |
| **Sustentable** | — | — | Nivel intermedio incorporado en la actualización de la norma `[VERIFICAR en IRAM 11605 edición vigente]` |
| **B — Medio** | 20 °C | **2,5 K** | La pared se siente algo fría al tacto pero no molesta |
| **C — Mínimo** | 18 °C | **4,0 K** | Pared perceptiblemente fría; asimetría radiante en el borde del disconfort |

> El **Nivel C es un piso de habitabilidad, no un objetivo de proyecto.** Con TDMN −6,0 el Nivel C admite un muro de K = 1,39: eso es peor que un muro de ladrillo hueco 18 revocado con 5 mm de aislante. **El estudio no proyecta en Nivel C.**

---

## 1.5 K máximos admisibles de IRAM 11605 — verano

Los valores dependen de la **zona bioambiental**, no de la TDMX. Tabla verificada:

### Tabla 1.5 — IRAM 11605, Tablas 2 y 3. K MÁX ADM, condición de VERANO [W/m²K]

| Zona bioambiental | A — Muros | A — Techos | Sust. — Muros | Sust. — Techos | B — Muros | B — Techos | C — Muros | C — Techos |
|---|---|---|---|---|---|---|---|---|
| I y II | 0,45 | 0,18 | 0,78 | 0,31 | 1,10 | 0,45 | 1,80 | 0,72 |
| **III y IV** | **0,50** | **0,19** | **0,88** | **0,34** | **1,25** | **0,48** | **2,00** | **0,76** |

**Hipótesis de la norma para obtener estos valores** (verificadas): radiación solar homogénea de **900 W/m² en techos y 400 W/m² en paredes**, coeficiente de absorción α = 0,7, y temperatura interior de confort de **27 °C para la Zona IV** (28 °C para la III) con temperatura exterior de diseño de **32 °C** (34 °C para la III). Los saltos superficie-aire admitidos son los mismos: 1 / 2,5 / 4 K para A / B / C.

> **Advertencia de la norma, textual:** *"La verificación debe realizarse **SIMULTÁNEAMENTE** para ambas condiciones (invierno y verano), excepto para las zonas bioambientales V y VI, donde solo se exige invierno."* **Santa Rosa debe verificar invierno Y verano.**

**Cuál manda en cada elemento, en Santa Rosa:**

| Elemento | Nivel | K adm invierno | K adm verano | **MANDA** |
|---|---|---|---|---|
| **Muros** | A | **0,30** | 0,50 | **INVIERNO** |
| **Muros** | B | **0,80** | 1,25 | **INVIERNO** |
| **Techos** | A | 0,26 | **0,19** | **VERANO** |
| **Techos** | B | 0,67 | **0,48** | **VERANO** |

> ### PRIMERA CONCLUSIÓN DE PROYECTO
> **El muro se dimensiona por invierno. La cubierta se dimensiona por verano.** Y como el admisible de verano en techos (0,19 / 0,48) es mucho más severo que el de muros (0,50 / 1,25), la propia estructura de la norma reproduce la recomendación de IRAM 11603 para Zona IV: **la cubierta lleva del orden del doble de aislante que el muro.**
>
> Relación de espesores que resulta en la práctica: **muro 100 mm de EPS / techo 170–180 mm de EPS para Nivel A**; **muro 30 mm / techo 60 mm para Nivel B**. Exactamente 2:1 en los dos casos.

---

## 1.6 Corrección por color: la decisión gratuita de mayor impacto

**Regla de IRAM 11605, apartados 5.3.2 y 5.3.3** (verificada): los valores de la Tabla 1.5 corresponden a superficies exteriores con α = 0,7 ± 0,1.

| Coeficiente de absorción α | Corrección en **MUROS** | Corrección en **TECHOS** |
|---|---|---|
| **α < 0,6** (colores claros) | **+20 %** (admite más K) | **+30 %** |
| α = 0,7 ± 0,1 (medios) | sin corrección | sin corrección |
| **α > 0,8** (colores oscuros) | **−15 %** (exige menos K) | **−20 %** |

### Tabla 1.6 — Coeficientes de absorción solar α (verificado, IRAM 11605 Tabla 3)

| Material | α | | Pintura | Claro | Mediano | Oscuro |
|---|---|---|---|---|---|---|
| Ladrillo común | 0,70 | | amarillo | 0,30 | 0,50 | 0,70 |
| Ladrillos negros u oscuros | 0,75–0,85 | | castaño claro (beige) | 0,35 | 0,55 | 0,90 |
| **Ladrillos rojos claros** | **0,50–0,60** | | castaño | 0,45 | 0,75 | 0,98 |
| Hormigón a la vista | 0,70 | | rojo | 0,65 | 0,80 | 0,90 |
| Hormigón a la vista texturado | 0,80 | | verde | 0,40 | 0,70 | 0,85 |
| Hormigón con cemento blanco | 0,50 | | azul | 0,40 | 0,75 | 0,90 |
| Revoque | 0,55 | | gris | 0,45 | 0,65 | 0,75 |
| **Revoque claro** | **0,40** | | anaranjado | 0,40 | 0,60 | 0,75 |
| Marfil / blanco | 0,40–0,50 | | rosa | 0,45 | 0,55 | 0,70 |
| **Baldosas rojas** | **0,85** | | púrpura | 0,60 | 0,80 | 0,90 |
| Fibrocemento | 0,60 | | aluminio puro | — | 0,45 | — |
| **Aluminio anodizado natural** | **0,45** | | **negro** | — | — | **0,95** |
| Aluminio envejecido | 0,80 | | | | | |
| **Chapa galvanizada** | **0,50** | | | | | |
| **Tejas cerámicas rojas** | **0,75–0,85** | | | | | |

### Cómo se traduce en espesor de aislante — cubierta

| Terminación de cubierta | α | K adm Nivel B verano | EPS necesario sobre losa de viguetas | Diferencia |
|---|---|---|---|---|
| Membrana con foil de aluminio, pintura blanca | **< 0,6** | 0,48 × 1,30 = **0,624** | **40 mm** | **base** |
| Membrana geotextil gris media, teja clara | 0,7 | **0,480** | **60 mm** | +20 mm |
| Membrana negra, teja roja oscura, baldosón rojo | **> 0,8** | 0,48 × 0,80 = **0,384** | **80 mm** | **+40 mm** |

> ### SEGUNDA CONCLUSIÓN DE PROYECTO
> **Especificar la cubierta clara vale 40 mm de EPS en toda la superficie de techo, y no cuesta nada.**
>
> Con TDMX = 38,8 °C y máxima absoluta de 42,1 °C, en una casa de una planta donde el techo es el 40–45 % de la envolvente, **la terminación clara de cubierta no es una opción estética: es un ítem de la memoria técnica**. Membrana con foil de aluminio, o pintura acrílica reflectiva blanca sobre membrana, o teja de color claro. Y su mantenimiento (repintado cada 4–6 años si es pintura) debe figurar en el manual de uso de la vivienda, porque el beneficio se pierde cuando la superficie se ensucia.
>
> **Cuidado con la trampa inversa:** la teja cerámica roja tradicional tiene α = 0,75–0,85. Si el ensayo o la ficha da α > 0,8, **el admisible de Nivel B cae a 0,384 y hay que poner 80 mm en lugar de 60**. Una cubierta de teja "porque es lo que se usa" cuesta 40 mm de aislante más que una cubierta clara.

---

## 1.7 TABLA MAESTRA: valores de proyecto para Santa Rosa

### Tabla 1.7 — LOS NÚMEROS CONTRA LOS QUE SE VERIFICA TODO EN ESTE DOCUMENTO

| Elemento | Condición | **Nivel A** | **Nivel Sustentable** | **Nivel B** | Nivel C |
|---|---|---|---|---|---|
| **MUROS** | Invierno (TDMN −6,0) — **manda** | **0,30** | 0,55 | **0,80** | 1,39 |
| MUROS | Verano (zona III/IV) | 0,50 | 0,88 | 1,25 | 2,00 |
| MUROS | Verano, muro claro α < 0,6 (+20 %) | 0,60 | 1,06 | 1,50 | 2,40 |
| MUROS | Verano, muro oscuro α > 0,8 (−15 %) | 0,43 | 0,75 | 1,06 | 1,70 |
| **TECHOS** | Invierno (TDMN −6,0) | 0,26 | 0,47 | 0,67 | 1,00 |
| **TECHOS** | **Verano (zona III/IV) — manda** | **0,19** | **0,34** | **0,48** | 0,76 |
| TECHOS | Verano, cubierta clara α < 0,6 (+30 %) | **0,247** | 0,442 | **0,624** | 0,988 |
| TECHOS | Verano, cubierta oscura α > 0,8 (−20 %) | **0,152** | 0,272 | **0,384** | 0,608 |
| **PISO en contacto con terreno** | (IRAM 11604 Tabla 2) | — | — | — | — |
| **PUENTE TÉRMICO** | K_pt ≤ 1,5 × K_muro | ≤ **0,45** | ≤ 0,83 | ≤ **1,20** | ≤ 2,09 |
| PUENTE TÉRMICO | si hay puentes cada ≤ 1,7 m: K_pt ≤ 1,35 × K_muro | ≤ 0,41 | ≤ 0,74 | ≤ 1,08 | ≤ 1,88 |

> **Nótese que con cubierta clara el verano SIGUE mandando en techos:** 0,247 (verano corregido) < 0,26 (invierno) en Nivel A, y 0,624 < 0,67 en Nivel B. **No hay ningún caso en Santa Rosa en que el invierno mande en la cubierta.**

### OBJETIVO DE PROYECTO DEL ESTUDIO

| | Objetivo | Piso contractual |
|---|---|---|
| **Muros** | **K ≤ 0,30 W/m²K** (Nivel A) | K ≤ 0,80 (Nivel B) |
| **Techos** | **K ≤ 0,19–0,25 W/m²K** (Nivel A, según α) | K ≤ 0,48 (Nivel B, α medio) |
| **Piso** | Aislación **total** (Pp = 0,93 W/m) | Aislación **perimetral** (Pp = 1,08 W/m) |
| **Ventanas** | K ≤ 2,13 (RPT + DVH low-e), categoría **K4/K3** IRAM 11507-4 | K ≤ 2,82 (RPT + DVH), **K4** |
| **Infiltración** | Clasificación **IRAM A2** o mejor | **IRAM A1** |
| **Coeficiente G** | G_cal ≤ 0,80 × G_adm | **G_cal ≤ G_adm** |
| **fRsi en todo encuentro** | ≥ **0,80** (ver §7) | ≥ 0,80 |

---

## 1.8 Pisos: la norma que hay que usar es la 11604, no la 11605

**IRAM 11605 no tabula K máximo admisible para pisos en contacto con el terreno.** Esto confunde permanentemente y lleva a dos errores opuestos: ignorar el piso, o intentar aplicarle el K de techos.

**El tratamiento normativo del piso está en IRAM 11604:2001, apartado 6.5** (texto verificado):

> *"Las pérdidas por el piso se calculan **por metro lineal del perímetro del piso en contacto con los muros exteriores**."*
> *Nota 4: "Solamente se calcula la pérdida por el piso en contacto con el suelo **contiguo a la envolvente vertical**."*

### Tabla 1.8 — IRAM 11604:2001, Tabla 2. Pérdidas por el piso en contacto con el terreno (Pp), en **W/m** de perímetro

| Zona bioambiental | **Sin aislación** | **Aislación perimetral** | **Aislación total** |
|---|---|---|---|
| I y II | 1,28 | 1,00 | 0,85 |
| **III y IV** | **1,38** | **1,08** | **0,93** |
| V y VI | 1,48 | 1,17 | 1,00 |

**Definiciones de la norma (verificadas):**

- **6.5.3.2 Aislación perimetral:** *"capa de material aislante térmico con un **R = 0,7 m²K/W**, un **ancho mínimo de 50 cm** y una densidad aparente comprendida entre **25 kg/m³ y 120 kg/m³**. La capa puede ser incorporada en **posición vertical u horizontal**."*
- **6.5.3.3 Aislación total:** *"capa de material aislante térmico con un **R = 0,7 m²K/W** y una densidad aparente comprendida entre 25 y 120 kg/m³, **sobre toda la superficie del piso**, colocada en forma horizontal."*
- **6.5.2.2:** locales calefaccionados en planta baja adyacentes a locales **no** calefaccionados → **50 %** de los valores de la tabla (zonas III a VI).
- **6.5.2.4:** pisos en contacto **directo con el aire exterior** (voladizo, sobre cochera abierta) → no se usa esta tabla: se calcula **K por IRAM 11601 con flujo descendente** y se multiplica por el **área**.
- **Nota 9:** *"En localidades con suelos muy densos y alta transmitancia térmica, o con suelos muy húmedos o nivel de la napa freática muy cercano a la superficie, las pérdidas por el piso serán mayores que las indicadas en la tabla 2. **En estos casos se recomienda el uso de aislación perimetral en las zonas III y IV**"*.

> **Aplicación a Santa Rosa.** El suelo loéssico pampeano es un limo eólico de estructura abierta; **seco es poco conductor, pero al saturarse su conductividad sube fuertemente** (comparar en la tabla de λ: arena seca 0,30 → con 10 % de humedad 0,93 → saturada 1,88 W/m·K). Sumado a que **el agua es el enemigo principal de la fundación en loess** y a que cualquier pérdida de cañería o vereda con contrapendiente satura el suelo bajo la casa, **se adopta como criterio del estudio la aislación perimetral como mínimo, y la total cuando hay losa radiante.** Es exactamente lo que recomienda la Nota 9.

**Espesor de aislante para R = 0,7 m²K/W:**

| Aislante | λ (W/m·K) | e calculado | **e a adoptar** | Apto para enterrar |
|---|---|---|---|---|
| **XPS** | 0,033 *(verificar en ficha)* | 23,1 mm | **30 mm** | **SÍ — es el único** |
| EPS 25 kg/m³ | 0,033 | 23,1 mm | 30 mm | No en contacto con humedad permanente |
| EPS 20 kg/m³ | 0,035 | 24,5 mm | 30 mm | No |
| EPS 30 kg/m³ | 0,032 | 22,4 mm | 25–30 mm | No |
| PUR proyectado protegido | 0,024 | 16,8 mm | 20 mm | Con protección |

> **El espesor que pide la norma para el piso es sorprendentemente chico: 30 mm de XPS.** Es el ítem de mejor relación beneficio/costo de toda la envolvente (ver §9). No hay excusa para omitirlo.

---

## 1.9 Exigencia normativa provincial y municipal en La Pampa

### Estado verificado

| Instrumento | Situación | Fuente / estado |
|---|---|---|
| **Ley provincial de acondicionamiento térmico de edificios (tipo Ley 13.059 de Buenos Aires)** | **No se encontró ninguna ley de La Pampa análoga a la Ley 13.059/03 bonaerense**, ni adhesión provincial a ella | Búsqueda sin resultado positivo. `[VERIFICAR en el Digesto de la Provincia de La Pampa y con el Colegio de Arquitectos de La Pampa antes de afirmarlo en un pliego]` |
| **Programa Nacional de Etiquetado de Viviendas (PRONEV)** | **La Pampa ESTÁ adherida.** Figura entre las provincias registradas al programa creado por Res. 5/2023 y con implementación por Res. 418/2023 de la Secretaría de Energía | Verificado en fuentes oficiales y de prensa institucional |
| **Obligatoriedad del etiquetado** | **El PRONEV es nacional y de adhesión voluntaria por jurisdicción. La obligatoriedad la establece cada provincia por ley propia** (Santa Fe fue la primera en sancionarla). **No se encontró ley pampeana que lo haga obligatorio** | `[VERIFICAR si La Pampa sancionó ley de obligatoriedad posterior a la fecha de este documento]` |
| **Código de Edificación de Santa Rosa** | **Ordenanza 1581/1995**, modificada por **Ordenanza 6445/2020**. **No se pudo acceder al texto** (el sitio del Concejo Deliberante devolvió 403 y el del CPITLP sólo enlaza un PDF no legible) | **`[VERIFICAR OBLIGATORIAMENTE: solicitar el texto vigente al Concejo Deliberante o al CPITLP y revisar si el capítulo de instalaciones o de condiciones de habitabilidad incorpora exigencias de acondicionamiento térmico, IRAM 11601/11605 o etiquetado.]`** |
| **IRAM 11507-6 — etiquetado de ventanas** | Vigente desde mayo de 2018, **de carácter voluntario** | Verificado en documentación del sector |

### Criterio del estudio ante el vacío normativo

> **La ausencia de exigencia municipal no es un permiso: es una responsabilidad profesional trasladada al proyectista.**
>
> 1. **Piso contractual del estudio: Nivel B de IRAM 11605** (muros 0,80 / techos 0,48), que es lo que la Ley 13.059 de Buenos Aires exige como máximo admisible. Si un proyecto bonaerense no puede construirse por debajo de eso, no hay razón técnica para que uno pampeano —con un clima **más frío** (GD18 1.394 contra ~1.150-1.200 del AMBA) y **más ventoso**— se construya peor.
> 2. **Objetivo del estudio: Nivel A** (0,30 / 0,19). Con 1.394 GD18 el repago es razonable (ver §9).
> 3. **Carpinterías:** adoptar como piso el criterio del Decreto 1030/2010 reglamentario de la Ley 13.059 (verificado): **clasificación IRAM A1** de infiltración de aire para aberturas en edificios de hasta 10 m, y **categoría de aislación térmica K5** como mínimo según IRAM 11507-4. **En Santa Rosa se eleva a A2 / K4**, por régimen de vientos más severo (VM 10,1 invierno / 12,5 verano) y TDMN más baja.
> 4. **Documentación a producir aunque nadie la pida:** planilla de cálculo de K por elemento (IRAM 11601), planilla de verificación de condensación superficial e intersticial (IRAM 11625/11630) y planilla de coeficiente G (IRAM 11604). Son las tres planillas que exige el decreto bonaerense y son las que permiten defender el proyecto ante un comitente, una tasación o un reclamo.
> 5. **Etiquetar la vivienda aunque sea voluntario.** La Pampa está adherida al PRONEV; el etiquetado se calcula por **IRAM 11900**, que produce un **Índice de Prestaciones Energéticas (IPE) en kWh/m²·año** cubriendo calefacción, refrigeración, ACS e iluminación, y lo traduce a una letra de A a G. Es un diferencial comercial y una verificación externa gratuita del proyecto. `[VERIFICAR el procedimiento y el registro de profesionales certificadores habilitados en La Pampa]`

---

## 1.10 Datos de entrada del cálculo (resistencias, λ, Rt)

Todos los K de este documento se calculan con `RT = Rsi + Σ(e/λ) + Σ R_cámaras + Rse` y `K = 1/RT`, según IRAM 11601.

### Tabla 1.9 — Resistencias térmicas superficiales (IRAM 11601) — **verificado**

| Situación | Rsi (m²K/W) | Rse (m²K/W) |
|---|---|---|
| **Muro**, flujo horizontal | **0,13** | 0,04 |
| **Techo, INVIERNO**, flujo ascendente | **0,10** | 0,04 |
| **Techo, VERANO**, flujo descendente | **0,17** | 0,04 |
| **Piso**, flujo descendente | **0,17** | 0,04 |
| **Verificación de condensación superficial** (IRAM 11625, paño central) | **0,17** | 0,04 |
| **Verificación en punto singular** (IRAM 11630) | **0,25 / 0,34 / 0,50** | 0,04 |

> **El detalle que casi todo el mundo omite:** en cubierta, **la verificación de verano se hace con flujo DESCENDENTE y Rsi = 0,17**, no con 0,10. Son 0,07 m²K/W de diferencia — equivalen a 2,5 mm de EPS, es poco, pero cambia el K en el tercer decimal y a veces decide una verificación al límite. **En este documento las cubiertas se calculan dos veces: K_inv con Rsi = 0,10 y K_ver con Rsi = 0,17.**

### Tabla 1.10 — Cámaras de aire y espacios áticos — **verificado**

| Situación | R (m²K/W) |
|---|---|
| **Cámara de aire en muro**, no ventilada, 20 mm, alta emitancia (IRAM 11601) | 0,16 |
| Cámara de aire en muro, no ventilada, 50–100 mm, alta emitancia | **0,17** |
| Cámara de aire en muro, no ventilada, 20 mm, **una cara de baja emitancia** | 0,37 |
| Cámara de aire en muro — valor simplificado de uso corriente | 0,15 |
| Cámara de aire en techo, no ventilada, 30–40 mm, flujo descendente | 0,14 |
| **Espacio ático no ventilado, cubierta de TEJA** | **0,23 (invierno) / 0,17 (verano)** |
| **Espacio ático no ventilado, cubierta de CHAPA** | **0,35 (invierno) / 0,22 (verano)** |
| Cámara de aire **ventilada** | **≈ 0** a efectos de cálculo (su beneficio es de verano y no lo captura el método estacionario) |

> **Tres lecturas.** (1) Una cámara de aire de 5 cm aporta 0,17 m²K/W = **6 mm de EPS**: la cámara no es aislación, es un lugar donde poner aislación. (2) Más allá de 20 mm la cámara **deja de mejorar** (la convección interna anula la ganancia). (3) Los valores con superficie de baja emitancia (foil) **sólo valen si la superficie permanece limpia**, cosa que la propia norma advierte que no puede asegurarse en obra: **no apoyar una verificación en ellos**.

### Tabla 1.11 — Conductividades térmicas λ usadas en este documento (IRAM 11601, salvo indicación)

| Material | ρ (kg/m³) | **λ (W/m·K)** |
|---|---|---|
| Revoque de mortero, **exterior** | 1800–1200 | **1,16** |
| Revoque de mortero, **interior** | 1900 | **0,93** |
| Azotado hidrófugo (mortero 1:3 con hidrófugo) | 2000 | 1,13 |
| Enlucido de yeso | 600–1000 | 0,31–0,44 |
| Placa de roca de yeso 12,5 mm | 1000 | **0,44** |
| Hormigón armado normal | **2400** | **1,63** |
| Hormigón de cascote (contrapiso) | 1600 | **0,76** |
| **Ladrillo cerámico macizo** | 1600 / 1800 | **0,81 / 0,91** |
| **HCCA (hormigón celular curado en autoclave)** | 465–680 | **0,12** *(INTI/CECON, ensayo sobre muestra; IRAM 11601 da 0,12 a 680 kg/m³)* |
| Madera de pino, perpendicular a fibras | 400–600 | 0,13–0,19 |
| Machimbre de pino (valor INTI usado por la Cámara de la Cerámica Roja) | 500 | 0,19 |
| OSB / multilaminado | 600 | 0,11–0,13 |
| **Teja cerámica** | — | **0,76** |
| Membrana asfáltica (mín. 7 mm) | 2000 | 0,70 |
| Baldosa cerámica | — | 0,70 |
| Grava / canto rodado | 1500–1800 | 0,93 |
| **Acero** | 7800 | **58** |
| **Aluminio** | 2700 | **204** |
| PVC rígido | 1350 | 0,16 |
| **EPS en planchas** | 15 / 20 / 25 / 30 | **0,037 / 0,035 / 0,033 / 0,032** |
| **EPS grafitado** | 15 / 20 | **0,034 / 0,031** |
| **XPS** | 28–40 | **≈ 0,033** *(VERIFICAR en ficha — no está en IRAM 11601)* |
| **Lana de vidrio** | 15-18 / 19-30 / 31-45 / 46-100 | **0,040 / 0,037 / 0,034 / 0,033** |
| **Lana de roca** | 30-50 / 51-70 / 71-150 | **0,042 / 0,040 / 0,038** |
| **PUR proyectado protegido entre barreras de vapor** | 30–60 | **0,022** |
| PUR proyectado protegido entre frenos de vapor | 30–60 | **0,024** |
| PUR en placas sin protección | 30–60 | 0,027 |
| Celulosa proyectada / insuflada | 30–60 | ≈ 0,038–0,042 *(VERIFICAR en ficha)* |
| Revoque termoaislante con perlas de EPS | — | 0,076 |
| Mortero de perlita con cemento | 300 / 400 | 0,088 / 0,093 |

### Tabla 1.12 — Resistencia térmica Rt de mampuestos y forjados (no se calcula con e/λ) — **verificado**

| Elemento | Espesor | **Rt (m²K/W)** | Fuente |
|---|---|---|---|
| **Ladrillo cerámico hueco 8×18×33** | 8 cm | ≈ 0,26 | `[VERIFICAR en IRAM 11601, Tabla A.2]` |
| **Ladrillo cerámico hueco 12×18×33** | 12 cm | **0,360** | IRAM 11601, tabla de bloques |
| **Ladrillo cerámico hueco 18×18×33** | 18 cm | **0,410** | IRAM 11601, tabla de bloques |
| **Ladrillo cerámico PORTANTE 18×19×33** | 18 cm | **0,430** | IRAM 11601 Tabla 7, citado por la Cámara Industrial de la Cerámica Roja |
| Ladrillo cerámico portante 12 (conductancia C = 2,33 W/m²K) | 12 cm | 0,429 | Ensayo INTI/CECON citado en ASADES 2004. `[VERIFICAR: coincide sospechosamente con el de 18 cm]` |
| **Bloque de hormigón hueco 19–20 cm** | 19–20 cm | **≈ 0,20** | **`[VERIFICAR en IRAM 11601, Tabla A.3]`** — valor coherente con el K de 2,44 del muro revocado que figura en la bibliografía del estudio |
| **Forjado de viguetas + bovedilla CERÁMICA**, h = 12 cm, e/e 50–60 | 12 cm | **0,19** | IRAM 11601, Tabla A.4 |
| Forjado con bovedilla de **mortero**, h = 12 cm | 12 cm | 0,13 | ídem |
| **Forjado con bovedilla de EPS**, h = 12 / 15 / 17 / 20 cm, capa de compresión 5 cm | — | **0,54 / 0,60 / 0,63 / 0,68** | ídem |
| Forjado cerámico de 16 cm, L = 50 cm: **K = 2,79** (verano, incluye Rsi y Rse) → Rt = 1/2,79 − 0,17 − 0,04 | 16 cm | **0,148** | IRAM 11601 Tabla 9, ejemplo de la Cámara de la Cerámica Roja |

> **Cómo se usa la Tabla A.4 (forjados):** la norma tabula **K**, no R. El procedimiento correcto (verificado en IRAM 11601): *"se calcula la resistencia térmica total (1/K) y se **restan** las resistencias térmicas superficiales interior y exterior, obteniendo de esta forma la resistencia térmica del forjado."* **Es un error frecuente sumar el K tabulado como si fuera una R de capa.**

---

# 2. MUROS

> **El punto de partida.** El muro estándar del interior argentino —ladrillo cerámico hueco de 18 cm revocado en ambas caras— tiene **K = 1,58 W/m²K**. Con TDMN de −6,0 °C, el Nivel C (el mínimo de la norma) admite 1,39. **El muro estándar de Santa Rosa no verifica ni el nivel mínimo de la norma.** No es que esté lejos del nivel recomendado: está fuera de la norma por completo. Todo lo que sigue parte de ahí.

**Capas comunes a las soluciones de mampostería revocada** (se repiten en todos los cálculos):

| Capa | e (m) | λ (W/m·K) | R (m²K/W) |
|---|---|---|---|
| Rsi (flujo horizontal) | — | — | 0,130 |
| Revoque fino interior (yeso/cal) | 0,005 | 0,70 | 0,007 |
| Revoque grueso interior | 0,020 | 0,93 | 0,022 |
| Azotado hidrófugo | 0,005 | 1,13 | 0,004 |
| Revoque grueso exterior | 0,020 | 1,16 | 0,017 |
| Revoque fino exterior | 0,005 | 1,16 | 0,004 |
| Rse | — | — | 0,040 |
| **Subtotal capas comunes** | | | **0,224** |

---

## 2.1 Las doce soluciones calculadas

### M1 — Ladrillo cerámico hueco 18, revocado (EL ESTÁNDAR, que NO verifica)

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,130 |
| 1 | Revoque fino interior | 0,005 | 0,70 | 0,007 |
| 2 | Revoque grueso interior | 0,020 | 0,93 | 0,022 |
| 3 | **Ladrillo hueco 18×18×33** | 0,180 | *Rt tabulado* | **0,410** |
| 4 | Azotado hidrófugo | 0,005 | 1,13 | 0,004 |
| 5 | Revoque grueso exterior | 0,020 | 1,16 | 0,017 |
| 6 | Revoque fino exterior | 0,005 | 1,16 | 0,004 |
| — | Rse | — | — | 0,040 |
| | **RT** | **0,235 m** | | **0,634** |

```
K = 1 / 0,634 = 1,58 W/m²K
```

| Nivel | K adm | ¿Verifica? | Exceso |
|---|---|---|---|
| A (0,30) | | **NO** | **5,3 veces** |
| Sustentable (0,55) | | **NO** | 2,9 veces |
| B (0,80) | | **NO** | 2,0 veces |
| **C (1,39)** | | **NO** | **1,14 veces** |

> **Un muro que no llega ni al mínimo legal de la peor norma disponible.** Y con este muro, la temperatura superficial interior con 20 °C adentro y −6 afuera es de **13,4 °C** (ver §7): **condensa** contra el aire interior a 20 °C y 70 % de HR (rocío 14,4 °C). No es un problema de eficiencia: es un problema de patología.

---

### M2 — Hueco 18 + trasdosado interior de EPS 50 mm + placa de yeso

Composición de interior a exterior: placa de roca de yeso 12,5 + EPS 50 + hueco 18 + azotado + revoque exterior.

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,130 |
| 1 | Placa de roca de yeso | 0,0125 | 0,44 | 0,028 |
| 2 | **EPS 20 kg/m³** | 0,050 | 0,035 | **1,429** |
| 3 | Ladrillo hueco 18 | 0,180 | — | 0,410 |
| 4 | Azotado hidrófugo | 0,005 | 1,13 | 0,004 |
| 5 | Revoque grueso + fino exterior | 0,025 | 1,16 | 0,021 |
| — | Rse | — | — | 0,040 |
| | **RT** | **0,27 m** | | **2,062** |

```
K = 1 / 2,062 = 0,49 W/m²K   →   verifica B (0,80) y Sustentable (0,55). NO verifica A.
```

> ### PERO: esta solución es una trampa
> 1. **No resuelve ningún puente térmico.** Columnas, encadenados, dinteles, antepechos y el encuentro con la cubierta siguen a K ≈ 2,9–3,5. Con K_muro = 0,49, el admisible de puente es **0,74**: un encadenado desnudo lo excede 4 a 5 veces. **La verificación de puentes térmicos de IRAM 11605 no se cumple.**
> 2. **Anula la inercia térmica.** Toda la masa del muro (unos 250 kg/m²) queda del lado frío del aislante. El interior "ve" 12,5 mm de placa de yeso. En un clima con 14,4 K de amplitud estival, **se está tirando a la basura la mejor herramienta pasiva del lugar** (§8.3).
> 3. **Condensa intersticialmente si no lleva barrera de vapor.** El cálculo de §7.3 muestra que sin barrera de vapor la cara interior del ladrillo queda a **−0,1 °C** con una presión de vapor por encima de la de saturación. Con barrera de vapor del lado cálido (Sd ≥ 10 m) el problema se elimina, pero entonces hay que ejecutarla continua y sellada en cada caja de electricidad y en cada pase — cosa que casi nunca se hace.
> 4. **Roba superficie útil:** 6,3 cm por muro exterior. En una casa de 130 m² con 48 m de perímetro son **≈ 3,0 m² de superficie cubierta perdida**.
>
> **Uso legítimo:** rehabilitación de una casa existente cuya fachada no se puede tocar (medianera, patrimonio, restricción de línea municipal). **En obra nueva no hay ninguna razón para elegirla.**

---

### M3 — Hueco 18 + SATE/EIFS de EPS 60 mm (el piso contractual)

Composición de interior a exterior: revoques + hueco 18 + adhesivo + EPS 60 + revoque base con malla + revestimiento acrílico.

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,130 |
| 1 | Revoque fino interior | 0,005 | 0,70 | 0,007 |
| 2 | Revoque grueso interior | 0,020 | 0,93 | 0,022 |
| 3 | Ladrillo hueco 18 | 0,180 | — | 0,410 |
| 4 | Mortero adhesivo | 0,005 | 1,16 | 0,004 |
| 5 | **EPS 20 kg/m³** | **0,060** | **0,035** | **1,714** |
| 6 | Revoque base + malla + revestimiento | 0,008 | 0,93 | 0,009 |
| — | Rse | — | — | 0,040 |
| | **RT** | **0,278 m** | | **2,336** |

```
K = 1 / 2,336 = 0,43 W/m²K   →   verifica B (0,80) con 46 % de margen. NO verifica A ni Sustentable.
```

**Ventaja decisiva: resuelve TODOS los puentes térmicos de la envolvente vertical**, porque el aislante pasa por delante de columnas, encadenados, dinteles y antepechos sin interrupción.

---

### M4 — Hueco 18 + SATE de EPS 100 mm — **LA RECOMENDACIÓN**

Idéntica a M3 con EPS de 100 mm:

```
R_EPS = 0,100 / 0,035 = 2,857 m²K/W
RT = 0,622 (base sin EPS) + 2,857 = 3,479 m²K/W
K = 1 / 3,479 = 0,287 ≈ 0,29 W/m²K   →   VERIFICA NIVEL A (0,30)
```
*(base sin EPS = 0,130 + 0,007 + 0,022 + 0,410 + 0,004 + 0,009 + 0,040 = 0,622)*

**Variante con EPS grafitado de 90 mm** (λ = 0,031): R = 2,903 → RT = 3,525 → **K = 0,284 → Nivel A con 10 mm menos de espesor.**

Espesor total del muro: **31,8 cm** (25 cm con EPS de 60 mm).

---

### M5 — Muro doble de hueco 12 + EPS 50 en cámara + hueco 18

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,130 |
| 1 | Revoque fino + grueso interior | 0,025 | — | 0,029 |
| 2 | **Hoja interior: hueco 12×18×33** | 0,120 | — | **0,360** |
| 3 | Azotado hidrófugo | 0,005 | 1,13 | 0,004 |
| 4 | **EPS 20 kg/m³ adherido a la hoja interior** | 0,050 | 0,035 | **1,429** |
| 5 | Cámara de aire residual (drenaje) | 0,020 | — | 0,160 |
| 6 | **Hoja exterior: hueco 18×18×33** | 0,180 | — | 0,410 |
| 7 | Revoque grueso + fino exterior | 0,025 | 1,16 | 0,021 |
| — | Rse | — | — | 0,040 |
| | **RT** | **0,425 m** | | **2,583** |

```
K = 1 / 2,583 = 0,39 W/m²K   →   verifica B holgadamente. NO verifica A (0,30).
```

**Variante sin aislante (cámara vacía de 50 mm):** RT = 0,130+0,029+0,360+0,004+0,170+0,410+0,021+0,040 = **1,164 → K = 0,86**. Verifica B (0,80)... **NO: 0,86 > 0,80. No verifica ni Nivel B.** Con TDMN −6,0 el clásico "muro doble con cámara de aire" de 33 cm **deja de verificar**. Con TDMN −2,7 (el dato equivocado) verificaba justo. **Éste es el ejemplo más claro de por qué resolver la discrepancia de TDMN no era un detalle académico.**

> **Muro de 42,5 cm de espesor para un K peor que el de M4 (31,8 cm).** Doble mano de obra de albañilería, doble tiempo, doble andamio, y encima **no resuelve los puentes térmicos de la estructura**: las columnas y los encadenados siguen atravesando las dos hojas. Su única ventaja real es la interrupción capilar y la inercia. **En obra nueva no se recomienda.**

---

### M6 — Muro doble con hoja exterior de ladrillo visto

Para cuando el comitente quiere ladrillo a la vista.

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,130 |
| 1 | Revoque fino + grueso interior | 0,025 | — | 0,029 |
| 2 | Hoja interior: hueco 18 | 0,180 | — | 0,410 |
| 3 | Azotado hidrófugo sobre cara exterior de la hoja interior | 0,005 | 1,13 | 0,004 |
| 4 | **EPS 20 kg/m³** | 0,050 | 0,035 | **1,429** |
| 5 | **Cámara ventilada y drenada** | 0,020 | — | **0,000** *(ventilada: no computa)* |
| 6 | Hoja exterior: ladrillo macizo visto | 0,120 | 0,91 | 0,132 |
| — | Rse | — | — | 0,040 |
| | **RT** | **0,40 m** | | **2,174** |

```
K = 1 / 2,174 = 0,46 W/m²K   →   verifica B. NO verifica A.
```
Con EPS de 80 mm: R = 2,286 → RT = 3,031 → **K = 0,33** (roza el A). Con EPS de 100 mm: RT = 3,602 → **K = 0,28 → Nivel A.**

> **Nota de cálculo honesta:** si la cámara se declara **ventilada** (llagas abiertas arriba y abajo, que es lo correcto para un ladrillo visto en clima con heladas), **su resistencia térmica no se computa** y, en rigor, tampoco debería computarse íntegramente la hoja exterior. El cálculo de arriba ya descuenta la cámara pero mantiene la hoja: es una hipótesis conservadora-optimista intermedia. `[VERIFICAR el criterio de fachada ventilada de IRAM 11601 antes de usar este número en una verificación formal; el criterio internacional (EN ISO 6946) descuenta la cámara Y la hoja exterior, y toma Rse = 0,13 en su lugar.]` Con ese criterio estricto: RT = 0,130+0,029+0,410+0,004+1,429+0,13 = 2,132 → K = 0,47. Prácticamente lo mismo.

---

### M7 — Ladrillo cerámico PORTANTE 18 + SATE de EPS 80 mm

El muro portante elimina columnas y encadenados intermedios: **menos puentes térmicos de origen, menos hormigón, obra más rápida.**

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,130 |
| 1 | Revoque fino + grueso interior | 0,025 | — | 0,029 |
| 2 | **Ladrillo portante 18×19×33** | 0,180 | *Rt tabulado* | **0,430** |
| 3 | Mortero adhesivo | 0,005 | 1,16 | 0,004 |
| 4 | **EPS 20 kg/m³** | **0,080** | 0,035 | **2,286** |
| 5 | Revoque base + malla + revestimiento | 0,008 | 0,93 | 0,009 |
| — | Rse | — | — | 0,040 |
| | **RT** | **0,298 m** | | **2,928** |

```
K = 1 / 2,928 = 0,34 W/m²K   →   verifica B ampliamente. Roza A (0,30) sin alcanzarlo.
```
**Con EPS de 100 mm:** RT = 3,499 → **K = 0,286 → Nivel A.**

> Ésta es, técnicamente, **la mejor solución de mampostería tradicional** para una casa de una planta: el portante de 18 hace de estructura y de cerramiento, se elimina el encadenado de encuentro con columnas, y el SATE resuelve lo poco que queda (encadenado superior y dinteles). **Su viabilidad depende de que el proyecto acepte la disciplina modular y de muros portantes que exige el sistema** (ver el capítulo de estructuras).

---

### M8 — Bloque de hormigón 19 + SATE de EPS 80 mm

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,130 |
| 1 | Revoque fino + grueso interior | 0,025 | — | 0,029 |
| 2 | **Bloque de hormigón hueco 19** | 0,190 | *Rt tabulado* | **0,200** `[VERIFICAR]` |
| 3 | Mortero adhesivo | 0,005 | 1,16 | 0,004 |
| 4 | **EPS 20 kg/m³** | 0,080 | 0,035 | **2,286** |
| 5 | Revoque base + malla + revestimiento | 0,008 | 0,93 | 0,009 |
| — | Rse | — | — | 0,040 |
| | **RT** | **0,308 m** | | **2,698** |

```
K = 1 / 2,698 = 0,37 W/m²K   →   verifica B. NO verifica A.
```
**Sin SATE** (bloque 19 revocado): RT = 0,130+0,029+0,200+0,004+0,021+0,040 = 0,424 → **K = 2,36. No verifica NADA** (ni el Nivel C, que admite 1,39). El bloque de hormigón desnudo es, térmicamente, **el peor mampuesto de uso corriente**: λ del hormigón 1,63 contra un cerámico hueco con cámaras.
**Para Nivel A:** RT_nec = 3,333; base sin EPS = 0,412; ΔR = 2,921 → **EPS 102 mm → adoptar 110 mm.**

> **El bloque de hormigón no es una mala elección: es una elección que obliga a aislar por fuera, sin excepción.** Su ventaja es el costo del mampuesto, la velocidad de levante y la modulación; su desventaja térmica se compensa íntegramente con el SATE, que de todos modos había que poner.

---

### M9 — HCCA (hormigón celular curado en autoclave) 20 cm, revocado

λ del HCCA = **0,12 W/m·K** (ensayo INTI/CECON sobre muestra comercial, ρ = 465 kg/m³; IRAM 11601 tabula 0,12 para ρ = 680).

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,130 |
| 1 | Revoque interior fino (el HCCA no necesita grueso) | 0,010 | 0,93 | 0,011 |
| 2 | **Bloque HCCA** | **0,200** | **0,12** | **1,667** |
| 3 | Revestimiento exterior | 0,005 | 1,16 | 0,004 |
| — | Rse | — | — | 0,040 |
| | **RT** | **0,215 m** | | **1,852** |

```
K = 1 / 1,852 = 0,54 W/m²K   →   verifica B (0,80) y Sustentable (0,55, justo). NO verifica A.
```

**HCCA de 30 cm:** R = 2,500 → RT = 2,685 → **K = 0,37.** Verifica B holgadamente, no A.
**HCCA 20 + SATE de EPS 60 mm:** RT = 1,852 + 1,714 = 3,566 → **K = 0,28 → Nivel A**, con 27 cm de espesor total.

> **Ventaja irrepetible del HCCA:** es el único mampuesto que resuelve el puente térmico estructural **por sí mismo**, porque su λ (0,12) es sólo 3,4 veces mayor que la del EPS y 13,6 veces menor que la del hormigón armado. Un encadenado embebido en un muro de HCCA sigue siendo un puente, pero de severidad muy inferior.
> **Desventajas a controlar:** absorción de agua alta (exige revestimiento exterior impermeable pero permeable al vapor, y protección durante el acopio en obra); resistencia a compresión menor; fijaciones específicas (tarugos de expansión largos); mano de obra que hay que instruir. En el estudio comparativo de ASADES (2004, Berazategui) un muro doble de HCCA de 15+15 con cámara dio **K = 0,35**, **164 kg/m²** (contra 456 y 368 kg/m² de las alternativas de mampostería tradicional aislada) y un costo de **$123/m² contra $156 y $163**, con un tiempo de ejecución de **2 h 45 min/m² contra 4 h 40 y 4 h 15**. *Los valores absolutos de 2004 no sirven; **la relación —HCCA ≈ 25 % más barato y 40 % más rápido que el muro doble tradicional— sí es el orden de magnitud a verificar hoy en Santa Rosa.*** `[VERIFICAR con presupuesto real y con la disponibilidad local del mampuesto.]`

---

### M10 — Steel framing con EPS exterior continuo

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,130 |
| 1 | Placa de roca de yeso 12,5 | 0,0125 | 0,44 | 0,028 |
| 2 | *(barrera de vapor — no computa térmicamente)* | — | — | 0,000 |
| 3 | **Lana de vidrio entre montantes** | **0,090** | **0,040** | **2,250** |
| 4 | OSB estructural | 0,0111 | 0,13 | 0,085 |
| 5 | *(membrana hidrófuga respirante — no computa)* | — | — | 0,000 |
| 6 | **EPS exterior continuo** | **0,030** | 0,035 | **0,857** |
| 7 | Revoque base + malla + revestimiento | 0,008 | 0,93 | 0,009 |
| — | Rse | — | — | 0,040 |
| | **RT en el PAÑO** | **0,17 m** | | **3,399** |

```
K_paño = 1 / 3,399 = 0,29 W/m²K   →   Nivel A EN EL PAÑO
```

> ### PERO EL K DEL PAÑO NO ES EL K DEL MURO
> El montante de acero galvanizado (λ = **58 W/m·K**) atraviesa los 90 mm de lana **cada 40–60 cm**. Es un puente térmico lineal, repetitivo y masivo. Con EPS exterior de sólo 30 mm el K real del muro compuesto queda **típicamente un 20–40 % por encima del K del paño**, es decir del orden de **0,35–0,41 W/m²K**. **`[VERIFICAR con cálculo bidimensional (THERM, Flixo, HTflux) o con el método de puentes térmicos de IRAM 11605 — no es aceptable presentar el K del paño como K del muro.]`**
>
> **Corrección:** llevar el EPS exterior continuo a **50 mm** (R = 1,429): RT_paño = 3,971 → **K_paño = 0,25**, y el K compuesto queda del orden de 0,29–0,32, es decir **Nivel A real**. En Santa Rosa, **50 mm de EPS exterior continuo es el mínimo en steel framing**, no 30.
>
> **Y el problema de fondo en este clima: masa cero.** Un muro de steel framing pesa unos 40–50 kg/m² contra 250–450 de la mampostería. Con 14,4 K de amplitud estival, la casa se calienta y se enfría rápido: se pierde el enfriamiento pasivo por inercia + ventilación nocturna (§8.3). Si se elige steel framing, **la masa hay que recuperarla en el piso**: contrapiso de hormigón de espesor generoso, sin aislante entre él y el interior, y tabiques interiores de mampostería en los locales que reciben sol directo.

---

### M11 — Hormigón armado 20 cm + SATE de EPS 100 mm

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,130 |
| 1 | **Hormigón armado** | 0,200 | **1,63** | **0,123** |
| 2 | Mortero adhesivo | 0,005 | 1,16 | 0,004 |
| 3 | **EPS 20 kg/m³** | 0,100 | 0,035 | **2,857** |
| 4 | Revoque base + malla + revestimiento | 0,008 | 0,93 | 0,009 |
| — | Rse | — | — | 0,040 |
| | **RT** | **0,313 m** | | **3,163** |

```
K = 1 / 3,163 = 0,32 W/m²K   →   verifica B ampliamente, roza A.
```
**Sin SATE:** RT = 0,130 + 0,123 + 0,021 + 0,040 = 0,314 → **K = 3,18.** El muro entero es un puente térmico. (Valor coherente con el K = 3,42 que publica el manual ICPA para hormigón de 20 cm sin aislación.)
**Con EPS de 120 mm:** RT = 3,734 → **K = 0,268 → Nivel A con margen.**

> Sólo tiene sentido en una casa de una planta si hay una razón formal fuerte (hormigón visto interior, sistema industrializado en sitio). **La masa es excelente y queda del lado correcto (interior) con el SATE.**

---

### M12 — Alta prestación: portante 18 + SATE de EPS grafitado 150 mm

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,130 |
| 1 | Revoque fino + grueso interior | 0,025 | — | 0,029 |
| 2 | Ladrillo portante 18×19×33 | 0,180 | — | 0,430 |
| 3 | Mortero adhesivo | 0,005 | 1,16 | 0,004 |
| 4 | **EPS grafitado 20 kg/m³** | **0,150** | **0,031** | **4,839** |
| 5 | Revoque base + doble malla + revestimiento | 0,010 | 0,93 | 0,011 |
| — | Rse | — | — | 0,040 |
| | **RT** | **0,37 m** | | **5,483** |

```
K = 1 / 5,483 = 0,182 W/m²K   →   Nivel A con 65 % de margen. Territorio de casa pasiva.
```

> **Cuándo tiene sentido.** Cuando el comitente quiere consumo casi nulo, o cuando la casa se calefacciona con electricidad (bomba de calor sin gas de red), donde el costo del kWh justifica espesores mayores. El límite práctico del SATE de EPS ronda los 150–200 mm (por encima hay que revisar fijaciones y estabilidad del sistema): **`[VERIFICAR en el manual del fabricante el espesor máximo admitido, la cantidad de fijaciones por m² para la zona de viento de La Pampa y la clasificación de reacción al fuego del sistema completo.]`**
>
> **Advertencia específica del EPS grafitado:** no dejarlo expuesto al sol antes de revocarlo — el grafito absorbe radiación, la placa se calienta y se deforma. En obra pampeana de verano hay que colocarlo y revocarlo el mismo día, o cubrirlo con media sombra.

---

## 2.2 Tabla comparativa general

### Tabla 2.1 — DOCE SOLUCIONES DE MURO PARA SANTA ROSA (TDMN = −6,0 °C)

| # | Solución | Espesor total | **RT** | **K (W/m²K)** | A (0,30) | Sust (0,55) | B (0,80) | C (1,39) | **Puentes térmicos** | Masa interior | Costo rel. | MO local |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **M1** | Hueco 18 + revoques | 23,5 cm | 0,634 | **1,58** | ✗ | ✗ | ✗ | **✗** | Todos sin resolver | Alta | **100** | Total |
| **M2** | Hueco 18 + EPS 50 int. + placa | 27 cm | 2,062 | **0,49** | ✗ | ✓ | ✓ | ✓ | **Ninguno resuelto** | **Nula (perdida)** | 145 | Alta |
| **M3** | Hueco 18 + **SATE EPS 60** | 27,8 cm | 2,336 | **0,43** | ✗ | ✗ | **✓** | ✓ | **Todos resueltos** | Alta | 165 | Media |
| **M4** | **Hueco 18 + SATE EPS 100** | 31,8 cm | 3,479 | **0,29** | **✓** | ✓ | ✓ | ✓ | **Todos resueltos** | Alta | 185 | Media |
| **M5** | Doble: hueco 12 + EPS 50 + hueco 18 | 42,5 cm | 2,583 | **0,39** | ✗ | ✓ | ✓ | ✓ | Parcialmente | Alta | 215 | Total |
| M5b | Doble con cámara de aire vacía 50 | 40 cm | 1,164 | **0,86** | ✗ | ✗ | **✗** | ✓ | Parcialmente | Alta | 195 | Total |
| **M6** | Doble c/hoja exterior de ladrillo visto + EPS 50 | 40 cm | 2,174 | **0,46** | ✗ | ✓ | ✓ | ✓ | Parcialmente | Alta | 240 | Alta |
| **M7** | **Portante 18 + SATE EPS 80** | 29,8 cm | 2,928 | **0,34** | ✗ (roza) | ✓ | ✓ | ✓ | **Casi ninguno de origen** | Alta | 175 | Media-baja |
| M7b | Portante 18 + SATE EPS 100 | 31,8 cm | 3,499 | **0,29** | **✓** | ✓ | ✓ | ✓ | **Casi ninguno de origen** | Alta | 190 | Media-baja |
| **M8** | Bloque hormigón 19 + SATE EPS 80 | 30,8 cm | 2,698 | **0,37** | ✗ | ✓ | ✓ | ✓ | **Todos resueltos** | Muy alta | 160 | Media |
| M8b | Bloque hormigón 19 + revoques (sin SATE) | 24 cm | 0,424 | **2,36** | ✗ | ✗ | ✗ | **✗** | Todos sin resolver | Muy alta | 95 | Alta |
| **M9** | **HCCA 20 + revoques** | 21,5 cm | 1,852 | **0,54** | ✗ | ✓ (justo) | ✓ | ✓ | **Muy reducidos** | Media | 130 | **Baja** |
| M9b | HCCA 30 + revoques | 31,5 cm | 2,685 | **0,37** | ✗ | ✓ | ✓ | ✓ | Muy reducidos | Media | 165 | **Baja** |
| M9c | HCCA 20 + SATE EPS 60 | 27 cm | 3,566 | **0,28** | **✓** | ✓ | ✓ | ✓ | **Todos resueltos** | Media | 190 | Baja |
| **M10** | Steel framing + lana 90 + **EPS ext. 50** | 19 cm | 3,971 (paño) | **0,25 paño / ≈0,30 real** | **✓** *(verificar)* | ✓ | ✓ | ✓ | **Montantes: sólo con EPS continuo** | **Nula** | 170 | **Baja** |
| M10b | Steel framing + lana 90 + EPS ext. 30 | 17 cm | 3,399 (paño) | 0,29 paño / **≈0,35–0,41 real** | **✗ real** | ✓ | ✓ | ✓ | Insuficiente | Nula | 155 | Baja |
| **M11** | HºAº 20 + SATE EPS 100 | 31,3 cm | 3,163 | **0,32** | ✗ (roza) | ✓ | ✓ | ✓ | **Todos resueltos** | **Máxima** | 230 | Baja |
| **M12** | Portante 18 + **SATE EPS grafitado 150** | 37 cm | 5,483 | **0,182** | **✓✓** | ✓ | ✓ | ✓ | **Todos resueltos** | Alta | 240 | Media-baja |

**Costo relativo:** índice con M1 = 100, materiales + mano de obra por m² de muro terminado, **estimación de orden de magnitud del estudio, no cotización.** `[VERIFICAR con presupuesto de corralones y contratistas de Santa Rosa antes de usarlo en una comparación de anteproyecto.]`
**MO local = disponibilidad de mano de obra capacitada en Santa Rosa** (evaluación cualitativa del estudio, a contrastar con el mercado local real).

### Lecturas de la tabla

1. **Cuatro soluciones no verifican ningún nivel:** M1 (hueco 18 revocado), M8b (bloque de hormigón revocado), M5b (muro doble con cámara vacía, que se cae al Nivel C con la TDMN correcta) y, si se es riguroso, M10b (steel framing con EPS de 30 mm). **Las tres primeras son las tres soluciones más construidas en Santa Rosa.**
2. **Ninguna solución sin aislante llega ni al Nivel C.** No existe el muro de mampostería que verifique en Santa Rosa sin aislante añadido, con la única excepción parcial del HCCA de 20 cm — que es un mampuesto **que es aislante**.
3. **El espesor no es el problema:** M4 (SATE de 100 mm) da K = 0,29 con 31,8 cm de espesor total; M5 (muro doble con EPS de 50) da K = 0,39 con 42,5 cm. **11 cm más de muro para un 34 % peor de K.**
4. **La columna de puentes térmicos decide.** M2 tiene mejor K que M9 y es peor solución: no resuelve un solo puente, pierde la inercia y arrastra riesgo de condensación intersticial.

---

## 2.3 Espesor de aislante necesario por objetivo

Método: `RT_nec = 1/K_obj` ; `ΔR = RT_nec − RT_base` ; `e = ΔR × λ`.

### Tabla 2.2 — Muro de ladrillo hueco 18 (RT_base sin aislante = 0,622 con acabado SATE)

| Objetivo | K adm | RT_nec | ΔR | **EPS λ 0,035** | **EPS graf. λ 0,031** | Lana roca λ 0,038 | **PUR λ 0,024** | XPS λ 0,033 |
|---|---|---|---|---|---|---|---|---|
| **Nivel C** (1,39) | 1,39 | 0,719 | 0,097 | 3,4 → **10 mm** | 3,0 → 10 mm | 3,7 → 10 mm | 2,3 → 10 mm | 3,2 → 10 mm |
| **Nivel B** (0,80) | 0,80 | 1,250 | 0,628 | 22,0 → **30 mm** | 19,5 → 20 mm | 23,9 → 30 mm | 15,1 → 20 mm | 20,7 → 30 mm |
| **Nivel Sustentable** (0,55) | 0,55 | 1,818 | 1,196 | 41,9 → **50 mm** | 37,1 → 40 mm | 45,4 → 50 mm | 28,7 → 30 mm | 39,5 → 40 mm |
| **Nivel A** (0,30) | 0,30 | 3,333 | 2,711 | 94,9 → **100 mm** | 84,0 → **90 mm** | 103,0 → 110 mm | 65,1 → **70 mm** | 89,5 → 90 mm |
| Casa pasiva (0,15) | 0,15 | 6,667 | 6,045 | 211,6 → 220 mm | 187,4 → 190 mm | 229,7 → 230 mm | 145,1 → 150 mm | 199,5 → 200 mm |

> ### LA CURVA DE RENDIMIENTO DEL AISLANTE ES FUERTEMENTE DECRECIENTE
> - De "no verifica nada" (K 1,58) a **Nivel C**: **10 mm** de EPS.
> - De Nivel C a **Nivel B**: **20 mm más**.
> - De Nivel B a **Nivel A**: **70 mm más**.
> - De Nivel A a casa pasiva: **120 mm más**.
>
> **Los primeros 30 mm hacen la mitad del trabajo.** Pero en Santa Rosa, con 1.394 GD18, los 70 mm adicionales que llevan de B a A siguen teniendo repago razonable (§9), porque el EPS es barato y el gas se consume 5 meses por año durante 50 años.

---

## 2.4 Costo relativo, mano de obra y disponibilidad en Santa Rosa

### Tabla 2.3 — Factores no térmicos de la decisión

| Solución | Disponibilidad de material en Santa Rosa | Mano de obra capacitada | Riesgo de ejecución | Mantenimiento | Robustez a impactos |
|---|---|---|---|---|---|
| **M1 Hueco 18** | Total | Total | Nulo | Bajo | Alta |
| **M3/M4 SATE sobre hueco 18** | Alta (EPS local; sistema SATE completo por distribuidor) | **Media — es la restricción real.** El SATE es un sistema, no un rubro | **Medio-alto**: doble malla en esquinas de vano, fijaciones según zona de viento, retornos en jambas | Medio: revestimiento acrílico a repintar cada 8–12 años | **Baja en planta baja** — exige zócalo reforzado o placa de mortero armado hasta 2 m |
| **M5/M6 Muro doble** | Total | Total | Bajo (oficio conocido), salvo la limpieza de la cámara | Bajo | Alta |
| **M7 Portante cerámico** | Media-alta | Media-baja: **exige replanteo modular y control de trabas** | Medio | Bajo | Alta |
| **M8 Bloque de hormigón** | Alta | Alta | Bajo | Bajo | Alta |
| **M9 HCCA** | **Media — verificar distribuidor en Santa Rosa** | **Baja: hay que instruir a la cuadrilla** (mortero adhesivo de junta delgada, herramientas específicas, corte con serrucho) | Medio | Bajo | Media: se marca con golpes |
| **M10 Steel framing** | Media | **Baja en obra unifamiliar** | Alto si la cuadrilla no es del sistema | Bajo | Baja |
| **M11 Hormigón armado** | Alta | Alta (hormigonera local) | Medio (encofrado) | Bajo | Máxima |

> **La restricción real en Santa Rosa no es el K: es quién ejecuta el SATE.** El sistema es sencillo pero implacable con los descuidos: sin refuerzo diagonal de malla en las esquinas de vano fisura, sin retorno del aislante sobre el marco aparece el puente térmico y la mancha de moho en la jamba, sin tapón de EPS sobre la cabeza de las espigas aparece el "efecto lunares" en la fachada, y con espigas insuficientes se despega con viento. **Consecuencia de gestión: en el primer proyecto con SATE, presupuestar la capacitación del contratista con el departamento técnico del fabricante y exigir el manual de colocación como parte del pliego.**

---

## 2.5 LA RECOMENDACIÓN POR DEFECTO

> ### MURO RECOMENDADO PARA UNA CASA DE UNA PLANTA EN SANTA ROSA
>
> ## **M4 — Ladrillo cerámico hueco 18 revocado + SATE de EPS de 100 mm**
> ## **K = 0,29 W/m²K — Nivel A de IRAM 11605**
>
> **Composición completa (de interior a exterior):**
> ```
> Revoque fino a la cal 5 mm
> Revoque grueso 20 mm
> LADRILLO CERÁMICO HUECO 18×18×33, junta de mortero 1:1:4
> Mortero adhesivo cementicio del sistema SATE, 5 mm (cordón perimetral + pelladas)
> PLACA DE EPS DE 20 kg/m³, 100 mm, colocada a junta trabada
> Fijación mecánica con espigas plásticas de expansión larga (para ladrillo hueco),
>   cantidad y longitud según manual del fabricante y zona de viento CIRSOC 102
>   [VERIFICAR], cabeza rehundida y tapada con tapón de EPS
> Capa base de mortero 3–5 mm con MALLA DE FIBRA DE VIDRIO ANTIÁLCALI embebida
>   + refuerzo diagonal de 30×50 cm a 45° en cada esquina de vano
> Segunda capa de mortero 2–3 mm
> Imprimación
> Revestimiento acrílico/siliconado texturado 1,5–3 mm, PERMEABLE AL VAPOR, color claro
> ```
> **Espesor total: 31,8 cm.** Variante equivalente: EPS grafitado de 90 mm (K = 0,284, 30,8 cm).
>
> ### Por qué ésta y no otra
>
> | Criterio | Por qué gana |
> |---|---|
> | **Verifica Nivel A** | 0,29 ≤ 0,30. No "casi": verifica |
> | **Resuelve TODOS los puentes térmicos de la envolvente vertical** | El aislante pasa continuo por delante de columnas, encadenados, dinteles y antepechos. **Es la única familia de soluciones que permite cumplir el requisito K_pt ≤ 1,5 × K_muro de IRAM 11605**, que con K_muro = 0,29 exige K_pt ≤ 0,45 — imposible con cualquier aislación interior o en cámara |
> | **Deja la masa del lado correcto** | Los 250 kg/m² del muro quedan en contacto térmico con el aire interior: la inercia funciona, y con 14,4 K de amplitud estival eso vale tanto como el aislante |
> | **Estanqueidad al aire** | La capa base continua de mortero armado con malla es, de hecho, la barrera al aire de la fachada. En una ciudad con viento medio de 10–12,5 km/h y ráfagas muy superiores, esto es tan importante como el K |
> | **No pierde superficie útil** | El espesor crece hacia afuera |
> | **Oficio disponible** | La albañilería es la de siempre; sólo el SATE exige capacitación, y es un rubro de un único contratista |
> | **Escalable** | El mismo detalle sirve para 60, 100 o 150 mm: si el presupuesto aprieta se arranca en 60 (Nivel B, K 0,43) sin cambiar ningún otro detalle de obra |
>
> ### Alternativas admitidas y cuándo
>
> | Situación | Solución |
> |---|---|
> | **El comitente quiere ladrillo visto** | **M6** con EPS de 100 mm en la cámara (K ≈ 0,28) y cámara ventilada y drenada. Cuesta ~30 % más y 8 cm más de espesor |
> | **El proyecto admite muros portantes y se quiere ahorrar estructura** | **M7b** (portante 18 + SATE EPS 100, K = 0,29). Técnicamente igual o mejor: menos hormigón, menos puentes de origen |
> | **Se busca velocidad de obra y bajo peso (fundación en loess)** | **M9c** (HCCA 20 + SATE EPS 60, K = 0,28, 27 cm). Muro liviano: menos carga sobre una fundación en suelo colapsable |
> | **Presupuesto ajustado, se acepta Nivel B** | **M3** (SATE EPS 60, K = 0,43). **Nunca por debajo de 30 mm de EPS**, que es el mínimo para el Nivel B |
> | **Rehabilitación con fachada intocable** | **M2**, con barrera de vapor continua del lado cálido y tratamiento explícito de cada puente térmico |
>
> ### Lo que NO se acepta en un proyecto del estudio
> - Muro de hueco 18 revocado sin aislante (**no verifica ni Nivel C**).
> - Bloque de hormigón revocado sin aislante (**K = 2,36**).
> - Muro doble con cámara de aire vacía (**K = 0,86: con la TDMN correcta ya no verifica Nivel B**).
> - "Aislación: manta reflectiva de 10 mm" como único aislante. Un reflectivo **no tiene λ útil**: aporta, en el mejor caso tabulado por IRAM 11601, **0,21 m²K/W = 7 mm de EPS**, y sólo si hay cámara de aire y la superficie permanece limpia — cosa que la propia norma dice que no puede asegurarse en obra.

---

# 3. TECHO

> **En una casa de una planta, el techo es la envolvente.** En la casa de referencia de este documento (130 m² cubiertos, 16 × 8 m, 2,60 m de altura) la superficie de techo es de **130 m²** contra **106,8 m² de muro neto** y **18 m² de ventanas**. El techo es el **41 %** de toda la superficie de envolvente y, con la construcción corriente, **el 41 % de la pérdida de calor por conducción**. En un edificio de departamentos ese mismo techo se reparte entre diez plantas y se vuelve irrelevante; acá es el ítem número uno.
>
> Y en verano es peor: la cubierta recibe **900 W/m² de radiación de diseño** según las hipótesis de IRAM 11605, contra **400 W/m² de los muros**. **Un techo mal resuelto en Santa Rosa hace inviable cualquier dimensionamiento razonable de equipo de frío.**

## 3.1 Por qué en cubierta manda el verano

| Nivel | K adm invierno (TDMN −6,0) | K adm verano (zona III/IV) | **Manda** | Con α<0,6 (verano +30 %) | ¿Sigue mandando el verano? |
|---|---|---|---|---|---|
| A | 0,26 | **0,19** | verano | **0,247** | **Sí** (0,247 < 0,26) |
| Sustentable | 0,47 | **0,34** | verano | 0,442 | **Sí** (0,442 < 0,47) |
| B | 0,67 | **0,48** | verano | **0,624** | **Sí** (0,624 < 0,67) |
| C | 1,00 | **0,76** | verano | 0,988 | **Sí** (0,988 < 1,00) |

> **No hay ningún caso en Santa Rosa, con ningún color, en que el invierno mande en la cubierta. La cubierta se dimensiona SIEMPRE por verano.** Y el verano se verifica con **flujo descendente**, es decir **Rsi = 0,17** (no 0,10). En este capítulo cada solución trae los dos K.

## 3.2 Las nueve soluciones calculadas

### T1 — Losa de viguetas + bovedilla cerámica + contrapiso + membrana (SIN aislación)

| # | Capa (de interior a exterior) | e (m) | λ | R |
|---|---|---|---|---|
| — | **Rsi** | — | — | **0,10 inv / 0,17 ver** |
| 1 | Revoque de cielorraso | 0,015 | 0,93 | 0,016 |
| 2 | **Forjado de viguetas + bovedilla cerámica h=12** | 0,17 | *Rt tabulado* | **0,190** |
| 3 | Contrapiso de pendiente de cascote | 0,080 | 0,76 | 0,105 |
| 4 | Carpeta hidrófuga | 0,020 | 1,13 | 0,018 |
| 5 | Membrana asfáltica 4 mm | 0,004 | 0,70 | 0,006 |
| — | Rse | — | — | 0,040 |
| | **RT** | | | **0,475 inv / 0,545 ver** |

```
K_invierno = 1 / 0,475 = 2,11 W/m²K
K_VERANO   = 1 / 0,545 = 1,83 W/m²K
```

| Nivel | A (0,19) | Sust. (0,34) | B (0,48) | **C (0,76)** |
|---|---|---|---|---|
| ¿Verifica? | ✗ | ✗ | ✗ | **✗ — 2,4 veces por encima** |

> **La cubierta plana estándar argentina está 2,4 veces por encima del nivel MÍNIMO de la norma en verano y 2,1 veces en invierno.** Un techo así, con 130 m², pierde en invierno **238 W/K**: más que todos los muros de la casa juntos.

---

### T2 — Losa de viguetas + **EPS sobre la losa** + contrapiso de pendiente + membrana

Es T1 con una plancha de EPS entre la losa y el contrapiso de pendiente. **El orden de capas correcto es: losa → barrera de vapor → EPS → contrapiso de pendiente → carpeta → membrana → protección clara.**

| e EPS (λ 0,035) | R del EPS | **RT verano** | **K verano** | **K invierno** | A (0,19) | A claro (0,247) | Sust. (0,34) | B (0,48) | B claro (0,624) |
|---|---|---|---|---|---|---|---|---|---|
| 40 mm | 1,143 | 1,688 | **0,59** | 0,62 | ✗ | ✗ | ✗ | ✗ | **✓** |
| **60 mm** | 1,714 | 2,259 | **0,443** | 0,457 | ✗ | ✗ | ✗ | **✓** | ✓ |
| 80 mm | 2,286 | 2,831 | **0,353** | 0,363 | ✗ | ✗ | ✗ (roza) | ✓ | ✓ |
| 90 mm | 2,571 | 3,116 | **0,321** | 0,330 | ✗ | ✗ | **✓** | ✓ | ✓ |
| **130 mm** | 3,714 | 4,259 | **0,235** | 0,241 | ✗ | **✓** | ✓ | ✓ | ✓ |
| **180 mm** | 5,143 | 5,688 | **0,176** | 0,180 | **✓** | ✓ | ✓ | ✓ | ✓ |

> **Con cubierta clara (α < 0,6), el Nivel A se alcanza con 130 mm de EPS en vez de 180 mm.** 50 mm de aislante en 130 m² de techo, ahorrados sólo por especificar membrana con foil de aluminio o pintura reflectiva blanca.

---

### T3 — Cubierta plana INVERTIDA (aislante sobre la impermeabilización)

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,10 inv / 0,17 ver |
| 1 | Revoque de cielorraso | 0,015 | 0,93 | 0,016 |
| 2 | **Losa maciza de HºAº** | 0,120 | 1,63 | 0,074 |
| 3 | Contrapiso de pendiente | 0,080 | 0,76 | 0,105 |
| 4 | Carpeta de nivelación | 0,020 | 1,13 | 0,018 |
| 5 | **Membrana (queda protegida, del lado cálido)** | 0,004 | 0,70 | 0,006 |
| 6 | **XPS** | **0,100** | **0,033** | **3,030** |
| 7 | Geotextil separador | — | — | 0,000 |
| 8 | Lastre de canto rodado lavado | 0,050 | 0,93 | 0,054 |
| — | Rse | — | — | 0,040 |
| | **RT** | | | **3,443 inv / 3,513 ver** |

```
K_verano = 1 / 3,513 = 0,285 W/m²K   →   verifica Sustentable (0,34) y B. NO verifica A (0,19).
```
**Con XPS de 140 mm:** R = 4,242 → RT_ver = 4,725 → **K = 0,212** → con canto rodado claro (α<0,6, adm 0,247) **verifica Nivel A**.
**Con XPS de 180 mm:** RT_ver = 5,938 → **K = 0,168** → **Nivel A absoluto.**

### Tabla 3.1 — Cubierta tradicional (caliente) vs. cubierta invertida en Santa Rosa

| | **TRADICIONAL (T2)** | **INVERTIDA (T3)** |
|---|---|---|
| Posición de la membrana | Arriba, expuesta a sol, UV y ciclo térmico completo | **Abajo, protegida por el aislante** |
| Rango térmico de trabajo de la membrana | De **−11 °C a más de +70 °C** en Santa Rosa | Rango estrecho, en torno a la temperatura interior |
| Vida útil de la membrana | Menor | **Mucho mayor** |
| Barrera de vapor | **Necesaria** bajo el aislante | **No necesaria** (la membrana es la barrera y está del lado cálido) |
| Aislante admisible | Cualquiera (queda protegido) | **Sólo XPS** (única absorción de agua suficientemente baja para trabajar mojado) |
| Peso | Menor | **Mayor: exige lastre** |
| Costo | Menor | Mayor (XPS + lastre) |
| **Riesgo pampeano específico** | Membrana expuesta al ciclo −11/+70 °C | **El XPS flota y vuela.** Sin lastre, la primera lluvia lo levanta y el primer viento fuerte lo saca |
| **Recomendación** | Aceptable en cubierta inaccesible, con membrana con foil de aluminio y barrera de vapor resuelta | **Preferida en azotea accesible y en cualquier cubierta donde el mantenimiento sea difícil** |

> **El lastre no es opcional.** En Santa Rosa hay que **calcular el lastre por succión de viento** (CIRSOC 102), no por costumbre. Mínimo habitual: 5 cm de canto rodado lavado de granulometría 20–40 mm, o baldosas sobre plots. `[VERIFICAR el peso mínimo con el agente de estructuras para la zona de viento de La Pampa.]`

---

### T4 — Losa con bovedilla de EPS + EPS sobre losa + **cubierta ventilada de chapa** por encima

El "doble techo": losa aislada e impermeabilizada, y sobre ella una cubierta liviana de chapa sobre estructura, separada por una **cámara de aire ventilada de 15–30 cm**.

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,10 inv / 0,17 ver |
| 1 | Revoque de cielorraso | 0,015 | 0,93 | 0,016 |
| 2 | **Forjado con bovedilla de EPS h=17** | 0,22 | *Rt tabulado* | **0,630** |
| 3 | **EPS sobre losa** | 0,080 | 0,035 | **2,286** |
| 4 | Carpeta + membrana | 0,024 | — | 0,006 |
| 5 | **Cámara de aire VENTILADA** | 0,20 | — | **0,000** *(ventilada: no computa)* |
| 6 | Chapa sinusoidal | — | 58 | 0,000 |
| — | Rse | — | — | 0,040 |
| | **RT** | | | **3,078 inv / 3,148 ver** |

```
K_verano = 1 / 3,148 = 0,318 W/m²K   →   verifica Sustentable (0,34) y B con amplio margen.
```

> ### EL NÚMERO SUBESTIMA MUCHO ESTA SOLUCIÓN
> El método estacionario de IRAM 11601 **le asigna resistencia cero a la cámara ventilada**, porque no puede computar lo que realmente hace: **interceptar la radiación solar antes de que llegue al aislante y evacuarla por convección**. En verano, la chapa superior llega a 60–70 °C, pero el aire de la cámara la barre y **la losa aislada nunca "ve" esa temperatura**. Es, en la práctica, **la mejor cubierta de verano posible en clima continental seco**, y la que mejor se lleva con la ventilación nocturna.
>
> **Su costo es el problema:** son dos cubiertas. Se justifica cuando el proyecto quiere el volumen de cubierta inclinada de chapa **y** la inercia y la seguridad de la losa; o cuando el techo tiene mucha superficie expuesta al oeste.
>
> **Requisitos de la cámara ventilada:** entrada de aire continua en el alero inferior y salida en la cumbrera o en el borde superior; **superficie libre de ventilación del orden del 0,5–1 % de la superficie de cubierta, repartida mitad abajo y mitad arriba** `[VERIFICAR contra el manual del sistema o la regla del fabricante de la chapa]`; rejilla antipájaros y antiinsectos en ambas; y **la cámara debe estar libre de obstrucciones que corten el tiro** (correas transversales, conductos).

---

### T5 — Techo de chapa sobre estructura (metálica o de madera) con lana de vidrio entre correas y cielorraso

La solución más frecuente en vivienda de una planta con techo inclinado o a un agua.

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,10 inv / 0,17 ver |
| 1 | Placa de roca de yeso 12,5 (cielorraso) | 0,0125 | 0,44 | 0,028 |
| 2 | **Barrera de vapor del lado cálido** (film de PE 200 μ o foil) | — | — | 0,000 |
| 3 | **Lana de vidrio entre y sobre correas** | **0,100** | **0,040** | **2,500** |
| 4 | **Espacio ático no ventilado, cubierta de chapa** | — | — | **0,35 inv / 0,22 ver** |
| 5 | Membrana hidrófuga respirante | — | — | 0,000 |
| 6 | Chapa sinusoidal o trapezoidal | — | 58 | 0,000 |
| — | Rse | — | — | 0,040 |
| | **RT** | | | **3,018 inv / 2,958 ver** |

```
K_invierno = 1 / 3,018 = 0,331 W/m²K
K_VERANO   = 1 / 2,958 = 0,338 W/m²K   →   verifica Sustentable (0,34) justo, y B con margen.
```

| e lana de vidrio (λ 0,040) | R | **K verano** | A (0,19) | A claro (0,247) | Sust. (0,34) | B (0,48) |
|---|---|---|---|---|---|---|
| 50 mm | 1,250 | **0,60** | ✗ | ✗ | ✗ | ✗ |
| **100 mm** | 2,500 | **0,338** | ✗ | ✗ | **✓** (justo) | ✓ |
| **150 mm** | 3,750 | **0,238** | ✗ | **✓** | ✓ | ✓ |
| **200 mm** | 5,000 | **0,183** | **✓** | ✓ | ✓ | ✓ |

> **Chapa galvanizada: α = 0,50 → cubierta clara → admisibles corregidos +30 %.** Con chapa galvanizada o prepintada blanca, **150 mm de lana de vidrio dan Nivel A**. Con chapa prepintada negra, gris oscuro o roja oscura (α > 0,8) el admisible A cae a **0,152** y el B a **0,384**: hacen falta **más de 200 mm**. **La chapa oscura es una decisión de 50 mm de lana en 130 m² de techo.**
>
> **Los cinco errores que arruinan esta cubierta:**
> 1. **Comprimir la lana.** Una lana de 100 mm aplastada a 60 mm por las correas pierde el 40 % de su R. Colocarla **entre correas y una segunda capa cruzada por encima**, o usar correas de altura suficiente.
> 2. **Omitir la barrera de vapor del lado cálido.** Con 20 °C y 70 % de HR adentro y −6 afuera, el vapor migra hacia arriba, atraviesa la lana y **condensa contra la cara interior fría de la chapa**. Gotea sobre el cielorraso y arruina la lana (la lana mojada **no recupera** su capacidad aislante). **La barrera de vapor va inmediatamente por encima del cielorraso, continua y sellada en cada perforación de luminaria.** Ver §7.4.
> 3. **Cerrar el ático.** El espacio entre la lana y la chapa debe estar **ventilado al exterior** para evacuar la humedad residual y el calor de verano; el valor de tabla de 0,35/0,22 es para ático **no** ventilado, y es la hipótesis conservadora de cálculo. Ventilarlo mejora el verano aunque no compute.
> 4. **Cañerías y conductos por encima de la lana.** Todo lo que pase por el ático queda **del lado frío**: caños de agua que se congelan con TMA de −11,3 °C, conductos de aire que pierden. Pasan **por debajo** de la aislación, o se aíslan por separado.
> 5. **Luminarias embutidas en el cielorraso.** Cada spot es un agujero en la barrera de vapor y en la aislación. Usar luminarias estancas aptas para contacto con aislación, o resolver la iluminación en un cielorraso técnico por debajo del plano de barrera de vapor.

---

### T6 — Panel sándwich chapa–poliuretano–chapa

| e del núcleo PUR (λ 0,024, protegido entre chapas que hacen de barrera de vapor) | R | **RT verano** | **K verano** | **K invierno** | A (0,19) | A claro (0,247) | Sust. (0,34) | B (0,48) |
|---|---|---|---|---|---|---|---|---|
| **50 mm** | 2,083 | 2,293 | **0,436** | 0,450 | ✗ | ✗ | ✗ | **✓** (justo) |
| **100 mm** | 4,167 | 4,377 | **0,228** | 0,232 | ✗ | **✓** | ✓ | ✓ |
| **150 mm** | 6,250 | 6,460 | **0,155** | 0,158 | **✓** | ✓ | ✓ | ✓ |

*Los K calculados coinciden con el valor de catálogo habitual para panel de 50 mm (≈ 0,43 W/m²K).* `[VERIFICAR el λ y el K declarados en la ficha técnica del panel efectivamente especificado, y su λ a largo plazo: el PUR envejece.]`

> **Ventajas:** una sola pieza aísla, impermeabiliza y estructura; montaje rapidísimo; sin puentes de correas dentro del aislante; barrera de vapor integrada (las dos chapas).
> **Desventajas en Santa Rosa:**
> - **Masa cero.** Sin ninguna inercia, la casa sigue instantáneamente la temperatura exterior. Muy malo para aprovechar los 14,4 K de amplitud estival.
> - **Las juntas son el punto débil**: térmico (puente lineal en cada solape), de estanqueidad al agua y al aire. Exigen el sistema de junta del fabricante ejecutado tal cual.
> - **Dilatación:** un faldón continuo de chapa expuesto a un rango de −11 a +70 °C se mueve varios milímetros por metro. Fijaciones con arandela y agujero ovalado según el fabricante.
> - **Ruido de lluvia y granizo.** En una casa, con granizo pampeano, es un tema real. Un cielorraso independiente por debajo lo mitiga (y agrega una cámara).

---

### T7 — Cubierta inclinada de TEJA sobre estructura de madera, con machimbre a la vista

La cubierta "de casa" con cielorraso de machimbre visto, la más pedida por los comitentes.

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,10 inv / 0,17 ver |
| 1 | **Machimbre de pino a la vista** | 0,013 | 0,19 | 0,068 |
| 2 | Techado / fieltro asfáltico (**barrera de vapor**) | 0,001 | 0,11 | 0,009 |
| 3 | **EPS entre clavaderas** | **0,100** | **0,035** | **2,857** |
| 4 | Cámara de aire de las clavaderas (no ventilada, 31 mm) | 0,031 | — | **0,140** |
| 5 | Teja cerámica | 0,013 | 0,76 | 0,017 |
| — | Rse | — | — | 0,040 |
| | **RT** | | | **3,231 inv / 3,301 ver** |

```
K_verano = 1 / 3,301 = 0,303 W/m²K
```

**Sensibilidad al color de la teja — esto es lo que hay que mirar:**

| e EPS | K verano | **Teja clara / engobada clara α<0,6** (B adm 0,624 / A adm 0,247) | **Teja media α=0,7** (B 0,48 / A 0,19) | **Teja roja oscura α>0,8** (B 0,384 / A 0,152) |
|---|---|---|---|---|
| 50 mm | 0,538 | ✓ B | ✗ | ✗ |
| **60 mm** | 0,463 | ✓ B | **✓ B (justo)** | **✗ NO verifica B** |
| **80 mm** | 0,357 | ✓ B | ✓ B | **✓ B (justo)** |
| 100 mm | 0,303 | ✓ B | ✓ B | ✓ B |
| 130 mm | 0,247 | **✓ A (justo)** | ✗ A | ✗ A |
| 180 mm | 0,189 | ✓ A | **✓ A** | ✗ A |

> ### LA TRAMPA DE LA TEJA ROJA
> La teja cerámica roja tradicional tiene **α = 0,75–0,85**. Si el ensayo o la ficha del producto la ubica por encima de 0,8, **el admisible de Nivel B baja de 0,48 a 0,384** y una cubierta con 60 mm de EPS —que verificaría con cualquier otro color— **deja de verificar**. Hay que ir a 80 mm.
> **`[VERIFICAR el coeficiente de absorción solar α de la teja efectivamente especificada en la ficha del fabricante. Es un dato que casi nunca se pide y que decide 20 mm de aislante en toda la cubierta.]`**
> **Recurso de proyecto:** teja de color claro, teja engobada clara, o teja de hormigón en tono claro. Baja el α, sube el admisible, ahorra aislante y baja la temperatura del ático.

---

### T8 — Cubierta inclinada de teja con **ático ventilado** y cielorraso horizontal aislado

La variante correcta cuando no se quiere el machimbre a la vista: la aislación va **horizontal sobre el cielorraso**, no siguiendo la pendiente. Se aísla mucha menos superficie (la del cielorraso, no la del faldón) y el ático ventilado hace de colchón.

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,10 inv / 0,17 ver |
| 1 | Placa de roca de yeso (cielorraso) | 0,0125 | 0,44 | 0,028 |
| 2 | **Barrera de vapor sobre el cielorraso** | — | — | 0,000 |
| 3 | **Lana de vidrio horizontal sobre el cielorraso** | **0,150** | **0,040** | **3,750** |
| 4 | **Espacio ático, cubierta de teja** | — | — | **0,23 inv / 0,17 ver** |
| 5 | Teja cerámica sobre listonado | 0,013 | 0,76 | 0,017 |
| — | Rse | — | — | 0,040 |
| | **RT** | | | **4,165 inv / 4,175 ver** |

```
K_verano = 1 / 4,175 = 0,240 W/m²K   →   con teja clara (adm A = 0,247) VERIFICA NIVEL A.
```

> **Ésta es la solución de mejor relación prestación/costo de todo el capítulo para una cubierta inclinada**, por una razón geométrica: en un techo a dos aguas con 30 % de pendiente, **el faldón tiene un 4–5 % más de superficie que el cielorraso horizontal**, y además el ático permite ventilar y pasar instalaciones sin perforar la aislación. Se aísla el plano chico, no el grande.
> **Exige:** ático **ventilado** (rejillas en alero y en cumbrera, superficie libre ≈ 1/300 de la superficie de cielorraso `[VERIFICAR criterio]`), pasarelas de inspección para no pisar el cielorraso, y **barrera de vapor continua sobre el cielorraso**, sellada en cada luminaria y en cada pase.

---

### T9 — Losa con bovedilla de EPS + EPS sobre losa (cubierta plana "económica de alta prestación")

Sustituye la bovedilla cerámica (Rt 0,19) por bovedilla de EPS (Rt 0,63 con h = 17 cm): **0,44 m²K/W gratis**, sin cambiar el proceso de obra.

| # | Capa | e (m) | λ | R |
|---|---|---|---|---|
| — | Rsi | — | — | 0,10 inv / 0,17 ver |
| 1 | Revoque de cielorraso | 0,015 | 0,93 | 0,016 |
| 2 | **Forjado con bovedilla de EPS h=17, capa de compresión 5 cm** | 0,22 | *Rt tabulado* | **0,630** |
| 3 | Barrera de vapor | — | — | 0,000 |
| 4 | **EPS sobre losa** | **0,080** | 0,035 | **2,286** |
| 5 | Contrapiso de pendiente | 0,080 | 0,76 | 0,105 |
| 6 | Carpeta hidrófuga | 0,020 | 1,13 | 0,018 |
| 7 | Membrana con foil de aluminio (α < 0,6) | 0,004 | 0,70 | 0,006 |
| — | Rse | — | — | 0,040 |
| | **RT** | | | **3,201 inv / 3,271 ver** |

```
K_verano = 1 / 3,271 = 0,306 W/m²K   →   Sustentable (0,34) ✓; con membrana clara, B (0,624) con mucho margen.
```
**Con EPS de 120 mm sobre la losa:** RT_ver = 4,414 → **K = 0,227** → con α < 0,6 (adm 0,247) **verifica Nivel A.**

> **Ojo con el peso del contrapiso de pendiente.** En una casa de una planta con 130 m² de losa, cada centímetro de contrapiso son ~2,6 toneladas. Con losa de viguetas hay que resolver la pendiente con el mínimo espesor posible (pendiente mínima **1,5 %** para membrana `[VERIFICAR contra el manual del fabricante de la membrana; muchos exigen 2 %]`) o dar la pendiente con la propia losa.

---

### T10 — Techo verde extensivo (mención)

Sustrato de 8–15 cm sobre drenaje y aislante. Aporta inercia, protección de la membrana y muy buen comportamiento de verano por evapotranspiración. **En Santa Rosa exige riego** (precipitación de verano de 380 mm concentrada en tormentas, con períodos secos y viento). No se desarrolla acá: ver `docs/05-construccion/tecnologia-constructiva.md` §6.3. `[VERIFICAR la carga admisible con el agente de estructuras: 100–150 kg/m² saturado en extensivo.]`

---

## 3.3 Tabla comparativa general de cubiertas

### Tabla 3.2 — NUEVE SOLUCIONES DE CUBIERTA PARA SANTA ROSA

| # | Solución | Aislante y espesor | **K verano** | K invierno | A (0,19) | Sust (0,34) | B (0,48) | **Comportamiento de verano** | Masa | Costo rel. |
|---|---|---|---|---|---|---|---|---|---|---|
| **T1** | Losa viguetas + bovedilla cerámica, sin aislar | — | **1,83** | 2,11 | ✗ | ✗ | **✗** *(ni C)* | **Pésimo.** Cielorraso a 32–35 °C | Alta | **100** |
| **T2** | Losa viguetas + EPS 60 + contrapiso + membrana | EPS 60 | **0,443** | 0,457 | ✗ | ✗ | **✓** | Aceptable si la membrana es clara | Alta | 125 |
| **T2c** | Idem con EPS 130 + membrana clara | EPS 130 | **0,235** | 0,241 | **✓ (α<0,6)** | ✓ | ✓ | **Muy bueno** | Alta | 150 |
| **T3** | **Cubierta invertida** (membrana abajo, XPS 140 + canto rodado) | XPS 140 | **0,212** | 0,217 | **✓ (α<0,6)** | ✓ | ✓ | **Muy bueno.** Lastre = inercia extra | **Muy alta** | 175 |
| **T4** | Losa aislada + **cubierta ventilada de chapa** | EPS 80 + bovedilla EPS | **0,318** | 0,325 | ✗ | ✓ | ✓ | **EL MEJOR.** La cámara evacúa la carga solar antes del aislante | Alta | 195 |
| **T5** | Chapa + lana de vidrio 150 entre correas + cielorraso | Lana 150 | **0,238** | 0,234 | **✓ (α<0,6)** | ✓ | ✓ | Bueno con chapa clara; malo con chapa oscura | **Nula** | 135 |
| **T6** | **Panel sándwich** chapa-PUR-chapa 100 mm | PUR 100 | **0,228** | 0,232 | **✓ (α<0,6)** | ✓ | ✓ | Bueno térmicamente; **sin inercia** | **Nula** | 165 |
| **T7** | Teja + machimbre a la vista + EPS 100 entre clavaderas | EPS 100 | **0,303** | 0,309 | ✗ | ✓ | ✓ (según α de la teja) | Bueno; **penalizado si la teja es α > 0,8** | Media | 190 |
| **T8** | **Teja + ático ventilado + lana 150 sobre cielorraso** | Lana 150 | **0,240** | 0,240 | **✓ (teja clara)** | ✓ | ✓ | **Muy bueno**: ático ventilado + aislación horizontal | Baja | 160 |
| **T9** | Losa con **bovedilla de EPS** + EPS 120 + membrana clara | EPS 120 + bovedilla | **0,227** | 0,232 | **✓ (α<0,6)** | ✓ | ✓ | Muy bueno | Alta | 155 |

*Costo relativo: índice T1 = 100, materiales + mano de obra por m² de cubierta terminada. **Estimación de orden de magnitud del estudio.*** `[VERIFICAR con presupuesto real de Santa Rosa.]`

---

## 3.4 Espesor de aislante necesario en cubierta

### Tabla 3.3 — Losa de viguetas con bovedilla cerámica (RT_base = 0,545 verano)

| Objetivo | K adm | RT_nec | ΔR | **EPS 0,035** | **XPS 0,033** | **Lana vidrio 0,040** | **PUR 0,024** |
|---|---|---|---|---|---|---|---|
| Nivel C (0,76) | 0,76 | 1,316 | 0,771 | 27 → **30 mm** | 25 → 30 | 31 → 40 | 19 → 20 |
| **Nivel B, α > 0,8** (0,384) | 0,384 | 2,604 | 2,059 | 72 → **80 mm** | 68 → 70 | 82 → 90 | 49 → 50 |
| **Nivel B, α medio** (0,48) | 0,48 | 2,083 | 1,538 | 54 → **60 mm** | 51 → 60 | 62 → 70 | 37 → 40 |
| **Nivel B, α < 0,6** (0,624) | 0,624 | 1,603 | 1,058 | 37 → **40 mm** | 35 → 40 | 42 → 50 | 25 → 30 |
| **Sustentable, α medio** (0,34) | 0,34 | 2,941 | 2,396 | 84 → **90 mm** | 79 → 80 | 96 → 100 | 58 → 60 |
| **Nivel A, α < 0,6** (0,247) | 0,247 | 4,049 | 3,504 | 123 → **130 mm** | 116 → 120 | 140 → 140 | 84 → **90 mm** |
| **Nivel A, α medio** (0,19) | 0,19 | 5,263 | 4,718 | 165 → **170 mm** | 156 → 160 | 189 → 190 | 113 → **120 mm** |
| **Nivel A, α > 0,8** (0,152) | 0,152 | 6,579 | 6,034 | 211 → **220 mm** | 199 → 200 | 241 → 250 | 145 → 150 |

> ### LA RELACIÓN 2:1 QUE PIDE IRAM 11603
> Muro Nivel A: **100 mm de EPS**. Techo Nivel A con cubierta clara: **130 mm**; con cubierta media: **170 mm**. La norma recomienda *"el doble de aislación en techos respecto de muros"* para Zona IV, y los números lo confirman solos.
> **En una casa de una planta el espesor en cubierta no cuesta superficie útil** (va sobre la losa o dentro del ático): es el lugar donde el aislante es más barato de colocar y más rinde. **Si hay que elegir dónde poner el dinero, va acá** (§9).

---

## 3.5 Ventilación de cubierta y cámara de aire

### Por qué ventilar

| Función | En invierno | En verano |
|---|---|---|
| **Evacuar vapor** | **Crítica.** El vapor que atraviesa la barrera de vapor (siempre pasa algo) debe poder salir antes de condensar contra la cara fría de la chapa o la teja | Menor |
| **Evacuar calor** | Irrelevante | **Crítica.** Una cámara ventilada bajo chapa baja la temperatura del aislante entre 10 y 20 K `[VERIFICAR con medición o simulación]` |
| **Secar la cubierta** | Importante: agua de condensación, filtración menor, agua de obra | Importante |

### Reglas de ejecución

| Elemento | Requisito |
|---|---|
| **Cubierta inclinada con ático** | Entrada de aire **continua en el alero** y salida en la **cumbrera** (cumbrera ventilada) o en el vértice. Superficie libre total ≈ **1/300 de la superficie de cielorraso**, repartida 50/50 entre entrada y salida `[VERIFICAR criterio contra manual del fabricante de la cubierta]` |
| **Cubierta de chapa sin ático** (chapa sobre correas con aislación bajo chapa) | **Cámara de al menos 40 mm entre el aislante y la chapa**, ventilada de alero a cumbrera. Es la única configuración en la que un **aislante reflectivo** rinde de verdad: bajo la chapa, con la cámara ventilada, cortando la radiación de la chapa caliente |
| **Cubierta plana** | La cubierta plana caliente (T2) **no se ventila**: se resuelve con **barrera de vapor bajo el aislante**. Si el proyecto tiene mucha carga de vapor interior (pileta cubierta, invernadero), se agregan **aireadores de cubierta** (uno cada 40–60 m² `[VERIFICAR]`), que ventilan la interfaz aislante-membrana. En cubierta **invertida** no hace falta: la membrana está del lado cálido |
| **Rejillas** | Todas con **malla antipájaro y antiinsecto**. En La Pampa, además, con **deflector contra el ingreso de agua y polvo por viento**: una entrada de alero sin deflector con viento de 60 km/h mete lluvia y tierra en el ático |
| **Compartimentación** | En cubierta de teja con ático corrido sobre varios locales, **cortar la cámara sobre los muros divisorios de sector de incendio** `[VERIFICAR exigencia en el Código de Edificación de Santa Rosa]` |
| **El error que anula todo** | Correas, conductos o el propio aislante obstruyendo el paso del aire en el alero. **La aislación no debe tapar la entrada de ventilación**: se usan **deflectores rígidos (bafles)** que mantienen abierto el canal entre el aislante y la chapa/teja en el arranque del alero |

### La cámara de aire: qué aporta y qué no

| Configuración | R (m²K/W) | Equivale a |
|---|---|---|
| Cámara de aire no ventilada en techo, 30–40 mm | 0,14 | 5 mm de EPS |
| Ático no ventilado bajo teja | 0,23 inv / 0,17 ver | 8 / 6 mm de EPS |
| Ático no ventilado bajo chapa | 0,35 inv / 0,22 ver | 12 / 8 mm de EPS |
| **Cámara VENTILADA** | **0,00 a efectos de cálculo** | **Su valor está en el verano, y no se computa** |

> **La cámara no reemplaza al aislante en ningún caso.** Un ático bajo chapa aporta 0,22 m²K/W en verano: **8 mm de EPS**. Se ventila por razones de humedad y de verano, no para sumar R.

---

## 3.6 LA RECOMENDACIÓN POR DEFECTO

> ### CUBIERTA RECOMENDADA PARA UNA CASA DE UNA PLANTA EN SANTA ROSA
>
> ## **T9/T2c — Losa de viguetas con bovedilla de EPS + EPS de 120–140 mm sobre la losa + contrapiso de pendiente + membrana de terminación CLARA**
> ## **K verano = 0,21–0,23 W/m²K — Nivel A con α < 0,6**
>
> **Composición completa (de interior a exterior):**
> ```
> Cielorraso: revoque a la cal 15 mm, o placa de roca de yeso suspendida
> LOSA DE VIGUETAS PRETENSADAS CON BOVEDILLA DE EPS h = 17 cm,
>   capa de compresión de 5 cm con malla  [Rt = 0,63 gratis]
> BARRERA DE VAPOR: film de polietileno de 200 μ, solapado 15 cm y sellado,
>   o pintura asfáltica de doble mano   ← VA ACÁ, DEL LADO CÁLIDO
> EPS de 25 kg/m³, 120–140 mm, placas a junta trabada
> Film separador
> CONTRAPISO DE PENDIENTE de hormigón de cascote, espesor mínimo, pendiente ≥ 1,5 %
> CARPETA HIDRÓFUGA 20 mm, fratasada
> MEMBRANA ASFÁLTICA de 4 mm CON FOIL DE ALUMINIO  ← α < 0,6, sin pintar
>   (alternativa: membrana geotextil + pintura acrílica reflectiva blanca,
>    con repintado cada 4–6 años consignado en el manual de uso)
> ```
>
> ### Por qué ésta y no otra
>
> | Criterio | Por qué gana |
> |---|---|
> | **Verifica Nivel A de verano** con cubierta clara | 0,227 ≤ 0,247. Y de invierno con muchísimo margen (0,232 ≤ 0,26) |
> | **Masa del lado interior** | La losa (≈ 300 kg/m²) queda por dentro del aislante: **es el volante de inercia de la casa**, y con 14,4 K de amplitud estival + ventilación nocturna, es lo que evita usar el aire acondicionado |
> | **La bovedilla de EPS es aislante gratis** | 0,63 contra 0,19 de la cerámica: **0,44 m²K/W sin cambiar un solo paso de obra ni un peso de mano de obra**, sólo especificando otra bovedilla |
> | **Espesor sin costo de superficie** | Los 140 mm van sobre la losa. No roban altura útil si la altura de local se define desde el cielorraso |
> | **Se lleva bien con la casa de una planta** | Permite parapetos bajos, cubierta accesible para mantenimiento, y equipos (condensadoras, termotanque solar) sin estructura adicional |
> | **Oficio disponible** | Es la cubierta que hace cualquier contratista de Santa Rosa. Lo único distinto es la bovedilla, el EPS y la exigencia de terminación clara |
>
> ### Alternativas admitidas y cuándo
>
> | Situación | Solución |
> |---|---|
> | **Azotea accesible o mantenimiento difícil** | **T3, cubierta invertida** con XPS de 140 mm y lastre calculado por succión de viento. La membrana dura el doble |
> | **El proyecto quiere techo inclinado y cielorraso plano** | **T8: teja o chapa + ático ventilado + 150 mm de lana de vidrio sobre el cielorraso.** Es la solución de mejor costo/prestación del capítulo |
> | **El proyecto quiere machimbre a la vista** | **T7** con **100 mm de EPS mínimo**, y **80 mm sólo si la teja es clara**. Verificar el α de la teja |
> | **Verano crítico: mucha superficie de techo al oeste, o techo sobre un local muy expuesto** | **T4, doble techo ventilado.** Es la mejor cubierta de verano posible; cuesta más |
> | **Obra muy rápida, presupuesto acotado, se acepta perder inercia** | **T6, panel sándwich de 100 mm.** Compensar la masa con contrapiso pesado en planta baja y tabiques de mampostería |
>
> ### Lo que NO se acepta
> - Losa sin aislante (**K = 1,83: 2,4 veces por encima del Nivel C**).
> - Cubierta de chapa con **sólo** manta reflectiva de 10 mm: no verifica ni de lejos.
> - **Cubierta oscura** (membrana negra sin pintar, teja roja oscura, chapa prepintada oscura) sin haber recalculado con la corrección de **−20 %**.
> - **Lana de vidrio sin barrera de vapor del lado cálido** en cubierta de chapa o de teja.
> - Lana comprimida por las correas.
