# Análisis del sistema y decisiones para el Hito 1 (cartera)

*13 de noviembre de 2026. Reemplaza las preguntas P1 a P5: lo que se pudo averiguar se averiguó, y lo demás se resolvió con una decisión explícita que se puede revisar.*

Etiquetas: **[Observado]** en el código o en los datos del repositorio · **[Investigado]** en fuentes públicas (detalle en `investigacion/factupyme.md`) · **[Decisión]** tomada para avanzar · **[Verificar]** confirmar con un archivo real.

## 1. Qué es Coronel Sur, según sus propios datos

- Distribuidora de **Santa Rosa, La Pampa**: lo dicen el comprobante impreso y el teléfono 2954. [Observado]
- Rubros que aparecen en el inventario de prueba: **BAZAR, LIBRERÍA, COSMÉTICA**. Proveedores: Torre & Liva, Editorial Ruy Díaz, Reckoimport. [Observado]
- Clientes de tipo `minorista`, `mayorista` e `institucional`, sobre una base de unas 4.180 personas ("CS Más"). Ningún importador carga clientes. [Observado]
- Responsable Inscripto en IVA, con precios y costos cargados con IVA incluido. [Confirmado por el dueño]
- Casi todos esos rubros pagan **IVA del 21 %**, así que el supuesto único del 21 % es razonable. Excepción: los **libros**, que están exentos. [Investigado / Verificar si vende libros]

## 2. Qué es FactuPyme y qué exporta

| Tema | Hallazgo | Fuente |
|---|---|---|
| Producto | factupyme.com.ar, empresa de Santa Rosa (tel. 2954). Web, "100 % online". **Sin API pública ni base de datos local.** | [Investigado] |
| Factura electrónica | Sí, con QR de AFIP/ARCA. | [Investigado] |
| Cuenta corriente | **Sin evidencia pública** de saldos, recibos, imputaciones ni vencimientos. | [Investigado] |
| Inventario exportado | `Codigo` ("Cod: 35674"), `Descripción`, `Cantidad`, `Precio Venta`, `Precio Costo`, `Fecha Modificado` (dd-mm-aaaa), `Rubro`, `Proveedor`. **Sin alícuota de IVA.** | [Observado] en el importador y en el registro de importaciones |
| Ventas exportadas | Una **línea por producto**: `Fecha`, `Producto`, `Rubro`, `Precio Costo`, `Cant.`, `Subtotal`, `Cliente` (nombre). **Sin número de comprobante, sin CUIT, sin forma de pago.** | [Observado] |
| Formato | latin-1, separador `;`. Números mixtos: `1.500` (punto de miles) y `850.5` (punto decimal). La web muestra `1.234,56` y `2,00`. | [Observado] + [Investigado] |

## 3. Conclusiones

1. **No hay de dónde sacar la cuenta corriente.** Ni FactuPyme ni sus exportes tienen cobros, saldos ni vencimientos. Por lo tanto, **el Copiloto es la fuente de verdad de la cuenta corriente**, y FactuPyme sigue siendo el sistema que emite las facturas fiscales.
2. **La fuente confiable de las facturas emitidas es ARCA, en "Mis Comprobantes – Emitidos"**, no el informe de ventas de FactuPyme. Trae número, tipo, CUIT del cliente e importe total, y cualquier Responsable Inscripto lo puede descargar. El nombre exacto de cada columna puede variar según la versión, así que el mapeo es configurable. [Verificar con un archivo real]
3. **El saldo inicial lo tiene que declarar el dueño una sola vez,** con una planilla simple: CUIT, cliente, saldo y fecha. Ningún sistema lo tiene.

## 4. Decisiones del Hito 1

| # | Decisión | Por qué |
|---|---|---|
| D1 | **Saldo inicial** desde la planilla `data/plantillas/saldo_inicial.csv` (CUIT; Cliente; Saldo; Fecha; Vencimiento opcional; Teléfono opcional). Cada fila crea un documento SI. | Es la única forma de conocer lo adeudado hoy. |
| D2 | **Facturas y notas de crédito posteriores** desde ARCA Mis Comprobantes Emitidos (CSV o Excel). Solo se toman los comprobantes **de clientes con cuenta corriente** y **posteriores a la fecha de corte** del saldo inicial. | Las ventas de contado no generan deuda, y así no se cuenta dos veces lo que ya entró en el saldo inicial. |
| D3 | Un cliente tiene cuenta corriente si vino en el saldo inicial o si se la habilitan a mano. | Separa contado de cuenta corriente sin preguntar factura por factura. |
| D4 | **Vencimiento** = el del archivo si viene; si no, fecha de emisión más la condición de pago del cliente (por defecto **30 días**, configurable). | Supuesto común en distribución, que se puede cambiar por cliente. |
| D5 | Las **notas de crédito** quedan como "créditos sin imputar" del cliente y **se restan del saldo**. No se imputan solas a una factura. | El archivo de ARCA no dice a qué factura corresponde cada NC, y el diseño pide aprobación humana. |
| D6 | **"Vencido" y "parcialmente cancelado" no se guardan:** se calculan. En la base, el documento solo guarda `emitido` o `anulado`. | Un estado guardado puede quedar desactualizado; uno calculado, no. |
| D7 | Los **teléfonos** se guardan como contactos **sin consentimiento** hasta que se registre uno. No se usan para mensajes. | Ley 25.326. Los mensajes llegan recién en el Hito 3. |
| D8 | **Permisos:** todos ven la cartera; importar lo hacen admin y responsable de cobranza; ajustes y exportación de datos personales, solo admin. | Matriz de la sección 6 del diseño. Todavía no hay asignación de clientes por cobrador. |
| D9 | Se suma `openpyxl` para leer Excel. | ARCA y probablemente FactuPyme descargan en `.xlsx`. |

## 5. Qué conviene confirmar (no bloquea)

- Descargar **un** archivo de "Mis Comprobantes – Emitidos" de un mes y probarlo en la pantalla Importar. Si alguna columna tiene otro nombre, se corrige el mapeo (`backend/copiloto/mapeos/*.json`) sin tocar código.
- Si se venden **libros** (exentos de IVA), la ganancia sin IVA de esos productos va a quedar un poco baja.
