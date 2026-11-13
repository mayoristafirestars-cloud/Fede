"""
Importación de cartera: vista previa → confirmar → (revertir).

Formatos:
- saldo_inicial: planilla del dueño con lo adeudado a una fecha de corte (documentos SI).
- arca_emitidos: ARCA "Mis Comprobantes Emitidos" (FC, ND, NC). Sólo se toman
  comprobantes de clientes con cuenta corriente y posteriores a su saldo inicial.

Reglas: nada se borra; reimportar no duplica; revertir anula los documentos del lote.
"""

import hashlib
import json
import os
from datetime import date, datetime
from decimal import Decimal

from copiloto import lectura
from copiloto.lectura import ErrorDato
from db.auditoria import registrar
from dinero import a_centavos

# Códigos de comprobante de ARCA → (tipo, letra)
TIPOS_ARCA = {
    1: ("FC", "A"), 2: ("ND", "A"), 3: ("NC", "A"),
    6: ("FC", "B"), 7: ("ND", "B"), 8: ("NC", "B"),
    11: ("FC", "C"), 12: ("ND", "C"), 13: ("NC", "C"),
    51: ("FC", "M"), 52: ("ND", "M"), 53: ("NC", "M"),
    201: ("FC", "A"), 202: ("ND", "A"), 203: ("NC", "A"),     # FCE MiPyME
    206: ("FC", "B"), 207: ("ND", "B"), 208: ("NC", "B"),
    211: ("FC", "C"), 212: ("ND", "C"), 213: ("NC", "C"),
}
MONEDAS_PESOS = {"", "PES", "$", "ARS", "PESOS"}


class ErrorImportacion(ValueError):
    pass


def condicion_defecto() -> int:
    return int(os.environ.get("CONDICION_PAGO_DIAS_DEFECTO", "30"))


def _nombre_clave(nombre: str) -> str:
    return lectura.clave(nombre)


# ─── Interpretación de filas ───────────────────────────────

def _celda(fila, columnas, campo):
    j = columnas.get(campo)
    if j is None or j >= len(fila):
        return None
    valor = fila[j]
    return valor.strip() if isinstance(valor, str) else valor


def _fila_saldo_inicial(fila, columnas, fecha_corte: date) -> dict:
    nombre = str(_celda(fila, columnas, "cliente") or "").strip()
    if not nombre:
        raise ErrorDato("cliente vacío")
    cuit_txt = _celda(fila, columnas, "cuit")
    cuit = lectura.normalizar_cuit(cuit_txt) if cuit_txt not in (None, "") else None
    saldo = lectura.parsear_importe(_celda(fila, columnas, "saldo"))
    if saldo < 0:
        raise ErrorDato("saldo negativo (a favor del cliente): cargalo después como ajuste crédito")
    fecha = lectura.parsear_fecha(_celda(fila, columnas, "fecha"))
    if fecha > fecha_corte:
        raise ErrorDato(f"la fecha ({fecha:%d/%m/%Y}) es posterior a la fecha de corte")
    venc_txt = _celda(fila, columnas, "vencimiento")
    cond_txt = _celda(fila, columnas, "condicion")
    condicion = int(lectura.parsear_importe(cond_txt)) if cond_txt not in (None, "") else None
    if condicion is not None and not 0 <= condicion <= 365:
        raise ErrorDato("condición de pago fuera de rango (0 a 365 días)")
    vencimiento = lectura.parsear_fecha(venc_txt) if venc_txt not in (None, "") else \
        lectura.mas_dias(fecha, condicion if condicion is not None else condicion_defecto())
    tel_txt = _celda(fila, columnas, "telefono")
    return {
        "cliente": nombre, "cuit": cuit, "importe": a_centavos(saldo), "tipo": "SI",
        "fecha_emision": fecha.isoformat(), "fecha_vencimiento": vencimiento.isoformat(),
        "condicion": condicion, "telefono": lectura.normalizar_telefono(tel_txt) if tel_txt else None,
        "telefono_original": str(tel_txt) if tel_txt else None,
        "id_externo": f"SI:{cuit or 'NOM:' + _nombre_clave(nombre)}:{fecha_corte.isoformat()}",
    }


def _fila_arca(fila, columnas) -> dict | None:
    tipo_txt = str(_celda(fila, columnas, "tipo") or "").strip()
    if not tipo_txt:
        raise ErrorDato("tipo de comprobante vacío")
    try:
        codigo = int(str(tipo_txt).split("-")[0].strip().split(" ")[0])
    except ValueError:
        raise ErrorDato(f"tipo de comprobante ilegible ({tipo_txt!r})")
    if codigo not in TIPOS_ARCA:
        return None                                   # recibos, remitos, etc.: no son deuda
    tipo, letra = TIPOS_ARCA[codigo]
    moneda = str(_celda(fila, columnas, "moneda") or "").strip().upper()
    if moneda not in MONEDAS_PESOS:
        raise ErrorDato(f"moneda no soportada ({moneda}): sólo pesos")
    fecha = lectura.parsear_fecha(_celda(fila, columnas, "fecha"))
    total = lectura.parsear_importe(_celda(fila, columnas, "total"))
    if total <= 0:
        raise ErrorDato("importe total cero o negativo")
    pv = int(lectura.parsear_importe(_celda(fila, columnas, "punto_venta")))
    numero = int(lectura.parsear_importe(_celda(fila, columnas, "numero")))
    venc_txt = _celda(fila, columnas, "vencimiento")
    return {
        "cliente": str(_celda(fila, columnas, "cliente") or "").strip(),
        "cuit": lectura.normalizar_cuit(_celda(fila, columnas, "cuit")),
        "importe": a_centavos(total), "tipo": tipo, "letra": letra,
        "punto_venta": pv, "numero": numero,
        "fecha_emision": fecha.isoformat(),
        "fecha_vencimiento": lectura.parsear_fecha(venc_txt).isoformat() if venc_txt not in (None, "") else None,
        "id_externo": f"{codigo:03d}-{pv:05d}-{numero:08d}",
    }


# ─── Vista previa ──────────────────────────────────────────

def vista_previa(conn, usuario, formato: str, nombre_archivo: str, contenido: bytes,
                 fecha_corte: date | None = None) -> dict:
    """Lee el archivo, valida fila por fila y guarda el lote en estado vista_previa."""
    if formato not in ("saldo_inicial", "arca_emitidos"):
        raise ErrorImportacion("Formato desconocido")
    empresa_id = usuario.empresa_id
    hash_archivo = hashlib.sha256(contenido).hexdigest()
    previo = conn.execute(
        "SELECT id FROM lote_importacion WHERE empresa_id = ? AND hash_sha256 = ? AND estado = 'confirmado'",
        (empresa_id, hash_archivo),
    ).fetchone()
    if previo:
        raise ErrorImportacion(f"Este archivo ya se importó (lote {previo['id']}). No se vuelve a importar.")

    mapeo = lectura.cargar_mapeo(formato)
    filas = lectura.leer_filas(nombre_archivo, contenido)
    inicio, columnas = lectura.ubicar_columnas(filas, mapeo)
    fecha_corte = fecha_corte or date.today()

    validas, errores, omitidas, vistos = [], [], [], set()
    for n, fila in enumerate(filas[inicio + 1:], start=inicio + 2):        # n = número de fila en el archivo
        if not any(v not in (None, "") for v in fila):
            continue
        try:
            dato = _fila_saldo_inicial(fila, columnas, fecha_corte) if formato == "saldo_inicial" else _fila_arca(fila, columnas)
        except ErrorDato as e:
            errores.append({"fila": n, "error": str(e)})
            continue
        if dato is None:
            omitidas.append({"fila": n, "motivo": "tipo de comprobante que no genera deuda"})
            continue
        if formato == "saldo_inicial" and dato["importe"] == 0:
            omitidas.append({"fila": n, "motivo": "saldo cero"})
            continue
        if dato["id_externo"] in vistos:
            errores.append({"fila": n, "error": "fila duplicada dentro del archivo"})
            continue
        vistos.add(dato["id_externo"])
        if formato == "arca_emitidos":
            motivo = _motivo_omision_arca(conn, empresa_id, dato)
            if motivo:
                omitidas.append({"fila": n, "motivo": motivo, "cuit": dato["cuit"]})
                continue
        if conn.execute("SELECT 1 FROM documento_comercial WHERE empresa_id = ? AND fuente = ? AND id_externo = ? AND estado = 'emitido'",
                        (empresa_id, formato, dato["id_externo"])).fetchone():
            omitidas.append({"fila": n, "motivo": "ya importado antes"})
            continue
        dato["fila"] = n
        validas.append(dato)

    total = sum(-d["importe"] if d["tipo"] == "NC" else d["importe"] for d in validas)
    cur = conn.execute(
        """INSERT INTO lote_importacion (empresa_id, formato, archivo, hash_sha256, filas_totales, filas_ok,
               filas_error, filas_omitidas, errores, filas, total_archivo_centavos, fecha_corte, importado_por)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (empresa_id, formato, os.path.basename(nombre_archivo)[:200], hash_archivo,
         len(validas) + len(errores) + len(omitidas), len(validas), len(errores), len(omitidas),
         json.dumps({"errores": errores, "omitidas": omitidas}, ensure_ascii=False),
         json.dumps(validas, ensure_ascii=False), total,
         fecha_corte.isoformat() if formato == "saldo_inicial" else None, usuario.id),
    )
    return detalle_lote(conn, empresa_id, cur.lastrowid)


def _motivo_omision_arca(conn, empresa_id: int, dato: dict) -> str | None:
    cliente = conn.execute(
        "SELECT id, cuenta_corriente FROM clientes WHERE empresa_id = ? AND cuit = ?",
        (empresa_id, dato["cuit"]),
    ).fetchone()
    if not cliente or not cliente["cuenta_corriente"]:
        return "cliente sin cuenta corriente (venta de contado)"
    corte = conn.execute(
        """SELECT MAX(l.fecha_corte) FROM documento_comercial d JOIN lote_importacion l ON l.id = d.lote_id
           WHERE d.empresa_id = ? AND d.cliente_id = ? AND d.tipo = 'SI' AND d.estado = 'emitido'""",
        (empresa_id, cliente["id"]),
    ).fetchone()[0]
    if corte and dato["fecha_emision"] <= corte:
        return f"anterior o igual a la fecha de corte del saldo inicial ({corte}): ya está incluido"
    return None


def detalle_lote(conn, empresa_id: int, lote_id: int) -> dict:
    lote = conn.execute("SELECT * FROM lote_importacion WHERE id = ? AND empresa_id = ?", (lote_id, empresa_id)).fetchone()
    if not lote:
        raise LookupError("Lote no encontrado")
    detalle = json.loads(lote["errores"] or "{}")
    filas = json.loads(lote["filas"] or "[]")
    return {
        "id": lote["id"], "formato": lote["formato"], "archivo": lote["archivo"], "estado": lote["estado"],
        "filas_totales": lote["filas_totales"], "filas_ok": lote["filas_ok"],
        "filas_error": lote["filas_error"], "filas_omitidas": lote["filas_omitidas"],
        "errores": detalle.get("errores", []), "omitidas": detalle.get("omitidas", []),
        "total_archivo_centavos": lote["total_archivo_centavos"],
        "total_informado_centavos": lote["total_informado_centavos"],
        "excepciones": json.loads(lote["excepciones"]) if lote["excepciones"] else None,
        "fecha_corte": lote["fecha_corte"], "creado_en": lote["creado_en"],
        "confirmado_en": lote["confirmado_en"], "revertido_en": lote["revertido_en"],
        "muestra": filas[:20],
    }


# ─── Confirmar ─────────────────────────────────────────────

def _cliente_para(conn, empresa_id: int, dato: dict, crear: bool) -> int | None:
    fila = None
    if dato.get("cuit"):
        fila = conn.execute("SELECT id FROM clientes WHERE empresa_id = ? AND cuit = ?", (empresa_id, dato["cuit"])).fetchone()
    if not fila and dato.get("cliente"):
        candidatos = [c for c in conn.execute("SELECT id, nombre, cuit FROM clientes WHERE empresa_id = ?", (empresa_id,))
                      if _nombre_clave(c["nombre"]) == _nombre_clave(dato["cliente"]) and (not c["cuit"] or not dato.get("cuit"))]
        if len(candidatos) == 1:
            fila = candidatos[0]
            if dato.get("cuit"):
                conn.execute("UPDATE clientes SET cuit = ? WHERE id = ?", (dato["cuit"], fila["id"]))
    if fila:
        return fila["id"]
    if not crear:
        return None
    cur = conn.execute(
        "INSERT INTO clientes (nombre, empresa_id, cuit, tipo) VALUES (?, ?, ?, 'mayorista')",
        (dato["cliente"] or dato.get("cuit"), empresa_id, dato.get("cuit")),
    )
    return cur.lastrowid


def confirmar(conn, usuario, lote_id: int, total_informado: Decimal | None, motivo_diferencia: str | None) -> dict:
    empresa_id = usuario.empresa_id
    lote = conn.execute("SELECT * FROM lote_importacion WHERE id = ? AND empresa_id = ?", (lote_id, empresa_id)).fetchone()
    if not lote:
        raise LookupError("Lote no encontrado")
    if lote["estado"] != "vista_previa":
        raise ErrorImportacion(f"El lote está {lote['estado']}: no se puede confirmar")
    formato = lote["formato"]
    total_archivo = lote["total_archivo_centavos"]

    if formato == "saldo_inicial" and total_informado is None:
        raise ErrorImportacion("Falta el total que informa tu registro (cuaderno, planilla o sistema anterior)")
    informado_c = a_centavos(total_informado) if total_informado is not None else None
    excepciones = None
    if informado_c is not None and informado_c != total_archivo:
        if not (motivo_diferencia or "").strip():
            raise ErrorImportacion(
                f"El total del archivo ($ {Decimal(total_archivo) / 100:,.2f}) no coincide con el informado "
                f"($ {Decimal(informado_c) / 100:,.2f}). Diferencia: $ {Decimal(informado_c - total_archivo) / 100:,.2f}. "
                "Corregí el archivo o explicá la diferencia para confirmar igual.")
        excepciones = {"tipo": "diferencia_de_total", "total_archivo_centavos": total_archivo,
                       "total_informado_centavos": informado_c, "diferencia_centavos": informado_c - total_archivo,
                       "motivo": motivo_diferencia.strip(), "filas_con_error": lote["filas_error"]}

    creados, duplicados, clientes_nuevos = 0, 0, 0
    for dato in json.loads(lote["filas"] or "[]"):
        if conn.execute("SELECT 1 FROM documento_comercial WHERE empresa_id = ? AND fuente = ? AND id_externo = ? AND estado = 'emitido'",
                        (empresa_id, formato, dato["id_externo"])).fetchone():
            duplicados += 1
            continue
        antes = conn.execute("SELECT COUNT(*) FROM clientes WHERE empresa_id = ?", (empresa_id,)).fetchone()[0]
        cliente_id = _cliente_para(conn, empresa_id, dato, crear=(formato == "saldo_inicial"))
        if cliente_id is None:
            duplicados += 1                       # el cliente dejó de existir o de tener cuenta corriente
            continue
        clientes_nuevos += conn.execute("SELECT COUNT(*) FROM clientes WHERE empresa_id = ?", (empresa_id,)).fetchone()[0] - antes

        vencimiento = dato["fecha_vencimiento"]
        if formato == "saldo_inicial":
            conn.execute("UPDATE clientes SET cuenta_corriente = 1 WHERE id = ?", (cliente_id,))
            if dato.get("condicion") is not None:
                conn.execute("UPDATE clientes SET condicion_pago_dias = ? WHERE id = ?", (dato["condicion"], cliente_id))
            if dato.get("telefono"):
                conn.execute(
                    """INSERT OR IGNORE INTO contacto_autorizado (empresa_id, cliente_id, telefono_e164, canal)
                       VALUES (?, ?, ?, 'whatsapp')""", (empresa_id, cliente_id, dato["telefono"]))
        elif vencimiento is None:
            condicion = conn.execute("SELECT condicion_pago_dias FROM clientes WHERE id = ?", (cliente_id,)).fetchone()[0]
            dias = condicion if condicion is not None else condicion_defecto()
            vencimiento = lectura.mas_dias(date.fromisoformat(dato["fecha_emision"]), dias).isoformat()

        conn.execute(
            """INSERT INTO documento_comercial (empresa_id, cliente_id, tipo, letra, punto_venta, numero,
                   fecha_emision, fecha_vencimiento, importe_centavos, fuente, id_externo, lote_id)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (empresa_id, cliente_id, dato["tipo"], dato.get("letra"), dato.get("punto_venta"), dato.get("numero"),
             dato["fecha_emision"], vencimiento, dato["importe"], formato, dato["id_externo"], lote_id),
        )
        creados += 1

    ahora = datetime.now().isoformat(timespec="seconds")
    conn.execute(
        """UPDATE lote_importacion SET estado = 'confirmado', confirmado_en = ?, confirmado_por = ?,
               total_informado_centavos = ?, excepciones = ? WHERE id = ?""",
        (ahora, usuario.id, informado_c, json.dumps(excepciones, ensure_ascii=False) if excepciones else None, lote_id),
    )
    resultado = {"documentos_creados": creados, "duplicados_omitidos": duplicados,
                 "clientes_nuevos": clientes_nuevos, "excepciones": excepciones}
    registrar(conn, "cartera.importacion.confirmar", entidad="lote_importacion", entidad_id=lote_id,
              despues={"formato": formato, "archivo": lote["archivo"], **resultado,
                       "total_archivo_centavos": total_archivo, "total_informado_centavos": informado_c},
              usuario=usuario)
    return resultado


# ─── Revertir ──────────────────────────────────────────────

def revertir(conn, usuario, lote_id: int, motivo: str) -> dict:
    """Anula los documentos del lote. No borra nada: queda la historia y la auditoría."""
    empresa_id = usuario.empresa_id
    if not (motivo or "").strip():
        raise ErrorImportacion("Indicá el motivo de la reversión")
    lote = conn.execute("SELECT * FROM lote_importacion WHERE id = ? AND empresa_id = ?", (lote_id, empresa_id)).fetchone()
    if not lote:
        raise LookupError("Lote no encontrado")
    if lote["estado"] != "confirmado":
        raise ErrorImportacion(f"El lote está {lote['estado']}: sólo se revierte un lote confirmado")
    con_aplicaciones = conn.execute(
        """SELECT d.id FROM documento_comercial d
           WHERE d.lote_id = ? AND d.estado = 'emitido' AND (
               (SELECT COALESCE(SUM(importe_centavos), 0) FROM aplicacion a WHERE a.documento_id = d.id) <> 0
            OR (d.tipo = 'NC' AND (SELECT COALESCE(SUM(importe_centavos), 0) FROM aplicacion a
                                   WHERE a.origen_tipo = 'nota_credito' AND a.origen_id = d.id) <> 0))""",
        (lote_id,),
    ).fetchall()
    if con_aplicaciones:
        raise ErrorImportacion("Hay documentos de este lote con aplicaciones vigentes: revertí primero esas aplicaciones")
    ids = [r["id"] for r in conn.execute("SELECT id FROM documento_comercial WHERE lote_id = ? AND estado = 'emitido'", (lote_id,))]
    conn.execute("UPDATE documento_comercial SET estado = 'anulado' WHERE lote_id = ? AND estado = 'emitido'", (lote_id,))
    conn.execute("UPDATE lote_importacion SET estado = 'revertido', revertido_en = ?, revertido_por = ? WHERE id = ?",
                 (datetime.now().isoformat(timespec="seconds"), usuario.id, lote_id))
    registrar(conn, "cartera.importacion.revertir", entidad="lote_importacion", entidad_id=lote_id,
              antes={"estado": "confirmado"}, despues={"estado": "revertido", "documentos_anulados": ids, "motivo": motivo.strip()},
              usuario=usuario)
    return {"documentos_anulados": len(ids)}
