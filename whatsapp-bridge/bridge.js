/**
 * Bridge WhatsApp <-> Max.
 *
 * Corre en la máquina donde está el WhatsApp del bot (via WhatsApp Web).
 * La primera vez muestra un QR en la terminal: escanearlo desde el
 * teléfono del bot (WhatsApp > Dispositivos vinculados > Vincular).
 * La sesión queda guardada en .wwebjs_auth/ (no hace falta re-escanear).
 *
 * Requiere max_server.py corriendo:  uvicorn max_server:app --port 8002
 *
 * Config por variables de entorno (opcionales):
 *   MAX_API_URL        default http://127.0.0.1:8002/api/max
 *   WHATSAPP_ALLOWED   numeros permitidos separados por coma, formato
 *                      internacional sin '+' (ej: "5492954111222").
 *                      Vacio = responde a CUALQUIERA que le escriba.
 *
 * ADVERTENCIA: WhatsApp Web automatizado va contra los terminos de
 * servicio de Meta. Usar solo con un numero descartable y volumen bajo.
 */
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

const MAX_API_URL = process.env.MAX_API_URL || 'http://127.0.0.1:8002/api/max';

// Numeros permitidos: variable de entorno WHATSAPP_ALLOWED o archivo allowed.txt
let allowedRaw = process.env.WHATSAPP_ALLOWED || '';
if (!allowedRaw) {
  const allowedFile = path.join(__dirname, 'allowed.txt');
  if (fs.existsSync(allowedFile)) {
    allowedRaw = fs.readFileSync(allowedFile, 'utf8');
  }
}
const ALLOWED = allowedRaw
  .split(/[\n,]/)
  .map((n) => n.trim().replace(/[^0-9]/g, ''))
  .filter(Boolean);

const busy = new Set();

const client = new Client({
  authStrategy: new LocalAuth({ dataPath: '.wwebjs_auth' }),
  puppeteer: {
    headless: true,
    executablePath: process.env.CHROME_PATH || undefined,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  },
});

client.on('qr', (qr) => {
  console.log('\nEscanea este QR desde el telefono del bot');
  console.log('(WhatsApp > Ajustes > Dispositivos vinculados > Vincular dispositivo):\n');
  qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
  console.log('✅ Bridge conectado. Max esta escuchando WhatsApp.');
  if (ALLOWED.length) {
    console.log('Numeros permitidos:', ALLOWED.join(', '));
  } else {
    console.log('⚠️  Sin lista de permitidos: responde a cualquiera que escriba.');
  }
});

client.on('auth_failure', (msg) => console.error('❌ Fallo de auth:', msg));
client.on('disconnected', (reason) => {
  console.error('❌ Desconectado:', reason, '- reiniciando en 10s');
  setTimeout(() => client.initialize(), 10000);
});

async function preguntarAMax(sessionId, mensaje) {
  const res = await fetch(MAX_API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, message: mensaje }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Max API ${res.status}: ${err.slice(0, 200)}`);
  }
  const data = await res.json();
  return data.response;
}

async function mandarAudioAMax(sessionId, audioB64, mimetype) {
  const url = MAX_API_URL.replace('/api/max', '/api/audio');
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, audio_b64: audioB64, mimetype }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Max API ${res.status}: ${err.slice(0, 200)}`);
  }
  const data = await res.json();
  return data.response;
}

function partir(texto, maxLen = 3500) {
  const partes = [];
  for (let i = 0; i < texto.length; i += maxLen) {
    partes.push(texto.slice(i, i + maxLen));
  }
  return partes;
}

client.on('message', async (msg) => {
  try {
    // Ignorar grupos y estados; solo chats directos.
    if (msg.from.endsWith('@g.us') || msg.from === 'status@broadcast') return;

    const esAudio = msg.type === 'ptt' || msg.type === 'audio';
    const texto = (msg.body || '').trim();
    if (!texto && !esAudio) return;

    console.log(
      esAudio
        ? `Audio entrante de ${msg.from}`
        : `Mensaje entrante de ${msg.from}: "${texto.slice(0, 60)}"`
    );

    if (ALLOWED.length) {
      // WhatsApp a veces identifica al contacto con un ID interno (@lid)
      // distinto del numero visible; chequeamos las dos formas.
      let permitido = ALLOWED.includes(msg.from.replace(/[^0-9]/g, ''));
      if (!permitido) {
        try {
          const contacto = await msg.getContact();
          const numReal = (contacto.number || '').replace(/[^0-9]/g, '');
          permitido = ALLOWED.includes(numReal);
        } catch (_) {}
      }
      if (!permitido) {
        console.log('  -> Ignorado: numero no permitido.');
        return;
      }
    }

    if (busy.has(msg.from)) {
      await msg.reply('Para un toque, todavia estoy con tu encargo anterior 🙏');
      return;
    }
    busy.add(msg.from);

    let respuesta;
    if (esAudio) {
      const media = await msg.downloadMedia();
      if (!media || !media.data) {
        respuesta = 'No pude descargar el audio 😕 ¿Me lo mandás de nuevo?';
      } else {
        respuesta = await mandarAudioAMax(
          msg.from,
          media.data,
          media.mimetype || 'audio/ogg'
        );
      }
    } else {
      respuesta = await preguntarAMax(msg.from, texto);
    }

    for (const parte of partir(respuesta)) {
      await client.sendMessage(msg.from, parte);
    }
  } catch (e) {
    console.error('Error procesando mensaje:', e.message);
    try {
      await client.sendMessage(msg.from, `Uy, tuve un problema: ${e.message}`);
    } catch (_) {}
  } finally {
    busy.delete(msg.from);
  }
});

client.initialize();
