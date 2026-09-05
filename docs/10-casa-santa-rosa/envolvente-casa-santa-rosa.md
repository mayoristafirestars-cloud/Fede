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

---

# 4. PISO

> **En una casa de una planta, TODO el piso está en contacto con el terreno.** No hay entrepisos, no hay unidades debajo. Y como el resto de la envolvente se aísla bien, **la pérdida por el piso pasa de ser un ítem menor a ser el segundo o el tercero de la lista**: en la casa de referencia con envolvente Nivel A representa el **31 % de la pérdida por conducción**. Es el ítem más ignorado y el más barato de resolver.

## 4.1 Cómo se computa la pérdida por el piso

**No se usa K por metro cuadrado. Se usa una pérdida lineal por metro de perímetro.** El flujo de calor del piso hacia el terreno no es unidimensional: sale por el borde, rodeando la fundación, hacia el aire exterior. Por eso IRAM 11604 lo tabula en **W por metro lineal de perímetro** y aclara (Nota 4, verificada): *"Solamente se calcula la pérdida por el piso en contacto con el suelo **contiguo a la envolvente vertical**."* El centro de la casa, a varios metros del borde, prácticamente no pierde.

```
Pérdida total por el piso [W/K] = Perímetro [m] × Pp [W/m·K]
```

| Situación | **Pp — zona III y IV** |
|---|---|
| **Sin aislación en el piso** | **1,38 W/m·K** |
| **Aislación perimetral** (R ≥ 0,7 m²K/W, ancho ≥ 50 cm) | **1,08 W/m·K** |
| **Aislación total** (R ≥ 0,7 m²K/W en toda la superficie) | **0,93 W/m·K** |

**Casos especiales de la norma (verificados):**

| Caso | Tratamiento |
|---|---|
| Local calefaccionado en PB **adyacente a local no calefaccionado** (garaje, depósito) | **50 %** de los valores de la tabla, en ese tramo de perímetro |
| Semisótano calefaccionado | **+25 %** sobre los valores de la tabla |
| Semisótano: perímetro a computar | El del **nivel del suelo exterior**, no el del piso |
| Piso en contacto **directo con el aire exterior** (voladizo, sobre cochera abierta) | **No se usa esta tabla.** Se calcula K por IRAM 11601 **con flujo descendente (Rsi = 0,17)** y se multiplica por el **área** |
| Suelo muy denso, muy húmedo o con napa cercana | Las pérdidas **serán mayores** que las de la tabla. **La norma recomienda aislación perimetral en zonas III y IV** (Nota 9) |

> **Santa Rosa cae de lleno en la Nota 9.** El loess seco es poco conductor, pero **la conductividad del suelo se multiplica por 3 a 6 al saturarse** (arena seca λ 0,30 → saturada λ 1,88 W/m·K), y en suelo loéssico la saturación local bajo la casa es un escenario realista: una pérdida de cañería, un embudo tapado, una vereda con contrapendiente. **Criterio del estudio: aislación perimetral como mínimo, en todos los proyectos.**

## 4.2 Las tres situaciones de la norma y cómo se materializan

### Tabla 4.1 — Espesor de aislante para R = 0,7 m²K/W (lo que pide la norma)

| Aislante | λ | e calculado | **e a adoptar** | ¿Apto para enterrar / bajo contrapiso? |
|---|---|---|---|---|
| **XPS** | 0,033 `[VERIFICAR ficha]` | 21,2 mm | **30 mm** | **SÍ — el único plenamente apto.** Celda cerrada, absorción de agua muy baja, resistencia a compresión |
| EPS 30 kg/m³ | 0,032 | 22,4 mm | **30 mm** | Sí bajo contrapiso protegido y seco; **no** en contacto directo con terreno húmedo |
| EPS 25 kg/m³ | 0,033 | 23,1 mm | 30 mm | Ídem |
| EPS 20 kg/m³ | 0,035 | 24,5 mm | 30 mm | Marginal en resistencia a compresión bajo contrapiso |
| PUR proyectado protegido | 0,024 | 16,8 mm | 20 mm | Con protección; complicado de ejecutar bajo contrapiso |
| Lana mineral | 0,038–0,042 | 27–29 mm | 40 mm | **NO. Se aplasta y absorbe agua** |
| Vidrio celular (foam glass) | ≈ 0,045 `[VERIFICAR]` | 31,5 mm | 40 mm | Sí, es el material de referencia internacional para aislación bajo fundación. **`[VERIFICAR disponibilidad en Argentina]`** |

> **El espesor es pequeño: 30 mm de XPS.** Lo que cuesta no es el material sino recordar ponerlo. La densidad debe estar **entre 25 y 120 kg/m³** por exigencia expresa de la norma.

### Cuándo alcanza la perimetral y cuándo hay que ir a la total

| Situación | Solución | Fundamento |
|---|---|---|
| Casa sin losa radiante, envolvente Nivel B | **Perimetral** (vertical en el borde, 50 cm) | Es lo que pide la norma y captura la mayor parte del beneficio (−22 %) |
| Casa sin losa radiante, envolvente **Nivel A** | **Total** | Con el resto de la envolvente a 0,23–0,29, el piso pasa a ser el 31 % de la pérdida. La aislación total baja otro 14 % la pérdida del piso por muy poco dinero |
| **Casa con LOSA RADIANTE** | **Total, obligatoria, y con R mayor que el mínimo de la norma** | Ver §4.5 |
| Casa con locales húmedos o de mucho uso descalzo (baño, dormitorio) | **Total** al menos en esos locales | Confort de contacto: el piso frío se siente en los pies, no en el termómetro |
| Piso de hormigón alisado visto (mucha masa, mucho contacto) | **Total** | Sin aislar, el alisado es una placa fría permanente |

## 4.3 Cuánto pesa el piso en una casa de una planta

**Casa de referencia:** 130 m² cubiertos (16,0 × 8,0 m), altura 2,60 m, **perímetro en contacto con el terreno = 48 m**, volumen calefaccionado 338 m³.

### Tabla 4.2 — Pérdida por el piso y su peso relativo

| Escenario de envolvente | Pérdida piso (W/K) | Pérdida total por conducción (W/K) | **% del piso** |
|---|---|---|---|
| **Construcción corriente** (M1 + T1 + aluminio s/RPT + piso sin aislar) | 48 × 1,38 = **66,2** | 614,1 | **11 %** |
| **Nivel B** (M3 + T2 EPS 60 + RPT/DVH + piso con aislación perimetral) | 48 × 1,08 = **51,8** | 207,7 | **25 %** |
| **Nivel A** (M4 + T9 EPS 120 + RPT/DVH low-e + piso con aislación total) | 48 × 0,93 = **44,6** | 143,8 | **31 %** |

> ### LA PARADOJA DEL PISO
> **Cuanto mejor se aísla el resto de la casa, más importa el piso.** En una casa corriente el piso es el 11 % del problema y nadie lo mira; en una casa Nivel A es el **31 %** y sigue sin mirarse. Y es, con enorme diferencia, **el ítem más barato de la envolvente**: 24 m² de XPS de 30 mm para la faja perimetral (48 m × 0,50 m) o 130 m² para la aislación total.
>
> **Ahorro anual, casa de referencia** (con la fórmula `Q = 24 × GD18 × ΔUA / 1000`, GD18 = 1.394):
> - Pasar de **sin aislación** a **aislación perimetral**: ΔUA = 14,4 W/K → **482 kWh/año**
> - Pasar de **perimetral** a **total**: ΔUA = 7,2 W/K → **241 kWh/año**
> - Total: **723 kWh/año**, para siempre, por 130 m² de XPS de 30 mm.

## 4.4 Aislación perimetral: detalle constructivo

### D-PISO-01 — Aislación perimetral vertical (la solución recomendada)

```
        INTERIOR                    │   EXTERIOR
                                    │
   Solado                           │   Vereda perimetral 0,80–1,20 m
   Carpeta 20 mm                    │   con pendiente 2 % hacia afuera
   Contrapiso 80–100 mm             │
   Film de polietileno 200 μ ───────┤   ┌── Zócalo del SATE: XPS (no EPS)
   (aislación hidrófuga + corte     │   │   desde 30 cm sobre el terreno
    de capilaridad)                 │   │   hasta 50–60 cm por debajo
   Suelo compactado                 │   │   del nivel de piso terminado
                                    │   │
   ══════ MURO ═══════════════╗     │   │
                              ║ ◄───┼───┘  XPS de 30 mm, 50 cm de altura,
   ▓▓ XPS 30 mm ▓▓▓▓▓▓▓▓▓▓▓▓▓║     │      adherido a la cara exterior de
   (faja perimetral vertical, ║     │      la viga de fundación / cimiento,
    50 cm de altura mínima)   ║     │      protegido con revoque impermeable
                              ║     │      o placa de protección
   ══════ VIGA DE FUNDACIÓN ══╝     │
```

**Reglas:**

| # | Regla | Por qué |
|---|---|---|
| 1 | **El XPS del piso y el aislante del muro deben SOLAPARSE**, sin interrupción | Si no, el encuentro muro-piso queda como un puente térmico lineal continuo en todo el perímetro (§6.6). El SATE del muro baja hasta 50–60 cm bajo el nivel de piso, en XPS; la faja perimetral del piso lo encuentra ahí |
| 2 | **Por debajo del nivel del terreno, XPS — nunca EPS** | El EPS absorbe agua si está sumergido o en contacto con terreno húmedo, y la pierde en R |
| 3 | **Perfil de arranque de aluminio con goterón** en el SATE, al menos **30 cm sobre el nivel del terreno** | Evita que el revestimiento del SATE toque el suelo y absorba humedad por capilaridad |
| 4 | **Film de polietileno de 200 μ continuo bajo el contrapiso**, solapado 20 cm y subiendo por el perímetro | Corte de capilaridad. En loess es tan importante como el aislante |
| 5 | **La faja horizontal es alternativa válida**: XPS de 30 mm × 50 cm de ancho bajo el contrapiso, en todo el perímetro | La norma admite *"posición vertical u horizontal"*. La vertical es térmicamente mejor (corta el camino del flujo); la horizontal es más fácil de ejecutar |
| 6 | **La vereda perimetral con pendiente 2 % es parte del detalle térmico** | En loess colapsable, mantener el suelo seco bajo la fundación es simultáneamente una medida estructural y térmica: suelo seco = λ 0,30 en vez de 1,88 |
| 7 | **Proteger el XPS enterrado contra el ataque mecánico y de roedores** | Revoque impermeable armado, placa cementicia o membrana de drenaje con relieve |

### D-PISO-02 — Aislación total

```
   Solado (porcelanato / hormigón alisado / madera)
   Carpeta de nivelación 20 mm
   CONTRAPISO de hormigón 80–100 mm  ← ES LA MASA TÉRMICA: no aislar por encima
   Film separador de polietileno
   ▓▓▓ XPS de 30 mm en TODA la superficie ▓▓▓
   Film de polietileno de 200 μ (corte de capilaridad)
   Suelo compactado / cama de tosca compactada
   + FAJA PERIMETRAL VERTICAL de XPS 30 mm × 50 cm en todo el borde
```

> **El orden importa:** el **contrapiso queda por ENCIMA del aislante**, no por debajo. Así la masa del contrapiso queda del lado interior y funciona como volante térmico (§8.3). Aislar por encima del contrapiso (aislante bajo la carpeta) desperdicia esa masa exactamente igual que el trasdosado interior desperdicia la del muro.

## 4.5 Piso y losa radiante

> **La losa radiante cambia todos los números del piso.** Un piso normal está a la temperatura del ambiente (20 °C). Un piso radiante está a **26–29 °C en superficie**, con la carpeta a 30–35 °C y el agua a 35–45 °C. **El salto térmico hacia abajo se triplica.** Sin aislación bajo la losa radiante, una fracción muy grande del calor generado se va al terreno.

### Requisitos

| Elemento | Requisito | Por qué |
|---|---|---|
| **Aislación bajo la losa** | **Obligatoria, TOTAL, y con R muy superior al mínimo de IRAM 11604.** Criterio del estudio: **R ≥ 1,25 m²K/W**, es decir **XPS de 40–50 mm** o EPS de alta densidad (30 kg/m³) de 40–50 mm. **`[VERIFICAR el espesor exigido por EN 1264-4 y por el fabricante del sistema para piso sobre terreno]`** | Con el piso a 30–35 °C, con R = 0,7 la pérdida hacia abajo es inaceptable |
| **Densidad del aislante** | **≥ 30 kg/m³ (EPS) o XPS.** Debe soportar la carga del contrapiso, la carpeta, el solado, el mobiliario y las cargas de uso **sin deformarse** | Si el aislante cede, la carpeta fisura y la cañería queda mal apoyada |
| **Banda perimetral** | **Obligatoria: banda de espuma de polietileno de 8–10 mm de espesor y altura completa de la carpeta**, en todo el perímetro de cada paño y contra todo elemento vertical (muros, columnas, marcos) | (a) Permite la dilatación de la carpeta calefaccionada, que si no fisura; (b) **corta el puente térmico entre la carpeta caliente y el muro**, que si no se convierte en un radiador hacia el exterior en todo el perímetro |
| **Faja perimetral vertical** | **Además de la aislación total**, la faja vertical de XPS de 30 mm × 50 cm en el borde exterior de la fundación | Con losa radiante, el borde es el punto de fuga más caliente |
| **Barrera de vapor bajo el aislante** | Film de polietileno de 200 μ | Si el aislante se moja desde abajo pierde su R y la losa radiante consume más para siempre |
| **Film reflectivo sobre el aislante** | Habitual en los sistemas comerciales; **su aporte térmico real es marginal** (la cañería está en contacto con la carpeta, no con una cámara de aire) | Su función práctica es la **grilla impresa de replanteo** y la protección del aislante durante el montaje. No computarlo como aislación |
| **Prueba de presión** | **6 bar durante 24 h ANTES de hormigonar la carpeta**, con la cañería presurizada durante el llenado | Una pérdida detectada después obliga a romper el piso terminado |
| **Curado y puesta en marcha** | Curado de la carpeta ~21 días y ciclo de puesta en marcha progresivo antes de colocar el solado | |

### La regla que decide si conviene losa radiante

> **La losa radiante tiene un techo de emisión del orden de 100 W/m² en zona de permanencia** (limitado por la temperatura superficial máxima admisible del piso, no por el equipo).
>
> **Casa de referencia, 130 m², carga de calefacción:**
>
> | Escenario de envolvente | Q transmisión + infiltración a ΔT = 26 K | **W/m² de piso** | ¿La losa radiante alcanza? |
> |---|---|---|---|
> | **Construcción corriente** (G = 2,52) | 2,52 × 338 × 26 = 22.146 W | **170 W/m²** | **NO. Muy lejos.** Haría falta 1,7 veces la superficie disponible |
> | **Nivel B** (G = 1,31) | 1,31 × 338 × 26 = 11.510 W | **89 W/m²** | **Sí, al límite** |
> | **Nivel A** (G = 0,78) | 0,78 × 338 × 26 = 6.854 W | **53 W/m²** | **Sí, con holgura** |
>
> ### **LA LOSA RADIANTE EXIGE UNA ENVOLVENTE AISLADA. NO ES UN SISTEMA QUE SE PUEDA "AGREGAR" A UNA CASA FRÍA.**
> Es el error más caro que se comete con losa radiante en Argentina: se instala en una casa con muros de hueco 18 sin aislar, no calienta, y se culpa al sistema. **En un proyecto del estudio, la losa radiante se acepta sólo con envolvente verificada en Nivel B como mínimo, y preferentemente en Nivel A.**
>
> Y el corolario de verano: **en Santa Rosa la losa radiante es un excelente sistema de calefacción y un mal sistema de refrigeración** (con TDMX 38,8 °C, refrigerar por el piso lleva a condensación superficial sobre el solado). Combinar losa radiante para invierno + splits o fan coils para verano.

---

# 5. CARPINTERÍAS Y VIDRIOS

> **En una casa bien aislada, las ventanas son el punto más débil, por lejos.** Con muros a K = 0,29 y una ventana de aluminio sin RPT con vidrio simple a K = 5,86, **1 m² de esa ventana pierde lo mismo que 20 m² de muro**. En la casa de referencia con envolvente Nivel A, los 18 m² de aberturas son el **27 % de la pérdida por conducción** ocupando el **7 % de la superficie de envolvente**.
>
> Y hay un segundo frente: **con el viento pampeano, la infiltración por una carpintería mal cerrada o mal sellada puede superar la pérdida por conducción de la propia ventana.**

## 5.1 Perfilería comparada

### Tabla 5.1 — Materiales de carpintería

| Material | λ del material (W/m·K) | **K del perfil (W/m²K)** | Rotura de puente térmico | Condensa sobre el marco | Mantenimiento | Vida útil | Costo rel. | Veredicto Santa Rosa |
|---|---|---|---|---|---|---|---|---|
| **Aluminio sin RPT** | **204** | **6,02** *(IRAM 11507-4 Tabla A.3, verificado)* | No | **Sí, siempre** | Muy bajo | 40+ años | **100** | **Inadmisible en la envolvente térmica** |
| **Aluminio con RPT** | 204, con inserto de poliamida | **2,85** *(IRAM 11507-4, verificado)* | **Sí** | Rara vez | Muy bajo | 40+ años | 160–220 | **La opción correcta.** Reduce el K del perfil a menos de la mitad |
| **PVC** | **0,16** | *orden de magnitud 1,3–2,0* `[VERIFICAR en ficha del fabricante]` | **El material ES la rotura** | No | Bajo | ~50 años | 130–200 | **Excelente.** No conduce, no condensa, no hay par galvánico, el marco hace de premarco |
| **Madera** | 0,13–0,19 | *orden de magnitud 1,8–2,2* `[VERIFICAR]` | El material lo es | No | **Alto**: repintado cada 2–4 años en exterior expuesto | 30–80 años con mantenimiento | 150–300 | Térmicamente excelente. **El clima pampeano (UV alto, amplitud 53 K, viento seco) es muy duro con la madera exterior** |
| **Madera-aluminio** | — | *`[VERIFICAR]`* | Sí | No | Bajo | 40+ años | 250–400 | Lo mejor de ambos; poco difundido y caro en Argentina |
| **Hierro / acero** | **58** | *muy alto* `[VERIFICAR]` | No | **Sí** | Alto (anticorrosivo) | 30+ años | 70–110 | **El peor.** Sólo en aberturas de seguridad o industriales |

### Tabla 5.2 — De abrir vs. corrediza: la diferencia que decide la infiltración

| | **De abrir / oscilobatiente / proyectante** | **Corrediza** | **Corrediza elevable (lift & slide)** |
|---|---|---|---|
| Mecanismo de cierre | **Compresión** de burlete perimetral continuo | **Deslizamiento** de felpas | **Compresión** al bajar la manija |
| Estanqueidad al aire | **Muy alta** | **Limitada por diseño**: el encuentro de las dos hojas nunca cierra por compresión | **Muy alta** |
| Clasificación IRAM alcanzable | A2/A3, E3/E4, V3 `[VERIFICAR por producto]` | Habitualmente inferior | Alta |
| Superficie de paso | 50 % o 100 % del vano | Máximo 50 % | 50 % |
| Costo | Medio | Bajo | Alto |
| **Veredicto Santa Rosa** | **Preferible siempre que sea posible** | Aceptable hacia galería protegida, o en líneas de alta prestación | **La única corrediza admisible en un vano grande de la envolvente** |

> **Con viento medio de 10–12,5 km/h y ráfagas muy superiores, la infiltración de una corrediza económica es un problema permanente y no reparable.** La diferencia entre una casa que "se siente con corriente de aire" y una que no, en Santa Rosa, suele ser la elección entre corrediza y abrir, no el espesor del aislante.

## 5.2 Vidrios: K y factor solar

### Tabla 5.3 — Transmitancia térmica de vidrios — **verificado** (IRAM 11507-4 Tabla A.2)

| Tipología | **K del vidrio (W/m²K)** |
|---|---|
| Vidrio simple incoloro 4 mm | 5,70 |
| **Vidrio simple incoloro 6 mm** | **5,80** |
| DVH con cámara de 6 mm | 3,20 |
| DVH con cámara de 9 mm | 3,00 |
| **DVH incoloro–incoloro 6-12-6** | **2,80** |
| **DVH incoloro–Low-E 6-12-6** | **1,80** |
| Triple vidriado (TVH) con cámara de 6 mm | 1,90 |
| **DVH incoloro–Low-E con argón 4-15-4** | **1,30** |

**Dato complementario verificado (VASA/Pilkington):** el low-E tipo *Energy Advantage* tiene **emisividad 0,15** contra **0,84** del float común, y la capacidad aislante de un DVH con low-E es **~35 % mejor** que con dos floats comunes. Combinado con un control solar en la cara exterior, **reduce el factor solar y el coeficiente de sombra del DVH en casi un 10 %**.

### Factor solar: el parámetro que no es K

El **factor solar (g o FS)** es la fracción de energía solar incidente que atraviesa el vidrio. **Es independiente de K:** un vidrio puede aislar muy bien del frío y dejar pasar mucho sol (lo que se quiere al norte), o al revés.

> **`[VERIFICAR: los valores de factor solar (g), coeficiente de sombra y transmisión luminosa (TL) de cada producto deben tomarse de la ficha técnica del fabricante (VASA/Blindex y equivalentes). No se reproducen números acá porque no se pudieron verificar contra catálogo en esta investigación. Se pide al proveedor la planilla con K, g y TL de cada composición ofertada, y se archiva con el legajo.]`**

### Tabla 5.4 — Estrategia de vidrio por orientación en Santa Rosa

| Orientación | Qué se busca | Vidrio a especificar | Protección solar |
|---|---|---|---|
| **NORTE** | **K bajo + factor solar ALTO.** Se quiere la ganancia solar de invierno; el control de verano lo hace el alero | **DVH con low-E de ALTA GANANCIA SOLAR** (low-E blando de baja emisividad y g alto). **NO control solar** | **Alero calculado** (§8.2) |
| **OESTE** | **K bajo + factor solar BAJO.** El sol de la tarde de verano entra casi horizontal y ningún alero lo detiene | **DVH con control solar** en la cara exterior + low-E en la interior | **Protección móvil EXTERIOR obligatoria** (§8.5) |
| **ESTE** | Intermedio | DVH incoloro o low-E | Persiana o parasol vertical |
| **SUR** | **Sólo importa el K.** No hay ganancia solar directa que compense | **DVH low-E siempre. Superficie vidriada mínima** | No hace falta |
| **Claraboya / techo vidriado** | **Factor solar bajo obligatorio** | Control solar + laminado de seguridad | **Protección exterior.** Un vidriado horizontal recibe el máximo de radiación en verano (900 W/m² de diseño) |

## 5.3 Ventana completa: la tabla que hay que usar

**El vidrio solo no define nada: el marco es el 20–30 % de la superficie de la ventana y conduce 6 W/m²K.**

### Tabla 5.5 — K de VENTANAS COMPLETAS con perfilería de aluminio — **verificado** (IRAM 11507-4, Tabla A.1)

| Tipología de ventana | Vidrio simple 6 mm | **DVH 6-12-6** | **DVH Low-E 6-12-6** | DVH Low-E c/argón 4-15-4 |
|---|---|---|---|---|
| **Ventana simple SIN ruptor de puente térmico** | **5,86** | **3,82** | **3,14** | **2,80** |
| **Ventana simple CON ruptor de puente térmico** | 4,86 | **2,82** | **2,13** | **1,79** |
| Doble ventana con ruptor de puente térmico | 1,99 | 1,25 | 0,97 | 0,83 |
| Doble ventana con **cortina de enrollar cerrada** | 1,52 | 1,05 | 0,84 | 0,74 |

*Nota de la norma: los valores resultan de cálculos teóricos; cada fabricante debe aportar el valor de su sistema.*

### Tabla 5.6 — Clasificación IRAM 11507-4 y veredicto

| Categoría | K (W/m²K) | Combinación típica | Veredicto Santa Rosa |
|---|---|---|---|
| **K1** | K < 1,0 | Doble ventana con RPT + DVH low-E (0,97) | Nivel Passivhaus. Sólo si el proyecto lo justifica |
| **K2** | 1,0 ≤ K ≤ 1,5 | Doble ventana con RPT + DVH (1,25) | Excelente |
| **K3** | 1,5 < K ≤ 2,0 | RPT + DVH low-E c/argón (1,79) | **Excelente. Objetivo de máxima** |
| **K4** | 2,0 < K ≤ 3,0 | **RPT + DVH low-E (2,13)** / **RPT + DVH (2,82)** | **2,13 = objetivo de proyecto. 2,82 = piso recomendable** |
| **K5** | 3,0 < K ≤ 4,0 | Sin RPT + DVH (3,82) o + DVH low-E (3,14) | Mínimo tolerable. **El marco sigue condensando** |
| **No clasificable** | **K > 4,0** | **Sin RPT + vidrio simple (5,86)** | **FUERA DE NORMA.** IRAM 11507-4 exige K < 4,0 |

> ### CONSECUENCIA INMEDIATA
> **Una ventana de aluminio sin RPT con vidrio simple NO ES CLASIFICABLE según IRAM 11507-4.** No tiene una categoría baja: está fuera de la norma. Y es la ventana que lleva el 90 % del parque construido de Santa Rosa.
>
> **Lectura de la tabla:** pasar de vidrio simple a DVH en un marco sin RPT baja K de 5,86 a 3,82 (**−35 %**). Agregar RPT al marco con DVH baja de 3,82 a 2,82 (**−26 %**). **Los dos movimientos son necesarios: cambiar sólo el vidrio deja el marco conduciendo 6 W/m²K y condensando.**
>
> **Y el dato escondido en la última fila:** una **cortina de enrollar cerrada de noche reduce el K de la ventana entre 0,3 y 0,5 W/m²K**. En una casa que se calefacciona de noche, cerrar las persianas es aislación gratis, y en la casa de referencia equivale a ~6 W/K sobre 18 m². **Consignarlo en el manual de uso de la vivienda.**

## 5.4 ¿Se justifica el DVH en Santa Rosa? Análisis con supuestos explícitos

### Los supuestos (todos declarados, ninguno oculto)

| # | Supuesto | Valor | Estado |
|---|---|---|---|
| S1 | Superficie de aberturas de la casa de referencia | **18 m²** | Hipótesis de proyecto |
| S2 | Grados-día de calefacción base 18 °C | **1.394 °C·día** | **Verificado** (IRAM 11603) |
| S3 | Fórmula de carga térmica anual | `Q = 24 × GD × ΔUA / 1000` [kWh/año] | **Verificado** (IRAM 11604 §6.7.1) |
| S4 | Poder calorífico del gas natural | ≈ **9,3 kWh/m³** | **`[VERIFICAR con la distribuidora]`** |
| S5 | Rendimiento estacional del equipo de calefacción | **90 %** (caldera moderna). Con calefactor de tiro balanceado: **70–75 %** | **`[VERIFICAR según el equipo del proyecto]`** |
| S6 | Precio del gas natural, tarifa residencial La Pampa | **P $/m³** — **no se adopta un valor: se deja como parámetro** | **`[VERIFICAR tarifa vigente]`** |
| S7 | Sobrecosto del upgrade de carpintería | **ΔC $/m² de abertura** — **parámetro** | **`[VERIFICAR con cotización local]`** |
| S8 | La fórmula de IRAM 11604 supone calefacción **24 h/día toda la temporada, sin ganancias solares ni internas** | Sobreestima el consumo absoluto; **los AHORROS COMPARATIVOS entre escenarios son válidos** porque el sesgo es el mismo en todos | Limitación declarada |

### El cálculo

```
Ahorro anual [kWh] = 24 × GD18 × (K₁ − K₂) × A / 1000
Ahorro anual [m³ de gas] = Ahorro [kWh] / (9,3 × rendimiento)
Repago [años] = (ΔC × A) / (Ahorro [m³] × P)
```

### Tabla 5.7 — Ahorro por cada escalón de mejora, 18 m² de aberturas

| Escalón | K₁ → K₂ | ΔK | ΔUA (W/K) | **Ahorro (kWh/año)** | **Ahorro (m³ gas/año)** con rend. 90 % |
|---|---|---|---|---|---|
| **Sin RPT + simple → sin RPT + DVH** | 5,86 → 3,82 | 2,04 | 36,7 | **1.229** | **147** |
| **Sin RPT + simple → CON RPT + DVH** | 5,86 → 2,82 | **3,04** | **54,7** | **1.830** | **219** |
| Con RPT + DVH → con RPT + DVH low-E | 2,82 → 2,13 | 0,69 | 12,4 | **415** | **50** |
| Con RPT + DVH low-E → + argón 4-15-4 | 2,13 → 1,79 | 0,34 | 6,1 | **205** | **25** |
| **Sin RPT + simple → CON RPT + DVH low-E** | 5,86 → 2,13 | **3,73** | **67,1** | **2.245** | **268** |

### Tabla 5.8 — Repago en años, en función del sobrecosto y del precio del gas

Para el escalón principal (**sin RPT + simple → con RPT + DVH**, ahorro de 219 m³/año):

| Sobrecosto del upgrade ΔC ($/m² de abertura) | Repago si el gas cuesta P = $X/m³ |
|---|---|
| ΔC | Repago [años] = (ΔC × 18) / (219 × P) = **0,0822 × ΔC / P** |
| **Ejemplos** (reemplazar por valores reales de Santa Rosa) | |
| ΔC = 50.000 $/m², P = 100 $/m³ | 41 años |
| ΔC = 50.000 $/m², P = 300 $/m³ | 14 años |
| ΔC = 50.000 $/m², P = 600 $/m³ | 7 años |
| ΔC = 100.000 $/m², P = 600 $/m³ | 14 años |

> **`[VERIFICAR: completar esta tabla con la cotización real de carpinterías en Santa Rosa y la tarifa de gas vigente. La fórmula es lo que hay que conservar; los ejemplos son ilustrativos.]`**

### El veredicto — y por qué el repago no es el argumento principal

> ### EN SANTA ROSA EL DVH SE JUSTIFICA SIEMPRE EN LOCALES DE PERMANENCIA
>
> **Y no principalmente por el repago energético, sino por tres razones que el cálculo de repago no captura:**
>
> **1. CONDENSACIÓN.** Con vidrio simple (K = 5,80), interior a 20 °C y exterior a −6 °C, la temperatura de la cara interior del vidrio es:
> ```
> θsi = 20 − (Rsi/RT) × Δt = 20 − (0,17 / (1/5,80)) × 26 = 20 − (0,17/0,172) × 26 ≈ 20 − 25,7 ≈ −5,7 °C
> ```
> *(el vidrio simple no tiene prácticamente resistencia propia: su cara interior está casi a la temperatura exterior corregida por la película de aire)*.
> La temperatura de rocío interior a 20 °C y 70 % de HR es **14,4 °C**. **El vidrio simple condensa masivamente, todas las mañanas de invierno, sin excepción.** El agua chorrea al marco, se acumula en el contramarco, y en el mediano plazo produce moho en la jamba y en la mocheta. **Con DVH (K = 2,80) la cara interior queda a θsi = 20 − (0,17/0,357) × 26 = 7,6 °C** — sigue siendo baja pero **con low-E (K = 1,80): θsi = 20 − (0,17/0,556) × 26 = 12,1 °C**, y con la HR interior en 60 % (rocío 12,0 °C) ya no condensa. **El DVH low-E es lo que elimina el problema, no el DVH simple.**
> **`[Nota de método: este cálculo simplificado usa el K global del vidrio; la verificación formal se hace con IRAM 11625. Sirve para ver el orden de magnitud y la jerarquía entre soluciones.]`**
>
> **2. ASIMETRÍA RADIANTE.** Sentado a 1 m de un vidrio simple a −5,7 °C, el cuerpo pierde calor por radiación hacia esa superficie fría. **La sensación es de frío aunque el termómetro marque 21 °C**, y la respuesta del usuario es subir la calefacción. Ese sobreconsumo **no aparece en el cálculo de repago** porque el cálculo supone temperatura interior constante. **En la realidad, la casa con vidrio simple se calefacciona a 23 °C para sentirse a 20.**
>
> **3. IRAM 11507-4 EXIGE K < 4,0.** Una ventana sin RPT con vidrio simple **está fuera de norma**. No es una opción de proyecto: es un incumplimiento.
>
> ### La discusión real: DVH simple o DVH low-E, por orientación
>
> | Orientación | Recomendación | Fundamento |
> |---|---|---|
> | **SUR y OESTE** | **DVH low-E siempre** (K ventana 2,13) | No hay ganancia solar invernal que compense la pérdida. El low-E la reduce donde no hay contrapartida |
> | **NORTE** | **DVH con low-E de ALTA ganancia solar**; o **DVH simple** si el presupuesto aprieta y el alero está bien calculado | Al norte se quiere que entre el sol de invierno. Un low-E de control solar mal elegido tira a la basura la ganancia solar invernal, que es el mayor recurso energético gratuito de Santa Rosa |
> | **ESTE** | DVH simple o low-E, indistinto | |
> | **Baños, lavaderos, despensa** | DVH simple, o vidrio simple + persiana si el local no es de permanencia | El criterio de la norma es "locales de permanencia" |
>
> **Regla de decisión presupuestaria:** si hay que elegir entre **(a)** DVH low-E en todo y marco sin RPT, y **(b)** DVH simple en todo y marco CON RPT, **elegir (b)**: K = 2,82 contra 3,14, y además **desaparece la condensación sobre el marco**, que es el origen del deterioro. **El RPT primero, el low-E después.**

## 5.5 Cajón de persiana

> **El cajón de persiana de enrollar es, simultáneamente, el peor puente térmico, el peor puente acústico y el mayor punto de infiltración de aire de una vivienda argentina.** Es un cajón hueco, con una tapa registrable que casi nunca cierra hermética, y con un pasaje de cinta que es un agujero directo al exterior. Y está en cada ventana.

### Tabla 5.9 — Soluciones ordenadas de mejor a peor

| # | Solución | Descripción | Puente térmico | Infiltración | Costo |
|---|---|---|---|---|---|
| **1** | **Persiana exterior montada por FUERA de la aislación** (cajón adosado al SATE, tipo monoblock exterior) | El cajón queda del lado frío, **fuera de la envolvente aislada**. El aislante del muro pasa continuo por detrás | **Eliminado** | Sólo el pasaje de cinta / motor | Medio |
| **2** | **Persiana enrollable con guías exteriores y motor**, sin cinta (motor tubular) | Elimina el agujero de la cinta, que es el punto de fuga | Eliminado | **Mínima** | Medio-alto |
| **3** | **Cajón compacto (monoblock) con aislante integrado de 30–40 mm** y burletes en tapa y en pasaje de cinta | El cajón viene aislado de fábrica y con cierres | Reducido | Baja si los burletes son buenos | Medio |
| **4** | **Cajón de mampostería aislado in situ** con 40 mm de EPS en las tres caras + tapa con burlete perimetral + pasacinta con cepillo | La solución "de obra" bien hecha | Reducido, **si la aislación es continua con la del muro** | Media | Bajo |
| **5** | **Postigón exterior de aluminio o madera, o cortina de tela exterior enrollable, en lugar de persiana embutida** | **Elimina el cajón por completo.** Protección solar exterior con cero puente térmico | **Inexistente** | Ninguna | Bajo-medio |
| ✗ | **Cajón de mampostería sin aislar, con tapa de placa de yeso y pasacinta abierto** | Lo que se construye habitualmente | **Muy alto** | **Muy alta** | 100 |

### D-PERS-01 — Detalle del cajón compacto aislado (solución 3/4)

```
                     ┌──────────────────────────────┐
   SATE del muro ────┤ ▓▓▓▓ EPS 100 mm continuo ▓▓▓▓│  ← EL AISLANTE DEL MURO
   (continúa sin     │                              │     PASA POR DELANTE DEL
    interrupción)    │  ┌────────────────────────┐  │     CAJÓN, sin interrupción
                     │  │ EPS 40 mm             │  │
                     │  │  ┌──────────────────┐  │  │
                     │  │  │                  │  │  │
                     │  │  │   ROLLO DE       │  │  │
                     │  │  │   PERSIANA       │  │  │
                     │  │  │                  │  │  │
                     │  │  └──────────────────┘  │  │
                     │  │ EPS 40 mm             │  │
                     │  └────────────────────────┘  │
                     │  ══ TAPA DE REGISTRO ══      │
                     │  con BURLETE PERIMETRAL      │
                     │  de EPDM en todo el contorno │
                     └──────────────────────────────┘
                              ▲
                    PASACINTA CON CEPILLO
                    (o motor tubular sin cinta)
                              │
                     ┌────────┴─────────┐
                     │ DINTEL AISLADO   │  ← retorno del aislante de 20–30 mm
                     │ (§6.4)           │     sobre el marco de la ventana
                     └──────────────────┘
```

**Reglas:**
1. **El aislante del muro debe pasar por delante del cajón**, no interrumpirse en él. Si el cajón está por dentro del plano del SATE, el SATE lo cubre; si sobresale, se lo envuelve.
2. **Burlete perimetral de EPDM en la tapa de registro**, comprimido al cerrar. No un ajuste "a presión" de la placa.
3. **Pasacinta con cepillo** o, mejor, **motor tubular** que elimina la cinta.
4. **La tapa se abre desde el interior**: si se abre desde afuera, además es un problema de seguridad.
5. **Verificar el cajón como puente térmico:** con K_muro = 0,29, el admisible es **K_pt ≤ 0,45**. Un cajón de mampostería sin aislar no baja de 2,5–3,0. **Con 40 mm de EPS en las tres caras y el SATE pasando por delante, el conjunto se lleva al orden de 0,4–0,5** `[VERIFICAR con cálculo 2D en THERM/Flixo para el detalle concreto]`.

## 5.6 Sellado perimetral y estanqueidad al aire en zona ventosa

> ### EL PUNTO MÁS DESCUIDADO DE LA CONSTRUCCIÓN ARGENTINA
> Se especifica una carpintería A2/E3/K4, se paga el DVH low-E, y después se la coloca con "un poco de mortero alrededor" y un cordón de silicona por fuera. **El resultado es una ventana de excelente prestación instalada en un vano que filtra aire y agua por todo su perímetro.** La prestación de una ventana no la da la ventana: **la da la ventana MÁS su instalación.**

### Tabla 5.10 — Reglas de sellado (verificadas, manual INCoSe)

| Regla | Especificación |
|---|---|
| **Holgura de fabricación** | La abertura debe ser **al menos 10 mm más chica** en ancho y alto que la menor medida del vano. Holgura mínima perimetral: **5 mm** |
| **Relleno de la holgura** | **Espuma de poliuretano de baja expansión** en todo el perímetro. **Es relleno térmico y acústico, NO es el sello** |
| **Sellador exterior** | **Silicona NEUTRA**, nunca acética. Admite deformación de hasta **25 %**, no ataca al PVC, adhiere sobre poroso y no poroso |
| **RELACIÓN DE SELLADO 2:1** | **2 de ancho por 1 de profundidad.** Es lo que permite que el sellador se deforme sin desgarrarse |
| **Fondo de junta** | **Cordón de espuma de celda cerrada de sección circular** en todo el perímetro, para materializar la relación 2:1 **y evitar la adherencia en tres caras**. Si el sellador adhiere también al fondo, cuando la junta se abre no puede deformarse en su sección y **se desgarra**. El fondo de junta no es un relleno de ahorro: es un elemento funcional |
| **Terminación exterior** | Pieza de **¼ de caña** adherida con la misma silicona: protege el sellador de los UV y mejora la escorrentía |
| **Terminación interior** | Contramarco o tapajunta atornillado |
| **Ventanas con aleta de clavado** | **Recubrir el total de la aleta con cinta impermeable** antes de la terminación exterior |
| **Drenajes del marco** | Orificios de drenaje en el perfil inferior, con tapa antiviento. **NO taparlos con silicona durante la colocación** — el error más frecuente: el marco se convierte en una batea |

### Estanqueidad al aire: por qué en Santa Rosa vale tanto como el aislante

**La infiltración es el término `0,35 × n` del coeficiente G.** Con `n = 2 renovaciones/h` (el valor que IRAM 11604 impone por defecto), la infiltración aporta **0,70 W/m³K**. Comparado con la conducción de una casa Nivel A (0,425 W/m³K):

> ### **EN UNA CASA BIEN AISLADA EN SANTA ROSA, LA INFILTRACIÓN ES LA MAYOR PÉRDIDA INDIVIDUAL: 62 % DEL TOTAL.**

| Escenario | Conducción (W/m³K) | Infiltración (W/m³K) | **% de infiltración** |
|---|---|---|---|
| Construcción corriente (n = 2) | 1,817 | 0,70 | 28 % |
| Nivel B (n = 2) | 0,614 | 0,70 | **53 %** |
| Nivel A (n = 2) | 0,425 | 0,70 | **62 %** |
| **Nivel A con carpintería A2 y sellado ejecutado (n = 1)** | 0,425 | **0,35** | 45 % |

**Bajar de n = 2 a n = 1 ahorra 3.958 kWh/año** en la casa de referencia — **casi tanto como aislar los muros completos** (4.105 kWh/año), y **cuesta una fracción**.

### Cómo se consigue

| Medida | Efecto |
|---|---|
| **Carpintería clasificada IRAM A2** (en lugar de A1 o sin clasificar) | El requisito bonaerense es A1 hasta 10 m; **en Santa Rosa se exige A2 por el régimen de viento** |
| **Ventanas de abrir en lugar de corredizas** donde sea posible | La corrediza no cierra por compresión |
| **Cierre multipunto** en hojas de más de 1,20 m de alto | Con cierre en un punto, las esquinas no comprimen el burlete y filtran |
| **Sellado perimetral con fondo de junta y relación 2:1** | Elimina la fuga por el encuentro marco-vano, que suele ser mayor que la de la propia ventana |
| **Cajón de persiana estanco o eliminado** | Es la mayor fuga individual de una fachada |
| **Sellado de pases de instalaciones** en la envolvente (caños de gas, agua, eléctricos, conductos de extracción) | Cada pase sin sellar es un agujero permanente |
| **Cajas de electricidad no enfrentadas** en el mismo hueco de muro, y estancas | |
| **Chimenea / hogar a leña con toma de aire exterior conducida y regulable** | Un hogar abierto es un extractor de 200–400 m³/h permanente, encendido o no |
| **Ensayo Blower Door** al terminar la obra | La única forma de saber si se logró. `[VERIFICAR disponibilidad del servicio en La Pampa o en Bahía Blanca / Neuquén]` |

> **La contrapartida sanitaria:** una casa estanca **necesita ventilación controlada**. No se puede bajar n a 1 y no prever renovación de aire: la humedad interior (personas, cocina, baños, ropa) se acumula, la HR sube, y **entonces sí condensa en todas partes**. La regla es **"sellar bien y ventilar a propósito"**: extracción mecánica en baños y cocina, y microventilación o entradas de aire regulables en dormitorios y estar. **La norma exige explícitamente que la ventilación natural y controlada cumpla los requisitos mínimos de salubridad y confort aunque se reduzca n.**

## 5.7 Superficie vidriada máxima y cómo convive con querer luz y sol

### Lo que dicen las normas

| Norma | Exigencia |
|---|---|
| **IRAM 11603, recomendaciones para Zona IV** | *"La relación superficie vidriada / superficie opaca **no debería superar el 15 %**"* |
| **IRAM 11604, §6.7.3** | Los valores de Gadm corresponden a edificios con **hasta 20 % de la superficie de envolvente vidriada**. Por encima, Gadm se corrige: `Gadm_corregido = Gadm × [1,75 − 0,347 × (Sv/Se)]`, válido para `0,2 < Sv/Se ≤ 1` |

### La casa de referencia

```
Superficie de envolvente total Se = muros brutos (124,8) + techo (130) + piso (130) = 384,8 m²
Superficie vidriada Sv = 18 m²
Sv / Se = 18 / 384,8 = 4,7 %              ← muy por debajo del 20 % de IRAM 11604
Sv / superficie opaca de muro = 18 / 124,8 = 14,4 %   ← cumple el 15 % de IRAM 11603
Sv / superficie cubierta = 18 / 130 = 13,8 %
```

### Cómo convive el 15 % con querer luz y sol

> **El 15 % es una recomendación sobre el TOTAL, no sobre cada fachada.** Ahí está la salida de proyecto: **no se distribuye parejo, se concentra al norte.**

| Fachada | % de la superficie vidriada total (criterio del estudio) | Superficie en la casa de referencia | Por qué |
|---|---|---|---|
| **NORTE** | **55–65 %** | 10–12 m² | Es la única orientación donde el vidrio **gana más de lo que pierde** en el balance invernal. Ganancia solar directa + alero calculado que la corta en verano |
| **ESTE** | 15–20 % | 3 m² | Sol de la mañana, agradable en invierno y tolerable en verano |
| **OESTE** | **5–10 %, y protegido** | 1–2 m² | **La orientación problema.** Cada m² al oeste sin protección es una carga de refrigeración enorme (§8.5) |
| **SUR** | **10–15 %, mínimo indispensable** | 2–3 m² | Sólo pierde. Se abre lo necesario para ventilación cruzada e iluminación de servicios |

**Y cuatro recursos para tener luz sin superficie vidriada:**

| Recurso | Aporta |
|---|---|
| **Ventanas altas (clerestorios) al norte** | Luz profunda con poca superficie: una franja de 40–60 cm bajo el techo ilumina hasta 2,5 veces su altura hacia adentro |
| **Locales pasantes N-S** | Doble iluminación con la mitad de vidrio por lado, y **ventilación cruzada de regalo** (§8.4) |
| **Colores interiores claros y techo blanco** | Duplican la luz útil de la misma ventana |
| **Galería al norte** | Espacio de transición con luz abundante y sin envolvente térmica que verificar (§8.6) |

> **El argumento definitivo contra el ventanal grande al norte "porque da al jardín":** un ventanal de 12 m² con la mejor ventana disponible (K = 2,13) pierde **25,6 W/K**, que es lo mismo que **88 m² del muro recomendado** (K = 0,29). En una casa de 130 m² eso es toda la fachada. **La ganancia solar invernal al norte compensa parte de esa pérdida, pero sólo mientras hay sol: de noche, y en los días nublados (48 % de heliofanía relativa en invierno), el ventanal es un agujero.** El equilibrio se busca con: superficie razonable (no 12 m², sino 8), **el mejor vidrio posible**, **persiana o cortina pesada que se cierre de noche** (−0,3 a −0,5 W/m²K), y **masa térmica en el piso frente al ventanal para acumular la ganancia**.

---

# 6. PUENTES TÉRMICOS DE UNA CASA DE UNA PLANTA

## 6.0 El requisito y por qué obliga a aislar por fuera

**IRAM 11605, apartado 5.4 (verificado):**

> *"En todos los casos, la transmitancia térmica correspondiente a un puente térmico **no puede ser mayor que una vez y medio el valor de la transmitancia térmica del cerramiento opaco** establecido en Norma IRAM 11605."*
> *Si los puentes térmicos lineales están a **distancia ≤ 1,7 m entre sí**, ese porcentaje se reduce: **K_pt / K_mo ≤ 1,35**.*
> *"Los materiales aislantes térmicos... **sólo podrán estar interrumpidos por elementos estructurales y/o tuberías**... deberán cubrir el máximo de la superficie de la parte del muro, techo y piso, **conformando un elemento continuo por todo el contorno de la envolvente expuesta al aire exterior**."*

### Tabla 6.1 — Lo que esto significa en números, en Santa Rosa

| Si el muro es… | K del muro | **K máximo del puente** | Un encadenado de hormigón desnudo tiene K ≈ 2,9–3,5 | ¿Se puede cumplir sin aislación exterior continua? |
|---|---|---|---|---|
| M1 (hueco 18 sin aislar) | 1,58 | 2,37 | **Cumple por accidente** (porque el muro también es pésimo) | — |
| M2 (EPS interior) | 0,49 | **0,74** | Excede **4 a 5 veces** | **NO** |
| M3 (SATE 60) | 0,43 | **0,64** | El SATE lo cubre → K_pt ≈ 0,50–0,60 | **Sí** |
| **M4 (SATE 100)** | **0,29** | **0,45** | El SATE lo cubre → K_pt ≈ 0,33–0,40 | **Sí** |
| M5 (muro doble con EPS en cámara) | 0,39 | 0,59 | La columna atraviesa las dos hojas | **NO, salvo detalle específico** |

> ### LA REGLA DE ORO
> **Un puente térmico que se aísla por dentro no se elimina: se desplaza y se agrava el riesgo de condensación.**
>
> Si se aísla la columna por dentro, la columna queda **más fría todavía** (ya no recibe calor del interior) y el vapor que atraviese la placa condensa contra ella. Además aparece el **"puente de retorno"**: el calor sale por el muro adyacente rodeando el parche de aislante.
>
> **La única solución completa es la aislación exterior continua (SATE o fachada ventilada).** Todo lo demás es mitigación parcial que hay que verificar con cálculo.
>
> **Criterio adicional del estudio — factor de temperatura superficial:** exigir **fRsi ≥ 0,80** en todo encuentro de la envolvente (ver §7.2 para la deducción de ese valor a partir de las condiciones de Santa Rosa). El criterio alemán de DIN 4108-2 es 0,70, pero está calibrado para un clima menos frío: **con TDMN = −6,0 °C y HR interior del 70 %, el mínimo teórico en Santa Rosa es 0,785**.

---

## 6.1 Encuentro MURO – CUBIERTA (el más importante de todos)

**Por qué es crítico en una casa de una planta:** es el único encuentro entre las dos superficies grandes de la envolvente, recorre **todo el perímetro** (48 m en la casa de referencia), y es donde la aislación del muro y la de la cubierta —que muchas veces las ejecutan contratistas distintos, en momentos distintos— tienen que encontrarse. **Es el encuentro que más se ejecuta mal.**

### D-PT-01 — Cubierta plana con parapeto (la peor geometría)

El parapeto es una **aleta de mampostería que sale del volumen aislado y está expuesta al aire por sus dos caras y por arriba**. Sin tratar, es simultáneamente el mayor puente térmico y el punto donde aparece la primera mancha de moho del interior.

```
                          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
            Albardilla ──►│ pendiente ≥ 5 % │ ← hacia adentro, con goterón
            con goterón   │  hacia la azotea│    a ambos lados
                          ├─────────────────┤
    EPS/XPS 50 mm  ──────►│▓▓│         │▓▓▓│◄──── EPS del SATE, 100 mm,
    cara interior del     │▓▓│ PARAPETO │▓▓▓│      SUBE POR LA CARA EXTERIOR
    parapeto              │▓▓│ mampost. │▓▓▓│      DEL PARAPETO Y DOBLA
                          │▓▓│          │▓▓▓│      SOBRE EL CORONAMIENTO
    Membrana que sube ───►│▓▓│          │▓▓▓│
    30 cm por el          │▓▓│          │▓▓▓│   ═══ LAS TRES CARAS
    parapeto y remata     │▓▓│          │▓▓▓│       ENVUELTAS ═══
    en babeta ─────────── │▓▓└──────────┘▓▓▓│
    ══════════════════════╪═════════════════╡
      Membrana            │                 │
      Carpeta             │                 │
      Contrapiso pendiente│                 │
   ▓▓▓ EPS 120 mm ▓▓▓▓▓▓▓▓│▓▓▓  ◄─────────── EL EPS DE LA CUBIERTA
      Barrera de vapor    │                     Y EL DEL MURO SE TOCAN.
      LOSA ══════════════╗│                     Sin interrupción, sin
                         ║│▓▓▓ EPS 100 mm (SATE del muro)
      Cielorraso         ║│
                         ║│
      ═══ MURO ══════════╝│
```

**Capa por capa, de adentro hacia afuera, en el nudo:**

| # | Capa | Requisito |
|---|---|---|
| 1 | Cielorraso / revoque | Continuo hasta el muro |
| 2 | Losa | — |
| 3 | **Barrera de vapor de la cubierta** | Debe **doblar hacia arriba y solaparse con el film del parapeto** |
| 4 | **EPS de cubierta (120 mm)** | Llega **hasta el arranque del parapeto, sin interrupción** |
| 5 | **EPS de la cara interior del parapeto (50 mm)** | Sube desde el nivel del aislante de cubierta hasta el coronamiento, **en continuidad física con el EPS de cubierta** |
| 6 | **EPS del SATE del muro (100 mm)** | **Sube por la cara exterior del parapeto y dobla sobre el coronamiento**, encontrando al del punto 5 |
| 7 | Membrana | Sube ≥ 30 cm por la cara interior del parapeto, sobre el EPS con su malla de refuerzo, y remata en **babeta metálica o en buña** |
| 8 | **Albardilla de coronamiento** | Con pendiente ≥ 5 % hacia la azotea y **goterón a ambos lados**. En La Pampa, **fijada mecánicamente y calculada para succión de viento**, no sólo adherida |

> **Alternativa que elimina el problema de raíz: NO HACER PARAPETO.** En una casa de una planta, una **cubierta con alero y canaleta** en lugar de parapeto y embudo elimina el puente térmico, elimina el punto de filtración número uno de la construcción argentina, y **agrega la protección solar que hay que poner igual** (§8.2). Cuando el partido lo permite, es la mejor decisión de todo el capítulo.

### D-PT-02 — Cubierta inclinada con alero (la geometría correcta)

```
                    ╱ Teja o chapa
                   ╱  Listonado / correas
                  ╱   Membrana hidrófuga respirante
                 ╱    ┌─── ÁTICO VENTILADO ───┐
                ╱     │ ▓▓ Lana de vidrio 150 ▓▓▓▓▓▓▓▓▓▓▓▓▓
        ALERO  ╱      │ ═══ BARRERA DE VAPOR ═══════════════
       0,50 m ╱       │ ─── Cielorraso ─────────────────────
      ────── ╱        │
            ╱         │   ◄── BAFLE / DEFLECTOR: mantiene abierto
           ╱  ┌───────┤       el canal de ventilación del alero
    Canaleta  │  ▓▓▓  │       sin que la lana lo tape
              │  ▓▓▓  │
              │  ▓▓▓  │  ◄── LA AISLACIÓN HORIZONTAL DEL CIELORRASO
              │  ▓▓▓  │      Y EL EPS DEL SATE SE ENCUENTRAN AQUÍ,
    ══════════╡  ▓▓▓  │      POR ENCIMA DEL ENCADENADO
     ENCADENADO  ▓▓▓  │
    ═══════════╡ ▓▓▓  │  ← EPS 100 mm del SATE, continuo por delante
      MURO     │ ▓▓▓  │     del encadenado
               │ ▓▓▓  │
```

**Reglas:**
1. **La aislación del cielorraso debe llegar hasta el plano del aislante del muro, por encima del encadenado**, y ambas deben solaparse. El punto donde el encadenado queda "en el medio" es donde aparece la mancha de moho en el ángulo techo-pared.
2. **El bafle o deflector rígido** es obligatorio: si la lana tapa la entrada de aire del alero, el ático deja de ventilar y condensa.
3. **El alero es también protección solar y protección del muro contra la lluvia batida.** En una ciudad ventosa, un alero de 50–70 cm reduce mucho la carga de agua sobre la fachada y el SATE.

---

## 6.2 Encadenado / viga de encadenado

**Mecanismo:** hormigón (λ = 1,63) sustituyendo al mampuesto (Rt 0,41) en una franja horizontal continua de 20–30 cm de altura, en todo el perímetro y en cada nivel de dintel.

**K del encadenado desnudo:** RT = 0,13 + revoques 0,05 + 0,20/1,63 (0,123) + 0,04 = 0,343 → **K = 2,92 W/m²K**. Con K_muro = 0,29 el admisible es 0,45: **excede 6,5 veces**.

### D-PT-03 — Solución

```
   INTERIOR                                    EXTERIOR
                    ┌─────────────────────┐
   Revoque ─────────┤  ENCADENADO HºAº    ├──── ▓▓▓▓▓▓▓▓▓▓▓▓
                    │  20 × 18 cm         │     ▓ EPS 100  ▓  ← SATE continuo,
                    └─────────────────────┘     ▓   mm     ▓     pasa por delante
   Revoque ─────────┤ LADRILLO HUECO 18   ├──── ▓▓▓▓▓▓▓▓▓▓▓▓     sin interrupción
                    └─────────────────────┘
```

| Solución | Efecto | K resultante |
|---|---|---|
| **SATE continuo por delante (recomendada)** | El encadenado queda **por dentro** de la aislación: deja de ser puente | RT = 0,13+0,05+0,123+2,857+0,04 = **3,20 → K = 0,31** ✓ (≤ 0,45) |
| Encadenado con **pieza en U de cerámico o de HCCA** como encofrado perdido exterior | Reduce el puente pero no lo elimina | ≈ 1,0–1,3 `[VERIFICAR con cálculo 2D]` ✗ |
| Aislación **interior** local sobre el encadenado, con solape ≥ 60 cm a cada lado | Mitigación parcial; **desplaza el problema y agrava la condensación** | ✗ |
| **Muro portante (M7): eliminar el encadenado intermedio** | Sólo queda el encadenado superior | Menos superficie de puente de origen |

---

## 6.3 Columna embebida en el muro

Igual que el encadenado pero en franja **vertical**, y **peor cuando está en una esquina** (puente constructivo + geométrico simultáneos: la superficie exterior que capta frío es mayor que la interior que emite, y en el diedro el aire tiene menor movilidad).

**Solución: SATE continuo.** Sin excepción. Si por alguna razón no se puede (medianera), la mitigación es aislación interior con **solape mínimo de 60 cm a cada lado de la columna** para evitar el puente de retorno, **más verificación de condensación con Rsi = 0,50** (rincón, IRAM 11630), que casi con seguridad no va a dar.

> **En una casa de una planta hay una salida de proyecto que no existe en un edificio: eliminar las columnas.** Con **muro portante de ladrillo cerámico (M7) o de bloque de hormigón (M8)** no hay columnas embebidas. El puente térmico que no existe no hay que resolverlo. **Es un argumento térmico —además del estructural y económico— a favor del muro portante en vivienda de una planta.**

---

## 6.4 Dintel

**Mecanismo:** viga de hormigón o perfil metálico sobre el vano, más el **cajón de persiana** que casi siempre lo acompaña (§5.5), más el **retorno del aislante hacia el marco**.

### D-PT-04 — Encuentro dintel / cajón de persiana / marco

```
                       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                       ▓ EPS 100 mm (SATE) ▓  ← continuo por delante del
                       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     dintel Y del cajón
   ┌───────────────────┬────────────────────┐
   │  DINTEL HºAº      │ ▓ EPS 40 mm ▓      │
   ├───────────────────┤                    │
   │  CAJÓN DE         │ ▓ EPS 40 mm ▓      │
   │  PERSIANA         │                    │
   │  (§5.5)           │ ▓ EPS 40 mm ▓      │
   └───────────────────┴────────────────────┘
              │              ▓▓▓▓▓▓  ← RETORNO DEL AISLANTE:
              │              ▓ 30  ▓     el EPS dobla hacia el vano
       Tapa   │              ▓ mm  ▓     y SOLAPA 20–30 mm SOBRE EL MARCO
       con    │            ┌─▓▓▓▓▓▓─┐
       burlete│            │ MARCO  │ ← perfil con RPT
              ▼            │  RPT   │
                           └────────┘
                        ▲
              PERFIL DE GOTERÓN sobre el marco,
              en el borde del retorno del aislante
```

**Reglas:**

| # | Regla | Por qué |
|---|---|---|
| 1 | **El aislante retorna hacia el vano y solapa 20–30 mm sobre el marco** | Sin el retorno, la jamba, el dintel y el antepecho quedan sin aislar: es un marco de mampostería fría de 15 cm de ancho rodeando cada ventana. **Es el puente térmico más frecuente de un SATE mal ejecutado**, y produce la mancha de moho en el borde interior del vano |
| 2 | **Perfil de goterón en el dintel**, en el borde del retorno | Corta el escurrimiento sobre el vidrio y protege el sellado |
| 3 | **Premarco de PVC o de madera**, nunca de chapa doblada | Un premarco de chapa es un puente térmico metálico adicional; el de PVC o madera **es en sí mismo una rotura de puente térmico** entre marco y mampostería |
| 4 | **El marco se alinea con el plano del aislante**, no con el plano de la mampostería | Cuanto más hacia afuera está el marco (dentro del espesor del aislante), menor es el puente térmico perimetral |
| 5 | **Doble malla a 45° en las cuatro esquinas del vano** (refuerzo de 30 × 50 cm) | Sin esto, el SATE fisura en las esquinas del vano. Garantizado |

---

## 6.5 Antepecho

Es el mismo problema que el dintel, con el agregado de que **el alféizar es una pieza que atraviesa la envolvente de lado a lado**.

### D-PT-05 — Antepecho y alféizar

```
                     ┌────────┐
                     │ MARCO  │
                     │  RPT   │
                     └───┬────┘
     ┌───────────────────┴──────────────────┐
     │  ALFÉIZAR: pendiente ≥ 5 %,          │  ← de piedra, granito, chapa
     │  GOTERÓN en el borde,                │     plegada o premoldeado
     │  OREJAS LATERALES que entran BAJO    │
     │  el revestimiento del SATE           │
     └──────────────┬───────────────────────┘
                    │  ▓▓▓▓▓ EPS 30 mm ▓▓▓▓  ← retorno del aislante
     ═══════════════╡  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
       ANTEPECHO    │  ▓                  ▓
       mampostería  │  ▓ EPS 100 mm (SATE)▓  ← continuo
     ═══════════════╡  ▓                  ▓
```

| # | Regla | Por qué |
|---|---|---|
| 1 | **Pendiente ≥ 5 %** hacia afuera | Con menos, el agua se estanca y con heladas revienta la junta |
| 2 | **Goterón continuo en el borde exterior** | Sin goterón, el agua vuelve por capilaridad a la cara del SATE y produce el churreteado y, con el tiempo, la degradación del revestimiento |
| 3 | **Orejas laterales que entran bajo el revestimiento** del SATE, al menos 3 cm a cada lado | Es por donde entra el agua en el 90 % de los alféizares mal hechos |
| 4 | **Membrana o banda de estanqueidad bajo el alféizar**, con vuelta hacia arriba en el encuentro con el marco | El alféizar no es estanco: lo que pasa por sus juntas tiene que ser conducido hacia afuera |
| 5 | **Retorno del aislante bajo el alféizar** | Idem dintel |
| 6 | **Junta elástica alféizar–marco** con silicona neutra y fondo de junta | El alféizar y el marco se dilatan distinto |

---

## 6.6 Encuentro MURO – PISO (arranque)

**Mecanismo:** si la aislación del muro termina al nivel del piso terminado, el muro y la fundación conducen calor hacia el terreno y hacia el aire exterior, **en todo el perímetro**. Es un puente lineal de 48 m en la casa de referencia.

### D-PT-06 — Arranque del SATE y encuentro con la aislación perimetral

```
        INTERIOR              │           EXTERIOR
                              │
   Solado                     │
   Carpeta                    │   ▓▓▓▓▓▓▓▓▓▓ EPS 100 (SATE) ▓▓▓▓
   CONTRAPISO (la masa)       │   ▓                             ▓
   ─────────────────────      │   ▓                             ▓
   ▓▓ XPS 30 mm (total) ▓▓    │   ══ PERFIL DE ARRANQUE de aluminio
   Film PE 200 μ              │      con GOTERÓN, ≥ 30 cm sobre el terreno
   Suelo compactado           │   ▓                             ▓
                              │   ▓▓ XPS 30 mm ▓▓  ← por debajo del perfil
   ═══════════════════════╗   │   ▓  (no EPS)   ▓     de arranque va XPS,
     MURO                 ║   │   ▓             ▓     protegido con revoque
   ═══════════════════════╣   │   ▓             ▓     impermeable armado
                          ║   │   ▓             ▓
   ▓▓ XPS 30 mm faja ▓▓▓▓▓║───┼───▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ← LA FAJA PERIMETRAL DEL
   perimetral vertical    ║   │   ▓  50–60 cm   ▓     PISO Y EL XPS DEL MURO
   (50 cm)                ║   │   ▓  bajo NPT   ▓     SE TOCAN
   ═══ VIGA DE FUNDACIÓN ═╝   │   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                              │
                              │   ═══ VEREDA PERIMETRAL 0,80–1,20 m,
                              │       pendiente 2 % hacia afuera
```

| # | Regla | Por qué |
|---|---|---|
| 1 | **El aislante del muro baja 50–60 cm por debajo del nivel de piso terminado** | Es lo que corta el camino del flujo por la fundación |
| 2 | **Por debajo del nivel del terreno: XPS, nunca EPS** | Absorción de agua |
| 3 | **Perfil de arranque de aluminio con goterón, ≥ 30 cm sobre el terreno** | Evita que el revestimiento del SATE toque el suelo |
| 4 | **La faja perimetral del piso (§4.4) y el XPS del muro deben tocarse** | Si no, queda un puente lineal continuo en 48 m |
| 5 | **Zócalo de mayor resistencia mecánica** (EPS de alta densidad, XPS, o placa de mortero armado) hasta 1,50–2,00 m | El SATE en planta baja de una casa recibe golpes: bicicletas, herramientas, cortadora de césped, granizo rebotado |
| 6 | **Vereda perimetral con pendiente 2 %** | Suelo loéssico: alejar el agua es simultáneamente estructural y térmico |

---

## 6.7 Tabique de medianera y muros que sobresalen del volumen

En una casa de una planta entre medianeras o con muros que continúan hacia afuera (muro de cerco vinculado, muro de galería, muro que sale a hacer un patio):

| Situación | Problema | Solución |
|---|---|---|
| **Muro de medianera que sobresale del plano de fachada** | Aleta de mampostería expuesta a dos caras, con el interior del otro lado | **Aislar por ambas caras el tramo sobresaliente, con retorno mínimo de 60 cm** hacia adentro del muro |
| **Muro de cerco o de patio vinculado estructuralmente al muro de la casa** | Aleta que sale del volumen aislado y conduce calor al exterior por su masa | **Independizar con junta**, o **envolver el arranque con aislación por las dos caras y por el coronamiento en al menos 60 cm** desde la fachada |
| **Muro divisorio entre casa y garaje no calefaccionado** | El garaje está a temperatura intermedia | Tratarlo como envolvente: **aislar el muro divisorio**. IRAM 11604 permite adoptar γ = 1,0 para el cerramiento, o calcular γ. La pérdida por el piso en ese tramo de perímetro se computa al **50 %** |
| **Muro de galería cubierta pero abierta** | El muro del fondo de la galería es envolvente; los muros laterales pueden no serlo | Definir explícitamente el contorno de la envolvente en el plano y aislar todo lo que quede en él |

> **Regla general para toda aleta:** si un elemento macizo atraviesa la envolvente y sale al exterior, hay tres opciones y sólo tres — **(a)** independizarlo estructuralmente con junta y aislante intermedio; **(b)** envolverlo con aislación por todas sus caras expuestas; **(c)** aislar el arranque con un retorno de al menos 60 cm a cada lado. **No hay una cuarta.**

---

## 6.8 Anclajes, fijaciones y pases de instalación

| Elemento | Severidad | Solución |
|---|---|---|
| **Espigas de fijación del SATE** que atraviesan el aislante | Baja individual, **acumulativa** (5–8 por m²) | Espiga con **cabeza de plástico y clavo de nylon**, no metálico. **Cabeza rehundida y tapada con tapón de EPS** — si no, aparece el "efecto lunares" en la fachada: cada espiga se marca como un punto frío que acumula suciedad |
| **Ménsulas de toldo, parasol, aire acondicionado, farol, cámara** | Media, puntual | Anclar con **separador térmico de poliamida** entre la ménsula y el muro. **Definir estos anclajes en proyecto**, no en obra: perforar un SATE terminado para colgar el toldo arruina el sistema |
| **Condensadora de aire acondicionado apoyada sobre el SATE** | Alta (peso + vibración + perforación) | **Ménsula pasante hasta la mampostería**, con separador térmico, o apoyo en el suelo |
| **Cajas de electricidad** en muro exterior | Baja térmicamente, **alta como fuga de aire** | No enfrentar cajas en el mismo hueco. Cajas estancas. Sellar el pase de la cañería |
| **Pases de caños de gas, agua, desagüe, conductos de extracción** | Media, y **fuga de aire directa** | **Sellar con espuma de PU + sellador elástico por ambas caras.** En la barrera de vapor, sellar con cinta específica |

---

## 6.9 Tabla resumen de puentes térmicos de la casa de una planta

### Tabla 6.2 — Catálogo, severidad y solución

| # | Puente térmico | ¿Existe en una casa de una planta? | Longitud típica (casa 130 m²) | Severidad | **Solución** | Detalle |
|---|---|---|---|---|---|---|
| 1 | **Encuentro muro–cubierta / parapeto** | **Sí, siempre** | **48 m** | **Muy alta** | Envolver el parapeto por sus tres caras; o **eliminar el parapeto y hacer alero** | D-PT-01 / 02 |
| 2 | **Encadenado superior** | **Sí, siempre** | 48 m | Alta | SATE continuo por delante | D-PT-03 |
| 3 | **Encadenado intermedio / de dintel** | Sí, salvo muro portante | 30–50 m | Alta | SATE continuo | D-PT-03 |
| 4 | **Columna embebida** | Sí, salvo muro portante | 10–20 unidades × 2,6 m | **Alta** (y **muy alta** si está en esquina) | SATE continuo; o **eliminar las columnas con muro portante** | — |
| 5 | **Dintel + cajón de persiana** | **Sí, en cada ventana** | 8–12 vanos | **Muy alta** — puente térmico + puente acústico + fuga de aire | Cajón exterior aislado, o compacto con 40 mm de EPS + burletes; SATE por delante; retorno del aislante sobre el marco | D-PT-04 |
| 6 | **Jamba y antepecho de vano** | **Sí, en cada ventana** | Perímetro de todos los vanos | Alta | **Retorno del aislante 20–30 mm sobre el marco**; alféizar con goterón y orejas | D-PT-04 / 05 |
| 7 | **Encuentro muro–piso (arranque)** | **Sí, siempre** | **48 m** | **Alta** | Aislante del muro 50–60 cm bajo NPT en XPS + faja perimetral del piso que lo encuentra | D-PT-06 |
| 8 | **Esquinas del edificio** (geométrico) | **Sí, 4 como mínimo** | 4 × 2,6 m | Media, **muy visible** (mancha de moho en el rincón) | El SATE lo resuelve casi por completo. Verificar con **Rsi = 0,50** de IRAM 11630 | — |
| 9 | **Tabique de medianera / muro que sobresale** | Según partido | Variable | Media-alta | Aislar por ambas caras con retorno ≥ 60 cm | — |
| 10 | **Muro divisorio con garaje no calefaccionado** | Frecuente | 8–10 m | Media | Tratarlo como envolvente; piso al 50 % en ese tramo | — |
| 11 | **Losa de galería o alero macizo vinculado** | Frecuente | 8–15 m | **Alta** — es una aleta de hormigón que sale del volumen | Envolver por arriba, abajo y canto; o **independizar estructuralmente** (columnas propias) | — |
| 12 | **Montante de acero (steel framing)** | Sólo en steel framing | Cada 40–60 cm | **Alta y repetitiva** | **EPS exterior continuo de 50 mm mínimo.** No hay otra | — |
| 13 | **Espigas, ménsulas y anclajes** | Sí | 5–8/m² + puntuales | Baja acumulativa | Espigas con cabeza plástica y tapón; separadores de poliamida | — |
| 14 | **Cajas y pases de instalación** | Sí | Muchos | Baja térmica, **alta como fuga** | Sellado sistemático | — |
| 15 | **Chimenea / conducto de humos que atraviesa la cubierta** | Frecuente en casas | 1–2 | **Alta**: puente térmico + fuga de aire + punto de filtración | Sellar la barrera de vapor contra el conducto con collarín; aislar el conducto con material apto para alta temperatura; babeta y contrababeta en la cubierta | — |

> ### LO QUE DICE ESTA TABLA
> **En una casa de una planta hay del orden de 150 a 200 metros lineales de puente térmico potencial** (encuentros 1, 2, 3, 7 y los perímetros de vanos), sobre 106,8 m² de muro. **Es una densidad de puentes altísima**, muy superior a la de un edificio en altura, porque la casa es toda perímetro.
>
> **Y la conclusión práctica es una sola:** las tres decisiones que resuelven el 90 % de los puentes térmicos de una casa de una planta en Santa Rosa son, en orden:
> 1. **Aislación exterior continua (SATE)**, que resuelve 1, 2, 3, 4, 5, 6, 8, 9 y 11.
> 2. **Continuidad de la aislación en los dos encuentros extremos** (muro-cubierta arriba, muro-piso abajo), que es donde el SATE tiene que "cerrarse" con otras dos aislaciones.
> 3. **Resolver el cajón de persiana**, o eliminarlo.

---

# 7. CONDENSACIÓN

> **Santa Rosa no es un clima seco en invierno.** La HR media de invierno es del **73 %** según IRAM 11603 (76 % según el otro dataset). Con TDMN de −6,0 °C y una casa a 20 °C con 70 % de HR interior, **el riesgo de condensación superficial e intersticial es real, y la propia IRAM 11603 lo dice explícitamente para las subzonas IVc y IVd: "se verificará el riesgo de condensación, controlando los puentes térmicos"**. La verificación no es opcional.

## 7.1 Condiciones de diseño adoptadas

| Parámetro | Valor | Origen |
|---|---|---|
| **Temperatura interior θi** | **20 °C** | Nivel B de IRAM 11605 (Nivel A: 22 °C; Nivel C: 18 °C) |
| **Humedad relativa interior HRi** | **70 %** | Hipótesis conservadora para local de permanencia de vivienda. `[VERIFICAR el valor que impone IRAM 11625 por tipo de local — puede diferenciar dormitorio, estar, cocina y baño]` |
| **Temperatura exterior θe** | **−6,0 °C** | TDMN, IRAM 11603 |
| **Humedad relativa exterior HRe** | **76 %** | Valor conservador entre 73 % (IRAM 11603) y 76 % (dataset alternativo) |
| **Rsi para verificación de PAÑO CENTRAL** | **0,17 m²K/W** | IRAM 11625 |
| **Rsi para PUNTOS SINGULARES** | **0,25 / 0,34 / 0,50 m²K/W** | IRAM 11630 (rincón diedro, triedro, detrás de mueble) |
| Rse | 0,04 | IRAM 11601 |

### Tabla 7.1 — Presión de vapor de saturación Pvs (referencia termodinámica)

| θ (°C) | Pvs (Pa) | | θ (°C) | Pvs (Pa) |
|---|---|---|---|---|
| 22 | 2.645 | | 5 | 872 |
| **20** | **2.337** | | 2 | 705 |
| 18 | 2.064 | | 0 | 611 |
| 17 | 1.937 | | −2 | 528 (sobre agua) / 517 (sobre hielo) |
| 16 | 1.817 | | −4 | 455 / 437 |
| **15** | **1.704** | | **−6** | **391 / 368** |
| 14 | 1.598 | | −8 | 335 / 310 |
| **13** | **1.497** | | −10 | 287 / 260 |
| 12 | 1.402 | | | |
| 10 | 1.228 | | | |

`[VERIFICAR contra la tabla de Pvs de IRAM 11625 antes de usar en una verificación formal. Los valores son los estándar de la formulación de Magnus.]`

### Los tres puntos de rocío que importan

```
Interior a 20 °C, HR 70 %:  Pv = 0,70 × 2.337 = 1.636 Pa  →  ROCÍO = 14,4 °C
Interior a 20 °C, HR 60 %:  Pv = 0,60 × 2.337 = 1.402 Pa  →  ROCÍO = 12,0 °C
Interior a 20 °C, HR 50 %:  Pv = 0,50 × 2.337 = 1.169 Pa  →  ROCÍO =  9,3 °C
Exterior a −6 °C, HR 76 %:  Pv = 0,76 ×   368 =   280 Pa
```

> **La HR interior es una variable de proyecto, no un dato del clima.** Bajar la HR interior de 70 % a 60 % baja el punto de rocío **2,4 K** y es, muchas veces, más barato que agregar aislante: se consigue con **extracción mecánica en baños y cocina**, **no secar ropa adentro**, y **campana de cocina que descargue al exterior**. Es lo primero que hay que verificar en una casa con moho.

## 7.2 Condensación SUPERFICIAL

### Método

```
θsi = θi − (Rsi / RT) × (θi − θe)          [°C]
CONDICIÓN:  θsi > θrocío interior

Factor de temperatura superficial:  fRsi = (θsi − θe) / (θi − θe)
fRsi REQUERIDO en Santa Rosa = (14,4 − (−6,0)) / (20 − (−6,0)) = 20,4 / 26,0 = 0,785
```

> ### **CRITERIO DEL ESTUDIO: fRsi ≥ 0,80 EN TODO PUNTO DE LA ENVOLVENTE**
> (El criterio alemán de DIN 4108-2 es fRsi ≥ 0,70, pero está calibrado para condiciones menos severas. **Con TDMN −6,0 y HRi 70 %, el mínimo teórico en Santa Rosa es 0,785**; se adopta 0,80 con un pequeño margen.)

### Tabla 7.2 — Verificación en PAÑO CENTRAL (Rsi = 0,17), θi = 20 °C, θe = −6 °C, rocío 14,4 °C

| Solución | RT con Rsi = 0,17 | **θsi (°C)** | **fRsi** | ¿Condensa? | Margen sobre el rocío |
|---|---|---|---|---|---|
| **M1 — hueco 18 revocado** | 0,674 | **13,44** | **0,748** | **SÍ** | **−0,96 K** |
| M2 — EPS 50 interior + placa | 2,102 | 17,90 | 0,919 | No | +3,50 K |
| **M3 — SATE EPS 60** | 2,376 | **18,14** | 0,928 | No | +3,74 K |
| **M4 — SATE EPS 100** | 3,519 | **18,74** | **0,952** | No | **+4,34 K** |
| M9 — HCCA 20 revocado | 1,892 | 17,66 | 0,910 | No | +3,26 K |
| **T1 — losa sin aislar** | 0,545 | **11,89** | **0,688** | **SÍ** | **−2,51 K** |
| **T9 — losa + EPS 120** | 4,414 | **19,00** | **0,962** | No | **+4,60 K** |
| **Vidrio simple 6 mm** (K 5,80) | 0,342 | **7,08** | 0,503 | **SÍ, masivamente** | **−7,32 K** |
| DVH 6-12-6 (K 2,80) | 0,527 | 11,61 | 0,677 | **SÍ** | −2,79 K |
| **DVH low-E 6-12-6** (K 1,80) | 0,726 | **13,91** | 0,766 | **SÍ, al límite** (con HRi 60 %: **NO condensa**, margen +1,91 K) | −0,49 K |
| **Ventana completa RPT + DVH low-E** (K 2,13) | 0,600 | 12,63 | 0,716 | Sí con HRi 70 %; **no con HRi 60 %** | −1,77 K |

> ### CUATRO CONCLUSIONES
> **1. El muro estándar de Santa Rosa condensa.** Con 20 °C y 70 % de HR adentro y −6 afuera, la cara interior del hueco 18 revocado queda a **13,4 °C**, casi 1 K por debajo del rocío. No es teoría: es la mancha de humedad en el rincón del dormitorio que tiene la mitad de las casas de la ciudad.
> **2. La losa sin aislar condensa peor todavía**: 11,9 °C, 2,5 K bajo el rocío. Es la mancha en el encuentro de techo y pared.
> **3. El vidrio condensa siempre, incluso el mejor.** Con HRi de 70 %, ni el DVH low-E salva. **La condensación en el vidrio es la señal de que la HR interior es demasiado alta**, no de que el vidrio sea malo: bajando la HR interior a 60 %, el DVH low-E deja de condensar y el vidrio simple sigue chorreando.
> **4. La aislación exterior resuelve el problema con margen de 3,5 a 4,6 K**, que es lo que permite que la casa tolere un pico de humedad (una ducha, una olla, ropa tendida) sin que aparezca agua en las paredes.

### Tabla 7.3 — Verificación en PUNTOS SINGULARES (IRAM 11630): rincones y detrás de muebles

**Éste es el cálculo que separa una casa Nivel B de una casa Nivel A.**

| Solución | Rsi = 0,25 (arista) | Rsi = 0,34 | **Rsi = 0,50 (triedro / detrás de mueble)** | Veredicto |
|---|---|---|---|---|
| **M1 — hueco 18 revocado** | θsi = **11,25** ✗ | θsi = **9,26** ✗ | θsi = **7,05** ✗✗ | **Condensa en todas partes** |
| **M2 — EPS 50 interior** | 17,05 ✓ | 16,18 ✓ | **14,65** ✓ *(margen 0,25 K)* | **Al límite** |
| **M3 — SATE EPS 60** | 17,35 ✓ | 16,53 ✓ | **15,20** ✓ *(margen 0,80 K, fRsi 0,815)* | **Al límite** |
| **M4 — SATE EPS 100** | 18,25 ✓ | 17,60 ✓ | **16,62** ✓ *(margen 2,22 K, fRsi 0,870)* | **Con margen real** |
| **M9 — HCCA 20 revocado** | 16,88 ✓ | 15,83 ✓ | **14,15** ✗ *(rocío 14,4 — CONDENSA)* | **No verifica en triedro** |

*(Cálculo: `θsi = 20 − (Rsi / (RT_base − 0,13 + Rsi)) × 26`, con RT_base el de la Tabla 2.1.)*

> ### **POR QUÉ EL NIVEL A NO ES UN LUJO EN SANTA ROSA**
> Un muro **Nivel B** (M3, K = 0,43) **verifica el paño central con holgura, pero queda al límite en el triedro y detrás de un mueble: 0,80 K de margen.** Basta con que la HR interior suba a 72 %, o con que el comitente ponga un ropero contra el muro sur, para que aparezca moho.
>
> Un muro **Nivel A** (M4, K = 0,29) tiene **2,22 K de margen en el mismo punto**. Esa diferencia —40 mm de EPS— es la diferencia entre una casa que tolera el uso real y una que exige que el usuario se comporte perfecto.
>
> **Y el HCCA de 20 cm revocado, que verifica cómodamente el Nivel B en paño central, NO verifica el triedro.** Es la razón por la que este documento recomienda **HCCA 20 + SATE de 60 mm** (M9c) y no HCCA solo.

### Dónde condensa una casa mal resuelta — el mapa

| Lugar | Por qué | Qué se ve |
|---|---|---|
| **Rincones y aristas (diedros y triedros)** | Puente geométrico: la superficie exterior que capta frío es mayor que la interior que emite, y en el rincón el aire tiene menor movilidad por rozamiento y no homogeneiza la temperatura. **Rsi efectivo 0,25–0,50 en lugar de 0,17** | **La mancha negra en la esquina superior del dormitorio.** El diagnóstico número uno |
| **Detrás de muebles apoyados contra muros exteriores** | El mueble bloquea la convección: Rsi sube a 0,50. Además la superficie está oculta y nadie la ve hasta que huele | Moho en la pared detrás del ropero, y en la cara posterior del mueble |
| **Dinteles, jambas y antepechos** | Puente térmico constructivo: mampostería fría rodeando cada ventana, sin retorno del aislante | Mancha perimetral alrededor de la ventana, en el borde del revoque |
| **Cajón de persiana** | Puente térmico + entrada de aire frío + falta de ventilación de la cavidad | Moho en el interior del cajón y en el cielorraso adyacente |
| **Encuentro techo–pared** | Encadenado + esquina geométrica + aire caliente y húmedo que asciende y se estanca ahí | Línea de moho corrida en todo el perímetro del cielorraso |
| **Sobre el vidrio y en el marco de aluminio sin RPT** | K 5,8–6,0: la superficie está prácticamente a la temperatura exterior | Agua chorreando, charco en el contramarco, madera de contramarco podrida, moho en la mocheta |
| **Bajo la chapa, en cubierta liviana sin barrera de vapor** | El vapor asciende, atraviesa la lana y llega a la cara interior de la chapa a **−5,7 °C** | Goteo sobre el cielorraso que parece filtración de lluvia pero aparece en días secos y fríos |
| **Baños y cocinas sin extracción** | Producción localizada de vapor sin evacuación: la HR local sube a 85–95 % | Moho en el cielorraso del baño, en la junta de los azulejos, en el ángulo de la ducha |
| **Locales cerrados y poco usados** (dormitorio de huéspedes, vestidor) | Sin renovación de aire ni aporte de calor, la temperatura superficial baja y la humedad se acumula | Olor a humedad, moho en la ropa guardada |

## 7.3 Condensación INTERSTICIAL

### Método (Glaser, IRAM 11625/11630)

Se calcula, en cada interfaz entre capas: **(a)** la temperatura, por reparto de las resistencias térmicas; **(b)** la presión de vapor **real**, por reparto de las **resistencias a la difusión de vapor** (Sd = μ × e, donde μ es el factor de resistencia a la difusión del material). **Si la presión real supera la de saturación a esa temperatura, condensa.**

```
θ(x) = θi − (ΣR hasta x / RT) × (θi − θe)
Pv(x) = Pvi − (ΣSd hasta x / ΣSd total) × (Pvi − Pve)
CONDICIÓN:  Pv(x) < Pvs(θ(x))  en todo punto
```

**Valores de μ adoptados** — `[VERIFICAR TODOS en la ficha técnica del producto y en IRAM 11601; son órdenes de magnitud de la literatura]`:

| Material | μ | Sd por espesor típico |
|---|---|---|
| Revoque de mortero | ≈ 20 | 0,025 m → 0,50 m |
| Ladrillo cerámico hueco | ≈ 10 | 0,18 m → 1,80 m |
| **EPS 20 kg/m³** | ≈ 30 | 0,06 m → **1,80 m** / 0,10 m → **3,00 m** |
| Placa de roca de yeso | ≈ 8 | 0,0125 m → 0,10 m |
| Lana de vidrio | ≈ 1 | 0,10 m → 0,10 m |
| Revestimiento acrílico transpirable | — | ≈ 0,3 m |
| **Film de polietileno 200 μ** | — | **≈ 20–50 m** (es barrera de vapor) |
| **Chapa metálica** | ∞ | **Barrera de vapor absoluta** |

---

### CASO A — Muro con aislación EXTERIOR (M3, SATE de EPS 60 mm)

**Plano crítico: cara exterior de la mampostería (interfaz ladrillo–EPS).**

```
R acumulada hasta el plano = 0,17 + 0,029 + 0,410 + 0,004 = 0,613
RT = 2,376
θ = 20 − (0,613 / 2,376) × 26 = 20 − 6,71 = 13,29 °C
Pvs(13,29 °C) ≈ 1.527 Pa

Sd hasta el plano = 0,50 (revoques int) + 1,80 (ladrillo) + 0,10 (adhesivo) = 2,40 m
Sd total = 2,40 + 1,80 (EPS 60) + 0,30 (revestimiento) = 4,50 m
Pv = 1.636 − (2,40 / 4,50) × (1.636 − 280) = 1.636 − 723 = 913 Pa
```

| | Presión de vapor real | Presión de saturación | ¿Condensa? |
|---|---|---|---|
| Interfaz ladrillo–EPS | **913 Pa** | **1.527 Pa** | **NO — margen de 614 Pa (40 %)** |

**Con SATE de 100 mm (M4):** θ en la interfaz = 20 − (0,613/3,519) × 26 = **15,47 °C** → Pvs = 1.758 Pa; Pv = 1.636 − (2,40/5,70) × 1.356 = **1.065 Pa**. **NO condensa, margen de 693 Pa.**

> ### **CON AISLACIÓN EXTERIOR NO HACE FALTA BARRERA DE VAPOR.**
> Y **cuanto más grueso el aislante exterior, mayor el margen**: el aislante calienta el punto crítico. Es la razón física por la que el SATE es la solución higrotérmicamente robusta. **El único requisito es que el revestimiento exterior sea PERMEABLE AL VAPOR** (revestimiento acrílico o siliconado transpirable). **Un esmalte impermeable sobre un SATE atrapa la humedad y produce ampollas.**

---

### CASO B — Muro con aislación INTERIOR (M2, EPS 50 mm por dentro), SIN barrera de vapor

**Plano crítico: cara fría del EPS (interfaz EPS–ladrillo).**

```
R acumulada hasta el plano = 0,17 + 0,028 + 1,429 = 1,627
RT = 2,102
θ = 20 − (1,627 / 2,102) × 26 = 20 − 20,13 = −0,13 °C
Pvs(−0,13 °C) ≈ 610 Pa

Sd hasta el plano = 0,10 (placa) + 1,50 (EPS 50) = 1,60 m
Sd total = 1,60 + 1,80 (ladrillo) + 0,50 (revoques ext) = 3,90 m
Pv = 1.636 − (1,60 / 3,90) × 1.356 = 1.636 − 556 = 1.080 Pa
```

| | Presión de vapor real | Presión de saturación | ¿Condensa? |
|---|---|---|---|
| Interfaz EPS–ladrillo | **1.080 Pa** | **610 Pa** | **SÍ — supera la saturación en 470 Pa (77 %)** |

**Con barrera de vapor del lado cálido:**

| Sd de la barrera de vapor | Pv en la interfaz | Pvs (610 Pa) | ¿Condensa? |
|---|---|---|---|
| Sin barrera | 1.080 Pa | 610 | **SÍ** |
| Sd = 10 m (film PE fino) | 504 Pa | 610 | No, **margen 106 Pa (escaso)** |
| **Sd = 20 m (film PE 200 μ bien ejecutado)** | **410 Pa** | 610 | **No, margen 200 Pa** |
| Sd = 50 m (foil de aluminio) | 341 Pa | 610 | No, margen 269 Pa |

> ### **LA AISLACIÓN INTERIOR EXIGE BARRERA DE VAPOR CON Sd ≥ 20 m, CONTINUA Y SELLADA.**
> Y esa continuidad es la que nunca se logra en obra: cada caja de electricidad, cada pase de cañería, cada empalme mal solapado y cada perforación para colgar un cuadro es un agujero. **Por eso el estudio no recomienda la aislación interior en obra nueva.** No porque el K sea peor —M2 tiene K = 0,49 y M3 tiene 0,43, están cerca— sino **porque la solución interior sólo funciona si se ejecuta perfecta, y la exterior funciona aunque se ejecute con las imperfecciones normales de una obra.**

---

### CASO C — Cubierta de chapa con lana de vidrio, SIN barrera de vapor

**Plano crítico: cara interior de la chapa.**

```
R acumulada hasta el plano = 0,10 + 0,028 + 2,500 + 0,35 = 2,978
RT = 3,018
θ = 20 − (2,978 / 3,018) × 26 = 20 − 25,66 = −5,66 °C
Pvs(−5,66 °C) ≈ 380 Pa
```

**Y la difusión de vapor:** la chapa es una **barrera de vapor absoluta (μ = ∞) del lado FRÍO**. El vapor entra por el cielorraso, atraviesa la lana (μ ≈ 1: prácticamente no ofrece resistencia) y **no tiene por dónde salir**. La presión de vapor en la cara interior de la chapa tiende al **valor interior (1.636 Pa)** contra una saturación de **380 Pa**.

| | Presión de vapor real | Presión de saturación | ¿Condensa? |
|---|---|---|---|
| Cara interior de la chapa | **≈ 1.636 Pa** | **380 Pa** | **SÍ — 4,3 veces la saturación** |

> ### **LA CUBIERTA METÁLICA ES EL CASO MÁS PELIGROSO DE TODOS.**
> La chapa es una barrera de vapor **del lado equivocado**: impide que el vapor salga y le ofrece una superficie a −5,7 °C donde condensar. **El agua se forma en la cara interior de la chapa, gotea sobre la lana —que pierde su capacidad aislante y no la recupera— y de ahí sobre el cielorraso.** Aparece en días fríos y secos, lo que hace que se diagnostique erróneamente como filtración de lluvia.
>
> **Las dos defensas, y hacen falta LAS DOS:**
> 1. **Barrera de vapor continua del lado cálido** (inmediatamente sobre el cielorraso), con **Sd ≥ 20 m**, solapada 15 cm, sellada con cinta en todos los solapes y **sellada contra cada perforación** (luminarias, conducto de extracción, chimenea, tirantes).
> 2. **Cámara de aire VENTILADA entre el aislante y la chapa**, de al menos 40 mm, con entrada en el alero y salida en la cumbrera. **Es lo que evacúa el vapor que inevitablemente atraviesa la barrera.**
>
> **Si sólo se puede hacer una, hacer las dos igual.** No hay atajo.

## 7.4 Barrera de vapor: dónde va y por qué

### La regla del lado cálido

> ### **LA BARRERA DE VAPOR VA SIEMPRE DEL LADO CÁLIDO DE LA AISLACIÓN.**
>
> **Por qué.** El vapor migra de donde hay más presión de vapor (el interior cálido y húmedo) hacia donde hay menos (el exterior frío y seco). Si la barrera está del lado cálido, **frena el vapor antes de que llegue a la zona fría** donde podría condensar. Si está del lado frío, **el vapor entra, llega a la barrera, se encuentra con una superficie fría e impermeable y condensa contra ella**: la barrera pasa de ser la solución a ser la causa.
>
> **En Argentina "lado cálido" = lado interior**, porque el problema dominante es el invierno (GD18 1.394 contra una demanda de refrigeración mucho menor). En un clima tropical con aire acondicionado permanente sería al revés.

### Tabla 7.4 — Las dos barreras: no confundirlas

| | **BARRERA DE VAPOR** | **BARRERA DE AGUA Y VIENTO** (membrana respirante) |
|---|---|---|
| **Qué frena** | **Vapor de agua** (difusión) | **Agua líquida** y **aire**; deja pasar el vapor |
| **Dónde va** | **Lado CÁLIDO (interior) del aislante** | **Lado FRÍO (exterior) del aislante** |
| **Material** | Film de PE 200 μ, foil de aluminio, pintura barrera de vapor, membrana asfáltica | Membrana de polipropileno microporoso ("tyvek" y equivalentes) |
| **Sd** | **≥ 20 m** | **≤ 0,3 m** (debe ser transpirable) |
| **Error clásico** | Colocarla del lado frío, o discontinua | Usar un film de PE como membrana exterior: **atrapa el vapor y arruina el muro** |

### Tabla 7.5 — Cuándo hace falta y cuándo no, en las soluciones de este documento

| Solución | ¿Barrera de vapor? | Dónde | Por qué |
|---|---|---|---|
| **M3 / M4 — SATE sobre mampostería** | **NO** | — | El aislante exterior mantiene todo el muro por encima del rocío (Caso A). Sólo se exige que el revestimiento exterior sea permeable al vapor |
| **M2 — aislación interior** | **SÍ, imprescindible, Sd ≥ 20 m** | Entre la placa de yeso y el EPS | Caso B |
| **M5 / M6 — muro doble con aislante en cámara** | **Verificar caso por caso.** Generalmente sí, del lado interior del aislante | Sobre la cara interior de la hoja interior | Depende de la relación de resistencias |
| **M10 — steel framing** | **SÍ, imprescindible, Sd ≥ 20 m** | Entre la placa de yeso interior y la lana | El OSB y la membrana exterior no frenan el vapor |
| **T2 / T9 — cubierta plana tradicional (aislante bajo la membrana)** | **SÍ** | **Entre la losa y el aislante** | Si no, el vapor llega al aislante, condensa y además **forma ampollas bajo la membrana** al evaporarse en verano |
| **T3 — cubierta INVERTIDA** | **NO** | — | **La propia membrana es la barrera de vapor, y está del lado cálido del XPS.** Es la ventaja higrotérmica de la cubierta invertida |
| **T5 / T8 — cubierta de chapa o teja con lana** | **SÍ, imprescindible, Sd ≥ 20 m** | Inmediatamente sobre el cielorraso | Caso C |
| **T6 — panel sándwich** | **Integrada** | Las dos chapas | La chapa interior es la barrera de vapor. **El punto débil son las juntas entre paneles** |
| **T7 — teja con machimbre a la vista** | **SÍ** | Entre el machimbre y el aislante (el techado asfáltico cumple esa función) | El machimbre es permeable |
| **Piso sobre terreno** | **SÍ (aquí es corte de capilaridad, no barrera de vapor)** | Film de PE 200 μ bajo el contrapiso y bajo el aislante | Evita el ascenso de humedad del suelo, que arruinaría el aislante |

### Los cinco errores con las barreras

1. **Ponerla del lado frío.** Convierte la barrera en el plano de condensación.
2. **Ponerla discontinua.** Una barrera con el 1 % de la superficie abierta pierde la mayor parte de su eficacia: el vapor busca el agujero. **Solapes de 15 cm sellados con cinta, sellado perimetral contra muros y contra cada perforación.**
3. **Perforarla después.** Cada spot embutido, cada tornillo de cielorraso, cada caja de electricidad. **Resolver la iluminación por debajo del plano de la barrera**, en un cielorraso técnico.
4. **Poner dos barreras, una de cada lado del aislante.** El aislante queda encerrado: la humedad que entre (y siempre entra algo, por la ejecución) **no puede salir por ningún lado**. Regla: **una sola barrera, del lado cálido; del lado frío, permeable.**
5. **Confundir el reflectivo con aislante.** Un foil de aluminio **es una barrera de vapor** y aporta, en el mejor caso tabulado por IRAM 11601, el equivalente a 7 mm de EPS —y sólo con cámara de aire y superficie limpia. **Colocado del lado equivocado, produce condensación.**

---

# 8. ESTRATEGIAS PASIVAS

> **En una casa de una planta, las estrategias pasivas rinden más que en cualquier otra tipología**, por tres razones: toda la casa es planta baja (todos los locales pueden tener orientación buena), todo el techo está disponible para captar o proteger, y hay contacto directo con el terreno y con el jardín. **Lo que se resuelve con el partido no hay que pagarlo en aislante ni en equipos.**

## 8.1 Orientación óptima

**Recomendación de IRAM 11603 para Zona IV** (verificada): para latitudes mayores a 30°, las **orientaciones favorables son NO – N – NE – E**. Santa Rosa está a **36,57° S**: la fachada norte es el recurso energético principal.

### Tabla 8.1 — Programa por orientación en una casa de una planta

| Orientación | Locales | Por qué | Superficie vidriada |
|---|---|---|---|
| **NORTE** | **Estar, comedor, dormitorio principal, estudio.** Todo lo de permanencia diurna prolongada | Sol de invierno todo el día (h de 30° al mediodía: entra profundo en el local); sol de verano alto (77°), que un alero corta por completo. **Es la única orientación donde una ventana puede ganar más de lo que pierde** | **55–65 % del total** |
| **ESTE** | Dormitorios, cocina, desayunador | Sol de la mañana; en verano el sol de la mañana es tolerable porque el aire todavía está fresco. **En invierno, calienta el dormitorio a la hora de levantarse** | 15–20 % |
| **SUR** | **Servicios: lavadero, despensa, baño, garaje, circulaciones, depósito.** Escaleras si las hubiera | Sin ganancia solar directa nunca. **Los locales de servicio hacen de colchón térmico entre el sur frío y los locales de permanencia** | **10–15 %, mínimo indispensable** |
| **OESTE** | **Lo mínimo posible: garaje, depósito, muro ciego, o galería protegida.** Nunca dormitorio de niños ni estar | **El problema de verano.** Sol de las 16–19 h, casi horizontal, contra el aire en su máxima temperatura del día | **5–10 %, siempre protegido** |

### Tabla 8.2 — Forma y compacidad

| Estrategia | Efecto | Aplicación en casa de una planta |
|---|---|---|
| **Minimizar la relación superficie de envolvente / volumen (factor de forma)** | Una casa compacta pierde menos con la misma superficie útil | Una casa de 130 m² en un rectángulo de 16 × 8 tiene 384,8 m² de envolvente; **la misma superficie en forma de L de 3 alas puede llegar a 450–480 m² (+20 %)**. Cada quiebre del perímetro cuesta calor |
| **Alargar el eje ESTE-OESTE** | Maximiza la fachada norte y minimiza la este y la oeste | El rectángulo 16 × 8 con el lado largo al norte es la forma correcta. **Nunca al revés** |
| **Locales de doble altura, patios internos, atrios** | Aumentan la superficie de envolvente | En clima con 1.394 GD18, **cada m² adicional de envolvente cuesta energía todos los inviernos**. Usar con criterio |
| **Volumen del garaje / galería como amortiguador** | Protege la fachada más expuesta | **Poner el garaje al oeste o al sur** es una de las decisiones pasivas más eficaces y de costo cero |

## 8.2 Cálculo de alero para latitud 36,57° S

### Los ángulos solares de Santa Rosa

```
Altura solar al mediodía solar:   h = 90° − |φ − δ|      (φ = −36,57°)

21 de JUNIO   (solsticio de invierno, δ = +23,45°):  h = 90 − 60,02 = 29,98° ≈ 30,0°
21 de MARZO / 23 de SEPTIEMBRE (equinoccios, δ = 0):  h = 90 − 36,57 = 53,43°
21 de DICIEMBRE (solsticio de verano, δ = −23,45°):   h = 90 − 13,12 = 76,88°
```

### Tabla 8.3 — Ángulos solares de Santa Rosa (36,57° S)

| Fecha | δ | **Altura al mediodía solar** | tan(h) | **Azimut de salida / puesta del sol** (desde el norte) |
|---|---|---|---|---|
| **21 de junio** (invierno) | +23,45° | **30,0°** | **0,577** | **60,3° / 299,7°** — es decir, **30° al NORTE del E y del O** |
| 21 de marzo / 23 de septiembre | 0° | **53,4°** | 1,348 | 90° / 270° — exactamente E y O |
| **21 de diciembre** (verano) | −23,45° | **76,9°** | **4,289** | **119,7° / 240,3°** — es decir, **30° al SUR del E y del O** |

**Posición del sol en las horas críticas de verano (21 de diciembre, hora solar):**

| Hora solar | **Altura h** | **Azimut** | Qué fachada golpea |
|---|---|---|---|
| 12:00 | **76,9°** | 0° (norte) | Norte, casi vertical → **el alero la corta** |
| 15:00 | 50,1° | 285,4° (ONO) | Norte y **oeste** |
| **16:00** | **37,3°** | **266,7° (O)** | **OESTE, casi perpendicular** |
| **17:00** | **26,0°** | **259,1° (O-SO)** | **OESTE, perpendicular. Hora de temperatura máxima del día** |
| 18:00 | 13,7° | 250,8° (OSO) | **Oeste, radiación casi horizontal** |

> **A las 16–18 h del 21 de diciembre el sol está prácticamente al oeste, con alturas de 14° a 37°.** Ningún alero horizontal lo detiene: para cortar un rayo a 26° de altura desde arriba haría falta una proyección de **P = H / tan(26°) = 2,10 / 0,488 = 4,30 m**. **La fachada oeste no se protege con alero. Punto.** (§8.5)

### El cálculo del alero para la fachada NORTE

```
Sombra proyectada sobre el muro, medida desde el borde del alero:

        d = P × tan(h)

donde P = proyección horizontal del alero [m]
      h = altura solar al mediodía solar [°]
      d = profundidad de la sombra sobre el muro, hacia abajo [m]

Para sombrear COMPLETAMENTE una abertura de altura H cuyo dintel coincide
con el alero, en el solsticio de verano:

        P = H / tan(76,88°) = H / 4,289 = 0,233 × H
```

### Tabla 8.4 — Alero necesario y su efecto en las tres fechas

**Caso 1: el alero está a la altura del dintel (hd = 0)**

| Altura de la abertura H | **P necesario** (21 dic) | Sombra el 21 jun (d = 0,577 P) | **% de la ventana sombreado en invierno** | Sombra en el equinoccio (d = 1,348 P) | % sombreado en el equinoccio |
|---|---|---|---|---|---|
| 1,80 m | **0,42 m** | 0,24 m | 13 % | 0,57 m | 32 % |
| 2,00 m | **0,47 m** | 0,27 m | 14 % | 0,63 m | 32 % |
| **2,10 m** | **0,49 m** | **0,28 m** | **13 %** | 0,66 m | 31 % |
| 2,40 m | **0,56 m** | 0,32 m | 13 % | 0,76 m | 32 % |
| 2,60 m | **0,61 m** | 0,35 m | 13 % | 0,82 m | 32 % |

**Caso 2: el alero está elevado 0,40 m por encima del dintel (hd = 0,40) — LA SOLUCIÓN MEJOR**

| Altura de la abertura H | **P necesario** = (0,40 + H)/4,289 | Sombra el 21 jun desde el alero | Parte de la ventana sombreada en invierno | **% sombreado en invierno** |
|---|---|---|---|---|
| 2,00 m | **0,56 m** | 0,32 m | **0 m** (0,32 < 0,40) | **0 % — SOL PLENO** |
| **2,10 m** | **0,58 m** | 0,34 m | **0 m** | **0 % — SOL PLENO** |
| 2,40 m | **0,65 m** | 0,38 m | **0 m** | **0 % — SOL PLENO** |
| 2,60 m | **0,70 m** | 0,40 m | **0 m** (justo) | **0 % — SOL PLENO** |

> ### **LA REGLA DEL ALERO PARA SANTA ROSA**
> ## **Alero de 0,55 a 0,70 m de proyección, colocado 0,30 a 0,40 m por encima del dintel.**
>
> **Resultado:**
> - **21 de diciembre al mediodía: sombra completa** sobre toda la abertura.
> - **21 de junio al mediodía: sol pleno** sobre toda la abertura. Ganancia solar invernal íntegra.
> - **Equinoccios: la ventana queda sombreada en su tercio superior**, lo que es aproximadamente lo que se quiere en marzo (aún calor) y algo conservador en septiembre (aún frío).
>
> **Elevar el alero por encima del dintel es el truco que casi nadie usa y que resuelve la contradicción "quiero sombra en verano y sol en invierno".** Cuesta nada: es la altura del antepecho de cubierta o del canto de la losa.
>
> ### La limitación del alero fijo, dicha con honestidad
> Un alero fijo es **simétrico respecto del solsticio**: sombrea igual el 21 de octubre que el 21 de febrero, aunque en octubre todavía haga frío y en febrero calor. **El desfase térmico del año (el mes más caluroso es enero-febrero, no diciembre) hace que el alero fijo sombree de más en primavera y de menos en otoño.** Si el proyecto lo justifica:
> - **Parral o pérgola con vid o glicina** al norte: hoja en verano, sin hoja en invierno, **y el desfase de la planta coincide con el desfase térmico** mucho mejor que el alero.
> - **Toldo retráctil**, controlado por el usuario.
> - **Alero + persiana**, que da el ajuste fino.

## 8.3 Masa térmica e inercia

**El dato que lo habilita todo: amplitud térmica media de verano de 14,4 K** (máxima media 29,4 °C, mínima media 15,0 °C). Con esa amplitud y una mínima nocturna de 15 °C, **Santa Rosa está en el escenario ideal para enfriamiento pasivo por masa + ventilación nocturna**.

### El mecanismo

```
DÍA (12–19 h):   La casa está cerrada, con protección solar. La masa (contrapiso, losa,
                 muros interiores) absorbe el calor que entra y lo almacena.
                 El interior se mantiene 5–8 K por debajo del exterior.

NOCHE (23–7 h):  El exterior baja a 15–18 °C. Se ventila intensamente (cruzada).
                 La masa descarga el calor al aire de la noche.

MAÑANA:          La masa vuelve a estar "cargada de frío" y el ciclo se repite.
```

### Tabla 8.5 — Parámetros y objetivos

| Parámetro | Definición | Objetivo en clima cálido-seco de gran amplitud |
|---|---|---|
| **Capacidad térmica areal κ** (kJ/m²K) | Masa × calor específico de las capas **accesibles desde el interior** | Lo más alta posible en las superficies interiores |
| **Retardo o desfasaje φ** (horas) | Tiempo que tarda la onda térmica en atravesar el cerramiento | **10–12 h**: que el pico de calor exterior de las 16 h llegue al interior a las 2–4 de la mañana, cuando ya se está ventilando |
| **Factor de amortiguamiento f** | Amplitud de la onda interior / amplitud de la exterior | **f ≤ 0,10** |

*El cálculo de φ y f requiere método dinámico (**ISO 13786**); IRAM 11601 es estacionario y no lo captura.* `[VERIFICAR con simulación dinámica (EnergyPlus, DesignBuilder, Simusol) en proyectos donde el verano sea crítico.]`

### LA REGLA DE POSICIÓN

> ### **AISLACIÓN AFUERA, MASA ADENTRO.**
>
> La misma cantidad de masa y de aislante da resultados **opuestos** según el orden:
>
> | Configuración | Qué pasa | Ejemplo |
> |---|---|---|
> | **Aislante por fuera, masa por dentro** | La masa está en contacto térmico con el aire interior. **Absorbe y libera calor al interior: la inercia funciona** | **M3, M4, M7, M8, M11 — SATE.** Es la configuración correcta |
> | **Aislante por dentro, masa por fuera** | La masa queda del lado frío. El interior "ve" 12,5 mm de placa de yeso. **La inercia se pierde por completo**, y aparece riesgo de condensación intersticial | M2 — trasdosado interior |
> | **Masa encerrada entre dos aislantes** | La inercia existe pero **no está disponible para el interior**. La casa se calienta y se enfría rápido | ICF, panel sándwich |
> | **Sin masa** | Sigue instantáneamente la temperatura exterior | M10 steel framing, T6 panel sándwich |

### Dónde poner la masa en una casa de una planta

| Elemento | Aporte | Nota |
|---|---|---|
| **CONTRAPISO DE HORMIGÓN, sin aislante entre él y el interior** | **La masa más barata y más efectiva de todas.** 10 cm de hormigón sobre 130 m² son ~31 toneladas en contacto directo con el aire interior | **El orden correcto es: aislante ABAJO, contrapiso ARRIBA** (§4.4). Con solado de porcelanato u hormigón alisado (no alfombra ni flotante grueso, que aíslan la masa) |
| **LOSA DE CUBIERTA de hormigón, con el aislante por encima** | ~300 kg/m² × 130 m² = 39 toneladas, disponibles desde el interior | Es la razón por la que **T9 (losa + EPS por encima) gana a T6 (panel sándwich)** en este clima |
| **Muros exteriores con SATE** | 250–450 kg/m² accesibles desde adentro | |
| **Tabiques interiores de MAMPOSTERÍA en lugar de tabiquería seca**, al menos en los locales que reciben sol directo | Masa donde llega la radiación | Un tabique de hueco 8 revocado son ~130 kg/m² |
| **Muro acumulador / muro Trombe en la fachada norte** | Captación + acumulación solar invernal | Solución avanzada; `[VERIFICAR el diseño con simulación]` |
| Placas de yeso de alta densidad o doble placa | Aporte modesto pero no nulo | Recurso para sistemas livianos |
| Materiales de cambio de fase (PCM) | Tecnología disponible internacionalmente | `[VERIFICAR disponibilidad y costo en Argentina]` |

> **Si se elige un sistema liviano (steel framing, panel sándwich, wood frame), la masa hay que recuperarla en el piso.** Contrapiso pesado, solado de alta conductividad y capacidad (porcelanato, hormigón alisado, piedra), tabiques interiores de mampostería. **De lo contrario, en Santa Rosa se está renunciando a la mejor herramienta climática del lugar.**

## 8.4 Ventilación cruzada y nocturna

**Advertencia de IRAM 11603 para las subzonas secas de la Zona IV:** se recomienda **ventilación SELECTIVA combinada con inercia térmica**, no ventilación cruzada permanente. Es decir: **ventilar cuando el aire exterior es más fresco que el interior, y cerrar cuando no.**

### Tabla 8.6 — Régimen de ventilación por estación y hora

| Momento | Exterior | Acción | Por qué |
|---|---|---|---|
| **Verano, 7–11 h** | 15–22 °C | **Ventilar a fondo** | Terminar de descargar la masa |
| **Verano, 11–20 h** | 25–35 °C, hasta 38,8 de diseño | **CERRAR todo. Persianas y protección solar bajadas** | Ventilar con el exterior a 33 °C es meter calor. **Éste es el error de uso más frecuente** |
| **Verano, 21 h – 7 h** | 15–22 °C | **VENTILACIÓN NOCTURNA INTENSIVA**, cruzada, con la mayor superficie posible | Es el mecanismo de enfriamiento pasivo. **Objetivo: 10–30 renovaciones por hora durante la noche** `[VERIFICAR el caudal con cálculo de ventilación natural]` |
| **Invierno** | −6 a 16 °C | **Ventilación mínima higiénica**, concentrada (ventilación "de golpe": abrir 5–10 minutos con todo abierto, 2–3 veces al día) | Renovar el aire sin enfriar la masa. **Una ventana entreabierta todo el día enfría la masa y no renueva mejor** |

### Requisitos de proyecto para que la ventilación cruzada funcione

| # | Requisito | Detalle |
|---|---|---|
| 1 | **Aberturas en fachadas OPUESTAS o al menos adyacentes**, en todos los locales de permanencia | Un local con ventanas en una sola pared no ventila cruzado: ventila por difusión, que es 5–10 veces menos efectivo |
| 2 | **Superficie de salida ≥ superficie de entrada**, idealmente mayor | El caudal lo limita la abertura más chica. Si la salida es mayor, la velocidad de entrada aumenta |
| 3 | **Camino de aire libre**: puertas interiores con paso de aire (rejilla, luz inferior de 1,5–2 cm), o el partido resuelto en planta libre | Una puerta cerrada anula la ventilación cruzada de todo el sector |
| 4 | **Aprovechar el efecto chimenea**: abertura alta de salida (ventana alta, claraboya practicable, linterna) + abertura baja de entrada | El aire caliente sale por arriba y aspira aire fresco por abajo. **Funciona incluso sin viento**, que es cuando más se necesita |
| 5 | **Orientar las entradas hacia el viento dominante de verano** `[VERIFICAR la rosa de vientos de Santa Rosa: IRAM 11603 da VM = 12,5 en verano pero no la dirección]` | |
| 6 | **Seguridad**: la ventilación nocturna exige poder dejar aberturas abiertas de noche | **Ventanas oscilobatientes** (posición oscilante), **postigones con celosía**, **rejas de diseño** o **paños superiores fijos con banderola practicable**. Sin resolver la seguridad, el usuario cierra todo y la estrategia no se usa |
| 7 | **Protección contra insectos**: mosquiteros en todas las aberturas de ventilación nocturna | Sin mosquitero, no se abre. Y el mosquitero reduce el caudal un 20–50 % `[VERIFICAR]`: sobredimensionar |
| 8 | **Protección contra el polvo y el viento fuerte** | En La Pampa una noche de viento con tierra obliga a cerrar. Preverlo: postigón exterior que permita ventilar con la ventana protegida |

## 8.5 Protección solar en el OESTE — el problema de verano

> **La fachada oeste es el problema de verano de Santa Rosa, y no se resuelve ni con aislante ni con alero.**
>
> **Por qué el aislante no alcanza:** el muro oeste con SATE de 100 mm (K = 0,29) recibe a las 17 h del 21 de diciembre una radiación casi perpendicular. Con la temperatura sol-aire (`T_sa ≈ T_ext + α·I/h_e`), un muro de color medio (α = 0,7) con I ≈ 650 W/m² y h_e ≈ 22,7 W/m²K alcanza:
> ```
> T_sa ≈ 38,8 + (0,7 × 650 / 22,7) ≈ 38,8 + 20,0 = 58,8 °C
> ```
> **El muro oeste "ve" 58,8 °C, no 38,8.** El Δt efectivo pasa de 13,8 K a 33,8 K.
>
> **Por qué el alero no alcanza:** el sol de las 17 h está a 26° de altura y prácticamente al oeste. Un alero horizontal necesitaría **4,30 m de proyección** para sombrear una ventana de 2,10 m.

### Tabla 8.7 — Soluciones para el oeste, ordenadas por eficacia

| # | Solución | Eficacia | Costo | Observaciones |
|---|---|---|---|---|
| **1** | **NO ABRIR AL OESTE.** Poner ahí el garaje, el depósito, el lavadero, un muro ciego | **Total** | **Cero — es una decisión de partido** | **Es la única solución perfecta, y es gratis si se toma en el anteproyecto** |
| **2** | **Parasoles VERTICALES orientables** (lamas verticales, celosías móviles) en el plano de la fachada | **Muy alta** | Alto | Los verticales son los que sirven para el oeste; los horizontales no. Orientables porque el azimut cambia mucho en el día |
| **3** | **Postigón exterior ciego u orientable** de aluminio o madera | **Muy alta** | Medio | Además elimina el cajón de persiana y da seguridad. **La mejor relación eficacia/costo** |
| **4** | **Persiana de enrollar exterior**, bajada de 15 a 20 h | **Muy alta** cuando está bajada | Medio | Depende del uso; y el cajón hay que resolverlo (§5.5) |
| **5** | **Vegetación de hoja caduca al oeste**: árbol de copa ancha a 3–6 m de la fachada | **Alta**, y con el desfase estacional correcto | Bajo, pero **tarda 5–10 años** | **Precaución en suelo loéssico: alejar del perímetro una distancia ≥ altura adulta del árbol** para no desecar/rehidratar el suelo de fundación |
| **6** | **Galería o pérgola profunda al oeste** (§8.6) | Alta | Medio-alto | Además crea espacio de uso |
| **7** | **Vidrio de CONTROL SOLAR** en las aberturas oeste | Media (reduce, no elimina) | Medio | **Es complemento, no sustituto**: el vidrio de control solar detiene parte de la radiación pero se calienta y reemite hacia adentro |
| **8** | **Muro claro (α < 0,6) al oeste** | Media | **Cero** | Baja la T sol-aire de 58,8 a ~50 °C con α = 0,4. **Y la norma premia el muro claro con +20 % de K admisible** |
| ✗ | Cortina o persiana **interior** | **Baja** | Bajo | La radiación ya entró y se convirtió en calor dentro del local. **Toda protección solar eficaz es EXTERIOR** |

> ### **REGLA: TODA PROTECCIÓN SOLAR EFICAZ ES EXTERIOR.** Una cortina interior detiene la luz, no el calor.

## 8.6 La galería como espacio de transición

> **La galería es la respuesta tipológica del clima pampeano, y sigue siendo la mejor idea disponible.** No es nostalgia: es un dispositivo bioclimático de precisión.

| Función | Cómo la cumple |
|---|---|
| **Protección solar de verano** | Una galería al norte de 2,50–3,00 m de profundidad sombrea la fachada completa al mediodía de verano y hasta buena parte de la tarde |
| **Ganancia solar de invierno** | Con altura suficiente (2,80–3,20 m de altura libre), **el sol de invierno a 30° entra bajo la galería y llega hasta 4,8–5,5 m adentro del local** (`profundidad = altura / tan 30° = altura × 1,732`) |
| **Espacio de uso real** | En Santa Rosa se vive afuera de octubre a abril. La galería es superficie de uso a costo de semicubierto |
| **Amortiguador térmico** | El aire de la galería está siempre más templado que el exterior: el muro que da a la galería pierde y gana menos |
| **Protección de la fachada contra la lluvia batida y el viento** | Prolonga la vida del revestimiento del SATE |
| **Protección de las carpinterías** | Menos UV, menos agua, menos mantenimiento |

### Reglas de diseño de la galería

```
Altura libre h de la galería, para que el sol de invierno (30°) entre P metros:
        P = h × tan(60°) = h × 1,732

    h = 2,60 m  →  el sol de invierno llega 4,50 m adentro
    h = 2,80 m  →  el sol de invierno llega 4,85 m adentro
    h = 3,20 m  →  el sol de invierno llega 5,54 m adentro

Profundidad de la galería para sombra completa en verano (77°):
    la galería sombrea la fachada completa si su profundidad ≥ h / 4,289
    h = 2,80 m  →  profundidad ≥ 0,65 m  (cualquier galería real lo cumple)
```

> **Es decir: la galería sombrea totalmente en verano con cualquier profundidad razonable, y deja entrar el sol de invierno hasta 5 m si tiene altura suficiente.** **La altura de la galería es más importante que su profundidad.** Una galería baja (2,40 m) al norte bloquea el sol de invierno y es un error térmico.

| Regla | Detalle |
|---|---|
| **Galería al NORTE: alta y de profundidad moderada** (2,80–3,20 m de altura, 2,50–3,00 m de profundidad) | Sombra total en verano, sol profundo en invierno |
| **Galería al OESTE: profunda y con protección vertical en el extremo** | El sol de las 17 h entra horizontal por el lateral: la galería sola no alcanza, hay que cerrar el testero oeste con celosía o vegetación |
| **Piso de la galería: material claro y permeable si es posible** | Un piso oscuro se calienta y reirradia hacia el interior |
| **La estructura de la galería debe ser INDEPENDIENTE de la del muro**, o su vínculo debe aislarse | Si la losa o la viga de la galería es continua con la estructura del muro, es un puente térmico de primer orden (§6.7) |
| **Techo de la galería: no hace falta aislarlo** (no es envolvente), pero conviene que sea **claro o ventilado** | Un techo de chapa oscura a 2,80 m sobre una galería la vuelve inhabitable en enero |

## 8.7 Color de cubierta y de fachada

| Superficie | α recomendado | Materialización | Beneficio |
|---|---|---|---|
| **CUBIERTA** | **α < 0,6, y cuanto más bajo mejor** | Membrana con **foil de aluminio**, pintura acrílica reflectiva blanca sobre membrana, chapa galvanizada o prepintada blanca, teja clara o engobada clara | **+30 % de K admisible** → ahorra 40 mm de EPS en toda la cubierta. Y baja la temperatura superficial de la cubierta de ~70 °C a ~45 °C `[VERIFICAR con medición]` |
| **FACHADA NORTE** | Media a clara | Revoque claro (α 0,40) o color medio | **+20 % de K admisible** de verano si α < 0,6. Al norte el alero ya protege, hay margen para el color |
| **FACHADA OESTE** | **α < 0,6 obligatorio** | **Revoque claro o blanco** | Baja la T sol-aire de 58,8 a ~50 °C. **Es gratis y ataca directamente el problema de verano** |
| **FACHADA SUR** | Indiferente térmicamente | Libre | El sur no recibe radiación directa |
| **Revestimiento del SATE** | **Claro, obligatorio por razón técnica además de térmica** | Los colores oscuros sobre EPS acumulan temperatura y **deforman la placa**, fisurando el revestimiento. Los fabricantes de SATE limitan el índice de reflectancia mínimo | `[VERIFICAR el índice de reflectancia (IR/Y) mínimo que exige el fabricante del sistema — típicamente IR ≥ 20–25]` |
| **PISO de galerías, patios y veredas al norte y oeste** | Claro | Hormigón peinado claro, baldosón claro, grava clara | Un piso exterior oscuro frente a un ventanal reirradia calor hacia el interior toda la tarde |

> **Y el mantenimiento es parte de la especificación:** el beneficio del color claro **se pierde cuando la superficie se ensucia**. En una ciudad con viento y tierra, la cubierta clara pierde reflectancia en 3–5 años. **Consignar el repintado o el lavado de cubierta en el manual de uso y mantenimiento de la vivienda**, con periodicidad de 4–6 años. Si el proyecto no puede garantizar ese mantenimiento, **calcular con α medio (0,7) y no con α < 0,6.**

---

# 9. PRIORIDAD DE INVERSIÓN

## 9.1 El balance completo de la casa de referencia

**Casa de referencia:** planta baja única, 130 m² cubiertos (16,0 × 8,0 m), altura de local 2,60 m, **V = 338 m³**, perímetro en contacto con el terreno **48 m**, muro exterior neto **106,8 m²**, techo **130 m²**, aberturas **18 m²**.

**Coeficiente G admisible (IRAM 11604:2001, Tabla 1, interpolado):**
```
GD18 = 1.394 °C·día ;  V = 338 m³
V = 300 m³:  1.300 °D → 1,615  ;  1.400 °D → 1,598  ;  a 1.394 °D → 1,599
V = 400 m³:  1.300 °D → 1,531  ;  1.400 °D → 1,516  ;  a 1.394 °D → 1,517
V = 338 m³:  1,599 + (38/100) × (1,517 − 1,599) = 1,599 − 0,031 = 1,568

                    G adm ≈ 1,57 W/m³K
```

### Tabla 9.1 — Tres escenarios de envolvente: G y carga térmica anual

Fórmula de IRAM 11604 §6.1: `G = [Σ(K·S) + Per·Pp] / V + 0,35·n`, con **n = 2** por defecto.
Carga térmica anual (§6.7.1): `Q = 24 × GD18 × G × V / 1000` [kWh/año].

| Elemento | **ESC. 1 — Construcción corriente** | **ESC. 2 — Nivel B** | **ESC. 3 — Nivel A** |
|---|---|---|---|
| **Muro** | M1 hueco 18: K = 1,58 | M3 SATE 60: K = 0,43 | **M4 SATE 100: K = 0,29** |
| Pérdida muro (106,8 m²) | 168,7 W/K | 45,7 W/K | 30,7 W/K |
| **Techo** | T1 losa sin aislar: K_inv = 2,11 | T2 losa + EPS 60: K_inv = 0,457 | **T9 losa + EPS 120: K_inv = 0,232** |
| Pérdida techo (130 m²) | **273,7 W/K** | 59,4 W/K | 30,2 W/K |
| **Aberturas** | Aluminio s/RPT + simple: K = 5,86 | Aluminio RPT + DVH: K = 2,82 | **RPT + DVH low-E: K = 2,13** |
| Pérdida aberturas (18 m²) | 105,5 W/K | 50,8 W/K | 38,3 W/K |
| **Piso** | Sin aislación: Pp = 1,38 | Aislación perimetral: Pp = 1,08 | **Aislación total: Pp = 0,93** |
| Pérdida piso (48 m) | 66,2 W/K | 51,8 W/K | 44,6 W/K |
| **Σ pérdidas por conducción** | **614,1 W/K** | **207,7 W/K** | **143,8 W/K** |
| Conducción / V | 1,817 W/m³K | 0,614 W/m³K | 0,425 W/m³K |
| **Infiltración** (0,35 × n) | n = 2 → 0,700 | n = 2 → 0,700 | **n = 1 → 0,350** (carpintería A2 + sellado ejecutado) |
| **G calculado** | **2,517 W/m³K** | **1,314 W/m³K** | **0,775 W/m³K** |
| **¿G ≤ G adm (1,57)?** | **✗ NO — 60 % por encima** | **✓ SÍ (−16 %)** | **✓✓ SÍ (−51 %)** |
| **Carga térmica anual Q** | **28.463 kWh/año** | **14.859 kWh/año** | **8.764 kWh/año** |
| Reducción respecto de ESC. 1 | — | **−48 %** | **−69 %** |
| Equivalente en gas natural (9,3 kWh/m³, rend. 90 %) | **≈ 3.401 m³/año** | **≈ 1.775 m³/año** | **≈ 1.047 m³/año** |

> **Advertencias de método, declaradas:**
> - `Q` de IRAM 11604 supone **calefacción 24 h/día durante toda la temporada, sin ganancias solares ni internas**. **Sobreestima el consumo absoluto**; los **ahorros comparativos entre escenarios sí son válidos** porque el sesgo es idéntico en los tres.
> - El poder calorífico del gas (9,3 kWh/m³) y el rendimiento estacional (90 %) son **`[VERIFICAR]`**.
> - **La construcción corriente de Santa Rosa NO CUMPLE el coeficiente G de IRAM 11604**, con un 60 % de exceso. No es un detalle: es el resultado que aparece en cualquier verificación que se haga.

## 9.2 Tabla de costo-beneficio: qué se gana con cada peso

**Fórmula:** `Ahorro anual [kWh] = 24 × 1.394 × ΔUA / 1.000 = 33,456 × ΔUA`

### Tabla 9.2 — Medidas ordenadas por AHORRO ABSOLUTO

| # | Medida | ΔK o Δ | Superficie / longitud | **ΔUA (W/K)** | **Ahorro (kWh/año)** | **Ahorro (m³ gas/año)** | Costo relativo de la medida | **Rendimiento** (kWh/año por unidad de costo relativo) |
|---|---|---|---|---|---|---|---|---|
| **1** | **Aislar la CUBIERTA** (de T1 a T9 con EPS 120) | 2,11 → 0,232 | 130 m² | **243,5** | **8.147** | **973** | **Medio-bajo** (30) | **272** |
| **2** | **Aislar los MUROS** con SATE 60 (de M1 a M3) | 1,58 → 0,43 | 106,8 m² | **122,7** | **4.105** | **490** | **Alto** (65) | **63** |
| **3** | **Estanqueidad al aire** (de n = 2 a n = 1) | 0,35 × 338 | — | **118,3** | **3.958** | **473** | **Muy bajo** (8) | **495** |
| **4** | **Carpinterías: de aluminio s/RPT + simple a RPT + DVH** | 5,86 → 2,82 | 18 m² | **54,7** | **1.830** | **219** | **Alto** (55) | **33** |
| **5** | **Engrosar el SATE de 60 a 100 mm** (de M3 a M4) | 0,43 → 0,29 | 106,8 m² | **15,1** | **505** | **60** | Bajo (12) | **42** |
| **6** | **Aislar el PISO en perímetro** (de sin aislar a perimetral) | 1,38 → 1,08 | 48 m | **14,4** | **482** | **58** | **Muy bajo** (4) | **121** |
| **7** | **Vidrio low-E** (de DVH a DVH low-E) | 2,82 → 2,13 | 18 m² | **12,4** | **415** | **50** | Medio (15) | **28** |
| **8** | **Engrosar la cubierta de 120 a 180 mm de EPS** | 0,232 → 0,176 | 130 m² | **7,3** | **244** | **29** | Bajo (10) | **24** |
| **9** | **Piso: de perimetral a total** | 1,08 → 0,93 | 48 m | **7,2** | **241** | **29** | Bajo (8) | **30** |
| **10** | **Cerrar las persianas de noche** (efecto declarado por IRAM 11507-4) | −0,3 a −0,5 W/m²K | 18 m² | **≈ 7,2** | **≈ 241** | **≈ 29** | **CERO** | **∞** |

*Costo relativo: escala arbitraria interna (mismo orden de magnitud entre filas), **estimación del estudio**.* `[VERIFICAR con presupuesto real de Santa Rosa: es el único dato que falta para convertir esta tabla en un análisis económico cerrado.]`

## 9.3 EL ORDEN DE INVERSIÓN

> ### SI EL PRESUPUESTO NO ALCANZA PARA TODO, SE GASTA EN ESTE ORDEN

| Orden | Medida | Por qué va acá | Costo | Qué NO hacer antes |
|---|---|---|---|---|
| **0** | **LAS DECISIONES DE PARTIDO: orientación, compacidad, eje E-O, aleros, servicios al sur y al oeste, galería al norte** | **Cuestan CERO** y determinan la mitad del comportamiento de la casa. Una vez dibujada la planta, no se pueden recuperar | **$0** | No pasar al presupuesto sin haber orientado la casa |
| **1** | **AISLAR LA CUBIERTA. EPS de 120 mm sobre la losa + terminación CLARA.** Bovedilla de EPS en lugar de cerámica | **8.147 kWh/año, el ahorro absoluto más grande de toda la lista**, y el aislante más barato de colocar (no roba superficie, no exige oficio especial). En una casa de una planta el techo es el 41 % de la envolvente | Medio-bajo | Nada. **Es el primer peso que se gasta** |
| **2** | **ESTANQUEIDAD AL AIRE: carpintería clasificada A2, sellado perimetral con fondo de junta, cajón de persiana resuelto o eliminado, pases sellados** | **3.958 kWh/año por casi nada.** Es el mejor rendimiento por peso de toda la tabla. Y en una casa Nivel A la infiltración es el 45–62 % de la pérdida total | **Muy bajo** | No pagar DVH antes de sellar el perímetro de la ventana |
| **3** | **AISLAR EL PISO EN EL PERÍMETRO. XPS de 30 mm × 50 cm en 48 m** | **482 kWh/año por 24 m² de XPS.** Y es **irrecuperable después**: no se puede aislar el perímetro de una casa terminada sin romper la vereda y el contrapiso | **Muy bajo** | Nada. **Se hace o no se hace nunca** |
| **4** | **AISLAR LOS MUROS: SATE de 60 mm (Nivel B)** | **4.105 kWh/año.** Es el segundo ahorro absoluto, pero el costo por m² es alto. **Es también lo que elimina todos los puentes térmicos y el riesgo de condensación** | Alto | — |
| **5** | **CARPINTERÍAS: aluminio con RPT + DVH** | **1.830 kWh/año**, y **elimina la condensación sobre el marco**, que es el origen del deterioro. **El RPT antes que el low-E** | Alto | No comprar low-E con marco sin RPT |
| **6** | **ENGROSAR EL SATE de 60 a 100 mm (pasar de Nivel B a Nivel A)** | 505 kWh/año. Pero además: **es lo que da 2,2 K de margen de condensación detrás de los muebles** en lugar de 0,8 K (§7.2). El argumento no es energético, es patológico | Bajo (el material ya está en obra, sólo cambia el espesor de la placa) | — |
| **7** | **VIDRIO LOW-E, empezando por sur y oeste** | 415 kWh/año, y es lo que finalmente elimina la condensación sobre el vidrio | Medio | — |
| **8** | **Piso con aislación total; engrosar la cubierta a 180 mm; DVH con argón** | Refinamientos de rendimiento decreciente | Bajo-medio | — |

### Los tres errores de asignación de presupuesto más caros

| Error | Por qué es un error | Qué hacer en su lugar |
|---|---|---|
| **Poner DVH y dejar el techo sin aislar** | El techo ahorra **8.147 kWh/año**; el DVH ahorra **1.830**. Con el mismo dinero se compra 4,5 veces más ahorro en el techo. Y es lo que se hace habitualmente, porque el DVH se ve y el aislante del techo no | **Techo primero, siempre** |
| **Comprar losa radiante en una casa sin aislar** | Con envolvente corriente la carga es de **170 W/m²** y la losa radiante emite **100 W/m²** como máximo: **no calienta**. Se gasta en el sistema y la casa sigue fría | **Aislar primero; la losa radiante sólo con envolvente Nivel B verificada** |
| **Gastar en un equipo de aire acondicionado más grande en lugar de resolver el oeste y el techo** | Un equipo grande enfría un local con carga de 150–200 W/m² gastando electricidad todos los veranos durante 20 años. **Cerrar el oeste y pintar la cubierta de blanco cuesta una vez y no consume nada** | **Protección solar y cubierta clara primero** |

## 9.4 El argumento para el comitente

> **Una casa de 130 m² en Santa Rosa construida como se construye habitualmente consume del orden de 3.400 m³ de gas por año en calefacción. La misma casa en Nivel B consume 1.775 m³. En Nivel A, 1.047 m³.**
>
> **La diferencia entre la casa corriente y la casa Nivel A son 2.354 m³ de gas por año, todos los años, durante los 50 o 60 años de vida de la casa.** A eso hay que agregarle:
> - **el equipo de calefacción más chico** que se compra el primer día (la carga baja de 22.146 W a 6.854 W: **la potencia instalada se divide por 3**);
> - **la ausencia de moho, humedad y deterioro** en rincones, dinteles y detrás de los muebles;
> - **el confort real**: sin paredes frías, sin corrientes de aire, sin condensación en los vidrios;
> - **el valor de reventa y la etiqueta de eficiencia energética** (La Pampa está adherida al PRONEV);
> - y **la posibilidad de usar losa radiante o una bomba de calor**, que en una casa sin aislar directamente no funcionan.
>
> **El sobrecosto está concentrado en tres rubros —aislante de cubierta, SATE y carpinterías— y representa una fracción del costo total de la obra.** `[VERIFICAR el porcentaje con presupuesto real: el orden de magnitud citado en la bibliografía para el mercado argentino es del 4 % al 10 % del costo de construcción, con repagos de 2 a 6 años para los niveles C, B y A respectivamente en el AMBA — y en Santa Rosa, con 1.394 GD18 contra ~1.150 del AMBA, más rápido.]`

---

# 10. CHECKLIST DE ENVOLVENTE PARA EL PROYECTO DE UNA CASA

## 10.1 Anteproyecto — antes de dibujar la planta definitiva

- [ ] ¿Se usó **TDMN = −6,0 °C**, **TDMX = 38,8 °C** y **GD18 = 1.394** (IRAM 11603, estación Santa Rosa Aero)? ← *No usar −2,7 / 33,8 / 1.331 (§1.1)*
- [ ] ¿Se fijó el **nivel objetivo de IRAM 11605** y está escrito en la memoria? (Objetivo del estudio: **A**; piso contractual: **B**)
- [ ] ¿El **eje largo de la casa está E-O**, con la fachada larga al **norte**?
- [ ] ¿Los locales de **permanencia están al N y al E**, y los **servicios al S y al O**?
- [ ] ¿Se **evitó abrir al oeste**? Si hay aberturas al oeste, ¿está definida la **protección solar exterior**?
- [ ] ¿El **factor de forma** es razonable? (¿Se contó cuántos metros de perímetro agregó cada quiebre de la planta?)
- [ ] ¿La **relación superficie vidriada / superficie opaca de muro es ≤ 15 %** (IRAM 11603 Zona IV) y está concentrada al norte (55–65 % del vidrio total)?
- [ ] ¿Está previsto el **alero de 0,55–0,70 m, elevado 0,30–0,40 m sobre el dintel**, en la fachada norte? (§8.2)
- [ ] ¿Hay **galería al norte con altura libre ≥ 2,80 m** (para que entre el sol de invierno)?
- [ ] ¿Todos los locales de permanencia tienen **ventilación cruzada** (aberturas en fachadas opuestas o adyacentes)?
- [ ] ¿Está resuelta la **seguridad y el mosquitero** de las aberturas que quedarán abiertas de noche en verano?
- [ ] ¿Se decidió **cubierta con alero y canaleta** en vez de **parapeto y embudo**? (§6.1)
- [ ] ¿El **garaje / depósito está al oeste o al sur**, haciendo de amortiguador?

## 10.2 Proyecto — definición de la envolvente

### Muros
- [ ] ¿La solución de muro verifica **K ≤ 0,30** (A) o al menos **≤ 0,80** (B)? ¿Está el **cálculo de K según IRAM 11601** en el legajo?
- [ ] ¿La **aislación es EXTERIOR y continua** (SATE, fachada ventilada, o cámara con aislante y detalle de puentes resuelto)?
- [ ] ¿La **masa queda del lado interior** del aislante? (Aislación afuera, masa adentro)
- [ ] ¿Se descartó explícitamente el **muro de hueco 18 sin aislar** (K 1,58, no verifica ni C), el **bloque de hormigón sin aislar** (K 2,36) y el **muro doble con cámara vacía** (K 0,86, no verifica B)?
- [ ] ¿El **revestimiento exterior del SATE es permeable al vapor** y de **color claro** (α < 0,6 y con el índice de reflectancia que exige el fabricante)?
- [ ] ¿Está especificado el **sistema SATE completo de un único fabricante**, con su manual de colocación adjunto al pliego?
- [ ] ¿Está definida la **cantidad y tipo de fijaciones por m² para la zona de viento de La Pampa** (CIRSOC 102)?
- [ ] ¿Hay **zócalo de mayor resistencia mecánica** hasta 1,50–2,00 m en planta baja?

### Techo
- [ ] ¿La cubierta se verificó **por la condición de VERANO, con flujo descendente (Rsi = 0,17)**?
- [ ] ¿Verifica **K ≤ 0,19** (A) / **≤ 0,48** (B), **corregido por el α real de la terminación**?
- [ ] ¿Se determinó el **α de la terminación de cubierta** con la ficha del producto? (Membrana, teja, chapa)
- [ ] ¿La terminación es **CLARA (α < 0,6)** y está consignado su **mantenimiento** (repintado cada 4–6 años) en el manual de uso?
- [ ] ¿Se especificó **bovedilla de EPS** en lugar de cerámica? (0,44 m²K/W gratis)
- [ ] ¿La aislación del techo es del orden del **doble** que la del muro? (IRAM 11603, Zona IV)
- [ ] Si hay cámara o ático: ¿está **ventilada**, con entrada en alero y salida en cumbrera, con **bafles** que impidan que el aislante tape el paso?
- [ ] Si es cubierta de chapa o de teja con lana: ¿hay **barrera de vapor continua del lado cálido (Sd ≥ 20 m)** Y **cámara ventilada de ≥ 40 mm** bajo la chapa? ← *Las dos, no una*
- [ ] ¿La lana **NO queda comprimida** por las correas?
- [ ] Si es cubierta invertida: ¿el **lastre está calculado por succión de viento**?
- [ ] ¿Las **cañerías y conductos pasan POR DEBAJO de la aislación** (lado cálido)? ← *TMA de −11,3 °C: lo que quede arriba se congela*
- [ ] ¿Las **luminarias no perforan la barrera de vapor** (cielorraso técnico o luminarias estancas aptas)?

### Piso
- [ ] ¿Está prevista la **aislación perimetral** (R ≥ 0,7 m²K/W, ancho ≥ 50 cm, XPS 30 mm) como mínimo?
- [ ] En Nivel A o con losa radiante: ¿es **aislación total**?
- [ ] Con **losa radiante**: ¿la aislación es total, con **R ≥ 1,25 m²K/W**, densidad ≥ 30 kg/m³, **banda perimetral de 8–10 mm**, y **faja perimetral vertical** además?
- [ ] ¿El **contrapiso queda POR ENCIMA del aislante** (la masa del lado interior)?
- [ ] ¿Hay **film de polietileno de 200 μ** bajo el contrapiso y bajo el aislante (corte de capilaridad)?
- [ ] ¿La **faja perimetral del piso se toca con el XPS del muro** (que baja 50–60 cm bajo NPT)?
- [ ] ¿Está la **vereda perimetral de 0,80–1,20 m con pendiente 2 % hacia afuera**? ← *Suelo loéssico: es un detalle estructural y térmico*

### Carpinterías
- [ ] ¿Todas las aberturas de la envolvente tienen **RPT o son de PVC**?
- [ ] ¿Todas tienen **DVH como mínimo**? ¿**Low-E en sur y oeste**?
- [ ] ¿Ninguna abertura de la envolvente queda con **K > 4,0** (IRAM 11507-4: **no clasificable**)?
- [ ] ¿Se especificó la **clasificación IRAM 11507-1 mínima: A2 de infiltración** (no A1)?
- [ ] ¿Se privilegiaron **ventanas de abrir / oscilobatientes** sobre corredizas, y las corredizas grandes son **elevables**?
- [ ] ¿Hay **cierre multipunto** en hojas de más de 1,20 m de alto?
- [ ] ¿El **cajón de persiana está resuelto**: exterior, o compacto con 40 mm de EPS y burletes en tapa y pasacinta? ¿O eliminado a favor de **postigón exterior**?
- [ ] ¿El **premarco es de PVC o madera**, nunca de chapa doblada?
- [ ] ¿Está dibujado el **retorno del aislante 20–30 mm sobre el marco** en jamba, dintel y antepecho?
- [ ] ¿El **alféizar tiene pendiente ≥ 5 %, goterón y orejas laterales** que entran bajo el revestimiento?
- [ ] ¿Está especificado el **sellado con fondo de junta, relación 2:1 y silicona neutra**?
- [ ] ¿Está prohibido en el pliego **tapar los drenajes del marco con silicona**?
- [ ] ¿Se pidió al proveedor la **planilla con K, factor solar g y transmisión luminosa TL** de cada composición ofertada?

### Puentes térmicos
- [ ] ¿Se listaron **todos** los puentes térmicos del proyecto y cada uno tiene su detalle dibujado? (Tabla 6.2)
- [ ] ¿Se verificó que **K_pt ≤ 1,5 × K_muro** (o ≤ 1,35 si están a ≤ 1,7 m)?
- [ ] ¿Se verificó **fRsi ≥ 0,80** en cada encuentro?
- [ ] ¿La aislación del muro y la de la cubierta **se tocan** en todo el perímetro? (D-PT-01/02)
- [ ] ¿La aislación del muro y la del piso **se tocan** en todo el perímetro? (D-PT-06)
- [ ] ¿Hay **doble malla a 45° en las cuatro esquinas de cada vano**?
- [ ] ¿Los **anclajes de toldos, parasoles, condensadoras y faroles están definidos en proyecto**, con separador térmico? ← *No perforar el SATE terminado*
- [ ] ¿La **estructura de la galería es independiente** del muro, o su vínculo está aislado?

### Condensación
- [ ] ¿Se hizo la verificación de **condensación superficial (IRAM 11625)** en paño central, con **Rsi = 0,17**?
- [ ] ¿Se hizo la verificación en **puntos singulares (IRAM 11630)** con **Rsi = 0,25 / 0,34 / 0,50**? ← *Es la que decide entre Nivel B y Nivel A*
- [ ] ¿Se hizo la verificación de **condensación intersticial** (Glaser) en cada cerramiento con aislante?
- [ ] ¿La **barrera de vapor está del lado cálido** en cada solución que la requiere? (Tabla 7.5)
- [ ] ¿Hay **una sola barrera** (no dos, encerrando el aislante)?
- [ ] ¿Está previsto el **sellado de la barrera de vapor** en solapes, perímetros y perforaciones?
- [ ] ¿Hay **extracción mecánica en baños y cocina**, con descarga al exterior? ← *Bajar la HR interior de 70 % a 60 % baja el rocío 2,4 K: a veces más barato que aislante*
- [ ] ¿Hay lugar previsto para **secar la ropa** que no sea el interior de la casa?

### Estanqueidad y ventilación
- [ ] ¿Están **sellados todos los pases de instalación** que atraviesan la envolvente?
- [ ] ¿Las **cajas de electricidad de muros exteriores no están enfrentadas** en el mismo hueco, y son estancas?
- [ ] Si hay **hogar a leña o estufa**: ¿tiene **toma de aire exterior conducida y regulable**?
- [ ] ¿Está prevista la **ventilación controlada** (extracción en húmedos, microventilación o entradas regulables en secos)? ← *Sellar sin ventilar produce condensación*
- [ ] ¿Se previó un **ensayo Blower Door** al terminar? `[VERIFICAR disponibilidad del servicio en la región]`

## 10.3 Documentación a producir

- [ ] **Planilla de cálculo de K** por elemento (IRAM 11601), con las capas, λ, Rt y las resistencias superficiales correctas por estación
- [ ] **Planilla de verificación de K máximo admisible** (IRAM 11605), **invierno Y verano**, con la corrección por α
- [ ] **Planilla de verificación de condensación** superficial e intersticial (IRAM 11625 / 11630)
- [ ] **Planilla de coeficiente G** (IRAM 11604), con G_cal ≤ G_adm
- [ ] **Detalles constructivos a escala 1:5 / 1:10** de: encuentro muro-cubierta, encuentro muro-piso, dintel con cajón de persiana, antepecho con alféizar, jamba, arranque del SATE, encuentro con la galería
- [ ] **Planilla de carpinterías** con K de la ventana completa, clasificación IRAM 11507-1 y -4, y composición de vidrio con g y TL
- [ ] **Memoria técnica** con el nivel de IRAM 11605 adoptado y su justificación
- [ ] **Manual de uso y mantenimiento** de la vivienda: régimen de ventilación estacional, cierre de persianas de noche en invierno, protección solar de verano, repintado de cubierta, limpieza de canaletas, mantenimiento del revestimiento del SATE
- [ ] **Etiqueta de eficiencia energética (IRAM 11900 / PRONEV)** — La Pampa está adherida `[VERIFICAR el registro de certificadores habilitados]`

## 10.4 Obra — los diez controles que hay que hacer sí o sí

| # | Momento | Control |
|---|---|---|
| 1 | **Antes del contrapiso** | La **faja perimetral de XPS** está colocada y se toca con el XPS del muro |
| 2 | **Antes del contrapiso** | El **film de polietileno de 200 μ** está continuo y solapado 20 cm |
| 3 | **Con la mampostería levantada** | Los **premarcos están a plomo, escuadra y en el plano correcto** (alineados con el aislante, no con la mampostería) |
| 4 | **Antes de cerrar la cubierta** | La **barrera de vapor está continua, solapada 15 cm y sellada en cada perforación** |
| 5 | **Antes de cerrar la cubierta** | La **lana NO está comprimida** y los **bafles del alero están colocados** |
| 6 | **Durante el SATE** | **Doble malla a 45° en las esquinas de vano**; **retorno del aislante sobre el marco**; **cabezas de espiga rehundidas y tapadas** |
| 7 | **Durante el SATE** | **XPS (no EPS) por debajo del perfil de arranque**, hasta 50–60 cm bajo NPT |
| 8 | **Encuentro muro-cubierta** | El **EPS del muro y el de la cubierta se tocan**; el parapeto está envuelto por sus tres caras |
| 9 | **Colocación de carpinterías** | **Fondo de junta colocado**, espuma de PU en toda la holgura, silicona neutra con relación 2:1, **drenajes del marco NO tapados** |
| 10 | **Antes de tapar** | **Fotografiar todo**: la faja perimetral, la barrera de vapor, el encuentro muro-cubierta, el retorno del aislante en los vanos. **Es la única prueba de que se hizo, y el archivo del legajo** |

---

# 11. Fuentes y estado de verificación

## 11.1 Qué está verificado y contra qué

| Dato | Estado | Fuente |
|---|---|---|
| **Datos climáticos de Santa Rosa (Aero): TDMN −6,0, TDMX 38,8, GD18 1.394, TMA −11,3 / +42,1, HR 73/61,6 %, serie 1980-2009** | **VERIFICADO** sobre el texto de la norma | **IRAM 11603:2011** (esquema 1, revisión de la ed. 1996), Anexo de datos climáticos |
| **Definición de temperatura de diseño: percentil 1 % / 99 % de las mínimas/máximas diarias de mayo-agosto / diciembre-marzo** | **VERIFICADO** | IRAM 11603:2011, apartado 3.3 |
| **Regla simplificada: TDMN = TMIN − 4,5 ; TDMX = TMAX + 3,5** (origen del valor −2,7 del otro registro) | **VERIFICADO** | Material de cátedra de Instalaciones (UNLP) que reproduce las tablas de IRAM 11605 |
| **Encuadre departamental: La Pampa, Depto. Capital → zona IIIa; límites de zona IV: 1.170–1.950 GD18** | **VERIFICADO** | IRAM 11603:2011, listado departamental y criterio de zonificación |
| **IRAM 11605 Tabla 1 completa (invierno), niveles A / Sustentable / B / C, para TDMN de −15 a 0 °C** | **VERIFICADO** (reproducida idénticamente en dos fuentes independientes) | Material de cátedra UNLP y manual ICPA cap. 6 |
| **IRAM 11605 Tablas 2 y 3 (verano), zonas III y IV: muros 0,50 / 0,88 / 1,25 / 2,00 ; techos 0,19 / 0,34 / 0,48 / 0,76** | **VERIFICADO** | Ídem |
| **Correcciones por α: muros +20 % / −15 % ; techos +30 % / −20 %. Tabla de coeficientes de absorción** | **VERIFICADO** | IRAM 11605, apartados 5.3.2 y 5.3.3 |
| **Criterio de niveles: Δθ superficie-aire de 1 / 2,5 / 4 K; temperaturas interiores 22 / 20 / 18 °C; hipótesis de verano (900 W/m² en techos, 400 en muros, 27 °C interior en zona IV)** | **VERIFICADO** | Material de cátedra UNLP sobre la actualización de IRAM 11605 |
| **Regla de puentes térmicos: K_pt ≤ 1,5 × K_mo, y ≤ 1,35 si están a ≤ 1,7 m** | **VERIFICADO** | IRAM 11605 apartado 5.4, citado en la reglamentación de la Ley 13.059 PBA |
| **IRAM 11604:2001 completa: fórmula de G, Tabla 1 de Gadm, Tabla 2 de pérdidas por el piso (1,38 / 1,08 / 0,93 en zona III-IV), definición de aislación perimetral (R = 0,7, ancho ≥ 50 cm, densidad 25–120 kg/m³) y total, n = 2 por defecto, fórmula de carga térmica anual, corrección de Gadm por superficie vidriada > 20 %** | **VERIFICADO** sobre el texto de la norma | **IRAM 11604:2001** |
| **Resistencias superficiales: muro 0,13/0,04; techo invierno 0,10; techo verano 0,17; piso 0,17** | **VERIFICADO** | IRAM 11601, reproducido en dos fuentes |
| **Espacios áticos: teja 0,23 inv / 0,17 ver ; chapa 0,35 inv / 0,22 ver. Cámara en muro 0,15–0,17** | **VERIFICADO** | Material de cátedra UNLP sobre IRAM 11601 |
| **Tabla de conductividades λ (IRAM 11601)** | **VERIFICADO** | IRAM 11601, reproducida en dos fuentes independientes |
| **Rt del ladrillo cerámico portante 18×19×33 = 0,43 m²K/W; muro con revoques RT = 0,638 → K = 1,57** | **VERIFICADO** | **Cámara Industrial de la Cerámica Roja**, Ficha Técnica N°1, sobre IRAM 11601 Tabla 7 |
| **Forjado cerámico de 16 cm, L = 50: K = 2,79 (verano, incluye resistencias superficiales). Método: Rt = 1/K − Rsi − Rse** | **VERIFICADO** | Ídem, sobre IRAM 11601 Tablas 9 y A.4 |
| **λ del HCCA = 0,12 W/mK (ρ 465), permeabilidad al vapor 11,7×10⁻² g/m·h·kPa. Muro doble HCCA 15+15: K = 0,35, 164 kg/m². Relación de costos HCCA / muro doble tradicional ≈ 123 / 156-163 y tiempos 2h45 / 4h15-4h40 por m²** | **VERIFICADO** (ensayo INTI/CECON sobre muestra comercial, publicado en ASADES 2004) | J. Reyes, *Evaluación térmica y económica de muros de bloques de hormigón celular…*, ASADES vol. 8, 2004 |
| **Cubierta de chapa con celulosa proyectada de 150 mm: K = 0,17, 85 kg/m², verifica Nivel A** | **VERIFICADO** | Ídem |
| **K de hormigón sin aislar: 10 cm → 4,32; 15 cm → 3,82; 20 cm → 3,42. Muro de hueco 18 revocado → 1,77. Hormigón 15 + SATE EPS 50 → 0,58** | **VERIFICADO** | **Manual ICPA**, capítulo 6 (Aislación térmica y acústica) |
| **IRAM 11507-4: categorías K1 a K5, exigencia K < 4,0, Tabla A.1 de ventanas completas, Tabla A.2 de vidrios, K del perfil de aluminio 6,02 sin RPT y 2,85 con RPT** | **VERIFICADO** | IRAM 11507-4, citado en el manual de la Cámara del Vidrio Plano y en el manual INCoSe |
| **Emisividad del low-E 0,15 vs 0,84 del float; mejora del 35 % del DVH con low-E** | **VERIFICADO** | VASA / Pilkington, documentación de producto |
| **Requisitos del Decreto 1030/2010 reglamentario de la Ley 13.059 PBA: Nivel B máximo admisible, IRAM A1 hasta 10 m y A2 por encima, categoría K5 hasta 10 m y K4 por encima, verificación de condensación y planilla de G** | **VERIFICADO** | Decreto 1030/2010, Provincia de Buenos Aires |
| **La Pampa adherida al PRONEV (Res. 5/2023 y 418/2023 de la Secretaría de Energía). Etiquetado calculado por IRAM 11900 mediante el IPE en kWh/m²·año, escala A a G** | **VERIFICADO** | Fuentes oficiales del Programa Nacional de Etiquetado de Viviendas |
| **Reglas de sellado perimetral, premarco y herrajes** | **VERIFICADO** | Manual INCoSe |
| **Ángulos solares para 36,57° S** | **CALCULADO** en este documento con geometría solar estándar | — |
| **Todos los K de las soluciones M1–M12 y T1–T10** | **CALCULADOS** en este documento con IRAM 11601 y los λ/Rt verificados de las tablas 1.11 y 1.12 | — |

## 11.2 Qué NO está verificado — la lista de pendientes

| # | Pendiente | Impacto | Cómo resolverlo |
|---|---|---|---|
| **1** | **Texto vigente del Código de Edificación de Santa Rosa** (Ord. 1581/95 mod. por Ord. 6445/2020). No se pudo acceder (403 en el Concejo Deliberante, PDF no legible en el CPITLP) | **Alto**: puede haber exigencias térmicas municipales | Solicitar el texto al Concejo Deliberante o al CPITLP |
| **2** | **Existencia de una ley provincial de La Pampa de acondicionamiento térmico** (análoga a la 13.059 PBA) o de obligatoriedad del etiquetado | Alto | Digesto de la Provincia de La Pampa; Colegio de Arquitectos de La Pampa |
| **3** | **Rt de bloques de hormigón huecos** (IRAM 11601, Tabla A.3). Se usó ≈ 0,20 estimado | Medio: afecta a M8 | IRAM 11601, Tabla A.3 |
| **4** | **Rt del ladrillo hueco cerámico de 8 cm** | Bajo | IRAM 11601, Tabla A.2 |
| **5** | **λ del XPS** — no figura en IRAM 11601. Se usó 0,033 | Medio: afecta a T3 y a todas las aislaciones enterradas | Ficha técnica con ensayo del producto especificado |
| **6** | **Factores de resistencia a la difusión de vapor μ** de todos los materiales usados en §7.3 | **Medio-alto**: las conclusiones cualitativas son robustas, los números exactos no | IRAM 11601 y fichas técnicas |
| **7** | **Coeficiente de absorción solar α de la teja, la membrana y la chapa efectivamente especificadas** | **Alto**: decide 20–40 mm de aislante en toda la cubierta | Ficha técnica del producto |
| **8** | **Factor solar (g), coeficiente de sombra y transmisión luminosa (TL)** de los vidrios | **Alto**: es lo que decide la estrategia de vidrio por orientación (§5.2) | Planilla del proveedor de vidrio (VASA/Blindex y equivalentes) |
| **9** | **Todos los COSTOS RELATIVOS** de las tablas 2.1, 3.2 y 9.2 | **Alto para la decisión económica** | Presupuesto real de corralones y contratistas de Santa Rosa |
| **10** | **Tarifa de gas natural y poder calorífico** (9,3 kWh/m³ y rendimiento 90 % son supuestos) | Alto para el análisis de repago | Distribuidora local |
| **11** | **K del perfil de PVC y de madera** | Medio | Ficha técnica del fabricante |
| **12** | **Valores ψ de puentes térmicos lineales** (ISO 14683) y verificación 2D | Medio | Cálculo con THERM / Flixo / HTflux para los detalles concretos |
| **13** | **Espesor máximo de EPS admitido por el sistema SATE, cantidad de fijaciones para la zona de viento de La Pampa, y clasificación de reacción al fuego** | **Alto para la ejecución** | Manual del fabricante del sistema + CIRSOC 102 |
| **14** | **Valores de HR interior de diseño que impone IRAM 11625 por tipo de local** | Medio | IRAM 11625 |
| **15** | **Disponibilidad local en Santa Rosa** de: HCCA, sistemas SATE completos, bovedillas de EPS, XPS, carpintería con RPT, ensayo Blower Door | **Alto para la viabilidad** | Relevamiento de mercado local |
| **16** | **Rosa de vientos de Santa Rosa** (dirección dominante por estación) | Medio para ventilación cruzada y protección de fachadas | SMN |
| **17** | **Edición vigente de IRAM 11603 y 11605** y si el "Nivel Sustentable" está en la edición vigente | Medio | IRAM |

## 11.3 Correcciones a introducir en el resto del repositorio

| Documento | Corrección |
|---|---|
| `docs/05-construccion/tecnologia-constructiva.md` §0.1, Tablas 0.1 y 0.2 | **Los datos son del dataset de Czajkowski con la regla simplificada, no de IRAM 11603.** Reemplazar TDMN −2,7 por **−6,0**, TDMX 33,8 por **38,8** y GD18 1.331 por **1.394**, o dejar ambos con la explicación de §1.1 de este documento |
| Ídem, Tabla 0.3 | El salto térmico de diseño invernal pasa de 20,7 K a **26,0 K**; el estival de 9,8 K a **13,8 K** |
| Ídem, Tabla 4.7 | **Falta la columna del Nivel C y la del Nivel Sustentable.** Completar con la Tabla 1.4 de este documento |
| Ídem, **Tabla 4.9** | Los valores de aplicación (0,34 / 0,92 / 0,29 / 0,75) están calculados con la TDMN equivocada. **Reemplazar por 0,30 / 0,80 / 0,26 / 0,67** |
| Ídem, **Tabla 4.10** | Los K están bien calculados, pero **la columna de verificación de nivel está evaluada contra los admisibles equivocados**. Varias soluciones que figuran como "B" o "casi A" ya no llegan. En particular: **el muro doble con cámara de aire (K = 0,86) deja de verificar el Nivel B** |
| Ídem, Tabla 4.8 | Falta la tabla de **muros** en condición de verano (0,50 / 0,88 / 1,25 / 2,00 para zonas III y IV) |
| Ídem, §4.7.3 | El **fRsi requerido recalculado con TDMN −6,0 y HRi 70 % es 0,785**, no 0,676. **El criterio del estudio pasa a fRsi ≥ 0,80** |
| `docs/04-instalaciones/instalaciones.md` §6.1.2 | **La resolución de la contradicción de zona es correcta y se ratifica.** Agregar que el listado departamental verificado (IRAM 11603:2011) ubica al Depto. Capital en IIIa junto con Atreucó, Catriló, Conhelo, Chapaleufú, Loventué, Maracó, Quemú Quemú, Rancul, Realicó, Toay y Trenel |
| Ídem, §6.2.4 | Agregar la **columna del Nivel Sustentable** (muros 0,88 / techos 0,34 en verano; 0,55 / 0,47 en invierno para TDMN −6) |
| Ambos documentos | **Ninguno trata los PISOS con IRAM 11604 Tabla 2.** Es el vacío más importante: remitir a §1.8 y §4 de este documento |

---

*Documento de proyecto. Todos los K de las soluciones fueron calculados según IRAM 11601 con los λ y Rt de las Tablas 1.11 y 1.12. Los valores marcados `[VERIFICAR]` no fueron confirmados contra la norma o el catálogo correspondiente y no deben usarse en documentación técnica sin verificar. Los costos relativos son estimaciones de orden de magnitud del estudio, no cotizaciones.*
