# Agente de Soporte al Cliente

Agente de IA para atención al cliente de e-commerce, construido con Python y la API de Claude (Anthropic).

## Setup

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Crear tu archivo de credenciales:
   ```bash
   cp .env.example .env
   ```

3. Editar `.env` y pegar tu API key de Anthropic (https://console.anthropic.com).

4. Correr el agente:
   ```bash
   python agente.py
   ```

## Estructura

- `agente.py` — código del agente
- `prompts/` — prompts de personalidad del agente
- `.env` — credenciales (NUNCA se sube a git)
- `requirements.txt` — dependencias Python
