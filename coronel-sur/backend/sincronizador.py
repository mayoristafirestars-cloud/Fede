"""
Sincronizador de inventario — FUENTE ÚNICA de precios y stock.

Eva (vendedor_server) y la tienda web / sistema deben mostrar SIEMPRE lo mismo.
Las dos derivan del MISMO archivo: negocio/inventario.csv (export de FactuPyme).

- Eva lo lee en vivo y se auto-refresca cuando el archivo cambia.
- La tabla `productos` (que leen la tienda y el sistema) se sincroniza acá con
  EXACTAMENTE la misma lógica de precios que Eva, cada vez que el CSV cambia.

Resultado: cuando actualizás el inventario, la web y Eva quedan en lockstep,
en vez de que la tienda muestre precios/stock viejos hasta que alguien corra
el importador a mano.
"""
import os
import csv
import re
import time
import threading
import unicodedata

from db.database import conectar

# Raíz del repo:  .../coronel-sur/backend/sincronizador.py  ->  subir 2 = coronel-sur, 3 = raíz
_BACKEND = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_BACKEND))
# Mismo archivo que lee Eva (negocio/inventario.csv en la raíz del proyecto).
CSV_PATH = os.getenv("INVENTARIO_CSV", os.path.join(_REPO, "negocio", "inventario.csv"))

_lock = threading.Lock()
_ultimo_mtime: float | None = None
_ultimo_intento = 0.0
INTERVALO_MIN = 30  # segundos: no chequear el mtime más seguido que esto


def _normalizar(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return s.lower().strip()


def _precio(s: str) -> float:
    """MISMO parser que Eva (vendedor_server.parsear_precio): la coma es
    separador de miles, el punto es decimal. Que sea idéntico garantiza que
    el precio que muestra la tienda sea el mismo que cotiza Eva."""
    s = (s or "").strip().replace("$", "").replace(" ", "").replace(",", "")
    try:
        return float(s)
    except ValueError:
        return 0.0


def _asegurar_columna(conn) -> None:
    """Agrega columnas nuevas si la DB es de una versión previa."""
    cols = [r[1] for r in conn.execute("PRAGMA table_info(productos)")]
    if "precio_mayorista" not in cols:
        conn.execute("ALTER TABLE productos ADD COLUMN precio_mayorista REAL DEFAULT 0")
    if "foto" not in cols:
        conn.execute("ALTER TABLE productos ADD COLUMN foto TEXT DEFAULT ''")


def _leer_csv() -> list[dict]:
    filas = []
    with open(CSV_PATH, encoding="latin-1", newline="") as f:
        for fila in csv.DictReader(f, delimiter=";"):
            c = {_normalizar(k): (v or "").strip() for k, v in fila.items() if k}
            cod = c.get("codigo", "").replace("Cod:", "").strip()
            m = re.search(r"\d+", cod)
            cod = m.group(0) if m else cod
            desc = c.get("descripcion", "").strip()
            if not cod or not desc:
                continue
            costo = _precio(c.get("precio costo"))
            u2 = _precio(c.get("utilidad 2"))
            # FactuPyme calcula Lista 2 = costo * (1 + U2/100) incluso con U2=0.
            lista2 = round(costo * (1 + u2 / 100), 2) if costo > 0 else 0.0
            try:
                stock = int(float(c.get("cantidad", "0") or 0))
            except ValueError:
                stock = 0
            foto = c.get("imagenes", "")
            if "product.png" in foto:  # placeholder de FactuPyme, no es foto real
                foto = ""
            filas.append({
                "codigo": cod,
                "descripcion": desc,
                "rubro": c.get("rubro", ""),
                "proveedor": c.get("provedor", "") or c.get("proveedor", ""),
                "precio_venta": _precio(c.get("precio venta")),   # Lista 1 (público)
                "precio_costo": costo,                            # interno, no se expone
                "precio_mayorista": lista2,                       # Lista 2 (interno)
                "stock": stock,
                "foto": foto,
                "fecha_ingreso": c.get("fecha modificado", ""),
            })
    return filas


def sincronizar() -> dict:
    """Vuelca el CSV a la tabla productos (upsert + baja lógica de faltantes).
    Devuelve un resumen para loguear."""
    global _ultimo_mtime
    if not os.path.exists(CSV_PATH):
        return {"ok": False, "motivo": "no se encontró el CSV", "ruta": CSV_PATH}
    with _lock:
        filas = _leer_csv()
        conn = conectar()
        try:
            _asegurar_columna(conn)
            vistos: set[str] = set()
            nuevos = actualizados = 0
            for r in filas:
                vistos.add(r["codigo"])
                ex = conn.execute(
                    "SELECT id FROM productos WHERE codigo = ?", (r["codigo"],)
                ).fetchone()
                if ex:
                    conn.execute("""
                        UPDATE productos SET
                            descripcion = ?, rubro = ?, proveedor = ?, stock = ?,
                            precio_venta = ?, precio_costo = ?, precio_mayorista = ?,
                            foto = ?, fecha_ingreso = ?, activo = 1,
                            actualizado_en = datetime('now','localtime')
                        WHERE codigo = ?""",
                        (r["descripcion"], r["rubro"], r["proveedor"], r["stock"],
                         r["precio_venta"], r["precio_costo"], r["precio_mayorista"],
                         r["foto"], r["fecha_ingreso"], r["codigo"]))
                    actualizados += 1
                else:
                    conn.execute("""
                        INSERT INTO productos
                            (codigo, descripcion, rubro, proveedor, stock,
                             precio_venta, precio_costo, precio_mayorista,
                             foto, fecha_ingreso, activo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)""",
                        (r["codigo"], r["descripcion"], r["rubro"], r["proveedor"],
                         r["stock"], r["precio_venta"], r["precio_costo"],
                         r["precio_mayorista"], r["foto"], r["fecha_ingreso"]))
                    nuevos += 1
            # Baja lógica: lo que ya no está en el CSV deja de ofrecerse (no se
            # borra, para no romper referencias históricas de comprobantes).
            bajas = 0
            if vistos:
                marcadores = ",".join("?" * len(vistos))
                bajas = conn.execute(
                    f"UPDATE productos SET activo = 0 "
                    f"WHERE codigo NOT IN ({marcadores}) AND activo = 1",
                    tuple(vistos),
                ).rowcount
            conn.commit()
        finally:
            conn.close()
        _ultimo_mtime = os.path.getmtime(CSV_PATH)
        return {"ok": True, "nuevos": nuevos, "actualizados": actualizados,
                "bajas": bajas, "total_csv": len(filas)}


def sincronizar_si_cambio() -> None:
    """Barato de llamar seguido (en cada request de la tienda): solo re-sincroniza
    si el CSV cambió desde la última vez, y como mucho una vez cada INTERVALO_MIN."""
    global _ultimo_intento
    ahora = time.time()
    if ahora - _ultimo_intento < INTERVALO_MIN:
        return
    _ultimo_intento = ahora
    try:
        if not os.path.exists(CSV_PATH):
            return
        if os.path.getmtime(CSV_PATH) != _ultimo_mtime:
            print(f"[sync inventario] {sincronizar()}")
    except Exception as e:
        print(f"[sync inventario] error: {e}")
