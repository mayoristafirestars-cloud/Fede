"""
API HTTP mínima para Max (la usa el bridge de WhatsApp en Node).

POST /api/max  {"session_id": "...", "message": "..."}  -> {"response": "..."}

Correr: uvicorn max_server:app --port 8002
"""
import traceback

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from asistente import chat

app = FastAPI(title="Max - API")

sessions: dict[str, list[dict]] = {}


class MaxRequest(BaseModel):
    session_id: str
    message: str


@app.post("/api/max")
def api_max(req: MaxRequest):
    texto = req.message.strip()
    if not texto:
        raise HTTPException(status_code=400, detail="Mensaje vacío.")
    if texto.lower() == "reset":
        sessions.pop(req.session_id, None)
        return {"response": "Listo, empezamos de cero. ¿Qué necesitás?"}
    historial = sessions.setdefault(req.session_id, [])
    try:
        respuesta = chat(historial, texto)
    except Exception as e:
        print("\n===== ERROR COMPLETO (sacale foto a esto) =====")
        traceback.print_exc()
        print("===============================================\n")
        raise HTTPException(status_code=500, detail=str(e)[:500])
    return {"response": respuesta}


@app.get("/health")
def health():
    return {"ok": True}
