---
name: buscar-pasajes
description: Busca pasajes aéreos y los ordena por lo que realmente cuestan en Argentina, no por el precio de vidriera. Usar cuando se pidan vuelos, pasajes, aéreos, tarifas o precios de avión; cuando se pregunte cuándo conviene comprar o volar; cuando haya que comparar aerolíneas, fechas o aeropuertos alternativos; o cuando se mencionen Flybondi, JetSmart, Aerolíneas Argentinas, Ezeiza, Aeroparque, la percepción del 30%, el impuesto PAIS o el dólar tarjeta aplicado a viajes.
---

# Buscar pasajes aéreos

Herramienta de línea de comandos que busca vuelos y los ordena por **costo
real para un comprador argentino**, no por el precio que muestra el buscador.

## Por qué no alcanza con mirar Google Flights

Tres cosas que ningún metabuscador te dice y que esta herramienta sí calcula:

1. **La percepción del 30% (RG 5617).** Sobre pasajes al exterior pagados en
   pesos con tarjeta. No está en el precio publicado porque es un cargo del
   medio de pago. **Pagando en dólares se evita**, y es el ahorro más grande
   disponible: más que cambiar de fecha o de aerolínea.
2. **El equipaje.** La tarifa base de Flybondi y JetSmart no incluye
   carry-on; la Base de Aerolíneas sí. Comparar precios pelados favorece
   sistemáticamente a las low-cost y da una respuesta equivocada.
3. **Lo que cuesta el itinerario.** Una escala de siete horas, una conexión
   de 40 minutos que se pierde una de cada tres veces, o una salida a las 3
   de la mañana tienen un costo real que la herramienta convierte a pesos y
   suma al precio.

## Cómo usarla

```bash
python -m buscador ORIGEN DESTINO --ida FECHA [--vuelta FECHA] [opciones]
```

Origen y destino aceptan código IATA (`BRC`) o nombre de ciudad
(`bariloche`, `cordoba`). Las fechas aceptan `15/10`, `2026-10-15`, `+45d`,
`hoy` y `mañana`.

### Ejemplos

```bash
# Ida y vuelta de cabotaje
python -m buscador AEP BRC --ida 15/10 --vuelta 22/10

# Desde Santa Rosa, mirando también Bahía Blanca y Neuquén, con 3 días de
# flexibilidad en cada punta
python -m buscador RSA MDZ --ida 10/11 --vuelta 20/11 --flex 3 --cerca 600

# A Europa, pagando en dólares para esquivar la percepción
python -m buscador EZE MAD --ida +90d --vuelta +104d --pago dolares

# Familia con valija despachada, sólo vuelos directos
python -m buscador AEP IGR --ida 20/12 --vuelta 27/12 \
    --adultos 2 --ninos 2 --bodega 2 --directo

# Para procesar el resultado
python -m buscador AEP USH --ida +60d --json
```

### Las opciones que más cambian el resultado

| Opción | Qué hace |
|---|---|
| `--flex N` | Prueba N días antes y después. Con 3 días suele aparecer 20-30% de diferencia. |
| `--cerca KM` | Suma aeropuertos alternativos hasta KM por ruta, y descuenta el costo de manejar hasta ahí. |
| `--perfil` | `mochilero` (aguanta escalas por ahorrar), `ocio` (default), `comodo`, `trabajo` (paga por no sufrir), `solo-precio` (ordena por plata y nada más). |
| `--pago dolares` | Calcula el precio sin la percepción del 30%. |
| `--bodega N` | Cuántas valijas despachás. Cambia radicalmente la comparación entre low-cost y tradicionales. |
| `--sin-carry-on` | Viajás sólo con mochila chica: no cotiza el carry-on. |
| `--directo` / `--max-escalas N` | Filtros duros. |
| `--top N`, `--markdown`, `--json` | Formato de salida. |

## Cómo interpretar la salida

- **★ MEJOR OPCIÓN** es la de menor costo total, no la más barata.
- **💲 EL MÁS BARATO** puede estar más abajo: si aparece en el puesto 5, es
  porque su itinerario cuesta caro en tiempo o en riesgo.
- El puntaje de 0 a 100 es sólo para leer de un vistazo; el orden lo decide
  el costo total en pesos.
- `+$X de costo total vs. la mejor` es la línea más útil: dice cuánto sale de
  verdad elegir esa opción.
- `≈ precio de referencia` marca una cotización cacheada, no en vivo.

## Antes de correr una búsqueda

1. **Preguntá lo que falte**, pero sólo lo que cambia el resultado: fechas,
   si lleva valija despachada, y si puede pagar en dólares. Lo demás tiene
   default razonable.
2. **Si no hay credenciales cargadas**, la herramienta cae al proveedor
   `demo`, que genera datos sintéticos. Sirve para probar el flujo, **no para
   decidir una compra**. Avisalo siempre que la salida diga `vía demo`.
3. **La cuota gratuita de SerpApi son 250 búsquedas por mes** (unas 8 por
   día). Usá `--flex` con criterio y no repitas la misma consulta.

## Al reportar los resultados

- Dale el precio **final en pesos**, no el de vidriera.
- Si es internacional y paga en pesos, mencioná el ahorro concreto de pagar
  en dólares, con el número.
- Si la mejor opción es una low-cost, aclará qué equipaje incluye.
- Si la búsqueda es a más de 3 meses o cae cerca de un Hot Sale, Cyber Monday
  o Black Friday, mencionalo: puede convenir esperar.
- No prometas el precio. Se confirma recién en el checkout de la aerolínea.

## Configuración

Las credenciales van en `.env` (ver `.env.example`). Sin ninguna, funciona el
modo demo. Con `SERPAPI_KEY` (250 búsquedas gratis por mes, sin tarjeta) ya
tenés precios reales del mercado argentino, incluidas Flybondi y JetSmart.

Documentación completa en `README.md`; el detalle de por qué cada decisión
está en `docs/investigacion.md`.
