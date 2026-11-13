"""
Coronel Sur — Servidor principal
Ejecutar: python main.py
"""

from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
config.cargar_env()

import seguridad
from db.database import inicializar_db, conectar
from routers.facturacion import router as router_facturacion
from routers.auth import router as router_auth

# En producción no se publica la documentación automática de la API.
_docs = {} if not config.es_produccion() else {"docs_url": None, "redoc_url": None, "openapi_url": None}
app = FastAPI(title="Coronel Sur", version="1.0.0", **_docs)

BACKEND  = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(os.path.dirname(BACKEND), "frontend")
STATIC   = os.path.join(FRONTEND, "static")
TEMPLATE = os.path.join(FRONTEND, "templates", "index.html")
LOGIN    = os.path.join(FRONTEND, "templates", "login.html")

# Rutas /api que no requieren sesión.
API_PUBLICA = {"/api/auth/login"}
METODOS_SEGUROS = {"GET", "HEAD", "OPTIONS"}

os.makedirs(STATIC, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC), name="static")
app.include_router(router_auth)
app.include_router(router_facturacion)


@app.middleware("http")
async def control_de_sesion(request: Request, call_next):
    """Toda ruta /api exige sesión válida; las que modifican datos, además, token CSRF."""
    request.state.usuario = seguridad.usuario_de_token(request.cookies.get(seguridad.COOKIE_SESION))
    ruta = request.url.path
    if ruta.startswith("/api/") and ruta not in API_PUBLICA:
        usuario = request.state.usuario
        if not usuario:
            return JSONResponse({"detail": "Sesión requerida"}, status_code=401)
        if request.method not in METODOS_SEGUROS and not seguridad.csrf_valido(request, usuario):
            return JSONResponse({"detail": "Token CSRF inválido"}, status_code=403)
    return await call_next(request)


@app.on_event("startup")
def startup():
    seguridad.secret_key()          # en producción falla si falta SECRET_KEY
    inicializar_db()
    print("🚀 Coronel Sur en http://localhost:8000")

def _leer(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/", response_class=HTMLResponse)
def raiz(request: Request):
    if not request.state.usuario:
        return RedirectResponse("/login", status_code=303)
    return _leer(TEMPLATE)

@app.get("/login", response_class=HTMLResponse)
def pagina_login(request: Request):
    if request.state.usuario:
        return RedirectResponse("/", status_code=303)
    return _leer(LOGIN)

@app.get("/salud")
def salud():
    """Chequeo de vida para Render. No expone datos."""
    return {"estado": "ok"}

@app.get("/api/estado")
def estado_db(_u=Depends(seguridad.requiere("producto.ver"))):
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
def listar_productos(rubro: str = None, buscar: str = None, limit: int = 50,
                     _u=Depends(seguridad.requiere("producto.ver"))):
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
def listar_rubros(_u=Depends(seguridad.requiere("producto.ver"))):
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
