"""
Endpoints de administración del sistema.

TODOS requieren rol admin. Los GETs mutativos del código anterior fueron
eliminados — sólo POST acepta cambios de estado.

Cambios respecto a la versión anterior:
- Quitados los hashes MD5 hardcodeados de "1234".
- `crear-usuarios` ahora usa bcrypt y recibe las passwords por body (ya
  no reinicia a "1234").
- Todos los endpoints requieren Depends(require_admin).
- Sólo POST, nunca GET.
"""
from __future__ import annotations

import json
import os
import sys
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import conectar, USE_PG
from security import require_admin
from security.passwords import hash_password, validar_fortaleza


router = APIRouter(prefix="/api/admin", tags=["admin"])


JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "inventario_clean.json")


# ─── Fix encoding (strings con mojibake heredadas de imports viejos) ──

FIXES = [
    ("Ã±", "ñ"), ("Ã\x91", "Ñ"),
    ("Ã¡", "á"), ("Ã©", "é"), ("Ã­", "í"), ("Ã³", "ó"), ("Ãº", "ú"),
    ("Ã\x81", "Á"), ("Ã\x89", "É"), ("Ã\x8d", "Í"), ("Ã\"", "Ó"), ("Ã\x9a", "Ú"),
    ("\u00c2\u00b0", "\u00b0"),
    ("\u00c2\u00bf", "\u00bf"),
    ("\u00c2\u00a1", "\u00a1"),
]


def _fix_text(t):
    if not t:
        return t
    for malo, bueno in FIXES:
        t = t.replace(malo, bueno)
    return t


# ─── Modelos ───────────────────────────────────────────────

class UsuarioInicial(BaseModel):
    username: str
    nombre: str
    password: str
    rol: str = "facturacion"


class CrearUsuariosReq(BaseModel):
    usuarios: List[UsuarioInicial]


# ─── Endpoints ─────────────────────────────────────────────

@router.post("/fix-tablas")
def fix_tablas(u: dict = Depends(require_admin)):
    """
    Crea tablas y columnas faltantes. Idempotente.
    Sólo admin.
    """
    conn = conectar()
    try:
        if USE_PG:
            statements = [
                """CREATE TABLE IF NOT EXISTS numeracion_afip (
                    id SERIAL PRIMARY KEY, tipo TEXT UNIQUE NOT NULL,
                    punto_venta TEXT DEFAULT '0001', ultimo_num INTEGER DEFAULT 0
                )""",
                """CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL,
                    nombre TEXT NOT NULL, password_hash TEXT NOT NULL,
                    rol TEXT DEFAULT 'facturacion', activo INTEGER DEFAULT 1,
                    debe_cambiar_password INTEGER DEFAULT 0,
                    creado_en TEXT DEFAULT NOW()::TEXT
                )""",
                """CREATE TABLE IF NOT EXISTS sesiones (
                    token TEXT PRIMARY KEY, user_id INTEGER NOT NULL,
                    username TEXT NOT NULL, rol TEXT NOT NULL, nombre TEXT NOT NULL,
                    ip TEXT DEFAULT '', user_agent TEXT DEFAULT '',
                    creado_en TEXT NOT NULL, expira_en TEXT NOT NULL,
                    ultima_actividad TEXT NOT NULL
                )""",
                """CREATE TABLE IF NOT EXISTS auditoria (
                    id SERIAL PRIMARY KEY, fecha TEXT DEFAULT NOW()::TEXT,
                    user_id INTEGER, username TEXT, rol TEXT,
                    accion TEXT NOT NULL, recurso TEXT, detalle TEXT,
                    ip TEXT, exito INTEGER DEFAULT 1
                )""",
                """CREATE TABLE IF NOT EXISTS cuenta_corriente (
                    id SERIAL PRIMARY KEY, cliente_id INTEGER, cliente_nombre TEXT NOT NULL,
                    comprobante_id INTEGER, tipo TEXT NOT NULL, concepto TEXT NOT NULL,
                    monto REAL NOT NULL, saldo_post REAL NOT NULL, fecha TEXT,
                    forma_cobro TEXT, creado_en TEXT DEFAULT NOW()::TEXT
                )""",
                """CREATE TABLE IF NOT EXISTS caja_sesiones (
                    id SERIAL PRIMARY KEY, fecha TEXT NOT NULL, apertura TEXT,
                    cierre TEXT, saldo_inicial REAL DEFAULT 0, saldo_final REAL,
                    total_ingresos REAL DEFAULT 0, total_egresos REAL DEFAULT 0,
                    estado TEXT DEFAULT 'abierta', creado_en TEXT DEFAULT NOW()::TEXT
                )""",
                """CREATE TABLE IF NOT EXISTS caja_movimientos (
                    id SERIAL PRIMARY KEY, sesion_id INTEGER, tipo TEXT NOT NULL,
                    descripcion TEXT, monto REAL DEFAULT 0, comprobante_id INTEGER,
                    creado_en TEXT DEFAULT NOW()::TEXT
                )""",
                """CREATE TABLE IF NOT EXISTS compras (
                    id SERIAL PRIMARY KEY, numero TEXT, proveedor TEXT NOT NULL,
                    fecha TEXT, total REAL DEFAULT 0, estado TEXT DEFAULT 'pendiente',
                    notas TEXT, creado_en TEXT DEFAULT NOW()::TEXT
                )""",
                """CREATE TABLE IF NOT EXISTS compra_items (
                    id SERIAL PRIMARY KEY, compra_id INTEGER, producto_id INTEGER,
                    producto_desc TEXT, cantidad REAL, precio_costo REAL, subtotal REAL
                )""",
            ]
            for sql in statements:
                try:
                    conn.execute(sql)
                except Exception:
                    pass

            for tipo in ["factura", "presupuesto", "remito", "nota_credito"]:
                try:
                    conn.execute(
                        "INSERT INTO numeracion_afip (tipo, punto_venta, ultimo_num) "
                        "VALUES (%s,%s,%s) ON CONFLICT (tipo) DO NOTHING",
                        (tipo, "0001", 0),
                    )
                except Exception:
                    pass

            for col, tipo in [
                ("ean", "TEXT DEFAULT ''"),
                ("foto_url", "TEXT DEFAULT ''"),
                ("precio_mayorista", "REAL DEFAULT 0"),
            ]:
                try:
                    conn.execute(f"ALTER TABLE productos ADD COLUMN {col} {tipo}")
                except Exception:
                    pass

            try:
                conn.execute(
                    "ALTER TABLE comprobantes ADD COLUMN forma_pago TEXT DEFAULT 'efectivo'"
                )
            except Exception:
                pass

            try:
                conn.execute(
                    "ALTER TABLE usuarios ADD COLUMN debe_cambiar_password INTEGER DEFAULT 0"
                )
            except Exception:
                pass

        else:
            import sqlite3 as _sq
            from db.database import DB_PATH

            raw = _sq.connect(DB_PATH)
            raw.execute(
                """CREATE TABLE IF NOT EXISTS numeracion_afip (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, tipo TEXT UNIQUE NOT NULL,
                    punto_venta TEXT DEFAULT '0001', ultimo_num INTEGER DEFAULT 0
                )"""
            )
            raw.execute(
                """CREATE TABLE IF NOT EXISTS sesiones (
                    token TEXT PRIMARY KEY, user_id INTEGER NOT NULL,
                    username TEXT NOT NULL, rol TEXT NOT NULL, nombre TEXT NOT NULL,
                    ip TEXT DEFAULT '', user_agent TEXT DEFAULT '',
                    creado_en TEXT NOT NULL, expira_en TEXT NOT NULL,
                    ultima_actividad TEXT NOT NULL
                )"""
            )
            raw.execute(
                """CREATE TABLE IF NOT EXISTS auditoria (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT DEFAULT (datetime('now','localtime')),
                    user_id INTEGER, username TEXT, rol TEXT,
                    accion TEXT NOT NULL, recurso TEXT, detalle TEXT,
                    ip TEXT, exito INTEGER DEFAULT 1
                )"""
            )
            for tipo in ["factura", "presupuesto", "remito", "nota_credito"]:
                raw.execute(
                    "INSERT OR IGNORE INTO numeracion_afip (tipo,punto_venta,ultimo_num) "
                    "VALUES (?,?,?)",
                    (tipo, "0001", 0),
                )
            for col, tipo in [
                ("ean", "TEXT DEFAULT ''"),
                ("foto_url", "TEXT DEFAULT ''"),
                ("precio_mayorista", "REAL DEFAULT 0"),
            ]:
                try:
                    raw.execute(f"ALTER TABLE productos ADD COLUMN {col} {tipo}")
                except Exception:
                    pass
            try:
                raw.execute(
                    "ALTER TABLE comprobantes ADD COLUMN forma_pago TEXT DEFAULT 'efectivo'"
                )
            except Exception:
                pass
            try:
                raw.execute(
                    "ALTER TABLE usuarios ADD COLUMN debe_cambiar_password INTEGER DEFAULT 0"
                )
            except Exception:
                pass
            raw.commit()
            raw.close()

        conn.commit()
        return {"ok": True, "mensaje": "Tablas creadas y columnas agregadas correctamente"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        conn.close()


@router.post("/reimportar-inventario")
def reimportar_inventario(
    offset: int = 0,
    lote: int = 500,
    u: dict = Depends(require_admin),
):
    """Reimporta inventario en lotes. Sólo admin."""
    if not os.path.exists(JSON_PATH):
        return {"ok": False, "error": "inventario_clean.json no encontrado"}

    with open(JSON_PATH, encoding="utf-8") as f:
        todos = json.load(f)

    productos = todos[offset: offset + lote]
    if not productos:
        return {"ok": True, "mensaje": "Completado", "total": len(todos), "offset": offset}

    conn = conectar()
    try:
        actualizados = 0
        nuevos = 0
        for p in productos:
            existe = conn.execute(
                "SELECT id FROM productos WHERE codigo = ?", (p["codigo"],)
            ).fetchone()
            if existe:
                conn.execute(
                    """UPDATE productos SET
                       descripcion=?, rubro=?, proveedor=?,
                       precio_costo=?, precio_venta=?, stock=?
                       WHERE codigo=?""",
                    (
                        p["descripcion"], p["rubro"], p["proveedor"],
                        p["precio_costo"], p["precio_venta"], p["stock"],
                        p["codigo"],
                    ),
                )
                actualizados += 1
            else:
                conn.execute(
                    """INSERT INTO productos
                       (codigo, descripcion, rubro, proveedor, precio_costo, precio_venta, stock, activo)
                       VALUES (?,?,?,?,?,?,?,1)""",
                    (
                        p["codigo"], p["descripcion"], p["rubro"], p["proveedor"],
                        p["precio_costo"], p["precio_venta"], p["stock"],
                    ),
                )
                nuevos += 1
        conn.commit()
        siguiente = offset + lote
        hay_mas = siguiente < len(todos)
        return {
            "ok": True,
            "actualizados": actualizados,
            "nuevos": nuevos,
            "offset": offset,
            "siguiente_offset": siguiente if hay_mas else None,
            "total": len(todos),
            "completado": not hay_mas,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        conn.close()


@router.post("/fix-encoding")
def fix_encoding(u: dict = Depends(require_admin)):
    """Corrige mojibake en strings de la DB. Sólo admin."""
    conn = conectar()
    try:
        tablas = {
            "productos":         ["descripcion", "rubro", "proveedor"],
            "ventas_historicas": ["producto_desc", "rubro"],
            "clientes":          ["nombre", "direccion"],
            "comprobantes":      ["cliente_nombre"],
        }
        total = 0
        for tabla, cols in tablas.items():
            try:
                filas = conn.execute(
                    f"SELECT id, {', '.join(cols)} FROM {tabla}"
                ).fetchall()
                for fila in filas:
                    updates = {}
                    for col in cols:
                        val = fila[col]
                        fixed = _fix_text(val)
                        if fixed != val:
                            updates[col] = fixed
                    if updates:
                        sets = ", ".join(f"{c}=?" for c in updates)
                        conn.execute(
                            f"UPDATE {tabla} SET {sets} WHERE id=?",
                            list(updates.values()) + [fila["id"]],
                        )
                        total += 1
            except Exception:
                pass
        conn.commit()
        return {"ok": True, "total_corregidos": total}
    finally:
        conn.close()


@router.post("/crear-usuarios")
def crear_usuarios(data: CrearUsuariosReq, u: dict = Depends(require_admin)):
    """
    Crea o actualiza usuarios con passwords provistas en el body.
    Ya NO resetea a "1234" — cada password la definís vos al llamar.
    Todas las passwords se validan contra la política de fortaleza.
    Se setea debe_cambiar_password=0 si la creaste vos (confiás).
    """
    if not data.usuarios:
        raise HTTPException(status_code=400, detail="Lista de usuarios vacía")

    for usr in data.usuarios:
        ok, motivo = validar_fortaleza(usr.password)
        if not ok:
            raise HTTPException(
                status_code=400,
                detail=f"Usuario '{usr.username}': {motivo}",
            )
        if usr.rol not in {"admin", "facturacion", "crm", "bot"}:
            raise HTTPException(
                status_code=400,
                detail=f"Usuario '{usr.username}': rol inválido",
            )

    conn = conectar()
    try:
        resultado = []
        for usr in data.usuarios:
            username = usr.username.lower().strip()
            pwd_hash = hash_password(usr.password)
            existe = conn.execute(
                "SELECT id FROM usuarios WHERE username = ?", (username,)
            ).fetchone()
            if existe:
                conn.execute(
                    """UPDATE usuarios
                       SET password_hash=?, nombre=?, rol=?, debe_cambiar_password=0
                       WHERE username=?""",
                    (pwd_hash, usr.nombre, usr.rol, username),
                )
                resultado.append({"username": username, "accion": "actualizado"})
            else:
                conn.execute(
                    """INSERT INTO usuarios
                       (username, nombre, password_hash, rol, activo, debe_cambiar_password)
                       VALUES (?,?,?,?,1,0)""",
                    (username, usr.nombre, pwd_hash, usr.rol),
                )
                resultado.append({"username": username, "accion": "creado"})
        conn.commit()
        return {"ok": True, "usuarios": resultado}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        conn.close()


@router.post("/limpiar-sesiones")
def limpiar_sesiones(u: dict = Depends(require_admin)):
    """Borra sesiones expiradas. Útil como cron manual."""
    from security.sessions import limpiar_sesiones_expiradas
    n = limpiar_sesiones_expiradas()
    return {"ok": True, "sesiones_borradas": n}
