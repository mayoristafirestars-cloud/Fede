"""
Agente de soporte - Paso 2: agente mínimo por consola.
Cada mensaje es independiente (todavía no tiene memoria).
"""
import os
import sys

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024

client = Anthropic()


def chat(mensaje: str) -> str:
    """Envía un mensaje a Claude y devuelve la respuesta."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": mensaje}],
    )
    return response.content[0].text


def main():
    print("Agente de soporte iniciado. Escribí 'salir' para terminar.\n")
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
            print(f"\nAgente: {respuesta}\n")
        except Exception as e:
            print(f"\n[Error]: {e}\n")


if __name__ == "__main__":
    main()
