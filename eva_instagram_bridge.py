"""
Cartero de Instagram para Eva — Instagram API con Instagram Login (Meta).

Gemelo de eva_cloud_bridge.py (WhatsApp) pero para los DMs de Instagram.
Recibe el DM por webhook -> se lo pasa al MISMO cerebro (vendedor_server,
:8003) -> manda la respuesta por la API de Instagram (graph.instagram.com).

Corre como proceso APARTE (no toca el de WhatsApp): si algo de Instagram
falla, WhatsApp —el canal probado— no se ve afectado.

El cerebro es agnóstico del canal: los pedidos que se confirmen se crean
igual como presupuesto en el ERP (lo hace vendedor_server vía CORONEL_URL),
así que este cartero solo se ocupa de recibir el DM y responderlo.

Config en .env (las claves NUNCA en git):
  IG_TOKEN=...          Instagram User access token (app "Dist Coronel Sur-IG")
  IG_APP_SECRET=...     Clave secreta de la app de Instagram (valida la firma del webhook)
  IG_VERIFY_TOKEN=...   palabra secreta que inventás; la misma se pone en Meta
  IG_ID=me              opcional; 'me' resuelve a la cuenta del token

Correr: uvicorn eva_instagram_bridge:app --host 127.0.0.1 --port 8012
El cerebro (vendedor_server, :8003) debe estar corriendo.
"""
import hashlib
import hmac
import json as _json
import os
import threading
import time
from collections import OrderedDict

import httpx
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Request, Response

load_dotenv()

IG_TOKEN = os.getenv("IG_TOKEN", "")
IG_APP_SECRET = os.getenv("IG_APP_SECRET", "")
IG_VERIFY_TOKEN = os.getenv("IG_VERIFY_TOKEN", "coronel-sur-ig-verify")
IG_ID = os.getenv("IG_ID", "me")
GRAPH = "https://graph.instagram.com/v21.0"

# El cerebro de Eva (mismo que usa WhatsApp).
EVA_API = os.getenv("VENDEDOR_API_URL", "http://127.0.0.1:8003/api/vendedor")

# Topes anti-abuso (por usuario/hora y global/día).
LIMITE_POR_USUARIO_HORA = int(os.getenv("IG_LIMITE_POR_USUARIO_HORA", "30"))
LIMITE_GLOBAL_DIA = int(os.getenv("IG_LIMITE_GLOBAL_DIA", "500"))

app = FastAPI(title="Eva - Instagram DM (Instagram Login)")

# ---- Deduplicación de message.mid (Meta reenvía eventos) ----
_vistos: "OrderedDict[str, float]" = OrderedDict()
_vistos_lock = threading.Lock()


def ya_procesado(mid: str) -> bool:
    if not mid:
        return False
    with _vistos_lock:
        if mid in _vistos:
            return True
        _vistos[mid] = time.time()
        while len(_vistos) > 500:
            _vistos.popitem(last=False)
        return False


# ---- Límites anti-abuso ----
_ventanas: dict[str, list[float]] = {}
_dia = time.strftime("%Y-%m-%d")
_hoy = 0
_lock = threading.Lock()


def permitido(uid: str) -> bool:
    global _dia, _hoy
    with _lock:
        dia = time.strftime("%Y-%m-%d")
        if dia != _dia:
            _dia, _hoy = dia, 0
        if _hoy >= LIMITE_GLOBAL_DIA:
            return False
        ahora = time.time()
        recientes = [t for t in _ventanas.get(uid, []) if ahora - t < 3600]
        if len(recientes) >= LIMITE_POR_USUARIO_HORA:
            _ventanas[uid] = recientes
            return False
        recientes.append(ahora)
        _ventanas[uid] = recientes
        _hoy += 1
        return True


# ---- Firma del webhook (viene DE VERDAD de Meta) ----
def firma_valida(cuerpo: bytes, cabecera: str) -> bool:
    if not IG_APP_SECRET:
        print("[ig] ⚠️ IG_APP_SECRET vacío: rechazo el webhook por seguridad. Cargalo en .env.")
        return False
    if not cabecera or not cabecera.startswith("sha256="):
        return False
    esperado = "sha256=" + hmac.new(
        IG_APP_SECRET.encode(), cuerpo, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(esperado, cabecera)


# ---- Envío por la API de Instagram ----
def enviar_texto(igsid: str, texto: str) -> None:
    # IG corta los DMs largos; troceamos en ~900 chars.
    for parte in (texto[i:i + 900] for i in range(0, len(texto), 900)):
        try:
            r = httpx.post(
                f"{GRAPH}/{IG_ID}/messages",
                params={"access_token": IG_TOKEN},
                json={"recipient": {"id": igsid}, "message": {"text": parte}},
                timeout=15,
            )
            if r.status_code != 200:
                print(f"[ig] Error enviando texto: {r.status_code} {r.text[:200]}")
        except Exception as e:
            print(f"[ig] enviar_texto falló: {e}")


def enviar_imagen(igsid: str, url: str, caption: str = "") -> None:
    # En Instagram la imagen va como attachment por URL; el pie (si hay) como texto aparte.
    try:
        r = httpx.post(
            f"{GRAPH}/{IG_ID}/messages",
            params={"access_token": IG_TOKEN},
            json={"recipient": {"id": igsid},
                  "message": {"attachment": {"type": "image", "payload": {"url": url}}}},
            timeout=20,
        )
        if r.status_code != 200:
            print(f"[ig] Error enviando imagen: {r.status_code} {r.text[:200]}")
    except Exception as e:
        print(f"[ig] enviar_imagen falló: {e}")
    if caption:
        enviar_texto(igsid, caption)


# ---- Procesamiento: DM -> cerebro -> respuesta ----
def procesar(igsid: str, texto: str) -> None:
    algo_enviado = False
    try:
        r = httpx.post(
            EVA_API,
            json={"session_id": igsid, "message": texto, "telefono": ""},
            timeout=180,
        )
        r.raise_for_status()
        data = r.json()

        secuencia = data.get("secuencia") or []
        if secuencia:
            for parte in secuencia:
                if parte.get("tipo") == "texto" and parte.get("contenido"):
                    enviar_texto(igsid, parte["contenido"])
                    algo_enviado = True
                elif parte.get("tipo") == "foto" and str(parte.get("url", "")).startswith("http"):
                    enviar_imagen(igsid, parte["url"], parte.get("caption", ""))
                    algo_enviado = True
        else:
            if data.get("response"):
                enviar_texto(igsid, data["response"])
                algo_enviado = True
            for foto in data.get("fotos", []):
                if str(foto).startswith("http"):
                    enviar_imagen(igsid, foto)
                    algo_enviado = True

        if not algo_enviado:
            enviar_texto(igsid, "Dame un segundito que lo reviso y te confirmo 🙌")
    except Exception as e:
        print(f"[ig] Error procesando DM de {igsid}: {e}")
        if not algo_enviado:
            try:
                enviar_texto(igsid, "Disculpá, tuve un problema técnico. Probá de nuevo en un ratito 🙏")
            except Exception:
                pass


# ---- Webhook ----
@app.get("/ig/webhook")
def verificar(request: Request):
    """Verificación inicial del webhook (Meta manda un challenge)."""
    p = request.query_params
    if (p.get("hub.mode") == "subscribe"
            and p.get("hub.verify_token") == IG_VERIFY_TOKEN):
        return Response(content=p.get("hub.challenge", ""), media_type="text/plain")
    return Response(status_code=403)


@app.post("/ig/webhook")
async def recibir(request: Request, background_tasks: BackgroundTasks):
    """Recibe los DMs entrantes de Instagram."""
    cuerpo = await request.body()
    if not firma_valida(cuerpo, request.headers.get("X-Hub-Signature-256", "")):
        print("[ig] Webhook rechazado: firma inválida")
        return Response(status_code=403)
    try:
        body = _json.loads(cuerpo)
    except Exception:
        return {"status": "ok"}

    try:
        for entry in body.get("entry", []):
            for m in entry.get("messaging", []):
                msg = m.get("message") or {}
                if msg.get("is_echo"):        # eco de lo que mandamos nosotros -> ignorar
                    continue
                igsid = (m.get("sender") or {}).get("id", "")
                if not igsid:
                    continue
                if ya_procesado(msg.get("mid", "")):
                    continue
                texto = msg.get("text")
                if not texto:
                    # Adjuntos (foto/audio/historia/sticker): pedimos texto.
                    if msg.get("attachments"):
                        background_tasks.add_task(
                            enviar_texto, igsid,
                            "¡Hola! 🙂 Por acá te leo mejor por texto — contame qué "
                            "producto buscás y te paso precio y foto.")
                    continue
                if not permitido(igsid):      # tope -> no lo dejamos en loop, simplemente no respondemos
                    continue
                background_tasks.add_task(procesar, igsid, texto)
    except Exception as e:
        print(f"[ig] Webhook con formato inesperado: {e}")
    return {"status": "ok"}  # siempre 200 rápido, si no Meta reintenta


@app.get("/health")
def health():
    return {"ok": True, "configurado": bool(IG_TOKEN and IG_APP_SECRET)}
