"""
Coronel Sur — Servidor principal
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db.database import inicializar_db, conectar
from routers.facturacion import router as router_facturacion
from routers.crm import router as router_crm
from routers.tienda import router as router_tienda
from routers.agente import router as router_agente
from routers.inventario import router as router_inventario
from routers.reportes import router as router_reportes
from routers.auth import router as router_auth
from routers.caja import router as router_caja
from routers.compras import router as router_compras
from routers.pdf import router as router_pdf
from routers.cuenta_corriente import router as router_cc
from routers.config import router as router_config
from routers.tienda_v2 import router as router_tienda_v2
from routers.predictor import router as router_predictor
from routers.agente_stock import router as router_agente_stock
from routers.agente_ml import router as router_agente_ml
from routers.agente_precios import router as router_agente_precios
from routers.agente_cobranzas import router as router_agente_cobranzas
from routers.admin import router as router_admin
from routers.admin_panel import router as router_admin_panel
from routers.bot import router as router_bot
from routers.tienda_publica import router as router_tienda_publica
from routers.admin_banners import router as router_admin_banners

# Rate limiter: 120 req/min por IP (general)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["120/minute"],
    storage_uri="memory://",
)

app = FastAPI(title="Coronel Sur", version="1.4.0")
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Demasiadas solicitudes. Espera un momento antes de reintentar."}
    )


BACKEND  = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(os.path.dirname(BACKEND), "frontend")
STATIC   = os.path.join(FRONTEND, "static")
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
app.include_router(router_admin_panel)
app.include_router(router_bot)
app.include_router(router_tienda_publica)
app.include_router(router_admin_banners)

@app.on_event("startup")
def startup():
    inicializar_db()
    print("Coronel Sur v1.4.0 en http://localhost:8000")

@app.get("/", response_class=HTMLResponse)
def raiz():
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/estado")
def estado_db():
    conn = conectar()
    try:
        return {
            "estado": "ok",
            "registros": {
                "productos":    conn.execute("SELECT COUNT(*) FROM productos").fetchone()[0],
                "clientes":     conn.execute("SELECT COUNT(*) FROM clientes").fetchone()[0],
                "ventas":       conn.execute("SELECT COUNT(*) FROM ventas_historicas WHERE origen='factura'").fetchone()[0],
                "presupuestos": conn.execute("SELECT COUNT(*) FROM ventas_historicas WHERE origen='presupuesto'").fetchone()[0],
            }
        }
    finally:
        conn.close()

@app.get("/api/productos")
def listar_productos(rubro: str = None, buscar: str = None, limit: int = 50):
    conn = conectar()
    try:
        query  = "SELECT * FROM productos WHERE activo = 1"
        params = []
        if rubro:
            query += " AND rubro = ?"; params.append(rubro)
        if buscar:
            query += " AND (descripcion LIKE ? OR codigo LIKE ?)"; params += [f"%{buscar}%", f"%{buscar}%"]
        limit = max(1, min(int(limit), 500))
        query += f" ORDER BY descripcion LIMIT {limit}"
        return [dict(f) for f in conn.execute(query, params).fetchall()]
    finally:
        conn.close()

@app.get("/api/rubros")
def listar_rubros():
    conn = conectar()
    try:
        return [dict(f) for f in conn.execute(
            "SELECT DISTINCT rubro, COUNT(*) as cantidad FROM productos WHERE rubro != '' GROUP BY rubro ORDER BY cantidad DESC"
        ).fetchall()]
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
