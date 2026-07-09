"""
Recorte seguro del historial de conversación (compartido por Max y Eva).

Sin esto, cada mensaje nuevo re-envía TODA la conversación a la API:
el costo por respuesta crece sin límite y la RAM también.

El recorte respeta los pares tool_use/tool_result: después de cortar,
el historial nunca puede empezar con un tool_result huérfano (la API
lo rechaza) ni con un mensaje del asistente.
"""


def _tiene_tool_result(mensaje: dict) -> bool:
    contenido = mensaje.get("content")
    if isinstance(contenido, list):
        for bloque in contenido:
            tipo = bloque.get("type") if isinstance(bloque, dict) else getattr(bloque, "type", None)
            if tipo == "tool_result":
                return True
    return False


def recortar_historial(historial: list, max_mensajes: int = 30) -> None:
    """Deja solo los últimos max_mensajes, cortando en un lugar válido.
    Modifica la lista in-place (es la misma que guarda la sesión)."""
    if len(historial) <= max_mensajes:
        return
    del historial[: len(historial) - max_mensajes]
    # El primer mensaje debe ser del usuario y no puede ser un tool_result
    while historial and (
        historial[0].get("role") != "user" or _tiene_tool_result(historial[0])
    ):
        del historial[0]


# ---------- Persistencia de sesiones (sobreviven a reinicios) ----------
import json
import os
import threading

_lock_guardado = threading.Lock()


def _serializar_historial(historial: list) -> list:
    """Convierte los bloques del SDK a dicts JSON-serializables."""
    out = []
    for m in historial:
        contenido = m.get("content")
        if isinstance(contenido, list):
            bloques = []
            for b in contenido:
                if isinstance(b, dict):
                    bloques.append(b)
                else:
                    bloques.append(b.model_dump(exclude_none=True))
            out.append({"role": m["role"], "content": bloques})
        else:
            out.append({"role": m["role"], "content": contenido})
    return out


def cargar_sesiones(ruta) -> dict:
    """Carga las sesiones guardadas (o {} si no hay archivo)."""
    try:
        with open(ruta, encoding="utf-8") as f:
            data = json.load(f)
        print(f"[memoria] {len(data)} sesiones recuperadas de {os.path.basename(str(ruta))}")
        return data
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"[memoria] No pude leer las sesiones guardadas: {e}")
        return {}


def guardar_sesiones(sessions: dict, ruta) -> None:
    """Guarda todas las sesiones a disco en segundo plano (escritura atómica)."""

    def _run():
        with _lock_guardado:
            try:
                data = {k: _serializar_historial(v) for k, v in list(sessions.items())}
                tmp = str(ruta) + ".tmp"
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False)
                os.replace(tmp, str(ruta))
            except Exception as e:
                print(f"[memoria] No pude guardar sesiones: {e}")

    threading.Thread(target=_run, daemon=True).start()
