"""
Verificador de importación — muestra resumen de lo que hay en la DB
Uso: python verificar.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from database.schema import get_conexion


def verificar():
    conn = get_conexion()
    cur = conn.cursor()

    print("\n" + "="*55)
    print("  VERIFICACIÓN DE BASE DE DATOS — CORONEL SUR")
    print("="*55)

    # Productos
    cur.execute("SELECT COUNT(*) as n, SUM(stock_actual) as stock FROM productos WHERE activo=1")
    r = cur.fetchone()
    print(f"\n📦 PRODUCTOS")
    print(f"   Total productos activos: {r['n']:,}")
    print(f"   Unidades en stock:       {int(r['stock'] or 0):,}")

    # Por rubro
    cur.execute("""
        SELECT rubro, COUNT(*) as n, SUM(stock_actual) as stock
        FROM productos WHERE activo=1 AND rubro != ''
        GROUP BY rubro ORDER BY n DESC LIMIT 8
    """)
    rubros = cur.fetchall()
    if rubros:
        print(f"\n   Top rubros:")
        for r in rubros:
            print(f"   · {r['rubro']:<25} {r['n']:>4} productos  |  {int(r['stock'] or 0):>6} uds")

    # Productos sin costo o sin precio
    cur.execute("SELECT COUNT(*) as n FROM productos WHERE precio_costo = 0 AND activo=1")
    sin_costo = cur.fetchone()['n']
    cur.execute("SELECT COUNT(*) as n FROM productos WHERE precio_venta = 0 AND activo=1")
    sin_precio = cur.fetchone()['n']
    if sin_costo > 0:
        print(f"\n   ⚠️  Sin precio costo: {sin_costo} productos")
    if sin_precio > 0:
        print(f"   ⚠️  Sin precio venta: {sin_precio} productos")

    # Facturas
    cur.execute("""
        SELECT tipo, COUNT(*) as n, SUM(total) as total
        FROM facturas GROUP BY tipo
    """)
    facturas = cur.fetchall()
    if facturas:
        print(f"\n🧾 FACTURAS IMPORTADAS")
        for f in facturas:
            print(f"   {f['tipo']:<15} {f['n']:>5} registros  |  ${f['total']:>15,.0f}")

    # Clientes
    cur.execute("SELECT COUNT(*) as n FROM clientes")
    n_clientes = cur.fetchone()['n']
    print(f"\n👥 CLIENTES EN DB: {n_clientes:,}")

    # Log de importaciones
    cur.execute("""
        SELECT tipo, archivo, filas_totales, filas_ok, filas_error, fecha
        FROM log_importacion ORDER BY fecha DESC LIMIT 5
    """)
    logs = cur.fetchall()
    if logs:
        print(f"\n📋 ÚLTIMAS IMPORTACIONES")
        for l in logs:
            estado = "✅" if l['filas_error'] == 0 else "⚠️ "
            print(f"   {estado} {l['tipo']:<15} {l['archivo']:<30} "
                  f"{l['filas_ok']}/{l['filas_totales']} filas  |  {l['fecha'][:16]}")

    print("\n" + "="*55)
    conn.close()


if __name__ == '__main__':
    verificar()
