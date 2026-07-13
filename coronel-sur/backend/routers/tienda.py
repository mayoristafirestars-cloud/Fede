"""
Tienda online pública — catálogo web para clientes (sin login).
Muestra SOLO datos públicos: descripción, precio de venta (Lista 1),
foto y si hay stock. El carrito termina en un mensaje a WhatsApp de Eva.
"""
import os
import sys
import json

from fastapi import APIRouter, Response
from fastapi.responses import HTMLResponse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar
from sincronizador import sincronizar_si_cambio

router = APIRouter(tags=["tienda"])

# Número de WhatsApp de Eva (donde caen los pedidos de la tienda)
WA_TIENDA = os.getenv("WA_TIENDA", "").replace("+", "").replace(" ", "")
NEGOCIO_NOMBRE = os.getenv("NEGOCIO_NOMBRE", "Dist Coronel Sur")
# URL pública donde se sirve ESTA tienda (para Open Graph / canonical al
# compartir el link). Debe ser el dominio real: si la tienda se sirve en
# sistema.coronelsur.com.ar, poné eso. Configurable por env PUBLIC_URL.
BASE_URL = os.getenv("PUBLIC_URL", "https://sistema.coronelsur.com.ar").rstrip("/")
PAGINA = 30  # productos por página (server-side y scroll)


def _esc(s) -> str:
    """Escapa para insertar texto de la DB en HTML de forma segura (anti-XSS)."""
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;"))


def _precio_ar(valor) -> str:
    """Formato $16.999 (igual que el JS con es-AR)."""
    try:
        return "$" + f"{int(round(float(valor))):,}".replace(",", ".")
    except (TypeError, ValueError):
        return "$0"


def _consultar_productos(buscar: str, rubro: str, limit: int, offset: int):
    """Devuelve (lista_de_productos, total). Fuente única para la API y el
    render server-side de /tienda."""
    conn = conectar()
    try:
        base = ("FROM productos WHERE activo = 1 AND precio_venta > 0")
        params = []
        if buscar:
            base += " AND (descripcion LIKE ? OR codigo LIKE ?)"
            params += [f"%{buscar}%", f"%{buscar}%"]
        if rubro:
            base += " AND rubro = ?"
            params.append(rubro)
        total = conn.execute("SELECT COUNT(*) " + base, params).fetchone()[0]
        q = ("SELECT codigo, descripcion, rubro, precio_venta, stock, "
             "COALESCE(foto,'') AS foto " + base +
             " ORDER BY (stock > 0) DESC, descripcion COLLATE NOCASE LIMIT ? OFFSET ?")
        prods = [
            {
                "codigo": r["codigo"],
                "descripcion": r["descripcion"],
                "rubro": r["rubro"],
                "precio": r["precio_venta"],
                "hay_stock": r["stock"] > 0,
                "foto": r["foto"] if str(r["foto"]).startswith("http") else "",
            }
            for r in conn.execute(q, params + [limit, offset])
        ]
        return prods, total
    finally:
        conn.close()


def _card_html(p: dict) -> str:
    """Una tarjeta de producto renderizada en el servidor (misma estructura
    que la que arma el JS), con todo escapado."""
    nom = _esc(p["descripcion"])
    foto = str(p.get("foto") or "")
    img = (f'<img class="pfoto" src="{_esc(foto)}" alt="{nom}" loading="lazy" '
           f'onerror="this.style.display=&#39;none&#39;">' if foto.startswith("http")
           else '<div class="pfoto sinfoto" aria-hidden="true"></div>')
    if p["hay_stock"]:
        sin = ""
        boton = (f'<button class="add" data-codigo="{_esc(p["codigo"])}" data-nom="{nom}" '
                 f'data-precio="{float(p["precio"]):.2f}" aria-label="Agregar {nom}">Agregar</button>')
    else:
        # Sin stock: se muestra pero NO se puede agregar (evita pedidos incumplibles).
        sin = '<div class="sinstock">Sin stock — consultá</div>'
        boton = '<button disabled aria-label="Sin stock, consultá por WhatsApp">Sin stock</button>'
    return (f'<li class="prod">{img}<div class="nom">{nom}</div>'
            f'<div class="precio">{_precio_ar(p["precio"])}</div>{sin}{boton}</li>')


@router.get("/api/tienda/productos")
def productos_publicos(response: Response, buscar: str = "", rubro: str = "",
                       limit: int = 60, offset: int = 0):
    sincronizar_si_cambio()  # mantiene el catálogo en lockstep con lo que lee Eva
    limit = max(1, min(int(limit), 100))  # tope: nadie vuelca el catálogo entero
    prods, total = _consultar_productos(buscar, rubro, limit, max(0, int(offset)))
    # El catálogo es igual para todos y se actualiza por sync: cachear unos
    # segundos alivia la base cuando muchos clientes navegan a la vez.
    response.headers["Cache-Control"] = "public, max-age=60"
    return {"productos": prods, "total": total}


@router.get("/api/tienda/rubros")
def rubros_publicos(response: Response):
    response.headers["Cache-Control"] = "public, max-age=300"
    conn = conectar()
    try:
        return [
            r["rubro"]
            for r in conn.execute(
                "SELECT DISTINCT rubro FROM productos WHERE activo=1 AND rubro!='' AND precio_venta>0 ORDER BY rubro"
            )
        ]
    finally:
        conn.close()


@router.get("/tienda", response_class=HTMLResponse)
def tienda_home():
    ruta = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "frontend", "templates", "tienda.html",
    )
    with open(ruta, encoding="utf-8") as f:
        html = f.read()

    if not WA_TIENDA:
        print("[tienda] ⚠️ WA_TIENDA vacío: los pedidos de la tienda NO tienen a "
              "dónde ir. Configurá WA_TIENDA en el .env para no perder ventas.")

    # Render server-side de la primera página + rubros, para que Google y los
    # bots de WhatsApp/redes vean productos reales (no una página vacía) y para
    # que el primer pintado sea instantáneo aunque la API tarde.
    ssr_ok = True
    productos_html = ""
    rubros_html = ""
    total = 0
    try:
        sincronizar_si_cambio()
        prods, total = _consultar_productos("", "", PAGINA, 0)
        productos_html = "".join(_card_html(p) for p in prods)
        rubros = [
            r["rubro"] for r in conectar().execute(
                "SELECT DISTINCT rubro FROM productos "
                "WHERE activo=1 AND rubro!='' AND precio_venta>0 ORDER BY rubro")
        ]
        rubros_html = "".join(f'<option value="{_esc(r)}">{_esc(r)}</option>' for r in rubros)
        offset_inicial = len(prods)
    except Exception as e:  # si la DB falla, el JS hace el fallback (fetch en el cliente)
        print(f"[tienda] SSR falló, el cliente cargará por API: {e}")
        ssr_ok = False
        offset_inicial = 0

    descripcion = (f"Comprá en {NEGOCIO_NOMBRE}: catálogo con precios, envíos a "
                   "todo el país y tu pedido por WhatsApp. Bazar, regalería, "
                   "electrónica y mucho más — Santa Rosa, La Pampa.")
    hay_mas = offset_inicial < total

    # Datos estructurados (schema.org): Google entiende que sos un comercio y
    # puede mostrar tu ficha + productos con precio en los resultados.
    tienda_schema = {
        "@context": "https://schema.org", "@type": "Store",
        "name": NEGOCIO_NOMBRE, "url": f"{BASE_URL}/tienda",
        "image": f"{BASE_URL}/static/og-tienda.png", "description": descripcion,
        "address": {"@type": "PostalAddress", "addressLocality": "Santa Rosa",
                    "addressRegion": "La Pampa", "addressCountry": "AR"},
        "areaServed": "AR",
    }
    if WA_TIENDA:
        tienda_schema["telephone"] = "+" + WA_TIENDA
    bloques = [tienda_schema]
    if ssr_ok and prods:
        bloques.append({
            "@context": "https://schema.org", "@type": "ItemList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "item": {
                    "@type": "Product", "name": p["descripcion"],
                    "image": p.get("foto") or f"{BASE_URL}/static/og-tienda.png",
                    "offers": {"@type": "Offer", "priceCurrency": "ARS",
                               "price": round(float(p["precio"])),
                               "availability": "https://schema.org/InStock" if p["hay_stock"]
                               else "https://schema.org/OutOfStock"}}}
                for i, p in enumerate(prods[:20])
            ],
        })
    jsonld = "".join(
        '<script type="application/ld+json">'
        + json.dumps(b, ensure_ascii=False).replace("<", "\\u003c")
        + "</script>" for b in bloques)

    reemplazos = {
        "{{WA_TIENDA}}": WA_TIENDA,
        "{{NEGOCIO}}": _esc(NEGOCIO_NOMBRE),
        "{{DESCRIPCION}}": _esc(descripcion),
        "{{BASE_URL}}": BASE_URL,
        "{{PRODUCTOS_HTML}}": productos_html,
        "{{RUBROS_HTML}}": rubros_html,
        "{{OFFSET_INICIAL}}": str(offset_inicial),
        "{{TOTAL}}": str(total),
        "{{SSR_OK}}": "true" if ssr_ok else "false",
        "{{EMPTY_STYLE}}": "block" if (ssr_ok and total == 0) else "none",
        "{{MAS_STYLE}}": "block" if hay_mas else "none",
        "{{JSONLD}}": jsonld,
    }
    for k, v in reemplazos.items():
        html = html.replace(k, v)
    return html
