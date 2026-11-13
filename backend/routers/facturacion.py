"""
Módulo de Facturación — Rutas API
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar
import seguridad
from db.auditoria import registrar
from dinero import a_centavos, a_decimal, a_pesos, redondear, sin_iva
import config
from db.secuencias import siguiente_numero

EMPRESA_ID = 1   # una sola empresa por ahora

router = APIRouter(prefix="/api/facturacion", tags=["facturacion"])


# ─── Modelos ───────────────────────────────────────────────

class ItemComprobante(BaseModel):
    producto_id:    Optional[int] = None
    producto_desc:  str
    cantidad:       float
    precio_unitario: float
    precio_costo:   float = 0.0

class NuevoComprobante(BaseModel):
    tipo:           str = "factura"   # factura | presupuesto
    cliente_nombre: Optional[str] = ""
    cliente_id:     Optional[int] = None
    items:          list[ItemComprobante]
    descuento:      float = 0.0


# ─── Endpoints ─────────────────────────────────────────────

@router.get("/buscar-producto")
def buscar_producto(q: str = "", limit: int = 10,
                    _u=Depends(seguridad.requiere("producto.ver"))):
    """Busca productos por código o descripción para el buscador de la factura."""
    conn = conectar()
    try:
        if not q:
            return []
        filas = conn.execute("""
            SELECT id, codigo, descripcion, rubro, precio_venta, precio_costo, stock
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
def crear_comprobante(data: NuevoComprobante, request: Request,
                      usuario=Depends(seguridad.requiere("comprobante.emitir"))):
    """Crea una nueva factura o presupuesto."""
    if not data.items:
        raise HTTPException(status_code=400, detail="El comprobante no tiene ítems")

    conn = conectar()
    try:
        # Calcular totales en Decimal: cada ítem se redondea al centavo y el total
        # se redondea después de aplicar el descuento (porcentaje).
        items_c = [a_centavos(a_decimal(i.cantidad) * a_decimal(i.precio_unitario)) for i in data.items]
        subtotal_c = sum(items_c)
        total_c = a_centavos(redondear(a_decimal(subtotal_c) / 100 * (1 - a_decimal(data.descuento) / 100)))

        # Generar número de comprobante
        prefijo  = "F" if data.tipo == "factura" else "P"
        numero   = f"{prefijo}-{str(siguiente_numero(conn, EMPRESA_ID, data.tipo)).zfill(6)}"

        from datetime import date
        fecha = date.today().isoformat()          # AAAA-MM-DD

        # Insertar cabecera (las columnas REAL se siguen escribiendo por compatibilidad)
        cur = conn.execute("""
            INSERT INTO comprobantes
                (tipo, numero, cliente_id, cliente_nombre, fecha, subtotal, descuento, total,
                 subtotal_centavos, total_centavos)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data.tipo, numero, data.cliente_id, data.cliente_nombre,
              fecha, a_pesos(subtotal_c), data.descuento, a_pesos(total_c), subtotal_c, total_c))
        comprobante_id = cur.lastrowid

        # Insertar ítems y actualizar stock
        for item, item_c in zip(data.items, items_c):
            precio_c = a_centavos(item.precio_unitario)
            costo_c  = a_centavos(item.precio_costo)
            conn.execute("""
                INSERT INTO comprobante_items
                    (comprobante_id, producto_id, producto_desc, cantidad,
                     precio_unitario, precio_costo, subtotal,
                     precio_unitario_centavos, precio_costo_centavos, subtotal_centavos)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (comprobante_id, item.producto_id, item.producto_desc, item.cantidad,
                  a_pesos(precio_c), a_pesos(costo_c), a_pesos(item_c), precio_c, costo_c, item_c))

            # Descontar stock si es factura y tiene producto_id
            if data.tipo == "factura" and item.producto_id:
                conn.execute("""
                    UPDATE productos SET
                        stock = stock - ?,
                        actualizado_en = datetime('now', 'localtime')
                    WHERE id = ?
                """, (item.cantidad, item.producto_id))

        registrar(conn, "comprobante.emitir", entidad="comprobante", entidad_id=comprobante_id,
                  despues={"numero": numero, "tipo": data.tipo, "total_centavos": total_c,
                           "cliente_nombre": data.cliente_nombre, "items": len(data.items)},
                  usuario=usuario, ip=seguridad.ip_de(request))
        conn.commit()
        return {
            "ok": True,
            "comprobante_id": comprobante_id,
            "numero": numero,
            "total": a_pesos(total_c)
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


def _en_pesos(fila, campos: tuple) -> dict:
    """Devuelve la fila con los importes en pesos calculados desde los centavos."""
    d = dict(fila)
    for campo in campos:
        centavos = d.get(f"{campo}_centavos")
        if centavos is not None:
            d[campo] = a_pesos(centavos)
    return d


CAMPOS_COMPROBANTE = ("subtotal", "total")
CAMPOS_ITEM = ("precio_unitario", "precio_costo", "subtotal")


@router.get("/historial")
def historial(tipo: str = None, limit: int = 50, offset: int = 0,
              _u=Depends(seguridad.requiere("comprobante.ver"))):
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
        return [_en_pesos(f, CAMPOS_COMPROBANTE) for f in filas]
    finally:
        conn.close()


@router.get("/resumen-dia")
def resumen_dia(fecha: Optional[str] = None,
                _u=Depends(seguridad.requiere("comprobante.ver"))):
    """
    Ventas, costo, ganancia y margen de un día (por defecto, hoy), con y sin IVA.
    Sólo facturas no anuladas: un presupuesto no es una venta.
    El costo es el que tenía cada producto al momento de vender (precio_costo del ítem).
    """
    from datetime import date
    try:
        dia = date.fromisoformat(fecha) if fecha else date.today()
    except ValueError:
        raise HTTPException(status_code=400, detail="Fecha inválida: usar AAAA-MM-DD")

    conn = conectar()
    try:
        comps = conn.execute("""
            SELECT id, total, total_centavos FROM comprobantes
            WHERE tipo = 'factura' AND estado != 'anulado' AND fecha = ?
        """, (dia.isoformat(),)).fetchall()
        ids = [c["id"] for c in comps]
        items = []
        if ids:
            marcas = ",".join("?" * len(ids))
            items = conn.execute(f"""
                SELECT cantidad, precio_costo, precio_costo_centavos FROM comprobante_items
                WHERE comprobante_id IN ({marcas})
            """, ids).fetchall()
    finally:
        conn.close()

    total_c = sum(c["total_centavos"] if c["total_centavos"] is not None else a_centavos(c["total"] or 0) for c in comps)
    costo_c, sin_costo = 0, 0
    for i in items:
        unitario_c = i["precio_costo_centavos"] if i["precio_costo_centavos"] is not None else a_centavos(i["precio_costo"] or 0)
        if not unitario_c:
            sin_costo += 1
        costo_c += a_centavos(a_decimal(i["cantidad"]) * a_decimal(unitario_c) / 100)
    ganancia_c = total_c - costo_c
    margen = float(redondear(a_decimal(ganancia_c) * 100 / a_decimal(total_c))) if total_c > 0 else None

    # Precios y costos incluyen IVA. Para un Responsable Inscripto, la ganancia real es sin IVA:
    # el IVA de la diferencia se le debe a ARCA. Se asume una sola alícuota (config.iva_alicuota).
    alicuota = config.iva_alicuota()
    total_neto_c, costo_neto_c = sin_iva(total_c, alicuota), sin_iva(costo_c, alicuota)

    return {
        "fecha":           dia.isoformat(),
        "facturas":        len(comps),
        "total":           a_pesos(total_c),
        "costo":           a_pesos(costo_c),
        "ganancia":        a_pesos(ganancia_c),
        "margen_pct":      margen,             # ganancia / venta, en %; None si no hubo ventas (igual con o sin IVA)
        "alicuota_iva":    float(alicuota),    # supuesta, igual para todos los productos
        "total_sin_iva":   a_pesos(total_neto_c),
        "costo_sin_iva":   a_pesos(costo_neto_c),
        "ganancia_sin_iva": a_pesos(total_neto_c - costo_neto_c),
        "items":           len(items),
        "items_sin_costo": sin_costo,          # si es > 0, la ganancia está sobreestimada
    }


@router.get("/{comprobante_id}")
def detalle_comprobante(comprobante_id: int,
                        _u=Depends(seguridad.requiere("comprobante.ver"))):
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
        return {**_en_pesos(cab, CAMPOS_COMPROBANTE), "items": [_en_pesos(i, CAMPOS_ITEM) for i in items]}
    finally:
        conn.close()


@router.post("/{comprobante_id}/anular")
def anular_comprobante(comprobante_id: int, request: Request,
                       usuario=Depends(seguridad.requiere("comprobante.anular"))):
    """Anula un comprobante y revierte el stock si era factura."""
    conn = conectar()
    try:
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
            for item in items:
                if item["producto_id"]:
                    conn.execute(
                        "UPDATE productos SET stock = stock + ? WHERE id = ?",
                        (item["cantidad"], item["producto_id"])
                    )

        conn.execute(
            "UPDATE comprobantes SET estado = 'anulado' WHERE id = ?", (comprobante_id,)
        )
        registrar(conn, "comprobante.anular", entidad="comprobante", entidad_id=comprobante_id,
                  antes={"numero": comp["numero"], "estado": comp["estado"]},
                  despues={"numero": comp["numero"], "estado": "anulado"},
                  usuario=usuario, ip=seguridad.ip_de(request))
        conn.commit()
        return {"ok": True, "mensaje": "Comprobante anulado"}
    finally:
        conn.close()
