"""
Módulo de Facturación — Rutas API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal
from decimal import Decimal
import stock
from document_photos import safe_photo,effective_photo
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar

router = APIRouter(prefix="/api/facturacion", tags=["facturacion"])


# ─── Modelos ───────────────────────────────────────────────

class ItemComprobante(BaseModel):
    producto_id:    Optional[int] = None
    producto_desc:  str
    cantidad:       float = Field(gt=0,le=99999999999,allow_inf_nan=False)
    precio_unitario: float = Field(ge=0,allow_inf_nan=False)
    precio_costo:   float = Field(default=0,ge=0,allow_inf_nan=False)

class NuevoComprobante(BaseModel):
    tipo:           Literal['factura','presupuesto'] = "factura"
    cliente_nombre: Optional[str] = ""
    cliente_id:     Optional[int] = None
    items:          list[ItemComprobante]
    descuento:      float = Field(default=0,ge=0,le=100,allow_inf_nan=False)


# ─── Endpoints ─────────────────────────────────────────────

@router.get("/buscar-producto")
def buscar_producto(q: str = "", limit: int = 10):
    """Busca productos por código o descripción para el buscador de la factura."""
    conn = conectar()
    try:
        if not q:
            return []
        filas = conn.execute("""
            SELECT id, codigo, descripcion, rubro, precio_venta, precio_costo, stock, foto, unidad_venta
            FROM productos
            WHERE activo = 1
              AND stock > 0
              AND (descripcion LIKE ? OR codigo LIKE ?)
            ORDER BY descripcion
            LIMIT ?
        """, (f"%{q}%", f"%{q}%", limit)).fetchall()
        return [dict(f) for f in filas]
    finally:
        conn.close()


@router.post("/nuevo")
def crear_comprobante(data: NuevoComprobante):
    """Crea una nueva factura o presupuesto."""
    if not data.items:
        raise HTTPException(status_code=400, detail="El comprobante no tiene ítems")

    conn = conectar()
    try:
        conn.execute('BEGIN IMMEDIATE')
        # Calcular totales
        subtotal = sum(i.cantidad * i.precio_unitario for i in data.items)
        total    = subtotal * (1 - data.descuento / 100)

        # Generar número de comprobante
        prefijo  = "F" if data.tipo == "factura" else "P"
        ultimo   = conn.execute(
            "SELECT COUNT(*) FROM comprobantes WHERE tipo = ?", (data.tipo,)
        ).fetchone()[0]
        numero   = f"{prefijo}-{str(ultimo + 1).zfill(6)}"

        from datetime import datetime
        fecha = datetime.now().strftime("%d-%m-%Y")

        # Insertar cabecera
        cur = conn.execute("""
            INSERT INTO comprobantes
                (tipo, numero, cliente_id, cliente_nombre, fecha, subtotal, descuento, total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (data.tipo, numero, data.cliente_id, data.cliente_nombre,
              fecha, subtotal, data.descuento, total))
        comprobante_id = cur.lastrowid

        # Insertar ítems y actualizar stock
        for item in data.items:
            item_subtotal = item.cantidad * item.precio_unitario
            item_cursor = conn.execute("""
                INSERT INTO comprobante_items
                    (comprobante_id, producto_id, producto_desc, cantidad,
                     precio_unitario, precio_costo, subtotal)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (comprobante_id, item.producto_id, item.producto_desc,
                  item.cantidad, item.precio_unitario, item.precio_costo, item_subtotal))
            image=conn.execute('SELECT foto FROM productos WHERE id=?',(item.producto_id,)).fetchone() if item.producto_id else None
            conn.execute('UPDATE comprobante_items SET foto=? WHERE id=?',(safe_photo(image[0]) if image else '',item_cursor.lastrowid))

            # Descontar stock si es factura y tiene producto_id
            if data.tipo == "factura" and item.producto_id:
                stock.consume_sale(conn,item.producto_id,Decimal(str(item.cantidad)).normalize(),comprobante_id,item_cursor.lastrowid)

        conn.commit()
        return {
            "ok": True,
            "comprobante_id": comprobante_id,
            "numero": numero,
            "total": total
        }
    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@router.get("/historial")
def historial(tipo: str = None, limit: int = 50, offset: int = 0):
    """Lista los comprobantes con filtro opcional por tipo."""
    conn = conectar()
    try:
        query  = "SELECT * FROM comprobantes WHERE estado != 'anulado'"
        params = []
        if tipo:
            query += " AND tipo = ?"
            params.append(tipo)
        query += " ORDER BY id DESC LIMIT ? OFFSET ?"
        params += [limit, offset]
        filas = conn.execute(query, params).fetchall()
        return [dict(f) for f in filas]
    finally:
        conn.close()


@router.get("/{comprobante_id}")
def detalle_comprobante(comprobante_id: int):
    """Devuelve el detalle completo de un comprobante."""
    conn = conectar()
    try:
        cab = conn.execute(
            "SELECT * FROM comprobantes WHERE id = ?", (comprobante_id,)
        ).fetchone()
        if not cab:
            raise HTTPException(status_code=404, detail="Comprobante no encontrado")
        items = conn.execute(
            "SELECT * FROM comprobante_items WHERE comprobante_id = ?", (comprobante_id,)
        ).fetchall()
        result=[dict(i) for i in items]
        for line in result:line['foto']=effective_photo(conn,'legado',line['id'],line['foto'])
        return {**dict(cab), "items": result}
    finally:
        conn.close()


@router.post("/{comprobante_id}/anular")
def anular_comprobante(comprobante_id: int):
    """Anula un comprobante y revierte el stock si era factura."""
    conn = conectar()
    try:
        conn.execute('BEGIN IMMEDIATE')
        comp = conn.execute(
            "SELECT * FROM comprobantes WHERE id = ?", (comprobante_id,)
        ).fetchone()
        if not comp:
            raise HTTPException(status_code=404, detail="No encontrado")
        if comp["estado"] == "anulado":
            raise HTTPException(status_code=400, detail="Ya está anulado")

        # Revertir stock si era factura
        if comp["tipo"] == "factura":
            items = conn.execute(
                "SELECT * FROM comprobante_items WHERE comprobante_id = ?", (comprobante_id,)
            ).fetchall()
            stock.reverse_sale(conn,comprobante_id,items)

        conn.execute(
            "UPDATE comprobantes SET estado = 'anulado' WHERE id = ?", (comprobante_id,)
        )
        conn.commit()
        return {"ok": True, "mensaje": "Comprobante anulado"}
    finally:
        conn.close()
