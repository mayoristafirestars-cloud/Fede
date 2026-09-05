# INGENIERÍA ESTRUCTURAL PARA VIVIENDA UNIFAMILIAR Y EDIFICIOS HASTA PB+9

**Manual técnico de estudio — Obra nueva y reforma**
**Contexto de aplicación: Santa Rosa, La Pampa, República Argentina**

---

## ADVERTENCIA PROFESIONAL PREVIA (leer antes que nada)

Este documento es una **herramienta de anteproyecto, coordinación y control**. Reúne reglamentación argentina, reglas de predimensionado y criterios de obra. **No reemplaza el cálculo estructural**.

Regla de oro que atraviesa todo el documento:

| Etiqueta usada en el texto | Qué significa |
|---|---|
| **[PD]** Predimensionado | Regla práctica para dibujar el anteproyecto y presupuestar. **Siempre** debe verificarse por cálculo. |
| **[RC]** Requisito reglamentario | Prescripción de un reglamento CIRSOC / INPRES-CIRSOC. Es obligatorio si la jurisdicción lo adoptó. |
| **[VER]** A verificar | Dato que **no pude confirmar con la fuente primaria**. No lo uses sin chequear la norma citada. |
| **[FIRMA]** | Exige cálculo, memoria y firma de profesional matriculado (Ingeniero Civil / en Construcciones, según incumbencia del CPIALP). |

Todo proyecto estructural de obra nueva o de intervención sobre estructura existente en La Pampa requiere **memoria de cálculo firmada por matriculado**, visada por el Consejo Profesional correspondiente y aprobada por el municipio. Los valores de este manual son insumo, no conclusión.

**Honestidad sobre incertidumbre:** donde no verifiqué el número de artículo o el valor exacto, escribí **[VER]** en lugar de inventar. Preferí decir "no lo sé" antes que dar un número falso que se convierta en una fisura.

---

## ÍNDICE

1. [Marco normativo argentino](#1-marco-normativo-argentino)
   - 1.1 Mapa de reglamentos CIRSOC / INPRES-CIRSOC
   - 1.2 Jerarquía: CIRSOC vs. código de edificación municipal
   - 1.3 Métodos de diseño: LRFD vs. ASD
   - 1.4 Combinaciones de carga completas
   - 1.5 Factores φ de reducción de resistencia
   - 1.6 Documentación mínima del proyecto estructural
2. [Cargas](#2-cargas)
   - 2.1 Cargas permanentes D: pesos unitarios de materiales
   - 2.2 Armado de paquetes constructivos típicos (kN/m²)
   - 2.3 Sobrecargas de uso L por destino
   - 2.4 Reducción de sobrecargas
   - 2.5 Viento (CIRSOC 102) — Santa Rosa en particular
   - 2.6 Sismo (INPRES-CIRSOC 103) — La Pampa en particular
   - 2.7 Nieve (CIRSOC 104)
   - 2.8 Acciones no reglamentadas que igual hay que considerar
3. [Estudio de suelos](#3-estudio-de-suelos)
   - 3.1 Cuándo, cuántos y hasta qué profundidad
   - 3.2 Ensayos: SPT, CPT, DMT, calicatas, placa de carga
   - 3.3 Correlaciones N-SPT
   - 3.4 Tensiones admisibles orientativas
   - 3.5 Suelos loéssicos colapsables — el problema central del centro argentino
   - 3.6 Napa freática
   - 3.7 Contenido mínimo exigible al informe geotécnico
4. [Fundaciones](#4-fundaciones)
   - 4.1 Árbol de decisión
   - 4.2 Zapatas aisladas, corridas y combinadas
   - 4.3 Vigas de fundación y encadenados
   - 4.4 Plateas
   - 4.5 Pozos romanos
   - 4.6 Pilotes y micropilotes
   - 4.7 Asentamientos: totales y diferenciales admisibles
   - 4.8 **Ejemplo numérico 1**: fundación de edificio PB+9
5. [Estructura de hormigón armado](#5-estructura-de-hormigón-armado)
   - 5.1 Losas: tipologías y predimensionado
   - 5.2 Vigas
   - 5.3 Columnas
   - 5.4 Tabiques
   - 5.5 Armaduras mínimas y máximas
   - 5.6 Recubrimientos por exposición
   - 5.7 Cuantías de acero para presupuestar
   - 5.8 Hormigones H-17 a H-45
   - 5.9 Control de calidad del hormigón
   - 5.10 **Ejemplo numérico 2**: predimensionado de losa y viga
6. [Sistema sismorresistente y estabilidad lateral](#6-sistema-sismorresistente-y-estabilidad-lateral)
7. [Alternativas estructurales](#7-alternativas-estructurales)
8. [Reformas y rehabilitación](#8-reformas-y-rehabilitación)
   - 8.1 Relevamiento y diagnóstico
   - 8.2 Ensayos sobre estructura existente
   - 8.3 Patologías: catálogo de fisuras
   - 8.4 Corrosión y carbonatación
   - 8.5 Técnicas de refuerzo
   - 8.6 Apertura de vanos
   - 8.7 Ampliación en altura
   - 8.8 Demoliciones parciales y apuntalamiento
   - 8.9 **Ejemplo numérico 3**: apertura de vano en muro portante
9. [Interacción con arquitectura](#9-interacción-con-arquitectura)
10. [Software y flujo de cálculo](#10-software-y-flujo-de-cálculo)
11. [Errores frecuentes y checklist](#11-errores-frecuentes-y-checklist-de-verificación)
12. [Bibliografía comentada](#12-bibliografía-comentada)

---
---

# 1. MARCO NORMATIVO ARGENTINO

## 1.1 Mapa de reglamentos CIRSOC / INPRES-CIRSOC

El sistema argentino se organiza por **áreas numéricas**. El CIRSOC (Centro de Investigación de los Reglamentos Nacionales de Seguridad para las Obras Civiles), dependiente del INTI, redacta; la Secretaría de Obras Públicas de la Nación aprueba por resolución.

| Área | Reglamento | Objeto | Edición de referencia |
|---|---|---|---|
| **100 — Acciones** | CIRSOC 101 | Cargas permanentes y sobrecargas mínimas de diseño | 2005 / **101-25** |
| | CIRSOC 102 | Acción del viento | 2005 / **102-25** |
| | INPRES-CIRSOC 103 Parte I | Construcciones sismorresistentes — general | **2018** |
| | INPRES-CIRSOC 103 Parte II | Construcciones sismorresistentes de hormigón armado | 2021 |
| | INPRES-CIRSOC 103 Parte III | Construcciones sismorresistentes de mampostería | 2018 |
| | INPRES-CIRSOC 103 Parte IV | Construcciones sismorresistentes de acero | 2005 |
| | INPRES-CIRSOC 103 Parte V | Construcciones de madera [VER alcance exacto] | 2015 |
| | CIRSOC 104 | Acción de la nieve y del hielo | 2005 |
| | CIRSOC 108 | Cargas de diseño durante la construcción | 2007 |
| **200 — Hormigón** | CIRSOC 200 | Tecnología del hormigón | 2024 |
| | CIRSOC 201 | Estructuras de hormigón | 2005 / **201-25** |
| **300 — Acero** | CIRSOC 301 | Estructuras de acero para edificios | 2018 |
| | CIRSOC 302 | Estabilidad del equilibrio en estructuras de acero | 2005 |
| | CIRSOC 303 | Elementos de acero de sección abierta conformados en frío (*steel framing*) | 2009 |
| | CIRSOC 304 | Soldadura de estructuras de acero | 2007 |
| | CIRSOC 308 | Estructuras livianas de acero para viviendas | 2007 |
| **400 — Geotecnia** | CIRSOC 401 | Estudios geotécnicos | 2015 |
| | CIRSOC 402 | Estructuras de fundación | **en desarrollo** |
| **500 — Mampostería** | CIRSOC 501 | Estructuras de mampostería (cálculo) | 2007 |
| | CIRSOC 501-E | Mampostería de bajo compromiso estructural (empírico) | 2023 |
| **600 — Madera** | CIRSOC 601 | Estructuras de madera | 2016 |
| **700 — Aluminio** | CIRSOC 701 / 704 | Estructuras de aluminio | 2010 |
| **800 — Puentes** | CIRSOC 801 a 804 | Puentes carreteros | 2019-2023 |

### 1.1.1 Cuestión de versiones — leer con atención

Existe una **transición de generación** de reglamentos: las versiones 2005 de CIRSOC 101, 102 y 201 fueron reemplazadas por versiones **-25** (basadas en ASCE 7-2010/2016 y ACI 318 más reciente), junto con el nuevo CIRSOC 200 de tecnología del hormigón.

**[VER] — obligatorio antes de firmar cualquier proyecto:** confirmá con el CIRSOC (cirsoc@inti.gob.ar), con el CPIALP y con la Municipalidad de Santa Rosa **qué edición está adoptada en la jurisdicción y desde qué fecha**. La adopción provincial/municipal suele ir a la zaga de la aprobación nacional, y en una obra privada rige lo que el municipio exige, no lo último publicado.

Diferencia práctica más importante entre generaciones (verificada):

| Concepto | CIRSOC 201-2005 | CIRSOC 101-25 |
|---|---|---|
| Factor de carga de viento en combinación de resistencia | **1,6 W** | **1,0 W** |
| Razón | V del mapa CIRSOC 102-2005 con recurrencia 50 años | V de mapas con recurrencia 700-1700 años según categoría de riesgo |

**Nunca mezcles**: si usás el mapa de vientos de CIRSOC 102-2005 (V=50 m/s para Santa Rosa), tenés que usar 1,6 W. Si usás mapas de nueva generación con velocidades mayores, corresponde 1,0 W. Mezclar las dos cosas produce un error de ~60% en la acción lateral, para cualquiera de los dos lados.

## 1.2 Jerarquía: CIRSOC vs. código de edificación municipal

Es la pregunta que más confusión genera en estudio. La respuesta correcta:

```
        CONSTITUCIÓN / poder de policía edilicio = MUNICIPAL
                              |
        +---------------------+----------------------+
        |                                            |
  CÓDIGO DE EDIFICACIÓN                    REGLAMENTOS CIRSOC
  Y CÓDIGO URBANÍSTICO                     (seguridad estructural)
  (Municipalidad de Santa Rosa)
        |                                            |
  Regula: FOS, FOT, altura máxima,        Regula: cómo se calcula
  retiros, ocupación, medianeras,         la estructura para que
  ventilación, iluminación,               no se caiga.
  accesibilidad, protección               NO regula uso del suelo.
  contra incendio, tramitación,
  QUÉ REGLAMENTO TÉCNICO ADOPTA
```

Reglas operativas:

1. **El municipio decide qué reglamento técnico rige.** El CIRSOC es de uso obligatorio en obra pública nacional; en obra privada es obligatorio **cuando la jurisdicción lo adopta** (por ordenanza o por ley provincial). En la práctica argentina de hoy, prácticamente todos los municipios de cierto tamaño lo adoptaron o lo exigen de hecho vía visado profesional.
2. **Si el código municipal es más exigente, gana el municipal.** Ejemplo típico: sobrecargas de uso mayores en balcones, o exigencia de estudio de suelos por debajo de cierta altura.
3. **Si el código municipal es menos exigente que CIRSOC, no te ampara.** La responsabilidad civil y penal del proyectista se juzga contra el estado del arte, no contra el mínimo administrativo. Un código de edificación viejo que permita algo que CIRSOC prohíbe no te salva en un peritaje.
4. **El CIRSOC no habla de urbanismo.** Altura máxima, FOT, FOS, retiros, tanque, sala de máquinas, medianeras: eso es código municipal + Código Civil y Comercial (arts. de medianería y de restricciones al dominio).
5. **El INPRES-CIRSOC 103 tiene jerarquía propia** en lo sismorresistente y es de aplicación nacional por convenio INPRES-CIRSOC.

**[VER] Santa Rosa (La Pampa):** consultá en la Dirección de Obras Particulares de la Municipalidad de Santa Rosa el texto vigente del Código de Edificación y del Código de Planeamiento (números de ordenanza, alturas máximas por distrito, exigencia de estudio de suelos, exigencia de dirección técnica). No pude verificar esos números y **no los voy a inventar**.

## 1.3 Métodos de diseño: LRFD vs. ASD

| | **LRFD / Diseño por resistencia** | **ASD / Tensiones admisibles** |
|---|---|---|
| Nombre argentino | Método de los estados límites | Método de las tensiones admisibles |
| Idea | Mayoro las cargas, minoro la resistencia | Trabajo con cargas de servicio y limito la tensión a σ_adm = σ_rotura / FS |
| Ecuación | φ·Rn ≥ Σ γi·Qi | σ_actuante ≤ σ_admisible |
| Dónde se usa hoy | **CIRSOC 201 (hormigón), CIRSOC 301 (acero), 303 (conformado en frío)** | **CIRSOC 501-E (mampostería empírica)**, geotecnia (tensión admisible del suelo), verificaciones de servicio |
| Estados límite | Últimos (ELU) + de servicio (ELS) por separado | Un único chequeo, con FS global |

Puntos que se equivocan seguido:

- **La geotecnia sigue trabajando en tensiones admisibles.** El informe de suelos te da σ_adm en kg/cm² para cargas **de servicio** (sin mayorar). Si dimensionás el área de la base con cargas mayoradas, la base te da un 40-50% más grande de lo necesario. Regla: **área de la base con cargas de servicio; armadura de la base con cargas mayoradas.**
- **CIRSOC 101-25 eliminó el capítulo de combinaciones ASD** que existía en la práctica ASCE. Si necesitás combinaciones de servicio (para flechas, fisuración, confort), usá las cargas nominales sin mayorar con los coeficientes de simultaneidad que corresponda [VER en la edición vigente].
- **No se admite mezclar métodos** dentro de un mismo elemento (CIRSOC 101-25, art. C 2.3.1: los factores de carga LRFD "no se deben utilizar con especificaciones de diseño por tensiones admisibles").

## 1.4 Combinaciones de carga completas

### 1.4.1 Simbología (común a toda la normativa)

| Símbolo | Acción |
|---|---|
| **D** | Carga permanente (peso propio + terminaciones + tabiquería fija) |
| **F** | Carga por peso y presión de fluidos con altura y densidad bien definidas |
| **T** | Efectos de coacción: asentamientos diferenciales, fluencia lenta, contracción, temperatura |
| **L** | Sobrecarga de uso (*live load*) |
| **Lr** | Sobrecarga de cubierta (*roof live load*) |
| **S** | Carga de nieve |
| **R** | Carga de lluvia (acumulación) |
| **W** | Acción del viento |
| **E** | Acción sísmica |
| **H** | Empuje lateral del suelo, agua en el suelo o materiales a granel |

### 1.4.2 Combinaciones LRFD — **CIRSOC 201-2005, art. 9.2.1** (verificado, texto reglamentario)

Estas son las que aplican si tu jurisdicción trabaja con la generación 2005 (mapa de vientos CIRSOC 102-2005):

```
(9-1)   U = 1,4 (D + F)
(9-2)   U = 1,2 (D + F + T) + 1,6 (L + H) + 0,5 (Lr ó S ó R)
(9-3)   U = 1,2 D + 1,6 (Lr ó S ó R) + (f1·L ó 0,8 W)
(9-4)   U = 1,2 D + 1,6 W + f1·L + 0,5 (Lr ó S ó R)
(9-5)   U = 1,2 D + 1,0 E + f1 (L + Lr) + f2·S
(9-6)   U = 0,9 D + 1,6 W + 1,6 H
(9-7)   U = 0,9 D + 1,0 E + 1,6 H
```

con:

| Coeficiente | Valor | Cuándo |
|---|---|---|
| **f1** | **1,0** | Lugares de concentración de público con L > 5,00 kN/m², playas de estacionamiento y garajes |
| **f1** | **0,5** | Todas las demás sobrecargas |
| **f2** | **0,7** | Cubiertas que no permiten evacuar la nieve acumulada (p. ej. dientes de sierra) |
| **f2** | **0,2** | Otras configuraciones de cubierta |

Excepciones textuales del art. 9.2.1:
- (a) Si **W no fue reducida por factor de direccionalidad Kd**, se permite usar **1,3 W** en lugar de 1,6 W en (9-4) y (9-6).
- (b) El factor de carga de H puede tomarse **igual a 0** en (9-6) y (9-7) si la acción debida a H contrarresta a W o a E.

### 1.4.3 Combinaciones LRFD — **CIRSOC 101-25, art. 2.3.2** (verificado, texto reglamentario)

Generación nueva, base ASCE 7-10/16:

```
(1)   1,4 D
(2)   1,2 D + 1,6 L + 0,5 (Lr ó S ó R)
(3)   1,2 D + 1,6 (Lr ó S ó R) + (L ó 0,5 W)
(4)   1,2 D + 1,0 W + L + 0,5 (Lr ó S ó R)
(5)   1,2 D + 1,0 E + L + 0,2 S
(6)   0,9 D + 1,0 W
(7)   0,9 D + 1,0 E
```

Excepciones textuales:
1. El factor de carga L en las combinaciones (3), (4) y (5) **puede tomarse 0,5** para todos los destinos en los que Lo de la Tabla 4.1 sea **≤ 5 kN/m²**, salvo garajes y áreas de reunión pública.
2. En (2), (4) y (5) la carga complementaria S se considera **carga de nieve sobre cubierta plana**.

Tratamiento de F y H:
- **F** se incluye con el mismo factor que D en las combinaciones 1 a 5 y 7.
- **H** se incluye con **γ = 1,6** cuando su efecto se suma al efecto de carga variable primario; con **γ = 0,9** cuando se opone y la carga es permanente; con **γ = 0** cuando se opone en todas las demás condiciones.

Prescripciones adicionales del mismo artículo:
- "Se deberán investigar los efectos de una o más cargas que no estén actuando."
- "Los efectos más desfavorables de las cargas debidas al viento y a los sismos se deberán investigar cuando sea apropiado **pero no será necesario considerar que actúan simultáneamente**."
- "Se deberá investigar cada estado límite de resistencia que resulte relevante."

### 1.4.4 Combinación para eventos extraordinarios (CIRSOC 101-25, art. 2.4)

```
(0,9 ó 1,2) D + Ak + 0,5 L + 0,2 S          (2.4.1)
```

donde **Ak** es la acción extraordinaria (impacto vehicular, explosión, pérdida localizada de un elemento portante). Se usa en verificación de **integridad estructural / colapso progresivo**. Para un edificio de 10 plantas con planta baja libre o con columnas expuestas a rampa vehicular, este chequeo **no es opcional** aunque no lo pida el municipio.

### 1.4.5 Cómo se aplican en la práctica (edificio en Santa Rosa)

Para un edificio PB+9 de vivienda en Santa Rosa (zona sísmica 0):

- **E prácticamente no gobierna** (ver §2.6), pero el 103 exige una verificación con **1,5% del peso** si no se cumplen las condiciones de exención.
- **W gobierna la estabilidad lateral.** Con V=50 m/s, el viento es la acción horizontal de diseño.
- Combinaciones que realmente controlan el dimensionado:

| Elemento | Combinación gobernante típica |
|---|---|
| Losas de entrepiso | (9-2) / (2): 1,2D + 1,6L |
| Vigas de entrepiso | (9-2) / (2) |
| Columnas interiores plantas bajas | (9-2) / (2), y (9-1) en carga axial pura |
| Columnas de borde y esquina, plantas altas | (9-4)/(4) y (9-6)/(6) — el viento produce tracción |
| Tabiques / núcleo | (9-4)/(4) para corte y flexión; (9-6)/(6) para tracción en el extremo |
| Fundaciones (dimensión en planta) | **Cargas de servicio, sin mayorar** |
| Fundaciones (armadura) | (9-2) / (2) y combinaciones con W |
| Vuelco global | (9-6)/(6): 0,9D + 1,6W (ó 1,0W) — el 0,9 castiga el peso estabilizante |

## 1.5 Factores φ de reducción de resistencia (CIRSOC 201-2005, art. 9.3.2) — verificado

| Solicitación | φ |
|---|---|
| Secciones **controladas por tracción** (flexión dúctil) | **0,90** |
| Secciones controladas por compresión, con **zunchos en espiral** | **0,70** |
| Secciones controladas por compresión, con **estribos** | **0,65** |
| **Corte y torsión** | **0,75** |
| Aplastamiento en el hormigón (excepto anclaje de postesado y bielas) | 0,65 |
| Zonas de anclaje de postesado | 0,85 |
| Modelos de bielas y tensores (Apéndice A) | 0,75 |

**Transición φ:** para secciones donde la deformación específica neta de tracción del acero más traccionado, a resistencia nominal, está entre el límite de compresión (**0,002** para fy=420 MPa) y **0,005**, φ se interpola linealmente entre el valor de compresión y 0,90.

Consecuencia de diseño que conviene tener presente: **una viga sobrearmada te penaliza doble** — pierde ductilidad y encima le baja el φ. Diseñá siempre en zona controlada por tracción (εt ≥ 0,005).

## 1.6 Documentación mínima del proyecto estructural

Lo que tiene que salir del estudio, con o sin que el municipio lo pida:

1. **Memoria de cálculo** [FIRMA]: acciones adoptadas con referencia normativa, modelo estructural, hipótesis, combinaciones, verificaciones ELU y ELS, listados de software con datos de entrada y salida reproducibles por terceros (CIRSOC 501-E art. 1.4.4 lo exige explícitamente para mampostería; es buena práctica universal).
2. **Plano de fundaciones**: replanteo, cotas de fondo, tensión admisible adoptada y cota del estrato resistente, hormigón de limpieza, detalle de armaduras.
3. **Planos de encofrado por nivel**: ejes, cotas, espesores de losa, secciones de vigas y columnas, niveles.
4. **Planillas de columnas**: sección, armadura longitudinal, estribado por tramo, empalmes, hormigón.
5. **Planos de armadura de losas y vigas**: despiece con longitudes, diámetros, separaciones, recubrimientos.
6. **Planilla de doblado y cómputo de acero**.
7. **Especificaciones técnicas**: clase de hormigón por elemento, clase de exposición, asentamiento, tamaño máximo del agregado, curado, desencofrado, tolerancias.
8. **Plan de control de calidad**: frecuencia de moldeo de probetas, ensayos, criterios de aceptación.
9. **Plan de hormigonado y juntas de construcción**.
10. **Memoria de sobrecargas por sector**, para adjuntar al manual de mantenimiento del edificio. El CIRSOC 101-25 lo recomienda en el comentario C 4.3.1: "Se recomienda confeccionar manuales de mantenimiento de los edificios, en los cuales se incluyan planos con indicación de las sobrecargas consideradas en cada sector". Es la mejor defensa profesional que existe frente a un cambio de destino futuro.

---
---

# 2. CARGAS

## 2.1 Cargas permanentes D: pesos unitarios de materiales

Todos los valores siguientes están **transcriptos de la Tabla 3.1 y Tabla 3.2 del CIRSOC 101** (verificados). Conversión: **1 kN ≅ 100 kgf**; **1 kN/m³ ≅ 100 kgf/m³**.

### 2.1.1 Hormigones — kN/m³

| Material | γ (kN/m³) | ≅ kg/m³ |
|---|---|---|
| Hormigón de cemento pórtland, arena y canto rodado o piedra partida — **sin armar** | **23,5** | 2350 |
| Hormigón de cemento pórtland, arena y canto rodado o piedra partida — **armado** | **25,0** | 2500 |
| Hormigón con agregado basáltico | 25,0 | 2500 |
| Hormigón de cemento, arena y cascote | 18,0 | 1800 |
| Hormigón de cemento, arena y mineral de hierro | 36,0 | 3600 |
| Hormigón con arcilla expandida | 8 a 20 | 800-2000 |
| Hormigón de cal, arena y cascote | 16,0 | 1600 |
| Hormigón con agregado de poliestireno de alta densidad | 5 a 12 | 500-1200 |

> **Nota de obra:** el 25 kN/m³ del hormigón armado es el valor de cálculo. Si tu cuantía de acero es alta (tabiques muy armados, vigas de transferencia), el peso real sube; a los efectos prácticos 25 kN/m³ cubre cuantías normales hasta ~150 kg/m³.

### 2.1.2 Mamposterías — kN/m³ (incluye mortero)

| Mampostería | Con revoque completo (kN/m³) | Sin revoque (kN/m³) |
|---|---|---|
| Ladrillo cerámico macizo común | **17** | 16 |
| Ladrillo hueco cerámico **portante** (< 60% huecos) | **12** | 10 |
| Ladrillo hueco cerámico **no portante** (> 60% huecos) | **10,5** | 8 |
| Bloque hueco de hormigón | **17** | 15 |
| Bloque hueco de hormigón liviano | **15** | 12,5 |
| Ladrillo de yeso | 12 | — |
| Ladrillo refractario | 26 | — |
| Piedra arenisca / granítica | 26 | — |

Mampuestos sueltos (sin mortero), kN/m³:

| Mampuesto | γ |
|---|---|
| Ladrillo cerámico macizo común | 14 |
| Ladrillo hueco cerámico portante (< 60% huecos) | 9 |
| Ladrillo hueco cerámico no portante (> 60% huecos) | 7 |
| Bloque hueco de hormigón | 14 |
| Bloque hueco de hormigón liviano | 11 |
| Bloque de mortero de cemento celular | 6,5 |
| Ladrillo de yeso | 10 |

### 2.1.3 Morteros, enlucidos, contrapisos — kN/m³

| Material | γ |
|---|---|
| Mortero de cemento pórtland y arena | **21** |
| Mortero de cemento pórtland, cal y arena | **19** |
| Mortero de cal y arena | 17 |
| Mortero de cal, arena y polvo de ladrillo | 16 |
| Enlucido de cemento pórtland | 21 |
| Enlucido de cal y cemento pórtland | 19 |
| Enlucido de cal | 17 |
| Enlucido de yeso | 13 |
| **Contrapiso de cemento, arena y cascote** | **18** |
| Contrapiso de cal, arena, polvo de ladrillo y cascote | 16 |
| Contrapiso de piedra o canto rodado con mortero de cal | 17 |

### 2.1.4 Pisos y solados — kN/m² (por su espesor indicado)

| Piso | Espesor | Peso (kN/m²) |
|---|---|---|
| Baldosa cerámica | 12 mm | **0,28** |
| Baldosa de gres cerámico | 20 mm | 0,38 |
| **Porcelanato** | — | **0,20** |
| Mosaico calcáreo | 20 mm | 0,42 |
| Mosaico de granito reconstituido | — | 0,60 |
| Baldosón granítico | 38 mm | 0,90 |
| Baldosa vinílica | 3,2 mm | 0,07 |
| Linóleo / loseta de goma | 6 mm | 0,05 |
| Parquet madera dura | ≤14 mm | 0,15 |
| Parquet madera semidura | ≤14 mm | 0,12 |
| Piso de madera dura | ≤22 mm | 0,25 |
| Piso de madera semidura | ≤22 mm | 0,20 |
| **Piso elevado o flotante (técnico)** | — | **0,40** |
| Chapa rayada / lisa | 6 / 8 / 10 mm | 0,47 / 0,63 / 0,78 |

### 2.1.5 Cielorrasos — kN/m²

| Cielorraso | Peso (kN/m²) |
|---|---|
| Placas superlivianas (EPS, poliuretano) e/estructura, 50 mm | 0,05 |
| Suspendido de placa acústica de fibra mineral e/estructura | 0,05 |
| Listones de acero e/estructura | 0,05 |
| Placas huecas de PVC rígido e/estructura | 0,05 |
| Termoacústico modular de fibra de madera e/estructura | 0,10 |
| Plaquetas de yeso s/armadura de aluminio | 0,20 |
| **Yeso con metal desplegado** | **0,18** |
| **Mezcla de cemento, cal, arena con metal desplegado** | **0,50** |

> El cielorraso aplicado bajo losa (revoque de yeso a la cal, ~1,5 cm) se estima con γ del enlucido: 13 kN/m³ × 0,015 m ≈ **0,20 kN/m²**. Si es cielorraso suspendido de placa de yeso, **0,15-0,25 kN/m²** incluida estructura [PD].

### 2.1.6 Cubiertas — kN/m²

| Cubierta | Peso (kN/m²) |
|---|---|
| Chapa acanalada acero zincado 0,4 / 0,7 / 1,0 mm | 0,04 / 0,07 / 0,10 |
| Chapa acanalada aluminio 0,6 / 0,8 / 1,0 mm | 0,025 / 0,03 / 0,04 |
| Teja cerámica española/colonial/árabe s/entablonado (incluido) | **0,90** |
| Teja cerámica francesa (Marsella) s/entablonado (incluido) | **0,65** |
| Teja cerámica flamenca s/entablonado | 0,70 |
| Teja cerámica normanda s/entablonado | 0,80 |
| Teja de mortero de cemento tipo romano s/enlistonado | 0,50 |
| Teja asfáltica s/enlistonado | 0,20 |
| Teja de pizarra natural s/entablonado | 0,90 |
| Teja de pizarra artificial s/entablonado | 0,45 |
| Membrana / cartón asfáltico 7 capas | 0,10 |
| Doble chapa de aluminio con núcleo de EPS | 0,13 |

> Nota al pie de la Tabla 3.1: para cubiertas montadas **sobre enlistonado solamente** (sin entablonado), restar **0,1 kN/m²** a los valores marcados con (*) en el reglamento: chapa de zinc, tejas cerámicas española, francesa, flamenca, normanda, pizarra artificial.

### 2.1.7 Tabiques livianos — kN/m²

| Tabique | Peso (kN/m²) |
|---|---|
| Placa de yeso **simple** s/bastidor metálico, 95 mm | **0,35** |
| Placa de yeso **doble** s/bastidor metálico, 120 mm | **0,55** |
| Panel premoldeado de yeso cerámico autoportante 70 mm | 0,55 |
| Panel premoldeado de yeso cerámico autoportante 100 mm | 0,65 |

### 2.1.8 Metales, vidrios, suelos y agua — kN/m³

| Material | γ (kN/m³) |
|---|---|
| **Acero** | **78,5** |
| Aluminio | 27 |
| Hierro colado | 71 |
| Hierro forjado | 76 |
| Bronce / latón | 86 |
| Plomo | 114 |
| Zinc | 72 |
| Granito / mármol | 28 |
| Mica | 32 |
| **Arcilla seca / húmeda** (no sumergida) | 9,9 / 17,3 |
| **Arena y grava seca suelta / seca densa / húmeda** | 15,7 / 17,3 / 18,9 |
| Arcilla y grava, seca | 15,7 |
| Limo húmedo poco compacto | 12,3 |
| Tierra negra o vegetal | 11 |
| Suelo **sumergido**: arcilla / arena o grava / fango de río | 12,6 / 9,4 / 14,1 |
| Yeso en polvo / para cielorrasos | 12 / 13 |

Vidrios (kN/m²):

| Vidrio | Peso |
|---|---|
| Plano transparente sencillo 2,0 mm | 0,05 |
| Plano transparente doble 2,7 mm | 0,068 |
| Plano transparente grueso 4,2 mm | 0,105 |
| Vidrio armado 6,0 mm | 0,15 |
| **Por cada mm adicional de espesor de vidrio** | **+0,025** |
| Por cada mm de policarbonato compacto | +0,012 |

Regla mnemotécnica: **vidrio ≈ 25 kg/m² por cada cm de espesor**.

## 2.2 Armado de paquetes constructivos típicos (kN/m²)

Esto es lo que realmente usás. Todos los cálculos siguientes son **sumas de los valores tabulados arriba** [PD para el armado del paquete, [RC] para cada componente].

### 2.2.1 Entrepiso de losa maciza de HºAº — vivienda

| Componente | Cálculo | kN/m² |
|---|---|---|
| Losa maciza h = 12 cm | 25 × 0,12 | 3,00 |
| Contrapiso de cascote e = 8 cm | 18 × 0,08 | 1,44 |
| Carpeta de nivelación e = 2 cm | 21 × 0,02 | 0,42 |
| Piso porcelanato + pegamento | tabla | 0,20 |
| Cielorraso yeso aplicado | tabla | 0,20 |
| **Subtotal D (sin tabiques)** | | **5,26** |
| Tabiquería interior distribuida (ver 2.2.4) | | **1,00** |
| **D total** | | **≈ 6,3** |
| **L (vivienda)** | Tabla 4.1 | **2,00** |
| **D + L de servicio** | | **≈ 8,3 kN/m²** |

### 2.2.2 Entrepiso de losa de viguetas pretensadas + EPS (la más usada en La Pampa)

| Componente | kN/m² |
|---|---|
| Losa de viguetas + bloque EPS + capa de compresión 5 cm, h total 17 cm | **2,20** [VER catálogo del proveedor: varía 1,9-2,6 según altura y tipo de bloque] |
| Contrapiso 8 cm | 1,44 |
| Carpeta 2 cm | 0,42 |
| Piso | 0,20 |
| Cielorraso | 0,20 |
| Tabiquería | 1,00 |
| **D total** | **≈ 5,5** |
| L vivienda | 2,00 |
| **Total servicio** | **≈ 7,5 kN/m²** |

Con bloque **cerámico** en vez de EPS, sumar ~0,7-1,0 kN/m² (peso propio de losa ≈ 2,9-3,2 kN/m²). **[VER] siempre en la ficha técnica del fabricante de viguetas.** La diferencia entre EPS y cerámico en 10 plantas son ~100 tn en la fundación.

### 2.2.3 Azotea accesible con aislación

| Componente | kN/m² |
|---|---|
| Losa maciza 12 cm | 3,00 |
| Barrera de vapor | 0,05 |
| Contrapiso de pendiente e medio 10 cm (hormigón de cascote) | 1,80 |
| Aislación térmica EPS 5 cm | 0,02 |
| Carpeta 2,5 cm | 0,53 |
| Membrana asfáltica | 0,10 |
| Piso baldosón / cerámico + pegamento | 0,30 |
| Cielorraso | 0,20 |
| **D total** | **≈ 6,0** |
| L azotea accesible privadamente | 3,00 |
| **Total servicio** | **≈ 9,0 kN/m²** |

### 2.2.4 Cómo cargar la tabiquería: el error más caro del anteproyecto

Tres criterios, en orden de preferencia:

1. **Tabiques ubicados en planos** (obra nueva con arquitectura definida): cargarlos como **carga lineal** sobre la losa o la viga que los recibe.
   - Muro de ladrillo hueco portante 18 cm revocado, h = 2,60 m: `12 kN/m³ × 0,18 m × 2,60 m = 5,6 kN/m`
   - Muro de ladrillo hueco no portante 12 cm revocado, h = 2,60 m: `10,5 × 0,12 × 2,60 = 3,3 kN/m`
   - Tabique de placa de yeso doble 120 mm, h = 2,60 m: `0,55 × 2,60 = 1,4 kN/m`
   - Muro de ladrillo macizo 30 cm revocado, h = 2,60 m: `17 × 0,30 × 2,60 = 13,3 kN/m`
2. **Carga distribuida equivalente** (anteproyecto o tabiquería reubicable): repartir el peso total de tabiques sobre la superficie de planta.
   - **Vivienda con tabiques de ladrillo hueco: 1,0 a 1,5 kN/m²** [PD]
   - Vivienda con tabiquería seca: 0,3 a 0,6 kN/m² [PD]
   - Oficinas con tabiquería móvil: 0,8 a 1,0 kN/m² [PD]
3. **[RC] CIRSOC 101-25 art. 4.3.2** fija requerimientos específicos para elementos divisorios cuando la planta se proyecta con tabiquería reubicable. **[VER] el valor mínimo exacto en la edición vigente.**

> **Advertencia:** el interiorismo es el enemigo silencioso de la estructura. Un cliente que en obra decide poner un muro de ladrillo macizo de 30 cm donde el proyecto tenía durlock agrega 12 kN/m sobre una losa dimensionada para 1,4. Toda modificación de tabiquería **en obra o en reforma** debe volver al calculista. Esto no es burocracia: es la causa más común de flechas excesivas y fisuras en cielorrasos.

## 2.3 Sobrecargas de uso L por destino

**Transcripción textual de la Tabla 4.1 del CIRSOC 101** (verificada). Valores uniformes en kN/m² y concentrados en kN. Multiplicar por 100 para kgf/m².

### 2.3.1 Usos residenciales y afines

| Destino | Uniforme (kN/m²) | Concentrada (kN) |
|---|---|---|
| **Viviendas uni y bifamiliares — todas las áreas excepto escaleras** (incluye baños, cocinas, lavaderos, comedores, salas de estar y dormitorios) | **2,00** | — |
| Áticos inhabitables **sin** almacenamiento | 0,50 | — |
| Áticos inhabitables **con** almacenamiento | 1,00 | — |
| Áticos habitables y áreas para dormir | 1,50 | — |
| Otros usos residenciales — salas y habitaciones privadas y sus corredores | 2,00 | — |
| Otros usos residenciales — salas y áreas comunes y sus corredores | 5,00 | — |
| Baños en viviendas / otros destinos | 2,00 / 3,00 | — |
| Cocinas en viviendas / otros destinos | 2,00 / 4,00 | — |
| Lavaderos en viviendas / otros destinos | 2,00 / 3,00 | — |
| Dormitorios de uso colectivo / individuales (Tabla C 4.1, orientativa) | 4,00 / 2,00 | — |

### 2.3.2 Balcones, azoteas y cubiertas

| Destino | Uniforme (kN/m²) |
|---|---|
| **Balcones — viviendas en general** | **5,00** |
| Balcones — casas de 1 y 2 familias, **que no excedan 10 m²** | **3,00** |
| Balcones — otros casos | Ver art. 4.11 [VER] |
| **Azoteas y terrazas donde pueden congregarse personas** | **5,00** |
| **Azoteas accesibles privadamente** | **3,00** |
| **Azoteas inaccesibles** | **1,00** |
| Cubiertas planas, inclinadas y curvas usuales | **1,00** |
| Cubiertas para jardines en terrazas y azoteas | 5,00 |
| Cubiertas usadas con fines de montaje u otras ocupaciones | Igual a la ocupación a la que sirven |
| Toldos y marquesinas de tela sobre esqueleto | 0,25 (no reducible) |
| Cerramientos de pantalla para patios, piscinas, pérgolas | 0,25 (no reducible) + 1,0 kN concentrada |
| Todas las superficies de cubierta sujetas a trabajo de mantenimiento | — (1,40 kN concentrada) |
| **Marquesinas y estructuras de entrada a edificios** | 3,50 |

> **El balcón de 5 kN/m² es el ítem que más se subestima en anteproyecto.** Un balcón en voladizo de 1,50 m de vuelo, 1 m de ancho: `D ≈ 5,5 kN/m² × 1,5 = 8,3 kN/m` + `L = 5,0 × 1,5 = 7,5 kN/m` + baranda. Momento en el empotramiento con combinación (2): `M = (1,2×8,3 + 1,6×7,5) × 1,5²/2 = (9,96 + 12,0) × 1,125 = 24,7 kNm/m`. Eso ya no es una losa de 10 cm.

### 2.3.3 Escaleras y circulaciones

| Destino | Uniforme (kN/m²) |
|---|---|
| **Escaleras — viviendas uni y bifamiliares y hoteles en áreas privadas** | **2,00** |
| **Escaleras — todos los demás destinos** | **5,00** |
| Salidas y escaleras de emergencia — en viviendas unifamiliares únicamente | 5,00 |
| Pasillos de circulación — planta baja | 5,00 |
| Pasillos de circulación — otros pisos | Igual al destino con el que comunican |
| Pasarelas y plataformas elevadas (no vías de escape) | 3,00 |
| Patios y lugares de paseo peatonales | 5,00 |

### 2.3.4 Cocheras y garajes

| Destino | Uniforme (kN/m²) | Concentrada |
|---|---|---|
| **Garajes sólo para vehículos de pasajeros** | **2,00** | Ver notas (b) |
| Garajes para camiones y ómnibus | Ver art. 4.10.3 [VER] | Ver art. 4.10 |
| Veredas, entradas vehiculares y patios sujetos a entrada de camiones | 12,00 | 36 kN |

**Nota (b) verificada, muy importante:** los pisos de garajes deben diseñarse para la sobrecarga uniforme **o** para las siguientes cargas concentradas, la que sea más desfavorable:
- Garajes restringidos a vehículos de pasajeros de hasta 9 pasajeros: **14 kN sobre un área de 114 mm × 114 mm**.
- Estructuras de estacionamiento mecánico sin losa, sólo para vehículos de pasajeros: **10 kN por rueda**.

**Nota (a) verificada:** en garajes **no se admite la reducción de sobrecarga** del art. 4.7, salvo excepciones específicas aprobadas por la Autoridad de Aplicación.

> Con L = 2,00 kN/m² la cochera parece más liviana que un dormitorio. **No lo es**: la carga concentrada de 14 kN sobre 11,4 × 11,4 cm gobierna el punzonamiento local de la losa y el corte, y en losas delgadas (h ≤ 12 cm) es determinante. Además f1 = 1,0 en las combinaciones (9-3), (9-4), (9-5), lo que duplica el efecto respecto de una losa de vivienda.

### 2.3.5 Comercio, oficinas y otros

| Destino | Uniforme (kN/m²) | Concentrada (kN) |
|---|---|---|
| **Comercios, venta minorista — planta baja** | **5,00** | 4,5 |
| **Comercios, venta minorista — pisos superiores** | **4,00** | 4,5 |
| Comercios, venta mayorista, todos los pisos | 6,00 | 4,5 |
| **Oficinas** | **2,50** | 9,0 |
| Oficinas — vestíbulos y pasillos de planta baja | 5,00 | 9,0 |
| Oficinas — pasillos en pisos superiores | 4,00 | 9,0 |
| Restaurantes, confiterías y salones comedor | 5,00 | — |
| Escuelas — aulas | 3,00 | 4,5 |
| Escuelas — pasillos PB / pisos superiores | 5,00 / 4,00 | 4,5 |
| Áreas de reunión — asientos fijos / vestíbulos / asientos móviles | 3,00 / 5,00 / 5,00 | — |
| Áreas de reunión — pisos de escenarios | 7,00 | — |
| Gimnasios, áreas principales y balcones | 5,00 | — |
| Templos | 5,00 | — |
| Bibliotecas — salas de lectura / almacenamiento de libros | 3,00 / **7,00** | 4,5 |
| **Archivos** | **7,00** | — |
| Depósitos liviano / pesado | 6,00 / 12,00 | — |
| Fábricas — manufactura liviana / pesada | 6,00 / 12,00 | 9 / 14 |
| **Cuartos de máquinas y calderas** | **7,50** | — |
| Salas de máquinas de ascensores (Tabla C 4.1) | 7,00 | 1,5 (piso enrejado, sobre 2500 mm²) |
| Salas de transformadores (Tabla C 4.1) | 10,00 | — |
| Aire acondicionado, espacio para máquinas (Tabla C 4.1) | 10,00 | — |
| Vestuarios | 2,50 | — |
| Instituciones penitenciarias — celdas / pasillos | 2,00 / 5,00 | — |
| Hospitales — quirófanos y laboratorios / habitaciones / pasillos sup. | 3,00 / 2,00 / 4,00 | 4,5 |
| Cielorrasos con almacenamiento liviano / ocasional | 1,00 / 0,50 | 1,0 (mantenimiento) |
| Helipuertos | 3,00 (no reducible) | Ver notas (e),(f),(g) |
| Sistemas de piso técnico — oficina / computación | 2,50 / 5,00 | 9,0 |

**Nota (*) del reglamento:** para archivos, cocinas de destinos no residenciales, lavaderos, cuartos de máquinas y calderas "se recomienda efectuar el cálculo con cargas y equipos reales. En ningún caso la sobrecarga a utilizar será menor que la fijada en esta Tabla."

### 2.3.6 Barandas, defensas y cargas de impacto

| Elemento | Requisito | Referencia |
|---|---|---|
| Barandas y pasamanos | Ver art. 4.5.1 [VER valor exacto en la edición vigente; el orden de magnitud usual es una carga lineal horizontal de 0,75 kN/m aplicada en el pasamanos, más una concentrada de 1,0 kN en cualquier punto] | CIRSOC 101 art. 4.5.1 |
| Sistemas de barreras para vehículos | Art. 4.5.3 [VER] | CIRSOC 101 |
| Escaleras fijas | Art. 4.5.4 [VER] | CIRSOC 101 |
| Ascensores — impacto | Art. 4.6.2 [VER; en la práctica se mayora la reacción del guiado y del amortiguador según el fabricante] | CIRSOC 101 |
| Maquinaria — impacto | Art. 4.6.3 [VER] | CIRSOC 101 |
| Entrepiso liviano, sobre 650 mm² | 1,0 kN concentrada | Tabla 4.1 |
| Escotillas y claraboyas | 1,0 kN concentrada | Tabla 4.1 |

**[FIRMA]** Las barandas de balcón en edificios en altura han sido objeto de siniestros graves. La verificación del anclaje de la baranda (no sólo de la baranda) es responsabilidad del proyecto estructural, no del herrero.

## 2.4 Reducción de sobrecargas

CIRSOC 101 art. 4.7 permite reducir L en función del **área tributaria influenciada**, con la lógica de que es improbable que toda la superficie tributaria de una columna de planta baja esté cargada al máximo simultáneamente.

**[VER] la expresión exacta y el KLL en la edición vigente.** La formulación tipo ASCE 7 es:

```
L = Lo · ( 0,25 + 4,57 / sqrt(KLL · AT) )      [con AT en m²]
```

con límites: **L ≥ 0,50·Lo** para elementos que soportan **un solo piso**, y **L ≥ 0,40·Lo** para elementos que soportan **dos o más pisos**.

Coeficientes KLL orientativos (verificar en la tabla del reglamento):

| Elemento | KLL |
|---|---|
| Columnas interiores y exteriores sin losas en voladizo | 4 |
| Columnas de borde con losas en voladizo | 3 |
| Columnas de esquina con losas en voladizo | 2 |
| Vigas de borde sin losas en voladizo | 2 |
| Vigas interiores | 2 |
| Todos los demás elementos (losas en una dirección, etc.) | 1 |

**Dónde NO se puede reducir** (verificado en las notas de la Tabla 4.1 y art. 4.7):
- Todos los destinos marcados con nota (a): áreas de reunión, bibliotecas de almacenamiento, comercios mayoristas, garajes, gimnasios, depósitos, fábricas, restaurantes, pasillos de PB, estadios.
- Helipuertos.
- Toldos, marquesinas y cerramientos de pantalla (0,25 kN/m²).
- **Sobrecargas pesadas** (L > 4,80 kN/m²) — art. 4.7.3 [VER umbral exacto].
- **Losas armadas en una sola dirección** — art. 4.7.6 impone limitaciones específicas.

> **Efecto práctico en un PB+9:** una columna interior de un edificio de 10 plantas con AT = 30 m²/planta tiene KLL·AT = 4 × 30 × 10 = 1200 m² acumulados. La reducción llega al piso (0,40·Lo), es decir L de 2,00 baja a 0,80 kN/m². Sobre un total D+L ≈ 8 kN/m², eso es un **15% menos de carga axial**, que se traduce en una columna y una base sensiblemente menores. Es dinero real. Pero **hay que documentarlo en la memoria** porque un revisor lo va a preguntar.

## 2.5 Viento (CIRSOC 102) — Santa Rosa en particular

### 2.5.1 Velocidad básica del viento V

**Verificado — CIRSOC 102-2005, Figura 1B "Velocidades básicas del viento en ciudades":**

| Ciudad | V (m/s) | Ciudad | V (m/s) |
|---|---|---|---|
| **SANTA ROSA (La Pampa)** | **50,0** | Buenos Aires | 45,0 |
| Bahía Blanca | 55,0 | Córdoba | 45,0 |
| Neuquén | 48,0 | Rosario | 50,0 |
| Viedma | 60,0 | Santa Fe | 51,0 |
| Mar del Plata | 51,0 | Paraná | 52,0 |
| Comodoro Rivadavia | **67,5** | Mendoza | 39,0 |
| Rawson | 60,0 | San Juan | 40,0 |
| Río Gallegos | 60,0 | San Luis | 45,0 |
| Ushuaia | 60,0 | Salta | 35,0 |
| Bariloche | 46,0 | San Salvador de Jujuy | 34,0 |
| Corrientes | 46,0 | S. M. de Tucumán | 40,0 |
| La Plata | 46,0 | Santiago del Estero | 43,0 |
| Resistencia / Formosa / Posadas | 45,0 | La Rioja / Catamarca | 44,0 / 43,0 |

**Definición reglamentaria de V (nota de la figura, textual):** "velocidad de ráfaga de 3 segundos en m/s a 10 m sobre el terreno para Categoría de Exposición C y están asociadas con una probabilidad anual de 0,02" (es decir, período de retorno 50 años).

**Santa Rosa con V = 50 m/s = 180 km/h es un valor alto**, comparable a Rosario y superior a Buenos Aires y Córdoba. Estás en el corredor de vientos del centro-sur pampeano. **El viento es la acción horizontal dominante en tu zona.**

### 2.5.2 Procedimiento simplificado vs. analítico

CIRSOC 102 ofrece dos caminos:

| | **Método 1 — Simplificado** | **Método 2 — Analítico** |
|---|---|---|
| Aplicabilidad | Edificios de **baja altura**, regulares, cerrados, simplemente diafragmados, sin juntas de expansión, sin efectos topográficos, h ≤ 18 m [VER condiciones exactas del art. 5.2] | Universal |
| Salida | Tabla de presiones de diseño directas por zona (N/m²) | qz y coeficientes calculados |
| Uso típico | Vivienda unifamiliar, PB+1, galpón chico | **Edificio en altura — obligatorio en PB+9** |

**Para un PB+9 en Santa Rosa: método analítico, sin discusión.** El simplificado no cubre el edificio.

**Nota verificada de las tablas del método simplificado:** los valores tabulados corresponden a **Exposición B** y factor de importancia I = 1,0. Para otras exposiciones se multiplican por: **Exposición C: 1,40** y **Exposición D: 1,66**. Este es un factor gigante y se olvida seguido: pasar de B a C incrementa la presión un 40%.

### 2.5.3 Presión dinámica qz — método analítico

**Expresión (13) del reglamento, verificada:**

```
qz = 0,613 · Kz · Kzt · Kd · V² · I          [N/m²]
```

con V en m/s. Para tenerla en kN/m²: `qz = 0,613 · Kz · Kzt · Kd · V² · I / 1000`.

### 2.5.4 Factor de direccionalidad Kd — Tabla 6 (verificada)

| Tipo de estructura | Kd |
|---|---|
| **Edificios — sistema principal resistente a la fuerza del viento (SPRFV)** | **0,85** |
| **Edificios — componentes y revestimientos (C&R)** | **0,85** |
| Cubiertas abovedadas | 0,85 |
| Chimeneas, tanques: cuadradas / hexagonales / redondas | 0,90 / 0,95 / 0,95 |
| Carteles llenos, carteles abiertos, estructura reticulada | 0,85 |
| Torres reticuladas triangular, cuadrada, rectangular | 0,85 |
| Torres reticuladas, toda otra sección transversal | 0,95 |

**Nota al pie textual, crítica:** "El factor de direccionalidad Kd se ha calibrado con las combinaciones de carga especificadas en el Apéndice B. Este factor **se debe aplicar solo cuando se use conjuntamente con las combinaciones de carga** especificadas en B.3 o en los respectivos reglamentos de aplicación." Esto engancha directo con la excepción (a) del art. 9.2.1 de CIRSOC 201: **si no aplicás Kd, usás 1,3 W en vez de 1,6 W**.

### 2.5.5 Categorías de exposición (art. 5.6, verificado en su descripción)

| Cat. | Descripción reglamentaria | Dónde aparece en Santa Rosa |
|---|---|---|
| **A** | Centro de grandes ciudades con al menos 50% de los edificios de altura > 21 m [VER altura exacta] | Prácticamente inexistente en Santa Rosa |
| **B** | **Áreas urbanas y suburbanas, áreas boscosas, o terrenos con numerosas obstrucciones próximas entre sí, del tamaño de viviendas unifamiliares o mayores** | **Centro y macrocentro consolidado** |
| **C** | **Terrenos abiertos con obstrucciones dispersas, con alturas generalmente menores que 9,1 m** | **Bordes de ciudad, loteos nuevos, chacras, zona industrial, frentes sobre espacios abiertos** |
| **D** | Áreas costeras planas, sin obstrucciones, expuestas al viento sobre grandes cuerpos de agua | No aplica en La Pampa |

**Criterio de decisión honesto:** un edificio de 10 plantas en el centro de Santa Rosa **sobresale** por encima del tejido urbano. La rugosidad B se define por las obstrucciones **en la dirección de barlovento** en una distancia importante. Si tu edificio es 3 veces más alto que lo que lo rodea, la parte superior está efectivamente en exposición C. **Ante la duda, adoptá C.** El costo de la rigidez extra es marginal comparado con el riesgo.

### 2.5.6 Constantes de exposición del terreno — Tabla 4 (verificada)

| Exposición | α | zg (m) | â | b̂ | ᾱ | b̄ | c | ℓ (m) | ε | zmin (m) |
|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 5,0 | 457 | 1/5 | 0,64 | 1/3,0 | 0,30 | 0,45 | 55 | 1/2,0 | 18,3 |
| **B** | 7,0 | 366 | 1/7 | 0,84 | 1/4,0 | 0,45 | 0,30 | 98 | 1/3,0 | 9,2 |
| **C** | 9,5 | 274 | 1/9,5 | 1,00 | 1/6,5 | 0,65 | 0,20 | 152 | 1/5,0 | 4,6 |
| **D** | 11,5 | 213 | 1/11,5 | 1,07 | 1/9,0 | 0,80 | 0,15 | 198 | 1/8,0 | 2,1 |

### 2.5.7 Coeficiente de exposición Kz — Tabla 5 (verificada, transcripción completa)

```
Para 5 m ≤ z ≤ zg :   Kz = 2,01 · (z / zg)^(2/α)
Para z < 5 m       :   Kz = 2,01 · (5 / zg)^(2/α)
```

| z (m) | A Caso 1 | A Caso 2 | B Caso 1 | B Caso 2 | **C** (Casos 1 y 2) | D (Casos 1 y 2) |
|---|---|---|---|---|---|---|
| 0 – 5 | 0,68 | 0,33 | 0,72 | 0,59 | **0,87** | 1,05 |
| 6 | 0,68 | 0,36 | 0,72 | 0,62 | **0,90** | 1,08 |
| 7,50 | 0,68 | 0,39 | 0,72 | 0,66 | **0,94** | 1,12 |
| 10 | 0,68 | 0,44 | 0,72 | 0,72 | **1,00** | 1,18 |
| 12,50 | 0,68 | 0,48 | 0,77 | 0,77 | **1,05** | 1,23 |
| 15 | 0,68 | 0,51 | 0,81 | 0,81 | **1,09** | 1,27 |
| 17,50 | 0,68 | 0,55 | 0,84 | 0,84 | **1,13** | 1,30 |
| 20 | 0,68 | 0,57 | 0,88 | 0,88 | **1,16** | 1,33 |
| 22,50 | 0,68 | 0,60 | 0,91 | 0,91 | **1,19** | 1,36 |
| 25 | 0,68 | 0,63 | 0,93 | 0,93 | **1,21** | 1,38 |
| **30** | 0,68 | 0,68 | 0,98 | 0,98 | **1,26** | 1,43 |
| 35 | 0,72 | 0,72 | 1,03 | 1,03 | **1,30** | 1,47 |
| 40 | 0,76 | 0,76 | 1,07 | 1,07 | 1,34 | 1,50 |
| 45 | 0,80 | 0,80 | 1,10 | 1,10 | 1,37 | 1,53 |
| 50 | 0,83 | 0,83 | 1,14 | 1,14 | 1,40 | 1,56 |
| 60 | 0,89 | 0,89 | 1,20 | 1,20 | 1,46 | 1,61 |
| 75 | 0,98 | 0,98 | 1,28 | 1,28 | 1,53 | 1,68 |
| 90 | 1,05 | 1,05 | 1,35 | 1,35 | 1,59 | 1,73 |
| 120 | 1,18 | 1,18 | 1,46 | 1,46 | 1,69 | 1,82 |
| 150 | 1,29 | 1,29 | 1,56 | 1,56 | 1,77 | 1,89 |

**Casos (nota 1 de la tabla, verificada):**
- **Caso 1:** (a) todos los componentes y revestimientos; (b) SPRFV en edificios de baja altura diseñados con la Figura 4.
- **Caso 2:** (a) todos los SPRFV excepto los de baja altura con Figura 4; (b) todos los SPRFV en otras estructuras.
- Observación: no tomar z menor que 30 m para Caso 1 en exposición A, ni menos de 10 m para Caso 1 en exposición B.
- Se permite interpolación lineal para alturas intermedias.

### 2.5.8 Factor topográfico Kzt

```
Kzt = (1 + K1·K2·K3)²
```

**Kzt = 1,0** cuando el terreno es sensiblemente plano o cuando no se cumplen las condiciones del art. 5.7.1 (lomas, escarpas o colinas aisladas que sobresalen abruptamente del terreno circundante).

**Para Santa Rosa y su entorno inmediato: Kzt = 1,0** en el 95% de los casos — la topografía es de llanura suavemente ondulada. **Excepción a revisar:** obras en los bordes de los valles y bajos (Valle Argentino, bajos salitrosos), donde puede haber escarpas locales. K1, K2 y K3 salen de la Figura 2 del reglamento en función de H/Lh, x/Lh y z/Lh.

### 2.5.9 Factor de importancia I — Tabla 1 (verificada)

| Categoría de la construcción | I (viento) |
|---|---|
| **I** (bajo riesgo para la vida humana: depósitos aislados, agrícolas, temporarias) | **0,87** |
| **II** (todas las no incluidas en I, III y IV — **vivienda y la mayoría de los edificios**) | **1,00** |
| **III** (riesgo sustancial: gran ocupación, escuelas, teatros) | **1,15** |
| **IV** (esenciales: hospitales, bomberos, policía, comunicaciones) | **1,15** |

La clasificación de la construcción sale de la Tabla A-1 del Apéndice A del CIRSOC 102.

### 2.5.10 Coeficientes de presión externa Cp para paredes — verificado

| Superficie | L/B | Cp | Usar con |
|---|---|---|---|
| **Pared a barlovento** | Todos los valores | **+0,80** | **qz** (variable con la altura) |
| **Pared a sotavento** | 0 – 1 | **−0,50** | **qh** (constante, evaluada en h) |
| | 2 | −0,30 | qh |
| | ≥ 4 | −0,20 | qh |
| **Paredes laterales** | Todos los valores | **−0,70** | qh |

(L = dimensión paralela a la dirección del viento; B = dimensión perpendicular.)

Coeficientes de presión para cubiertas a dos aguas, viento normal a la cumbrera, h/L ≤ 0,25 (extracto verificado):

| θ (grados) | 10 | 15 | 20 | 25 | 30 |
|---|---|---|---|---|---|
| **Barlovento** | −0,7 | −0,5 / **0,0** | −0,3 / **+0,2** | −0,2 / **+0,3** | −0,2 / **+0,3** |
| **Sotavento** (θ ≥ 20°) | | | −0,6 [VER valor completo en Fig. 3] | | |

> El doble valor (negativo y positivo) en barlovento significa que **hay que verificar los dos casos**. Una cubierta a 20° puede succionar o presionar según la turbulencia; ambas hipótesis son reales.

### 2.5.11 Coeficientes de presión interna GCpi — Tabla 7 (verificada)

| Clasificación de cerramiento | GCpi |
|---|---|
| Edificios **abiertos** | 0,00 |
| Edificios **parcialmente cerrados** | **±0,55** |
| Edificios **cerrados** | **±0,18** |

**Notas verificadas:** los signos indican presiones actuando hacia y desde las superficies internas. Hay que considerar **dos casos**: (I) GCpi positivo aplicado a todas las superficies internas; (II) GCpi negativo aplicado a todas las superficies internas.

> **Lección de obra para vivienda en La Pampa:** una vivienda con un portón de garaje grande o un ventanal sin protección que rompe en la tormenta **pasa de "cerrado" a "parcialmente cerrado"** y el GCpi salta de 0,18 a 0,55. La presión interna se **triplica** y vuela el techo desde adentro. Por eso los techos livianos de chapa se pierden en tormenta: no falla la chapa, falla el anclaje porque nadie consideró el cambio de clasificación de cerramiento. Si el proyecto tiene aberturas grandes en una sola fachada, **calculalo como parcialmente cerrado o exigí vidrios resistentes al impacto**.

### 2.5.12 Presión de diseño

```
Para SPRFV, edificios rígidos:     p = q·G·Cp − qi·(GCpi)
```
donde:
- `q = qz` para la pared a barlovento (variable con z),
- `q = qh` para paredes a sotavento, laterales y cubierta (evaluada en h),
- `qi = qh` para edificios cerrados,
- **G = 0,85** para edificios rígidos [VER art. 5.8.1: el reglamento permite G=0,85 para estructuras rígidas, definidas como aquellas con frecuencia natural n1 ≥ 1 Hz. **En un PB+9 hay que verificar la frecuencia**: si T > 1 s, el edificio es flexible y se debe calcular Gf con el procedimiento del art. 5.8.2].

**Verificación de frecuencia [PD]:** para pórticos de hormigón `T ≈ 0,0466·h^0,9` (fórmula tipo ASCE/103). Para h = 30 m: `T ≈ 0,0466 × 30^0,9 = 0,0466 × 21,2 = 0,99 s → n1 ≈ 1,0 Hz`. **Estás justo en el límite.** Un PB+9 con pórticos flexibles es "flexible" a los efectos del viento y requiere el factor Gf. Con núcleo de tabiques rígidos, T baja a ~0,6 s y podés usar G = 0,85.

### 2.5.13 **Ejemplo numérico intermedio: presión de viento en PB+9 en Santa Rosa**

Datos:
- Edificio: PB+9, altura total **h = 30 m** (PB 3,50 m + 9 × 2,95 m ≈ 30 m)
- Planta rectangular: **B = 20 m** (frente) × **L = 15 m** (profundidad)
- Vivienda multifamiliar → Categoría II → **I = 1,00**
- Ubicación urbana pero sobresaliendo → adoptamos **Exposición C** (criterio conservador)
- Terreno plano → **Kzt = 1,00**
- Edificio cerrado → **GCpi = ±0,18**
- **V = 50 m/s** (Santa Rosa)
- **Kd = 0,85**
- G = 0,85 (asumiendo sistema con núcleo rígido; verificar T)

**Paso 1 — presión dinámica base:**
```
0,613 × Kd × V² × I = 0,613 × 0,85 × 50² × 1,00 = 0,613 × 0,85 × 2500 = 1302,6 N/m²
```
Entonces `qz = 1302,6 × Kz × Kzt` [N/m²], con Kzt = 1.

**Paso 2 — tabla de qz por altura (Exposición C, Caso 2):**

| z (m) | Kz | qz (N/m²) | qz (kN/m²) |
|---|---|---|---|
| 0 – 5 | 0,87 | 1133 | 1,13 |
| 10 | 1,00 | 1303 | 1,30 |
| 15 | 1,09 | 1420 | 1,42 |
| 20 | 1,16 | 1511 | 1,51 |
| 25 | 1,21 | 1576 | 1,58 |
| **30 = h** | **1,26** | **1641** | **1,64** |

Entonces **qh = 1,64 kN/m²**.

**Paso 3 — presiones de diseño (viento normal al frente de 20 m; L/B = 15/20 = 0,75 → Cp sotavento = −0,50):**

Barlovento, a z = 30 m:
```
p = qz·G·Cp − qh·(GCpi) = 1,64 × 0,85 × 0,80 − 1,64 × (−0,18)
p = 1,115 + 0,295 = 1,41 kN/m²   (caso GCpi negativo, succión interna → suma)
```
Sotavento:
```
p = qh·G·Cp − qh·(GCpi) = 1,64 × 0,85 × (−0,50) − 1,64 × (+0,18)
p = −0,697 − 0,295 = −0,99 kN/m²
```

**Paso 4 — presión neta sobre el SPRFV (barlovento + sotavento):**

La presión interna se cancela al sumar caras opuestas para el análisis global. Presión neta a nivel z:
```
p_neta(z) = G · [ qz·(+0,80) + qh·(+0,50) ]
```

| z (m) | qz (kN/m²) | p_barlovento (kN/m²) | p_sotavento (kN/m²) | **p_neta (kN/m²)** |
|---|---|---|---|---|
| 5 | 1,13 | 0,77 | 0,70 | **1,47** |
| 10 | 1,30 | 0,88 | 0,70 | **1,58** |
| 15 | 1,42 | 0,97 | 0,70 | **1,67** |
| 20 | 1,51 | 1,03 | 0,70 | **1,73** |
| 25 | 1,58 | 1,07 | 0,70 | **1,77** |
| 30 | 1,64 | 1,12 | 0,70 | **1,82** |

**Paso 5 — corte basal por viento (fachada de 20 m de ancho):**

Integrando aproximadamente (promedio ponderado ≈ 1,70 kN/m²):
```
V_base ≈ 1,70 kN/m² × 20 m × 30 m ≈ 1020 kN ≈ 104 tn
```

**Paso 6 — momento de vuelco:**
```
M_vuelco ≈ 1020 kN × 0,55 × 30 m ≈ 16.800 kNm ≈ 1710 tn·m
```
(el factor 0,55 aproxima el centroide de la distribución trapecial creciente)

**Paso 7 — comparación con el peso del edificio (control de sensatez):**
```
Peso ≈ (20 × 15 m²) × 10 plantas × 9 kN/m² ≈ 27.000 kN ≈ 2750 tn
V_base / W = 1020 / 27.000 = 3,8 %
```

**Este número es la clave de todo el análisis sísmico en Santa Rosa** (ver §2.6.4): la resultante del viento supera holgadamente el 1,5% del peso que exige el INPRES-CIRSOC 103 como umbral de exención en zona 0.

**Paso 8 — mayoración:**
```
Con CIRSOC 201-2005 (comb. 9-4):  1,6 × 1020 = 1632 kN mayorados
Con CIRSOC 101-25   (comb. 4)  :  1,0 × W', con W' del mapa nuevo (mayor V)
```
**No mezclar.** [VER cuál rige en tu jurisdicción.]

## 2.6 Sismo (INPRES-CIRSOC 103) — La Pampa en particular

### 2.6.1 Zonificación sísmica argentina — Tabla 2.1 (verificada)

| Zona sísmica | Peligrosidad |
|---|---|
| **0** | **Muy reducida** |
| 1 | Reducida |
| 2 | Moderada |
| 3 | Elevada |
| 4 | Muy elevada |

El "sismo de diseño" del reglamento representa el movimiento más destructivo que puede ocurrir en una zona, con **intervalo de recurrencia de 500 años**.

### 2.6.2 **La Pampa — Anexo A del INPRES-CIRSOC 103 Parte I (verificado, transcripción textual)**

**ZONA 0 (peligrosidad muy reducida) — Departamentos de La Pampa:**

| Nº | Departamento | | Nº | Departamento |
|---|---|---|---|---|
| 2 | Realicó | | **12** | **Capital (SANTA ROSA)** |
| 3 | Chapaleufú | | 13 | Catriló |
| 4 | Trenel | | 15 | Limay Mahuida |
| 5 | Maracó (Gral. Pico) | | 16 | Utracán |
| 6 | Conhelo | | 17 | Atreucó |
| 7 | Quemú-Quemú | | 18 | Guatraché |
| 9 | parte de Chalileo | | 19 | Curacó |
| 10 | Loventué | | 20 | Lihué Calel |
| 11 | Toay | | 21 | Hucal |
| | | | 22 | Caleu-Caleu |

**ZONA 1 (peligrosidad reducida) — Departamentos de La Pampa:**

| Nº | Departamento |
|---|---|
| 1 | Rancul |
| 8 | Chical Có |
| 9 | parte de Chalileo |
| 14 | Puelén |

**Conclusión operativa: SANTA ROSA (Departamento Capital) y TOAY están en ZONA SÍSMICA 0.** El oeste de la provincia (Puelén, Chical Có, Rancul, parte de Chalileo) está en Zona 1.

> **Nota:** el reglamento aclara que en www.inpres.gob.ar, ingresando latitud y longitud, se obtiene la zona sísmica correspondiente. Usalo para verificar obras cerca de límites departamentales.

### 2.6.3 Clasificación del sitio — Tabla 2.2 (verificada, transcripción)

| Tipo espectral | Sitio | Descripción del perfil de suelos | Vsm (m/s) | Nm (SPT) | Sum (kPa) |
|---|---|---|---|---|---|
| **Tipo 1** | **SA** | Roca dura con presencia superficial y escasa meteorización | > 1500 | — | — |
| | **SB** | Roca dura con pequeña capa de suelo denso y/o roca meteorizada < 3 m | 760 – 1500 | — | — |
| | **SC** | Roca blanda o meteorizada que no cumple SA/SB. Gravas y/o arenas **muy densas**. Suelo cohesivo preconsolidado muy duro. Gravas y/o arenas de densidad media | 360 – 760 | > 50 | > 100 |
| **Tipo 2** | **SD** | Suelo cohesivo consistente de baja plasticidad. Gravas y/o arenas de **baja densidad** | 180 – 360 | 15 – 50 | 50 – 100 |
| **Tipo 3** | **SE** | Suelo cohesivo **blando** de baja plasticidad | < 180 | < 15 | < 50 |
| — | **SF** | Suelos dinámicamente inestables. **Requieren estudios especiales** | — | — | — |

**Suelos SF que exigen evaluación específica del sitio (art. 2.3.2, verificado):**
- a) Suelos vulnerables o propensos a falla, pérdida de capacidad portante o colapso bajo acciones sísmicas.
- b) Suelos potencialmente licuables (Anexo B).
- **c) Arcillas altamente sensitivas, suelos colapsables débilmente cementados.** ← **ESTO ES LOESS. Relevante en La Pampa.**
- d) Turbas o arcillas altamente orgánicas de más de 3 m de espesor.
- e) Arcillas de muy alta plasticidad, espesor > 8 m e IP > 75.
- f) Arcillas de media o baja rigidez de espesores > 15 m.
- g) Suelos expuestos a inestabilidad de taludes, laderas o terraplenes.

La clasificación se basa en la **velocidad media de la onda de corte Vsm en los primeros 30 m**. Se acepta correlación con SPT o con resistencia al corte no drenada.

### 2.6.4 **[RC] Construcciones en Zona 0 — art. 2.5.2 (verificado, transcripción textual)**

Esto es lo más importante de toda la sección para vos:

> **a)** Para las construcciones del **grupo Ao** será de aplicación todo lo establecido en el presente Reglamento.
>
> **b)** Las construcciones de **hasta 3 pisos o 12 m de altura están eximidas** de la aplicación del presente Reglamento.
>
> **c)** Las construcciones de **altura total superior a los 12 m**, diseñadas para los efectos del viento, **están eximidas** de la aplicación del presente Reglamento **si se cumplen simultáneamente** las siguientes condiciones:
> - **c1)** Han sido verificadas bajo los efectos del viento en las **dos direcciones principales**.
> - **c2)** La **resultante en cada dirección de las fuerzas del viento es igual o mayor que el 1,5% del peso total** de la construcción.
> - **c3)** El punto de aplicación de la fuerza resultante de la acción del viento se encuentra aproximadamente coincidente o **por encima del centro de gravedad** de la construcción.
>
> Cuando **no** se cumplan los requisitos c1, c2 y c3, se deberá **verificar la estructura bajo la acción de fuerzas horizontales aplicadas en los centros de gravedad de intensidad igual al 1,5% de los pesos respectivos** y cumplir los requisitos sobre **arriostramiento de fundaciones** establecidos en el Capítulo 9.

**Lectura práctica para Santa Rosa:**

| Caso | Qué hacer |
|---|---|
| Vivienda unifamiliar PB, PB+1, PB+2 (≤ 12 m) | **Eximida del 103**. No hay que hacer análisis sísmico. |
| PB+9 (30 m) de vivienda, grupo B | Verificar viento en X e Y. Si **V_viento ≥ 1,5% W** en ambas direcciones **y** el punto de aplicación está por encima del CG → **eximido del 103**. |
| PB+9 que no cumple c1/c2/c3 | Verificar con **fuerzas horizontales = 1,5% de los pesos por nivel**, aplicadas en los CG, **más** los requisitos de arriostramiento de fundaciones del Cap. 9. |
| Hospital, cuartel de bomberos, central de comunicaciones (**grupo Ao**) | **Aplicación íntegra del reglamento**, sin importar la altura. |

En el ejemplo de §2.5.13 obtuvimos **V_viento/W = 3,8%**, muy por encima del 1,5%. Y la resultante del viento en un edificio esbelto se aplica por encima de la mitad de la altura, mientras el CG está aproximadamente a la mitad (masas uniformes) → c3 se cumple. **Conclusión: un PB+9 típico de vivienda en Santa Rosa, correctamente verificado a viento en ambas direcciones, queda eximido del análisis sísmico.**

**Pero — y esto es importante — la exención es del *análisis de fuerzas sísmicas*, no del buen criterio sismorresistente.** Seguí aplicando:
- Redundancia estructural (nunca un único sistema resistente por dirección).
- Continuidad vertical de columnas y tabiques.
- Nudos bien armados.
- Arriostramiento de fundaciones (vigas de encadenado en ambas direcciones).
- Evitar planta baja débil (columnas libres bajo tabiques que arrancan en el 1er piso).

Cuesta muy poco y convierte un edificio frágil en uno robusto ante cualquier acción imprevista (asentamiento diferencial, impacto, sismo lejano).

### 2.6.5 Clasificación de construcciones por destino — factor de riesgo γr (verificado)

| Grupo | γr | Destino |
|---|---|---|
| **Ao** | **1,5** | Funciones esenciales o cuyo colapso produce efectos catastróficos: hospitales, policía, bomberos, centrales de comunicación, centrales de energía de emergencia, agua potable, depósitos de gases/líquidos inflamables o tóxicos, áreas esenciales de aeropuertos |
| **A** | **1,3** | Gran repercusión por ocupación o uso: uso público **> 300 m² y > 100 personas**, servicios médicos, radio y TV, centrales telefónicas, correos, edificios gubernamentales, escuelas, universidades, cines, teatros, estadios, templos, terminales, grandes comercios e industrias, museos, bibliotecas, plantas de bombeo. Depósitos de combustibles hasta 100 m³ |
| **B** | **1,0** | **Vivienda unifamiliar o multifamiliar; hoteles, comercios e industrias no incluidos en A** |
| **C** | **0,8** | Construcciones aisladas con ocupación < 10 personas: depósitos y casillas aislados, establos, silos y tanques apoyados en el suelo |

### 2.6.6 Coeficiente sísmico normalizado Cn — Tabla 4.1 (verificado)

Para la **verificación simplificada** (art. 4.2), aplicable a sitios clase A, B, C y D:

```
C = Cn · γr           [4.1]
Vo = C · W            [4.2]
```

| Zona sísmica | Cn |
|---|---|
| **1** | **0,23** |
| **2** | **0,38** |
| **3** | **0,44** |
| **4** | **0,50** |

**Nota:** la tabla **no incluye zona 0** — coherente con la exención del art. 2.5.2.

**Ejemplo comparativo:** ese mismo PB+9 en Mendoza (Zona 4) tendría `C = 0,50 × 1,0 = 0,50` → `Vo = 0,50 × 27.000 kN = 13.500 kN` = **13 veces el corte por viento** que calculamos para Santa Rosa. La diferencia de costo estructural entre construir en Santa Rosa y en Mendoza es enorme. **Aprovechá tu ventaja competitiva, pero no la conviertas en descuido.**

### 2.6.7 Factores de comportamiento R, Cd, Ωo — Tabla 5.1 (verificada, extracto)

| Nº | Tipo estructural | R | Cd | Ωo |
|---|---|---|---|---|
| **Estructuras de hormigón armado** | | | | |
| 1 | Tabiques aislados y acoplados | R = f(z), 5 ≤ R ≤ 7 | | 2,5 |
| 2 | **Pórticos con ductilidad completa** | **7** | 5,5 | 3 |
| 3 | **Sistema dual Pórtico-Tabique** | **6** | 5 | 2,5 |
| 4 | Estructuras con diagonales concéntricas | 4 | 4 | 2,5 |
| 5 | Estructuras rigidizadas con diagonales excéntricas | 6 | 4 | 2,5 |
| 6 | **Columnas en voladizo** | **2,5** | 2,5 | 1,5 |
| 7 | Estructura con **ductilidad limitada** | 3,5 | 3,5 | 2,5 |
| **Mampostería — ladrillos cerámicos macizos** | | | | |
| 8 | Encadenada simple | 3 | 2,3 | 2,5 |
| 9 | Encadenada armada | 3,5 | 2,5 | 2,5 |
| 10 | Reforzada con armadura distribuida | 4 | 3 | 2,5 |
| 11 | **Sin encadenados** | **1,5** | 2 | 2 |
| **Mampostería — bloques huecos portantes cerámicos** | | | | |
| 12 / 13 / 14 | Encadenada simple / armada / reforzada | 2 / 2,5 / 3 | 2,3 / 2,5 / 3 | 2,5 |
| **Mampostería — bloques huecos portantes de hormigón** | | | | |
| 15 / 16 / 17 | Encadenada simple / armada / reforzada | 2,5 / 3 / 3,5 | 2,3 / 2,5 / 3 | 2,5 |
| **Acero** | | | | |
| 18 | Pórticos no arriostrados **especiales** | **7** | 5,5 | 3 |
| 19 | Pórticos no arriostrados intermedios | 4,5 | 4 | 3 |
| 20 | Pórticos no arriostrados convencionales | 3 | 3 | 3 |
| 22 | Pórticos especiales arriostrados **concéntricamente** | 5 | 5,5 | 2 |
| 24 | Pórticos arriostrados **excéntricamente** | **7** | 4 | 2 |
| 25 | Dual: pórtico especial + arriostrado concéntrico especial | 6 | 5,5 | 2,5 |

Además, **art. 5.1.2 (verificado):** si el propietario o el proyectista optan por diseño con **comportamiento elástico**, se adopta **R = 1,5**.

**Lectura de la tabla:** R es cuánto podés reducir el espectro elástico aprovechando la ductilidad. R = 7 (pórtico dúctil) significa que diseñás para 1/7 de la fuerza elástica, pero **a cambio tenés que garantizar la ductilidad con un detallado severo** (confinamiento de nudos, estribado cerrado con ganchos a 135°, columna fuerte-viga débil, longitudes de rótula plástica). **La mampostería sin encadenados tiene R = 1,5: es un sistema frágil.** Ese solo número explica por qué una casa de ladrillo sin encadenados se rompe en un sismo y una encadenada armada no.

### 2.6.8 Regularidad estructural — Tablas 2.3 y 2.4 (verificadas)

**Regularidad en planta (Tabla 2.3):**

| Línea | Condición |
|---|---|
| **1a** | Torsionalmente regular / irregularidad torsional **baja**: en todos los niveles **δmk / δbk ≤ 1,2** |
| **1b** | Irregularidad torsional **media**: en algún nivel **1,2 < δmk/δbk ≤ 1,4** |
| **1c** | Irregularidad torsional **extrema**: en algún nivel **δmk/δbk > 1,4** → exige rediseño (art. 2.6.3-a) |
| 2a | Regular: los elementos resistentes son **continuos en altura** y el esfuerzo se mantiene en un único plano vertical |
| 2b | Irregular: todos los casos no incluidos en 2a |
| 3a | Regular: sistemas formados por elementos **perpendiculares o con doble simetría** |
| 3b | Irregular: los demás |
| **4a** | Regular en **esquinas entrantes**: la proyección de la planta se extiende más allá de la esquina entrante una longitud **< 15%** de las dimensiones de la planta en las direcciones de análisis |
| 4b | Irregular: los demás |

(δm = desplazamiento máximo del nivel, δb = desplazamiento medio o del baricentro [VER definición exacta de la simbología en el Cap. 2].)

**Regularidad en altura (Tabla 2.4):**

| Línea | Condición |
|---|---|
| **1a** | Regular / irregularidad **baja** de rigidez: en todos los niveles **Kk ≤ 1,4·Kk+1** |
| **1b** | Irregularidad de rigidez **media**: en algún nivel **1,4·Kk+1 < Kk ≤ 1,7·Kk+1** |
| **1c** | Irregularidad de rigidez **extrema**: en algún nivel **Kk > 1,7·Kk+1** → rediseño |
| **2** | Regularidad de **masas**: las masas de cada nivel varían **menos de 30%** respecto de los niveles adyacentes (se excluyen techos livianos < 1,5 kN/m² y cuerpos salientes) |
| **3** | Regularidad **geométrica**: la dimensión horizontal del sistema resistente varía **menos de 30%** respecto de los niveles adyacentes |
| 4a | Regular: elementos verticales **continuos** en altura, o retranqueos en su plano menores que la longitud del elemento. Dimensiones constantes o **crecientes hacia abajo** |
| 4b | Irregular: los demás |
| **5a** | Regular en **resistencia**: en todos los niveles la resistencia lateral es **> 80%** de la del nivel inmediato superior |
| **5b** | Irregular (**PISO DÉBIL**): los demás |

**Exigencias adicionales a las construcciones irregulares (art. 2.6.3, verificado):**
- a) **Rediseñar la estructura para reducir la irregularidad** en las construcciones y zonas indicadas en 8.3.1.1.
- b) Los componentes que soportan **elementos discontinuos** deben diseñarse para las solicitaciones que resultan de **agotar la capacidad** de los elementos interrumpidos.
- c) Verificar la **transferencia de esfuerzos** entre el elemento interrumpido y el que recibe.
- d) Evaluar la resistencia del piso según 8.3.1.4.

> **El "piso débil" es la irregularidad que mata edificios.** La configuración clásica: planta baja libre para cocheras o local comercial (columnas exentas, doble altura), plantas superiores con tabiques de mampostería en los ejes. La rigidez de PB puede ser 1/5 de la del 1er piso. Cuando llega la acción lateral, toda la demanda de deformación se concentra en PB. **Si tu arquitectura pide PB libre, la solución no es negociar con el calculista: es meter tabiques de hormigón que bajen hasta la fundación, o pórticos de PB mucho más rígidos.**

### 2.6.9 Método de análisis admisible — Tabla 2.5 (verificada)

| Zona sísmica | Altura máxima (m) para método estático | | | Regularidad en planta (Tabla 2.3, línea) | | | Regularidad en altura (Tabla 2.4, línea) | | |
|---|---|---|---|---|---|---|---|---|---|
| | Ao | A | B | Ao | A | B | Ao | A | B |
| **3 y 4** | 12 | 30 | 45 | 1a, 3a, 4a | 1b, 4a | 1b | 1a, 2, 3, 5a | 1b, 2, 3, 5a | 1b, 2, 3, 5a |
| **0*, 1 y 2** | **16** | **45** | **60** | 1b | 1b | 1b | 1a, 2, 3 | 1b, 2, 3 | 1b, 2, 3 |

(*) Construcciones de la zona 0 para las que es exigible la aplicación completa del reglamento (grupo Ao).

Además (art. 2.7.2, verificado): **el método estático se admite para todas las construcciones hasta 3 niveles o de altura menor que 9 m**, sin más condiciones.

**Métodos dinámicos obligatorios** (art. 2.7.3, verificado): cuando no se cumplen las condiciones anteriores, y **también obligatorio cuando el período fundamental T > 3·T2** (T2 correspondiente a la zona sísmica y tipo espectral del sitio).

### 2.6.10 Distorsión horizontal de piso — Tabla 6.4 (verificada)

```
θsk = (dubk − dubk−1) / hsk = Δsk / hsk          [6.18]
du = Cd · de / R                                 [6.17]
```

donde de son los desplazamientos del análisis con espectros elásticos reducidos por R.

| Condición | Grupo Ao o A | Grupo B |
|---|---|---|
| **D** (existen elementos no estructurales que **pueden ser dañados** por las deformaciones) | **0,010** | **0,015** |
| **ND** (elementos no estructurales vinculados de forma que **no sufran daños**) | **0,015** | **0,025** |

- La verificación de la distorsión **no es exigible en estructuras del grupo C**.
- La distorsión se evalúa considerando el **desplazamiento del borde más desfavorable** (no el del centro de masa).
- Para el cálculo de deformaciones se permite usar el período de la construcción **sin considerar el límite** que impone la expresión [6.7].

**Interpretación de obra:** con h = 2,95 m entre pisos y grupo B condición D, la deriva admisible es `0,015 × 2950 = 44 mm` por piso. Eso es mucho. Pero para **viento** el criterio de servicio es más estricto:

| Criterio | Valor típico [PD] | Fundamento |
|---|---|---|
| Deriva de piso bajo viento de servicio | **h / 500 a h / 400** | Confort y no fisuración de tabiques/vidrios |
| Desplazamiento total en la cumbrera bajo viento de servicio | **H / 500** | Práctica internacional |
| Aceleración pico en el último piso, viento 10 años | 15 a 25 milli-g | Confort de ocupantes en vivienda |

Para H = 30 m: `Δ_total ≤ 30.000/500 = 60 mm`. Es un criterio **de servicio**, no reglamentario, pero es el que evita fisuras en tabiques y quejas de clientes. **[VER] si el CIRSOC 102 vigente fija un límite; en la versión 2005 no lo hace explícitamente para viento.**

### 2.6.11 Efecto P-Δ — art. 8.4.4 (verificado)

**Coeficiente de estabilidad:**
```
CE = (Pk · θsk) / (Vk · hsk · Cd)              [8.3]
Pk = Σ Wi   (desde el nivel k hasta el último)  [8.4]
```

- Los efectos P-Δ **deben tomarse en cuenta** cuando en algún nivel **CE ≥ 0,10**.
- Valor máximo admisible:
```
CE_MAX = 0,5 / (β · Cd) ≤ 0,25                 [8.5]
```
donde β es la relación entre el corte de diseño y la capacidad a corte entre el nivel k y k−1. **Conservadoramente se admite β = 1,0.**
- **Si CE > CE_MAX, la estructura es potencialmente inestable y debe ser rediseñada.**
- Para 0,10 < CE ≤ CE_MAX se admite amplificar deformaciones y esfuerzos por:
```
1 / (1 − CE)                                    [8.6]
```

**Con Cd = 5 y β = 1,0: CE_MAX = 0,5/5 = 0,10.** Es decir que para sistemas duales prácticamente cualquier CE ≥ 0,10 exige rediseño con β conservador. Refiná β con la relación real corte de diseño / capacidad.

### 2.6.12 Separaciones y juntas sísmicas — art. 8.4.5 (verificado)

**8.4.5.1 — Separación entre construcciones nuevas y existentes:** "Toda nueva construcción deberá proyectarse y construirse **separada** de las construcciones existentes."

**Excepción** (se permite continuidad si se cumplen simultáneamente):
- a) El conjunto estudiado como una única estructura espacial satisface todos los requerimientos del Reglamento.
- b) La vinculación tiene la capacidad necesaria para soportar las acciones resultantes de la unión.
- c) Los niveles de los diafragmas horizontales difieren **hasta el 30% del canto** del componente vertical más débil en la dirección de la unión.
- d) Los períodos propios de las construcciones adyacentes (supuestas independientes) difieren **hasta el 15%**.

**8.4.5.3 — Dimensionamiento de separaciones y juntas:**

La distancia Yk de la construcción al eje medianero o al eje de la junta sísmica en cada nivel debe cumplir **simultáneamente**:
```
a)  Yk ≥ 1,05 · dubk           [8.7]
b)  Yk ≥ 2,5 cm                [8.8]
c)  Para construcciones existentes: Yke ≥ 2,5 cm     [8.9]
```

**8.4.5.2:** las construcciones irregulares en planta o elevación se proyectarán como cuerpos regulares por medio de separaciones sísmicas, salvo que se compruebe la posibilidad de funcionamiento conjunto. **No es necesario prolongar las juntas por debajo del nivel del suelo (fundaciones)** si su objeto es la separación dinámica.

> **Aplicación en Santa Rosa:** el edificio entre medianeras es la tipología dominante. En zona 0 el martilleo sísmico no es la preocupación, pero **la separación por dilatación térmica y por asentamiento diferencial sí lo es** (ver §6.7).

### 2.6.13 Arriostramiento de fundaciones — Cap. 9 (art. 9.2.4)

Aun en zona 0, cuando la estructura debe verificarse con el 1,5% del peso, **el 103 exige cumplir los requisitos de arriostramiento de fundaciones del Capítulo 9**. Esto significa **vigas de fundación (encadenados) en ambas direcciones** vinculando todas las bases.

**[VER] art. 9.2.4.1 para el dimensionamiento exacto** (el criterio clásico es que el arriostramiento resista una tracción/compresión igual a un porcentaje de la carga axial de la base más cargada — habitualmente del orden del 10%, pero **no lo tomes de acá, verificalo**). El art. 9.2.4.2 fija los casos en que se puede prescindir del arriostramiento, y el 9.2.4.3 habilita losas de fundación o de arriostramiento como alternativa.

## 2.7 Nieve (CIRSOC 104)

### 2.7.1 Expresión básica (verificada)

```
pf = 0,7 · Ce · Ct · I · pg          [kN/m²]           (1)
```
válida para cubiertas con pendiente ≤ 5°.

**Valores mínimos de pf para cubiertas de baja pendiente (art. 3.4, verificado):**
```
pf = I · pg            para pg ≤ 1 kN/m²
pf = I · (1)           para pg > 1 kN/m²
```
aplicables a: cubiertas de una sola pendiente < 15°; cubiertas de dos y cuatro aguas con pendiente ≤ [(21/W) + 0,5] con W en m; cubiertas curvas con ángulo vertical alero-cumbrera < 10°.

Para cubiertas con pendiente: `ps = Cs · pf` (2).

### 2.7.2 La Pampa — Tabla 1.6 (verificada)

| Nº | Localidad | Departamento | HSNM (m) | pg (kN/m²) |
|---|---|---|---|---|
| 8 | Algarrobo del Águila | Chical-Co | 311 | 0,3* |
| 14 | Colonia 25 de Mayo | Puelén | 320 | 0,3* |
| 15 | Limay Mahuida | Limay Mahuida | 262 | 0,3 |
| 19 | Puelches | Curacó | 380 | 0,3 |
| 9 | Santa Isabel | Chalileo | 315 | 0,3 |
| 10 | Victorica | Loventué | 311 | 0,3 |

**Santa Rosa (La Pampa) no figura explícitamente en la Tabla 1.6.** Todas las localidades pampeanas listadas tienen **pg = 0,3 kN/m²**, que es el valor de piso del reglamento.

**Conclusión práctica [PD, con [VER] recomendado]:** adoptar **pg = 0,3 kN/m²** para Santa Rosa. Entonces:
```
pf = 0,7 × 1,0 × 1,0 × 1,0 × 0,3 = 0,21 kN/m²
Mínimo: pf = I · pg = 1,0 × 0,3 = 0,30 kN/m²  →  RIGE 0,30 kN/m²
```

**Comparación con Lr:** la sobrecarga mínima de cubierta de la Tabla 4.1 del CIRSOC 101 es **1,00 kN/m²**. Como **Lr = 1,00 > S = 0,30**, en Santa Rosa **la nieve nunca gobierna el diseño de la cubierta** — gobierna Lr.

**[VER]** el Anexo/mapa del CIRSOC 104 para confirmar el valor de pg de la ciudad de Santa Rosa si el municipio lo exige explícitamente en la memoria.

### 2.7.3 Factores Ce, Ct, I

| Factor | Tabla | Rango típico [PD] |
|---|---|---|
| **Ce** — exposición | Tabla 2 | 0,7 (muy expuesta) a 1,2 (protegida) [VER valores exactos] |
| **Ct** — térmico | Tabla 3 | 1,0 (cubierta cálida) a 1,2-1,3 (cubierta fría, no calefaccionada) [VER] |
| **I** — importancia | Tabla 4 | 0,8 (cat. I) a 1,2 (cat. IV) [VER] |

**Casos donde la nieve SÍ importa aunque pg sea baja:**
- **Acumulación en resaltos** (*drifting*): un parapeto alto, un volumen que sobresale, un techo escalonado. La nieve acumulada localmente puede multiplicar por 3-5 la carga uniforme.
- **Deslizamiento sobre cubiertas inferiores** (*sliding snow*).
- **Cargas desbalanceadas** en cubiertas a dos aguas.
- **Retención de agua por hielo** (*ice damming*) en aleros de cubiertas frías.

Nada de eso es relevante en Santa Rosa con pg = 0,3, pero sí lo es si el estudio toma obras en la cordillera o en la Patagonia.

## 2.8 Acciones no reglamentadas que igual hay que considerar

| Acción | Por qué importa | Tratamiento |
|---|---|---|
| **Retracción del hormigón** | Deformación libre ~0,3 a 0,6 ‰; en una losa de 30 m produce 9-18 mm de acortamiento restringido | Juntas de contracción, armadura mínima de retracción, curado. Ver §5.5 |
| **Fluencia lenta (*creep*)** | Multiplica la flecha de larga duración por ~2 a 3 | Coeficiente λΔ de CIRSOC 201 art. 9.5.2.5 [VER expresión exacta] |
| **Temperatura** | ΔT de 30-40 °C en La Pampa (amplitud térmica continental fuerte). α = 10⁻⁵/°C | Juntas de dilatación cada 25-35 m [PD]. Ver §6.7 |
| **Empuje de suelo H** | Subsuelos, muros de contención, tanques enterrados | Ka, Ko o Kp según posibilidad de desplazamiento. **Nunca Ka en un muro impedido de moverse.** |
| **Subpresión / flotación** | Subsuelo bajo napa: la platea flota | Verificar `W_estructura ≥ 1,2 × U_subpresión` [PD; verificar coeficiente exigido] |
| **Cargas de construcción** | **CIRSOC 108-2007** las reglamenta | Apuntalamiento, acopio de materiales, hormigonado de la planta superior sobre losa joven |
| **Vibraciones de servicio** | Losas de gran luz en oficinas o gimnasios | Frecuencia natural del entrepiso ≥ 8 Hz [PD] para uso residencial/oficinas |
| **Impacto vehicular** | Columnas en cocheras y rampas | Comb. de eventos extraordinarios §1.4.4, o protección física (guardarruedas) |

---
---

# 3. ESTUDIO DE SUELOS

## 3.1 Cuándo, cuántos y hasta qué profundidad

### 3.1.1 Cuándo es obligatorio

El **CIRSOC 401-2015 (Reglamento Argentino de Estudios Geotécnicos)** rige la materia. **[VER]** los umbrales exactos de obligatoriedad y la cantidad mínima de sondeos por superficie, que no pude confirmar en la fuente primaria.

Criterio profesional de mínima [PD] — hacé estudio de suelos **siempre** que:

| Situación | Estudio |
|---|---|
| Vivienda unifamiliar PB o PB+1 en zona con antecedentes conocidos y buenos | Calicata + antecedentes de la zona puede alcanzar |
| Vivienda unifamiliar en terreno de relleno, cerca de bajos, con napa, o sin antecedentes | **SPT obligatorio** |
| **Cualquier edificio de más de 2 plantas** | **SPT obligatorio** |
| **Edificio en altura (PB+3 o más)** | **SPT + ensayos de laboratorio + análisis de colapsabilidad** |
| Ampliación en altura sobre edificio existente | **SPT obligatorio** + verificación de la fundación existente |
| Obra lindera a excavación o a edificio con patologías | SPT + relevamiento del lindero |

**Nunca aceptes proyectar un edificio en altura sin estudio de suelos.** Es el ítem más barato del proyecto (del orden de 0,2-0,5% del costo de obra) y el que evita el 100% de los problemas irreversibles.

### 3.1.2 Cuántos sondeos [PD]

| Superficie de la planta | Sondeos mínimos |
|---|---|
| Vivienda unifamiliar (< 200 m²) | 1 (2 si el terreno es heterogéneo) |
| 200 – 500 m² | 2 a 3 |
| 500 – 1000 m² | 3 a 4 |
| > 1000 m² | 1 cada 300-400 m², mínimo 4 |
| Edificio en altura con núcleo de tabiques | +1 sondeo específico bajo el núcleo (es donde se concentra la carga) |

**Distribución:** en los vértices del área cargada, más uno en el centro. Si aparece dispersión grande entre sondeos, **densificar antes de proyectar**, no después.

### 3.1.3 Profundidad de investigación [PD]

Regla general: investigar hasta la profundidad donde el **incremento de tensión por la obra sea ≤ 10% de la tensión geostática efectiva**, o hasta encontrar un estrato claramente competente de espesor suficiente.

| Tipo de fundación | Profundidad mínima de sondeo |
|---|---|
| Zapatas aisladas de lado B | **2 B a 3 B** por debajo del plano de fundación |
| Zapatas corridas de ancho B | **3 B a 4 B** por debajo del plano de fundación |
| Platea de lado menor B | **1,5 B a 2 B** por debajo de la platea |
| Pilotes de longitud L | **L + 3 D** (D = diámetro), mínimo L + 5 m |
| **Edificio PB+9 sobre platea de 20 × 15 m** | **B = 15 m → 22 a 30 m de sondeo** |

> Esa última fila suele sorprender al cliente. Un edificio de 10 plantas sobre platea "comprime" el suelo hasta más de 20 m de profundidad. Un sondeo de 8 m no dice nada sobre el asentamiento de esa obra. **En La Pampa, además, los estratos loéssicos y loessoides tienen espesores de 10 a 40 m** (ver §3.5), por lo que un sondeo corto puede quedar íntegramente dentro del manto problemático sin llegar a nada.

## 3.2 Ensayos: SPT, CPT, DMT, calicatas, placa de carga

### 3.2.1 SPT — Standard Penetration Test

El ensayo dominante en Argentina. Se hinca un sacamuestras partido (cuchara Terzaghi) con una maza de **63,5 kg cayendo desde 76 cm**; se cuenta el número de golpes para hincar tres tramos de 15 cm y se toma **N = suma de los dos últimos tramos** (últimos 30 cm).

**Correcciones que casi nadie hace y hay que exigir en el informe:**

| Corrección | Símbolo | Qué corrige |
|---|---|---|
| Energía | **N60** | Relación de energía real del martillo al 60% de la teórica. Los martillos manuales tipo "cabo de soga" argentinos entregan del orden del 45-60%. Sin esta corrección las correlaciones internacionales no aplican. |
| Tensión de confinamiento | **(N1)60** | Normaliza a σ'v = 100 kPa. `CN = (100/σ'vo)^0,5` acotado a ≤ 1,7 [PD]. Necesaria para densidad relativa y licuación. |
| Longitud de varillas, diámetro de perforación, tipo de sacamuestras | CR, CB, CS | Factores menores pero acumulativos |

**Ventajas:** barato, universal, entrega muestra alterada para clasificar, hay correlaciones para todo.
**Limitaciones:** muy dependiente del operador; **no sirve para arcillas blandas ni para gravas**; da un valor cada 1 m (baja resolución); **no detecta colapsabilidad**.

### 3.2.2 CPT / CPTu — Ensayo de penetración estática (piezocono)

Se hinca a velocidad constante (2 cm/s) un cono de 60° de 10 cm² midiendo continuamente:
- **qc** — resistencia de punta
- **fs** — fricción lateral del manguito
- **u2** — presión de poros (CPTu)

De ahí: `Rf = fs/qc` (relación de fricción) → clasificación del comportamiento del suelo (cartas de Robertson).

| | SPT | CPT |
|---|---|---|
| Resolución vertical | 1 m | **2 cm — continuo** |
| Repetibilidad | Baja (operador) | **Muy alta** |
| Muestra | Sí (alterada) | No |
| Detecta capas delgadas | No | **Sí** |
| Costo por metro | Bajo | Medio-alto |
| Disponibilidad en La Pampa | Alta | **Baja — hay que traerlo** |

**Correlación práctica SPT-CPT [PD]:** `qc / N60 ≈ 0,4 a 0,5 MPa` en limos y arenas limosas (el cociente crece con el tamaño de grano: 0,2 en arcillas, 0,5-0,6 en arenas limpias, 0,8-1,0 en gravas arenosas).

### 3.2.3 DMT — Dilatómetro de Marchetti

Menos frecuente pero muy potente para estimar módulos y OCR. **Tabla de correlaciones base (verificada del material de cátedra de Leoni, FCEIA-UNR):**

| Símbolo | Descripción | Fórmula |
|---|---|---|
| p0 | Primera lectura corregida | `p0 = 1,05(A − ZM + ΔA) − 0,05(B − ZM − ΔB)` |
| p1 | Segunda lectura corregida | `p1 = B − ZM − ΔB` |
| **ID** | Índice de material | `ID = (p1 − p0)/(p0 − u0)` |
| **KD** | Índice de empuje horizontal | `KD = (p0 − u0)/σ'v0` |
| **ED** | Módulo dilatométrico | `ED = 34,7 (p1 − p0)` |
| K0 | Empuje en reposo | `K0,DMT = (KD/1,5)^0,47 − 0,6` (para ID < 1,2) |
| OCR | Sobreconsolidación | `OCR_DMT = (0,5·KD)^1,56` (para ID < 1,2) |

**Advertencia del propio método:** ED **no es** un módulo de Young. Hay que combinarlo con KD (historia tensional) para obtener MDMT, y recién entonces `E ≈ 0,8 · MDMT`.

### 3.2.4 Calicatas

Excavación a máquina o a mano (1,0 × 1,5 m mínimo para entrar).

**Lo que da la calicata y no da el SPT:**
- **Visión directa de la estratigrafía**, con sus lentes, raíces, rellenos, escombros.
- **Muestras inalteradas en bloque** (imprescindibles para ensayar colapsabilidad en loess).
- Identificación de **rellenos antrópicos**, basureros, pozos ciegos rellenados, antiguos cimientos.
- Estado real del suelo de apoyo de una fundación existente en una reforma.

**Limitaciones:** profundidad práctica **≤ 3-4 m** (por encima requiere entibado y es peligroso), y **no se puede entrar sin entibado por debajo de 1,50 m** — esto es seguridad e higiene, no opción.

**En reforma la calicata es insustituible:** es el único modo de ver qué tiene abajo la casa que vas a intervenir. Calicata contra el cimiento existente, para relevar tipo, ancho, profundidad, material y estado.

### 3.2.5 Ensayo de placa de carga

Plato rígido (habitualmente 30, 45, 60 o 76 cm) cargado escalonadamente midiendo asentamiento. Da el **módulo de reacción de subrasante (balasto) k** y una idea directa de la capacidad.

**Utilidad crítica en loess:** el ensayo de placa **saturando el suelo** es el modo directo de medir el colapso in situ. Dato verificado (Núñez et al., 1970, citado por Rocca-Redolfi-Terzariol): *"En ensayos de plato de carga, al saturarse se observan bruscos descensos con valores de asiento **10 a 20 veces** al que corresponde en condiciones de humedad natural."*

**Limitación:** el plato "siente" hasta ~2 veces su diámetro. Un plato de 60 cm no dice nada sobre un estrato blando a 4 m. **Nunca extrapoles un ensayo de placa a una fundación grande sin corrección por escala.**

### 3.2.6 Ensayos de laboratorio a exigir

| Ensayo | Para qué | Cuándo pedirlo |
|---|---|---|
| Granulometría + límites de Atterberg | Clasificación SUCS | Siempre |
| Humedad natural y densidad seca | Estado del suelo | Siempre |
| **Doble edométrico (compresión confinada a humedad natural y saturada)** | **Potencial de colapso** | **Siempre en suelos loéssicos** |
| Edométrico simple | Cc, Cs, σ'p (preconsolidación) | Suelos cohesivos compresibles |
| Triaxial UU / CU / CD | c y φ | Cálculo de capacidad portante y empujes |
| Corte directo | c y φ (más barato, menos riguroso) | Alternativa económica |
| Compresión simple (qu) | Cohesión no drenada en cohesivos | Suelos finos |
| Sales solubles, sulfatos, cloruros, pH | **Agresividad al hormigón** | **Siempre** — define la clase de exposición (§5.6) |
| Contenido de materia orgánica | Suelos con materia orgánica | Cuando la calicata muestra suelo oscuro |

> **El ensayo de sulfatos se olvida sistemáticamente y es barato.** Un suelo con sulfatos agresivos exige cemento ARS y a/c ≤ 0,45; si te enterás después de hormigonar la fundación, no hay reparación posible.

## 3.3 Correlaciones N-SPT

### 3.3.1 Suelos finos — consistencia (verificada)

| Consistencia | N (SPT) | qu (kg/cm²) | cu = qu/2 (kg/cm²) | cu (kPa) |
|---|---|---|---|---|
| **Muy blando** | < 2 | < 0,25 | < 0,125 | < 12,5 |
| **Blando** | 2 – 4 | 0,25 – 0,50 | 0,125 – 0,25 | 12,5 – 25 |
| **Medianamente compacto** | 4 – 8 | 0,50 – 1,00 | 0,25 – 0,50 | 25 – 50 |
| **Compacto** | 8 – 15 | 1,00 – 2,00 | 0,50 – 1,00 | 50 – 100 |
| **Muy compacto** | 15 – 30 | 2,00 – 4,00 | 1,00 – 2,00 | 100 – 200 |
| **Duro** | > 30 | > 4,00 | > 2,00 | > 200 |

### 3.3.2 Suelos granulares — densidad relativa (verificada)

| Descripción | Muy suelta | Suelta | Med. densa | Densa | Muy densa |
|---|---|---|---|---|---|
| **Dr (%)** | 0 – 15 | 15 – 30 | 30 – 60 | 60 – 80 | 80 – 100 |
| (N1)60 — **arena fina** | 1 – 2 | 3 – 6 | 7 – 15 | 16 – 30 | > 30 |
| (N1)60 — **arena media** | 2 – 3 | 4 – 7 | 8 – 20 | 21 – 40 | > 40 |
| (N1)60 — **arena gruesa** | 3 – 6 | 5 – 9 | 10 – 25 | 26 – 45 | > 45 |

Expresiones alternativas (verificadas):
```
Dr(%) = 100 · (N1)60 / [ 23 + 0,716·(N1)60 ]
Dr(%) = 11,7 + 0,76·[ 222·(N1)60 + 1600 − 53·σ'ov − 50·Cu² ]^0,5     (σ'ov en lb/pulg²)
```

### 3.3.3 Módulo de deformación Es a partir del SPT (verificado)

**Suelos finos** — Es en MPa:

| N60 | Fs = 1,5 | Fs = 2 | Fs = 3 |
|---|---|---|---|
| 5 | 9 | 15 | 23 |
| 10 | 15 | 26 | 39 |
| 20 | 29 | 48 | 73 |
| 30 | 44 | 72 | 109 |
| 40 | 60 | 98 | 147 |
| 50 | 78 | 126 | 187 |

Resumido por consistencia (Fs = 2):

| Consistencia | N60 | Es (MPa) |
|---|---|---|
| Arcillas blandas | 2 – 4 | 8 – 13 |
| Arcillas medianamente compactas | 4 – 8 | 13 – 21 |
| Arcillas compactas | 8 – 15 | 21 – 37 |
| Arcillas muy compactas | 15 – 30 | 37 – 72 |
| Arcillas duras | > 30 | > 72 |

**Suelos granulares** — Es en MPa:

| N60 | Fs = 1,5 | Fs = 2 | Fs = 3 |
|---|---|---|---|
| 5 | 5,92 | 9,87 | 15,13 |
| 10 | 10,40 | 17,32 | 26,44 |
| 20 | 19,74 | 32,67 | 49,51 |
| 30 | 30,05 | 49,46 | 74,37 |
| 40 | 41,38 | 67,74 | 101,12 |
| 50 | 53,71 | 87,45 | 129,58 |

Resumido por densidad (Fs = 2):

| Densidad | (N1)60 | Es (MPa) |
|---|---|---|
| Muy suelta | 2 – 3 | 5 – 7 |
| Suelta | 4 – 6 | 8 – 11 |
| Medianamente densa | 7 – 15 | 12 – 25 |
| Densa | 16 – 30 | 26 – 49 |
| Muy densa | > 30 | > 50 |

Correlaciones clásicas complementarias (D'Apolonia et al., 1970):
```
Arenas normalmente consolidadas:  E (kg/cm²) = 215 + 10,6 · N_SPT
Arenas preconsolidadas:           E (kg/cm²) = 540 + 13,5 · N_SPT
```

### 3.3.4 Módulo de balasto vertical unitario kv1 (verificado)

Correlación en suelos finos (a partir de N60, con Fs = 1,5):
```
kv1 ≈ 192 · (N60)^1,5 / 11        [MN/m³]   (aprox. según la expresión 2.57 citada)
```

| N60 | kv1 (MN/m³) | N60 | kv1 (MN/m³) |
|---|---|---|---|
| 5 | 36 | 40 | 240 |
| 10 | 62 | 45 | 275 |
| 15 | 89 | 50 | 311 |
| 20 | 116 | 55 | 348 |
| 25 | 145 | 60 | 386 |
| 30 | 176 | 65 | 425 |
| 35 | 207 | 70 | 466 |

**Advertencia crítica sobre el balasto:** kv1 es el valor **unitario**, medido sobre un plato cuadrado de 1 pie (30,5 cm) de lado. Para una base real de ancho B hay que corregir. Fórmulas de Terzaghi [PD]:
```
Arenas:            k = kv1 · [ (B + 0,305) / (2B) ]²      (B en m)
Arcillas:          k = kv1 · (0,305 / B)
Base rectangular:  k_B×L = k_cuadrada · (1 + 0,5·B/L) / 1,5
```

Para una platea de 15 m de lado en arcilla: `k = kv1 × 0,305/15 = kv1/49`. **El balasto de una platea es 40-50 veces menor que el de un plato de ensayo.** Modelar una platea con el kv1 del ensayo es uno de los errores más groseros y más comunes en Cypecad/SAFE: te da una platea rígida ficticia con asentamientos irreales y momentos subestimados.

### 3.3.5 Cohesión no drenada a partir del SPT (verificadas)

```
cu = [ (1 + Ip) · N90 / 20 ] · Pa                    (Leoni, 2005)   Ip en decimales
cu = 0,07 · N90 · Pa                                 (Decourt, 1989)  [kN/m²]
cu = 0,145 · (N60)^0,72 · Pa                         (Kulhawy y Mayne, 1990)
cu = f1 · N60 · Pa / 100                             (Mayne, 2010)   válida 15% < Ip < 50%
```
con Pa = presión atmosférica ≈ 101,3 kPa.

**Uso honesto de estas correlaciones:** son para **anteproyecto**. Para el proyecto ejecutivo de un edificio en altura, exigí ensayos triaxiales sobre muestras inalteradas. El costo de dos triaxiales es menor que el de una sola base sobredimensionada.

## 3.4 Tensiones admisibles típicas por tipo de suelo

**[PD]** Valores de orden de magnitud, para anteproyecto y presupuesto. **Nunca los uses para proyecto ejecutivo.** La tensión admisible la fija el informe geotécnico, no una tabla genérica.

| Tipo de suelo | σ_adm orientativa (kg/cm²) | σ_adm (kPa) |
|---|---|---|
| Roca sana masiva | 30 – 100 | 3000 – 10000 |
| Roca fracturada / meteorizada | 5 – 15 | 500 – 1500 |
| Grava densa / grava arenosa densa | 4 – 6 | 400 – 600 |
| Grava medianamente densa | 2 – 4 | 200 – 400 |
| Arena gruesa densa | 3 – 4,5 | 300 – 450 |
| Arena media densa | 2 – 3 | 200 – 300 |
| Arena media medianamente densa | 1,0 – 2,0 | 100 – 200 |
| Arena fina suelta | 0,5 – 1,0 | 50 – 100 |
| Arena fina saturada suelta | **potencialmente licuable — estudio especial** | — |
| Arcilla dura (qu > 4 kg/cm²) | 2 – 4 | 200 – 400 |
| Arcilla muy compacta (qu 2-4) | 1,5 – 2,0 | 150 – 200 |
| Arcilla compacta (qu 1-2) | 1,0 – 1,5 | 100 – 150 |
| Arcilla medianamente compacta (qu 0,5-1) | 0,5 – 1,0 | 50 – 100 |
| Arcilla blanda (qu 0,25-0,5) | 0,25 – 0,5 | 25 – 50 |
| Arcilla muy blanda | **inapto para fundación directa** | — |
| Limo compacto | 1,0 – 2,0 | 100 – 200 |
| **Loess a humedad natural, no colapsable** | **1,0 – 2,0** | **100 – 200** |
| **Loess colapsable, a humedad natural** | **0,8 – 1,5 aparente** | 80 – 150 |
| **Loess colapsable, saturado** | **0,3 – 0,8 (¡o menos!)** | **30 – 80** |
| **Loess autocolapsable** | **NO APTO para fundación directa** | — |
| Relleno antrópico no controlado | **NO APTO** | — |
| Suelo orgánico / turba | **NO APTO** | — |

> **La fila que define tu práctica en La Pampa es la del loess colapsable.** El informe de suelos puede darte σ_adm = 1,2 kg/cm² "a humedad natural" y estar diciendo la verdad. Pero el día que rompe un caño, ese mismo suelo tiene 0,4 kg/cm². **Preguntá siempre al geotécnico: ¿esta tensión es a humedad natural o saturada?** Si la respuesta es "a humedad natural" y no hay análisis de colapsabilidad, el estudio está incompleto.

### 3.4.1 Fórmula general de capacidad portante

Para verificación (no para anteproyecto):

**Terzaghi (base corrida):**
```
qu = c·Nc + q·Nq + 0,5·γ·B·Nγ
```
**Meyerhof / Vesić / Hansen (forma general):**
```
qu = c·Nc·sc·dc·ic + q·Nq·sq·dq·iq + 0,5·γ·B·Nγ·sγ·dγ·iγ
```
con factores de forma (s), profundidad (d) e inclinación de la carga (i).

```
Nq = e^(π·tanφ) · tan²(45 + φ/2)
Nc = (Nq − 1) · cotφ
Nγ = 2·(Nq + 1)·tanφ           (Vesić)
```

Y luego:
```
q_adm = qu_neta / FS + γ·Df
```

**Factor de seguridad FS habitual [PD]:**

| Situación | FS |
|---|---|
| Cargas permanentes + sobrecargas, edificio convencional | **3,0** |
| Con viento o sismo incluidos | 2,0 – 2,5 |
| Suelos bien caracterizados, control estricto | 2,5 |
| Suelos variables o mal caracterizados | 3,5 – 4,0 |

**El asentamiento suele gobernar antes que la rotura.** En arenas y limos, la σ_adm de un edificio queda casi siempre limitada por el asentamiento tolerable, no por la capacidad última.

## 3.5 Suelos loéssicos colapsables — el problema central del centro argentino

Esta es la sección más importante del capítulo para tu ubicación.

### 3.5.1 Qué son y dónde están (verificado — Rocca, Redolfi y Terzariol, 2006)

Datos textuales del trabajo *"Características geotécnicas de los loess de Argentina"* (Rev. Int. de Desastres Naturales, Accidentes e Infraestructura Civil, Vol. 6(2)):

- Los suelos loéssicos de Argentina **cubren más de 600.000 km²**, el principal depósito de su tipo en Sudamérica.
- Se extienden en las planicies entre **23° y 38° S**. Subdivisión propuesta: **loess pampeano** (al sur de 30° S) y **loess chaqueño, subtropical** (al norte de 30° S).
- La faja de **"Mar de Arena"** (arenas eólicas) tiene **2.000 km de longitud y 250-300 km de ancho**, con el cinturón de loess detrás. **La Pampa está en el corazón de esta geografía**: al oeste el mar de arena, al este el loess pampeano típico.
- Origen: partículas de origen volcánico de los Andes Centrales y la Patagonia, transportadas por los vientos del S-SW hacia el centro del país.
- **Espesores**: ~10-15 m en las pampas del este, aumentando hasta **40 m hacia el sur y el oeste**; 20-60 m en valles subtropicales preandinos; 10-20 m en las llanuras chaqueñas occidentales.
- Composición mineralógica del loess pampeano: **plagioclasas 20-60%, cuarzo 20-30%, vidrio volcánico 15-30%**. Arcilla dominante: **illita**.
- La presencia de cenizas volcánicas genera reacciones **puzolánicas** que forman capas cementadas — la **"tosca"**. La cementación es variable en extensión y en características mecánicas.

### 3.5.2 Propiedades índice (verificadas)

**Loess recientes (loess primario, colapsable) — Tabla 2 del trabajo citado:**

| Complejo litológico | ω (%) | ωL (%) | IP (%) | Pasa T200 (%) | γd (kN/m³) |
|---|---|---|---|---|---|
| **CL 2A** (loess primario, el más reciente y colapsable) | 16,08 | 24,25 | 4,58 | 90,64 | **12,9** |
| **CL 2Ax** (con cementación carbonática) | 17,37 | 24,50 | 4,84 | 87,82 | **13,9** |
| **CL 2B** (loess secundario, Pleistoceno Superior) | 22,07 | 26,54 | 6,71 | 84,17 | **14,8** |
| **CL 2C** (Pleistoceno Medio) | 28,66 | 35,02 | 10,86 | 88,55 | **13,4** |

(Promedios sobre 420 perfiles de la ciudad de Córdoba.)

**Rangos generales de los loess recientes (texto verificado):**

| Propiedad | Valor |
|---|---|
| Granulometría | **Arena 5-15%, limo 40-60%, arcilla 20-35%** |
| Límite líquido ωL | **22,0 – 30,0 %** |
| Límite plástico ωP | **16,0 – 20,0 %** |
| Clasificación SUCS | **ML ó CL-ML** |
| **Peso unitario seco γd** | **11,0 – 14,0 kN/m³** ← extremadamente bajo |
| **Humedad natural ω** | **8,0 – 25,0 %** |
| Gravedad específica Gs | **2,65** |
| Porosidad n | ≈ 0,5 |
| Ángulo de fricción interna efectivo (triaxial drenado, saturado) | **φ' ≈ 24°** |
| Distribución de poros | Submicroscópicos 5-25% del volumen de vacíos; 1-20 μm: 30-80%; **macroporosidad milimétrica** tapizada por carbonatos recristalizados |
| Sales solubles Ca y Na | 0,4 – 1,2 % |
| Aniones dominantes | Sulfatos y cloruros ← **¡agresividad al hormigón!** |
| Superficie específica | 1 a > 10 m²/g |

> **γd = 12,9 kN/m³ es un dato demoledor.** Con Gs = 2,65 (γs = 26 kN/m³), el índice de poros es `e = 26/12,9 − 1 = 1,02`. Un suelo con **más de la mitad del volumen vacío**, sostenido por puentes de arcilla floculada y sales precipitadas. Eso es lo que se disuelve cuando llega agua.

**Loess pampeanos antiguos (loessoides preconsolidados por desecación) — Tabla 1, Bolognesi (1975):**

| Zona | Prof. (m) | e0 | ω (%) | ωL (%) | ωP (%) | IP (%) | Cc | Cs+Cr | γs (kN/m³) | γ (kN/m³) |
|---|---|---|---|---|---|---|---|---|---|---|
| Ia | 10,16 | 0,848 | 32,0 | 67,0 | 30,0 | 37,0 | 0,32 | 0,024 | 25,98 | 18,53 |
| Ia | 12,16 | 0,888 | 33,5 | 67,0 | 31,5 | 35,5 | 0,33 | 0,025 | 25,98 | 18,33 |
| Ib | 20,00 | 0,826 | 31,4 | 41,3 | 27,8 | 13,5 | 0,15 | 0,010 | 25,78 | 18,53 |
| Ib | 27,20 | 0,848 | 32,0 | 51,0 | 30,0 | 21,0 | 0,18 | 0,012 | 25,98 | 18,53 |
| Ic | 32,70 | 1,180 | 44,5 | 69,0 | 33,5 | 35,5 | 0,28 | 0,020 | 25,98 | 17,25 |

Los loessoides antiguos, **sobreconsolidados por desecación, no son colapsables** — son el "buen loess". La cuestión es distinguirlos.

### 3.5.3 El mecanismo del colapso

```
ESTRUCTURA METAESTABLE                  COLAPSO
                                        
  o     o     o                          o o o
   \   / \   /       + AGUA →            ooooo
    puentes de                           ooooo
    arcilla + sales                      
  γd = 12,9 kN/m³                      γd = 16-17 kN/m³
  e = 1,0                              e = 0,55
                                        
  ΔH/H = 3 a 10 %  →  en 10 m de manto = 30 a 100 cm de asentamiento
```

Del texto verificado:
- *"Eventualmente, la estructura se debilita y colapsa aún sin alcanzar la saturación. Muy poca carga externa se requiere para alcanzar el colapso final, y a veces **el propio peso de la masa del suelo es suficiente**."*
- *"La resistencia, la rigidez y el grado de colapso están condicionados por la relación de vacíos inicial y el contenido de humedad."*
- *"La resistencia al corte medida varía sustancialmente con el grado de saturación... En general, **la cohesión es el parámetro que mayor variación tiene**, no así el ángulo de fricción interna."*

### 3.5.4 Clasificación reglamentaria del colapso (verificada)

El ensayo de referencia es el **doble edométrico**: dos probetas gemelas, una ensayada a humedad natural y otra saturada. En la curva de compresibilidad saturada aparece la **presión inicial de colapso o presión de fluencia saturada σF.SAT**.

Comparando con la presión de tapada σ0 (peso propio del suelo suprayacente):

| Tipo | Condición | Consecuencia |
|---|---|---|
| **Loess potencialmente colapsable** | **σ0 < σF.SAT** | Colapsa si se lo humedece **y** la presión actuante (tapada + estructura) supera σF.SAT. **Se puede fundar directamente si se controla la carga y el agua.** |
| **Loess AUTOCOLAPSABLE** | **σ0 > σF.SAT** | **Colapsa espontáneamente al humedecerse, sin necesidad de carga exterior.** Genera fricción negativa sobre pilotes. |

**Datos numéricos verificados** (relación σF.SAT/σ0 en la ciudad de Córdoba):

| Tipo | Primeros 3 m | En profundidad |
|---|---|---|
| **Autocolapsables** | 0,72 | 0,60 |
| **Potencialmente colapsables** | 1,49 | 1,40 |

**[FIRMA]** *"Cuando los suelos son autocolapsables **ninguna estructura fundada sobre ellos tiene comportamiento satisfactorio**."* — texto literal del trabajo. Si el informe de suelos identifica un manto autocolapsable, **no hay solución de fundación directa; hay que tratar el suelo o atravesarlo.**

### 3.5.5 Cómo detectarlo — checklist para exigir al geotécnico

1. **Perfil de colapsibilidad**: gráfico en profundidad de σ0 y σF.SAT superpuestos, con y sin el incremento de presión de la obra. Donde σ_actuante > σF.SAT, hay colapso.
2. **Ensayo doble edométrico** sobre muestras **inalteradas** de cada estrato (por eso hacen falta calicatas o muestreo inalterado con tubo Shelby).
3. **Potencial de colapso (PC)** — criterio de Jennings y Knight [PD]:
```
PC (%) = Δe_colapso / (1 + e0) × 100     medido a 200 kPa
```
| PC (%) | Severidad |
|---|---|
| 0 – 1 | No problemático |
| 1 – 5 | Problema moderado |
| 5 – 10 | Problema |
| 10 – 20 | Problema severo |
| > 20 | Problema muy severo |

4. **Indicadores de gabinete rápidos** [PD, para tamizar, no para decidir]:
   - **γd < 14 kN/m³** en un limo → sospechar
   - Índice de poros **e > 0,9** con IP bajo (< 10) → sospechar
   - **Criterio de Denisov**: `K = e_L / e0` (e_L = índice de poros al límite líquido); K < 1 indica colapsabilidad
   - **Criterio de Gibbs y Bara**: si el suelo saturado tiene humedad > ωL, es colapsable
   - Suelo que, seco, se disgrega entre los dedos y en agua se deshace rápido
5. **Antecedentes de la zona**: patologías en construcciones vecinas, historia de la napa, roturas de cañerías conocidas.
6. **Prueba de infiltración / ensayo de placa saturado** para los casos importantes.

### 3.5.6 Soluciones — las tres estrategias (verificadas del trabajo citado)

El texto identifica exactamente **tres caminos**:

#### Estrategia 1 — Eliminar la colapsabilidad (mejorar el suelo)

| Técnica | Descripción | Cuándo sirve |
|---|---|---|
| **Sustitución de suelo** | Excavar 1,0-2,0 m, compactar el fondo, rellenar con suelo seleccionado o suelo-cemento compactado al 95-98% Proctor | **La solución más usada y más confiable en vivienda y edificios medianos.** Barata, verificable, controlable |
| **Compactación dinámica** | Caída de masas pesadas desde altura | Obras grandes, deformables (presas, caminos). *"Efectos menos alentadores en el caso de obras puntuales como edificaciones arquitectónicas"* |
| **Hidrocompactación (compactación hidráulica)** | Inundar el terreno para provocar el colapso antes de construir | **Obras hidráulicas y de gran escala.** Requiere mucho tiempo y agua |
| **Compactación por vibrado / hinca de pilotes / voladuras** | Densificación in situ | Casos particulares |
| **Silicatización, jet grouting, inyección química** | Refuerzo de los vínculos entre partículas | *"Han dado buenos resultados ante problemas localizados pero resultaron en general **onerosos**"* |
| **Cocción** | Tratamiento térmico del suelo | Anecdótico, muy caro |

> El texto es explícito: *"En estas últimas [edificaciones arquitectónicas], suele dar mejor resultado la adopción de medidas de diseño que minimicen el riesgo de ingreso de agua al terreno, **o mejoras en el terreno mediante sustitución de suelo combinados con plateas** que disminuyan significativamente las presiones en el suelo."*

**Esta frase es la receta para vivienda y edificios medianos en La Pampa: sustitución de suelo + platea.**

#### Estrategia 2 — Impedir que llegue el agua

Esto es **diseño arquitectónico y de instalaciones**, y es donde tu estudio tiene control directo:

| Medida | Detalle |
|---|---|
| **Veredas perimetrales** | Ancho mínimo **1,20 m** (mejor 1,50 m), con pendiente ≥ 2% hacia afuera, **con junta elástica sellada contra el muro**. No una vereda fisurada que sea un embudo |
| **Desagües pluviales alejados** | Descarga a **no menos de 3 m** del perímetro. Nunca a "pozo absorbente" cerca de la fundación |
| **Cañerías enterradas envainadas** | Toda cañería de agua o cloaca enterrada dentro del predio, **dentro de vaina con pendiente y cámara de inspección testigo**, de modo que una pérdida se vea y se drene, no se infiltre |
| **Prohibición de pozos absorbentes cerca** | Un pozo ciego a 3 m de una base en loess es una bomba de tiempo |
| **Riego y jardinería** | **Sin césped ni riego contra el muro.** Los canteros pegados a la casa son la causa n.º 1 de colapso localizado en vivienda |
| **Piletas de natación** | Verificar impermeabilidad y drenaje. Una pileta con pérdida junto a una casa en loess la parte al medio |
| **Nivelación general del terreno** | Pendiente que aleje el agua superficial de la construcción |

> **Este es el punto donde el interiorismo y el paisajismo tienen consecuencias estructurales.** Un cliente que quiere un jardín exuberante pegado a la casa está comprando un problema. Hay que decírselo en el anteproyecto, no cuando aparece la fisura.

#### Estrategia 3 — Convivir con el colapso (medidas estructurales)

*"Adopción de medidas estructurales (encadenado de las fundaciones y muros, empleo de tabiques estructurales, estructuras isostáticas, etc.) o disminuir la carga litostática mediante alivianamientos por excavación."*

| Medida | Efecto |
|---|---|
| **Encadenado completo de fundaciones y muros** | Convierte la estructura en una caja rígida que se asienta como un todo. Reduce las distorsiones angulares |
| **Estructuras isostáticas** | Un sistema isostático no genera esfuerzos secundarios por asentamiento diferencial |
| **Tabiques estructurales rígidos** | Rigidizan el conjunto y distribuyen |
| **Alivianamiento por excavación (fundación compensada)** | Excavar un subsuelo cuyo peso de suelo removido compense el peso del edificio → incremento neto de presión ≈ 0 → no se supera σF.SAT |
| **Plateas** | Bajan la presión de contacto y rigidizan |

**El texto también advierte sobre pilotes (verificado):**
> *"Con los antecedentes que tienen los suelos loessicos, existe una propensión a fundar las construcciones mediante pilotes. Sin embargo, existen numerosos casos donde este tipo de solución **no ha sido satisfactoria**... aún estructuras fundadas sobre pilotes han sufrido daños de importancia al colapsar el suelo que las rodea. Esta problemática está asociada a problemas de **disminución de capacidad friccional**, con la consiguiente transferencia de carga a la base del pilote y al fenómeno de **fricción negativa**, por un colapso generalizado de estratos de suelo autocolapsable."*

**Consecuencia de diseño [FIRMA]:** si vas a pilotes en loess colapsable:
1. **No cuentes con fricción lateral** en el manto colapsable — diseñá por punta.
2. **Sumá la fricción negativa** como carga adicional descendente sobre el pilote.
3. Considerá **camisa/vaina bituminosa** en el tramo colapsable para anular ambas.
4. La punta tiene que apoyar en un estrato competente **verificado**, no supuesto.

### 3.5.7 Efecto del nivel freático

Verificado: *"En muchas localidades, el aumento del nivel freático trae aparejado importantes asentamientos de las construcciones, debido al colapso y **cuando baja el nivel freático (o se abate por bombeo), se generan asentamientos por variación de tensiones efectivas**."*

Es decir: **te asienta cuando sube y te asienta cuando baja.** El ascenso satura y colapsa; el descenso aumenta las tensiones efectivas y consolida. Ambos procesos son irreversibles.

En Santa Rosa y en muchas localidades pampeanas hay antecedentes históricos de **ascenso de napa** por urbanización (impermeabilización de superficies, pérdidas de red, riego, eliminación de vegetación freatófita). **Pedí siempre la evolución histórica del nivel freático, no sólo la lectura del día del sondeo.**

## 3.6 Napa freática

### 3.6.1 Efectos sobre el proyecto

| Efecto | Consecuencia |
|---|---|
| **Reducción de la capacidad portante** | Bajo napa, γ' = γsat − γw ≈ γsat − 10 kN/m³. En el término `0,5·γ·B·Nγ` la capacidad puede caer ~50% |
| **Subpresión / flotación** | Un subsuelo bajo napa recibe `u = γw · h`. Con 3 m de napa sobre el fondo: 30 kPa hacia arriba, o sea 3 tn/m² |
| **Empuje hidrostático sobre muros** | Se suma al empuje de tierra y es **triangular con γw = 10 kN/m³**, mucho mayor que el empuje efectivo del suelo |
| **Ejecución** | Excavación bajo napa requiere depresión (wellpoints, pozos de bombeo) o recinto estanco |
| **Agresividad** | El agua freática puede contener sulfatos, cloruros. **Analizarla.** |
| **En loess** | Ascenso de napa → colapso. Descenso por bombeo → consolidación. **Ambos peligrosos.** |

### 3.6.2 Verificación de flotación [PD]

```
FS_flotación = W_estructura_permanente / U_subpresión ≥ 1,10 a 1,30
```
Usar **sólo cargas permanentes mínimas** (0,9 D). No contar con sobrecargas de uso ni con el peso del suelo sobre voladizos si no está garantizado.

Si no verifica: aumentar el peso (contrapiso pesado, losa de fondo más gruesa), anclar con micropilotes a tracción, o disponer drenaje permanente con alivio de subpresión (y entonces mantenerlo por siempre — es una servidumbre de mantenimiento).

### 3.6.3 Depresión de napa — advertencia

**Deprimir la napa para excavar produce asentamientos en las construcciones vecinas** en un radio que puede llegar a 5-10 veces la profundidad de depresión. En loess es doblemente peligroso. Antes de deprimir:
- Relevamiento y **acta de estado con fotos y fisurómetros** de todos los linderos.
- Cálculo del cono de depresión y de los asentamientos inducidos.
- **Sistema de recarga (*recharge wells*)** si hay linderos sensibles.
- Monitoreo topográfico durante toda la obra.

## 3.7 Contenido mínimo exigible al informe geotécnico

Devolvé el informe si le falta algo de esto:

1. **Ubicación exacta** de sondeos y calicatas en plano acotado, con cotas relativas al nivel de vereda.
2. **Perfiles estratigráficos** individuales con: descripción visual-manual, clasificación SUCS, N-SPT por metro, humedad natural, nivel freático.
3. **Perfil geotécnico interpretado** (corte transversal entre sondeos).
4. **Nivel freático**: cota medida, fecha, y **evolución histórica o estacional estimada**.
5. **Ensayos de laboratorio** con planillas: granulometría, Atterberg, densidad, y los específicos según el suelo.
6. **Análisis de colapsabilidad** (en loess): doble edométrico, perfil de σ0 vs. σF.SAT, potencial de colapso.
7. **Análisis químico**: sulfatos, cloruros, sales solubles totales, pH, materia orgánica. **Con la clase de exposición del CIRSOC 201 recomendada explícitamente.**
8. **Tensión admisible recomendada**, indicando: tipo de fundación supuesto, ancho y profundidad de referencia, factor de seguridad adoptado, y **si es a humedad natural o saturada**.
9. **Estimación de asentamientos** totales y diferenciales para la carga prevista.
10. **Módulo de balasto** (con indicación del ancho de referencia) si se va a modelar platea.
11. **Recomendaciones explícitas de tipo de fundación**, cota de fundación, y tratamientos de suelo si corresponden.
12. **Recomendaciones de excavación**: taludes estables, entibado, drenaje.
13. **Firma de profesional matriculado en geotecnia.**
14. **Parámetros para el cálculo de empujes** (c, φ, γ, Ka, Ko) si hay subsuelo o muros de contención.

**Lo que un buen geotécnico agrega y hay que pedirle:** una conversación. Mostrale el anteproyecto **antes** de que haga el estudio. Que sepa dónde va el núcleo de ascensores, si hay subsuelo, cuántas plantas. Un estudio hecho "a ciegas" sobre un lote es la mitad de útil.

---
---

# 4. FUNDACIONES

## 4.1 Árbol de decisión

```
                     ¿Qué carga baja y qué suelo hay?
                                   |
        +--------------------------+---------------------------+
        |                          |                           |
  ESTRATO COMPETENTE        ESTRATO COMPETENTE           SIN ESTRATO
  A POCA PROFUNDIDAD        A PROFUNDIDAD MEDIA          COMPETENTE
  (Df ≤ 3 m)                (3 - 8 m)                    ACCESIBLE
        |                          |                           |
  FUNDACIÓN DIRECTA          POZOS ROMANOS               PILOTES
        |                    (pozos de fundación)         (o mejorar
        |                     o pilotes cortos             el suelo)
        |
   ¿Σ área de bases / área de planta?
        |
   +----+---------------------+
   |                          |
  < 40-50%                  > 50%
   |                          |
  ZAPATAS                   PLATEA
  aisladas /                (o platea con
  corridas /                 vigas / con
  combinadas                 pilotes)
```

**Reglas de decisión rápidas [PD]:**

| Condición | Fundación |
|---|---|
| Σ áreas de zapatas > 50% del área de planta | **Conviene platea** — a partir de ahí el ahorro de excavación y encofrado compensa |
| Suelo heterogéneo con riesgo de asentamiento diferencial | **Platea** (rigidiza y reparte) |
| Suelo colapsable potencialmente colapsable | **Sustitución de suelo + platea** |
| Suelo autocolapsable | **Pilotes atravesando el manto + verificación de fricción negativa**, o tratamiento masivo del suelo |
| Napa alta con subsuelo | **Platea estanca (tipo "bañera")** con verificación de flotación |
| Bases muy cercanas entre sí (ejes a < 2× el ancho) | **Zapata combinada** |
| Base contra medianera con carga excéntrica | **Zapata combinada o excéntrica con viga de equilibrio** |
| Carga muy alta, suelo bueno pero profundo | **Pozos romanos o pilotes** |
| Edificio PB+9 en loess | Ver §4.8 |

## 4.2 Zapatas aisladas, corridas y combinadas

### 4.2.1 Predimensionado [PD]

**Paso 1 — área en planta (con cargas de SERVICIO, sin mayorar):**
```
A_requerida = N_servicio / σ_adm
```
Para zapata cuadrada: `B = sqrt(A)`. Para rectangular con relación L/B: `B = sqrt(A·B/L)`.

**Peso propio de la base y del suelo sobre ella:** se puede incluir aproximadamente incrementando N un **8-12%** [PD], o restándolo de σ_adm.

**Paso 2 — canto (altura) de la zapata [PD]:**

| Criterio | Expresión |
|---|---|
| **Zapata rígida** (recomendable — comportamiento predecible) | `h ≥ vuelo v` (v = (B − a)/2, a = lado de la columna). Es decir, ángulo de reparto ≤ 45° |
| **Zapata flexible** | `h ≥ v / 2`, pero exige verificación de flexión y de corte más cuidadosa |
| **Mínimo absoluto** | h ≥ 25 cm en zapatas aisladas; h ≥ 20 cm en corridas [VER exigencia del CIRSOC 201 art. 15.7] |
| **Recubrimiento** | 50 mm sobre hormigón de limpieza (verificado, Tabla 7.7.1 (a)) |

**Paso 3 — verificaciones obligatorias [FIRMA]:**

| Verificación | Sección crítica |
|---|---|
| **Presión de contacto** | σ_max ≤ σ_adm; con momento: `σ = N/A ± M/W`. Si e > B/6 hay despegue → recalcular con distribución triangular |
| **Punzonamiento (corte en dos direcciones)** | Perímetro crítico a **d/2** de la cara de la columna. `Vu ≤ φ·Vc` con φ = 0,75 |
| **Corte en una dirección** | Sección a **d** de la cara de la columna |
| **Flexión** | Sección **en la cara de la columna** (columna de hormigón) o a mitad entre cara y borde de placa (columna metálica) |
| **Anclaje de armaduras** | Longitud disponible desde la sección crítica hasta el borde |
| **Aplastamiento en la base de la columna** | Transferencia de la carga de la columna a la zapata |
| **Vuelco y deslizamiento** | Si hay momento o empuje |
| **Asentamiento** | Ver §4.7 |

**Paso 4 — armadura [PD]:**
- Cuantía mínima de la Tabla 7.12.2.1 (**ρ ≥ 0,0018 para fy = 420 MPa**, verificado) en cada dirección.
- Separación máxima: `s ≤ 3h` y `s ≤ 300 mm` (verificado, art. 7.12.2.2).
- En zapatas rectangulares, la armadura en la dirección corta se concentra: una fracción `2/(β+1)` en una banda central de ancho B [PD, verificar en CIRSOC 201 art. 15.4.4].

### 4.2.2 Zapatas corridas bajo muro portante

Para vivienda de mampostería portante:

```
B = q_muro [kN/m] / σ_adm [kPa]
```

Ejemplo [PD]: muro de ladrillo hueco portante 18 cm, PB+1, con losa de viguetas.
```
Carga del muro por metro:
  Muro PB (2,60 m) + muro PA (2,60 m) = 12 kN/m³ × 0,18 × 5,20 = 11,2 kN/m
  Losa PA + azotea (2 losas × 5,5 kN/m² × 3,0 m de tributaria) = 33,0 kN/m
  Sobrecargas (2 × 2,0 × 3,0)                                  = 12,0 kN/m
  Cimiento propio (estimado)                                    =  6,0 kN/m
  TOTAL SERVICIO                                               ≈ 62 kN/m

Con σ_adm = 100 kPa (1,0 kg/cm²):   B = 62/100 = 0,62 m  →  adoptar B = 0,70 m
Con σ_adm = 150 kPa (1,5 kg/cm²):   B = 62/150 = 0,41 m  →  adoptar B = 0,50 m
```
Canto: con B = 0,70 m y muro de 0,18 m, `v = (0,70 − 0,18)/2 = 0,26 m` → **h = 0,30 m** (rígida).

> **Cimiento de hormigón ciclópeo vs. zapata de HºAº:** el ciclópeo (hormigón pobre con piedra) trabaja sólo a compresión y necesita un ángulo de reparto de 60° respecto de la horizontal, lo que da cimientos altos y de mucho hormigón. Es tradicional y funciona en suelos buenos y cargas bajas, pero **es rígido y frágil ante asentamientos diferenciales**. En loess y en cualquier edificio, **zapata de hormigón armado con encadenado**, siempre.

### 4.2.3 Zapatas medianeras y combinadas

**Problema:** la columna medianera está en el borde de la zapata → excentricidad enorme → el suelo no puede equilibrar el momento.

**Soluciones:**

| Solución | Cuándo | Detalle |
|---|---|---|
| **Zapata combinada** (une la medianera con la primera columna interior) | Distancia entre columnas ≤ ~5-6 m | Se dimensiona para que la resultante de las dos cargas pase por el **centro de gravedad de la zapata** → presión uniforme. La zapata trabaja como viga invertida |
| **Viga de equilibrio (viga centradora / "cantilever footing")** | Distancia mayor | Viga rígida que une la zapata medianera con la interior; transfiere el momento. La base interior se descarga parcialmente — **verificar tracción** |
| **Zapata excéntrica con momento resistido por la estructura** | Solo con pórtico muy rígido | Poco recomendable, genera momentos importantes en la columna |

**Dimensionado de zapata combinada [PD]:**
```
Resultante: R = N1 + N2
Posición desde la columna 1:  x = N2·L / R
Longitud de la zapata:        Lz = 2·(x + a1/2)     (con a1 = lado de la columna medianera)
Ancho:                        Bz = R / (σ_adm · Lz)
```

## 4.3 Vigas de fundación y encadenados

Son la pieza que más se recorta en presupuesto y más problemas evita. **No las negocies.**

### 4.3.1 Funciones

1. **Arriostrar las bases** en ambas direcciones (exigido por INPRES-CIRSOC 103 Cap. 9 cuando aplica).
2. **Absorber momentos** de columnas medianeras y de esquina.
3. **Reducir asentamientos diferenciales** vinculando bases.
4. **Soportar los muros de planta baja** (evitar que carguen el contrapiso).
5. **Rigidizar el conjunto** frente a colapso localizado del suelo — **esencial en loess**.

### 4.3.2 Predimensionado [PD]

| Parámetro | Valor |
|---|---|
| Altura h | **L/12 a L/15** (L = luz entre bases), mínimo **40 cm** en edificios |
| Ancho b | **h/2 a h/3**, mínimo 20 cm (25 cm si recibe muro de 20) |
| Armadura | Simétrica arriba y abajo (puede haber inversión de momentos) |
| Cuantía mínima | ρ_min de flexión (art. 10.5.1) + estribos ϕ8 c/20 cm mínimo |
| Esfuerzo axial de arriostramiento | **[VER] INPRES-CIRSOC 103 art. 9.2.4.1.** Criterio usual [PD]: la viga debe resistir a tracción y compresión un valor del orden del **10% de la carga axial** de la base más cargada que vincula |

### 4.3.3 Encadenados en vivienda de mampostería

| Encadenado | Ubicación | Sección mínima típica [PD] |
|---|---|---|
| **Inferior** | Sobre el cimiento, bajo el muro | 20 × 20 cm, 4 ϕ8, estribos ϕ6 c/20 |
| **Intermedio** | A nivel de dintel de aberturas | 15-20 cm de altura, 4 ϕ8 |
| **Superior** | Coronando todos los muros bajo la losa/cubierta | 20 × 20 cm mínimo, 4 ϕ10 |
| **Verticales (columnas de encadenado)** | En esquinas, encuentros de muros, bordes de aberturas grandes, y cada **≤ 3,50 m** de muro | 20 × 20 cm o el espesor del muro, 4 ϕ10, estribos ϕ6 c/20 |

**[RC]** En zona sísmica 0 y con CIRSOC 501-E, los requisitos son los del reglamento empírico. En zonas 1-4, aplica **INPRES-CIRSOC 103 Parte III (2018)** y los requisitos son considerablemente más severos.

**El factor R de la Tabla 5.1 del 103 lo dice todo:** mampostería **sin encadenados R = 1,5**; **encadenada simple R = 3,0**; **encadenada armada R = 3,5**; **reforzada con armadura distribuida R = 4,0** (ladrillos cerámicos macizos). Encadenar duplica la capacidad de disipación. En La Pampa, aunque no sea exigible por sismo, **encadenar es la mejor protección contra el asentamiento diferencial por colapso del loess**.

## 4.4 Plateas

### 4.4.1 Cuándo

- Σ áreas de zapatas > 50% del área de planta.
- Suelo de baja capacidad o heterogéneo.
- **Suelo colapsable** (reduce la presión de contacto y rigidiza).
- Napa alta con subsuelo (estanqueidad).
- Cuando se busca **fundación compensada** (el peso del suelo excavado compensa el del edificio).

### 4.4.2 Tipologías

| Tipo | Descripción | Espesor típico [PD] |
|---|---|---|
| **Platea plana (losa maciza)** | Losa uniforme | h = 25 a 60 cm en edificios; 15-25 cm en vivienda |
| **Platea con capiteles / engrosamientos** | Refuerzo local bajo columnas | Base + 15-25 cm de sobreespesor local |
| **Platea nervurada (con vigas)** | Vigas invertidas o hacia abajo | Losa 20-25 cm + vigas de 60-100 cm de altura |
| **Platea celular / cajón** | Dos losas unidas por tabiques — máxima rigidez | Para edificios muy altos o suelos muy malos |
| **Platea sobre pilotes (*piled raft*)** | Combinada | Cuando la platea sola no basta pero los pilotes solos son antieconómicos |

### 4.4.3 Predimensionado [PD]

| Regla | Expresión |
|---|---|
| Espesor mínimo por punzonamiento | `h ≈ L/10` con L = luz entre columnas, o el que dé la verificación de punzonamiento sin armadura de corte |
| Espesor por número de plantas (edificios) | **h ≈ 5 cm por planta**, mínimo 30 cm. PB+9 → h ≈ 50 cm [PD, muy grosero] |
| Vivienda unifamiliar sobre suelo de baja capacidad | h = 15 a 20 cm + vigas perimetrales e interiores de 40-50 cm de altura |
| Armadura | Doble malla (superior e inferior), en ambas direcciones. Cuantía **≥ 0,0018** en cada cara y dirección |
| Cuantía real típica en edificios | 80 – 140 kg/m³ [PD] |

### 4.4.4 Modelado — el error del balasto

Ver §3.3.4. Repito porque es central: **el módulo de balasto NO es una propiedad del suelo, es una propiedad del conjunto suelo-fundación.** Depende del ancho cargado.

**Procedimiento correcto [PD]:**
1. Pedile al geotécnico el **k para el ancho real de tu platea**, no el kv1 de plato.
2. O calculalo: `k = q / s`, donde s es el asentamiento estimado de la platea bajo la presión media q.
3. **Iterá:** con el k inicial calculás asentamientos; si difieren de los estimados, corregís k.
4. **Análisis de sensibilidad obligatorio:** corré el modelo con **k/2 y k×2**. Si los momentos cambian mucho, tenés que refinar la geotecnia. Si cambian poco, estás cubierto.
5. Para plateas grandes, considerá **k variable**: mayor en el borde, menor en el centro (el "efecto plato"), o usá un modelo de semiespacio elástico.

### 4.4.5 Plateas en suelo colapsable — recomendaciones específicas

1. **Sustitución de suelo previa**: excavar 1,0-1,5 m, compactar el fondo, rellenar en capas de 20-25 cm con suelo seleccionado (o suelo-cemento 4-6% cemento) al **95-98% del Proctor estándar**, con control de densidad **cada capa y cada 200 m²**.
2. **Presión de contacto baja**: apuntá a `q ≤ 0,5 · σF.SAT` [PD] para tener margen frente al colapso.
3. **Rigidez alta**: vigas perimetrales e interiores. La platea tiene que poder "puentear" una zona colapsada.
4. **Vereda perimetral de 1,20-1,50 m** solidaria pero con junta sellada.
5. **Membrana de polietileno de 200 μm** bajo la platea (barrera de vapor y de humedad ascendente).
6. **Nunca cañerías bajo la platea** sin vaina registrable. Todo pase de instalación por encima o en vaina.

## 4.5 Pozos romanos (pozos de fundación)

Solución tradicional argentina, muy usada en el centro del país, **precisamente por el loess**: permite atravesar el manto superficial colapsable y apoyar en el estrato competente (frecuentemente la "tosca").

### 4.5.1 Descripción

Excavación cilíndrica de diámetro **0,80 a 1,20 m** (habitualmente 1,00 m), ejecutada a mano o con equipo de hélice, hasta el estrato resistente, y rellenada con **hormigón simple o pobre** (H-8 a H-13), a veces con **ensanchamiento de la base ("campana", "bulbo")**. Sobre el pozo apoya un **dado o cabezal de HºAº** que recibe la columna.

```
       columna
          |
     +---------+  ← dado / cabezal de HºAº armado
     |         |
     +---------+
        |   |
        |   |     ← fuste de hormigón simple  Ø 0,80-1,20 m
        |   |        (H-8 a H-13)
        |   |
      /       \   ← base ensanchada (campana), opcional
     /         \     Ø hasta 2,0-2,5 veces el fuste
    +-----------+
   ESTRATO COMPETENTE (tosca / loess denso / arena densa)
```

### 4.5.2 Cuándo usarlos

| Favorable | Desfavorable |
|---|---|
| Estrato competente entre **2,5 y 8 m** | Estrato competente > 8-10 m (usar pilotes) |
| Suelo cohesivo que se sostiene sin entibar | **Suelo granular suelto o con napa: NO se puede excavar a mano** |
| Sin napa (o napa por debajo del fondo) | Napa por encima del fondo |
| Cargas medias a altas por columna (300-2000 kN) | Cargas muy bajas (antieconómico) |
| Necesidad de atravesar manto colapsable | — |

### 4.5.3 Predimensionado [PD]

**Capacidad por punta (el fuste de hormigón simple no toma tracción ni flexión, sólo compresión):**
```
Q_adm = σ_adm_estrato · A_base
```
**Verificación del fuste como elemento de hormigón simple:**
```
σ_hormigón = N / A_fuste ≤ 0,3 · f'c  [PD, criterio conservador para hormigón simple; VER art. 22 del CIRSOC 201 para hormigón estructural simple]
```
Con H-13 (f'c = 13 MPa) y ϕ 1,00 m (A = 0,785 m²):
```
N_max ≈ 0,3 × 13.000 kPa × 0,785 = 3060 kN ≈ 310 tn
```
Es decir, **el hormigón del fuste rara vez es el condicionante; lo es la capacidad del estrato de apoyo.**

**Ensanchamiento de base:** relación diámetro base / diámetro fuste habitual ≤ 2,5. El ángulo del tronco de cono ≥ 60° respecto de la horizontal, para que trabaje por compresión pura.

### 4.5.4 Reglas de ejecución [FIRMA en el control]

1. **Hormigón de limpieza / fondo limpio y seco.** Ver el fondo antes de hormigonar: **inspección obligatoria por el director técnico**, con fotos y planilla.
2. **Nunca dejar un pozo abierto de un día para el otro sin tapa.** Riesgo de vida y de derrumbe.
3. **Prohibido el ingreso de personal sin entibado, ventilación y línea de vida** por debajo de 1,50 m. Los accidentes en pozos romanos son de los más letales de la construcción argentina.
4. **Verificar profundidad de cada pozo individualmente.** El estrato competente ondula. Un pozo "corto" es una base que se va a asentar.
5. **Cabezal armado y vinculado con vigas de fundación** en ambas direcciones.
6. **En loess:** el pozo debe atravesar **todo** el manto colapsable. Si el manto autocolapsable sigue por debajo de la punta, hay fricción negativa y no hay solución con pozos.

## 4.6 Pilotes y micropilotes

### 4.6.1 Tipologías

| Tipo | Diámetro | Ejecución | Cuándo |
|---|---|---|---|
| **Pilote excavado / perforado (*bored pile*)** | 0,40 – 1,50 m | Perforación con hélice o balde, armado y hormigonado in situ | El más usado en edificios. Sin vibración |
| **Pilote hélice continua (CFA)** | 0,40 – 1,00 m | Hélice continua, hormigón bombeado por el alma | Rápido, limpio, sin entubado. Requiere equipo especializado |
| **Pilote hincado prefabricado** | 0,25 – 0,50 m | Hincado con martillo | Alta capacidad, pero **vibraciones** que dañan linderos |
| **Micropilote** | **0,10 – 0,30 m** | Perforado, armado con tubo o barra, inyectado con lechada de cemento | **Recalce, refuerzo, espacios reducidos, obras en edificios existentes** |

### 4.6.2 Capacidad de un pilote

```
Q_ult = Q_punta + Q_fuste − W_pilote
Q_punta = qp · Ap
Q_fuste = Σ ( fsi · As,i )
Q_adm = Q_ult / FS          FS = 2,0 a 3,0  [PD]
```

Para suelos cohesivos [PD]:
```
qp = 9 · cu                      (arcillas)
fs = α · cu                      α ≈ 0,5 a 1,0 (método α, decreciente con cu)
```
Para suelos granulares [PD]:
```
qp = σ'v · Nq*                   (Nq* de Meyerhof/Berezantzev, función de φ)
fs = K · σ'v · tanδ              K ≈ 0,7-1,0·K0 (perforado), δ ≈ 0,7-1,0·φ
```

**Siempre limitar qp y fs a valores máximos** (qp ≤ 10-15 MPa, fs ≤ 100-200 kPa) porque las expresiones divergen con la profundidad.

### 4.6.3 Fricción negativa (*down-drag*) — obligatorio en loess colapsable

Cuando el suelo se asienta **más que el pilote**, la fricción cambia de sentido y **carga** al pilote en lugar de sostenerlo.

```
Q_total_pilote = Q_estructura + Q_fricción_negativa
```

Causas: colapso del loess por humedecimiento, consolidación de un relleno reciente, descenso de napa, terraplenado sobre el terreno.

**Mitigación:**
- **Vaina bituminosa** (*bitumen slip coat*) en el tramo colapsable: reduce la fricción negativa un 70-90%.
- **Camisa perdida de PVC o chapa** con relleno anular de bentonita.
- Diseñar el pilote **exclusivamente por punta** en el tramo comprometido.
- Reducir el número de pilotes y aumentar el diámetro (menos superficie lateral por unidad de carga).

### 4.6.4 Micropilotes — la herramienta de la reforma

| Característica | Valor típico [PD] |
|---|---|
| Diámetro de perforación | 100 – 300 mm |
| Armadura | Tubo de acero (API N-80 o similar) o barra ϕ25-40 mm o barra autoperforante |
| Carga admisible | **150 – 600 kN** por unidad (hasta 1000 kN con tubos gruesos e inyección repetitiva) |
| Longitud | 6 – 25 m |
| Inyección | IU (única global), IR (repetitiva), IRS (repetitiva selectiva con obturador doble) — la IRS es la que da mayor capacidad |
| Equipo | Perforadora de pequeño porte: **entra por una puerta, trabaja con 2,5 m de altura libre** |

**Por qué son la solución de reforma:**
- Se ejecutan **desde el interior de un edificio existente**, en sótanos, con altura libre mínima.
- **Vibración prácticamente nula** — no dañan lo existente.
- Se pueden inclinar para llegar bajo un cimiento existente.
- Trabajan a **compresión y a tracción** (anclajes contra subpresión).

**Usos típicos:**
1. **Recalce** de cimientos que se asientan.
2. **Refuerzo** de fundaciones para ampliación en altura.
3. **Anclaje** contra flotación.
4. Fundación de nuevas columnas dentro de un edificio existente.
5. Estabilización de taludes y muros.

## 4.7 Asentamientos: totales y diferenciales admisibles

### 4.7.1 Qué es qué

```
   Columna A                      Columna B
      |                              |
   ---+------------------------------+---   nivel original
      |                              |
      |  s_A                         |  s_B
      v                              v
   ---+---------____                 |
                    ------____       |
                              -------+---   nivel deformado
                              
   δ = |s_B − s_A|  = asentamiento diferencial
   β = δ / L        = distorsión angular  ← ESTE es el parámetro de daño
```

### 4.7.2 Límites de distorsión angular β [PD] — criterio clásico (Bjerrum, Skempton-MacDonald)

| β = δ/L | Consecuencia |
|---|---|
| **1/750** | Límite para maquinaria sensible |
| **1/600** | Límite para pórticos arriostrados |
| **1/500** | **Límite seguro para no fisurar** en edificios convencionales |
| **1/300** | Primeras fisuras en tabiques y muros. Dificultades en grúas puente |
| **1/250** | Inclinación de edificios altos perceptible a simple vista |
| **1/150** | **Fisuración severa** en tabiques y muros. Daño estructural probable |
| **1/150** | Límite de seguridad para muros flexibles |

**Criterio operativo [PD]:** proyectá para **β ≤ 1/500** en edificios con tabiquería de mampostería, **β ≤ 1/300** con tabiquería seca.

### 4.7.3 Asentamiento total admisible [PD]

| Tipo de estructura | s_total admisible |
|---|---|
| Zapatas aisladas en arena | 25 mm |
| Zapatas aisladas en arcilla | 40 mm |
| Plateas en arena | 40 – 65 mm |
| Plateas en arcilla | 65 – 100 mm |
| Estructura hiperestática sensible | 25 mm |

**Nota importante:** el asentamiento total en sí mismo no daña (un edificio que baja 5 cm uniformemente no se fisura). **Lo que daña es el diferencial.** Pero se limita el total porque el diferencial suele ser una fracción del total (habitualmente 50-75% para zapatas y 30-50% para plateas).

### 4.7.4 Cálculo de asentamientos

**Inmediato (elástico):**
```
s_i = q · B · (1 − ν²) · If / Es
```
con If = factor de forma y rigidez (0,88 para placa rígida cuadrada; 1,12 para flexible cuadrada en el centro).

**Por consolidación primaria (suelos cohesivos saturados):**
```
s_c = ( Cc · H / (1 + e0) ) · log10( (σ'0 + Δσ) / σ'0 )       (normalmente consolidado)
s_c = ( Cs · H / (1 + e0) ) · log10( σ'p / σ'0 ) + ( Cc · H / (1+e0) ) · log10( (σ'0+Δσ)/σ'p )   (sobreconsolidado)
```

**Por colapso (loess) — el que importa acá:**
```
s_colapso = Σ ( PCi / 100 ) · Hi        para los estratos donde σ_actuante > σF.SAT
```
Con PC = potencial de colapso (%) del doble edométrico y Hi = espesor del estrato.

> **Ejemplo del orden de magnitud:** manto de 6 m de loess con PC = 4% bajo la presión de la obra → `s = 0,04 × 6000 mm = 240 mm`. **24 cm.** No hay estructura que tolere eso diferencialmente. Por eso la sustitución de suelo y el control del agua no son "recomendaciones", son el proyecto.

## 4.8 EJEMPLO NUMÉRICO 1 — Fundación de un edificio PB+9

### Enunciado

Edificio de vivienda multifamiliar en Santa Rosa, La Pampa.

| Dato | Valor |
|---|---|
| Plantas | PB + 9 (10 niveles) + azotea + sala de máquinas |
| Planta | 20,00 m × 15,00 m = **300 m²** |
| Altura total | 30 m |
| Estructura | Pórticos de HºAº + núcleo de tabiques (ascensores + escalera) |
| Malla de columnas | 5,00 × 5,00 m (5 ejes × 4 ejes = 20 columnas) |
| Grupo (103) | B → γr = 1,0 |
| **Suelo (informe geotécnico ficticio pero realista para la zona)** | |
| 0,00 – 1,50 m | Suelo vegetal + relleno + loess primario muy suelto. **NO APTO** |
| 1,50 – 7,00 m | **Loess limoso ML, N-SPT 6-10, γd = 13,5 kN/m³, potencialmente colapsable (PC = 3,5% a 200 kPa)** |
| 7,00 – 12,00 m | Loess loessoide compacto, N-SPT 18-25, no colapsable |
| 12,00 m – + | Tosca / limo cementado, N-SPT > 40 |
| Napa | No detectada hasta 20 m |
| σ_adm a 2,00 m de profundidad, a humedad natural | 130 kPa (1,3 kg/cm²) |
| σ_adm a 2,00 m, **saturado** | **60 kPa (0,6 kg/cm²)** |
| σF.SAT del manto 1,5-7,0 m | ≈ 120 kPa |

### Paso 1 — Cargas de servicio

Peso por planta tipo:

| Concepto | kN/m² |
|---|---|
| Losa de viguetas + capa de compresión (h=17 cm) | 2,20 |
| Contrapiso + carpeta + piso | 2,06 |
| Cielorraso | 0,20 |
| Tabiquería | 1,00 |
| Peso propio de vigas y columnas repartido [PD: 1,5-2,0 kN/m²] | 1,80 |
| **D por planta** | **7,26** |
| L (vivienda) | 2,00 |
| **D + L de servicio por planta** | **9,26** |

Azotea (con equipos, tanque, sala de máquinas — mayorada localmente):

| Concepto | kN/m² |
|---|---|
| D azotea (losa + contrapiso pendiente + aislaciones + parapetos) | 7,50 |
| Lr | 1,00 |
| **Total azotea** | **8,50** |

**Peso total del edificio (servicio):**
```
9 plantas tipo + PB:  10 × 300 m² × 9,26 kN/m² = 27.780 kN
Azotea:                    300 m² × 8,50 kN/m² =  2.550 kN
Tanque + sala de máquinas (estimado)           =    600 kN
                                          TOTAL ≈ 30.930 kN  ≈ 3.150 tn
```

Presión media si repartiéramos en toda la planta:
```
q_media = 30.930 kN / 300 m² = 103 kPa  ≈ 1,03 kg/cm²
```

### Paso 2 — Reducción de sobrecarga en columnas interiores

Columna interior típica: AT = 5,00 × 5,00 = 25 m²/planta, 10 plantas.
```
KLL · AT = 4 × 25 × 10 = 1000 m²
L = Lo · (0,25 + 4,57/sqrt(1000)) = 2,00 × (0,25 + 0,1445) = 2,00 × 0,395 = 0,79 kN/m²
Límite inferior: 0,40 · Lo = 0,80 kN/m²   →  RIGE L = 0,80 kN/m²
```
Carga axial de servicio de columna interior:
```
D:  10 plantas × 25 m² × 7,26 = 1.815 kN
Lr azotea:  25 × 1,00        =    25 kN
L reducida: 10 × 25 × 0,80   =   200 kN   (aprox.)
N_servicio ≈ 2.040 kN ≈ 208 tn
```

**Control rápido [PD]:** regla de "1 tonelada por m² tributario por planta" → `25 m² × 10 plantas × 1,0 tn = 250 tn`. Nuestro cálculo (208 tn) queda por debajo porque aplicamos reducción de sobrecarga. **El orden de magnitud cierra.** Esa regla es útil para chequear que no metiste un cero de más.

### Paso 3 — Tanteo A: zapatas aisladas

Con σ_adm = 130 kPa (a humedad natural, cota −2,00 m):
```
A = 2.040 / 130 = 15,7 m²  →  B = 3,96 m  →  adoptar 4,00 × 4,00 m
```

Verificación de superficie ocupada:
```
20 columnas × 16 m² = 320 m²  >  300 m² de planta
```
**Las zapatas no entran en la planta.** Se solapan. **Descartado: hay que ir a platea.**

Este es exactamente el criterio de la §4.1: cuando Σ áreas de zapatas > 50-100% del área de planta, **la platea es obligada**.

### Paso 4 — Tanteo B: platea

**Presión de contacto:**
```
Peso del edificio                     = 30.930 kN
Peso propio de la platea (h = 0,60 m) = 300 × 0,60 × 25 = 4.500 kN
Peso del contrapiso y solado de PB    ≈   300 kN
                              TOTAL   ≈ 35.730 kN

Área de platea (con voladizo de 0,50 m perimetral): 21,0 × 16,0 = 336 m²
q_media = 35.730 / 336 = 106 kPa  ≈ 1,06 kg/cm²
```

**Verificación 1 — capacidad a humedad natural:**
```
q = 106 kPa  <  σ_adm = 130 kPa      ✓ VERIFICA
```

**Verificación 2 — CAPACIDAD EN CONDICIÓN SATURADA (la que importa):**
```
q = 106 kPa  >  σ_adm_saturado = 60 kPa      ✗ NO VERIFICA
```

**Verificación 3 — riesgo de colapso:**
```
Presión de tapada a 2,00 m:        σ0 = 18 kN/m³ × 2,00 = 36 kPa
Presión total con la obra:         σ = 36 + 106 = 142 kPa
σF.SAT del manto:                  120 kPa
142 kPa > 120 kPa      ✗ HAY COLAPSO SI SE HUMEDECE
```

**Estimación del asentamiento por colapso:**
```
Manto comprometido: de 2,0 a 7,0 m = 5,0 m de espesor
s_colapso = 0,035 × 5.000 mm = 175 mm  = 17,5 cm
```
**Inaceptable.** Y ese es el promedio: el diferencial sería del orden de la mitad, es decir ~9 cm en una luz de 5 m → `β = 90/5000 = 1/56`. Colapso de la mampostería, roturas de instalaciones, edificio inutilizable.

### Paso 5 — Decisión de proyecto

Tres alternativas, evaluadas:

| Alternativa | Descripción | Costo relativo [PD] | Riesgo residual |
|---|---|---|---|
| **A. Platea + sustitución masiva de suelo** | Excavar hasta −4,0 m, rellenar 2,0 m con suelo-cemento compactado, platea a −2,0 m | 1,00 | **Medio**: quedan 3 m de manto colapsable entre −4,0 y −7,0 m que sigue recibiendo presión |
| **B. Platea sobre pilotes (*piled raft*)** | Platea de 0,60 m + pilotes ϕ0,60 m hasta −13,0 m (empotrados 1 m en tosca) | 1,45 | **Bajo**, si se trata la fricción negativa |
| **C. Fundación compensada** | Subsuelo de 2 niveles (cochera), platea a −6,0 m. Suelo removido: 6,0 × 18 = 108 kPa ≈ presión de la obra | 1,60 (pero **genera superficie vendible**) | **Bajo** |

**Recomendación: alternativa B o C.** Si el proyecto arquitectónico requiere cochera (habitual en PB+9), la **C es la mejor**: resuelve el problema estructural y agrega valor comercial.

### Paso 6 — Desarrollo de la alternativa B (platea sobre pilotes)

**Pilotes:** ϕ 0,60 m, desde −2,0 m (fondo de platea) hasta −13,0 m → L = 11,0 m.

**Capacidad por punta en tosca (N > 40):**
```
qp ≈ 0,4 · N · Pa  ≈ 0,4 × 40 × 100 = 1600 kPa   [PD, correlación gruesa; VERIFICAR con ensayo de carga]
Ap = π × 0,30² = 0,283 m²
Q_punta = 1600 × 0,283 = 453 kN
```

**Capacidad por fuste — SOLO en el tramo NO colapsable (−7,0 a −13,0 m, L = 6,0 m):**
```
fs ≈ 0,01 · N · Pa ≈ 0,01 × 20 × 100 = 20 kPa (tramo −7 a −12, loessoide)
fs ≈ 0,01 × 40 × 100 = 40 kPa (tramo −12 a −13, tosca)
As = π × 0,60 = 1,885 m²/m
Q_fuste = 20 × 1,885 × 5,0 + 40 × 1,885 × 1,0 = 188 + 75 = 263 kN
```

**Fricción NEGATIVA en el tramo colapsable (−2,0 a −7,0 m, L = 5,0 m):**
```
fs_neg ≈ 15 kPa  [PD, estimado]
Q_neg = 15 × 1,885 × 5,0 = 141 kN   ← SE RESTA / SE SUMA COMO CARGA
```

**Capacidad neta:**
```
Q_ult_neta = (453 + 263) − 141 = 575 kN
Q_adm = 575 / 2,5 = 230 kN por pilote     ≈ 23 tn
```

**Con vaina bituminosa en el tramo colapsable** (reduce Q_neg un 80%):
```
Q_neg = 28 kN
Q_ult_neta = 716 − 28 = 688 kN
Q_adm = 688 / 2,5 = 275 kN  ≈ 28 tn
```

**Número de pilotes:**
```
n = 35.730 kN / 275 kN = 130 pilotes
```

**130 pilotes de ϕ0,60 × 11 m es mucho.** Vamos a ϕ0,80 m:
```
Ap = 0,503 m²  →  Q_punta = 1600 × 0,503 = 805 kN
As = 2,513 m²/m
Q_fuste = 20 × 2,513 × 5 + 40 × 2,513 × 1 = 251 + 101 = 352 kN
Q_neg (con vaina) = 15 × 0,2 × 2,513 × 5 = 38 kN
Q_ult_neta = 1157 − 38 = 1119 kN  →  Q_adm = 448 kN ≈ 46 tn
n = 35.730 / 448 = 80 pilotes
```

**80 pilotes ϕ0,80 × 11 m**, distribuidos ~4 por columna en un cabezal, o repartidos bajo la platea (piled raft) con mayor densidad bajo el núcleo de tabiques.

**Volumen de hormigón de pilotes:**
```
80 × 0,503 m² × 11 m = 443 m³
```

**[FIRMA] Verificaciones que faltan y son obligatorias:**
1. **Ensayo de carga sobre pilote de prueba** — indispensable, las correlaciones qp/fs tienen dispersión de ±50%.
2. Asentamiento del grupo de pilotes (mayor que el del pilote aislado por factor de grupo).
3. Punzonamiento de la platea sobre cada pilote y bajo cada columna.
4. Armadura de la platea por flexión con el modelo de suelo/pilotes correcto.
5. Verificación del núcleo de tabiques: es donde se concentra la carga y el momento de vuelco por viento.
6. Efecto del momento de vuelco del viento (§2.5.13: M ≈ 16.800 kNm) sobre la distribución de reacciones en los pilotes de borde.

**Efecto del viento sobre los pilotes de borde:**
```
Módulo resistente del grupo (aprox., dirección de 20 m):
  Con 80 pilotes distribuidos en 20 m de ancho:
  W_grupo ≈ n · x²_medio / x_max ≈ ... 
  Simplificando con distribución uniforme sobre B=20 m:
  ΔN = ± 6·M / (n · B) = ± 6 × 16.800 / (80 × 20) = ± 63 kN por pilote
```
Con N_medio = 448 kN, el pilote de borde pasa a **511 kN** en compresión (14% más) y a **385 kN** en el otro extremo. **No hay tracción.** ✓ El vuelco no compromete la fundación en este caso.

### Paso 7 — Resumen del ejemplo

| Concepto | Resultado |
|---|---|
| Peso total del edificio | ≈ 31.000 kN (3.150 tn) |
| Presión media si fuera platea directa | 106 kPa |
| σ_adm a humedad natural | 130 kPa ✓ |
| **σ_adm saturado** | **60 kPa ✗** |
| **Asentamiento por colapso estimado** | **17,5 cm — inadmisible** |
| **Solución adoptada** | **Platea 0,60 m sobre 80 pilotes ϕ0,80 × 11 m, con vaina bituminosa en tramo colapsable**, o subsuelo compensado |
| Ensayo obligatorio | **Prueba de carga sobre pilote** |

**Moraleja del ejemplo:** el número que decidió todo el proyecto de fundación no fue la carga del edificio; fue **σF.SAT = 120 kPa** del ensayo doble edométrico. Si el estudio de suelos no lo hubiera reportado, se habría proyectado una platea, el edificio se habría construido, y el problema habría aparecido a los 3-8 años, cuando alguien rompiera un caño o subiera la napa. **Ese es el valor de un buen estudio geotécnico.**

---
---

# 5. ESTRUCTURA DE HORMIGÓN ARMADO

## 5.1 Losas: tipologías y predimensionado

### 5.1.1 Panorama de tipologías

| Tipología | Luz económica | Espesor típico | Peso propio | Cuándo usarla |
|---|---|---|---|---|
| **Losa maciza en una dirección** | 3 – 6 m | 10 – 20 cm | 2,5 – 5,0 kN/m² | Luces cortas, plantas irregulares, balcones, escaleras |
| **Losa maciza en dos direcciones (con vigas)** | 4 – 8 m | 12 – 25 cm | 3,0 – 6,3 kN/m² | Paños aproximadamente cuadrados |
| **Losa de viguetas pretensadas + bloque (EPS o cerámico)** | 3 – 7 m | 12 + 5 a 20 + 5 cm | 2,0 – 3,5 kN/m² | **La más usada en vivienda en Argentina.** Rápida, sin encofrado de fondo continuo |
| **Losa nervurada in situ (unidireccional)** | 6 – 10 m | 25 – 40 cm | 3,5 – 5,5 kN/m² | Luces medias-grandes, se ve el nervio |
| **Losa casetonada / reticulada (bidireccional)** | 8 – 14 m | 30 – 50 cm | 4,5 – 7,0 kN/m² | **Grandes luces sin vigas descolgadas.** Cocheras, oficinas, plantas libres |
| **Losa plana maciza sin vigas (*flat slab*)** | 5 – 8 m | 18 – 30 cm | 4,5 – 7,5 kN/m² | Máxima altura libre, encofrado simple. **Cuidado con el punzonamiento** |
| **Losa plana con ábacos (*flat slab with drop panels*)** | 6 – 9 m | 18 – 28 cm + ábaco | 5,0 – 8,0 kN/m² | Ídem, resolviendo punzonamiento |
| **Losa postesada (adherente o no adherente)** | 8 – 14 m | L/40 a L/45 | 4,0 – 6,5 kN/m² | Grandes luces con espesor mínimo. Requiere especialista |
| **Losa colaborante (steel deck)** | 2,5 – 4,0 m sin apuntalar | 10 – 15 cm total | 1,8 – 2,8 kN/m² | Estructura metálica, obra rápida, sin encofrado |
| **Losa alveolar pretensada prefabricada** | 6 – 16 m | 15 – 40 cm | 2,5 – 5,0 kN/m² | Prefabricado, luces grandes, montaje veloz |

### 5.1.2 **[RC] Altura mínima sin verificar flechas — Tabla 9.5.a) CIRSOC 201-2005 (verificada, transcripción)**

Aplica a **vigas no pretensadas o losas armadas en una dirección**, para elementos que **NO soporten ni estén vinculados a tabiques divisorios u otros elementos susceptibles de sufrir daños por grandes flechas**:

| Elemento | Simplemente apoyado | Un extremo continuo | Ambos extremos continuos | En voladizo |
|---|---|---|---|---|
| **Losas macizas armadas en una dirección** | **L/20** | **L/24** | **L/28** | **L/10** |
| **Vigas o losas nervuradas en una dirección** | **L/16** | **L/18,5** | **L/21** | **L/8** |

**Notas textuales del reglamento:**
- La luz L se expresa en mm.
- Los valores son para hormigón de peso normal (**wc = 2500 kg/m³**) y armadura con **fy = 420 MPa**.
- a) Para hormigón liviano estructural con wc entre 1500 y 2000 kg/m³, multiplicar por **(1,65 − 0,0003·wc)**, valor que debe ser **≥ 1,09**.
- b) Para fy ≠ 420 MPa, multiplicar por **(0,4 + fy/700)**.

> **ATENCIÓN — el error más común con esta tabla:** dice explícitamente *"elementos que **no** soporten o estén vinculados a tabiques divisorios u otro tipo de elementos susceptibles de sufrir daños por grandes flechas"*. **En una vivienda o un edificio, casi todas las losas SÍ soportan tabiques.** Por lo tanto:
>
> **En la práctica, la tabla 9.5.a) NO te exime del cálculo de flechas en un edificio de vivienda.** O calculás flechas, o adoptás cantos con un margen del orden de **20-25% por encima** de los de la tabla [PD].

### 5.1.3 **[RC] Espesor mínimo de losas sin vigas interiores — Tabla 9.5.c) (verificada)**

Para losas con relación entre lados ≤ 2 (ℓn = luz libre en el sentido del lado mayor, en mm):

| fy (MPa) | Sin ábacos — losas exteriores **sin** vigas de borde | Sin ábacos — losas exteriores **con** vigas de borde | Sin ábacos — losas interiores | Con ábacos — exteriores sin vigas de borde | Con ábacos — exteriores con vigas de borde | Con ábacos — interiores |
|---|---|---|---|---|---|---|
| 280 | ℓn/33 | ℓn/36 | ℓn/36 | ℓn/36 | ℓn/40 | ℓn/40 |
| **420** | **ℓn/30** | **ℓn/33** | **ℓn/33** | **ℓn/33** | **ℓn/36** | **ℓn/36** |
| 520 | ℓn/28 | ℓn/31 | ℓn/31 | ℓn/31 | ℓn/34 | ℓn/34 |

**Espesores mínimos absolutos (art. 9.5.3.2, verificado):**
- **Losas sin ábacos: 120 mm**
- **Losas con ábacos: 100 mm**

Las vigas de borde deben tener **αf ≥ 0,8**.

### 5.1.4 **[RC] Espesor mínimo de losas con vigas en todos los lados (art. 9.5.3.3, verificado)**

```
a) para αfm ≤ 0,2:              se aplica el artículo 9.5.3.2 (tabla anterior)

b) para 0,2 < αfm ≤ 2,0:
                ℓn · ( 0,8 + fy/1400 )
        h ≥  ────────────────────────────────       pero h ≥ 120 mm
              36 + 5·β·(αfm − 0,2)

c) para αfm > 2,0:
                ℓn · ( 0,8 + fy/1400 )
        h ≥  ────────────────────────────           pero h ≥ 90 mm
                    36 + 9·β
```
donde β = relación entre luz libre larga y luz libre corta, y αfm = promedio de los αf de las vigas del contorno.

### 5.1.5 Reglas prácticas de predimensionado [PD]

| Tipología | Regla rápida |
|---|---|
| Losa maciza en una dirección, con tabiques encima | **h ≈ L/25** (continua) a **L/22** (simplemente apoyada) |
| Losa maciza en dos direcciones | **h ≈ (Lx + Ly) / 60** ó **h ≈ Lcorta/30** |
| Losa maciza en voladizo | **h ≈ L/9** (más exigente que L/10 por flechas) |
| Losa de viguetas | **h_total ≈ L/22 a L/25** (usar tablas del fabricante) |
| Losa nervurada | **h ≈ L/18 a L/20** |
| Losa casetonada | **h ≈ L/22 a L/25** |
| Losa plana sin vigas | **h ≈ L/30 a L/33** (según Tabla 9.5.c) |
| Losa postesada | **h ≈ L/40 a L/45** |

**Espesores mínimos por otras razones [PD]:**

| Razón | Espesor mínimo |
|---|---|
| Losa que recibe tabiques de mampostería | 12 cm |
| Losa de azotea accesible | 12 cm |
| Losa de cochera (carga concentrada 14 kN) | 15 cm |
| Losa de balcón en voladizo de 1,5 m | 15 cm |
| Resistencia al fuego F60 (losa maciza) | ≈ 10 cm [VER Tabla del CIRSOC 201 art. 7.7.7 / futuro CIRSOC 110] |
| Resistencia al fuego F120 | ≈ 12 cm [VER] |
| Aislación acústica entre unidades funcionales | ≥ 14 cm de losa maciza o solución multicapa [VER exigencia municipal] |

### 5.1.6 Flechas máximas admisibles — Tabla 9.5.b) (verificada parcialmente)

| Tipo de elemento | Deformación a considerar | Flecha límite |
|---|---|---|
| Cubiertas planas que **no** soportan ni están unidas a elementos no estructurales dañables | Flecha instantánea debida a **L** | **L/180** |
| Entrepisos que **no** soportan ni están unidos a elementos no estructurales dañables | Flecha instantánea debida a **L** | **L/360** |
| Entrepisos o cubiertas que **SÍ** soportan o están unidos a elementos no estructurales **susceptibles** de sufrir daños | Parte de la flecha que ocurre **después** de colocar los elementos no estructurales (flecha diferida + instantánea por L adicional) | **L/480** |
| Ídem, con elementos **no susceptibles** de sufrir daños | Ídem | **L/240** |

**[VER] los dos últimos valores exactos en la tabla del reglamento** — los dos primeros están verificados textualmente.

**El límite que importa en una vivienda es L/480 de la flecha diferida.** Una losa de 5 m: `5000/480 = 10,4 mm`. Con la fluencia lenta multiplicando por 2-3 la flecha instantánea, ese límite se alcanza rápido. Es la razón física por la que se fisuran los cielorrasos y se traban las puertas de placard.

**Factor de flecha diferida [VER art. 9.5.2.5]:** la formulación tipo ACI es
```
λΔ = ξ / (1 + 50·ρ')
```
con ξ = 2,0 para duración ≥ 5 años; 1,4 para 12 meses; 1,2 para 6 meses; 1,0 para 3 meses. ρ' = cuantía de armadura de compresión.

> **Truco de diseño real:** poner **armadura de compresión** (ρ' > 0) en el tramo reduce la flecha diferida notablemente. Con ρ' = 0,01: `λΔ = 2,0/(1+0,5) = 1,33` en lugar de 2,0. Un **33% menos de flecha diferida** con muy poco acero. En losas de gran luz con tabiquería encima, es una de las mejores relaciones costo/beneficio del proyecto.

### 5.1.7 Nota específica sobre losas de viguetas pretensadas

Es el sistema dominante en vivienda y edificios medios en La Pampa. Puntos que hay que controlar:

1. **Los fabricantes dan tablas de "luz máxima vs. sobrecarga"**. Esas tablas suelen estar hechas para una configuración de apoyo simple, con un valor de flecha admisible. **Verificá cuál es la hipótesis** — muchas tablas usan L/300, no L/480.
2. **Capa de compresión mínima: 5 cm** [VER exigencia exacta; el orden es 4-5 cm] con malla de ϕ4,2 c/15 cm o ϕ6 c/20 cm como armadura de retracción.
3. **Armadura de negativos sobre apoyos continuos** — se olvida sistemáticamente y produce fisuras transversales sobre las vigas.
4. **Nervios de reparto transversales** cada 1,50-2,00 m en losas de más de 4 m, para distribuir cargas concentradas.
5. **Apoyo mínimo de la vigueta**: 5 cm sobre viga de hormigón, 7-10 cm sobre muro [VER catálogo].
6. **Zonas macizadas**: alrededor de perforaciones, bajo tabiques paralelos a las viguetas, en apoyos con momento.
7. **Un tabique de mampostería paralelo a las viguetas y apoyado sobre una sola vigueta la sobrecarga groseramente.** Hay que macizar o poner un nervio de refuerzo.
8. **Apuntalamiento durante el hormigonado**: puntales cada 1,50-1,80 m, y **no retirarlos antes de los 14-21 días** (o antes de que el hormigón alcance la resistencia especificada).
9. **En balcones y voladizos NO se usan viguetas pretensadas** salvo diseño específico: el momento es negativo y las viguetas están armadas para positivo. **Balcón = losa maciza.**

## 5.2 Vigas

### 5.2.1 Predimensionado [PD]

| Parámetro | Regla |
|---|---|
| **Altura h** | **L/10 a L/12** (vigas de entrepiso continuas, cargas normales) |
| | **L/8 a L/10** (vigas muy cargadas, vigas de transferencia) |
| | **L/12 a L/14** (vigas poco cargadas, vigas de arriostramiento) |
| | **L/6 a L/8** en voladizo |
| | **Mínimo Tabla 9.5.a)**: L/16 (simple apoyo), L/18,5 (un extremo continuo), L/21 (ambos continuos), L/8 (voladizo) |
| **Ancho b** | **h/2 a h/3**, mínimo **20 cm** en edificios |
| | Si va embebida en muro de 20 cm: b = 20 cm |
| | Si va embebida en muro de 15 cm: b = 15 cm (y h más grande) |
| **Relación b/h** | Evitar h/b > 4 sin verificar **pandeo lateral-torsional** de la viga esbelta |
| **Cuantía objetivo** | ρ ≈ **0,008 a 0,015** — apuntá acá para tener economía y ductilidad |

**Regla mnemotécnica de obra [PD]:** *"altura en cm ≈ luz en metros × 8 a 10"*. Viga de 6 m → 50 a 60 cm de altura. Simple y sorprendentemente confiable para entrepisos de vivienda.

### 5.2.2 Vigas planas (embebidas en el espesor de la losa)

Cuando la arquitectura no admite viga descolgada:

| Aspecto | Consideración |
|---|---|
| **Altura** | h = espesor de losa (no puede crecer) |
| **Ancho** | Crece mucho: b = 40 a 100 cm |
| **Rigidez** | **Muy baja.** No aporta a la estabilidad lateral del pórtico |
| **Flechas** | Críticas. Verificar SIEMPRE |
| **Corte** | Crítico. h pequeño → d pequeño → Vc pequeño. Suele necesitar mucho estribado |
| **Armadura** | Cuantías altas, congestión de barras |
| **Cuándo evitarla** | Vigas de borde, vigas que reciben columnas, vigas de un pórtico resistente a acción lateral |

**Criterio [PD]:** viga plana **sólo** en luces ≤ 5 m, con cargas normales, y **nunca** como parte del sistema resistente a acciones laterales. Si la arquitectura la exige en luces mayores, la solución correcta es **losa postesada** o **casetonada**, no una viga plana forzada.

### 5.2.3 Ancho efectivo del ala (viga T)

Una viga solidaria a la losa trabaja como **viga T**, lo que aumenta mucho su capacidad a momento positivo. Ancho efectivo bef [VER art. 8.10 del CIRSOC 201 para los valores exactos; la formulación tipo ACI es]:

```
Viga T interior:   bef ≤ menor de { L/4 ;  bw + 16·hf ;  separación entre ejes de vigas }
Viga L (de borde): bef ≤ menor de { bw + L/12 ;  bw + 6·hf ;  bw + ½·luz libre a la viga adyacente }
```

**Aprovechar el ala te ahorra armadura en el tramo.** Pero ojo: en **momento negativo** (sobre apoyos) el ala está traccionada y **no colabora** — ahí la viga es rectangular de ancho bw, y ahí es donde suele necesitar más canto.

### 5.2.4 Verificaciones obligatorias [FIRMA]

| Verificación | Nota |
|---|---|
| Flexión ELU en tramo y apoyos | Con redistribución de momentos si corresponde [VER art. 8.4] |
| **Corte** | Vc + Vs. Estribos mínimos aunque no haga falta por cálculo |
| Torsión | Crítica en vigas de borde que reciben losa de un solo lado |
| Anclajes y empalmes | Longitudes de anclaje, empalmes por yuxtaposición o soldados |
| **Flechas ELS** | Instantánea + diferida (§5.1.6) |
| **Fisuración ELS** | Separación máxima de barras traccionadas [VER art. 10.6] |
| Apoyo de la viga | Aplastamiento, biela de apoyo |
| Vigas de gran canto (h/L > 0,25) | Modelo de bielas y tensores (Apéndice A) |

## 5.3 Columnas

### 5.3.1 Predimensionado por área tributaria — el método operativo [PD]

**Paso 1 — carga axial estimada:**
```
N = A_tributaria × n_plantas × q_planta
```
con q_planta = D + L de servicio por planta. Valores típicos:

| Uso | q_planta (kN/m²) | ≈ tn/m² |
|---|---|---|
| Vivienda con losa de viguetas | 7,5 – 9,0 | 0,75 – 0,90 |
| Vivienda con losa maciza | 8,5 – 10,0 | 0,85 – 1,00 |
| Oficinas | 8,0 – 9,5 | 0,80 – 0,95 |
| Cochera | 8,0 – 9,0 | 0,80 – 0,90 |
| Comercio | 10,0 – 12,0 | 1,00 – 1,20 |

**Regla de bolsillo argentina: 1 tn/m² por planta.** Es notablemente robusta para vivienda.

**Paso 2 — mayoración por flexión y posición:**

| Posición de la columna | Factor de mayoración [PD] |
|---|---|
| **Interior, vano intermedio** | **1,10** |
| **Interior, primer vano (adyacente al borde)** | **1,20 – 1,25** |
| **De borde (medianera)** | **1,30 – 1,40** |
| **De esquina** | **1,50 – 1,60** |

**Paso 3 — sección requerida:**
```
Ag = N_mayorado_por_posición / ( k · f'c )
```
con k = coeficiente que engloba φ, la contribución del acero y el margen para flexión:

| Situación | k [PD] |
|---|---|
| Columna con poca flexión, ρ ≈ 0,01-0,015 | **0,25 – 0,30** |
| Columna con flexión importante (borde, esquina, pórtico lateral) | **0,18 – 0,22** |
| Columna de planta baja de edificio alto (máxima carga) | **0,28 – 0,33** |

**Fórmula operativa unificada [PD]:**
```
Ag [cm²] = ( AT [m²] × n_plantas × q [tn/m²] × f_posición ) / ( 0,25 × f'c [MPa] / 10 )
```
o más simple, con f'c = 25 MPa (H-25) y k = 0,28:
```
Ag [cm²] ≈ N [tn] × 14
```
o con f'c = 30 MPa:
```
Ag [cm²] ≈ N [tn] × 12
```

**Tabla directa de predimensionado — vivienda, q = 0,85 tn/m², H-25, columna interior [PD]:**

| AT (m²) → | 12 | 16 | 20 | 25 | 30 | 36 |
|---|---|---|---|---|---|---|
| **PB+1** (2 plantas) | 20×20 | 20×20 | 20×20 | 20×25 | 20×25 | 20×30 |
| **PB+3** (4 plantas) | 20×20 | 20×25 | 20×30 | 20×35 | 25×35 | 25×40 |
| **PB+5** (6 plantas) | 20×30 | 20×35 | 25×35 | 25×40 | 30×40 | 30×45 |
| **PB+7** (8 plantas) | 25×30 | 25×40 | 30×40 | 30×45 | 30×50 | 35×50 |
| **PB+9** (10 plantas) | 25×40 | 30×40 | 30×45 | 30×55 | 35×55 | 40×55 |

> **Advertencia sobre esta tabla:** es para **columnas interiores** de un pórtico con losas y vigas normales, sin momentos importantes, con **H-25** y **cuantía ρ ≈ 0,015**. Para columnas de borde multiplicá el área por 1,3; para esquina por 1,5. Si la columna forma parte de un pórtico que toma viento sin tabiques, puede ser mucho mayor. **[FIRMA] Es predimensionado: hay que verificar con diagrama de interacción P-M.**

### 5.3.2 Dimensiones mínimas

| Criterio | Valor |
|---|---|
| **Lado mínimo de columna** | **20 cm** [PD; en zona sísmica 1-4, INPRES-CIRSOC 103 Parte II exige más — **[VER]**, el criterio ACI para pórticos especiales es 30 cm] |
| Lado mínimo en pórticos que resisten acción lateral | **25-30 cm** [PD] |
| Relación entre lados | **b/h ≥ 0,40** (evitar columnas muy alargadas que se comportan como tabiques cortos) |
| Área mínima | Ag ≥ 400 cm² (20×20) |

### 5.3.3 Esbeltez y efectos de segundo orden

```
λ = k · lu / r
```
con r = radio de giro (≈ 0,30·h para sección rectangular, 0,25·D para circular).

| Condición | Consecuencia |
|---|---|
| **Pórtico indesplazable (arriostrado):** `λ ≤ 34 − 12·(M1/M2)` y `λ ≤ 40` | Se pueden **despreciar** los efectos de esbeltez [VER art. 10.12.2] |
| **Pórtico desplazable:** `λ ≤ 22` | Se pueden despreciar [VER art. 10.13.2] |
| λ mayor | Hay que amplificar momentos: método de amplificación de momentos (δns, δs) o análisis de segundo orden |

**Para una columna típica de vivienda:** h = 30 cm → r = 9 cm; lu = 2,60 m (altura libre) → `λ = 1,0 × 260/9 = 29`. En pórtico arriostrado, **no hay problema de esbeltez**. En pórtico desplazable (sin tabiques), 29 > 22 → **hay que considerar esbeltez**.

> Esto explica por qué **poner tabiques rigidizadores no sólo resuelve el viento, sino que simplifica todas las columnas.** Un edificio con núcleo rígido tiene columnas indesplazables, sin problemas de esbeltez ni P-Δ significativo.

### 5.3.4 Continuidad y transiciones

- **Las columnas deben ser continuas desde la fundación hasta la cubierta.** Una columna que "nace" en el 1er piso apoyada en una viga es una **irregularidad estructural grave** (Tabla 2.4 línea 4b del 103) y exige diseñar la viga de transferencia para agotar la capacidad del elemento discontinuo (art. 2.6.3-b).
- **Las secciones deben ser constantes o crecientes hacia abajo** (Tabla 2.4, línea 4a).
- **Cambios de sección**: reducir de a poco (ej. de 30×50 a 30×40, no de 40×60 a 20×20 de golpe), y siempre manteniendo un eje o una cara alineada para poder empalmar barras.
- **Empalmes de armadura**: en la zona central del tramo de columna, no en los extremos (donde están los momentos y las rótulas plásticas potenciales).

## 5.4 Tabiques (muros de hormigón armado)

### 5.4.1 Cuándo van

**En un PB+9 en Santa Rosa, prácticamente siempre.** Razones:
1. Toman el corte y el momento de vuelco por viento con muy poca deformación.
2. Hacen indesplazable el pórtico → simplifican columnas, eliminan P-Δ.
3. El **núcleo de ascensores y escalera** es un tabique gratis: la arquitectura ya lo pide.
4. Rigidizan frente a asentamientos diferenciales.

### 5.4.2 Predimensionado [PD]

| Parámetro | Regla |
|---|---|
| **Espesor** | **h/25 de la altura libre entre losas**, mínimo **20 cm** en edificios (15 cm en PB+3 o menos). Para PB+9: **20-30 cm** |
| **Longitud total requerida** | Regla gruesa: la suma de las longitudes de tabiques en cada dirección ≈ **1,5 a 3 %** del área de planta [PD]. Para 300 m²: 4,5 a 9,0 m de tabique por dirección |
| **Relación de aspecto** | H/L > 2 → tabique esbelto, gobierna la flexión. H/L < 1 → tabique bajo, gobierna el corte |
| **Armadura mínima** | Ver §5.5. Doble malla en ambas direcciones si el espesor ≥ 20 cm |
| **Elementos de borde** | En los extremos del tabique, zona confinada con estribos cerrados — funciona como una "columna" embebida que toma la tracción y compresión del par |

### 5.4.3 Verificación de rigidez lateral [PD]

Rigidez de un tabique en voladizo:
```
K = 1 / ( H³/(3·E·I) + 1,2·H/(G·A) )
```
(el segundo término es la deformación por corte, **no despreciable** en tabiques bajos y anchos)

Con E = 4700·sqrt(f'c) MPa [VER art. 8.5.1 — la expresión reglamentaria para hormigón de peso normal es `Ec = 4700·sqrt(f'c)` en MPa] y G ≈ 0,4·E.

**Reducción de rigidez por fisuración [PD]:** para el análisis lateral, usar **I_efectivo ≈ 0,35·Ig** en tabiques fisurados y **0,70·Ig** en tabiques no fisurados. Para columnas 0,70·Ig, para vigas 0,35·Ig. Usar la rigidez bruta subestima las derivas un 40-60%.

### 5.4.4 Disposición en planta — la regla que evita torsión

```
❌ MAL: núcleo excéntrico              ✓ BIEN: tabiques repartidos
                                       
 +---------------------+               +---------------------+
 |[T]                  |               |[T]              [T] |
 |                     |               |                     |
 |                     |               |     [núcleo]        |
 |                     |               |                     |
 |                     |               |[T]              [T] |
 +---------------------+               +---------------------+
 CR muy lejos de CM                     CR ≈ CM
 → torsión grande                       → torsión mínima
```

**Regla [PD]:** la excentricidad entre el **centro de rigidez (CR)** y el **centro de masa (CM)** debería ser **< 10% de la dimensión de la planta en esa dirección**. Si el núcleo de ascensores está en una esquina (habitual en lotes entre medianeras), hay que compensar con tabiques en el lado opuesto.

**Verificación reglamentaria:** Tabla 2.3 línea 1a del INPRES-CIRSOC 103 — `δmk/δbk ≤ 1,2` para irregularidad torsional baja.

## 5.5 Armaduras mínimas y máximas

### 5.5.1 **[RC] Flexión — art. 10.5.1 CIRSOC 201 (verificado)**

```
              sqrt(f'c)
As,min  =  ───────────── · bw · d          (10-3)
              4 · fy

siempre que:      As,min ≥ 1,4 · bw · d / fy
```

Con f'c = 25 MPa y fy = 420 MPa:
```
sqrt(25)/(4×420) = 5/1680 = 0,00298
1,4/420 = 0,00333    ←  RIGE
As,min = 0,00333 · bw · d
```

Con f'c = 30 MPa: `sqrt(30)/(4×420) = 0,00326`; `1,4/420 = 0,00333` → sigue rigiendo 1,4/fy.
Con f'c = 35 MPa: `sqrt(35)/(4×420) = 0,00352` → **rige la primera expresión**.

**Regla práctica:** para f'c ≤ 31 MPa, `ρ_min = 1,4/fy = 0,00333`.

**Excepciones (verificadas):**
- **Art. 10.5.2:** para elementos estáticamente determinados con el ala traccionada, As,min ≥ el menor valor de (10-3) reemplazando bw por 2bw, o por el ancho del ala.
- **Art. 10.5.3:** si en cada sección el As adoptado **excede al menos en 1/3** al determinado por cálculo, no es necesario aplicar 10.5.1 ni 10.5.2.
- **Art. 10.5.4:** para **losas estructurales y fundaciones de espesor constante**, As,min en la dirección de la luz debe ser **la misma que la especificada en el art. 7.12** (contracción y temperatura).

### 5.5.2 **[RC] Contracción y temperatura — art. 7.12.2.1 (verificado)**

Cuantía mínima **respecto de la sección total o bruta (b·h)**:

| Condición | ρ mínima |
|---|---|
| **fy ≤ 420 MPa** | **0,0018** |
| **fy > 420 MPa** | **0,0018 × 420 / fy** |
| **En ningún caso** | **≥ 0,0014** |

**Separación máxima (art. 7.12.2.2, verificado):**
```
s ≤ 3 · h  (espesor de la losa)
s ≤ 300 mm
```

### 5.5.3 **[RC] Elementos comprimidos (columnas) — art. 10.9.1 (verificado)**

```
0,01 · Ag  ≤  Ast  ≤  0,08 · Ag
```

**Art. 10.9.2 (verificado) — número mínimo de barras longitudinales:**
- **4 barras** dentro de estribos rectangulares o circulares
- [VER el resto: 3 barras en estribos triangulares, 6 barras en zunchos en espiral]

**Nota importante (verificada, art. 10.8.4):** cuando la sección de la columna es mayor que la necesaria por consideraciones de carga, se puede usar un **área efectiva reducida Ag ≥ 50% del área total** para determinar la armadura mínima y la resistencia de diseño. Esto evita tener que armar una columna arquitectónicamente sobredimensionada con 1% de su área real.

**Cuantías prácticas [PD]:**

| Situación | ρ típica |
|---|---|
| Columna poco cargada / arquitectónica | 0,010 (mínimo) |
| Columna normal de edificio | **0,015 – 0,025** ← zona económica |
| Columna muy cargada de planta baja | 0,030 – 0,040 |
| Máximo práctico por congestión y empalmes | **0,04** (aunque el reglamento admita 0,08) |

> Por encima de ρ = 0,04 el hormigonado se vuelve un problema real: las barras y los empalmes no dejan pasar el hormigón, aparecen nidos de abeja, y el resultado es peor que una columna más grande con menos acero. **Si necesitás ρ > 0,04, agrandá la sección o subí la calidad del hormigón.**

### 5.5.4 **[RC] Estribos de columna — Tabla 7.10.5.1 (verificada)**

| Barras longitudinales db | Diámetro mínimo de estribo dbe |
|---|---|
| db ≤ 16 mm | **6 mm** |
| 16 mm < db ≤ 25 mm | **8 mm** |
| 25 mm < db ≤ 32 mm | **10 mm** |
| db > 32 mm | [VER — el valor sigue en la tabla, presumiblemente 12 mm] |

**Separación máxima de estribos [VER art. 7.10.5.2]** — criterio tipo ACI:
```
s ≤ 16 · db (diámetro de la barra longitudinal)
s ≤ 48 · dbe (diámetro del estribo)
s ≤ menor dimensión de la columna
```
Con ϕ12 longitudinal y ϕ6 de estribo, columna 20×30: `s ≤ min(192; 288; 200) = 192 mm` → **s = 15 cm** (adoptar redondo).

**En zonas de confinamiento (extremos de columna, longitud lo), la separación se reduce a la mitad o menos.** Aunque en zona sísmica 0 no sea exigible, es buena práctica.

### 5.5.5 Estribos mínimos en vigas [VER art. 11.5.5 y 11.5.6]

Criterio tipo ACI (verificar en el reglamento):
```
Av,min = 0,062 · sqrt(f'c) · bw · s / fyt      pero ≥ 0,35 · bw · s / fyt
s_max = d/2 ≤ 600 mm          (si Vs ≤ 0,33·sqrt(f'c)·bw·d)
s_max = d/4 ≤ 300 mm          (si Vs > 0,33·sqrt(f'c)·bw·d)
```

**[PD] Regla de obra:** estribos ϕ6 c/20 cm como piso absoluto en cualquier viga; ϕ8 c/15 en vigas de edificio; densificar a c/10 en los tercios extremos.

### 5.5.6 Cuantía balanceada y máxima por ductilidad

```
ρb = 0,85 · β1 · (f'c/fy) · ( 600 / (600 + fy) )
```
con β1 = 0,85 para f'c ≤ 30 MPa, reduciéndose 0,05 por cada 7 MPa por encima [VER art. 10.2.7.3], acotado a ≥ 0,65.

Con f'c = 25 MPa, fy = 420 MPa:
```
ρb = 0,85 × 0,85 × (25/420) × (600/1020) = 0,7225 × 0,0595 × 0,588 = 0,0253
```

**El CIRSOC 201-2005 (como ACI 318-02 en adelante) no limita ρ explícitamente**, sino que lo hace **a través de εt**: exige εt ≥ 0,004 en elementos a flexión, y penaliza con φ menor si εt < 0,005. En la práctica:

```
ρ_max (para εt = 0,005, φ = 0,90) ≈ 0,63 · ρb ≈ 0,016  (con f'c=25, fy=420)
```

**Diseñá con ρ ≤ 0,016 y tenés φ = 0,90, ductilidad y flechas razonables.** Es la zona económica.

## 5.6 Recubrimientos por exposición

### 5.6.1 **[RC] Tabla 7.7.1 CIRSOC 201 — recubrimientos mínimos (verificada, transcripción textual)**

Para hormigón colocado en obra (no pretensado), **clases de exposición A1 y A2**:

| Condición | Recubrimiento mínimo (mm) |
|---|---|
| **(a)** Hormigón colocado en la **base de las fundaciones**, en contacto con la capa de hormigón de limpieza (**no** incluye el espesor de la capa de limpieza) | **50** |
| **(b)** Hormigón **en contacto vertical con el suelo o expuesto al aire libre**: | |
| — para barras con db > 16 mm | **35** |
| — para barras y alambres con db ≤ 16 mm | **30** |
| **(c)** Hormigón **no expuesto al aire libre ni en contacto con el suelo**: | |
| **Losas, tabiques, nervaduras:** | |
| — para barras con db > 32 mm | **30** |
| — para barras y alambres con db ≤ 32 mm | **20**, pero ≥ db |
| **Vigas, columnas:** | |
| — para armadura principal | **db**, pero **≥ 20 y ≤ 40** |
| — para estribos abiertos y cerrados | **20** |
| — para zunchos en espiral | **40** |
| **Cáscaras y placas plegadas:** | |
| — para barras con db > 16 mm | 20 |
| — para barras y alambres con db ≤ 16 mm | 15 |

**Incrementos por clase de exposición (nota (*) verificada):**
- **Para A3, Q1 y C1**: incrementar los valores de la tabla un **30 %**
- **Para CL, M1, M2, M3, C2, Q2 y Q3**: incrementar los valores un **50 %**

**Ejemplo de aplicación:** una viga de balcón en Santa Rosa, expuesta al aire libre, clase A2:
```
Recubrimiento: 35 mm (barras > 16 mm) — es (b), aire libre
```
Si el ambiente fuera clase A3 (por ejemplo, alta humedad con ciclos de humedecimiento):
```
35 × 1,30 = 45,5 mm  →  adoptar 45 mm
```

**Adicionalmente:**
- **Art. 7.7.4 [verificado en su idea]:** el recubrimiento mínimo para **paquetes de barras** debe ser igual al diámetro equivalente del paquete, pero no mayor que 50 mm; **excepto** para hormigón colado contra el suelo y permanentemente en contacto con él, donde el recubrimiento mínimo será **70 mm**.
- **Art. 7.7.7 — recubrimiento por resistencia al fuego:** hay una tabla específica que clasifica losas y vigas según el tipo de agregado y la duración de la resistencia requerida. **[VER Tabla del art. 7.7.7.2]**

### 5.6.2 Clases de exposición — Tablas 2.1 y 2.2

**Clases generales que producen corrosión de armaduras (Tabla 2.1):**

| Clase | Descripción general [VER descripciones textuales exactas] |
|---|---|
| **A1** | Ambiente interior seco o protegido, sin riesgo de corrosión |
| **A2** | Ambiente exterior normal, humedad moderada |
| **A3** | Ambiente húmedo con ciclos de humedecimiento y secado |
| **CL** | Ambiente con cloruros de origen no marino (sales de deshielo, industrias) |
| **M1, M2, M3** | Ambientes marinos de agresividad creciente |

**Clases específicas (Tabla 2.2)** — degradación distinta de la corrosión:

| Clase | Descripción |
|---|---|
| **C1, C2** | Congelación y deshielo (C2 con sales) |
| **Q1, Q2, Q3** | Ataque químico de agresividad creciente (**sulfatos**, ácidos, etc.) |

**Para Santa Rosa [PD]:**

| Elemento | Clase probable |
|---|---|
| Estructura interior de vivienda o edificio | **A1** |
| Fachadas, balcones, azoteas expuestas | **A2** |
| Elementos en contacto con el suelo, sin sulfatos agresivos | **A2 o A3** |
| **Fundaciones en suelo con sulfatos** (frecuente en loess con yeso — verificado en §3.5.2: *"Frecuentemente se encuentra Yeso en cantidades variables"*, *"Los aniones más comunes son Sulfatos y Cloruros"*) | **Q1, Q2 o Q3 según el ensayo químico** |
| Piletas de natación, tanques | A3 / Q [VER] |

> **Esta es la razón por la cual el análisis químico del suelo es obligatorio en La Pampa.** El loess pampeano contiene yeso (sulfato de calcio) en cantidades variables. Un contenido alto de sulfatos exige **cemento resistente a sulfatos (ARS)** y **a/c ≤ 0,45 o 0,40**, más recubrimientos incrementados un 30-50%. No es un capricho: el ataque por sulfatos destruye la pasta de cemento y es irreparable.

### 5.6.3 **[RC] Tabla 2.5 — Requisitos de durabilidad (verificada, extracto)**

| Requisito | A1 | A2 | A3 y M1 | CL y M2 | M3 | C1 | C2 | Q1 | Q2 | Q3 |
|---|---|---|---|---|---|---|---|---|---|---|
| **a/c máxima — Hormigón simple** | — | — | — | 0,45 | 0,45 | 0,45 | 0,40 | 0,50 | 0,45 | 0,40 |
| **a/c máxima — Hormigón armado** | **0,60** | **0,50** | **0,50** | **0,45** | **0,40** | 0,45 | 0,40 | 0,50 | 0,45 | 0,40 |
| **a/c máxima — Hormigón pretensado** | 0,60 | 0,50 | 0,50 | 0,45 | 0,40 | 0,45 | 0,40 | 0,50 | 0,45 | 0,40 |
| **f'c mín (MPa) — Hormigón simple** | — | — | — | 30 | [VER] | [VER] | [VER] | [VER] | [VER] | [VER] |
| **f'c mín (MPa) — Hormigón armado** | **20** | **25** | **30** | **35** | [VER] | [VER] | [VER] | [VER] | [VER] | [VER] |
| **f'c mín (MPa) — Hormigón pretensado** | 25 | 30 | 35 | 40 | [VER] | [VER] | [VER] | [VER] | [VER] | [VER] |

**Lectura fundamental:** **la durabilidad, no la resistencia, es lo que suele fijar la clase de hormigón.** Una viga de balcón puede necesitar sólo H-20 por cálculo, pero si está en clase A2 el reglamento exige **H-25 y a/c ≤ 0,50**. Si está en A3, **H-30 y a/c ≤ 0,50**. **Especificá siempre la clase de exposición junto con la clase de hormigón: "H-25 / A2".**

Otros requisitos verificados de la Tabla 2.5 y artículos asociados:
- Elementos de espesor ≤ 500 mm en cierta clase: **H-30**; espesor > 500 mm: **H-20** [VER a qué clase corresponde exactamente].
- **Art. 3.1.1.2:** los hormigones de clase superior a **H-25** se deben elaborar con cementos de [VER tipo exacto]. También se pueden obtener hormigones de clase superior a H-25 con cementos de [VER].
- **Art. 5.1.2.4:** para hormigones de clase igual o mayor que **H-35**, las cantidades de aire intencionalmente incorporado tienen requisitos especiales.
- **Art. 5.3.1.2:** en la producción de hormigones de clase igual o mayor que **H-20** [VER exigencia].
- **Art. 5.3.x:** medición de materiales — **exclusivamente en masa para hormigones de clase mayor que H-20**; en masa o en volumen para clase ≤ H-20.
- El agregado fino para hormigones **H-20 o superior** tiene requisitos específicos (art. 3.x).

## 5.7 Cuantías de acero para presupuestar

**[PD]** Valores para cómputo de anteproyecto. Dispersión ±25%.

### 5.7.1 Por elemento — kg de acero por m³ de hormigón

| Elemento | kg/m³ típico | Rango |
|---|---|---|
| **Zapatas y bases aisladas** | **50** | 35 – 70 |
| **Vigas de fundación / encadenados** | **90** | 70 – 120 |
| **Platea de vivienda** | **70** | 55 – 90 |
| **Platea de edificio** | **110** | 80 – 150 |
| **Pilotes** | **80** | 60 – 120 |
| **Cabezales de pilotes** | **90** | 70 – 120 |
| **Losas macizas** | **80** | 60 – 100 |
| **Losas nervuradas / casetonadas** | **95** | 75 – 120 |
| **Capa de compresión sobre viguetas** | **35** | 25 – 50 |
| **Losas planas sin vigas** | **110** | 90 – 140 |
| **Vigas de entrepiso** | **120** | 90 – 160 |
| **Vigas de gran luz o de transferencia** | **180** | 140 – 250 |
| **Columnas de vivienda (PB+2)** | **90** | 70 – 120 |
| **Columnas de edificio (PB+9)** | **150** | 110 – 220 |
| **Tabiques / muros de HºAº** | **80** | 60 – 110 |
| **Núcleo de ascensores** | **100** | 80 – 140 |
| **Escaleras** | **95** | 75 – 120 |
| **Muros de contención** | **90** | 70 – 120 |
| **Tanque de agua elevado** | **130** | 100 – 180 |

### 5.7.2 Por planta — indicadores globales

| Tipología | Hormigón (m³/m² de planta) | Acero (kg/m² de planta) | Encofrado (m²/m² de planta) |
|---|---|---|---|
| **Vivienda unifamiliar, losa de viguetas** | 0,10 – 0,14 | **8 – 14** | 0,4 – 0,7 |
| **Vivienda unifamiliar, losa maciza** | 0,15 – 0,20 | 13 – 20 | 1,0 – 1,3 |
| **Edificio PB+3, losa de viguetas** | 0,14 – 0,18 | **14 – 20** | 0,8 – 1,1 |
| **Edificio PB+5, losa maciza + vigas** | 0,18 – 0,24 | **20 – 30** | 1,3 – 1,7 |
| **Edificio PB+9, losa maciza + vigas + tabiques** | 0,22 – 0,30 | **30 – 45** | 1,6 – 2,2 |
| **Edificio PB+9, losa plana sin vigas** | 0,25 – 0,32 | 35 – 50 | 1,2 – 1,5 |
| **Losa casetonada, luces 10-12 m** | 0,22 – 0,28 | 28 – 40 | 1,8 – 2,4 |
| **Losa postesada, luces 10-14 m** | 0,18 – 0,24 | 12 – 20 pasivo + **4 – 7 de cable** | 1,1 – 1,4 |
| **Cocheras subterráneas** | 0,30 – 0,45 | 40 – 60 | 1,8 – 2,5 |

### 5.7.3 Cómo usar estos números

**Ejemplo de cómputo rápido — edificio PB+9 de 300 m²/planta [PD]:**
```
Superficie total cubierta:  11 niveles × 300 m² = 3.300 m²
Hormigón de superestructura: 3.300 × 0,26 m³/m² = 858 m³
Acero de superestructura:    3.300 × 37 kg/m²   = 122.100 kg = 122 tn
Ratio de control:            122.100 / 858 = 142 kg/m³   ✓ razonable

Fundación (del Ejemplo 1):
  Pilotes:  443 m³ × 80 kg/m³   =  35.400 kg
  Platea:   336 × 0,60 = 202 m³ × 110 kg/m³ = 22.200 kg
  Subtotal fundación: 645 m³ / 57.600 kg

TOTAL OBRA:  1.503 m³ de hormigón / 179,7 tn de acero
Ratio global: 120 kg/m³
Acero por m² de planta cubierta: 179.700/3.300 = 54 kg/m²  (incluye fundación profunda)
```

**Chequeo de sensatez:** si tu cómputo de acero da menos de 25 kg/m² o más de 70 kg/m² en un edificio en altura, **revisá el modelo**. Alguna de las dos cosas está mal.

## 5.8 Hormigones H-17 a H-45

### 5.8.1 Designación

En Argentina, **H-XX** designa la **resistencia característica a compresión a 28 días sobre probeta cilíndrica, en MPa** (art. 2.x del CIRSOC 201, verificado: *"compresión del hormigón a la edad de diseño, expresada en MPa. Ejemplo: H-20, H-30..."*).

**H-20 = f'c = 20 MPa = 200 kg/cm².**

### 5.8.2 Tabla de usos, dosificaciones orientativas y control

| Clase | f'c (MPa) | Uso típico | a/c máx. orientativa [PD] | Cemento aprox. (kg/m³) [PD] | Asentamiento típico |
|---|---|---|---|---|---|
| **H-8 / H-13** | 8 / 13 | Hormigón de limpieza, relleno de pozos romanos, contrapisos | — | 150 – 200 | 5 – 10 cm |
| **H-17** | 17 | Hormigón simple, bases poco cargadas, muretes. **Insuficiente para HºAº en A1 (mínimo H-20)** | 0,65 | 250 | 8 – 12 cm |
| **H-20** | 20 | **Mínimo reglamentario para hormigón armado clase A1.** Bases, contrapisos armados, losas de vivienda simple | **0,60 (A1)** | 280 – 300 | 8 – 14 cm |
| **H-25** | 25 | **Mínimo para clase A2.** El "hormigón de uso general" en edificios. Losas, vigas, columnas de vivienda y edificios bajos | **0,50 (A2)** | 320 – 350 | 10 – 16 cm |
| **H-30** | 30 | **Mínimo para clase A3/M1.** Columnas de edificios medios, tabiques, elementos expuestos | **0,50 (A3)** | 350 – 380 | 10 – 18 cm |
| **H-35** | 35 | **Mínimo para clase CL/M2.** Columnas de plantas bajas en edificios altos, elementos pretensados, ambientes agresivos | **0,45** | 380 – 420 | 12 – 18 cm |
| **H-40** | 40 | Columnas muy cargadas, postesado, prefabricados. Requiere control estricto | 0,40 – 0,45 | 400 – 450 | 14 – 20 cm (con superfluidificante) |
| **H-45 y superiores** | ≥ 45 | Hormigón de alta resistencia. Columnas de edificios de gran altura, elementos especiales. **Requiere aditivos, adiciones (microsílice/escoria) y control de laboratorio** | ≤ 0,40 | 430 – 500 | Autocompactante o con superfluidificante |

> **Las dosificaciones son ORIENTATIVAS [PD].** La dosificación real la determina el hormigonero o el laboratorio a partir de los materiales disponibles, mediante **pastones de prueba**. No dosifiques vos por tabla.

### 5.8.3 Reglas de especificación

1. **Especificá siempre `H-XX / clase de exposición`**, ej. `H-25 / A2`.
2. **Especificá el tamaño máximo nominal del agregado (TMN)** en función de la separación de armaduras y del espesor: `TMN ≤ 1/5 de la menor dimensión`, `≤ 1/3 del espesor de la losa`, `≤ 3/4 de la separación libre entre barras` [VER art. 3.3.2].
3. **Especificá el asentamiento (cono de Abrams)** con tolerancia.
4. **Especificá el contenido mínimo de cemento**, no sólo el a/c.
5. **Especificá el aire incorporado** si hay exposición a congelación (clases C1/C2).
6. **Prohibí explícitamente el agregado de agua en obra.** Es la causa n.º 1 de hormigón que no cumple.
7. **Especificá el curado**: método y duración mínima.

### 5.8.4 Relación entre f'c y otras propiedades

```
Módulo de elasticidad (peso normal):  Ec = 4700 · sqrt(f'c)      [MPa]   [VER art. 8.5.1]
   H-20 → Ec = 21.019 MPa    H-25 → 23.500 MPa    H-30 → 25.743 MPa
   H-35 → 27.806 MPa         H-40 → 29.725 MPa    H-45 → 31.529 MPa

Módulo de rotura (tracción por flexión):  fr = 0,62 · sqrt(f'c)  [MPa]   [VER art. 9.5.2.3]
   H-25 → fr = 3,10 MPa

Resistencia a tracción por compresión diametral:  fct ≈ 0,53 · sqrt(f'c)  [PD]

Resistencia al corte del hormigón:  Vc = 0,17 · sqrt(f'c) · bw · d    [VER art. 11.3.1.1]
   (expresión simplificada, en N y mm)
```

**Consecuencia práctica que sorprende:** pasar de H-25 a H-40 (**+60% de resistencia**) sube el módulo de elasticidad sólo un **26%** y la resistencia al corte un **26%**. **La rigidez no crece proporcionalmente a la resistencia.** Si tu problema es la flecha o la deriva, subir la clase de hormigón es un remedio pobre; **agrandar la sección es mucho más efectivo** (la inercia va con h³).

## 5.9 Control de calidad del hormigón

### 5.9.1 Frecuencia de moldeo de probetas [VER art. 4.x y Cap. 5 del CIRSOC 201 / CIRSOC 200]

Criterio de referencia [PD, verificar en la norma vigente]:
- **Mínimo 1 pastón por día de hormigonado** y por clase de hormigón.
- **1 pastón cada 120 m³** o cada **500 m² de superficie de losas y tabiques**.
- **Mínimo 5 pastones** por obra (o ensayo de cada pastón si hay menos de 5).
- Cada pastón: **al menos 2 probetas** ensayadas a 28 días (más las que se ensayen a 7 días para control temprano).

### 5.9.2 Criterio de aceptación [VER art. 4.4 / 5.6 del CIRSOC 201]

Criterio de referencia tipo ACI [PD, **verificar textualmente**]:
1. **Todo promedio de 3 ensayos consecutivos** debe ser **≥ f'c**.
2. **Ningún ensayo individual** debe estar por debajo de **f'c − 3,5 MPa** (para f'c ≤ 35 MPa) o por debajo de **0,90·f'c** (para f'c > 35 MPa).

### 5.9.3 Si el hormigón no cumple

Secuencia [PD]:
1. **Revisar el ensayo** (curado de probetas, refrentado, prensa calibrada).
2. **Ensayos no destructivos** in situ: esclerómetro (índice de rebote), ultrasonido.
3. **Extracción de testigos** (norma IRAM 1551 [VER número y edición]) — el ensayo dirimente. Se acepta si el promedio de 3 testigos ≥ **0,85·f'c** y ningún testigo < **0,75·f'c** [VER criterio exacto].
4. **Prueba de carga** de la estructura (CIRSOC 201 Cap. 20 [VER]).
5. **Refuerzo o demolición.**

### 5.9.4 Otros controles a exigir en obra

| Control | Frecuencia |
|---|---|
| **Asentamiento (cono de Abrams)** | En cada camión, antes de descargar |
| **Temperatura del hormigón fresco** | En verano (> 30 °C es problema) y en invierno (< 5 °C es problema) |
| **Remito con hora de carga** | Máximo 90 min (o lo que fije el reglamento) entre carga y descarga |
| **Recubrimientos antes de hormigonar** | Separadores cada 50 cm en ambas direcciones. **Ladrillitos NO.** |
| **Limpieza del encofrado y de las armaduras** | Antes de cada colada |
| **Curado** | 7 días mínimo con riego, membrana o cobertura húmeda |
| **Desencofrado** | Laterales: 1-2 días. Fondos de losas y vigas: según edad y luz — **típicamente 14-21 días para losas y 21-28 para vigas de gran luz** [PD, verificar según proyecto] |
| **Reapuntalamiento** | Al menos 2 plantas apuntaladas por debajo de la que se hormigona |

## 5.10 EJEMPLO NUMÉRICO 2 — Predimensionado y verificación de losa y viga

### Enunciado

Entrepiso de vivienda multifamiliar, planta tipo del edificio del Ejemplo 1.

| Dato | Valor |
|---|---|
| Paño de losa | 5,00 × 5,00 m entre ejes de vigas |
| Vigas | 25 cm de ancho → luz libre 4,75 × 4,75 m |
| Uso | Vivienda → L = 2,00 kN/m² |
| Hormigón | H-25 (f'c = 25 MPa), clase A1 (interior) |
| Acero | ADN-420 (fy = 420 MPa) |
| **La losa soporta tabiques de mampostería** | → verificar flechas |

### Parte A — Losa maciza en dos direcciones

**A.1 — Predimensionado**

Losa con vigas en los cuatro lados, paño cuadrado (β = 1,0).

Regla rápida [PD]: `h ≈ Lcorta/30 = 4750/30 = 158 mm`.

Verificación con el art. 9.5.3.3, suponiendo αfm > 2,0 (vigas de canto importantes):
```
        ℓn · (0,8 + fy/1400)       4750 × (0,8 + 420/1400)     4750 × 1,10
h  ≥  ────────────────────────  =  ─────────────────────────  = ───────────  = 116 mm
             36 + 9·β                    36 + 9×1,0                 45
```
Mínimo absoluto: 90 mm (caso c).

**Pero la losa soporta tabiques.** Adoptamos con margen: **h = 15 cm**.

**A.2 — Cargas**

| Concepto | kN/m² |
|---|---|
| Peso propio losa: 25 × 0,15 | **3,75** |
| Contrapiso 8 cm: 18 × 0,08 | 1,44 |
| Carpeta 2 cm: 21 × 0,02 | 0,42 |
| Piso porcelanato | 0,20 |
| Cielorraso yeso | 0,20 |
| Tabiquería distribuida | 1,00 |
| **D total** | **7,01** |
| **L** | **2,00** |

**Combinación (9-2) / (2):**
```
qu = 1,2 × 7,01 + 1,6 × 2,00 = 8,41 + 3,20 = 11,61 kN/m²
```

**A.3 — Momentos (método de coeficientes, losa cuadrada empotrada en los 4 lados)**

Coeficientes [PD, tipo tablas de Marcus/Czerny/PCA para losa continua en 4 bordes, β=1]:
```
m_tramo   ≈ 0,036 · qu · ℓ²
m_apoyo   ≈ 0,075 · qu · ℓ²
```
Con ℓ = 4,75 m:
```
ℓ² = 22,56 m²
M_tramo = 0,036 × 11,61 × 22,56 = 9,43 kNm/m
M_apoyo = 0,075 × 11,61 × 22,56 = 19,64 kNm/m
```

**A.4 — Armadura**

Altura útil (recubrimiento 20 mm, barra ϕ10):
```
d = 150 − 20 − 10/2 = 125 mm = 0,125 m
```

**Armadura de tramo:**
```
Estimación:  As ≈ Mu / (φ · fy · 0,90 · d)
As = 9,43 × 10⁶ N·mm / (0,90 × 420 × 0,90 × 125) = 9,43e6 / 42.525 = 222 mm²/m
```
Verificación de cuantía mínima:
```
As,min = 0,0018 × 1000 × 150 = 270 mm²/m     ←  RIGE la mínima
```
**Adoptar ϕ8 c/18 cm = 279 mm²/m** ✓ (o ϕ10 c/25 = 314 mm²/m)

**Armadura de apoyo (negativos):**
```
As = 19,64e6 / 42.525 = 462 mm²/m
```
**Adoptar ϕ10 c/16 cm = 491 mm²/m** ✓

Verificación de separación máxima (art. 7.12.2.2):
```
s ≤ 3h = 450 mm  y  s ≤ 300 mm     →  180 y 160 mm ✓ VERIFICAN
```

**A.5 — Verificación de corte**
```
Vu ≈ 0,5 · qu · ℓn = 0,5 × 11,61 × 4,75 = 27,6 kN/m   (aprox., con coeficiente ~0,36 en losa bidireccional: ~19,8 kN/m)

φVc = 0,75 × 0,17 × sqrt(25) × 1000 × 125 / 1000 = 0,75 × 0,17 × 5 × 125 = 79,7 kN/m
```
```
Vu = 27,6 kN/m  <  φVc = 79,7 kN/m      ✓ VERIFICA con amplio margen
```
Las losas macizas de espesor normal casi nunca fallan por corte. ✓

**A.6 — Verificación de flecha (la crítica)**

Momento de inercia bruto:
```
Ig = 1000 × 150³ / 12 = 281,25 × 10⁶ mm⁴/m
```
Módulo de rotura:
```
fr = 0,62 × sqrt(25) = 3,10 MPa
```
Momento de fisuración:
```
Mcr = fr · Ig / yt = 3,10 × 281,25e6 / 75 = 11,63 × 10⁶ N·mm = 11,63 kNm/m
```

**Momento de servicio en el tramo** (D + L sin mayorar):
```
q_serv = 7,01 + 2,00 = 9,01 kN/m²
M_serv,tramo = 0,036 × 9,01 × 22,56 = 7,32 kNm/m
```
```
M_serv = 7,32 kNm/m  <  Mcr = 11,63 kNm/m      →  LA LOSA NO FISURA EN EL TRAMO
```
Se puede usar **Ie = Ig** en el tramo. ✓ Excelente.

**Flecha instantánea** (losa cuadrada empotrada, coeficiente α ≈ 0,00126 para carga uniforme y bordes empotrados [PD]):
```
Ec = 4700 × sqrt(25) = 23.500 MPa
δ_inst = α · q · ℓ⁴ / (Ec · Ie)  ... trabajando por franja de 1 m:
δ_inst ≈ 0,00126 × 9,01 N/mm/mm-ancho ... 
```
Cálculo por franja unitaria simplificado (viga empotrada-empotrada, y luego corregido por bidireccionalidad ~0,5):
```
δ_viga_emp = q·ℓ⁴/(384·E·I) = 9,01 × 4750⁴ / (384 × 23.500 × 281,25e6)
           = 9,01 × 5,09e14 / (3,175e15) = 1,44 mm     [q en N/mm por m de ancho = 9,01 N/mm]
Corrección por trabajo bidireccional ≈ ×0,7 (reparto en dos direcciones, apoyo en 4 bordes):
δ_inst ≈ 1,0 mm
```

**Flecha diferida** (λΔ = 2,0 sin armadura de compresión):
```
Flecha por carga permanente sostenida (D = 7,01 de 9,01 total):
δ_D_inst = 1,0 × 7,01/9,01 = 0,78 mm
δ_diferida = 2,0 × 0,78 = 1,56 mm
```

**Flecha total después de colocar los tabiques:**
```
δ = δ_diferida + δ_inst(L) = 1,56 + 1,0 × 2,00/9,01 = 1,56 + 0,22 = 1,78 mm
```

**Límite de la Tabla 9.5.b) para elementos que soportan tabiques dañables: L/480**
```
δ_adm = 4750 / 480 = 9,9 mm

δ = 1,78 mm  <<  9,9 mm      ✓ VERIFICA CON GRAN MARGEN
```

**Conclusión de la parte A:** losa maciza de **15 cm**, ϕ8 c/18 en ambas direcciones en el tramo, ϕ10 c/16 en los negativos sobre las vigas. **Verifica flexión, corte y flechas con holgura.**

> **Reflexión:** el margen es tan amplio porque el paño de 4,75 m es corto para una losa de 15 cm. Con h = 12 cm también verificaría flexión y corte, pero la flecha crecería con `(15/12)³ = 1,95` → δ ≈ 3,5 mm, todavía admisible. **Con h = 12 cm el peso propio baja de 3,75 a 3,00 kN/m², un ahorro de 0,75 kN/m² × 3.300 m² = 2.475 kN = 250 tn en toda la obra.** Eso son ~8 pilotes menos. **Vale la pena optimizar el espesor de losa en un edificio en altura.**

### Parte B — Viga de entrepiso

**B.1 — Datos**

Viga continua de 5,00 m de luz entre ejes de columnas, que recibe losas de 5,00 m a ambos lados.

**B.2 — Predimensionado**
```
h ≈ L/11 = 5000/11 = 455 mm   →  adoptar h = 50 cm
b ≈ h/2 = 25 cm               →  adoptar b = 25 cm  (coincide con el muro)
```
Verificación con la Tabla 9.5.a) (viga con ambos extremos continuos): `L/21 = 5000/21 = 238 mm`. Nuestro h = 500 mm está muy por encima. ✓ (Pero la tabla no aplica porque soporta tabiques; el criterio L/11 es el correcto.)

**B.3 — Cargas sobre la viga**

Ancho tributario: 2,50 m a cada lado = **5,00 m** total.

| Concepto | Cálculo | kN/m |
|---|---|---|
| Reacción de las losas (D) | 7,01 kN/m² × 5,00 m | 35,05 |
| Reacción de las losas (L) | 2,00 kN/m² × 5,00 m | 10,00 |
| Peso propio de la viga (bajo losa: 0,50 − 0,15 = 0,35 m) | 25 × 0,25 × 0,35 | 2,19 |
| Muro de ladrillo hueco 18 cm sobre la viga, h = 2,45 m | 12 × 0,18 × 2,45 | 5,29 |
| **D total** | | **42,53** |
| **L total** | | **10,00** |

**Combinación mayorada:**
```
qu = 1,2 × 42,53 + 1,6 × 10,00 = 51,04 + 16,00 = 67,04 kN/m
```

**B.4 — Momentos (viga continua, coeficientes aproximados del CIRSOC 201 art. 8.3.3 / ACI)**
```
M_tramo  = qu · ℓn² / 16 = 67,04 × 4,75² / 16 = 67,04 × 22,56 / 16 = 94,5 kNm
M_apoyo  = qu · ℓn² / 10 = 67,04 × 22,56 / 10 = 151,3 kNm
V_apoyo  = 1,15 · qu · ℓn / 2 = 1,15 × 67,04 × 4,75 / 2 = 183,1 kN
```

**B.5 — Armadura de tramo (viga T)**

Ancho efectivo del ala:
```
bef ≤ L/4 = 5000/4 = 1250 mm
bef ≤ bw + 16·hf = 250 + 16×150 = 2650 mm
bef ≤ separación entre ejes de vigas = 5000 mm
→  bef = 1250 mm
```

Altura útil (recubrimiento 25 mm sobre estribo ϕ8, barra ϕ16):
```
d = 500 − 25 − 8 − 16/2 = 459 mm
```

Verificación de si el bloque comprimido entra en el ala:
```
As ≈ Mu / (φ·fy·0,95·d) = 94,5e6 / (0,90 × 420 × 0,95 × 459) = 94,5e6 / 164.850 = 573 mm²
a = As·fy / (0,85·f'c·bef) = 573 × 420 / (0,85 × 25 × 1250) = 240.660 / 26.563 = 9,1 mm
```
```
a = 9,1 mm  <  hf = 150 mm      →  El bloque comprimido está dentro del ala. Viga T se comporta como rectangular de ancho bef. ✓
```
Recalculando con brazo real:
```
z = d − a/2 = 459 − 4,5 = 454,5 mm
As = 94,5e6 / (0,90 × 420 × 454,5) = 94,5e6 / 171.800 = 550 mm²
```
**Adoptar 3 ϕ16 = 603 mm²** ✓

Verificación de cuantía mínima:
```
ρ_min = 1,4/420 = 0,00333
As,min = 0,00333 × 250 × 459 = 382 mm²   <  550 mm²  ✓
```

Verificación de εt (ductilidad):
```
c = a/β1 = 9,1/0,85 = 10,7 mm
εt = 0,003 × (d − c)/c = 0,003 × (459 − 10,7)/10,7 = 0,126
```
```
εt = 0,126  >>  0,005      →  sección FUERTEMENTE controlada por tracción, φ = 0,90  ✓
```

**B.6 — Armadura de apoyo (sección rectangular, ala traccionada)**
```
Estimación:  As = 151,3e6 / (0,90 × 420 × 0,90 × 459) = 151,3e6 / 156.100 = 969 mm²
a = 969 × 420 / (0,85 × 25 × 250) = 406.980 / 5.313 = 76,6 mm
z = 459 − 38,3 = 420,7 mm
As = 151,3e6 / (0,90 × 420 × 420,7) = 151,3e6 / 159.020 = 951 mm²
```
**Adoptar 5 ϕ16 = 1005 mm²** ✓ (o 3 ϕ20 = 942 mm², ligeramente insuficiente; 2ϕ20 + 2ϕ16 = 1030 mm² ✓)

Verificación de εt:
```
c = 76,6/0,85 = 90,1 mm
εt = 0,003 × (459 − 90,1)/90,1 = 0,0123
```
```
εt = 0,0123  >  0,005      →  controlada por tracción, φ = 0,90  ✓
```

Cuantía:
```
ρ = 1005 / (250 × 459) = 0,00876     →  en zona económica (0,008-0,015)  ✓
```

**B.7 — Verificación de corte**
```
Vu en la cara del apoyo: 183,1 kN
Vu a distancia d del apoyo: Vu − qu·d = 183,1 − 67,04 × 0,459 = 183,1 − 30,8 = 152,3 kN

φVc = 0,75 × 0,17 × sqrt(25) × 250 × 459 / 1000 = 0,75 × 0,17 × 5 × 114.750/1000
    = 0,75 × 97,5 = 73,2 kN
```
```
Vu = 152,3 kN  >  φVc = 73,2 kN      →  SE REQUIERE ARMADURA DE CORTE
Vs requerido = (Vu − φVc)/φ = (152,3 − 73,2)/0,75 = 105,5 kN
```
Con estribos ϕ8 de dos ramas (Av = 2 × 50,3 = 100,6 mm²):
```
s = Av · fyt · d / Vs = 100,6 × 420 × 459 / 105.500 = 19.394.000 / 105.500 = 184 mm
```
**Adoptar estribos ϕ8 c/15 cm** en los tercios extremos.

Verificación de separación máxima:
```
0,33 · sqrt(f'c) · bw · d = 0,33 × 5 × 250 × 459 / 1000 = 189 kN
Vs = 105,5 kN  <  189 kN   →  s_max = d/2 = 229 mm  ≤ 600 mm     ✓  (adoptamos 150 mm)
```

En el tercio central:
```
Vu(centro) ≈ 0  →  usar estribos mínimos:  ϕ8 c/22 cm  (adoptar c/20 cm)
```

**B.8 — Verificación de flecha**
```
Ig = 250 × 500³/12 = 2604 × 10⁶ mm⁴   (sección rectangular; con el ala es mayor)
Mcr = 3,10 × 2604e6 / 250 = 32,3 × 10⁶ N·mm = 32,3 kNm

M_serv,tramo = (42,53 + 10,00) × 22,56/16 = 52,53 × 1,41 = 74,1 kNm
```
```
M_serv = 74,1 kNm  >  Mcr = 32,3 kNm      →  LA VIGA FISURA. Hay que usar Ie
```

Momento de inercia efectivo (Branson):
```
Ie = (Mcr/Ma)³ · Ig + [1 − (Mcr/Ma)³] · Icr

(Mcr/Ma)³ = (32,3/74,1)³ = (0,436)³ = 0,0829

Icr (estimado para ρ = 0,0048 en el tramo, con ala):
Icr ≈ 0,35 · Ig ≈ 911 × 10⁶ mm⁴   [PD, estimación; el cálculo riguroso requiere la sección fisurada transformada]

Ie = 0,0829 × 2604e6 + 0,9171 × 911e6 = 216e6 + 836e6 = 1052 × 10⁶ mm⁴
```

Flecha instantánea (viga continua, coeficiente 1/384 con extremos continuos y ~5/384 en el tramo con apoyos parciales; adoptamos el conservador de viga con un extremo continuo, coef. ≈ 1/185):
```
δ_inst = q · ℓ⁴ / (185 · Ec · Ie)
       = 52,53 N/mm × 4750⁴ / (185 × 23.500 × 1052e6)
       = 52,53 × 5,09e14 / (4,574e15)
       = 5,85 mm
```

Flecha diferida (sin armadura de compresión, λΔ = 2,0):
```
δ_D_inst = 5,85 × 42,53/52,53 = 4,74 mm
δ_diferida = 2,0 × 4,74 = 9,48 mm
δ_total_post-tabiques = 9,48 + 5,85 × 10,00/52,53 = 9,48 + 1,11 = 10,59 mm
```

**Límite L/480:**
```
δ_adm = 4750/480 = 9,90 mm

δ = 10,59 mm  >  9,90 mm      ✗ NO VERIFICA (por poco)
```

**Solución 1 — agregar armadura de compresión.** Con 2ϕ12 en la cara comprimida del tramo:
```
ρ' = 226 / (250 × 459) = 0,00197
λΔ = 2,0 / (1 + 50 × 0,00197) = 2,0/1,0985 = 1,82
δ_diferida = 1,82 × 4,74 = 8,63 mm
δ_total = 8,63 + 1,11 = 9,74 mm  <  9,90 mm      ✓ VERIFICA (justo)
```

**Solución 2 — aumentar el canto a h = 55 cm.**
```
Ig = 250 × 550³/12 = 3466e6 mm⁴  (+33%)
d = 509 mm
δ ≈ 10,59 × (500/550)³ × ajuste ≈ 10,59 × 0,751 ≈ 7,95 mm   ✓ VERIFICA CON MARGEN
```

**Solución 3 — contraflecha de ejecución.** Dar una contraflecha de 10 mm en el encofrado. **Es la solución más barata**, pero sólo compensa la flecha, no reduce la fisuración ni el efecto sobre los tabiques por deformación relativa.

**Recomendación: Solución 2 (h = 55 cm) o combinación de 1 + 3.** La solución 1 sola queda demasiado justa para un edificio real, donde las cargas de tabiquería tienen incertidumbre.

### B.9 — Resumen del ejemplo 2

| Elemento | Dimensión | Armadura |
|---|---|---|
| **Losa maciza 5,00 × 5,00 m** | **h = 15 cm** | Tramo: ϕ8 c/18 en ambas direcciones. Negativos: ϕ10 c/16 |
| **Viga 5,00 m** | **b×h = 25 × 55 cm** | Tramo: 3ϕ16 inferior + 2ϕ12 superior. Apoyos: 5ϕ16 superior. Estribos ϕ8 c/15 en tercios extremos, c/20 en el central |

**Lo que gobernó cada elemento:**

| Elemento | Verificación que gobernó |
|---|---|
| Losa | **Cuantía mínima de retracción (0,0018)** — no la flexión |
| Viga: canto | **FLECHA DIFERIDA (L/480)** — no la resistencia |
| Viga: armadura de tramo | Flexión (con margen enorme de ductilidad) |
| Viga: estribos | Corte |

> **Esta es la lección más útil del ejemplo:** en entrepisos de vivienda de luces normales, **la resistencia casi nunca gobierna**. Gobiernan la **cuantía mínima** en losas y la **flecha diferida** en vigas. Por eso un calculista experimentado predimensiona por flecha (L/11 en vigas) y no por resistencia — y por eso los programas que sólo verifican ELU te dejan pasar vigas que después se van a flechar.

---
---

# 6. SISTEMA SISMORRESISTENTE Y ESTABILIDAD LATERAL

En Santa Rosa (zona sísmica 0), este capítulo trata fundamentalmente de **estabilidad frente al viento**, pero los criterios de configuración son idénticos y todos se toman prestados de la ingeniería sismorresistente, porque es la disciplina que los desarrolló.

## 6.1 Los tres sistemas básicos

### 6.1.1 Pórticos (*moment frames*)

```
   ═══╤═══════╤═══════╤═══     Vigas y columnas rígidamente unidas.
      │       │       │        La estabilidad lateral proviene de la
   ═══╪═══════╪═══════╪═══     rigidez a flexión de los nudos.
      │       │       │
   ═══╪═══════╪═══════╪═══     Deformada: "corte" — la deriva es
      │       │       │        aproximadamente uniforme en altura.
   ▓▓▓▓▓   ▓▓▓▓▓   ▓▓▓▓▓
```

| Ventaja | Desventaja |
|---|---|
| **Máxima libertad arquitectónica** (sin muros que estorben) | **Flexible** — derivas grandes |
| Alta ductilidad si está bien detallado (R = 7) | Exige vigas de canto (afecta altura libre) |
| Redundante: muchas rótulas antes del colapso | Columnas grandes en plantas bajas |
| Buena para plantas que cambian de uso | El nudo viga-columna es un punto crítico de detallado |
| — | **Efectos P-Δ importantes** en altura |

**Límite práctico [PD]: pórticos solos hasta ~8-10 plantas.** Por encima, las derivas y P-Δ obligan a secciones antieconómicas.

**Filosofía obligatoria: "COLUMNA FUERTE — VIGA DÉBIL".** La suma de momentos resistentes de las columnas que concurren a un nudo debe superar la de las vigas (típicamente ΣMc ≥ 1,2·ΣMb [VER coeficiente exacto en INPRES-CIRSOC 103 Parte II]). Si falla la columna antes que la viga, se forma un mecanismo de piso y el edificio colapsa.

### 6.1.2 Tabiques (*shear walls*)

```
   ═══╤═══════════════════╤═══   Muros de hormigón armado
      │  ███████████████  │      trabajando como voladizos
   ═══╪══█████████████████╪═══   empotrados en la fundación.
      │  ███████████████  │
   ═══╪══█████████████████╪═══   Deformada: "flexión" — la deriva
      │  ███████████████  │      crece con la altura.
   ▓▓▓▓▓▓█████████████▓▓▓▓▓▓
```

| Ventaja | Desventaja |
|---|---|
| **Muy rígidos** — derivas mínimas | **Restricción arquitectónica fuerte** |
| Poco P-Δ | Concentran carga → fundación pesada |
| Protegen los elementos no estructurales | Menos redundantes |
| Aprovechan el núcleo de ascensores/escalera | Momento de vuelco importante en la base |
| Simplifican columnas (indesplazables) | Requieren continuidad hasta la fundación |

### 6.1.3 Sistema dual (pórtico + tabique)

```
   ═══╤═══════╤═══█████╤═══════╤═══
      │       │   █████│       │      Los tabiques toman la mayor parte
   ═══╪═══════╪═══█████╪═══════╪═══   del corte en las plantas bajas;
      │       │   █████│       │      los pórticos, en las altas.
   ═══╪═══════╪═══█████╪═══════╪═══   Interacción beneficiosa: la
      │       │   █████│       │      deformada resultante es más
   ▓▓▓▓▓   ▓▓▓▓▓ █████ ▓▓▓▓▓ ▓▓▓▓▓   uniforme que la de cualquiera solo.
```

**Es la solución óptima para PB+9 y es la que recomiendo por defecto.**

**[RC]** Según la Tabla 5.1 del INPRES-CIRSOC 103: **Sistema dual Pórtico-Tabique: R = 6, Cd = 5, Ωo = 2,5**.

**[VER]** el requisito de que los pórticos sean capaces de resistir al menos un porcentaje del corte basal (en el 103 Parte IV para acero se menciona "al menos el 25% del corte basal" para sistemas duales; verificar el requisito equivalente para hormigón en la Parte II).

**La magia del sistema dual:** el tabique se deforma por flexión (deriva creciente con la altura) y el pórtico por corte (deriva uniforme). Cuando se los vincula por los diafragmas de piso, **se contienen mutuamente**: abajo el tabique frena al pórtico, arriba el pórtico frena al tabique. El resultado es un edificio mucho más rígido que la suma de las partes.

### 6.1.4 Tabla comparativa

| Sistema | R | Rigidez relativa | Libertad arquitectónica | Costo estructural | Altura práctica |
|---|---|---|---|---|---|
| Pórtico de HºAº dúctil | **7** | Baja | **Máxima** | Medio | ≤ 10 plantas |
| Pórtico de ductilidad limitada | 3,5 | Baja | Máxima | Bajo | ≤ 5 plantas |
| Tabiques aislados | 5 – 7 | **Muy alta** | Baja | Medio-alto | 25+ plantas |
| **Sistema dual** | **6** | **Alta** | **Media-alta** | **Medio** | **20+ plantas** |
| Columnas en voladizo | 2,5 | Muy baja | Máxima | Alto | 1-2 plantas |
| Pórtico de acero no arriostrado especial | 7 | Baja | Máxima | Alto | ≤ 15 plantas |
| Pórtico de acero arriostrado excéntricamente | 7 | Alta | Media | Alto | 20+ plantas |
| Mampostería encadenada armada | 3,5 | Alta | Muy baja | Bajo | ≤ 3-4 plantas |
| Mampostería sin encadenados | **1,5** | Alta | Muy baja | Muy bajo | **1 planta** |

## 6.2 Núcleo de ascensores y escaleras

**El núcleo es el mejor tabique del edificio y es gratis** — la arquitectura ya lo pide.

### 6.2.1 Aprovecharlo bien

| Aspecto | Recomendación |
|---|---|
| **Forma** | Núcleo cerrado (tipo cajón) es muchísimo más rígido a torsión que uno abierto en U o C. **Cerralo con dinteles altos sobre las puertas** |
| **Espesor de muros** | 20 – 30 cm en PB+9 |
| **Continuidad** | **De la fundación a la cubierta, sin interrupciones.** Ni una puerta de más en el lugar equivocado |
| **Aberturas** | Alinearlas verticalmente. Aberturas desalineadas crean vigas de acople débiles y concentraciones |
| **Vigas de acople (dinteles)** | Sobre las puertas del núcleo. Su altura define cuánto acoplan los dos "brazos" del núcleo. Dinteles altos = núcleo casi monolítico. Armarlos con **armadura diagonal** si son cortos y muy solicitados |
| **Elementos de borde** | Confinar los extremos y las intersecciones con estribos cerrados |
| **Fundación** | El núcleo baja **toda la carga vertical de la escalera y el ascensor + el momento de vuelco**. Requiere fundación específica, más profunda o con más pilotes |

### 6.2.2 El problema del núcleo excéntrico

En lote entre medianeras, el núcleo suele ir contra una medianera → **el centro de rigidez se corre hacia esa medianera** → torsión importante.

**Soluciones:**
1. **Tabiques adicionales en el lado opuesto** — la mejor.
2. Convertir columnas de la fachada opuesta en **pantallas** (columnas alargadas, 25×120 cm por ejemplo), que son tabiques cortos.
3. Reforzar los pórticos del lado opuesto (menos eficiente).
4. Aceptar la torsión y verificar Tabla 2.3 línea 1a: `δmk/δbk ≤ 1,2`.

### 6.2.3 Escaleras — el elemento traicionero

**Una escalera de hormigón conectada rígidamente a dos niveles es una diagonal estructural.** Rigidiza el vano donde está y atrae fuerza lateral que el modelo no previó. Consecuencias en sismo real (documentadas en Chile 2010 y en Nueva Zelanda): rotura de escaleras, pérdida de la vía de evacuación.

| Solución | Descripción |
|---|---|
| **Modelarla como diagonal** | Incluirla en el modelo y diseñar el vano en consecuencia |
| **Desvincularla** | Apoyo deslizante en un extremo (neopreno + junta), de modo que no trabaje como diagonal. **Es la práctica moderna** |
| **Escalera aislada del núcleo** | Con junta perimetral |

**En zona 0 con viento como acción dominante esto es menos crítico, pero la escalera igual rigidiza y hay que decidir conscientemente qué hacés con ella.**

## 6.3 Irregularidades en planta

Ver la Tabla 2.3 verificada en §2.6.8. Catálogo gráfico:

### 6.3.1 Irregularidad torsional

```
  CM = centro de masa     CR = centro de rigidez
  
  ❌                              ✓
  +-------------------+          +-------------------+
  |███                |          |███             ███|
  |███  CR      CM    |          |      CR=CM        |
  |███   ↑       ↑    |          |       ↑           |
  |███   |   e   |    |          |                   |
  |███   +-------+    |          |███             ███|
  +-------------------+          +-------------------+
  Momento torsor = V·e            Sin torsión
```

**Criterio [RC]:** `δmk/δbk ≤ 1,2` (regular), ≤ 1,4 (irregularidad media), > 1,4 (extrema → rediseñar).

**Criterio complementario [PD]:** excentricidad `e ≤ 0,10 · B`.

**Excentricidad accidental:** aun con CR = CM hay que considerar una excentricidad accidental (típicamente **±5% de la dimensión perpendicular** [VER valor exacto en el 103]) por incertidumbre en la distribución de masas.

### 6.3.2 Esquinas entrantes (plantas en L, T, U, H)

```
  ❌  Planta en L                    ✓  Dos bloques con junta
  +-----------+                      +-----------+ | +-----+
  |           |                      |           | | |     |
  |           |                      |           | | |     |
  |     +-----+                      |     +-----+ | +-----+
  |     |                            |     |       ‖ junta
  |     |  ← concentración de        |     |
  +-----+     tensiones y torsión    +-----+
```

**[RC] Tabla 2.3, línea 4a:** regular si la proyección se extiende más allá de la esquina entrante **menos del 15%** de la dimensión de la planta en esa dirección.

**Solución:** **junta sísmica/estructural** dividiendo la planta en bloques regulares. Es más barato que resolver los esfuerzos de la esquina entrante.

### 6.3.3 Diafragma discontinuo

Grandes aberturas en la losa (patios de luz, vacíos de escalera, atrios) que interrumpen la transferencia de fuerzas horizontales.

**Verificación:** la losa es el diafragma que reparte la fuerza lateral entre los elementos verticales. Si tiene un vacío del 40% del área, **no puede repartir**. Hay que:
- Diseñar **colectores y cordones** (vigas perimetrales del vacío) que rodeen la abertura y transfieran.
- Verificar la losa como diafragma (art. 9.1 del INPRES-CIRSOC 103, verificado en el índice: *"9.1.1 Solicitaciones en el diafragma debidas a la acción sísmica; 9.1.2 Verificación de conexiones y colectores"*).
- Considerar **diafragma flexible** en el modelo si la abertura es grande (los modelos por defecto asumen diafragma rígido).

### 6.3.4 Elementos resistentes no ortogonales

**[RC] Tabla 2.3, línea 3a:** regular si los elementos son perpendiculares o con doble simetría.

Plantas en lotes irregulares con ejes girados exigen análisis con las direcciones principales del sistema resistente, no con los ejes del terreno.

## 6.4 Irregularidades en elevación

Ver Tabla 2.4 verificada en §2.6.8.

### 6.4.1 PISO BLANDO / PISO DÉBIL — la irregularidad letal

```
  ❌ PISO BLANDO                       ✓ SOLUCIÓN
  
  ═══╤══█████═══╤══█████═══╤═══      ═══╤══█████═══╤══█████═══╤═══
     │  █████   │  █████   │            │  █████   │  █████   │
  ═══╪══█████═══╪══█████═══╪═══      ═══╪══█████═══╪══█████═══╪═══
     │  █████   │  █████   │            │  █████   │  █████   │
  ═══╪══█████═══╪══█████═══╪═══      ═══╪══█████═══╪══█████═══╪═══
     │          │          │            │  █████   │  █████   │
     │  PB LIBRE (local /  │            │  █████   │  █████   │
     │   cochera)          │            │  ↓ tabiques continuos hasta
  ▓▓▓▓▓      ▓▓▓▓▓     ▓▓▓▓▓          ▓▓▓▓▓▓▓▓▓  la fundación ▓▓▓▓
  
  Rigidez PB << rigidez 1er piso      Rigidez continua
  → toda la demanda se concentra
    en PB → mecanismo de piso
```

**[RC] Tabla 2.4 línea 5b:** "piso débil" cuando la resistencia lateral de un nivel **no supera el 80%** de la del nivel superior.
**[RC] Tabla 2.4 líneas 1b/1c:** irregularidad de rigidez media (Kk > 1,4·Kk+1) o extrema (Kk > 1,7·Kk+1).

**Esta configuración — planta baja libre para local o cochera, plantas altas con muros de mampostería entre columnas — es la tipología dominante del edificio urbano argentino y es la que más edificios ha derribado en terremotos en todo el mundo.**

**Soluciones:**
1. **Tabiques de hormigón continuos desde la fundación** (la única realmente buena).
2. Pórticos de PB significativamente más rígidos (columnas mucho mayores, vigas de gran canto).
3. Diagonales de acero en PB.
4. **Aislar la mampostería de los pórticos superiores** (juntas perimetrales de 2 cm rellenas con material compresible) para que la rigidez sea uniforme. Barato y muy efectivo — pero hay que ejecutarlo bien y sellarlo.

### 6.4.2 Columna corta

```
  ❌                              ✓
     │                              │
     │  ┌──────────┐                │
     │  │ mampostería                │  Junta de 2-3 cm
  h  │  │ (antepecho)                │  entre antepecho
  lib│  │          │                 │  y columna
     │  └──────────┘                 │
     │  ← h_libre reducida           │  ← h_libre = h completa
  ═══╧═══                        ═══╧═══
  
  V = 2M/h_libre  →  el corte se     El corte queda en el valor
  MULTIPLICA al reducirse h          previsto
```

**El mecanismo:** un antepecho de mampostería que abraza parcialmente la columna reduce su altura libre. Como el corte va con `V = 2M/h`, reducir h a la mitad **duplica el corte**. La columna falla por corte (frágil) en lugar de por flexión (dúctil).

**Es la falla más fotografiada de todos los terremotos.** Escuelas con ventanas altas, edificios con antepechos, rampas de cochera con columnas de distinta altura.

**Soluciones:** junta perimetral entre mampostería y columna, o diseñar la columna para el corte real de la altura reducida, con estribado denso en toda la altura.

### 6.4.3 Retranqueos (*setbacks*) y masas irregulares

**[RC] Tabla 2.4:**
- Línea 2: masas de cada nivel varían **< 30%** respecto de los adyacentes (se excluyen techos livianos < 1,5 kN/m²).
- Línea 3: dimensión horizontal del sistema resistente varía **< 30%** respecto de los adyacentes.
- Línea 4a: elementos verticales continuos, o retranqueos en su plano **inferiores a la longitud del elemento**; dimensiones constantes o **crecientes hacia abajo**.

**El tanque de agua y la sala de máquinas** son el caso típico de masa irregular en la cubierta. Aunque su masa sea pequeña, está en el extremo del voladizo vertical y tiene efecto de "látigo" (amplificación dinámica). **INPRES-CIRSOC 103 Cap. 10** trata partes de la construcción y componentes no estructurales, con **factor de amplificación dinámica y factor de magnificación en altura** (art. 10.2.2 y 10.2.4).

## 6.5 Efecto P-Δ

Ver §2.6.11 para la formulación reglamentaria verificada.

### 6.5.1 El mecanismo

```
        P                    P
        ↓                    ↓
        │                  ╱ │
        │                ╱   │  Δ
        │      →       ╱     │
        │            ╱       │
     ═══╧═══      ═══╧═══
     
   Momento de 1er orden: M1 = V·h
   Momento adicional:    M2 = P·Δ
   Momento total:        M = V·h + P·Δ
   
   Pero Δ crece por M2 → que aumenta M → que aumenta Δ...
   Es un proceso iterativo que puede DIVERGIR.
```

### 6.5.2 Reglas prácticas

| CE (coeficiente de estabilidad) | Acción |
|---|---|
| **CE < 0,10** | Se pueden despreciar los efectos P-Δ |
| **0,10 ≤ CE ≤ CE_MAX** | Amplificar por `1/(1−CE)`, o análisis de segundo orden |
| **CE > CE_MAX = 0,5/(β·Cd) ≤ 0,25** | **ESTRUCTURA POTENCIALMENTE INESTABLE — REDISEÑAR** |

**[PD] Cómo evitar el problema de raíz:** poner tabiques. Un edificio con núcleo rígido tiene derivas pequeñas → θsk pequeño → CE pequeño → P-Δ despreciable. **Un edificio de pórticos flexibles en 10 plantas suele estar en la zona de CE > 0,10.**

**En el ejemplo del §2.5.13:** con viento y sistema dual bien dimensionado, la deriva de servicio sería del orden de H/500 = 60 mm en 30 m, es decir θ ≈ 0,002 por piso. Con Pk en el nivel medio ≈ 15.000 kN y Vk ≈ 500 kN:
```
CE = 15.000 × 0,002 / (500 × 2,95 × 5) = 30 / 7375 = 0,004
```
**Absolutamente despreciable.** Con pórticos solos y deriva 5 veces mayor, CE = 0,02 — todavía despreciable. **En zona 0 con viento, P-Δ rara vez es un problema.** Sí lo es en zonas sísmicas 3-4.

## 6.6 Distorsión de piso admisible

Recopilación:

| Criterio | Fuente | Valor |
|---|---|---|
| **Sismo — grupo Ao/A, condición D** | **[RC] Tabla 6.4 del 103** | **0,010** |
| **Sismo — grupo Ao/A, condición ND** | **[RC] Tabla 6.4** | **0,015** |
| **Sismo — grupo B, condición D** | **[RC] Tabla 6.4** | **0,015** |
| **Sismo — grupo B, condición ND** | **[RC] Tabla 6.4** | **0,025** |
| Sismo — grupo C | [RC] | No exigible |
| **Viento de servicio — deriva de piso** | [PD] práctica internacional | **h/400 a h/500** |
| **Viento de servicio — desplazamiento total** | [PD] | **H/500** |
| **Confort (aceleración pico, vivienda, recurrencia 10 años)** | [PD, ISO 10137] | **15 – 25 milli-g** |

**Condición D vs. ND (definición verificada del reglamento):**
- **Condición D:** existen elementos no estructurales que **pueden ser dañados** por las deformaciones impuestas por la estructura.
- **Condición ND:** los elementos no estructurales están vinculados a la estructura **de forma que no sufran daños** por las deformaciones de ésta.

> **La condición ND se compra con detalles constructivos**, no con estructura: juntas entre tabiques y estructura, vidrios con holgura en el marco, cielorrasos con vinculación deslizante. Cuesta poco y te da un límite de deriva **66% mayor**, lo que puede ahorrar mucha estructura. **Pero hay que ejecutarlo y documentarlo.**

## 6.7 Juntas de dilatación y separación entre edificios

### 6.7.1 Los tres tipos de junta — no confundirlos

| Junta | Motivo | Atraviesa la fundación | Ancho típico |
|---|---|---|---|
| **De dilatación / contracción** | Movimientos térmicos y de retracción | **No necesariamente** | 2 – 4 cm |
| **De asentamiento** | Diferencia de carga o de suelo entre partes | **SÍ, siempre** | 3 – 5 cm |
| **Sísmica / estructural** | Separación dinámica de bloques | **No es necesario** (art. 8.4.5.2 verificado) | Según fórmula [8.7]-[8.9] |

### 6.7.2 Juntas de dilatación — separación máxima [PD]

| Situación | Separación máxima entre juntas |
|---|---|
| Estructura de HºAº a la intemperie | **25 – 30 m** |
| Estructura de HºAº protegida (interior) | **30 – 40 m** |
| Estructura de HºAº con hormigón de retracción compensada | 45 – 60 m |
| Estructura metálica a la intemperie | 40 – 60 m |
| Losas de piso sobre terreno (contrapisos) | **4 – 6 m** en ambas direcciones |
| Muros de mampostería a la intemperie | 8 – 12 m |

**Cálculo del movimiento térmico [PD]:**
```
ΔL = α · L · ΔT
α_hormigón = 1,0 × 10⁻⁵ /°C
```
Para L = 30 m y ΔT = 35 °C (amplitud térmica en La Pampa entre invierno y verano en un elemento expuesto):
```
ΔL = 1,0e-5 × 30.000 mm × 35 = 10,5 mm
```
Más retracción de fraguado (~0,3-0,5 ‰ = 9-15 mm en 30 m, parcialmente ocurrida antes de la puesta en servicio).

**Ancho de junta: 2 cm es el mínimo práctico**, 3 cm es lo recomendable para 30 m de bloque.

### 6.7.3 Separación sísmica — [RC] art. 8.4.5.3 (verificado)

```
a)  Yk ≥ 1,05 · dubk          (dubk = desplazamiento último del nivel k)
b)  Yk ≥ 2,5 cm
c)  Para construcciones existentes:  Yke ≥ 2,5 cm
```

**En zona 0**, si el edificio queda eximido, no hay exigencia de separación sísmica; **pero sí sigue habiendo exigencia de separación por dilatación y por asentamiento.**

### 6.7.4 Ejecución de juntas — donde se arruina todo

Una junta mal ejecutada es peor que no tener junta:

| Error | Consecuencia |
|---|---|
| Junta rellena con escombro / mortero | La junta no funciona. Se transmiten esfuerzos. Fisuras |
| Junta que no atraviesa el contrapiso y el piso | El piso se fisura en la línea de la junta |
| Junta sin tapajuntas | Entra agua, se acumula suciedad |
| Junta que no llega hasta la fundación cuando es de asentamiento | No sirve |
| **Junta simple (una sola columna compartida)** | **NO ES UNA JUNTA.** Una junta real requiere **doble columna** o ménsula con apoyo deslizante |
| Instalaciones que cruzan la junta rígidamente | Se rompen |

**Detalle correcto:** doble estructura (dos columnas, dos vigas), separadas por el ancho de junta, con material compresible (poliestireno expandido, lana mineral), sellador elástico y tapajuntas metálico o de PVC que permita el movimiento. Instalaciones con **liras o juntas flexibles** en el cruce.

## 6.8 Diafragmas de piso

La losa transfiere las fuerzas horizontales a los elementos verticales. Sin diafragma no hay sistema.

| Aspecto | Requisito |
|---|---|
| **Rigidez** | Diafragma rígido si la deformación en su plano es << que la de los elementos verticales. **Losa maciza de HºAº = rígido** |
| Diafragma flexible | Losas de viguetas sin capa de compresión adecuada, entrepisos de madera, chapas colaborantes sin conectores. **Requiere modelo con diafragma flexible** |
| **Capa de compresión mínima sobre viguetas para diafragma** | **5 cm con malla** [PD; verificar] |
| **Colectores** | Elementos (vigas, franjas de losa armadas) que recolectan la fuerza del diafragma y la entregan al tabique. Los tabiques cortos requieren colectores largos |
| **Cordones (*chords*)** | Armadura en el perímetro del diafragma que toma la tracción/compresión de la "viga" que es el diafragma |
| **[RC]** | INPRES-CIRSOC 103 art. 9.1: solicitaciones en el diafragma y verificación de conexiones y colectores |

**Error frecuente:** un tabique de 4 m de largo en una planta de 20 m. La losa tiene que "traer" la fuerza de toda la planta y meterla en esos 4 m. La tensión de corte en la interfaz losa-tabique es enorme. **Hay que armar el colector explícitamente** — no aparece solo.

---
---

# 7. ALTERNATIVAS ESTRUCTURALES

## 7.1 Tabla comparativa general

| Sistema | Luz máxima económica | Costo relativo estructura | Plazo relativo | Altura práctica | Peso propio (kN/m²) |
|---|---|---|---|---|---|
| **Mampostería portante encadenada** | 4 – 5 m | **0,60** | 1,00 | **3 pisos / 10 m** | 6 – 9 |
| **HºAº in situ — losa de viguetas** | 5 – 7 m | **1,00** (referencia) | **1,00** | Sin límite práctico | 5 – 7 |
| **HºAº in situ — losa maciza + vigas** | 6 – 8 m | 1,10 | 1,10 | Sin límite | 6 – 8 |
| **HºAº — losa plana sin vigas** | 6 – 9 m | 1,15 | 0,90 | 20+ plantas | 7 – 9 |
| **HºAº — losa casetonada** | 10 – 14 m | 1,30 | 1,20 | 20+ plantas | 6 – 8 |
| **HºAº postesado** | 10 – 16 m | 1,25 | 0,85 | 40+ plantas | 5 – 7 |
| **Acero + losa colaborante** | 8 – 15 m | 1,50 – 1,90 | **0,60** | 40+ plantas | **3 – 4,5** |
| **Prefabricado de hormigón** | 8 – 16 m | 1,20 | **0,55** | 10 – 15 plantas | 5 – 7 |
| **Mixto (acero-hormigón)** | 10 – 18 m | 1,60 | 0,70 | 40+ plantas | 4 – 6 |
| **Steel framing** | 4 – 6 m | 0,90 – 1,20 | **0,50** | **2 – 3 plantas** | **1,0 – 1,8** |
| **Madera (CIRSOC 601)** | 4 – 8 m | 1,00 – 1,40 | 0,60 | 3 – 5 plantas | 1,5 – 3 |

> **Sobre los costos relativos [PD]:** son órdenes de magnitud para el **costo de la estructura sola**, no del edificio. Varían enormemente con la escala, la disponibilidad de mano de obra local y el precio del acero. En La Pampa, la mano de obra de hormigón es abundante y la de estructura metálica de calidad es más escasa y cara — eso empuja los ratios hacia arriba en las columnas de acero.

## 7.2 Acero (CIRSOC 301-2018)

### 7.2.1 Perfiles

| Tipo | Descripción | Uso |
|---|---|---|
| **Laminados en caliente** | IPN, IPB (HEB), IPE, UPN, ángulos, tubos estructurales | Lo estándar. Disponibilidad variable en el mercado argentino |
| **Soldados (armados)** | Perfiles I y H armados con chapas soldadas | Cuando no hay laminado del tamaño necesario, o para secciones optimizadas (alma esbelta, alas anchas) |
| **Tubos estructurales** | Circulares, cuadrados, rectangulares | Columnas (excelente comportamiento a pandeo en las dos direcciones), reticulados vistos |
| **Conformados en frío** | **CIRSOC 303-2009** — secciones abiertas de chapa de hasta **25,4 mm** de espesor | Correas, steel framing, estructuras livianas |

### 7.2.2 CIRSOC 301-2018 — puntos clave

- Basado en la **AISC 360** (LRFD y ASD).
- Aplica **con cargas predominantemente estáticas** (art. A.1).
- Las **acciones sísmicas** se remiten a **INPRES-CIRSOC 103 Parte IV** (art. A.3).
- Se complementa con **CIRSOC 302** (estabilidad del equilibrio: pandeo global, lateral-torsional, abollamiento) y **CIRSOC 304** (soldadura).

### 7.2.3 Predimensionado de acero [PD]

| Elemento | Regla |
|---|---|
| **Viga de entrepiso simplemente apoyada** | h ≈ L/20 a L/22 |
| **Viga de entrepiso continua** | h ≈ L/24 a L/28 |
| **Viga mixta (con losa colaborante)** | h ≈ L/22 a L/25 (el perfil solo) |
| **Reticulado de cubierta** | h ≈ L/12 a L/15 |
| **Correa de cubierta** | h ≈ L/40 a L/50 |
| **Columna de edificio** | A ≈ N/(0,5·fy) para predimensionar (deja margen para pandeo) |
| **Flecha admisible viga de entrepiso** | L/360 (L) y L/240 (D+L) [PD; verificar exigencia] |
| **Consumo de acero, entrepiso de oficinas** | **35 – 55 kg/m²** [PD] |
| **Consumo de acero, entrepiso industrial** | 45 – 80 kg/m² |
| **Consumo de acero, cubierta liviana de galpón** | 20 – 35 kg/m² |

### 7.2.4 Losa colaborante (steel deck)

```
   ┌─────────────────────────────────────┐
   │ hormigón + malla                    │  ← h_total 10-15 cm
   ├──╥──────╥──────╥──────╥──────╥──────┤
   │  ║      ║      ║      ║      ║      │  ← chapa colaborante
   └──╨──────╨──────╨──────╨──────╨──────┘     0,76 - 1,20 mm
        ↑ conectores de corte (pernos Nelson)
   ═════════════════════════════════════════   ← viga metálica
```

| Parámetro | Valor típico [PD] |
|---|---|
| Espesor de chapa | 0,76 / 0,90 / 1,00 / 1,20 mm |
| Altura del nervio | 38 / 50 / 76 mm |
| **Espesor total de losa** | **10 – 15 cm** |
| **Luz sin apuntalar** | **2,0 – 3,5 m** según chapa y espesor |
| **Luz con apuntalamiento intermedio** | 3,5 – 5,0 m |
| **Peso propio de la losa** | **1,8 – 2,8 kN/m²** ← **menos de la mitad de una losa maciza** |
| Malla de reparto | ϕ4,2 – 6 c/15-20 cm |
| Conectores de corte | Pernos ϕ16-19 mm soldados a través de la chapa |
| Resistencia al fuego | Requiere protección de la chapa y de las vigas, o armadura adicional en los nervios |

**Ventajas decisivas:** la chapa es **encofrado + armadura positiva + plataforma de trabajo**. Elimina el encofrado de fondo, permite trabajar en varias plantas a la vez, y reduce el peso propio a la mitad → **fundaciones más chicas**.

**Desventaja:** requiere estructura metálica (o al menos vigas metálicas), montaje con grúa, y control de la soldadura de conectores.

### 7.2.5 Protección contra la corrosión y el fuego

| Aspecto | Solución |
|---|---|
| **Corrosión — interior seco** | Fondo antióxido + esmalte sintético, o pintura epoxi |
| **Corrosión — exterior** | Sistema epoxi-poliuretano (3 capas, 200-280 μm) o **galvanizado en caliente** (el mejor: 60-100 μm de zinc, 30-50 años de vida) |
| **Fuego** | **Es el gran costo oculto del acero.** El acero pierde ~50% de su resistencia a 550 °C. Opciones: pintura intumescente (F30-F120, cara), mortero proyectado (barato, feo), encajonado con placas de yeso RF, o **hormigonado parcial** (perfiles rellenos/embebidos) |
| **[VER]** | La exigencia de resistencia al fuego (F30/F60/F120/F180) la fija el **código de edificación municipal** según destino, superficie y altura. **Consultar en Santa Rosa.** El futuro **CIRSOC 110** tratará la acción del fuego |

## 7.3 Estructura mixta (acero-hormigón)

| Elemento mixto | Descripción | Beneficio |
|---|---|---|
| **Viga mixta** | Perfil de acero + losa de hormigón conectada con pernos | Aumento de rigidez del **40-100%** y de resistencia del 30-60% respecto del perfil solo |
| **Columna mixta rellena** | Tubo estructural relleno de hormigón | El tubo confina el hormigón (mayor f'c efectivo) y el hormigón evita la abolladura del tubo. **Excelente relación resistencia/tamaño** |
| **Columna mixta embebida** | Perfil H embebido en hormigón armado | Protección al fuego incorporada, muy alta capacidad |
| **Losa mixta** | Steel deck (§7.2.4) | — |

**Cuándo conviene [PD]:** edificios de 8-20 plantas donde se busca velocidad de obra y luces de 8-12 m. En Santa Rosa el mercado no está muy desarrollado; requiere taller metalúrgico de calidad y montaje con grúa.

## 7.4 Prefabricado de hormigón

| Elemento | Luces | Uso |
|---|---|---|
| **Vigueta pretensada** | 3 – 7 m | Vivienda (§5.1.7) |
| **Losa alveolar (*hollow core*)** | 6 – 16 m | Entrepisos, cubiertas, muros |
| **Doble T (TT)** | 10 – 25 m | Cubiertas de naves, estacionamientos |
| **Viga pretensada I o T invertida** | 8 – 25 m | Naves, puentes |
| **Columna prefabricada** | Hasta 3-4 plantas en una pieza | Naves industriales, edificios |
| **Panel de fachada (arquitectónico o portante)** | — | Cerramiento y/o estructura |

**Ventajas:** control de calidad de fábrica, velocidad de montaje (una nave de 2000 m² se monta en 2-3 semanas), superficies terminadas, menor desperdicio, obra limpia.

**Desventajas y advertencias [FIRMA]:**
1. **Las uniones son el punto crítico.** Un edificio prefabricado es tan bueno como sus conexiones. Requieren diseño específico y verificación de tolerancias.
2. **Comportamiento frente a acciones laterales:** un prefabricado con uniones articuladas no tiene pórticos. Necesita **tabiques o arriostramientos explícitos**.
3. **Diafragma:** los elementos prefabricados yuxtapuestos no forman diafragma por sí solos. Requieren **capa de compresión armada** (5 cm mínimo) o conexiones de corte entre piezas.
4. **Tolerancias:** el prefabricado no perdona. Los ejes de fundación tienen que estar en ±1 cm.
5. **Logística:** transporte de piezas grandes desde Buenos Aires, Córdoba o Rosario a Santa Rosa es un costo y una restricción de dimensiones (largo máximo por ruta).

## 7.5 Mampostería portante

### 7.5.1 Los dos reglamentos

| Reglamento | Alcance | Método |
|---|---|---|
| **CIRSOC 501-2007** | Estructuras de mampostería en general, **cálculo** | Tensiones admisibles y/o resistencia [VER] |
| **CIRSOC 501-E-2023** | **"Reglamento Empírico para Construcciones de Mampostería de Bajo Compromiso Estructural"** | **Tensiones admisibles, diseño simplificado sin cálculo detallado** |
| **INPRES-CIRSOC 103 Parte III-2018** | Mampostería en zonas sísmicas 1, 2, 3 y 4 | — |

### 7.5.2 **[RC] Limitaciones del CIRSOC 501-E (verificadas, transcripción textual)**

**Art. 1.1 — Campo de validez:** *"Todo lo establecido en este Reglamento es válido sólo para construcciones ejecutadas con **bloques huecos cerámicos, bloques huecos de hormigón y ladrillos cerámicos macizos**."*

**Art. 1.2.1 — Viento:** *"Los requerimientos de este Reglamento **no son de aplicación** para el diseño o construcción de mampostería para edificios... que se ubiquen en zonas donde la **velocidad básica del viento supere los 55 m/seg**."*
> **Santa Rosa: V = 50 m/s < 55 m/s.** ✓ El 501-E **es aplicable** en Santa Rosa. (Bahía Blanca con 55 m/s está justo en el límite; Comodoro con 67,5 m/s queda fuera.)

**Art. 1.2.2 — Otras cargas horizontales:** *"Las prescripciones contenidas en este Reglamento son de aplicación en la **zona sísmica 0** (baja sismicidad) del territorio nacional. Para las otras zonas sísmicas (1; 2; 3 y 4) se deberá aplicar lo establecido en el Reglamento **INPRES-CIRSOC 103 - Parte III - Construcciones de mampostería – 2018**."*
> **Santa Rosa: Zona 0.** ✓ Aplicable.

**Art. 1.2.3.2 — Nieve:** *"Solamente será posible su utilización en aquellas zonas donde la 'carga de nieve sobre el nivel del terreno', pg, sea **menor o igual a 0,90 kN/m² (90 kgf/m²)**."*
> **La Pampa: pg = 0,3 kN/m².** ✓ Aplicable.

**Art. 1.2.4 — ALTURA:** *"Los edificios comprendidos en este Reglamento **no podrán tener una altura superior a 10 m o tres pisos**."*
> **Este es EL límite de la mampostería portante empírica en Argentina: 10 m o 3 pisos.**

### 7.5.3 **[RC] Espesores mínimos de muros portantes — Tabla 7.1 del 501-E (verificada, transcripción)**

| Espesor de muros de una hoja de mampuestos macizos o huecos | Altura máxima de planta | Altura máxima del edificio | Distancia máxima entre soportes verticales |
|---|---|---|---|
| **110 a 169 mm** (1) | **2,80 m** | **3,0 m, o piso superior de un edificio de 2 o 3 pisos** | **4,00 m** |
| **170 a 240 mm** | **3,00 m** | **10 m** | **4,50 m** |
| **241 a 300 mm** | **3,50 m** | **10 m** | **6,00 m** |

Notas verificadas:
- (1) No se admite tomado de junta profundo; el tomado de junta deberá ser **al ras**.
- Los muros portantes **no podrán tener un espesor menor que 110 mm** para ladrillos macizos y **120 mm** para ladrillos huecos portantes.
- La **altura máxima de planta** corresponde a la **luz libre interior entre soportes horizontales** (no se tiene en cuenta el espesor de cielorrasos, pisos y contrapisos).
- La **distancia máxima entre soportes verticales** (largo) corresponde a la **luz libre interior** entre dichos soportes (no se tiene en cuenta el espesor de los revoques).
- Los requerimientos de espesor mínimo se basan en las **dimensiones nominales**. **No se tiene en cuenta el espesor de los revoques.**

**Lectura operativa para tu estudio:**

| Quiero hacer | Espesor mínimo de muro portante |
|---|---|
| PB con muros de hasta 4,00 m entre encadenados verticales, altura 2,80 m | **12 cm** (bloque hueco) o **11 cm** (macizo) |
| PB+2 (3 pisos, 10 m), muros de hasta 4,50 m, altura 3,00 m | **18 cm** (o 17-24 cm) |
| PB+2 con muros de hasta 6,00 m entre soportes, altura 3,50 m | **25-30 cm** |
| **Más de 3 pisos o más de 10 m** | **NO SE PUEDE con el 501-E. Requiere CIRSOC 501 con cálculo, o cambiar de sistema.** |

### 7.5.4 **[RC] Anclajes y trabas — art. 7.3 del 501-E (verificado)**

Los muros que se intersecan deben anclarse por alguno de estos métodos:
1. **Traba de la mampostería:** el 50% de los mampuestos de la intersección se traban con mampuestos alternados que apoyen **al menos 80 mm** sobre el mampuesto inferior.
2. **Conectores de acero** de sección mínima **3,2 × 40 mm**, extremos doblados hacia arriba al menos 50 mm, **largo ≥ 500 mm**, separación vertical máxima **600 mm**.
3. **Armadura en juntas de asiento**, separadas verticalmente **≤ 600 mm**, barras o alambres longitudinales de **diámetro ≥ 4,2 mm**, extendidos **≥ 700 mm** en cada dirección de la intersección.
4. **Anclaje de encadenados verticales a los muros** mediante armadura embutida en el mortero de asiento: espaciamiento vertical **≤ 600 mm**, longitud mínima **500 mm**, diámetro **4,2 mm**.

**Cubiertas (art. 7.4, verificado):**
- 7.4.1: las cubiertas con pendiente se deben diseñar de manera que **sus cargas gravitatorias no transmitan empujes laterales perpendiculares al plano del muro**.
- 7.4.2: cuando exista **succión** en las cubiertas, debe ser resistida **en su totalidad** por un sistema de anclaje empotrado en el encadenado vertical y/o horizontal, que se debe dimensionar.

> El punto 7.4.2 es el que resuelve el problema del techo que vuela (§2.5.11). **El anclaje de la cubierta al encadenado es reglamentario, no opcional.**

### 7.5.5 Cuándo usar mampostería portante

| Favorable | Desfavorable |
|---|---|
| Vivienda de hasta 3 plantas | Más de 3 plantas o 10 m |
| Plantas con muchos muros y luces cortas (≤ 4,5 m) | **Plantas libres, grandes luces, grandes vanos** |
| Muros que se repiten en todas las plantas | Plantas que cambian de distribución en altura |
| Mano de obra local abundante | Necesidad de velocidad |
| Presupuesto ajustado | Necesidad de flexibilidad futura |
| Buen aislamiento térmico y acústico "gratis" | **Reforma futura: cada muro es estructural. Muy poco flexible** |

> **Advertencia para tu práctica de reformas:** una vivienda de mampostería portante es **rígida para siempre**. Cada muro que el cliente quiera tirar en el futuro será una intervención estructural con apuntalamiento y dintel. Si el cliente valora la flexibilidad, **pórticos de hormigón con tabiquería no portante** es la elección correcta aunque cueste 15% más. Decíselo en el anteproyecto.

## 7.6 Hormigón postesado

### 7.6.1 Qué es

Se colocan cables de acero de alta resistencia (**fpu ≈ 1860 MPa**, contra 420 MPa del acero pasivo) dentro de vainas en la losa o viga. Se hormigona. Cuando el hormigón alcanza resistencia suficiente, se **tesan** los cables con un gato y se anclan. La fuerza de pretensado comprime el hormigón y genera una carga "hacia arriba" (efecto de la curvatura del cable) que **contrarresta parte de la carga gravitatoria**.

```
   Carga gravitatoria ↓↓↓↓↓↓↓↓↓↓↓↓
   ═══════════════════════════════════
        ╲___                    ___╱      ← trazado parabólico del cable
            ╲________________╱
   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
   Carga equivalente hacia arriba
```

### 7.6.2 Adherente vs. no adherente

| | **Adherente** (*bonded*) | **No adherente** (*unbonded*) |
|---|---|---|
| Vaina | Metálica corrugada, **inyectada con lechada de cemento** después de tesar | Plástica, con **grasa** — el cable queda libre |
| Cables | Torones agrupados (4-19 por vaina) | Torón individual ϕ12,7 o 15,2 mm |
| Resistencia última | **Mayor** (el acero desarrolla toda su capacidad localmente) | Menor (deformación promediada en toda la longitud) |
| Comportamiento ante rotura de un cable | Localizado | **Se pierde todo el cable** |
| Durabilidad | Buena (protección de la lechada) | Depende de la grasa y del ancoraje. **Los anclajes son el punto débil** |
| Uso típico | Vigas, losas de gran solicitación, puentes | **Losas de edificios** |
| Costo de ejecución | Mayor (inyección) | Menor |
| Modificaciones futuras | **Muy difícil** | **MUY PELIGROSO cortar un cable** |

### 7.6.3 Predimensionado [PD]

| Parámetro | Valor |
|---|---|
| **Espesor de losa plana postesada** | **L/40 a L/45** |
| **Espesor de losa con vigas postesadas** | L/45 a L/50 |
| **Altura de viga postesada** | L/20 a L/25 |
| **Luz económica** | **8 – 16 m** |
| **Compresión media en la losa** | **0,9 – 2,0 MPa** (típico 1,2-1,5) |
| **Carga balanceada** | 60 – 90% de la carga permanente |
| **Cable de torón ϕ12,7 mm** | Fuerza de tesado ≈ 140 kN por torón |
| **Consumo de cable** | **4 – 7 kg/m²** de losa |
| **Acero pasivo adicional** | 12 – 20 kg/m² |
| **f'c mínimo** | **H-30 mínimo, H-35 recomendado** |
| **f'c en el momento del tesado** | **≥ 0,80 · f'c** (o el que fije el proyectista de postesado) |

### 7.6.4 Ventajas, desventajas y advertencias

**Ventajas:**
- **Grandes luces con espesor mínimo** → más plantas en la misma altura reglamentaria, o mayor altura libre.
- **Menos peso propio** → fundaciones más chicas. En 10 plantas la diferencia es enorme.
- **Control de fisuras y flechas** — la losa está comprimida, prácticamente no fisura.
- **Desencofrado rápido** (se tesa a los 3-7 días y se puede desencofrar).

**Desventajas y riesgos [FIRMA]:**
1. **Requiere especialista.** No es algo que se improvise. El diseño del trazado de cables, las pérdidas por fricción, el retroceso de cuña, la relajación del acero, la retracción y fluencia son cálculos delicados.
2. **Acortamiento elástico de la losa.** Una losa postesada se acorta 3-8 mm cada 10 m al tesarse. Si hay tabiques rígidos o columnas cortas y rígidas que se lo impiden, **se fisuran los tabiques y se agrietan las columnas de borde**. Hay que prever **juntas de acortamiento** o columnas flexibles en los bordes.
3. **Anclajes y zonas de anclaje**: concentraciones de tensión enormes. Armadura de zunchado específica. φ = 0,85 para zonas de anclaje de postesado (verificado, art. 9.3.2.5), y **art. 9.2.5: para el dimensionamiento de la zona de anclaje se debe aplicar un factor de carga de 1,2 a la máxima fuerza del gato de tesado** (verificado).
4. **REFORMAS FUTURAS — PELIGRO MORTAL.** Cortar un cable postesado no adherente **libera la energía de todo el cable de golpe**. Es un accidente potencialmente fatal. **Toda perforación en una losa postesada requiere detección previa de cables** (georradar/pacómetro especializado) **y aprobación del proyectista original.**
   - **Documentá la existencia del postesado**: planos as-built, cartel permanente en el edificio, mención en el reglamento de copropiedad.
5. **Recubrimiento incrementado**: art. 7.7.x del CIRSOC 201 exige incrementar el recubrimiento de la armadura pretensada **un 50%** en condiciones severas de exposición [verificado en el texto: "para condiciones severas de exposición, el recubrimiento mínimo de la armadura pretensada se deberá incrementar un..." — **[VER] el porcentaje exacto**].
6. **f'c mínimo por durabilidad más alto**: Tabla 2.5 verificada — hormigón **pretensado** exige f'c mín 25 MPa en A1, 30 en A2, 35 en A3/M1, 40 en CL/M2 (contra 20/25/30/35 del armado).

## 7.7 Steel framing

### 7.7.1 Qué es

Estructura de **perfiles de chapa de acero galvanizado conformada en frío** (perfiles C y U, tipo PGC y PGU), montados como un entramado de montantes y soleras a **40-60 cm** de separación, arriostrado con placas o cruces de San Andrés, y cerrado con placas de yeso (interior) y placas cementicias o OSB + revestimiento (exterior).

### 7.7.2 Reglamentación

| Reglamento | Alcance |
|---|---|
| **CIRSOC 303-2009** | Elementos estructurales de acero de sección abierta conformados en frío, a partir de chapas de espesor **≤ 25,4 mm**. Base: AISI Specification 1996 y AISI North American Specification 2001 |
| **CIRSOC 308-2007** | Estructuras livianas de acero para viviendas |
| **INPRES-CIRSOC 103 Parte IV** | Acciones sísmicas (art. A.3 del 303 lo remite) |
| **IRAM IAS U 500-205** | Perfiles de chapa de acero galvanizado [VER número y edición] |

**Nota verificada:** CIRSOC 303 art. A.1 establece que aplica *"con cargas predominantemente estáticas"*, y el art. A.3 remite las acciones sísmicas al INPRES-CIRSOC 103.

### 7.7.3 Límite de plantas

**[VER] — no encontré un límite numérico explícito de plantas en el CIRSOC 303 o 308.** Lo que sí es cierto:

| Consideración | Realidad práctica |
|---|---|
| **Práctica argentina habitual** | **PB y PB+1 (2 plantas)** |
| Con diseño específico y arriostramiento adecuado | **Hasta 3 plantas** |
| Internacional (con perfiles estructurales de mayor espesor y sistemas de arriostramiento diseñados) | Hasta 5-6 plantas |
| Limitación real | **La rigidez lateral y el acortamiento acumulado de los montantes**, no la resistencia |

**Criterio honesto [PD]: en tu práctica, steel framing hasta 2 plantas sin discusión; 3 plantas con verificación estructural específica y arriostramiento diseñado; más de 3 plantas, no.**

### 7.7.4 Ventajas y desventajas

| Ventaja | Desventaja |
|---|---|
| **Peso propio bajísimo (1,0-1,8 kN/m²)** → fundaciones mínimas | Requiere **mano de obra capacitada** — escasa en el interior |
| **Velocidad**: obra seca, 50% del plazo | Sensible a errores de ejecución (un tornillo mal puesto no se ve) |
| **Excelente aislación térmica** (aislante entre montantes, sin puentes térmicos si se ejecuta bien) | **Puentes térmicos** en los montantes si no hay barrera exterior continua |
| Precisión dimensional | **Percepción de mercado**: "casa de chapa". Menor valor de reventa en el interior |
| Instalaciones dentro de los tabiques | **Aislación acústica** requiere diseño (masa baja) |
| **Ideal para ampliar en altura** sobre estructura existente (§8.7) | Corrosión si falla el galvanizado o hay condensación intersticial |
| Poca generación de residuos | Modificaciones posteriores requieren conocer la estructura |
| Sismorresistente por peso bajo | **Certificación**: no hay CAT obligatorio, pero conviene verificar antecedentes del proveedor |

### 7.7.5 Puntos de control [FIRMA]

1. **Espesor de chapa**: 0,89 / 0,94 / 1,25 / 1,60 / 2,00 mm. Los montantes estructurales de 0,89 mm son sólo para tabiques no portantes.
2. **Galvanizado**: Z275 (275 g/m² de zinc) mínimo en ambientes normales.
3. **Arriostramiento**: cruces de San Andrés de fleje, o placas estructurales (OSB o cementicia) con clavado/atornillado diseñado. **Sin arriostramiento no hay estructura.**
4. **Anclaje a la fundación**: es donde se transmite el vuelco por viento. Requiere **hold-downs** (anclajes de tracción) en los extremos de los paneles arriostrados, no sólo brocas químicas cada tanto.
5. **Con V = 50 m/s en Santa Rosa, el arriostramiento y los anclajes de una casa de steel framing son un cálculo real, no un detalle.** Una casa liviana tiene poco peso estabilizante contra el vuelco y la succión.
6. **Barrera de agua y viento** (membrana hidrófuga) por fuera de la placa exterior, y **barrera de vapor** por dentro en el clima de La Pampa (para evitar condensación intersticial).

## 7.8 Madera (CIRSOC 601-2016)

Sistema en crecimiento en Argentina, especialmente con **entramado (*platform frame*)** y con **madera laminada encolada (MLE / glulam)** y **CLT** en obras mayores.

| Aspecto | Dato [PD] |
|---|---|
| Reglamento | **CIRSOC 601-2016** |
| Luces económicas — entramado | 4 – 6 m |
| Luces económicas — MLE | 8 – 25 m |
| Altura práctica en entramado | 2 – 3 plantas |
| Peso propio | 1,5 – 3,0 kN/m² |
| **Especies argentinas** | Pino Paraná (γ=6 kN/m³), pino Spruce, pinos implantados (Elliottii, Taeda), eucaliptos, lapacho, quebracho |
| Pesos unitarios (verificados, Tabla 3.1 CIRSOC 101) | Blanda 6 kN/m³ (Janka < 30 MPa) / Semidura 9 (30-45 MPa) / Dura 11 (45-60 MPa) / Muy dura 13 (> 60 MPa) |
| Puntos críticos | **Humedad, insectos (termitas), fuego, uniones** |
| Tratamiento | CCA, CCB o similar para clase de riesgo 3-4. **Obligatorio en contacto con el suelo o exterior** |

**Regla de oro de la madera: "sombrero y botas"** — alero generoso que la proteja de la lluvia, y separación del suelo (≥ 20 cm sobre el nivel de terreno terminado, sobre fundación de hormigón con barrera capilar).

---
---

# 8. REFORMAS Y REHABILITACIÓN

Este es el capítulo que más diferencia a un estudio que "sabe" de uno que improvisa. En obra nueva conocés todo; en reforma **trabajás con incertidumbre** y el trabajo consiste en reducirla ordenadamente.

## 8.1 Relevamiento y diagnóstico: la secuencia completa

### 8.1.1 Regla n.º 1

> **No se interviene lo que no se conoce.** Ninguna demolición, apertura, ampliación o refuerzo se proyecta sin relevamiento previo. Y ninguna obra empieza sin **acta de estado** documentada de la construcción y de sus linderos.

### 8.1.2 Secuencia de trabajo

```
1. DOCUMENTAL          → Planos municipales aprobados, memorias, planos
                          de obra, permisos, antecedentes de siniestros
                          
2. HISTÓRICO            → Edad, sistema constructivo de la época,
                          modificaciones anteriores, cambios de uso,
                          eventos (incendio, inundación, obra lindera)
                          
3. VISUAL / GEOMÉTRICO  → Relevamiento dimensional, mapeo de daños,
                          fotografía sistemática, verticalidad, niveles
                          
4. NO DESTRUCTIVO       → Pacometría, esclerometría, ultrasonido,
                          termografía, humedad
                          
5. SEMI-DESTRUCTIVO     → Calas, picado localizado, extracción de
                          testigos, calicatas contra el cimiento
                          
6. LABORATORIO          → Resistencia de testigos, carbonatación,
                          cloruros, análisis de morteros, suelos
                          
7. MONITOREO            → Fisurómetros, testigos de yeso, topografía,
                          inclinómetros (si hay proceso activo)
                          
8. MODELO Y VERIFICACIÓN → Modelo estructural con los datos reales
                          
9. DIAGNÓSTICO Y PROYECTO DE INTERVENCIÓN  [FIRMA]
```

### 8.1.3 Documentación municipal — qué pedir

| Documento | Dónde | Qué te dice |
|---|---|---|
| Legajo de obra aprobado | Dirección de Obras Particulares, Municipalidad | Planos, superficies, año, profesional interviniente |
| Planos de estructura | Ídem, o archivo del profesional original | Secciones, armaduras, hormigón especificado |
| Final de obra / conforme a obra | Ídem | Si lo construido coincide con lo aprobado |
| Estudio de suelos original | Propietario / consorcio | Cotas y tensiones adoptadas |
| Reglamento de copropiedad y plano de PH | Registro de la Propiedad | Qué es propio y qué es común. **Los muros portantes y las losas suelen ser COMUNES** |

> **Advertencia legal:** en un edificio en propiedad horizontal, **la estructura es cosa común**. Cualquier intervención sobre columnas, vigas, losas o muros portantes requiere **autorización de la asamblea de copropietarios**, no sólo del municipio. Esto no es un tecnicismo: es la causa de la mayoría de los conflictos judiciales en reformas de departamentos.

### 8.1.4 Relevamiento visual — qué mirar y en qué orden

| Zona | Qué buscar |
|---|---|
| **Fachada** | Fisuras (mapearlas TODAS con ancho y orientación), desprendimientos, manchas de óxido, eflorescencias, desplomes |
| **Encuentro con el terreno** | Fisuras en zócalos y veredas, hundimientos, humedad ascendente, raíces de árboles |
| **Losas y cielorrasos** | Flechas visibles (usar hilo tendido y medir), fisuras paralelas a las vigas, manchas de humedad, armaduras vistas |
| **Vigas y columnas** | Fisuras (verticales, horizontales, diagonales — cada una dice algo distinto), desprendimientos en aristas, cangrejeras |
| **Muros interiores** | Fisuras en encuentros con losas, sobre y bajo aberturas, en las esquinas de los vanos |
| **Aberturas** | Puertas y ventanas que no cierran (indicador clásico de distorsión) |
| **Pisos** | Desniveles (nivel láser o manguera), fisuras, baldosas sonadas |
| **Sala de máquinas y azotea** | Sobrecargas no previstas: equipos de aire, tanques, antenas, obras de vecinos |
| **Sótanos y cámaras** | Humedad, filtraciones, estado de cañerías (¡pérdidas!) |
| **Linderos** | **SIEMPRE.** Fotos fechadas, mapeo de fisuras existentes, acta firmada por el vecino |

### 8.1.5 Herramientas del relevamiento

| Herramienta | Uso | Costo relativo |
|---|---|---|
| **Fisurómetro (regla de fisuras)** | Medir ancho de fisura en mm | Muy bajo |
| **Testigo de yeso o vidrio** | Detectar si una fisura está viva. Se rompe si hay movimiento | Nulo |
| **Fisurómetro de placas (tipo Avongard)** | Medir evolución en dos direcciones con precisión de 0,5 mm | Bajo |
| **Nivel láser / manguera de nivel** | Desniveles de pisos, flechas de losas | Bajo |
| **Plomada / desplomímetro** | Verticalidad de muros y columnas | Muy bajo |
| **Cámara fotográfica con fecha** | Documentación. **Imprescindible legalmente** | Nulo |
| **Higrómetro / humedímetro** | Contenido de humedad de muros | Bajo |
| **Cámara termográfica** | Puentes térmicos, humedades ocultas, delaminaciones | Medio |
| **Estación total / nivel óptico** | Monitoreo de asentamientos con precisión mm | Medio |
| **Endoscopio / boroscopio** | Ver dentro de cavidades con perforación mínima | Bajo |

## 8.2 Ensayos sobre estructura existente

### 8.2.1 Pacometría (detección de armaduras)

**Qué hace:** localiza barras de acero, mide **recubrimiento** y estima **diámetro**.

| Aspecto | Dato |
|---|---|
| Principio | Inducción electromagnética (pacómetro) o **georradar (GPR)** para mayor profundidad y resolución |
| Precisión de recubrimiento | ±2-5 mm hasta 80-100 mm de profundidad |
| Precisión de diámetro | ±1 escalón de diámetro (estimativa) |
| Limitación | En zonas muy armadas o con mallas densas, las señales se superponen. **El GPR resuelve mejor** |
| **Uso crítico** | **ANTES DE PERFORAR CUALQUIER COSA.** Antes de una cala, de un anclaje químico, de un pase de instalación |
| Norma | [VER: la referencia internacional es BS 1881-204; en Argentina, verificar norma IRAM aplicable] |

> **El pacómetro es la mejor inversión de un estudio que hace reformas.** Un equipo de gama media cuesta lo que una jornada de un albañil y evita cortar una armadura principal.

### 8.2.2 Esclerometría (índice de rebote)

**Qué hace:** mide la **dureza superficial** del hormigón con un martillo Schmidt, correlacionándola con la resistencia.

| Aspecto | Dato |
|---|---|
| Norma argentina | **IRAM 1694** [VER número y edición vigente] |
| Norma internacional | ASTM C805, EN 12504-2 |
| **Qué mide realmente** | La dureza de los **primeros 30-50 mm**. **NO mide la resistencia del núcleo** |
| Dispersión | **±20-30%** respecto de la resistencia real. Es enorme |
| **Uso correcto** | **Comparativo**: identificar zonas de menor calidad dentro de un mismo elemento o edificio. **Mapeo de homogeneidad** |
| **Uso INCORRECTO** | Tomar el valor absoluto de la curva del fabricante como "la resistencia del hormigón". **Nunca hagas esto** |
| Factores que distorsionan | Carbonatación (**sube el rebote**, sobreestima), humedad superficial (baja), edad, tipo de agregado, dirección del golpe (hay que corregir), revoque o pintura (hay que retirarlos) |
| Procedimiento | Superficie lisa, seca y limpia; **mínimo 9-10 impactos** por zona de ensayo, separados ≥ 25 mm; descartar valores anómalos; promediar |

**Cómo usarla bien [PD]:**
1. Mapeá el edificio con esclerómetro → identificás zonas de baja calidad.
2. **Calibrás la curva con 3-6 testigos extraídos** de zonas de distinto índice de rebote.
3. Con la curva calibrada, extendés al resto del edificio.

**Esta combinación (esclerometría + testigos de calibración) es la práctica correcta y la que reconoce cualquier perito.**

### 8.2.3 Extracción de testigos

**Qué hace:** el ensayo **dirimente** para conocer la resistencia real del hormigón.

| Aspecto | Dato |
|---|---|
| Norma argentina | **IRAM 1551** [VER número y edición: extracción, acondicionamiento y ensayo de testigos] |
| Norma internacional | ASTM C42, EN 12504-1 |
| **Diámetro** | Preferentemente **100 mm**; mínimo **3 veces el TMN del agregado** (típicamente 75-100 mm) |
| **Relación altura/diámetro** | **Ideal 2,0.** Si es menor, hay que aplicar factores de corrección (h/d=1,75→0,98; 1,50→0,96; 1,25→0,93; 1,00→0,87) [PD, verificar en IRAM 1551] |
| Preparación | Refrentado con azufre o rectificado de caras |
| **Dónde extraer** | **NUNCA en zonas de máxima solicitación.** En vigas: cerca del eje neutro, en el tercio central, alejado de armaduras. En columnas: zona media de la altura. **Usar pacómetro antes** |
| **Reparación del agujero** | Obligatoria: limpieza, imprimación epoxi y relleno con mortero de reparación de retracción compensada |
| **Criterio de aceptación** | El hormigón se considera aceptable si el promedio de 3 testigos ≥ **0,85·f'c** y ningún testigo individual < **0,75·f'c** [VER criterio exacto en CIRSOC 201 / IRAM 1551] |
| Cantidad mínima | **3 testigos por zona de ensayo** de resistencia homogénea |

### 8.2.4 Ultrasonido (velocidad de pulso ultrasónico, UPV)

| Aspecto | Dato |
|---|---|
| Norma | ASTM C597, EN 12504-4 [VER IRAM equivalente] |
| Qué mide | Velocidad de propagación de ondas ultrasónicas → **homogeneidad, presencia de fisuras internas, huecos, delaminaciones, profundidad de fisuras** |
| Velocidad típica en hormigón sano | **3.500 – 4.500 m/s** |
| Interpretación [PD] | > 4500: excelente / 3500-4500: bueno / 3000-3500: dudoso / 2000-3000: pobre / < 2000: muy pobre |
| Método | Transmisión directa (caras opuestas — el mejor), semidirecta, o indirecta (misma cara) |
| **Combinado con esclerómetro** | El método **SonReb** combina UPV + índice de rebote y reduce mucho la dispersión de la estimación de resistencia |

### 8.2.5 Ensayo de profundidad de carbonatación

| Aspecto | Dato |
|---|---|
| Método | Pulverizar **fenolftaleína** (solución al 1% en alcohol) sobre una fractura fresca del hormigón |
| Resultado | **Rosa/fucsia** = hormigón alcalino (pH > 9), **NO carbonatado**, armadura protegida. **Incoloro** = carbonatado, pH < 9, **armadura desprotegida** |
| Medición | Profundidad del frente incoloro desde la superficie, en mm |
| Norma | EN 14630 [VER IRAM equivalente] |
| **Lo que importa** | Comparar la **profundidad de carbonatación** con el **recubrimiento real** (medido con pacómetro). Si `xc ≥ recubrimiento`, la armadura está en riesgo de corrosión activa |

**Modelo de avance [PD]:**
```
xc = K · sqrt(t)
```
con t en años y K en mm/√año:

| Condición | K (mm/√año) [PD] |
|---|---|
| Hormigón de alta calidad (a/c ≤ 0,45), protegido | 1 – 2 |
| Hormigón normal (a/c ≈ 0,55), interior seco | 3 – 5 |
| Hormigón normal, exterior protegido de la lluvia | 4 – 7 |
| Hormigón pobre (a/c ≥ 0,65), exterior | 8 – 15 |

**Ejemplo:** hormigón normal exterior, K = 5. A los 40 años: `xc = 5 × √40 = 32 mm`. Si el recubrimiento real es 20 mm (típico en obras de los 60-70), **la armadura lleva más de 20 años despasivada**.

### 8.2.6 Contenido de cloruros

| Aspecto | Dato |
|---|---|
| Método | Extracción de polvo a distintas profundidades (perforación con broca), análisis químico |
| Umbral crítico | **0,4 % de Cl⁻ respecto del peso de cemento** (aproximadamente 0,05-0,08% respecto del peso de hormigón) [PD; verificar el umbral exacto en el CIRSOC 201] |
| Cuándo | Ambientes marinos, industrias, edificios donde se usó cloruro de calcio como acelerante (**práctica común hasta los años 70**), garajes con sales |
| Resultado | Perfil de concentración en profundidad → estima la vida residual |

### 8.2.7 Potencial de corrosión (semipilas / half-cell)

| Aspecto | Dato |
|---|---|
| Norma | ASTM C876 |
| Qué mide | Potencial eléctrico de la armadura respecto de un electrodo de referencia (Cu/CuSO₄) |
| Interpretación (Cu/CuSO₄) [PD] | > −200 mV: **probabilidad de corrosión < 10%** / −200 a −350 mV: incierto / < −350 mV: **probabilidad > 90%** |
| Ventaja | Mapea la corrosión **antes de que sea visible**. Permite delimitar la zona a reparar |
| Complemento | **Resistividad eléctrica** del hormigón (indica velocidad de corrosión) |

### 8.2.8 Prueba de carga

El ensayo definitivo cuando todo lo demás es insuficiente.

| Aspecto | Dato |
|---|---|
| Norma | **CIRSOC 201, Capítulo 20** — "Evaluación de la resistencia de estructuras existentes" [VER numeración exacta] |
| Carga de ensayo | Típicamente `0,85 · (1,4D + 1,7L)` [VER expresión en la edición vigente] |
| Duración | Carga mantenida **24 horas**, luego descarga |
| **Criterios de aceptación [VER exactos]** | Flecha máxima `Δmax ≤ ℓt²/(20.000·h)` y recuperación `Δr ≥ 75% de Δmax` tras 24 h de descarga |
| Cuándo | Cuando el análisis no permite concluir, o cuando hay dudas sobre la ejecución. **Cambio de destino con aumento de sobrecarga** |
| **Precaución** | Apuntalamiento de seguridad debajo, evacuación del área, instrumentación con comparadores, **procedimiento firmado** |

### 8.2.9 Otros ensayos

| Ensayo | Para qué |
|---|---|
| **Arrancamiento (pull-off)** | Adherencia de revoques, morteros de reparación, refuerzos FRP |
| **Extracción de barras de armadura** | Ensayo de tracción para determinar fy real (destructivo, sólo en casos justificados) |
| **Análisis de mortero de mampostería** | Composición, resistencia (importante en edificios antiguos) |
| **Ensayo con gato plano (*flat jack*)** | Tensión in situ en muros de mampostería y módulo de deformación |
| **Termografía infrarroja** | Delaminaciones, humedades, puentes térmicos, mapeo de mamposterías bajo revoque |
| **Georradar (GPR)** | Espesores, armaduras profundas, huecos, vainas de postesado |

## 8.3 Patologías: catálogo de fisuras y su diagnóstico

### 8.3.1 Cómo leer una fisura — los cuatro datos

Toda ficha de fisura debe registrar:
1. **Ubicación y trazado** (croquis sobre plano)
2. **Ancho** (mm, con fisurómetro) y **variación a lo largo** (¿se abre hacia arriba, hacia abajo?)
3. **Profundidad** (¿pasante? ¿sólo revoque?)
4. **Actividad**: ¿viva o muerta? (testigo de yeso, fisurómetro con lectura en 2-3 meses)

**Y la regla más importante:** *"La fisura es perpendicular a la dirección de la tracción que la causó."*

### 8.3.2 Catálogo de fisuras

#### A. Fisuras por ASENTAMIENTO DIFERENCIAL

```
A.1 — ASENTAMIENTO EN UN EXTREMO (el extremo derecho baja)

  ┌─────────────────────────────────┐
  │              ╱                  │      Fisuras INCLINADAS a ~45°,
  │            ╱  ╱                 │      más ANCHAS ARRIBA,
  │          ╱  ╱                   │      apuntando HACIA el
  │        ╱  ╱                     │      asentamiento
  │  ────────────────────────────   │
  └─────────────────────────────────┘
      zona estable   ←→   zona que baja
```

```
A.2 — ASENTAMIENTO CENTRAL (pandeo hacia abajo, "sagging")

  ┌─────────────────────────────────┐
  │  ╲                         ╱    │      Fisuras hacia el CENTRO,
  │    ╲                     ╱      │      más anchas ARRIBA
  │      ╲                 ╱        │
  │  ─────────────────────────      │
  └─────────────────────────────────┘
        ↓↓↓ centro que baja ↓↓↓
```

```
A.3 — LEVANTAMIENTO CENTRAL / ASENTAMIENTO DE BORDES ("hogging")

  ┌─────────────────────────────────┐
  │    ╱                       ╲    │      Fisuras hacia los EXTREMOS,
  │  ╱                           ╲  │      más anchas ABAJO
  │╱                               ╲│
  └─────────────────────────────────┘
   ↓↓ bordes bajan ↓↓        ↓↓
```

**Diagnóstico diferencial:**

| Indicio | Interpretación |
|---|---|
| Fisura de **ancho variable, más ancha en un extremo** | Asentamiento (movimiento de rotación) |
| Fisura que **atraviesa mampuestos** (no sólo juntas) | Movimiento importante y rápido |
| Fisura que sigue las **juntas de mortero en escalera** | Movimiento más lento, mortero débil |
| Fisura **pasante** (se ve de los dos lados del muro) | Estructural |
| Aberturas que **dejan de cerrar** | Distorsión angular significativa |
| **Pisos desnivelados** en la misma dirección | Confirma asentamiento |
| Fisura que **continúa en la vereda o el zócalo** | Asentamiento (el revoque no fisura la vereda) |
| **Actividad estacional** (se abre en verano, se cierra en invierno) | Suelo expansivo o retracción de arcillas por árboles |
| **Progresión monótona** | Proceso activo — urgente |
| **Estabilizada** (testigo intacto tras 6 meses) | Proceso concluido — reparación cosmética + monitoreo |

**Causas frecuentes en La Pampa:**
1. **Colapso de loess por humedecimiento** (§3.5). Localizado, junto a una pérdida de cañería, un canterito, una bajada pluvial.
2. **Árboles** (eucaliptos, álamos, paraísos) que desecan el suelo y luego se retiran → hinchamiento.
3. **Excavación lindera** sin protección.
4. **Ampliación con fundación a distinta cota** o distinta rigidez (el caso clásico: ampliación en el fondo con cimiento superficial, casa original con cimiento más profundo).
5. **Relleno mal compactado** bajo parte de la construcción.
6. **Ascenso o descenso de napa.**

#### B. Fisuras por SOBRECARGA / FLEXIÓN

```
B.1 — FLEXIÓN EN VIGA (tramo)

     ═══════════════════════════════
     │  │  │  │  │  │  │  │  │  │      Fisuras VERTICALES en el
     │  │  │  │  │  │  │  │  │  │      TERCIO CENTRAL, en la cara
     └──┴──┴──┴──┴──┴──┴──┴──┴──┘      INFERIOR, perpendiculares al eje
   ▲                             ▲
   
B.2 — FLEXIÓN EN VIGA (apoyo, momento negativo)

     ═╤═╤═╤═════════════════╤═╤═╤═     Fisuras VERTICALES en la
      │ │ │                 │ │ │      cara SUPERIOR, sobre los apoyos
     ───────────────────────────
   ▲                             ▲

B.3 — CORTE EN VIGA

     ═══════════════════════════════
     │╱ ╱                   ╲ ╲│      Fisuras DIAGONALES a ~45°
     │╱                       ╲│      cerca de los APOYOS, ascendentes
     └─────────────────────────┘      hacia el centro. ¡PELIGROSAS!
   ▲                             ▲
```

| Tipo | Ancho | Peligrosidad |
|---|---|---|
| **Flexión, ancho ≤ 0,3 mm** | Normal. El hormigón armado **fisura por diseño** | Baja, si el ancho es admisible |
| **Flexión, ancho 0,3 – 0,5 mm** | Atención. Verificar armadura y cargas | Media. Riesgo de durabilidad |
| **Flexión, ancho > 0,5 mm** | **Sobrecarga o armadura insuficiente** | **Alta** |
| **CORTE (diagonal cerca del apoyo)** | Cualquier ancho | **MUY ALTA — falla frágil sin aviso. APUNTALAR** |
| **Fisura horizontal en el eje neutro cerca del apoyo** | — | **CRÍTICA — falla de adherencia / anclaje** |

**Anchos de fisura admisibles [PD]** (criterio de durabilidad):

| Exposición | w_max |
|---|---|
| Interior seco | 0,40 mm |
| Exterior / húmedo | 0,30 mm |
| Ambiente agresivo (cloruros) | 0,20 mm |
| Estanqueidad requerida | 0,10 – 0,20 mm |

#### C. Fisuras por CORROSIÓN DE ARMADURAS

```
     ┌───────────────────────────────┐
     │═══════════════════════════════│  ← Fisura PARALELA a la armadura
     │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    │     Manchas de ÓXIDO
     │═══════════════════════════════│     Desprendimiento del recubrimiento
     └───────────────────────────────┘     ("delaminación", "spalling")
```

**Signo inconfundible: la fisura sigue exactamente el trazado de la barra**, con manchas ocres y, en estado avanzado, **desprendimiento del recubrimiento dejando la barra a la vista**.

**Mecanismo:** el óxido de hierro ocupa **2 a 7 veces** el volumen del acero original. Esa expansión revienta el recubrimiento desde adentro.

Ver §8.4 para el tratamiento completo.

#### D. Fisuras por RETRACCIÓN

```
D.1 — RETRACCIÓN PLÁSTICA (hormigón fresco, primeras horas)

     ┌───────────────────────────────┐
     │   ╱      ╱      ╱      ╱      │   Fisuras cortas, paralelas,
     │  ╱      ╱      ╱      ╱       │   irregulares, superficiales,
     │ ╱      ╱      ╱      ╱        │   a ~45° del eje. Superficie de
     └───────────────────────────────┘   losas hormigonadas con viento/sol

D.2 — RETRACCIÓN HIDRÁULICA (semanas-meses)

     Fisuras en zonas de cambio de sección, esquinas de aberturas,
     encuentros con elementos rígidos. Trazado recto, ancho uniforme.

D.3 — RETRACCIÓN EN REVOQUES / "piel de cocodrilo"

     ┌───────────────────────────────┐
     │  ╱─╲╱─╲╱─╲╱─╲╱─╲╱─╲╱─╲        │  Fisuración en red, muy fina,
     │  ╲─╱╲─╱╲─╱╲─╱╲─╱╲─╱╲─╱        │  sólo en el revoque.
     └───────────────────────────────┘  Exceso de cemento o de agua,
                                        curado deficiente
```

| Característica | Retracción | Estructural |
|---|---|---|
| Ancho | **Uniforme** a lo largo | Variable |
| Profundidad | Superficial (plástica) o pasante (hidráulica) | Pasante |
| Evolución | **Se estabiliza** en meses/años | Puede progresar |
| Ubicación | Zonas de restricción, cambios de sección | Zonas de máxima solicitación |
| Ancho típico | 0,1 – 0,5 mm | Variable |

#### E. Fisuras TÉRMICAS

- Trazado **vertical** en muros largos, aproximadamente equidistantes.
- **Actividad estacional marcada**: se abren en invierno (contracción), se cierran en verano.
- Típicas en **losas de azotea sin aislación** que dilatan y empujan los muros de la última planta → fisura horizontal en el encuentro muro-losa, y fisuras diagonales en las esquinas del último piso.

```
   ÚLTIMO PISO — el problema clásico de la losa de azotea sin aislar

   ═══════════════════════════════════════  ← losa de azotea que dilata
   ────────────────────────────────────────  ← fisura horizontal en el
   │╲                                   ╱│     encuentro (empuje de la losa)
   │  ╲                               ╱  │  ← fisuras diagonales en
   │    ╲                           ╱    │     las esquinas
   │                                     │
```

**Solución:** aislación térmica sobre la losa de azotea (cubierta invertida o aislación bajo membrana), y **junta deslizante** entre losa de azotea y muro de la última planta.

#### F. Fisuras por EXPANSIÓN DE MATERIALES

| Causa | Signo |
|---|---|
| **Oxidación de perfiles metálicos embebidos** (dinteles de hierro, viguetas de perfil) | Fisura horizontal continua sobre el dintel, con manchas de óxido. **Muy común en construcciones de 1920-1960** |
| **Ataque por sulfatos** | Fisuración en mapa, desintegración de la pasta, aspecto "blando" y blanquecino. **Relevante en fundaciones en loess con yeso** |
| **Reacción álcali-sílice (RAS)** | Fisuración en mapa con exudación de gel, en hormigones con agregados reactivos. Rara pero posible |
| **Expansión de morteros de cal viva mal apagada** | Cráteres ("caliches") en revoques antiguos |
| **Congelación** (irrelevante en Santa Rosa, relevante en cordillera) | Descascaramiento superficial |

#### G. Fisuras por EMPUJE

| Situación | Signo |
|---|---|
| Cubierta a dos aguas sin tensor | **Fisura horizontal** en la parte superior de los muros perimetrales, muros que se desploman hacia afuera |
| Muro de contención sin drenaje | Fisuras horizontales en el tercio inferior, desplome |
| Arco o bóveda sin estribo | Fisuras en la clave y en los arranques |
| **Bóveda de ladrillo sobre perfiles ("bovedilla")** | Fisura en el intradós, oxidación del perfil |

#### H. Fisuras en TABIQUES NO PORTANTES

```
   Tabique de mampostería trabado a la estructura, que recibe
   la flecha diferida de la losa superior:

   ═══════════════════════════════════════  ← losa que flecha ↓
    ╲___                             ___╱
   ┌────╲─────────────────────────╱─────┐
   │      ╲                     ╱        │  ← fisuras diagonales
   │        ╲                 ╱          │     desde las esquinas
   │  ┌─────┐ ╲             ╱  ┌─────┐   │     superiores
   │  │vano │   ╲         ╱    │vano │   │  ← y en las esquinas
   │  └─────┘     ╲     ╱      └─────┘   │     de las aberturas
   └───────────────────────────────────┘
```

**Es la patología más frecuente en edificios nuevos y no es estructural**: es la flecha diferida de la losa que "carga" al tabique. Prevención: **junta superior de 2 cm entre el tabique y la losa superior**, rellena con material compresible y sellada. Y **ejecutar los tabiques lo más tarde posible**, cuando la mayor parte de la flecha ya ocurrió.

### 8.3.3 Tabla resumen de diagnóstico rápido

| Trazado | Ubicación | Causa más probable | Urgencia |
|---|---|---|---|
| Diagonal ~45°, ancho variable | Muros, cerca de esquinas | **Asentamiento diferencial** | **Alta** |
| Vertical, tercio central, cara inferior | Vigas y losas | Flexión (normal si w ≤ 0,3 mm) | Baja-Media |
| Vertical, cara superior sobre apoyos | Vigas y losas continuas | Momento negativo (normal si w ≤ 0,3 mm) | Baja |
| **Diagonal cerca del apoyo** | **Vigas** | **CORTE** | **CRÍTICA** |
| Horizontal en el eje neutro cerca del apoyo | Vigas | **Falla de anclaje/adherencia** | **CRÍTICA** |
| Paralela a la armadura + óxido | Vigas, columnas, losas, balcones | **Corrosión de armaduras** | Media-Alta |
| Vertical en columna, con desprendimiento | Columnas | **Sobrecarga axial / aplastamiento** | **CRÍTICA** |
| Horizontal en columna | Columnas | Junta de hormigonado mal ejecutada, o flexión | Media |
| Red fina superficial | Revoques, losas | Retracción / curado deficiente | Baja |
| Horizontal, encuentro muro-losa último piso | Última planta | **Dilatación térmica de losa de azotea** | Media |
| Horizontal sobre dintel con óxido | Dinteles antiguos | **Oxidación de perfil embebido** | Media-Alta |
| Diagonal desde esquinas superiores de tabique | Tabiques no portantes | Flecha de la losa superior | Baja (no estructural) |
| En escalera por juntas de mortero | Mampostería | Asentamiento lento / mortero débil | Media |

## 8.4 Corrosión de armaduras y carbonatación

### 8.4.1 El mecanismo

```
FASE 1 — INICIACIÓN                    FASE 2 — PROPAGACIÓN
(el hormigón protege)                  (la armadura se corroe)

pH del hormigón ≈ 12,5-13,5            El acero pierde sección
→ capa pasiva de óxido protege         El óxido expande 2-7 veces
  el acero                             → fisura el recubrimiento
                                       → entra más agua y O₂
El frente de carbonatación             → se acelera
avanza: CO₂ + Ca(OH)₂ → CaCO₃ + H₂O    → desprendimiento (spalling)
→ el pH baja a ~8-9                    → pérdida de adherencia
→ se DESPASIVA el acero                → pérdida de capacidad

O bien: entran cloruros que
rompen localmente la capa pasiva
(corrosión por picadura, más grave)

     ─────────────────────────────────────────────────►  tiempo
     ▲                                    ▲
   construcción                    fin de vida útil
```

**Requisitos simultáneos para que haya corrosión:**
1. **Despasivación** (carbonatación o cloruros)
2. **Agua** (electrolito)
3. **Oxígeno**

Si falta cualquiera de los tres, no hay corrosión. Por eso el hormigón permanentemente sumergido no se corroe (falta oxígeno) y el hormigón permanentemente seco tampoco (falta agua). **El peor caso es el ciclo húmedo-seco**: balcones, fachadas, zonas de salpicadura.

### 8.4.2 Diagnóstico de la corrosión

| Ensayo | Qué determina |
|---|---|
| **Inspección visual** | Extensión de fisuras, manchas, desprendimientos |
| **Pacometría** | Recubrimiento real (la causa raíz suele ser recubrimiento insuficiente) |
| **Carbonatación (fenolftaleína)** | Profundidad del frente vs. recubrimiento |
| **Cloruros** | Perfil de concentración |
| **Potencial de corrosión (ASTM C876)** | Mapa de probabilidad de corrosión activa |
| **Resistividad** | Velocidad de corrosión |
| **Picado localizado** | Medición de pérdida de sección de la barra (con calibre) |

### 8.4.3 Evaluación de la pérdida de sección

```
% pérdida = (A_original − A_actual) / A_original × 100
```

| Pérdida de sección | Consecuencia [PD] |
|---|---|
| < 10 % | Generalmente aceptable si se detiene el proceso |
| 10 – 20 % | Verificar por cálculo. Puede requerir refuerzo |
| 20 – 30 % | **Refuerzo necesario** casi con certeza |
| > 30 % | **Sustitución o refuerzo obligatorio.** Apuntalar durante los trabajos |
| Pérdida de estribos | **Crítica** — puede llevar al pandeo de las barras longitudinales |

### 8.4.4 Reparación — el procedimiento completo

```
1. APUNTALAR              si la pérdida de sección es significativa
                          o si se va a picar en zona traccionada

2. DELIMITAR              con martillo de percusión / sondeo sonoro,
                          marcar TODA la zona con hormigón delaminado
                          (siempre es mayor que lo que se ve)

3. PICAR                  eliminar todo el hormigón carbonatado,
                          fisurado y disgregado. Bordes CORTADOS a
                          disco (no en pico de pato), profundidad
                          mínima 1 cm en el borde.
                          ► DEJAR AL DESCUBIERTO LA BARRA EN TODO SU
                            PERÍMETRO: mínimo 2 cm de espacio libre
                            detrás de la barra. Si no, el óxido de
                            atrás sigue trabajando.
                          ► Extender el picado 5 cm más allá de la
                            zona corroída visible.

4. LIMPIAR EL ACERO       arenado, granallado o cepillo mecánico
                          hasta grado Sa 2½ / St 3.
                          ► Eliminar TODO el óxido, incluido el de
                            las picaduras.

5. EVALUAR SECCIÓN        medir con calibre. Si pérdida > 20%,
                          AGREGAR BARRAS nuevas solapadas
                          (longitud de empalme completa) o soldadas
                          (sólo si el acero es soldable — verificar)

6. PROTEGER EL ACERO      imprimación anticorrosiva de base cementicia
                          con inhibidor, o epoxi. Dos manos.
                          ► NO usar antióxido sintético común

7. PUENTE DE ADHERENCIA   lechada cementicia modificada con polímero,
                          o resina epoxi, sobre el hormigón saturado
                          con superficie seca (SSS)

8. RECONSTRUIR            mortero de reparación de RETRACCIÓN
                          COMPENSADA, tixotrópico, clase R3/R4
                          (EN 1504-3), aplicado en capas de
                          10-25 mm. Para volúmenes grandes,
                          microhormigón fluido con encofrado.

9. CURAR                  imprescindible. 3-7 días con riego,
                          membrana o film.

10. PROTEGER              revestimiento anticarbonatación
                          (pintura elastomérica con baja permeabilidad
                          al CO₂ y alta al vapor de agua), o
                          hidrofugante de silano/siloxano

11. MONITOREAR            inspección a 6, 12 y 24 meses
```

**El error clásico:** picar sólo lo que se ve, dejar la barra apoyada en hormigón contaminado por detrás, y tapar con mortero común. **Resultado: reaparece en 1-3 años, y peor** — porque se genera un **efecto de par galvánico** entre la zona reparada (alcalina) y la contigua (carbonatada), que acelera la corrosión justo al borde del parche. Este fenómeno se llama **"efecto ánodo incipiente"** y es la razón por la cual las reparaciones parciales mal hechas fallan sistemáticamente.

### 8.4.5 Protecciones adicionales

| Técnica | Descripción | Cuándo |
|---|---|---|
| **Revestimiento anticarbonatación** | Pintura que reduce la difusión de CO₂ | Preventivo y post-reparación en fachadas |
| **Hidrofugante (silano/siloxano)** | Impregnación que repele el agua sin cerrar el poro | Fachadas expuestas |
| **Inhibidores de corrosión migratorios (MCI)** | Se aplican en superficie y migran hasta la armadura | Complemento, no sustituto de la reparación |
| **Ánodos de sacrificio de zinc** | Se embeben en el parche de reparación y protegen catódicamente el perímetro | **Evitan el efecto ánodo incipiente.** Muy recomendable |
| **Protección catódica por corriente impresa** | Sistema activo con fuente de corriente | Estructuras muy contaminadas por cloruros, de alto valor |
| **Realcalinización electroquímica** | Restaura el pH del hormigón carbonatado | Casos especiales, caro |
| **Extracción electroquímica de cloruros** | — | Casos especiales, caro |

## 8.5 Técnicas de refuerzo

### 8.5.1 Tabla comparativa

| Técnica | Aumenta | Aumenta rigidez | Aumenta sección | Peso agregado | Costo | Plazo | Reversible |
|---|---|---|---|---|---|---|---|
| **Encamisado de hormigón armado** | Flexión, corte, axial | **Mucho** | **Mucho** | Alto | Medio | Largo | No |
| **Encamisado metálico (angulares + presillas)** | Axial, confinamiento | Medio | Poco | Medio | Medio | Corto | Sí |
| **FRP — fibra de carbono (CFRP)** | **Flexión, corte, confinamiento** | **Poco** | **Nada** | **Casi nulo** | Alto | **Muy corto** | Parcial |
| **Perfiles metálicos adosados (vigas de refuerzo)** | Flexión, corte | Mucho | Medio | Medio | Medio | Corto | Sí |
| **Postesado exterior** | Flexión, corte | Mucho | Nada | Bajo | Alto | Medio | Sí |
| **Recrecido de losa (capa colaborante)** | Flexión, rigidez | Mucho | Medio | **Alto** | Bajo | Medio | No |
| **Chapas de acero encoladas** | Flexión | Medio | Poco | Bajo | Medio | Corto | Parcial |
| **Nuevos apoyos (columnas, muros)** | Reduce luces | Mucho | — | Bajo | Bajo | Corto | Sí |

### 8.5.2 Encamisado de hormigón armado

```
   ANTES                          DESPUÉS
   
   ┌──────────┐                ┌────────────────┐
   │          │                │ ┌──────────┐   │  ← nuevo hormigón
   │ 20 × 30  │      →         │ │ 20 × 30  │   │     6-10 cm de espesor
   │          │                │ └──────────┘   │
   └──────────┘                └────────────────┘  → 32 × 42
   
   Preparación de la superficie existente:
   ► Picado / escarificado hasta dejar el agregado a la vista
     (rugosidad ≥ 5 mm de amplitud)
   ► Conectores de corte (barras ancladas químicamente) para
     garantizar el trabajo monolítico
   ► Armadura nueva con estribos CERRADOS que abracen todo
     (requiere perforar la losa arriba y abajo)
   ► Hormigón fluido o autocompactante, o mortero proyectado
```

| Aspecto | Detalle |
|---|---|
| **Espesor mínimo del recrecido** | **6 cm** para hormigón vertido (necesita paso del agregado); **4 cm** para mortero proyectado o autocompactante |
| **Armadura mínima** | Como columna nueva: ρ ≥ 0,01 del área agregada |
| **Estribos** | **Cerrados**, atravesando la losa. Es lo más laborioso y lo que más se recorta — **no lo permitas**: sin estribos cerrados no hay confinamiento y el encamisado no funciona |
| **Conectores** | Barras ϕ8-12 ancladas con resina epoxi en perforaciones, cada 30-50 cm, en tresbolillo |
| **Hormigón** | H-30 mínimo, con aditivo expansor o retracción compensada. Autocompactante si el espacio es reducido |
| **Continuidad entre plantas** | **Fundamental.** Un encamisado que se corta en la losa no transmite carga. Hay que perforar la losa y continuar |
| **Fundación** | **Casi siempre hay que ampliar la base también.** Un encamisado que aumenta la capacidad de la columna pero no la de la base no sirve |
| **Cuándo usarlo** | Cuando se necesita **mucho** aumento de capacidad axial (ampliación en altura), o cuando la columna está muy deteriorada |
| **Desventaja principal** | **Invasivo, lento, sucio, ocupa espacio.** Y agrega peso |

**Referencia técnica:** ACI 369R (Guide for Seismic Rehabilitation of Existing Concrete Frame Buildings), ACI 546R (Guide to Concrete Repair). En Argentina, INPRES-CIRSOC 103 **Capítulo 11 "Construcciones existentes"** (verificado en el índice: art. 11.1 Alcances; 11.2 Definiciones; 11.3 Principios fundamentales; 11.4 Clasificación de las construcciones; 11.5 Excepciones permitidas; 11.6 Exigencias y comprobaciones). **[VER] el contenido de este capítulo — es la referencia normativa argentina directa para intervención en existentes.**

### 8.5.3 Refuerzo con FRP (fibra de carbono y afines)

**Materiales:**

| Fibra | Módulo E (GPa) | Resistencia (MPa) | Deformación de rotura | Uso |
|---|---|---|---|---|
| **Carbono (CFRP) estándar** | 230 – 240 | 3.500 – 4.900 | 1,5 – 2,0 % | **El más usado.** Alta resistencia y rigidez |
| Carbono de alto módulo | 350 – 640 | 2.500 – 4.000 | 0,5 – 1,0 % | Cuando se necesita rigidez |
| **Vidrio (GFRP)** | 70 – 85 | 1.900 – 3.400 | 2,5 – 4,5 % | Más barato, menos rígido. Confinamiento |
| **Aramida (AFRP)** | 70 – 125 | 3.500 – 4.100 | 2,0 – 4,0 % | Resistencia al impacto |
| **Acero (SRP/SRG)** | 200 | 3.000 | 1,5 % | Alternativa económica, compatible con matriz cementicia (SRG) |

**Presentaciones:**
- **Tejido unidireccional** (300-600 g/m²), impregnado in situ con resina epoxi (*wet lay-up*). El más versátil.
- **Laminado pultruido** (platina de 1,2-1,4 mm × 50-120 mm), pegado con adhesivo epoxi. Más rígido y de mayor calidad, pero sólo para superficies planas.
- **Barras y tejidos NSM** (*near surface mounted*): ranura en el hormigón + barra o platina de CFRP + adhesivo. Mejor protegido contra el fuego y el vandalismo.

**Normativa:**
- **ACI 440.2R-17** — "Guide for the Design and Construction of Externally Bonded FRP Systems for Strengthening Concrete Structures". **Es la referencia.**
- ACI 440.1R-15 — hormigón armado con barras de FRP.
- fib Bulletin 90 (2019), CNR-DT 200 R1/2013 (Italia).
- **[VER] En Argentina no existe reglamento CIRSOC específico de FRP.** Se proyecta según ACI 440, lo cual es la práctica aceptada. **Documentalo en la memoria.**

**Tres aplicaciones:**

```
1. REFUERZO A FLEXIÓN
   ═════════════════════════════════   viga
   ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬   ← laminado CFRP en la cara traccionada
   
2. REFUERZO A CORTE
   ═══╥══╥══╥═══════════╥══╥══╥════
      ║  ║  ║           ║  ║  ║        ← bandas en U o envolventes
      ╚══╝  ╚═══════════╝  ╚══╝           cerca de los apoyos
   
3. CONFINAMIENTO DE COLUMNAS
   ┌─────────┐                        ← envoltura circunferencial completa
   │▓▓▓▓▓▓▓▓▓│                          aumenta f'c efectivo y ductilidad
   │▓▓▓▓▓▓▓▓▓│                          (esquinas REDONDEADAS R ≥ 20-30 mm)
   └─────────┘
```

**Puntos críticos de diseño [FIRMA]:**

1. **El modo de falla que gobierna es el DESPEGUE (*debonding*)**, no la rotura de la fibra. ACI 440 limita la deformación efectiva del FRP a un valor muy inferior al de rotura (típicamente **εfe ≤ 0,9·εfu** y además `εfd = 0,41·sqrt(f'c/(n·Ef·tf)) ≤ 0,9·εfu` [VER expresión exacta en ACI 440.2R-17]).
2. **El FRP no aporta rigidez significativa** al estado de servicio: es delgado. **No reduce flechas ni fisuración** de manera relevante. Si tu problema es la flecha, el FRP no lo resuelve.
3. **El FRP sólo trabaja para las cargas que se agregan DESPUÉS de pegarlo.** El estado tensional preexistente lo toma la estructura original. Si querés que el FRP tome parte de la carga permanente, hay que **descargar la estructura** (apuntalar) antes de pegarlo.
4. **[RC/PD] Límite de capacidad sin refuerzo (ACI 440.2R):** la estructura **sin** el FRP debe poder resistir un nivel mínimo de carga (típicamente `1,1·D + 0,75·L`), para el caso de que el FRP se pierda (fuego, vandalismo, impacto). **Esto limita cuánto podés reforzar con FRP: no podés duplicar la capacidad de una viga.** El aumento realista es del **20-50%**.
5. **FUEGO: el epoxi pierde propiedades a partir de la Tg (~60-80 °C).** En un incendio, el FRP se pierde en minutos. Por eso el punto 4. Si hay exigencia de resistencia al fuego, **hay que proteger el FRP** con mortero o placas, o usar sistemas SRG con matriz cementicia.
6. **Preparación de la superficie:** es el 60% del éxito. Superficie sana (arenado/granallado), plana (rellenar irregularidades > 1 mm), seca (humedad < 4%), sin lechada superficial. **Ensayo de arrancamiento (pull-off) previo: ≥ 1,5 MPa con falla en el hormigón** [PD, verificar en ACI 440].
7. **Esquinas redondeadas** (radio ≥ 13 mm según ACI; en la práctica 20-30 mm) para envolturas de confinamiento. Una esquina viva corta la fibra.
8. **Anclaje de los extremos:** los laminados a flexión tienden a despegarse por los extremos. Anclajes mecánicos, bandas en U, o **anclajes de fibra (*fiber anchors*)**.
9. **Control de calidad:** ensayos de arrancamiento sobre el sistema ejecutado, control de espesor de resina, registro de temperatura y humedad durante la aplicación.

**Cuándo el FRP es la mejor opción:**
- Aumentos de capacidad moderados (20-50%).
- Cuando **no se puede agregar peso ni sección**.
- Cuando el **plazo es crítico** (se ejecuta en días).
- Cuando hay que reforzar por **corte** o **confinar columnas** (es donde mejor funciona).
- Cuando la geometría es complicada (nudos, elementos curvos).

**Cuándo NO:**
- Cuando se necesita **más rigidez** (flechas).
- Cuando el aumento requerido es grande (> 50-60%).
- Cuando hay exigencia de fuego sin posibilidad de proteger.
- Cuando el hormigón base está muy deteriorado (hay que repararlo primero).
- Cuando el problema es la **fundación** (el FRP no baja carga al suelo).

### 8.5.4 Perfiles metálicos

**a) Encamisado metálico de columnas (angulares + presillas):**

```
   ┌─┐                    ┌─┐         Angulares en las 4 esquinas
   │ │                    │ │         + presillas (planchuelas)
   ├─┼────────────────────┼─┤   ← presilla soldada
   │ │                    │ │
   │ │      COLUMNA       │ │
   │ │                    │ │
   ├─┼────────────────────┼─┤   ← presilla
   │ │                    │ │
   └─┘                    └─┘
```

- Los angulares toman carga axial **sólo si están apretados contra la estructura superior e inferior** (calzado con cuña, mortero de alta resistencia sin retracción, o precarga con gato).
- Las presillas **confinan** el hormigón (efecto zunchado) y arriostran los angulares.
- Separación de presillas: `s ≤ 0,5 · lado menor de la columna` y `s ≤ 50 · espesor del angular` [PD].
- **Ventaja:** rápido, reversible, no agrega casi peso, poco espesor.
- **Desventaja:** requiere protección contra fuego y corrosión; estéticamente visible.

**b) Vigas metálicas de refuerzo bajo losas o vigas:**

- Perfil I o cajón bajo la viga existente, con separadores o con mortero de contacto.
- **Precarga:** si querés que tome parte de la carga permanente, hay que **levantar la estructura con gatos** antes de fijar el perfil, o dejar cuñas metálicas apretadas.
- Apoyo en columnas o en muros nuevos → **verificar la fundación de esos apoyos**.

**c) Perfiles como dinteles en apertura de vanos:** ver §8.6.

### 8.5.5 Recalce de cimientos

```
RECALCE POR BATACHES (el método tradicional)

  Muro existente
  ████████████████████████████████████████
  ┌──────┐          ┌──────┐          ┌──────┐   ← cimiento existente
  │ old  │          │ old  │          │ old  │
  └──┬───┘          └──┬───┘          └──┬───┘
     │  ┌──────┐       │  ┌──────┐       │      ← bataches NUEVOS
     │  │ NEW  │       │  │ NEW  │       │         (excavados y
     │  └──────┘       │  └──────┘       │          hormigonados
     │                 │                 │          POR TRAMOS)
   
  REGLA: bataches de 1,00-1,50 m de ancho, alternados,
  nunca más del 25% del muro descalzado a la vez,
  y nunca dos bataches contiguos abiertos simultáneamente.
  Orden: 1 - 4 - 2 - 5 - 3 - 6  (no consecutivo)
```

| Método | Descripción | Cuándo |
|---|---|---|
| **Bataches (recalce tradicional)** | Excavación por tramos alternados bajo el cimiento existente y hormigonado hasta el estrato competente | Profundizaciones de 1-3 m, suelos cohesivos estables, sin napa |
| **Micropilotes** | Perforación desde arriba o desde el costado, atravesando o junto al cimiento existente | **La solución moderna.** Cualquier profundidad, cualquier suelo, espacio reducido |
| **Pilotes de reacción (*jacked piles*)** | Se hincan tramos de tubo con un gato que reacciona contra el cimiento existente | Recalce con control de carga y de asentamiento |
| **Inyección de resinas expansivas** | Resina de poliuretano expansivo inyectada bajo la fundación: densifica el suelo y levanta la estructura | **Rápido, no invasivo, sin obra.** Bueno para asentamientos moderados en suelos granulares y limosos. **Menos confiable en loess autocolapsable** |
| **Jet grouting** | Columnas de suelo-cemento creadas con inyección a alta presión | Mejora masiva del suelo bajo la estructura. Caro, requiere control estricto |
| **Ensanchamiento de la base** | Hormigón armado alrededor de la base existente, con conectores | Cuando el problema es capacidad portante, no profundidad |

**Reglas de oro del recalce [FIRMA]:**
1. **Apuntalar la estructura antes de descalzar.**
2. **Bataches alternos**, nunca contiguos. Máximo 25% del muro abierto simultáneamente.
3. **Contacto entre el recalce nuevo y el cimiento viejo:** el hormigón nuevo **retrae** y deja una junta abierta. Hay que **calzar** con mortero expansivo, o con cuñas de acero y luego mortero sin retracción. **Sin este paso, el recalce no toma carga y no sirve para nada.**
4. **Monitoreo topográfico continuo** durante todo el recalce.
5. **Nunca recalzar sin conocer la causa del asentamiento.** Si la causa es una pérdida de cañería, arreglá la cañería primero.
6. **Suelo colapsable:** un recalce que baja la fundación pero deja el manto colapsable alrededor no resuelve el problema si hay fricción negativa.

### 8.5.6 Postesado exterior

Cables de postesado colocados **por fuera** del elemento, desviados con sillas, anclados en los extremos.

| Ventaja | Desventaja |
|---|---|
| **Activo**: comprime la estructura desde el momento de tesar, cierra fisuras y reduce flechas | Requiere zonas de anclaje robustas (a menudo hay que construirlas) |
| Muy eficaz para vigas de gran luz | Los cables son visibles |
| **Reversible y ajustable** (se puede retesar) | Requiere protección contra fuego y corrosión |
| Poco peso agregado | Especialista |

Es la técnica de elección para **reforzar vigas de gran luz con problemas de flecha o fisuración**, y para puentes.

## 8.6 Apertura de vanos

### 8.6.1 En muros portantes de mampostería

**Secuencia obligatoria [FIRMA]:**

```
PASO 1 — VERIFICAR QUE EL MURO ES PORTANTE
  ► Ver planos, ver espesor, ver si recibe losa o viguetas
  ► ¿Continúa hasta la fundación? ¿Está en todas las plantas?
  ► ¿Hay muro encima en la planta superior?
  ► En PH: ¿es cosa común? → autorización de asamblea

PASO 2 — CALCULAR LA CARGA SOBRE EL DINTEL
  ► Peso propio del muro sobre el vano (efecto arco: sólo el
    triángulo/cono de descarga si el muro tiene altura suficiente
    por encima)
  ► Reacción de las losas que apoyan sobre el muro
  ► Carga de plantas superiores
  ► Cargas concentradas (vigas, columnas que apoyan)

PASO 3 — DIMENSIONAR EL DINTEL Y SUS APOYOS
  ► Dintel: perfiles metálicos, viga de HºAº in situ, o viga
    prefabricada
  ► APOYOS: mínimo 20-30 cm a cada lado, sobre superficie sana
  ► ► ► VERIFICAR LA TENSIÓN DE APLASTAMIENTO EN EL APOYO ← EL PUNTO
    MÁS OLVIDADO. Es donde falla.
  ► Verificar que el muro bajo el apoyo llegue a la fundación
  ► Verificar la fundación bajo el apoyo

PASO 4 — APUNTALAR
  ► Puntales bajo la losa/viguetas a ambos lados del vano
  ► En muros de más de una planta: apuntalar TODAS las plantas
  ► Puntales sobre durmientes que repartan sobre el piso

PASO 5 — EJECUTAR EL DINTEL POR MITADES
  ► Abrir la canaleta de UNA cara del muro
  ► Colocar el primer perfil, calzarlo CONTRA EL MURO SUPERIOR
    con cuñas de acero y mortero expansivo sin retracción
  ► Esperar el fragüe
  ► Repetir del otro lado
  ► Unir los perfiles con presillas o pasadores

PASO 6 — DEMOLER EL VANO
  ► De arriba hacia abajo, sin percusión brusca
  ► NUNCA antes de que el dintel esté colocado y calzado

PASO 7 — RETIRAR PUNTALES
  ► Gradualmente, a los 7-14 días si hay hormigón nuevo
  ► Monitorear fisuras
```

**El error mortal: demoler primero y poner el dintel después.** Aunque "aguante", el muro superior ya se asentó sobre el vacío y el dintel entra sin carga; después trabaja mal y se fisura todo.

**Dimensionado del dintel [PD]:**

Carga sobre el dintel con efecto arco (muro de altura ≥ 0,7·L sobre el vano):
```
Se considera el peso del triángulo de 60° sobre el vano, más
cualquier carga que caiga dentro de ese triángulo:

q_dintel ≈ γ_muro · e_muro · (L · tan60° / 2) / L ... 

Simplificado:  W_triángulo = γ · e · L² · tan(60°) / 4 = 0,433 · γ · e · L²
```
Si el muro sobre el vano tiene menos altura, o si hay una losa apoyada dentro del triángulo, **hay que tomar toda la carga**.

**Perfiles orientativos para dinteles [PD]** (muro de 20 cm, un perfil a cada cara):

| Luz del vano | Carga baja (sólo muro) | Carga alta (muro + losa) |
|---|---|---|
| 1,00 m | 2 UPN 100 o 2 IPN 100 | 2 UPN 120 |
| 1,50 m | 2 UPN 120 | 2 UPN 140 / 2 IPN 140 |
| 2,00 m | 2 UPN 140 | 2 IPN 160 / 2 IPN 180 |
| 2,50 m | 2 IPN 160 | 2 IPN 200 |
| 3,00 m | 2 IPN 180 | 2 IPN 220 / viga HºAº 20×40 |
| 4,00 m | 2 IPN 220 | Viga de HºAº 20×50 |
| > 4,00 m | **Viga de HºAº o perfil armado, con verificación específica** | |

> **[FIRMA] Esta tabla es orientativa para presupuestar. Cada dintel se calcula.** La carga real depende de si hay losa apoyada, si hay muro arriba, si hay una columna que baja.

**Verificación del aplastamiento en el apoyo [PD]:**
```
σ_apoyo = R / (b_apoyo × e_muro)  ≤  f_adm_mampostería
```
Con f_adm del orden de **0,8 – 2,0 MPa** según el mampuesto y el mortero [VER en CIRSOC 501/501-E]. Si no verifica: aumentar la longitud de apoyo, colocar una **placa de reparto de acero**, o construir una **jamba de hormigón armado**.

### 8.6.2 En muros de hormigón armado (tabiques)

**Es una intervención de otro orden de gravedad.** Un tabique de hormigón es parte del sistema resistente lateral.

| Consideración | Detalle |
|---|---|
| **Antes que nada** | ¿Es un tabique estructural o un muro de cerramiento de hormigón? Ver planos originales |
| **Efecto sobre el sistema lateral** | Abrir un vano en un tabique **reduce su rigidez de forma no lineal**: un vano del 20% del área puede reducir la rigidez un 40-50%. Hay que **rehacer el análisis lateral de todo el edificio** |
| **Redistribución** | La rigidez que se pierde se transfiere a otros elementos. Verificarlos |
| **Torsión** | Si el tabique era parte de la simetría, abrir el vano corre el centro de rigidez |
| **Refuerzo del borde del vano** | Marco de acero o refuerzo de hormigón armado alrededor. **Los ángulos del vano concentran tensiones** — refuerzo diagonal |
| **Corte de armaduras** | Hay que reponer la capacidad de las barras cortadas mediante armadura de borde anclada |
| **Ejecución** | **Corte con sierra de diamante (hilo o disco), NUNCA con percusión.** La percusión fisura el hormigón remanente |
| **[FIRMA]** | Proyecto específico, cálculo del edificio completo, firma de matriculado, autorización municipal |

### 8.6.3 Perforaciones en losas

**Reglas prácticas [PD]:**

| Tipo de losa | Perforación admisible sin refuerzo |
|---|---|
| **Losa maciza en una dirección** | ϕ ≤ 15 cm, alejada de apoyos ≥ 2h, sin cortar armadura principal. Corriendo las barras a los lados |
| **Losa maciza en dos direcciones** | ϕ ≤ 20-25 cm en el centro del paño |
| **Losa de viguetas** | **Entre viguetas**, sin cortar ninguna. Máximo el ancho del bloque. **Cortar una vigueta requiere refuerzo con nervios transversales de reparto** |
| **Losa nervurada / casetonada** | En los casetones, sin cortar nervios |
| **Losa plana sin vigas** | **PELIGRO: la zona alrededor de las columnas es la de punzonamiento.** Ninguna perforación a menos de 3h de la cara de la columna sin verificación |
| **Losa POSTESADA** | **DETECCIÓN DE CABLES OBLIGATORIA** (georradar). Cortar un cable puede ser mortal. §7.6.4 |

**Perforaciones grandes (huecos de escalera, ascensores, patios):**
- Marco perimetral: **vigas de borde** que recojan la carga del paño interrumpido.
- **Apuntalamiento previo** de toda el área afectada.
- Corte con **sierra de hilo diamantado**, con la losa apuntalada, y retiro de la pieza con precaución (una losa de 15 cm de 2×2 m pesa 1,5 tn).
- Verificación del **diafragma** (§6.8) — un hueco grande en la losa afecta la transferencia de fuerzas horizontales.
- **[FIRMA]**

**Regla de agrupación:** varias perforaciones pequeñas juntas equivalen a una grande. Distancia mínima entre perforaciones ≥ 3 veces el diámetro mayor [PD].

## 8.7 Ampliación en altura sobre edificio existente

Es la intervención de mayor riesgo y la que más plata pierde cuando se hace mal. **Lista de verificación obligatoria — ninguna se puede saltear.**

### 8.7.1 Los seis chequeos que SIEMPRE hay que hacer

```
┌─────────────────────────────────────────────────────────────────┐
│  1. FUNDACIÓN                                                    │
│     ► ¿Qué tipo es? (calicata para verlo, no suponerlo)          │
│     ► ¿A qué cota apoya? ¿Sobre qué estrato?                     │
│     ► ¿Cuál es la tensión actual? ¿Y con la ampliación?          │
│     ► ¿Cuánto se asentó ya? ¿Cuánto más se asentará?             │
│     ► ► ESTUDIO DE SUELOS NUEVO — no vale el original            │
├─────────────────────────────────────────────────────────────────┤
│  2. COLUMNAS Y MUROS PORTANTES                                   │
│     ► ¿Cuál es la sección real? (relevamiento con pacómetro)     │
│     ► ¿Cuál es la armadura real?                                 │
│     ► ¿Cuál es el f'c real? (testigos)                           │
│     ► ¿Están corroídas? ¿Pérdida de sección?                     │
│     ► ¿Verifican con la carga nueva? (P-M, esbeltez, corte)      │
│     ► ¿Hay continuidad hasta la fundación?                       │
├─────────────────────────────────────────────────────────────────┤
│  3. LOSA DE APOYO                                                │
│     ► ¿La losa existente puede recibir la nueva estructura?      │
│     ► ¿Los apoyos de las nuevas columnas caen sobre columnas     │
│       existentes? (deben caer sobre columnas, NO sobre losa)     │
│     ► ¿Hay que reforzarla?                                       │
├─────────────────────────────────────────────────────────────────┤
│  4. ESTABILIDAD LATERAL                                          │
│     ► La ampliación aumenta H → aumenta el momento de vuelco     │
│       por viento (crece con H²) y el corte basal                 │
│     ► ¿El sistema resistente lateral existente lo aguanta?       │
│     ► ¿Hay que agregar tabiques o arriostramientos?              │
│     ► Nueva verificación del INPRES-CIRSOC 103 (¿supera 12 m?)   │
├─────────────────────────────────────────────────────────────────┤
│  5. CONTINUIDAD Y COMPATIBILIDAD                                 │
│     ► Los ejes nuevos DEBEN coincidir con los existentes         │
│     ► Compatibilidad de deformaciones entre lo viejo y lo nuevo  │
│     ► Juntas si los sistemas son distintos                       │
│     ► ¿El nuevo material (acero, steel framing) es compatible?   │
├─────────────────────────────────────────────────────────────────┤
│  6. NORMATIVO Y LEGAL                                            │
│     ► ¿El código de edificación municipal permite esa altura?    │
│       (FOT, altura máxima, retiros, plano límite)  [VER]         │
│     ► ¿Hay que actualizar la protección contra incendio?         │
│       (¿escalera presurizada? ¿segunda vía de escape?)           │
│     ► ¿Cambia la categoría del edificio para el 103?             │
│     ► En PH: autorización de la asamblea + modificación del      │
│       reglamento de copropiedad                                  │
│     ► Ascensor: ¿alcanza? ¿Hay que modificar la sala de máquinas?│
│     ► Instalaciones: presión de agua, capacidad del tanque,      │
│       capacidad eléctrica, desagües cloacales y pluviales        │
└─────────────────────────────────────────────────────────────────┘
```

### 8.7.2 La estrategia dominante: ampliar con material liviano

Comparación de una planta adicional de 200 m²:

| Sistema | Peso propio | Carga adicional total | Aumento sobre la fundación |
|---|---|---|---|
| **HºAº convencional** | 7,0 kN/m² + L 2,0 | 200 × 9,0 = **1.800 kN** | Referencia |
| **Acero + steel deck** | 3,5 kN/m² + L 2,0 | 200 × 5,5 = **1.100 kN** | **−39%** |
| **Steel framing** | 1,5 kN/m² + L 2,0 | 200 × 3,5 = **700 kN** | **−61%** |
| **Madera (entramado)** | 2,0 kN/m² + L 2,0 | 200 × 4,0 = **800 kN** | −56% |

> **Ampliar con steel framing o estructura metálica liviana suele ser la única alternativa viable** cuando la fundación existente no tiene margen. La diferencia de 1.100 kN sobre una fundación al límite es la diferencia entre "se puede" y "hay que recalzar todo el edificio".

**Pero atención:** en steel framing hay que verificar que la estructura existente pueda **recibir los anclajes de tracción (hold-downs)** que exige el arriostramiento. Una estructura liviana tiene poco peso estabilizante contra la succión y el vuelco por viento (V = 50 m/s en Santa Rosa).

### 8.7.3 Cálculo del margen disponible en la fundación [PD]

```
Margen = σ_adm − σ_actual

σ_actual = (Carga existente + peso propio de la base + suelo sobre ella) / Área de la base
```

**Pero hay una sutileza importante:** el suelo bajo una fundación existente lleva décadas cargado. **Está preconsolidado bajo esa carga.** Un incremento de carga:
- Si `σ_nueva ≤ σ_actual`: prácticamente no genera asentamiento nuevo (recarga en la rama de descarga-recarga, con Cs << Cc).
- Si `σ_nueva > σ_actual`: genera asentamiento en la rama virgen.

**Esto es una ventaja** — el edificio existente "ya se asentó". Pero también significa que **cualquier incremento produce asentamiento adicional inmediato**, que el edificio existente (con sus tabiques ya construidos y sin capacidad de acomodarse) va a **acusar con fisuras**.

**Criterio [PD]:** para ampliación sobre edificio existente con tabiquería terminada, apuntá a un **asentamiento adicional ≤ 5-10 mm** y una **distorsión angular adicional ≤ 1/1000**. Es mucho más estricto que en obra nueva.

**En loess:** el incremento de carga puede llevar σ por encima de σF.SAT donde antes estaba por debajo. **Rehacer el análisis de colapsabilidad con las cargas nuevas.**

## 8.8 Demoliciones parciales y apuntalamiento

### 8.8.1 Principio rector

> **Toda demolición es una operación estructural.** El orden de demolición debe ser el **inverso** al de construcción, y en cada etapa la estructura remanente tiene que estar en equilibrio estable.

### 8.8.2 Proyecto de demolición [FIRMA]

Contenido mínimo:
1. **Relevamiento del sistema estructural existente** (§8.1).
2. **Identificación de los elementos portantes** y de los que se van a retirar.
3. **Análisis de la estructura remanente en cada etapa** — no sólo al final.
4. **Proyecto de apuntalamiento**: ubicación, tipo, capacidad, apoyos, arriostramiento.
5. **Secuencia de demolición** paso a paso, con planos.
6. **Protección de linderos**: apuntalamiento del medianero, submuración si hay excavación.
7. **Acta de estado de linderos** con fotos y fisurómetros.
8. **Plan de monitoreo** durante la demolición.
9. **Plan de contingencia**.
10. **Gestión de residuos y de servicios** (cortar agua, gas, electricidad antes).

### 8.8.3 Apuntalamiento — reglas

| Regla | Detalle |
|---|---|
| **Capacidad** | Puntal metálico telescópico común: **10 – 20 kN** de servicio, **decreciendo mucho con la altura extendida** (a 3,5 m puede bajar a 8-10 kN). **Verificar la tabla del fabricante para la altura real** |
| **Torre de apuntalamiento (multidireccional)** | 20 – 60 kN por pata. Necesaria para cargas altas |
| **Durmiente inferior** | Tablón o perfil que reparta sobre el piso. **El puntal apoyado directamente sobre un contrapiso lo punzona** |
| **Durmiente superior** | Idem contra la losa |
| **Arriostramiento** | Puntales de más de 3 m **deben arriostrarse** horizontalmente en las dos direcciones. Un puntal sin arriostrar pandea |
| **Verticalidad** | Un puntal inclinado 5° pierde capacidad y genera empuje horizontal |
| **Continuidad en altura** | Si apuntalás una losa, **la carga baja a la losa inferior**, que puede no aguantarla. **Apuntalar en todas las plantas hasta llegar al terreno o a un elemento capaz** |
| **Precarga** | Apretar el puntal hasta hacer contacto firme, **sin levantar la estructura** (levantar genera esfuerzos inversos) |
| **Registro** | Planilla de apuntalamiento firmada, con ubicación y capacidad |

```
   APUNTALAMIENTO CORRECTO — continuidad hasta el terreno

   ═══════════════════════════════   ← losa a demoler / intervenir
      ║   ║   ║   ║   ║              ← puntales
   ═══╬═══╬═══╬═══╬═══╬═══════════   ← losa 1er piso
      ║   ║   ║   ║   ║              ← puntales ALINEADOS
   ═══╬═══╬═══╬═══╬═══╬═══════════   ← losa PB
      ║   ║   ║   ║   ║
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ← terreno / platea

   ❌ ERROR: apuntalar sólo la planta intervenida.
      La carga se transfiere a la losa de abajo, que no
      estaba dimensionada para eso, y falla.
```

### 8.8.4 Submuración de medianeras

Cuando se excava junto a una medianera existente (subsuelo, cochera), hay que **submurar**: extender el cimiento del vecino hasta la nueva cota.

**Reglas [FIRMA]:**
1. **Bataches alternos** (igual que en recalce, §8.5.5): tramos de 1,00-1,50 m, nunca contiguos, máximo 25% abierto.
2. **Calzar el nuevo hormigón contra el cimiento existente** con mortero expansivo — sin esto, no toma carga.
3. **Acta de estado del lindero** con fotos, fisurómetros y firma del vecino, **antes de empezar**.
4. **Monitoreo topográfico diario** durante la submuración.
5. **Notificación fehaciente al vecino** (carta documento) y, si corresponde, mediación previa.
6. **Seguro de responsabilidad civil** con cobertura por daño a linderos.
7. **[VER]** Marco legal: Código Civil y Comercial de la Nación, artículos sobre medianería y restricciones al dominio; código de edificación municipal.
8. **En loess:** la excavación descomprime lateralmente y puede provocar colapso. Excavación **por tramos cortos y hormigonado inmediato**.

### 8.8.5 Errores mortales en demolición

| Error | Consecuencia |
|---|---|
| Demoler un muro portante sin identificarlo como tal | Colapso |
| Demoler de abajo hacia arriba | Colapso |
| Retirar apuntalamiento antes de que el elemento nuevo tenga resistencia | Colapso |
| Acopiar escombro sobre losas | Sobrecarga muy superior a la de diseño (1 m³ de escombro ≈ 16 kN/m² sobre 1 m²) |
| Usar martillo neumático sobre losa apuntalada con puntales sueltos | Los puntales "saltan" con la vibración |
| No cortar servicios (gas, electricidad) | Incendio, explosión, electrocución |
| Demoler tabiques que resultaron ser rigidizadores del pórtico | Cambio no previsto en la rigidez lateral |
| No verificar la estabilidad de muros que quedan libres | Un muro sin arriostrar es una pared de 20 cm parada de canto |

## 8.9 EJEMPLO NUMÉRICO 3 — Apertura de vano en muro portante

### Enunciado

Vivienda en Santa Rosa. Se quiere unir living y comedor abriendo un vano de **3,00 m** en un muro portante interior.

| Dato | Valor |
|---|---|
| Muro | Ladrillo hueco cerámico portante, **18 cm** + revoque a ambas caras (espesor total 22 cm) |
| Tipología | PB + 1 planta alta |
| Altura de muro sobre el vano (en PB) | 2,60 − 2,10 (altura del vano) = **0,50 m** hasta la losa de PA |
| Muro en planta alta sobre el mismo eje | Sí, **2,60 m** de altura |
| Losa de PA | Viguetas pretensadas, apoyadas **perpendicularmente** al muro, luz 4,00 m |
| Losa de azotea | Ídem, luz 4,00 m |
| Sobrecarga | Vivienda L = 2,00 kN/m²; azotea inaccesible Lr = 1,00 kN/m² |

### Paso 1 — Verificar que el muro es portante

✓ Recibe viguetas perpendiculares en PB y en PA. **Es portante.** Espesor 18 cm, dentro del rango 170-240 mm de la Tabla 7.1 del CIRSOC 501-E → **altura máxima de edificio 10 m, distancia máxima entre soportes verticales 4,50 m**. ✓

**Consecuencia importante:** al abrir un vano de 3,00 m, el tramo de muro remanente a cada lado debe seguir cumpliendo la función portante y el arriostramiento. **Hay que verificar que la distancia entre soportes verticales del muro remanente siga siendo ≤ 4,50 m.**

### Paso 2 — Cargas sobre el dintel

**Ancho tributario de las losas:** las viguetas apoyan a ambos lados con luz 4,00 m → tributaria = 4,00/2 × 2 = **4,00 m**.

**a) Peso propio del muro sobre el vano en PB (0,50 m de altura):**
```
γ_muro con revoque = 12 kN/m³  (ladrillo hueco portante con revoque, Tabla 3.1 verificada)
q1 = 12 × 0,18 × 0,50 = 1,08 kN/m
```
> **Efecto arco:** con sólo 0,50 m de muro sobre el vano (< 0,7 × 3,00 = 2,10 m), **NO hay efecto arco.** Se toma toda la carga.

**b) Reacción de la losa de PA sobre el muro:**
```
D_losa PA = 5,50 kN/m²  (viguetas 2,20 + contrapiso 1,44 + carpeta 0,42 + piso 0,20 + cielorraso 0,20 + tabiquería 1,04)
L_losa PA = 2,00 kN/m²
q2_D = 5,50 × 4,00 = 22,00 kN/m
q2_L = 2,00 × 4,00 =  8,00 kN/m
```

**c) Peso del muro de planta alta (2,60 m):**
```
q3 = 12 × 0,18 × 2,60 = 5,62 kN/m
```

**d) Reacción de la losa de azotea:**
```
D_azotea = 6,00 kN/m²  (viguetas 2,20 + contrapiso pendiente 1,80 + aislaciones 0,65 + membrana 0,10 + cielorraso 0,20 + parapeto repartido 1,05)
Lr = 1,00 kN/m²
q4_D = 6,00 × 4,00 = 24,00 kN/m
q4_Lr = 1,00 × 4,00 = 4,00 kN/m
```

**Totales:**
```
D_total = 1,08 + 22,00 + 5,62 + 24,00 = 52,70 kN/m
L_total = 8,00 kN/m
Lr_total = 4,00 kN/m
```

**Combinación mayorada (9-2):**
```
qu = 1,2 × 52,70 + 1,6 × 8,00 + 0,5 × 4,00 = 63,24 + 12,80 + 2,00 = 78,04 kN/m
```

**Combinación de servicio (para flechas y apoyos):**
```
q_serv = 52,70 + 8,00 + 4,00 = 64,70 kN/m
```

### Paso 3 — Solicitaciones en el dintel

Luz de cálculo (luz libre + apoyo, o luz libre × 1,05):
```
L_cálculo = 3,00 + 0,25 = 3,25 m    (asumiendo 25 cm de apoyo a cada lado, centro a centro de apoyos ≈ 3,25 m)
```

**Momento máximo (biapoyado, conservador):**
```
Mu = qu · L² / 8 = 78,04 × 3,25² / 8 = 78,04 × 10,5625 / 8 = 103,0 kNm
```

**Corte máximo:**
```
Vu = qu · L / 2 = 78,04 × 3,25 / 2 = 126,8 kN
```

**Reacción de servicio en cada apoyo:**
```
R_serv = 64,70 × 3,25 / 2 = 105,1 kN
```

### Paso 4 — Dimensionar el dintel metálico

Se propone **2 perfiles IPN**, uno por cada cara del muro, unidos con pasadores. Cada perfil toma la mitad:
```
Mu_perfil = 103,0 / 2 = 51,5 kNm
```

Acero F-24 (fy = 235 MPa) — el habitual en perfiles nacionales.

**Módulo resistente requerido (LRFD, φb = 0,90, sección compacta):**
```
Wx,req = Mu / (φb · fy) = 51,5 × 10⁶ N·mm / (0,90 × 235 N/mm²) = 51,5e6 / 211,5 = 243.500 mm³ = 243,5 cm³
```

**Selección de perfil:**

| Perfil | Wx (cm³) | Ix (cm⁴) | Peso (kg/m) | ¿Verifica Wx ≥ 243,5? |
|---|---|---|---|---|
| IPN 200 | 214 | 2140 | 26,2 | ✗ |
| **IPN 220** | **278** | **3060** | **31,1** | **✓** |
| IPN 240 | 354 | 4250 | 36,2 | ✓ (holgado) |
| IPE 240 | 324 | 3892 | 30,7 | ✓ |
| IPE 270 | 429 | 5790 | 36,1 | ✓ |

**Adoptar 2 IPN 220** (o 2 IPE 240, más eficiente en peso).

**Verificación de flecha (servicio):**
```
q_serv_perfil = 64,70 / 2 = 32,35 kN/m = 32,35 N/mm
E = 210.000 MPa
Ix = 3060 cm⁴ = 30,6 × 10⁶ mm⁴

δ = 5 · q · L⁴ / (384 · E · I)
  = 5 × 32,35 × 3250⁴ / (384 × 210.000 × 30,6e6)
  = 5 × 32,35 × 1,1157e14 / (2,4676e15)
  = 1,8047e16 / 2,4676e15
  = 7,31 mm
```

**Límite [PD] para dintel que soporta mampostería: L/500** (más estricto que L/360 porque hay muro encima que se fisura):
```
δ_adm = 3250 / 500 = 6,50 mm

δ = 7,31 mm  >  6,50 mm      ✗ NO VERIFICA
```

**Adoptar 2 IPN 240** (Ix = 4250 cm⁴ = 42,5e6 mm⁴):
```
δ = 7,31 × 3060/4250 = 5,26 mm  <  6,50 mm      ✓ VERIFICA
```

O **2 IPE 270** (Ix = 5790 cm⁴):
```
δ = 7,31 × 3060/5790 = 3,86 mm      ✓ VERIFICA CON MARGEN
```

**Adoptamos 2 IPE 270** (36,1 kg/m cada uno; mejor relación rigidez/peso que el IPN 240).

**Verificación de corte:**
```
Vu_perfil = 126,8 / 2 = 63,4 kN
Área del alma IPE 270: Aw ≈ h × tw = 270 × 6,6 = 1782 mm²
φVn = 0,90 × 0,60 × 235 × 1782 / 1000 = 0,90 × 251,3 = 226 kN

Vu = 63,4 kN  <  226 kN      ✓ VERIFICA CON GRAN MARGEN
```

**Verificación de pandeo lateral-torsional:** el perfil está embebido en el muro y arriostrado lateralmente de forma continua por la mampostería y por los pasadores al perfil opuesto → **Lb ≈ 0, no hay pandeo lateral-torsional.** ✓

### Paso 5 — VERIFICAR EL APOYO (el punto crítico)

**Reacción de servicio por apoyo: R = 105,1 kN.**

**Longitud de apoyo propuesta: 25 cm.**

**Tensión de aplastamiento sobre la mampostería:**
```
σ = R / (L_apoyo × e_muro) = 105.100 N / (250 mm × 180 mm) = 105.100 / 45.000 = 2,34 N/mm² = 2,34 MPa
```

**Tensión admisible de la mampostería de ladrillo hueco portante [PD]:** del orden de **0,8 – 1,5 MPa** para f'm típico [VER en CIRSOC 501 o 501-E el valor de f'a en función de f'u del mampuesto y del mortero].

```
σ = 2,34 MPa  >  σ_adm ≈ 1,2 MPa      ✗ NO VERIFICA
```

**¡Este es el punto que hace fallar los dinteles en la práctica!** El perfil aguanta perfectamente, pero **el muro debajo del apoyo se aplasta.**

**Soluciones:**

**Opción A — Aumentar la longitud de apoyo:**
```
L_apoyo,req = 105.100 / (1,2 × 180) = 105.100 / 216 = 487 mm  →  50 cm de apoyo a cada lado
```
Reduce el vano útil o exige alargar el dintel. Vano total del dintel: 3,00 + 2×0,50 = 4,00 m → **hay que recalcular el perfil con L = 3,50 m centro a centro**.

**Opción B — Placa de reparto de acero:**
```
Placa de 250 × 400 mm × 20 mm bajo el apoyo (repartiendo en 40 cm de altura de muro)
σ = 105.100 / (400 × 180) = 1,46 MPa   ← todavía alto
Placa de 250 × 500: σ = 105.100 / (500 × 180) = 1,17 MPa    ✓ VERIFICA (justo)
```

**Opción C — Jamba de hormigón armado (LA MEJOR):**
```
Construir una jamba de HºAº de 20 × 25 cm a cada lado del vano,
desde la fundación hasta el dintel, armada con 4ϕ12 + estribos ϕ6 c/15.

σ sobre el hormigón = 105.100 / (200 × 250) = 2,10 MPa
Con H-20:  σ_adm ≈ 0,45 · f'c = 9 MPa       ✓ VERIFICA CON GRAN MARGEN
```

**Adoptamos Opción C.** Además la jamba:
- Reemplaza estructuralmente el muro que se quita.
- Da continuidad de carga hasta la fundación.
- Sirve de encadenado vertical.

### Paso 6 — Verificar la fundación bajo la jamba

```
Carga total en la jamba (servicio) = R_dintel + peso propio de la jamba
Peso propio jamba: 25 kN/m³ × 0,20 × 0,25 × 2,60 m = 3,25 kN
Carga total ≈ 105,1 + 3,3 = 108,4 kN
```

**Cimiento existente:** zapata corrida de 0,50 m de ancho bajo el muro.

**Antes de la reforma**, esa zapata recibía la carga distribuida del muro:
```
q_muro_antes = 52,70 + 8,00 + 4,00 = 64,70 kN/m (la misma carga, distribuida)
σ_antes = 64,70 / 0,50 = 129 kPa   ← distribuido uniformemente
```

**Después de la reforma**, la carga que antes se distribuía en 3,00 m se concentra en las dos jambas:
```
Carga concentrada por jamba: 108,4 kN
Ancho de la jamba: 0,25 m
Si el cimiento corrido reparte en 3 veces el ancho de la jamba (efecto viga):
Longitud efectiva ≈ 0,25 + 2 × 0,50 (canto del cimiento) = 1,25 m  [PD]
σ_después = 108,4 / (1,25 × 0,50) = 108,4 / 0,625 = 173 kPa
```

```
σ_después = 173 kPa   vs.   σ_antes = 129 kPa      →  incremento del 34%
```

**Verificación:**

| Si σ_adm es... | Resultado |
|---|---|
| **σ_adm = 200 kPa** (suelo bueno) | ✓ VERIFICA. No hay que hacer nada |
| **σ_adm = 150 kPa** | ✗ NO VERIFICA. Hay que **ensanchar el cimiento bajo la jamba** |
| **σ_adm = 130 kPa** (loess) | ✗ NO VERIFICA. **Ensanchar y verificar colapsabilidad** |

**Solución si no verifica:** dado bajo la jamba, de 0,80 × 0,80 m:
```
σ = 108,4 / (0,80 × 0,80) = 169 kPa   ← no alcanza
Dado de 1,00 × 1,00 m:
σ = 108,4 / 1,00 = 108 kPa      ✓ VERIFICA
```
Se ejecuta descalzando por bataches (§8.5.5) y calzando con mortero expansivo.

### Paso 7 — Secuencia de ejecución

```
1.  Acta de estado con fotos y fisurómetros (incluida la planta alta)
2.  Ensanchar el cimiento bajo cada jamba (bataches alternos, 
    calzado con mortero expansivo). Curado 7 días.
3.  Ejecutar las jambas de HºAº, hormigonadas hasta 5 cm por
    debajo del nivel del dintel. Curado 7 días.
    ► Armadura anclada al cimiento nuevo con barras de espera.
4.  APUNTALAR la losa de PA y la de azotea a ambos lados del muro,
    con puntales continuos hasta el terreno (PB y PA).
5.  Abrir la canaleta en UNA cara del muro, a la altura del dintel,
    de 3,00 m + apoyos sobre las jambas.
6.  Colocar el primer IPE 270. Calzarlo contra el muro superior
    con cuñas de acero y mortero de alta resistencia sin retracción
    (grout expansivo). Rellenar completamente el hueco superior.
    ► ESTE PASO ES EL CRÍTICO. Sin calzado firme, el dintel no
      toma carga y el muro superior se asienta y fisura.
7.  Esperar 48-72 h de fragüe del grout.
8.  Repetir del otro lado (segundo IPE 270).
9.  Colocar pasadores ϕ16 c/50 cm atravesando el muro y uniendo
    ambos perfiles, con tuercas y arandelas.
10. Rellenar el espacio entre perfiles con hormigón fluido o mortero.
11. Demoler el muro bajo el dintel, de arriba hacia abajo,
    sin percusión brusca (sierra + martillo liviano).
12. Esperar 7 días monitoreando fisuras.
13. Retirar apuntalamiento gradualmente (primero PA, luego PB),
    monitoreando.
14. Proteger los perfiles: antióxido + esmalte, o encajonado con
    placa de yeso RF (resistencia al fuego).
15. Terminaciones.
```

### Paso 8 — Resumen del ejemplo 3

| Item | Resultado |
|---|---|
| Vano | 3,00 m en muro portante de 18 cm |
| Carga sobre el dintel (servicio) | **64,70 kN/m** |
| Momento mayorado | **103,0 kNm** |
| **Dintel adoptado** | **2 IPE 270**, unidos con pasadores ϕ16 c/50 cm |
| Verificación que gobernó el perfil | **FLECHA (L/500)** — no la resistencia |
| **Apoyo** | **Jambas de HºAº 20×25 cm** con 4ϕ12, desde la fundación |
| Verificación que casi hace fallar el proyecto | **APLASTAMIENTO EN EL APOYO** (2,34 MPa vs. 1,2 MPa admisible) |
| Fundación | **Dado de 1,00 × 1,00 m** bajo cada jamba (si σ_adm ≤ 150 kPa) |
| Apuntalamiento | **PB y PA, hasta el terreno** |

**Las tres lecciones del ejemplo:**

1. **El perfil casi nunca es el problema; el apoyo sí.** La verificación de aplastamiento sobre la mampostería falló por factor 2. Es la causa más frecuente de fisuras después de abrir un vano.
2. **Abrir un vano concentra cargas que antes estaban repartidas.** La fundación que servía perfectamente para carga distribuida puede no servir para carga concentrada. **Siempre hay que llegar hasta la fundación en el análisis.**
3. **La flecha gobierna el dintel, no la resistencia** — igual que en el Ejemplo 2. Un dintel que "aguanta" pero flecha 10 mm fisura todo el muro de arriba.

---
---
