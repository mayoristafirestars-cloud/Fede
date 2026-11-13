"""
Hito 1 — cartera de cuentas corrientes, de punta a punta por la API.
Datos inventados: CUIT válidos generados, nombres de ejemplo.
"""

import io
import sqlite3
from datetime import date, timedelta

import pytest

from conftest import crear_usuario, login
from test_lectura import cuit_valido

HOY = date.today()
CORTE = HOY - timedelta(days=40)
PEPE = cuit_valido("20", "12345678")
SOL = cuit_valido("27", "23456789")
RIO = cuit_valido("30", "71234567")
CONTADO = cuit_valido("20", "99887766")


def _f(d: date) -> str:
    return d.strftime("%d/%m/%Y")


def csv_saldo_inicial(filas=None) -> bytes:
    filas = filas or [
        ("Almacén Don Pepe", PEPE, "125.000,50", _f(CORTE - timedelta(days=60)), "", "30", "2954 123456"),
        ("Kiosco Sol", SOL, "40.000", _f(CORTE - timedelta(days=10)), "", "", ""),
        ("Librería Río", RIO, "0", _f(CORTE), "", "", ""),                       # saldo cero: se omite
        ("Sin Datos", "20-11111111-1", "1.000", _f(CORTE), "", "", ""),           # CUIT inválido
        ("Bazar Norte", "", "15.500,00", _f(CORTE - timedelta(days=95)), "", "", "02954-15-998877"),
    ]
    lineas = ["Cliente;CUIT;Saldo;Fecha;Vencimiento;Condición de pago (días);Teléfono"]
    lineas += [";".join(f) for f in filas]
    return ("\n".join(lineas) + "\n").encode("cp1252")


# total válido del archivo de arriba: 125.000,50 + 40.000 + 15.500 = 180.500,50
TOTAL_SI = "180.500,50"


def csv_arca(filas) -> bytes:
    enc = ("Fecha de Emisión;Tipo de Comprobante;Punto de Venta;Número Desde;Número Hasta;Cód. Autorización;"
           "Tipo Doc. Receptor;Nro. Doc. Receptor;Denominación Receptor;Tipo Cambio;Moneda;Imp. Neto Gravado;"
           "Imp. Neto No Gravado;Imp. Op. Exentas;IVA;Imp. Total")
    lineas = [enc]
    for fecha, tipo, pv, num, cuit, nombre, total in filas:
        lineas.append(f"{fecha};{tipo};{pv};{num};{num};7{num:013d};80;{cuit};{nombre};1;PES;0;0;0;0;{total}")
    return ("\n".join(lineas) + "\n").encode("utf-8-sig")


FILAS_ARCA = [
    (_f(CORTE + timedelta(days=5)), "1 - Factura A", 3, 101, PEPE.replace("-", ""), "ALMACEN DON PEPE", "121.000,00"),
    (_f(CORTE - timedelta(days=3)), "1 - Factura A", 3, 90, PEPE.replace("-", ""), "ALMACEN DON PEPE", "50.000,00"),   # anterior al corte
    (_f(CORTE + timedelta(days=6)), "6 - Factura B", 3, 102, CONTADO.replace("-", ""), "CLIENTE CONTADO", "9.000,00"),  # sin cta cte
    (_f(CORTE + timedelta(days=7)), "3 - Nota de Crédito A", 3, 5, PEPE.replace("-", ""), "ALMACEN DON PEPE", "20.000,00"),
    (_f(CORTE + timedelta(days=8)), "15 - Recibo C", 3, 7, PEPE.replace("-", ""), "ALMACEN DON PEPE", "1.000,00"),    # no es deuda
    (_f(CORTE + timedelta(days=9)), "6 - Factura B", 3, 103, "123", "MAL CUIT", "1.000,00"),                          # error
    (_f(CORTE + timedelta(days=10)), "6 - Factura B", 3, 104, SOL.replace("-", ""), "KIOSCO SOL", "30.000,00"),
]


def subir(c, formato, contenido, nombre="archivo.csv", fecha_corte=None):
    datos = {"formato": formato}
    if fecha_corte:
        datos["fecha_corte"] = fecha_corte.isoformat()
    return c.post("/api/cartera/importaciones", files={"archivo": (nombre, contenido, "text/csv")}, data=datos)


def importar_saldo_inicial(c):
    lote = subir(c, "saldo_inicial", csv_saldo_inicial(), fecha_corte=CORTE).json()
    r = c.post(f"/api/cartera/importaciones/{lote['id']}/confirmar", json={"total_informado": TOTAL_SI})
    assert r.status_code == 200, r.text
    return lote


def importar_arca(c, filas=FILAS_ARCA):
    lote = subir(c, "arca_emitidos", csv_arca(filas)).json()
    r = c.post(f"/api/cartera/importaciones/{lote['id']}/confirmar", json={})
    assert r.status_code == 200, r.text
    return lote


def cliente_id(c, nombre):
    return next(x["id"] for x in c.get("/api/cartera/clientes").json() if x["nombre"] == nombre)


def saldo(c, nombre):
    return c.get(f"/api/cartera/clientes/{cliente_id(c, nombre)}").json()["resumen"]["saldo"]


# ─── Saldo inicial ─────────────────────────────────────────

def test_vista_previa_valida_fila_por_fila(cliente):
    r = subir(cliente, "saldo_inicial", csv_saldo_inicial(), fecha_corte=CORTE)
    assert r.status_code == 200, r.text
    lote = r.json()
    assert lote["estado"] == "vista_previa"
    assert (lote["filas_ok"], lote["filas_error"], lote["filas_omitidas"]) == (3, 1, 1)
    assert lote["total_archivo"] == 180500.50
    assert "dígito verificador" in lote["errores"][0]["error"] and lote["errores"][0]["fila"] == 5
    assert lote["omitidas"][0]["motivo"] == "saldo cero"
    # nada se creó todavía
    assert cliente.get("/api/cartera/clientes").json() == []


def test_confirmar_exige_total_y_que_coincida(cliente):
    lote = subir(cliente, "saldo_inicial", csv_saldo_inicial(), fecha_corte=CORTE).json()
    url = f"/api/cartera/importaciones/{lote['id']}/confirmar"
    assert cliente.post(url, json={}).status_code == 409                                 # falta el total
    r = cliente.post(url, json={"total_informado": "181.500,50"})
    assert r.status_code == 409 and "Diferencia" in r.json()["detail"]                  # no coincide
    r = cliente.post(url, json={"total_informado": "181.500,50", "motivo_diferencia": "Sin Datos tiene CUIT mal: lo cargo después"})
    assert r.status_code == 200
    det = cliente.get(f"/api/cartera/importaciones/{lote['id']}").json()
    assert det["estado"] == "confirmado"
    assert det["excepciones"]["diferencia_centavos"] == 100000 and "CUIT mal" in det["excepciones"]["motivo"]


def test_saldo_inicial_crea_cartera_con_antiguedad(cliente):
    importar_saldo_inicial(cliente)
    res = cliente.get("/api/cartera/resumen").json()
    assert res["saldo"] == 180500.50
    assert res["clientes_con_saldo"] == 3
    assert res["datos_al"] == HOY.isoformat() and res["desactualizado"] is False
    # Don Pepe: fecha corte-60, condición 30 → vence corte-30 → hoy tiene 70 días de atraso
    pepe = next(x for x in cliente.get("/api/cartera/clientes").json() if x["nombre"] == "Almacén Don Pepe")
    assert pepe["tramos"]["61_90"] == 125000.50 and pepe["dias_mayor_atraso"] == 70
    assert pepe["cuit"] == PEPE.replace("-", "")
    # ordenado por vencido: el que más debe vencido primero
    assert [x["nombre"] for x in cliente.get("/api/cartera/clientes").json()][0] == "Almacén Don Pepe"


def test_telefono_queda_sin_consentimiento(cliente):
    importar_saldo_inicial(cliente)
    det = cliente.get(f"/api/cartera/clientes/{cliente_id(cliente, 'Bazar Norte')}").json()
    assert det["contactos"][0]["telefono_e164"] == "+5492954998877"
    assert det["contactos"][0]["consentimiento_fecha"] is None


# ─── Prueba 9: reimportar no duplica ───────────────────────

def test_mismo_archivo_dos_veces_se_rechaza(cliente):
    importar_saldo_inicial(cliente)
    r = subir(cliente, "saldo_inicial", csv_saldo_inicial(), fecha_corte=CORTE)
    assert r.status_code == 409 and "ya se importó" in r.json()["detail"]


def test_mismas_filas_en_otro_archivo_no_duplican(cliente):
    importar_saldo_inicial(cliente)
    otro = csv_saldo_inicial() + b"\n"                     # otro archivo (otro hash), mismas filas
    lote = subir(cliente, "saldo_inicial", otro, fecha_corte=CORTE).json()
    assert lote["filas_ok"] == 0 and all(o["motivo"] in ("ya importado antes", "saldo cero") for o in lote["omitidas"])
    assert cliente.get("/api/cartera/resumen").json()["saldo"] == 180500.50


# ─── ARCA Mis Comprobantes ─────────────────────────────────

def test_arca_toma_solo_cuenta_corriente_posterior_al_corte(cliente):
    importar_saldo_inicial(cliente)
    lote = subir(cliente, "arca_emitidos", csv_arca(FILAS_ARCA)).json()
    assert (lote["filas_ok"], lote["filas_error"], lote["filas_omitidas"]) == (3, 1, 3)
    motivos = " | ".join(o["motivo"] for o in lote["omitidas"])
    assert "anterior o igual a la fecha de corte" in motivos
    assert "sin cuenta corriente" in motivos and "no genera deuda" in motivos
    cliente.post(f"/api/cartera/importaciones/{lote['id']}/confirmar", json={})
    # Pepe: 125.000,50 + 121.000 − 20.000 (NC sin imputar)
    det = cliente.get(f"/api/cartera/clientes/{cliente_id(cliente, 'Almacén Don Pepe')}").json()
    assert det["resumen"]["saldo"] == 226000.50 and det["resumen"]["creditos_sin_imputar"] == 20000.0
    fc = next(d for d in det["documentos"] if d["tipo"] == "FC")
    assert (fc["letra"], fc["punto_venta"], fc["numero"]) == ("A", 3, 101)
    assert fc["fecha_vencimiento"] == (CORTE + timedelta(days=35)).isoformat()   # emisión + 30 días
    assert saldo(cliente, "Kiosco Sol") == 70000.0


def test_arca_desde_excel_con_titulo(cliente):
    from openpyxl import Workbook
    importar_saldo_inicial(cliente)
    libro = Workbook()
    hoja = libro.active
    hoja.append(["Mis Comprobantes Emitidos - CUIT 30-00000000-0"])
    hoja.append(["Fecha de Emisión", "Tipo de Comprobante", "Punto de Venta", "Número Desde", "Nro. Doc. Receptor",
                 "Denominación Receptor", "Moneda", "Imp. Total"])
    hoja.append([CORTE + timedelta(days=3), "6 - Factura B", 4, 1, int(SOL.replace("-", "")), "KIOSCO SOL", "$", 12345.67])
    buf = io.BytesIO()
    libro.save(buf)
    lote = subir(cliente, "arca_emitidos", buf.getvalue(), nombre="emitidos.xlsx").json()
    assert lote["filas_ok"] == 1, lote
    cliente.post(f"/api/cartera/importaciones/{lote['id']}/confirmar", json={})
    assert saldo(cliente, "Kiosco Sol") == 52345.67


# ─── Prueba 14: NC aplicada a dos documentos ───────────────

def test_nota_de_credito_aplicada_a_dos_documentos(cliente):
    importar_saldo_inicial(cliente)
    importar_arca(cliente, FILAS_ARCA + [(_f(CORTE + timedelta(days=11)), "3 - Nota de Crédito A", 3, 6,
                                          PEPE.replace("-", ""), "ALMACEN DON PEPE", "150.000,00")])
    cid = cliente_id(cliente, "Almacén Don Pepe")
    det = cliente.get(f"/api/cartera/clientes/{cid}").json()
    si = next(d for d in det["documentos"] if d["tipo"] == "SI")
    fc = next(d for d in det["documentos"] if d["tipo"] == "FC")
    nc = next(d for d in det["documentos"] if d["tipo"] == "NC" and d["importe"] == 150000.0)
    antes = det["resumen"]["saldo"]

    excede = cliente.post("/api/cartera/aplicaciones", json={"nota_credito_id": nc["id"], "aplicaciones": [
        {"documento_id": si["id"], "importe": "125.000,50"}, {"documento_id": fc["id"], "importe": "30.000"}]})
    assert excede.status_code == 409                                      # 155.000,50 > 150.000 disponibles

    r = cliente.post("/api/cartera/aplicaciones", json={"nota_credito_id": nc["id"], "aplicaciones": [
        {"documento_id": si["id"], "importe": "125.000,50"}, {"documento_id": fc["id"], "importe": "24.999,50"}]})
    assert r.status_code == 200, r.text
    det = cliente.get(f"/api/cartera/clientes/{cid}").json()
    docs = {d["id"]: d for d in det["documentos"]}
    assert docs[si["id"]]["estado"] == "cancelado" and docs[si["id"]]["saldo"] == 0
    assert docs[fc["id"]]["estado"] == "parcialmente_cancelado" and docs[fc["id"]]["saldo"] == 96000.50
    assert docs[nc["id"]]["estado"] == "aplicada"
    assert det["resumen"]["saldo"] == antes                                # aplicar no cambia el saldo neto


# ─── Prueba 13: revertir ajuste y lote conserva la historia ─

def test_ajuste_y_su_reverso(cliente):
    importar_saldo_inicial(cliente)
    cid = cliente_id(cliente, "Kiosco Sol")
    r = cliente.post("/api/cartera/ajustes", json={"cliente_id": cid, "sentido": "credito", "importe": "5.000",
                                                     "motivo": "Bonificación acordada"})
    assert r.status_code == 200
    assert saldo(cliente, "Kiosco Sol") == 35000.0
    rev = cliente.post(f"/api/cartera/ajustes/{r.json()['ajuste_id']}/revertir", json={"motivo": "Se cargó por error"})
    assert rev.status_code == 200
    assert saldo(cliente, "Kiosco Sol") == 40000.0
    ajustes = cliente.get(f"/api/cartera/clientes/{cid}").json()["ajustes"]
    assert len(ajustes) == 2 and ajustes[1]["revierte_a"] == ajustes[0]["id"]           # historia completa
    assert cliente.post(f"/api/cartera/ajustes/{ajustes[0]['id']}/revertir", json={"motivo": "otra vez"}).status_code == 409


def test_ajuste_aplicado_a_documento_y_reverso(cliente):
    importar_saldo_inicial(cliente)
    cid = cliente_id(cliente, "Kiosco Sol")
    doc = cliente.get(f"/api/cartera/clientes/{cid}").json()["documentos"][0]
    r = cliente.post("/api/cartera/ajustes", json={"cliente_id": cid, "sentido": "credito", "importe": "40.000",
                                                     "motivo": "Devolución de mercadería", "documento_id": doc["id"]})
    det = cliente.get(f"/api/cartera/clientes/{cid}").json()
    assert det["documentos"][0]["estado"] == "cancelado" and det["resumen"]["saldo"] == 0
    cliente.post(f"/api/cartera/ajustes/{r.json()['ajuste_id']}/revertir", json={"motivo": "No correspondía"})
    det = cliente.get(f"/api/cartera/clientes/{cid}").json()
    assert det["documentos"][0]["estado"] == "emitido" and det["resumen"]["saldo"] == 40000.0


def test_revertir_lote(cliente):
    importar_saldo_inicial(cliente)
    lote_arca = importar_arca(cliente)
    cid = cliente_id(cliente, "Almacén Don Pepe")
    det = cliente.get(f"/api/cartera/clientes/{cid}").json()
    nc = next(d for d in det["documentos"] if d["tipo"] == "NC")
    fc = next(d for d in det["documentos"] if d["tipo"] == "FC")
    ap = cliente.post("/api/cartera/aplicaciones", json={"nota_credito_id": nc["id"], "aplicaciones": [
        {"documento_id": fc["id"], "importe": "20.000"}]}).json()["aplicaciones"][0]

    url = f"/api/cartera/importaciones/{lote_arca['id']}/revertir"
    r = cliente.post(url, json={"motivo": "Archivo de otro mes"})
    assert r.status_code == 409 and "aplicaciones vigentes" in r.json()["detail"]
    cliente.post(f"/api/cartera/aplicaciones/{ap}/revertir", json={"motivo": "Para revertir el lote"})
    r = cliente.post(url, json={"motivo": "Archivo de otro mes"})
    assert r.status_code == 200 and r.json()["documentos_anulados"] == 3       # FC Pepe, NC Pepe, FC Sol
    assert saldo(cliente, "Almacén Don Pepe") == 125000.50                             # volvió al saldo inicial
    docs = cliente.get(f"/api/cartera/clientes/{cid}").json()["documentos"]
    assert sum(1 for d in docs if d["estado"] == "anulado") == 2                          # siguen en la historia
    assert cliente.post(url, json={"motivo": "de nuevo"}).status_code == 409


# ─── Prueba 11: aislamiento entre empresas ─────────────────

def test_otra_empresa_no_ve_nada(cliente, db_temporal):
    lote = importar_saldo_inicial(cliente)
    cid = cliente_id(cliente, "Kiosco Sol")
    conn = sqlite3.connect(db_temporal)
    conn.execute("INSERT INTO empresa (id, razon_social) VALUES (2, 'Otra Distribuidora')")
    conn.commit()
    conn.close()
    from fastapi.testclient import TestClient
    from main import app
    with TestClient(app) as otro:
        crear_usuario("ajeno", {"admin"}, empresa_id=2)
        login(otro, "ajeno")
        assert otro.get(f"/api/cartera/clientes/{cid}").status_code == 404
        assert otro.get(f"/api/cartera/importaciones/{lote['id']}").status_code == 404
        assert otro.get("/api/cartera/clientes").json() == []
        assert otro.get("/api/cartera/resumen").json()["saldo"] == 0
        r = otro.post("/api/cartera/ajustes", json={"cliente_id": cid, "sentido": "credito", "importe": "1", "motivo": "x"})
        assert r.status_code == 404
        assert otro.post(f"/api/cartera/importaciones/{lote['id']}/revertir", json={"motivo": "x"}).status_code == 404


# ─── Prueba 15: restaurar y reimportar ─────────────────────

def test_restaurar_y_reimportar_no_duplica(cliente):
    from db import respaldos
    importar_saldo_inicial(cliente)
    copia = respaldos.respaldar(motivo="prueba")
    importar_arca(cliente)
    saldo_final = cliente.get("/api/cartera/resumen").json()["saldo"]
    respaldos.restaurar(copia)
    assert cliente.get("/api/cartera/resumen").json()["saldo"] == 180500.50
    importar_arca(cliente)                                    # se vuelve a cargar lo posterior al respaldo
    assert cliente.get("/api/cartera/resumen").json()["saldo"] == saldo_final
    lote = subir(cliente, "arca_emitidos", csv_arca(FILAS_ARCA) + b"\n").json()
    assert lote["filas_ok"] == 0                              # y no se duplica


# ─── Prueba 8: datos desactualizados ───────────────────────

def test_datos_desactualizados(cliente, db_temporal):
    assert cliente.get("/api/cartera/resumen").json()["desactualizado"] is True       # nunca se importó
    importar_saldo_inicial(cliente)
    conn = sqlite3.connect(db_temporal)
    conn.execute("UPDATE lote_importacion SET confirmado_en = ?", ((HOY - timedelta(days=5)).isoformat() + "T10:00:00",))
    conn.commit()
    conn.close()
    res = cliente.get("/api/cartera/resumen").json()
    assert res["desactualizado"] is True and "5 días" in res["aviso"]
    assert cliente.get(f"/api/cartera/clientes/{cliente_id(cliente, 'Kiosco Sol')}").json()["desactualizado"] is True


# ─── Configuración del cliente y exportación ───────────────

def test_configurar_cliente(cliente):
    importar_saldo_inicial(cliente)
    cid = cliente_id(cliente, "Bazar Norte")
    r = cliente.patch(f"/api/cartera/clientes/{cid}", json={"condicion_pago_dias": 15, "cuit": RIO, "limite_informativo": "200.000"})
    assert r.status_code == 200, r.text
    det = cliente.get(f"/api/cartera/clientes/{cid}").json()["cliente"]
    assert (det["condicion_pago_dias"], det["cuit"], det["limite_informativo"]) == (15, RIO.replace("-", ""), 200000.0)
    assert cliente.patch(f"/api/cartera/clientes/{cid}", json={"cuit": "20-12345678-5"}).status_code == 400


def test_exportar_csv(cliente):
    importar_saldo_inicial(cliente)
    r = cliente.get("/api/cartera/exportar.csv")
    assert r.status_code == 200 and "attachment" in r.headers["content-disposition"]
    texto = r.content.decode("utf-8-sig")
    assert texto.splitlines()[0].startswith("Cliente;CUIT;Saldo;Vencido")
    assert "Almacén Don Pepe;" in texto and "125000,50" in texto


# ─── Permisos ──────────────────────────────────────────────

@pytest.mark.parametrize("rol,importa,ajusta,exporta", [
    ("admin", True, True, True),
    ("responsable_cobranza", True, False, False),
    ("cobrador", False, False, False),
    ("consulta", False, False, False),
])
def test_permisos_de_cartera(cliente_anonimo, rol, importa, ajusta, exporta):
    crear_usuario("jefe", {"admin"})
    login(cliente_anonimo, "jefe")
    importar_saldo_inicial(cliente_anonimo)
    cid = cliente_id(cliente_anonimo, "Kiosco Sol")
    cliente_anonimo.post("/api/auth/logout")

    crear_usuario("persona", {rol})
    login(cliente_anonimo, "persona")
    assert cliente_anonimo.get("/api/cartera/resumen").status_code == 200                  # todos ven
    assert cliente_anonimo.get(f"/api/cartera/clientes/{cid}").status_code == 200
    r = subir(cliente_anonimo, "arca_emitidos", csv_arca(FILAS_ARCA))
    assert (r.status_code == 200) == importa
    r = cliente_anonimo.post("/api/cartera/ajustes", json={"cliente_id": cid, "sentido": "credito", "importe": "1", "motivo": "x"})
    assert (r.status_code == 200) == ajusta
    assert (cliente_anonimo.get("/api/cartera/exportar.csv").status_code == 200) == exporta


def test_sin_sesion_401(cliente_anonimo):
    assert cliente_anonimo.get("/api/cartera/resumen").status_code == 401


def test_operaciones_quedan_auditadas(cliente, db_temporal):
    importar_saldo_inicial(cliente)
    cid = cliente_id(cliente, "Kiosco Sol")
    cliente.post("/api/cartera/ajustes", json={"cliente_id": cid, "sentido": "debito", "importe": "100", "motivo": "Flete"})
    conn = sqlite3.connect(db_temporal)
    acciones = [r[0] for r in conn.execute("SELECT accion FROM evento_auditoria WHERE accion LIKE 'cartera.%' ORDER BY id")]
    conn.close()
    assert acciones == ["cartera.importacion.confirmar", "cartera.ajuste.crear"]
