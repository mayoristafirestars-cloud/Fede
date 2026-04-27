"""
Agente de soporte - Paso 6: con tools.
Sofi puede llamar a buscar_pedido y consultar_stock cuando los necesita.
El loop agéntico: pedido -> Claude pide tool -> Python lo ejecuta ->
Claude recibe resultado -> arma respuesta final al cliente.
"""
import json
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from tools.db import buscar_pedido, consultar_stock

load_dotenv()

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024
MAX_TURNS = 5  # límite de seguridad para evitar loops infinitos

BASE_DIR = Path(__file__).parent
PROMPT_PATH = BASE_DIR / "prompts" / "system_prompt.md"
FAQS_PATH = BASE_DIR / "data" / "faqs.md"
PRODUCTOS_PATH = BASE_DIR / "data" / "productos.md"

client = Anthropic()


def build_system_prompt() -> str:
    persona = PROMPT_PATH.read_text(encoding="utf-8")
    faqs = FAQS_PATH.read_text(encoding="utf-8")
    productos = PRODUCTOS_PATH.read_text(encoding="utf-8")
    return f"""{persona}

---

# BASE DE CONOCIMIENTO — FAQS

{faqs}

---

# BASE DE CONOCIMIENTO — CATÁLOGO

{productos}

---

# TOOLS DISPONIBLES

Tenés acceso a herramientas para consultar datos en tiempo real:

- `buscar_pedido`: usalo cuando el cliente quiera saber el estado de un pedido. Necesitás número de orden + email. Si no te los dio, pedíselos primero.
- `consultar_stock`: usalo para CONFIRMAR stock real antes de prometer disponibilidad. El catálogo dice qué productos/colores/talles existen, pero el stock cambia minuto a minuto.

NUNCA inventes números de orden, tracking, ni unidades de stock. Si no tenés los datos, pedíselos al cliente o usá los tools.
"""


SYSTEM_PROMPT = build_system_prompt()

TOOLS = [
    {
        "name": "buscar_pedido",
        "description": "Busca el estado de un pedido por número de orden y email del cliente. Devuelve estado, tracking, courier y productos del pedido.",
        "input_schema": {
            "type": "object",
            "properties": {
                "numero_orden": {
                    "type": "string",
                    "description": "Número de orden, ej: TRAMA-12345",
                },
                "email": {
                    "type": "string",
                    "description": "Email con el que el cliente hizo la compra",
                },
            },
            "required": ["numero_orden", "email"],
        },
    },
    {
        "name": "consultar_stock",
        "description": "Consulta cuántas unidades hay en stock de un producto en un talle y color específicos.",
        "input_schema": {
            "type": "object",
            "properties": {
                "producto": {
                    "type": "string",
                    "description": "Nombre exacto del producto (ej: 'Buzo Hoodie Classic')",
                },
                "talle": {
                    "type": "string",
                    "description": "Talle: S, M, L, XL o XXL",
                },
                "color": {
                    "type": "string",
                    "description": "Color del producto (ej: 'negro', 'marrón chocolate')",
                },
            },
            "required": ["producto", "talle", "color"],
        },
    },
]

TOOL_FUNCTIONS = {
    "buscar_pedido": buscar_pedido,
    "consultar_stock": consultar_stock,
}


def execute_tool(name: str, args: dict) -> str:
    """Ejecuta el tool y serializa el resultado a JSON."""
    func = TOOL_FUNCTIONS.get(name)
    if not func:
        return json.dumps({"error": f"Tool desconocido: {name}"}, ensure_ascii=False)
    try:
        result = func(**args)
    except Exception as e:
        result = {"error": str(e)}
    return json.dumps(result, ensure_ascii=False)


def chat(historial: list[dict], mensaje_usuario: str) -> str:
    """Loop agéntico: si Claude pide tools, los ejecuta y vuelve a llamarlo."""
    historial.append({"role": "user", "content": mensaje_usuario})

    for _ in range(MAX_TURNS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=historial,
        )

        # Guardamos lo que dijo el asistente (incluye tool_use blocks si los hay)
        historial.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")

        # Ejecutar todos los tools que pidió y devolverle los resultados
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                resultado = execute_tool(block.name, block.input)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": resultado,
                    }
                )
        historial.append({"role": "user", "content": tool_results})

    return "[El agente excedió el máximo de pasos sin completar la respuesta.]"


def main():
    print("Sofi (Trama) iniciada. Escribí 'salir' para terminar, 'reset' para empezar.\n")
    historial: list[dict] = []
    while True:
        try:
            user_input = input("Vos: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_input:
            continue
        if user_input.lower() in ("salir", "exit", "quit"):
            print("Chau!")
            break
        if user_input.lower() == "reset":
            historial = []
            print("[Conversación reiniciada]\n")
            continue
        try:
            respuesta = chat(historial, user_input)
            print(f"\nSofi: {respuesta}\n")
        except Exception as e:
            print(f"\n[Error]: {e}\n")


if __name__ == "__main__":
    main()
