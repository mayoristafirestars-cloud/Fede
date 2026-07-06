"""
Max — Asistente ejecutivo personal de Fede.
Investiga en internet, compara opciones, arma rankings y redacta
mensajes de contacto/negociación. No paga ni contrata: prepara todo
para que Fede cierre.

Correr: python3 asistente.py
"""
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096
MAX_WEB_SEARCHES = 8  # tope de búsquedas por respuesta (controla costo)
MAX_TURNS = 10  # tope de continuaciones por respuesta

BASE_DIR = Path(__file__).parent
PROMPT_PATH = BASE_DIR / "prompts" / "asistente_prompt.md"

client = Anthropic()
SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")

# Búsqueda web server-side: la ejecuta Anthropic, no hace falta código local.
TOOLS = [
    {
        "type": "web_search_20250305",
        "name": "web_search",
        "max_uses": MAX_WEB_SEARCHES,
    }
]


def chat(historial: list[dict], mensaje_usuario: str) -> str:
    """Turno completo del asistente, con búsquedas web incluidas."""
    historial.append({"role": "user", "content": mensaje_usuario})

    for _ in range(MAX_TURNS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=historial,
        )
        historial.append({"role": "assistant", "content": response.content})

        # pause_turn: la API cortó un turno largo (p.ej. entre búsquedas);
        # hay que reenviar para que continúe donde quedó.
        if response.stop_reason == "pause_turn":
            continue

        return "".join(b.text for b in response.content if b.type == "text")

    return "[Se alcanzó el máximo de pasos. Pedime que continúe.]"


def main():
    print("Max — tu asistente personal. Contame qué necesitás.")
    print("('salir' para terminar, 'reset' para empezar de cero)\n")
    historial: list[dict] = []
    while True:
        try:
            user_input = input("Fede: ").strip()
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
            print("\n[Max está trabajando...]\n")
            respuesta = chat(historial, user_input)
            print(f"Max: {respuesta}\n")
        except Exception as e:
            print(f"\n[Error]: {e}\n")


if __name__ == "__main__":
    main()
