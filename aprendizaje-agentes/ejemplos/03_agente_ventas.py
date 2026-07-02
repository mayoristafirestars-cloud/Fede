"""
FASE 3 — Agente conectado a una base de datos SQLite (como tu Coronel Sur).

Este ejemplo crea una base de datos de prueba con productos y ventas,
y le da a Claude herramientas para consultarla. Le podés preguntar en
lenguaje natural cosas como:

    "¿Cuáles fueron los productos más vendidos?"
    "¿Qué productos tienen stock bajo?"

IMPORTANTE (seguridad): las herramientas ejecutan SQL que escribimos
NOSOTROS, con parámetros. Nunca le des al modelo la capacidad de
ejecutar SQL libre contra tu base real.

Para adaptarlo a tu Coronel Sur: cambiá crear_db_demo() por una conexión
a tu coronel_sur.db y ajustá las consultas a tus tablas reales
(productos, clientes, ventas_historicas).

Ejecutar:
    python 03_agente_ventas.py
"""

import json
import sqlite3

from anthropic import beta_tool
import anthropic

client = anthropic.Anthropic()
MODELO = "claude-opus-4-8"
DB = "demo_ventas.db"


# ------------------------------------------------------------------
# Base de datos de prueba (en tu caso: usá tu coronel_sur.db)
# ------------------------------------------------------------------
def crear_db_demo():
    conn = sqlite3.connect(DB)
    conn.executescript("""
        DROP TABLE IF EXISTS productos;
        DROP TABLE IF EXISTS ventas;
        CREATE TABLE productos (
            id INTEGER PRIMARY KEY, nombre TEXT, rubro TEXT,
            precio REAL, stock INTEGER
        );
        CREATE TABLE ventas (
            id INTEGER PRIMARY KEY, producto_id INTEGER,
            cantidad INTEGER, fecha TEXT
        );
        INSERT INTO productos VALUES
            (1, 'Encendedor recargable', 'encendedores', 1500, 120),
            (2, 'Cargador USB-C 20W',    'electronica',   8000, 8),
            (3, 'Auriculares BT',        'electronica',  12000, 45),
            (4, 'Pilas AA x4',           'pilas',         2500, 5),
            (5, 'Linterna LED',          'iluminacion',   6000, 60);
        INSERT INTO ventas VALUES
            (1, 1, 50, '2026-06-10'), (2, 3, 12, '2026-06-12'),
            (3, 1, 30, '2026-06-15'), (4, 2, 5,  '2026-06-20'),
            (5, 4, 20, '2026-06-22'), (6, 3, 8,  '2026-06-28');
    """)
    conn.commit()
    conn.close()


def consulta(sql: str, params: tuple = ()) -> str:
    """Ejecuta una consulta de solo lectura y devuelve JSON."""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    try:
        filas = [dict(f) for f in conn.execute(sql, params).fetchall()]
        return json.dumps(filas, ensure_ascii=False)
    finally:
        conn.close()


# ------------------------------------------------------------------
# Herramientas del agente (con @beta_tool el SDK genera el esquema
# automáticamente desde la firma y el docstring de la función)
# ------------------------------------------------------------------
@beta_tool
def buscar_producto(texto: str) -> str:
    """Busca productos por nombre o rubro. Usala cuando pregunten por
    un producto específico, su precio o su stock.

    Args:
        texto: Texto a buscar en el nombre o rubro del producto.
    """
    return consulta(
        "SELECT * FROM productos WHERE nombre LIKE ? OR rubro LIKE ?",
        (f"%{texto}%", f"%{texto}%"),
    )


@beta_tool
def productos_mas_vendidos(limite: int = 5) -> str:
    """Devuelve los productos más vendidos (por unidades), de mayor a menor.
    Usala para preguntas sobre qué se vende más.

    Args:
        limite: Cuántos productos devolver (por defecto 5).
    """
    return consulta("""
        SELECT p.nombre, SUM(v.cantidad) AS unidades_vendidas
        FROM ventas v JOIN productos p ON p.id = v.producto_id
        GROUP BY p.id ORDER BY unidades_vendidas DESC LIMIT ?
    """, (limite,))


@beta_tool
def stock_bajo(limite: int = 10) -> str:
    """Lista productos con stock por debajo de un límite. Usala para
    preguntas sobre reposición o faltantes.

    Args:
        limite: Umbral de stock (por defecto 10 unidades).
    """
    return consulta(
        "SELECT nombre, stock, precio FROM productos WHERE stock < ? ORDER BY stock",
        (limite,),
    )


# ------------------------------------------------------------------
# El agente: el tool runner del SDK maneja el bucle por nosotros
# ------------------------------------------------------------------
def preguntar(pregunta: str):
    runner = client.beta.messages.tool_runner(
        model=MODELO,
        max_tokens=2048,
        system="Sos el asistente de datos de un negocio mayorista argentino. "
               "Usá las herramientas para responder con datos reales de la base. "
               "Respondé en español, corto y con números concretos.",
        tools=[buscar_producto, productos_mas_vendidos, stock_bajo],
        messages=[{"role": "user", "content": pregunta}],
    )
    # El runner itera: cada mensaje puede incluir usos de herramientas;
    # el último tiene la respuesta final.
    ultimo = None
    for mensaje in runner:
        ultimo = mensaje
    for bloque in ultimo.content:
        if bloque.type == "text":
            print(bloque.text)


if __name__ == "__main__":
    crear_db_demo()
    print("=== Pregunta 1 ===")
    preguntar("¿Cuáles fueron los 3 productos más vendidos?")
    print("\n=== Pregunta 2 ===")
    preguntar("¿Qué productos necesito reponer? Decime cuáles tienen stock bajo.")
