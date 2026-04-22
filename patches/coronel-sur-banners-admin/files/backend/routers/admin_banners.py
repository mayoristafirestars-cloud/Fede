"""
Router de banners de la tienda publica.

- GET /api/shop/banners       -> publico, lista banners activos ordenados
- GET /api/admin/banners      -> admin, lista todos
- PUT /api/admin/banners      -> admin, reemplaza la lista completa

Persistencia: archivo JSON en data/banners.json. Si no existe,
devuelve los banners por defecto (los 4 hardcoded del HTML original).

El check de admin es tolerante:
- Primero intenta usar security.sessions.validar_token (Fase 0 aplicada)
- Si no esta, cae a routers.auth.SESIONES_ACTIVAS (pre Fase 0)
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Request, Body
from fastapi.responses import HTMLResponse

router = APIRouter()

# data/banners.json en la raiz del proyecto
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
BANNERS_FILE = DATA_DIR / "banners.json"

BANNERS_DEFAULT: list[dict] = [
    {
        "id": 1,
        "orden": 1,
        "activo": True,
        "titulo": "Precio, Calidad<br>y Atención",
        "subtitulo": "Tu distribuidora de confianza. Pedí online, retirá en el local o te lo enviamos a domicilio.",
        "tag": "★ Distribuidora Coronel Sur",
        "emoji": "★",
        "bg_image": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1280&q=80",
        "bg_color": "#F08340",
        "overlay_from": "rgba(240,131,64,.78)",
        "overlay_to": "rgba(218,111,48,.88)",
        "btn_text": "Ver productos →",
        "btn_link": "#prods-container",
        "btn_color": "#DA6F30",
    },
    {
        "id": 2,
        "orden": 2,
        "activo": True,
        "titulo": "",
        "subtitulo": "",
        "tag": "",
        "emoji": "",
        "bg_image": "https://i.postimg.cc/7PWHB9SQ/Chat-GPT-Image-22-abr-2026-05-28-58-p-m.png",
        "bg_color": "#1A3F8B",
        "overlay_from": "transparent",
        "overlay_to": "transparent",
        "btn_text": "",
        "btn_link": "#prods-container",
        "btn_color": "",
    },
    {
        "id": 3,
        "orden": 3,
        "activo": True,
        "titulo": "",
        "subtitulo": "",
        "tag": "",
        "emoji": "",
        "bg_image": "https://i.postimg.cc/C5kwnTd5/Captura-de-pantalla-2026-04-22-173142.png",
        "bg_color": "#00A650",
        "overlay_from": "transparent",
        "overlay_to": "transparent",
        "btn_text": "",
        "btn_link": "#prods-container",
        "btn_color": "",
    },
    {
        "id": 4,
        "orden": 4,
        "activo": True,
        "titulo": "",
        "subtitulo": "",
        "tag": "",
        "emoji": "",
        "bg_image": "https://i.postimg.cc/430G8N96/Captura-de-pantalla-2026-04-22-173134.png",
        "bg_color": "#FF6A00",
        "overlay_from": "transparent",
        "overlay_to": "transparent",
        "btn_text": "",
        "btn_link": "#prods-container",
        "btn_color": "",
    },
]


def _cargar() -> list[dict]:
    if not BANNERS_FILE.exists():
        return [dict(b) for b in BANNERS_DEFAULT]
    try:
        data = json.loads(BANNERS_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, list) or not data:
            return [dict(b) for b in BANNERS_DEFAULT]
        return data
    except Exception:
        return [dict(b) for b in BANNERS_DEFAULT]


def _guardar(banners: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BANNERS_FILE.write_text(
        json.dumps(banners, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _check_admin(request: Request) -> dict:
    """Valida token y rol admin. Tolerante a Fase 0 aplicada o no."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Token requerido")
    token = auth_header.replace("Bearer ", "").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Token vacio")

    user: dict | None = None

    # 1) Intentar con sesiones persistentes (Fase 0)
    try:
        from security.sessions import validar_token  # type: ignore
        user = validar_token(token)
    except Exception:
        user = None

    # 2) Fallback: SESIONES_ACTIVAS en memoria (pre Fase 0)
    if not user:
        try:
            from routers.auth import SESIONES_ACTIVAS  # type: ignore
            user = SESIONES_ACTIVAS.get(token)
        except Exception:
            user = None

    if not user:
        raise HTTPException(status_code=401, detail="Sesion invalida")
    if user.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Requiere rol admin")
    return user


def _normalizar(banners: list[Any]) -> list[dict]:
    """Sanea el array: fuerza tipos, re-asigna orden e id si faltan."""
    out: list[dict] = []
    for i, b in enumerate(banners):
        if not isinstance(b, dict):
            continue
        out.append({
            "id": int(b.get("id") or (i + 1)),
            "orden": i + 1,
            "activo": bool(b.get("activo", True)),
            "titulo": str(b.get("titulo", "")).strip(),
            "subtitulo": str(b.get("subtitulo", "")).strip(),
            "tag": str(b.get("tag", "")).strip(),
            "emoji": str(b.get("emoji", "")).strip(),
            "bg_image": str(b.get("bg_image", "")).strip(),
            "bg_color": str(b.get("bg_color", "#F08340")).strip() or "#F08340",
            "overlay_from": str(b.get("overlay_from", "")).strip(),
            "overlay_to": str(b.get("overlay_to", "")).strip(),
            "btn_text": str(b.get("btn_text", "Ver más →")).strip() or "Ver más →",
            "btn_link": str(b.get("btn_link", "#prods-container")).strip() or "#prods-container",
            "btn_color": str(b.get("btn_color", "")).strip(),
        })
    return out


# ---------------- PAGINA ADMIN ----------------

TEMPLATE_DIR = Path(__file__).resolve().parent.parent.parent / "frontend" / "templates"

@router.get("/admin/banners", response_class=HTMLResponse)
def pagina_admin():
    html_path = TEMPLATE_DIR / "admin_banners.html"
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="Template no encontrado")
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@router.get("/admin/reportes", response_class=HTMLResponse)
def pagina_reportes():
    html_path = TEMPLATE_DIR / "admin_reportes.html"
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="Template no encontrado")
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


# ---------------- ENDPOINTS PUBLICOS ----------------

@router.get("/api/shop/banners")
def listar_publicos():
    """Banners activos y ordenados. Los consume la tienda."""
    banners = _cargar()
    activos = [b for b in banners if b.get("activo", True)]
    activos.sort(key=lambda x: x.get("orden", 999))
    # Solo devolver los campos que el frontend necesita
    return [
        {
            "titulo": b.get("titulo", ""),
            "subtitulo": b.get("subtitulo", ""),
            "tag": b.get("tag", ""),
            "emoji": b.get("emoji", ""),
            "bg_image": b.get("bg_image", ""),
            "bg_color": b.get("bg_color", "#F08340"),
            "overlay_from": b.get("overlay_from", ""),
            "overlay_to": b.get("overlay_to", ""),
            "btn_text": b.get("btn_text", "Ver más →"),
            "btn_link": b.get("btn_link", "#prods-container"),
            "btn_color": b.get("btn_color", ""),
        }
        for b in activos
    ]


# ---------------- ENDPOINTS ADMIN ----------------

@router.get("/api/admin/banners")
def listar_admin(request: Request):
    _check_admin(request)
    return _cargar()


@router.put("/api/admin/banners")
def reemplazar(request: Request, banners: list[dict] = Body(...)):
    _check_admin(request)
    if not isinstance(banners, list):
        raise HTTPException(status_code=400, detail="Se esperaba un array")
    if len(banners) > 12:
        raise HTTPException(status_code=400, detail="Máximo 12 banners")
    data = _normalizar(banners)
    _guardar(data)
    return {"ok": True, "total": len(data)}


@router.post("/api/admin/banners/reset")
def reset(request: Request):
    """Vuelve a los banners por defecto. Util si algo se rompe."""
    _check_admin(request)
    _guardar([dict(b) for b in BANNERS_DEFAULT])
    return {"ok": True, "total": len(BANNERS_DEFAULT)}
