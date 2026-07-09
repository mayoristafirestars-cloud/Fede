"""
Agente — puente con Eva (la vendedora virtual de WhatsApp).

Eva manda los pedidos confirmados acá (POST /api/agente/pedido con el
header X-Token) y se crean como PRESUPUESTOS con origen 'eva'.
Después Malcom los ve en la pestaña Agente y los factura.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar

router = APIRouter(prefix="/api/agente", tags=["agente"])


class ItemPedido(BaseModel):
    codigo: Optional[str] = None
    descripcion: str
    cantidad: float
    precio_unitario: float


class PedidoEva(BaseModel):
    telefono: str
    tipo_cliente: str = ""          # mayorista | consumidor final
    items: list[ItemPedido]
    total: float
    texto_original: Optional[str] = None


@router.post("/pedido")
def recibir_pedido(data: PedidoEva):
    """Recibe un pedido confirmado desde Eva y lo guarda como presupuesto."""
    if not data.items:
        raise HTTPException(status_code=400, detail="Pedido sin ítems")

    conn = conectar()
    try:
        # Cliente: buscar/crear por teléfono (nombre provisorio con el número)
        tel = data.telefono.strip()
        row = conn.execute(
            "SELECT id, nombre FROM clientes WHERE telefono = ?", (tel,)
        ).fetchone()
        if row:
            cliente_id, cliente_nombre = row[0], row[1]
        else:
            tipo = "mayorista" if "mayor" in data.tipo_cliente.lower() else "minorista"
            cliente_nombre = f"WhatsApp {tel}"
            cur = conn.execute(
                "INSERT INTO clientes (nombre, telefono, tipo, notas) VALUES (?, ?, ?, ?)",
                (cliente_nombre, tel, tipo, "Creado automáticamente por Eva"),
            )
            cliente_id = cur.lastrowid

        # Número de presupuesto
        ultimo = conn.execute(
            "SELECT COUNT(*) FROM comprobantes WHERE origen = 'eva'"
        ).fetchone()[0]
        numero = f"EVA-{str(ultimo + 1).zfill(5)}"
        fecha = datetime.now().strftime("%d-%m-%Y")

        subtotal = sum(i.cantidad * i.precio_unitario for i in data.items)
        cur = conn.execute("""
            INSERT INTO comprobantes
                (tipo, numero, cliente_id, cliente_nombre, fecha,
                 subtotal, descuento, total, estado, origen)
            VALUES ('presupuesto', ?, ?, ?, ?, ?, 0, ?, 'activo', 'eva')""",
            (numero, cliente_id, cliente_nombre, fecha, subtotal, data.total or subtotal))
        comp_id = cur.lastrowid

        for item in data.items:
            prod = None
            if item.codigo:
                prod = conn.execute(
                    "SELECT id, precio_costo FROM productos WHERE codigo = ?",
                    (item.codigo.strip(),),
                ).fetchone()
            conn.execute("""
                INSERT INTO comprobante_items
                    (comprobante_id, producto_id, producto_desc, cantidad,
                     precio_unitario, precio_costo, subtotal)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (comp_id, prod[0] if prod else None, item.descripcion,
                 item.cantidad, item.precio_unitario,
                 prod[1] if prod else 0,
                 item.cantidad * item.precio_unitario))

        conn.commit()
        return {"ok": True, "numero": numero, "comprobante_id": comp_id}
    finally:
        conn.close()


class ConversacionIn(BaseModel):
    session: str
    telefono: str = ""
    mensaje: str
    respuesta: str
    es_audio: int = 0


@router.post("/conversacion")
def guardar_conversacion(data: ConversacionIn):
    """Eva registra acá cada intercambio con un cliente."""
    conn = conectar()
    try:
        conn.execute("""
            INSERT INTO conversaciones_eva (session, telefono, mensaje, respuesta, es_audio)
            VALUES (?, ?, ?, ?, ?)""",
            (data.session, data.telefono, data.mensaje[:2000],
             data.respuesta[:4000], data.es_audio))
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()


@router.get("/conversaciones")
def listar_conversaciones(telefono: str = "", limit: int = 80):
    conn = conectar()
    try:
        query = "SELECT * FROM conversaciones_eva"
        params = []
        if telefono:
            query += " WHERE telefono LIKE ? OR session LIKE ?"
            params = [f"%{telefono}%"] * 2
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        filas = [dict(f) for f in conn.execute(query, params).fetchall()]
        hoy = conn.execute("""
            SELECT COUNT(*), COUNT(DISTINCT session) FROM conversaciones_eva
             WHERE date(creado_en) = date('now', 'localtime')""").fetchone()
        return {"conversaciones": filas, "hoy_mensajes": hoy[0], "hoy_clientes": hoy[1]}
    finally:
        conn.close()


class EstadoIn(BaseModel):
    estado: str


ESTADOS_VALIDOS = {"activo", "facturado", "entregado", "cancelado"}


@router.post("/pedido/{comprobante_id}/estado")
def cambiar_estado(comprobante_id: int, data: EstadoIn):
    """Cambia el estado de un pedido de Eva (pendiente/facturado/entregado/cancelado)."""
    if data.estado not in ESTADOS_VALIDOS:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Válidos: {ESTADOS_VALIDOS}")
    conn = conectar()
    try:
        row = conn.execute(
            "SELECT id FROM comprobantes WHERE id = ? AND origen = 'eva'",
            (comprobante_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        conn.execute("UPDATE comprobantes SET estado = ? WHERE id = ?",
                     (data.estado, comprobante_id))
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()


@router.get("/resumen-diario")
def resumen_diario():
    """Resumen del día para el reporte automático por WhatsApp."""
    conn = conectar()
    try:
        conv = conn.execute("""
            SELECT COUNT(*), COUNT(DISTINCT session) FROM conversaciones_eva
             WHERE date(creado_en) = date('now', 'localtime')""").fetchone()
        ped = conn.execute("""
            SELECT COUNT(*), COALESCE(SUM(total),0) FROM comprobantes
             WHERE origen = 'eva' AND estado != 'cancelado'
               AND date(creado_en) = date('now', 'localtime')""").fetchone()
        top = conn.execute("""
            SELECT mensaje FROM conversaciones_eva
             WHERE date(creado_en) = date('now', 'localtime')
             ORDER BY id DESC LIMIT 5""").fetchall()
        return {
            "mensajes": conv[0], "clientes": conv[1],
            "pedidos": ped[0], "total_pedidos": round(ped[1], 2),
            "ultimas_consultas": [t[0][:80] for t in top],
        }
    finally:
        conn.close()


@router.get("/pedidos")
def listar_pedidos(limit: int = 50):
    """Pedidos que entraron por Eva, más recientes primero."""
    conn = conectar()
    try:
        pedidos = [dict(f) for f in conn.execute("""
            SELECT id, numero, cliente_nombre, fecha, total, estado, creado_en
              FROM comprobantes WHERE origen = 'eva'
             ORDER BY id DESC LIMIT ?""", (limit,)).fetchall()]
        for p in pedidos:
            p["items"] = [dict(i) for i in conn.execute("""
                SELECT producto_desc, cantidad, precio_unitario, subtotal
                  FROM comprobante_items WHERE comprobante_id = ?""",
                (p["id"],)).fetchall()]
        kpi = conn.execute("""
            SELECT COUNT(*), COALESCE(SUM(total),0) FROM comprobantes
             WHERE origen = 'eva' AND estado NOT IN ('anulado', 'cancelado')""").fetchone()
        return {"pedidos": pedidos, "cantidad": kpi[0], "total": round(kpi[1], 2)}
    finally:
        conn.close()
