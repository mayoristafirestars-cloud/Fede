"""Access boundary for an Internet-facing installation."""
import os
import re
from urllib.parse import urlsplit
from fastapi import HTTPException
from starlette.responses import JSONResponse, RedirectResponse
from routers.comercial import actor
from routers.preparacion import database


def production():
    return os.environ.get('NATIVA_ENV') == 'production'


def public_host(request):
    hosts = os.environ.get('NATIVA_PUBLIC_HOSTS', 'nativa.ar,www.nativa.ar').split(',')
    return (request.url.hostname or '').lower() in {h.strip().lower() for h in hosts if h.strip()}


def storefront_path(path):
    return path in ('/tienda', '/tienda/pedido', '/api/tienda/catalogo', '/api/tienda/pedidos') or bool(re.fullmatch(
        r'/api/tienda/(productos/[0-9]+/foto|pedidos/[0-9a-f-]{36}(/(aprobacion|repetir|reclamos|cancelacion))?)', path))


async def protect(request, call_next):
    if not production():
        return await call_next(request)
    path = request.url.path
    store = storefront_path(path)
    if public_host(request) and not (store or path in ('/', '/healthz') or path.startswith('/static/tienda')):
        return JSONResponse({'detail': 'No encontrado'}, status_code=404)
    public = store or (public_host(request) and path == '/') or path in ('/login', '/healthz', '/api/comercial/sesion', '/api/comercial/autorizacion') or path.startswith('/static/')
    if request.method not in ('GET', 'HEAD', 'OPTIONS'):
        origin = request.headers.get('origin')
        if origin:
            parsed = urlsplit(origin)
            if parsed.scheme != 'https' or parsed.netloc != request.headers.get('host'):
                return JSONResponse({'detail': 'Origen no permitido'}, status_code=403)
    if not public:
        try:
            with database() as conn:
                person = actor(conn, request.cookies.get('cs_sesion'))
            if person['rol'] == 'cajero' and request.method not in ('GET', 'HEAD', 'OPTIONS') and not path.startswith('/api/mostrador/'):
                raise HTTPException(403, 'Esta operación requiere dueño o encargada')
        except HTTPException as exc:
            if exc.status_code == 401 and request.method == 'GET' and not path.startswith(('/api/', '/media/')):
                return RedirectResponse('/login', status_code=303)
            return JSONResponse({'detail': exc.detail}, status_code=exc.status_code)
    response = await call_next(request)
    response.headers['Cache-Control'] = 'no-store'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'same-origin'
    return response
