# Etapa 1: definición del negocio y catálogo

## Qué se construyó

| Punto | Implementación | Estado de los datos reales |
|---|---|---|
| 1. Operación | Formulario de nombre, localidad, atención, pesaje, cobro y entrega | Pendiente de relevar con el dueño |
| 2. Personas | Registro de nombres y funciones previstas: dueño, encargado, cajero | Pendiente. No crea cuentas ni aplica permisos |
| 3. Equipos | Tipo, modelo, conexión y disponibilidad de computadora, balanza, lector e impresora | Pendiente. Sin integración ni compatibilidad demostrada |
| 4. Pagos | Selección de efectivo, transferencia, QR, débito y crédito | Pendiente. No conecta proveedores de pagos |
| 5. Fiscalidad | Contador, situación fiscal, comprobantes y revisión declarada | Pendiente. No emite comprobantes ARCA |
| 6. Conectividad | Estado de internet y plan de contingencia | Pendiente. No implementa modo offline |
| 7. Catálogo | Alta, edición, búsqueda y desactivación de productos | Listo para cargar productos reales |
| 8. Unidades | kg, g, unidad, atado, bolsa, bandeja y cajón | Configuradas. Sin asumir peso fijo por cajón |
| 9. Variantes | Variedad, calidad y presentación por ficha independiente | Listo para cargar |
| 10. Identidad | Código/PLU, alias y carga de foto validada | Listo para cargar |

El usuario todavía no conoce los datos del local: no se inventaron nombre, personas, equipos, régimen fiscal ni medios de pago. El progreso de la pantalla refleja relevamiento guardado, no certificación ni puesta en producción. Si un tipo de equipo no se utiliza, se debe precisar esa decisión en una iteración del relevamiento.

## Flujo inicial propuesto

Relevar operación y equipo → confirmar equipamiento y fiscalidad → cargar productos con unidad/calidad/código → continuar con costos y precios (puntos 11–14). Atención por mostrador/autoservicio, momento de pesaje y responsable de cobro se eligen en la configuración; no se impone una decisión desconocida.

La selección de personas sirve para planificar. Autenticación, permisos y auditoría corresponden a los puntos 60–62. Esta versión se usa en desarrollo local, sin exposición pública ni datos personales reales hasta incorporar esos controles. La página anterior se conserva en `/ventas`: sus documentos son internos y su módulo no adquiere validez fiscal por este cambio.

## Datos y compatibilidad

- Se conservó el ZIP original sin cambios y se extrajo el código al checkout para poder versionarlo.
- Migración aditiva e idempotente: conserva productos, stock, costos, precios y comprobantes. Los productos anteriores reciben `kg` como valor heredado; revisar su unidad antes del uso real porque el esquema anterior no la registraba.
- Los códigos y alias se comparan sin distinguir mayúsculas ni tildes. Un identificador no puede asignarse a dos productos, incluso si uno está inactivo. Los nombres descriptivos pueden repetirse para distintas variedades o calidades.
- Desactivar no borra datos ni historial. La edición del catálogo no cambia stock ni precios.
- Las fotos se validan, redimensionan y recodifican a JPEG, sin conservar metadatos del original. No se aceptan SVG, HTML o URLs externas. Se conservan archivos de fotos reemplazadas para no borrar recursos por error; su limpieza automática queda pendiente.
- Copias de desarrollo: incluir la base SQLite usando su API de backup y `backend/uploads/`. No incluir esos datos en Git.
- `CORONEL_DB_PATH` y `CORONEL_MEDIA_DIR` permiten bases y fotos aisladas en pruebas.

## Validación y próximos pasos

Las pruebas automatizadas cubren persistencia, validación fiscal del formulario, unidades, colisiones de alias/código, migración, conservación de stock/precios, desactivación y fotos. Las pruebas de navegador cubren configuración, recarga, búsqueda, creación/edición y vista móvil. No se probó hardware físico ni acceso fiscal.

Resultado de esta entrega: 10 pruebas de backend aprobadas con `unittest`; recorrido Playwright aprobado con Chromium del entorno, a 1440 px y 390 px, sin errores JavaScript. Las pruebas usaron bases temporales. Se verificó también el servidor de desarrollo y que la base del negocio no contiene productos o personas ficticias. El ZIP original conserva exactamente su contenido.

Antes de operar: completar datos reales, revisar unidades heredadas, construir precios y compras, autenticación, caja/cobros y emisión fiscal según el alcance acordado.
