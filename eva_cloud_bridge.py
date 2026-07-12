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
import hashlib
import hmac
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
# App Secret de Meta: valida que el webhook viene DE VERDAD de Meta (firma HMAC).
# Si está vacío, no se valida (se avisa por log) — cargarlo en producción.
WA_APP_SECRET = os.getenv("WA_APP_SECRET", "")
GRAPH = "https://graph.facebook.com/v21.0"

# Deduplicación: message.id ya procesados (evita responder/cobrar dos veces
# si Meta reenvía el mismo evento).
_vistos: "OrderedDict[str, float]" = None
from collections import OrderedDict
_vistos = OrderedDict()
_vistos_lock = threading.Lock()


def ya_procesado(msg_id: str) -> bool:
    """True si este message.id ya fue procesado (y lo registra si es nuevo)."""
    if not msg_id:
        return False
    with _vistos_lock:
        if msg_id in _vistos:
            return True
        _vistos[msg_id] = time.time()
        while len(_vistos) > 500:  # conservar los últimos 500
            _vistos.popitem(last=False)
        return False


def firma_valida(cuerpo: bytes, cabecera: str) -> bool:
    """Verifica el header X-Hub-Signature-256 con el App Secret.
    A prueba de fallas: si no hay App Secret configurado, se RECHAZA el webhook
    (antes se aceptaba cualquier POST, que era un agujero de seguridad)."""
    if not WA_APP_SECRET:
        print("[cloud] ⚠️ WA_APP_SECRET vacío: rechazo el webhook por seguridad. Cargalo en .env.")
        return False
    if not cabecera or not cabecera.startswith("sha256="):
        return False
    esperado = "sha256=" + hmac.new(
        WA_APP_SECRET.encode(), cuerpo, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(esperado, cabecera)

EVA_API = os.getenv("VENDEDOR_API_URL", "http://127.0.0.1:8003/api/vendedor")
VENDEDOR_HUMANO = os.getenv("VENDEDOR_HUMANO", "5492954829943")
# Tu número, para avisarte si Eva toca el tope global del día.
ALERTA_WHATSAPP = os.getenv("ALERTA_WHATSAPP", "")
# Token compartido con el sistema para pedidos máquina-a-máquina (ej: aviso de pago).
AGENTE_TOKEN = os.getenv("AGENTE_TOKEN", "eva-coronel-2026")

LIMITE_POR_NUMERO_HORA = int(os.getenv("LIMITE_POR_NUMERO_HORA", "20"))
LIMITE_GLOBAL_DIA = int(os.getenv("LIMITE_GLOBAL_DIA", "400"))

app = FastAPI(title="Eva - WhatsApp Cloud API (oficial)")

# ---- límites anti-abuso (mismos criterios que el bridge no-oficial) ----
_ventanas: dict[str, list[float]] = {}
_dia = time.strftime("%Y-%m-%d")
_hoy = 0
_lock = threading.Lock()
_aviso_tope: dict[str, float] = {}   # numero -> último aviso "mucha demanda"
_aviso_global_dia = ""               # día en que ya avisé al dueño del tope global


def estado_limite(numero: str) -> str:
    """Devuelve 'ok', 'numero' (tope por número/hora) o 'global' (tope del día)."""
    global _dia, _hoy
    with _lock:
        dia = time.strftime("%Y-%m-%d")
        if dia != _dia:
            _dia, _hoy = dia, 0
        if _hoy >= LIMITE_GLOBAL_DIA:
            return "global"
        ahora = time.time()
        recientes = [t for t in _ventanas.get(numero, []) if ahora - t < 3600]
        if len(recientes) >= LIMITE_POR_NUMERO_HORA:
            _ventanas[numero] = recientes
            return "numero"
        recientes.append(ahora)
        _ventanas[numero] = recientes
        _hoy += 1
        return "ok"


def avisar_tope(numero: str, motivo: str) -> None:
    """Cuando un cliente pega contra un tope, NO lo dejamos mudo: le mandamos
    UN aviso (como mucho 1 por hora por número, para no spamear) y, si es el
    tope global del día, te avisamos a vos una sola vez."""
    ahora = time.time()
    with _lock:
        avisar_cliente = (ahora - _aviso_tope.get(numero, 0)) > 3600
        if avisar_cliente:
            _aviso_tope[numero] = ahora
    if avisar_cliente:
        try:
            enviar_texto(numero,
                         "¡Estamos con mucha demanda en este momento! 🙌 "
                         "Un vendedor te va a escribir enseguida para ayudarte.")
        except Exception:
            pass
    if motivo == "global" and ALERTA_WHATSAPP:
        global _aviso_global_dia
        with _lock:
            hoy = time.strftime("%Y-%m-%d")
            avisar_duenio = _aviso_global_dia != hoy
            if avisar_duenio:
                _aviso_global_dia = hoy
        if avisar_duenio:
            try:
                enviar_texto(
                    ALERTA_WHATSAPP,
                    f"⚠️ Eva alcanzó el tope de {LIMITE_GLOBAL_DIA} mensajes de hoy. "
                    "Los clientes están recibiendo un aviso de 'mucha demanda'. "
                    "Si es tráfico real, avisame y subimos el tope.")
            except Exception:
                pass


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


# Caché de imágenes ya subidas a Meta: url -> (media_id, timestamp).
# Meta conserva el media ~30 días; re-subimos pasados 25 por las dudas.
_media_cache: dict[str, tuple[str, float]] = {}
_media_lock = threading.Lock()
_MEDIA_TTL = 25 * 86400


def subir_media(url: str) -> str:
    """Descarga la imagen (el servidor SÍ puede leer FactuPyme aunque Meta no)
    y la sube a Meta. Devuelve el media_id, o '' si falla. Cachea el resultado."""
    with _media_lock:
        cache = _media_cache.get(url)
        if cache and (time.time() - cache[1]) < _MEDIA_TTL:
            return cache[0]
    try:
        img = httpx.get(url, timeout=20, follow_redirects=True)
        if img.status_code != 200 or not img.content:
            print(f"[cloud] No pude descargar la imagen ({img.status_code}): {url[:60]}")
            return ""
        mime = img.headers.get("content-type", "image/jpeg").split(";")[0]
        if mime not in ("image/jpeg", "image/png"):
            mime = "image/jpeg"
        r = httpx.post(
            f"{GRAPH}/{WA_PHONE_ID}/media",
            headers=_headers(),
            data={"messaging_product": "whatsapp", "type": mime},
            files={"file": ("foto.jpg", img.content, mime)},
            timeout=30,
        )
        if r.status_code == 200:
            media_id = r.json().get("id", "")
            if media_id:
                with _media_lock:
                    _media_cache[url] = (media_id, time.time())
                return media_id
        print(f"[cloud] Error subiendo media: {r.status_code} {r.text[:150]}")
    except Exception as e:
        print(f"[cloud] subir_media falló: {e}")
    return ""


def enviar_imagen(a: str, url: str, caption: str = "") -> None:
    # 1) Intentar por media_id (servidor descarga + sube -> Meta siempre puede enviarla)
    media_id = subir_media(url)
    if media_id:
        imagen = {"id": media_id}
    else:
        imagen = {"link": url}  # fallback: link directo
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
        # Si falló con media_id, reintentar con link como último recurso
        if media_id:
            imagen2 = {"link": url}
            if caption:
                imagen2["caption"] = caption[:1024]
            httpx.post(
                f"{GRAPH}/{WA_PHONE_ID}/messages", headers=_headers(),
                json={"messaging_product": "whatsapp", "to": a,
                      "type": "image", "image": imagen2},
                timeout=15,
            )


def descargar_audio(media_id: str) -> tuple[bytes, str]:
    meta = httpx.get(f"{GRAPH}/{media_id}", headers=_headers(), timeout=15).json()
    audio = httpx.get(meta["url"], headers=_headers(), timeout=30)
    return audio.content, meta.get("mime_type", "audio/ogg")


# ---- procesamiento ----
def procesar(numero: str, payload: dict) -> None:
    algo_enviado = False  # ¿le mandamos ALGO al cliente? Si no, nunca lo dejamos mudo.
    try:
        tipo = payload.get("type")
        if tipo == "text":
            r = httpx.post(EVA_API, json={
                "session_id": numero, "message": payload["text"]["body"],
                "telefono": numero,
            }, timeout=180)
            r.raise_for_status()  # 500 del cerebro -> excepción -> fallback (no silencio)
            data = r.json()
        elif tipo == "audio":
            contenido, mime = descargar_audio(payload["audio"]["id"])
            r = httpx.post(EVA_API + "/audio", json={
                "session_id": numero,
                "audio_b64": base64.b64encode(contenido).decode(),
                "mimetype": mime, "telefono": numero,
            }, timeout=300)
            r.raise_for_status()
            data = r.json()
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
                    algo_enviado = True
                elif parte.get("tipo") == "foto" and str(parte.get("url", "")).startswith("http"):
                    enviar_imagen(numero, parte["url"], parte.get("caption", ""))
                    algo_enviado = True
        else:
            if data.get("response"):
                enviar_texto(numero, data["response"])
                algo_enviado = True
            for foto in data.get("fotos", []):
                if foto.startswith("http"):
                    enviar_imagen(numero, foto)
                    algo_enviado = True
        # El cerebro respondió 200 pero sin nada visible: igual contestamos algo.
        if not algo_enviado:
            enviar_texto(numero, "Dame un segundito que lo reviso y te confirmo 🙌")
            algo_enviado = True
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
        # Solo mandamos el aviso de error si el cliente no recibió NADA todavía
        # (si ya le mandamos medio pedido, no lo asustamos con un "error").
        if not algo_enviado:
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
    cuerpo = await request.body()
    # 1) Validar que el POST viene DE VERDAD de Meta (firma HMAC)
    if not firma_valida(cuerpo, request.headers.get("X-Hub-Signature-256", "")):
        print("[cloud] Webhook rechazado: firma inválida")
        return Response(status_code=403)
    if not WA_APP_SECRET:
        print("[cloud] ⚠️ WA_APP_SECRET vacío: el webhook NO valida firma (cargalo en .env)")

    import json as _json
    try:
        body = _json.loads(cuerpo)
    except Exception:
        return {"status": "ok"}

    try:
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                for msg in change.get("value", {}).get("messages", []):
                    numero = msg.get("from", "")
                    # 2) Deduplicar: no procesar dos veces el mismo mensaje
                    if ya_procesado(msg.get("id", "")):
                        continue
                    if not numero:
                        continue
                    # 3) Topes: si se pasó, NO lo dejamos mudo -> le avisamos.
                    estado = estado_limite(numero)
                    if estado != "ok":
                        background_tasks.add_task(avisar_tope, numero, estado)
                        continue
                    background_tasks.add_task(procesar, numero, msg)
    except Exception as e:
        print(f"[cloud] Webhook con formato inesperado: {e}")
    return {"status": "ok"}  # siempre 200 rápido, si no Meta reintenta


@app.post("/notificar")
async def notificar_interno(request: Request):
    """Endpoint INTERNO (localhost): el sistema Coronel Sur pide enviar un
    WhatsApp por Eva — ej: avisar que un pago se acreditó. Protegido por X-Token
    (el mismo AGENTE_TOKEN máquina-a-máquina)."""
    if request.headers.get("X-Token") != AGENTE_TOKEN:
        return Response(status_code=401)
    try:
        data = await request.json()
    except Exception:
        return Response(status_code=400)
    a = str(data.get("a", "")).strip()
    texto = str(data.get("texto", "")).strip()
    if not a or not texto:
        return {"ok": False}
    try:
        enviar_texto(a, texto)
        return {"ok": True}
    except Exception as e:
        print(f"[cloud] /notificar falló: {e}")
        return {"ok": False}


@app.get("/health")
def health():
    return {"ok": True, "configurado": bool(WA_TOKEN and WA_PHONE_ID)}
