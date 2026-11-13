"""
Usuarios, contraseñas, sesiones y permisos.

- Contraseñas con argon2.
- La sesión es un token aleatorio en una cookie HttpOnly; en la base sólo se
  guarda su HMAC con SECRET_KEY, así un respaldo filtrado no sirve para entrar.
- Protección CSRF por doble envío: cookie cs_csrf + encabezado X-CSRF-Token.
"""

import hashlib
import hmac
import os
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from fastapi import HTTPException, Request

import config
from db.database import conectar

COOKIE_SESION = "cs_sesion"
COOKIE_CSRF = "cs_csrf"
ENCABEZADO_CSRF = "X-CSRF-Token"
MAX_INTENTOS = 5
BLOQUEO_MINUTOS = 15
LARGO_MINIMO = 10
MENSAJE_LOGIN = "Usuario o contraseña incorrectos. Después de 5 intentos fallidos el acceso se bloquea 15 minutos."

ROLES = {"admin", "responsable_cobranza", "cobrador", "consulta"}
TODOS = frozenset(ROLES)

# Qué roles pueden hacer cada acción (matriz de la sección 6 del diseño).
# Emitir y anular comprobantes no están en esa matriz: ver "Decisiones" en el resumen del Hito 0.
PERMISOS = {
    "producto.ver":       TODOS,
    "comprobante.ver":    TODOS,
    "comprobante.emitir": frozenset({"admin", "responsable_cobranza"}),
    "comprobante.anular": frozenset({"admin"}),
    "usuario.gestionar":  frozenset({"admin"}),
}

_hasher = PasswordHasher()
_HASH_FALSO = _hasher.hash("contraseña-de-relleno-para-igualar-tiempos")
_clave_desarrollo = None


@dataclass
class Usuario:
    id: int
    usuario: str
    nombre: str
    empresa_id: int
    roles: frozenset = field(default_factory=frozenset)
    csrf: str = ""


# ─── Utilidades ────────────────────────────────────────────

def ahora() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def secret_key() -> bytes:
    """SECRET_KEY de entorno. En desarrollo, si falta, se genera una temporal."""
    global _clave_desarrollo
    clave = os.environ.get("SECRET_KEY")
    if clave:
        if len(clave) < 32:
            raise RuntimeError("SECRET_KEY debe tener al menos 32 caracteres")
        return clave.encode()
    if config.es_produccion():
        raise RuntimeError("Falta la variable SECRET_KEY (obligatoria en producción)")
    if _clave_desarrollo is None:
        _clave_desarrollo = secrets.token_bytes(32)
        print("⚠️  SECRET_KEY no definida: se usa una clave temporal (las sesiones se pierden al reiniciar).")
    return _clave_desarrollo


def _hmac(token: str) -> str:
    return hmac.new(secret_key(), token.encode(), hashlib.sha256).hexdigest()


def hash_contrasena(contrasena: str) -> str:
    return _hasher.hash(contrasena)


def validar_contrasena_nueva(contrasena: str):
    if len(contrasena) < LARGO_MINIMO:
        raise ValueError(f"La contraseña debe tener al menos {LARGO_MINIMO} caracteres")


# ─── Usuarios ──────────────────────────────────────────────

def crear_usuario(conn, usuario: str, nombre: str, contrasena: str, roles: set, empresa_id: int = 1) -> int:
    """Crea un usuario con sus roles. No hace commit."""
    usuario = usuario.strip().lower()
    if not usuario or not nombre.strip():
        raise ValueError("Usuario y nombre son obligatorios")
    desconocidos = set(roles) - ROLES
    if desconocidos or not roles:
        raise ValueError(f"Roles inválidos: {sorted(desconocidos) or 'ninguno'}")
    validar_contrasena_nueva(contrasena)
    if conn.execute("SELECT 1 FROM usuario WHERE usuario = ?", (usuario,)).fetchone():
        raise ValueError(f"Ya existe el usuario '{usuario}'")
    cur = conn.execute(
        "INSERT INTO usuario (empresa_id, usuario, nombre, hash_contrasena) VALUES (?,?,?,?)",
        (empresa_id, usuario, nombre.strip(), hash_contrasena(contrasena)),
    )
    uid = cur.lastrowid
    for rol in roles:
        conn.execute(
            "INSERT INTO usuario_rol (usuario_id, rol_id) SELECT ?, id FROM rol WHERE codigo = ?",
            (uid, rol),
        )
    return uid


def _roles_de(conn, usuario_id: int) -> frozenset:
    filas = conn.execute(
        "SELECT r.codigo FROM usuario_rol ur JOIN rol r ON r.id = ur.rol_id WHERE ur.usuario_id = ?",
        (usuario_id,),
    ).fetchall()
    return frozenset(f[0] for f in filas)


# ─── Login y sesiones ──────────────────────────────────────

def autenticar(conn, usuario: str, contrasena: str) -> tuple[dict | None, str]:
    """
    Verifica credenciales y aplica el bloqueo por intentos.
    Devuelve (fila_usuario | None, motivo) y deja los cambios sin commit.
    motivo: ok | inexistente | inactivo | bloqueado | contrasena
    """
    fila = conn.execute("SELECT * FROM usuario WHERE usuario = ?", (usuario.strip().lower(),)).fetchone()
    if not fila:
        try:
            _hasher.verify(_HASH_FALSO, contrasena)   # mismo tiempo de respuesta
        except VerificationError:
            pass
        return None, "inexistente"
    if fila["bloqueado_hasta"] and datetime.fromisoformat(fila["bloqueado_hasta"]) > ahora():
        return None, "bloqueado"
    try:
        _hasher.verify(fila["hash_contrasena"], contrasena)
    except (VerificationError, InvalidHashError):
        intentos = fila["intentos_fallidos"] + 1
        if intentos >= MAX_INTENTOS:
            conn.execute(
                "UPDATE usuario SET intentos_fallidos = 0, bloqueado_hasta = ? WHERE id = ?",
                (_iso(ahora() + timedelta(minutes=BLOQUEO_MINUTOS)), fila["id"]),
            )
        else:
            conn.execute("UPDATE usuario SET intentos_fallidos = ? WHERE id = ?", (intentos, fila["id"]))
        return None, "contrasena"
    if not fila["activo"]:
        return None, "inactivo"
    if _hasher.check_needs_rehash(fila["hash_contrasena"]):
        conn.execute("UPDATE usuario SET hash_contrasena = ? WHERE id = ?", (hash_contrasena(contrasena), fila["id"]))
    conn.execute(
        "UPDATE usuario SET intentos_fallidos = 0, bloqueado_hasta = NULL, ultimo_acceso = ? WHERE id = ?",
        (_iso(ahora()), fila["id"]),
    )
    return dict(fila), "ok"


def crear_sesion(conn, usuario_id: int, empresa_id: int, ip: str | None) -> tuple[str, str]:
    """Crea la sesión y devuelve (token, csrf). No hace commit."""
    token = secrets.token_urlsafe(32)
    csrf = secrets.token_urlsafe(32)
    conn.execute(
        "INSERT INTO sesion (token_hmac, usuario_id, empresa_id, csrf, creada_en, expira_en, ip) VALUES (?,?,?,?,?,?,?)",
        (_hmac(token), usuario_id, empresa_id, csrf, _iso(ahora()),
         _iso(ahora() + timedelta(hours=config.sesion_horas())), ip),
    )
    return token, csrf


def usuario_de_token(token: str) -> Usuario | None:
    """Usuario de una sesión vigente, o None."""
    if not token:
        return None
    conn = conectar()
    try:
        fila = conn.execute(
            """SELECT s.csrf, s.expira_en, s.revocada, u.id, u.usuario, u.nombre, u.empresa_id, u.activo
               FROM sesion s JOIN usuario u ON u.id = s.usuario_id
               WHERE s.token_hmac = ?""",
            (_hmac(token),),
        ).fetchone()
        if not fila or fila["revocada"] or not fila["activo"]:
            return None
        if datetime.fromisoformat(fila["expira_en"]) <= ahora():
            return None
        return Usuario(fila["id"], fila["usuario"], fila["nombre"], fila["empresa_id"],
                       _roles_de(conn, fila["id"]), fila["csrf"])
    finally:
        conn.close()


def revocar_sesion(conn, token: str):
    conn.execute("UPDATE sesion SET revocada = 1 WHERE token_hmac = ?", (_hmac(token),))


def csrf_valido(request: Request, usuario: Usuario) -> bool:
    enviado = request.headers.get(ENCABEZADO_CSRF, "")
    return bool(enviado) and hmac.compare_digest(enviado, usuario.csrf)


# ─── Permisos ──────────────────────────────────────────────

def requiere(permiso: str):
    """Dependencia de FastAPI: exige sesión y un rol habilitado para el permiso."""
    roles_ok = PERMISOS[permiso]

    def _dependencia(request: Request) -> Usuario:
        usuario = getattr(request.state, "usuario", None)
        if not usuario:
            raise HTTPException(status_code=401, detail="Sesión requerida")
        if not (usuario.roles & roles_ok):
            raise HTTPException(status_code=403, detail="No tenés permiso para esta acción")
        return usuario

    return _dependencia


def ip_de(request: Request) -> str | None:
    return request.client.host if request.client else None
