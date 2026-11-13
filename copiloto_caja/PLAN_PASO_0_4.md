# Paso 0.4 — Importes y fechas: plan para aprobar

**Estado: EJECUTADO** (aprobado por el dueño). Ver el commit "Paso 0.4" y tests/test_importes_fechas.py.

## Qué hay hoy [Observado]

| Tabla | Columna | Tipo actual | Qué es |
|---|---|---|---|
| `comprobantes` | `subtotal`, `total` | `REAL` | Pesos (plata) |
| `comprobantes` | `descuento` | `REAL` | **Porcentaje** (10 = 10 %), no plata |
| `comprobantes` | `fecha` | `TEXT` `dd-mm-YYYY` | Fecha de emisión |
| `comprobante_items` | `precio_unitario`, `precio_costo`, `subtotal` | `REAL` | Pesos (plata) |
| `comprobante_items` | `cantidad` | `REAL` | Cantidad (puede ser fraccionaria, por ejemplo kg). No es plata |

## Qué propongo

### Migración `0006_importes_fechas` (Python, no SQL puro)

Se necesita Python para convertir con `Decimal` y redondeo `ROUND_HALF_EVEN`, porque el `ROUND()` de SQLite redondea distinto. Hace falta un cambio chico en el migrador: que acepte archivos `NNNN_nombre.py` con una función `migrar(conn)`, dentro de la misma transacción.

1. **Respaldo automático** antes de migrar (ya existe).
2. **Columnas nuevas, sin borrar las viejas:**
   - `comprobantes.subtotal_centavos`, `comprobantes.total_centavos` (`INTEGER`);
   - `comprobante_items.precio_unitario_centavos`, `precio_costo_centavos`, `subtotal_centavos` (`INTEGER`);
   - `comprobantes.fecha_original` (`TEXT`): guarda el texto anterior de la fecha.
3. **Conversión de importes:** `centavos = Decimal(str(valor)).quantize(Decimal("0.01"), ROUND_HALF_EVEN) * 100`.
4. **Conversión de fechas:**
   - `fecha` pasa a ISO `YYYY-MM-DD` cuando el texto es exactamente `dd-mm-aaaa` y es una fecha válida.
   - El texto anterior queda en `fecha_original`.
   - Si una fecha no se puede convertir, **queda como estaba** y se lista como problema.
5. **Reporte de verificación** (en pantalla y en un archivo dentro de `BACKUP_DIR`):
   - filas migradas por tabla;
   - suma de `total` antes (pesos) contra suma de `total_centavos` / 100 después: tienen que coincidir al centavo;
   - por comprobante, que la suma de los ítems coincida con el subtotal, informando las diferencias que ya existieran;
   - lista de filas con problemas: fecha ilegible, importe negativo o nulo.
6. **Si el reporte detecta una diferencia de totales, la migración se deshace** y no queda nada aplicado.

### Cambios de código

- **Emisión:** calcula en `Decimal` y guarda centavos y, mientras tanto, también las columnas viejas (doble escritura), para que nada que lea las columnas viejas se rompa. La fecha nueva se guarda en ISO.
- **API:** devuelve **los mismos campos** de hoy (`subtotal`, `total`, `fecha`, etc.):
  - los importes se calculan desde los centavos, en pesos;
  - `fecha` sale en ISO.
- **Frontend:**
  - muestra `fecha` como `dd/mm/aaaa`;
  - el indicador **"Hoy"** compara contra la fecha ISO de hoy. Hoy **siempre muestra $0** por un error que ya existía: compara `13/11/2026` contra `13-11-2026`.
- **Pruebas:**
  - conversión de casos límite (`0,005`, `1999,995`, `10000`);
  - fecha ilegible;
  - totales que coinciden;
  - la migración se puede correr dos veces;
  - las pruebas de caracterización siguen pasando.

### Fuera de este paso (lo anoto para decidir)

- `productos.precio_venta` y `precio_costo`, y `ventas_historicas` (importes en `REAL` y fechas como vengan del CSV): mismo problema, otra migración.
- **La "Ganancia" de la barra superior no es real:** hoy es siempre el 44 % de lo vendido (`v*0.44`), sin mirar los costos. Se puede calcular con los costos de los ítems.
- **Retirar las columnas `REAL` viejas:** recién cuando nada las use, en una migración posterior.

## Qué necesito de vos

1. **OK para ejecutar este plan.**
2. **Si en tu base real hay fechas con otro formato.** Si me pasás una muestra anonimizada, la pruebo antes.
