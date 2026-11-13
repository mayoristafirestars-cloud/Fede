# Prompt: Mejora de Coronel Sur — Hito 0 (base segura) e Hito 1 (cartera)

**Antes de pegarlo:** completá la sección "Respuestas del dueño". Lo que no sepas, dejalo como `PENDIENTE` y el agente trabaja sin ese dato o te pregunta. Después copiá todo lo que está debajo de la línea en una sesión nueva de Claude Code abierta sobre este repositorio.

---

## Rol y objetivo

Actuá como desarrollador senior responsable de Coronel Sur, el sistema de gestión de mi distribuidora (Santa Rosa, La Pampa).

Tu tarea es implementar los **Hitos 0 y 1** del diseño que está en `copiloto_caja/DISENO_COPILOTO_CAJA.md`. **Leelo completo antes de empezar.** Ahí están el diagnóstico, el modelo de datos, los estados, los roles y las pruebas de aceptación. Si algo de este prompt contradice el diseño, avisame antes de decidir.

- **Hito 0:** dejar el sistema seguro, ordenado y con pruebas.
- **Hito 1:** poder importar, validar y consultar la cartera de cuentas corrientes.

No implementes nada de los hitos 2 en adelante (conciliación con extractos, mensajes, IA, tablero completo). Eso va en otro trabajo.

## Respuestas del dueño (completar)

```
P1. Dónde se lleva hoy la cuenta corriente:            PENDIENTE
P2. Informes que exporta FactuPyme (y ejemplos):       PENDIENTE
    Ubicación de los ejemplos anonimizados:            PENDIENTE (ej: data/ejemplos/)
P3. Banco/billetera principal y formato de extracto:   PENDIENTE   (se usa recién en el Hito 2)
P4. Usuarios y roles que van a usar el sistema:        PENDIENTE
P5. ¿Render en producción? ¿Disco persistente?:        PENDIENTE
P6. Autorización para trabajar en rama:                SÍ — rama: mejora/h0-h1
```

## Reglas de trabajo (obligatorias)

1. **Rama:** trabajá en `mejora/h0-h1`. Hacé un commit por paso, con mensajes claros en español. No hagas push a `main` y no despliegues nada.
2. **Sin datos reales ni servicios externos:**
   - No uses datos reales de clientes en pruebas ni en commits; usá datos inventados.
   - No te conectes a Render, bancos, ARCA, WhatsApp, BCRA ni a ninguna API de IA.
   - No contactes a nadie.
3. **Nada de bases de datos ni secretos en el repo:** no subas `.db`, `.env`, contraseñas ni claves. Los secretos van en variables de entorno.
4. **Cambios mínimos y revisables:**
   - Mantené FastAPI, Python 3.11 y el estilo actual: código en español, funciones simples, comentarios cortos.
   - No reescribas lo que funciona sin un motivo.
   - Si cambiás una tecnología, explicá por qué antes de hacerlo.
5. **No romper lo que anda:** la emisión, el historial y la anulación de comprobantes tienen que seguir funcionando igual para el usuario. Antes de tocar nada, escribí pruebas que fijen ese comportamiento.
6. **Plata:**
   - Importes nuevos en **enteros de centavos**, con cálculos en `Decimal` y redondeo `ROUND_HALF_EVEN` documentado. Nunca `float`.
   - Mostrá los importes en formato argentino: `$ 1.234.567,89`.
7. **Nunca borrar historia financiera:** las correcciones se hacen con ajustes o reversos vinculados.
8. **Ser honesto con el estado:**
   - Al final de cada paso, informá qué quedó **terminado y probado**, qué quedó **solo diseñado** y qué está **pendiente**.
   - No digas que una prueba pasó si no la ejecutaste.
   - Mostrá la salida de `pytest`.
9. **Cuándo frenar y preguntarme:**
   - si un dato imprescindible está `PENDIENTE` y bloquea;
   - si encontrás algo que contradice el diseño;
   - antes de cualquier migración que transforme datos existentes.

---

## HITO 0 — Base segura

### Paso 0.1 — Ordenar el proyecto
- Descomprimí `coronel-sur-render_1.zip` en la raíz del repo, manteniendo `backend/`, `frontend/`, `data/`, los `.bat`, `render.yaml` y `requirements.txt`.
- Borrá las carpetas basura con llaves en el nombre (`{backend/`, `{data/`, etc.).
- Mové la versión anterior (`database/`, `importador/` y `data/coronel_sur.db`) a `legacy/` con un `README` que explique que no se usa. No se borra: queda en la historia de git.
- Confirmá que `.gitignore` excluye `*.db`, `.env`, `venv/` y `data/csv_originales/`.
- Fijá versiones en `requirements.txt` y sumá un `requirements-dev.txt` con `pytest` y `httpx`.
- **Verificación:** la app levanta con `python backend/main.py` y la emisión de comprobantes funciona igual que antes.

### Paso 0.2 — Pruebas de caracterización
- Con pytest y el `TestClient` de FastAPI, sobre una base temporal (nunca la real), probá el comportamiento actual:
  - crear factura y presupuesto;
  - que el stock baje con la factura y no con el presupuesto;
  - el historial;
  - el detalle;
  - la anulación con reversión de stock;
  - el error al anular dos veces.
- Estas pruebas tienen que seguir pasando hasta el final.

### Paso 0.3 — Migraciones versionadas y respaldo
- Creá `backend/db/migraciones/` con archivos SQL numerados (`0001_...sql`) y una tabla `schema_migraciones`. Un ejecutor los aplica al arrancar, en orden, una sola vez y dentro de una transacción.
- **Antes de aplicar cualquier migración, hacé un respaldo automático** de la base con la API `backup` de sqlite3, con nombre fechado.
- Sumá `scripts/respaldar.py` y `scripts/restaurar.py`, más una prueba que restaure un respaldo y verifique que los datos quedan iguales.
- Escribí el SQL lo más portable posible a PostgreSQL. No migres a Postgres en este hito.
- **Render:** proponé en `render.yaml` un disco persistente montado donde vive la base, y la variable `DB_PATH`. Explicame el costo y la alternativa con Postgres. **No despliegues.**

### Paso 0.4 — Importes y fechas
- **Frená y mostrame el plan antes de ejecutar esta migración.**
- Migrá `comprobantes` y `comprobante_items`:
  - sumá columnas en centavos enteros, pobladas desde las actuales;
  - fecha en ISO `YYYY-MM-DD`, convertida desde `dd-mm-YYYY`.
- Generá un **reporte de verificación** con filas migradas, totales antes y después, y filas con problemas.
- La API debe seguir devolviendo los mismos campos que usa hoy el frontend. La conversión a pesos se hace al responder.
- El frontend muestra la fecha como `dd/mm/aaaa`.

### Paso 0.5 — Numeración de comprobantes
- Reemplazá el `COUNT(*)` por una tabla `secuencias (empresa_id, tipo, ultimo)` que se incrementa dentro de la misma transacción.
- La secuencia arranca desde el número más alto que ya existe.
- Probá que dos emisiones seguidas y una anulación no repiten números.

### Paso 0.6 — Empresa, usuarios, roles y login
- Tabla `empresa` con un registro para Coronel Sur. Todas las tablas nuevas llevan `empresa_id`, y una capa común de acceso lo exige en cada consulta.
- Tablas `usuario`, `rol` y `usuario_rol`.
  - Roles: `admin`, `responsable_cobranza`, `cobrador`, `consulta`, con la matriz de la sección 6 del diseño.
  - Contraseñas con argon2 (`argon2-cffi`) o bcrypt.
- **Sesión:**
  - cookie `HttpOnly`, `Secure` en producción y `SameSite=Lax`, con expiración;
  - protección CSRF en las operaciones que modifican datos;
  - bloqueo temporal después de varios intentos fallidos.
- Pantalla de login simple, con el mismo estilo visual del `index.html`. **Todas** las rutas `/api/*` y la página principal requieren sesión, salvo un `/salud` sin datos.
- Creación del primer admin con un comando (`python scripts/crear_admin.py`) que pide la contraseña por consola. **No dejes usuarios ni contraseñas por defecto.**
- `SECRET_KEY` y la configuración se leen de variables de entorno. Sumá un `.env.example` sin valores reales.

### Paso 0.7 — Auditoría
- Tabla `evento_auditoria` en la que solo se agregan filas: actor, acción, entidad, id, antes, después, IP y momento.
- Registrá login, login fallido, logout, emisión, anulación, creación y cambio de usuarios, migraciones y restauraciones.
- No guardes contraseñas ni datos sensibles en los logs.

### Criterio de salida del Hito 0
- Todas las pruebas en verde, mostrando la salida.
- Sin sesión no se accede a nada.
- La restauración de un respaldo está probada.
- La emisión y la anulación funcionan igual que antes.
- Un `README` actualizado explica cómo instalar, crear el admin, respaldar, restaurar y correr las pruebas.

**Frená acá. Mostrame el resumen y esperá mi OK antes del Hito 1.**

---

## HITO 1 — Cartera de cuentas corrientes

### Paso 1.1 — Modelo de datos (seguí la sección 5 del diseño)
- **`cliente`:** sumá `cuit` (validado con dígito verificador), `condicion_pago_dias`, `limite_informativo_centavos` (solo informativo, no bloquea nada) y `cliente_origen_id` (el identificador en FactuPyme).
- **`contacto_autorizado`:** teléfono en formato E.164, normalizado para Argentina, con el consentimiento (fecha y fuente) y la fecha de baja.
- **`documento_comercial`:** tipo (FC, NC, ND, SI = saldo inicial), punto de venta, número, fecha de emisión, fecha de vencimiento, importe total, moneda, estado (`emitido`, `parcialmente_cancelado`, `cancelado`, `anulado`), fuente, `id_externo` y `lote_id`.
  - Restricción única `(empresa_id, fuente, id_externo)`.
- **`aplicacion`:** en este hito solo para notas de crédito contra facturas y ajustes, con `revierte_a`.
- **`ajuste`:** motivo, evidencia, aprobado_por y `revierte_a`.
- **`lote_importacion`:** archivo, hash SHA-256, filas totales, filas ok, filas con error, errores en JSON, importado_por y estado (`vista_previa`, `confirmado`, `revertido`).
- **"Vencido" no se guarda:** se calcula con el vencimiento, el saldo y la fecha de corte.

### Paso 1.2 — Motor de saldos (código puro)
- En `backend/copiloto/motor/`, funciones sin acceso a la base que calculen:
  - el saldo de un documento;
  - el saldo de un cliente;
  - la antigüedad por tramos (al día, 1-30, 31-60, 61-90, +90);
  - el estado derivado del documento.
- **Pruebas unitarias exhaustivas:**
  - pago parcial;
  - nota de crédito parcial y total;
  - ajuste y su reverso;
  - documento anulado;
  - redondeo;
  - suma de aplicaciones que no puede superar el total.

### Paso 1.3 — Importador de cartera con mapeo configurable
- El formato real de FactuPyme todavía no lo conozco con certeza (ver P2). Por eso:
  - El importador lee CSV o Excel con un **mapeo de columnas configurable** (archivo JSON por formato), con soporte para latin-1, separador `;` y números en formato argentino. Reutilizá `parsear_numero` del importador actual y sumale pruebas.
  - Primero hace una **vista previa**: filas válidas, errores por fila (CUIT inválido, fecha inválida, importe ilegible, cliente desconocido, duplicado) y totales.
  - El usuario carga el **total que informa la fuente** y el sistema muestra la diferencia. Solo se confirma si coincide al centavo o si cada diferencia queda registrada como excepción.
  - Al confirmar, crea clientes nuevos o vincula existentes (por CUIT, o por `cliente_origen_id`) y crea los documentos.
  - **Reimportar el mismo archivo o las mismas filas no duplica nada.** La deduplicación se hace por hash e `id_externo`.
  - Un lote confirmado se puede **revertir** con reversos trazables, sin borrar filas.
- **Saldo inicial:** se puede importar como documentos abiertos (lo ideal) o como un documento SI por cliente, con fecha de corte y evidencia (el archivo de origen).
- Si en P2 hay ejemplos reales anonimizados, armá el mapeo para ellos. **Si no hay, frená y pedímelos.** Mientras tanto, trabajá con un CSV de ejemplo inventado en `tests/fixtures/`.

### Paso 1.4 — API y pantallas de cartera
- **Endpoints** con permisos según la matriz:
  - lista de clientes con saldo, vencido y antigüedad;
  - detalle de cliente con sus documentos y aplicaciones;
  - documentos con filtros;
  - lotes de importación (vista previa, confirmar, revertir);
  - ajuste (crear y revertir, solo admin).
- **Página "Cartera"** en `index.html`, reemplazando el placeholder de CRM o sumándola al menú:
  - total de cartera, total vencido por tramos, clientes ordenados por vencido;
  - buscador;
  - detalle por cliente;
  - exportación a Excel o CSV.
- **Fuente desactualizada:** mostrá siempre "Datos al {fecha de la última importación confirmada}". Si pasaron más de N días (configurable, por defecto 3), mostrá un aviso visible.
- **Página "Importar"** con el flujo vista previa → total informado → confirmar → resultado.

### Paso 1.5 — Pruebas de aceptación de este hito
Implementá y ejecutá, además de las del motor:
- **Prueba 9** (adaptada): importar dos veces el mismo archivo o las mismas filas genera un solo registro.
- **Prueba 11:** un usuario de otra empresa recibe 404 sin que se revele información. Creá una segunda empresa de prueba.
- **Prueba 13:** revertir un ajuste o un lote deja el saldo como estaba y conserva la historia.
- **Prueba 14** (parcial): una nota de crédito aplicada a dos facturas conserva la suma y los remanentes.
- **Prueba 15:** restaurar un respaldo y reimportar no duplica nada y deja los saldos consistentes.
- **Prueba 8** (parcial): la API devuelve la fecha de los datos y la marca de desactualizado.
- **Permisos:** un `cobrador` no puede confirmar importaciones ni crear ajustes, y `consulta` solo puede leer.

### Criterio de salida del Hito 1
- Con un archivo de ejemplo veo la cartera total, el vencido por tramos y el detalle por cliente. **El total coincide al centavo con el total informado**, o la diferencia queda explicada como excepción.
- Reimportar no duplica, revertir deja todo como estaba y todas las pruebas están en verde.
- El `README` explica cómo exportar desde la fuente, importar y verificar.

---

## Entrega final

Al terminar cada hito, dame:
1. Un resumen en 10 líneas como máximo.
2. Cómo probarlo, paso a paso.
3. La salida de `pytest`.
4. Qué quedó terminado, qué solo diseñado y qué pendiente.
5. Las decisiones que necesito tomar.
6. Los riesgos que viste.

**Empezá por el Paso 0.1.** Antes, contame en 5 líneas qué vas a hacer y confirmá que leíste el diseño.
