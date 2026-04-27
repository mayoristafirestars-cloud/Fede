"""
Agente de soporte - Paso 4: con memoria de conversación.
Mantiene el historial completo dentro de cada sesión, así Sofi
recuerda lo que se habló antes en la misma charla.
"""
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024
PROMPT_PATH = Path(__file__).parent / "prompts" / "system_prompt.md"

client = Anthropic()
SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")


def chat(historial: list[dict], mensaje_usuario: str) -> str:
    """Agrega el mensaje del usuario al historial, llama a Claude
    y agrega la respuesta también al historial. Devuelve la respuesta."""
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
