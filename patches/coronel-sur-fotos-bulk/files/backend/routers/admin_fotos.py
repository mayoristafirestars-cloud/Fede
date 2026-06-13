"""
Router de importacion masiva de fotos desde CSV.

El CSV tiene formato FactuPyme:
Codigo;Descripcion;...;imagenes

Donde Codigo es "Cod: 8065" e imagenes es una URL.

- GET /admin/fotos            -> pagina HTML para subir el CSV
- POST /api/admin/fotos/importar -> procesa el CSV y hace UPDATE foto_url

Solo admin.
"""
from __future__ import annotations

import csv
import io
import re
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar

router = APIRouter()

TEMPLATE_DIR = Path(__file__).resolve().parent.parent.parent / "frontend" / "templates"

_RE_COD = re.compile(r"(?:Cod\s*:\s*)?(\d+)", re.IGNORECASE)


def _check_admin(request: Request) -> dict:
    auth = request.headers.get("Authorization", "")
    if not auth:
        raise HTTPException(401, "Token requerido")
    token = auth.replace("Bearer ", "").strip()
    if not token:
        raise HTTPException(401, "Token vacio")
    user = None
    try:
        from security.sessions import validar_token  # type: ignore
        user = validar_token(token)
    except Exception:
        user = None
    if not user:
        try:
            from routers.auth import SESIONES_ACTIVAS  # type: ignore
            user = SESIONES_ACTIVAS.get(token)
        except Exception:
            user = None
    if not user:
        raise HTTPException(401, "Sesion invalida")
    if user.get("rol") != "admin":
        raise HTTPException(403, "Requiere rol admin")
    return user


def _normalizar_codigo(raw: str) -> str:
    """'Cod: 8065' -> '8065', ' 123 ' -> '123'."""
    if not raw:
        return ""
    m = _RE_COD.search(raw.strip())
    return m.group(1) if m else raw.strip()


@router.get("/admin/fotos", response_class=HTMLResponse)
def pagina():
    html_path = TEMPLATE_DIR / "admin_fotos.html"
    if not html_path.exists():
        raise HTTPException(404, "Template no encontrado")
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@router.post("/api/admin/fotos/importar")
async def importar(request: Request, archivo: UploadFile = File(...)):
    _check_admin(request)

    raw = await archivo.read()
    # Probar varios encodings comunes en exports de sistemas viejos
    text = None
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        raise HTTPException(400, "No se pudo decodificar el archivo")

    # Detectar delimitador
    sample = text[:2048]
    delim = ";" if sample.count(";") > sample.count(",") else ","

    reader = csv.DictReader(io.StringIO(text), delimiter=delim)
    filas = list(reader)
    if not filas:
        raise HTTPException(400, "CSV vacio o sin encabezado")

    # Buscar columna de codigo y de imagen (nombres tolerantes)
    headers_lower = {h.lower().strip(): h for h in reader.fieldnames or []}
    col_cod = None
    col_img = None
    for key in ("codigo", "código", "cod", "code"):
        if key in headers_lower:
            col_cod = headers_lower[key]
            break
    for key in ("imagenes", "imágenes", "imagen", "foto", "foto_url", "image", "url"):
        if key in headers_lower:
            col_img = headers_lower[key]
            break

    if not col_cod or not col_img:
        raise HTTPException(400, f"No se encontraron columnas de codigo/imagen. Columnas: {list(reader.fieldnames or [])}")

    actualizados = 0
    no_encontrados = 0
    sin_foto = 0
    ejemplos_no_encontrados: list[str] = []

    conn = conectar()
    try:
        for fila in filas:
            cod_raw = (fila.get(col_cod) or "").strip()
            img = (fila.get(col_img) or "").strip()
            cod = _normalizar_codigo(cod_raw)
            if not cod:
                continue
            if not img:
                sin_foto += 1
                continue
            # Update con match por codigo (case insensitive)
            cur = conn.execute(
                "UPDATE productos SET foto_url = ? WHERE codigo = ? OR codigo = ?",
                (img, cod, cod_raw),
            )
            filas_afectadas = getattr(cur, "rowcount", 0) or 0
            if filas_afectadas > 0:
                actualizados += filas_afectadas
            else:
                no_encontrados += 1
                if len(ejemplos_no_encontrados) < 10:
                    ejemplos_no_encontrados.append(cod_raw)
        conn.commit()
    finally:
        conn.close()

    return {
        "ok": True,
        "total_filas": len(filas),
        "actualizados": actualizados,
        "no_encontrados_en_db": no_encontrados,
        "sin_foto_en_csv": sin_foto,
        "ejemplos_no_encontrados": ejemplos_no_encontrados,
    }
