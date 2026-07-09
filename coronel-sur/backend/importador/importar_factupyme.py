"""
Importador de CSVs de FactuPyme → Coronel Sur DB

Archivos esperados en data/csv_originales/:
  - inventario.csv    (productos y stock)
  - ventas.csv        (facturas)
  - presupuestos.csv  (presupuestos)

Formato FactuPyme: latin-1, separador punto y coma (;)
"""

import csv
import os
import sys
import re

# Agregar el directorio padre al path para importar database
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar, inicializar_db

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data", "csv_originales"
)


# ─────────────────────────────────────────────
# UTILIDADES DE PARSEO
# ─────────────────────────────────────────────

def parsear_numero(valor: str) -> float:
    """
    Parsea números de FactuPyme con cuidado:
    - Punto con 3 dígitos después → separador de miles → se elimina
    - Punto con 1 o 2 dígitos después → decimal → se respeta
    Ejemplos: "10.000" → 10000.0 | "1999.5" → 1999.5 | "1.234.567" → 1234567.0
    """
    if not valor or valor.strip() == "":
        return 0.0
    v = valor.strip().replace(" ", "")
    # Si hay coma, es separador decimal estilo europeo → reemplazar por punto
    v = v.replace(",", ".")
    # Múltiples puntos → todos menos el último son miles
    partes = v.split(".")
    if len(partes) > 2:
        v = "".join(partes[:-1]) + "." + partes[-1]
    elif len(partes) == 2 and len(partes[1]) == 3:
        # Punto con exactamente 3 dígitos → separador de miles
        v = "".join(partes)
    try:
        return float(v)
    except ValueError:
        return 0.0


def parsear_codigo(valor: str) -> str:
    """
    Extrae solo el número del código de FactuPyme.
    Ejemplo: "Cod: 12345" → "12345"
    """
    if not valor:
        return ""
    match = re.search(r'\d+', valor)
    return match.group(0) if match else valor.strip()


def leer_csv(ruta: str) -> list[dict]:
    """Lee un CSV de FactuPyme (latin-1, punto y coma)."""
    if not os.path.exists(ruta):
        print(f"⚠️  No se encontró: {ruta}")
        return []
    with open(ruta, newline='', encoding='latin-1') as f:
        lector = csv.DictReader(f, delimiter=';')
        return [dict(fila) for fila in lector]


# ─────────────────────────────────────────────
# IMPORTADORES
# ─────────────────────────────────────────────

def importar_inventario(conn, ruta: str) -> int:
    """
    Importa productos desde el CSV de inventario de FactuPyme.
    Columnas esperadas: Codigo, Descripción, Cantidad, Precio Venta,
                        Precio Costo, Fecha Modificado, Rubro, Proveedor
    """
    filas = leer_csv(ruta)
    if not filas:
        return 0

    insertados = 0
    actualizados = 0

    for fila in filas:
        codigo      = parsear_codigo(fila.get("Codigo", ""))
        descripcion = fila.get("Descripción", fila.get("Descripcion", "")).strip()

        if not codigo or not descripcion:
            continue

        stock        = parsear_numero(fila.get("Cantidad", "0"))
        precio_venta = parsear_numero(fila.get("Precio Venta", "0"))
        precio_costo = parsear_numero(fila.get("Precio Costo", "0"))
        fecha_ingreso = fila.get("Fecha Modificado", "").strip()
        rubro        = fila.get("Rubro", "").strip()
        proveedor    = fila.get("Proveedor", "").strip()

        # Upsert: si el código ya existe, actualiza; si no, inserta
        existe = conn.execute(
            "SELECT id FROM productos WHERE codigo = ?", (codigo,)
        ).fetchone()

        if existe:
            conn.execute("""
                UPDATE productos SET
                    descripcion    = ?,
                    rubro          = ?,
                    proveedor      = ?,
                    stock          = ?,
                    precio_venta   = ?,
                    precio_costo   = ?,
                    fecha_ingreso  = ?,
                    actualizado_en = datetime('now', 'localtime')
                WHERE codigo = ?
            """, (descripcion, rubro, proveedor, stock,
                  precio_venta, precio_costo, fecha_ingreso, codigo))
            actualizados += 1
        else:
            conn.execute("""
                INSERT INTO productos
                    (codigo, descripcion, rubro, proveedor, stock,
                     precio_venta, precio_costo, fecha_ingreso)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (codigo, descripcion, rubro, proveedor, stock,
                  precio_venta, precio_costo, fecha_ingreso))
            insertados += 1

    conn.commit()
    print(f"✅ Inventario: {insertados} productos nuevos, {actualizados} actualizados")
    return insertados + actualizados


def importar_ventas(conn, ruta: str, origen: str = "factura") -> int:
    """
    Importa ventas o presupuestos históricos desde CSV de FactuPyme.
    Columnas esperadas: Fecha, Producto, Rubro, Precio Costo, Cant., Subtotal, Cliente
    """
    filas = leer_csv(ruta)
    if not filas:
        return 0

    # Limpiar historial previo del mismo origen para evitar duplicados al re-importar
    conn.execute(
        "DELETE FROM ventas_historicas WHERE origen = ?", (origen,)
    )

    insertados = 0
    for fila in filas:
        fecha    = fila.get("Fecha", "").strip()
        producto = fila.get("Producto", "").strip()

        if not fecha or not producto:
            continue

        costo_unit = parsear_numero(fila.get("Precio Costo", "0"))
        cantidad   = parsear_numero(fila.get("Cant.", fila.get("Cantidad", "0")))
        subtotal   = parsear_numero(fila.get("Subtotal", "0"))
        rubro      = fila.get("Rubro", "").strip()
        cliente    = fila.get("Cliente", "").strip()

        # Regla del negocio: ganancia = subtotal - (costo_unit × cantidad)
        ganancia = subtotal - (costo_unit * cantidad)

        conn.execute("""
            INSERT INTO ventas_historicas
                (fecha, producto, rubro, costo_unit, cantidad, subtotal, ganancia, cliente, origen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (fecha, producto, rubro, costo_unit, cantidad,
              subtotal, ganancia, cliente, origen))
        insertados += 1

    conn.commit()
    print(f"✅ {'Ventas' if origen == 'factura' else 'Presupuestos'}: {insertados} registros importados")
    return insertados


# ─────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────

def importar_todo(
    inventario="inventario.csv",
    ventas="ventas.csv",
    presupuestos="presupuestos.csv"
):
    print("\n🔄 Iniciando importación de FactuPyme...\n")

    inicializar_db()
    conn = conectar()

    total = 0
    # Fuente única: si no hay inventario en csv_originales, usar el MISMO
    # archivo que lee Eva (negocio/inventario.csv en la raíz del proyecto).
    ruta_inventario = os.path.join(DATA_DIR, inventario)
    if not os.path.exists(ruta_inventario):
        raiz = os.path.dirname(os.path.dirname(DATA_DIR))
        alternativa = os.path.join(os.path.dirname(raiz), "negocio", "inventario.csv")
        if os.path.exists(alternativa):
            print(f"ℹ️  Usando el inventario compartido con Eva: {alternativa}")
            ruta_inventario = alternativa
    total += importar_inventario(conn, ruta_inventario)
    total += importar_ventas(conn, os.path.join(DATA_DIR, ventas), origen="factura")
    total += importar_ventas(conn, os.path.join(DATA_DIR, presupuestos), origen="presupuesto")

    conn.close()

    print(f"\n✅ Importación completa — {total} registros procesados")
    print(f"📂 Base de datos: {os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db', 'coronel_sur.db')}")


if __name__ == "__main__":
    # Permite pasar nombres de archivo como argumentos opcionales
    args = sys.argv[1:]
    kwargs = {}
    if len(args) >= 1: kwargs["inventario"]    = args[0]
    if len(args) >= 2: kwargs["ventas"]        = args[1]
    if len(args) >= 3: kwargs["presupuestos"]  = args[2]
    importar_todo(**kwargs)
