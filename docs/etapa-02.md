# Etapa 2: precios, costos, proveedores y compras (11–20)

## Alcance entregado

| Punto | Implementación |
|---|---|
| 11 | Precio vigente e historial de cambios con fecha, unidad, valor anterior/nuevo, responsable y motivo. Vigencia inmediata; no se reescriben comprobantes anteriores. |
| 12 | Costos de compra históricos por recepción, costo promedio ponderado de existencias y costo de reposición actualizable por separado. |
| 13 | Margen sobre venta y recargo sobre costo, con base de reposición identificada. Valores desconocidos o denominadores cero no generan indicadores ficticios. |
| 14 | Autorización con clave propia para dueño/encargado. Cajero no puede modificar. Control en backend, sesión de 30 minutos e historial de cada ajuste. |
| 15 | Alta/edición/desactivación de proveedores, contacto, documento opcional, condiciones y plazo. |
| 16 | Pedidos con proveedor, entrega prevista, notas, productos, cantidad/unidad y precio estimado. Registrar un pedido no modifica stock. |
| 17 | Recepciones parciales y múltiples, estados pendiente/parcial/recibido, consulta de faltantes y detalle de cada entrega. |
| 18 | Bultos, peso bruto y tara total en kg, neto calculado y conversión a gramos cuando corresponde. Productos por unidad se reciben como cantidad entera. |
| 19 | Calidad, observaciones y cantidad rechazada. Solo lo aceptado ingresa al stock; lo rechazado queda pendiente de reposición. |
| 20 | Importe por unidad o importe total real de mercadería aceptada, flete y otros gastos, distribución exacta de centavos y costo puesto por unidad. |

## Cómo usarlo

1. Crear productos con sus unidades en **Productos**.
2. Entrar a **Precios y costos** y crear el primer responsable (dueño) con nombre y clave propia de 8–128 caracteres. No hay credenciales predeterminadas ni cuentas inventadas. Desde una autorización de dueño se pueden agregar encargados y cajeros.
3. Registrar costo de reposición y precio de venta, indicando motivo. Consultar historial y comparar margen/recargo.
4. En **Compras**, cargar el proveedor y sus condiciones. Crear el pedido en la unidad del catálogo. Su precio es una estimación; la recepción conserva su importe real por separado.
5. Al recibir, elegir las líneas entregadas, registrar bultos, peso bruto y tara (o unidades), cantidad rechazada, calidad y observaciones. Para rechazo, el motivo es obligatorio.
6. Elegir **precio por unidad** o **importe total de mercadería aceptada**. La segunda opción permite registrar lo pagado por cajones de peso variable sin convertir el importe a kg a mano. Registrar flete y otros gastos y confirmar.
7. Consultar en el pedido lo solicitado, aceptado y pendiente, con detalle de las recepciones. Verificar el stock y costos actualizados en Precios y costos.

Los nombres/funciones del relevamiento de la etapa 1 no se convierten automáticamente en credenciales. El primer dueño debe ser configurado por el operador legítimo en el entorno local. Las claves se guardan con scrypt y sal aleatoria; las sesiones usan tokens aleatorios cuyo hash se guarda en la base, cookie HttpOnly y SameSite estricto. Cinco fallos de clave bloquean esa cuenta durante 15 minutos. El dueño puede agregar responsables, no el encargado ni el cajero. La gestión completa de usuarios, recuperación de claves y permisos generales sigue correspondiendo a la etapa de seguridad.

## Reglas de costo e inventario

- Bruto y tara se expresan siempre en kg para evitar mezclar escalas. Neto = bruto − tara. Rechazado y aceptado se expresan en la unidad del producto; para un producto en gramos, el neto en kg se multiplica por 1.000.
- No se supone un peso fijo por cajón. Los bultos son una magnitud separada del peso y no generan stock adicional.
- Por unidad: subtotal de mercadería = aceptado × precio, redondeado a centavos por línea. Por importe: se usa el importe real declarado de mercadería aceptada.
- Flete + otros gastos se asignan por valor de cada línea aceptada. Si todas valen cero, se distribuyen por igual entre las líneas aceptadas. El reparto usa centavos y distribuye los remanentes; la suma asignada coincide con el gasto total.
- Costo puesto de línea = subtotal + gastos asignados. Costo unitario = costo puesto / aceptado, redondeado a cuatro decimales. Los totales de documentos y líneas se conservan a centavos; multiplicar posteriormente el costo unitario redondeado puede dar una pequeña diferencia y no reemplaza el total original.
- Promedio nuevo = (stock previo × costo promedio previo + costo total de entrada) / stock nuevo. Se conserva separado del último costo de reposición.
- Si el stock anterior tiene costo desconocido, no se inventa un promedio: queda sin registrar, aunque se conoce el costo de la nueva compra. Un stock negativo requiere corrección antes de recibir.
- Los valores monetarios nuevos se calculan con Decimal y se guardan como texto decimal. La venta/costo promedio y el stock también conservan proyecciones numéricas para compatibilidad con el módulo anterior. Este cambio no convierte sus cálculos de venta heredados en aritmética decimal.
- Cantidades: hasta tres decimales; costos/precios unitarios: hasta cuatro. Los costos unitarios resultantes superiores a $9.999.999.999,9999 se rechazan para detectar datos fuera de rango.
- Pedido, recepción y actualización de stock/costo se guardan transaccionalmente. Si una línea falla, no se guarda parcialmente la recepción.
- Pedidos, recepciones y ajustes llevan una clave de operación. Reintentar los mismos datos no duplica registros o stock; reutilizarla con otros datos produce un conflicto. Un cambio de precio/costo con versión desactualizada también se rechaza.
- Las condiciones del proveedor y la identidad/unidad de los productos quedan como foto histórica del pedido. No se permite cambiar la unidad de un producto con stock, precios o compras; debe crearse otra presentación.

## Ejemplos de aceptación

- Costo de reposición $1.000 y precio $1.500: margen 33,33%, recargo 50%.
- Pedido de 20 kg. Se entregan 13 kg brutos con tara de 1 kg y se rechazan 2 kg: ingresan 10 kg, quedan 10 kg pendientes. A $1.000/kg y $1.000 de flete, el costo puesto es $1.100/kg.
- Segunda entrega de 10 kg aceptados a $2.000/kg sin flete: stock 20 kg, costo promedio $1.550/kg y último costo de reposición $2.000/kg.
- Un cajón cuesta $20.000, tiene 19 kg brutos y 1 kg de tara, con $2.000 de flete: ingresan 18 kg y el costo puesto es $1.222,2222/kg. El total de la recepción queda en $22.000.

## Límites y continuidad

Los importes son ARS registrados por el operador; no se calculan IVA, percepciones ni deducibilidad fiscal. Debe acordarse con el contador una base consistente antes de interpretar márgenes como datos contables. Los indicadores no incluyen merma, comisiones ni gastos operativos y no representan utilidad neta.

Esta etapa registra compras y recepciones; todavía no liquida deuda/pagos al proveedor, devoluciones/reclamos ni envases retornables (puntos 21–22 y posteriores). La mercadería rechazada no se contabiliza como aceptada; cargos del proveedor por esa mercadería y su reclamo requieren el circuito posterior. Las recepciones confirmadas no se borran ni editan: un circuito de corrección/devolución queda para la siguiente etapa. Los pedidos no tienen cancelación/cierre de faltantes en esta entrega.

La autorización protege las escrituras del módulo comercial; no reemplaza autenticación general del catálogo ni restringe todavía todas las lecturas de costos. El módulo anterior `/ventas` conserva sus reglas y posibles cambios de precio por línea; no se presenta como caja final con permisos ni emisión fiscal. El entorno debe seguir siendo local/de desarrollo. Para desplegar será necesario completar esos controles y usar HTTPS con `CORONEL_SECURE_COOKIE=1`.

No se cargaron proveedores, productos, responsables o contraseñas ficticias en la base del negocio. Las pruebas usan bases temporales separadas. Conservar en backups la base completa (incluye autorizaciones e historial) y las fotos de la etapa anterior; no versionar esos datos.

## Validación reproducible

```bash
python -m unittest discover -s tests -v
python tests/browser_smoke.py
python tests/browser_comercial.py
```

Los navegadores requieren `requirements-browser.txt` y Chromium; `APP_PYTHON` y `CHROMIUM_PATH` permiten seleccionar los ejecutables. `browser_comercial.py` usa temporalmente el puerto 8003 y deja capturas en `/tmp/verduleria-precios.png`, `/tmp/verduleria-compras.png` y `/tmp/verduleria-compra-movil.png`. No instala ni conecta balanzas, terminales de pago o servicios fiscales.

Resultado de esta entrega: **34 pruebas de backend aprobadas** (24 comerciales y 10 de la etapa anterior). También pasaron ambos recorridos Playwright: etapa 1 y circuito comercial, con escritorio a 1440 px y celular a 390 px, sin errores JavaScript. La prueba comercial cubre autorización, historial, proveedor, pedido, compra por importe total, rechazo parcial, segunda entrega, costo promedio, recarga y bloqueo de escrituras después de cerrar autorización. Las bases temporales se eliminan al terminar.
