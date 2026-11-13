# Coronel Sur — Sistema de Gestión

Sistema de facturación e inventario de Distribuidora Coronel Sur (FastAPI + SQLite).

## Instalación (una sola vez)

**Windows:** doble click en `instalar.bat`.

**Linux / Mac / manual:**
```
python3.11 -m venv venv
venv/bin/pip install -r requirements.txt          # producción
venv/bin/pip install -r requirements-dev.txt      # + herramientas de prueba
```

### Configuración

Copiá `.env.example` como `.env` y completá `SECRET_KEY` (mínimo 32 caracteres):
```
python -c "import secrets; print(secrets.token_urlsafe(48))"
```
El `.env` no se sube al repositorio. En producción (`ENTORNO=produccion`) la `SECRET_KEY` es obligatoria y las cookies viajan sólo por HTTPS.

| Variable | Para qué | Por defecto |
|---|---|---|
| `ENTORNO` | `desarrollo` o `produccion` | `desarrollo` |
| `SECRET_KEY` | Firma de las sesiones | temporal en desarrollo, obligatoria en producción |
| `DB_PATH` | Archivo de la base | `backend/db/coronel_sur.db` |
| `BACKUP_DIR` | Carpeta de respaldos | `backend/db/respaldos` |
| `SESION_HORAS` | Duración de la sesión | `12` |
| `IVA_ALICUOTA` | IVA (%) que se asume para mostrar la ganancia sin IVA | `21` |
| `CONDICION_PAGO_DIAS_DEFECTO` | Días de plazo para calcular vencimientos si el cliente no tiene condición | `30` |
| `DIAS_DATOS_DESACTUALIZADOS` | Días sin importar a partir de los cuales la cartera muestra el aviso | `3` |

## Crear el primer usuario administrador

No hay usuarios ni contraseñas por defecto. Creá el primero desde la consola:
```
python scripts/crear_admin.py
```
Pide usuario, nombre, roles (Enter = `admin`) y la contraseña (mínimo 10 caracteres, no se muestra). Con el mismo comando se crean los demás usuarios.

Roles: `admin`, `responsable_cobranza`, `cobrador`, `consulta`. Qué puede hacer cada uno está en `backend/seguridad.py` (`PERMISOS`).

## Iniciar el sistema

- **Windows:** doble click en `iniciar.bat`.
- **Manual:** `python backend/main.py`, y abrir `http://localhost:8000`.

Al arrancar se aplican solas las migraciones pendientes. Si la base ya tiene datos, **antes se hace un respaldo automático**.

Sin sesión, la página lleva al login y toda ruta `/api` responde 401. `/salud` responde `{"estado":"ok"}` sin datos, para el chequeo de Render.

## Importar datos de FactuPyme

1. Exportar desde FactuPyme:
   - **Inventario** → `inventario.csv`
   - **Informe de Ventas** → `ventas.csv`
   - **Informe de Presupuestos** → `presupuestos.csv`
2. Copiar los 3 archivos a `data/csv_originales/`. Esa carpeta no se sube al repositorio.
3. Doble click en `importar.bat` (o `python backend/importador/importar_factupyme.py`).

## Cartera de cuentas corrientes (Copiloto de Caja · Hito 1)

FactuPyme emite las facturas, pero no exporta saldos ni cobros. Por eso **la cuenta corriente vive en este sistema**. Ver `copiloto_caja/ANALISIS_Y_DECISIONES_HITO1.md`.

1. **Saldo inicial (una sola vez).**
   - Completá `data/plantillas/saldo_inicial.csv` con lo que te debe cada cliente a una fecha de corte. Las instrucciones están en `data/plantillas/LEEME.md`.
   - En **Importar cartera** elegí "Saldo inicial", la fecha de corte y el archivo. Revisá la vista previa: filas con error y omitidas.
   - Escribí el **total de tu registro** (cuaderno o planilla). Si no coincide con el total del archivo, corregí el archivo o explicá la diferencia: queda registrada.
2. **Novedades (cada semana).**
   - En ARCA → Mis Comprobantes → **Emitidos**, descargá el período en CSV o Excel y subilo como "ARCA · Mis Comprobantes Emitidos".
   - Se toman sólo facturas, notas de débito y notas de crédito **de clientes con cuenta corriente** y **posteriores a su saldo inicial**. Las ventas de contado quedan omitidas.
   - Si ARCA cambia el nombre de una columna, agregá el alias en `backend/copiloto/mapeos/arca_emitidos.json`.
3. **Cartera.**
   - Muestra el saldo total y lo vencido por antigüedad (al día, 1-30, 31-60, 61-90, más de 90), y los clientes ordenados por vencido.
   - En el detalle de cada cliente: comprobantes con saldo y estado, aplicar notas de crédito, ajustes (solo admin) y configuración de la cuenta corriente.
   - Siempre muestra **"Datos al …"** y avisa si pasaron más de 3 días sin importar.
4. **Errores.**
   - Un lote confirmado se puede **revertir**: anula sus comprobantes, no los borra.
   - Ajustes y aplicaciones también se revierten con un reverso vinculado. Todo queda en la auditoría.
   - **Reimportar el mismo archivo o las mismas filas no duplica nada.**

Las notas de crédito que no se aplican a una factura quedan como "créditos sin imputar": restan del saldo, pero no del vencido. Por eso el vencido de un cliente puede ser mayor que su saldo.

## Respaldos

**Respaldar a mano:**
```
python scripts/respaldar.py
```
Crea una copia fechada en `BACKUP_DIR`.

**Restaurar** (primero detené el servidor):
```
python scripts/restaurar.py RUTA_DEL_RESPALDO
```
Pide escribir `RESTAURAR` para confirmar. Antes de pisar la base, guarda un respaldo de la base actual, y la restauración queda en la auditoría.

Los respaldos quedan en el mismo servidor. **Copialos periódicamente a otro lugar**: si se pierde el disco, se pierden también los respaldos.

## Pruebas

```
venv/bin/pip install -r requirements-dev.txt
venv/bin/python -m pytest
```
Las pruebas usan bases temporales: nunca tocan la base real.

## Estructura

```
backend/
  main.py                 servidor FastAPI, control de sesión y CSRF
  config.py               variables de entorno y .env
  seguridad.py            contraseñas, sesiones, roles y permisos
  routers/
    auth.py               login, logout, usuario actual
    facturacion.py        comprobantes
  db/
    database.py           conexión (DB_PATH)
    migrador.py           migraciones versionadas
    migraciones/          0001_... .sql (se aplican una sola vez, en orden)
    respaldos.py          respaldo y restauración
    secuencias.py         numeración sin repetidos
    auditoria.py          registro de auditoría (sólo agregar)
  importador/
    importar_factupyme.py importa los CSV de FactuPyme
frontend/templates/       index.html (sistema) y login.html
scripts/                  crear_admin.py, respaldar.py, restaurar.py
tests/                    pruebas (pytest)
legacy/                   versión anterior, no se usa
copiloto_caja/            diseño del Copiloto de Caja
```

## Despliegue en Render

`render.yaml` tiene una **propuesta** con disco persistente en `/var/data` para la base y los respaldos. Sin disco persistente, la base se borra en cada despliegue. Los discos requieren un plan pago. Nada se despliega automáticamente desde este repositorio.

Después del primer despliegue, crear el admin desde la consola (Shell) de Render con `python scripts/crear_admin.py`.
