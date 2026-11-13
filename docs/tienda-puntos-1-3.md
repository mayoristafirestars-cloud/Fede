# Tienda de Nativa: puntos 1, 2 y 3

Documento histórico de la primera entrega. Para el comportamiento actual, reservas, cobros manuales y actualización, ver [continuación: puntos 4–10](tienda-puntos-4-10.md).

## Implementado

1. Tienda móvil accesible por `/tienda`, sin instalar ni crear cuenta. En producción, `www.nativa.ar` y `nativa.ar` muestran la tienda en `/`; el host público no sirve gestión, login de personal ni APIs administrativas. `NATIVA_PUBLIC_HOSTS` permite configurar los hosts públicos.
2. Catálogo publicado expresamente por dueño/encargada, con foto del producto, precio por unidad comercial y cantidades rápidas/personalizadas. Búsqueda sin acentos, categorías, carrito persistente y control de cambios de precio/unidad. Ningún producto previo se publica automáticamente. No se agregaron productos ni fotos ficticias a la base real.
3. Solicitud invitada con estimado calculado en servidor; pesaje manual con bruto/tara/neto; detalle final y aprobación o pedido de revisión desde un enlace privado. Cada propuesta conserva los precios solicitados; el personal no puede modificar un importe ya aprobado desde el pesaje. Reintentos y versiones evitan duplicar solicitudes y aceptar una propuesta vieja.

## Uso

- En gestión, cargar nombre/foto/unidad desde Productos y precio desde Precios y costos.
- Ingresar con una cuenta de dueño o encargada y abrir **Tienda para vecinos**.
- Publicar los productos elegidos. Sólo pueden publicarse activos con precio positivo y foto existente.
- Abrir **Ver tienda**; el cliente elige cantidades, revisa su estimado y envía nombre/teléfono.
- El enlace de seguimiento contiene un secreto en el fragmento de URL, que no se envía en el query string ni se guarda en logs HTTP de acceso habituales. El backend guarda su hash, no el secreto. Cualquiera que posea el enlace puede consultar y responder esa solicitud: mantenerlo privado, no incluirlo en analítica ni compartir capturas con enlaces de solicitudes reales.
- Juliana ve las solicitudes en gestión, ingresa peso bruto/tara o cantidades enteras y envía una propuesta.
- El cliente actualiza su estado desde el enlace, ve pedido original/peso real/total y aprueba o pide revisión. El pedido sigue sin pago.

El carrito y, ante un envío interrumpido, la solicitud pendiente se conservan en el dispositivo para reintentar. El borrador pendiente incluye nombre y teléfono hasta que se recibe la respuesta exitosa o se descarta una solicitud inválida. No se solicitan datos de tarjeta ni se suscribe a publicidad. En dispositivos compartidos, cerrar o limpiar los datos del navegador según corresponda.

## Alcance real

Son solicitudes **sin reserva de mercadería y sin cobro**, no ventas completas. No se descuenta stock ni se emiten documentos fiscales. Todavía no hay franjas, reparto, sustituciones, reservas, conciliación de pagos, avisos automáticos o integración de balanza. El cliente debe volver al enlace y pulsar Actualizar estado; no se promete una notificación que no se envía.

No se implementó la instalación PWA: la compra ya funciona desde enlace; la instalación opcional pertenece a otra entrega. No hay cuenta de cliente obligatoria. El catálogo real puede estar vacío hasta que Nativa cargue/publica productos. Los dibujos y precios de las capturas de prueba pertenecen a bases temporales, no al catálogo del negocio.

## Seguridad y límites

- Las APIs públicas devuelven una lista explícita de campos. Costos, stock interno, proveedores y datos de responsables quedan privados.
- Las fotos públicas sólo se sirven por producto actualmente publicable/publicado; `/media` no se vuelve público.
- Los UUID identifican solicitudes y el secreto de 256 bits autoriza su lectura/respuesta. No hay un listado público ni acceso sólo por teléfono.
- Pesaje/publicación requieren dueño/encargada. El host público bloquea APIs administrativas aun con una cookie del personal.
- Precios, importes y cantidades se validan en servidor con Decimal. No se confía en un total calculado por el navegador.
- Se limita la creación a 10 solicitudes nuevas por minuto y dirección de cliente; los reintentos idénticos existentes no consumen cupo. Detrás de proxy, configurar confianza únicamente en la dirección del proxy real para obtener IPs correctas, y límites adicionales en el proxy antes de abrir tráfico. No confiar indiscriminadamente en X-Forwarded-For de Internet.
- Configurar HTTPS, hosts de proxy permitidos, renovación, respaldo externo y restauración antes de uso público. El límite de cuerpo debe fijarse en el proxy (por ejemplo 64 KiB para el JSON de pedidos; la carga administrativa de fotos necesita su propio límite de 5 MB).
- Validar identificación/contacto comercial, política de privacidad y conservación, términos, reclamos y procedimiento fiscal antes de captar clientes reales. El formulario informa la finalidad de coordinar la solicitud; eso no reemplaza la revisión completa del lanzamiento.
- Los enlaces vencen a los 30 días de crear la solicitud. No hay renovación/revocación individual en la interfaz en esta entrega; debe definirse la conservación de datos y el procedimiento de asistencia antes de operar a escala. Mantener privados los enlaces y la base.

## Verificación

Backend: `python -m unittest discover -s tests -v`. Navegador: `APP_PYTHON=/ruta/al/python python tests/browser_tienda.py` con Playwright y Chromium. Se prueban publicación selectiva, acceso público sin filtraciones, cantidades por unidad/peso, cambios de precio, tara, aprobación versionada, revisión, operaciones idempotentes, límite de solicitudes y separación de hosts.

El recorrido de navegador usa exclusivamente datos temporales y dibujos de prueba. Incluye pérdida de respuesta después de crear una solicitud, reintento sin duplicarla, carrito tras recarga, escritorio/móvil y pesaje/aprobación desde las dos interfaces.

## Actualización de la instalación de Hetzner

El código se preparó y probó en el entorno de desarrollo; no se actualizó automáticamente el servidor. El paquete `Nativa-puntos-1-3.tar.gz` contiene código y migración aditiva, sin bases ni fotos. Conserva usuarios y datos mediante el volumen existente `nativa-datos`. No ejecutar otra vez el alta del dueño.

Primero transferir el paquete desde la computadora al servidor como se hizo con el primer instalador. Dentro del servidor de Nativa, respaldar con el contenedor anterior todavía activo:

```bash
nativa_backup="antes-tienda-$(date +%Y%m%d-%H%M%S).tar.gz"
docker exec nativa python scripts/respaldo.py "/var/lib/nativa/$nativa_backup"
docker cp "nativa:/var/lib/nativa/$nativa_backup" "/root/$nativa_backup"
```

Guardar además una copia privada fuera del servidor. Con código extraído en una carpeta de versión nueva, construir antes de detener el servicio:

```bash
mkdir -p /opt/nativa-tienda-v1
tar -xzf /root/Nativa-puntos-1-3.tar.gz -C /opt/nativa-tienda-v1
cd /opt/nativa-tienda-v1
docker build -t nativa:tienda-v1 .
```

Después, en una ventana de mantenimiento sin operaciones concurrentes, generar un último respaldo consistente, detener y conservar el contenedor anterior. El nombre alternativo debe estar libre:

```bash
docker stop nativa
docker rename nativa nativa-anterior-tienda-v1
docker run -d --name nativa --restart unless-stopped --log-opt max-size=10m --log-opt max-file=3 -p 127.0.0.1:8000:8000 -v nativa-datos:/var/lib/nativa nativa:tienda-v1
curl --fail http://127.0.0.1:8000/healthz
```

Si todavía está arrancando, repetir la consulta unos segundos después y revisar `docker logs --tail 80 nativa`. No borrar volumen ni sobreescribir base con datos del entorno de desarrollo. DNS/HTTPS siguen siendo tareas aparte; no abrir 8000 a Internet. `www.nativa.ar` apunta al host público y `sistema.nativa.ar` al administrativo, ambos mediante proxy HTTPS al puerto local. Mantener los encabezados Host apropiados y evitar publicar el host administrativo mediante alias del sitio público.

Para volver al ejecutable anterior sin descartar datos: detener/renombrar el contenedor nuevo y volver a nombrar/iniciar el anterior. La migración agrega tablas sin alterar las anteriores; los pedidos web nuevos no se mostrarán en el código viejo. No restaurar una copia antigua encima de pedidos u operaciones reales sin revisar cómo conservarlos.
