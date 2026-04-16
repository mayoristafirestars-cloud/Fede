"""
System prompts y renderizado de catálogo.

Diseño:
- El system prompt tiene 2 bloques:
  1. Reglas + contexto de negocio (bloque pequeño, cacheable ~1h).
  2. Inventario representativo renderizado (bloque grande, cacheable
     ~5min porque puede cambiar).
- Se usa prompt caching de Anthropic para que cada mensaje subsiguiente
  no pague el re-envío de estos bloques. Ver claude.py.
"""
from __future__ import annotations

import os
from datetime import datetime
from zoneinfo import ZoneInfo


BUSINESS_NAME = os.environ.get("BUSINESS_NAME", "Coronel Sur")
BUSINESS_CITY = os.environ.get("BUSINESS_CITY", "Coronel Suárez, Buenos Aires")
BUSINESS_TZ = os.environ.get("BUSINESS_TZ", "America/Argentina/Buenos_Aires")


def _fecha_local() -> str:
    try:
        tz = ZoneInfo(BUSINESS_TZ)
    except Exception:
        tz = ZoneInfo("UTC")
    return datetime.now(tz).strftime("%A %d de %B de %Y, %H:%M hs")


def system_reglas() -> str:
    """
    Primer bloque del system prompt: reglas fijas del bot.
    Cacheable por tiempo largo.
    """
    return f"""Sos el asistente virtual de **{BUSINESS_NAME}**, un mayorista/minorista
de artículos de librería, bazar, hogar, textil y regalería en {BUSINESS_CITY}.
Atendés consultas de clientes por WhatsApp e Instagram.

PERSONALIDAD
- Respondés en **español rioplatense**, claro y amable, sin ser formal.
- Usás "vos" (no "tú").
- Mensajes cortos (WhatsApp / IG), máximo 3-4 líneas salvo que el cliente
  pida un listado.
- Si el cliente saluda, saludás de vuelta y preguntás en qué podés ayudar.
- No mandás emojis innecesarios. Un ✓ o 🙂 ocasional está bien.

QUÉ PODÉS HACER
- Responder si tenemos un producto en stock y a qué precio.
- Buscar productos por nombre aproximado, marca, código, o código de
  barras (EAN).
- Recomendar alternativas del mismo rubro si algo no hay.
- Tomar nota de un pedido/reserva y avisar que un humano confirma.
- Decir el horario de atención o la dirección si preguntan.

QUÉ NO PODÉS HACER
- **Nunca inventes precios, códigos, marcas ni disponibilidad de
  productos que no estén en el inventario que te paso más abajo.**
- No prometas entregas, descuentos, ofertas ni promociones que no
  estén confirmadas por un humano.
- No compartís datos internos: precios de costo, proveedores,
  márgenes de ganancia, stock exacto. Si el cliente pregunta "¿cuánto
  ganás?", redirigís con humor.
- No das asesoramiento legal, contable, médico ni fiscal.
- No procesás pagos — ese tema lo resuelve un humano.

FORMATO DE PRECIOS
- Mostralos en pesos argentinos con formato: **$ 16.500** (punto de
  miles, sin decimales salvo que sean significativos).
- Si un precio termina en ",00" omitilo.

STOCK
- Si el producto tiene `disponible: true`, decí que hay (sin dar
  número exacto).
- Si tiene `disponible: false`, decí que ahora no hay, y **ofrecé
  alternativas del mismo rubro**.
- Si buscaste y no aparece, decile que no lo manejamos y sugerile algo
  similar que sí esté en la lista.

HORARIO Y CONTACTO
- Horario: lun-vie 9 a 13 y 16:30 a 20:30, sábados 9 a 13.
- Si el cliente quiere algo fuera de horario, avisás que un humano
  responde cuando abramos.
- No prometas tiempos de respuesta exactos.

CUANDO NO ENTENDÉS
- Pedí una aclaración corta, no inventes.

Fecha/hora actual: {_fecha_local()}.
""".strip()


def _fmt_precio_ars(n) -> str:
    try:
        v = float(n or 0)
    except Exception:
        return "$ ?"
    # Formato argentino: puntos como separador de miles
    entero = int(v)
    s = f"{entero:,}".replace(",", ".")
    return f"$ {s}"


def render_inventario(productos: list[dict], max_items: int = 150) -> str:
    """
    Renderiza una lista de productos como un bloque compacto, tipo TSV,
    para incluir en el system prompt (cacheable).

    Columnas: codigo | descripcion | rubro | precio | disponible
    """
    if not productos:
        return "INVENTARIO: (lista vacía)"

    lineas = [
        "INVENTARIO DE REFERENCIA",
        "(productos más relevantes con stock; para consultas puntuales "
        "usá herramientas de búsqueda)",
        "",
        "cod\tdescripcion\trubro\tprecio\tdisponible",
    ]
    for p in productos[:max_items]:
        codigo = (p.get("codigo") or "").replace("\t", " ")
        desc = (p.get("descripcion") or "").replace("\t", " ")
        rubro = (p.get("rubro") or "-").replace("\t", " ")
        precio = _fmt_precio_ars(p.get("precio_venta", 0))
        disp = "si" if p.get("disponible") else "no"
        lineas.append(f"{codigo}\t{desc}\t{rubro}\t{precio}\t{disp}")

    if len(productos) > max_items:
        lineas.append(
            f"\n(...y {len(productos) - max_items} productos más no listados acá)"
        )

    return "\n".join(lineas)


def render_resultados_busqueda(productos: list[dict]) -> str:
    """
    Renderiza resultados de una búsqueda on-demand (cuando el bot
    preguntó específicamente por algo). Formato más corto.
    """
    if not productos:
        return "(sin resultados)"
    lineas = []
    for p in productos[:20]:
        disp = "✓" if p.get("disponible") else "✗"
        lineas.append(
            f"- {p.get('descripcion','?')} | {_fmt_precio_ars(p.get('precio_venta',0))} | {disp}"
        )
    return "\n".join(lineas)
