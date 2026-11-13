# Tienda de Nativa: puntos 4 al 10

Continuación de los diez puntos de la propuesta para clientes, no de la numeración del antiguo sistema de gestión. Código preparado en el entorno de desarrollo; no se actualizó automáticamente Hetzner.

## Funciones listas

4. **Reemplazos elegidos.** Por renglón: no reemplazar, consultar una propuesta o permitir únicamente un producto alternativo elegido. El backend impide otro reemplazo cuando hay restricción. El preparador puede omitir un renglón sin cargo; no puede enviar una propuesta vacía. El cliente ve producto original, alternativa, unidades, peso y precio reales y debe aprobar el detalle completo. No hay sustitución automática por silencio ni aprobación de un importe que todavía no fue presentado.
5. **Presupuesto máximo.** Opcional, en pesos con hasta dos decimales. Debe alcanzar el estimado inicial. El backend rechaza pesajes/reemplazos cuyo total supere el máximo. No hay envío ni cargos ocultos en este flujo de retiro. Para aumentar un máximo acordado se debe coordinar una nueva solicitud; el empleado no puede cambiarlo unilateralmente.
6. **Recompra.** Desde el enlace privado o Mi última compra se recupera la lista solicitada original con precios vigentes. Se omiten artículos ya no publicados o con unidad cambiada y se explican cambios. Si la alternativa elegida desapareció, hay que elegir otra o cambiar la preferencia. La lista se revisa antes de enviar; no crea pedidos ni cobra automáticamente. Si ya había carrito se pide confirmación antes de reemplazarlo. Se mantienen los enlaces privados y su vencimiento de treinta días; no es un historial de cuenta permanente.
7. **Disponibilidad compartida.** Una solicitud con franja reserva cantidades en una transacción SQLite. Mostrador y comprobantes anteriores no pueden consumir cantidades reservadas; inventario muestra físico, vendible, reservado web y libre. Al pesar se ajusta la reserva al neto y a los reemplazos reales, excluyendo la propia reserva al validar. Si cambia la aptitud del lote, se alerta al personal y no se puede aprobar/entregar sin resolver la falta. Las entradas previstas no cuentan como disponibles. El catálogo comunica disponible, agotado o a confirmar sin publicar costos ni cantidades internas.
8. **Cupos de retiro.** El encargado crea franjas en hora de Argentina, con cupo, hasta siete días por adelantado y duración máxima de ocho horas. Se impiden solapamientos activos o con compromisos vigentes aunque se haya cerrado la franja. Elegir una franja asigna cupo y reserva de forma atómica. Se pueden pausar nuevas solicitudes o exigir horario. Cerrar una franja no cancela pedidos existentes. Sin franja, si el comercio permite esa modalidad, la solicitud queda a coordinar y no promete reserva ni horario. Para operación con compromisos usar Exigir franja de retiro.
9. **Ayuda y reclamos.** Consulta vinculada al pedido y opcionalmente al producto, sin foto obligatoria. Motivos de faltante, calidad, cantidad, reemplazo, cobro, entrega o consulta. El personal responde y marca abierto, en revisión o resuelto. El cliente consulta respuestas con su enlace privado al actualizar. No se envían avisos de WhatsApp automáticamente ni se promete resolución por haber recibido la consulta. Se admiten hasta cinco casos abiertos por pedido. Cerrar un caso no transfiere dinero, no devuelve mercadería a vendible y no reemplaza los derechos legales del cliente.
10. **Contribución por pedido.** Reporte privado de ingreso, costo de mercadería y gastos declarados: empaque, comisión, minutos × valor hora, entrega a cargo del local e incidencias. Primero se estima por costo conocido del producto; al entregar se usan los costos de los lotes efectivamente descontados. Costos desconocidos aparecen sin datos; no se sustituyen por cero. El usuario declara explícitamente los gastos, incluso cuando son cero. Se guarda historial de declaraciones y la contribución se calcula antes de costos fijos e impuestos. No es una liquidación contable ni utilidad neta del negocio.

## Reservas y vencimientos

La duración inicial configurable es de 15 a 1440 minutos (120 por defecto), nunca más allá del fin de la franja. El cliente debe revisar/aprobar la propuesta durante esa ventana; al aprobar, la reserva se mantiene hasta el cierre de su franja. Si no alcanza a confirmarse, vence y libera mercadería y cupo. La duración se muestra al elegir horario y el vencimiento real en seguimiento.

Las consultas al catálogo/pedidos y las operaciones aplican vencimientos. La función central de stock ignora reservas ya vencidas aun sin un proceso de fondo. No hay notificación automática ni trabajo programado; no hace falta un cron para liberar cantidades del cálculo de disponibilidad. Cancelar libera únicamente la reserva de ese pedido, una vez. La cancelación comercial no permite deshacer una entrega ya registrada; para problemas posteriores usar el reclamo y el procedimiento de ajuste que corresponda.

Para el piloto, crear franjas cercanas que el local pueda preparar. Ofrecer una fecha futura no reemplaza el control de aptitud y frescura; la reserva depende de la existencia contada y del mantenimiento del inventario. Los ajustes físicos y la declaración de mercadería no apta siguen reflejando la realidad aun cuando afecten una reserva; el sistema alerta y bloquea la confirmación hasta resolverla.

## Entrega, stock y cobro manual

Después de aprobar el cliente, el personal puede registrar la entrega sólo declarando que verificó el cobro, medio e importe igual al aprobado, con referencia. Para transferencia/MP debe comprobar la acreditación por el canal real; una captura no demuestra acreditación.

La entrega consume los lotes una sola vez en la misma transacción y libera la reserva. El ingreso y la referencia manual quedan guardados. Una doble pulsación/reintento devuelve el resultado existente, no otro movimiento. Las entregas web alimentan última venta/rotación y reposición. No se crearon filas duplicadas en las ventas de mostrador: el origen web se conserva como tal en los movimientos y pedidos.

Esto no conecta Mercado Pago ni bancos, no emite comprobantes ARCA, no abre caja automáticamente ni crea una factura fiscal. No registrar entrega/cobro para pedidos de prueba en la base real. Los reclamos no generan reintegros ni notas fiscales automáticamente; deben gestionarse por el procedimiento validado con la contadora y registrarse correctamente.

## Uso desde la gestión

1. Ingresar como dueño o encargada y abrir Tienda para vecinos.
2. Configurar contacto público, recibir solicitudes y exigir franja si se quiere reservar/cumplir horarios. Crear cupos realistas. Publicar productos con foto y precio; tener stock conciliado en inventario.
3. Revisar solicitudes, preferencias y presupuesto. Elegir producto real, omisión o alternativa permitida. Cargar bruto/tara o cantidades enteras según la unidad del producto que se prepara.
4. Enviar propuesta y esperar aceptación. Si supera presupuesto, corregir antes de enviarla. Ante pérdida de aptitud revisar el inventario y resolver reemplazo/omisión/cancelación; no forzar stock negativo para cumplir.
5. Verificar cobro por el medio real y registrar entrega al momento de entregar. Si una reserva venció, coordinar una nueva solicitud; no se renueva a escondidas.
6. Responder consultas y completar costos reales o estimados, identificando el valor hora utilizado. Consultar la contribución privada y distinguirla de la recaudación y de la utilidad después de costos fijos/impuestos.

## Seguridad y conservación

El host público y sus APIs no entregan información de costos, reservas de terceros, teléfono de otros compradores ni datos del personal. Los nuevos endpoints privados requieren dueño/encargada. El acceso por enlace sigue verificando hash de secreto de 256 bits, vencimiento, pertenencia de reclamos y versiones. El teléfono no es una contraseña ni está verificado automáticamente. No hay campañas ni alta a listas de publicidad.

Se conservan precios/cantidades solicitados, alternativas propuestas, aprobación, costos y respuestas. Cambios de versión impiden aceptar un total viejo; claves idempotentes evitan repetir entrega, cancelación y respuestas. Migración aditiva sin publicar automáticamente artículos ni sobrescribir usuarios, configuración o ventas previas. Se mantiene compatibilidad de reintento con solicitudes de la primera entrega cuyo cuerpo no tenía preferencias nuevas.

Antes de abrir tráfico real, completar DNS/HTTPS, reglas del proxy y confianza acotada de IPs, límites de cuerpo, respaldo externo/restauración, actualización del servidor y revisión de identificación comercial, privacidad/conservación, cancelaciones/reclamos y procedimiento fiscal. El transporte electrónico de pagos y el reparto público siguen pendientes. El sistema permite un piloto de retiro, sin prometer integración o emisión fiscal inexistentes.

## Pruebas

`python -m unittest discover -s tests -v` incluye carrera por último cupo, carrera por últimas existencias, reserva frente a ventas locales, cancelación/expiración, cambio de aptitud, presupuesto, restricciones de sustitución, contribución desconocida y entrega idempotente.

`APP_PYTHON=/ruta/python python tests/browser_tienda_operacion.py` recorre el flujo en móvil con datos temporales: presupuesto bloqueante, preferencia, horario, reserva, propuesta, ayuda/respuesta, costos, aprobación, entrega y recompra con precios nuevos. `browser_tienda.py` verifica el flujo anterior, y `browser_mostrador.py` la caja. Las capturas usan datos e imágenes sintéticas sólo de prueba, no mercadería o precios reales.

## Actualización de Hetzner

Paquete: Nativa-puntos-1-10.tar.gz. No contiene bases, fotos reales ni claves. Transferir desde PowerShell, con el archivo en Descargas:

```powershell
scp "$env:USERPROFILE\Downloads\Nativa-puntos-1-10.tar.gz" root@116.203.234.174:/root/
```

En el servidor Nativa, construir sin detener el servicio:

```bash
mkdir -p /opt/nativa-tienda-v2
tar -xzf /root/Nativa-puntos-1-10.tar.gz -C /opt/nativa-tienda-v2
cd /opt/nativa-tienda-v2
docker build -t nativa:tienda-v2 .
```

Antes de cambiar contenedores, suspender el uso y hacer respaldo con el contenedor actual. El nombre de destino tiene que ser nuevo. Descargar una copia privada fuera del servidor:

```bash
nativa_backup="antes-tienda-v2-$(date +%Y%m%d-%H%M%S).tar.gz"
docker exec nativa python scripts/respaldo.py "/var/lib/nativa/$nativa_backup"
docker cp "nativa:/var/lib/nativa/$nativa_backup" "/root/$nativa_backup"
```

Con el servicio sin operaciones concurrentes y respaldo guardado:

```bash
docker stop nativa
docker rename nativa nativa-anterior-tienda-v2
docker run -d --name nativa --restart unless-stopped --log-opt max-size=10m --log-opt max-file=3 -p 127.0.0.1:8000:8000 -v nativa-datos:/var/lib/nativa nativa:tienda-v2
curl --fail http://127.0.0.1:8000/healthz
```

Si está arrancando, repetir la consulta unos segundos después y revisar `docker logs --tail 80 nativa`. Conservar volumen y contenedor anterior detenido; no volver a crear la dueña. Probar usuarios, productos, fotos y solicitudes existentes antes de habilitar tráfico. Mantener 8000 sólo local y publicar únicamente mediante proxy HTTPS. Este documento no acredita que DNS, HTTPS o la actualización remota ya estén realizados.

Volver a código anterior con reservas nuevas puede permitir ventas que no las respetan: si fuera necesario retroceder, detener pedidos y ventas, revisar/liberar reservas desde esta versión y conservar pedidos nuevos antes del cambio. No restaurar un respaldo viejo sobre operaciones reales sin reconciliarlas.
