# Investigación: por qué el buscador está hecho así

Este documento registra lo que se verificó antes de escribir el código, y por
qué cada decisión de diseño es la que es. Fecha de corte: **31 de agosto de
2026**. Todo lo que dice "vigente" hay que revalidarlo: la mitad de estas
reglas cambió durante 2026.

---

## 1. Qué API de vuelos se puede usar hoy

### Amadeus Self-Service está muerto

Es el hallazgo que invalida la mayoría de los tutoriales que circulan. El
portal se decomisionó el **17 de julio de 2026** y las API keys dejaron de
funcionar.

Verificado en este entorno:

```
test.api.amadeus.com          SIN DNS -> [Errno -5] No address associated with hostname
api.amadeus.com               SIN DNS -> [Errno -5] No address associated with hostname
developers.amadeus.com        DNS ok
serpapi.com                   DNS ok
api.travelpayouts.com         DNS ok
```

Los hosts de la API no resuelven, mientras que otros proveedores responden
`401` con normalidad desde la misma red — así que no es un bloqueo del
entorno. Además `developers.amadeus.com/self-service` redirige a la raíz: la
sección ya no existe. La alternativa oficial (Amadeus Quick Connect) requiere
acuerdo comercial y credencial IATA; no es accesible para un individuo.

### Comparación de lo que sí está vivo

| API | Free real | Tarjeta | Calendario | Flybondi | JetSmart | ARS nativo | Estado |
|---|---|---|---|---|---|---|---|
| **SerpApi Google Flights** | 250/mes | No | ✅ | ✅ | ✅ | ✅ | Vivo |
| **Travelpayouts** | sin tope de requests | No | ✅ | ⚠️ | ⚠️ | ✅ | Vivo |
| RapidAPI Sky-Scrapper | ~100/mes | No | ❌ | ✅ | ✅ | ✅ | Vivo (no oficial) |
| Duffel | sandbox falso | No | ❌ | ❌ | ❌ | ❌ | Vivo |
| FlightAPI.io | 20-100 | No | ❌ | ⚠️ | ⚠️ | ✅ | Vivo |
| Amadeus Self-Service | — | — | — | — | — | — | **Muerto 17/07/2026** |
| Kiwi Tequila | — | — | ✅ | ✅ | ✅ | ✅ | Sólo por invitación desde 2024 |
| Skyscanner oficial / Kayak | — | — | ✅ | ✅ | ✅ | ✅ | Detrás de revisión comercial |

### Por qué SerpApi como primario

**El argumento decisivo es la cobertura, no el precio ni la comodidad.**
Flybondi y JetSmart no publican en ningún GDS. Duffel, que es la API mejor
diseñada de la lista, no tiene ninguna de las dos en su roster de aerolíneas.
Para AEP–BRC, AEP–SLA o EZE–IGR eso significa **perderse sistemáticamente las
tarifas más baratas**: no es una limitación menor, es dar una respuesta
equivocada.

Google Flights sí las lista, con precios nativos en pesos (`currency=ARS`,
`gl=ar`). Además devuelve `price_insights` con `lowest_price`, `price_level`
y `typical_price_range`, que es lo que permite decir "está barato para esta
ruta" en vez de tirar un número sin contexto.

Contra: 250 búsquedas gratis por mes son unas 8 por día. Un agente
conversacional las quema en una tarde. **La caché y el barrido barato no son
optimizaciones, son requisitos.**

### Por qué Travelpayouts como secundario

Sus precios son caché de búsquedas de otros usuarios, de hasta una semana de
antigüedad, y para rutas de cabotaje argentino el caché suele venir muy fino
(casi nadie busca AEP–BRC desde Aviasales). No sirve para cotizar.

Sirve para otra cosa: `/v1/prices/calendar` devuelve un mes entero de precios
mínimos en una sola llamada y no cobra por request. Con eso se eligen las
fechas candidatas y se gastan los créditos caros sólo ahí. Por eso sus
ofertas salen marcadas `indicativo=True` y nunca se muestran como firmes.

### Descartadas

- **Duffel**: sin las low-cost argentinas, sin calendario de fechas, y su
  modelo de precios (ratio 1500:1 de búsquedas por reserva) castiga
  exactamente a un agente que busca mucho y reserva poco.
- **Kiwi Tequila**: cerrado a nuevos desarrolladores desde mayo de 2024. La
  pérdida real es su *virtual interlining*, que era lo mejor para combinar
  Flybondi o JetSmart con largo radio. No hay reemplazo equivalente.
- **FlightAPI.io**: la API key va en el path de la URL (se filtra en logs y
  en el header `Referer`), no tiene calendario, y su propia documentación se
  contradice sobre el tamaño del free tier.

---

## 2. Comprar pasajes desde Argentina

### Impuestos y percepciones

| Concepto | Alícuota | Alcance | ¿Se evita? |
|---|---|---|---|
| Impuesto PAÍS | **0%** | — | Derogado el 23/12/2024 |
| Percepción RG 5617/2024 | **30%** | pasajes al exterior pagados en pesos | **Sí, pagando en dólares.** Y es recuperable. |
| Impuesto DNT (código IATA `AR`) | **7%** | pasajes al exterior | No. Vigente hasta el 31/12/2027 |
| Tasa aeroestación `XR` | USD 57 | por pasajero, EZE/AEP | No |
| Tasa seguridad `TQ` | USD 9 | por pasajero | No (subió de 8 el 28/05/2026) |
| Cabotaje | IVA 10,5% + IIBB | — | No |

**La percepción del 30% es lo único grande que se puede evitar**, y no
aparece en ningún buscador porque es un cargo del medio de pago: sale en el
resumen de la tarjeta como `DB.RG 5617 30%`.

Formas de pagar en dólares y esquivarla: homebanking o DEBIN desde caja de
ahorro en USD, débito con "pagar en dólares" habilitado, dólar MEP más *stop
debit*, o efectivo por ventanilla.

Si igual se paga en pesos, la percepción es **a cuenta** de Ganancias y
Bienes Personales: se recupera vía ARCA (no inscriptos, mes a mes) o SIRADIG
(asalariados, hasta el 31 de marzo). Demora típica: 3 a 6 meses.

Esto se verificó de forma independiente contra el tipo de cambio del día:

```
dólar oficial: $1.530    dólar tarjeta: $1.989    →  recargo 30,0%
```

El dólar tarjeta **es** el oficial más la percepción. Por eso, cuando un
precio viene en dólares y se convierte a pesos con el tipo de cambio tarjeta,
la percepción ya está adentro y no hay que sumarla otra vez — un error fácil
de cometer que duplicaría el cargo.

> ⚠️ **Desinformación detectada.** En diciembre de 2025 circuló ampliamente
> la noticia de que ARCA eliminaba el 30% desde enero de 2026. Es una
> **inocentada del 28/12/2025**; el artículo original lleva el aviso de que
> el contenido es ficticio, pero varios medios lo replicaron como real. El
> 30% sigue vigente.

### Cuotas

- **Internacional: prohibido financiar en cuotas** por normativa del BCRA
  desde 2021. (Despegar lanzó un esquema propio de hasta 3 cuotas en dólares
  donde el financiamiento lo da la empresa, esquivando la restricción.)
- **Cabotaje: sí hay.** Cuota Simple (3 y 6 cuotas), Banco Nación hasta 12 sin
  interés en vuelos de Aerolíneas, Galicia hasta 12, Santander hasta 6.

### Equipaje: la regla de negocio más importante

Ninguna comparación de precios base es válida sin normalizar equipaje.

| Aerolínea | Incluido en la tarifa base | Carry-on | Bodega |
|---|---|---|---|
| **Flybondi** | 1 bulto 30×40×20, 6 kg | $14.149 | $10.399 (12 kg) |
| **JetSmart** | bolso 45×35×25, 10 kg | $9.990 | $12.590 (23 kg) |
| **Aerolíneas Base** | personal 3 kg + **carry-on 8 kg** | incluido | $42.350 |

Precios por tramo, al comprar junto con el pasaje. **Comprarlo en la puerta
de embarque cuesta entre 2,1 y 2,4 veces más.**

Aerolíneas eliminó el carry-on de la tarifa Base en mayo de 2026 y **lo
repuso en junio** tras el rechazo de los pasajeros; la tarifa Promo se
eliminó definitivamente. JetSmart cambió sus familias tarifarias en marzo de
2026 y desde enero controla el equipaje de mano por volumen total en el
medidor, no por cantidad de bultos.

El resultado no favorece a nadie de forma fija: con carry-on gana Aerolíneas,
con valija despachada vuelve a ganar Flybondi (porque Aerolíneas cobra la
bodega cuatro veces más). Hay que calcularlo caso por caso.

### Santa Rosa, La Pampa

Santa Rosa **sí** tiene aeropuerto (**RSA**, ICAO SAZR, pista de 2.300 m),
pero con **una sola ruta comercial**: RSA↔AEP con Aerolíneas Argentinas,
unas 4 frecuencias semanales. Sin competencia, casi nunca va a tener la
tarifa más barata.

| Aeropuerto | IATA | Distancia por ruta | Tiempo | Peajes |
|---|---|---|---|---|
| Santa Rosa | RSA | — | — | — |
| Bahía Blanca | BHI | **345 km** | 4 h 19 | sin peajes |
| Neuquén | NQN | **542 km** | 6 h 44 | sin peajes |
| Buenos Aires | AEP / EZE | **600 km** | 7 h 24 | ~$24.311 |

BHI y NQN tienen competencia low-cost que en RSA no existe: Flybondi opera
BHI–NQN y conexiones desde ambos a Córdoba, Rosario, Salta, Tucumán, El
Calafate, Iguazú, Mendoza, Bariloche y Ushuaia.

Estos números están en `buscador/aeropuertos.py` y el costo del traslado
(nafta, peajes y el tiempo al volante) se descuenta del ahorro antes de
comparar. Manejar de noche por la RN 35 o la RN 152 está desaconsejado por el
estado del asfalto y los animales sueltos.

> Skyscanner reporta "24 vuelos semanales AEP–RSA con GOL, LATAM y
> Aerolíneas". Es un artefacto de códigos compartidos: sólo AR opera RSA.

### Cuándo comprar

| Tipo de vuelo | Ventana óptima | Temporada alta |
|---|---|---|
| Cabotaje | 30–45 días antes | 60–90 días |
| Regional | 1–3 meses | — |
| Larga distancia | 3–6 meses | 5–6 meses |

Comprar con **mucha** antelación (6+ meses) sale peor, no mejor: es
contraintuitivo pero está medido. Según el informe Air Hacks 2026 de Expedia,
comprar 15–30 días antes en doméstico ahorra unos USD 130 contra hacerlo con
6 meses de anticipación.

- **Temporada baja en Argentina:** abril y mayo (los meses más baratos),
  agosto y la segunda quincena de marzo.
- **Temporada alta:** diciembre a febrero, julio y Semana Santa (+30% a +50%).
- **Días:** Expedia mide el viernes como el más barato para volar y comprar;
  las fuentes argentinas siguen señalando martes y miércoles. **Hay
  contradicción entre la data global y la práctica local**, así que no se
  hardcodeó ninguna de las dos.
- **Próximos eventos de descuentos:** Cyber Monday 2–4 de noviembre de 2026,
  Black Friday el 27 de noviembre.

---

## 3. Cómo se decide "el mejor"

### Qué hacen los grandes

Ninguno publica su fórmula. Google Flights dice que rankea por "el mejor
equilibrio entre precio y comodidad" y nombra tres factores: **duración,
cantidad de escalas y cambios de aeropuerto en las conexiones**. Skyscanner
es más explícito: usa un **modelo entrenado**, no una fórmula fija, sobre
precio, duración total, horario de salida, aerolínea, escalas, aeropuertos y
composición del grupo — por eso el orden varía entre búsquedas parecidas.

El paper de ingeniería de Skyscanner aporta el dato más útil y más sobrio:
**el baseline de "ordenar por precio" es durísimo de superar.** Su modelo le
ganó a una heurística de precio más duración, pero por márgenes modestos.

La lectura estratégica: los tres usan modelos entrenados sobre datos de
conversión que acá no existen. Sin ese dataset, un modelo de machine learning
no le gana a una fórmula económica bien parametrizada — y la fórmula además
es auditable y se le puede explicar al usuario.

### Por qué costo generalizado y no un puntaje normalizado

El enfoque clásico normaliza cada criterio (min-max, z-score, TOPSIS) y los
suma con pesos. Tiene dos defectos que lo descalifican para un buscador:

1. **El puntaje depende del conjunto de candidatos.** Si aparece una opción
   absurda de 40 horas, el min-max se estira y *todos* los puntajes cambian
   aunque los vuelos sean los mismos. Eso rompe la caché, la comparación
   entre fechas, las alertas de precio y la confianza del usuario.
2. **Los pesos no significan nada.** `w_duración = 0,3` no se puede
   justificar, calibrar ni explicar.

El **costo generalizado** convierte todo a dinero, que es lo que hace la
economía del transporte desde hace cincuenta años y lo que hacen
implícitamente los modelos logit de elección de itinerario: estiman un
coeficiente de tarifa y dividen todos los demás por él para obtener
disposición a pagar.

Es absoluto (no depende del conjunto), tiene unidades interpretables
("evitar una escala vale $25.000" es discutible y calibrable) y se explica
solo mostrando el desglose.

Hay un test que verifica la propiedad clave: agregar una opción absurda a la
lista **no cambia el orden de las demás**.

### La fórmula

```
costo = precio efectivo
      + valor_hora × (1,0 × tiempo de vuelo + 1,5 × tiempo de escala
                      + 1,3 × tiempo de traslado terrestre)
      + Σᵢ max(piso, 8% del precio de la ruta) × 1,6ⁱ
      + Σ P(perder la conexión) × costo de perderla
      + penalización por espera larga y por noche en aeropuerto
      + penalización por horario de salida y de llegada
      + penalización por cambio de aeropuerto
      + penalización por tramos separados
```

Decisiones que importan:

- **El tiempo de escala pesa 1,5 veces el de vuelo** (y el terrestre, 1,3).
  En economía del transporte el tiempo de transferencia se valora entre 1,5 y
  2,5 veces el tiempo en vehículo. Esto ya captura buena parte de la molestia
  de una escala, y distingue correctamente "una escala de 1 hora" de "una
  escala de 6".

- **La penalización por escala es 8% del precio de la ruta, no 20%.** El
  sobreprecio de mercado del vuelo directo es 10–20% en corto radio y 20–30%
  en largo. La mitad de eso ya lo está cobrando el término de tiempo. Poner
  el 20% completo sería **contar dos veces**, que es el error más común en
  estas fórmulas.

- **Crece 1,6× por escala.** La segunda escala es peor que la primera: dos
  chances de perder el equipaje, dos de perder la conexión, y el cansancio no
  es lineal.

- **El riesgo de conexión se mide contra el MCT real del aeropuerto.** IATA
  administra los tiempos mínimos de conexión (Resolución PSC 765) para más de
  400 aeropuertos. `P(perder) = 0,30 × exp(−colchón / 45)`, que da 15% con
  30 minutos de colchón, 8% con 60 y 4% con 90. Los valores por aeropuerto
  están en `MCT_POR_AEROPUERTO`.

- **Lo que cuesta perder la conexión depende de quién se hace cargo.** Con un
  billete único la aerolínea reacomoda y se pierden unas horas. Con tramos
  separados hay que comprar un pasaje nuevo de último momento, pagar hotel y
  perder un día: no hay a quién reclamarle. Además, al self-transfer se le
  suman 45 minutos al mínimo de conexión, porque hay que retirar el equipaje,
  volver a despacharlo y pasar seguridad de nuevo.

- **Valor del tiempo calibrado a Argentina.** La guía del US DOT usa 1,9
  veces el ingreso horario mediano del hogar para viaje aéreo personal, y los
  estudios de aviación reportan entre USD 75 y 153 la hora. Esos números
  salen de países de ingreso alto: aplicados tal cual acá, el vuelo directo
  caro gana siempre y el buscador deja de servir. Los perfiles
  (`mochilero` 3, `ocio` 7, `comodo` 16, `trabajo` 38 dólares la hora) están
  reescalados al ingreso mediano argentino.

### El contexto de precio va aparte del ranking

Saber si un precio es históricamente bueno es útil, pero **no puede entrar en
el orden**: el precio ya pesa dentro del costo generalizado, y bonificar
además por "es una buena oferta" lo contaría dos veces.

Por eso `evaluar_precio()` devuelve una etiqueta (`excelente`, `bueno`,
`tipico`, `caro`) que se muestra y sirve para disparar alertas, pero no se
usa para ordenar. Es lo mismo que hace Google Flights con su
`price_level: low/typical/high`.

### Presupuesto de consultas

Una búsqueda con ±3 días en cada punta son 49 combinaciones; con aeropuertos
alternativos, hasta 294. Inviable contra una cuota de 250 por mes.

La solución es una cascada:

1. **Barrido barato** (0–2 requests): el calendario de Travelpayouts devuelve
   un mes entero y no cobra por request.
2. **Refinamiento** (3–5 requests): sólo las mejores fechas del paso anterior
   se cotizan con el proveedor caro.
3. **Aeropuertos alternativos** (condicional): sólo si el mejor precio del par
   principal no fue bueno. Si ya conseguiste un precio bueno, no gastes cuota
   buscando marginalmente mejor.

Presupuesto de referencia: fecha fija 1 request, ±3 días unos 5, mes entero
unos 7, peor caso con guardas ≤ 20.

Además, la fecha que pidió el usuario **siempre** se consulta aunque el
barrido la descarte: puede tener un motivo para viajar ese día.

---

## Fuentes

**APIs**
- [Amadeus to shut down self-service APIs portal — PhocusWire](https://www.phocuswire.com/amadeus-shut-down-self-service-apis-portal-developers)
- [SerpApi — Google Flights API](https://serpapi.com/google-flights-api)
- [SerpApi — monedas soportadas](https://serpapi.com/google-travel-currencies)
- [Travelpayouts Data API](https://travelpayouts-data-api.readthedocs.io/en/latest/)
- [Duffel — Airlines](https://duffel.com/airlines)
- [Kiwi.com — nuevo enfoque de partnerships](https://media.kiwi.com/articles-and-interviews/better-for-business-kiwi-com-takes-a-new-approach-to-partnerships/)

**Impuestos y pagos**
- [Impuesto sobre pasajes aéreos al exterior — Argentina.gob.ar](https://www.argentina.gob.ar/turismoydeportes/fondo-nacional-de-turismo/impuesto-sobre-pasajes-aereos-al-exterior)
- [Prórroga del impuesto del 7% hasta 2027 — La Nación](https://www.lanacion.com.ar/economia/el-gobierno-prorrogo-hasta-2027-el-impuesto-para-los-pasajes-al-exterior-nid06012025/)
- [RG 5672/2025 sobre percepciones — ARCA](https://servicioscf.afip.gob.ar/publico/sitio/contenido/novedad/ver.aspx?id=4768)
- [El recargo del 30% sigue vigente — Diario Jornada](https://www.diariojornada.com.ar/408822/economia/ningun_chau_al_dolar_tarjeta_el_recargo_del_30_sigue_vigente)
- [Devolución del 30% — Infobae](https://www.infobae.com/economia/2026/01/12/quienes-pueden-pedir-la-devolucion-del-30-de-impuestos-por-gastos-en-el-exterior-y-como-hay-que-hacer-el-tramite/)
- [Suben las tasas aeroportuarias (mayo 2026) — Infobae](https://www.infobae.com/economia/2026/05/27/suben-las-tasas-en-los-aeropuertos-cuanto-aumentaran-los-pasajes-de-avion-en-la-argentina/)

**Equipaje y aerolíneas**
- [Costos del equipaje en las aerolíneas de Argentina — Aviacionline](https://www.aviacionline.com/los-costos-del-equipaje-en-las-aerolineas-de-argentina)
- [Aerolíneas repuso el carry-on en la tarifa Base (junio 2026) — Cholila Online](https://cholilaonline.ar/2026/06/aerolineas-argentinas-reacomodo-tarifas-carries-on-base.html)
- [Opcionales y precios Argentina — JetSMART](https://jetsmart.com/ar/es/opcionales)
- [Equipaje adicional — Flybondi](https://flybondi.com/ar/equipajeadicional)

**Aeropuertos y rutas**
- [Santa Rosa Airport — Wikipedia](https://en.wikipedia.org/wiki/Santa_Rosa_Airport_(Argentina))
- [Rutas y distancias — Ruta0](https://www.ruta0.com/)
- [Flybondi en Bahía Blanca — Política y Medios](https://politicaymedios.com.ar/nota/11628/flybondi-se-asienta-en-bahia-blanca-y-ocupa-rutas-de-aerolineas/)

**Ranking**
- [Cómo encontrar las mejores tarifas — Google Travel Help](https://support.google.com/travel/answer/7664728)
- [Cómo determina Skyscanner el mejor itinerario](https://skyscannerpartnersupport.zendesk.com/hc/en-us/articles/360002917673-How-does-Skyscanner-determine-the-best-itinerary-order)
- [Learning to rank for flight itinerary search — Skyscanner Engineering](https://nlathia.github.io/2017/09/Learning-to-rank-flights.html)
- [Modeling the Competition among Air Travel Itinerary Shares — Coldren & Koppelman](https://archiv.ivt.ethz.ch/news/archive/20030810_IATBR/coldren.pdf)
- [Revised Departmental Guidance on Valuation of Travel Time — US DOT](https://www.transportation.gov/sites/dot.gov/files/docs/2016%20Revised%20Value%20of%20Travel%20Time%20Guidance.pdf)
- [Station Standard Minimum Connecting Time — IATA](https://www.iata.org/en/publications/manuals/station-standard-minimum-connecting-time-mct/)
- [Non-stop versus connecting air services — MIT ICAT](https://dspace.mit.edu/bitstream/handle/1721.1/121459/ICAT-2019-3_Florian.pdf)
- [Expedia 2026 Air Hacks](https://www.expedia.com/newsroom/expedia-2026-air-hacks/)
