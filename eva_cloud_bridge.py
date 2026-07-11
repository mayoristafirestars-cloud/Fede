"""
Puente OFICIAL de WhatsApp para Eva — Meta WhatsApp Cloud API.

Reemplaza al bridge no-oficial (vendedor-bridge) cuando el negocio haga
los trámites de Meta. Ventajas: CERO riesgo de ban, número comercial
verificado, tilde verde posible. Gratis hasta ~1000 conversaciones/mes.

Trámites necesarios (una vez):
  1. Cuenta en developers.facebook.com + app de tipo Business
  2. Producto "WhatsApp" agregado a la app
  3. Número de teléfono registrado y verificado
  4. Token permanente + Phone Number ID
  5. Webhook apuntando a https://TU-DOMINIO/webhook (requiere VPS con HTTPS)

Config en .env:
  WA_TOKEN=...           (token permanente de Meta)
  WA_PHONE_ID=...        (Phone Number ID)
  WA_VERIFY_TOKEN=...    (palabra secreta que inventás; la misma se pone en Meta)
  VENDEDOR_HUMANO=5492954829943   (Malcom, recibe pedidos)

Correr: uvicorn eva_cloud_bridge:app --port 8010
El cerebro de Eva (vendedor_server, puerto 8003) debe estar corriendo.
"""
import base64
import os
import threading
import time

import httpx
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Request, Response

load_dotenv()

WA_TOKEN = os.getenv("WA_TOKEN", "")
WA_PHONE_ID = os.getenv("WA_PHONE_ID", "")
WA_VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN", "coronel-sur-verify")
GRAPH = "https://graph.facebook.com/v21.0"

EVA_API = os.getenv("VENDEDOR_API_URL", "http://127.0.0.1:8003/api/vendedor")
VENDEDOR_HUMANO = os.getenv("VENDEDOR_HUMANO", "5492954829943")

LIMITE_POR_NUMERO_HORA = int(os.getenv("LIMITE_POR_NUMERO_HORA", "20"))
LIMITE_GLOBAL_DIA = int(os.getenv("LIMITE_GLOBAL_DIA", "400"))

app = FastAPI(title="Eva - WhatsApp Cloud API (oficial)")

# ---- límites anti-abuso (mismos criterios que el bridge no-oficial) ----
_ventanas: dict[str, list[float]] = {}
_dia = time.strftime("%Y-%m-%d")
_hoy = 0
_lock = threading.Lock()


def permitido(numero: str) -> bool:
    global _dia, _hoy
    with _lock:
        dia = time.strftime("%Y-%m-%d")
        if dia != _dia:
            _dia, _hoy = dia, 0
        if _hoy >= LIMITE_GLOBAL_DIA:
            return False
        ahora = time.time()
        recientes = [t for t in _ventanas.get(numero, []) if ahora - t < 3600]
        if len(recientes) >= LIMITE_POR_NUMERO_HORA:
            _ventanas[numero] = recientes
            return False
        recientes.append(ahora)
        _ventanas[numero] = recientes
        _hoy += 1
        return True


# ---- envío por la Cloud API ----
def _headers():
    return {"Authorization": f"Bearer {WA_TOKEN}"}


def enviar_texto(a: str, texto: str) -> None:
    for parte in (texto[i:i + 3500] for i in range(0, len(texto), 3500)):
        r = httpx.post(
            f"{GRAPH}/{WA_PHONE_ID}/messages", headers=_headers(),
            json={"messaging_product": "whatsapp", "to": a,
                  "type": "text", "text": {"body": parte}},
            timeout=15,
        )
        if r.status_code != 200:
            print(f"[cloud] Error enviando texto: {r.status_code} {r.text[:200]}")


def enviar_imagen(a: str, url: str, caption: str = "") -> None:
    imagen = {"link": url}
    if caption:
        imagen["caption"] = caption[:1024]  # límite de caption de WhatsApp
    r = httpx.post(
        f"{GRAPH}/{WA_PHONE_ID}/messages", headers=_headers(),
        json={"messaging_product": "whatsapp", "to": a,
              "type": "image", "image": imagen},
        timeout=15,
    )
    if r.status_code != 200:
        print(f"[cloud] Error enviando imagen: {r.status_code} {r.text[:200]}")


def descargar_audio(media_id: str) -> tuple[bytes, str]:
    meta = httpx.get(f"{GRAPH}/{media_id}", headers=_headers(), timeout=15).json()
    audio = httpx.get(meta["url"], headers=_headers(), timeout=30)
    return audio.content, meta.get("mime_type", "audio/ogg")


# ---- procesamiento ----
def procesar(numero: str, payload: dict) -> None:
    try:
        tipo = payload.get("type")
        if tipo == "text":
            data = httpx.post(EVA_API, json={
                "session_id": numero, "message": payload["text"]["body"],
                "telefono": numero,
            }, timeout=180).json()
        elif tipo == "audio":
            contenido, mime = descargar_audio(payload["audio"]["id"])
            data = httpx.post(EVA_API + "/audio", json={
                "session_id": numero,
                "audio_b64": base64.b64encode(contenido).decode(),
                "mimetype": mime, "telefono": numero,
            }, timeout=300).json()
        elif tipo in ("image", "video", "document", "sticker"):
            enviar_texto(numero,
                         "Por ahora no puedo ver fotos ni archivos 🙈 Contame por "
                         "texto qué producto buscás y te paso precio y foto al toque.")
            return
        else:
            return

        secuencia = data.get("secuencia") or []
        if secuencia:
            # Orden natural: producto -> su foto -> producto -> su foto -> ...
            for parte in secuencia:
                if parte.get("tipo") == "texto" and parte.get("contenido"):
                    enviar_texto(numero, parte["contenido"])
                elif parte.get("tipo") == "foto" and str(parte.get("url", "")).startswith("http"):
                    enviar_imagen(numero, parte["url"], parte.get("caption", ""))
        else:
            if data.get("response"):
                enviar_texto(numero, data["response"])
            for foto in data.get("fotos", []):
                if foto.startswith("http"):
                    enviar_imagen(numero, foto)
        if data.get("pedido"):
            # Nota: si Malcom no escribió al número en las últimas 24hs,
            # Meta puede rechazar este mensaje (ventana de 24hs). El pedido
            # igual queda en el sistema (pestaña Agente).
            enviar_texto(
                VENDEDOR_HUMANO,
                f"🛒 *NUEVO PEDIDO* (via Eva)\nCliente: +{numero}\n"
                f"WhatsApp: https://wa.me/{numero}\n\n{data['pedido']}",
            )
    except Exception as e:
        print(f"[cloud] Error procesando mensaje de {numero}: {e}")
        try:
            enviar_texto(numero, "Disculpá, tuve un problema técnico. Probá de nuevo en un ratito 🙏")
        except Exception:
            pass


@app.get("/webhook")
def verificar(request: Request):
    """Verificación inicial del webhook (Meta manda un challenge)."""
    params = request.query_params
    if (params.get("hub.mode") == "subscribe"
            and params.get("hub.verify_token") == WA_VERIFY_TOKEN):
        return Response(content=params.get("hub.challenge", ""), media_type="text/plain")
    return Response(status_code=403)


@app.post("/webhook")
async def recibir(request: Request, background_tasks: BackgroundTasks):
    """Recibe los mensajes entrantes de WhatsApp."""
    body = await request.json()
    try:
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                for msg in change.get("value", {}).get("messages", []):
                    numero = msg.get("from", "")
                    if not numero or not permitido(numero):
                        continue
                    background_tasks.add_task(procesar, numero, msg)
    except Exception as e:
        print(f"[cloud] Webhook con formato inesperado: {e}")
    return {"status": "ok"}  # siempre 200 rápido, si no Meta reintenta


@app.get("/health")
def health():
    return {"ok": True, "configurado": bool(WA_TOKEN and WA_PHONE_ID)}
