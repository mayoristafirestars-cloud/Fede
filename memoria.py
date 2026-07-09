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
