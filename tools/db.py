"""
Base de datos SIMULADA de Trama.
En producción estas funciones se conectarían a Tiendanube/Shopify/ERP.
"""

PEDIDOS = {
    "TRAMA-12345": {
        "email": "juan@example.com",
        "estado": "Enviado",
        "tracking": "AND123456789",
        "courier": "Andreani",
        "items": [
            {"producto": "Buzo Hoodie Classic", "talle": "M", "color": "negro", "cantidad": 1}
        ],
        "fecha_compra": "2025-04-22",
        "fecha_estimada_entrega": "2025-04-25",
    },
    "TRAMA-12346": {
        "email": "maria@example.com",
        "estado": "En preparación",
        "tracking": None,
        "courier": None,
        "items": [
            {"producto": "Remera Basic Box", "talle": "S", "color": "blanco", "cantidad": 2}
        ],
        "fecha_compra": "2025-04-26",
        "fecha_estimada_entrega": "2025-05-01",
    },
    "TRAMA-12347": {
        "email": "pedro@example.com",
        "estado": "Entregado",
        "tracking": "AND987654321",
        "courier": "Andreani",
        "items": [
            {"producto": "Jogger Relax Fit", "talle": "L", "color": "gris melange", "cantidad": 1}
        ],
        "fecha_compra": "2025-04-15",
        "fecha_entrega": "2025-04-20",
    },
}


# Estructura: producto -> color -> talle -> unidades disponibles
STOCK = {
    "Remera Basic Box": {
        "blanco": {"S": 12, "M": 8, "L": 15, "XL": 6, "XXL": 4},
        "negro": {"S": 10, "M": 14, "L": 20, "XL": 7, "XXL": 3},
        "gris melange": {"S": 5, "M": 9, "L": 11, "XL": 4, "XXL": 2},
        "verde militar": {"S": 6, "M": 7, "L": 8, "XL": 3, "XXL": 1},
        "beige": {"S": 4, "M": 6, "L": 9, "XL": 2, "XXL": 0},
    },
    "Remera Oversize Drop": {
        "negro": {"S": 8, "M": 10, "L": 12, "XL": 5, "XXL": 3},
        "blanco": {"S": 6, "M": 8, "L": 10, "XL": 4, "XXL": 2},
        "lila pastel": {"S": 0, "M": 4, "L": 6, "XL": 2, "XXL": 1},
        "terracota": {"S": 3, "M": 5, "L": 7, "XL": 2, "XXL": 1},
    },
    "Buzo Crew Heavy": {
        "negro": {"S": 7, "M": 11, "L": 14, "XL": 5, "XXL": 2},
        "gris melange": {"S": 5, "M": 8, "L": 10, "XL": 3, "XXL": 1},
        "off-white": {"S": 4, "M": 6, "L": 8, "XL": 2, "XXL": 0},
        "verde botella": {"S": 3, "M": 5, "L": 7, "XL": 2, "XXL": 1},
    },
    "Buzo Hoodie Classic": {
        "negro": {"S": 6, "M": 10, "L": 13, "XL": 5, "XXL": 2},
        "gris claro": {"S": 4, "M": 7, "L": 9, "XL": 3, "XXL": 1},
        "marrón chocolate": {"S": 5, "M": 8, "L": 10, "XL": 4, "XXL": 2},
        "azul navy": {"S": 3, "M": 6, "L": 8, "XL": 2, "XXL": 1},
    },
    "Jogger Relax Fit": {
        "negro": {"S": 5, "M": 9, "L": 0, "XL": 4, "XXL": 1},
        "gris melange": {"S": 4, "M": 7, "L": 9, "XL": 3, "XXL": 1},
        "beige": {"S": 3, "M": 5, "L": 7, "XL": 2, "XXL": 1},
        "verde militar": {"S": 2, "M": 4, "L": 6, "XL": 2, "XXL": 0},
    },
    "Campera Workwear": {
        "marrón": {"S": 3, "M": 5, "L": 6, "XL": 2},
        "negro": {"S": 4, "M": 6, "L": 8, "XL": 3},
        "verde botella": {"S": 2, "M": 4, "L": 5, "XL": 1},
    },
}


def buscar_pedido(numero_orden: str, email: str) -> dict:
    """Busca un pedido por número y verifica el email."""
    pedido = PEDIDOS.get(numero_orden.strip().upper())
    if not pedido:
        return {"encontrado": False, "error": "No encontramos ese número de orden."}
    if pedido["email"].lower() != email.strip().lower():
        return {"encontrado": False, "error": "El email no coincide con el del pedido."}
    return {"encontrado": True, "numero_orden": numero_orden.strip().upper(), **pedido}


def consultar_stock(producto: str, talle: str, color: str) -> dict:
    """Consulta el stock disponible para un producto/talle/color."""
    talle = talle.strip().upper()
    color = color.strip().lower()

    producto_match = next(
        (p for p in STOCK if p.lower() == producto.strip().lower()), None
    )
    if not producto_match:
        return {
            "disponible": False,
            "error": f"No encontramos el producto '{producto}' en el catálogo.",
            "productos_disponibles": list(STOCK.keys()),
        }

    colores = STOCK[producto_match]
    color_match = next((c for c in colores if c.lower() == color), None)
    if not color_match:
        return {
            "disponible": False,
            "error": f"El color '{color}' no está disponible para '{producto_match}'.",
            "colores_disponibles": list(colores.keys()),
        }

    talles = colores[color_match]
    if talle not in talles:
        return {
            "disponible": False,
            "error": f"El talle '{talle}' no se fabrica para '{producto_match}'.",
            "talles_disponibles": list(talles.keys()),
        }

    unidades = talles[talle]
    return {
        "disponible": unidades > 0,
        "unidades": unidades,
        "producto": producto_match,
        "color": color_match,
        "talle": talle,
    }
