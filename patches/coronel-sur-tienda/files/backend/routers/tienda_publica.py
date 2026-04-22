"""
Tienda publica online — API y template HTML.
"""
from __future__ import annotations

import os, sys, re
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar


router = APIRouter(tags=["tienda-publica"])

FRONTEND = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "..", "frontend"
)
TEMPLATE = os.path.abspath(os.path.join(FRONTEND, "templates", "tienda_publica.html"))

ICONOS_RUBRO = {
    "LIBRERIA":"📚","BAZAR":"🍽️","HOGAR/JARDIN":"🏠","TEXTIL":"🧶",
    "LIBROS":"📖","REGALERIA":"🎁","JUGUETERIA":"🧸","ELECTRO":"🔌",
    "ELECTRONICA":"🔌","DEPORTES":"⚽","HIGIENE":"🧴","ALIMENTOS":"🥫",
    "ACCESORIOS":"💍","COSMETICA":"💄","LIMPIEZA":"🧹",
}
def _icono(rubro):
    return ICONOS_RUBRO.get((rubro or "").upper().strip(), "📦")


@router.get("/shop", response_class=HTMLResponse)
@router.get("/tienda-online", response_class=HTMLResponse)
def servir_tienda():
    try:
        with open(TEMPLATE, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse("<h1>Tienda aun no desplegada</h1>", status_code=500)


@router.get("/api/shop/categorias")
def listar_categorias():
    conn = conectar()
    try:
        filas = conn.execute(
            """SELECT rubro, COUNT(*) as cantidad
               FROM productos
               WHERE activo = 1 AND stock > 0 AND COALESCE(rubro, '') != ''
               GROUP BY rubro HAVING COUNT(*) >= 1
               ORDER BY cantidad DESC"""
        ).fetchall()
        return [{"rubro": dict(f)["rubro"], "cantidad": dict(f)["cantidad"], "icono": _icono(dict(f)["rubro"])} for f in filas]
    finally:
        conn.close()


@router.get("/api/shop/productos")
def listar_productos(
    q: Optional[str] = None, rubro: Optional[str] = None,
    limit: int = Query(40, ge=1, le=100), offset: int = Query(0, ge=0),
    tipo_cliente: str = "minorista",
):
    conn = conectar()
    try:
        sql = "SELECT * FROM productos WHERE activo = 1 AND stock > 0"
        params: list = []
        if q:
            qlike = f"%{q.strip()}%"
            sql += " AND (descripcion LIKE ? OR codigo LIKE ? OR COALESCE(ean,'') LIKE ?)"
            params += [qlike, qlike, qlike]
        if rubro:
            sql += " AND rubro = ?"
            params.append(rubro.strip())
        sql += " ORDER BY (foto_url != '' AND foto_url NOT LIKE '%product.png%') DESC, descripcion ASC"
        sql += f" LIMIT {int(limit)} OFFSET {int(offset)}"
        filas = conn.execute(sql, params).fetchall()
        productos = []
        for f in filas:
            d = dict(f)
            precio = d.get("precio_mayorista", 0) if tipo_cliente == "mayorista" and d.get("precio_mayorista", 0) > 0 else d.get("precio_venta", 0)
            productos.append({"id":d.get("id"),"codigo":d.get("codigo"),"descripcion":d.get("descripcion"),"rubro":d.get("rubro"),"precio":float(precio or 0),"foto_url":d.get("foto_url") or "","ean":d.get("ean") or ""})
        return {"productos": productos, "tipo_cliente": tipo_cliente}
    finally:
        conn.close()


@router.get("/api/shop/destacados")
def productos_destacados(limit: int = 12):
    conn = conectar()
    try:
        try:
            filas = conn.execute(
                """SELECT p.*, COALESCE(SUM(v.cantidad), 0) as total_vendido
                   FROM productos p
                   LEFT JOIN ventas_historicas v ON v.codigo = p.codigo
                   WHERE p.activo = 1 AND p.stock > 0
                   GROUP BY p.id
                   HAVING COALESCE(SUM(v.cantidad), 0) > 0
                   ORDER BY total_vendido DESC
                   LIMIT ?""",
                (int(limit),),
            ).fetchall()
        except Exception:
            filas = conn.execute(
                "SELECT * FROM productos WHERE activo = 1 AND stock > 0 ORDER BY precio_venta DESC LIMIT ?",
                (int(limit),),
            ).fetchall()
        return [{"id":dict(f).get("id"),"codigo":dict(f).get("codigo"),"descripcion":dict(f).get("descripcion"),"rubro":dict(f).get("rubro"),"precio":float(dict(f).get("precio_venta",0) or 0),"foto_url":dict(f).get("foto_url") or ""} for f in filas]
    finally:
        conn.close()


@router.get("/api/shop/ofertas")
def productos_oferta(limit: int = 16):
    """Productos outlet: con stock pero sin ventas historicas (o muy pocas). 25% OFF."""
    conn = conectar()
    try:
        try:
            filas = conn.execute(
                """SELECT p.*, COALESCE(SUM(v.cantidad), 0) as total_vendido
                   FROM productos p
                   LEFT JOIN ventas_historicas v ON v.codigo = p.codigo
                   WHERE p.activo = 1 AND p.stock > 0 AND p.precio_venta > 0
                   GROUP BY p.id
                   HAVING COALESCE(SUM(v.cantidad), 0) = 0
                   ORDER BY p.stock DESC, p.precio_venta DESC
                   LIMIT ?""",
                (int(limit),),
            ).fetchall()
        except Exception:
            filas = conn.execute(
                "SELECT * FROM productos WHERE activo = 1 AND stock > 0 AND precio_venta > 0 ORDER BY stock DESC LIMIT ?",
                (int(limit),),
            ).fetchall()
        productos = []
        for f in filas:
            d = dict(f)
            precio_original = float(d.get("precio_venta", 0) or 0)
            precio_costo = float(d.get("precio_costo", 0) or 0)
            precio_oferta = round(precio_original * 0.75)
            if precio_costo > 0 and precio_oferta < precio_costo:
                precio_oferta = round(precio_costo)
            descuento = round((1 - precio_oferta / precio_original) * 100) if precio_original > 0 else 0
            productos.append({
                "id": d.get("id"), "codigo": d.get("codigo"),
                "descripcion": d.get("descripcion"), "rubro": d.get("rubro"),
                "precio_original": precio_original, "precio_oferta": precio_oferta,
                "descuento": descuento, "foto_url": d.get("foto_url") or "",
            })
        return productos
    finally:
        conn.close()


@router.get("/api/shop/productos/{producto_id}")
def detalle_producto(producto_id: int, tipo_cliente: str = "minorista"):
    conn = conectar()
    try:
        fila = conn.execute("SELECT * FROM productos WHERE activo = 1 AND id = ? LIMIT 1", (int(producto_id),)).fetchone()
        if not fila:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        d = dict(fila)
        precio = d.get("precio_mayorista", 0) if tipo_cliente == "mayorista" and d.get("precio_mayorista", 0) > 0 else d.get("precio_venta", 0)
        return {"id":d.get("id"),"codigo":d.get("codigo"),"descripcion":d.get("descripcion"),"rubro":d.get("rubro"),"precio":float(precio or 0),"foto_url":d.get("foto_url") or "","ean":d.get("ean") or "","disponible":(d.get("stock",0) or 0) > 0}
    finally:
        conn.close()


class ItemPedido(BaseModel):
    producto_id: int
    cantidad: int

class PedidoReq(BaseModel):
    nombre: str
    telefono: str
    tipo_entrega: str = "retiro"
    direccion: str = ""
    notas: str = ""
    tipo_cliente: str = "minorista"
    items: list[ItemPedido]

@router.post("/api/shop/pedido")
def crear_pedido(data: PedidoReq):
    if not data.nombre.strip():
        raise HTTPException(status_code=400, detail="Pone tu nombre")
    tel = re.sub(r"\D", "", data.telefono)
    if len(tel) < 8:
        raise HTTPException(status_code=400, detail="Pone un telefono valido")
    if not data.items:
        raise HTTPException(status_code=400, detail="Tu carrito esta vacio")
    if data.tipo_entrega == "envio" and not data.direccion.strip():
        raise HTTPException(status_code=400, detail="Pone la direccion de envio")
    conn = conectar()
    try:
        subtotal = 0.0
        items_db = []
        for it in data.items:
            fila = conn.execute("SELECT id, descripcion, precio_venta, precio_mayorista, stock FROM productos WHERE activo = 1 AND id = ?", (int(it.producto_id),)).fetchone()
            if not fila:
                raise HTTPException(status_code=400, detail=f"Producto {it.producto_id} no disponible")
            p = dict(fila)
            precio = p.get("precio_mayorista", 0) if data.tipo_cliente == "mayorista" and p.get("precio_mayorista", 0) > 0 else p.get("precio_venta", 0)
            precio = float(precio or 0)
            cant = max(1, int(it.cantidad))
            item_subtotal = precio * cant
            subtotal += item_subtotal
            items_db.append({"producto_id":p["id"],"descripcion":p["descripcion"],"cantidad":cant,"precio":precio,"subtotal":item_subtotal})
        cur = conn.execute("INSERT INTO pedidos_tienda (nombre_cliente, telefono, tipo_entrega, direccion, notas, subtotal, estado) VALUES (?,?,?,?,?,?,'pendiente')", (data.nombre.strip(), tel, data.tipo_entrega, data.direccion.strip(), data.notas.strip(), subtotal))
        pedido_id = cur.lastrowid
        if not pedido_id:
            f = conn.execute("SELECT id FROM pedidos_tienda WHERE nombre_cliente = ? AND telefono = ? ORDER BY id DESC LIMIT 1", (data.nombre.strip(), tel)).fetchone()
            if f: pedido_id = dict(f)["id"]
        for it in items_db:
            conn.execute("INSERT INTO pedidos_tienda_items (pedido_id, descripcion, cantidad, precio, subtotal) VALUES (?,?,?,?,?)", (pedido_id, it["descripcion"], it["cantidad"], it["precio"], it["subtotal"]))
        conn.commit()
        return {"ok": True, "pedido_id": pedido_id, "total": subtotal}
    except HTTPException:
        raise
    except Exception as e:
        try: conn.rollback()
        except: pass
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@router.get("/api/shop/info")
def info_tienda():
    return {
        "nombre": "Coronel Sur",
        "telefono_wa": "5492954821628",
        "horario": "Lun a Sáb 8:30 a 12:30 y 16:30 a 20:30",
        "direccion": "Roque Sáenz Peña 1297, Santa Rosa (6300), La Pampa",
    }
