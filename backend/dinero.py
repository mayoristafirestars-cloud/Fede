"""
Plata en centavos enteros, calculada con Decimal y redondeo bancario (ROUND_HALF_EVEN).
Nunca float para calcular; float sólo al responder la API (pesos con 2 decimales).
"""

from decimal import Decimal, ROUND_HALF_EVEN

CENTAVO = Decimal("0.01")


def a_decimal(valor) -> Decimal:
    return Decimal(str(valor))


def redondear(valor: Decimal) -> Decimal:
    """A 2 decimales, con redondeo bancario (0,005 → 0,00; 0,015 → 0,02)."""
    return valor.quantize(CENTAVO, rounding=ROUND_HALF_EVEN)


def a_centavos(valor) -> int:
    """Pesos (número, texto o Decimal) a centavos enteros."""
    return int(redondear(a_decimal(valor)) * 100)


def a_pesos(centavos: int) -> float:
    """Centavos a pesos para responder la API (siempre exacto a 2 decimales)."""
    return float(Decimal(centavos) / 100)


def formato_ar(centavos: int) -> str:
    """$ 1.234.567,89"""
    signo = "-" if centavos < 0 else ""
    entero, cent = divmod(abs(centavos), 100)
    return f"{signo}$ {entero:,}".replace(",", ".") + f",{cent:02d}"


def sin_iva(centavos: int, alicuota_pct: Decimal) -> int:
    """Quita el IVA incluido: 1.210 con 21 % → 1.000."""
    return a_centavos(Decimal(centavos) / 100 / (1 + alicuota_pct / 100))
