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
from routers.clientes import router as router_clientes
from routers.inventario import router as router_inventario
from routers.reportes import router as router_reportes
from routers.agente import router as router_agente
from auth import AuthMiddleware, registrar_rutas as registrar_auth

app = FastAPI(title="Coronel Sur", version="1.0.0")

BACKEND  = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(os.path.dirname(BACKEND), "frontend")
STATIC   = os.path.join(FRONTEND, "static")
TEMPLATE = os.path.join(FRONTEND, "templates", "index.html")

os.makedirs(STATIC, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC), name="static")
app.include_router(router_facturacion)
app.include_router(router_clientes)
app.include_router(router_inventario)
app.include_router(router_reportes)
app.include_router(router_agente)
app.add_middleware(AuthMiddleware)
registrar_auth(app)

def backup_diario():
    """Copia la base una vez por día a db/backups/, conservando las últimas 14."""
    import shutil, time, threading
    from datetime import datetime
    from db.database import DB_PATH

    backups_dir = os.path.join(os.path.dirname(DB_PATH), "backups")
    os.makedirs(backups_dir, exist_ok=True)

    def ciclo():
        while True:
            try:
                destino = os.path.join(
                    backups_dir,
                    f"coronel_sur_{datetime.now().strftime('%Y%m%d')}.db",
                )
                if not os.path.exists(destino) and os.path.exists(DB_PATH):
                    shutil.copy2(DB_PATH, destino)
                    print(f"💾 Backup diario: {destino}")
                    viejos = sorted(
                        f for f in os.listdir(backups_dir)
                        if f.startswith("coronel_sur_") and f.endswith(".db")
                    )
                    for f in viejos[:-14]:
                        os.remove(os.path.join(backups_dir, f))
            except Exception as e:
                print(f"⚠️ Backup falló: {e}")
            time.sleep(3600)  # chequea una vez por hora

    threading.Thread(target=ciclo, daemon=True).start()


@app.on_event("startup")
def startup():
    inicializar_db()
    backup_diario()
    print("🚀 Coronel Sur en http://localhost:8000")

@app.get("/", response_class=HTMLResponse)
def raiz():
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
