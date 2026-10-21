# Prompt: Copiloto de Caja para Distribuidora Coronel Sur

Copiá todo lo que está debajo de la línea y pegalo en una sesión nueva de Claude Code abierta sobre el repositorio de Coronel Sur.

---

## Contexto

Sos el desarrollador de **Coronel Sur**, el sistema de gestión de mi distribuidora, Distribuidora Coronel Sur. Quiero sumarle un módulo nuevo, el **Copiloto de Caja**, para cobrar mejor la cuenta corriente, controlar el riesgo de cada cliente y no perder plata con los cheques. Más adelante va a servir para detectar saldos a favor de impuestos.

Primero lo uso yo en mi negocio. Si funciona, lo vendemos a otros mayoristas. Por eso tiene que quedar prolijo y con datos medibles.

### Sistema actual (leelo antes de tocar nada)

El código está en `coronel-sur-render_1.zip`, en la raíz del repo. Descomprimilo en una carpeta `coronel-sur/` y borrá las carpetas basura con llaves en el nombre (`{backend/`, `{data/`, etc.), que vienen de un `mkdir` mal hecho.

- **Backend:** FastAPI + SQLite (`backend/main.py`, `backend/db/database.py`, `backend/db/schema.sql`, `backend/routers/facturacion.py`).
- **Tablas:**
  - `productos`;
  - `clientes`, con unos 4.180 registros del tipo `minorista | mayorista | institucional`; tiene `telefono` y `dni` pero no CUIT;
  - `comprobantes` (factura | presupuesto | nota_credito), con estado `activo | anulado | cobrado`;
  - `comprobante_items`;
  - `ventas_historicas`.
- **Importador de FactuPyme:** `backend/importador/importar_factupyme.py` lee CSV en latin-1, separados por `;`, con números en formato argentino. Archivos: `inventario.csv`, `ventas.csv`, `presupuestos.csv`.
- **Frontend:** una sola página, `frontend/templates/index.html`, con páginas que se cambian con `goPage('...')`.
- **Deploy:** Render (`render.yaml`).

### Problemas conocidos que tenés que resolver como parte del trabajo

1. **No existe la cuenta corriente.** No hay tabla de pagos ni de recibos, ni saldo por cliente.
2. **Las fechas se guardan como texto `dd-mm-YYYY`.** Así no se pueden ordenar ni calcular antigüedad de deuda. Migrá a ISO `YYYY-MM-DD` sin perder los datos existentes.
3. **No hay login.** Antes de guardar deudas y teléfonos de clientes hace falta autenticación: usuario y contraseña con hash, sesiones y dos roles (`admin` y `cobrador`).
4. **SQLite en Render se borra en cada deploy** si no hay disco persistente. Proponé y dejá configurado un disco persistente de Render, o la migración a PostgreSQL. Explicame la opción elegida y su costo.
5. **El número de comprobante** se genera con `COUNT(*)` y se repite si hay anulados o pedidos simultáneos. Corregilo con una secuencia.

## Qué quiero construir (por fases)

Trabajá **una fase por vez**. Al terminar cada una:
- mostrame cómo probarla;
- corré los tests;
- hacé commit con un mensaje claro;
- esperá mi OK antes de seguir.

### Fase 1: Cuenta corriente y tablero de caja (sin integraciones externas)

1. **Modelo de datos nuevo:**
   - `movimientos_cc`: id, cliente_id, fecha, tipo (`factura | nota_credito | recibo | ajuste | saldo_inicial`), comprobante_id (opcional), importe con signo (débito positivo, crédito negativo), vencimiento, observaciones y usuario.
   - `recibos` con sus `recibo_medios`: efectivo, transferencia, ECHEQ, cheque físico, Mercado Pago o retención sufrida.
   - Imputación de recibos contra facturas: total, parcial o a cuenta.
   - Campo `cuit` en `clientes`, con validación del dígito verificador.
   - Condición de pago por cliente: días de plazo, límite de crédito y un campo para bloquear la venta.
2. **Al emitir una factura**, que se genere el débito en la cuenta corriente con vencimiento según la condición del cliente. Al anularla, que se revierta.
3. **Saldos iniciales:** necesito importar lo que hoy me deben mis clientes.
   - Primero averiguá si FactuPyme exporta la cuenta corriente o un informe de saldos de clientes. Si no podés saberlo, preguntame.
   - Mientras tanto, hacé un importador de CSV simple (cliente, CUIT, saldo, fecha del comprobante más viejo impago), con una vista previa antes de confirmar.
4. **Antigüedad de deuda por cliente:** al día, 1-30, 31-60, 61-90 y más de 90 días.
5. **Tablero de caja (página nueva "Caja"):**
   - Total a cobrar y cuánto está vencido.
   - Días promedio de cobro (DSO) del mes y su evolución.
   - Lo que se cobró esta semana.
   - Los 10 clientes con más deuda vencida.
   - Clientes que pasaron su límite de crédito.
   - **"A quién cobrar hoy":** lista ordenada por monto vencido × antigüedad, con el último contacto y la última promesa de pago.
6. **Gestiones de cobranza:**
   - Registrar cada contacto: fecha, canal, resultado, promesa de pago con fecha y monto, y notas.
   - Avisar cuando una promesa de pago no se cumplió.
7. **Mensajes de WhatsApp asistidos (envío manual):**
   - Para cada cliente, generar el texto del recordatorio con plantillas según la antigüedad: amable, firme o último aviso.
   - Botón que abre `https://wa.me/<teléfono>?text=<mensaje>`. El envío lo hace una persona; en esta fase no hay envío automático.
   - Normalizar los teléfonos argentinos al formato internacional (+54 9 ...) y marcar los que no se puedan corregir.
8. **Cartera de cheques:**
   - Registrar los ECHEQ y cheques recibidos: banco, número, librador, CUIT del librador, fecha de pago, importe y estado (`en_cartera | depositado | endosado | rechazado | acreditado`).
   - Vencimientos de la semana.
   - Si un cheque se rechaza, que vuelva a la cuenta corriente del cliente como débito, con los gastos.
9. **Exportar a Excel o CSV** el resumen de cuenta de cada cliente y la antigüedad de deuda.

**Criterio de aceptación:** cargo los saldos iniciales y veo en el tablero cuánto me deben, quién me debe más y hace cuánto. Registro un cobro con un ECHEQ y el saldo baja. Mando un recordatorio por WhatsApp en dos clics.

### Fase 2: Riesgo de clientes con datos públicos del BCRA

1. Integrar las **APIs públicas del BCRA** consultando por CUIT:
   - Central de Deudores: situación del cliente en el sistema financiero.
   - Cheques rechazados.
   - Verificá en la documentación oficial (api.bcra.gob.ar) los endpoints, los límites de uso y las condiciones antes de implementarlo.
2. Guardar las consultas en caché (una por cliente cada 7 días como máximo) y registrar la fecha de cada una.
3. **Semáforo de riesgo por cliente** (verde, amarillo, rojo), combinando:
   - la situación en el BCRA;
   - los cheques rechazados recientes;
   - mi propia historia de cobro con ese cliente: atraso promedio, promesas incumplidas, cheques rechazados conmigo.
   - Mostrá siempre **por qué** tiene ese color.
4. **Alertas:**
   - "Este cliente empeoró su situación en el BCRA".
   - "Pasó el límite de crédito".
   - "Tiene un cheque rechazado en el sistema".
   - Aviso al facturarle a un cliente en rojo (no lo bloquea, salvo que yo active el bloqueo).

### Fase 3: Cobranza con IA y WhatsApp automático (con aprobación humana)

1. Integrar la **API de WhatsApp Business (Cloud API de Meta)**.
   - Antes de programar, revisá y explicame las reglas vigentes: plantillas aprobadas, ventana de 24 horas, costo por mensaje en Argentina y política sobre asistentes de IA.
   - Todas las credenciales van en variables de entorno, nunca en el código.
2. **Recordatorios programados** según la antigüedad y la condición de cada cliente, con plantillas aprobadas por Meta. Cada envío va a una **cola de aprobación**: yo los apruebo en bloque o uno por uno. Nada sale sin aprobación salvo que yo lo active por cliente.
3. **Agente de IA (API de Anthropic, modelo Claude):**
   - Lee las respuestas de los clientes y propone la siguiente acción: registrar una promesa, avisar que un pago ya se hizo, pasar el caso a una persona, etc.
   - Lee **comprobantes de pago** que llegan como foto o PDF (transferencia, ECHEQ, Mercado Pago), extrae monto, fecha, CUIT y número de operación, y propone el recibo y su imputación **para que yo lo confirme**.
   - Redacta el mensaje en el tono adecuado al historial del cliente.
   - Nunca inventa saldos: todo número que use sale de la base.
   - Guardá un registro de cada sugerencia de la IA y de lo que hizo la persona (aceptó, editó o rechazó), para medir la precisión.
4. **Métricas del piloto** (tienen que quedar en el tablero):
   - DSO antes y después;
   - porcentaje de deuda vencida;
   - plata cobrada atribuible a gestiones del sistema;
   - promesas cumplidas;
   - precisión de la IA leyendo comprobantes.

### Fase 4: Saldos a favor de impuestos (detección; el trámite lo hace mi contador)

1. Importar los archivos que hoy bajo a mano:
   - retenciones y percepciones sufridas (ARCA "Mis Retenciones");
   - retenciones bancarias de Ingresos Brutos (SIRCREB);
   - percepciones de IIBB de las facturas de compra;
   - el resumen de las declaraciones juradas de IIBB e IVA.
   - Antes de programar el parser, pedime ejemplos reales de cada archivo.
2. Conciliar por período y por jurisdicción: cuánto me retuvieron, cuánto me correspondía pagar y **cuánto saldo a favor se va acumulando**.
3. Reporte para el contador:
   - saldo a favor por impuesto y jurisdicción;
   - evolución mensual;
   - alícuota efectiva contra la nominal;
   - pérdida por inflación estimada.
   - Agregar el texto: "Revisar con contador matriculado; no constituye asesoramiento fiscal".

## Reglas de trabajo

- **Mantené el stack:** FastAPI, Python 3.11 y el mismo estilo de código (español, funciones simples, comentarios cortos). Si cambiás algo de arquitectura (Postgres, por ejemplo), explicame antes por qué.
- **Migraciones seguras:** antes de modificar la base, hacé un backup automático. Cada migración tiene que poder correrse dos veces sin romper nada.
- **Plata en centavos enteros o `Decimal`,** nunca `float`, para importes nuevos. Mostrá los importes en formato argentino: `$ 1.234.567,89`.
- **Tests (pytest) obligatorios para:**
  - el cálculo del saldo y de la antigüedad;
  - las imputaciones parciales;
  - la anulación de facturas;
  - el cheque rechazado;
  - la normalización de teléfonos;
  - la validación de CUIT.
- **Datos personales (Ley 25.326):**
  - Los teléfonos y las deudas solo los ve un usuario logueado.
  - Logs sin datos sensibles.
  - Opción de dar de baja a un cliente de los mensajes.
- **No envíes mensajes reales ni consultes APIs externas** con datos de clientes sin que yo lo confirme. Para las pruebas usá datos de ejemplo.
- **Al final de cada fase,** dame un resumen corto: qué se hizo, cómo probarlo, qué quedó pendiente y qué decisiones necesito tomar.

## Empezá así

1. Descomprimí y ordená el proyecto. Corré la app localmente y confirmá que funciona como hoy.
2. Leé todo el código y el esquema. Respondeme en 10 líneas cómo está armado y qué riesgos ves.
3. Proponeme el modelo de datos de la Fase 1 (tablas y campos) y **esperá mi OK** antes de implementarlo.
