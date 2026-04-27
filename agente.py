"""
Agente de soporte - Paso 5: con base de conocimiento.
Carga personalidad (prompts/system_prompt.md) y datos de la tienda
(data/faqs.md, data/productos.md). Mantiene memoria de la conversación.
"""
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024

BASE_DIR = Path(__file__).parent
PROMPT_PATH = BASE_DIR / "prompts" / "system_prompt.md"
FAQS_PATH = BASE_DIR / "data" / "faqs.md"
PRODUCTOS_PATH = BASE_DIR / "data" / "productos.md"

client = Anthropic()


def build_system_prompt() -> str:
    """Combina la personalidad con la base de conocimiento."""
    persona = PROMPT_PATH.read_text(encoding="utf-8")
    faqs = FAQS_PATH.read_text(encoding="utf-8")
    productos = PRODUCTOS_PATH.read_text(encoding="utf-8")
    return f"""{persona}

---

# BASE DE CONOCIMIENTO — FAQS

Usá esta sección para responder preguntas frecuentes con info exacta.

{faqs}

---

# BASE DE CONOCIMIENTO — CATÁLOGO DE PRODUCTOS

Usá esta sección cuando el cliente pregunte por productos, talles, colores, precios o stock.

{productos}
"""


SYSTEM_PROMPT = build_system_prompt()


def chat(historial: list[dict], mensaje_usuario: str) -> str:
    """Envía el mensaje + historial a Claude y guarda la respuesta."""
    historial.append({"role": "user", "content": mensaje_usuario})
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=historial,
    )
    respuesta = response.content[0].text
    historial.append({"role": "assistant", "content": respuesta})
    return respuesta


def main():
    print("Sofi (Trama) iniciada. Escribí 'salir' para terminar, 'reset' para empezar de nuevo.\n")
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
