"""
Motor de saldos de la cartera. Código puro: no toca la base ni la red.

Todo en centavos enteros. Conceptos:
- Deudores: FC, ND, SI y ajustes débito. Su saldo baja con aplicaciones.
- Créditos: NC y ajustes crédito. Si no están aplicados a un documento,
  quedan "sin imputar" y se restan del saldo del cliente.
- "Vencido" y "parcialmente cancelado" se calculan con la fecha de corte.
- Un ajuste revertido y su reverso no cuentan (se compensan), pero quedan en la historia.
"""

from dataclasses import dataclass, field
from datetime import date

DEUDORES = ("FC", "ND", "SI")
TRAMOS = ("al_dia", "1_30", "31_60", "61_90", "mas_90")


class ErrorAplicacion(ValueError):
    pass


@dataclass
class Documento:
    id: int
    tipo: str                    # FC | ND | NC | SI
    importe: int                 # centavos, siempre positivo
    fecha_emision: date
    fecha_vencimiento: date
    anulado: bool = False


@dataclass
class Aplicacion:
    documento_id: int            # documento deudor
    origen_tipo: str             # nota_credito | ajuste
    origen_id: int
    importe: int                 # negativo si es un reverso


@dataclass
class Ajuste:
    id: int
    sentido: str                 # debito | credito
    importe: int
    fecha: date
    documento_id: int | None = None
    revierte_a: int | None = None


@dataclass
class Partida:
    """Algo que el cliente debe (documento o ajuste débito), con su saldo."""
    clave: str
    importe: int
    saldo: int
    fecha_vencimiento: date
    dias_vencido: int
    tramo: str
    estado: str


@dataclass
class Resumen:
    saldo: int = 0                       # deuda neta: partidas - créditos sin imputar
    deuda_bruta: int = 0                 # suma de saldos de partidas
    creditos_sin_imputar: int = 0
    vencido: int = 0
    tramos: dict = field(default_factory=lambda: {t: 0 for t in TRAMOS})
    partidas: list = field(default_factory=list)
    creditos: dict = field(default_factory=dict)   # clave → disponible


# ─── Funciones básicas ─────────────────────────────────────

def tramo(dias_vencido: int) -> str:
    if dias_vencido <= 0:
        return "al_dia"
    if dias_vencido <= 30:
        return "1_30"
    if dias_vencido <= 60:
        return "31_60"
    if dias_vencido <= 90:
        return "61_90"
    return "mas_90"


def estado_documento(importe: int, saldo: int, anulado: bool) -> str:
    if anulado:
        return "anulado"
    if saldo <= 0:
        return "cancelado"
    if saldo < importe:
        return "parcialmente_cancelado"
    return "emitido"


def aplicado_a(documento_id: int, aplicaciones: list[Aplicacion]) -> int:
    return sum(a.importe for a in aplicaciones if a.documento_id == documento_id)


def usado_de(origen_tipo: str, origen_id: int, aplicaciones: list[Aplicacion]) -> int:
    return sum(a.importe for a in aplicaciones if a.origen_tipo == origen_tipo and a.origen_id == origen_id)


def ajustes_efectivos(ajustes: list[Ajuste]) -> list[Ajuste]:
    """Excluye los ajustes revertidos y los reversos."""
    revertidos = {a.revierte_a for a in ajustes if a.revierte_a is not None}
    return [a for a in ajustes if a.revierte_a is None and a.id not in revertidos]


def validar_aplicacion(saldo_documento: int, disponible_origen: int, importe: int):
    """Una aplicación no puede superar el saldo del documento ni lo disponible del crédito."""
    if importe <= 0:
        raise ErrorAplicacion("El importe a aplicar debe ser mayor que cero")
    if importe > saldo_documento:
        raise ErrorAplicacion(f"El importe ({importe}) supera el saldo del documento ({saldo_documento})")
    if importe > disponible_origen:
        raise ErrorAplicacion(f"El importe ({importe}) supera lo disponible del crédito ({disponible_origen})")


# ─── Resumen de un cliente ─────────────────────────────────

def resumir(documentos: list[Documento], aplicaciones: list[Aplicacion],
            ajustes: list[Ajuste], corte: date) -> Resumen:
    r = Resumen()
    efectivos = ajustes_efectivos(ajustes)

    for d in documentos:
        if d.tipo not in DEUDORES:
            continue
        saldo = 0 if d.anulado else d.importe - aplicado_a(d.id, aplicaciones)
        dias = (corte - d.fecha_vencimiento).days
        estado = estado_documento(d.importe, saldo, d.anulado)
        r.partidas.append(Partida(f"doc:{d.id}", d.importe, saldo, d.fecha_vencimiento,
                                  dias, tramo(dias) if saldo > 0 else "al_dia", estado))

    for a in efectivos:
        if a.sentido == "debito":
            dias = (corte - a.fecha).days
            r.partidas.append(Partida(f"ajuste:{a.id}", a.importe, a.importe, a.fecha, dias, tramo(dias), "emitido"))

    for d in documentos:
        if d.tipo == "NC" and not d.anulado:
            disponible = d.importe - usado_de("nota_credito", d.id, aplicaciones)
            if disponible:
                r.creditos[f"doc:{d.id}"] = disponible
    for a in efectivos:
        if a.sentido == "credito":
            disponible = a.importe - usado_de("ajuste", a.id, aplicaciones)
            if disponible:
                r.creditos[f"ajuste:{a.id}"] = disponible

    for p in r.partidas:
        if p.saldo > 0:
            r.deuda_bruta += p.saldo
            r.tramos[p.tramo] += p.saldo
            if p.dias_vencido > 0:
                r.vencido += p.saldo
    r.creditos_sin_imputar = sum(r.creditos.values())
    r.saldo = r.deuda_bruta - r.creditos_sin_imputar
    return r
