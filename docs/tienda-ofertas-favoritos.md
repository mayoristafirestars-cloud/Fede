# Nativa: ofertas por producto y favoritos

Continuación posterior a los puntos 1–10 y la identidad elegida. Código preparado y probado aquí; no se actualizó automáticamente el servidor de Hetzner.

## Ofertas de la tienda digital

Desde Tienda para vecinos se puede programar una oferta por producto, con título, precio unitario, inicio/fin en hora de Argentina y motivo interno. El precio promocional debe ser positivo y menor al habitual. Se registra precio/unidad de referencia, responsable, motivo y costo conocido al programar. No se publica automáticamente ningún producto.

No se permiten promociones superpuestas para un mismo producto. Se admiten hasta treinta días de duración y programación hasta noventa días por adelantado. El precio entra/sale de vigencia al consultar o enviar un pedido, sin necesitar un cron. Sólo se muestran títulos y precios vigentes, nunca motivos internos, costos ni nombres del personal.

Si cambia el precio habitual o la unidad frente a la referencia registrada, la oferta queda suspendida mientras difieran; no se muestra un precio tachado que ya no corresponda. El personal puede cancelarla y crear otra con las condiciones actuales. Desactivar el producto o quitarlo del catálogo también impide su compra pública. Vencimiento y cancelación no borran el historial.

Al programar un precio inferior al costo de referencia conocido se exige dueño, casilla de autorización expresa y motivo. La encargada puede programar otras ofertas, pero no autorizar esa excepción. Se usa costo de reposición si está informado, luego promedio y finalmente costo heredado positivo; desconocido no equivale a cero. Este control se aplica al momento de programar, no garantiza margen futuro ni reemplaza revisar costos y contribución.

## Precio, peso y presupuesto

Catálogo, detalle, carrito, solicitud y reemplazos usan el precio promocional vigente. El servidor revalida precio y unidad al recibir la solicitud. Si una oferta termina mientras el cliente todavía arma el carrito, debe revisar el precio actual antes de enviar.

Una solicitud ya recibida conserva su precio acordado aunque después venza o se cancele la promoción. El pesaje multiplica ese precio por la cantidad neta real, respetando el presupuesto máximo y la aprobación final. Cada reemplazo toma su precio/oferta actual y sigue sujeto a preferencias y aprobación. Los decimales por gramo se conservan antes de multiplicar; no se redondea anticipadamente el precio unitario a centavos.

La recompra trae precios y ofertas actuales, nunca vuelve a cobrar ni garantiza condiciones históricas. El ingreso del reporte de contribución ya refleja el precio de oferta: no se debe volver a restar el mismo descuento como gasto. El costo de mercadería sigue siendo el conocido/asignado; no disminuye por anunciar una promoción.

Las ofertas de esta entrega son para la tienda digital. No modifican el precio habitual del producto ni aplican descuentos automáticamente a ventas de mostrador. No hay cupones, acumulación de descuentos, tope por persona ni cupo de campaña independiente: disponibilidad física y franjas siguen limitando reservas. Los títulos deben describir honestamente la promoción; el sistema no verifica por sí solo afirmaciones escritas por el operador como porcentajes o superlativos. Las reglas de publicidad y precios deben revisarse antes del lanzamiento comercial.

## Favoritos en el dispositivo

El corazón guarda identificadores de productos en el navegador, sin registro ni envío de datos personales al servidor. Se conservan al recargar y pueden quitarse. No se sincronizan entre equipos; borrar datos del navegador o cerrar una sesión privada puede eliminarlos. Un producto que deja de publicarse no se expone por estar marcado: sólo aparecen los favoritos que el catálogo público devuelve.

Mis favoritos y Ofertas son filtros que pueden combinarse con categorías y búsqueda. Guardar un favorito no reserva mercadería, congela precios ni crea un pedido. La interfaz conserva etiquetas de accesibilidad y estados de selección. Los precios se revisan nuevamente al comprar.

## Verificación y actualización

Pruebas de backend: `python -m unittest discover -s tests -v`. Prueba de navegador: `APP_PYTHON=/ruta/python python tests/browser_tienda_ofertas.py`.

Se verifica programación, vigencia futura/expirada, solapamiento, cancelación, autorización bajo costo, cuatro decimales por gramo, snapshot del pedido, reemplazos, permisos, favoritos tras recarga y recompra con precio actual. Los datos e ilustraciones de las capturas pertenecen a bases temporales.

Paquete completo: Nativa-ofertas-y-favoritos.tar.gz. Incluye logo y funciones previas, sin bases, fotos del negocio ni claves. Para actualizar usar el procedimiento de respaldo y cambio de contenedor de `docs/tienda-puntos-4-10.md`, sustituyendo el paquete por este archivo y usando una carpeta/tag nuevos, por ejemplo `/opt/nativa-ofertas-v1` y `nativa:ofertas-v1`. Conservar `nativa-datos` y las cuentas existentes; no volver a crear la dueña. Antes del cambio hacer respaldo consistente y guardar una copia privada fuera del servidor. Mantener puerto 8000 local, DNS/HTTPS y permisos del proxy; esos pasos no se completan por descargar el paquete.
