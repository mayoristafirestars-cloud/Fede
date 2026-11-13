# FactuPyme: qué ofrece realmente (investigación al 13/11/2026)

Convención: **[CONFIRMADO]** = lo dice una fuente pública citada. **[INFERENCIA]** = deducción razonable, no verificada. **[NO ENCONTRADO]** = se buscó y no hay información pública.

Resumen honesto: FactuPyme tiene muy poca presencia pública. Hay una landing page, una pantalla de login y dos imágenes promocionales con capturas de la app. **No encontramos manual, centro de ayuda, canal de YouTube, foros, API documentada ni listado de columnas de exportación.** Casi todo lo que pide el módulo de cuenta corriente (puntos 2, 3 y 6) queda en **NO ENCONTRADO** y habrá que verificarlo con un archivo real exportado por el cliente o con una cuenta demo.

---

## 1. Qué es FactuPyme y cuál de los productos con ese nombre corresponde

### El que corresponde: factupyme.com.ar (La Pampa, Argentina)
- **Sitio:** https://www.factupyme.com.ar/ . Título: "FactuPyme – Gestión y Facturación online". [CONFIRMADO]
- **Proveedor:** el sitio solo dice "© FactuPyme", "Ubicación: La Pampa, Argentina" y "Teléfono +54 (2954) 680842", con WhatsApp al mismo número (https://api.whatsapp.com/send?phone=542954680842). No figura razón social, email ni CUIT del proveedor. [CONFIRMADO] La característica 2954 es la de Santa Rosa, La Pampa, la misma ciudad que Coronel Sur. [INFERENCIA, muy probable: es un desarrollador local]
- **Dominio:** registrado en NIC Argentina el 2018-03-10 y vence el 2027-03-10, con DNS en AWS Route 53 (RDAP: https://rdap.nic.ar/domain/factupyme.com.ar). [CONFIRMADO] Un sitio de listados de dominios (https://www.websitescrawl.com/domain-list-10560) lo marca como "Removed", pero el sitio responde con normalidad al 13/11/2026. [CONFIRMADO, lo verificamos nosotros]
- **Escritorio o nube:** es 100% web. La landing dice "100% Online", "Sin instalación", "Usuarios ilimitados", "Copias de seguridad automáticas" y "Desde el celular o la computadora". [CONFIRMADO] La app vive en https://factupyme.com.ar/inventario/ y redirige a `login.php` ("Acceso a Factupyme": usuario, clave y reCAPTCHA). Los headers HTTP muestran `Server: Apache/2.4.69 (Amazon Linux)` y `X-Powered-By: PHP/8.5.12`. [CONFIRMADO, lo observamos con curl] Por lo tanto **no hay base de datos local** (Access, SQLite o Firebird) en la PC del cliente. El backend es PHP alojado en AWS, probablemente con MySQL o MariaDB, pero el motor no está publicado. [INFERENCIA]
- **Versiones y planes:** no hay números de versión públicos. Hay dos planes, "Plan PyME" (factura, stock y ventas, usuarios ilimitados, factura electrónica AFIP, soporte por WhatsApp) y "Plan Negocio" (agrega tienda online, módulo restaurante, "reportes", integración con balanzas y backups automáticos). Los dos cuestan "$0 el primer mes". "El valor de los meses siguientes lo confirmamos por WhatsApp". **Los precios no son públicos.** [CONFIRMADO]
- **Público objetivo:** comercio minorista ("Almacén, Ferretería, Indumentaria, Kiosco, Jugueterías, Café y restaurante"), más gimnasios y restaurantes. Un banner de la propia web dice "Ideal para almacenes, kioscos, bazares, regalerías" (https://factupyme.com.ar/assets/tu_negocio_con_FactuPyme.jpg). [CONFIRMADO] La web no menciona distribuidoras mayoristas.
- **Factura electrónica:** "Factura con QR AFIP, ticket 80 mm y comprobantes listos para imprimir", "Emisión automática con QR AFIP" y "Certificados AFIP y QR en comprobantes". [CONFIRMADO] Esto implica autorización de comprobantes con CAE por web service de ARCA/AFIP. [INFERENCIA fuerte: el QR AFIP exige CAE]
- **Tipos de comprobante (A, B, C, NC, ND, remito, presupuesto, recibo):** [NO ENCONTRADO]. La web no los enumera. Como Coronel Sur es Responsable Inscripto, se infiere que emite A y B. Que emita NC/ND, remitos, presupuestos o recibos no está confirmado públicamente.

### Homónimos (para no confundirse)
- **FACTUPYME de Querry S.A. (Málaga, España)**, https://www.factupyme.com/ . Es un programa con licencia (86 €, 192 € la versión de 5 usuarios, más un "Módulo e-Factura" de 39 €; https://www.factupyme.com/10-factupyme). Teléfono 900714109 e info@factupyme.com. No menciona AFIP, CUIT ni ARCA, y dice "exportar los datos a los formatos más habituales en ofimática" (https://www.factupyme.com/content/12-que-es-factupyme). **No es el de Coronel Sur.** Ojo con la documentación de este producto, porque no aplica.
- **FactorPyme / FACTORPYME S.A.** (CABA, CUIT 30-71861784-3, constituida en 2024; https://factorpyme.com.ar/ , https://indicadores.ar/empresa/30718617843). Es una plataforma de finanzas y factoring, no un sistema de facturación. No tiene relación.
- Otros nombres parecidos del mercado argentino: e-pyme, Nexo Pymes, Gestar Pyme, ERPyme y TusFacturasAPP. Son productos distintos.

**Conclusión:** el producto que usa Coronel Sur es casi con certeza **factupyme.com.ar**, por la coincidencia de nombre, provincia, característica telefónica 2954 y factura AFIP.

## 2. Cuenta corriente de clientes
- Lo confirmado es poco. La web habla de "Clientes", "Historial completo de operaciones", "Clientes y proveedores: Historial y mejores precios" y, en el módulo restaurante, "caja" y "cierre de mesa con el medio de pago". En el módulo gimnasio menciona "cobros". [CONFIRMADO]
- **Cuenta corriente, saldos, recibos, imputación, resumen de cuenta, deudores, vencimientos y condición de pago:** [NO ENCONTRADO]. Ni la web ni las capturas mencionan cuenta corriente. Tampoco hay reportes públicos con nombres como "Saldos de clientes" o "Deudores".
- [INFERENCIA] El "historial de operaciones" por cliente sugiere que existe al menos un listado de ventas por cliente. No asumir que FactuPyme imputa cobros contra facturas: es posible que el módulo que construimos tenga que ser la fuente de verdad de los cobros.

## 3. Exportación, API y base de datos
- Confirmado: "Stock, clientes y ventas: historial completo de operaciones, control de inventario en tiempo real y **reportes descargables**". [CONFIRMADO] **No se especifica el formato** (Excel, CSV o PDF). [NO ENCONTRADO]
- Columnas, encoding y separador: [NO ENCONTRADO].
- **API pública:** [NO ENCONTRADO]. El login usa `verify.php` por AJAX con reCAPTCHA (https://factupyme.com.ar/inventario/icaptcha.script.js), así que no hay forma práctica de automatizar la extracción. [CONFIRMADO / INFERENCIA]
- **Acceso a base de datos:** no aplica localmente, porque es SaaS. [INFERENCIA fuerte]
- **Backups:** "Copias de seguridad automáticas" y "Backups automáticos" en el plan Negocio. El formato y si el cliente puede descargarlos no están publicados. [CONFIRMADO / NO ENCONTRADO]
- Migración: "Si ya usás otra solución, te ayudamos a migrar tus datos". Indica que el proveedor maneja importaciones, posiblemente desde planillas. [CONFIRMADO / INFERENCIA]

## 4. Maestro de clientes
- Existe un módulo de clientes con historial. [CONFIRMADO] Hay un "Plano/mesa" con nombre de cliente en el módulo resto (captura en https://factupyme.com.ar/assets/factupyme_resto.jpg).
- Los campos CUIT, condición IVA, teléfono, email, dirección, lista de precios y límite de crédito: [NO ENCONTRADO]. [INFERENCIA] Para emitir Factura A con CAE el sistema necesita al menos CUIT o tipo y número de documento, y condición frente al IVA del receptor. Límite de crédito: sin evidencia.
- Exportación de clientes: [NO ENCONTRADO].

## 5. Productos e inventario
- Lo que se ve en la captura del listado "Listado de Productos/Servicios" (banner https://factupyme.com.ar/assets/tu_negocio_con_FactuPyme.jpg) [CONFIRMADO visualmente]:
  - **Columnas:** `Código` (EAN de 13 dígitos, ej. 7792993339320), `Imagen`, `Modificado` (fecha dd/mm/aaaa), `Producto` (descripción en mayúsculas), `Rubro`, `Estado` ("Activo"), `Web` ("Si", publicado en la tienda) y `Stock` (con 2 decimales y coma decimal, ej. "2,00").
  - **Filtros:** buscar por nombre, Código, Rubros, Subrubro, Temporada, Marca y Proveedor. Botón "+ Agregar producto rápido".
- Otras funciones publicitadas: "Precios por rubro y actualización masiva", "Alta de artículos y listas de precios", lector de código de barras e integración con balanzas. [CONFIRMADO]
- Alícuota de IVA por producto, precio con o sin IVA y costo: [NO ENCONTRADO]. [INFERENCIA débil] La captura del módulo resto muestra un ticket con "Neto $ 23.750,00 / IVA $ 4.121,90 / TOTAL $ 23.750,00". Como 4.121,90 = 23.750 × 21/121, el precio de venta parece cargarse **con IVA incluido** y el sistema desglosa el 21%. El rótulo "Neto" mostrando el total con IVA sugiere que esa pantalla rotula de forma imprecisa.
- **Formato numérico:** formato argentino, con punto de miles y coma decimal ("3.750,00"). Cualquier exportación probablemente siga ese formato. [INFERENCIA]

## 6. Informe de ventas e informe de presupuestos
- Los "reportes" están en el Plan Negocio y hay "Stock y ventas" con "reportes descargables". [CONFIRMADO]
- Nombres de informes, columnas, número y tipo de comprobante, CUIT, desglose de IVA y forma de pago: [NO ENCONTRADO]. La única evidencia de forma de pago es "cierre de mesa con el medio de pago" (resto), lo que sugiere que las ventas registran el medio de pago. [INFERENCIA]
- La existencia de un "Informe de presupuestos" no está confirmada públicamente.

## 7. Manuales, soporte y canales
- Manual o centro de ayuda: [NO ENCONTRADO].
- YouTube, Instagram o Facebook: [NO ENCONTRADO] (búsquedas sin resultados).
- Soporte: WhatsApp y teléfono +54 2954 680842, más un formulario de contacto en la landing (https://www.factupyme.com.ar/#contacto). [CONFIRMADO]
- La barra de menú visible en las capturas tiene íconos de gráfico/dashboard, resto, cajas/stock, clientes, camión (proveedores o envíos), bolsa, carrito (ventas), calculadora, maletín, gráfico de barras (reportes), documentos y configuración. Los rótulos no se ven, así que el mapeo exacto es [INFERENCIA].

---

## Implicancias para el importador de cuenta corriente
1. No hay API ni base local. La única vía realista es **pedir al cliente un archivo exportado** desde la UI ("reportes descargables") o una captura o PDF. Hay que diseñar el importador tolerante: detectar el delimitador (`,` `;` o tab), el encoding (UTF-8 con o sin BOM, o Windows-1252), números con formato `1.234,56` y fechas `dd/mm/aaaa`, y mapear encabezados por nombre flexible.
2. No asumir que FactuPyme tiene recibos o imputaciones. Hay que prever que nuestro módulo registre los cobros y use FactuPyme solo como fuente de comprobantes de venta (facturas, NC y, si existen, remitos).
3. Para conciliar con ARCA, los comprobantes se pueden validar contra "Mis Comprobantes" de ARCA, que ofrece una exportación oficial independiente de FactuPyme. Esto es un respaldo para tener números, tipos, CUIT e IVA garantizados.
4. Primera acción concreta: conseguir **un archivo real** de cada reporte (ventas, clientes, productos) para fijar las columnas, y preguntar por WhatsApp de FactuPyme qué formatos exporta.

### Fuentes
- https://www.factupyme.com.ar/ (landing, texto completo leído)
- https://factupyme.com.ar/inventario/login.php ; https://factupyme.com.ar/inventario/icaptcha.script.js
- https://factupyme.com.ar/assets/tu_negocio_con_FactuPyme.jpg ; https://factupyme.com.ar/assets/factupyme_resto.jpg
- https://rdap.nic.ar/domain/factupyme.com.ar
- https://www.websitescrawl.com/domain-list-10560
- https://www.factupyme.com/ ; https://www.factupyme.com/10-factupyme ; https://www.factupyme.com/content/12-que-es-factupyme (homónimo español)
- https://factorpyme.com.ar/ ; https://indicadores.ar/empresa/30718617843 (homónimo financiero)
