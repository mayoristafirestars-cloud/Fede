"""
Cartera de cuentas corrientes — Rutas API.
Importes en la API: pesos (con decimales). Internamente: centavos.
"""

import csv
import io
import sys, os
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import seguridad
from copiloto import cartera, importador, lectura, operaciones
from copiloto.lectura import ErrorDato
from db.auditoria import registrar
from db.database import conectar
from dinero import a_centavos, a_pesos

router = APIRouter(prefix="/api/cartera", tags=["cartera"])

TAMANO_MAXIMO = 10 * 1024 * 1024     # 10 MB


# ─── Utilidades ────────────────────────────────────────────

def _pesos(dic: dict) -> dict:
    """Agrega la versión en pesos de cada campo *_centavos (también en tramos)."""
    salida = {}
    for k, v in dic.items():
        if k.endswith("_centavos"):
            nombre = k[: -len("_centavos")]
            if isinstance(v, dict):
                salida[nombre] = {t: a_pesos(c) for t, c in v.items()}
            else:
                salida[nombre] = a_pesos(v) if v is not None else None
        salida[k] = v
    return salida


def _importe(valor, campo="importe") -> int:
    try:
        return a_centavos(lectura.parsear_importe(valor))
    except (ErrorDato, InvalidOperation):
        raise HTTPException(status_code=400, detail=f"{campo} inválido")


def _transaccion(funcion):
    """Ejecuta funcion(conn) en una transacción y traduce los errores a HTTP."""
    conn = conectar()
    try:
        resultado = funcion(conn)
        conn.commit()
        return resultado
    except LookupError as e:
        conn.rollback()
        raise HTTPException(status_code=404, detail=str(e))
    except (importador.ErrorImportacion, operaciones.ErrorOperacion, ErrorDato) as e:
        conn.rollback()
        raise HTTPException(status_code=409, detail=str(e))
    except HTTPException:
        conn.rollback()
        raise
    finally:
        conn.close()


# ─── Consultas ─────────────────────────────────────────────

@router.get("/resumen")
def resumen(usuario=Depends(seguridad.requiere("cartera.ver"))):
    conn = conectar()
    try:
        return _pesos(cartera.resumen_cartera(conn, usuario.empresa_id))
    finally:
        conn.close()


@router.get("/clientes")
def clientes(buscar: Optional[str] = None, usuario=Depends(seguridad.requiere("cartera.ver"))):
    conn = conectar()
    try:
        return [_pesos(c) for c in cartera.resumen_clientes(conn, usuario.empresa_id, buscar=buscar)]
    finally:
        conn.close()


@router.get("/clientes/{cliente_id}")
def detalle_cliente(cliente_id: int, usuario=Depends(seguridad.requiere("cartera.ver"))):
    conn = conectar()
    try:
        d = cartera.detalle_cliente(conn, usuario.empresa_id, cliente_id)
    finally:
        conn.close()
    if not d:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    d["resumen"] = _pesos(d["resumen"])
    d["documentos"] = [_pesos(x) for x in d["documentos"]]
    d["aplicaciones"] = [_pesos(x) for x in d["aplicaciones"]]
    d["ajustes"] = [_pesos(x) for x in d["ajustes"]]
    d["cliente"] = _pesos(d["cliente"])
    return d


@router.get("/documentos")
def documentos(cliente_id: Optional[int] = None, tipo: Optional[str] = None,
               usuario=Depends(seguridad.requiere("cartera.ver"))):
    sql, params = "SELECT * FROM documento_comercial WHERE empresa_id = ?", [usuario.empresa_id]
    if cliente_id is not None:
        sql += " AND cliente_id = ?"
        params.append(cliente_id)
    if tipo:
        sql += " AND tipo = ?"
        params.append(tipo)
    conn = conectar()
    try:
        return [_pesos(dict(d)) for d in conn.execute(sql + " ORDER BY fecha_emision DESC, id DESC LIMIT 1000", params)]
    finally:
        conn.close()


# ─── Importación ───────────────────────────────────────────

@router.post("/importaciones")
async def importar_vista_previa(archivo: UploadFile = File(...), formato: str = Form(...),
                                fecha_corte: Optional[str] = Form(None),
                                usuario=Depends(seguridad.requiere("cartera.importar"))):
    contenido = await archivo.read(TAMANO_MAXIMO + 1)
    if len(contenido) > TAMANO_MAXIMO:
        raise HTTPException(status_code=413, detail="El archivo supera los 10 MB")
    if not contenido:
        raise HTTPException(status_code=400, detail="El archivo está vacío")
    corte = None
    if fecha_corte:
        try:
            corte = lectura.parsear_fecha(fecha_corte)
        except ErrorDato:
            raise HTTPException(status_code=400, detail="Fecha de corte inválida")
    return _pesos(_transaccion(lambda conn: importador.vista_previa(
        conn, usuario, formato, archivo.filename or "archivo", contenido, corte)))


@router.get("/importaciones")
def lotes(usuario=Depends(seguridad.requiere("cartera.ver"))):
    conn = conectar()
    try:
        return [dict(l) for l in conn.execute(
            """SELECT id, formato, archivo, estado, filas_ok, filas_error, filas_omitidas, total_archivo_centavos,
                      total_informado_centavos, fecha_corte, creado_en, confirmado_en, revertido_en
               FROM lote_importacion WHERE empresa_id = ? ORDER BY id DESC LIMIT 100""", (usuario.empresa_id,))]
    finally:
        conn.close()


@router.get("/importaciones/{lote_id}")
def lote(lote_id: int, usuario=Depends(seguridad.requiere("cartera.ver"))):
    return _pesos(_transaccion(lambda conn: importador.detalle_lote(conn, usuario.empresa_id, lote_id)))


class Confirmacion(BaseModel):
    total_informado: Optional[str] = None
    motivo_diferencia: Optional[str] = None


@router.post("/importaciones/{lote_id}/confirmar")
def confirmar(lote_id: int, data: Confirmacion, usuario=Depends(seguridad.requiere("cartera.importar"))):
    total = lectura.parsear_importe(data.total_informado) if data.total_informado not in (None, "") else None
    return _pesos(_transaccion(lambda conn: importador.confirmar(conn, usuario, lote_id, total, data.motivo_diferencia)))


class Motivo(BaseModel):
    motivo: str


@router.post("/importaciones/{lote_id}/revertir")
def revertir_lote(lote_id: int, data: Motivo, usuario=Depends(seguridad.requiere("cartera.importar"))):
    return _transaccion(lambda conn: importador.revertir(conn, usuario, lote_id, data.motivo))


# ─── Operaciones ───────────────────────────────────────────

class ItemAplicacion(BaseModel):
    documento_id: int
    importe: str


class NuevaAplicacion(BaseModel):
    nota_credito_id: int
    aplicaciones: list[ItemAplicacion]


@router.post("/aplicaciones")
def aplicar(data: NuevaAplicacion, usuario=Depends(seguridad.requiere("cartera.aplicar"))):
    items = [(a.documento_id, _importe(a.importe)) for a in data.aplicaciones]
    ids = _transaccion(lambda conn: operaciones.aplicar_nota_credito(conn, usuario, data.nota_credito_id, items))
    return {"ok": True, "aplicaciones": ids}


@router.post("/aplicaciones/{aplicacion_id}/revertir")
def revertir_aplicacion(aplicacion_id: int, data: Motivo, usuario=Depends(seguridad.requiere("cartera.aplicar"))):
    return {"ok": True, "reverso_id": _transaccion(lambda conn: operaciones.revertir_aplicacion(conn, usuario, aplicacion_id, data.motivo))}


class NuevoAjuste(BaseModel):
    cliente_id: int
    sentido: str
    importe: str
    motivo: str
    documento_id: Optional[int] = None
    evidencia: Optional[str] = None


@router.post("/ajustes")
def crear_ajuste(data: NuevoAjuste, usuario=Depends(seguridad.requiere("cartera.ajustar"))):
    importe = _importe(data.importe)
    ajuste_id = _transaccion(lambda conn: operaciones.crear_ajuste(
        conn, usuario, data.cliente_id, data.sentido, importe, data.motivo, data.documento_id, data.evidencia))
    return {"ok": True, "ajuste_id": ajuste_id}


@router.post("/ajustes/{ajuste_id}/revertir")
def revertir_ajuste(ajuste_id: int, data: Motivo, usuario=Depends(seguridad.requiere("cartera.ajustar"))):
    return {"ok": True, "reverso_id": _transaccion(lambda conn: operaciones.revertir_ajuste(conn, usuario, ajuste_id, data.motivo))}


class ConfigCliente(BaseModel):
    cuenta_corriente: Optional[bool] = None
    condicion_pago_dias: Optional[int] = None
    limite_informativo: Optional[str] = None
    cuit: Optional[str] = None


@router.patch("/clientes/{cliente_id}")
def configurar_cliente(cliente_id: int, data: ConfigCliente, usuario=Depends(seguridad.requiere("cartera.configurar"))):
    cambios = data.model_dump(exclude_unset=True)
    if "limite_informativo" in cambios:
        valor = cambios.pop("limite_informativo")
        cambios["limite_informativo_centavos"] = _importe(valor, "límite") if valor not in (None, "") else None
    if cambios.get("cuit"):
        try:
            cambios["cuit"] = lectura.normalizar_cuit(cambios["cuit"])
        except ErrorDato as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {"ok": True, "cambios": _transaccion(lambda conn: operaciones.configurar_cliente(conn, usuario, cliente_id, cambios))}


# ─── Exportación ───────────────────────────────────────────

@router.get("/exportar.csv")
def exportar(usuario=Depends(seguridad.requiere("cartera.exportar"))):
    """Saldos por cliente y antigüedad, para abrir con Excel (separador ;, coma decimal)."""
    conn = conectar()
    try:
        filas = cartera.resumen_clientes(conn, usuario.empresa_id)
        registrar(conn, "cartera.exportar", entidad="cartera", despues={"clientes": len(filas)}, usuario=usuario)
        conn.commit()
    finally:
        conn.close()

    def pesos(c):
        return f"{Decimal(c) / 100:.2f}".replace(".", ",")

    salida = io.StringIO()
    w = csv.writer(salida, delimiter=";")
    w.writerow(["Cliente", "CUIT", "Saldo", "Vencido", "Al día", "1-30", "31-60", "61-90", "Más de 90",
                "Créditos sin imputar", "Días de mayor atraso"])
    for c in filas:
        t = c["tramos_centavos"]
        w.writerow([c["nombre"], c["cuit"] or "", pesos(c["saldo_centavos"]), pesos(c["vencido_centavos"]),
                    pesos(t["al_dia"]), pesos(t["1_30"]), pesos(t["31_60"]), pesos(t["61_90"]), pesos(t["mas_90"]),
                    pesos(c["creditos_sin_imputar_centavos"]), c["dias_mayor_atraso"]])
    datos = ("﻿" + salida.getvalue()).encode("utf-8")
    nombre = f"cartera_{date.today().isoformat()}.csv"
    return StreamingResponse(io.BytesIO(datos), media_type="text/csv; charset=utf-8",
                             headers={"Content-Disposition": f'attachment; filename="{nombre}"'})
