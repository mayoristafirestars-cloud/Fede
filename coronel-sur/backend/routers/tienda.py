"""
Tienda online pública — catálogo web para clientes (sin login).
Muestra SOLO datos públicos: descripción, precio de venta (Lista 1),
foto y si hay stock. El carrito termina en un mensaje a WhatsApp de Eva.
"""
import os
import sys

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar

router = APIRouter(tags=["tienda"])

# Número de WhatsApp de Eva (donde caen los pedidos de la tienda)
WA_TIENDA = os.getenv("WA_TIENDA", "").replace("+", "").replace(" ", "")
NEGOCIO_NOMBRE = os.getenv("NEGOCIO_NOMBRE", "Dist Coronel Sur")


@router.get("/api/tienda/productos")
def productos_publicos(buscar: str = "", rubro: str = "", limit: int = 60, offset: int = 0):
    conn = conectar()
    try:
        query = "SELECT codigo, descripcion, rubro, precio_venta, stock FROM productos WHERE activo = 1 AND precio_venta > 0"
        params = []
        if buscar:
            query += " AND (descripcion LIKE ? OR codigo LIKE ?)"
            params += [f"%{buscar}%", f"%{buscar}%"]
        if rubro:
            query += " AND rubro = ?"
            params.append(rubro)
        total = conn.execute(
            query.replace(
                "SELECT codigo, descripcion, rubro, precio_venta, stock", "SELECT COUNT(*)"
            ),
            params,
        ).fetchone()[0]
        query += " ORDER BY (stock > 0) DESC, descripcion COLLATE NOCASE LIMIT ? OFFSET ?"
        params += [limit, offset]
        prods = [
            {
                "codigo": r["codigo"],
                "descripcion": r["descripcion"],
                "rubro": r["rubro"],
                "precio": r["precio_venta"],
                "hay_stock": r["stock"] > 0,
            }
            for r in conn.execute(query, params)
        ]
        return {"productos": prods, "total": total}
    finally:
        conn.close()


@router.get("/api/tienda/rubros")
def rubros_publicos():
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
    return html.replace("{{WA_TIENDA}}", WA_TIENDA).replace("{{NEGOCIO}}", NEGOCIO_NOMBRE)
