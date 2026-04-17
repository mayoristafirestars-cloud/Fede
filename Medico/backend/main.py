"""
Médico — Servidor principal
Ejecutar: python main.py
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db.database import inicializar_db, conectar
from routers.profesionales import router as router_profesionales

app = FastAPI(title="Médico", version="1.0.0")

BACKEND  = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(os.path.dirname(BACKEND), "frontend")
STATIC   = os.path.join(FRONTEND, "static")
TEMPLATE = os.path.join(FRONTEND, "templates", "index.html")

os.makedirs(STATIC, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC), name="static")
app.include_router(router_profesionales)


@app.on_event("startup")
def startup():
    inicializar_db()
    print("🩺 Médico en http://localhost:8001")


@app.get("/", response_class=HTMLResponse)
def raiz():
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/api/estado")
def estado():
    conn = conectar()
    try:
        return {
            "estado": "ok",
            "registros": {
                "medicos":        conn.execute("SELECT COUNT(*) FROM profesionales WHERE tipo='medico' AND activo=1").fetchone()[0],
                "nutricionistas": conn.execute("SELECT COUNT(*) FROM profesionales WHERE tipo='nutricionista' AND activo=1").fetchone()[0],
                "pacientes":      conn.execute("SELECT COUNT(*) FROM pacientes").fetchone()[0],
                "consultas":      conn.execute("SELECT COUNT(*) FROM consultas").fetchone()[0],
            },
        }
    finally:
        conn.close()


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
