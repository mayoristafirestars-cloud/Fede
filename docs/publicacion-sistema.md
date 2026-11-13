# Publicación del sistema privado de Nativa

La web pública queda para otra etapa. El sistema aún no está publicado.
No hace falta comprar un dominio para la primera prueba: el proveedor asigna una dirección HTTPS.
Más adelante se puede conectar `sistema.<dominio-elegido>`; ningún dominio fue comprado ni verificado.

## Preparado en este repositorio

- `render.yaml`: un servicio Python con un solo proceso y disco persistente para SQLite y las fotos. El plan y el disco requieren revisar el precio vigente antes de contratar.
- `NATIVA_ENV=production`: protege páginas, documentos, fotos y API con la sesión del responsable. La sesión dura 30 minutos. El inicio de sesión, sus archivos estáticos, el estado de autorización y la comprobación mínima de salud son públicos.
- Cookie de sesión HttpOnly, Secure y SameSite Strict. Render debe terminar HTTPS; no exponer directamente el servidor HTTP a Internet.
- El primer dueño se crea desde consola; nadie puede registrarse como dueño por Internet. Las siguientes cuentas se agregan desde una sesión de dueño. Sin contraseñas predeterminadas.
- Un cajero no puede escribir fuera del módulo mostrador; dueño y encargada tienen acceso a la gestión. La instalación de desarrollo conserva el comportamiento local anterior y no debe exponerse a Internet.

## Pasos de puesta en marcha

1. Revisar y subir los archivos fuente a GitHub. La base, fotos reales y claves no se incluyen en Git.
2. Conectar el repositorio a Render y revisar el Blueprint, la región, el plan y el costo. No se contrató ningún servicio desde este entorno.
3. Para conservar la configuración real de Nativa, generar un respaldo local con `python scripts/respaldo.py /tmp/nativa-inicial.tar.gz`. No usar una base de prueba. Transferirlo mediante un canal privado; no publicarlo en GitHub.
4. Antes de habilitar el uso, restaurar la base como `/var/data/nativa.db` y las fotos en `/var/data/uploads` con el servicio detenido. Para la primera migración, el respaldo sólo contiene `nativa.db` y `uploads/`. Nunca reemplazar una base que ya tenga operaciones sin reconciliarlas.
5. Desde Shell del servicio, ejecutar `python scripts/crear_dueno.py`. Introducir nombre y clave ahí, nunca en el chat ni en argumentos del comando. Si ya existe un responsable, el comando se detiene.
6. Abrir la URL HTTPS del servicio, ingresar y comprobar configuración de Nativa y fotos. Sin sesión, verificar que `/api/gestion/productos` y `/media/` no entreguen datos.
7. Crear la cuenta de la encargada desde la sesión del dueño. Probar una operación controlada, cerrar sesión y volver a ingresar. Comprobar comportamiento de una sesión vencida antes del uso diario.
8. Configurar respaldos diarios y antes de actualizar: `python scripts/respaldo.py /var/data/nativa-FECHA.tar.gz` (usar un nombre nuevo). Descargar una copia privada fuera del servidor. El script es manual: no hay programación automática ni almacenamiento externo configurados.
9. Probar recuperación en una instalación aislada: detenerla, extraer el respaldo en una carpeta vacía, configurar las rutas, iniciar y comprobar usuarios, productos, stock y documentos. No restaurar sobre SQLite abierto ni olvidar archivos `-wal`/`-shm` de una instalación anterior.

El archivo de respaldo contiene datos del negocio y hashes de claves. Mantenerlo privado, con acceso restringido; no compartirlo como un documento comercial. Las fotos se conservan por identificador y no se eliminan al cambiarlas, de modo que el respaldo incluye las usadas en documentos históricos.

## Pendiente antes del uso real

Elegir cuenta/proveedor y aceptar su costo; configurar respaldo externo y verificar su restauración; revisar el uso real de tablet y balanza. La integración física de la Kretz Ouro, los cobros electrónicos y la facturación ARCA todavía no están implementados. Los comprobantes internos no son facturas fiscales.
