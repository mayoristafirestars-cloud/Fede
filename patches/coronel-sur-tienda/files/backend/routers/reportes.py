"""
Modulo Reportes - Dashboard, KPIs, analisis de ventas
"""

from fastapi import APIRouter
import sys, os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar

router = APIRouter(prefix="/api/reportes", tags=["reportes"])


def get_periodo_filtros(periodo: str, hoy: datetime):
    """Devuelve (like_pattern, fecha_inicio, fecha_fin) segun el periodo."""
    if periodo == 'mes':
        mes = hoy.strftime("%m-%Y")
        return f"%-{mes}", None, None
    elif periodo == 'anterior':
        ant = (hoy.replace(day=1) - timedelta(days=1))
        mes = ant.strftime("%m-%Y")
        return f"%-{mes}", None, None
    elif periodo == 'trimestre':
        meses = []
        for i in range(3):
            dt = hoy.replace(day=1) - timedelta(days=i*30)
            meses.append(dt.strftime("%m-%Y"))
        return meses, None, None
    elif periodo == 'anio':
        anio = hoy.strftime("%Y")
        return f"%-{anio}", None, None
    else:  # todo
        return "%", None, None


def query_total(conn, like):
    if isinstance(like, list):
        total = 0
        gan = 0
        cant = 0
        for m in like:
            r = conn.execute(
                "SELECT SUM(subtotal) as t, SUM(ganancia) as g, COUNT(*) as c FROM ventas_historicas WHERE fecha LIKE ?",
                (f"%-{m}",)
            ).fetchone()
            total += (r["t"] or 0) if r else 0
            gan += (r["g"] or 0) if r else 0
            cant += (r["c"] or 0) if r else 0
        return total, gan, cant
    else:
        r = conn.execute(
            "SELECT SUM(subtotal) as t, SUM(ganancia) as g, COUNT(*) as c FROM ventas_historicas WHERE fecha LIKE ?",
            (like,)
        ).fetchone()
        if not r:
            return 0, 0, 0
        return r["t"] or 0, r["g"] or 0, r["c"] or 0


@router.get("/dashboard")
def dashboard(periodo: str = "mes"):
    conn = conectar()
    try:
        hoy = datetime.now()
        mes = hoy.strftime("%m-%Y")
        hoy_str = hoy.strftime("%d-%m-%Y")

        like = get_periodo_filtros(periodo, hoy)
        if isinstance(like, tuple):
            like = like[0]

        # Totales del periodo
        total_periodo, ganancia_periodo, cant_periodo = query_total(conn, like)
        margen_periodo = (ganancia_periodo / total_periodo * 100) if total_periodo > 0 else 0

        # Mes anterior para comparacion
        ant = (hoy.replace(day=1) - timedelta(days=1))
        mes_ant_str = ant.strftime("%m-%Y")
        total_ant, gan_ant, cant_ant = query_total(conn, f"%-{mes_ant_str}")

        # Ventas de hoy (sistema)
        hoy_sistema = conn.execute(
            "SELECT SUM(total) as t, COUNT(*) as c FROM comprobantes WHERE fecha=? AND estado!='anulado' AND tipo='factura'",
            (hoy_str,)
        ).fetchone()
        total_hoy = (hoy_sistema["t"] or 0) if hoy_sistema else 0
        cant_hoy  = (hoy_sistema["c"] or 0) if hoy_sistema else 0

        # Meta
        meta_mes = 11_269_041
        dias_habiles_mes = 26
        dia_actual = min(hoy.day, dias_habiles_mes)
        meta_diaria = meta_mes / dias_habiles_mes
        proyeccion = (total_periodo / dia_actual * dias_habiles_mes) if dia_actual > 0 else 0

        # Dias para meta
        ventas_diarias = total_periodo / dia_actual if dia_actual > 0 else 0
        faltante = max(0, meta_mes - total_periodo)
        dias_meta = round(faltante / ventas_diarias) if ventas_diarias > 0 else -1

        # Ventas por mes (ultimos 12)
        ventas_por_mes = []
        for i in range(11, -1, -1):
            dt = hoy.replace(day=1) - timedelta(days=i*30)
            m = dt.strftime("%m-%Y")
            lbl = dt.strftime("%b %y")
            rr = conn.execute(
                "SELECT SUM(subtotal) as t FROM ventas_historicas WHERE fecha LIKE ?",
                (f"%-{m}",)
            ).fetchone()
            tot = (rr["t"] or 0) if rr else 0
            ventas_por_mes.append({"mes": lbl, "total": round(tot, 0)})

        # Margen por mes (ultimos 6)
        margen_por_mes = []
        for i in range(5, -1, -1):
            dt = hoy.replace(day=1) - timedelta(days=i*30)
            m = dt.strftime("%m-%Y")
            lbl = dt.strftime("%b %y")
            r = conn.execute(
                "SELECT SUM(subtotal) as t, SUM(ganancia) as g FROM ventas_historicas WHERE fecha LIKE ?",
                (f"%-{m}",)
            ).fetchone()
            t = (r["t"] or 0) if r else 0
            g = (r["g"] or 0) if r else 0
            mar = round(g/t*100, 1) if t > 0 else 0
            margen_por_mes.append({"mes": lbl, "margen": mar})

        # Por dia de la semana
        dias_map = {0:'Lun',1:'Mar',2:'Mie',3:'Jue',4:'Vie',5:'Sab',6:'Dom'}
        dias_totales = {d: 0 for d in range(7)}

        if isinstance(like, list):
            rows_dias = []
            for m in like:
                rows_dias += conn.execute(
                    "SELECT fecha, SUM(subtotal) as total FROM ventas_historicas WHERE fecha LIKE ? GROUP BY fecha",
                    (f"%-{m}",)
                ).fetchall()
        else:
            rows_dias = conn.execute(
                "SELECT fecha, SUM(subtotal) as total FROM ventas_historicas WHERE fecha LIKE ? GROUP BY fecha",
                (like,)
            ).fetchall()

        mejor_dia_total = 0
        mejor_dia_str = None
        for row in rows_dias:
            try:
                partes = str(row[0]).split('-')
                if len(partes) == 3:
                    dt = datetime(int(partes[2]), int(partes[1]), int(partes[0]))
                    dias_totales[dt.weekday()] += row[1] or 0
                    if (row[1] or 0) > mejor_dia_total:
                        mejor_dia_total = row[1] or 0
                        mejor_dia_str = row[0]
            except:
                pass

        por_dia_semana = [{"dia": dias_map[i], "total": round(dias_totales[i], 0)} for i in range(7)]

        # Por rubro
        if isinstance(like, list):
            placeholders = ','.join(['?' for _ in like])
            likes = [f"%-{m}" for m in like]
            por_rubro_rows = []
            for lk in likes:
                por_rubro_rows += conn.execute(
                    "SELECT rubro, SUM(subtotal) as total, SUM(ganancia) as ganancia FROM ventas_historicas WHERE fecha LIKE ? AND rubro != '' GROUP BY rubro",
                    (lk,)
                ).fetchall()
            rubro_dict = {}
            for r in por_rubro_rows:
                rub = r[0]
                if rub not in rubro_dict:
                    rubro_dict[rub] = {'rubro': rub, 'total': 0, 'ganancia': 0}
                rubro_dict[rub]['total'] += r[1] or 0
                rubro_dict[rub]['ganancia'] += r[2] or 0
            por_rubro_data = sorted(rubro_dict.values(), key=lambda x: -x['total'])
        else:
            por_rubro_data = [dict(r) for r in conn.execute(
                "SELECT rubro, SUM(subtotal) as total, SUM(ganancia) as ganancia FROM ventas_historicas WHERE fecha LIKE ? AND rubro != '' GROUP BY rubro ORDER BY total DESC",
                (like,)
            ).fetchall()]

        rubro_data = []
        for r in por_rubro_data:
            r['margen'] = round(r['ganancia'] / r['total'] * 100, 1) if r['total'] > 0 else 0
            rubro_data.append(r)

        # Top 10 productos
        if isinstance(like, list):
            prod_dict = {}
            for lk in [f"%-{m}" for m in like]:
                rows = conn.execute(
                    "SELECT producto, rubro, SUM(cantidad) as unidades, SUM(subtotal) as facturado, SUM(ganancia) as ganancia FROM ventas_historicas WHERE fecha LIKE ? GROUP BY producto",
                    (lk,)
                ).fetchall()
                for r in rows:
                    k = r[0]
                    if k not in prod_dict:
                        prod_dict[k] = {'producto': r[0], 'rubro': r[1], 'unidades': 0, 'facturado': 0, 'ganancia': 0}
                    prod_dict[k]['unidades'] += r[2] or 0
                    prod_dict[k]['facturado'] += r[3] or 0
                    prod_dict[k]['ganancia'] += r[4] or 0
            top_productos = sorted(prod_dict.values(), key=lambda x: -x['facturado'])[:10]
        else:
            top_productos = [dict(r) for r in conn.execute(
                "SELECT producto, rubro, SUM(cantidad) as unidades, SUM(subtotal) as facturado, SUM(ganancia) as ganancia FROM ventas_historicas WHERE fecha LIKE ? GROUP BY producto ORDER BY facturado DESC LIMIT 10",
                (like,)
            ).fetchall()]

        top_data = []
        for p in top_productos:
            p['margen'] = round(p['ganancia'] / p['facturado'] * 100, 1) if p['facturado'] > 0 else 0
            top_data.append(p)

        # Top clientes
        if isinstance(like, list):
            cli_dict = {}
            for lk in [f"%-{m}" for m in like]:
                rows = conn.execute(
                    "SELECT cliente_nombre, SUM(subtotal) as total, COUNT(*) as compras FROM ventas_historicas WHERE fecha LIKE ? AND cliente_nombre IS NOT NULL AND cliente_nombre != '' GROUP BY cliente_nombre",
                    (lk,)
                ).fetchall()
                for r in rows:
                    k = r[0]
                    if k not in cli_dict:
                        cli_dict[k] = {'nombre': r[0], 'total': 0, 'compras': 0}
                    cli_dict[k]['total'] += r[1] or 0
                    cli_dict[k]['compras'] += r[2] or 0
            top_clientes = sorted(cli_dict.values(), key=lambda x: -x['total'])[:5]
        else:
            top_clientes = [dict(r) for r in conn.execute(
                "SELECT cliente_nombre as nombre, SUM(subtotal) as total, COUNT(*) as compras FROM ventas_historicas WHERE fecha LIKE ? AND cliente_nombre IS NOT NULL AND cliente_nombre != '' GROUP BY cliente_nombre ORDER BY total DESC LIMIT 5",
                (like,)
            ).fetchall()]

        # Mes actual vs anterior (para comparacion)
        total_mes_act, gan_mes_act, comp_mes_act = query_total(conn, f"%-{mes}")
        comparacion = {
            'ventas_actual':   round(total_mes_act, 0),
            'ventas_anterior': round(total_ant, 0),
            'gan_actual':      round(gan_mes_act, 0),
            'gan_anterior':    round(gan_ant, 0),
            'comp_actual':     comp_mes_act,
            'comp_anterior':   cant_ant,
        }

        # Comisiones
        comisiones = []
        for nombre in ["Malcolm", "Ana Mar"]:
            escalones = [(8_000_000,1.0),(10_000_000,1.5),(13_000_000,2.0),(16_000_000,2.5)]
            nivel = None
            pct = 0
            for meta, p in escalones:
                if total_mes_act >= meta:
                    nivel = meta
                    pct = p
            comision = total_mes_act * pct / 100 if nivel else 0
            comisiones.append({
                "nombre":  nombre,
                "comision": round(comision, 0),
                "pct":      pct,
                "nivel":    "BRONCE" if pct==1 else "PLATA" if pct==1.5 else "ORO" if pct==2 else "DIAMANTE" if pct==2.5 else "—",
            })

        # ── VENTAS POR HORA (usando comprobantes.creado_en) ──
        por_hora = []
        for h in range(24):
            por_hora.append({"hora": f"{h:02d}:00", "total": 0, "cant": 0})
        mejor_hora = por_hora[0]
        peor_hora_activa = None
        try:
            rows_hora = conn.execute(
                "SELECT creado_en, total FROM comprobantes WHERE estado != 'anulado' AND tipo = 'factura'",
                ()
            ).fetchall()
            for row in rows_hora:
                try:
                    d = dict(row)
                    ts = str(d.get("creado_en") or "")
                    monto = float(d.get("total") or 0)
                    if " " in ts and monto > 0:
                        partes_hora = ts.split(" ")[1].split(":")
                        h = int(partes_hora[0])
                        if 0 <= h < 24:
                            por_hora[h]["total"] += monto
                            por_hora[h]["cant"] += 1
                except Exception:
                    continue
            mejor_hora = max(por_hora, key=lambda x: x["total"])
            horas_activas = [h for h in por_hora if h["cant"] > 0]
            if horas_activas:
                peor_hora_activa = min(horas_activas, key=lambda x: x["total"])
        except Exception:
            pass

        return {
            "hoy": {
                "total":    round(total_hoy, 0),
                "cant":     cant_hoy,
                "meta_dia": round(meta_diaria, 0),
                "pct_meta": round(total_hoy / meta_diaria * 100, 1) if meta_diaria > 0 else 0,
            },
            "mes": {
                "total":       round(total_periodo, 0),
                "ganancia":    round(ganancia_periodo, 0),
                "margen":      round(margen_periodo, 1),
                "meta":        meta_mes,
                "pct_meta":    round(total_periodo / meta_mes * 100, 1),
                "proyeccion":  round(proyeccion, 0),
                "vs_anterior": round((total_periodo - total_ant) / total_ant * 100, 1) if total_ant > 0 else 0,
            },
            "comprobantes":   cant_periodo,
            "mejor_dia":      mejor_dia_str,
            "dias_para_meta": dias_meta,
            "ventas_por_mes": ventas_por_mes,
            "margen_por_mes": margen_por_mes,
            "por_dia_semana": por_dia_semana,
            "por_rubro":      rubro_data,
            "top_productos":  top_data,
            "top_clientes":   top_clientes,
            "comparacion":    comparacion,
            "comisiones":     comisiones,
            "por_hora":       por_hora,
            "mejor_hora":     mejor_hora,
            "peor_hora":      peor_hora_activa,
        }
    finally:
        conn.close()


@router.get("/comisiones")
def comisiones_mes(ventas: float = 0):
    escalones = [
        {"nivel": "BRONCE",   "meta": 8_000_000,  "pct": 1.0},
        {"nivel": "PLATA",    "meta": 10_000_000, "pct": 1.5},
        {"nivel": "ORO",      "meta": 13_000_000, "pct": 2.0},
        {"nivel": "DIAMANTE", "meta": 16_000_000, "pct": 2.5},
    ]
    resultado = []
    for e in escalones:
        com = ventas * e["pct"] / 100 if ventas >= e["meta"] else 0
        resultado.append({
            **e,
            "alcanzado": ventas >= e["meta"],
            "comision":  round(com, 0),
            "faltante":  max(0, round(e["meta"] - ventas, 0)),
        })
    return {"ventas": ventas, "escalones": resultado}
