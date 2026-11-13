"""Configuración leída de variables de entorno (y de un archivo .env opcional)."""

import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cargar_env(ruta: str = None):
    """Carga KEY=VALOR de .env sin pisar variables ya definidas."""
    ruta = ruta or os.path.join(RAIZ, ".env")
    if not os.path.isfile(ruta):
        return
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            clave, valor = linea.split("=", 1)
            os.environ.setdefault(clave.strip(), valor.strip().strip('"').strip("'"))


def entorno() -> str:
    return os.environ.get("ENTORNO", "desarrollo").lower()


def es_produccion() -> bool:
    return entorno() == "produccion"


def sesion_horas() -> int:
    return int(os.environ.get("SESION_HORAS", "12"))


def iva_alicuota() -> "Decimal":
    """
    Alícuota de IVA supuesta para mostrar la ganancia sin IVA (Responsable Inscripto).
    Precios y costos se cargan con IVA incluido. Hasta tener la alícuota de cada
    producto, se asume la misma para todo: IVA_ALICUOTA (por defecto 21).
    """
    from decimal import Decimal
    valor = Decimal(os.environ.get("IVA_ALICUOTA", "21"))
    if not (0 <= valor < 100):
        raise ValueError("IVA_ALICUOTA debe estar entre 0 y 100")
    return valor
