"""
Webhook de Mercado Pago — cierra el círculo del pago.

Cuando un cliente paga el link que le mandó Eva, Mercado Pago avisa acá.
El flujo:
  1. MP nos notifica (POST /api/pagos/webhook) con el id del pago.
  2. RECONSULTAMOS el pago a la API de MP con nuestro token (autoritativo:
     un webhook falso no sirve, porque validamos contra MP directamente).
  3. Si está 'approved', marcamos el pedido (comprobante origen='eva') como
     'cobrado' — de forma idempotente (no procesa dos veces el mismo pago).
  4. Avisamos por WhatsApp (via el bridge de Eva): a Malcom/dueño para preparar,
     y al cliente confirmándole que recibimos el pago.

Config en .env:
  MP_ACCESS_TOKEN=APP_USR-...   (token de PRODUCCIÓN de Mercado Pago)
  EVA_BRIDGE_URL=http://127.0.0.1:8011   (opcional; donde corre eva_cloud_bridge)
  ALERTA_WHATSAPP=549...        (tu número, recibe el aviso de pago)
"""
import os
import sys

import httpx
from fastapi import APIRouter, BackgroundTasks, Request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar

router = APIRouter(prefix="/api/pagos", tags=["pagos"])

MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN", "")
BRIDGE_URL = os.getenv("EVA_BRIDGE_URL", "http://127.0.0.1:8011").rstrip("/")
AGENTE_TOKEN = os.getenv("AGENTE_TOKEN", "eva-coronel-2026")
ALERTA_WHATSAPP = os.getenv("ALERTA_WHATSAPP", "")
VENDEDOR_HUMANO = os.getenv("VENDEDOR_HUMANO", "")


def _avisar_whatsapp(a: str, texto: str) -> None:
    """Le pide al bridge de Eva (localhost) que mande un WhatsApp. Best-effort."""
    a = "".join(ch for ch in (a or "") if ch.isdigit())
    if not a:
        return
    try:
        httpx.post(f"{BRIDGE_URL}/notificar",
                   json={"a": a, "texto": texto},
                   headers={"X-Token": AGENTE_TOKEN}, timeout=8)
    except Exception as e:
        print(f"[pagos] no pude avisar por WhatsApp: {e}")


def _consultar_pago(payment_id: str) -> dict | None:
    try:
        r = httpx.get(
            f"https://api.mercadopago.com/v1/payments/{payment_id}",
            headers={"Authorization": f"Bearer {MP_ACCESS_TOKEN}"}, timeout=15)
        if r.status_code == 200:
            return r.json()
        print(f"[pagos] MP respondió {r.status_code} al consultar el pago {payment_id}")
    except Exception as e:
        print(f"[pagos] error consultando el pago {payment_id}: {e}")
    return None


def procesar_pago(payment_id: str) -> None:
    """Consulta el pago a MP y, si está acreditado, cierra el pedido y avisa."""
    if not MP_ACCESS_TOKEN:
        print("[pagos] MP_ACCESS_TOKEN no configurado; ignoro el webhook.")
        return
    pago = _consultar_pago(payment_id)
    if not pago:
        return
    if pago.get("status") != "approved":
        return  # solo nos interesa el pago efectivamente acreditado
    referencia = (pago.get("external_reference") or "").strip()
    monto = pago.get("transaction_amount") or 0
    # Datos del pagador que trae MP -> sirven para enriquecer el CRM.
    payer = pago.get("payer") or {}
    ident = payer.get("identification") or {}
    dni = "".join(ch for ch in str(ident.get("number") or "") if ch.isdigit())
    email = (payer.get("email") or "").strip()
    nombre_pagador = " ".join(
        x for x in [payer.get("first_name"), payer.get("last_name")] if x).strip()

    conn = conectar()
    try:
        # Idempotencia: si ya registramos este pago, no repetimos nada.
        if conn.execute("SELECT 1 FROM pagos_mp WHERE payment_id = ?",
                        (str(payment_id),)).fetchone():
            return
        comp = conn.execute(
            "SELECT id, numero, cliente_id FROM comprobantes "
            "WHERE numero = ? AND origen = 'eva'", (referencia,)).fetchone()
        conn.execute(
            "INSERT INTO pagos_mp (payment_id, referencia, comprobante_id, monto, estado) "
            "VALUES (?, ?, ?, ?, 'approved')",
            (str(payment_id), referencia, comp["id"] if comp else None, monto))
        tel_cliente = ""
        if comp:
            conn.execute("UPDATE comprobantes SET estado = 'cobrado' WHERE id = ?",
                         (comp["id"],))
            cli = conn.execute(
                "SELECT nombre, telefono, email, dni FROM clientes WHERE id = ?",
                (comp["cliente_id"],)).fetchone()
            if cli:
                tel_cliente = (cli["telefono"] or "")
                # CRM: completar SOLO lo que falta (no pisar datos cargados a mano).
                nuevos = {}
                if dni and not (cli["dni"] or "").strip():
                    nuevos["dni"] = dni
                if email and not (cli["email"] or "").strip():
                    nuevos["email"] = email
                nombre_actual = (cli["nombre"] or "").strip()
                if nombre_pagador and (not nombre_actual or nombre_actual.startswith("WhatsApp ")):
                    nuevos["nombre"] = nombre_pagador
                if nuevos:
                    sets = ", ".join(f"{k} = ?" for k in nuevos)
                    conn.execute(
                        f"UPDATE clientes SET {sets}, "
                        "actualizado_en = datetime('now','localtime') WHERE id = ?",
                        (*nuevos.values(), comp["cliente_id"]))
                    print(f"[pagos] CRM enriquecido (cliente {comp['cliente_id']}): "
                          f"{', '.join(nuevos)}")
        conn.commit()
        numero_txt = comp["numero"] if comp else (referencia or "s/ref")
    finally:
        conn.close()

    # Avisos (best-effort, nunca rompen el webhook)
    destino_duenio = ALERTA_WHATSAPP or VENDEDOR_HUMANO
    _avisar_whatsapp(
        destino_duenio,
        f"💰 *PAGO ACREDITADO* — pedido {numero_txt}\n"
        f"Monto: ${monto:,.0f}\nYa podés prepararlo/entregarlo.")
    if tel_cliente:
        _avisar_whatsapp(
            tel_cliente,
            f"¡Recibimos tu pago! ✅ Tu pedido {numero_txt} quedó confirmado y lo "
            "estamos preparando. ¡Gracias por tu compra! 🙌")
    print(f"[pagos] Pago {payment_id} acreditado -> pedido {numero_txt} marcado cobrado.")


def _extraer_payment_id(qp, body: dict) -> str:
    """MP notifica en varios formatos; sacamos el id del pago de cualquiera."""
    if qp.get("topic") == "payment" or qp.get("type") == "payment":
        pid = qp.get("id") or qp.get("data.id")
        if pid:
            return str(pid)
    if body.get("type") == "payment":
        pid = (body.get("data") or {}).get("id")
        if pid:
            return str(pid)
    if body.get("topic") == "payment":
        pid = body.get("id") or (body.get("data") or {}).get("id")
        if pid:
            return str(pid)
    return ""


@router.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    """Recibe la notificación de Mercado Pago. Responde 200 rápido siempre."""
    try:
        body = await request.json()
    except Exception:
        body = {}
    payment_id = _extraer_payment_id(request.query_params, body if isinstance(body, dict) else {})
    if payment_id:
        background_tasks.add_task(procesar_pago, payment_id)
    return {"status": "ok"}


@router.get("/webhook")
def webhook_ping():
    """MP a veces hace un GET para chequear que el endpoint existe."""
    return {"ok": True}
