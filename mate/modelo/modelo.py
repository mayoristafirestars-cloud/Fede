# Adaptador para un modelo propio (una IA que no es la que trae Mate).
#
# Esto NO es Mate: es Python. Desde un programa de Mate se trae con
#     usar python "modelo/modelo.py"
# y se usa así:
#     sea contestado = modelo.pedir_al_modelo("Elegí el producto.", "la cinta de 5 m")
#     sea dato = de_json(contestado)         # un mapa, por ejemplo {producto: "cinta_5m"}
#
# El acuerdo es uno solo: pedir_al_modelo(instrucciones, pregunta) devuelve SIEMPRE un texto
# JSON que describe un objeto, como {"producto":"cinta_5m"}. Si el modelo contesta otra cosa,
# o no se puede llegar hasta él, la función falla con un error claro que desde Mate se ataja
# con 'intentar'.
#
# A qué modelo le pide:
#   - Sin configurar nada, a uno SIMULADO: no sale a internet y no gasta.
#   - A uno de verdad, cuando existe la variable de entorno MATE_MODELO_PROPIO_URL con la
#     dirección de un servicio que habla como "chat completions" (Ollama, LM Studio,
#     llama.cpp, vLLM y muchos otros). En PowerShell:
#         $env:MATE_MODELO_PROPIO_URL = "http://localhost:11434/v1/chat/completions"
#         $env:MATE_MODELO_PROPIO_NOMBRE = "el-nombre-de-tu-modelo"
#     Si el servicio pide clave, va en MATE_MODELO_PROPIO_CLAVE. La clave nunca se escribe
#     en un programa ni en este archivo, y este archivo nunca la muestra.
#   - Con MATE_MODELO_PROPIO_SIMULADO=1 se usa el simulado aunque haya dirección.
#
# OJO: con una dirección configurada, también la orden 'probar' sale a buscar al modelo.
# En las pruebas llamá primero a modelo.simular_modelo([...]): desde ahí no se usa la red.

import json
import os
import socket
import urllib.error
import urllib.request

ESPERA_EN_SEGUNDOS = 60
FALLA_DE_CONEXION = "!conexion"

_respuestas_simuladas = None
_pedidos = []


def pedir_al_modelo(instrucciones, pregunta):
    """Le pide al modelo y devuelve un texto JSON que describe un objeto."""
    if not isinstance(instrucciones, str) or not isinstance(pregunta, str):
        raise TypeError("pedir_al_modelo lleva dos textos: las instrucciones y la pregunta")
    if _usa_simulado():
        crudo = _pedir_al_simulado(instrucciones, pregunta)
    else:
        crudo = _pedir_al_servicio(instrucciones, pregunta)
    limpio = _dejar_json_valido(crudo)
    _pedidos.append({"instrucciones": instrucciones, "pregunta": pregunta, "respuesta": limpio})
    return limpio


def simular_modelo(respuestas):
    """Deja preparado lo que va a contestar el modelo simulado, en orden.

    Recibe una lista de textos. El texto "!conexion" simula que no se pudo llegar al modelo.
    Desde que se llama, no se usa la red aunque haya una dirección configurada. Con una
    lista vacía vuelve a la respuesta simulada de siempre. Borra la cuenta de pedidos.
    """
    global _respuestas_simuladas
    if not isinstance(respuestas, list) or not all(isinstance(r, str) for r in respuestas):
        raise TypeError("simular_modelo lleva una lista de textos")
    _respuestas_simuladas = list(respuestas)
    _pedidos.clear()
    return len(_respuestas_simuladas)


def pedidos_al_modelo():
    """Lo que se le pidió al modelo hasta ahora: instrucciones, pregunta y respuesta."""
    return [dict(p) for p in _pedidos]


def proveedor():
    """Dice a quién le pide: "simulado" o "propio"."""
    return "simulado" if _usa_simulado() else "propio"


def _usa_simulado():
    if _respuestas_simuladas is not None:
        return True
    if os.environ.get("MATE_MODELO_PROPIO_SIMULADO", "").strip() not in ("", "0"):
        return True
    return not os.environ.get("MATE_MODELO_PROPIO_URL", "").strip()


def _pedir_al_simulado(instrucciones, pregunta):
    if _respuestas_simuladas:
        respuesta = _respuestas_simuladas.pop(0)
        if respuesta == FALLA_DE_CONEXION:
            raise ConnectionError("no se pudo llegar al modelo (falla simulada)")
        return respuesta
    return json.dumps({"simulado": True, "pregunta": pregunta}, ensure_ascii=False)


def _pedir_al_servicio(instrucciones, pregunta):
    direccion = os.environ.get("MATE_MODELO_PROPIO_URL", "").strip()
    if not direccion.lower().startswith(("http://", "https://")):
        raise ValueError("MATE_MODELO_PROPIO_URL tiene que empezar con http:// o https://")
    clave = os.environ.get("MATE_MODELO_PROPIO_CLAVE", "").strip()
    cuerpo = {
        "model": os.environ.get("MATE_MODELO_PROPIO_NOMBRE", "").strip() or "modelo",
        "messages": [
            {"role": "system", "content": instrucciones + "\nContestá solo con un objeto JSON."},
            {"role": "user", "content": pregunta},
        ],
        "temperature": 0,
    }
    encabezados = {"Content-Type": "application/json"}
    if clave:
        encabezados["Authorization"] = "Bearer " + clave
    pedido = urllib.request.Request(
        direccion, data=json.dumps(cuerpo).encode("utf-8"), headers=encabezados, method="POST")
    try:
        with urllib.request.urlopen(pedido, timeout=ESPERA_EN_SEGUNDOS) as respuesta:
            recibido = respuesta.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        raise ConnectionError(
            "el modelo contestó con el error %s. Revisá la dirección, el nombre del modelo "
            "y la clave" % error.code) from None
    except (urllib.error.URLError, socket.timeout, TimeoutError, OSError) as error:
        motivo = _tapar(str(getattr(error, "reason", error)), clave)
        raise ConnectionError(
            "no se pudo llegar al modelo en %s (%s). ¿Está prendido?"
            % (_sin_datos_de_acceso(direccion), motivo)) from None
    try:
        return json.loads(recibido)["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        raise ValueError(
            "el servicio contestó con una forma que no conozco (esperaba la de "
            "'chat completions'): " + _recortar(_tapar(recibido, clave))) from None


def _dejar_json_valido(crudo):
    if not isinstance(crudo, str) or not crudo.strip():
        raise ValueError("el modelo no contestó nada")
    texto = crudo.strip()
    if texto.startswith("```"):
        renglones = texto.splitlines()[1:]
        if renglones and renglones[-1].strip().startswith("```"):
            renglones = renglones[:-1]
        texto = "\n".join(renglones).strip()
    try:
        dato = json.loads(texto)
    except ValueError:
        raise ValueError(
            "el modelo contestó algo que no es JSON: " + _recortar(crudo)) from None
    if not isinstance(dato, dict):
        raise ValueError(
            "el modelo contestó un JSON que no es un objeto entre llaves: " + _recortar(crudo))
    return json.dumps(dato, ensure_ascii=False, separators=(",", ":"))


def _recortar(texto, largo=120):
    texto = " ".join(str(texto).split())
    return texto if len(texto) <= largo else texto[:largo] + "..."


def _tapar(texto, clave):
    return texto.replace(clave, "<clave>") if clave else texto


def _sin_datos_de_acceso(direccion):
    """La dirección sin usuario y contraseña (http://usuario:clave@lugar) ni lo que va después de '?'."""
    direccion = direccion.split("?", 1)[0]
    if "@" in direccion and "://" in direccion:
        protocolo, resto = direccion.split("://", 1)
        direccion = protocolo + "://" + resto.split("@", 1)[1]
    return direccion
