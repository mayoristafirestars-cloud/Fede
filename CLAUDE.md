# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository State

This repo currently contains a single artifact: `coronel-sur-render_1.zip`. The actual project (a Python/FastAPI + SQLite app called **Coronel Sur**) lives inside the zip and is not checked in as source files. Before making code changes, extract it:

```bash
unzip -o coronel-sur-render_1.zip -d .
```

All paths and commands below refer to the extracted layout.

## Commands

The project is designed for Windows end-users via `.bat` wrappers, but the underlying commands are plain Python:

- Install deps: `pip install -r requirements.txt` (the `.bat` uses a `venv/`; on Linux/macOS create one with `python -m venv venv && source venv/bin/activate`)
- Run the server locally: `python backend/main.py` (serves on `http://localhost:8000`, honors `$PORT` — this is also the Render `startCommand`)
- Import FactuPyme CSVs: `python backend/importador/importar_factupyme.py` (reads `data/csv_originales/{inventario,ventas,presupuestos}.csv`; accepts alternate filenames as positional args)
- Health check while the server runs: `GET /api/estado` returns counts of productos/clientes/ventas/presupuestos
- There are **no tests, linters, or build steps** configured. Don't invent commands for them.

## Architecture

### Two parallel, inconsistent implementations

The extracted zip contains **two overlapping code trees** with different schemas. Know which one you are editing:

- **`backend/`** — the live implementation. This is what `render.yaml`, `iniciar.bat`, and `importar.bat` invoke. Schema in `backend/db/schema.sql`: tables `productos` (with `stock`), `clientes`, `comprobantes` + `comprobante_items`, `ventas_historicas`.
- **Top-level `database/` + `importador/`** — an older/alternate variant. Schema in `database/schema.py`: tables `productos` (with `stock_actual`), `facturas` + `factura_items`, `movimientos_stock`, `log_importacion`. Not wired into `main.py` or the `.bat` entry points.

Default to `backend/` unless the user is explicitly working on the legacy tree. Changes that touch schema or importer logic usually need to be made in `backend/` only.

### Backend layout (`backend/`)

- `main.py` — FastAPI app factory. Mounts `/static` from `../frontend/static`, serves `../frontend/templates/index.html` at `/`, includes the facturación router, and on startup runs `inicializar_db()` which executes `backend/db/schema.sql` (idempotent via `CREATE TABLE IF NOT EXISTS`). It mutates `sys.path` so imports use `db.database` / `routers.facturacion` — this is why the server must be launched as `python backend/main.py` from the repo root (Render does exactly that).
- `db/database.py` — resolves `DB_PATH` to `backend/db/coronel_sur.db` (note: **not** `data/coronel_sur.db`, despite a stray `data/coronel_sur.db` shipping in the zip). `conectar()` sets `row_factory = sqlite3.Row`, `PRAGMA foreign_keys = ON`, and `journal_mode = WAL`.
- `routers/facturacion.py` — all comprobante endpoints under `/api/facturacion`. Business rules to preserve:
  - Comprobante number is generated as `F-######` / `P-######` from a `COUNT(*)` on existing rows of the same `tipo` — this is **not concurrency-safe**; don't assume monotonic numbering under load.
  - Stock is decremented on `POST /nuevo` **only when** `tipo == "factura"` and the item has a `producto_id`. Presupuestos never touch stock.
  - `POST /{id}/anular` reverses the stock adjustment (factura only) and sets `estado = 'anulado'`. The `historial` endpoint filters out `anulado` rows.
- `importador/importar_factupyme.py` — reads the three FactuPyme CSVs from `<repo>/data/csv_originales/` (resolved via `../../../` from the module). Always call `parsear_numero()` and `parsear_codigo()` for any CSV numeric/code field.

### FactuPyme CSV contract

All three CSVs are **latin-1 encoded with `;` as the delimiter**. Don't change encoding or delimiter. Column names contain Spanish accents (e.g. `Descripción`) — the importer tolerates both `Descripción` and `Descripcion`, and `Cant.` vs `Cantidad`. Preserve that dual lookup when adding fields.

Two parsing rules are load-bearing and must be preserved:

- **`parsear_numero`**: a `.` followed by exactly 3 digits is a thousands separator and is stripped; otherwise `.` is a decimal. Commas are European decimals and become `.`. Examples: `"10.000" → 10000.0`, `"1999.5" → 1999.5`, `"1.234.567" → 1234567.0`.
- **`parsear_codigo`**: extracts the first run of digits from strings like `"Cod: 12345"`.

`importar_ventas` **deletes all `ventas_historicas` rows matching the current `origen`** before inserting, so re-running the importer is idempotent per-origen but destroys any manual edits to historical data. Ganancia is computed as `subtotal - (costo_unit * cantidad)` at import time.

### Deployment

`render.yaml` pins Python 3.11.0, installs `requirements.txt`, and starts with `python backend/main.py`. `PORT` is provided by Render and read in `main.py`. The SQLite DB file is ephemeral on Render's default disk — there is no persistent-disk config in `render.yaml`, so data written in production does not survive redeploys unless that is added.

### Language & conventions

Code, identifiers, comments, log messages, and API field names are all in **Spanish** (e.g. `productos`, `comprobantes`, `rubro`, `anular`). Match this when adding code — don't introduce English names into the domain model.
