"""
Rate limiting para FastAPI usando slowapi.

Configuración:
- /api/auth/login : 10 req/min por IP (protección contra brute force)
- /api/* (general) : 120 req/min por IP
- /webhooks/meta   : 300 req/min por IP (Meta puede mandar ráfagas)

El limiter se basa en la IP del request. En Render, la IP real llega
en X-Forwarded-For (el proxy de Render la pone). slowapi la lee
automáticamente si se configura key_func con get_remote_address.
"""
from __future__ import annotations

import logging
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


log = logging.getLogger("rate_limit")

# Configurable por env. Formato slowapi: "120/minute", "10/minute", etc.
RATE_GENERAL = os.environ.get("RATE_LIMIT_GENERAL", "120/minute")
RATE_LOGIN = os.environ.get("RATE_LIMIT_LOGIN", "10/minute")
RATE_WEBHOOK = os.environ.get("RATE_LIMIT_WEBHOOK", "300/minute")


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[RATE_GENERAL],
    storage_uri="memory://",  # En memoria, se resetea con deploys. Fino para este volumen.
)


def setup_rate_limiting(app: FastAPI) -> None:
    """Engancha el limiter a la app FastAPI."""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _custom_rate_limit_handler)


async def _custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Handler customizado para devolver JSON (no HTML)."""
    log.warning(
        "Rate limit excedido: %s %s desde %s",
        request.method,
        request.url.path,
        get_remote_address(request),
    )
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Demasiadas solicitudes. Esperá un momento antes de reintentar.",
            "retry_after": str(exc.detail),
        },
    )
