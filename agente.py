"""
Agente de soporte - Paso 3: con personalidad de soporte.
Carga un system prompt desde prompts/system_prompt.md.
Todavía no tiene memoria (cada mensaje es independiente).
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


def chat(mensaje: str) -> str:
    """Envía un mensaje a Claude con el system prompt de Trama."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": mensaje}],
    )
    return response.content[0].text


def main():
    print("Sofi (Trama) iniciada. Escribí 'salir' para terminar.\n")
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
        try:
            respuesta = chat(user_input)
            print(f"\nSofi: {respuesta}\n")
        except Exception as e:
            print(f"\n[Error]: {e}\n")


if __name__ == "__main__":
    main()
