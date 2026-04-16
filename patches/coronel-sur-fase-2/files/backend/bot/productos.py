"""
Acceso a productos/inventario desde el bot, con filtro de rol "bot".

El bot SÓLO ve campos públicos: código, descripción, rubro, precio_venta,
stock (como booleano "disponible"). NO ve precio_costo, precio_mayorista,
proveedor, ni historial de ventas.

Todas las búsquedas devuelven productos con activo=1, ordenados:
1. Con stock disponible primero.
2. Por descripción alfabética.
"""
from __future__ import annotations

import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar


# Campos que el bot puede exponer al cliente. Ajustar acá si cambia la
# política.
CAMPOS_PUBLICOS = (
    "id",
    "codigo",
    "descripcion",
    "rubro",
    "precio_venta",
    "stock",
    "ean",
    "foto_url",
)


# Formato con el que se muestra el stock en respuestas. "booleano"
# oculta la cantidad exacta; "numerico" la muestra. Configurable por
# env var por si querés activar después.
STOCK_FORMATO = os.environ.get("BOT_STOCK_FORMATO", "booleano").lower()


def _fila_a_dict_publico(row) -> dict:
    """Convierte una fila a dict con SÓLO los campos públicos."""
    d = dict(row)
    publico = {k: d.get(k) for k in CAMPOS_PUBLICOS if k in d}
    # Normalizar stock como "disponible": bool si STOCK_FORMATO=booleano,
    # cantidad si STOCK_FORMATO=numerico.
    stock = publico.get("stock", 0) or 0
    if STOCK_FORMATO == "numerico":
        publico["disponible"] = stock > 0
    else:
        publico["disponible"] = stock > 0
        publico.pop("stock", None)
    return publico


def buscar(
    q: Optional[str] = None,
    rubro: Optional[str] = None,
    limit: int = 40,
    solo_con_stock: bool = False,
) -> list[dict]:
    """
    Busca productos por texto en descripción/código/EAN + filtros.
    Devuelve como máximo `limit` resultados, ordenados con stock primero.
    """
    limit = max(1, min(int(limit), 200))

    conn = conectar()
    try:
        sql = "SELECT * FROM productos WHERE activo = 1"
        params: list = []

        if q:
            qlike = f"%{q.strip()}%"
            sql += " AND (descripcion LIKE ? OR codigo LIKE ? OR COALESCE(ean,'') LIKE ?)"
            params += [qlike, qlike, qlike]

        if rubro:
            sql += " AND rubro = ?"
            params.append(rubro.strip())

        if solo_con_stock:
            sql += " AND stock > 0"

        # Con stock > 0 primero; después alfabético.
        sql += f" ORDER BY (stock > 0) DESC, descripcion ASC LIMIT {limit}"

        filas = conn.execute(sql, params).fetchall()
        return [_fila_a_dict_publico(f) for f in filas]
    finally:
        conn.close()


def por_ean(ean: str) -> Optional[dict]:
    """Busca por código de barras exacto."""
    if not ean or not ean.strip():
        return None
    conn = conectar()
    try:
        fila = conn.execute(
            "SELECT * FROM productos WHERE activo = 1 AND ean = ? LIMIT 1",
            (ean.strip(),),
        ).fetchone()
        return _fila_a_dict_publico(fila) if fila else None
    finally:
        conn.close()


def por_codigo(codigo: str) -> Optional[dict]:
    """Busca por código interno exacto."""
    if not codigo or not codigo.strip():
        return None
    conn = conectar()
    try:
        fila = conn.execute(
            "SELECT * FROM productos WHERE activo = 1 AND codigo = ? LIMIT 1",
            (codigo.strip(),),
        ).fetchone()
        return _fila_a_dict_publico(fila) if fila else None
    finally:
        conn.close()


def ficha(producto_id: int) -> Optional[dict]:
    """Detalle de un producto por id."""
    conn = conectar()
    try:
        fila = conn.execute(
            "SELECT * FROM productos WHERE activo = 1 AND id = ? LIMIT 1",
            (int(producto_id),),
        ).fetchone()
        return _fila_a_dict_publico(fila) if fila else None
    finally:
        conn.close()


def rubros_disponibles(min_productos: int = 5) -> list[dict]:
    """Lista de rubros con al menos `min_productos` productos activos."""
    conn = conectar()
    try:
        filas = conn.execute(
            """SELECT rubro, COUNT(*) as cantidad
               FROM productos
               WHERE activo = 1 AND COALESCE(rubro, '') != ''
               GROUP BY rubro
               HAVING COUNT(*) >= ?
               ORDER BY cantidad DESC""",
            (int(min_productos),),
        ).fetchall()
        return [dict(f) for f in filas]
    finally:
        conn.close()


def snapshot_para_prompt(limit: int = 150) -> list[dict]:
    """
    Lista de productos para meter en el system prompt (con prompt
    caching). Trae sólo productos activos con stock, más populares
    (según ventas_historicas si existe; si no, orden alfabético).

    No trae TODOS los 9785 — sólo una muestra representativa. El bot
    puede invocar buscar() para consultas específicas.
    """
    conn = conectar()
    try:
        # Intentamos ordenar por ventas históricas (si la tabla existe y
        # tiene datos). Si falla, caemos a orden alfabético.
        try:
            filas = conn.execute(
                """SELECT p.*,
                          COALESCE(SUM(v.cantidad), 0) as veces_vendido
                   FROM productos p
                   LEFT JOIN ventas_historicas v ON v.codigo = p.codigo
                   WHERE p.activo = 1 AND p.stock > 0
                   GROUP BY p.id
                   ORDER BY veces_vendido DESC, p.descripcion ASC
                   LIMIT ?""",
                (int(limit),),
            ).fetchall()
        except Exception:
            filas = conn.execute(
                """SELECT * FROM productos
                   WHERE activo = 1 AND stock > 0
                   ORDER BY descripcion ASC
                   LIMIT ?""",
                (int(limit),),
            ).fetchall()
        return [_fila_a_dict_publico(f) for f in filas]
    finally:
        conn.close()
