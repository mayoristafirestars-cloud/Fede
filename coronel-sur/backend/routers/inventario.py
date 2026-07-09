"""
Inventario — consulta y edición de stock/precios.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar

router = APIRouter(prefix="/api/inventario", tags=["inventario"])


class ProductoEdit(BaseModel):
    stock: Optional[float] = None
    precio_venta: Optional[float] = None
    precio_costo: Optional[float] = None
    activo: Optional[int] = None


@router.get("/resumen")
def resumen():
    conn = conectar()
    try:
        r = conn.execute("""
            SELECT COUNT(*),
                   COALESCE(SUM(stock * precio_costo), 0),
                   COALESCE(SUM(stock * precio_venta), 0),
                   SUM(CASE WHEN stock <= 0 THEN 1 ELSE 0 END),
                   SUM(CASE WHEN stock > 0 AND stock <= 3 THEN 1 ELSE 0 END)
              FROM productos WHERE activo = 1""").fetchone()
        return {
            "productos": r[0],
            "valor_costo": round(r[1], 2),
            "valor_venta": round(r[2], 2),
            "sin_stock": r[3] or 0,
            "stock_bajo": r[4] or 0,
        }
    finally:
        conn.close()


@router.get("/listar")
def listar(buscar: str = "", rubro: str = "", solo_sin_stock: int = 0,
           limit: int = 100, offset: int = 0):
    conn = conectar()
    try:
        query = "SELECT * FROM productos WHERE activo = 1"
        params = []
        if buscar:
            query += " AND (descripcion LIKE ? OR codigo LIKE ?)"
            params += [f"%{buscar}%", f"%{buscar}%"]
        if rubro:
            query += " AND rubro = ?"
            params.append(rubro)
        if solo_sin_stock:
            query += " AND stock <= 0"
        total = conn.execute(
            query.replace("SELECT *", "SELECT COUNT(*)"), params
        ).fetchone()[0]
        query += " ORDER BY descripcion COLLATE NOCASE LIMIT ? OFFSET ?"
        params += [limit, offset]
        return {
            "total": total,
            "productos": [dict(f) for f in conn.execute(query, params).fetchall()],
        }
    finally:
        conn.close()


@router.put("/{producto_id}")
def editar(producto_id: int, data: ProductoEdit):
    campos, params = [], []
    for campo in ("stock", "precio_venta", "precio_costo", "activo"):
        valor = getattr(data, campo)
        if valor is not None:
            campos.append(f"{campo} = ?")
            params.append(valor)
    if not campos:
        raise HTTPException(status_code=400, detail="Nada para actualizar")
    params.append(producto_id)

    conn = conectar()
    try:
        if not conn.execute("SELECT id FROM productos WHERE id = ?",
                            (producto_id,)).fetchone():
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        conn.execute(
            f"""UPDATE productos SET {', '.join(campos)},
                actualizado_en = datetime('now','localtime') WHERE id = ?""",
            params)
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()
