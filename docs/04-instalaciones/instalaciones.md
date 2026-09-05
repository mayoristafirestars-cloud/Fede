# INSTALACIONES PARA VIVIENDAS Y EDIFICIOS HASTA PB+9

## Manual técnico de proyecto ejecutivo — Obra nueva y reforma
### Estudio de arquitectura — Santa Rosa, La Pampa, República Argentina

> **Versión:** 1.0 — Septiembre 2026
> **Alcance:** vivienda unifamiliar, vivienda colectiva y edificios en altura hasta PB+9 (10 plantas), destino residencial y mixto (comercial en PB).
> **Uso:** documento de trabajo interno del estudio para la elaboración del proyecto ejecutivo de instalaciones (planos, planillas, memorias de cálculo y pliegos).

---

## AVISO IMPORTANTE — LEER ANTES DE USAR

1. **Este documento NO reemplaza a la norma.** Los valores transcriptos provienen de las fuentes citadas en el Capítulo 12. Antes de usar un número en un plano firmado, **verificar la edición vigente** de la norma y la reglamentación de la prestadora local.
2. **Todo valor que no pudimos verificar contra fuente primaria está marcado con la leyenda `[verificar en …]`.** No usar esos valores en documentación de obra sin confirmación.
3. **La jurisdicción manda.** Buena parte de las tablas de sanitarias provienen de la *Guía para Ejecución de Instalaciones Sanitarias Domiciliarias y Asimilables a Domiciliarias* (AySA / ERAS, actualización de las Normas y Gráficos OSN Res. 67.017/81). En La Pampa la autoridad es otra: **verificar exigencias particulares con la prestadora de agua y cloaca de Santa Rosa y con la Administración Provincial del Agua (APA) de La Pampa**, y con el Código de Edificación municipal (Ordenanza 1581/95 y modificatorias, entre ellas la Ord. 6445/2020).
4. **Firmas.** Cada instalación requiere firma de profesional o instalador matriculado ante el organismo que corresponda. Ver Capítulo 10, apartado 10.6.

---

# ÍNDICE

**[0. Marco normativo, jurisdicciones y quién firma qué](#0-marco-normativo-jurisdicciones-y-quién-firma-qué)**

**[1. SANITARIAS — AGUA FRÍA Y CALIENTE](#1-sanitarias--agua-fría-y-caliente)**
- 1.1 Dotaciones y consumos de referencia
- 1.2 Caudales por artefacto y presiones mínimas
- 1.3 Simultaneidad: método del coeficiente K (AySA/ERAS) y método Hunter (unidades de gasto)
- 1.4 Tabla de diámetros por cantidad de artefactos (guía rápida)
- 1.5 Determinación de la reserva: balance de caudales
- 1.6 Reparto reserva/bombeo, altura de tanque y carga máxima
- 1.7 **EJEMPLO RESUELTO Nº 1 — Tanque de reserva y bombeo de un edificio PB+9 con 40 departamentos**
- 1.8 Equipos de bombeo: dimensionado, NPSH, golpe de ariete
- 1.9 Grupos de presurización: cuándo y cómo
- 1.10 Colectores, bajadas, montantes, válvulas, ruptores de vacío
- 1.11 Materiales: PPR, PEAD, PEX/multicapa, cobre, PVC — comparativa técnica y de costo
- 1.12 Agua caliente sanitaria: producción, dimensionado de acumulación, recirculación, legionela
- 1.13 Medición individual y sala de medidores

**[2. SANITARIAS — DESAGÜES CLOACALES](#2-sanitarias--desagües-cloacales)**
- 2.1 Sistema primario y secundario: definiciones operativas
- 2.2 Caudales de desagüe por artefacto y simultaneidad
- 2.3 Diámetros mínimos por artefacto y longitudes máximas
- 2.4 Pendientes: criterio de autolimpieza y tabla de verificación
- 2.5 **EJEMPLO RESUELTO Nº 2 — Verificación de un colector cloacal Ø110 y Ø160**
- 2.6 Sifones, piletas de piso, bocas de acceso, bocas de desagüe
- 2.7 Cámaras de inspección, tapadas, saltos
- 2.8 Ventilaciones: principal, subsidiaria (secundaria) y auxiliar
- 2.9 Montantes (caño de descarga y ventilación) en edificios en altura
- 2.10 Subsuelos: pozo de bombeo cloacal y bombas trituradoras
- 2.11 Interceptores de grasa, de trapos y de nafta
- 2.12 Sistemas estáticos: cámara séptica, pozo absorbente, zanjas de infiltración
- 2.13 **EJEMPLO RESUELTO — Ensayo de percolación y dimensionado de sistema estático**

**[3. DESAGÜES PLUVIALES](#3-desagües-pluviales)**
- 3.1 Cómo se obtiene el dato de lluvia de diseño para Santa Rosa / La Pampa
- 3.2 Superficie de aporte: reglas de cómputo
- 3.3 Embudos, piletas de piso pluviales y canaletas
- 3.4 Montantes (caños de lluvia) y albañales
- 3.5 Pendientes de azotea, balcones y terrazas
- 3.6 Bombeo pluvial de subsuelos
- 3.7 Sistemas de retardo (retención pluvial)
- 3.8 **EJEMPLO RESUELTO — Azotea de 320 m² con dos montantes**

**[4. GAS](#4-gas)**
- 4.1 Marco: ENARGAS, NAG-200 y NAG-201, prestadora
- 4.2 Presiones de servicio y gas de proyecto
- 4.3 Caudales nominales por artefacto
- 4.4 Simultaneidad individual y de la instalación común
- 4.5 Longitud equivalente y pérdida de carga admisible
- 4.6 Cálculo del diámetro: Renouard lineal y cuadrática
- 4.7 Tabla de caudales por diámetro y longitud (baja presión)
- 4.8 **EJEMPLO RESUELTO Nº 3 — Caudal y diámetros de un edificio PB+9**
- 4.9 Gabinetes y compartimentos de medidores
- 4.10 Ventilación de ambientes con artefactos: rejillas superior e inferior
- 4.11 Prohibiciones por ambiente (dormitorios, baños, monoambientes, cocinas)
- 4.12 Evacuación de productos de la combustión: tiro natural, balanceado, conductos colectivos
- 4.13 Gas natural vs. envasado / zeppelin
- 4.14 Pruebas de hermeticidad y de obstrucción
- 4.15 Trámite y documentación

**[5. INSTALACIONES ELÉCTRICAS](#5-instalaciones-eléctricas)**
- 5.1 Marco: AEA 90364, partes 7-770 y 7-771
- 5.2 Grados de electrificación
- 5.3 Tipos de circuito y número mínimo de circuitos
- 5.4 Puntos mínimos de utilización por ambiente
- 5.5 Secciones mínimas y corrientes admisibles
- 5.6 Caída de tensión admisible
- 5.7 Demanda de potencia máxima simultánea (DPMS) y coeficientes
- 5.8 **EJEMPLO RESUELTO Nº 4 — Demanda de un edificio PB+9 de 40 unidades**
- 5.9 Protecciones: termomagnéticas, diferenciales, selectividad
- 5.10 Puesta a tierra y jabalina
- 5.11 Protección contra sobretensiones (DPS)
- 5.12 Tableros: principal, seccionales, de servicios generales
- 5.13 Sala de medidores, alimentador y montantes
- 5.14 Grupo electrógeno y servicios esenciales
- 5.15 Canalizaciones: cañerías, bandejas, cajas
- 5.16 Iluminación de emergencia y señalización
- 5.17 Corrientes débiles: datos, TV, portero visor, alarma, CCTV, control de accesos
- 5.18 Cargador de vehículo eléctrico (EVSE)
- 5.19 Generación distribuida fotovoltaica — Ley 27.424

**[6. TERMOMECÁNICAS: CLIMATIZACIÓN Y VENTILACIÓN](#6-termomecánicas-climatización-y-ventilación)**
- 6.1 Datos climáticos de Santa Rosa (La Pampa) y zona bioambiental
- 6.2 Transmitancia térmica: IRAM 11601 / 11605 y niveles A, B, C
- 6.3 Consecuencias de proyecto de la zona bioambiental
- 6.4 Cálculo de carga térmica: método simplificado (W/m²) y método detallado
- 6.5 **EJEMPLO RESUELTO — Carga térmica de un departamento tipo en Santa Rosa**
- 6.6 Coeficiente volumétrico G — IRAM 11604
- 6.7 Sistemas: split, multisplit, VRF/VRV, fan coil + caldera/enfriadora
- 6.8 Losa radiante: dimensionado, paso, temperatura de impulsión
- 6.9 Radiadores
- 6.10 Ventilación mecánica y recuperadores de calor
- 6.11 Extracción de baños y cocinas
- 6.12 Ventilación de cocheras y salas de máquinas

**[7. PROTECCIÓN CONTRA INCENDIOS](#7-protección-contra-incendios)**
- 7.1 Lógica normativa: protección pasiva y activa
- 7.2 Resistencia al fuego F30 a F180 y sectorización
- 7.3 Medios de escape
- 7.4 Escalera protegida y presurizada
- 7.5 Matafuegos: tipo, potencial extintor, cantidad y ubicación
- 7.6 Detección y alarma
- 7.7 Red de incendio: reserva, bombas, hidrantes, cañerías
- 7.8 **EJEMPLO RESUELTO — Reserva y bombas de incendio**
- 7.9 Rociadores automáticos
- 7.10 Señalización

**[8. ASCENSORES Y ELEVACIÓN](#8-ascensores-y-elevación)**
- 8.1 Marco normativo
- 8.2 Cálculo de tráfico: población, RTT, intervalo, capacidad de acarreo
- 8.3 **EJEMPLO RESUELTO — Cuántos ascensores para un PB+9**
- 8.4 Dimensiones: cabina, hueco, foso, sobrerrecorrido
- 8.5 Sala de máquinas vs. gearless sin sala
- 8.6 Montacoches y plataformas
- 8.7 Accesibilidad
- 8.8 Interfaces con obra civil y otras instalaciones

**[9. INSTALACIONES EN REFORMAS](#9-instalaciones-en-reformas)**
- 9.1 Relevamiento de lo existente: protocolo
- 9.2 Qué se reutiliza y qué se cambia siempre
- 9.3 Plomo, hierro galvanizado y fibrocemento
- 9.4 Instalación eléctrica antigua sin diferencial ni tierra
- 9.5 Mover baños y cocinas: límites reales
- 9.6 Reformar sin romper: canalizaciones vistas, cielorrasos técnicos, pisos flotantes
- 9.7 Orden de trabajo y coordinación de gremios

**[10. COORDINACIÓN Y DOCUMENTACIÓN](#10-coordinación-y-documentación)**
- 10.1 Entregables por instalación y escalas
- 10.2 Simbología
- 10.3 Plantas, isométricos, esquemas unifilares
- 10.4 Coordinación de pases y colisiones (BIM)
- 10.5 Altura de cielorraso técnico
- 10.6 Quién firma cada instalación y qué trámites requiere

**[11. CHECKLISTS Y ERRORES FRECUENTES](#11-checklists-y-errores-frecuentes)**

**[12. BIBLIOGRAFÍA Y NORMAS COMENTADAS](#12-bibliografía-y-normas-comentadas)**

---

# 0. Marco normativo, jurisdicciones y quién firma qué

## 0.1 Las cuatro capas normativas

El proyecto de instalaciones en Argentina se resuelve superponiendo cuatro capas. Cuando entran en conflicto, **manda la más restrictiva**, salvo que la más específica tenga jerarquía legal expresa (por ejemplo, ENARGAS en gas).

| Capa | Quién la dicta | Ejemplos | Fuerza |
|---|---|---|---|
| **Nacional / regulador sectorial** | ENARGAS, Secretaría de Energía, ENRE | NAG-200, NAG-201, Ley 27.424, Ley 19.587 y Dto. 351/79 | Obligatoria, prevalece en su materia |
| **Técnica de referencia** | AEA, IRAM | AEA 90364 (todas sus partes), IRAM 11601/11603/11604/11605, IRAM 2005, IRAM 3517 | Obligatoria cuando la adopta la prestadora o el municipio |
| **Prestadora del servicio** | Distribuidora de agua/cloaca, gas y electricidad | Reglamento de instalaciones sanitarias, condiciones de conexión eléctrica y de gas | Obligatoria para obtener el servicio |
| **Municipal / provincial** | Municipalidad de Santa Rosa, Provincia de La Pampa | Código de Edificación de Santa Rosa (Ord. 1581/95 y modif.), reglamentaciones de bomberos y de la APA | Obligatoria para el permiso de obra y el final de obra |

## 0.2 Situación particular de Santa Rosa, La Pampa

Este es el punto donde más se equivoca un estudio que trabaja con manuales porteños:

- **Sanitarias.** Las tablas y criterios de este documento provienen de la **Guía AySA / ERAS** (heredera de las Normas y Gráficos OSN). Es la referencia técnica más completa y difundida del país, y la que usan de hecho la mayoría de los proyectistas argentinos. **Pero no es la norma vigente en La Pampa.** Antes de presentar, verificar el reglamento de la prestadora local de agua y cloaca de Santa Rosa y las exigencias de la **Administración Provincial del Agua (APA)** de La Pampa, especialmente en: volumen mínimo de reserva, exigencia de tanque de bombeo, tratamiento de efluentes fuera de radio servido y destino del pluvial. `[verificar en reglamento de la prestadora local y en normativa de la APA - La Pampa]`
- **Gas.** Aquí **no hay ambigüedad**: rige ENARGAS con NAG-200 (instalaciones internas domiciliarias) y NAG-201 (redes/instalaciones de mayor porte). La prestadora de la región pampeana es **Camuzzi Gas Pampeana**. `[verificar en la distribuidora que efectivamente presta servicio en la parcela]`
- **Electricidad.** Rige **AEA 90364** en todo el territorio nacional. La aprobación de la conexión y la potencia contratada dependen de la distribuidora local. En Santa Rosa la prestación eléctrica está a cargo de una cooperativa eléctrica local y/o de la administración provincial de energía. `[verificar prestadora y su reglamento de conexión antes de definir la sala de medidores]`
- **Incendio.** No existe un código nacional único de edificación. Los criterios que se usan como referencia son el **Decreto 351/79 (Anexo VII, Ley 19.587 de Higiene y Seguridad)**, el **Código de Edificación de CABA con sus Reglamentos Técnicos** (que es la referencia más moderna y detallada del país) y las **normas IRAM de la serie 3500**. Para Santa Rosa: **verificar exigencias del Código de Edificación municipal y de la Dirección de Bomberos de La Pampa.** `[verificar en Código de Edificación de Santa Rosa y en la autoridad de bomberos provincial]`
- **Térmica.** Salvo que el municipio haya adoptado expresamente las IRAM 11600, su cumplimiento no es exigible legalmente; **pero es exigible técnicamente**: Santa Rosa tiene 1.394 grados-día base 18 °C (ver Capítulo 6) y una vivienda sin aislación en esa zona es un pasivo económico para el comitente y un problema de condensación para el estudio.

## 0.3 Regla de oro del estudio

> Antes de dibujar un solo caño, **hacer la consulta de factibilidad**: agua/cloaca (diámetro y presión disponible de conexión), gas (caudal disponible y presión de servicio), electricidad (potencia disponible y tipo de suministro, monofásico o trifásico). **Los tres datos condicionan el proyecto completo.** Sin ellos, cualquier dimensionamiento es una suposición.

---

# 1. SANITARIAS — AGUA FRÍA Y CALIENTE

## 1.1 Dotaciones y consumos de referencia

### 1.1.1 Consumo por habitante y día en conjuntos urbanos

Valores de la Guía AySA/ERAS, apartado 2.9.1.1 — se usan para **loteos, barrios y evaluación de la red**, no para dimensionar el tanque de un edificio:

| Tipología | Dotación (l/hab/día) |
|---|---|
| Grandes ciudades | 500 |
| Poblaciones menores a 50.000 hab. | 350 |
| Áreas rurales | 150 |

> **Nota para Santa Rosa:** la ciudad supera los 50.000 habitantes, por lo que en la lógica de la tabla corresponde el valor de "grandes ciudades" o un valor intermedio. Para estudios de red y factibilidad de loteo, **verificar la dotación de diseño que use la prestadora local** — típicamente entre 250 y 400 l/hab/día en el interior. `[verificar en normativa de la APA - La Pampa]`

### 1.1.2 Dotaciones por destino (valores de proyecto de uso corriente)

Estos valores **no** figuran en la Guía AySA/ERAS actualizada (que reemplazó el criterio de dotación por el de balance de caudales). Son los valores clásicos de OSN / Nisnovich, muy usados todavía en el interior y en muchos reglamentos municipales. Usarlos como **verificación cruzada** del método de balance de caudales, no como método único.

| Destino | Dotación de referencia | Unidad |
|---|---|---|
| Vivienda unifamiliar / departamento | 200 – 250 | l/hab/día |
| Vivienda económica / social | 150 – 200 | l/hab/día |
| Oficinas | 50 – 60 | l/persona/día |
| Locales comerciales | 6 – 10 | l/m²/día |
| Hotel (por cama) | 200 – 300 | l/cama/día |
| Restaurante | 30 – 60 | l/cubierto/día |
| Escuela sin internado | 40 – 50 | l/alumno/día |
| Clínica / sanatorio | 500 – 800 | l/cama/día |
| Gimnasio con duchas | 30 – 50 | l/usuario/día |
| Riego de jardín | 2 – 8 | l/m²/día |
| Lavado de auto | 100 – 150 | l/auto |

`[verificar en el reglamento de la prestadora local: algunos municipios fijan dotaciones propias de cumplimiento obligatorio]`

### 1.1.3 Ocupación teórica de una vivienda

Para pasar de superficie a habitantes, el criterio corriente en el proyecto argentino:

| Local | Ocupación teórica |
|---|---|
| Dormitorio principal (≥ 9 m²) | 2 personas |
| Dormitorio secundario | 1 – 2 personas |
| Monoambiente | 2 personas |

Regla práctica: **N.º de habitantes = N.º de dormitorios + 1**. Para un edificio con mezcla de tipologías, se computa unidad por unidad.

---

## 1.2 Caudales por artefacto y presiones mínimas

### 1.2.1 Caudales unitarios (qu) — artefactos domésticos

Fuente: Guía AySA/ERAS, apartado 2.9.1.2. Son los **valores máximos de época invernal** y sirven para dimensionar la distribución.

| Artefacto | qu total (l/s) | qu agua fría (l/s) | qu agua caliente (l/s) |
|---|---|---|---|
| Inodoro con válvula automática | 1,50 | 1,50 | — |
| Inodoro con depósito (DAI) | 0,20 | 0,08 | 0,12 |
| Bañera | 0,30 | 0,12 | 0,18 |
| Receptáculo de ducha | 0,30 | 0,12 | 0,18 |
| Bidet | 0,20 | 0,08 | 0,12 |
| Lavatorio | 0,20 | 0,08 | 0,12 |
| Pileta de cocina | 0,20 | 0,08 | 0,12 |
| Pileta de lavar | 0,20 | 0,08 | 0,12 |
| Máquina lavavajillas | 0,20 | 0,20 | — |
| Máquina lavarropas | 0,20 | 0,20 | — |

> **Ojo con la columna de agua fría/caliente:** la Guía descompone el caudal según la mezcla. La proporción se calcula con:
>
> **% Agua Fría = (Tu_AC − Te_AF) / (Ts_AC − Te_AF)**
>
> donde Ts_AC = temperatura de salida del sistema de ACS, Tu_AC = temperatura de uso, Te_AF = temperatura de entrada de agua fría.
>
> *Ejemplo de la Guía:* Ts=70 °C, Tu=35 °C, Te=10 °C → %AF = (35−10)/(70−10) = 0,42 = 42 %. Para una ducha de 0,30 l/s el agua fría aporta 0,30 × 0,42 = 0,125 l/s.
>
> **Consecuencia para Santa Rosa:** en invierno la temperatura de entrada de agua fría es más baja que 10 °C en varios días del año, lo que **aumenta** la proporción de agua caliente en la mezcla. Es una de las razones por las que en La Pampa el acumulador de ACS debe dimensionarse con más holgura que en el AMBA.

### 1.2.2 Caudales unitarios — artefactos de uso no doméstico

Fuente: Guía AySA/ERAS, apartado 2.9.1.3.

| Artefacto | qu (l/s) |
|---|---|
| Válvula de mingitorio | 0,15 |
| Pileta de cocina industrial | 0,50 |
| Lavavajillas industrial | 0,40 |
| Lavarropas industrial | 0,50 |
| Lavachatas | 1,20 |

### 1.2.3 Presiones mínimas en el artefacto

Fuente: Guía AySA/ERAS, apartado 2.9.1.4. **Este es el dato que fija la altura del tanque.**

| Artefacto | Presión mínima (kg/cm² = bar ≈ 10 m.c.a.) | Equivalente en m.c.a. |
|---|---|---|
| Lavatorio y bidet | 0,60 | 6,0 |
| Canilla de servicio | 0,60 | 6,0 |
| Pileta de lavar y de cocina | 0,60 | 6,0 |
| Bañera y receptáculo de ducha | 0,60 | 6,0 |
| Duchas individuales | 0,60 | 6,0 |
| Máquina lavadora | 0,30 | 3,0 |
| Inodoro con depósito | 0,60 | 6,0 |
| **Inodoro con válvula** | **1,50** | **15,0** |
| Mingitorio con válvula | 0,90 | 9,0 |
| Lavavajillas industrial | 0,90 | 9,0 |
| Lavarropas industrial | 0,90 | 9,0 |
| Lavachatas | 1,50 | 15,0 |
| Calentador instantáneo (calefón) | 1,00 | 10,0 |

> **Regla de proyecto:** la presión de referencia para fijar la altura del tanque en vivienda es **6 m.c.a. sobre el artefacto más alto y más alejado**, más las pérdidas de carga del recorrido. Si hay calefón instantáneo, sube a 10 m.c.a. Si hay inodoros con válvula (uso comercial), sube a 15 m.c.a. y en la práctica **obliga a presurización**.
>
> Muchos reglamentos y manuales del interior usan **20 m.c.a. como piezométrica mínima en el punto más alto** en instalaciones de edificios. Es un criterio más exigente y más seguro para calefones y termotanques modernos. `[verificar el valor exigido por la prestadora local antes de fijar la cota de tanque]`

### 1.2.4 Carga máxima admisible

Fuente: Guía AySA/ERAS, apartado 2.14.

- **Carga máxima: 45 m.c.a.**
- Si se supera (edificios de altura excepcional), hay tres soluciones admitidas:
  1. **Tanques de reserva intermedios**, divididos en dos secciones con cañerías de limpieza, alimentados por bombeo o desde el tanque superior. Capacidad del tanque intermedio que actúa a la vez como bombeo y reserva: los servicios que surte **+ 1/5 como mínimo del tanque más elevado que alimente**.
  2. **Tanque intermedio reductor de presión**: volumen mínimo igual a 1/5 de la reserva total diaria de los artefactos que alimente y **no menor de 2.000 litros**, dividido en 2 secciones con entrada de agua independiente a cada sección.
  3. **Válvulas reductoras-reguladoras de presión** certificadas según **IRAM 2634:2005**, con al menos dos ramales regulados iguales más uno de reserva, con válvulas de maniobra, limpieza, retención, seguridad por sobrepresión, filtros, purga automática de aire y manómetros. Grupo acústico I (≤ 20 dBA). Recinto de acceso común con desagüe de piso.

- **Dispositivos anti-ariete:** obligatorios en bajadas a válvulas de limpieza de inodoros con **carga estática superior a 30 m**, a diafragma o vejiga, ubicados en el local sanitario.

> **Traducción a un PB+9:** con entrepisos de 2,80 m, la altura desde el tanque a la planta baja ronda los 30-32 m. **Estamos justo por debajo del límite de 45 m.c.a., pero por encima del umbral de 30 m que dispara el anti-ariete.** En PB+9 típicamente NO hace falta tanque intermedio, pero SÍ conviene verificar la presión en el primer piso: si supera 40 m.c.a., poner reductora de presión por unidad o por sector de bajada (los tres o cuatro pisos inferiores).

---

## 1.3 Simultaneidad: dos métodos coexistentes

### 1.3.1 Método de la Guía AySA/ERAS — coeficiente K

Es el método vigente y el que hay que usar para tramitar. Procedimiento (apartado 2.9.2):

**Paso 1 — Caudal máximo instantáneo probable:**

> **Q_max = Σ (n × qu)**  [l/s]

donde n = cantidad de cada artefacto y qu su caudal unitario (tabla 1.2.1).

**Paso 2 — Coeficiente de simultaneidad base:**

> **Kc = 1 / (n − 1)^0,5**

donde n = número **total** de artefactos, que debe ser ≥ 2.

**Paso 3 — Coeficiente de mayoración según tipología:**

| Tipología del proyecto | a |
|---|---|
| Oficinas privadas y vivienda individual | 1 |
| **Viviendas multifamiliares**, oficinas públicas, centros educativos | **2** |
| Edificios públicos, aeropuertos, centros de salud | 3 |
| Centros de detención, deportivos, comerciales, terminales de pasajeros | 4 |

**Paso 4 — Coeficiente final y caudal de cálculo:**

> **K = Kc × a**   (y en la práctica se acota **K ≤ 1**)
>
> **Qc = Q_max × K**  [l/s]

> **Atención al detalle que se pasa por alto:** en recintos sanitarios de **vivienda** con inodoros de válvula automática, la Guía indica tomar **solamente el caudal de la válvula** para el cálculo de simultaneidad. En **baños públicos** con válvulas automáticas, en cambio, se consideran todos los artefactos con sus caudales respectivos.

### 1.3.2 Método Hunter — unidades de gasto (UG)

Sigue siendo el método más difundido en la bibliografía (Nisnovich, manuales de ingeniería sanitaria, IMSS, y su descendiente moderno **UNE 149201** en España). Sirve muy bien como **verificación cruzada** y es lo que muchos programas de cálculo usan internamente.

**Concepto:** Hunter define la "unidad de gasto" o "unidad mueble" (UG / fixture unit) como el consumo de un lavatorio doméstico típico durante un uso. Cada artefacto recibe un peso proporcional a su caudal, frecuencia y duración de uso.

**Unidades de gasto de uso corriente** (valores de la tradición Hunter; existen variantes según la fuente — **verificar contra la tabla de la bibliografía que se adopte**):

| Artefacto | UG — uso privado | UG — uso público |
|---|---|---|
| Lavatorio | 1 | 2 |
| Bidet | 1 | 2 |
| Bañera / ducha | 2 | 4 |
| Inodoro con depósito | 3 | 5 |
| Inodoro con válvula | 6 | 10 |
| Mingitorio con válvula | — | 5 |
| Pileta de cocina | 2 | 4 |
| Lavavajillas | 2 | 4 |
| Lavarropas | 2 | 4 |
| Pileta de lavar | 2 | 4 |
| Canilla de servicio Ø13 | 2 | 3 |
| **Baño completo privado (conjunto)** | **6** | — |
| **Toilette privada (conjunto)** | **3** | — |

`[verificar en Nisnovich, "Instalaciones Sanitarias" o en la tabla de Hunter que adopte el proyecto — las tablas difieren entre fuentes]`

**Conversión UG → caudal:** se hace por la curva de Hunter. Aproximación práctica utilizable para vivienda colectiva:

| Total UG | Caudal probable aproximado (l/s) |
|---|---|
| 10 | 0,60 |
| 20 | 0,95 |
| 40 | 1,50 |
| 60 | 1,95 |
| 100 | 2,70 |
| 150 | 3,50 |
| 200 | 4,20 |
| 300 | 5,50 |
| 500 | 7,60 |
| 750 | 10,0 |
| 1.000 | 12,3 |

`[valores aproximados de la curva clásica de Hunter — verificar contra la curva de la fuente adoptada antes de usar en documentación]`

**Método español UNE 149201 (útil como sanity check):** para viviendas,
> Q_cálculo = 0,682 × (Q_total)^0,45 − 0,14  para Q_total > 1,0 l/s
> Q_cálculo = Q_total  para Q_total ≤ 0,5 l/s

Es más moderno que Hunter y da valores más ajustados para grifería de bajo caudal. Sirve como contraste, no para tramitar en Argentina.

### 1.3.3 Cuál usar

| Situación | Método |
|---|---|
| Trámite ante prestadora argentina | **Coeficiente K (AySA/ERAS)** — es el que exige la memoria |
| Verificación cruzada / segunda opinión | Hunter |
| Grifería moderna de bajo caudal, edificios con medición individual | UNE 149201 como contraste |
| Discusión con el instalador | Tabla rápida de diámetros (§1.4) |

---

## 1.4 Diámetros: método de cálculo y tabla rápida

### 1.4.1 Procedimiento de la Guía AySA/ERAS (apartado 2.12.1)

**Velocidades de escurrimiento admisibles:**

| Rango de diámetro | Velocidad admisible |
|---|---|
| 0,013 m a 0,060 m (13 a 60 mm) | **1 a 3 m/s** |
| 0,075 m a 0,200 m (75 a 200 mm) | **1,5 a 2 m/s** |

**Sección necesaria:**

> **Ae [cm²] = (Qc / 1000) / (Ve / 100)**
>
> con Qc en l/s y Ve en m/s. Se adopta el diámetro interior comercial igual o mayor.

**Pérdida de carga distribuida — Hazen-Williams:**

> **J = 1 / (0,287 × C)^1,85 × (Qc^1,85 / D^4,87)**

**Pérdidas localizadas:**

> **Js = Ks × V² / (2g)**

**Coeficientes Ks (Tabla Nº 7 de la Guía):**

| Accesorio | Ks |
|---|---|
| Griferías | 9,18 |
| Llave de paso | 9,18 |
| Curva a 45° | 0,43 |
| Curva a 90° | 0,81 |
| Codo a 90° | 1,35 |
| Te, paso recto | 1,00 |
| Te, salida lateral | 1,62 |
| Te, entrada central y salidas laterales | 3,00 |
| Uniones | 0,10 |
| Válvula esclusa | 0,17 |
| Reducciones | 0,75 |
| Tubo saliente | 1,00 |

> **Lo que más se subestima:** los Ks de grifería y llave de paso (9,18) son enormes. En un baño con dos llaves de paso y grifería, las pérdidas localizadas pueden superar a las distribuidas. Por eso las bajadas "calculadas justas" fallan en el último piso.

### 1.4.2 Tabla rápida de diámetros por cantidad de artefactos

Guía de predimensionado para **agua fría en vivienda, alimentación por tanque elevado**, con velocidad de 1,5–2 m/s. **Verificar siempre por cálculo.**

| Tramo | Artefactos servidos (orientativo) | Ø nominal termofusión PPR | Ø nominal cobre / hierro | Ø interior aprox. |
|---|---|---|---|---|
| Conexión a artefacto individual | 1 | 20 mm | 13 mm (½") | ~13 mm |
| Ramal de baño (lavatorio + bidet + inodoro) | 2 – 3 | 20 mm | 13 mm (½") | ~13 mm |
| Ramal a baño completo | 4 – 5 | 25 mm | 19 mm (¾") | ~19 mm |
| Ramal a baño + toilette | 6 – 8 | 32 mm | 19 mm (¾") | ~19 – 22 mm |
| Bajada a un departamento (1 baño + cocina) | 6 – 9 | 25 – 32 mm | 19 mm (¾") | ~19 mm |
| Bajada a un departamento (2 baños + cocina + lavadero) | 10 – 14 | 32 mm | 25 mm (1") | ~25 mm |
| Montante que sirve 3 – 4 departamentos | 30 – 50 | 40 mm | 32 mm (1¼") | ~32 mm |
| Montante que sirve 5 – 8 departamentos | 50 – 90 | 50 mm | 38 mm (1½") | ~38 mm |
| Montante / colector 10 – 20 departamentos | 100 – 200 | 63 mm | 51 mm (2") | ~50 mm |
| Colector general 30 – 50 departamentos | 250 – 450 | 75 – 90 mm | 63 mm (2½") | ~63 mm |

> **Advertencia crítica sobre PPR:** el diámetro nominal del PPR es el **exterior**, no el interior. Un PPR de 25 mm PN20 tiene un interior de apenas ~16,6 mm; un PPR de 32 mm PN20 tiene ~21,2 mm de interior. **Un caño de PPR de 25 mm NO equivale a un ¾" de hierro.** Este error es el origen de la mayoría de las quejas de "poca presión" en obras nuevas.
>
> La Guía lo dice expresamente (apartado 2.7): *"Para el caso de empleo de materiales plásticos, los diámetros nominales adoptados y que se indiquen en la documentación gráfica corresponderán a aquellos que garanticen un diámetro interior real mayor o igual al diámetro nominal de la tabla."*

**Tabla de equivalencias reales PPR (PN20, fusión) — dato de proyecto:**

| PPR Ø exterior nominal | Espesor típico PN20 | Ø interior aprox. | Equivale aprox. a |
|---|---|---|---|
| 20 mm | 3,4 mm | 13,2 mm | ½" |
| 25 mm | 4,2 mm | 16,6 mm | entre ½" y ¾" |
| 32 mm | 5,4 mm | 21,2 mm | ¾" |
| 40 mm | 6,7 mm | 26,6 mm | 1" |
| 50 mm | 8,3 mm | 33,4 mm | 1¼" |
| 63 mm | 10,5 mm | 42,0 mm | 1½" |
| 75 mm | 12,5 mm | 50,0 mm | 2" |
| 90 mm | 15,0 mm | 60,0 mm | 2¼" |
| 110 mm | 18,3 mm | 73,4 mm | 3" |

`[valores nominales de mercado; verificar contra la ficha técnica del fabricante que se especifique — cambian con la serie SDR/PN]`

---

## 1.5 Determinación de la reserva: el método del balance de caudales

La Guía AySA/ERAS **abandonó** el criterio antiguo de "reserva = dotación × habitantes" y adoptó un **balance entre lo que consume el edificio y lo que entrega la conexión**. Esto es más racional pero exige un dato que hay que pedir: **el caudal que la prestadora garantiza en la conexión**.

### 1.5.1 Procedimiento (apartado 2.10.2)

1. Calcular **Qc** (caudal de cálculo del edificio) por el método K.
2. Pedir a la prestadora el **caudal de ingreso** de la conexión, en función de su diámetro y de la presión disponible sobre el nivel de vereda.
3. Calcular el **déficit de caudal**:
   > **Dc = Qc − Q_conexión**  [l/s → convertir a m³/h]
4. Adoptar el **tiempo estimado de consumo máximo Tc**: entre **1 y 4 horas** según las características de la instalación (criterio del proyectista, debe justificarse).
5. Calcular:
   > **Reserva Total Diaria de Diseño = Dc × Tc**  [m³]
6. Adoptar la **Reserva Total Diaria a Ejecutar** redondeando hacia arriba a un volumen comercial de tanque.

### 1.5.2 Ejemplo de la propia Guía (vivienda unifamiliar)

| Concepto | Valor |
|---|---|
| Artefactos: 2 lavatorios, 1 bañera, 2 inodoros c/depósito, 1 bidet, 1 pileta de cocina, 1 pileta de lavar, 1 receptáculo de ducha | n = 9 |
| Q_total (suma de qu) | 2,00 l/s |
| Kc = 1/(9−1)^0,5 | 0,35 |
| a (vivienda única) | 1 |
| K | 0,35 |
| **Qc = 2,00 × 0,35** | **0,71 l/s** (42,43 l/min) |
| Caudal de conexión Ø 0,019 m con 5 m.c.a. | 0,60 l/s |
| **Dc = 0,71 − 0,60** | **0,11 l/s = 0,39 m³/h** |
| Tc adoptado | 2,00 h |
| **Reserva de diseño = 0,39 × 2** | **0,77 m³** |
| **Reserva a ejecutar** | **1,00 m³** |

### 1.5.3 Distribución entre reserva y bombeo

Fuente: Guía AySA/ERAS, apartado 2.11.3:

> **Los tanques de bombeo y reserva deben poseer un volumen mínimo de 1/3 de la Reserva Total Diaria.**

Es decir: si la Reserva Total Diaria es V, el **tanque de reserva (elevado) ≥ V/3** y el **tanque de bombeo (cisterna) ≥ V/3**. El criterio de proyecto habitual en edificios es más generoso:

| Criterio | Tanque de bombeo (cisterna) | Tanque de reserva (elevado) |
|---|---|---|
| **Mínimo normativo** | 1/3 de RTD | 1/3 de RTD |
| **Práctica corriente en edificios** | 2/3 de RTD | 1/3 de RTD |
| **Práctica alternativa** | 1/2 de RTD | 1/2 de RTD |

> **Razón de fondo:** el tanque elevado es carga muerta en la cubierta y ocupa altura útil; el de bombeo va en subsuelo o PB donde el volumen es barato. Por eso se tiende a cargar el volumen abajo. **Pero el tanque elevado no puede achicarse demasiado**: si es muy chico, la bomba arranca y para permanentemente (ciclado), lo que destruye el motor y molesta a los vecinos. **Regla práctica: el tanque elevado debe permitir al menos 10-15 minutos de consumo pico sin que arranque la bomba.**

### 1.5.4 Verificación cruzada por dotación

Como el método de balance depende de un dato de la prestadora que a veces no llega a tiempo, conviene hacer siempre el cálculo clásico en paralelo:

> **RTD = N_habitantes × dotación [l/hab/día]**

y adoptar **el mayor de los dos**. Muchos reglamentos del interior siguen exigiendo el criterio de **reserva mínima de 24 horas de consumo**. `[verificar cuál criterio exige la prestadora de Santa Rosa]`

---

## 1.6 Requisitos constructivos de los tanques

Fuente: Guía AySA/ERAS, apartado 2.11. **Estos son los detalles que se olvidan en el plano y aparecen en la inspección.**

| Requisito | Valor |
|---|---|
| Pendiente de fondo hacia el desagüe | mínimo **1:25** (los cilíndricos prefabricados están eximidos pero debe garantizarse pendiente) |
| Chaflán unión paredes-fondo | 45°, mínimo **0,20 m** |
| Tapa hermética sumergida, luz mínima | **0,50 m**, ubicada entre 0,40 y 0,60 m medidos del fondo al filo inferior de la tapa |
| Tapa de inspección en la cubierta | **0,25 × 0,25 m**, a no más de 0,15 m de la válvula a flotante o pico de entrada, sellada y precintada |
| Escalera a la cubierta | exigible si el desnivel entre cubierta y piso > 2,50 m; **no puede amurarse al tanque por debajo del nivel de agua** |
| Plataforma de maniobra | ancho 0,70 m, baranda 0,90 m, debe sobrepasar 0,25 m los costados de la tapa sumergida. No exigible si la maniobra es cómoda (altura máxima eje tapa-piso: 1,40 m) |
| **División en secciones** | **Tanques de bombeo y reserva de 4.000 litros o más deben dividirse en dos o más secciones iguales** |
| Separación de medianera | **0,80 m** mínimo del filo interior de pared medianera o de paredes propias que den a terraplén |
| Separación reserva sanitaria / reserva de incendio | **0,50 m** libre mínimo |
| Altura libre bajo tanques | **0,60 m** mínimo |
| Altura libre sobre tanques | **0,40 m** mínimo |
| **Tanques enterrados** | **PROHIBIDOS** (en general) |
| Prohibición de conexión de colector | **por lateral de tanques** — el colector sale por el fondo |
| Caño ventilador de tanque hermético | Ø 3 rangos menor que el colector, **mínimo 0,025 m**, curvado y con abertura hacia abajo, al aire libre, sobreelevado **2,50 m** como mínimo sobre piso frecuentable, con malla fina de bronce |
| Desborde | **prohibido en general**; obligatorio en tanque de expansión y en tanques expuestos a contaminación, siempre 0,10 m por debajo de la válvula flotante o pico |
| Tanques ≤ 1.000 l | se tolera sustituir tapa sumergida por tapa superior de luz mínima 0,50 m |

### 1.6.1 Válvulas de limpieza (Tabla Nº 5 de la Guía)

Todo tanque debe tener válvula de limpieza **en cada una de sus secciones** (excepto el de expansión). **No se permite llave de paso a válvula suelta; debe ser esclusa o de cuarto de vuelta.**

| Capacidad de la cuba (litros) | Válvula esclusa (m) | Llave de cuarto de vuelta (m) |
|---|---|---|
| Hasta 100 | 0,013 | 0,019 |
| 101 a 500 | 0,019 | 0,025 |
| 501 a 1.000 | 0,025 | 0,032 |
| 1.001 a 2.000 | 0,032 | 0,038 |
| 2.001 a 3.000 | 0,038 | 0,050 |
| Más de 3.000 | 0,050 | 0,060 |

> **Prohibición expresa:** no se puede conectar directamente el desagüe de limpieza del tanque a una pileta de piso ni a cualquier otro desagüe. Debe descargar a pileta de piso **abierta** o boca de desagüe abierta, con corte de aire.

---
