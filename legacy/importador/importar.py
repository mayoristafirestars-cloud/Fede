"""
Importador de CSVs de FactuPyme → Base de datos Coronel Sur

Uso:
    python importar.py inventario  archivo.csv
    python importar.py ventas      archivo.csv
    python importar.py presupuestos archivo.csv

Encoding esperado: latin-1  |  Separador: punto y coma (;)
"""

import csv
import sys
import json
import os
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from database.schema import get_conexion, crear_tablas


# ── HELPERS ────────────────────────────────────────────────────────────────

def parsear_numero(texto):
    """
    Convierte texto de FactuPyme a float.
    Regla clave: si hay punto con 3 dígitos después = separador de miles (ignorar)
                 si hay punto con 1-2 dígitos después = decimal (conservar)
    Ej: "10.000" → 10000.0  |  "1999.5" → 1999.5  |  "1.234.567" → 1234567.0
    """
    if not texto or texto.strip() == '':
        return 0.0
    t = texto.strip().replace(' ', '')
    # Remover puntos que sean separadores de miles (seguidos de exactamente 3 dígitos)
    t = re.sub(r'\.(?=\d{3}(?:[.,]|$))', '', t)
    # Reemplazar coma decimal por punto
    t = t.replace(',', '.')
    try:
        return float(t)
    except ValueError:
        return 0.0


def parsear_codigo(texto):
    """Extrae número de 'Cod: 12345' → '12345' """
    if not texto:
        return texto
    match = re.search(r'\d+', texto)
    return match.group() if match else texto.strip()


def normalizar_fecha(texto):
    """DD-MM-AAAA o DD/MM/AAAA → AAAA-MM-DD para SQLite"""
    if not texto or texto.strip() == '':
        return None
    t = texto.strip().replace('/', '-')
    partes = t.split('-')
    if len(partes) == 3:
        if len(partes[0]) == 2:  # formato DD-MM-AAAA
            return f"{partes[2]}-{partes[1]}-{partes[0]}"
        return t  # ya está en formato correcto
    return texto.strip()


def leer_csv(ruta):
    """Lee CSV de FactuPyme (latin-1, punto y coma)"""
    filas = []
    with open(ruta, newline='', encoding='latin-1') as f:
        lector = csv.DictReader(f, delimiter=';')
        for fila in lector:
            # Limpiar espacios en claves y valores
            fila_limpia = {k.strip(): v.strip() if v else '' for k, v in fila.items()}
            filas.append(fila_limpia)
    return filas


# ── IMPORTADORES ───────────────────────────────────────────────────────────

def importar_inventario(ruta):
    """
    Importa productos desde CSV de inventario de FactuPyme.
    Columnas: Codigo, Descripción, Cantidad, Precio Venta, Precio Costo,
              Fecha Modificado, Rubro, Proveedor
    """
    print(f"\n📦 Importando inventario desde: {ruta}")
    filas = leer_csv(ruta)
    conn = get_conexion()
    cur = conn.cursor()

    ok = 0
    errores = []

    for i, fila in enumerate(filas, 1):
        try:
            codigo = parsear_codigo(fila.get('Codigo', '') or fila.get('Código', ''))
            descripcion = fila.get('Descripción', '') or fila.get('Descripcion', '')

            if not codigo or not descripcion:
                errores.append(f"Fila {i}: sin código o descripción — {fila}")
                continue

            precio_venta = parsear_numero(fila.get('Precio Venta', '0'))
            precio_costo = parsear_numero(fila.get('Precio Costo', '0'))
            stock = int(parsear_numero(fila.get('Cantidad', '0')))
            rubro = fila.get('Rubro', '')
            proveedor = fila.get('Proveedor', '')
            fecha_ingreso = normalizar_fecha(fila.get('Fecha Modificado', ''))

            # INSERT OR REPLACE — si el código ya existe, actualiza
            cur.execute("""
                INSERT INTO productos
                    (codigo, descripcion, rubro, proveedor, precio_venta,
                     precio_costo, stock_actual, fecha_ingreso)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(codigo) DO UPDATE SET
                    descripcion   = excluded.descripcion,
                    rubro         = excluded.rubro,
                    proveedor     = excluded.proveedor,
                    precio_venta  = excluded.precio_venta,
                    precio_costo  = excluded.precio_costo,
                    stock_actual  = excluded.stock_actual,
                    fecha_ingreso = excluded.fecha_ingreso
            """, (codigo, descripcion, rubro, proveedor, precio_venta,
                  precio_costo, stock, fecha_ingreso))
            ok += 1

        except Exception as e:
            errores.append(f"Fila {i}: {e} — {fila}")

    conn.commit()
    _registrar_log(cur, conn, ruta, 'inventario', len(filas), ok, errores)
    conn.close()
    _mostrar_resumen('inventario', len(filas), ok, errores)
    return ok, errores


def importar_ventas(ruta, tipo='ventas'):
    """
    Importa ventas o presupuestos desde CSV de FactuPyme.
    Columnas: Fecha, Producto, Rubro, Precio Costo, Cant., Subtotal, Cliente
    tipo: 'ventas' o 'presupuestos'
    """
    print(f"\n🧾 Importando {tipo} desde: {ruta}")
    filas = leer_csv(ruta)
    conn = get_conexion()
    cur = conn.cursor()

    ok = 0
    errores = []
    facturas_creadas = {}  # clave: (fecha, cliente) → factura_id

    for i, fila in enumerate(filas, 1):
        try:
            fecha = normalizar_fecha(fila.get('Fecha', ''))
            producto_nombre = fila.get('Producto', '')
            precio_costo = parsear_numero(fila.get('Precio Costo', '0'))
            cantidad = parsear_numero(fila.get('Cant.', '') or fila.get('Cantidad', '1'))
            subtotal = parsear_numero(fila.get('Subtotal', '0'))
            cliente_nombre = fila.get('Cliente', 'Consumidor Final').strip() or 'Consumidor Final'

            if not fecha or not producto_nombre:
                errores.append(f"Fila {i}: sin fecha o producto — {fila}")
                continue

            # Calcular precio_venta unitario desde subtotal
            precio_venta = subtotal / cantidad if cantidad > 0 else 0

            # Agrupar items del mismo cliente/fecha en una factura
            clave = (fecha, cliente_nombre)
            if clave not in facturas_creadas:
                cur.execute("""
                    INSERT INTO facturas (tipo, cliente_nombre, fecha, total, origen)
                    VALUES (?, ?, ?, 0, 'importado_factu')
                """, (tipo.rstrip('s'),  # 'venta' o 'presupuesto'
                      cliente_nombre, fecha))
                facturas_creadas[clave] = cur.lastrowid

            factura_id = facturas_creadas[clave]

            # Buscar producto en DB por nombre (puede no estar si el inventario no se importó)
            cur.execute("SELECT id FROM productos WHERE descripcion = ? LIMIT 1",
                        (producto_nombre,))
            prod = cur.fetchone()
            producto_id = prod['id'] if prod else None

            # Insertar item
            cur.execute("""
                INSERT INTO factura_items
                    (factura_id, producto_id, descripcion, cantidad,
                     precio_venta, precio_costo, subtotal)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (factura_id, producto_id, producto_nombre,
                  cantidad, precio_venta, precio_costo, subtotal))

            ok += 1

        except Exception as e:
            errores.append(f"Fila {i}: {e} — {fila}")

    # Actualizar totales de cada factura
    cur.execute("""
        UPDATE facturas SET total = (
            SELECT COALESCE(SUM(subtotal), 0)
            FROM factura_items WHERE factura_id = facturas.id
        )
        WHERE origen = 'importado_factu'
    """)

    conn.commit()
    _registrar_log(cur, conn, ruta, tipo, len(filas), ok, errores)
    conn.close()
    _mostrar_resumen(tipo, len(filas), ok, errores)
    return ok, errores


def importar_presupuestos(ruta):
    return importar_ventas(ruta, tipo='presupuestos')


# ── HELPERS INTERNOS ───────────────────────────────────────────────────────

def _registrar_log(cur, conn, archivo, tipo, total, ok, errores):
    cur.execute("""
        INSERT INTO log_importacion
            (archivo, tipo, filas_totales, filas_ok, filas_error, errores)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (os.path.basename(archivo), tipo, total, ok, len(errores),
          json.dumps(errores[:20], ensure_ascii=False)))  # max 20 errores en log
    conn.commit()


def _mostrar_resumen(tipo, total, ok, errores):
    print(f"   Total filas:  {total}")
    print(f"   ✅ Importadas: {ok}")
    print(f"   ❌ Errores:    {len(errores)}")
    if errores:
        print("\n   Primeros errores:")
        for e in errores[:5]:
            print(f"   · {e}")


# ── CLI ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Uso: python importar.py [inventario|ventas|presupuestos] archivo.csv")
        sys.exit(1)

    tipo = sys.argv[1].lower()
    archivo = sys.argv[2]

    if not os.path.exists(archivo):
        print(f"❌ Archivo no encontrado: {archivo}")
        sys.exit(1)

    # Crear tablas si no existen
    crear_tablas()

    if tipo == 'inventario':
        importar_inventario(archivo)
    elif tipo == 'ventas':
        importar_ventas(archivo)
    elif tipo == 'presupuestos':
        importar_presupuestos(archivo)
    else:
        print(f"❌ Tipo desconocido: {tipo}. Usar: inventario / ventas / presupuestos")
        sys.exit(1)
