"""
CRM — Gestión de clientes.

Endpoints:
  GET    /api/clientes                 lista con métricas de compra
  GET    /api/clientes/{id}            ficha completa con historial
  POST   /api/clientes/nuevo           alta
  PUT    /api/clientes/{id}            edición
  DELETE /api/clientes/{id}            baja (si no tiene comprobantes)
  POST   /api/clientes/importar-historicos   crea clientes desde ventas importadas
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar

router = APIRouter(prefix="/api/clientes", tags=["clientes"])


class ClienteIn(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    dni: Optional[str] = None
    direccion: Optional[str] = None
    tipo: str = "minorista"          # minorista | mayorista | institucional
    notas: Optional[str] = None


def _metricas(conn):
    """Compras por cliente: del sistema (comprobantes) e históricas (FactuPyme)."""
    sistema = {}
    for cid, cant, total, ult in conn.execute("""
        SELECT cliente_id, COUNT(*), COALESCE(SUM(total),0), MAX(id)
          FROM comprobantes
         WHERE estado != 'anulado' AND cliente_id IS NOT NULL
         GROUP BY cliente_id"""):
        sistema[cid] = {"compras": cant, "total": total, "ultima_id": ult}

    historicas = {}
    for nombre, cant, total, ult in conn.execute("""
        SELECT cliente, COUNT(*), COALESCE(SUM(subtotal),0), MAX(fecha)
          FROM ventas_historicas
         WHERE cliente != ''
         GROUP BY cliente"""):
        historicas[nombre.strip().lower()] = {"compras": cant, "total": total, "ultima": ult}
    return sistema, historicas


@router.get("")
@router.get("/")
def listar_clientes(buscar: str = "", tipo: str = "", limit: int = 200, offset: int = 0):
    conn = conectar()
    try:
        query = "SELECT * FROM clientes WHERE 1=1"
        params = []
        if buscar:
            query += " AND (nombre LIKE ? OR telefono LIKE ? OR email LIKE ? OR dni LIKE ?)"
            params += [f"%{buscar}%"] * 4
        if tipo:
            query += " AND tipo = ?"
            params.append(tipo)
        query += " ORDER BY nombre COLLATE NOCASE LIMIT ? OFFSET ?"
        params += [limit, offset]

        cols = None
        clientes = []
        sistema, historicas = _metricas(conn)
        for row in conn.execute(query, params):
            if cols is None:
                cols = [d[0] for d in conn.execute(query, params).description]
            c = dict(zip(cols, row))
            met_s = sistema.get(c["id"], {})
            met_h = historicas.get((c["nombre"] or "").strip().lower(), {})
            c["compras"] = met_s.get("compras", 0) + met_h.get("compras", 0)
            c["total_comprado"] = round(met_s.get("total", 0) + met_h.get("total", 0), 2)
            c["ultima_compra"] = met_h.get("ultima") or ""
            clientes.append(c)

        total = conn.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
        por_tipo = dict(conn.execute("SELECT tipo, COUNT(*) FROM clientes GROUP BY tipo"))
        return {"clientes": clientes, "total": total, "por_tipo": por_tipo}
    finally:
        conn.close()


@router.get("/{cliente_id}")
def ficha_cliente(cliente_id: int):
    conn = conectar()
    try:
        row = conn.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        cols = [d[0] for d in conn.execute("SELECT * FROM clientes LIMIT 0").description]
        cliente = dict(zip(cols, row))

        comprobantes = [
            {"id": r[0], "numero": r[1], "tipo": r[2], "fecha": r[3], "total": r[4], "estado": r[5]}
            for r in conn.execute("""
                SELECT id, numero, tipo, fecha, total, estado FROM comprobantes
                 WHERE cliente_id = ? OR (cliente_nombre != '' AND cliente_nombre = ?)
                 ORDER BY id DESC LIMIT 30""", (cliente_id, cliente["nombre"]))
        ]
        historicas = [
            {"fecha": r[0], "producto": r[1], "cantidad": r[2], "subtotal": r[3], "origen": r[4]}
            for r in conn.execute("""
                SELECT fecha, producto, cantidad, subtotal, origen FROM ventas_historicas
                 WHERE LOWER(TRIM(cliente)) = LOWER(TRIM(?))
                 ORDER BY id DESC LIMIT 50""", (cliente["nombre"],))
        ]
        total_hist = conn.execute("""
            SELECT COALESCE(SUM(subtotal),0) FROM ventas_historicas
             WHERE LOWER(TRIM(cliente)) = LOWER(TRIM(?))""", (cliente["nombre"],)).fetchone()[0]

        return {
            "cliente": cliente,
            "comprobantes": comprobantes,
            "compras_historicas": historicas,
            "total_historico": round(total_hist, 2),
        }
    finally:
        conn.close()


@router.post("/nuevo")
def crear_cliente(data: ClienteIn):
    nombre = data.nombre.strip()
    if not nombre:
        raise HTTPException(status_code=400, detail="El nombre es obligatorio")
    conn = conectar()
    try:
        dup = conn.execute(
            "SELECT id FROM clientes WHERE LOWER(TRIM(nombre)) = LOWER(TRIM(?))", (nombre,)
        ).fetchone()
        if dup:
            raise HTTPException(status_code=400, detail="Ya existe un cliente con ese nombre")
        cur = conn.execute("""
            INSERT INTO clientes (nombre, telefono, email, dni, direccion, tipo, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (nombre, data.telefono, data.email, data.dni, data.direccion, data.tipo, data.notas))
        conn.commit()
        return {"ok": True, "id": cur.lastrowid}
    finally:
        conn.close()


@router.put("/{cliente_id}")
def editar_cliente(cliente_id: int, data: ClienteIn):
    conn = conectar()
    try:
        if not conn.execute("SELECT id FROM clientes WHERE id = ?", (cliente_id,)).fetchone():
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        conn.execute("""
            UPDATE clientes
               SET nombre = ?, telefono = ?, email = ?, dni = ?, direccion = ?,
                   tipo = ?, notas = ?, actualizado_en = datetime('now','localtime')
             WHERE id = ?""",
            (data.nombre.strip(), data.telefono, data.email, data.dni,
             data.direccion, data.tipo, data.notas, cliente_id))
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()


@router.delete("/{cliente_id}")
def borrar_cliente(cliente_id: int):
    conn = conectar()
    try:
        tiene = conn.execute(
            "SELECT COUNT(*) FROM comprobantes WHERE cliente_id = ?", (cliente_id,)
        ).fetchone()[0]
        if tiene:
            raise HTTPException(
                status_code=400,
                detail=f"No se puede borrar: tiene {tiene} comprobantes asociados",
            )
        conn.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()


@router.post("/importar-historicos")
def importar_desde_historicas():
    """Crea un cliente por cada nombre distinto en las ventas importadas
    de FactuPyme que todavía no exista en el CRM."""
    conn = conectar()
    try:
        cur = conn.execute("""
            INSERT INTO clientes (nombre, tipo)
            SELECT DISTINCT TRIM(cliente), 'minorista'
              FROM ventas_historicas
             WHERE TRIM(cliente) != ''
               AND LOWER(TRIM(cliente)) NOT IN
                   (SELECT LOWER(TRIM(nombre)) FROM clientes)""")
        conn.commit()
        return {"ok": True, "importados": cur.rowcount}
    finally:
        conn.close()
