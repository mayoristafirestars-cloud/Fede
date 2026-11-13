"""
Lectura de archivos de importación (CSV o Excel) y normalización de datos argentinos:
importes, fechas, CUIT y teléfonos. Funciones puras, sin acceso a la base.
"""

import csv
import io
import json
import os
import re
import unicodedata
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation

DIR_MAPEOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mapeos")


class ErrorDato(ValueError):
    pass


# ─── Texto y mapeos ────────────────────────────────────────

def clave(texto) -> str:
    """Normaliza un encabezado: sin tildes, minúsculas, sin puntuación ni espacios dobles."""
    t = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-z0-9]+", " ", t.lower())
    return t.strip()


def cargar_mapeo(formato: str) -> dict:
    ruta = os.path.join(DIR_MAPEOS, f"{formato}.json")
    if not re.fullmatch(r"[a-z_]+", formato) or not os.path.isfile(ruta):
        raise ErrorDato(f"Formato desconocido: {formato}")
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


# ─── Archivos ──────────────────────────────────────────────

def _texto(contenido: bytes) -> str:
    for codificacion in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return contenido.decode(codificacion)
        except UnicodeDecodeError:
            continue
    raise ErrorDato("No se pudo leer el archivo como texto")


def leer_filas(nombre: str, contenido: bytes) -> list[list]:
    """Devuelve todas las filas del archivo (sin decidir cuál es el encabezado)."""
    if nombre.lower().endswith((".xlsx", ".xlsm")):
        from openpyxl import load_workbook
        try:
            libro = load_workbook(io.BytesIO(contenido), read_only=True, data_only=True)
        except Exception as e:
            raise ErrorDato(f"No se pudo abrir el Excel: {e}")
        hoja = libro.worksheets[0]
        return [list(f) for f in hoja.iter_rows(values_only=True)]
    if nombre.lower().endswith(".xls"):
        raise ErrorDato("Formato .xls antiguo: guardalo como .xlsx o .csv")
    texto = _texto(contenido)
    muestra = texto[:5000]
    try:
        separador = csv.Sniffer().sniff(muestra, delimiters=";,\t").delimiter
    except csv.Error:
        separador = ";"
    return [fila for fila in csv.reader(io.StringIO(texto), delimiter=separador)]


def ubicar_columnas(filas: list[list], mapeo: dict) -> tuple[int, dict]:
    """
    Busca la fila de encabezados (puede haber títulos arriba, como en el Excel de ARCA)
    y devuelve (índice de esa fila, {campo: índice de columna}).
    """
    campos = mapeo["campos"]
    obligatorios = [c for c, d in campos.items() if d.get("obligatorio")]
    for i, fila in enumerate(filas[:15]):
        encabezados = {clave(v): j for j, v in enumerate(fila) if v not in (None, "")}
        ubicadas = {}
        for campo, definicion in campos.items():
            for alias in definicion["alias"]:
                if clave(alias) in encabezados:
                    ubicadas[campo] = encabezados[clave(alias)]
                    break
        if all(c in ubicadas for c in obligatorios):
            return i, ubicadas
    faltan = ", ".join(campos[c]["alias"][0] for c in obligatorios)
    raise ErrorDato(f"No se encontraron las columnas obligatorias ({faltan}). Revisá que sea el archivo correcto.")


# ─── Datos ─────────────────────────────────────────────────

def parsear_importe(valor) -> Decimal:
    """
    Importes en formato argentino o mixto, como los exporta FactuPyme:
    "1.234,56" → 1234.56 · "1.500" → 1500 · "850.5" → 850.5 · "2,00" → 2 · "$ -1.000" → -1000.
    """
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        raise ErrorDato("importe vacío")
    if isinstance(valor, (int, float, Decimal)):
        return Decimal(str(valor))
    v = re.sub(r"[\s$]", "", str(valor))
    negativo = v.startswith("(") and v.endswith(")")
    v = v.strip("()")
    if "," in v:                                  # coma = decimal; los puntos son miles
        v = v.replace(".", "").replace(",", ".")
    else:
        partes = v.split(".")
        if len(partes) > 2 or (len(partes) == 2 and len(partes[1]) == 3):
            v = "".join(partes)                   # "1.500" y "1.234.567" son miles
    try:
        numero = Decimal(v)
    except InvalidOperation:
        raise ErrorDato(f"importe ilegible ({valor!r})")
    return -numero if negativo else numero


def parsear_fecha(valor) -> date:
    """dd-mm-aaaa, dd/mm/aaaa, aaaa-mm-dd o fecha de Excel."""
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    texto = str(valor or "").strip()
    if not texto:
        raise ErrorDato("fecha vacía")
    m = re.fullmatch(r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})", texto)
    try:
        if m:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})(?:[ T].*)?", texto)
        if m:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        pass
    raise ErrorDato(f"fecha inválida ({texto!r})")


def normalizar_cuit(valor) -> str:
    """Devuelve el CUIT/CUIL de 11 dígitos si el dígito verificador es correcto."""
    digitos = re.sub(r"\D", "", str(valor or ""))
    if len(digitos) != 11:
        raise ErrorDato(f"CUIT inválido ({valor!r}): debe tener 11 dígitos")
    pesos = (5, 4, 3, 2, 7, 6, 5, 4, 3, 2)
    resto = 11 - sum(int(d) * p for d, p in zip(digitos, pesos)) % 11
    verificador = 0 if resto == 11 else 9 if resto == 10 else resto
    if verificador != int(digitos[-1]):
        raise ErrorDato(f"CUIT inválido ({valor!r}): dígito verificador incorrecto")
    return digitos


def normalizar_telefono(valor, caracteristica_defecto: str = "2954") -> str | None:
    """
    Teléfono argentino a E.164 para celulares (+549...). Devuelve None si no se puede
    asegurar el número. Acepta: 2954 525928 · 02954-15-525928 · +54 9 2954 525928.
    Sin característica se asume la de Santa Rosa (2954).
    """
    d = re.sub(r"\D", "", str(valor or ""))
    if not d:
        return None
    if d.startswith("549") and len(d) == 13:
        return "+" + d
    if d.startswith("54") and len(d) == 12:
        return "+549" + d[2:]
    d = d.lstrip("0")
    if len(d) == 12 and "15" in d[2:6]:            # característica + 15 + número local
        for largo in (2, 3, 4):
            if d[largo:largo + 2] == "15" and len(d[:largo] + d[largo + 2:]) == 10:
                return "+549" + d[:largo] + d[largo + 2:]
    if len(d) == 10:
        return "+549" + d
    if len(d) == 6 and caracteristica_defecto:
        return "+549" + caracteristica_defecto + d
    if len(d) == 8 and d.startswith("15") and caracteristica_defecto:
        return "+549" + caracteristica_defecto + d[2:]
    return None


def mas_dias(fecha: date, dias: int) -> date:
    return fecha + timedelta(days=dias)
