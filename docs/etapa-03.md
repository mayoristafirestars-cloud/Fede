# Etapa 3: proveedores e inventario (puntos 21–30)

## Funciones entregadas

| Punto | Implementación |
|---|---|
| 21 | Devoluciones físicas vinculadas a lote, ubicación, recepción y proveedor. Reclamos por calidad, faltante, precio u otro motivo, con historial de seguimiento y estado. |
| 22 | Cuenta por proveedor y recepción: cargos, vencimientos, pagos parciales, créditos confirmados, saldos a favor, reintegros y reversión de registros erróneos. |
| 23 | Libro de movimientos para recepciones, ventas y anulaciones del módulo anterior, traslados, devoluciones, merma, otros destinos y ajustes de conteo. |
| 24 | Existencias por producto, lote y ubicación. Salón, depósito, cámara y cuarentena; traslado con salida y entrada vinculadas. |
| 25 | Cada nueva recepción aceptada genera un lote con proveedor, fecha, unidad y costo de ingreso. La procedencia desconocida se identifica como tal. |
| 26 | Estados verde, listo, maduro, para revisar y no apto. Notas, responsable, próxima revisión e historial de cambios. |
| 27 | Merma con cantidad, ubicación, causa, motivo, responsable, fecha y valor a costo cuando se conoce. |
| 28 | Regalo, consumo interno y donación separados del descarte. Diferencias de conteo sin causa conocida no se etiquetan como deterioro o robo. |
| 29 | Conteo físico pendiente y aprobación del ajuste, con saldo esperado, cantidad contada y fecha de corte. Control de versión para evitar sobrescribir movimientos posteriores. |
| 30 | Alertas de mínimo vendible, falta de producto, baja rotación y lotes a revisar. Mínimos y días configurables por producto. |

## Uso del inventario

1. Autorizarse como dueño o encargado, usando las claves de la etapa 2. También se puede abrir la autorización desde Inventario o Proveedores y cuentas.
2. En Compras, seleccionar la ubicación de ingreso al confirmar una recepción. Se conservan bruto, tara, aceptación, rechazo e importe de la etapa anterior.
3. Abrir Inventario: consultar existencia física, vendible y desglose de ubicaciones. No se suman kilos con unidades, atados o cajones.
4. En un lote, elegir trasladar, registrar salida, revisar maduración, contar o devolver al proveedor. La cantidad se expresa siempre en la unidad de ese producto.
5. Registrar el conteo real, sin completar automáticamente el número contado con el saldo del sistema. Revisar la diferencia y aprobarla desde Conteos físicos.
6. Consultar el libro de movimientos, con paginación. La cantidad tiene signo; el valor a costo se muestra como magnitud del movimiento, no como ganancia o pérdida de todo el negocio.

**Mercadería sin origen** registra existencias adicionales que todavía no pertenecen a otro lote. No debe usarse para volver a cargar el total de un producto ya inventariado. Crea un lote sin recepción ni costo confirmado y un conteo pendiente; solo la aprobación modifica stock. Un lote de origen desconocido no puede devolverse a un proveedor como si se conociera su compra.

No apto y cuarentena excluyen mercadería del saldo vendible, pero la conservan en existencia física. Marcar un estado no certifica inocuidad, no controla temperaturas y no descarta automáticamente alimentos. Es una decisión registrada por el operador competente.

## Devolución, reclamo y crédito: tres operaciones distintas

La devolución quita mercadería físicamente del lote y conserva la referencia a su recepción. No borra la recepción original, no reabre silenciosamente el pedido y no disminuye por sí sola la deuda. Su cantidad no puede superar lo aceptado originalmente del lote ni lo que queda en la ubicación elegida.

El reclamo documenta el problema y su seguimiento: abierto, en gestión, resuelto o rechazado. Cambiar su estado no genera stock ni dinero. Un proveedor puede resolver un reclamo con reposición, descuento o rechazo; esa decisión no se presupone.

Cuando el proveedor confirma un crédito, se registra en la cuenta de la recepción con importe, fecha, referencia y motivo. Puede vincularse a una devolución o reclamo de esa misma recepción. No se acepta una vinculación a otro documento. No se emite una nota de crédito fiscal ni se verifica automáticamente el documento externo.

## Deuda y pagos a proveedores

- Una nueva recepción genera un cargo por la mercadería aceptada. Flete y otros gastos se incluyen en esa deuda **solo si se marca que los cobra el mismo proveedor**. Los gastos pagados a terceros siguen formando parte del costo del alimento, pero no se adeudan automáticamente al proveedor de la mercadería.
- Vencimiento = fecha de recepción en Argentina + plazo de días calendario que quedó guardado en el pedido. El tablero identifica saldos pendientes y documentos vencidos.
- Un pago disminuye el saldo de esa recepción y puede ser parcial. No se permite pagar más que su deuda registrada.
- Un crédito confirmado disminuye el saldo y puede dejarlo a favor si la compra ya estaba pagada. Los créditos activos no pueden superar el cargo original de la recepción.
- El reintegro recibido aumenta el saldo hacia cero; no puede superar el crédito disponible de esa recepción.
- Una reversión agrega el importe contrario, conserva el original y solo puede aplicarse una vez al movimiento. No revierte físicamente una transferencia bancaria.
- Las operaciones se registran como ya ocurridas o confirmadas, con referencia y motivo. No se envía dinero, no se consulta el banco ni se modifica todavía un arqueo de caja.
- Los créditos no se imputan automáticamente entre recepciones diferentes. La vista separa documentos pendientes y saldos a favor; un saldo neto por proveedor no sustituye la conciliación por documento.

Ejemplo: 20 kg a $1.000/kg y $2.000 de flete pagado a un transportista. Costo del alimento: $22.000, o $1.100/kg. Deuda con el proveedor de fruta: $20.000. Devolver 1 kg deja stock de 19 kg y mantiene esa deuda. Un crédito confirmado de $1.000 reduce la deuda a $19.000; el valor físico de salida a costo es $1.100. Son importes y hechos diferentes.

## Reglas de integridad

Las escrituras nuevas requieren dueño o encargado. Las operaciones llevan clave de reintento, se ejecutan en transacción y no duplican stock, pagos o créditos al repetirse. Reutilizar una clave con otros datos produce un conflicto.

Los conteos guardan la versión de la existencia de un lote y ubicación. Si hubo una venta, traslado, devolución u otra entrada/salida posterior, se rechaza la aprobación; hay que contar nuevamente. El conteo anterior se conserva pendiente como evidencia y no puede sobrescribir el saldo actual. El aprobador puede ser la misma persona que contó, porque este negocio puede operar con una sola persona.

Las cantidades nuevas se calculan con Decimal y se conservan como texto decimal en el libro y posiciones. El campo numérico `productos.stock` se mantiene como proyección para las pantallas anteriores. Si se modifica por SQL o por un importador que no usa el nuevo libro, el sistema muestra el descuadre y bloquea salidas/recepciones/traslados hasta conciliar mediante un conteo físico. No usar los importadores antiguos directamente sobre una base activa sin adaptación.

Un saldo negativo heredado se conserva para revisión y bloquea operaciones del producto hasta contar y corregir ese lote. No se compensa silenciosamente usando otro lote positivo. El costo promedio no se presenta como conocido cuando alguna existencia no está valorizada.

El costo promedio se recalcula al quitar o ajustar existencias usando los costos de los lotes restantes. Una merma usa costo, no precio de venta. Regalos, consumo y diferencias desconocidas conservan sus tipos. Los traslados no cambian el total físico ni se interpretan como ventas o pérdidas.

## Migración y trazabilidad limitada por la evidencia

La migración es aditiva e idempotente. Conserva compras, precios, stock anterior y comprobantes. Las existencias anteriores se representan como saldo de apertura sin proveedor ni recepción adjudicados automáticamente. Las recepciones históricas se conservan como lotes documentales con cantidad actual no atribuida; no se supone que toda la compra sigue en el local.

Las cuentas incorporan los cargos de las recepciones anteriores. Los pagos que no se habían registrado todavía deben cargarse antes de interpretar el saldo como deuda real. En recepciones antiguas sin declaración sobre quién cobra flete/gastos, el cargo inicial incluye solo mercadería; revisar esa clasificación contra los documentos. No se inventan deudas anteriores que no tengan recepción en este sistema.

Las ventas del módulo anterior descuentan lotes disponibles por orden de ingreso, excluyendo cuarentena y no aptos. La selección es **inferida**, porque el cajero anterior no identifica físicamente el lote entregado. Se indica en el libro y no se promete trazabilidad exacta si se mezcló mercadería. Esta asignación no implementa todavía priorización avanzada por vida útil del punto 31.

Anular una venta registrada en el libro revierte sus movimientos una sola vez. Anular un comprobante anterior al libro genera un lote a revisar sin origen físico confirmado. La operación informática no verifica que el alimento haya vuelto físicamente ni que sea apto para reventa.

## Alertas y límites

Faltante significa vendible menor o igual al mínimo configurado. Baja rotación requiere existencia vendible y suficientes días desde la última venta activa registrada, o desde el inicio de las observaciones si no hay ventas. Un artículo recién recibido no se marca lento automáticamente. Se informa cuántos días hay observados; las ventas anuladas no cuentan como venta activa. Los datos históricos de ventas sin identificación fiable de producto no se emparejan por nombre.

No hay todavía pronóstico de demanda, sugerencia de compras (31), envases retornables (32), caja nueva, valuación contable fiscal, conciliación bancaria ni autenticación general de toda la aplicación. Las lecturas siguen disponibles en el entorno local de desarrollo. El módulo de ventas anterior conserva su autenticación pendiente; sus movimientos se rotulan como procedentes de ese módulo, sin inventar un responsable autenticado. No se presenta esta entrega como sistema publicado o preparado para exposición pública.

## Verificación

```bash
python -m unittest discover -s tests -v
python tests/browser_smoke.py
python tests/browser_comercial.py
python tests/browser_inventario.py
```

Los recorridos de navegador requieren las dependencias de `requirements-browser.txt` y Chromium. `APP_PYTHON` selecciona el Python del servidor y `CHROMIUM_PATH` el navegador. La prueba de esta etapa usa el puerto 8004 y bases temporales; no modifica la base del negocio. Capturas: `/tmp/verduleria-inventario.png`, `/tmp/verduleria-cuentas.png` y `/tmp/verduleria-inventario-movil.png`.
