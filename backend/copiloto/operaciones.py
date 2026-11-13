"""
Operaciones sobre la cartera hechas por una persona autorizada.
Nada se borra: las correcciones son reversos vinculados. Todo queda en la auditoría.
"""

from datetime import date

from copiloto import motor
from copiloto.motor import ErrorAplicacion
from db.auditoria import registrar


class ErrorOperacion(ValueError):
    pass


def _documento(conn, empresa_id, documento_id):
    d = conn.execute("SELECT * FROM documento_comercial WHERE id = ? AND empresa_id = ?", (documento_id, empresa_id)).fetchone()
    if not d:
        raise LookupError("Documento no encontrado")
    return d


def _saldo_documento(conn, documento) -> int:
    if documento["estado"] == "anulado":
        return 0
    aplicado = conn.execute("SELECT COALESCE(SUM(importe_centavos), 0) FROM aplicacion WHERE documento_id = ?",
                            (documento["id"],)).fetchone()[0]
    return documento["importe_centavos"] - aplicado


def _disponible(conn, origen_tipo: str, origen_id: int, importe: int) -> int:
    usado = conn.execute("SELECT COALESCE(SUM(importe_centavos), 0) FROM aplicacion WHERE origen_tipo = ? AND origen_id = ?",
                         (origen_tipo, origen_id)).fetchone()[0]
    return importe - usado


# ─── Aplicar una nota de crédito a uno o varios documentos ─

def aplicar_nota_credito(conn, usuario, nota_credito_id: int, aplicaciones: list[tuple[int, int]]) -> list[int]:
    """aplicaciones: [(documento_id, importe_centavos)]. Todo o nada."""
    nc = _documento(conn, usuario.empresa_id, nota_credito_id)
    if nc["tipo"] != "NC" or nc["estado"] == "anulado":
        raise ErrorOperacion("El origen tiene que ser una nota de crédito vigente")
    if not aplicaciones:
        raise ErrorOperacion("No hay documentos para aplicar")
    disponible = _disponible(conn, "nota_credito", nc["id"], nc["importe_centavos"])
    ids = []
    for documento_id, importe in aplicaciones:
        doc = _documento(conn, usuario.empresa_id, documento_id)
        if doc["cliente_id"] != nc["cliente_id"]:
            raise ErrorOperacion("La nota de crédito y el documento son de clientes distintos")
        if doc["tipo"] not in motor.DEUDORES or doc["estado"] == "anulado":
            raise ErrorOperacion(f"El documento {documento_id} no es una deuda vigente")
        try:
            motor.validar_aplicacion(_saldo_documento(conn, doc), disponible, importe)
        except ErrorAplicacion as e:
            raise ErrorOperacion(str(e))
        cur = conn.execute(
            """INSERT INTO aplicacion (empresa_id, documento_id, origen_tipo, origen_id, importe_centavos, fecha, aprobado_por)
               VALUES (?, ?, 'nota_credito', ?, ?, ?, ?)""",
            (usuario.empresa_id, documento_id, nc["id"], importe, date.today().isoformat(), usuario.id))
        disponible -= importe
        ids.append(cur.lastrowid)
    registrar(conn, "cartera.aplicacion.crear", entidad="documento_comercial", entidad_id=nc["id"],
              despues={"aplicaciones": [{"id": i, "documento_id": d, "importe_centavos": m} for i, (d, m) in zip(ids, aplicaciones)]},
              usuario=usuario)
    return ids


def revertir_aplicacion(conn, usuario, aplicacion_id: int, motivo: str) -> int:
    if not (motivo or "").strip():
        raise ErrorOperacion("Indicá el motivo de la reversión")
    a = conn.execute("SELECT * FROM aplicacion WHERE id = ? AND empresa_id = ?", (aplicacion_id, usuario.empresa_id)).fetchone()
    if not a:
        raise LookupError("Aplicación no encontrada")
    if a["revierte_a"] is not None or a["importe_centavos"] < 0:
        raise ErrorOperacion("Un reverso no se revierte")
    if conn.execute("SELECT 1 FROM aplicacion WHERE revierte_a = ?", (aplicacion_id,)).fetchone():
        raise ErrorOperacion("La aplicación ya fue revertida")
    cur = conn.execute(
        """INSERT INTO aplicacion (empresa_id, documento_id, origen_tipo, origen_id, importe_centavos, fecha, aprobado_por, revierte_a)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (usuario.empresa_id, a["documento_id"], a["origen_tipo"], a["origen_id"], -a["importe_centavos"],
         date.today().isoformat(), usuario.id, aplicacion_id))
    registrar(conn, "cartera.aplicacion.revertir", entidad="aplicacion", entidad_id=aplicacion_id,
              despues={"reverso_id": cur.lastrowid, "motivo": motivo.strip()}, usuario=usuario)
    return cur.lastrowid


# ─── Ajustes ───────────────────────────────────────────────

def crear_ajuste(conn, usuario, cliente_id: int, sentido: str, importe: int, motivo: str,
                 documento_id: int | None = None, evidencia: str | None = None) -> int:
    if sentido not in ("debito", "credito"):
        raise ErrorOperacion("El sentido tiene que ser débito o crédito")
    if importe <= 0:
        raise ErrorOperacion("El importe tiene que ser mayor que cero")
    if not (motivo or "").strip():
        raise ErrorOperacion("El motivo es obligatorio")
    if not conn.execute("SELECT 1 FROM clientes WHERE id = ? AND empresa_id = ?", (cliente_id, usuario.empresa_id)).fetchone():
        raise LookupError("Cliente no encontrado")
    if documento_id is not None:
        if sentido != "credito":
            raise ErrorOperacion("Sólo un ajuste crédito se aplica a un documento")
        doc = _documento(conn, usuario.empresa_id, documento_id)
        if doc["cliente_id"] != cliente_id or doc["tipo"] not in motor.DEUDORES:
            raise ErrorOperacion("El documento no es una deuda de este cliente")
        try:
            motor.validar_aplicacion(_saldo_documento(conn, doc), importe, importe)
        except ErrorAplicacion as e:
            raise ErrorOperacion(str(e))
    cur = conn.execute(
        """INSERT INTO ajuste (empresa_id, cliente_id, documento_id, sentido, importe_centavos, motivo, evidencia, aprobado_por)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (usuario.empresa_id, cliente_id, documento_id, sentido, importe, motivo.strip(), evidencia, usuario.id))
    ajuste_id = cur.lastrowid
    if documento_id is not None:
        conn.execute(
            """INSERT INTO aplicacion (empresa_id, documento_id, origen_tipo, origen_id, importe_centavos, fecha, aprobado_por)
               VALUES (?, ?, 'ajuste', ?, ?, ?, ?)""",
            (usuario.empresa_id, documento_id, ajuste_id, importe, date.today().isoformat(), usuario.id))
    registrar(conn, "cartera.ajuste.crear", entidad="ajuste", entidad_id=ajuste_id,
              despues={"cliente_id": cliente_id, "sentido": sentido, "importe_centavos": importe,
                       "documento_id": documento_id, "motivo": motivo.strip()}, usuario=usuario)
    return ajuste_id


def revertir_ajuste(conn, usuario, ajuste_id: int, motivo: str) -> int:
    if not (motivo or "").strip():
        raise ErrorOperacion("Indicá el motivo de la reversión")
    a = conn.execute("SELECT * FROM ajuste WHERE id = ? AND empresa_id = ?", (ajuste_id, usuario.empresa_id)).fetchone()
    if not a:
        raise LookupError("Ajuste no encontrado")
    if a["revierte_a"] is not None:
        raise ErrorOperacion("Un reverso no se revierte")
    if conn.execute("SELECT 1 FROM ajuste WHERE revierte_a = ?", (ajuste_id,)).fetchone():
        raise ErrorOperacion("El ajuste ya fue revertido")
    cur = conn.execute(
        """INSERT INTO ajuste (empresa_id, cliente_id, documento_id, sentido, importe_centavos, motivo, aprobado_por, revierte_a)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (usuario.empresa_id, a["cliente_id"], a["documento_id"], a["sentido"], a["importe_centavos"],
         f"Reverso: {motivo.strip()}", usuario.id, ajuste_id))
    for ap in conn.execute("SELECT * FROM aplicacion WHERE origen_tipo = 'ajuste' AND origen_id = ? AND revierte_a IS NULL AND importe_centavos > 0",
                           (ajuste_id,)).fetchall():
        conn.execute(
            """INSERT INTO aplicacion (empresa_id, documento_id, origen_tipo, origen_id, importe_centavos, fecha, aprobado_por, revierte_a)
               VALUES (?, ?, 'ajuste', ?, ?, ?, ?, ?)""",
            (usuario.empresa_id, ap["documento_id"], ajuste_id, -ap["importe_centavos"], date.today().isoformat(), usuario.id, ap["id"]))
    registrar(conn, "cartera.ajuste.revertir", entidad="ajuste", entidad_id=ajuste_id,
              despues={"reverso_id": cur.lastrowid, "motivo": motivo.strip()}, usuario=usuario)
    return cur.lastrowid


# ─── Datos de cuenta corriente del cliente ─────────────────

def configurar_cliente(conn, usuario, cliente_id: int, cambios: dict) -> dict:
    permitidos = {"cuenta_corriente", "condicion_pago_dias", "limite_informativo_centavos", "cuit"}
    cambios = {k: v for k, v in cambios.items() if k in permitidos}
    c = conn.execute("SELECT * FROM clientes WHERE id = ? AND empresa_id = ?", (cliente_id, usuario.empresa_id)).fetchone()
    if not c:
        raise LookupError("Cliente no encontrado")
    if "condicion_pago_dias" in cambios and cambios["condicion_pago_dias"] is not None and not 0 <= cambios["condicion_pago_dias"] <= 365:
        raise ErrorOperacion("La condición de pago va de 0 a 365 días")
    if "cuenta_corriente" in cambios:
        cambios["cuenta_corriente"] = 1 if cambios["cuenta_corriente"] else 0
    antes = {k: c[k] for k in cambios}
    for k, v in cambios.items():
        conn.execute(f"UPDATE clientes SET {k} = ? WHERE id = ?", (v, cliente_id))
    registrar(conn, "cartera.cliente.configurar", entidad="cliente", entidad_id=cliente_id,
              antes=antes, despues=cambios, usuario=usuario)
    return cambios
