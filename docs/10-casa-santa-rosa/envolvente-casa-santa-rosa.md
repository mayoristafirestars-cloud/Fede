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
