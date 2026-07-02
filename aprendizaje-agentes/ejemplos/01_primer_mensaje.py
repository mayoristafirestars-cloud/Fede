"""
FASE 1 — Tu primera llamada a la API de Claude.

Antes de correr:
    pip install anthropic
    export ANTHROPIC_API_KEY="tu-clave"   (o setx en Windows)

Ejecutar:
    python 01_primer_mensaje.py
"""

import anthropic

# El cliente lee la API key de la variable de entorno ANTHROPIC_API_KEY.
# NUNCA pongas la clave directamente en el código.
client = anthropic.Anthropic()

MODELO = "claude-opus-4-8"

# ------------------------------------------------------------------
# PARTE 1: una llamada simple
# ------------------------------------------------------------------
respuesta = client.messages.create(
    model=MODELO,
    max_tokens=1024,
    # El "system" define el comportamiento permanente del asistente:
    system="Sos un asistente para un negocio mayorista argentino. "
           "Respondé corto, claro y en español rioplatense.",
    messages=[
        {"role": "user", "content": "¿Qué es un agente de IA? Explicámelo en 3 oraciones."}
    ],
)

# La respuesta viene como una lista de bloques; los de texto tienen .type == "text"
for bloque in respuesta.content:
    if bloque.type == "text":
        print(bloque.text)

print(f"\n[tokens usados: {respuesta.usage.input_tokens} entrada, "
      f"{respuesta.usage.output_tokens} salida]")

# ------------------------------------------------------------------
# PARTE 2: mini chat con memoria (multi-turno)
# ------------------------------------------------------------------
# CLAVE: la API no tiene memoria. En cada llamada le mandamos TODA
# la conversación acumulada en la lista `historial`.
print("\n--- Mini chat (escribí 'salir' para terminar) ---")

historial = []
while True:
    pregunta = input("\nVos: ").strip()
    if pregunta.lower() in ("salir", "exit", "chau"):
        break

    historial.append({"role": "user", "content": pregunta})

    respuesta = client.messages.create(
        model=MODELO,
        max_tokens=1024,
        system="Sos un asistente para un negocio mayorista argentino. "
               "Respondé corto y en español rioplatense.",
        messages=historial,
    )

    texto = next(b.text for b in respuesta.content if b.type == "text")
    print(f"\nClaude: {texto}")

    # Guardamos también la respuesta del asistente para que la recuerde
    historial.append({"role": "assistant", "content": texto})
