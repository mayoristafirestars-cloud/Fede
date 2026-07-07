"""
Webhook de WhatsApp (Twilio) para Max, el asistente personal.

Flujo:
  WhatsApp -> Twilio -> POST /whatsapp -> respondemos 200 al instante
  -> Max investiga en segundo plano -> enviamos la respuesta por la
  API REST de Twilio.

Config en .env:
  TWILIO_ACCOUNT_SID=ACxxxx
  TWILIO_AUTH_TOKEN=xxxx
  TWILIO_WHATSAPP_FROM=whatsapp:+14155238886   (número del sandbox)
  WHATSAPP_ALLOWED=whatsapp:+549XXXXXXXXXX     (tu número; separa con comas si hay varios)

Sin credenciales de Twilio configuradas corre en modo DRY RUN:
procesa el mensaje y muestra la respuesta por consola en vez de enviarla.

Correr: uvicorn whatsapp:app --port 8001
"""
import os
import threading

from fastapi import BackgroundTasks, FastAPI, Form, Response
from dotenv import load_dotenv

from asistente import chat

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "")
ALLOWED = {
    n.strip() for n in os.getenv("WHATSAPP_ALLOWED", "").split(",") if n.strip()
}

DRY_RUN = not (TWILIO_SID and TWILIO_TOKEN and TWILIO_FROM)

# WhatsApp corta mensajes largos; Twilio acepta hasta 1600 chars por mensaje.
MAX_MSG_LEN = 1500

app = FastAPI(title="Max - WhatsApp webhook")

# Una conversación por número de WhatsApp.
sessions: dict[str, list[dict]] = {}
# Evita procesar dos encargos a la vez del mismo número.
busy: set[str] = set()
lock = threading.Lock()


def send_whatsapp(to: str, body: str) -> None:
    """Envía un mensaje por Twilio, partiéndolo si es muy largo."""
    chunks = []
    while body:
        chunks.append(body[:MAX_MSG_LEN])
        body = body[MAX_MSG_LEN:]

    if DRY_RUN:
        for c in chunks:
            print(f"\n[DRY RUN -> {to}]:\n{c}\n")
        return

    from twilio.rest import Client

    client = Client(TWILIO_SID, TWILIO_TOKEN)
    for c in chunks:
        client.messages.create(from_=TWILIO_FROM, to=to, body=c)


def procesar(numero: str, mensaje: str) -> None:
    """Corre a Max y envía la respuesta. Se ejecuta en segundo plano."""
    try:
        historial = sessions.setdefault(numero, [])
        respuesta = chat(historial, mensaje)
        send_whatsapp(numero, respuesta)
    except Exception as e:
        send_whatsapp(numero, f"Uy, tuve un problema procesando eso: {e}")
    finally:
        with lock:
            busy.discard(numero)


@app.post("/whatsapp")
def whatsapp_webhook(
    background_tasks: BackgroundTasks,
    Body: str = Form(""),
    From: str = Form(""),
):
    # Si hay lista de permitidos, ignorar cualquier otro número.
    if ALLOWED and From not in ALLOWED:
        return Response(content="<Response></Response>", media_type="application/xml")

    texto = Body.strip()
    if not texto:
        return Response(content="<Response></Response>", media_type="application/xml")

    if texto.lower() == "reset":
        sessions.pop(From, None)
        send_whatsapp(From, "Listo, empezamos de cero. ¿Qué necesitás?")
        return Response(content="<Response></Response>", media_type="application/xml")

    with lock:
        if From in busy:
            send_whatsapp(
                From,
                "Pará un toque, todavía estoy con tu encargo anterior. "
                "Te respondo apenas termine.",
            )
            return Response(
                content="<Response></Response>", media_type="application/xml"
            )
        busy.add(From)

    send_whatsapp(From, "Dale, me pongo con eso. Dame 1-2 minutos 🔎")
    background_tasks.add_task(procesar, From, texto)
    return Response(content="<Response></Response>", media_type="application/xml")


@app.get("/health")
def health():
    return {"ok": True, "dry_run": DRY_RUN}
