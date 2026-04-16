"""
Router del bot — webhooks de Meta (WhatsApp + Instagram).

Endpoints públicos (los llama Meta, sin auth de usuario):
- GET  /webhooks/meta  →  verificación (handshake).
- POST /webhooks/meta  →  recepción de mensajes.

Firma HMAC con X-Hub-Signature-256 obligatoria en POST.

Endpoints internos (requieren auth admin):
- GET  /api/bot/stats    →  métricas básicas
- POST /api/bot/probar   →  simular un mensaje para testing en seco
"""
from __future__ import annotations

import logging
import os
import sys
import traceback

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot import claude, conversaciones, meta, productos, prompts, transcribe
from db.database import conectar
from security import require_admin


log = logging.getLogger("bot.router")

router = APIRouter(tags=["bot"])


# Caché muy simple en memoria del inventario renderizado para el
# prompt. Se refresca cada TTL_INVENTARIO_SEGUNDOS. Si el usuario hace
# cambios en el inventario, el bot los ve al próximo refresh.
_CACHE = {"fecha": 0.0, "texto": ""}
_TTL = int(os.environ.get("BOT_INVENTARIO_TTL_SEG", "300"))  # 5 min


def _get_inventario_texto() -> str:
    import time
    ahora = time.time()
    if (ahora - _CACHE["fecha"]) < _TTL and _CACHE["texto"]:
        return _CACHE["texto"]
    try:
        snapshot = productos.snapshot_para_prompt(limit=150)
        texto = prompts.render_inventario(snapshot, max_items=150)
    except Exception:
        log.exception("Error renderizando inventario")
        texto = "INVENTARIO: (error al cargar)"
    _CACHE["fecha"] = ahora
    _CACHE["texto"] = texto
    return texto


# ─── Webhook Meta ──────────────────────────────────────────

@router.get("/webhooks/meta", response_class=PlainTextResponse)
def webhook_verificar(
    mode: str = Query("", alias="hub.mode"),
    token: str = Query("", alias="hub.verify_token"),
    challenge: str = Query("", alias="hub.challenge"),
):
    """Handshake GET — Meta llama esto una sola vez al configurar."""
    resp = meta.verificar_webhook(mode, token, challenge)
    if resp is None:
        raise HTTPException(status_code=403, detail="Token inválido")
    return resp


@router.post("/webhooks/meta")
async def webhook_recibir(
    request: Request,
    background: BackgroundTasks,
):
    """
    Recibe mensajes. Devuelve 200 rápido y procesa en background.
    Meta reintenta si tarda más de ~20s.
    """
    body = await request.body()
    firma = request.headers.get("x-hub-signature-256", "")

    if not meta.validar_firma(body, firma):
        log.warning("Webhook con firma inválida")
        raise HTTPException(status_code=401, detail="Firma inválida")

    payload = await request.json()

    try:
        mensajes = meta.parsear_mensajes(payload)
    except Exception:
        log.exception("Error parseando payload")
        return {"ok": True}  # Meta considera error si devolvemos !=2xx

    for m in mensajes:
        if conversaciones.ya_procesado(m.message_id):
            continue
        # Procesar en background: así devolvemos 200 a Meta al toque.
        background.add_task(_procesar_mensaje, m)

    return {"ok": True}


def _procesar_mensaje(m: meta.MensajeEntrante) -> None:
    """Pipeline completo para un mensaje entrante."""
    try:
        conversaciones.marcar_procesado(m.message_id)

        # 1. Resolver texto del mensaje
        texto = m.texto
        if m.tipo == "audio" and not texto:
            texto = _transcribir_audio(m) or ""
        if not texto.strip():
            # Si no pudimos sacar texto, pedimos amablemente que escriba
            texto_respuesta = (
                "Perdón, no pude entender tu mensaje. ¿Podés escribirlo en "
                "texto así te ayudo?"
            )
            meta.enviar(m.canal, m.sesion_id, texto_respuesta)
            return

        # 2. Sesión + guardar mensaje del user
        sesion = conversaciones.obtener_sesion(
            canal=m.canal,
            sesion_id=m.sesion_id,
            telefono=m.telefono,
            nombre_cliente=m.nombre_cliente,
        )
        sesion_id_db = sesion["id"]

        conversaciones.agregar_mensaje(sesion_id_db, "user", texto)

        # 3. Armar contexto
        historial = conversaciones.ultimos_mensajes(sesion_id_db)
        # Quitar el último mensaje (ya lo vamos a pasar como user_message
        # en claude.responder)
        historial_previo = historial[:-1] if historial else []

        system_reglas = prompts.system_reglas()
        inventario_txt = _get_inventario_texto()

        # 4. Llamar a Claude
        respuesta = claude.responder(
            system_reglas=system_reglas,
            inventario_texto=inventario_txt,
            historial=historial_previo,
            mensaje_usuario=texto,
        )

        # 5. Guardar respuesta y enviar
        conversaciones.agregar_mensaje(sesion_id_db, "assistant", respuesta)
        meta.enviar(m.canal, m.sesion_id, respuesta)

    except Exception as e:
        log.error(
            "Error procesando mensaje %s (canal=%s): %s\n%s",
            m.message_id, m.canal, e, traceback.format_exc(),
        )
        try:
            meta.enviar(
                m.canal,
                m.sesion_id,
                "Tuve un problema técnico procesando tu mensaje. Un humano "
                "te va a responder en cuanto pueda.",
            )
        except Exception:
            pass


def _transcribir_audio(m: meta.MensajeEntrante) -> str | None:
    if m.canal != "whatsapp":
        return None  # IG trae URL directa — implementación mínima no lo usa
    data = meta.bajar_media_whatsapp(m.media_id)
    if not data:
        return None
    return transcribe.transcribir(data, formato_hint="ogg")


# ─── Endpoints internos (admin) ────────────────────────────

@router.get("/api/bot/stats", dependencies=[Depends(require_admin)])
def stats():
    """Métricas básicas del bot."""
    conn = conectar()
    try:
        sesiones = conn.execute("SELECT COUNT(*) FROM bot_sesiones").fetchone()[0]
        mensajes = conn.execute("SELECT COUNT(*) FROM bot_conversaciones").fetchone()[0]
        procesados = conn.execute(
            "SELECT COUNT(*) FROM bot_mensajes_procesados"
        ).fetchone()[0]
        por_canal = {}
        for r in conn.execute(
            "SELECT canal, COUNT(*) as n FROM bot_sesiones GROUP BY canal"
        ).fetchall():
            d = dict(r)
            por_canal[d["canal"]] = d["n"]
        return {
            "sesiones_totales": sesiones,
            "mensajes_totales": mensajes,
            "mensajes_procesados": procesados,
            "sesiones_por_canal": por_canal,
        }
    finally:
        conn.close()


class ProbarReq(BaseModel):
    texto: str
    sesion_id: str = "test:dev"
    canal: str = "whatsapp"


@router.post("/api/bot/probar", dependencies=[Depends(require_admin)])
def probar(req: ProbarReq):
    """
    Simula un mensaje entrante sin pasar por Meta. Útil para testear
    respuestas con tu inventario real desde un curl/httpie.
    """
    if not req.texto.strip():
        raise HTTPException(status_code=400, detail="Texto vacío")

    sesion = conversaciones.obtener_sesion(
        canal=req.canal,
        sesion_id=req.sesion_id,
        telefono="",
        nombre_cliente="Tester",
    )
    sesion_id_db = sesion["id"]

    conversaciones.agregar_mensaje(sesion_id_db, "user", req.texto)
    historial = conversaciones.ultimos_mensajes(sesion_id_db)
    historial_previo = historial[:-1] if historial else []

    respuesta = claude.responder(
        system_reglas=prompts.system_reglas(),
        inventario_texto=_get_inventario_texto(),
        historial=historial_previo,
        mensaje_usuario=req.texto,
    )
    conversaciones.agregar_mensaje(sesion_id_db, "assistant", respuesta)

    return {"ok": True, "respuesta": respuesta}
