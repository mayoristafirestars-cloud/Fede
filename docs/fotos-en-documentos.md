# Fotos por producto en remitos y comprobantes

Cada renglón toma la imagen de su producto, no una foto común para todo el documento. La ficha del catálogo permite cargar JPG, PNG o WebP, que el servidor valida y convierte a JPEG.

## Flujo

1. Ir a Productos, editar la ficha y cargar la foto que corresponda a esa variedad/presentación.
2. Registrar la venta. La referencia de imagen se conserva en cada renglón de la venta y del módulo anterior.
3. En Mostrador, abrir **Ver comprobante con fotos** o **Ver remito con fotos**.
4. Usar **Imprimir / Guardar PDF**. Se esperan las imágenes antes de imprimir. El remito muestra fotos, productos y cantidades; el comprobante también muestra precios e importes originales.

Las fotos no se modifican al cambiar posteriormente la ficha del producto. Los archivos anteriores se conservan. Los documentos anteriores a esta función no reciben una imagen actual de forma silenciosa.

## Si falta una imagen

La vista muestra **Foto pendiente** y la lista de productos afectados. Se puede seguir registrando ventas, pero la impresión del documento completo queda bloqueada hasta completar sus imágenes. La impresión por Ctrl+P también muestra un aviso en lugar del documento incompleto. No se usa una foto genérica como si fuera la del producto.

Cargar la foto en el catálogo y pulsar **Completar fotos desde catálogo** como dueño/encargada. Esto agrega una asociación posterior auditada con fecha y responsable; conserva la referencia original, cantidades, precios y stock. El complemento se hace solo para imágenes faltantes o archivos no disponibles; no reemplaza una imagen histórica válida con la foto actual por haber cambiado el catálogo.

Los renglones antiguos sin producto identificado no se vinculan por coincidencia de nombre. No se inventan imágenes históricas ni se alteran importes para resolver una foto pendiente. Si una copia de respaldo tiene la base pero no los archivos de fotos, deben restaurarse también esos archivos o completarse explícitamente las referencias faltantes.

## Formatos y límites

- La vista y el PDF usan fotos pequeñas por renglón, con nombre, cantidad y unidad cuando estaban registradas. Se conserva la proporción de la imagen y se evitan cortes de renglón entre páginas.
- El documento identifica a Nativa desde su configuración, mantiene número y fecha y muestra estado y cobro. Las cantidades e importes son originales; las devoluciones/correcciones permanecen informadas en el sistema.
- Los documentos son **internos y no válidos como factura fiscal**. Agregar fotos no implementa emisión ARCA ni constituye un comprobante fiscal.
- Imprimir desde el navegador o guardar PDF no conecta la impresora de la balanza. El soporte de imágenes y el protocolo de la Kretz Ouro todavía requieren verificación de la variante y pruebas físicas.
- La correspondencia visual depende de asignar la foto correcta a cada ficha. El sistema no decide mediante reconocimiento de imagen si una foto es la fruta o variedad correcta.
- Las imágenes de prueba son sintéticas y solo se usan en bases temporales. No se cargaron productos o fotos ficticias en el catálogo real de Nativa.

## Verificación

```bash
python -m unittest discover -s tests -p test_documentos.py -v
python tests/browser_documentos.py
```

Se comprueban imágenes distintas por producto, conservación al cambiar fotos del catálogo, complemento posterior auditado, permisos, faltantes, archivos perdidos, remito sin precios, escape de texto, impresión y PDF con imágenes, vista del módulo anterior y pantalla móvil. El navegador usa el puerto 8006 y archivos temporales. Genera `/tmp/nativa-comprobante-fotos-prueba.pdf` y una captura de prueba; estos archivos no representan documentos reales del negocio.

Resultado de esta entrega: **97 pruebas de backend aprobadas** (9 específicas de fotos/documentos y 88 anteriores), recorrido de documentos aprobado y recorrido completo del mostrador aprobado. El PDF de prueba contiene las dos imágenes de producto; también se verificó que la impresión quede bloqueada cuando falta una foto y se habilite después de completarla con auditoría.
