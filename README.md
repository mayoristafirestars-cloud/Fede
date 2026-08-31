# Buscador de pasajes aéreos

Agente que busca vuelos y los ordena por **lo que realmente te cuestan**, no
por el precio que muestra el buscador.

Está pensado para comprar desde Argentina, que es un caso particular: la
carga impositiva más pesada no está en el ticket sino en el medio de pago, y
la aerolínea más barata de la lista suele dejar de serlo apenas llevás una
valija.

```
$479.300  · WJ  100/100  ★ MEJOR OPCIÓN
    IDA    AEP→BRC  15/10 07:50 → 10:10  2h 20m  ·  directo
    VUELTA BRC→AEP  22/10 21:40 → 00:00 +1d  2h 20m  ·  directo
    carry-on ✗, sin bodega  ·  ¡quedan 1!
    equipaje: $19.980
    ✈ sin escalas 🎒 sin carry-on incluido
```

---

## Las tres cosas que hace y ningún metabuscador hace

### 1. Te dice lo que vas a pagar, no lo que dice la vidriera

Un pasaje al exterior comprado en pesos con tarjeta lleva la **percepción del
30% (RG 5617/2024)**, que no aparece en ningún buscador porque es un cargo
del medio de pago: se ve recién en el resumen de la tarjeta, como
`DB.RG 5617 30%`.

**Pagando en dólares se evita.** Sobre un pasaje de USD 800 son unos
$360.000 de diferencia — más de lo que se gana cambiando de fecha, de
aerolínea o de aeropuerto. La herramienta lo calcula y lo dice con el número
puesto.

Y si igual pagás en pesos, te recuerda que la percepción es *a cuenta* de
Ganancias y Bienes Personales: se recupera vía ARCA o SIRADIG.

> El impuesto PAÍS está derogado desde el 23/12/2024 y **no** se suma.
> Cualquier calculadora que lo siga cobrando está desactualizada.

### 2. Compara viajes, no precios pelados

La tarifa base de **Flybondi** incluye un solo bulto de 6 kg; el carry-on
sale $14.149 por tramo. La de **JetSmart** incluye un bolso de 10 kg bajo el
asiento; el carry-on, $9.990. La tarifa **Base de Aerolíneas** incluye
carry-on de 8 kg (lo sacó en mayo de 2026 y lo repuso en junio).

Comparar los precios de vidriera favorece sistemáticamente a las low-cost. El
buscador normaliza el equipaje antes de comparar, y el resultado no es
siempre el que uno espera:

| Escenario (ida y vuelta) | Flybondi | Aerolíneas | Gana |
|---|---|---|---|
| Sin equipaje | $180.000 | $205.000 | Flybondi |
| Con carry-on | $208.298 | $205.000 | **Aerolíneas** |
| Con carry-on y una valija | $229.096 | $289.700 | Flybondi |

No hay una regla fija a favor de nadie: hay que calcularlo caso por caso, que
es exactamente lo que hace la herramienta.

### 3. Le pone precio al itinerario

Una escala de siete horas, una conexión de 40 minutos que se pierde una de
cada tres veces o una salida a las 3 de la mañana tienen un costo real. El
buscador lo convierte a pesos y lo suma al precio, así que el orden final
responde a *cuánto te sale el viaje*, no a *cuánto sale el ticket*.

Por eso el más barato puede aparecer quinto — y cuando pasa, la salida dice
por qué.

---

## Instalación

```bash
git clone <este-repo> && cd Fede
pip install -r requirements.txt
cp .env.example .env      # opcional: ver "Proveedores"
```

Requiere Python 3.11 o superior. El núcleo corre con la librería estándar;
la única dependencia es `requests`.

## Uso

```bash
python -m buscador ORIGEN DESTINO --ida FECHA [--vuelta FECHA] [opciones]
```

Origen y destino aceptan código IATA (`BRC`) o nombre de ciudad
(`bariloche`, `cordoba`, `buenos aires`). Las fechas aceptan `15/10`,
`2026-10-15`, `+45d`, `hoy` y `mañana`.

```bash
# Cabotaje, ida y vuelta
python -m buscador AEP BRC --ida 15/10 --vuelta 22/10

# Desde Santa Rosa, mirando también Bahía Blanca y Neuquén,
# con tres días de flexibilidad
python -m buscador RSA MDZ --ida 10/11 --vuelta 20/11 --flex 3 --cerca 600

# A Europa, pagando en dólares
python -m buscador EZE MAD --ida +90d --vuelta +104d --pago dolares

# Familia con dos valijas, sólo directos
python -m buscador AEP IGR --ida 20/12 --vuelta 27/12 \
    --adultos 2 --ninos 2 --bodega 2 --directo

# Para procesar el resultado en otro lado
python -m buscador AEP USH --ida +60d --json
```

`python -m buscador --help` lista todo.

### Las opciones que más mueven el resultado

| Opción | Qué hace |
|---|---|
| `--flex N` | Prueba N días antes y después de cada fecha. |
| `--cerca KM` | Suma aeropuertos alternativos hasta KM **por ruta**, y descuenta lo que cuesta manejar hasta ahí (nafta, peajes y tu tiempo). |
| `--perfil` | Cuánto vale tu tiempo: `mochilero`, `ocio` (default), `comodo`, `trabajo`, `solo-precio`. |
| `--pago dolares` | Calcula el precio sin la percepción del 30%. |
| `--bodega N` | Cuántas valijas despachás. Cambia radicalmente la comparación. |
| `--sin-carry-on` | Viajás sólo con mochila chica. |

### Desde Claude Code

El repo trae una skill (`.claude/skills/buscar-pasajes/`). Alcanza con pedirlo
en castellano:

> *buscame pasajes a Bariloche para la primera quincena de octubre, somos dos
> y llevamos una valija*

## Proveedores

Se usan todos los que encuentre configurados en `.env`, y se combinan los
resultados.

| Proveedor | Rol | Cuota gratis | Para qué |
|---|---|---|---|
| **SerpApi** (`google_flights`) | primario | 250/mes, sin tarjeta | Es el único de acceso abierto que ve **Flybondi y JetSmart**, que no publican en ningún GDS. Sin ellas, cualquier búsqueda de cabotaje argentino da una respuesta equivocada. Precios nativos en pesos. |
| **Travelpayouts** | secundario | sin límite de requests | Devuelve un mes entero de precios mínimos en una sola llamada y no cobra por request. Se usa para **elegir qué fechas cotizar**, no para cotizar: sus precios son caché y salen marcados como indicativos. |
| **demo** | red de seguridad | — | Datos sintéticos deterministas. Sirve para probar el flujo **sin decidir una compra**. |

Sin ninguna credencial, la herramienta funciona en modo demo y lo avisa.

> **Amadeus Self-Service ya no existe.** El portal se decomisionó el
> 17/07/2026 y sus hosts de API ya no resuelven por DNS. Si encontrás un
> tutorial que arranca con `test.api.amadeus.com`, está desactualizado.

### Presupuesto de consultas

Una búsqueda con ±3 días en cada punta son 49 combinaciones. A un crédito
cada una, se funde la cuota gratuita del mes en una sola consulta.

La búsqueda se hace en dos fases: primero un **barrido gratis** del
calendario para saber qué fechas valen la pena, y recién después la búsqueda
cara sólo sobre esas. Baja de 49 requests a unos 5. El tope se controla con
`--presupuesto`.

## Cómo se decide "el mejor"

Todo lo que molesta de un itinerario se convierte a plata y se suma al
precio. Es el **costo generalizado** de la economía del transporte:

```
costo = precio + equipaje faltante + percepción
      + valor de tu hora × (tiempo de vuelo + 1,5 × tiempo de escala)
      + costo por escala          (8% del precio de la ruta, creciente)
      + P(perder la conexión) × lo que cuesta perderla
      + penalización por espera larga, salida de madrugada,
        cambio de aeropuerto, tramos separados
      + traslado terrestre a un aeropuerto alternativo
```

Los parámetros salen de la literatura de elección de itinerarios aéreos
(modelos logit, guía de valor del tiempo del US DOT, tiempos mínimos de
conexión de IATA), reescalados a ingresos argentinos.

**Por qué así y no un puntaje de 0 a 100:** un puntaje normalizado depende
del conjunto de opciones. Si mañana aparece un vuelo absurdo de 40 horas,
todos los puntajes cambian aunque los vuelos sean los mismos — y eso rompe la
caché, la comparación entre fechas y las alertas de precio. El costo
generalizado es absoluto: no se mueve porque aparezca o desaparezca otra
opción. Hay un test que verifica exactamente eso.

Además tiene unidades. "Evitar una escala vale $25.000" se puede discutir y
calibrar; "el peso de la duración es 0,3" no significa nada.

El puntaje de 0 a 100 que se muestra se **deriva** del costo generalizado.
Nunca se usa para ordenar.

## Estructura

```
buscador/
  modelos.py        Oferta, Itinerario, Segmento, Consulta: el lenguaje común
  busqueda.py       orquestador: qué consultar, en qué orden, con qué presupuesto
  ranking.py        costo generalizado, perfiles de viajero, contexto de precio
  precios_ar.py     percepción del 30%, tipo de cambio, costo real en pesos
  equipaje_ar.py    qué incluye cada tarifa base y qué cuesta igualarlas
  aeropuertos.py    catálogo IATA, distancias, aeropuertos alternativos por ruta
  reporte.py        salida a consola, Markdown y JSON
  cli.py            línea de comandos
  proveedores/
    base.py         el contrato: agregar una fuente es escribir una clase
    serpapi.py      Google Flights vía SerpApi
    travelpayouts.py  barrido de calendario
    demo.py         datos sintéticos para probar sin cuota
docs/investigacion.md   por qué cada decisión, con fuentes
```

## Tests

```bash
python -m pytest tests/ -q
```

203 tests. Los de proveedores corren contra respuestas reales de cada API; los
de la CLI, de punta a punta contra el proveedor demo: sin red, sin
credenciales y sin consumir cuota.

## Advertencias

- **El precio se confirma recién en el checkout de la aerolínea.** Acá se
  estima, con la mejor información disponible.
- Los importes de equipaje son de agosto de 2026 y cambian seguido:
  Aerolíneas modificó su política dos veces sólo en 2026.
- Flybondi y JetSmart venden fuerte por canal directo. Ninguna API ve el 100%
  de su inventario ni sus promos relámpago.
- Comprar desde una IP extranjera para esquivar impuestos no funciona: varias
  aerolíneas bloquean las clases más baratas para compradores del exterior, y
  el impuesto DNT del 7% alcanza igual a los residentes argentinos.
