"""
Coronel Sur — Servidor principal
Ejecutar: python main.py
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db.database import inicializar_db, conectar
from routers.facturacion import router as router_facturacion
from routers.preparacion import router as router_preparacion, MEDIA_DIR
from routers.comercial import router as router_comercial
from routers.inventario import router as router_inventario
from routers.mostrador import router as router_mostrador
from routers.documentos import router as router_documentos
from security import protect, public_host
from routers.tienda import router as router_tienda
from routers.tienda_operacion import router as router_tienda_operacion
from routers.tienda_promociones import router as router_tienda_promociones
from fastapi import Request

app = FastAPI(title="Coronel Sur", version="1.0.0")
app.middleware('http')(protect)

@app.get('/healthz')
def health():
    return {'estado': 'ok'}

@app.get('/login', response_class=HTMLResponse)
def login_page():
    with open(os.path.join(FRONTEND, 'templates', 'login.html'), encoding='utf-8') as f:
        return f.read()

BACKEND  = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(os.path.dirname(BACKEND), "frontend")
STATIC   = os.path.join(FRONTEND, "static")
TEMPLATE = os.path.join(FRONTEND, "templates", "index.html")

os.makedirs(STATIC, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC), name="static")
app.include_router(router_facturacion)
app.include_router(router_preparacion)
app.include_router(router_comercial)
app.include_router(router_inventario)
app.include_router(router_mostrador)
app.include_router(router_documentos)
app.include_router(router_tienda)
app.include_router(router_tienda_operacion)
app.include_router(router_tienda_promociones)
os.makedirs(MEDIA_DIR, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

@app.on_event("startup")
def startup():
    inicializar_db()
    print("🚀 Coronel Sur en http://localhost:8000")

@app.get('/tienda', response_class=HTMLResponse)
@app.get('/tienda/pedido', response_class=HTMLResponse)
def tienda():
    with open(os.path.join(FRONTEND, 'templates', 'tienda.html'), encoding='utf-8') as f:
        return f.read()

@app.get("/", response_class=HTMLResponse)
def raiz(request: Request):
    template = 'tienda.html' if public_host(request) else 'gestion.html'
    with open(os.path.join(FRONTEND, "templates", template), "r", encoding="utf-8") as f:
        return f.read()

@app.get("/ventas", response_class=HTMLResponse)
def ventas_existentes():
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        return f.read()

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

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
