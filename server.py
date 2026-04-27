"""
Agente de soporte - Paso 7: servidor web.
Expone Sofi como una API HTTP y sirve una página HTML de chat.

Correr: uvicorn server:app --reload --port 8000
Después abrir: http://localhost:8000
"""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agente import chat

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Trama - Agente de Soporte")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estado en memoria: una conversación por session_id.
# (Para producción real esto va a Redis o una DB.)
sessions: dict[str, list[dict]] = {}


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    session_id: str


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/chat", response_model=ChatResponse)
def api_chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío.")
    historial = sessions.setdefault(req.session_id, [])
    try:
        respuesta = chat(historial, req.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del agente: {e}")
    return ChatResponse(response=respuesta, session_id=req.session_id)


@app.post("/api/reset")
def api_reset(req: ChatRequest):
    sessions.pop(req.session_id, None)
    return {"ok": True}


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
