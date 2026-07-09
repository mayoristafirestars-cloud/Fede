"""
API HTTP mínima para Max (la usa el bridge de WhatsApp en Node).

POST /api/max    {"session_id": "...", "message": "..."}  -> {"response": "..."}
POST /api/audio  {"session_id": "...", "audio_b64": "...", "mimetype": "..."}
                 -> {"response": "...", "transcript": "..."}

Correr: uvicorn max_server:app --port 8002
"""
import base64
import traceback

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from asistente import chat
from transcripcion import transcribir, sufijo_por_mime

app = FastAPI(title="Max - API")

sessions: dict[str, list[dict]] = {}


class MaxRequest(BaseModel):
    session_id: str
    message: str


class AudioRequest(BaseModel):
    session_id: str
    audio_b64: str
    mimetype: str = "audio/ogg"


def responder(session_id: str, texto: str) -> str:
    if texto.lower() == "reset":
        sessions.pop(session_id, None)
        return "Listo, empezamos de cero. ¿Qué necesitás?"
    historial = sessions.setdefault(session_id, [])
    return chat(historial, texto)


@app.post("/api/max")
def api_max(req: MaxRequest):
    texto = req.message.strip()
    if not texto:
        raise HTTPException(status_code=400, detail="Mensaje vacío.")
    try:
        return {"response": responder(req.session_id, texto)}
    except Exception as e:
        print("\n===== ERROR COMPLETO (sacale foto a esto) =====")
        traceback.print_exc()
        print("===============================================\n")
        raise HTTPException(status_code=500, detail=str(e)[:500])


@app.post("/api/audio")
def api_audio(req: AudioRequest):
    try:
        audio = base64.b64decode(req.audio_b64)
    except Exception:
        raise HTTPException(status_code=400, detail="Audio inválido (base64).")
    if not audio:
        raise HTTPException(status_code=400, detail="Audio vacío.")

    try:
        texto = transcribir(audio, suffix=sufijo_por_mime(req.mimetype))
    except Exception as e:
        print("\n===== ERROR DE TRANSCRIPCION =====")
        traceback.print_exc()
        print("==================================\n")
        raise HTTPException(status_code=500, detail=f"Transcripción: {str(e)[:300]}")

    if not texto:
        return {
            "response": "No pude entender el audio 😕 ¿Me lo repetís o me lo escribís?",
            "transcript": "",
        }

    print(f"[audio] Transcripto: {texto[:120]}")
    try:
        return {"response": responder(req.session_id, texto), "transcript": texto}
    except Exception as e:
        print("\n===== ERROR COMPLETO (sacale foto a esto) =====")
        traceback.print_exc()
        print("===============================================\n")
        raise HTTPException(status_code=500, detail=str(e)[:500])


@app.get("/health")
def health():
    return {"ok": True}
