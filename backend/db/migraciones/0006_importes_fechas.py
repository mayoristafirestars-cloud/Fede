"""
0006: importes en centavos enteros y fechas en ISO (YYYY-MM-DD).

- Agrega columnas *_centavos sin borrar las REAL viejas (se siguen escribiendo
  mientras haya código que las lea).
- Convierte con Decimal y ROUND_HALF_EVEN (redondeo bancario).
- comprobantes.fecha pasa de dd-mm-aaaa a ISO; el texto anterior queda en fecha_original.
  Una fecha ilegible no se toca: se informa como problema.
- Genera un reporte JSON en la carpeta de respaldos. Si los totales no cierran,
  lanza un error y la migración entera se deshace.
- Se puede volver a ejecutar sin efecto: sólo convierte lo que falta.

Es autocontenida a propósito: no depende de código de la app que pueda cambiar.
"""

import json
import os
import re
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_EVEN

CENTAVO = Decimal("0.01")
FECHA_DMA = re.compile(r"^(\d{2})-(\d{2})-(\d{4})$")
FECHA_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")

COLUMNAS = {
    "comprobantes": [("subtotal_centavos", "INTEGER"), ("total_centavos", "INTEGER"), ("fecha_original", "TEXT")],
    "comprobante_items": [("precio_unitario_centavos", "INTEGER"), ("precio_costo_centavos", "INTEGER"), ("subtotal_centavos", "INTEGER")],
}


def a_centavos(valor) -> int | None:
    """Pesos (float o texto) a centavos enteros, con redondeo bancario."""
    if valor is None:
        return None
    return int(Decimal(str(valor)).quantize(CENTAVO, rounding=ROUND_HALF_EVEN) * 100)


def _necesito_redondear(valor) -> bool:
    return valor is not None and Decimal(str(valor)) != Decimal(str(valor)).quantize(CENTAVO)


def fecha_a_iso(texto: str) -> str | None:
    """dd-mm-aaaa válido → aaaa-mm-dd. Ya ISO válido → igual. Otro caso → None."""
    if texto is None:
        return None
    texto = texto.strip()
    if FECHA_ISO.match(texto):
        try:
            return date.fromisoformat(texto).isoformat()
        except ValueError:
            return None
    m = FECHA_DMA.match(texto)
    if not m:
        return None
    try:
        return date(int(m.group(3)), int(m.group(2)), int(m.group(1))).isoformat()
    except ValueError:
        return None


def verificar_totales(suma_pesos: Decimal, suma_centavos: int, filas_redondeadas: int):
    """
    La suma en centavos debe coincidir con la suma original al centavo.
    Sólo se admite la diferencia que explica el redondeo de filas con más de 2 decimales
    (como máximo medio centavo por fila redondeada).
    """
    diferencia = abs(suma_pesos - Decimal(suma_centavos) / 100)
    tolerancia = CENTAVO / 2 * filas_redondeadas
    if diferencia > tolerancia:
        raise ValueError(
            f"Los totales no cierran: antes {suma_pesos}, después {Decimal(suma_centavos) / 100} "
            f"(diferencia {diferencia}, tolerancia {tolerancia}). La migración se deshace."
        )
    return diferencia


def _agregar_columnas(conn):
    for tabla, columnas in COLUMNAS.items():
        existentes = {f[1] for f in conn.execute(f"PRAGMA table_info({tabla})")}
        for nombre, tipo in columnas:
            if nombre not in existentes:
                conn.execute(f"ALTER TABLE {tabla} ADD COLUMN {nombre} {tipo}")


def _dir_reportes() -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # backend/db
    return os.environ.get("BACKUP_DIR", os.path.join(base, "respaldos"))


def _guardar_reporte(reporte: dict) -> str:
    os.makedirs(_dir_reportes(), exist_ok=True)
    ruta = os.path.join(_dir_reportes(), f"reporte_migracion_0006_{datetime.now():%Y%m%d_%H%M%S_%f}.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)
    return ruta


def migrar(conn):
    _agregar_columnas(conn)
    problemas = []
    reporte = {"migracion": "0006_importes_fechas", "momento": datetime.now().isoformat(timespec="seconds")}

    # ── Comprobantes: importes ──
    comprobantes = conn.execute(
        "SELECT id, numero, subtotal, total FROM comprobantes WHERE total_centavos IS NULL"
    ).fetchall()
    suma_antes, redondeadas = Decimal("0"), 0
    for cid, numero, subtotal, total in comprobantes:
        if total is None:
            problemas.append({"tabla": "comprobantes", "id": cid, "numero": numero, "problema": "total vacío"})
            continue
        if total < 0:
            problemas.append({"tabla": "comprobantes", "id": cid, "numero": numero, "problema": f"total negativo ({total})"})
        suma_antes += Decimal(str(total))
        redondeadas += _necesito_redondear(total)
        conn.execute(
            "UPDATE comprobantes SET subtotal_centavos = ?, total_centavos = ? WHERE id = ?",
            (a_centavos(subtotal), a_centavos(total), cid),
        )
    ids = [c[0] for c in comprobantes if c[3] is not None]
    suma_despues = 0
    if ids:
        marcas = ",".join("?" * len(ids))
        suma_despues = conn.execute(f"SELECT COALESCE(SUM(total_centavos), 0) FROM comprobantes WHERE id IN ({marcas})", ids).fetchone()[0]

    # ── Ítems: importes ──
    items = conn.execute(
        "SELECT id, comprobante_id, precio_unitario, precio_costo, subtotal FROM comprobante_items WHERE subtotal_centavos IS NULL"
    ).fetchall()
    suma_items_antes, redondeados_items = Decimal("0"), 0
    for iid, cid, precio, costo, subtotal in items:
        if subtotal is None:
            problemas.append({"tabla": "comprobante_items", "id": iid, "comprobante_id": cid, "problema": "subtotal vacío"})
            continue
        suma_items_antes += Decimal(str(subtotal))
        redondeados_items += _necesito_redondear(subtotal)
        conn.execute(
            "UPDATE comprobante_items SET precio_unitario_centavos = ?, precio_costo_centavos = ?, subtotal_centavos = ? WHERE id = ?",
            (a_centavos(precio), a_centavos(costo), a_centavos(subtotal), iid),
        )
    suma_items_despues = sum(a_centavos(i[4]) for i in items if i[4] is not None)

    # ── Fechas ──
    fechas = conn.execute("SELECT id, numero, fecha FROM comprobantes WHERE fecha_original IS NULL").fetchall()
    fechas_convertidas = 0
    for cid, numero, fecha in fechas:
        iso = fecha_a_iso(fecha)
        if iso is None:
            problemas.append({"tabla": "comprobantes", "id": cid, "numero": numero, "problema": f"fecha ilegible ({fecha!r}): no se modificó"})
            conn.execute("UPDATE comprobantes SET fecha_original = fecha WHERE id = ?", (cid,))
            continue
        conn.execute("UPDATE comprobantes SET fecha_original = fecha, fecha = ? WHERE id = ?", (iso, cid))
        fechas_convertidas += iso != fecha

    # ── Diferencias que ya existían: suma de ítems contra subtotal del comprobante ──
    diferencias = conn.execute("""
        SELECT c.id, c.numero, c.subtotal_centavos, COALESCE(SUM(i.subtotal_centavos), 0) AS items
        FROM comprobantes c LEFT JOIN comprobante_items i ON i.comprobante_id = c.id
        GROUP BY c.id HAVING c.subtotal_centavos IS NOT NULL AND c.subtotal_centavos != items
    """).fetchall()
    for cid, numero, sub, suma_items in diferencias:
        problemas.append({"tabla": "comprobantes", "id": cid, "numero": numero,
                          "problema": f"la suma de ítems ({suma_items / 100:.2f}) no coincide con el subtotal ({sub / 100:.2f}); ya venía así"})

    reporte.update({
        "comprobantes_migrados": len(comprobantes),
        "items_migrados": len(items),
        "fechas_revisadas": len(fechas),
        "fechas_convertidas": fechas_convertidas,
        "total_antes_pesos": str(suma_antes),
        "total_despues_pesos": str(Decimal(suma_despues) / 100),
        "comprobantes_con_mas_de_2_decimales": redondeadas,
        "items_total_antes_pesos": str(suma_items_antes),
        "items_total_despues_pesos": str(Decimal(suma_items_despues) / 100),
        "problemas": problemas,
    })

    try:
        reporte["diferencia_total"] = str(verificar_totales(suma_antes, suma_despues, redondeadas))
        reporte["diferencia_items"] = str(verificar_totales(suma_items_antes, suma_items_despues, redondeados_items))
        reporte["resultado"] = "aplicada"
    except ValueError as e:
        reporte["resultado"] = f"deshecha: {e}"
        print(f"📄 Reporte de la migración 0006: {_guardar_reporte(reporte)}")
        raise

    ruta = _guardar_reporte(reporte)
    print(f"📄 Reporte de la migración 0006: {ruta}")
    print(f"   Comprobantes: {len(comprobantes)} · Ítems: {len(items)} · Fechas convertidas: {fechas_convertidas} · Problemas: {len(problemas)}")
    print(f"   Total antes: $ {suma_antes} · después: $ {Decimal(suma_despues) / 100}")
