"""
FASE 2 — El bucle agéntico: Claude usa herramientas que VOS ejecutás.

Este ejemplo muestra el bucle A MANO para que entiendas qué pasa por dentro.
(El SDK tiene un atajo, el "tool runner", pero primero conviene ver el mecanismo.)

El ciclo es:
    1. Le mandás mensajes + definiciones de herramientas
    2. Si Claude quiere usar una herramienta, responde con stop_reason == "tool_use"
    3. Tu código ejecuta la herramienta y le devuelve el resultado (tool_result)
    4. Repetís hasta que Claude termina (stop_reason == "end_turn")

Ejecutar:
    python 02_agente_con_herramientas.py
"""

import json
from datetime import date

import anthropic

client = anthropic.Anthropic()
MODELO = "claude-opus-4-8"

# ------------------------------------------------------------------
# 1. Definir las herramientas (nombre + descripción + parámetros)
# ------------------------------------------------------------------
# La DESCRIPCIÓN es clave: Claude la lee para decidir cuándo usar cada una.
HERRAMIENTAS = [
    {
        "name": "obtener_fecha_hoy",
        "description": "Devuelve la fecha de hoy. Usala cuando la pregunta "
                       "dependa de la fecha actual.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "calcular_precio_con_iva",
        "description": "Calcula el precio final con IVA (21%) a partir de un "
                       "precio neto. Usala para cualquier cálculo de IVA.",
        "input_schema": {
            "type": "object",
            "properties": {
                "precio_neto": {
                    "type": "number",
                    "description": "Precio sin IVA, en pesos",
                }
            },
            "required": ["precio_neto"],
        },
    },
]


# ------------------------------------------------------------------
# 2. Implementar las herramientas (funciones Python comunes)
# ------------------------------------------------------------------
def ejecutar_herramienta(nombre: str, entrada: dict) -> str:
    if nombre == "obtener_fecha_hoy":
        return date.today().isoformat()
    if nombre == "calcular_precio_con_iva":
        neto = float(entrada["precio_neto"])
        return f"${neto * 1.21:,.2f} (neto ${neto:,.2f} + IVA 21%)"
    return f"Error: herramienta desconocida '{nombre}'"


# ------------------------------------------------------------------
# 3. El bucle agéntico
# ------------------------------------------------------------------
def agente(pregunta: str) -> str:
    mensajes = [{"role": "user", "content": pregunta}]

    while True:
        respuesta = client.messages.create(
            model=MODELO,
            max_tokens=2048,
            tools=HERRAMIENTAS,
            messages=mensajes,
        )

        # Si no pidió herramientas, terminó: devolvemos el texto final
        if respuesta.stop_reason != "tool_use":
            return next(
                (b.text for b in respuesta.content if b.type == "text"), ""
            )

        # Pidió una o más herramientas:
        # a) agregamos SU respuesta al historial (con los bloques tool_use)
        mensajes.append({"role": "assistant", "content": respuesta.content})

        # b) ejecutamos cada herramienta y juntamos los resultados
        resultados = []
        for bloque in respuesta.content:
            if bloque.type == "tool_use":
                print(f"  [usando herramienta: {bloque.name}({json.dumps(bloque.input)})]")
                salida = ejecutar_herramienta(bloque.name, bloque.input)
                resultados.append({
                    "type": "tool_result",
                    "tool_use_id": bloque.id,  # tiene que coincidir con el id del pedido
                    "content": salida,
                })

        # c) le devolvemos TODOS los resultados en UN solo mensaje de usuario
        mensajes.append({"role": "user", "content": resultados})
        # ...y el while vuelve a llamar a la API con el historial actualizado


if __name__ == "__main__":
    print(agente("Si un producto sale $10.000 neto, ¿cuánto paga el cliente con IVA? "
                 "¿Y qué fecha es hoy?"))
