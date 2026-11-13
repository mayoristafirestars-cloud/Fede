# Coronel Sur — Sistema de Gestión

## Sistema privado de Nativa

La preparación para publicar con inicio de sesión, disco persistente y respaldos está documentada en [publicación del sistema](docs/publicacion-sistema.md). Todavía no se contrató hosting ni se publicó el sistema. La web para clientes queda para una etapa posterior. No exponer el modo de desarrollo a Internet.

## Tienda para vecinos · puntos 1–10

Disponible en `/tienda`, con catálogo publicado, cantidades claras, solicitud invitada, presupuesto máximo, preferencias de reemplazo y aprobación del pesaje. Incluye recompra a precios actuales, franjas de retiro con reservas compartidas con mostrador, consultas/respuestas y contribución por pedido. La entrega registra cobro verificado manualmente y descuenta stock una vez. Sin integración automática de cobros, ARCA ni reparto. Ver [puntos 4–10, pruebas y actualización](docs/tienda-puntos-4-10.md). La versión preparada no se publicó automáticamente en Hetzner.

## Ofertas y favoritos

La tienda permite promociones por producto con vigencia, control de superposición y autorización expresa del dueño para precios debajo del costo conocido. Los pedidos conservan su precio acordado. Los vecinos pueden guardar favoritos en su dispositivo y filtrar ofertas. Ver [alcance y actualización](docs/tienda-ofertas-favoritos.md).

## Desarrollo en Linux / entorno en la nube

El código está disponible fuera del ZIP para mantenerlo con Git. El archivo ZIP original se conserva.

```bash
cd /workspace/Fede
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
```

La página principal contiene **Mi negocio** (1–6), **Productos** (7–10), **Precios y costos** (11–14), **Compras** (15–20), **Proveedores y cuentas** (21–22), **Inventario** (23–30), **Rotación y compra** (31), **Envases retornables** (32) y **Mostrador** (33–40). La interfaz anterior se conserva en `/ventas`. Base local: `backend/db/coronel_sur.db`; fotos: `backend/uploads/`. Consultar [etapa 1](docs/etapa-01.md), [etapa 2](docs/etapa-02.md), [etapa 3](docs/etapa-03.md) y [etapa 4](docs/etapa-04.md). La integración física de balanza permanece pendiente del modelo y sus pruebas; no se requiere para probar la carga manual.

Pruebas de backend (dependencia de desarrollo: `python -m pip install -r requirements-dev.txt`):

```bash
python -m unittest discover -s tests -v
```

Prueba opcional de navegador: instalar `requirements-browser.txt` y disponer de Chromium. Ejecutar `python tests/browser_smoke.py`; `CHROMIUM_PATH` permite elegir su ejecutable y `APP_PYTHON` el Python del servidor. Usa datos temporales, verifica escritorio/celular y deja capturas en `/tmp/verduleria-productos.png` y `/tmp/verduleria-movil.png`.

La etapa 2 incluye autorización para modificar precios, costos y compras: en desarrollo, crear el primer responsable desde **Precios y costos**, sin credenciales predeterminadas. En producción el acceso general requiere sesión y el primer dueño se crea desde consola. Cobros integrados, conexión con balanza, funcionamiento offline y emisión fiscal quedan pendientes. Las personas, equipos y medios de pago de **Mi negocio** se registran como definición de la operación.

## Instalación (una sola vez)

Los documentos imprimibles incluyen fotos por renglón. Consultar [fotos en remitos y comprobantes](docs/fotos-en-documentos.md) para carga, conservación histórica y cómo completar imágenes faltantes. La emisión fiscal y la impresión física en la balanza siguen pendientes de sus integraciones.
1. Doble click en `instalar.bat`

## Importar datos de FactuPyme
1. Exportar desde FactuPyme:
   - **Inventario** → guardar como `inventario.csv`
   - **Informe de Ventas** → guardar como `ventas.csv`
   - **Informe de Presupuestos** → guardar como `presupuestos.csv`
2. Copiar los 3 archivos a la carpeta `data/csv_originales/`
3. Doble click en `importar.bat`

## Iniciar el sistema
- Doble click en `iniciar.bat`
- El navegador se abre en `http://localhost:8000`

## Verificar que todo está bien
- Ir a `http://localhost:8000/api/estado`
- Debe mostrar los conteos de productos, clientes y ventas

## Estructura del proyecto
```
coronel-sur/
├── backend/
│   ├── db/
│   │   ├── schema.sql          ← estructura de la base de datos
│   │   └── database.py         ← conexión a SQLite
│   ├── importador/
│   │   └── importar_factupyme.py ← importa los CSVs
│   └── main.py                 ← servidor FastAPI
├── frontend/
│   └── static/                 ← CSS, JS, imágenes
├── data/
│   └── csv_originales/         ← pegar aquí los CSVs de FactuPyme
├── instalar.bat
├── importar.bat
└── iniciar.bat
```
