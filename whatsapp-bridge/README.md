# Max por WhatsApp (bridge no oficial)

Conecta un número de WhatsApp (teléfono dedicado) con Max, usando
WhatsApp Web automatizado.

> ⚠️ **Advertencia**: esto va contra los términos de servicio de Meta.
> El número puede ser baneado. Usar SOLO con un chip descartable y
> volumen bajo (uso personal). Nunca con un número que te importe.

## Requisitos

- Una computadora o VPS prendida mientras el bot esté activo
- Node.js 18+ y Python 3.10+
- El teléfono del bot con WhatsApp activo (solo para escanear el QR;
  después puede quedar guardado en un cajón, pero debe seguir teniendo
  la línea activa)

## Puesta en marcha

**Terminal 1 — API de Max:**
```bash
cd Fede
pip install -r requirements.txt
uvicorn max_server:app --port 8002
```

**Terminal 2 — Bridge de WhatsApp:**
```bash
cd Fede/whatsapp-bridge
npm install
WHATSAPP_ALLOWED=549XXXXXXXXXX npm start
```

- `WHATSAPP_ALLOWED` = TU número (desde el que le vas a escribir a Max),
  formato internacional sin `+` (ej: `5492954111222`).
  Podés poner varios separados por coma. Si lo omitís, Max le responde
  a CUALQUIERA que le escriba al número del bot (no recomendado).

**Primera vez:** aparece un QR en la terminal.
En el teléfono del bot: WhatsApp → Ajustes → Dispositivos vinculados →
Vincular dispositivo → escanear el QR.

Cuando diga `✅ Bridge conectado`, escribile al número del bot desde tu
WhatsApp y Max responde.

## Comandos

- `reset` — borra la memoria y empieza conversación nueva
- Cualquier otro texto — es un encargo para Max
