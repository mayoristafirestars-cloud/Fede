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

## 1.7 EJEMPLO RESUELTO Nº 1 — Reserva y bombeo de un edificio PB+9 con 40 departamentos

### Datos de partida

| Dato | Valor |
|---|---|
| Edificio | PB + 9 pisos (10 plantas sobre nivel) + 1 subsuelo de cocheras |
| Unidades | 40 departamentos: 12 de 1 dormitorio, 20 de 2 dormitorios, 8 de 3 dormitorios |
| Altura de entrepiso | 2,90 m (piso a piso) |
| PB comercial | 2 locales con toilette |
| Ubicación | Santa Rosa, La Pampa |
| Conexión otorgada por la prestadora | Ø 0,050 m (2"), presión sobre vereda 12 m.c.a. → **Q_conexión = 4,20 l/s** `[valor supuesto: PEDIR EL DATO REAL A LA PRESTADORA]` |

### Paso 1 — Artefactos y caudal máximo instantáneo

**Departamento de 1 dormitorio (12 unidades):** 1 lavatorio, 1 inodoro DAI, 1 bidet, 1 ducha, 1 pileta de cocina, 1 lavarropas = **6 artefactos**

| Artefacto | Cant. | qu (l/s) | Subtotal |
|---|---|---|---|
| Lavatorio | 1 | 0,20 | 0,20 |
| Inodoro DAI | 1 | 0,20 | 0,20 |
| Bidet | 1 | 0,20 | 0,20 |
| Ducha | 1 | 0,30 | 0,30 |
| Pileta de cocina | 1 | 0,20 | 0,20 |
| Lavarropas | 1 | 0,20 | 0,20 |
| **Total** | **6** | | **1,30 l/s** |

**Departamento de 2 dormitorios (20 unidades):** agrega toilette (1 lavatorio + 1 inodoro) → **8 artefactos**, Q_total = 1,30 + 0,40 = **1,70 l/s**

**Departamento de 3 dormitorios (8 unidades):** 2 baños completos + toilette + cocina + lavadero → **12 artefactos**, Q_total = **2,50 l/s**

**Locales PB (2):** 1 toilette c/u (lavatorio + inodoro) + 1 pileta = 3 artefactos c/u, Q = 0,60 l/s c/u

**Servicios generales:** 2 canillas de servicio (0,20 l/s c/u) + 1 pileta de lavar de portería = 3 artefactos, Q = 0,60 l/s

**Totales del edificio:**

| Concepto | Artefactos (n) | Q_total (l/s) |
|---|---|---|
| 12 dptos. de 1 dorm. | 12 × 6 = 72 | 12 × 1,30 = 15,60 |
| 20 dptos. de 2 dorm. | 20 × 8 = 160 | 20 × 1,70 = 34,00 |
| 8 dptos. de 3 dorm. | 8 × 12 = 96 | 8 × 2,50 = 20,00 |
| 2 locales | 6 | 1,20 |
| Servicios generales | 3 | 0,60 |
| **TOTAL EDIFICIO** | **n = 337** | **Q_max = 71,40 l/s** |

### Paso 2 — Coeficiente de simultaneidad

> Kc = 1 / (n − 1)^0,5 = 1 / (337 − 1)^0,5 = 1 / 336^0,5 = 1 / 18,33 = **0,0546**

Coeficiente de mayoración: **a = 2** (viviendas multifamiliares)

> **K = Kc × a = 0,0546 × 2 = 0,1092**

### Paso 3 — Caudal de cálculo

> **Qc = Q_max × K = 71,40 × 0,1092 = 7,80 l/s = 28,07 m³/h = 468 l/min**

### Paso 4 — Balance de caudales y reserva

| Concepto | Valor |
|---|---|
| Consumo máximo del edificio, Qc | 7,80 l/s = 28,07 m³/h |
| Caudal de ingreso de la conexión | 4,20 l/s = 15,12 m³/h |
| **Déficit de caudal, Dc** | **3,60 l/s = 12,95 m³/h** |
| Tiempo estimado de consumo máximo, Tc (adoptado: edificio de vivienda con pico matinal y vespertino marcados) | **3,0 horas** |
| **Reserva Total Diaria de Diseño = Dc × Tc = 12,95 × 3,0** | **38,85 m³** |
| **Reserva Total Diaria a Ejecutar** | **40,00 m³** |

### Paso 5 — Verificación cruzada por dotación

Habitantes teóricos: 12×2 + 20×3 + 8×4 = 24 + 60 + 32 = **116 habitantes**

> RTD = 116 hab × 250 l/hab/día = 29.000 l = **29,0 m³**

El método de balance da **40 m³** y el de dotación **29 m³**. **Se adopta el mayor: 40 m³.** (Si la prestadora de Santa Rosa exigiera reserva de 24 h de consumo, el criterio de dotación quedaría cubierto con holgura.)

### Paso 6 — Reparto reserva / bombeo

| | Volumen | Verificación |
|---|---|---|
| Mínimo normativo por sección (1/3 de RTD) | 13,33 m³ | — |
| **Tanque de reserva elevado adoptado (1/3)** | **14,00 m³** | ≥ 13,33 ✓ |
| **Tanque de bombeo / cisterna adoptado (2/3)** | **26,00 m³** | ≥ 13,33 ✓ |
| **Total** | **40,00 m³** | ✓ |

**Configuración adoptada:**

- **Tanque elevado:** 14.000 l → **supera 4.000 l, obligatoriamente dividido en 2 secciones iguales de 7.000 l**, cada una con su válvula flotante, su llave de paso a válvula suelta y su válvula de limpieza. Válvula de limpieza: **0,050 m (esclusa) o 0,060 m (cuarto de vuelta)** según la Tabla Nº 5 (cuba > 3.000 l).
  - Solución constructiva: **2 tanques de hormigón armado de 7 m³** o **4 tanques de polietileno tricapa de 3.500 l** conectados de a dos con colector común. En Santa Rosa, con heladas frecuentes, **el tanque elevado va dentro de sala cerrada y aislada**, nunca a la intemperie sin protección.
- **Cisterna:** 26.000 l en subsuelo, en 2 secciones de 13.000 l, hormigón armado impermeabilizado, con tapa sumergida, escalera fija, ventilación Ø 0,025 m mínimo y válvulas de limpieza de 0,050/0,060 m.

### Paso 7 — Equipo de bombeo

**Caudal de bombeo (Qb):** criterio — llenar el tanque elevado en un tiempo razonable y responder al consumo pico.

> Qb ≥ Qc = 7,80 l/s → adoptamos **Qb = 8,0 l/s = 28,8 m³/h**

Verificación de tiempo de llenado del elevado: 14.000 l / (8,0 l/s) = 1.750 s = **29 minutos**. Razonable.

**Altura manométrica (Hm):**

| Componente | Valor |
|---|---|
| Altura geométrica: desde el nivel mínimo de la cisterna (subsuelo, −3,00 m) hasta el pelo de agua del tanque elevado. PB+9 × 2,90 m = 26,10 m + 3,00 m subsuelo + 3,50 m sala de tanques sobre última losa | **32,60 m** |
| Pérdidas distribuidas en la impulsión (Ø 63 mm PEAD o Ø 2" hierro galvanizado, L ≈ 40 m, Hazen-Williams C=140) | ≈ **3,5 m** |
| Pérdidas localizadas (válvula de retención, esclusa, 6 codos, junta elástica, salida) | ≈ **2,0 m** |
| Margen de seguridad (10 %) | ≈ **3,8 m** |
| **Hm total** | **≈ 42,0 m.c.a.** |

**Potencia hidráulica y de eje:**

> P_hidráulica [kW] = (ρ × g × Q × H) / 1000 = (1000 × 9,81 × 0,008 × 42,0) / 1000 = **3,30 kW**
>
> P_eje = P_hidr / η_bomba = 3,30 / 0,65 = **5,07 kW**
>
> P_motor = P_eje / η_motor = 5,07 / 0,88 = **5,76 kW ≈ 7,7 HP → adoptar motor de 7,5 kW (10 HP)**

**Configuración:** **dos bombas centrífugas idénticas, alternadas automáticamente**, cada una capaz de dar el 100 % del caudal. Una trabaja, la otra queda en reserva, con conmutación automática por tablero y alternancia por ciclos para igualar horas de marcha.

**Exigencias constructivas de la Guía (apartado 2.18):**
- Conexión de agua corriente **exclusiva** para el servicio de bombeo.
- **Junta elástica obligatoria** entre bomba y caño de impulsión.
- **Válvula de retención al pie** del caño de impulsión.
- **Apoyo antivibratorio** del equipo.
- Ubicación de equipo (tanque de bombeo y bomba) **en área común**.
- Bomba alejada **0,80 m como mínimo de la medianera**.
- Diámetro de impulsión dimensionado por caudal, altura manométrica y velocidad (§1.4.1).
- El colector del tanque de bombeo y la cañería de aspiración deben verificar la velocidad admisible.
- **Indicar en planos:** caudal de los equipos, altura manométrica, diámetro de impulsión y adjuntar memoria de cálculo.
- **Impulsiones mayores a 35 m.c.a.:** debe verificarse el **golpe de ariete** (presiones máximas y depresiones) y diseñar los elementos para minimizarlo. **En nuestro caso Hm = 42 m > 35 m → ES OBLIGATORIO el estudio de golpe de ariete y la previsión de un tanque hidroneumático o válvula anticipadora de onda en la impulsión.**

### Paso 8 — Verificación de presión en el artefacto más desfavorable

El artefacto más desfavorable es la **ducha del 9.º piso** (última planta de vivienda).

| Concepto | Valor |
|---|---|
| Cota de fondo del tanque elevado sobre la losa del 9.º | 3,50 m |
| Nivel mínimo de agua en el tanque (fondo + 0,20 m de reserva de succión) | 3,70 m |
| Cota de la ducha del 9.º sobre su piso | 2,10 m |
| **Altura estática disponible** | **3,70 − 2,10 = 1,60 m.c.a.** |

**❌ NO VERIFICA.** Se necesitan 6,0 m.c.a. mínimos en el artefacto.

**Soluciones posibles (esto es lo que hay que resolver en el anteproyecto, no en la obra):**

| Solución | Descripción | Cuándo conviene |
|---|---|---|
| **A — Elevar el tanque** | Llevar el fondo del tanque a **8,50 m** sobre la losa del 9.º (torre de tanque). Da 8,50 − 2,10 = 6,40 m.c.a. antes de pérdidas | Solo si el Código de Edificación municipal admite esa altura sobre el plano límite. **Verificar retiros y altura máxima en el Código de Santa Rosa.** Estéticamente pesado |
| **B — Grupo de presurización para los 2 últimos pisos** | Tanque elevado en cota razonable (3,50 m) que alimenta por gravedad los pisos 1.º a 7.º, y un **grupo hidropresor de velocidad variable** que toma del mismo tanque y presuriza los pisos 8.º y 9.º | **ES LA SOLUCIÓN CORRIENTE Y LA RECOMENDADA.** Menor impacto volumétrico, presión constante y regulada |
| **C — Presurización total desde cisterna** | Eliminar el tanque elevado y presurizar todo el edificio con grupo de velocidad variable desde la cisterna, con tanque de reserva bajo. La Guía lo admite expresamente (apartado 2.14): *"Podrá optarse también en reemplazar los tanques intermedios por un tanque con la reserva diaria en el nivel inferior contando con equipos presurizadores"* | Cuando no hay lugar en cubierta o el partido arquitectónico no admite la torre. **Contra: si se corta la luz, no hay agua.** Exige grupo electrógeno o al menos un tanque de reserva mínimo por gravedad |

**Adoptamos la solución B.** Ver §1.9.

### Paso 9 — Dimensionado del colector y bajadas

Con Qc = 7,80 l/s y velocidad de 2,0 m/s (rango 1,5–2 m/s para Ø > 75 mm):

> Ae = (7,80/1000) / (2,0/100) = 0,39 dm²... **cuidado con las unidades**. Aplicando la fórmula de la Guía tal cual: Ae [cm²] = (Qc/1000)/(Ve/100) = (7,80/1000)/(2,0/100) = 0,0078/0,02 = **0,39** → el resultado sale en dm², no en cm². Verificando directamente:
>
> **A = Q / V = 0,0078 m³/s / 2,0 m/s = 0,0039 m² = 39 cm²**
>
> **D = (4 × A / π)^0,5 = (4 × 0,0039 / 3,1416)^0,5 = 0,0705 m = 70,5 mm de diámetro interior**

**Colector general adoptado: Ø 90 mm PPR PN20 (interior 60 mm) → NO alcanza. Adoptar Ø 110 mm PPR PN20 (interior 73,4 mm) ✓, o Ø 75 mm (3") en hierro galvanizado / cobre.**

> **Este es exactamente el error que denunciamos en §1.4.2.** Quien hubiera puesto "PPR 90" pensando que equivale a 3" habría subdimensionado el colector general de un edificio de 40 unidades.

**Bajadas (montantes) de agua fría:** con 4 departamentos por piso y 10 plantas, cada montante sirve una columna de 10 unidades.
- Unidades servidas: 10 dptos. de 2 dorm. → n = 80 artefactos, Q_total = 17,0 l/s
- Kc = 1/(80−1)^0,5 = 0,1125; K = 0,1125 × 2 = 0,225
- Qc_montante = 17,0 × 0,225 = **3,83 l/s**
- A = 0,00383/2,0 = 0,00191 m² = 19,1 cm² → **D = 49,3 mm interior**
- **Montante adoptada: Ø 75 mm PPR PN20 (interior 50 mm) ✓** o 2" hierro galvanizado.

### Resumen del ejemplo

| Elemento | Resultado |
|---|---|
| Caudal de cálculo del edificio | **7,80 l/s** |
| Reserva Total Diaria | **40 m³** |
| Tanque elevado | **14 m³**, 2 secciones de 7 m³ |
| Cisterna de bombeo | **26 m³**, 2 secciones de 13 m³ |
| Bombas | **2 × 7,5 kW**, Q = 8,0 l/s, Hm = 42 m.c.a., alternadas |
| Estudio de golpe de ariete | **OBLIGATORIO** (Hm > 35 m) |
| Colector general | **Ø 110 mm PPR PN20** (int. 73,4 mm) |
| Montantes | **Ø 75 mm PPR PN20** (int. 50 mm) |
| Presurización | **Grupo hidropresor para pisos 8.º y 9.º** |
| Válvulas reductoras | **Verificar en pisos 1.º a 3.º**: presión estática desde el tanque elevado (~30 m) más las alturas → puede superar los 40 m.c.a. |

---

## 1.8 Equipos de bombeo — criterios adicionales

### 1.8.1 Selección

| Parámetro | Criterio |
|---|---|
| Caudal de la bomba | ≥ Qc del edificio. Verificar que el tiempo de llenado del tanque elevado esté entre 20 y 60 min |
| Altura manométrica | H_geométrica + pérdidas distribuidas + pérdidas localizadas + 10 % de margen |
| Punto de funcionamiento | Debe caer en el **tercio central** de la curva de la bomba, cerca del punto de máximo rendimiento |
| Redundancia | **Siempre 2 bombas al 100 %** en edificios de vivienda colectiva. Nunca una sola |
| NPSH | NPSH_disponible ≥ NPSH_requerido + 0,5 m. **En cisternas enterradas con bomba en aspiración positiva (bomba por debajo del pelo de agua) el NPSH nunca es problema.** Evitar bombas en aspiración negativa |
| Arranque | Contactor con relé térmico + protección por falta de fase + sonda de nivel mínimo en cisterna (protección contra marcha en seco) |
| Control de nivel | Electrodos o sondas en tanque elevado (arranque/parada) y en cisterna (mínimo). **No usar flotantes mecánicos en edificios: fallan** |

### 1.8.2 Golpe de ariete

Obligatorio verificar cuando **Hm > 35 m.c.a.** (Guía AySA/ERAS 2.18).

Sobrepresión de Joukowsky (cierre instantáneo):
> **ΔH = (a × ΔV) / g**

donde a = celeridad de la onda (m/s), ΔV = variación de velocidad (m/s), g = 9,81 m/s².

Celeridad orientativa:

| Material de la impulsión | Celeridad a (m/s) |
|---|---|
| Acero / hierro galvanizado | 1.000 – 1.200 |
| Cobre | 1.200 – 1.300 |
| PEAD PE100 | 250 – 400 |
| PPR | 300 – 450 |
| PVC presión | 350 – 500 |

> **Consecuencia de proyecto:** una impulsión en **acero** genera 3 a 4 veces más sobrepresión que una en **PEAD**. En impulsiones largas y altas de edificios, el PEAD PE100 es una elección técnica, no solo económica.

**Medidas de mitigación:** válvula de retención de cierre lento o de clapeta amortiguada, tanque hidroneumático (membrana) en la impulsión, válvula anticipadora de onda, arranque/parada suave (variador de frecuencia o arrancador progresivo).

---

## 1.9 Grupos de presurización — cuándo y cómo

### 1.9.1 Cuándo hace falta

| Situación | ¿Presurización? |
|---|---|
| Tanque elevado da ≥ 6 m.c.a. sobre el artefacto más desfavorable, sin calefón instantáneo | **No** |
| Hay **calefón instantáneo** en la última planta y el tanque da menos de 10 m.c.a. | **Sí** (o cambiar a termotanque) |
| Hay **inodoros con válvula automática** (locales comerciales, oficinas) | **Sí** — requieren 15 m.c.a. |
| Últimos 1 a 3 pisos con altura de tanque insuficiente | **Sí**, presurización parcial (solución habitual) |
| No hay lugar en cubierta para el tanque elevado o el Código no permite la altura | **Sí**, presurización total desde cisterna |
| Grifería termostática, duchas de lluvia, columnas de hidromasaje | **Sí** — requieren presión estable, no solo suficiente |

### 1.9.2 Tipos de grupo

| Tipo | Descripción | Pro | Contra |
|---|---|---|---|
| **Hidroneumático clásico** | Bomba + tanque de membrana. Arranque/parada por presostato | Simple, barato | Ciclado, presión variable entre P_arranque y P_parada, tanque voluminoso |
| **Velocidad variable (VFD) — 1 bomba** | Bomba con variador de frecuencia y transductor de presión. Mantiene presión constante | Presión constante, ahorro energético 30-50 %, menos golpe de ariete | Más caro, requiere protección electrónica |
| **Velocidad variable multibomba** | 2 o 3 bombas con VFD en cascada | Redundancia + rendimiento en todo el rango de caudal | Costo, espacio |

> **Recomendación del estudio para PB+9:** **grupo de velocidad variable de 2 bombas** para presurización de los 2 o 3 últimos pisos, con pequeño tanque de membrana (20-50 l) de amortiguación. Alimentado desde el tanque elevado (no desde la red), con protección de marcha en seco.

### 1.9.3 Dimensionado del grupo de presurización parcial (continuación del Ejemplo Nº 1)

Presuriza pisos 8.º y 9.º = 8 departamentos (4 por piso).

- Artefactos: 8 × 8 = 64 → n = 64; Q_total = 8 × 1,70 = 13,60 l/s
- Kc = 1/(64−1)^0,5 = 0,126; K = 0,126 × 2 = 0,252
- **Qc = 13,60 × 0,252 = 3,43 l/s = 12,3 m³/h**
- Altura a vencer: presión requerida en la ducha del 9.º (6 m.c.a.) + altura del artefacto sobre la aspiración (2,10 − 3,70 = −1,60, es decir el tanque está por encima, aporta 1,60 m) + pérdidas de carga en el tramo (≈ 4 m)
- **Hm = 6,0 + 4,0 − 1,6 = 8,4 m.c.a. → adoptar Hm = 15 m.c.a.** para dar margen y cubrir el caso de tanque en nivel mínimo y consumo simultáneo.
- P_eje = (1000 × 9,81 × 0,00343 × 15) / (1000 × 0,60) = **0,84 kW → 2 bombas de 1,1 kW (1,5 HP) con VFD**

---

## 1.10 Colectores, bajadas, montantes y válvulas

### 1.10.1 Reglas de la Guía AySA/ERAS (apartado 2.17)

| Regla | Detalle |
|---|---|
| Llave de paso a válvula suelta general | En edificios **con** micromedición individual: ubicada **después de la medición** y en la entrada de cada unidad locativa |
| Llave por bajada | **Toda bajada de tanque debe tener llave de paso a válvula suelta.** Lo mismo las derivadas de una bajada general que se bifurque |
| Excepción | Puede no tener llave general el colector del que se derivan **únicamente dos bajadas**, en edificios sin micromedición |
| Prohibición | **Prohibida la llave de paso a válvula suelta bajo piso** |
| Ubicación del colector de llaves | Para tanques de reserva con bifurcaciones de bajadas, el colector debe estar en **lugar común accesible al portero** |
| Alimentación del tanque | Llave de paso obligatoria en el ramal de alimentación del tanque de reserva (facultativa si la conexión es exclusiva al tanque) |

### 1.10.2 Ruptores de vacío (apartado 2.13)

Obligatorios en **edificios sin micromedición individual**, en las bajadas que sirven más de una planta y alimentan válvulas, bidets, salivaderas o cualquier artefacto que pueda considerarse peligroso (riesgo de retrosifonaje).

| Altura de la bajada | Diámetro del ruptor |
|---|---|
| Entre 45 m y 15 m | **2 rangos menor** que la bajada |
| Menor de 15 m | **3 rangos menor** que la bajada |
| Mínimo absoluto | 0,013 m |
| Máximo exigible | 0,050 m |

- Por arriba del pelo de agua pueden conectarse entre sí dos o más ruptores sin aumento de diámetro (conservando el del mayor).
- El extremo terminal del ruptor debe reunir las mismas condiciones que el caño ventilador de tanque (§1.6), o puede conectarse al tanque por la cubierta.
- **En sistemas presurizados o con presiones reguladas se instalan válvulas de desaire en reemplazo de los ruptores de vacío.**

### 1.10.3 Alimentación directa vs. por tanque (apartado 2.8)

| Situación | Régimen |
|---|---|
| Subsuelos en general y pisos bajos **no** destinados a vivienda | Agua corriente **directa**, verificando la piezométrica mínima residual sobre el artefacto más desfavorable. Si no alcanza, tanque elevado |
| **Pisos bajos destinados a vivienda y pisos altos** | **Provisión con reserva de tanque, OBLIGATORIAMENTE** |
| Edificación con servicio mínimo, instalaciones solo en PB | Puede ser directa, **salvo que abastezca a un calentador instantáneo** |

> **Consecuencia práctica:** en un edificio de vivienda, **ningún departamento puede tomar agua directa de la red**, ni siquiera el de planta baja. Todo por tanque.

### 1.10.4 Distribución de bajadas: dos escuelas

| Sistema | Descripción | Ventajas | Desventajas |
|---|---|---|---|
| **Montante única con derivaciones por piso** | Una columna vertical con un ramal por unidad | Menos caño, menos pases de losa | Un corte afecta a toda la columna; medición individual difícil; ruido transmitido |
| **Bajada individual por unidad desde colector en cubierta** | Una bajada por departamento desde el colector del tanque | Corte individual sin afectar a nadie; medición individual sencilla en el colector | Mucho más caño; muchos pases de losa; ocupa más pleno |
| **Montante con medidores individuales por piso (mixto)** | Montante única + batería de medidores en cada piso o en PB | Balance razonable; es lo que se hace hoy | Requiere gabinete de medidores en el palier |

> **Recomendación:** en PB+9 con 4 unidades por piso, **montante única de agua fría y única de agua caliente por núcleo húmedo, con batería de medidores individuales en gabinete de palier** y llave de corte por unidad. Prever el pleno con **acceso registrable desde el palier, nunca desde el interior de la unidad**.

---

## 1.11 Materiales: comparativa técnica y de costo

### 1.11.1 Tabla comparativa

| Material | Uso típico | Temp. máx. de servicio | Presión nominal | Unión | Vida útil estimada | Costo relativo (material) | Costo relativo (mano de obra) |
|---|---|---|---|---|---|---|---|
| **PPR (polipropileno random, tipo 3)** | Agua fría y caliente interior | 70 °C continuo / 95 °C pico | PN10, PN16, PN20, PN25 | **Termofusión** (soldadura por calor) | 50 años | Bajo | Bajo (rápido) |
| **PEAD (polietileno de alta densidad, PE100)** | Impulsiones, enterrado, agua fría | 40 °C | PN6 a PN16 | Electrofusión, fusión a tope, compresión | 50 años | Medio-bajo | Medio |
| **PEX / multicapa (PE-X/Al/PE-X)** | Distribución interior, colectores, losa radiante | 95 °C | PN10 – PN16 | Prensado, accesorios mecánicos | 50 años | Medio-alto | Bajo (muy rápido) |
| **Cobre** | Agua fría y caliente, gas, ACS de alta temperatura | 120 °C+ | Muy alta | Soldadura capilar (estaño-plata) | 50+ años | Alto | Alto (requiere oficio) |
| **Hierro galvanizado** | (Histórico) agua fría y caliente | 60 °C | Alta | Roscada | 20-30 años | Medio | Alto |
| **PVC presión** | Agua fría, riego, enterrado | 45 °C | Clase 6, 10 | Encolado (adhesivo) | 50 años | Muy bajo | Bajo |
| **Acero inoxidable AISI 316** | ACS central, hospitales, recirculación | 150 °C | Muy alta | Prensado, soldadura | 50+ años | Muy alto | Alto |

### 1.11.2 Análisis crítico por material

**PPR (termofusión) — el estándar argentino actual**
- ✅ Rápido de instalar, económico, sin corrosión, sin incrustación, buen aislante acústico y térmico. La unión por termofusión, bien hecha, es monolítica: **no hay junta, hay continuidad de material**.
- ❌ **Muy alta dilatación térmica: ≈ 0,15 mm/m·°C.** Un tramo recto de 10 m de agua caliente que pasa de 20 °C a 60 °C se alarga **60 mm**. Sin liras, brazos de dilatación o abrazaderas deslizantes, el caño pandea, rompe el revoque o desprende accesorios. **Este es el defecto Nº 1 de las instalaciones de PPR en Argentina.**
- ❌ **Diámetro interior mucho menor que el nominal** (ver tabla en §1.4.2). Es el defecto Nº 2.
- ❌ Rigidez baja: exige soportes cada 60-80 cm en horizontal caliente.
- ❌ La calidad de la termofusión depende del operario: **tiempo de calentamiento, tiempo de unión y limpieza del caño**. Una fusión mal hecha estrangula la sección interior con un rebaba anular.
- **Especificar siempre PPR fibra de vidrio (PPR-FV / "faser") para agua caliente:** reduce la dilatación en ~75 %.

**PEX / multicapa — lo mejor para reformas y losa radiante**
- ✅ Se instala en rollo, sin uniones dentro del muro (sistema de colector con "patas de araña"). **Cero juntas embutidas = cero riesgo de pérdida oculta.**
- ✅ Curvable a mano, ideal para reformas donde no se puede romper mucho.
- ✅ El multicapa con alma de aluminio tiene dilatación baja (0,025 mm/m·°C) y conserva la forma al curvarlo.
- ❌ Accesorios caros y propietarios de cada marca (no son intercambiables).
- ❌ Exige herramienta de prensado calibrada.

**Cobre — la referencia técnica**
- ✅ Bacteriostático (relevante contra legionela), resistente a alta temperatura, admite recirculación de ACS a 60 °C indefinidamente, reciclable, no aporta sabor.
- ✅ Diámetro interior real generoso.
- ❌ Costo alto y **robo de material en obra**: es la razón práctica por la que desapareció de la vivienda económica.
- ❌ **Corrosión por picadura** si el agua es agresiva (pH bajo, alta conductividad) o si la velocidad supera 1,5 m/s en agua caliente (erosión-corrosión). **En Santa Rosa, verificar el análisis del agua de red: aguas con alto contenido de sales o arsénico pueden condicionar el material.** `[verificar análisis fisicoquímico del agua de red de Santa Rosa]`
- ❌ **Par galvánico**: nunca conectar cobre aguas arriba de hierro galvanizado sin junta dieléctrica.

**PEAD — el material de la impulsión**
- ✅ El mejor para el tramo cisterna → tanque elevado: alta resistencia al golpe de ariete (baja celeridad), rollo continuo sin uniones en toda la montante, no se incrusta.
- ✅ Enterrado directo, sin cama especial exigente.
- ❌ Solo agua fría. Accesorios de electrofusión caros.

**PVC presión**
- ✅ Barato para colectores enterrados y riego.
- ❌ **Frágil al impacto y a los rayos UV.** No usar a la vista sin protección. No usar en agua caliente. No usar en montantes de edificio.

**Hierro galvanizado — solo para relevar, nunca para especificar**
- Ver §9.3. En una reforma, si aparece hierro galvanizado de más de 25 años, **se cambia completo**. No se parchea.

### 1.11.3 Especificación recomendada para un PB+9 en Santa Rosa

| Tramo | Material recomendado |
|---|---|
| Conexión y alimentación a cisterna | PEAD PE100 PN10 o PVC clase 10 enterrado |
| Impulsión cisterna → tanque elevado | **PEAD PE100 PN16** (golpe de ariete) o acero galvanizado con dispositivo antiariete |
| Colector de tanque y bajadas generales | **PPR PN20** o cobre |
| Montantes de agua fría | **PPR PN20** |
| Montantes de agua caliente y recirculación | **PPR-FV (fibra de vidrio) PN20** o **cobre**, con aislación de espuma elastomérica de espesor ≥ 19 mm |
| Distribución interior de unidad | **PPR PN20** o **multicapa con colector** |
| Losa radiante | **PEX-a con barrera antioxígeno** o multicapa |
| Todo caño de agua caliente y toda impulsión en zonas no calefaccionadas | **Aislación obligatoria.** En Santa Rosa hay riesgo real de congelamiento en sala de tanques y plenos exteriores |

---

## 1.12 Agua caliente sanitaria (ACS)

### 1.12.1 Sistemas de producción — comparativa

| Sistema | Principio | Potencia / capacidad típica | Rendimiento | Costo inicial | Costo de operación | Cuándo usarlo |
|---|---|---|---|---|---|---|
| **Calefón (calentador instantáneo)** | Calienta al paso, sin acumulación | 10 a 16 l/min (14.000 a 25.500 kcal/h) | 80-85 % | Muy bajo | Bajo si es de tiro balanceado y modulante | Monoambientes y 1 dormitorio con un solo punto de consumo por vez |
| **Termotanque a gas de acumulación** | Acumula y mantiene temperatura | 50 a 180 l | 65-75 % (alta pérdida por mantenimiento) | Bajo | Medio (pérdidas de standby) | Vivienda con 2 o más puntos simultáneos. **Es el estándar argentino** |
| **Termotanque eléctrico** | Resistencia + acumulación | 50 a 150 l | ~95 % en el aparato, pero energía primaria cara | Bajo | **Alto** | Solo donde no hay gas |
| **Caldera mural individual (dual)** | Produce ACS instantánea + calefacción | 20.000 a 30.000 kcal/h | 90-95 % (condensación: 105 % PCI) | Medio-alto | Bajo | **Departamentos con calefacción por radiadores o losa. La solución más eficiente para PB+9 con calefacción individual** |
| **Caldera central + intercambiador + acumulación** | Producción centralizada | Según edificio | 90-95 % | Alto | Bajo por unidad, pero requiere gestión de consorcio y medición individual de calorías | Edificios grandes, hoteles. **En vivienda colectiva argentina genera conflicto de expensas: usar con medición individual de calorías obligatoria** |
| **Bomba de calor para ACS (aerotermia)** | Ciclo frigorífico toma calor del aire | COP 2,5 – 4,0 | 250-400 % | Alto | **Muy bajo** | Excelente donde no hay gas o hay tarifa eléctrica favorable. **Advertencia para Santa Rosa: el COP cae bruscamente por debajo de 5 °C. Especificar equipo con resistencia de apoyo y verificar COP a temperatura de diseño de invierno (−6 °C)** |
| **Solar térmica + apoyo** | Colectores + acumulador + backup | Cubre 50-70 % anual | — | Alto | Muy bajo | **Santa Rosa tiene buena heliofanía (4,8 h/día de heliofanía relativa en invierno según IRAM 11603). Técnicamente muy viable.** Requiere superficie de cubierta y previsión de peso y de cañerías |

### 1.12.2 Dimensionado de la acumulación

**Método del consumo punta:**

> **V_acumulador = N_personas × C_persona × f**

| Destino | C_persona (l ACS a 60 °C / persona / día) |
|---|---|
| Vivienda | 22 – 30 |
| Hotel 4-5 estrellas | 50 – 70 |
| Hospital | 55 – 80 |
| Gimnasio con duchas | 20 – 30 (por usuario) |
| Escuela | 3 – 5 |

`[valores de referencia de práctica; verificar contra CTE DB-HE4 español o contra ASHRAE Handbook Applications si se requiere respaldo documental]`

**Método del caudal punta (más riguroso para vivienda):**

> **V = Q_punta × t_punta × [(T_uso − T_red) / (T_acum − T_red)]**

*Ejemplo — departamento de 3 dormitorios en Santa Rosa:*
- Consumo punta: 2 duchas simultáneas × 0,20 l/s de ACS = 0,40 l/s → 24 l/min
- Duración de punta: 15 min → 360 l de agua a temperatura de uso (40 °C)
- T_red en invierno en Santa Rosa: **8 °C** `[verificar temperatura de red invernal: en La Pampa puede bajar de 8 °C]`
- T_acumulación: 60 °C
- V = 360 × (40 − 8)/(60 − 8) = 360 × 0,615 = **221 litros**
- Adoptar **termotanque de 250 l** o **caldera dual de 28.000 kcal/h con producción instantánea de 14 l/min a ΔT 30 °C**

**Método de la potencia de recuperación (para calderas y termotanques de rápida recuperación):**

> **P [kcal/h] = V [l/h] × ΔT [°C] × 1 [kcal/l·°C] / η**

*Ejemplo:* recuperar 200 l/h a ΔT = 45 °C con η = 0,85:
> P = 200 × 45 / 0,85 = **10.588 kcal/h ≈ 12,3 kW**

### 1.12.3 Recirculación de ACS

**La Guía AySA/ERAS lo dice sin matices (apartado 2.19.1):** *"La colocación de cañerías de retorno en sistemas centrales es obligatoria."*

**Por qué:** sin retorno, el usuario del punto más alejado tira litros de agua fría antes de que llegue la caliente. Con 30 m de cañería de Ø 25 mm, eso son ~15 litros y 40 segundos por cada uso.

**Criterio de proyecto:**

| Parámetro | Valor recomendado |
|---|---|
| **Cuándo es obligatoria** | Sistema central. **Recomendable siempre que la distancia del generador al punto más alejado supere los 15 m** |
| Caudal de recirculación | Se calcula para compensar la pérdida térmica del circuito: **Q_rec = P_pérdida / (ρ × c × ΔT)** con ΔT = 5 °C entre ida y retorno |
| Velocidad en el retorno | 0,3 – 0,6 m/s (baja, para no erosionar) |
| Temperatura de retorno | **≥ 50 °C en todo punto del circuito** (criterio antilegionela) |
| Bomba de recirculación | De rotor húmedo, bronce o inoxidable (nunca fundición en ACS), con temporizador o control por termostato |
| Aislación | **Obligatoria en ida y retorno.** Sin aislación, la recirculación es un radiador que calienta el pleno |
| Equilibrado | Válvulas de equilibrado termostáticas en el pie de cada montante de retorno. **Sin equilibrado, el montante más cercano se lleva todo el caudal y el más lejano no recircula** |

### 1.12.4 Riesgo de legionela

*Legionella pneumophila* prolifera en agua estancada entre **20 °C y 45 °C**, con óptimo en 35-40 °C. Se transmite por **inhalación de aerosoles** (duchas, torres de enfriamiento, spas), no por ingestión.

**Reglas de proyecto (referencia metodológica: RD 865/2003 y UNE 100030 españolas; en Argentina no hay norma equivalente de cumplimiento obligatorio para vivienda):**

| Regla | Valor |
|---|---|
| **Temperatura de acumulación** | **≥ 60 °C** permanente |
| **Temperatura en todo punto del circuito de retorno** | **≥ 50 °C** |
| **Temperatura de distribución a los puntos de consumo** | Mezclada a ≤ 45 °C **en el punto de uso** con válvula termostática, para evitar quemaduras |
| **Choque térmico periódico** | Elevar el acumulador a 70 °C y purgar todos los grifos durante ≥ 5 min (rutina de mantenimiento) |
| **Puntos muertos** | **Eliminar todo ramal ciego.** Un tramo de cañería sin consumo es un reactor biológico. En reformas, **cortar y taponar en el origen, no dejar el ramal muerto** |
| **Materiales** | Evitar materiales que favorezcan biofilm. **El cobre es bacteriostático.** Evitar juntas de goma natural, mangueras flexibles largas y cabezales de ducha con acumulación de agua |
| **Purga del acumulador** | Válvula de limpieza en la parte más baja — **es obligatoria por la Guía AySA/ERAS (2.19.1)**, y sirve exactamente para esto |
| **Intermediarios con serpentín interno** | **Tapa de inspección obligatoria** (Guía 2.19.1), de cualquier capacidad |

> **La contradicción que hay que resolver en el proyecto:** el ahorro energético empuja a bajar la temperatura de acumulación (50 °C), la seguridad sanitaria a subirla (60 °C) y la seguridad de las personas a limitar la de uso (45 °C). **La solución correcta es: acumular a 60 °C + distribuir a 60 °C + mezclar en el punto de uso con válvula termostática de punto final.** Nunca bajar la temperatura de acumulación por ahorro.
>
> **Riesgo específico de la bomba de calor para ACS:** muchos equipos trabajan naturalmente a 50-55 °C, que es exactamente la zona de riesgo. **Especificar equipos con ciclo antilegionela programado** que suban semanalmente a 60-65 °C con la resistencia de apoyo.

### 1.12.5 Prohibiciones y reglas de la Guía para ACS

| Regla (Guía AySA/ERAS 2.19.1) |
|---|
| **Obligatoria válvula de limpieza** en la parte más baja del elemento de producción, para vaciado total |
| **Obligatoria tapa de inspección** en intermediarios con serpentín interno, de cualquier capacidad |
| **Obligatoria la cañería de retorno** en sistemas centrales |

---

## 1.13 Medición individual y sala de medidores

### 1.13.1 Medición individual de agua

La Guía AySA/ERAS (apartado 2.12) indica que **debe instalarse un sistema de medición individual del consumo de agua**. Diámetro y caudal máximo según **ISO 4064**:

**Tabla Nº 6 de la Guía — selección de medidor:**

| Ø medidor (mm) | Qc de proyecto (m³/h) | Caudal medio (m³/h) | Caudal máximo "C" (m³/h) |
|---|---|---|---|
| 15 | 1,5 | 2,25 | 3 |
| 19 | 2,5 | 3,75 | 5 |
| 25 | 3,5 | 5,25 | 7 |
| 32 | 5 | 7,5 | 10 |
| 38 | 10 | 15 | 20 |
| 50 | 15 | 22,5 | 30 |
| 60 | 25 | 37,5 | 50 |
| 75 | 40 | 60 | 80 |

**Pérdida de carga del medidor:**

> **Jm = 0,036 × (Qcl / C)²**
>
> Qcl = gasto máximo probable en **l/min**; C = capacidad máxima del medidor en **m³/h**; Jm en **m.c.a.**

*Ejemplo de la Guía:* Qc = 0,71 l/s = 42,1 l/min → 2,5 m³/h. De la tabla se adopta medidor de **19 mm** (C = 7 m³/h).
> Jm = 0,036 × (42,1 / 7)² = 0,036 × 36,2 = **1,3 m.c.a.**

*Aplicación al Ejemplo Nº 1:* Qc_edificio = 28,07 m³/h → **medidor general de Ø 60 mm** (Qc de proyecto 25 m³/h) o **Ø 75 mm** (40 m³/h) para tener margen. **Adoptar Ø 75 mm.**
> Qcl = 468 l/min; C = 80 m³/h → Jm = 0,036 × (468/80)² = 0,036 × 34,2 = **1,23 m.c.a.**

Medidor individual por departamento de 2 dormitorios: Qc_unidad = 1,70 × [1/(8−1)^0,5 × 1] = 1,70 × 0,378 = 0,64 l/s = 2,31 m³/h → **medidor de Ø 19 mm**.

### 1.13.2 Sala / gabinete de medidores de agua

- Debe incluirse en el proyecto sanitario el **detalle de instalación del medidor general**, sus conexiones, accesorios, dimensiones de la caja, diámetros de todas las cañerías y separaciones entre cañerías y entre cañerías y elementos del gabinete, **en escala 1:20 o 1:25** (Guía 2.6).
- Ubicación en **espacio común accesible**, con desagüe de piso.
- En edificios con micromedición, la **llave de paso a válvula suelta general va después de la medición**, y hay otra en la entrada de cada unidad locativa.

---

# 2. SANITARIAS — DESAGÜES CLOACALES

## 2.1 Sistema primario y sistema secundario

Es la distinción básica del sistema argentino y **define qué se ventila, qué lleva sifón y qué diámetro corresponde**.

| | **Sistema primario** | **Sistema secundario** |
|---|---|---|
| **Qué recibe** | Descargas de inodoros, mingitorios, lavachatas, piletas de cocina con desagüe primario, y todo lo que viene aguas abajo de un sifón | Descargas de lavatorios, bidets, bañeras, duchas, piletas de lavar, lavarropas, lavavajillas — es decir, artefactos con sifón propio |
| **Contacto con gases cloacales** | Sí, directo | No: está separado del primario por un **cierre hidráulico** (sifón, pileta de piso o boca de acceso) |
| **Ventilación** | **Obligatoria** (ventilación principal y subsidiaria) | Requiere ventilación cuando se exceden longitudes o cantidad de ramales |
| **Elemento de transición** | — | Pileta de piso, boca de acceso o sifón que descarga al primario |

**Regla clave:** un artefacto secundario **nunca** descarga directamente al primario sin interposición de un cierre hidráulico. Y un cierre hidráulico **nunca** se pone en serie con otro (doble sifonaje): se rompe el arrastre y se produce sedimentación.

---

## 2.2 Caudales de desagüe por artefacto y simultaneidad

Fuente: Guía AySA/ERAS, Capítulo 3, apartado 3.6.1, Tabla Nº 1.

| Artefacto | qu (l/s) |
|---|---|
| Inodoro con depósito de limpieza | **0,90** |
| Inodoro con limpieza por válvula automática | **1,50** |
| Mingitorio con limpieza por válvula automática | 0,20 |
| Duchas | 0,30 |
| Lavatorio, bidet, bañera, pileta de lavar | 0,20 |
| Pileta de cocina | 0,20 |
| Máquina lavarropas | **0,60** |
| Lavavajillas doméstico | **0,60** |

> Los artefactos que no figuran se incluyen con los caudales de descarga dados por el fabricante.

**Caudal del tramo:**

> **Qt = K × n × qu**
>
> **Kc = 1 / (n − 2)^0,5**  ← *ojo: en desagües es (n−2), no (n−1) como en agua*
>
> **K = Kc × a**

| Tipología | a |
|---|---|
| Oficinas privadas y vivienda individual | 1 |
| **Viviendas multifamiliares**, oficinas públicas | **2** |
| Edificios públicos, aeropuertos, centros de salud | 3 |
| Centros de detención, deportivos, comerciales | 4 |

**Caudales adicionales (3.6.2):** a Qt se le suman los caudales de **bombeos** y **desagües continuos** (condensado de equipos de refrigeración, purgas, etc.).

> **Esto se olvida sistemáticamente:** en un PB+9 con 40 splits, el condensado suma. Un split de 3.000 frigorías genera del orden de **0,3 a 0,8 l/h** en régimen; 40 equipos ≈ 20 l/h. No es un caudal de diseño relevante para el colector, **pero sí exige que exista un desagüe de condensado proyectado**, con pendiente y con descarga a pileta de piso abierta, y no un caño que termina en el balcón goteando a la vereda.

---

## 2.3 Diámetros mínimos y longitudes máximas

Fuente: Guía AySA/ERAS, Capítulo 3.

| Elemento | Regla |
|---|---|
| **Cañería principal** (nuevo radio / distritos bajos) | **0,100 m y 0,150 m**, según cálculo del apartado 3.6 |
| **Desagüe de lavatorio/bidet/bañera a pileta de piso abierta de 0,060 m ubicada a máximo 3,00 m** | **0,038 m** |
| Desagüe secundario pasando de 5,00 m, o para conectar a cañería principal | **0,060 m** |
| **Pileta de piso abierta de 0,060 m** | Puede recibir como máximo el desagüe de **cuatro (4) artefactos** |
| Diámetro máximo de desagües afluentes a boca de acceso | **0,060 m**; la suma de secciones no debe superar la de la boca |
| **A boca de acceso no pueden conectarse ventilaciones mayores de 0,060 m** | — |
| **Boca de acceso no puede recibir caño de descarga y ventilación** | — |
| Las bocas de acceso son **independientes para cada unidad locativa** | — |
| Pileta de cocina con desagüe primario | Sifón de **0,050 m**, desagüe de **0,060 m hasta 5,00 m** como máximo |
| Pileta de cocina con desagüe directo a cámara de inspección | **5,00 m como máximo de 0,060 m** |
| Pileta de cocina doble | Se permite una sin sifón, con desagüe conectado **aguas arriba del sifón de la otra** |
| **Desagüe de piso obligatorio** en locales sanitarios | Pileta de piso abierta 0,060 m o 0,050 m, o rejilla de piso |
| Sifón en mingitorios | Facultativo si desagua a pileta de piso ubicada **en el propio recinto** |
| **Prohibiciones** | Desagües **en contrapendiente** y **excesiva cantidad de desagües** conectados |
| Desagüe con canilla de servicio | Cuando el desagüe es de uso exclusivo/esporádico: **canilla de servicio obligatoria para reponer la carga del sifón** |

### 2.3.1 Diámetros de desagüe por artefacto — tabla de proyecto

| Artefacto | Ø sifón | Ø desagüe individual | Sistema |
|---|---|---|---|
| Inodoro | — (sifón integrado) | **0,100 m (110 mm)** | Primario |
| Bidet | 0,038 m | 0,038 m | Secundario |
| Lavatorio | 0,038 m | 0,038 m | Secundario |
| Bañera | 0,038 m | 0,038 m | Secundario |
| Ducha / receptáculo | 0,038 – 0,050 m | 0,038 – 0,050 m | Secundario |
| Pileta de cocina | 0,050 m | 0,060 m | Primario o secundario según diseño |
| Pileta de lavar | 0,038 – 0,050 m | 0,050 m | Secundario |
| Lavarropas | 0,038 m | 0,050 m | Secundario |
| Lavavajillas | 0,038 m | 0,050 m | Secundario |
| Mingitorio | 0,038 – 0,050 m | 0,050 m | Primario |
| Pileta de piso abierta | — | **0,060 m** o 0,050 m | Recibe secundarios, descarga a primario |
| Rejilla de piso | — | 0,050 – 0,060 m | Secundario |
| Boca de acceso | — | **0,100 m** | Primario |
| Cañería principal | — | **0,100 m / 0,150 m** | Primario |

### 2.3.2 Tapadas mínimas (3.4)

| Material | Tapada mínima |
|---|---|
| Caño de hierro fundido liviano o pesado | **0,20 m** |
| Otros materiales (PVC, PP) | **0,40 m** |

### 2.3.3 Saltos (3.3)

- **Salto mínimo: 0,50 m**
- Saltos a 45° en cañerías: se prolongan hasta boca de inspección.

---

## 2.4 Pendientes

### 2.4.1 Criterio de fondo (apartado 3.5)

La capacidad de los tirones horizontales debe cumplir:

| Condición | Valor |
|---|---|
| Sección de escurrimiento | **Parcialmente llena** |
| Relación tirante/diámetro | **0,3 < h/d < 0,7** |
| Velocidad de escurrimiento | **> 0,60 m/s** (velocidad de autolimpieza, para sección llena) |

Verificación por **Manning**:

> **V = (1/n) × R^(2/3) × P^(1/2)**
>
> R = radio hidráulico = **d/4** para secciones circulares (d = diámetro interior)
> P = pendiente de instalación [1/1]

**Coeficientes n de Manning (Guía):**

| Material | n |
|---|---|
| Materiales plásticos (PVC, PP) | **0,011** |
| Hierro fundido | **0,015** |
| Latón | **0,011** |

### 2.4.2 Pendientes normativas de la cañería principal

De la Guía (Capítulo 3):

| Diámetro | Pendiente máxima | Pendiente mínima |
|---|---|---|
| **0,100 m (110 mm)** | **1:20 (5,0 %)** | **1:60 (1,67 %)** |
| **0,150 m (160 mm)** | **1:20 (5,0 %)** | **1:100 (1,0 %)** |

> **Ojo con la pendiente máxima.** Muchos instaladores creen que "cuanto más pendiente, mejor". **Falso.** Con pendiente excesiva el líquido corre más rápido que los sólidos, que quedan atrás y taponan. Por eso hay un techo de 1:20.

### 2.4.3 Tabla de pendientes de proyecto

| Ø nominal | Pendiente mínima | Pendiente máxima | Pendiente **recomendada de proyecto** | Caída en 1 m | Caída en 10 m |
|---|---|---|---|---|---|
| 0,038 m (40 mm) | 2,0 % | 5,0 % | **3,0 %** | 30 mm | 300 mm |
| 0,050 m (50 mm) | 2,0 % | 5,0 % | **2,5 %** | 25 mm | 250 mm |
| 0,060 m (63 mm) | 1,7 % | 5,0 % | **2,0 %** | 20 mm | 200 mm |
| **0,100 m (110 mm)** | **1,67 % (1:60)** | **5,0 % (1:20)** | **2,0 %** | 20 mm | 200 mm |
| **0,150 m (160 mm)** | **1,0 % (1:100)** | **5,0 % (1:20)** | **1,5 %** | 15 mm | 150 mm |
| 0,200 m (200 mm) | 0,8 % | 5,0 % | **1,0 %** | 10 mm | 100 mm |

`[los diámetros de 40, 50, 63 y 200 mm no están tabulados explícitamente en el capítulo 3 de la Guía con esos límites de pendiente: verificar por cálculo de Manning en cada caso]`

> **Regla mnemotécnica de obra:** *"2 % en 110, 1,5 % en 160"*. Es fácil de comunicar al gremio y está del lado seguro.
>
> **Consecuencia de proyecto que hay que resolver en el anteproyecto:** una cañería de 110 mm con 2 % que corre 20 m baja **40 cm**. Si el baño está a 20 m de la cámara y el contrapiso tiene 12 cm, **no entra**. Este es el conflicto más frecuente entre arquitectura y sanitarias, y se resuelve en planta, moviendo el núcleo húmedo, no en obra rompiendo la losa.

### 2.4.4 Capacidad de los caños de descarga y ventilación (montantes) — 3.6.3

Para evitar velocidades excesivas y sobrepresiones, los montantes se diseñan para un **factor de llenado r entre 0,15 y 0,33** de la sección.

> **Qcdv = 32,86761 × 10³ × r^1,667 × dc^2,667**
>
> Qcdv en l/s, dc en **metros**, r = factor de llenado

> **Vcdv = 0,639 × (Qcdv / dc)^0,4**

Esta velocidad se alcanza y se mantiene constante **a partir de aproximadamente 10 m del punto de descarga** (velocidad terminal).

**Longitud de tranquilización — el dato que nadie usa y explica muchos problemas:**

En el desvío horizontal de la cañería de descarga se produce un **resalto hidráulico** que corta el circuito de aire y genera una presión positiva que se expande por el sistema (y sifona los cierres hidráulicos de las plantas bajas). Existe una distancia **Lt** en la cual **no se debe conectar ningún artefacto**:

> **Lt = 0,1686 × Vcdv²**  [m]

*Ejemplo:* montante Ø 0,100 m con r = 0,20 →
- Qcdv = 32.867,61 × 0,20^1,667 × 0,100^2,667 = 32.867,61 × 0,0679 × 0,00217 = **4,84 l/s** (coincide con la Tabla Nº 4 del capítulo pluvial de la Guía)
- Vcdv = 0,639 × (4,84 / 0,100)^0,4 = 0,639 × 48,4^0,4 = 0,639 × 4,71 = **3,01 m/s**
- **Lt = 0,1686 × 3,01² = 1,53 m**

> **Traducción a obra:** en el tramo horizontal al pie de una montante de Ø110, **no conectar ningún artefacto en el primer 1,5 m** (y por seguridad, en los primeros 2 m). **Éste es el motivo real por el que "el baño de planta baja huele" en muchos edificios**: le conectaron el inodoro de PB al pie de la montante, y cada descarga desde arriba le sopla el sifón.

---

## 2.5 EJEMPLO RESUELTO Nº 2 — Verificación de un colector cloacal

### Datos

Colector principal del edificio del Ejemplo Nº 1 (PB+9, 40 departamentos), tramo desde el pie de la última montante hasta la cámara de inspección de línea municipal. Material: **PVC cloacal Ø 160 mm** (interior real ≈ 152 mm), pendiente adoptada **1,5 %**.

### Paso 1 — Caudal de desagüe del edificio

Artefactos con descarga cloacal (mismo conteo del Ejemplo Nº 1, n = 337):

| Artefacto | Cantidad | qu (l/s) | Subtotal (l/s) |
|---|---|---|---|
| Inodoros con depósito | 12×1 + 20×2 + 8×3 + 2 (locales) + 0 = 78 | 0,90 | 70,20 |
| Lavatorios | 12×1 + 20×2 + 8×3 + 2 = 78 | 0,20 | 15,60 |
| Bidets | 12×1 + 20×1 + 8×2 = 48 | 0,20 | 9,60 |
| Duchas/bañeras | 12×1 + 20×1 + 8×2 = 48 | 0,30 | 14,40 |
| Piletas de cocina | 40 + 2 = 42 | 0,20 | 8,40 |
| Lavarropas | 40 | 0,60 | 24,00 |
| Piletas de lavar / canillas de servicio | 3 | 0,20 | 0,60 |
| **TOTAL** | **n = 337** | | **Σ = 142,80 l/s** |

### Paso 2 — Simultaneidad

> Kc = 1 / (n − 2)^0,5 = 1 / (337 − 2)^0,5 = 1 / 335^0,5 = 1 / 18,30 = **0,0546**
>
> a = 2 (viviendas multifamiliares) → **K = 0,1093**
>
> **Qt = 142,80 × 0,1093 = 15,61 l/s**

**Caudales adicionales:** condensado de 40 splits ≈ 0,006 l/s (despreciable) + bombeo pluvial de subsuelo, si descarga a cloaca — **en este caso NO** (el pluvial va a calzada). **Qt de diseño = 15,6 l/s.**

### Paso 3 — Verificación por Manning del Ø160 al 1,5 %

Datos: d_int = 0,152 m; P = 0,015; n = 0,011 (PVC)

**Velocidad a sección llena:**
> R = d/4 = 0,152/4 = 0,038 m
> V = (1/0,011) × 0,038^0,667 × 0,015^0,5 = 90,91 × 0,1123 × 0,1225 = **1,25 m/s**

**Caudal a sección llena:**
> A = π × 0,152²/4 = 0,01815 m²
> Q_lleno = 1,25 × 0,01815 = 0,02269 m³/s = **22,69 l/s**

**Relación de llenado:**
> Q_diseño / Q_lleno = 15,61 / 22,69 = **0,688**

Para Q/Q_lleno = 0,688, la relación **h/d ≈ 0,60** (de la curva de escurrimiento parcial en conducto circular).

### Paso 4 — Verificación de las tres condiciones

| Condición normativa | Requerido | Obtenido | ¿Verifica? |
|---|---|---|---|
| Sección parcialmente llena | Sí | Sí (h/d = 0,60) | ✅ |
| **0,3 < h/d < 0,7** | 0,3 – 0,7 | **0,60** | ✅ (aunque está cerca del límite) |
| **V > 0,60 m/s** a sección llena | > 0,60 | **1,25 m/s** | ✅ |
| Pendiente entre 1:100 y 1:20 para Ø150 | 1,0 % – 5,0 % | **1,5 %** | ✅ |

**✅ EL Ø160 AL 1,5 % VERIFICA**, con h/d = 0,60. Pero está a un 14 % del límite superior: si se agregan unidades o cambia la tipología, se pierde el margen.

### Paso 5 — Comprobación: ¿alcanzaría un Ø110?

d_int Ø110 PVC ≈ 0,104 m; adoptando P = 2,0 % (la mínima es 1,67 %):
> R = 0,026 m; V = 90,91 × 0,026^0,667 × 0,020^0,5 = 90,91 × 0,0876 × 0,1414 = **1,13 m/s**
> A = 0,0085 m²; Q_lleno = **9,60 l/s**
> Q_diseño / Q_lleno = 15,61 / 9,60 = **1,63 > 1**

**❌ NO VERIFICA — el Ø110 se desborda.** El colector principal de este edificio **debe ser Ø160 como mínimo.**

### Paso 6 — Verificación de una montante (caño de descarga y ventilación)

Montante Ø 110 mm que sirve 10 departamentos de 2 dormitorios (una columna).

Artefactos: 10 × 8 = **80**; Σ qu = 10 × (0,90×2 + 0,20×2 + 0,20 + 0,30 + 0,20 + 0,60) = 10 × 4,10 = **41,0 l/s**
> Kc = 1/(80−2)^0,5 = 0,1132; K = 0,2265
> **Qt = 41,0 × 0,2265 = 9,29 l/s**

Capacidad de la montante Ø 0,100 m con **r = 0,33** (llenado máximo admitido):
> Qcdv = 32.867,61 × 0,33^1,667 × 0,100^2,667 = 32.867,61 × 0,1571 × 0,002154 = **11,12 l/s**

> 9,29 < 11,12 ✅ **Verifica**, pero al 84 % de la capacidad máxima. La Guía **recomienda que r no supere 0,20** en los verticales. Con r = 0,20 la capacidad es 4,84 l/s → **NO verifica el criterio recomendado.**

**Conclusión de proyecto:** con 4 departamentos de 2 dormitorios por piso y 10 plantas en **una sola montante**, hay que:
- **Opción A:** montante de **Ø 160 mm** (con r=0,20 da Qcdv = 14,26 l/s ✅)
- **Opción B (recomendada):** **dos montantes de Ø 110 mm**, una por par de departamentos (cada una con 5 dptos. → n=40, Σqu=20,5, Kc=1/38^0,5=0,162, K=0,324, Qt=6,64 l/s → con r=0,25 da 7,02 l/s ✅). Además da redundancia y simplifica el trazado.

> **Regla práctica que sale de este ejemplo:** en un PB+9, **no colgar más de 5 o 6 departamentos de una misma montante de Ø110**. Con 8 o más, ir a Ø160 o desdoblar.

---

## 2.6 Sifones, piletas de piso, bocas de acceso y de desagüe

| Elemento | Función | Regla |
|---|---|---|
| **Sifón** | Cierre hidráulico que impide el paso de gases | Sello de agua mínimo ~50 mm. **Prohibido el doble sifonaje.** Prohibidos los sifones de "botella" en desagües primarios |
| **Pileta de piso abierta (PPA)** | Recibe hasta 4 desagües secundarios y actúa de cierre hidráulico hacia el primario | Ø 0,060 m (o 0,050 m). **Obligatoria en todo local sanitario.** Recibe máximo 4 artefactos |
| **Pileta de piso tapada (PPT)** | Igual, pero con tapa hermética. Se usa donde no puede haber rejilla visible | Requiere reposición de agua (canilla de servicio) si el uso es esporádico |
| **Boca de acceso (BA)** | Punto de acceso al sistema primario dentro del edificio | Ø 0,100 m. **No puede recibir caño de descarga y ventilación.** No pueden conectarse ventilaciones > 0,060 m. **Independiente para cada unidad locativa.** Diámetro máximo de afluentes: 0,060 m |
| **Boca de desagüe abierta (BDA)** | Recibe descargas al aire libre y patios | Con reja |
| **Boca de desagüe tapada (BDT)** | Igual, tapada | Ventilada |
| **Rejilla de piso (RP)** | Desagüe de superficie sin cierre hidráulico propio | Descarga a PPA |

**Reglas adicionales de la Guía:**
- En serie de inodoro común o inodoro a la turca conectado a caño de descarga y ventilación: **boca de acceso** obligatoria.
- Caño de descarga y ventilación que reciba inodoro, lavachata o pileta de cocina: verificar el punto de acceso. En desvíos, **caño cámara vertical aguas arriba del desvío**.
- **En lo posible, no colocar ramales de caño de descarga y ventilación bajo losa de planta baja** (dificulta el mantenimiento).
- **Prohibido conectar el desagüe de limpieza del tanque de agua directamente a pileta de piso o cualquier otro desagüe** (debe ir a PPA con corte de aire).

---

## 2.7 Cámaras de inspección

| Parámetro | Valor |
|---|---|
| **Ubicación de la última cámara** | A no más de **10 metros de la línea municipal**, en espacio de uso general, independientemente de la propiedad |
| Dimensiones interiores típicas | 0,60 × 0,60 m hasta 1,20 m de profundidad; mayores para más profundidad `[verificar dimensiones exigidas por la prestadora local]` |
| Cojinete (media caña) | Con la pendiente establecida para las cañerías; los asientos apoyan en toda su longitud |
| Contratapa | Hermética, para evitar escape de gases |
| Tapa | A nivel de piso terminado, registrable |
| **Ventilación** | **Toda cámara de inspección debe quedar en circuito ventilado** (Guía 6.6) |
| Distancia entre cámaras | Cada cambio de dirección, cambio de pendiente, cambio de diámetro, y en tramos rectos cada 30 m aprox. `[verificar en reglamento local]` |
| Separación cañería principal / albañal no suspendidos | **0,40 m como mínimo** (distancia libre entre filos exteriores, medida en proyección horizontal). **No se permiten superpuestas** |

---

## 2.8 Ventilaciones: la parte que más se subestima

### 2.8.1 Por qué se ventila

Tres razones, ninguna opcional:
1. **Evitar el sifonaje** (aspiración del cierre hidráulico por depresión aguas abajo de una descarga).
2. **Evitar el contrasifonaje** (expulsión del cierre hidráulico por sobrepresión, típicamente al pie de la montante).
3. **Evacuar los gases** del sistema primario por encima de la cubierta.

### 2.8.2 Ventilación principal (o de extremo) — Guía 6.3

> **La cañería principal de desagüe cloacal debe estar ventilada en uno de sus puntos más distantes de la conexión externa.**

| Situación | Diámetro |
|---|---|
| General | **Ø 0,100 m** |
| Fincas de **una sola planta** con servicios mínimos, como máximo pileta de lavar, y cañería principal que **no exceda 15,00 m** | **Ø 0,060 m** |

### 2.8.3 Ventilación subsidiaria (secundaria) — Guía 6.1 y 3.7

> **En edificios de más de dos plantas en altura, que cuenten con instalaciones sanitarias en los pisos superiores, las cañerías de descarga primaria y secundaria estarán dotadas de una cañería subsidiaria de ventilación.**

Es la **columna de ventilación paralela a la montante**, conectada a ella en varios puntos. Es lo que impide que la descarga del 9.º piso vacíe el sifón del 2.º.

**Dimensionado (3.7):** la longitud máxima de la ventilación subsidiaria depende del caudal que escurre en la cañería de descarga (Qcdv) y del caudal de aire Qa que ese escurrimiento arrastra:

> **Qa = 32,86 × 10³ × r^0,667 × K1 × dc^2,667**  con **K1 = (1 − r)**

Se debe verificar que la pérdida de carga en la ventilación subsidiaria **no supere 0,025 m de columna de agua** (equivalente a **20,96 m de columna de aire**, tomando γ_aire = 1,24 kg/m³ y γ_agua = 1.000 kg/m³).

**Diámetros de CVS tabulados en la Guía: 0,050 m, 0,060 m y 0,100 m.**

**Regla práctica de proyecto:** la ventilación subsidiaria se dimensiona **un rango por debajo del caño de descarga** y nunca menos de 0,060 m en edificios en altura.

| Montante de descarga | Ventilación subsidiaria mínima recomendada |
|---|---|
| Ø 0,100 m | **Ø 0,060 m** |
| Ø 0,150 m | **Ø 0,100 m** |

`[verificar por el cálculo de 3.7 en cada caso: la longitud de la CVS es el parámetro que puede obligar a subir un diámetro]`

### 2.8.4 Ventilación auxiliar / de artefacto — Guía 6.4, 6.5, 6.7, 6.13

Es la que se agrega cuando un artefacto o un ramal queda "solo" y su sifón está expuesto.

| Regla | Valor |
|---|---|
| Artefactos de cualquier tipo | **Hasta 10 m sin ventilar** |
| Solo pileta de cocina con desagüe primario, mingitorio y pileta de piso | **Hasta 15 m sin ventilar** |
| **Más de 15 m** | **Todo se ventila.** Diámetros según cálculo (3.6) en todos los casos |
| **Artefacto secundario a más de 15,00 m de punto ventilado** | Debe ventilarse; **se puede no ventilar intercalando boca de desagüe abierta cada 15,00 m** |
| Artefacto alto provisto de sifón con desagüe a caño de descarga y ventilación | **Debe ser ventilado.** Puede ventilarse por ramal colocado sobre el empalme de la ramificación con el caño de descarga y ventilación, siempre que el desarrollo y el número de artefactos concurrentes respondan a la verificación de caudal y diámetro |
| **Número máximo de ramales sobre tirón no ventilado** (≤ 10 o 15 m) | **2 ramales de 0,100 m y 1 de 0,060 m directos**, más otros según la Guía |
| Bocas de acceso o empalme en pisos altos | Se ventila indistintamente la boca, el empalme o el sifón de la pileta de cocina, siempre que el ramal de acceso al caño de descarga y ventilación **no esté ya ventilado** |
| Conexión entre caños de ventilación | Permitida dentro de **un mismo sistema**. **El primario y el secundario son sistemas distintos**, igual que los que descargan en conexiones distintas |
| Trazado | **Preferentemente por muros; en lo posible NO bajo pisos** |
| Ventilación de 0,100 m | **No puede conectarse a boca de acceso** (debe hacerse a ramal T) |

### 2.8.5 Remates

| Regla |
|---|
| Los caños de descarga vertical de los artefactos de pisos altos **deben prolongarse para que sirvan también de ventilación** |
| Si no pueden prolongarse verticalmente, deben trasladar su extremo libre en forma horizontal cumpliendo lo establecido |
| Los remates de las cañerías de descarga y ventilación **pueden unificarse formando un colector** cuyo diámetro se verifica según 3.6 |
| **El remate del caño de descarga y ventilación debe ser de igual diámetro que el de su columna** |
| **Excepción:** caños de descarga que no excedan **4 metros de altura** y reciban como máximo un artefacto con desagüe de 0,100 m y uno de 0,060 m, ubicados en entrepisos de PB y a un mismo nivel |
| Remate a los cuatro vientos, por encima de la cubierta y alejado de aberturas y de tomas de aire de ventilación mecánica |

> **Error clásico en obra:** rematar la ventilación cloacal **al lado de una toma de aire del recuperador de calor o de una ventana del último piso**. Prever en el plano de cubierta la **posición y la altura de todos los remates**: cloacales, de tanque, de gas, de campanas y de extracción, con sus distancias mínimas.

---

## 2.9 Montantes en edificios en altura

### 2.9.1 Reglas de trazado

| Regla | Fundamento |
|---|---|
| **Verticalidad estricta.** Todo desvío de la montante genera resalto hidráulico y sobrepresión | 3.6.3 |
| Si hay desvío inevitable: **caño cámara vertical aguas arriba del desvío** y **no conectar artefactos en la longitud Lt** (§2.4.4) | 3.6.3 |
| **No conectar artefactos en los 2 m inferiores** de la montante (pie) ni en el tramo horizontal inmediato | Lt |
| Ramales a la montante **a favor de la corriente**, con ramal Y de 45° o T-Y. **Prohibido el ramal T a 90° en el sentido del escurrimiento** | Buena práctica; verificar exigencia local |
| **Ventilación subsidiaria paralela obligatoria** en edificios de más de 2 plantas | 6.1 |
| Alojar la montante en **pleno registrable desde espacio común**, nunca dentro del baño de una unidad | Mantenimiento |
| **Aislación acústica del pleno.** Un Ø110 de PVC con descarga de inodoro genera 55-60 dB(A). En pleno que linda con dormitorio, es un litigio | IRAM/ISO 140; `[verificar exigencia acústica del Código de Santa Rosa]` |
| Material recomendado: **PVC cloacal 3,2 mm o PP insonorizado de triple capa** en montantes que linden con locales habitables | — |

### 2.9.2 Aislación acústica de montantes — el detalle que se descubre tarde

| Solución | Reducción típica |
|---|---|
| PVC cloacal simple, pleno de placa de yeso simple | Referencia (peor caso) |
| PVC + manta de lana mineral 50 mm + placa de yeso | −8 a −12 dB |
| **Caño de PP insonorizado (triple capa con carga mineral)** + manta + doble placa | **−15 a −20 dB** |
| Abrazaderas con goma (nunca metálicas directas al muro) | −3 a −5 dB adicionales |

> **Especificación mínima recomendada del estudio:** en toda montante cloacal que linde con dormitorio o estar, **caño insonorizado + manta acústica + abrazaderas con elastómero + pleno con doble placa y lana mineral**. El sobrecosto es de un dígito porcentual sobre la instalación sanitaria y evita el reclamo más frecuente en edificios nuevos.

---

## 2.10 Subsuelos: pozo de bombeo cloacal

Todo desagüe por debajo de la cota de la cámara de inspección (típicamente el subsuelo de cocheras, la sala de máquinas, el sótano) debe elevarse por bombeo.

### 2.10.1 Diseño del pozo

| Parámetro | Criterio |
|---|---|
| **Estanqueidad** | Pozo impermeable de hormigón armado, con tapa hermética y contratapa |
| **Ventilación** | **Ø 0,060 m mínimo, a los cuatro vientos.** Un pozo cloacal sin ventilar es un riesgo de H₂S y de explosión |
| **Volumen útil** | Debe permitir que la bomba **no arranque más de 10-12 veces por hora**. V_útil = Q_afluente × t_ciclo / 4 |
| **Bombas** | **Dos, alternadas, sumergibles, con impulsor tipo vórtex o triturador**. Nunca una sola |
| **Trituradora** | Obligatoria si el pozo recibe inodoros. Si solo recibe piletas de piso y rejillas (achique de agua limpia), basta impulsor vórtex |
| **Impulsión** | Con válvula de retención y válvula de corte por bomba, uniendo a un colector común. Descarga **por encima del nivel de la cámara**, con **lira antirretorno** (curva que sube por encima del nivel de la cámara antes de bajar) |
| **Alarma de nivel alto** | Obligatoria, con señal en portería |
| **Alimentación eléctrica** | Circuito exclusivo, con diferencial de 30 mA, en tablero de servicios generales. **Considerar conexión a grupo electrógeno** |
| **Prohibición** | El desagüe cloacal bombeado **no puede unirse al pluvial** |

### 2.10.2 Bomba de achique (agua limpia)

Para el pozo que recibe drenajes de subsuelo, condensados y agua de lavado de cocheras:
- Bomba sumergible de achique con impulsor abierto.
- Interceptor de **barros y arena** aguas arriba (cámara desarenadora).
- **Interceptor de hidrocarburos** si recibe agua de cochera con vehículos (ver §2.11).

---

## 2.11 Interceptores

Fuente: Guía AySA/ERAS, Capítulo 7 (Instalaciones asimilables a las domiciliarias).

| Tipo | Cuándo | Ubicación | Ventilación |
|---|---|---|---|
| **Interceptor de grasas y aceites y espuma** (7.6.3.1) | Cocinas comerciales, restaurantes, comedores | Antes de la conexión al primario, accesible para limpieza | **Ventilación Ø 0,100 m a los cuatro vientos** |
| **Interceptor de trapos** (7.6.3.2) | Lavaderos industriales, lavanderías | Idem | Idem |
| **Interceptor de nafta / hidrocarburos** | Cocheras con más de X vehículos, estaciones de servicio, talleres | Antes del bombeo | Ventilado |
| **Desarenador** | Rampas de cochera, playas | Aguas arriba del interceptor de nafta | — |

> **Para un PB+9 con subsuelo de cocheras en Santa Rosa:** consultar si el municipio exige interceptor de hidrocarburos en cocheras de vivienda colectiva. **Es una exigencia que aparece tarde y obliga a romper piso.** `[verificar en Código de Edificación de Santa Rosa y normativa de la APA]`
>
> **Laberinto para mezcla de productos y desinfección** (7.6.1 y 7.6.2): aplicable a efluentes industriales y de salud. No aplica a vivienda.

---

## 2.12 Sistemas estáticos: zonas sin cloaca

Fuente: Guía AySA/ERAS, Capítulo 8 — *Disposición del efluente cloacal en el terreno*. **Muy relevante para La Pampa**, donde una parte importante de la superficie construida (barrios periféricos, chacras, countries, localidades del interior provincial) está fuera de radio servido.

### 2.12.1 Esquema del sistema

> **Artefactos → cañería primaria → CÁMARA SÉPTICA → (zanjas de infiltración) o (pozo absorbente) → terreno**

La cámara séptica **no depura**: sedimenta sólidos y digiere anaeróbicamente parte de la materia orgánica, para que el efluente no obstruya los poros del terreno. La depuración final la hace el suelo.

### 2.12.2 Ensayo de infiltración (percolación) — apartado 8.3

**Este ensayo es obligatorio y no es opcional. Sin él, el sistema es una adivinanza.**

**Preparación del pozo (8.3.1):**
- El **nivel de fondo del pozo de ensayo debe coincidir con el nivel donde se producirá la infiltración**.
- Adecuar el contorno del pozo retirando todo el material suelto, para lograr una interfase natural suelo-líquido.
- Agregar **0,05 m de arena gruesa o grava fina** para protección del fondo.
- **Un ensayo cada 100 m²** de área de infiltración, abarcando todas las zonas.

**Técnica del ensayo (8.3.2):**
- Llenar con agua limpia hasta **0,30 m sobre la gravilla**.
- **Mantener el nivel constante durante 24 horas**, especialmente durante el período nocturno. Esto asegura que el suelo se expanda y llegue a la condición de la época más húmeda del año.

**Medición de la tasa (8.3.3):**
- Cumplido el período de 24 h, ajustar el nivel a 0,30 m sobre la gravilla.
- Medir el **tiempo necesario para un descenso de nivel de 0,025 m (2,5 cm)**.
- **En suelos arenosos** (donde los primeros 0,15 m se infiltran en menos de 30 min): después del período nocturno, continuar agregando agua durante una hora y medir el descenso de 0,025 m **en los últimos 10 minutos**.

**TABLA Nº 1 — Velocidad permisible de aplicación de líquidos cloacales a un sistema de infiltración:**

| Velocidad de filtración (minutos para un descenso de 2,5 cm) | **Velocidad máxima de aplicación Vi (litros/m²·día)** |
|---|---|
| 1 o menos | **189** |
| 2 | **130** |
| 3 | **109** |
| 4 | **94** |
| 5 | **83** |
| 10 | **60** |
| 15 | **49** |
| **30** * | **34** |
| **45** ** | **30** |
| **60** ** | **22** |

> \* **Más de 30 minutos es INADECUADO PARA POZOS ABSORBENTES.**
> \*\* **Más de 60 minutos es INADECUADO PARA CUALQUIER SISTEMA DE ABSORCIÓN.**
>
> **Nota:** en zanjas de infiltración, el área de absorción se calcula como **la del fondo de zanja**.

**Condición hidrogeológica insalvable:** *"La elevación máxima estacional del nivel freático deberá estar como máximo a **1,20 m por debajo del nivel de infiltración**, o de formaciones de rocas o de estratos impermeables."*

> **Consecuencia crítica para La Pampa:** hay zonas de la provincia con **napa alta y con suelos con estratos calcáreos (tosca)** a poca profundidad. En esos casos **el sistema estático clásico no es viable** y hay que ir a **planta compacta de tratamiento (biodigestor + filtro percolador o lodos activados) con vuelco a zanja de infiltración superficial o a cuerpo receptor autorizado**, lo que requiere aprobación de la autoridad ambiental provincial. `[verificar exigencias de la Secretaría de Ambiente / APA de La Pampa para vuelco de efluentes tratados]`

### 2.12.3 Distancias mínimas — TABLA Nº 2 (8.3.4)

Distancia horizontal en metros:

| Sistema | Pozo semisurgente | Cañería de abastecimiento de agua | Cuerpo receptor | Límites de propiedad |
|---|---|---|---|---|
| **Cañería primaria** | 15 | 3 | 15 | — |
| **Cámara séptica** | 15 | 3 | 15 | 3 |
| **Zanja de infiltración** | **35** | **10** | 15 | **5** |
| **Pozo absorbente** | **35** | **15** | 15 | **5** |

Adicionalmente (8.6.2): *"Las cámaras no deben estar a menos de 15 m de cualquier fuente de abastecimiento de agua y a no menos de 3 m de cualquier edificio."*

> **Advertencia de la Guía:** *"La contaminación subterránea puede moverse en cualquier dirección y a grandes distancias; su movimiento sigue el normal de las aguas freáticas de la zona."* En La Pampa, con perforaciones domiciliarias frecuentes, **estas distancias no son burocracia: son salud pública.**

### 2.12.4 Dimensionado de la cámara séptica — apartado 8.6.1

| Parámetro | Valor |
|---|---|
| **Tiempo mínimo de permanencia** | **24 horas** |
| **Tiempo óptimo** | **36 horas** |
| Caudal de diseño | Según Capítulo 2 (dotación), **multiplicado por un factor de 0,8** |
| **Volumen de barros** | **0,036 litros/habitante·día** (un habitante produce 54 g/día de sólidos, de los cuales ~36 g quedan sin digerir) |
| **Volumen de natas** | **0,018 litros/habitante·día** |
| Período entre limpiezas | **≈ 1 año** |

**Fórmula:**

> **V = N.º habitantes × Caudal_hab/día × 24 h + V_barros + V_natas**

(el primer término expresado como volumen de permanencia de 24 h)

**Especificaciones constructivas (8.6.3):**

| Requisito | Valor |
|---|---|
| Estanqueidad | **Estancas**; hormigón o mampostería de ladrillos fuertemente calcinados |
| Protección de superficies de hormigón | **Mastic asfáltico o similar** |
| Relleno perimetral | Capas de **no más de 0,05 m**, compactadas. **Llenar la cámara con agua antes de rellenar, para evitar flotación** |
| Accesos | En cada compartimiento, en entrada y salida. Dimensiones típicas **0,60 × 0,60 m**, con **contratapa** para evitar escape de gases |
| **Puente de ventilación** | Los compartimientos de entrada y salida se unen externamente con **cañería Ø 0,100 m**, para continuar el circuito de ventilación desde el sistema de infiltración hasta el remate de la línea cloacal |
| **Desnivel entrada-salida** | **≈ 0,08 m por metro** de distancia entre entrada y salida |
| Dispositivos de entrada/salida en cámaras de más de 1 m de ancho | **Mínimo 3 cañerías**, para distribución uniforme y evitar corrientes parásitas |
| **Deflector de entrada** | Orienta el efluente hacia abajo, penetrando **0,20 m por debajo del nivel líquido** |
| **Dispositivo de salida** | Penetra **0,40 m** por debajo del nivel líquido, para retener natas |

### 2.12.5 Pozo absorbente — apartado 8.5.1

| Requisito | Valor |
|---|---|
| Relleno de fondo | Piedra o canto rodado limpio de **0,05 m de espesor promedio**, hasta **0,30 m por debajo del nivel del fondo** |
| Paredes | Ladrillos **sin junta tomada** (pared de ≈ 0,10 m) o anillos premoldeados perforados |
| Espacio anular | Diámetro exterior de la pared **0,15 m menor que la excavación**, con relleno de piedra o canto rodado limpio hasta la parte superior |
| Cubierta | Abertura de **0,25 m** para inspección |
| Cañería de entrada | Se extiende hacia abajo **≈ 0,30 m**, para encauzar el efluente en forma descendente |
| Protección | Todas las superficies de hormigón protegidas con material asfáltico |
| **Limitación** | **Tiempo de percolación > 30 min → NO usar pozo absorbente** |

### 2.12.6 Zanjas de infiltración — apartado 8.4

| Requisito | Valor |
|---|---|
| Cañería | Perforada en los **180° inferiores**, perforaciones de **≈ 0,01 m** de diámetro |
| Protección | Grava debajo y sobre la cañería |
| **Profundidad mínima de la zanja** | **0,60 m** |
| Zanja estándar | **0,15 m de grava bajo la cañería** |
| Nivel freático | **> 1,20 m del fondo del sistema** |
| Pendientes y caudales | Según Capítulo 3 (3.5 y 3.6.1) |
| Más de una línea | **Cámara partidora de caudales** antes de la infiltración |

**Longitud del sistema (8.4.3):**

> **S [m²] = Qc [l/día] / Vi [l/m²·día]**
>
> **Li [m] = S [m²] / b [m]**   donde b = ancho de zanja

**TABLA Nº 3 — Porcentaje de aplicación del área según profundidad del medio filtrante bajo cañería:**

| Profundidad del medio filtrante bajo cañería | 30 cm | 45 cm | 60 cm | 90 cm | 120 cm | 150 cm |
|---|---|---|---|---|---|---|
| **30 cm** | 75 | 78 | 80 | 85 | 85 | 87 |
| **45 cm** | 60 | 65 | 65 | 70 | 75 | 80 |

*(anchos de zanja en el encabezado; valores en % del área requerida)*

> **Lectura de la tabla:** a mayor profundidad de grava bajo la cañería, se aprovecha la **infiltración lateral** además de la del fondo, y se necesita **menos longitud de zanja**. Con 45 cm de grava y zanja de 30 cm de ancho, se necesita apenas el 60 % del área teórica.

### 2.12.7 EJEMPLO RESUELTO — Sistema estático para vivienda unifamiliar en zona rural de La Pampa

**Datos:**
- Vivienda de 3 dormitorios → **5 habitantes**
- Dotación adoptada: **200 l/hab·día**
- Ensayo de percolación: **descenso de 2,5 cm en 8 minutos** (interpolando entre 5 min → 83 y 10 min → 60 l/m²·día)
- Napa freática: a 4,50 m de profundidad ✓ (> 1,20 m bajo el fondo del sistema)

**Paso 1 — Caudal de diseño:**
> Qc = 5 hab × 200 l/hab·día = **1.000 l/día**
> Con el factor de 0,8 de la Guía para el dimensionado de la cámara: Q_cámara = 1.000 × 0,8 = **800 l/día**

**Paso 2 — Tasa de infiltración (interpolación lineal en la Tabla Nº 1):**
> Entre 5 min (83 l/m²·día) y 10 min (60 l/m²·día):
> Vi = 83 − (8 − 5)/(10 − 5) × (83 − 60) = 83 − 0,6 × 23 = 83 − 13,8 = **69,2 l/m²·día**
>
> Adoptar conservadoramente **Vi = 69 l/m²·día**. (8 min < 30 min → **pozo absorbente admisible**; también zanjas.)

**Paso 3 — Volumen de la cámara séptica:**
> Volumen de permanencia (24 h): V₁ = 800 l = **0,80 m³**
> Volumen de barros (1 año): V₂ = 5 hab × 0,036 l/hab·día × 365 días = **65,7 l = 0,066 m³**
> Volumen de natas (1 año): V₃ = 5 hab × 0,018 l/hab·día × 365 días = **32,9 l = 0,033 m³**
>
> **V_total = 0,80 + 0,066 + 0,033 = 0,899 m³**

Aplicando el criterio de **permanencia óptima de 36 h** (recomendado):
> V₁' = 800 × 1,5 = 1.200 l = 1,20 m³ → **V_total = 1,20 + 0,099 = 1,30 m³**

**Cámara séptica adoptada: 1.500 litros útiles, de 2 compartimientos** (relación de volúmenes 2:1, el primero mayor), de hormigón armado, con deflectores de entrada (0,20 m de penetración) y salida (0,40 m), tapas de inspección de 0,60 × 0,60 m con contratapa, y puente de ventilación Ø 0,100 m entre compartimientos.

Dimensiones interiores orientativas: 2,00 m largo × 0,90 m ancho × 1,20 m de tirante líquido (+ 0,30 m de borde libre) → V_útil = 2,16 m³ ✓ con holgura.

**Paso 4 — Superficie de infiltración:**
> S = Qc / Vi = 1.000 / 69 = **14,5 m²**

**Paso 5a — Opción zanjas de infiltración:**
- Ancho de zanja b = **0,60 m**, profundidad de grava bajo cañería = **0,45 m**
- De la Tabla Nº 3: para 45 cm de grava y 60 cm de ancho → **65 %** del área
- S_corregida = 14,5 × 0,65 = **9,43 m²**
- **Li = 9,43 / 0,60 = 15,7 m → adoptar 16 m de zanja**
- Se ejecuta en **2 líneas de 8 m** separadas ≥ 2,0 m entre ejes, con **cámara partidora de caudales**.
- Profundidad de zanja: 0,60 m mínimo; en este caso **0,90 m** para alojar 0,45 m de grava bajo el caño.
- Cañería perforada Ø 0,100 m con pendiente **0,3 a 0,5 %** (baja, para distribución uniforme).

**Paso 5b — Opción pozo absorbente:**
- Superficie de absorción = superficie lateral del pozo (las paredes), no el fondo.
- Con S = 14,5 m² y un pozo de **Ø 1,50 m**: perímetro = π × 1,50 = 4,71 m
- **Profundidad útil = 14,5 / 4,71 = 3,08 m → adoptar 3,50 m de profundidad útil** (más 0,50 m de relleno de fondo y la cubierta).

**Paso 6 — Verificación de distancias (Tabla Nº 2):**

| Elemento | Distancia requerida | ¿Cumple en el terreno? |
|---|---|---|
| Cámara séptica a perforación de agua | 15 m | Verificar en implantación |
| Cámara séptica a edificio | 3 m | Verificar |
| Cámara séptica a límite de propiedad | 3 m | Verificar |
| Zanja/pozo a perforación de agua | **35 m** | ⚠ **El más restrictivo. En lotes chicos suele ser el que no cierra** |
| Zanja/pozo a cañería de agua | 10 / 15 m | Verificar |
| Zanja/pozo a límite de propiedad | 5 m | Verificar |

> **Conclusión práctica:** en un lote de 20 × 40 m con perforación propia, **la distancia de 35 m al pozo semisurgente es casi imposible de cumplir**. En esos casos: (a) conectarse a red si existe, (b) usar agua de red y no perforación, o (c) planta compacta de tratamiento con vuelco autorizado. **Este análisis se hace en el anteproyecto, sobre el plano de implantación, no cuando ya está la platea.**

---

# 3. DESAGÜES PLUVIALES

## 3.1 La lluvia de diseño: cómo obtener el dato para Santa Rosa

### 3.1.1 El problema

Las tablas de la Guía AySA/ERAS están calculadas para una **lluvia de 130 mm/h**, que es el valor histórico de diseño del área metropolitana de Buenos Aires. **Ese valor no es automáticamente aplicable a Santa Rosa.**

### 3.1.2 Fuentes de dato válidas, en orden de preferencia

| Prioridad | Fuente | Comentario |
|---|---|---|
| **1** | **Curvas IDF locales elaboradas por la APA (Administración Provincial del Agua) de La Pampa, la UNLPam o el INA** para la estación Santa Rosa | Es el dato correcto. **Pedirlo formalmente.** `[verificar disponibilidad en APA La Pampa / Facultad de Ingeniería UNLPam / INA]` |
| **2** | **"Estudio Piloto de Lluvias Intensas en la República Argentina"**, Moyano y Medina, 1974, Subsecretaría de Recursos Hídricos + FCEN-UBA | Es la fuente que la propia Guía AySA/ERAS indica usar cuando no hay estudios más modernos (apartado 5.9.2). Cubre todo el país |
| **3** | Serie de datos del **Servicio Meteorológico Nacional**, estación Santa Rosa (Aero), ajustada por Gumbel para obtener la IDF | Requiere trabajo de hidrología. Se justifica en obras grandes |
| **4** | Adoptar el valor de la Guía (130 mm/h) del lado seguro | **Conservador y probablemente sobredimensionado para La Pampa**, pero defendible. Es lo que haremos por defecto mientras no tengamos el dato local |

### 3.1.3 Datos climáticos de Santa Rosa que sí tenemos verificados

De **IRAM 11603, Anexo A**, estación **SANTA ROSA (AERO), La Pampa** (lat. −36,57; long. −64,27; 191 m s.n.m.), serie 1980/2009:

| Parámetro | Invierno | Verano |
|---|---|---|
| Precipitación media del período | **105 mm** | **380 mm** |
| Humedad relativa media | 73 % | 61,6 % |

> **Lectura hidrológica:** Santa Rosa es un régimen **marcadamente estival**: llueve casi 4 veces más en verano. Las lluvias intensas de corta duración (las que dimensionan un desagüe pluvial) son de **origen convectivo, en verano**, y pueden ser violentas. **No subestimar la intensidad por el hecho de que la precipitación anual total (≈ 700 mm) sea menor que la de Buenos Aires.**

### 3.1.4 Recurrencia de diseño

| Elemento a dimensionar | Período de retorno recomendado |
|---|---|
| Embudos y bajadas de azotea de vivienda | 5 a 10 años |
| Colectores y albañales | 10 años |
| **Sistemas de retardo / retención** | **≥ 50 años** (exigencia expresa de la Guía, 5.9.2) |
| Desagüe de rampas de subsuelo y sótanos | **50 a 100 años** — el daño de una inundación de subsuelo es catastrófico |

### 3.1.5 Método racional (para superficies > 1.000 m² — apartado 5.10)

> **Q = C × i × A / 3,6**
>
> Q en l/s, C = coeficiente de escorrentía (adimensional), i = intensidad en mm/h, A = área en **hectáreas** ÷ ... — **cuidado con las unidades.** Forma práctica:
>
> **Q [l/s] = (C × i [mm/h] × A [m²]) / 3.600**

**Coeficientes de escorrentía C:**

| Superficie | C |
|---|---|
| Azotea impermeabilizada, cubierta metálica | **0,95 – 1,00** |
| Azotea verde extensiva | 0,30 – 0,50 |
| Pavimento de hormigón / asfalto | 0,85 – 0,95 |
| Adoquinado con juntas | 0,70 – 0,85 |
| Grava suelta | 0,15 – 0,30 |
| Césped en suelo arenoso, pendiente < 2 % | 0,05 – 0,10 |
| Césped en suelo arcilloso, pendiente > 7 % | 0,25 – 0,35 |

`[verificar valores de C contra la bibliografía adoptada; existen tablas más finas en el Manual de Drenaje del INA y en la bibliografía de hidrología urbana]`

**Verificación de coherencia con la Guía:** la Guía usa implícitamente, para el bombeo pluvial (5.5), **0,036 l/s por m² de superficie desaguada**. Eso equivale a:
> i = 0,036 l/s·m² × 3.600 / 1,00 = **129,6 mm/h ≈ 130 mm/h** ✓ (coincide con la lluvia de diseño declarada, con C = 1,0)

Y en el apartado 3 (desagües primarios) aparece **0,033 l/s por m² de superficie de aporte** para pluvial a cloaca, equivalente a ≈ **119 mm/h**.

---

## 3.2 Superficie de aporte: reglas de cómputo

### 3.2.1 Superficies adicionales — apartado 5.8

> *"A las superficies consideradas para el diseño deben adicionarse los aportes que los muros verticales anexos a estas superficies, considerando como mínimo el **área del muro vertical reducida en un 50 %**."*

> **Traducción:** una azotea de 200 m² rodeada por un parapeto de 1,00 m de altura y 60 m de perímetro aporta además 60 × 1,00 × 0,50 = **30 m²**. Superficie de cálculo: **230 m²**. En edificios entre medianeras con muros altos de división, el aporte de los paramentos verticales puede ser importante y es lo que se olvida.

### 3.2.2 Definición de balcón (5.1.1)

> *"Se considera balcón a toda superficie limitada por baranda o parapeto, accesible y saliente más de **0,20 m** de la cara externa de los muros."*

**Todo balcón debe tener desagüe proyectado.** No se admite que escurra por el borde.

### 3.2.3 Prohibiciones de libre escurrimiento (5.7)

| Prohibición |
|---|
| Escurrimiento superficial entre dependencias accesibles de **unidades locativas distintas** (se permite solo entre superficies absorbentes y entre terrazas: embudo debajo del tabique divisorio) |
| Escurrimiento superficial en **lugares cubiertos** (se permite bajo semicubierto que reciba descubiertos adyacentes) |
| Desagüe por libre escurrimiento a **patios de uso privativo** |
| **Definición:** se entiende por libre escurrimiento el que se realiza a través de **al menos la mitad del perímetro no empotrado** del saliente o del lado de la superficie a desaguar que da al vacío. **Cualquier otra solución que genere mayor concentración del desagüe está prohibida** |

> **Consecuencia de proyecto para balcones:** el balcón "que desagua por el frente" es la solución que menos molestias da al arquitecto y la que **está prohibida** si concentra el escurrimiento. **Todo balcón lleva embudo o rejilla lineal conectada a montante pluvial.** En un PB+9 con balcones corridos, hay que prever **un montante pluvial por columna de balcones** y su pase de losa, desde el anteproyecto.

### 3.2.4 Otras obligaciones

- **Obligatorio el desagüe de entradas de vehículos y de playas descubiertas** (Figura 5.3 de la Guía).
- Cañerías principales y de albañal no suspendidas: **separadas 0,40 m como mínimo** (distancia libre entre filos exteriores en proyección horizontal). **No se permiten superpuestas.**

---

## 3.3 Embudos, piletas de piso pluviales y canaletas

### 3.3.1 TABLA Nº 8 — Capacidades de embudos

| Dimensiones (m) | Material | Caudal de desagüe (l/s) | **Superficie de desagüe (m²)** |
|---|---|---|---|
| 0,15 × 0,15 | H°F° | 0,51 | **14** |
| 0,15 × 0,15 | Plástico | 0,68 | **19** |
| 0,20 × 0,20 | H°F° | 1,36 | **38** |
| 0,20 × 0,20 | Plástico | 1,53 | **43** |
| 0,30 × 0,30 | H°F° | 2,55 | **71** |
| 0,30 × 0,30 | Plástico | 3,06 | **85** |

### 3.3.2 TABLA Nº 9 — Capacidades de piletas de piso (pluviales)

| Dimensiones (m) | Material | Caudal de desagüe (l/s) | **Superficie de desagüe (m²)** |
|---|---|---|---|
| 0,06 | H°F° | 0,17 | **5** |
| 0,06 | Plástico | 0,34 | **9** |
| 0,10 | H°F° | 2,55 | **71** |
| 0,10 | Plástico | 3,06 | **85** |
| 0,15 | H°F° | 4,25 | **118** |
| 0,15 | Plástico | 5,10 | **142** |

### 3.3.3 TABLA Nº 1 — Superficie máxima para canaletas impermeables

| Sección a (ancho) × b (altura) | 0,10 × 0,10 m | 0,15 × 0,15 m | 0,15 × 0,25 m | 0,15 × 0,30 m |
|---|---|---|---|---|
| **Superficie máxima (m²)** | **250** | **600** | **1.200** | **1.600** |

- Las canaletas de zinc **pueden estar adosadas a medianera, pero nunca encima de ellas**.

---

## 3.4 Montantes (caños de lluvia) y albañales

### 3.4.1 Capacidad de los verticales pluviales — Tablas Nº 4 a 7

**Ø 0,100 m:**

| Factor de llenado r | 0,15 | 0,20 | 0,25 | 0,33 |
|---|---|---|---|---|
| Caudal máximo de transporte (l/s) | 2,99 | **4,84** | 7,02 | 11,14 |
| **Superficie máxima a desaguar (m²)** | 83 | **134** | 194 | 309 |

**Ø 0,150 m:**

| Factor de llenado r | 0,15 | 0,20 | 0,25 | 0,33 |
|---|---|---|---|---|
| Caudal máximo (l/s) | 8,83 | **14,26** | 20,69 | 32,86 |
| **Superficie máxima (m²)** | 244 | **395** | 573 | 910 |

**Ø 0,200 m:**

| Factor de llenado r | 0,15 | 0,20 | 0,25 | 0,33 |
|---|---|---|---|---|
| Caudal máximo (l/s) | 19,01 | **30,71** | 44,55 | 70,77 |
| **Superficie máxima (m²)** | 527 | **851** | 1.234 | 1.960 |

**Ø 0,300 m:**

| Factor de llenado r | 0,15 | 0,20 | 0,25 | 0,33 |
|---|---|---|---|---|
| Caudal máximo (l/s) | 56,07 | **90,57** | 131,38 | 208,70 |
| **Superficie máxima (m²)** | 1.553 | **2.508** | 3.638 | 5.779 |

> **NOTA EXPRESA DE LA GUÍA:** *"Se recomienda en el diseño de los verticales pluviales que el factor de llenado r no supere el valor de 0,20."*
>
> **Regla de proyecto que se deriva:** **usar siempre la columna r = 0,20**.
> - **Ø110 → 134 m² máximo**
> - **Ø160 → 395 m² máximo**
> - **Ø200 → 851 m² máximo**

### 3.4.2 Restricciones del Ø 0,060 m

| Regla |
|---|
| El uso de caño de lluvia de **0,060 m tiene carácter restrictivo** |
| **No puede recibir en una misma planta una superficie que exceda los 10 m²** |
| **No debe contar con desviación alguna** |
| **Prohibidos diámetros menores a 0,060 m** |
| El tramo horizontal de Ø 0,060 m puede ser de ese diámetro **únicamente si su largo no excede de 3,00 m**. De 3,00 m en adelante, **Ø 0,100 m** |
| **Prohibido embutir caño de lluvia común en medianera** |
| Se permite caño de lluvia horizontal suspendido en locales amplios, galpones, depósitos, **aislado de la medianera** |

### 3.4.3 Caso especial: montante alta cerca de la línea municipal

> *"Caño de lluvia a menos de 4,00 m de la línea oficial y cuyo afluente más bajo esté a más de 30 m de altura: **boca de desagüe tapada especial, con reductor de velocidad al pie**, salida en un número de cañerías de 0,100 m que aseguren una velocidad **no mayor a 1,5 m/s** sobre línea de edificación."*

> **Esto aplica directamente a un PB+9.** Con 10 plantas de 2,90 m, el afluente más alto está a ~29 m; si hay sala de máquinas o tanques, se pasan los 30 m. **Verificar y, si corresponde, proyectar el reductor de velocidad al pie de la montante.** Sin él, el agua sale a 8-10 m/s y erosiona la boca de desagüe y la vereda.

### 3.4.4 Albañales

| Parámetro | Valor |
|---|---|
| **Diámetro mínimo** | **0,100 m** |
| Relación tirante/diámetro | **0,5 < h/d < 0,7** *(distinta a la de cloaca, que es 0,3-0,7)* |
| **Velocidad mínima** | **> 0,90 m/s** a sección llena *(mayor que la cloacal de 0,60 m/s)* |
| Verificación | Manning, con n = 0,011 (plástico), 0,015 (hierro fundido), 0,011 (latón) |
| Enlaces por boca de desagüe o ramal | **A favor de la corriente (mínimo 90°)** |
| Acometida a cordón con pendiente de cuneta > 2 % | Tramo final de al menos **0,50 m** inclinado al menos **45°** respecto de la perpendicular al cordón, **a favor de la pendiente** |

**TABLA Nº 2 — Capacidades de albañales de materiales plásticos (h/d = 0,7; lluvia 130 mm/h), caudal en l/s:**

| Pendiente | 0,100 m | 0,150 m | 0,200 m | 0,250 m | 0,300 m |
|---|---|---|---|---|---|
| 1:10 (0,1000) | 13,5 | 39,9 | 86,0 | 155,9 | 253,4 |
| 1:20 (0,0500) | 9,6 | 28,2 | 60,8 | 110,2 | 179,2 |
| 1:30 (0,0333) | 7,8 | 23,1 | 49,6 | 90,0 | 146,3 |
| 1:40 (0,0250) | 6,8 | 20,0 | 43,0 | 77,9 | 126,7 |
| **1:50 (0,0200)** | **6,1** | **17,9** | **38,4** | **69,7** | **113,3** |
| 1:60 (0,0167) | 5,5 | 16,3 | 35,1 | 63,6 | 103,5 |
| 1:70 (0,0143) | 5,1 | 15,1 | 32,5 | 58,9 | 95,8 |
| 1:80 (0,0125) | — | 14,1 | 30,4 | 55,1 | 89,6 |
| 1:90 (0,0111) | — | 13,3 | 28,7 | 52,0 | 84,5 |
| **1:100 (0,0100)** | — | **12,6** | **27,2** | **49,3** | **80,1** |
| 1:200 (0,0050) | — | 8,9 | 19,2 | 34,9 | 56,7 |
| 1:250 (0,0040) | — | 8,0 | 17,2 | 31,2 | 50,7 |
| 1:300 (0,0033) | — | 7,3 | 15,7 | 28,5 | 46,3 |
| 1:500 (0,0020) | — | — | — | 22,0 | 35,8 |

**TABLA Nº 3 — Capacidades de albañales de hierro fundido (l/s):**

| Pendiente | 0,100 m | 0,150 m | 0,200 m | 0,250 m | 0,300 m |
|---|---|---|---|---|---|
| 1:10 | 11,5 | 33,8 | 72,7 | 131,9 | 214,4 |
| 1:20 | 8,1 | 23,9 | 51,4 | 93,3 | 151,6 |
| 1:30 | 6,6 | 19,5 | 42,0 | 76,1 | 123,8 |
| 1:40 | 5,7 | 16,9 | 36,4 | 65,9 | 107,2 |
| **1:50** | **5,1** | **15,1** | **32,5** | **59,0** | **95,9** |
| 1:60 | — | 13,8 | 29,7 | 53,8 | 87,5 |
| 1:70 | — | 12,8 | 27,5 | 49,8 | 81,0 |
| 1:80 | — | 11,9 | 25,7 | 46,6 | 75,8 |
| 1:90 | — | 11,3 | 24,2 | 44,0 | 71,5 |
| **1:100** | — | **10,7** | **23,0** | **41,7** | **67,8** |
| 1:200 | — | 7,6 | 16,3 | 29,5 | 47,9 |
| 1:250 | — | — | — | 26,4 | 42,9 |
| 1:300 | — | — | — | 24,1 | 39,1 |

> Las celdas vacías indican combinaciones diámetro-pendiente que **no cumplen la velocidad mínima de 0,90 m/s**. Por eso el Ø 0,100 m no aparece con pendientes menores a 1:70 en plástico ni 1:50 en hierro fundido: **el Ø110 pluvial necesita pendiente fuerte.**

---

## 3.5 Pendientes de azotea y balcones

| Elemento | Pendiente mínima recomendada |
|---|---|
| **Azotea accesible con solado** | **1,0 % a 1,5 %** hacia embudos |
| **Azotea inaccesible con membrana** | **1,5 % a 2,0 %** |
| **Balcón** | **1,0 % a 1,5 %** hacia el desagüe, **nunca hacia el interior** |
| Canaleta de chapa | **0,5 % a 1,0 %** hacia la bajada |
| Terraza jardín / azotea verde | 1,5 % en la lámina drenante bajo el sustrato |
| Cochera descubierta / rampa | **2,0 % mínimo**, hacia rejilla lineal |

**Reglas de proyecto complementarias:**

| Regla | Motivo |
|---|---|
| **Mínimo 2 embudos por azotea**, aunque el cálculo dé uno | Redundancia ante obstrucción por hojas o basura |
| **Rebosaderos (aliviaderos) en el parapeto**, a 5 cm sobre el nivel del solado | Si se tapan los embudos, la azotea se convierte en piscina y colapsa la losa. **Es una medida de seguridad estructural, no de sanitarias** |
| Embudo **nunca en el punto más alejado**: siempre en el punto bajo del plano de escurrimiento | Obvio pero se dibuja mal |
| Distancia máxima embudo-punto más alejado | ≈ 15 m, para no acumular espesor de contrapiso |
| **Cazoleta del embudo con reja y canasto** | Se limpia; sin canasto se tapa el caño |
| **Doble sellado de membrana en el embudo** | Es el punto de falla número uno de toda cubierta |

---

## 3.6 Bombeo pluvial de subsuelos — apartado 5.5

| Parámetro | Valor normativo |
|---|---|
| **Capacidad del pozo impermeable** | A razón de **0,036 l/s por m² de superficie de desagüe**, con un tiempo de **10 minutos** |
| **Capacidad máxima del pozo** | **1.000 litros.** Capacidades mayores deben solicitarse por expediente |
| Ubicación del pozo | Alejado **0,80 m mínimo** del filo interior de la medianera, en lugar común |
| Ubicación de la bomba | Alejada **0,80 m mínimo** del filo interior de la medianera, en lugar común |
| Antivibratorio | Obligatorio en los equipos de bombeo |
| A la salida de las bombas | **Junta elástica y válvula de retención**, obligatorias |
| Documentación | Indicar caudal en m³/h, altura manométrica y superficie a desaguar |
| Diámetro de aspiración | Velocidad de circulación de **1 a 1,5 m/s** |
| Diámetro de impulsión | Velocidad **no mayor a 1,5 m/s**. **No puede estar embutido en medianera** |

**Fórmula del volumen del pozo:**
> **V [l] = 0,036 [l/s·m²] × A [m²] × 600 [s]**

*Ejemplo:* rampa de cochera de 60 m² + patio de 40 m² = 100 m² →
> V = 0,036 × 100 × 600 = **2.160 l**
>
> **> 1.000 l → excede el máximo de la Guía: hay que tramitar por expediente**, o reducir la superficie que llega al pozo (por ejemplo, con una rejilla transversal en lo alto de la rampa que capte el agua que baja de la calle y la derive por gravedad).

**Caudal de la bomba:**
> Q_bomba ≥ 0,036 × A = 0,036 × 100 = **3,6 l/s = 12,96 m³/h**

**Configuración:** **2 bombas alternadas** (una de reserva), sumergibles, con impulsor abierto o vórtex, alarma de nivel alto, **alimentación desde el tablero de servicios generales con conexión al grupo electrógeno si existe**.

> **Advertencia de proyecto:** la rampa de cochera de un subsuelo es el punto por donde entra el agua de la calle en una tormenta extraordinaria. **Prever siempre: (a) resalto o lomo de burro en el arranque de la rampa, por encima de la cota de vereda; (b) rejilla lineal transversal en lo alto; (c) segunda rejilla al pie; (d) bombeo con redundancia y alarma.** Y verificar el nivel del cordón: si la vereda está por debajo de la calzada, hay que terraplenar (la Guía lo indica expresamente en 5.1.1).

---

## 3.7 Sistemas de retardo (retención pluvial) — apartado 5.9

### 3.7.1 Cuándo aplica

> Cuando se impermeabilice parcial o totalmente la superficie de la parcela **dentro del centro libre de manzana** por construcción de **subsuelos destinados a estacionamiento**, las aguas de lluvia provenientes del total de la superficie construida detrás de la Línea Interior de Basamento (**Superficie de Captación**) deben ser tratadas de manera de demorar su escurrimiento fuera de la propiedad.

> **Si el municipio de Santa Rosa tiene una exigencia equivalente, hay que verificarla antes del anteproyecto: condiciona el subsuelo y el presupuesto.** `[verificar en Código de Edificación de Santa Rosa]`

### 3.7.2 Requisitos del sistema

| Requisito |
|---|
| El sistema (elementos de toma, canalizaciones, reservorios, bombeo, impulsiones, ventilaciones y albañales) debe ser **independiente de cualquier otra instalación sanitaria** |
| El retardo se genera interponiendo **recipientes** que reciben el agua y se vacían por **bombeo** |
| Los recipientes deben reunir las características técnicas de **pozos de bombeo o tanques de agua contra incendio** |
| El agua bombeada se conduce fuera del predio por **albañal exclusivo**, que la recibe a través de **boca de desagüe tapada, ventilada con caño de Ø 0,060 m mínimo** |
| El albañal debe tener una **boca de desagüe tapada a menos de 10 m de la línea oficial** |
| **No se permite proyectar un sistema de bombeo que erogue un caudal mayor que el determinado** — el sobredimensionado de la bomba anula el efecto de retardo y está expresamente prohibido |

### 3.7.3 Parámetros de diseño (5.9.2)

| Parámetro | Valor |
|---|---|
| **Recurrencia de la lluvia de diseño** | **≥ 50 años** |
| **Fuente de los parámetros de la ecuación de lluvia** | *Estudio Piloto de Lluvias Intensas en la República Argentina* (Moyano y Medina, 1974, SSRH + FCEN), **de no presentarse estudios más modernos** |
| **Demora en el arranque del bombeo desde el inicio de la lluvia** | **≥ 10 minutos** |
| **Máximo caudal que puede erogar el bombeo** | El equivalente al que genera una lluvia de **30 mm/h** aplicada sobre la Superficie de Captación |

### 3.7.4 Dimensionado — procedimiento

1. Construir la **curva IDF** para T = 50 años.
2. Construir el **hietograma de diseño** (bloques alternos u otro método).
3. Calcular minuto a minuto: intensidad, altura caída, **volumen caído acumulado**.
4. Calcular el **volumen bombeado acumulado** = Q_bomba × (t − 10 min), con Q_bomba = 30 mm/h × A_captación / 3.600 [l/s].
5. **Volumen acumulado en el reservorio = volumen caído − volumen bombeado.**
6. **La capacidad neta del reservorio es el máximo de esa diferencia.**

### 3.7.5 Documentación exigida (5.9.3)

Memoria de cálculo firmada por propietario e instalador, con:
a) Parámetros adoptados
b) Ecuación de la lluvia de diseño
c) Demora en el arranque del bombeo
d) Máximo caudal erogable
e) Dimensionamiento de la capacidad neta de acumulación
f) Cálculo hidráulico del caudal real del sistema proyectado, con **isometría de la impulsión y curva característica de la bomba indicando el punto de funcionamiento**
g) Verificación de la capacidad del albañal exclusivo
h) **Tabla minuto a minuto** con intensidad, altura total caída, volumen caído, volumen bombeado y volumen acumulado, **resaltando el máximo**
i) **Gráficos**: intensidad y altura caída vs. tiempo; volumen caído, bombeado y acumulado vs. tiempo, resaltando el máximo

---

## 3.8 EJEMPLO RESUELTO — Azotea de 320 m² con balcones

### Datos
- Edificio PB+9 del Ejemplo Nº 1.
- **Azotea:** 320 m² de superficie en planta, con parapeto de 1,10 m de altura y 74 m de perímetro.
- **Balcones:** 4 columnas de balcones de 8 m² cada uno, 9 pisos → 36 balcones.
- Lluvia de diseño adoptada: **130 mm/h** (criterio conservador, a falta de IDF local). `[reemplazar por el dato de La Pampa cuando se obtenga]`
- Destino del pluvial: **calzada** (Guía 5.1.2: en nuevo radio, desagüe de lluvia en general a calzada).

### Paso 1 — Superficie de cálculo de la azotea

> Superficie en planta: 320 m²
> Aporte de paramentos verticales (5.8): 74 m × 1,10 m × 0,50 = **40,7 m²**
> **Superficie de cálculo = 320 + 40,7 = 360,7 m² → adoptar 361 m²**

### Paso 2 — Caudal de la azotea

> Q = (C × i × A) / 3.600 = (1,00 × 130 × 361) / 3.600 = **13,04 l/s**

Verificación con el criterio directo de la Guía: 0,036 l/s·m² × 361 = **13,00 l/s** ✓ (coinciden)

### Paso 3 — Montantes de la azotea

Con **r = 0,20** (valor recomendado):
- Ø 0,100 m → 134 m² máximo
- Ø 0,150 m → 395 m² máximo

**Opción A — Una montante de Ø160:** 361 m² < 395 m² ✓, pero **NO cumple la regla de tener al menos dos bajadas**.

**Opción B (ADOPTADA) — Tres montantes de Ø110:**
- Superficie por montante: 361 / 3 = **120,3 m² < 134 m²** ✓
- Caudal por montante: 13,04 / 3 = **4,35 l/s < 4,84 l/s** ✓
- **Adoptar 3 embudos + 3 montantes de Ø 0,110 m**, más **2 rebosaderos de emergencia en el parapeto**.

### Paso 4 — Embudos de la azotea

De la Tabla Nº 8, embudo **plástico de 0,20 × 0,20 m**: 43 m². **Insuficiente para 120 m² por montante.**
Embudo **plástico de 0,30 × 0,30 m**: **85 m²**. Sigue siendo insuficiente.

**Corrección:** con embudos de 0,30 × 0,30 m plásticos (85 m² c/u), se necesitan:
> 361 / 85 = 4,25 → **5 embudos**

**Solución adoptada:** **5 embudos de 0,30 × 0,30 m plásticos**, conectados de a pares/individualmente a **3 montantes de Ø110** (dos montantes reciben 2 embudos cada una, una recibe 1). Verificación por montante: la de 2 embudos recibe 2 × 85 = 170 m² > 134 m² ❌.

**Solución definitiva:** **5 embudos de 0,30 × 0,30 m plásticos, cada uno con su propia bajada:**
- 5 montantes de **Ø 0,110 m**, cada una recibiendo **361/5 = 72,2 m² < 134 m²** ✓✓ (con amplio margen)
- Caudal por montante: 13,04/5 = **2,61 l/s < 4,84 l/s** ✓
- Capacidad del embudo: 85 m² > 72,2 m² ✓
- **Más 2 rebosaderos de emergencia** en el parapeto, de 20 × 5 cm de luz, a 5 cm sobre el solado.

> **Lección del ejemplo:** en las azoteas de edificios **el elemento limitante casi nunca es el diámetro de la montante, sino la capacidad del embudo**. Es el error más frecuente en el proyecto pluvial: se calcula la bajada y se pone "un embudo" sin verificar su capacidad.

### Paso 5 — Balcones

Cada balcón: 8 m² + aporte del paramento del antepecho (3,5 m × 1,10 m × 0,50 = 1,9 m²) = **9,9 m² ≈ 10 m²**

Una montante Ø 0,110 m con r = 0,20 admite 134 m². Una columna de 9 balcones aporta 9 × 10 = **90 m² < 134 m²** ✓

Pero como los balcones descargan a distintas alturas y el caño de Ø0,060 m está limitado a **10 m² por planta sin desviación**, la solución es:
- **Embudo de 0,15 × 0,15 m plástico (19 m² > 10 m² ✓) en cada balcón**
- **Ramal de Ø 0,060 m** del embudo a la montante (**≤ 10 m² por planta ✓, sin desviación ✓, tramo horizontal ≤ 3,00 m ✓**)
- **1 montante pluvial de Ø 0,110 m por columna de balcones** (4 montantes en total)
- **Pase de losa previsto en cada balcón desde el proyecto de estructura**

### Paso 6 — Colector y albañal

Caudal total del edificio:
> Azotea: 13,04 l/s
> Balcones: 4 columnas × 90 m² = 360 m² → 0,036 × 360 = **12,96 l/s**
> **Q_total pluvial = 26,0 l/s**

Albañal a calzada, PVC, pendiente **1:50 (2 %)**:
- De la Tabla Nº 2: Ø 0,150 m al 1:50 → **17,9 l/s** ❌ insuficiente
- Ø 0,200 m al 1:50 → **38,4 l/s** ✓
- **Adoptar albañal Ø 0,200 m con pendiente 1:50 (2 %).**

Verificación con pendiente menor, 1:100 (1 %):
- Ø 0,200 m al 1:100 → **27,2 l/s** ✓ (justo)
- **Ø 0,200 m al 1:80 (1,25 %) → 30,4 l/s ✓ con margen. ADOPTAR.**

### Paso 7 — Verificación del reductor de velocidad al pie

Las montantes de azotea reciben su afluente más alto a ~32 m de altura (nivel de azotea + parapeto). Si alguna corre **a menos de 4,00 m de la línea oficial** y su **afluente más bajo está a más de 30 m** → hay que proyectar **boca de desagüe tapada especial con reductor de velocidad al pie**, con salida en cañerías de Ø 0,100 m que aseguren **velocidad ≤ 1,5 m/s** sobre la línea de edificación.

En este caso: el afluente más bajo de las montantes de balcones está en el 1.º piso (~5 m), **no aplica**. Para las montantes de azotea, cuyo único afluente está a 32 m: **sí aplica si están a menos de 4 m de la línea oficial**. Verificar en planta y, si corresponde, proyectar el reductor.

### Resumen

| Elemento | Solución |
|---|---|
| Superficie de cálculo de azotea | **361 m²** (320 en planta + 41 de paramentos) |
| Caudal de azotea | **13,04 l/s** |
| Embudos de azotea | **5 × 0,30 × 0,30 m plásticos** |
| Montantes de azotea | **5 × Ø 0,110 m** (72 m² c/u) |
| Rebosaderos de emergencia | **2 en parapeto**, 20 × 5 cm |
| Embudos de balcón | **1 × 0,15 × 0,15 m plástico por balcón** |
| Ramales de balcón | **Ø 0,060 m**, ≤ 3,00 m, sin desviación |
| Montantes de balcones | **4 × Ø 0,110 m** |
| Caudal total | **26,0 l/s** |
| Albañal a calzada | **Ø 0,200 m, pendiente 1:80 (1,25 %)** |
| Reductor de velocidad al pie | **Verificar** en montantes de azotea a < 4 m de LO |

---

# 4. GAS

## 4.1 Marco normativo

| Norma | Objeto |
|---|---|
| **NAG-200** | *Reglamento Técnico para la ejecución de instalaciones internas domiciliarias de gas.* Es LA norma de la instalación interna: cañería, artefactos, evacuación de gases, ventilación de ambientes, gabinetes, pruebas y trámite. Reemplaza a las históricas *Disposiciones y normas mínimas para la ejecución de instalaciones domiciliarias de gas* (1982) |
| **NAG-201** | Instalaciones industriales y de mayor porte / redes internas de mayor complejidad `[verificar alcance exacto de la edición vigente en enargas.gob.ar]` |
| **NAG-237** | Conjunto puerta-marco de gabinetes de medidores |
| **NAG-215** | Rejillas fijas de ventilación |
| **NAG-250** | Caños de acero para instalaciones de gas |
| **NAG-E 209** | Sistemas de tubería de cobre |
| **NAG-E 210** | Sistemas de tubería de polietileno-acero |
| **NAG-202** | Calificación de inspectores |

> **Los valores de este capítulo provienen del texto de NAG-200 (edición 2019, sometida a consulta pública). ENARGAS publicó posteriormente una edición 2025.** `[VERIFICAR CONTRA LA EDICIÓN VIGENTE de NAG-200 en enargas.gob.ar antes de firmar cualquier plano de gas]`

**Quién ejecuta y quién firma:** las instalaciones de gas solo pueden ser proyectadas, ejecutadas y presentadas por **Instalador Matriculado** habilitado por la prestadora (Camuzzi Gas Pampeana en la región). **El arquitecto no firma la instalación de gas.** Su rol es coordinar, prever espacios (gabinete, plenos, conductos, rejillas) y verificar que el proyecto de gas sea compatible con el proyecto arquitectónico.

---

## 4.2 Gas de proyecto y presiones

### 4.2.1 Características del gas de proyecto (4.6.1)

> Las instalaciones deben proyectarse para **gas natural con poder calorífico superior de 38,94 MJ/m³ (9.300 kcal/m³) y densidad relativa de 0,65** (aire = 1), salvo en zonas alejadas de fuentes actuales o futuras de GN, donde se considera el gas efectivamente a utilizar.

Para **GLP**: densidad relativa **1,52**.

### 4.2.2 Consumo mínimo de proyecto (4.6.2)

> Las instalaciones residenciales deben proyectarse, **como mínimo**, previendo el consumo de una **cocina doméstica y un calentador de agua**, dimensionando la cañería con una **potencia mínima de 21,63 kW (18.600 kcal/h)**.

> **Consecuencia:** aunque el comitente diga "en este departamento solo va la cocina", **la cañería se dimensiona para cocina + calefón**. No se puede subdimensionar por lo que hoy se instala.

### 4.2.3 Presiones y pérdidas de carga

| Concepto | Valor |
|---|---|
| **Baja presión** | ≤ 100 mbar. Presión de servicio nominal: **19 mbar** |
| **Media presión** | 100 mbar < P ≤ 4 bar. Presión mínima garantizada de cálculo: **0,5 bar** |
| **Pérdida de carga máxima admisible entre cada artefacto y el medidor** (todos los artefactos a máxima potencia) | **1 mbar (10 mm.c.a.)** |
| **Pérdida de carga máxima en tramo de media presión** | **≤ 10 % de la presión de entrada** |
| **Presión mínima en la válvula de corte de cada artefacto** | **≥ 19 mbar** |
| **Velocidad máxima del gas — baja presión** (P ≤ 100 mbar) | **≤ 7 m/s** |
| **Velocidad máxima del gas — media presión** (100 mbar < P ≤ 4 bar) | **≤ 20 m/s** |
| **Diámetro nominal mínimo de la instalación interna** | **9,5 mm (⅜")** |
| **Diámetro nominal mínimo de prolongación en media presión** | **13 mm (½")** |

**Fórmula de velocidad (4.6.7):**
> **V = 358,36 × Q / (d² × Pa)**
>
> V en m/s, Q en m³/h, d = diámetro interior en mm, Pa = presión absoluta al final del tramo en bar A (P manométrica + 1,01325 bar)

---

## 4.3 Caudales nominales por artefacto

### 4.3.1 Fórmula base (4.6.3)

> **Q [m³/h] = Cm [kcal/h] / Hs [kcal/m³]**
>
> con **Hs = 9.300 kcal/m³** para gas natural

### 4.3.2 TABLA E.1 (NAG-200, Anexo E) — Consumo medio de artefactos domésticos

| Artefacto | Cm (kcal/h) | **Q (m³/h)** |
|---|---|---|
| **COCINAS** | | |
| Quemador de hornalla chico | 800 – 1.000 | 0,086 – 0,11 |
| Quemador de hornalla mediano | 1.200 – 1.400 | 0,13 – 0,15 |
| Quemador de hornalla grande | 2.000 | 0,22 |
| Quemador de horno | 2.500 – 4.000 | 0,27 – 0,43 |
| **CALENTADORES DE AGUA INSTANTÁNEOS (CALEFONES)** | | |
| de 10 l/min | 15.000 – 16.000 | **1,61 – 1,72** |
| de 12 l/min | 18.000 – 19.000 | **1,94 – 2,04** |
| de 14 l/min | 21.000 – 22.400 | **2,26 – 2,41** |
| de 16 l/min | 24.000 – 25.500 | **2,58 – 2,74** |
| **TERMOTANQUES (acumulación de rápida recuperación)** | | |
| de 50 l | 4.000 – 5.000 | 0,43 – 0,54 |
| de 75 l | 5.000 – 6.500 | 0,54 – 0,70 |
| de 110 l | 6.500 – 8.000 | 0,70 – 0,86 |
| de 150 l | 8.000 – 9.500 | 0,86 – 1,02 |
| **CALEFACTORES (cámara abierta con ventilación al exterior, y cámara estanca / balanceados)** | | |
| — | 2.500 | 0,27 |
| — | 3.000 | 0,32 |
| — | 4.500 | 0,48 |
| — | 6.000 | 0,65 |
| — | 9.000 | 0,97 |
| — | 10.000 | 1,08 |
| **CALEFACCIÓN CENTRAL POR AIRE CALIENTE FORZADO** | | |
| ámbito doméstico | 12.000 – 60.000 | 1,29 – 6,45 |
| ámbito comercial | 60.000 – 600.000 | 6,45 – 64,52 |
| **HELADERAS (a gas)** | | |
| 0,070 – 0,090 dm³ | 200 | 0,02 |
| 0,090 – 0,120 dm³ | 340 | 0,04 |
| 0,225 – 0,300 dm³ | 650 | 0,07 |
| **SECADORES DE ROPA** | | |
| por kg de ropa húmeda centrifugada | 1.000 | 0,11 |
| equipos | 2.000 – 4.000 | 0,22 – 0,43 |
| **CALDERAS INDIVIDUALES** | | |
| tipo 1 | 20.000 | **2,15** |
| tipo 2 | 30.000 | **3,23** |
| tipo 3 | 40.000 | **4,30** |
| tipo 4 | 50.000 | **5,40** |

> **Nota de la norma:** para otros artefactos, los valores se extraen de la información técnica del fabricante.
>
> **Importante:** *"Para el cálculo de la instalación deben considerarse inclusive las tomas taponadas y potenciales incrementos previstos en el proyecto."* — **Toda toma tapada suma al cálculo.**

---

## 4.4 Simultaneidad

### 4.4.1 Instalación individual (2.5.1)

Para **uso doméstico**, cuando hay más de dos artefactos:

> **Q_Si = A + B + (C + D + … + N) / 2**
>
> A y B: caudales de **los dos artefactos de mayor consumo**
> C, D, …, N: caudales del **resto** de los artefactos

Para **locales de uso NO doméstico**:
> **Q_Si = A + B + C + D + … + N**  (suma directa, sin reducción)

### 4.4.2 Instalación común de un edificio (2.5.2)

> **Q_sc = n × Q_si × S_n**
>
> n = número de unidades funcionales
> Q_si = caudal de simultaneidad de cada vivienda (m³/h)
> S_n = factor de simultaneidad

### 4.4.3 TABLA de factores de simultaneidad S₁ y S₂ (NAG-200, 2.5.2)

> **S₁ = (19 + n) / [10 × (n + 1)]** — cuando **NO** existe calefacción individual
> **S₂ = (19 + n) / [4 × (n + 4)]** — cuando **SÍ** existe calefacción individual

| N.º viviendas | S₁ | S₂ | | N.º viviendas | S₁ | S₂ |
|---|---|---|---|---|---|---|
| 1 | 1,00 | 1,00 | | 17 | 0,20 | 0,43 |
| 2 | 0,70 | 0,88 | | 18 | 0,19 | 0,42 |
| 3 | 0,55 | 0,79 | | 19 | 0,19 | 0,41 |
| 4 | 0,46 | 0,72 | | 20 | 0,19 | 0,41 |
| 5 | 0,40 | 0,67 | | 21 | 0,18 | 0,40 |
| 6 | 0,36 | 0,63 | | 22 | 0,18 | 0,39 |
| 7 | 0,33 | 0,59 | | 23 | 0,18 | 0,39 |
| 8 | 0,30 | 0,56 | | 24 | 0,17 | 0,38 |
| 9 | 0,28 | 0,54 | | 25 | 0,17 | 0,38 |
| 10 | 0,26 | 0,52 | | 26 | 0,17 | 0,38 |
| 11 | 0,25 | 0,50 | | 27 | 0,16 | 0,37 |
| 12 | 0,24 | 0,48 | | 28 | 0,16 | 0,37 |
| 13 | 0,23 | 0,47 | | 29 | 0,16 | 0,36 |
| 14 | 0,22 | 0,46 | | 30 | 0,16 | 0,36 |
| 15 | 0,21 | 0,45 | | **Más de 30** | **0,15** | **0,35** |
| 16 | 0,21 | 0,44 | | | | |

> **REGLA CRÍTICA PARA LA PAMPA — la norma la dice textualmente:**
>
> *"**En las zonas climáticas frías, se recomienda utilizar siempre el factor S₂**, a no ser que la caldera de calefacción sea colectiva."*
>
> **Santa Rosa es zona climática fría (1.394 GD18). En todo edificio de vivienda en Santa Rosa se debe usar S₂**, que es **más del doble** de S₁ para n grande (0,35 vs. 0,15). Usar S₁ en un edificio pampeano es un error de proyecto que se traduce en **prolongación y montantes subdimensionadas** y en artefactos que no llegan a la potencia nominal en el pico de invierno.

---

## 4.5 Longitud equivalente y distribución de la pérdida de carga

### 4.5.1 Longitud equivalente (4.6.5)

> Para compensar el efecto de la pérdida de carga de los accesorios, se toma como longitud del tramo la **longitud real (L_R) incrementada en un 20 %**:
>
> **L_e = 1,20 × L_R**

> **Esto simplifica enormemente el cálculo:** NAG-200 **no exige** tabular longitud equivalente accesorio por accesorio (como sí hacen otras normas). El 20 % engloba todo. **Pero para instalaciones con muchos accesorios en poco desarrollo (por ejemplo, una batería de medidores muy compacta), conviene verificar accesorio por accesorio del lado seguro.**

### 4.5.2 Longitud de cálculo (4.6.7.2)

> *"Para calcular el diámetro de los distintos tramos, la longitud de cálculo debe ser el trayecto que recorre el gas **entre el punto de suministro y el artefacto más alejado del tramo considerado**. Para los tramos troncales, la longitud de cálculo siempre se calcula entre el punto de suministro y el artefacto más alejado, es decir, **el tramo de mayor longitud incrementada en un 20 %**."*

### 4.5.3 Distribución de la pérdida de carga (4.6.6 y 4.6 f-i)

Primera asignación proporcional a la longitud:
> **ΔP_i = ΔP_Total × (L_ei / L_eTotal)**

Y luego, **método iterativo tramo a tramo** — que es la parte que se hace mal en la mayoría de los cálculos:

> **ΔP_(i+1) = [ΔP_Total − Σ ΔP_i(real)] × L_e(i+1) / [L_eTotal − Σ L_ei]**

Es decir: se asigna una pérdida al tramo 1, se calcula el diámetro teórico, se adopta el **diámetro comercial superior**, se recalcula la **pérdida real** (que es menor a la asignada, porque el caño es más grande), y **el "sobrante" de pérdida de carga se redistribuye a los tramos siguientes**.

**Procedimiento completo (4.6):**
1. Trazado, longitudes de cada tramo, elección del tramo principal (el más desfavorable).
2. Material de la cañería (4.2).
3. Caudales nominales de cada artefacto (4.6.3).
4. Longitud equivalente de cada tramo.
5. Distribución de la pérdida de carga y diámetro mínimo por tramo.
6. Diámetro teórico del primer tramo por Renouard lineal.
7. **Adoptar el diámetro nominal igual o superior**, respetando el mínimo (9,5 mm).
8. Calcular la **pérdida de carga real** con el diámetro interior adoptado.
9. Nueva pérdida de carga para el tramo siguiente (fórmula iterativa).
10. **Verificar que la presión a la entrada de cada artefacto sea ≥ 19 mbar.**
11. Repetir hasta el extremo del tramo principal.
12. Cuadro resumen con: longitud real, material, diámetro nominal, pérdida de carga real, caudal máximo, presión inicial y final, velocidad del gas.

### 4.5.4 Instalaciones telescópicas (4.6.7.3)

En instalaciones de diámetros escalonados, se aplica Renouard lineal **por tramos**, donde en cada tramo el diámetro se mantiene constante o hay un accesorio en derivación (te). Los tramos van desde la regulación/medidor al primer escalón, de ahí al segundo, y así hasta los artefactos.

> **Caída de presión = Δp₁ + Δp₂ + Δp₃ ≤ 1 mbar**

Regla general: *"el diámetro de las cañerías debe mantenerse constante en todo el tramo entre derivaciones o válvulas de corte, minimizando la cantidad de uniones"*. El diámetro de la conexión al artefacto **debe ser como mínimo el que viene preparado el artefacto**.

---

## 4.6 Fórmulas de cálculo de diámetro

### 4.6.1 Renouard lineal — BAJA PRESIÓN (≤ 100 mbar)

> **ΔP = 23.200 × δ × L_e × Q^1,82 × d^(−4,82)**
>
> De donde: **d = [ (23.200 × δ × L_e × Q^1,82) / ΔP ]^0,2075**

| Símbolo | Significado | Unidad |
|---|---|---|
| d | diámetro **interior** de la cañería | mm |
| Q | caudal | m³/h |
| δ | densidad relativa del gas (aire = 1). **GN: 0,65 / GLP: 1,52** | — |
| L_e | longitud equivalente del tramo | m |
| ΔP | pérdida de carga | mbar |

### 4.6.2 Renouard cuadrática — MEDIA Y ALTA PRESIÓN

Válida cuando **Q/d < 150** o **P > 100 mbar**. Obligatoria para cañerías que operan a **0,5 bar o superior**.

> **P_A² − P_B² = 48,6 × δ × L_e × Q^1,82 × d^(−4,82)**
>
> **d = [ (48,6 × δ × L_e × Q^1,82) / (P_A² − P_B²) ]^0,2075**
>
> **Q = [ (P_A² − P_B²) × d^4,82 / (48,6 × δ × L_e) ]^0,5495**

P_A y P_B: presiones **absolutas** al inicio y al final del tramo, en **bar A** (manométrica + 1,01325 bar).

### 4.6.3 Dimensiones de caños de acero — TABLA E.2 (NAG-250)

| Ø nominal (mm) | Pulgadas | Ø exterior (mm) | **Ø interior (mm)** | Espesor (mm) |
|---|---|---|---|---|
| 9,5 | ⅜" | 17,20 | **12,5** | 2,35 |
| 13 | ½" | 21,30 | **16,6** | 2,35 |
| 19 | ¾" | 26,90 | **22,2** | 2,35 |
| 25 | 1" | 33,70 | **27,9** | 2,90 |
| 32 | 1¼" | 42,40 | **36,6** | 2,90 |
| 38 | 1½" | 48,30 | **42,5** | 2,90 |
| 51 | 2" | 60,30 | **53,8** | 3,25 |
| 63 | 2½" | 76,10 | **69,6** | 3,25 |
| 76 | 3" | 88,90 | **81,6** | 3,65 |
| 102 | 4" | 114,30 | **106,2** | 4,05 |
| 127 | 5" | 139,70 | **130,2** | 4,75 |
| 152 | 6" | 165,10 | **155,6** | 4,75 |

---

## 4.7 TABLA E.4 (NAG-200) — Caudales de cañería de acero NAG-250 en m³/h

**Gas natural, δ = 0,65, caída de presión de 1 mbar (10 mm.c.a.), Renouard lineal.**

| L_e (m) | 9,5 (⅜") | 13 (½") | 19 (¾") | 25 (1") | 32 (1¼") | 38 (1½") | 51 (2") | 63 (2½") | 76 (3") | 102 (4") |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 4,061 | 8,604 | 18,567 | 33,993 | 69,712 | 103,530 | 193,205 | 381,886 | 581,747 | 1168,282 |
| 2 | 2,776 | 5,881 | 12,691 | 23,234 | 47,648 | 70,762 | 132,055 | 261,016 | 397,620 | 798,514 |
| 3 | 2,222 | 4,707 | 10,158 | 18,597 | 38,139 | 56,641 | 105,701 | 208,927 | 318,269 | 639,158 |
| 4 | 1,897 | 4,019 | 8,674 | 15,880 | 32,567 | 48,366 | 90,259 | 178,403 | 271,771 | 545,779 |
| 5 | 1,679 | 3,556 | 7,674 | 14,049 | 28,812 | 42,789 | 79,852 | 157,833 | 240,436 | 482,851 |
| 6 | 1,519 | 3,217 | 6,943 | 12,711 | 26,068 | 38,714 | 72,246 | 142,800 | 217,535 | 436,861 |
| 7 | 1,395 | 2,956 | 6,380 | 11,680 | 23,953 | 35,572 | 66,384 | 131,212 | 199,883 | 401,411 |
| 8 | 1,297 | 2,747 | 5,929 | 10,854 | 22,259 | 33,058 | 61,691 | 121,937 | 185,754 | 373,037 |
| 9 | 1,216 | 2,575 | 5,557 | 10,174 | 20,866 | 30,988 | 57,828 | 114,302 | 174,122 | 349,678 |
| **10** | **1,147** | **2,430** | **5,245** | **9,603** | **19,693** | **29,246** | **54,578** | **107,878** | **164,336** | **330,026** |
| 11 | 1,089 | 2,307 | 4,978 | 9,113 | 18,689 | 27,755 | 51,796 | 102,379 | 155,959 | 313,201 |
| 12 | 1,038 | 2,199 | 4,745 | 8,688 | 17,817 | 26,460 | 49,380 | 97,603 | 148,684 | 298,591 |
| 13 | 0,993 | 2,104 | 4,541 | 8,314 | 17,051 | 25,323 | 47,257 | 93,407 | 142,292 | 285,754 |
| 14 | 0,954 | 2,021 | 4,360 | 7,983 | 16,371 | 24,313 | 45,373 | 89,683 | 136,619 | 274,362 |
| **15** | **0,918** | **1,945** | **4,198** | **7,686** | **15,763** | **23,410** | **43,686** | **86,349** | **131,541** | **264,164** |
| 16 | 0,886 | 1,878 | 4,052 | 7,419 | 15,214 | 22,595 | 42,165 | 83,343 | 126,962 | 254,968 |
| 17 | 0,857 | 1,816 | 3,920 | 7,176 | 14,716 | 21,855 | 40,785 | 80,615 | 122,805 | 246,622 |
| 18 | 0,831 | 1,760 | 3,798 | 6,954 | 14,262 | 21,180 | 39,525 | 78,125 | 119,012 | 239,003 |
| 19 | 0,807 | 1,709 | 3,687 | 6,751 | 13,844 | 20,560 | 38,369 | 75,840 | 115,531 | 232,013 |
| **20** | **0,784** | **1,661** | **3,585** | **6,563** | **13,460** | **19,990** | **37,304** | **73,734** | **112,323** | **225,571** |
| 21 | 0,763 | 1,617 | 3,490 | 6,390 | 13,104 | 19,461 | 36,318 | 71,785 | 109,354 | 219,609 |
| 22 | 0,744 | 1,576 | 3,402 | 6,229 | 12,774 | 18,970 | 35,402 | 69,975 | 106,597 | 214,071 |
| 23 | 0,726 | 1,538 | 3,320 | 6,079 | 12,466 | 18,513 | 34,549 | 68,288 | 104,027 | 208,910 |
| 24 | 0,709 | 1,503 | 3,244 | 5,938 | 12,178 | 18,086 | 33,751 | 66,711 | 101,624 | 204,085 |
| **25** | **0,694** | **1,470** | **3,172** | **5,807** | **11,908** | **17,685** | **33,003** | **65,233** | **99,372** | **199,562** |
| 26 | 0,679 | 1,438 | 3,104 | 5,683 | 11,654 | 17,308 | 32,300 | 63,843 | 97,255 | 195,311 |
| 27 | 0,665 | 1,409 | 3,040 | 5,566 | 11,415 | 16,953 | 31,637 | 62,534 | 95,261 | 191,306 |
| 28 | 0,652 | 1,381 | 2,980 | 5,456 | 11,190 | 16,618 | 31,012 | 61,298 | 93,378 | 187,525 |
| 29 | 0,639 | 1,355 | 2,923 | 5,352 | 10,976 | 16,301 | 30,420 | 60,128 | 91,596 | 183,946 |
| **30** | **0,628** | **1,330** | **2,870** | **5,253** | **10,774** | **16,000** | **29,859** | **59,019** | **89,907** | **180,554** |
| 32 | 0,606 | 1,283 | 2,770 | 5,071 | 10,399 | 15,443 | 28,820 | 56,965 | 86,777 | 174,269 |
| **35** | **0,577** | **1,222** | **2,637** | **4,827** | **9,900** | **14,702** | **27,436** | **54,230** | **82,612** | **165,903** |
| 38 | 0,551 | 1,168 | 2,520 | 4,614 | 9,463 | 14,053 | 26,225 | 51,836 | 78,965 | 158,579 |
| **40** | **0,536** | **1,135** | **2,450** | **4,486** | **9,200** | **13,663** | **25,497** | **50,397** | **76,772** | **154,176** |
| 42 | 0,522 | 1,105 | 2,386 | 4,367 | 8,957 | 13,302 | 24,823 | 49,065 | 74,743 | 150,101 |
| **45** | **0,502** | **1,064** | **2,297** | **4,205** | **8,624** | **12,807** | **23,900** | **47,241** | **71,965** | **144,522** |
| 48 | 0,485 | 1,027 | 2,217 | 4,059 | 8,324 | 12,361 | 23,068 | 45,597 | 69,460 | 139,491 |
| **50** | **0,474** | **1,004** | **2,168** | **3,969** | **8,139** | **12,087** | **22,557** | **44,586** | **67,920** | **136,400** |
| 52 | 0,464 | 0,983 | 2,122 | 3,884 | 7,966 | 11,830 | 22,077 | 43,636 | 66,473 | 133,494 |

> **Cómo usar la tabla:** entrar con la **longitud equivalente** del tramo y buscar la primera columna cuyo caudal sea **≥ al caudal de cálculo del tramo**. Ese es el diámetro nominal a adoptar.
>
> **Para longitudes intermedias:** interpolar linealmente, del lado seguro (tomar la longitud mayor).
>
> **La tabla está calculada para ΔP = 1 mbar en TODO el tramo.** Si al tramo se le asignó menos de 1 mbar (porque hay varios tramos en serie), hay que corregir. Corrección práctica: **Q_corregido = Q_tabla × (ΔP_asignado / 1 mbar)^0,55**.

---

## 4.8 EJEMPLO RESUELTO Nº 3 — Caudal de gas y diámetros de un edificio PB+9

### Datos

Mismo edificio del Ejemplo Nº 1: **PB+9, 40 departamentos**, Santa Rosa (La Pampa).

**Equipamiento previsto por departamento (tipo 2 dormitorios, el más numeroso):**

| Artefacto | Cm (kcal/h) | Q (m³/h) |
|---|---|---|
| Cocina: 4 hornallas (2 grandes de 2.000, 2 medianas de 1.400) + horno de 4.000 | 10.800 | **1,16** |
| Calefón de 14 l/min | 22.400 | **2,41** |
| Caldera individual mural para calefacción (radiadores) | 30.000 | **3,23** |

> **Nota:** en Santa Rosa, con 1.394 GD18, **la calefacción a gas es prácticamente obligatoria** en cualquier tipología. Se adopta caldera individual dual (calefacción + ACS). En ese caso el calefón desaparecería; **pero para el ejemplo mantenemos las tres cargas** como caso conservador (calefón + caldera solo calefacción), que es como muchos comitentes lo piden.

### Paso 1 — Simultaneidad individual (2.5.1)

Los dos artefactos de mayor consumo: caldera (3,23) y calefón (2,41). Resto: cocina (1,16).

> **Q_si = 3,23 + 2,41 + (1,16)/2 = 3,23 + 2,41 + 0,58 = 6,22 m³/h**

> **Verificación del mínimo de proyecto (4.6.2):** 21,63 kW = 18.600 kcal/h → 18.600/9.300 = **2,00 m³/h**. Nuestro Q_si = 6,22 m³/h > 2,00 ✓

### Paso 2 — Simultaneidad de la instalación común (2.5.2)

n = 40 viviendas. **Hay calefacción individual (caldera por unidad) → se usa S₂.** Y además, la norma recomienda **usar siempre S₂ en zonas climáticas frías**, lo que refuerza la elección.

Para n = 40 (> 30): **S₂ = 0,35**

Verificación por fórmula: S₂ = (19 + 40)/[4 × (40 + 4)] = 59/176 = 0,335 → la tabla redondea a 0,35 para n > 30. **Adoptamos S₂ = 0,35** (más conservador).

> **Q_sc = n × Q_si × S₂ = 40 × 6,22 × 0,35 = 87,08 m³/h**

**Comparación con S₁ (el error a evitar):**
> Q_sc(S₁) = 40 × 6,22 × 0,15 = **37,32 m³/h**
>
> **La diferencia es de 2,33 veces.** Usar S₁ en Santa Rosa habría llevado a una prolongación de 2½" en lugar de 4". Este es el error de proyecto de gas más caro de corregir.

### Paso 3 — Servicios generales

Agregar: caldera de sala de máquinas si existiera, secarropas comunes, etc. **En este caso, no hay.** Si hubiera calefacción central, **NO se usaría S₂ sino S₁** (la norma lo aclara: "a no ser que la caldera de calefacción sea colectiva").

**Q total del edificio = 87,08 m³/h → adoptar Q = 88 m³/h**

### Paso 4 — Dimensionado de la prolongación (media presión)

La prolongación interna desde el gabinete de regulación hasta el compartimento de baterías de medidores. Suponemos:
- **Media presión, P mínima garantizada = 0,5 bar** (manométrica) → P_A = 1,51325 bar A
- Longitud real: **25 m** (recorrido desde línea municipal, por espacio común, hasta el compartimento de medidores en PB)
- **L_e = 1,20 × 25 = 30 m**
- Pérdida de carga admisible: **10 % de la presión de entrada = 0,05 bar** → P_B = 0,45 bar manométrica = 1,46325 bar A

> **P_A² − P_B² = 1,51325² − 1,46325² = 2,28993 − 2,14110 = 0,14883**

> **d = [ (48,6 × 0,65 × 30 × 88^1,82) / 0,14883 ]^0,2075**

Cálculo de 88^1,82: ln(88) = 4,4773; × 1,82 = 8,1487; e^8,1487 = **3.463,4**

> Numerador = 48,6 × 0,65 × 30 × 3.463,4 = 947,7 × 3.463,4 = **3.282.309**
> 3.282.309 / 0,14883 = **22.054.216**
> d = 22.054.216^0,2075: ln(22.054.216) = 16,909; × 0,2075 = 3,5086; e^3,5086 = **33,4 mm**

**Diámetro interior necesario: 33,4 mm.** De la Tabla E.2, el primer diámetro con interior ≥ 33,4 mm es el de **38 mm nominal (1½"), con interior 42,5 mm**. (El de 32 mm nominal tiene interior 36,6 mm, que también supera 33,4 mm → **adoptar Ø 32 mm (1¼"), interior 36,6 mm**.)

**Verificación de velocidad:**
> Pa al final del tramo = 0,45 + 1,01325 = 1,46325 bar A
> V = 358,36 × 88 / (36,6² × 1,46325) = 31.535,7 / (1.339,6 × 1,46325) = 31.535,7 / 1.960,1 = **16,09 m/s**
>
> Límite para media presión: **≤ 20 m/s** ✓ **VERIFICA**

**Prolongación adoptada: Ø 32 mm (1¼") de acero NAG-250**, con verificación de velocidad de 16,09 m/s.

> **Recomendación de proyecto:** adoptar **Ø 38 mm (1½")** por seguridad. La velocidad baja a 358,36×88/(42,5²×1,46325) = 31.535,7/2.643,0 = **11,93 m/s**, y queda margen para futuras ampliaciones. El sobrecosto de un rango de diámetro en 25 m de cañería es marginal frente al costo de rehacerla.

### Paso 5 — Montante de gas (baja presión, después de los medidores)

Cada departamento tiene su medidor individual en el compartimento de PB, y de allí sale una **cañería interna individual** hasta la unidad. Esta cañería opera en **baja presión (19 mbar)** con **ΔP máximo de 1 mbar**.

**Tramo más desfavorable: departamento del 9.º piso.**
- Recorrido: 3 m horizontales en PB + 26,1 m verticales + 8 m dentro de la unidad hasta el artefacto más alejado = **37,1 m**
- **L_e = 1,20 × 37,1 = 44,5 m**
- Caudal: Q_si de la unidad = **6,22 m³/h**

**De la Tabla E.4**, para L_e = 45 m (interpolando del lado seguro):

| Ø nominal | Caudal a 45 m (m³/h) | ¿≥ 6,22? |
|---|---|---|
| 13 mm (½") | 1,064 | ❌ |
| 19 mm (¾") | 2,297 | ❌ |
| **25 mm (1")** | **4,205** | ❌ |
| **32 mm (1¼")** | **8,624** | ✅ |

**Cañería interna individual adoptada: Ø 32 mm (1¼") en el tramo completo**, o **telescópica**:
- Tramo 1 (medidor → entrada de la unidad, 29 m reales, L_e = 34,8 m, Q = 6,22 m³/h): de la tabla a 35 m, Ø 32 mm da 9,900 ✅. **Ø 32 mm.**
- Tramo 2 (dentro de la unidad, hasta la derivación de la caldera; Q = 6,22 − 1,16/2... ): se recalcula por tramo aplicando el método iterativo de 4.6.

**Verificación de velocidad en baja presión:**
> Pa = 0,019 + 1,01325 = 1,03225 bar A
> V = 358,36 × 6,22 / (36,6² × 1,03225) = 2.229,0 / (1.339,6 × 1,03225) = 2.229,0 / 1.382,8 = **1,61 m/s**
>
> Límite baja presión: **≤ 7 m/s** ✓ **VERIFICA holgadamente**

> **Observación importante:** en baja presión, **la velocidad casi nunca es la restricción; lo es la pérdida de carga de 1 mbar.** En media presión ocurre lo contrario.

### Paso 6 — Verificación de la caída de presión real (método iterativo)

Con Ø 32 mm (interior 36,6 mm), L_e = 44,5 m, Q = 6,22 m³/h:

> ΔP = 23.200 × 0,65 × 44,5 × 6,22^1,82 × 36,6^(−4,82)

6,22^1,82: ln(6,22) = 1,8278; × 1,82 = 3,3266; e^3,3266 = **27,85**
36,6^4,82: ln(36,6) = 3,6002; × 4,82 = 17,353; e^17,353 = **3,44 × 10⁷**

> ΔP = 23.200 × 0,65 × 44,5 × 27,85 / (3,44 × 10⁷)
> = 671.060 × 27,85 / 3,44 × 10⁷ = 18.689.021 / 3,44 × 10⁷ = **0,543 mbar**

**0,543 mbar < 1,0 mbar ✓ VERIFICA con 46 % de margen.**

**Presión en la válvula de corte del artefacto:** 19 − 0,543 = **18,46 mbar**.

> ⚠ **NO VERIFICA el requisito de 4.6 j): "La presión mínima en la válvula de corte de cada artefacto no debe ser inferior a 19 mbar."**
>
> **Interpretación:** el requisito se cumple si la presión de salida del regulador/medidor está **por encima de 19 mbar** de modo que, descontada la pérdida de carga de 1 mbar, en el artefacto haya al menos 19 mbar. En la práctica, la prestadora garantiza **20 mbar (o 21 mbar) a la salida del medidor** para baja presión, precisamente para que quede 19 mbar en el artefacto después de perder 1 mbar. `[VERIFICAR la presión de salida garantizada por Camuzzi Gas Pampeana en el medidor domiciliario]`
>
> **Este es un punto que el instalador matriculado debe resolver con la prestadora. No lo resuelve el arquitecto.**

### Resumen del Ejemplo Nº 3

| Concepto | Valor |
|---|---|
| Q_si por departamento (cocina + calefón + caldera) | **6,22 m³/h** |
| n | 40 viviendas |
| **Factor de simultaneidad (zona fría, calefacción individual)** | **S₂ = 0,35** |
| **Q_sc del edificio** | **87,08 → 88 m³/h** |
| Prolongación en media presión (0,5 bar), L_e = 30 m | **Ø 32 mm (1¼") calculado; se recomienda Ø 38 mm (1½")** |
| Velocidad en la prolongación | 16,09 m/s (< 20 ✓) |
| Cañería interna individual, L_e = 44,5 m, Q = 6,22 m³/h | **Ø 32 mm (1¼")** |
| ΔP real de la cañería interna | **0,543 mbar (< 1 mbar ✓)** |
| Velocidad en baja presión | 1,61 m/s (< 7 ✓) |

---

## 4.9 Gabinetes y compartimentos de medidores

### 4.9.1 Condiciones generales de ubicación (NAG-200, 3.2.1)

| Condición |
|---|
| Acceso libre y permanente para el personal de la Prestadora, por espacios de circulación de uso común. **No debe interponerse en una vía de emergencia** |
| Todo gabinete de reguladores dentro del edificio debe emplazarse **inmediatamente a continuación de los obstáculos estructurales a sortear y lo más cerca posible de la válvula de corte de línea municipal** |
| **Para gas de densidad superior a 1 (GLP): solo en planta baja**, con cota ≥ 0,10 m sobre el nivel de vereda (o ≥ 0,30 m sobre el terreno si la vereda no está definida) |
| En propiedad horizontal (Ley 13.512), acceso **desde espacio de uso común**, quedando **excluidos los pasos de circulación de escaleras o salidas de emergencia** |
| **Espacio frente a la puerta:** separación mínima de **1,00 m** de cualquier obstáculo, altura mínima **2,50 m**, ventilación permanente y apertura total de la/s puerta/s |
| **Base ≥ 0,10 m sobre el piso terminado; cara superior a cota máxima de 1,90 m** respecto de esa referencia |
| **Alejamiento de instalaciones eléctricas con riesgo de chispa** (tableros, llaves de medidor): **0,50 m mínimo**. Se reduce a **0,30 m** si el gabinete tiene ventilación al exterior o está en espacio abierto |
| No debe existir riesgo de filtración de agua |
| **No estar en ambiente cerrado con fuegos abiertos** |
| **Alejado ≥ 1,00 m** de toda toma de aire forzado y de todo sombrerete de conducto de evacuación de gases de combustión |
| **Alejado ≥ 0,50 m** de cualquier abertura de ventilación |
| **PROHIBIDO instalarlos:** (a) debajo o delante de ventanas u otras aberturas que puedan usarse como salida de emergencia, o debajo de escaleras interiores o exteriores; (b) en sótano de pequeña altura con espacio reducido; (c) cerca de entradas de aire del edificio |

### 4.9.2 Construcción (3.2.2)

| Requisito |
|---|
| **Ignífugo**, ejecutado con placas cementicias, chapas, mampostería o cavidad construida sobre un muro |
| Rígidamente amurado, con cimientos sobre terreno estable y nivelado |
| Piso con **pendiente hacia el frente** para escurrimiento de agua |
| **Estanco** cuando esté empotrado en muros de viviendas (salvo el conjunto puerta-marco). Traspaso de cañerías sellado |
| Dimensiones que garanticen acceso libre a todo componente **sin remover otro**, con herramientas comunes |
| Conjunto puerta-marco según **NAG-237** |
| **Medidor ≤ 10 m³/h: dimensiones interiores mínimas 0,45 m (alto) × 0,35 m (ancho) × 0,25 m (profundidad)** |
| **Medidor > 10 m³/h: dimensiones indicadas por la Prestadora** según el sistema a contener |
| Aberturas o conductos de ventilación comunicados con el exterior |
| Orificio en el piso, en el punto de ingreso de la cañería de servicio, para la vaina de protección |
| Si no hay conjunto aprobado de la medida: chapa de acero **≥ 1,27 mm (galga 18)**, pestaña doblada hacia adentro de 30 mm soldada en las 4 esquinas, refuerzos de perfil T de ≥ 15 mm soldados en cruz, marco de hierro ángulo de ala ≥ 19 mm, mínimo 2 bisagras desmontables, protección anticorrosiva interior y exterior, palabra **"GAS"** inalterable, llave de cuadro de 6,35 mm centrada en orificio de 25 mm |

### 4.9.3 Ventilación de gabinetes (3.3.1)

**Medidores individuales de hasta 10 m³/h:**

| Situación | Ventilación exigida |
|---|---|
| **Espacio abierto y aireado naturalmente** (GN o GLP) | Puertas con **aberturas superior e inferior de ≥ 10 cm² cada una** (NAG-237) |
| **GN, medidor en espacio cerrado** | Gabinete ventilado al exterior por **conducto de sección ≥ 30 cm²**, conectado herméticamente a una abertura de igual dimensión en la parte superior del recinto. La puerta lleva **únicamente abertura inferior de ≥ 30 cm²** |
| **GLP, en espacio cerrado** | El recinto debe ser **estanco respecto al ambiente** y ventilado al exterior por conductos conectados a la parte superior e inferior del gabinete |
| Gabinetes con paredes libres que rematen directamente al exterior | Pueden ventilarse sobre cualquiera de ellas, en reemplazo de las aberturas en puertas |
| **Medidores individuales > 10 m³/h** | Puerta con **abertura superior y otra inferior de 150 cm² cada una**, con conducto cuando corresponda |

### 4.9.4 Compartimento para baterías de medidores hasta 10 m³/h (3.3.2)

| Requisito |
|---|
| **Acceso desde la entrada del edificio a través de circulaciones comunes** |
| Si comunica directamente con locales donde funcionan **calderas, hornos, motores, instalaciones eléctricas no blindadas, motores de combustión interna estacionarios**, o hay almacenamiento de combustibles, productos corrosivos o generación de fuego/chispas: **debe interponerse una ANTECÁMARA de superficie mínima 1 m²**, con puerta de material incombustible y **ventilación en la parte inferior de sección igual a la de la puerta del compartimento de medidores** |

> **Consecuencia de proyecto para un PB+9:** el compartimento de medidores de gas de 40 unidades es un local de dimensiones significativas (típicamente 2,5 a 4 m² según la disposición de la batería), con acceso desde el hall de entrada, ventilación al exterior y separación de tableros eléctricos. **Hay que ubicarlo en el anteproyecto, no descubrirlo en el ejecutivo.** Y si queda contiguo a la sala de bombas o al tablero general, **hace falta antecámara de 1 m²**.
>
> **Iluminación:** para recintos con instalación APE que requieran iluminación artificial, aplica NAG-200 3.5. `[verificar requisitos de instalación eléctrica antiexplosiva en el compartimento]`

---

## 4.10 Ventilación de ambientes con artefactos a gas

Este es el apartado que más incide en el proyecto de arquitectura, porque **obliga a rejillas en fachadas y a dimensiones mínimas de local**.

### 4.10.1 Dimensionado de las aberturas (6.4.1)

> La superficie libre de ventilación se calcula en función de la **suma del consumo nominal o potencia total de los artefactos a gas de cámara abierta instalados en el ambiente**.
>
> **Superficie mínima: 4 cm² por kW (4 cm² por cada 860 kcal/h), con un MÍNIMO DE 100 cm².**

Esto vale tanto para ventilación **directa** como **indirecta**.

**Tabla práctica derivada:**

| Potencia instalada de cámara abierta | kcal/h | Superficie libre de rejilla |
|---|---|---|
| Hasta 21,5 kW | hasta 18.500 | **100 cm²** (el mínimo manda) |
| 25 kW | 21.500 | 100 cm² |
| 30 kW | 25.800 | 120 cm² |
| 40 kW | 34.400 | 160 cm² |
| 50 kW | 43.000 | 200 cm² |
| 60 kW | 51.600 | 240 cm² |
| 80 kW | 68.800 | 320 cm² |
| 100 kW | 86.000 | 400 cm² |

> **Ojo:** es **superficie LIBRE de pasaje**, no la superficie exterior de la rejilla. Una rejilla comercial tiene entre 50 % y 70 % de área libre. **Una rejilla de 20 × 20 cm con 60 % de área libre da 240 cm² de área libre.** Especificar siempre el área libre, no la medida exterior.

### 4.10.2 Ubicación de las aberturas (6.4.2 y 6.4.3)

Para artefactos **Tipo A** (sin conducto propio: cocinas, anafes, calefactores infrarrojos), es **obligatoria la ejecución de DOS aberturas**:

| Abertura | Ubicación |
|---|---|
| **INFERIOR** (ingreso de aire para la combustión) | **Entre 0,30 m y 0,50 m del nivel de piso** |
| **SUPERIOR** (salida de aire viciado) | **A no menos de 1,80 m del nivel de piso.** De ser posible, en la parte más elevada del ambiente |

> **NOTA de la norma:** ambos orificios **no necesariamente deben ser iguales**. Ejemplo: en una cocina con cocina y calefón, el orificio de aporte sirve a ambos artefactos, mientras el de salida solo a la cocina.

**Emplazamiento general de las tomas de aire (6.4.4):** *"El emplazamiento de las aberturas no debe superar 0,50 m por encima del nivel de piso y solamente ante obstáculos ineludibles se admite instalarlas a otra altura dentro del tercio inferior del ambiente."*

### 4.10.3 Reglas constructivas de las aberturas (6.4)

| Regla |
|---|
| Toda abertura de ventilación debe llevar en sus extremos **rejillas fijas aprobadas según NAG-215** |
| Deben ubicarse de manera que **no puedan ser obstruidas por muebles, objetos, puertas, etc.** |
| **No se admiten aberturas cuyo interior posea ramificaciones o huecos** que permitan la migración de productos de la combustión por el interior del muro o tabique |
| Si la abertura está en un muro, el canal de pasaje debe estar **revocado o materializado con un conducto** que asegure hermeticidad en los extremos con las rejillas, con superficie lisa, **sin obstrucciones ni reducción de sección** |
| **NO son válidas las aberturas sobre muros medianeros** |
| **Ambientes internos sin pared al exterior:** pueden abastecerse desde ambientes contiguos por aberturas compatibles con la potencia. **NO son ambientes contiguos válidos: dormitorios, baños, cocinas y garajes**, ni recintos con artefactos de cámara abierta o con productos tóxicos/combustibles |
| **Rejilla en taparrollos:** rejilla interna en el frente del taparrollo y rejilla externa en la parte exterior del muro, **con superficie 1,5 veces superior a la mínima requerida** |
| **Rejilla en superficies vidriadas:** permitida siempre que esté contenida en un **marco independiente** |
| **Campana directa al exterior con ventilación mecánica:** se puede prescindir de las aberturas superiores pasivas si **hay enclavamiento que corte el gas ante corte de energía o falla del sistema**, o si la sección de pasaje de la campana supera la de 6.4.1 |
| Otras aberturas permanentes (rejillas, campanas sin filtro, claraboyas, extractores con persiana fija) **pueden considerarse aceptables** si su ubicación y área libre igualan o superan lo de 6.4.1, y están indicadas en el plano de gas |

### 4.10.4 Ventilación indirecta a través de ambiente contiguo (6.4.4)

- La ventilación indirecta puede ser **como máximo a través de UN ambiente contiguo** al que tiene el artefacto, y ese ambiente **debe lindar con el exterior**.
- Debe tener como mínimo las dimensiones exigidas a la entrada de aire directa según la potencia instalada.
- **Toma de aire por conducto horizontal:** pendiente **ascendente del 4 % hacia el interior**, longitud **no mayor de 3 m**, emplazado a **no más de 0,50 m del nivel de piso interior**.

### 4.10.5 Recintos bajo nivel de terreno (6.4.5)

| Situación | Requisito |
|---|---|
| **Primer subsuelo** | Ventilación natural o mecánica, mediante **dos conductos ejecutados a desnivel**, con la mayor diferencia de altura posible y, de ser posible, en **lados opuestos** del edificio. El conducto de aporte, preferentemente del lado de los vientos predominantes |
| **Por debajo del primer subsuelo** | **Obligatoriamente ventilación MECÁNICA** |
| Toda ventilación mecánica | **Debe disponer de enclavamientos que bloqueen el suministro de gas ante fallas del sistema de ventilación** |

### 4.10.6 Espacio aire-luz (6.4.6)

> En edificios de **tres o más plantas**, el espacio de aire-luz **no puede utilizarse para la evacuación de gases de combustión cuando su superficie transversal sea menor que 4,0 m²**.
>
> Cuando esté **entre 4 m² y 9 m²**, debe contar con **aporte de aire en su parte inferior** desde el exterior del edificio, mediante conducto horizontal de **sección transversal mínima de 300 cm²**.
>
> *(Estas restricciones no aplican a la ventilación de ambientes, solo a la evacuación de gases.)*

> **Consecuencia directa para un PB+9:** si el partido arquitectónico usa un patio de aire y luz de menos de 4 m² para descargar los tiros de calefones o calderas de cámara abierta, **es inviable**. Hay que: (a) agrandar el patio a ≥ 4 m² (y con 4-9 m² poner el conducto de aporte de 300 cm²), o (b) usar artefactos de **cámara estanca** con salida a fachada, o (c) proyectar **conducto colectivo** (§4.12.4).

### 4.10.7 Espacio semicubierto / galería (6.4.7)

Se admite descargar productos de combustión si la relación entre **superficie de pared libre** y **superficie total techada (cubierta en planta)** es:

| Relación pared libre / superficie techada | Condición |
|---|---|
| **≥ 1,5** | **Sin restricción** |
| **> 1 y < 1,5** | Artefactos cuya suma de potencia **no supere 34,89 kW (30.000 kcal/h)** |
| **Entre 0,6 y 1** | Se puede ventilar siempre que el conducto de evacuación esté a **no más de 1,0 m del extremo libre** y la potencia **no supere 23,26 kW (20.000 kcal/h)** |
| **< 0,6** | **NO ES APTO para ventilar** |

- **Nota 1:** si la superficie libre no alcanza al cielorraso, debe instalarse rejilla de ventilación **≥ 50 % de la superficie de 6.4.1**.
- **Nota 2:** estos espacios también pueden usarse para aporte de aire (rejilla inferior) y ventilación de ambientes (rejilla superior).

### 4.10.8 Secarropas en lavanderías comerciales (6.4.4)

> Aberturas de **≥ 25 cm² por cada 1,16 kW (1.000 kcal/h)** de potencia instalada, con **abertura mínima de 100 cm²**.

---

## 4.11 Ambientes: prohibiciones expresas (NAG-200, 5.9)

### 4.11.1 Requisitos generales (5.9.1)

| Regla |
|---|
| **En pasos comunicados con dormitorios y baños**, la potencia térmica efectiva no debe superar **0,058 kW (50 kcal/h) por m³ de ambiente**. **En zonas frías se puede incrementar en 0,0029 kW (2,5 kcal/h) por m³ por cada °C bajo cero de temperatura media invernal.** Se considera el volumen del paso más el de los dormitorios. **No aplica a artefactos de cámara estanca** |
| **No se permiten calefactores de rayos infrarrojos en ambientes de volumen ≤ 30 m³** (salvo uso industrial determinado) |

> **Aplicación a Santa Rosa:** la temperatura media de invierno de Santa Rosa (Aero) es **9,77 °C** según IRAM 11603 — **no está bajo cero**, por lo que el incremento de 2,5 kcal/h·m³ por °C bajo cero **no aplica** con la temperatura media. `[verificar la interpretación de "temperatura media invernal" que aplica la prestadora: algunos criterios usan la temperatura mínima media del mes más frío, que en Santa Rosa es 3,5 °C — tampoco bajo cero]`

### 4.11.2 Cuadro de prohibiciones por ambiente (5.9.2)

| Ambiente | Qué se puede instalar |
|---|---|
| **DORMITORIOS** | **ÚNICAMENTE calefactores de cámara estanca (Tipo C).** Prohibido todo otro artefacto a gas |
| **BAÑOS Y ANTEBAÑOS** | **ÚNICAMENTE artefactos de cámara estanca (Tipo C)** |
| **PASOS A DORMITORIOS** | Calefacción de **cámara estanca (Tipo C)** o de **cámara abierta con salida directa al exterior y remate a los cuatro vientos (Tipo B)**. El calentador en paso debe estar instalado **antes del pedido de inspección**. Su potencia debe cumplir 5.9.1.1 |
| **COCINAS** | **Volumen < 7 m³: NO se pueden instalar calentadores de agua de cámara abierta** (calefón, termotanque o caldera). **Calderas de cámara abierta: máximo 1,16 kW (1.000 kcal/h) por m³** de ambiente (una caldera de 23,25 kW / 20.000 kcal/h requiere ≥ 20 m³) |
| **MONOAMBIENTES** | Ver 4.11.3 |
| **RECINTOS CON VAPORES O GASES COMBUSTIBLES** | Únicamente cámara estanca. Si se requiere llama abierta: sensores de ambiente y enclavamientos |
| **SUBSUELOS** | **PROHIBIDA la instalación de artefactos para funcionar con GLP** (5.8.10) |

> **REGLA IMPORTANTE sobre puertas (5.9.2.1):** *"La ausencia de puerta NO modifica el carácter o destino de un ambiente. Debe entenderse por ausencia de puerta al hueco, con o sin marco, cuyo ancho **no debe ser superior a 1 m**. Toda dimensión mayor de ese hueco o abertura califica al dormitorio como **ambiente integrado o monoambiente**."*
>
> **Traducción para el arquitecto:** si diseñás un dormitorio con un vano de 1,20 m sin puerta que da al estar, **la norma lo trata como monoambiente**, y entonces se aplican las reglas de monoambiente a **todo el conjunto**, incluyendo la cocina. Este es un caso real y frecuente en departamentos de un ambiente y en lofts.
>
> **Regla adicional:** las habilitaciones en "ambientes con prohibición expresa" deben efectuarse **con los artefactos instalados y conectados a la cañería interna, sin excepción**.

### 4.11.3 Monoambientes (5.9.2.5) — reglas detalladas

**Condiciones generales:**

| Regla |
|---|
| a) **Únicamente calefactores de cámara estanca (Tipo C)** |
| b) **Calentadores de agua de cámara estanca (calderas y calefones) no deben superar 0,682 kW (600 kcal/h) por m³** de volumen del ambiente |
| c) **PROHIBIDA la conexión de artefactos a conducto único de ventilación** |
| d) Cuando el único artefacto de cámara abierta sea la cocina/anafe: **campana orientadora de gases para ventilación superior, SIN filtros ni elementos que obstruyan el tiro natural**, instalada sobre la cocina y **rematando al exterior por conducto de sección mínima 100 cm²** |
| e) Si el conducto se desplaza horizontalmente: **pendiente mínima positiva 4 %**, desarrollo horizontal máximo **1,5 m**, y **tramo vertical de al menos el doble de la longitud del horizontal**, manteniendo el diámetro |

**Condiciones particulares por volumen:**

| Volumen del monoambiente | Qué se admite |
|---|---|
| **< 30 m³** | **Solo artefactos de cámara estanca**, y solo cocina/anafe con o sin horno **hasta 10,5 kW (9.000 kcal/h)**. **Abertura de ventilación inferior mínima de 100 cm² de pasaje libre y otra superior de igual sección** |
| **> 30 m³** | Se puede instalar **calentador de agua de cámara abierta de potencia máxima 10,5 kW (9.000 kcal/h)**, evacuando por conducto rematado a los cuatro vientos. **Ventilación inferior mínima de 150 cm² de área libre.** La potencia acumulada de artefactos de cocción (cocinas, hornos sin conducto, anafes) **no puede superar 12,8 kW (11.000 kcal/h)** |
| **Tipo LOFT, planta única sin entrepisos ni balcones internos, > 200 m³** | Se pueden instalar artefactos de **cámara abierta con salida de gases al exterior**, si se reúnen las condiciones de ventilación conforme a la potencia y las aberturas ventilan directamente al exterior. **En todos los casos el conducto debe ventilar a los cuatro vientos, independientemente de la potencia instalada** |

**Viviendas integradas / loft (5.9.2.7):**
> *"La ausencia de paredes o tabiques divisorios entre ambientes virtuales o entre diferentes niveles o plantas convierte la vivienda, desde el punto de vista de esta reglamentación, en **vivienda integrada o monoambiente**. En este caso, es obligatoria la instalación de artefactos indicados para monoambientes."*

> **Impacto de diseño enorme.** Un dúplex con doble altura sobre el estar, o una planta libre con cocina integrada y escalera abierta, **puede quedar clasificado como monoambiente** y perder la posibilidad de instalar calefón o termotanque de cámara abierta. **Esto se decide en el anteproyecto.**

### 4.11.4 Advertencia obligatoria en cocinas con conducto colectivo (5.9.2.4)

Cuando se instalen calentadores de agua conectados a conducto colectivo de ventilación, el artefacto debe llevar en su frente **chapa inalterable firmemente fijada** con la inscripción:

> **"Advertencia: No deben instalarse en este ambiente campanas ni extractores comunicados con el exterior por constituirse en causantes de graves riesgos de seguridad para sus ocupantes"**

> **Motivo físico:** un extractor de cocina en depresión invierte el tiro del conducto colectivo y trae los productos de combustión (con CO) de los pisos vecinos al interior de la cocina. **Es uno de los mecanismos más frecuentes de intoxicación por monóxido en edificios argentinos.**

### 4.11.5 Reglas de instalación de artefactos (5.8)

| Regla |
|---|
| Artefactos en medio combustible (pisos, paredes, muebles, techos, alfombras): cumplir el manual del fabricante. **Si no hay indicación: interponer material termoaislante e incombustible** |
| Artefactos en gabinete: se admiten los de **cámara estanca o abierta con conducto**, si no tienen contraindicaciones. Preverse aislación térmica adicional. **El gabinete debe llevar rejillas de ventilación conforme a 6.4** |
| Artefactos en ambientes con **sustancias químicas** que generen productos corrosivos/inflamables o alteren la combustión: **deben ser de cámara estanca** |
| **Equipos en techos:** sobre superficie bien drenada, construcción apta para las condiciones climáticas; si no, en gabinetes apropiados. **Si no hay acceso permanente: además de la válvula de corte del artefacto, una segunda válvula de seguridad identificada en lugar de fácil acceso.** Las válvulas de corte deben quedar afuera, a la vista y accesibles — **la falta de puerta no justifica ubicar la válvula adentro** |
| **Termotanques con salida horizontal de conducto:** se ubican **exclusivamente sobre la pared a traspasar con el conducto** (6.5.3) |
| **Conductos aéreos a la vista (TBU o TN):** protección mecánica adicional hasta al menos **2 m de altura** desde el piso. Los conductos aéreos en **dormitorios, baños, loft, monoambientes y pasos comunicados con dormitorios y/o baños** deben ir **incorporados en falsa columna o mocheta de terminación estanca respecto al ambiente** (6.3.5) |
| **Los conductos deben mantener en todo su recorrido la forma y sección del collarín de conexión del artefacto** (6.3.6) |
| **Tramos de conducto de más de 0,50 m a la intemperie**, de artefactos de tiro natural en ambientes habitables: **deben tener aislación térmica** (doble pared sellada, aislación no higroscópica o con revestimiento, resistente a las condiciones ambientales locales) (6.3.7) |

> **Esto último es crítico en Santa Rosa.** Un conducto de tiro natural sin aislar, en una noche de invierno con −6 °C, condensa los productos de combustión dentro del caño, se corroe y pierde tiro. **La aislación del conducto no es un extra: es un requisito normativo.**

---

## 4.12 Evacuación de productos de la combustión

### 4.12.1 Clasificación de artefactos (5.3.1 y 6.2)

| Tipo | Descripción | Evacuación |
|---|---|---|
| **Tipo A** | No conectados a conducto (cocinas, anafes, calefactores infrarrojos) | Al ambiente; requiere ventilación superior e inferior (§4.10.2) |
| **Tipo B** | **Cámara abierta**: toman el aire de combustión del ambiente y evacuan por conducto | Conducto individual o colectivo, tiro natural o mecánico |
| **Tipo C** | **Cámara estanca**: toman el aire del exterior y evacuan al exterior, sin contacto con el ambiente | Conducto horizontal (tiro balanceado, TB) o en "U" vertical (TBU) |

### 4.12.2 Materiales del conducto individual de tiro natural (6.5)

| Requisito |
|---|
| Material mecánicamente resistente (chapa de acero galvanizada, aluminio, acero inoxidable), duradero e incombustible, **apto para soportar temperaturas superiores a 200 °C** |
| **Estancos**, resistentes a oxidación y corrosión, paredes internas lisas |
| **PROHIBIDA la utilización de conductos de chapa de aluminio corrugada, de PVC, polietileno o policarbonato** |
| Conectores entre artefacto y conducto: chapa galvanizada, aluminio, acero inoxidable, u otro material que forme parte de la aprobación del artefacto |

> **El "flexible de aluminio corrugado" que se ve en tantas obras está expresamente prohibido.** Genera pérdida de carga, acumula hollín y se perfora.

### 4.12.3 Tiro natural vs. tiro balanceado — comparativa de proyecto

| | **Tiro natural (Tipo B)** | **Tiro balanceado / cámara estanca (Tipo C)** |
|---|---|---|
| Aire de combustión | Del ambiente | Del exterior |
| Evacuación | Por conducto vertical a los 4 vientos | Por conducto horizontal a fachada o en U vertical |
| **Rejillas de ventilación en el local** | **OBLIGATORIAS** (superior + inferior, 4 cm²/kW, mín. 100 cm²) | **NO requiere rejillas por combustión** |
| Admitido en dormitorios | **NO** | **SÍ** (calefactores) |
| Admitido en baños | **NO** | **SÍ** |
| Admitido en monoambientes | Solo con restricciones fuertes de volumen | **SÍ** |
| Riesgo de intoxicación por CO | **Existe** (tiro invertido, obstrucción, extractores) | **Prácticamente nulo** |
| Pérdida térmica del local | **Alta** (las rejillas son un agujero permanente) | **Nula** |
| Costo del artefacto | Menor | Mayor |
| Impacto en fachada | Sombrerete en cubierta | **Terminal a la vista en fachada** |

> **RECOMENDACIÓN DEL ESTUDIO PARA SANTA ROSA — sin matices:**
>
> **Especificar SIEMPRE artefactos de cámara estanca (Tipo C) en obra nueva.** Razones:
> 1. **Térmica:** con 1.394 GD18, dos rejillas permanentes de 100-200 cm² por local son una pérdida de calor considerable durante 5 meses al año. Un living con dos rejillas de 150 cm² pierde, con viento y ΔT de 20 °C, del orden de **0,3 a 0,6 kW continuos** — más que un radiador chico. `[valor estimativo: verificar con cálculo de infiltración según ASHRAE Fundamentals cap. 16]`
> 2. **Seguridad:** elimina el riesgo de CO.
> 3. **Libertad de proyecto:** permite calefactores en dormitorios y calefón/caldera en baño o lavadero.
> 4. **Compatibilidad con ventilación mecánica:** el Tipo B es incompatible con recuperadores de calor y con extractores de cocina.
>
> **Contrapartida a resolver en el proyecto:** los terminales de fachada de cámara estanca son visibles y tienen distancias mínimas a ventanas, esquinas, balcones y a otros terminales. **Hay que dibujarlos en la fachada, en el anteproyecto.** `[verificar tabla de distancias mínimas de terminales de cámara estanca en NAG-200, apartado 6.6]`

### 4.12.4 Conductos colectivos para artefactos de cámara abierta (6.10)

Sistema de "conducto único en derivación" (shunt): un conducto principal vertical al que se conectan conductos secundarios de cada piso.

| Aspecto | Referencia NAG-200 |
|---|---|
| Disposiciones generales | 6.10.1 |
| Elementos y materiales | 6.10.2 |
| **Secciones mínimas de conducto principal y secundario** | **6.10.3** `[verificar tabla completa en la edición vigente de NAG-200]` |
| Dimensionamiento del conducto | 6.10.4 |
| Montaje | 6.10.5 |
| Controles e inspecciones | 6.10.6 |
| Responsabilidad sobre la construcción | 6.11 |

> **Regla crítica ya citada (5.9.2.4):** en las cocinas con artefactos conectados a conducto colectivo, **prohibido instalar campanas o extractores comunicados con el exterior**, con chapa de advertencia obligatoria en el artefacto.
>
> **Recomendación:** en obra nueva, **evitar el conducto colectivo**. Es una tecnología heredada, con alto riesgo operativo (una sola unidad que instala un extractor compromete a todo el edificio) y de mantenimiento complejo. **Ir a cámara estanca individual.**

### 4.12.5 Dos o más artefactos a un conducto común (6.8) y control de tiro (6.9)

Existen requisitos generales (6.8.1), reglas para conductos que rematan verticalmente a los cuatro vientos (6.8.2), para tendido horizontal (6.8.3), para equipos secarropas (6.8.4) y para sistemas con control de tiro (6.9). `[consultar NAG-200 edición vigente para el detalle de estos apartados si el proyecto los requiere]`

### 4.12.6 Calderas murales y calentadores instantáneos de tiro forzado (6.12)

Tienen un apartado específico de evacuación de productos de combustión. `[consultar NAG-200, 6.12, edición vigente]`

---

## 4.13 Gas natural vs. gas envasado / zeppelin

### 4.13.1 Comparativa

| | **Gas natural (GN) de red** | **GLP envasado (garrafas / tubos)** | **GLP a granel (zeppelin / tanque)** |
|---|---|---|---|
| **Densidad relativa (aire=1)** | **0,65 — más liviano que el aire** | **1,52 — MÁS PESADO que el aire** | 1,52 |
| Poder calorífico superior | 9.300 kcal/m³ | ~ 22.500 kcal/m³ (propano) `[verificar]` | ídem |
| Presión de servicio interna | 19 mbar | ~ 28-37 mbar `[verificar en NAG-200 cap. 11]` | ídem |
| Continuidad de suministro | Total | Depende de la logística | Alta (con control de nivel) |
| Costo por caloría | **El más bajo** | El más alto | Intermedio |
| **Inversión inicial** | Conexión a red | Mínima | Alta (tanque, obra civil, distancias) |
| **Instalable en subsuelo** | Sí | **NO — PROHIBIDO (NAG-200, 5.8.10)** | NO |
| **Gabinete en planta baja** | En LM | **Solo PB**, cota ≥ 0,10 m sobre vereda | ídem |
| **Ventilación del gabinete en espacio cerrado** | Conducto superior ≥ 30 cm² + abertura inferior en puerta ≥ 30 cm² | **Recinto ESTANCO respecto al ambiente**, ventilado al exterior por conductos conectados a la parte **superior E INFERIOR** del gabinete | ídem |

### 4.13.2 Reglas específicas de GLP (NAG-200, capítulo 11)

| Aspecto | Apartado |
|---|---|
| Cañerías | 11.2.1 |
| Válvulas de corte | 11.2.2 |
| Artefactos | 11.2.3 |
| Evacuación de productos de combustión, aporte de aire y ventilación | 11.2.4 |
| Pruebas | 11.2.5 |
| Documentación y habilitación | 11.2.6 |
| Equipo individual y batería de cilindros | Anexo B (informativo) |

> **La razón física de todas las diferencias:** el GLP es **más pesado que el aire (δ = 1,52)**. Una fuga **no sube y se ventila: baja y se acumula en el punto más bajo** — el subsuelo, el foso del ascensor, la cámara de inspección. De ahí las prohibiciones de subsuelo y la exigencia de ventilación inferior estanca.
>
> **Para Santa Rosa:** la ciudad tiene red de gas natural. **El GLP a granel solo se justifica en implantaciones rurales o en localidades del interior de La Pampa sin red.** En esos casos, el proyecto debe considerar: distancias del tanque a medianeras y edificios, camino de acceso del camión cisterna, y **el sobrecosto energético en calefacción, que en zona fría es sustancial**. `[verificar distancias de seguridad del tanque de GLP a granel en la normativa ENARGAS y en el Código de Edificación de Santa Rosa]`

---

## 4.14 Pruebas de las instalaciones (NAG-200, capítulo 7)

### 4.14.1 Consideraciones generales (7.2)

| Regla |
|---|
| Toda instalación debe someterse a **verificación técnica**, **prueba de hermeticidad**, y **pruebas de obstrucción y funcionamiento de los conductos** |
| Las cañerías se prueban con **aire, nitrógeno o dióxido de carbono**. **PROHIBIDO el uso de oxígeno y de productos inflamables o corrosivos** |
| **Manómetro clase 1**, apto para el rango, con **calibración vigente**, hermético al agua y al polvo, **cuadrante de no menos de 100 mm de diámetro**. Se admiten instrumentos digitales que abarquen los valores requeridos |
| Se admite probar como unidad única o por secciones. **Las válvulas del tramo a probar deben permanecer ABIERTAS** durante el ensayo |
| Los componentes que puedan dañarse deben retirarse |
| **Las pruebas deben efectuarse ANTES de la habilitación**, y su resultado satisfactorio es condición indispensable |

### 4.14.2 TABLA DE PRUEBAS DE HERMETICIDAD

| Elemento | Presión de prueba | Duración mínima | Rango del manómetro | Criterio |
|---|---|---|---|---|
| **Prolongación interna — tramos a media presión** (0,5 a 4 bar) | **6 bar** | **15 min** | 0 a 10 bar | **Sin disminución de presión** |
| **Prolongación interna — tramos a baja presión** (19 mbar) | **150 mbar** | **15 min** | 0 a 0,5 bar | **Sin disminución de presión** |
| **Cañería interna — fase 1** (válvulas de corte terminales CERRADAS, intermedias abiertas) | **150 mbar** | **15 min** | 0 a 0,5 bar | **Debe mantenerse la presión** |
| **Cañería interna — fase 2** (válvulas terminales ABIERTAS, robinetes de artefactos cerrados) | **50 mbar** | **5 min** | 0 a 0,5 bar | **Debe mantenerse la presión** |

### 4.14.3 Prueba de obstrucción (7.3.1.2 y 7.3.2.2)

- **Prolongación:** finalizada la hermeticidad, ventear la cañería **por el extremo opuesto** a la conexión del manómetro.
- **Cañería interna:** sacar sucesivamente los tapones de las tomas declaradas y abrir los robinetes de cada artefacto para **comprobar la salida de aire en cada uno**.

### 4.14.4 Conductos de ventilación y de evacuación (7.3.3)

| Prueba | Criterio |
|---|---|
| **Obstrucción y hermeticidad** | Comprobar que **no existan fisuras ni obstrucciones** en todo el recorrido |
| **Funcionamiento y hermeticidad** | Someter a **prueba de estanquidad y tiraje mediante aporte de humo**. Es exigible la **total evacuación** de los productos de combustión por el remate, **sin fugas en el trayecto, sin migración a recintos o ambientes y sin retorno** |

> **La prueba de humo del conducto es la que más se saltea y la que más problemas evita.** En un edificio con conductos colectivos o con conductos que atraviesan varias plantas, es la única forma de detectar una junta abierta que va a llevar CO al departamento de al lado.

---

## 4.15 Documentación y trámite (NAG-200, capítulo 8)

### 4.15.1 Secuencia de trámite

```
1. FACTIBILIDAD DE SUMINISTRO DE GAS  ──────────────────────────►  Prestadora
   (formulario 8.6.1 + plano con ubicación del sistema de regulación/medición)
                    │
                    │  Aprobación. Retirar 2 copias (una para el usuario)
                    │  ⚠ Caduca a los 60 días corridos si no se retiran las copias
                    ▼
2. EJECUCIÓN DE LA OBRA por Instalador Matriculado
                    │
                    ▼
3. PEDIDO DE INSPECCIÓN PARCIAL (8.3.1) — cañerías a la vista, antes de tapar
                    │
                    ▼
4. PEDIDO DE INSPECCIÓN FINAL (8.3.2) — instalación completa con artefactos
                    │
                    ▼
5. HABILITACIÓN "IN SITU" DE ARTEFACTOS (8.4), si corresponde
                    │
                    ▼
6. PLANO CONFORME A OBRA (8.5)
                    │
                    ▼
7. HABILITACIÓN DE LA INSTALACIÓN (capítulo 9)
```

### 4.15.2 Reglas de documentación

| Regla |
|---|
| La documentación (formularios + planos) se tramita **por triplicado**: original para la Prestadora, una copia para el usuario, una para el Instalador Matriculado |
| Si se admite tramitación digital, **debe quedar siempre en poder del usuario una copia EN PAPEL** de: Factibilidad de suministro, Pedido de inspección final aprobado y Plano conforme a obra |
| En pedidos de factibilidad por **incremento de consumo** que no impliquen modificar el dimensionamiento: presentar **memoria de cálculo** comprobando que la instalación es apta |
| La Factibilidad **caduca** si las copias no se retiran dentro de los **60 días corridos** de la presentación |

### 4.15.3 Obligaciones del Instalador Matriculado (capítulo 12)

El capítulo 12 de NAG-200 establece las **obligaciones y responsabilidades del Instalador Matriculado** (12.2) y el procedimiento de **cambio de matriculado** (12.3).

> **Para el estudio:** el arquitecto **no puede firmar gas**. Debe: (a) contratar o exigir al comitente la contratación de un Instalador Matriculado desde el anteproyecto; (b) exigirle el cálculo y el plano de gas **antes de cerrar la arquitectura**, porque las rejillas, el gabinete, los conductos y las restricciones de ambiente **modifican el proyecto**; (c) verificar que se ejecute la inspección parcial antes de tapar cañerías.

### 4.15.4 Instalaciones en servicio (capítulo 10)

Cubre reparación (10.4.1) y modificación (10.4.2) de la instalación interna, cambio de medidor (10.5) e instalaciones fuera de uso (10.6). **Relevante para reformas: toda intervención sobre una instalación en servicio la realiza el matriculado, con medidas de seguridad específicas (10.3).**

---

# 5. INSTALACIONES ELÉCTRICAS

## 5.1 Marco normativo: AEA 90364

| Parte | Objeto |
|---|---|
| **AEA 90364-7-770** | **Viviendas, oficinas y locales unitarios hasta 63 A.** Es la parte que se usa para dimensionar la instalación de una vivienda o un departamento |
| **AEA 90364-7-771** | Viviendas, oficinas y locales (unitarios). Incluye requisitos adicionales para **instalaciones comunes de edificios** (ascensores, bombas, iluminación de espacios comunes) |
| **AEA 90364-7-701** | Cuartos de baño y duchas — **volúmenes de protección** |
| **AEA 90364-7-718** | Lugares de pública concurrencia `[verificar número exacto de la parte según la edición]` |
| **AEA 90364 capítulos 32, 51, 52** | Influencias externas, selección e instalación de materiales, canalizaciones |
| **AEA 90865** | Cálculo de corrientes de cortocircuito |
| **IRAM 2005** | Tomacorrientes / clavijas — sistema argentino `[verificar alcance exacto]` |
| **IRAM 2071** | Tomacorrientes 2x10+T |
| **IRAM-NM 60884-1 / IEC 60884-1** | Tomacorrientes con pantalla de protección |
| **IRAM 2183** | `[verificar objeto exacto — presumiblemente relacionado a conductores o accesorios]` |
| **IRAM-NM 247-3 / IRAM 62267** | Cables unipolares aislados para instalaciones fijas |
| **IRAM 2178 / IRAM 62266** | Cables con envoltura de protección |
| **IRAM 2309 / 2310** | Jabalinas cilíndricas de puesta a tierra |
| **IRAM 2343** | Tomacable de bronce o latón |
| **IRAM 2281 Parte I** | Puesta a tierra — mediciones `[verificar]` |

**Ámbito de aplicación de la parte 770:** viviendas con **corriente máxima de 63 A** y **corriente presunta de cortocircuito en el origen ≤ 10 kA**, clasificación de utilización **BA2 (presencia de niños)** y **BD1 (baja densidad de ocupación)**.

**Quién firma:** proyecto y dirección de la instalación eléctrica corresponden a un **profesional matriculado con incumbencia** (Ingeniero Electricista / Electromecánico, o Técnico según alcance), y la ejecución a un **Instalador Electricista matriculado en la categoría correspondiente**. La distribuidora exige la documentación firmada para dar el suministro. `[verificar exigencias de matrícula y categoría de la distribuidora de Santa Rosa]`

---

## 5.2 Grados de electrificación (770.7.4)

### TABLA 770.7.I — Resumen de los grados de electrificación

| Grado de electrificación | Superficie (límite de aplicación) |
|---|---|
| **Mínimo** | hasta **60 m²** |
| **Medio** | más de 60 m² hasta **130 m²** |
| **Elevado** | más de 130 m² hasta **200 m²** |
| **Superior** | más de **200 m²** |

**Notas de la norma (770.7.6):**
- *Nota 1:* Se considera que las viviendas con superficie inferior a 130 m² **no poseen dormitorios de superficie mayor a 36 m²**. Si ese caso fuese factible, los puntos mínimos de utilización deben tomarse del grado **"elevado"**.
- *Nota 2:* Los grados de electrificación para viviendas tipo **"loft"** se consideran de acuerdo a su **superficie total**.

> **Nota importante:** *"En el caso de las viviendas NO interviene la potencia en kW en función de la superficie."* El grado se determina **solo por superficie**. La potencia resulta del cálculo de DPMS (§5.7). Los valores de "3,5 / 6,6 / 10,6 kW" que circulan asociados a los grados son **de referencia orientativa, no un límite normativo**. `[verificar si alguna edición o guía de aplicación fija esos valores como límite]`

---

## 5.3 Tipos de circuito y número mínimo de circuitos

### 5.3.1 Nomenclatura de circuitos (770.6)

| Sigla | Circuito |
|---|---|
| **IUG** | Iluminación de Uso General |
| **TUG** | Tomacorrientes de Uso General |
| **IUE** | Iluminación de Uso Especial |
| **TUE** | Tomacorrientes de Uso Especial |
| **ACU** | Alimentación de Carga Única (un solo consumo, ej. aire acondicionado) |
| **ATE** | Alimentación a Tableros Eléctricos (seccionales) |
| **APM** | Alimentación a Pequeños Motores |
| **ITE** | Iluminación en Tensiones Especiales |
| **OCE** | Otros Circuitos Especiales |
| **MBTF** | Muy Baja Tensión Funcional |
| **MBTS** | Muy Baja Tensión de Seguridad (sin puesta a tierra) |

### 5.3.2 TABLA 770.7.II — Número mínimo de circuitos

| Grado de electrificación | Cantidad mínima de circuitos | Variante | IUG | TUG | Circuito de libre elección |
|---|---|---|---|---|---|
| **Mínimo** | **2** | Única | 1 | 1 | — |
| **Medio** | **3** | a) | 2 | 1 | — |
| | | b) | 1 | 2 | — |
| **Elevado** | **5** | a) | 2 | 3 | — |
| | | b) | 3 | 2 | — |
| **Superior** | **6** | a) | 2 | 3 | 1 |
| | | b) | 3 | 2 | 1 |

### 5.3.3 Límites por circuito de uso general

| Circuito | Número máximo de bocas | Protección máxima |
|---|---|---|
| **IUG** | **15 bocas de salida** | **≤ 16 A**, en ambos polos |
| **TUG** | **15 bocas de salida** | **≤ 20 A**, en ambos polos |

`[el valor de 16 A para IUG y 20 A para TUG figura en las guías de aplicación; verificar contra el texto exacto de la edición vigente de 770.7 y 770.15]`

### 5.3.4 Reglas de agrupamiento en cañería (770.7.3)

| Regla |
|---|
| Se permite que las líneas de alumbrado y tomacorrientes estén alojadas en **una misma cañería**, pero **no deben alimentar una misma boca de salida**. En bocas mixtas (interruptor + tomacorriente), cada una va a su circuito |
| **Dentro de cada cañería se pueden colocar hasta TRES líneas de circuitos de uso general**, siempre que: (a) pertenezcan a la **misma fase**, (b) la suma de sus cargas **no supere 20 A**, y (c) el número de bocas de salida **no supere 15** |
| Se consideran **casos especiales, que deben ir en cañerías independientes**, aquellos con **cargas individuales superiores a 8 A en 220 V c.a.** (ejemplo: aire acondicionado). **Se deben proyectar todos los tomacorrientes necesarios para los lugares de empleo de equipos** |
| Cuando exista cañería que vincule el **tablero principal con un primer tablero seccional**, debe ser de **diámetro mínimo R19 (¾")**, incluyendo las cañerías de columnas montantes |
| **Ventiladores de techo y extractores de aire** pueden cargarse a circuitos de iluminación (fijos o por tomacorriente). Para el cálculo de la demanda, **se computan como una boca de iluminación** |
| **Escaleras y rampas:** mínimo **una boca de iluminación de uso general cada 5 m de longitud o fracción**, o bien en cada descanso |
| **Fuentes de comunicación, portería, timbres:** se alimentan por circuitos de iluminación; se les asigna la potencia de **una boca de iluminación por cada fuente** y **cada punto se considera una boca** a efectos de la cantidad total |
| **Cajas en losa** (paso, derivación, o paso y derivación): **se consideran bocas y cuentan para el grado de electrificación si sus medidas alcanzan los 100 × 100 mm inclusive.** Medidas superiores no cuentan |
| **Circuitos de comando en ambientes mojados** (interruptores a flotante, señalizaciones, alarmas), incluyendo donde están los tanques cisterna y elevado: **deben alimentarse con MBTS** |
| **Toda parte metálica de timbres, porteros eléctricos, alarmas alimentados por MBTF debe estar conectada a tierra**, y el conductor de protección acompaña a los circuitos de MBTF. **En cambio, si están alimentados en MBTS por transformadores de seguridad certificados (IEC 61558-2-6) o fuentes (IEC 61558-2-16), las masas NO deben conectarse a tierra** |
| **Fuentes de muy baja tensión hasta 24 V:** transformador con primario y secundario independientes. **NO se permite el uso de autotransformadores** |
| **Ambientes integrados** (cocina-comedor diario): deben cumplir con las prescripciones de **cada uno de los ambientes por separado** |
| **Toilette** (cuarto de baño sin bañera ni ducha): el tomacorriente requerido **puede cargarse al circuito de iluminación** |
| **Kitchinette:** además de los puntos del ambiente donde está, mínimo **una boca de iluminación sobre la zona de la kitchinette** (puede ser bajo cenefa) y **dos bocas para TUG más un tomacorriente para artefactos de ubicación fija** |
| **Instalaciones trifásicas:** procurar el sistema lo más equilibrado posible |

---

## 5.4 TABLA 770.7.III — Puntos mínimos de utilización

| Ambiente | Grado | IUG | TUG |
|---|---|---|---|
| **Sala de estar, comedor, comedor diario, escritorio, estudio, biblioteca o similares** | Todos (Mínimo, Medio, Elevado, Superior) | **Una boca cada 18 m² de superficie o fracción (mínimo una)** | **Una boca cada 6 m² de superficie o fracción (mínimo dos)** |
| **Dormitorio de superficie < 10 m²** | Todos | **Una boca** | **Dos bocas** |
| **Dormitorio de 10 m² a 36 m²** | Todos | **Una boca** | **Tres bocas** |
| **Dormitorio > 36 m²** | Elevado y Superior | **Dos bocas** | **Tres bocas** |
| **Cocina** | Mínimo | Una boca | **Tres bocas + dos módulos de tomacorrientes\*** |
| | Medio | **Dos bocas** | **Tres bocas + dos módulos\*** |
| | Elevado | Dos bocas | **Tres bocas + tres módulos\*** |
| | Superior | Dos bocas | **Cuatro bocas + tres módulos\*** |
| **Baño** (para toilette ver 770.7.3.k) | Todos | **Una boca** | **Una boca** |
| **Vestíbulo, garaje, hall, vestidor o similares** | Todos | `[verificar valores en la tabla completa de la edición vigente]` | `[ídem]` |

> \* Los módulos de tomacorrientes se destinan a **electrodomésticos de ubicación fija** y pueden compartir una misma boca con los otros tomacorrientes.

**Electrodomésticos de ubicación fija en cocinas y lavaderos (770.7.3.i):** heladeras, freezers, extractores de humo, lavavajillas, cocinas eléctricas, cocinas/anafes/hornos a gas que requieran alimentación eléctrica, lavarropas, secarropas, máquinas fijas de planchado.

### 5.4.1 Ubicación de tomacorrientes e interruptores (770.7.7)

| Regla | Valor |
|---|---|
| Cajas de tomacorrientes por encima de zócalos: arista inferior | **≥ 0,15 m** del solado terminado |
| **Tomacorrientes a nivel de zócalo o hasta 0,90 m del solado** | Deben ser **2x10+T según IRAM 2071** y llevar **pantalla de protección contra inserción de cuerpos extraños** (IRAM-NM 60884-1 / IEC 60884-1). *Motivo: la Sección considera la presencia de niños, clasificación BA2* |
| Cajas sobre mesadas de baños, cocinas y lavaderos | Aristas inferiores a **≥ 0,10 m del nivel de mesada**, respetando además las distancias a fuentes de agua de la Sección 701 |
| Ambientes con limpieza por **baldeado** | Cajas con arista inferior a **≥ 0,20 m** del solado, con tomacorriente **IP20 mínimo**. **Si están por debajo de ese nivel: grado de protección mínimo IP54** del conjunto (caja, tomacorriente y tapa) |
| **Pasillos interiores de más de 3 m** | **Interruptores de combinación en cada extremo** |
| Tomacorrientes en planos horizontales con orificios hacia arriba | **No recomendados** (pierden propiedades dieléctricas por acumulación de material conductor) |
| **Bocas mixtas** (interruptor + tomacorriente) | El tomacorriente debe conectarse **al circuito de iluminación presente en la caja** e identificarse indeleblemente con el ideograma **N.º 5012 de IEC 60417**. **NO se permiten tomacorrientes conectados al circuito de iluminación situados a menos de 0,90 m del solado.** Si hacen falta a menor altura, deben pertenecer al circuito de tomacorrientes, en caja separada de los interruptores de iluminación |

---

## 5.5 Secciones mínimas y corrientes admisibles

### 5.5.1 Secciones mínimas por tipo de circuito (770.11)

| Tipo de línea | Sección mínima (Cu) |
|---|---|
| Circuitos terminales para **iluminación de usos generales** (fija o por tomacorrientes) | **1,50 mm²** |
| Circuitos terminales para **tomacorrientes de usos generales** | **2,50 mm²** |
| Circuitos terminales de **iluminación de usos generales que incluyen tomacorrientes** | **2,50 mm²** |
| Líneas de circuito para **usos especiales** | **2,50 mm²** |
| Líneas de circuito para **uso específico** (excepto MBTF) | **2,50 mm²** |
| Líneas de circuito para uso específico (alimentación a **MBTF**) | **1,50 mm²** |
| **Alimentaciones a interruptores de efecto** | **1,00 mm²** |
| **Retornos de interruptores de efecto** | **1,00 mm²** |
| **Conductor de protección (PE)** | **2,50 mm²** |

### 5.5.2 TABLA 770.12.I — Intensidad de corriente admisible [A] a 40 °C

Cables unipalares aislados PVC / LS0H (IRAM-NM 247-3 / IRAM 62267), en cañería:

| Sección Cu (mm²) | **2x** (2 cables cargados + PE) | **3x** (3 cables cargados + N + PE) |
|---|---|---|
| **1,5** | **15** | **14** |
| **2,5** | **21** | **18** |
| **4** | **28** | **25** |
| **6** | **36** | **32** |
| **10** | **50** | **44** |
| **16** | **66** | **59** |
| **25** | **88** | **77** |
| **35** | **109** | **96** |
| **50** | **131** | **117** |
| **70** | **167** | **149** |
| **95** | **202** | **180** |
| **120** | **234** | **208** |
| **150** | **261** | **228** |
| **185** | **297** | **258** |
| **240** | **348** | **301** |
| **300** | **398** | **343** |

### 5.5.3 TABLA 770.12.II — Factor de corrección por agrupamiento

| Circuitos en un mismo caño | N.º de cables cargados | Factor | Se aplica a |
|---|---|---|---|
| **2 monofásicos** | hasta 4 | **0,80** | Columna 2x |
| **3 monofásicos** | hasta 6 | **0,70** | Columna 2x |
| **2 trifásicos** | hasta 6 | **0,80** | Columna 3x |
| **3 trifásicos** | hasta 9 | **0,70** | Columna 3x |

- *Nota 1:* Los conductores de protección PE **no se contabilizan** como cables cargados.

> **Error frecuente:** meter 3 circuitos monofásicos en un caño de ¾" y usar la corriente admisible de tabla sin corregir. Con factor **0,70**, un 2,5 mm² pasa de 21 A a **14,7 A** — y ya no soporta una protección de 20 A. **Hay que corregir siempre.**

### 5.5.4 Diámetros mínimos de cañería (770.10.3)

| Caso | Diámetro mínimo |
|---|---|
| General | **15 mm (RL 19 y RS 19)**; sección mínima para otras formas: **200 mm²** |
| Caso particular (`verificar contexto exacto en el texto`) | **13 mm (RL 16 y RS 16)**; sección mínima para otras formas: **150 mm²** |
| Cañería tablero principal → primer tablero seccional, y columnas montantes | **R19 (¾") mínimo** |

---

## 5.6 Caída de tensión admisible (770.15.6)

> La caída de tensión **entre los bornes de salida del tablero principal y cualquier punto de utilización** no debe superar:

| Circuito | Caída máxima |
|---|---|
| **Circuitos terminales de uso general, especial y específico para iluminación** | **3 %** |
| **Circuitos de uso específico que alimentan solo motores** | **5 % en régimen** y **15 % durante el arranque** |

**Criterios de cálculo:**
- Los circuitos de iluminación y tomacorrientes se consideran **cargados con su DPMS en el extremo más alejado del tablero seccional**.
- **Los circuitos de iluminación se consideran con 2/3 de la carga total en el extremo más alejado del tablero seccional.**
- Para tableros seccionales donde se previó un factor de simultaneidad, **debe aplicarse ese mismo factor** al calcular la corriente máxima simultánea.

**Fórmula aproximada:**

> **ΔU = k × I × L × (R × cos φ + X × sen φ)**  [volts]

| Símbolo | Significado |
|---|---|
| **k** | **2** para sistemas monofásicos y bifásicos; **√3** para trifásicos |
| I | corriente de línea [A] |
| L | longitud del circuito [km] (distancia entre los dos puntos, **no** la longitud total de cables) |
| R | resistencia efectiva del conductor a la temperatura de servicio [Ω/km] |
| X | reactancia [Ω/km] |
| cos φ | factor de potencia |

**Factores de potencia a falta de datos más precisos:**
- **cos φ = 0,85 y sen φ = 0,53**
- **Durante el arranque de motores: cos φ = 0,30 y sen φ = 0,95**

Existe además la **Tabla 770.17.IV** de la norma, con caída de tensión directa en cables IRAM-NM 247-3 e IRAM 62267 para cos φ = 0,80 y sen φ = 0,60, válida para líneas monofásicas. `[consultar la tabla completa en la edición vigente]`

---

## 5.7 Demanda de potencia máxima simultánea (DPMS)

### 5.7.1 TABLA 770.8.I — Demanda máxima de potencia simultánea

| Circuito | Valor mínimo de la demanda de potencia simultánea |
|---|---|
| **Iluminación de uso general SIN tomacorrientes derivados** | **2/3 de la que resulte al considerar todos los puntos de utilización previstos, a razón de 60 VA cada uno** |
| **Iluminación de uso general CON tomacorrientes derivados** | **2.200 VA por cada circuito** |
| **Tomacorrientes de uso general (TUG)** | **2.200 VA por cada circuito** |
| **Tomacorrientes de uso especial (TUE)** | **3.300 VA por cada circuito** |

> *Nota de la norma:* estos valores son **mínimos**, por la incertidumbre en las cargas a conectar. **Si los consumos son conocidos y superan estos mínimos, la DPMS debe calcularse en función de los mayores valores.**

### 5.7.2 TABLA 770.8.II — Coeficientes de simultaneidad

| Grado de electrificación | Coeficiente de simultaneidad |
|---|---|
| **Mínimo** | **1** |
| **Medio** | **0,8** |
| **Elevado** | **0,7** |
| **Superior** | **0,6** |

### 5.7.3 Cargas específicas (770.8.2)

> Para otros tipos de circuitos (MBTF, APM, ATE, MBTS, ACU, IUE, ITE u OCE — ver AEA 90364-7-771), se **suman las potencias de los circuitos dedicados a cargas específicas, multiplicados por los coeficientes de utilización de cada carga y de simultaneidad de cada grupo o conjunto de cargas**, según criterio del proyectista.

### 5.7.4 Carga total (770.8.3.1)

> **Carga total = DPMS del grado de electrificación (770.8.1) + DPMS de los circuitos dedicados a cargas específicas (770.8.2)**

*Nota 1:* En alimentación trifásica con circuitos monofásicos y trifásicos coexistentes, **la corriente del circuito seccional se calcula sumando las corrientes por fase y eligiendo la de la fase más cargada.**

### 5.7.5 Reglas complementarias

| Regla | Referencia |
|---|---|
| **Contratación del suministro:** la instalación se dimensiona para las cargas calculadas. El propietario **puede contratar potencias inferiores** según sus necesidades | 770.8.3.2 |
| **Suministro monofásico o trifásico:** las distribuidoras pueden definir el valor de potencia a partir del cual el suministro debe ser trifásico. **Cuando la carga total calculada supere los 7 kVA o los 32 A para una línea monofásica, es recomendable solicitar suministro trifásico** | 770.8.3.3 |
| **Equilibrio de cargas:** en tableros trifásicos, se recomienda que **el máximo desequilibrio entre las corrientes de las fases no supere el 30 %** | 770.8.3.4 |

### 5.7.6 Condiciones ambientales normales — TABLA 770.9.I

| Utilización | Código | Descripción |
|---|---|---|
| Temperatura ambiente | **AA4** | **−5 a +40 °C (Normal)** |
| Humedad atmosférica | AB4 | 5 % a 95 % (Normal) |
| Altitud | AC1 | ≤ 2.000 m |
| Presencia de agua | AD1 | Despreciable |
| Presencia de cuerpos sólidos extraños | AE1 | Despreciable |
| Sustancias corrosivas o contaminantes | AF1 | Normal |
| Impacto | AG1 | Baja severidad |
| Vibración | AH1 | Baja severidad |
| Flora o moho | AK1 | Sin riesgo |
| Fauna | AL1 | Sin riesgo |
| Influencia electromagnética/electrostática/ionizante | AM1 | Despreciable |
| Radiación solar | AN1 | Despreciable |
| Efectos sísmicos | AP1 | Despreciable |
| **Descargas atmosféricas** | **AQ2** | **Exposición indirecta** |

> *La norma advierte:* para lugares con **climas extremos**, efectos sísmicos o situaciones geográficas particulares, deben usarse las condiciones particulares de los capítulos 32 y 51 de AEA 90364.
>
> **Para Santa Rosa:** la temperatura mínima absoluta registrada en la estación Santa Rosa (Aero) es **−11,3 °C** (IRAM 11603), por debajo del límite inferior de AA4 (−5 °C). **En instalaciones a la intemperie (medidores en LM, tableros exteriores, bombas en cubierta) puede corresponder una clase de temperatura distinta.** `[verificar clasificación AA aplicable con el capítulo 32 de AEA 90364 para instalaciones exteriores en La Pampa]`
>
> Además, **La Pampa tiene actividad eléctrica atmosférica relevante en verano.** Ver §5.11 (protección contra sobretensiones).

---

## 5.8 EJEMPLO RESUELTO Nº 4 — Demanda eléctrica de un edificio PB+9 de 40 unidades

### Parte A — Demanda de un departamento tipo de 2 dormitorios (85 m²)

**Paso 1 — Grado de electrificación**
> 85 m² → **más de 60 m² y hasta 130 m² → GRADO MEDIO**

**Paso 2 — Número mínimo de circuitos (Tabla 770.7.II)**
> Grado Medio → **mínimo 3 circuitos de uso general.**
> Adoptamos la **variante b): 1 IUG + 2 TUG.**

**Paso 3 — Puntos mínimos de utilización (Tabla 770.7.III)**

| Ambiente | Superficie | IUG requeridas | TUG requeridas |
|---|---|---|---|
| Estar-comedor | 26 m² | ⌈26/18⌉ = **2** | ⌈26/6⌉ = **5** |
| Dormitorio 1 | 14 m² | **1** | **3** |
| Dormitorio 2 | 11 m² | **1** | **3** |
| Cocina | 9 m² | **2** (grado Medio) | **3 + 2 módulos** |
| Baño | 4 m² | **1** | **1** |
| Toilette | 2 m² | **1** | **1** (puede ir al circuito de iluminación) |
| Paso / hall | 6 m² | **1** | **1** |
| Lavadero | 3 m² | **1** | **2** |
| **TOTAL** | **85 m²** | **10 bocas IUG** | **19 bocas TUG (+ 2 módulos)** |

**Paso 4 — Verificación del límite de 15 bocas por circuito**
- IUG: 10 bocas ≤ 15 ✓ → **1 circuito IUG** alcanza
- TUG: 19 bocas > 15 ✗ → **se necesitan 2 circuitos TUG** (por ejemplo 10 + 9) ✓

**Coincide con la variante b) del grado Medio: 1 IUG + 2 TUG. ✓**

**Paso 5 — Cargas específicas previstas**
- **1 circuito ACU** para aire acondicionado split de 3.000 frigorías (≈ 1.400 VA) — obligatorio en cañería independiente por superar 8 A `(770.7.3, casos especiales)`. En rigor, un split de 1.400 VA da 1.400/220 = 6,4 A < 8 A; pero un split de 4.500 frigorías (2.100 VA → 9,5 A) sí supera el umbral.
- **1 circuito TUE** para lavarropas + horno eléctrico
- **En Santa Rosa**, prever además la **caldera mural** (bomba + electrónica, ~150 VA) y eventualmente **1 circuito ACU adicional** para un segundo split.

**Paso 6 — Cálculo de la DPMS (Tabla 770.8.I)**

| Circuito | Cálculo | VA |
|---|---|---|
| **IUG** (sin tomacorrientes derivados) | 2/3 × (10 bocas × 60 VA) = 2/3 × 600 | **400** |
| **TUG 1** | valor mínimo de tabla | **2.200** |
| **TUG 2** | valor mínimo de tabla | **2.200** |
| **Subtotal DPMS del grado** | | **4.800 VA** |

**Paso 7 — Coeficiente de simultaneidad (Tabla 770.8.II)**
> Grado Medio → **0,8**
>
> **DPMS del grado = 4.800 × 0,8 = 3.840 VA**

**Paso 8 — Cargas específicas (770.8.2)**

| Circuito | Potencia | Coef. de utilización | Aporte |
|---|---|---|---|
| TUE (lavarropas + horno) | 3.300 VA (mínimo de tabla) | 1,0 | **3.300 VA** |
| ACU split 3.000 fg | 1.400 VA | 1,0 | **1.400 VA** |
| Caldera mural | 150 VA | 1,0 | **150 VA** |
| **Subtotal cargas específicas** | | | **4.850 VA** |

> **Nota:** al TUE **no se le aplica el coeficiente de simultaneidad del grado** — ese coeficiente se aplica solo a la DPMS de 770.8.1. Las cargas específicas llevan sus propios coeficientes de utilización y simultaneidad, a criterio del proyectista.

**Paso 9 — Carga total del departamento (770.8.3.1)**

> **Carga total = 3.840 + 4.850 = 8.690 VA = 8,69 kVA**
>
> **Potencia activa = 8,69 × 0,85 = 7,39 kW**
>
> **Corriente monofásica = 8.690 / 220 = 39,5 A**

**Paso 10 — Verificación del tipo de suministro (770.8.3.3)**
> 8,69 kVA **> 7 kVA** y 39,5 A **> 32 A**
>
> **→ ES RECOMENDABLE SUMINISTRO TRIFÁSICO PARA ESTA UNIDAD.**

> **Decisión de proyecto:** en un edificio de 40 unidades, dar trifásico a cada departamento es inviable operativamente. **La alternativa correcta es reducir la carga específica:** especificar **cocina y horno a gas** (no eléctricos) y **calefacción a gas** (no eléctrica). Con eso el TUE baja o desaparece:
>
> Carga total revisada (sin horno eléctrico, con TUE solo para lavarropas): 3.840 + 2.200 (TUE reducido a un TUG adicional) + 1.400 + 150 = **7.590 VA = 34,5 A** → sigue por encima de 32 A.
>
> **Con un solo split y sin TUE:** 3.840 + 1.400 + 150 = **5.390 VA = 24,5 A** → **monofásico ✓**
>
> **CONCLUSIÓN DE PROYECTO:** la definición de si el edificio va con departamentos monofásicos o trifásicos **se toma en el anteproyecto, junto con la decisión de qué se hace a gas y qué se hace a electricidad.** Si el comitente quiere cocina eléctrica y aire acondicionado en todos los ambientes, hay que ir a trifásico y a una sala de medidores mucho más grande.

### Parte B — Demanda del edificio completo

**Paso 1 — Demanda de las unidades**

| Tipología | Cant. | Superficie | Grado | DPMS del grado (VA) | Cargas específicas (VA) | Carga total unitaria (VA) |
|---|---|---|---|---|---|---|
| 1 dormitorio | 12 | 52 m² | **Mínimo** | (1 IUG: 2/3×7×60=280) + (1 TUG: 2.200) = 2.480 × **1,0** = **2.480** | ACU split 1.400 | **3.880** |
| 2 dormitorios | 20 | 85 m² | **Medio** | **3.840** | ACU 1.400 + caldera 150 = 1.550 | **5.390** |
| 3 dormitorios | 8 | 135 m² | **Elevado** | (2 IUG: 2/3×14×60=560) + (3 TUG: 6.600) = 7.160 × **0,7** = **5.012** | 2 ACU 2.800 + caldera 150 = 2.950 | **7.962** |

**Suma de cargas de las unidades:**
> 12 × 3.880 = 46.560 VA
> 20 × 5.390 = 107.800 VA
> 8 × 7.962 = 63.696 VA
> **Subtotal viviendas = 218.056 VA = 218,06 kVA**

**Paso 2 — Locales comerciales de PB**
> 2 locales × 5.000 VA (estimado, según destino) = **10.000 VA**
> `[verificar: la carga de local comercial se calcula por su destino específico, no por grado de electrificación de vivienda — ver AEA 90364-7-771]`

**Paso 3 — Servicios generales del edificio**

| Servicio | Potencia (VA) | Observación |
|---|---|---|
| **Ascensor 1** (630 kg, gearless, VVVF) | **7.500** | `[verificar potencia real con el proveedor]` |
| **Ascensor 2** | 7.500 | |
| **Bomba de agua** (7,5 kW, ver Ej. Nº 1) | **8.800** | Solo una en marcha (la otra en reserva) |
| **Grupo de presurización** (2 × 1,1 kW) | **2.600** | |
| **Bomba de achique pluvial** (2 × 1,5 kW) | **1.800** | Solo una en marcha |
| **Bomba cloacal de subsuelo** (2 × 1,5 kW) | **1.800** | Solo una en marcha |
| **Bombas de incendio** (ver Cap. 7) | **22.000** | Régimen de emergencia; **no simultáneo con el resto** |
| **Iluminación de palieres, escalera, hall, cocheras** (10 plantas + subsuelo) | **6.000** | Con LED y sensores |
| **Iluminación de emergencia** (autónoma) | 500 | |
| **Portero visor, CCTV, portón, antena** | **1.500** | |
| **Tomacorrientes de servicios y portería** | **2.200** | |
| **Extracción forzada de cocheras** (ver Cap. 6) | **4.000** | |
| **Presurización de escalera** (si corresponde) | `[verificar]` | Régimen de emergencia |
| **SUBTOTAL SERVICIOS GENERALES (sin incendio)** | **≈ 44.200 VA** | |

**Paso 4 — Aplicación del factor de simultaneidad del edificio**

Aquí la norma 770 no da una tabla directa (es para viviendas unitarias). Para el edificio se aplica **AEA 90364-7-771** y el criterio del proyectista, y **las tablas de la distribuidora**, que suelen ser las que mandan.

**Criterio adoptado (a verificar con la distribuidora):**

| Grupo | Carga (kVA) | Factor de simultaneidad adoptado | Demanda (kVA) |
|---|---|---|---|
| 40 viviendas | 218,06 | **0,35** | **76,32** |
| 2 locales | 10,00 | 0,80 | **8,00** |
| Servicios generales | 44,20 | **0,60** | **26,52** |
| **DEMANDA TOTAL DEL EDIFICIO** | | | **≈ 110,84 kVA** |

`[EL FACTOR DE SIMULTANEIDAD DEL EDIFICIO ES EL DATO MÁS SENSIBLE Y EL QUE MÁS VARÍA. VERIFICAR OBLIGATORIAMENTE contra el reglamento de la distribuidora de Santa Rosa. Valores típicos que se usan en Argentina para 40 viviendas: 0,30 a 0,45]`

**Paso 5 — Corriente y alimentador**

Suministro trifásico 3×380/220 V:
> **I = P / (√3 × U) = 110.840 / (1,732 × 380) = 110.840 / 658,2 = 168,4 A**

Adoptando margen de 25 % para crecimiento: **I_diseño = 210 A**

**Selección del alimentador (Tabla 770.12.I, columna 3x, corregida):**
- Cable de cobre en cañería enterrada o en bandeja, factor de agrupamiento 1,0 (circuito único)
- 240 mm² → 301 A ✓ (holgado)
- 185 mm² → 258 A ✓
- **150 mm² → 228 A ✓** ← primera sección que cumple con margen
- 120 mm² → 208 A (justo por debajo de 210 A) ✗

**→ Alimentador: 3 × 150 mm² + N 95 mm² + PE 95 mm², Cu, aislación PVC/LS0H.**

`[verificar tipo de cable exigido por la distribuidora — muchas exigen cable subterráneo tipo sintenax armado o similar, y el dimensionado puede diferir]`

**Verificación de caída de tensión** (longitud del alimentador desde la acometida hasta el tablero principal: 30 m):
> Para 150 mm² Cu: R ≈ 0,124 Ω/km a 70 °C; X ≈ 0,08 Ω/km
> ΔU = √3 × 168,4 × 0,030 × (0,124 × 0,85 + 0,08 × 0,53)
> ΔU = 1,732 × 168,4 × 0,030 × (0,1054 + 0,0424) = 8,75 × 0,1478 = **1,29 V**
> ΔU % = 1,29 / 380 = **0,34 %** ✓ (muy holgado)

### Resumen del Ejemplo Nº 4

| Concepto | Valor |
|---|---|
| Grado de electrificación de un dpto. de 85 m² | **Medio** |
| Circuitos mínimos | **3** (1 IUG + 2 TUG), más ACU y TUE según equipamiento |
| Bocas mínimas de ese departamento | **10 IUG + 19 TUG (+2 módulos)** |
| DPMS del grado, con coeficiente 0,8 | **3.840 VA** |
| Carga total del departamento tipo | **5.390 a 8.690 VA** según equipamiento |
| **Decisión crítica** | **Si hay cocina y calefacción eléctricas, el departamento supera 32 A y exige trifásico** |
| Suma de cargas de 40 viviendas | **218,06 kVA** |
| Servicios generales | **44,20 kVA** |
| **Demanda total del edificio** (con simultaneidad 0,35 en viviendas) | **≈ 110,8 kVA** |
| Corriente de proyecto trifásica | **168,4 A** (210 A de diseño) |
| **Alimentador** | **3 × 150 mm² + N 95 + PE 95, Cu** |
| Caída de tensión del alimentador | 0,34 % ✓ |

---

## 5.9 Protecciones

### 5.9.1 Interruptores diferenciales (770.15.2 / 770.14)

| Regla | Valor |
|---|---|
| **Protección complementaria contra contactos directos** | Interruptor diferencial de **I∆n ≤ 30 mA (alta sensibilidad), de actuación NO retardada ("instantánea")** |
| Reconocimiento normativo | *"El empleo de dispositivos diferenciales con corriente diferencial asignada ≤ 30 mA es reconocido como medida de protección complementaria contra los contactos directos"* |
| Tipo constructivo habitual | **Tipo AC** (actúa con corriente alterna sinusoidal), según IEC 61008. **Para cargas con electrónica de potencia (variadores, cargadores de auto eléctrico, inversores fotovoltaicos) puede requerirse tipo A o B** — ver §5.18 y §5.19 |
| **Contactos indirectos con ID de 30 mA** | Se admite si el valor máximo permanente de la **resistencia de puesta a tierra Ra ≤ 400 Ω** `[verificar el valor exacto en el texto: la norma menciona un límite asociado a ID de 30 mA y otro de 40 Ω asociado a ID de 300 mA]` |
| **Contactos indirectos con ID de 300 mA** | Se admite si **Ra ≤ 40 Ω** |
| Instalaciones donde no se pueda usar ID de 30 mA | Protección por ID **con I∆n ≤ 300 mA**, recomendándose que sean **selectivos** con los de 30 mA |
| Objetivo de la tensión límite de contacto | **≤ 24 V** |
| **Protección del propio ID contra sobrecargas y cortocircuitos** | Obligatoria (770.15.2.2.5). La corriente asignada del ID debe coordinarse con la protección contra cortocircuitos aguas arriba |
| **No se permite** | Prescindir de dispositivos diferenciales como medida de corte automático de la alimentación (770.15) |

> **Criterio de proyecto del estudio (más exigente que el mínimo):**
> - **Un diferencial de 30 mA por cada grupo de 2 a 3 circuitos**, nunca uno solo para toda la vivienda. Motivo: si salta el único diferencial, la vivienda queda a oscuras y sin heladera. Con diferenciales sectorizados, se identifica la falla y se conserva servicio.
> - **Diferencial de 30 mA independiente para: (a) baños y lavadero, (b) cocina, (c) tomacorrientes de estar y dormitorios, (d) iluminación, (e) cada ACU (aire acondicionado).**
> - **Diferencial superinmunizado o tipo A** para el circuito de la heladera/freezer y para el de la caldera: la electrónica genera fugas de alta frecuencia que disparan los diferenciales AC comunes.
> - **En el tablero de servicios generales:** diferencial de 300 mA selectivo aguas arriba + diferenciales de 30 mA por circuito.

### 5.9.2 Interruptores termomagnéticos

| Circuito | Corriente nominal típica | Curva |
|---|---|---|
| IUG (1,5 mm²) | **10 o 16 A** | B o C |
| TUG (2,5 mm²) | **16 o 20 A** | B o C |
| TUE (4 mm²) | **25 A** | C |
| ACU aire acondicionado (2,5 a 4 mm²) | **16 a 20 A** | **C** (soporta el pico de arranque del compresor) |
| Alimentación a motores (bombas) | Según motor | **C o D** + guardamotor con relé térmico |

**Regla de coordinación:** **I_carga ≤ I_nominal_protección ≤ I_admisible_conductor (corregida por agrupamiento y temperatura)**

### 5.9.3 Capacidad de ruptura

La parte 770 aplica a instalaciones con **corriente presunta de cortocircuito en el origen ≤ 10 kA**. Los interruptores del tablero seccional de vivienda deben tener capacidad de ruptura acorde. En edificios, **la Icc en el tablero principal puede superar los 10 kA** y hay que calcularla según **AEA 90865**.

`[VERIFICAR: pedir a la distribuidora la potencia de cortocircuito en el punto de conexión. Sin ese dato no se puede especificar el interruptor general del tablero principal.]`

---

## 5.10 Puesta a tierra y jabalina

### 5.10.1 Esquema de conexión

El esquema exigido es **TT**: neutro de la distribuidora puesto a tierra en su origen, masas de la instalación puestas a **tierra propia e independiente**.

> **Para asegurar el esquema TT, la toma de tierra de protección debe estar alejada de la toma de tierra de servicio más cercana de la distribuidora, a una distancia superior a DIEZ (10) VECES el valor del radio equivalente de la toma de tierra de mayor profundidad** (770.14.4.2).
>
> La toma de tierra de protección **debe ubicarse dentro de los límites del inmueble**.

### 5.10.2 Valor de resistencia

| Regla | Valor |
|---|---|
| **Valor máximo permanente de la resistencia de puesta a tierra de protección** | **≤ 40 Ω**, medida sobre el conjunto de los electrodos específicos (770.3.2 y 770.14.4.1) |

> **Nota:** el valor de 40 Ω está asociado al uso de diferenciales. Muchos proyectistas adoptan **≤ 10 Ω** como criterio de buena práctica, que da un margen razonable ante la variación estacional de la resistividad del suelo.
>
> **Para Santa Rosa:** los suelos pampeanos (loess, con presencia de tosca) pueden tener **resistividad alta y muy variable con la humedad**. En verano seco, una jabalina que medía 15 Ω en invierno puede pasar a 60 Ω. **Medir en la peor condición estacional o aplicar factor de corrección.** Soluciones: múltiples jabalinas en paralelo separadas ≥ su longitud, malla de tierra, o tratamiento del terreno con bentonita/gel conductor (**nunca con sal: acelera la corrosión**). `[verificar resistividad del suelo con medición de campo — método de Wenner]`

### 5.10.3 Electrodos

| Regla |
|---|
| Los electrodos (jabalinas, cintas, placas, cables o alambres) deben ajustarse a las **normas IRAM correspondientes** (jabalina cilíndrica acero-cobre: **IRAM 2309**; ver también IRAM 2310) |
| **Uniones enterradas: soldadura cuproaluminotérmica**, o compresión oval/hexagonal si los componentes tienen la misma sección |
| La conexión entre toma de tierra y cable de PAT se hace en **cámara de inspección** con **tapa removible**, a nivel de piso terminado, en lugar no transitable permanentemente y libre de obstáculos, para permitir inspecciones y mediciones periódicas |
| El conexionado se hace en **barra de cobre electrolítico con puentes removibles**, que permitan desconectar y conectar rápidamente para medir |
| Si la toma de tierra es **un solo electrodo tipo jabalina cilíndrica acero-cobre IRAM 2309**, se puede conectar el cable de PAT con la pieza de bronce o latón denominada **tomacable, conforme a IRAM 2343** |
| **Ingreso del cable de PAT:** se recomienda que ingrese **por el tablero principal** (favorece la protección contra sobretensiones transitorias). Si no es posible, por la caja o tablero más cercano a la toma de tierra |

### 5.10.4 TABLA 770.14.I — Sección del conductor de protección y del cable de PAT

| Sección de los cables de línea (fase) "S" [mm²] | Sección del conductor de protección "S_PE" y del cable de PAT "S_PAT" [mm²] |
|---|---|
| **S ≤ 16** | **S** (igual a la fase) |
| **16 < S ≤ 35** | **16** |
| **S > 35** | **S / 2** |

> **En ningún caso la sección del cable de puesta a tierra será menor que 4 mm².**
>
> El cable de PAT **debe tenderse en forma independiente del conductor de protección** (aun compartiendo la misma canalización) y debe **acometer a la barra o juego de bornes que conforman la barra equipotencial principal**.

### 5.10.5 Conductor de protección (PE) — 770.14.4.5

> El PE debe ser de **cobre electrolítico aislado** conforme a IRAM-NM 247-3, IRAM 2178, IRAM 62266 o IRAM 62267, y **recorre la instalación integralmente, incluyendo aquellas cajas y bocas que NO posean tomacorrientes**, desde la barra principal de tierra. Se exceptúan los circuitos secundarios de MBTS.
>
> El PE **debe ser eléctricamente continuo y no debe ser seccionado en ningún punto** (770.14).
>
> Cables unipolares aislados para PE: sección **no menor a 2,5 mm²**.
>
> **Las masas simultáneamente accesibles pertenecientes a la misma instalación deben conectarse a la misma toma de tierra.**

### 5.10.6 Equipotencialidad

**Barra equipotencial principal (BEP):** debe vincular la toma de tierra con:
- Estructura metálica del edificio (armaduras)
- Cañerías metálicas de agua fría, agua caliente, gas y calefacción **en su ingreso al edificio**
- Bandejas portacables, conductos metálicos
- Pantallas de cables de datos y TV
- Pararrayos, si existe

**Conexión equipotencial suplementaria (CES) en cuartos de baño (AEA 90364-7-701):** vincula entre sí todas las masas y elementos conductores del baño (cañerías, desagües metálicos, marcos metálicos, bañera de acero, etc.). **Sección mínima 2,5 mm² Cu aislado si está protegido mecánicamente, 4 mm² si no.** `[verificar valores en AEA 90364-7-701]`

---

## 5.11 Protección contra sobretensiones (DPS)

**Descargas atmosféricas:** la condición ambiental normal de la Tabla 770.9.I es **AQ2 — exposición indirecta**.

**Cuándo instalar DPS (dispositivo de protección contra sobretensiones):**

| Situación | Recomendación |
|---|---|
| Alimentación por **línea aérea** en zona con alta densidad de descargas atmosféricas | **DPS Tipo 2 obligatorio** en el tablero principal |
| Edificio con **pararrayos** | **DPS Tipo 1** en el origen + **Tipo 2** en tableros seccionales |
| Instalación con equipamiento electrónico sensible (ascensores VVVF, variadores, domótica, servidores, fotovoltaica) | **DPS Tipo 2 + Tipo 3** cerca de la carga |
| Vivienda unifamiliar en zona urbana con alimentación subterránea | Recomendable Tipo 2 |

> **Para La Pampa:** la provincia tiene **actividad convectiva importante en verano**, con tormentas eléctricas frecuentes. **La instalación de DPS Tipo 2 en el tablero principal debería ser estándar del estudio**, no un opcional. El costo es marginal frente al de reponer un ascensor con electrónica quemada. `[verificar el nivel ceráunico / densidad de descargas de Santa Rosa con datos del SMN para justificar el nivel de protección]`

**Reglas de instalación:**
- El DPS se instala **lo más cerca posible del origen de la instalación**, aguas abajo del interruptor general.
- Las conexiones del DPS a fase y a la barra de tierra deben ser **lo más cortas posible: total ≤ 0,50 m**. Una conexión larga anula la protección por la caída inductiva.
- **El DPS debe estar protegido por un fusible o termomagnético** de la corriente que indique el fabricante.
- **El ingreso del cable de PAT por el tablero principal favorece la protección contra sobretensiones transitorias** (770.14.4.4) — otra razón para respetar esa regla.

---

## 5.12 Tableros

### 5.12.1 Jerarquía

```
ACOMETIDA de la distribuidora
        │
        ▼
 MEDIDOR/ES  (sala de medidores)
        │
        ▼
 TABLERO PRINCIPAL (TP)  ── barra equipotencial principal ── PAT
        │
        ├──► TABLERO SECCIONAL de SERVICIOS GENERALES (TSG)
        │         ├─ ascensores (uno por ascensor)
        │         ├─ bombas de agua
        │         ├─ bombas de achique / cloacal
        │         ├─ iluminación de espacios comunes
        │         ├─ portero, CCTV, portón
        │         ├─ extracción de cocheras
        │         └─ bombas de incendio (tablero exclusivo)
        │
        └──► COLUMNAS MONTANTES ──► TABLERO SECCIONAL de cada UNIDAD (TS)
                                          ├─ IUG
                                          ├─ TUG 1, TUG 2
                                          ├─ TUE
                                          └─ ACU
```

### 5.12.2 Definiciones (AEA)

> **Tablero Seccional:** aquel al que acomete la línea seccional y del cual se derivan otras líneas seccionales o de circuito.

### 5.12.3 Requisitos de los tableros

| Requisito |
|---|
| **Grado de protección IP** según ubicación (IEC 60529): interior seco IP41 mínimo; interior húmedo / cocheras IP54; intemperie IP65 |
| **Espacio de reserva**: mínimo 30 % de módulos libres para futuras ampliaciones |
| **Identificación indeleble de cada circuito** (etiqueta con el destino, no solo el número) |
| **Esquema unifilar plastificado dentro del tablero** |
| **Barra de neutro y barra de tierra separadas y rotuladas** |
| **Puerta con cerradura** en tableros de espacios comunes |
| Altura de manipulación del interruptor general: entre **0,80 y 1,80 m** del solado `[verificar valor exacto en AEA]` |
| **Cálculo térmico del tablero** conforme a 770.16 y 770-B.3 |

### 5.12.4 Verificación final de la instalación (770.17 / lista de la guía AEA)

Antes de energizar, verificar:
- Ubicación y destino de los circuitos, secciones de los conductores activos
- Sección del conductor de protección
- Características nominales de los aparatos de maniobra, seccionamiento y protección
- **Caída de tensión**
- Continuidad del conductor de protección **a lo largo de las líneas seccionales** (se mide)
- Resistencia de aislación
- Resistencia de puesta a tierra
- Ensayo de funcionamiento de los diferenciales (botón de prueba **y** medición de corriente y tiempo de disparo)

---

## 5.13 Sala de medidores, alimentador y montantes

### 5.13.1 Sala de medidores

| Aspecto | Criterio |
|---|---|
| **Ubicación** | En **planta baja**, con **acceso directo desde el hall o desde la línea municipal**, para lectura y corte sin ingresar a la propiedad. **Requisito de la distribuidora** |
| **Dimensiones** | Función del número y tipo de medidores. Para 40 unidades + servicios generales + 2 locales: del orden de **4 a 8 m²**. `[verificar dimensiones y disposición exigidas por la distribuidora de Santa Rosa — ES UN DATO QUE SE PIDE ANTES DEL ANTEPROYECTO]` |
| **Separación de gas** | **≥ 0,50 m de todo gabinete de gas** (se reduce a 0,30 m si el gabinete de gas tiene ventilación al exterior). Si el compartimento de medidores de gas comunica con la sala eléctrica: **antecámara de 1 m²** (NAG-200, 3.3.2) |
| **Ventilación** | Natural permanente; los medidores y tableros disipan calor |
| **Iluminación** | Con circuito propio del tablero de servicios generales, con **iluminación de emergencia** |
| **Puesta a tierra** | Barra equipotencial principal ubicada aquí o en el tablero principal |
| **Puerta** | Metálica, con cerradura de la distribuidora, **abriendo hacia afuera** |

### 5.13.2 Columnas montantes

| Regla | Valor |
|---|---|
| **Diámetro mínimo de cañería de columna montante** | **R19 (¾")** — 770.7.3.p |
| Material | Caño de acero semipesado galvanizado, o bandeja portacable en pleno técnico |
| Ubicación | **Pleno técnico registrable desde espacio común**, nunca dentro de unidades |
| **Sectorización contra incendio** | El pleno vertical atraviesa todos los sectores de incendio. **Sellado cortafuego F60/F120 en cada paso de losa** (ver Cap. 7) |
| Cajas de derivación por piso | Registrables, identificadas |
| **Separación de otras instalaciones** | Separar de cañerías de gas y de agua. **Nunca compartir pleno con gas.** Si comparte pleno con agua, la eléctrica va **por encima** |

---

## 5.14 Grupo electrógeno y servicios esenciales

### 5.14.1 ¿Es obligatorio?

En Argentina no hay una exigencia nacional de grupo electrógeno para edificios de vivienda de 10 plantas. **Depende del Código municipal y de las exigencias de incendio.** `[verificar en el Código de Edificación de Santa Rosa y en la normativa de bomberos provincial si se exige fuente de energía de emergencia para PB+9]`

**Casos en que es técnicamente necesario:**

| Servicio | Motivo |
|---|---|
| **Bombas de incendio** | Si la fuente de alimentación no es "segura". El RT de CABA lo aborda en 2.4.5: *"Los motores eléctricos deben tener como mínimo una fuente de alimentación eléctrica segura. Se considera fuente segura a la alimentación directa desde una red pública de suministro confiable."* La alternativa a la segunda fuente eléctrica es la **bomba con motor diésel** |
| **Presurización de escaleras** | Inútil si no funciona en el corte de energía que suele acompañar al incendio |
| **Un ascensor (maniobra de emergencia)** | Para llevar la cabina al piso más cercano y abrir puertas. **Muchos ascensores modernos traen batería propia (UPS) para esta maniobra: verifica el requisito sin grupo electrógeno** |
| **Bomba de agua sanitaria** | Si el edificio es de presurización total sin tanque elevado (§1.9), **sin electricidad no hay agua**. Es un argumento fuerte a favor de conservar tanque elevado |
| **Bomba de achique de subsuelo** | Un corte de energía durante una tormenta inunda el subsuelo |
| **Iluminación de emergencia** | Se resuelve con equipos autónomos (batería propia), **no requiere grupo** |

### 5.14.2 Dimensionado orientativo

Para el edificio del ejemplo, si se optara por grupo electrógeno de servicios esenciales:

| Carga esencial | kVA |
|---|---|
| Bombas de incendio (1 en marcha) | 22,0 |
| Bomba de agua sanitaria (1) | 8,8 |
| Bomba de achique (1) | 1,8 |
| Bomba cloacal (1) | 1,8 |
| 1 ascensor | 7,5 |
| Iluminación de emergencia y espacios comunes esenciales | 3,0 |
| Portero, CCTV | 1,0 |
| **Subtotal** | **45,9 kVA** |
| Factor de simultaneidad (incendio no simultáneo con uso normal) | Se toma el caso más desfavorable |
| **Grupo recomendado** | **50 a 60 kVA**, con arranque automático y transferencia (ATS) |

**Consideraciones de proyecto del grupo:**
- Sala con **ventilación de entrada y salida dimensionada para el radiador**, aislación acústica, y **conducto de escape aislado con salida por encima de la cubierta**.
- **Tanque de combustible diario** con cubeto de contención.
- **Distancias a locales habitables** y control de vibraciones.
- `[verificar exigencias de emisiones sonoras del Código de Santa Rosa y distancias a medianeras]`

---

## 5.15 Canalizaciones

| Tipo | Uso | Observaciones |
|---|---|---|
| **Caño de acero semipesado galvanizado (RS)** | Embutido en losa y mampostería, montantes | El estándar argentino. Diámetros: RS16 (13 mm), RS19 (¾"), RS25 (1"), RS32, RS38 |
| **Caño de acero liviano (RL)** | Embutido en tabiques | RL16, RL19, RL25 |
| **Caño corrugado de PVC (flexible)** | Embutido en tabiques de placa de yeso, en contrapisos | **Verificar su admisión en el reglamento de la distribuidora.** No apto para hormigón estructural sin protección |
| **Bandeja portacable perforada** | Plenos técnicos, subsuelos, cocheras, sala de máquinas | Con separadores para separar potencia de corrientes débiles. **Con PE de continuidad** |
| **Cablecanal (zócalo o pared)** | Reformas, oficinas | Ver §9.6 |
| **Caño rígido de PVC a la vista** | Exteriores, cocheras | Requiere resistencia UV e IK |

**Reglas prácticas:**
- **Coeficiente de ocupación de la cañería:** la suma de las secciones de los conductores (con aislación) **no debe superar el 35 % de la sección interior del caño** para 3 o más conductores. `[verificar valor exacto en AEA 90364 cap. 52 y en 770.10.3.3.4]`
- **Cajas de paso cada 12-15 m** de tramo recto, o cada 3 curvas de 90°.
- **Nunca más de 3 curvas de 90° entre cajas.**
- **Separar potencia de corrientes débiles**: mínimo 20 cm de separación en paralelo, o pantalla metálica puesta a tierra. Cruces a 90°.

---

## 5.16 Iluminación de emergencia y señalización

| Aspecto | Criterio |
|---|---|
| **Dónde** | Medios de escape completos: pasillos, palieres, escaleras (**en cada descanso y en cada tramo**), hall de entrada, sala de máquinas, sala de bombas, sala de medidores, cocheras, salida a vía pública |
| **Tipo** | Equipos **autónomos** con batería (no requieren grupo electrógeno), de encendido automático ante falta de tensión |
| **Autonomía mínima** | **1 hora** `[verificar el valor exigido: 1 h es el mínimo habitual; algunos códigos exigen 1,5 o 3 h]` |
| **Nivel de iluminación en el eje del medio de escape** | **≥ 1 lux** en el suelo, a lo largo del eje `[verificar contra el Código de Santa Rosa e IRAM]` |
| **Señalización de salida** | Carteles fotoluminiscentes o retroiluminados según **IRAM 10005 Parte II** |
| **Alimentación** | Circuito propio desde el tablero de servicios generales, con protección diferencial |
| **Ensayo** | Prueba periódica de autonomía. Los equipos con autotest son recomendables |

---

## 5.17 Corrientes débiles

### 5.17.1 Sistemas a prever en un PB+9

| Sistema | Infraestructura mínima | Observaciones de proyecto |
|---|---|---|
| **Telefonía / Internet (fibra óptica)** | Sala de acometidas (SET) en PB, montante vertical con caja por piso, canalización hasta cada unidad | **Prever al menos 2 prestadores.** Caño Ø 40-50 mm por montante, o bandeja en pleno. Registrable |
| **TV (aérea, cable, satelital)** | Antena/parabólica en cubierta, amplificador en sala técnica, montante con derivadores por piso, **2 tomas de TV por unidad mínimo** | Coaxil RG-6 o RG-11 para troncal. **Prever espacio de mástil y sus vientos en la cubierta, y su vinculación al pararrayos** |
| **Portero eléctrico / visor** | Panel en acceso principal (y en acceso de cocheras), fuente en sala técnica, montante, **teléfono/monitor por unidad** | Los sistemas IP con cableado estructurado son el estándar actual. **Prever apertura de portón peatonal y vehicular desde la unidad** |
| **CCTV** | Cámaras en accesos, hall, palier de PB, cocheras, ascensores, perímetro. **NVR en sala técnica con UPS** | **Cableado UTP Cat 6 con PoE.** Prever espacio y ventilación del rack. **Consultar la normativa de protección de datos personales sobre el registro de imágenes en espacios comunes** |
| **Control de accesos** | Cerradura electromagnética o electromecánica en acceso principal y de cocheras, lectores de proximidad | Debe **liberarse ante alarma de incendio** (interfaz con la central) |
| **Alarma de intrusión** (por unidad, opcional) | Canalización vacía desde el tablero de la unidad hasta puntos de sensor | Dejar previsión, aunque no se instale |
| **Detección de incendio** | Ver Capítulo 7 |
| **Domótica / BMS** (opcional) | Canalización y espacio en tablero | |

### 5.17.2 Reglas de coordinación

| Regla |
|---|
| **Montante de corrientes débiles SEPARADA de la de potencia**, o en la misma bandeja con **separador metálico puesto a tierra** |
| **Separación mínima en paralelo: 20 cm** de cables de potencia. Cruces a 90° |
| **Sala técnica / rack:** local con ventilación, alimentación desde tablero de servicios generales con UPS, puesta a tierra de rack, iluminación. **Superficie mínima recomendada: 2 m²** |
| **Todo pase de losa de la montante de datos: sellado cortafuego** |
| **Cableado estructurado:** categoría mínima **Cat 6 U/UTP**; fibra óptica monomodo para la acometida y para la troncal vertical si el edificio es grande |
| **Documentar el cableado**: etiquetado de ambos extremos, planilla de puertos, plano de canalizaciones |

---

## 5.18 Cargador de vehículo eléctrico (EVSE)

### 5.18.1 Por qué preverlo ahora

Un edificio que se termina en 2027-2028 va a tener vehículos eléctricos entre sus cocheras antes de 2035. **Retrofitear la infraestructura eléctrica de un subsuelo terminado cuesta 5 a 10 veces más que preverla en obra.** Y en propiedad horizontal, la instalación posterior requiere asamblea, lo que puede bloquearla por años.

### 5.18.2 Previsión mínima recomendada (obra nueva)

| Elemento | Especificación |
|---|---|
| **Tablero de cargadores dedicado** en el subsuelo, alimentado desde el tablero principal | Con espacio para al menos **el 50 % de las cocheras** |
| **Alimentador del tablero de cargadores** | Dimensionado para al menos **el 20 % de las cocheras cargando simultáneamente a 7,4 kW** (monofásico 32 A) o con **sistema de gestión dinámica de carga (load balancing)** que limite la demanda total |
| **Bandeja portacable** recorriendo el subsuelo, con derivaciones previstas a cada cochera | Con capacidad de reserva |
| **Caño o bandeja vacía desde cada cochera hasta el tablero de cargadores** | Ø 25 mm mínimo por cochera |
| **Espacio físico** en el tablero principal y en la sala de medidores para el crecimiento de potencia | |
| **Protecciones** | Cada punto de carga: termomagnético + **diferencial Tipo A con detección de corriente continua residual de 6 mA DC, o Tipo B**. **Un diferencial AC común NO protege correctamente un cargador de auto eléctrico** |
| **Medición individual** por punto de carga | Imprescindible para el reparto de expensas |

### 5.18.3 Impacto en la demanda

Un cargador doméstico Modo 3 monofásico de **7,4 kW (32 A)** equivale, él solo, a **la carga total de un departamento de 2 dormitorios completo**. Diez cargadores simultáneos son **74 kVA**, es decir, **dos tercios de la demanda total del edificio del Ejemplo Nº 4**.

> **Conclusión de proyecto:** no se puede simplemente "sumar" cargadores a la demanda calculada. **Hay que usar un sistema de gestión dinámica de carga** que reparta la potencia disponible entre los vehículos conectados, limitando el pico total. Esto es la práctica estándar internacional y hay equipos comerciales disponibles.

`[verificar si la distribuidora de Santa Rosa y/o la Secretaría de Energía tienen normativa específica sobre puntos de carga de vehículos eléctricos en propiedad horizontal]`

---

## 5.19 Generación distribuida fotovoltaica — Ley 27.424

### 5.19.1 Marco

La **Ley 27.424 de "Régimen de Fomento a la Generación Distribuida de Energía Renovable Integrada a la Red Eléctrica Pública"** (2017) y su Decreto reglamentario **986/2018** habilitan al usuario a **generar energía renovable para autoconsumo e inyectar el excedente a la red**, recibiendo un crédito por la energía inyectada.

| Concepto | Definición |
|---|---|
| **Usuario-generador** | Usuario que genera energía para autoconsumo, con eventual inyección de excedentes a la red |
| **Balance neto de facturación** | El excedente inyectado se acredita en la factura |
| **Potencia máxima de la instalación** | Limitada a la **potencia contratada** por el usuario `[verificar el límite exacto vigente y las categorías de usuario-generador]` |
| **Adhesión provincial** | La ley es de adhesión provincial. **VERIFICAR SI LA PROVINCIA DE LA PAMPA ADHIRIÓ Y BAJO QUÉ CONDICIONES**, y cuál es el procedimiento de la distribuidora local |

`[VERIFICAR: (a) adhesión de La Pampa a la Ley 27.424; (b) reglamentación provincial; (c) procedimiento de solicitud, medidor bidireccional y requisitos técnicos de la distribuidora de Santa Rosa; (d) límites de potencia por categoría de usuario. Consultar en argentina.gob.ar/energia/generacion-distribuida]`

### 5.19.2 Previsión constructiva en un PB+9

Aun sin instalar los paneles, la obra nueva debería prever:

| Previsión | Detalle |
|---|---|
| **Superficie de cubierta libre y orientada** | En Santa Rosa (lat. −36,57°), orientación **norte** con inclinación óptima anual ≈ **32-36°** (≈ latitud). **Reservar la superficie de cubierta norte, sin sombras de tanques, salas de máquinas ni antenas** |
| **Sobrecarga estructural** | Un sistema FV con estructura sobre cubierta plana pesa del orden de **15 a 25 kg/m²**, más el lastre si es sin perforación. **Informarlo al calculista en la etapa de estructura** |
| **Canalización vertical desde cubierta hasta la sala de medidores** | Caño o bandeja de **Ø 50 mm mínimo**, vacía y registrable |
| **Espacio en sala de medidores** para inversor(es), protecciones DC y AC, y el **medidor bidireccional** | Del orden de **1 a 2 m² de paramento** |
| **Puesta a tierra** | Estructura de soporte y marcos de módulos vinculados a la PAT del edificio |
| **Protecciones específicas** | DPS del lado DC y del lado AC; interruptor DC; protección diferencial **Tipo B** o **Tipo A con detección DC** aguas abajo del inversor `[verificar según tipo de inversor: los inversores con transformador de aislación pueden admitir Tipo A]` |
| **Vía de acceso segura a la cubierta** para mantenimiento, con línea de vida | |

### 5.19.3 Potencial en Santa Rosa

De **IRAM 11603**, estación Santa Rosa (Aero):
- **Heliofanía relativa: 4,8 (invierno) / 9,0 (verano)** `[la unidad de este campo debe verificarse contra la definición de la norma: heliofanía relativa suele expresarse en % o en horas de sol]`
- Latitud −36,57°

> Con esos valores, **La Pampa tiene un recurso solar bueno**, comparable al de la región centro. **La irradiación global anual sobre plano inclinado óptimo se ubica del orden de 1.800 a 2.000 kWh/m²·año.** `[VERIFICAR con datos de irradiación del atlas solar de la Secretaría de Energía o del SMN para Santa Rosa antes de dimensionar cualquier sistema]`

---
