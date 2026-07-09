"""
Autenticación simple por clave única + cookie firmada.

- La clave se define en la variable de entorno CORONEL_CLAVE
  (por defecto "coronel2026" — CAMBIARLA antes de ponerlo online).
- El token del agente (para que Eva mande pedidos máquina-a-máquina)
  se define en AGENTE_TOKEN.
"""
import hashlib
import hmac
import os
import time

from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

CLAVE = os.getenv("CORONEL_CLAVE", "coronel2026")
AGENTE_TOKEN = os.getenv("AGENTE_TOKEN", "eva-coronel-2026")
_SECRET = hashlib.sha256(f"coronel-sur|{CLAVE}".encode()).hexdigest()
SESION_DIAS = 30

# Rutas que no requieren login
ABIERTAS = ("/login", "/static/", "/favicon", "/health")
# Rutas máquina-a-máquina (requieren header X-Token) — match EXACTO
MAQUINA = ("/api/agente/pedido", "/api/agente/conversacion", "/api/agente/resumen-diario")


def firmar(valor: str) -> str:
    return hmac.new(_SECRET.encode(), valor.encode(), hashlib.sha256).hexdigest()


def crear_token() -> str:
    exp = str(int(time.time()) + SESION_DIAS * 86400)
    return f"{exp}.{firmar(exp)}"


def token_valido(token: str) -> bool:
    try:
        exp, firma = token.split(".", 1)
        if int(exp) < time.time():
            return False
        return hmac.compare_digest(firma, firmar(exp))
    except Exception:
        return False


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if any(path.startswith(p) for p in ABIERTAS):
            return await call_next(request)

        if path in MAQUINA:
            if request.headers.get("X-Token") == AGENTE_TOKEN:
                return await call_next(request)
            return JSONResponse({"detail": "Token inválido"}, status_code=401)

        token = request.cookies.get("coronel_sesion", "")
        if token_valido(token):
            return await call_next(request)

        if path.startswith("/api/"):
            return JSONResponse({"detail": "No autenticado"}, status_code=401)
        return RedirectResponse("/login")


LOGIN_HTML = """<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Coronel Sur — Ingresar</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0c0c0e;color:#e2e2e8;font-family:system-ui,sans-serif;
     display:flex;align-items:center;justify-content:center;height:100vh}
.box{background:#131316;border:1px solid #2c2c36;border-radius:16px;
     padding:36px;width:min(360px,90vw);text-align:center}
h1{font-size:20px;margin-bottom:6px}
p{color:#9494a4;font-size:13px;margin-bottom:22px}
input{width:100%;background:#1a1a1f;border:1px solid #2c2c36;border-radius:10px;
      padding:12px 14px;color:#e2e2e8;font-size:15px;outline:none;text-align:center}
input:focus{border-color:#f0c93a}
button{width:100%;margin-top:12px;background:#f0c93a;color:#111;border:none;
       border-radius:10px;padding:12px;font-size:15px;font-weight:700;cursor:pointer}
.err{color:#e84545;font-size:13px;margin-top:10px;min-height:18px}
</style></head><body>
<div class="box">
  <h1>🔐 Coronel Sur</h1>
  <p>Sistema de gestión</p>
  <form method="post" action="/login">
    <input type="password" name="clave" placeholder="Clave de acceso" autofocus required>
    <button type="submit">Ingresar</button>
    <div class="err">{ERROR}</div>
  </form>
</div></body></html>"""


# Anti fuerza bruta: máximo 5 intentos fallidos por IP cada 15 minutos
_intentos_fallidos: dict = {}
MAX_INTENTOS = 5
VENTANA_SEG = 900


def _bloqueado(ip: str) -> bool:
    ahora = time.time()
    recientes = [t for t in _intentos_fallidos.get(ip, []) if ahora - t < VENTANA_SEG]
    _intentos_fallidos[ip] = recientes
    return len(recientes) >= MAX_INTENTOS


def registrar_rutas(app):
    from fastapi import Form

    @app.get("/login", response_class=HTMLResponse)
    def login_form():
        return LOGIN_HTML.replace("{ERROR}", "")

    @app.post("/login")
    def login_post(request: Request, clave: str = Form(...)):
        ip = request.client.host if request.client else "?"
        if _bloqueado(ip):
            return HTMLResponse(
                LOGIN_HTML.replace(
                    "{ERROR}", "Demasiados intentos. Esperá 15 minutos."
                ),
                status_code=429,
            )
        if hmac.compare_digest(clave, CLAVE):
            _intentos_fallidos.pop(ip, None)
            resp = RedirectResponse("/", status_code=303)
            resp.set_cookie(
                "coronel_sesion", crear_token(),
                max_age=SESION_DIAS * 86400, httponly=True, samesite="lax",
            )
            return resp
        _intentos_fallidos.setdefault(ip, []).append(time.time())
        return HTMLResponse(LOGIN_HTML.replace("{ERROR}", "Clave incorrecta"))

    @app.get("/logout")
    def logout():
        resp = RedirectResponse("/login")
        resp.delete_cookie("coronel_sesion")
        return resp
