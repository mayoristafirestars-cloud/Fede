"""
Generación de links de pago con Mercado Pago (Checkout Pro).

Opcional: si MP_ACCESS_TOKEN está en el .env, Eva incluye un link de
pago en cada pedido confirmado. El cliente paga al toque y, según la
política del negocio, la mercadería se reserva recién con el pago.

Cómo obtener el token (una vez):
  1. mercadopago.com.ar → Tu negocio → Credenciales
  2. Copiar el "Access Token" de PRODUCCIÓN (empieza con APP_USR-)
  3. En el .env: MP_ACCESS_TOKEN=APP_USR-...
"""
import os

MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN", "")
MP_API = "https://api.mercadopago.com/checkout/preferences"
# A dónde avisa Mercado Pago cuando el pago se acredita (el webhook del sistema).
MP_NOTIF_URL = os.getenv(
    "MP_NOTIF_URL", "https://coronelsur.com.ar/api/pagos/webhook"
)


def hay_pagos() -> bool:
    return bool(MP_ACCESS_TOKEN)


def crear_link_pago(items: list[dict], referencia: str = "") -> str:
    """Crea una preferencia de pago y devuelve el link (init_point).
    items: [{descripcion, cantidad, precio_unitario}, ...]
    Devuelve '' si no está configurado o si falla."""
    if not MP_ACCESS_TOKEN:
        return ""
    try:
        import httpx

        mp_items = [
            {
                "title": (it.get("descripcion") or "Producto")[:250],
                "quantity": int(it.get("cantidad") or 1),
                "unit_price": float(it.get("precio_unitario") or 0),
                "currency_id": "ARS",
            }
            for it in items
            if float(it.get("precio_unitario") or 0) > 0
        ]
        if not mp_items:
            return ""
        payload = {
            "items": mp_items,
            "external_reference": referencia,
            "back_urls": {
                "success": os.getenv("MP_BACK_URL", "https://wa.me/"),
            },
            "statement_descriptor": "CORONEL SUR",
        }
        # Si hay webhook configurado, MP nos avisa cuando el pago se acredita.
        if MP_NOTIF_URL:
            payload["notification_url"] = MP_NOTIF_URL
        r = httpx.post(
            MP_API,
            headers={"Authorization": f"Bearer {MP_ACCESS_TOKEN}"},
            json=payload,
            timeout=15,
        )
        if r.status_code in (200, 201):
            return r.json().get("init_point", "")
        print(f"[pagos] Mercado Pago respondió {r.status_code}: {r.text[:200]}")
        return ""
    except Exception as e:
        print(f"[pagos] No pude crear el link de pago: {e}")
        return ""
