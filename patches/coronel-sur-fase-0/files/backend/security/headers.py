"""
Middleware de headers de seguridad HTTP.

Aplica headers defensivos a todas las respuestas:
- HSTS: fuerza HTTPS por 1 año.
- X-Content-Type-Options: evita MIME sniffing.
- X-Frame-Options: evita que el sitio sea embebido (clickjacking).
- Referrer-Policy: no filtrar URLs a terceros.
- Content-Security-Policy: limita de dónde se pueden cargar recursos.
- Permissions-Policy: apaga features del browser que no usamos.
"""
from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


# CSP permisiva para empezar (permite Cloudinary, Google Fonts, etc.).
# En Fase 4 cuando tengamos design system fijo, la apretamos más.
_CSP_DEFAULT = (
    "default-src 'self'; "
    "img-src 'self' data: blob: https://res.cloudinary.com https://*.googleusercontent.com; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com data:; "
    "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
    "connect-src 'self' https://api.cloudinary.com https://api.anthropic.com; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    "form-action 'self'"
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, csp: str = _CSP_DEFAULT, hsts_seconds: int = 31536000):
        super().__init__(app)
        self.csp = csp
        self.hsts = f"max-age={hsts_seconds}; includeSubDomains"

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        h = response.headers
        h.setdefault("Strict-Transport-Security", self.hsts)
        h.setdefault("X-Content-Type-Options", "nosniff")
        h.setdefault("X-Frame-Options", "DENY")
        h.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        h.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        h.setdefault("Content-Security-Policy", self.csp)
        # Cache: por defecto, no cachear respuestas autenticadas
        if request.url.path.startswith("/api/"):
            h.setdefault("Cache-Control", "no-store")
        return response
