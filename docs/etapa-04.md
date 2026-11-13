# Etapa 4: rotación, envases y mostrador (31–40)

## Alcance

| Punto | Resultado |
|---|---|
| 31 | Rotación sugerida por condición/ingreso y compra sugerida con mínimos, seguridad, cobertura, plazo, ventas netas observadas o estimación manual. |
| 32 | Envases por proveedor y tipo: en el local, por devolver, pérdidas a regularizar y depósitos monetarios separados. |
| 33 | Mostrador táctil, búsqueda con alias, favoritos por operador y entrada de lector que emule teclado. F2 enfoca la búsqueda. |
| 34 | Una venta combina kg, g y unidades, atados, bolsas, bandejas o cajones enteros. |
| 35 | Peso bruto y tara en kg; neto calculado en servidor y convertido a la unidad del catálogo. Precio y unidad visibles antes del registro. |
| 36 | **Pendiente de hardware**: carga manual operativa y estado explícito sin balanza conectada. La referencia enviada por foto se identifica como Kretz Ouro; faltan variante exacta, conexiones, protocolo y prueba física de tablet, balanza e impresión. |
| 37 | Códigos internos/alias y formato de etiquetas EAN-13 configurable con validación de checksum, posiciones, prefijo y precisión. Peso neto puede agregarse; importe sin peso es informativo y no inventa kilos. El formato real de Nativa sigue pendiente de confirmar. |
| 38 | Suspender y recuperar carritos en servidor; sin reserva de stock y con precios actuales al recuperar. Recuperación de una sola vez, con reintento seguro. |
| 39 | Descuento porcentual con motivo, autorizado por sesión de dueño/encargada y verificado por backend. Cajero puede vender sin descuento; para autorizarlo debe intervenir un responsable. |
| 40 | Devoluciones parciales y anulación del remanente, conservando venta original, responsable, motivos, cantidades y valores. Mercadería devuelta a cuarentena o descarte explícito. |

## Uso de la nueva caja

1. Ingresar con un responsable desde Mostrador. El dueño/encargada puede autorizar descuentos y correcciones; cajero no.
2. Buscar y elegir productos. En productos por peso, ingresar bruto y tara en kg; en los demás, cantidad entera. El resultado se valida en el servidor antes de agregarlo.
3. Revisar el total cotizado. Un cambio de precio posterior invalida el registro de esa cotización y pide recalcular. Las cotizaciones duran cinco minutos y pertenecen a la sesión que las creó.
4. Si hace falta, suspender con una referencia. El carrito no reserva mercadería ni conserva un precio obligatorio. Para recuperar otro carrito, primero suspender o vaciar el actual.
5. Registrar la venta. Se guarda un documento interno `V-…`, se descuenta stock y el estado de cobro queda **pendiente**. No se ejecuta pago, transferencia, impresión ni autorización fiscal.
6. Para devolver, elegir cantidades todavía pendientes de cada línea y un destino físico. Para anular, se corrige todo el remanente aún no devuelto.

La venta registrada y el cobro confirmado son estados distintos. Los puntos 41–52 incorporarán ticket, cobros y caja. Esta etapa permite probar la operación comercial, pero no sustituye una caja final lista para atender con pagos y emisión fiscal.

## Dinero, descuentos y correcciones

Los importes se calculan con Decimal en servidor. Cada línea redondea su bruto a centavos. El descuento total se distribuye por valor de línea con reparto exacto del centavo restante. No se acepta un precio unitario suministrado por el navegador para alterar el catálogo.

Una devolución usa el neto de la línea original, aunque el precio actual haya cambiado. Para devoluciones fraccionadas se calcula el valor acumulado proporcional, redondeado a centavos, y se resta lo ya corregido. Esto evita devolver más que el neto original por sucesivos redondeos. Una anulación posterior corrige solo lo pendiente; el total de correcciones no supera el total de la venta.

Las correcciones comerciales muestran un importe a revisar. No confirman que se haya devuelto dinero, no cambian un banco o caja y no emiten notas fiscales. Una venta con cobro pendiente tampoco se considera pagada por el hecho de registrarse.

Por defecto, la mercadería devuelta entra en cuarentena y no vuelve al vendible. Si se declara descarte, se registran entrada y salida de cuarentena para conservar la evidencia; el stock vendible no aumenta. El sistema no determina inocuidad ni comprueba que la devolución ocurrió físicamente.

## Stock y trazabilidad

Las ventas del nuevo mostrador usan movimientos `venta_pos` y los datos nuevos se conservan separados del módulo anterior. La selección automática prioriza maduro, listo, verde y luego para revisar, dentro de ubicaciones vendibles; no apto y cuarentena quedan excluidos. El origen de lote sigue marcado como **inferido**, porque no se escaneó físicamente cada lote. La sugerencia de rotación no certifica que un alimento esté apto.

Las correcciones reconstruyen las asignaciones originales, conservan el costo del lote y no crean un origen inventado. Se bloquean cantidades superiores a las vendidas, correcciones repetidas, stock insuficiente, stock externo a conciliar y saldos negativos heredados. El historial no se borra.

Las ventas nuevas aparecen en los indicadores de última venta y baja rotación del inventario. Las sugerencias de demanda usan cantidades netas de devoluciones y excluyen anulaciones; no emparejan ventas antiguas por coincidencia de nombres.

## Planificación de compra

Base propuesta = máximo entre mínimo vendible y (venta diaria × (cobertura + plazo) + seguridad), menos stock vendible y entradas previstas dentro del período. El resultado se limita a cero y se redondea hacia arriba a tres decimales por peso o a unidades enteras.

La venta diaria puede ser manual o provenir de ventas observadas en una ventana de siete días, ajustada a los días de observación disponibles. Si no hay evidencia suficiente, se indica; no se convierte automáticamente falta de datos en demanda cero. Todavía puede sugerirse cubrir un mínimo configurado.

Pedidos sin fecha o atrasados no se restan como si fueran entregas seguras: se muestran por separado. Las fechas de próxima revisión de lotes no se usan como vencimientos legales. No se crean pedidos automáticos; el encargado debe revisar calidad real, vida útil, presupuesto, clima/estacionalidad y faltantes que oculten demanda.

## Envases retornables

Registrar tipos reales y movimientos por proveedor. No se generan deudas de cajones automáticamente a partir de bultos de mercadería, porque un bulto puede ser otro embalaje.

- Recibido / saldo inicial: aumenta lo físico y lo adeudado.
- Devuelto: disminuye ambos; no supera lo que hay en el local.
- Pérdida: disminuye lo físico, pero se sigue debiendo al proveedor.
- Baja acordada: regulariza una pérdida ya registrada; exige referencia y motivo de ese acuerdo.
- Depósito pagado: aumenta dinero a favor; reintegro o aplicación por acuerdo lo disminuye sin superar el saldo registrado.

Envases, depósitos y deuda de mercadería son registros diferentes. No se envía dinero ni se contabiliza automáticamente una indemnización o movimiento de caja. El saldo inicial solo puede cargarse antes de los demás movimientos de esa combinación proveedor/envase. Errores se deben corregir con movimientos explicados; esta entrega no borra el historial ni implementa aún una reversión general de envases.

## Etiquetas y balanza

No hay formatos de ejemplo cargados en la base real. El responsable configura el formato de una etiqueta auténtica: prefijo, posiciones del PLU, posiciones del valor, decimales y unidad. Las posiciones se cuentan desde 1, la 13 se reserva al dígito verificador y los campos no se pueden superponer. Se rechazan prefijos que colisionen entre reglas.

El PLU debe identificar un código/alias del catálogo. Un código interno corto, aunque empiece igual que un prefijo, no se interpreta como etiqueta completa. La etiqueta de peso guarda su regla y lectura en los datos de la línea para no reinterpretar ventas antiguas al cambiar la configuración. No se verificó que la variante de Kretz Ouro referida imprima este tipo de etiqueta o exponga peso a una tablet; la imagen frontal solo permite leer marca y familia/modelo.

Una etiqueta con solo importe no determina el peso real: no se divide silenciosamente por un precio actual que puede haber cambiado. Se informa el importe, pero el operador debe pesar y revisar el precio de la carga manual. La compatibilidad física con lector, balanza y tablet se debe demostrar con los equipos concretos. No hay lectura automática de puerto, red o Bluetooth activada.

## Persistencia y continuidad

El carrito puede recuperarse desde almacenamiento local del dispositivo. Los suspendidos quedan en servidor. No se guardan claves en ese almacenamiento; la sesión sigue en cookie HttpOnly. Esta función no permite completar ventas offline.

Antes de registrar, se conserva localmente la referencia de operación. Si se pierde la respuesta después del commit, queda un registro pendiente que se reintenta con la misma clave, incluso después de recargar, sin duplicar stock ni venta. Una misma cotización no genera dos ventas aunque se envíe otra clave. Operaciones, stock, venta y correcciones se guardan en transacciones.

No se promete sincronización offline, reserva de stock de suspendidos o coordinación completa entre varias pestañas/cajas. La seguridad general, exposición pública y permisos de módulos anteriores siguen pendientes según el plan. Esta es una entrega de desarrollo para validación del negocio, no una publicación en producción.

## Pruebas reproducibles

```bash
python -m unittest discover -s tests -v
python tests/browser_mostrador.py
```

El navegador usa el puerto 8005, datos temporales y Chromium. `APP_PYTHON` y `CHROMIUM_PATH` permiten elegir ejecutables. Capturas: `/tmp/nativa-mostrador.png`, `/tmp/nativa-mostrador-movil.png`, `/tmp/nativa-reposicion.png` y `/tmp/nativa-envases.png`. Las pruebas de hardware real no se han ejecutado por faltar el equipo/modelo.

Se intentó consultar `https://www.kretz.com.ar/` para documentación oficial, pero el proxy del entorno devolvió `403 Forbidden` antes de recuperar contenido. No se atribuyen interfaces ni protocolos a esa página no consultada.

Resultado de validación: **88 pruebas de backend aprobadas** (26 de mostrador y 62 anteriores) y los cuatro recorridos de navegador aprobados, sin errores JavaScript. El recorrido nuevo cubre favoritos, venta mixta, tara, descuento, suspensión, recarga tras pérdida de respuesta del registro, devolución parcial, anulación, configuración/lectura de etiqueta de prueba, previsión, envases y depósitos, en escritorio y a 390 px. Las bases de prueba son temporales; no se cargan productos, claves, ventas ni etiquetas ficticias en la base real.
