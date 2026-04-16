"""
Memoria conversacional del bot.

- Una sesión por (canal, sesion_id), donde sesion_id es el wa_id de
  WhatsApp o el IGSID de Instagram.
- Las sesiones se identifican automáticamente cuando llega un mensaje.
- Guardamos los últimos N mensajes por sesión; más viejos se pueden
  borrar para contener el tamaño de la DB.
- Deduplicación: los message_ids de Meta se guardan en
  bot_mensajes_procesados para que un reenvío no dispare 2 respuestas.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import conectar


# Cantidad de turnos (user+assistant) que el bot "recuerda" en el
# contexto. Por encima de esto, los mensajes viejos no se envían a Claude.
MEMORIA_N_TURNOS = int(os.environ.get("BOT_MEMORIA_TURNOS", "8"))

# Expiración "blanda": si pasaron X horas sin mensajes, el próximo
# mensaje arranca una conversación fresca (no toma en cuenta historial
# viejo, pero la sesión en DB se mantiene para métricas).
RESET_SI_PASARON_HORAS = int(os.environ.get("BOT_RESET_HORAS", "24"))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def obtener_sesion(
    canal: str,
    sesion_id: str,
    telefono: str = "",
    nombre_cliente: str = "",
) -> dict:
    """
    Devuelve la sesión. Si no existe, la crea.
    Si existe, actualiza ultima_actividad y nombre (si vino uno nuevo).
    """
    conn = conectar()
    try:
        row = conn.execute(
            "SELECT * FROM bot_sesiones WHERE canal = ? AND sesion_id = ?",
            (canal, sesion_id),
        ).fetchone()

        ahora = _now_iso()
        if row:
            d = dict(row)
            # Actualizar metadata si llegó info nueva
            updates = {"ultima_actividad": ahora}
            if nombre_cliente and not d.get("nombre_cliente"):
                updates["nombre_cliente"] = nombre_cliente
            if telefono and not d.get("telefono"):
                updates["telefono"] = telefono
            if updates:
                sets = ", ".join(f"{k} = ?" for k in updates)
                conn.execute(
                    f"UPDATE bot_sesiones SET {sets} WHERE id = ?",
                    list(updates.values()) + [d["id"]],
                )
                conn.commit()
                d.update(updates)
            return d

        # Crear nueva sesión. Intentamos linkear con tabla clientes si
        # el teléfono matchea.
        cliente_id = None
        if telefono:
            try:
                clt = conn.execute(
                    "SELECT id FROM clientes WHERE telefono = ? LIMIT 1",
                    (telefono,),
                ).fetchone()
                if clt:
                    cliente_id = dict(clt)["id"]
            except Exception:
                pass

        conn.execute(
            """INSERT INTO bot_sesiones
               (canal, sesion_id, telefono, nombre_cliente, cliente_id,
                iniciada_en, ultima_actividad)
               VALUES (?,?,?,?,?,?,?)""",
            (canal, sesion_id, telefono, nombre_cliente, cliente_id, ahora, ahora),
        )
        conn.commit()

        nueva = conn.execute(
            "SELECT * FROM bot_sesiones WHERE canal = ? AND sesion_id = ?",
            (canal, sesion_id),
        ).fetchone()
        return dict(nueva)
    finally:
        conn.close()


def agregar_mensaje(sesion_id_db: int, rol: str, contenido: str,
                    metadata: Optional[str] = None) -> None:
    """Guarda un mensaje en el historial de una sesión."""
    if rol not in ("user", "assistant", "system"):
        raise ValueError(f"rol inválido: {rol}")
    conn = conectar()
    try:
        conn.execute(
            """INSERT INTO bot_conversaciones
               (sesion_id, fecha, rol, contenido, metadata)
               VALUES (?,?,?,?,?)""",
            (int(sesion_id_db), _now_iso(), rol, contenido, metadata),
        )
        conn.commit()
    finally:
        conn.close()


def ultimos_mensajes(sesion_id_db: int, n_turnos: Optional[int] = None) -> list[dict]:
    """
    Últimos N turnos (cada turno = 1 user + 1 assistant, aproximadamente)
    como lista ordenada cronológicamente. Si pasó demasiado tiempo desde
    el último mensaje, devuelve lista vacía (reinicia la conversación).
    """
    n = (n_turnos or MEMORIA_N_TURNOS) * 2  # user + assistant

    conn = conectar()
    try:
        # ¿Expiró la sesión por inactividad?
        ult = conn.execute(
            "SELECT MAX(fecha) FROM bot_conversaciones WHERE sesion_id = ?",
            (int(sesion_id_db),),
        ).fetchone()
        ult_fecha = dict(ult).get("MAX(fecha)") if ult else None
        if ult_fecha:
            try:
                dt = datetime.fromisoformat(ult_fecha)
                horas = (datetime.now(timezone.utc) - dt).total_seconds() / 3600
                if horas > RESET_SI_PASARON_HORAS:
                    return []
            except Exception:
                pass

        filas = conn.execute(
            """SELECT rol, contenido, fecha FROM bot_conversaciones
               WHERE sesion_id = ?
               ORDER BY fecha DESC
               LIMIT ?""",
            (int(sesion_id_db), n),
        ).fetchall()
        # Invertir para orden cronológico ascendente
        return [dict(f) for f in reversed(list(filas))]
    finally:
        conn.close()


# ─── Dedupe de webhooks ─────────────────────────────────────

def ya_procesado(message_id: str) -> bool:
    """True si el message_id ya fue procesado antes."""
    if not message_id:
        return False
    conn = conectar()
    try:
        row = conn.execute(
            "SELECT 1 FROM bot_mensajes_procesados WHERE message_id = ? LIMIT 1",
            (message_id,),
        ).fetchone()
        return row is not None
    finally:
        conn.close()


def marcar_procesado(message_id: str) -> None:
    if not message_id:
        return
    conn = conectar()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO bot_mensajes_procesados (message_id, procesado_en) "
            "VALUES (?, ?)",
            (message_id, _now_iso()),
        )
        conn.commit()
    except Exception:
        # Si la constraint de uniqueness la rechaza, está bien — ya está.
        pass
    finally:
        conn.close()


def purgar_procesados_viejos(dias: int = 30) -> int:
    """Borra registros de dedupe más viejos que N días."""
    from datetime import timedelta
    corte = (datetime.now(timezone.utc) - timedelta(days=dias)).isoformat()
    conn = conectar()
    try:
        conn.execute(
            "DELETE FROM bot_mensajes_procesados WHERE procesado_en < ?",
            (corte,),
        )
        conn.commit()
        return 0
    finally:
        conn.close()
