"""
Coronel Sur — Servidor principal

Punto de entrada FastAPI. Wire de todos los routers y middlewares.
"""
from __future__ import annotations

import logging
import os
import sys

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.database import conectar, inicializar_db
from logging_config import setup_logging
from migrations import ejecutar_migraciones
from rate_limit import limiter, setup_rate_limiting
from security.headers import SecurityHeadersMiddleware
from security.sessions import limpiar_sesiones_expiradas

# Routers
from routers.admin import router as router_admin
from routers.agente import router as router_agente
from routers.agente_cobranzas import router as router_agente_cobranzas
from routers.bot import router as router_bot
from routers.agente_ml import router as router_agente_ml
from routers.agente_precios import router as router_agente_precios
from routers.agente_stock import router as router_agente_stock
from routers.auth import router as router_auth
from routers.caja import router as router_caja
from routers.compras import router as router_compras
from routers.config import router as router_config
from routers.crm import router as router_crm
from routers.cuenta_corriente import router as router_cc
from routers.facturacion import router as router_facturacion
from routers.inventario import router as router_inventario
from routers.pdf import router as router_pdf
from routers.predictor import router as router_predictor
from routers.reportes import router as router_reportes
from routers.tienda import router as router_tienda
from routers.tienda_v2 import router as router_tienda_v2


# ─── Logging antes que nada ────────────────────────────────
setup_logging()
log = logging.getLogger("coronel_sur")


# ─── App FastAPI ───────────────────────────────────────────
app = FastAPI(title="Coronel Sur", version="1.2.0")

# Middlewares
app.add_middleware(SecurityHeadersMiddleware)
setup_rate_limiting(app)


BACKEND = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(os.path.dirname(BACKEND), "frontend")
STATIC = os.path.join(FRONTEND, "static")
TEMPLATE = os.path.join(FRONTEND, "templates", "index.html")

os.makedirs(STATIC, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC), name="static")

app.include_router(router_facturacion)
app.include_router(router_crm)
app.include_router(router_tienda)
app.include_router(router_agente)
app.include_router(router_inventario)
app.include_router(router_reportes)
app.include_router(router_auth)
app.include_router(router_caja)
app.include_router(router_compras)
app.include_router(router_pdf)
app.include_router(router_cc)
app.include_router(router_config)
app.include_router(router_tienda_v2)
app.include_router(router_predictor)
app.include_router(router_agente_stock)
app.include_router(router_agente_ml)
app.include_router(router_agente_precios)
app.include_router(router_agente_cobranzas)
app.include_router(router_admin)
app.include_router(router_bot)


@app.on_event("startup")
def startup():
    log.info("Inicializando Coronel Sur…")
    inicializar_db()

    n = ejecutar_migraciones()
    if n:
        log.info("Migraciones aplicadas: %d", n)

    try:
        limpiar_sesiones_expiradas()
    except Exception as e:
        log.warning("No se pudieron limpiar sesiones viejas: %s", e)

    log.info("Coronel Sur v1.2.0 iniciado")


@app.get("/", response_class=HTMLResponse)
def raiz():
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/health")
def health():
    """Health check para Render. No requiere auth."""
    return {"status": "ok"}


@app.get("/api/estado")
def estado_db():
    conn = conectar()
    try:
        return {
            "estado": "ok",
            "registros": {
                "productos": conn.execute("SELECT COUNT(*) FROM productos").fetchone()[0],
                "clientes": conn.execute("SELECT COUNT(*) FROM clientes").fetchone()[0],
                "ventas": conn.execute(
                    "SELECT COUNT(*) FROM ventas_historicas WHERE origen='factura'"
                ).fetchone()[0],
                "presupuestos": conn.execute(
                    "SELECT COUNT(*) FROM ventas_historicas WHERE origen='presupuesto'"
                ).fetchone()[0],
            },
        }
    finally:
        conn.close()


@app.get("/api/productos")
def listar_productos(rubro: str = None, buscar: str = None, limit: int = 50):
    conn = conectar()
    try:
        query = "SELECT * FROM productos WHERE activo = 1"
        params = []
        if rubro:
            query += " AND rubro = ?"
            params.append(rubro)
        if buscar:
            query += " AND (descripcion LIKE ? OR codigo LIKE ?)"
            params += [f"%{buscar}%", f"%{buscar}%"]
        limit = max(1, min(int(limit), 500))
        query += f" ORDER BY descripcion LIMIT {limit}"
        return [dict(f) for f in conn.execute(query, params).fetchall()]
    finally:
        conn.close()


@app.get("/api/rubros")
def listar_rubros():
    conn = conectar()
    try:
        return [
            dict(f)
            for f in conn.execute(
                "SELECT DISTINCT rubro, COUNT(*) as cantidad FROM productos "
                "WHERE rubro != '' GROUP BY rubro ORDER BY cantidad DESC"
            ).fetchall()
        ]
    finally:
        conn.close()


@app.get("/tienda", response_class=HTMLResponse)
def tienda_v2():
    tpl = os.path.join(FRONTEND, "templates", "tienda_v2.html")
    with open(tpl, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/sw.js")
def service_worker():
    sw_path = os.path.join(FRONTEND, "static", "sw.js")
    return FileResponse(sw_path, media_type="application/javascript")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
