"""
Consultas de cartera: arma los datos de la base y llama al motor.
Toda consulta filtra por empresa_id.
"""

import os
from collections import defaultdict
from datetime import date, datetime

from copiloto import motor
from copiloto.motor import Ajuste, Aplicacion, Documento


def dias_desactualizado() -> int:
    return int(os.environ.get("DIAS_DATOS_DESACTUALIZADOS", "3"))


def _fecha(texto: str) -> date:
    return date.fromisoformat(texto[:10])


def _cargar(conn, empresa_id: int, cliente_id: int | None = None):
    filtro, params = "empresa_id = ?", [empresa_id]
    if cliente_id is not None:
        filtro += " AND cliente_id = ?"
        params.append(cliente_id)
    documentos, aplicaciones, ajustes = defaultdict(list), defaultdict(list), defaultdict(list)
    cliente_de_doc = {}
    for d in conn.execute(f"SELECT * FROM documento_comercial WHERE {filtro}", params):
        cliente_de_doc[d["id"]] = d["cliente_id"]
        documentos[d["cliente_id"]].append(Documento(d["id"], d["tipo"], d["importe_centavos"], _fecha(d["fecha_emision"]),
                                                     _fecha(d["fecha_vencimiento"]), d["estado"] == "anulado"))
    for a in conn.execute("SELECT * FROM aplicacion WHERE empresa_id = ?", (empresa_id,)):
        if a["documento_id"] in cliente_de_doc:
            aplicaciones[cliente_de_doc[a["documento_id"]]].append(
                Aplicacion(a["documento_id"], a["origen_tipo"], a["origen_id"], a["importe_centavos"]))
    for a in conn.execute(f"SELECT * FROM ajuste WHERE {filtro}", params):
        ajustes[a["cliente_id"]].append(Ajuste(a["id"], a["sentido"], a["importe_centavos"], _fecha(a["creado_en"]),
                                               a["documento_id"], a["revierte_a"]))
    return documentos, aplicaciones, ajustes


def datos_al(conn, empresa_id: int) -> dict:
    """Fecha de la última importación confirmada y si los datos están desactualizados."""
    ultima = conn.execute(
        "SELECT MAX(confirmado_en) FROM lote_importacion WHERE empresa_id = ? AND estado = 'confirmado'", (empresa_id,)
    ).fetchone()[0]
    if not ultima:
        return {"datos_al": None, "desactualizado": True, "aviso": "Todavía no se importó ninguna cartera."}
    fecha = datetime.fromisoformat(ultima).date()
    dias = (date.today() - fecha).days
    viejo = dias > dias_desactualizado()
    return {"datos_al": fecha.isoformat(), "desactualizado": viejo,
            "aviso": f"Los datos tienen {dias} días: importá las novedades antes de cobrar." if viejo else None}


def resumen_clientes(conn, empresa_id: int, corte: date | None = None, buscar: str | None = None) -> list[dict]:
    corte = corte or date.today()
    documentos, aplicaciones, ajustes = _cargar(conn, empresa_id)
    clientes = conn.execute(
        "SELECT id, nombre, cuit, condicion_pago_dias, cuenta_corriente, limite_informativo_centavos FROM clientes WHERE empresa_id = ?",
        (empresa_id,),
    ).fetchall()
    salida = []
    for c in clientes:
        if not (c["cuenta_corriente"] or documentos.get(c["id"]) or ajustes.get(c["id"])):
            continue
        if buscar and buscar.lower() not in f"{c['nombre']} {c['cuit'] or ''}".lower():
            continue
        r = motor.resumir(documentos.get(c["id"], []), aplicaciones.get(c["id"], []), ajustes.get(c["id"], []), corte)
        vencidas = [p for p in r.partidas if p.saldo > 0 and p.dias_vencido > 0]
        salida.append({
            "id": c["id"], "nombre": c["nombre"], "cuit": c["cuit"],
            "condicion_pago_dias": c["condicion_pago_dias"],
            "limite_informativo_centavos": c["limite_informativo_centavos"],
            "saldo_centavos": r.saldo, "vencido_centavos": r.vencido,
            "creditos_sin_imputar_centavos": r.creditos_sin_imputar, "tramos_centavos": r.tramos,
            "dias_mayor_atraso": max((p.dias_vencido for p in vencidas), default=0),
        })
    salida.sort(key=lambda x: (-x["vencido_centavos"], -x["saldo_centavos"], x["nombre"]))
    return salida


def resumen_cartera(conn, empresa_id: int, corte: date | None = None) -> dict:
    clientes = resumen_clientes(conn, empresa_id, corte)
    tramos = {t: sum(c["tramos_centavos"][t] for c in clientes) for t in motor.TRAMOS}
    return {
        "corte": (corte or date.today()).isoformat(),
        "saldo_centavos": sum(c["saldo_centavos"] for c in clientes),
        "vencido_centavos": sum(c["vencido_centavos"] for c in clientes),
        "creditos_sin_imputar_centavos": sum(c["creditos_sin_imputar_centavos"] for c in clientes),
        "tramos_centavos": tramos,
        "clientes_con_saldo": sum(1 for c in clientes if c["saldo_centavos"] > 0),
        "clientes_con_vencido": sum(1 for c in clientes if c["vencido_centavos"] > 0),
        **datos_al(conn, empresa_id),
    }


def detalle_cliente(conn, empresa_id: int, cliente_id: int, corte: date | None = None) -> dict | None:
    corte = corte or date.today()
    c = conn.execute("SELECT * FROM clientes WHERE id = ? AND empresa_id = ?", (cliente_id, empresa_id)).fetchone()
    if not c:
        return None
    documentos, aplicaciones, ajustes = _cargar(conn, empresa_id, cliente_id)
    r = motor.resumir(documentos.get(cliente_id, []), aplicaciones.get(cliente_id, []), ajustes.get(cliente_id, []), corte)
    partidas = {p.clave: p for p in r.partidas}
    docs = []
    for d in conn.execute("SELECT * FROM documento_comercial WHERE cliente_id = ? AND empresa_id = ? ORDER BY fecha_emision, id",
                          (cliente_id, empresa_id)):
        p = partidas.get(f"doc:{d['id']}")
        disponible = r.creditos.get(f"doc:{d['id']}")
        docs.append({
            "id": d["id"], "tipo": d["tipo"], "letra": d["letra"], "punto_venta": d["punto_venta"], "numero": d["numero"],
            "fecha_emision": d["fecha_emision"], "fecha_vencimiento": d["fecha_vencimiento"],
            "importe_centavos": d["importe_centavos"], "fuente": d["fuente"], "lote_id": d["lote_id"],
            "saldo_centavos": p.saldo if p else None,
            "disponible_centavos": disponible if d["tipo"] == "NC" and d["estado"] != "anulado" else None,
            "estado": p.estado if p else ("anulado" if d["estado"] == "anulado" else ("aplicada" if not disponible else "sin_imputar")),
            "dias_vencido": p.dias_vencido if p and p.saldo > 0 else 0,
        })
    contactos = [dict(x) for x in conn.execute(
        "SELECT id, nombre, telefono_e164, email, canal, consentimiento_fecha, baja_fecha FROM contacto_autorizado WHERE cliente_id = ? AND empresa_id = ?",
        (cliente_id, empresa_id))]
    return {
        "cliente": {k: c[k] for k in ("id", "nombre", "cuit", "tipo", "telefono", "email", "condicion_pago_dias",
                                      "cuenta_corriente", "limite_informativo_centavos")},
        "resumen": {"saldo_centavos": r.saldo, "deuda_bruta_centavos": r.deuda_bruta, "vencido_centavos": r.vencido,
                    "creditos_sin_imputar_centavos": r.creditos_sin_imputar, "tramos_centavos": r.tramos},
        "documentos": docs,
        "aplicaciones": [dict(x) for x in conn.execute(
            """SELECT a.* FROM aplicacion a JOIN documento_comercial d ON d.id = a.documento_id
               WHERE d.cliente_id = ? AND a.empresa_id = ? ORDER BY a.id""", (cliente_id, empresa_id))],
        "ajustes": [dict(x) for x in conn.execute(
            "SELECT * FROM ajuste WHERE cliente_id = ? AND empresa_id = ? ORDER BY id", (cliente_id, empresa_id))],
        "contactos": contactos,
        **datos_al(conn, empresa_id),
    }
