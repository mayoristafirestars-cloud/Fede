"""
Reportes — ventas por período, productos top, clientes top, márgenes.
Fuente: ventas_historicas (importadas de FactuPyme) + comprobantes del sistema.

Las fechas de FactuPyme vienen como DD-MM-YYYY; se convierten a ISO
(YYYY-MM-DD) dentro de las consultas para poder filtrar y agrupar.
"""
from fastapi import APIRouter
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar

router = APIRouter(prefix="/api/reportes", tags=["reportes"])

# fecha DD-MM-YYYY -> YYYY-MM-DD (expresión SQL reutilizable)
ISO = "substr(fecha,7,4) || '-' || substr(fecha,4,2) || '-' || substr(fecha,1,2)"


@router.get("/resumen")
def resumen(dias: int = 30):
    """KPIs + tops del período. dias=0 -> todo el historial."""
    conn = conectar()
    try:
        filtro = f"WHERE {ISO} >= date('now', '-{int(dias)} days')" if dias > 0 else ""

        # KPIs generales del período
        kpi = conn.execute(f"""
            SELECT COALESCE(SUM(subtotal),0), COALESCE(SUM(ganancia),0),
                   COUNT(DISTINCT fecha || cliente), COUNT(*)
              FROM ventas_historicas {filtro}""").fetchone()
        total_vendido, ganancia, tickets, lineas = kpi
        margen = round(ganancia / total_vendido * 100, 1) if total_vendido else 0

        # Top 10 productos por facturación
        top_productos = [
            {"producto": r[0], "cantidad": r[1], "total": round(r[2], 2)}
            for r in conn.execute(f"""
                SELECT producto, SUM(cantidad), SUM(subtotal)
                  FROM ventas_historicas {filtro}
                 GROUP BY producto ORDER BY SUM(subtotal) DESC LIMIT 10""")
        ]

        # Top 10 clientes por facturación
        top_clientes = [
            {"cliente": r[0], "compras": r[1], "total": round(r[2], 2)}
            for r in conn.execute(f"""
                SELECT cliente, COUNT(*), SUM(subtotal)
                  FROM ventas_historicas
                  {filtro + (' AND ' if filtro else ' WHERE ')} cliente != ''
                 GROUP BY cliente ORDER BY SUM(subtotal) DESC LIMIT 10""")
        ]

        # Top 10 rubros
        top_rubros = [
            {"rubro": r[0] or "(sin rubro)", "total": round(r[1], 2)}
            for r in conn.execute(f"""
                SELECT rubro, SUM(subtotal) FROM ventas_historicas {filtro}
                 GROUP BY rubro ORDER BY SUM(subtotal) DESC LIMIT 10""")
        ]

        # Ventas por mes (últimos 12 con datos)
        por_mes = [
            {"mes": r[0], "total": round(r[1], 2), "ganancia": round(r[2], 2)}
            for r in conn.execute(f"""
                SELECT substr({ISO}, 1, 7) AS mes,
                       SUM(subtotal), SUM(ganancia)
                  FROM ventas_historicas
                 GROUP BY mes ORDER BY mes DESC LIMIT 12""")
        ][::-1]

        # Comprobantes emitidos desde el sistema en el período
        comps = conn.execute("""
            SELECT COUNT(*), COALESCE(SUM(total),0) FROM comprobantes
             WHERE estado != 'anulado'""").fetchone()

        return {
            "dias": dias,
            "total_vendido": round(total_vendido, 2),
            "ganancia": round(ganancia, 2),
            "margen_pct": margen,
            "tickets": tickets,
            "lineas": lineas,
            "top_productos": top_productos,
            "top_clientes": top_clientes,
            "top_rubros": top_rubros,
            "por_mes": por_mes,
            "sistema": {"comprobantes": comps[0], "total": round(comps[1], 2)},
        }
    finally:
        conn.close()
