/**
 * Bridge WhatsApp <-> Vendedor virtual.
 *
 * Igual que el bridge de Max pero para atender CLIENTES:
 * - responde a cualquiera que escriba (los clientes son desconocidos)
 * - puede mandar FOTOS de productos
 * - usa su propia sesion de WhatsApp (.wwebjs_auth propia)
 *
 * Requiere vendedor_server.py corriendo:
 *   uvicorn vendedor_server:app --port 8003
 *
 * ADVERTENCIA: WhatsApp Web automatizado va contra los terminos de Meta.
 * Usar con un numero dedicado al bot, no con el numero personal.
 */
const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const API_URL = process.env.VENDEDOR_API_URL || 'http://127.0.0.1:8003/api/vendedor';

// WhatsApp del vendedor humano que recibe los pedidos confirmados (Malcom).
const VENDEDOR_HUMANO = (process.env.VENDEDOR_HUMANO || '5492954829943') + '@c.us';

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
  console.log('\nEscanea este QR desde el telefono del NEGOCIO');
  console.log('(WhatsApp > Ajustes > Dispositivos vinculados > Vincular dispositivo):\n');
  qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
  console.log('✅ Vendedor conectado. Atendiendo clientes por WhatsApp.');
});

client.on('auth_failure', (msg) => console.error('❌ Fallo de auth:', msg));
client.on('disconnected', (reason) => {
  console.error('❌ Desconectado:', reason, '- reiniciando en 10s');
  setTimeout(() => client.initialize(), 10000);
});

async function preguntarAlVendedor(sessionId, mensaje) {
  const res = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, message: mensaje }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Vendedor API ${res.status}: ${err.slice(0, 200)}`);
  }
  return res.json(); // {response, fotos}
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
    if (msg.from.endsWith('@g.us') || msg.from === 'status@broadcast') return;

    const texto = (msg.body || '').trim();
    if (!texto) return;

    console.log(`Cliente ${msg.from}: "${texto.slice(0, 60)}"`);

    if (busy.has(msg.from)) return;
    busy.add(msg.from);

    const data = await preguntarAlVendedor(msg.from, texto);

    if (data.response) {
      for (const parte of partir(data.response)) {
        await client.sendMessage(msg.from, parte);
      }
    }

    for (const foto of data.fotos || []) {
      try {
        const media = foto.startsWith('http')
          ? await MessageMedia.fromUrl(foto, { unsafeMime: true })
          : MessageMedia.fromFilePath(foto);
        await client.sendMessage(msg.from, media);
      } catch (e) {
        console.error('No pude mandar la foto', foto, e.message);
      }
    }

    // Pedido confirmado -> avisar al vendedor humano (Malcom)
    if (data.pedido) {
      try {
        const numeroCliente = msg.from.replace('@c.us', '').replace('@lid', '');
        await client.sendMessage(
          VENDEDOR_HUMANO,
          `🛒 *NUEVO PEDIDO* (via asistente)\nCliente: ${numeroCliente}\n\n${data.pedido}`
        );
        console.log('Pedido reenviado a Malcom.');
      } catch (e) {
        console.error('No pude avisar al vendedor humano:', e.message);
      }
    }
  } catch (e) {
    console.error('Error procesando mensaje:', e.message);
    try {
      await client.sendMessage(
        msg.from,
        'Disculpá, tuve un problema técnico. Probá de nuevo en un ratito 🙏'
      );
    } catch (_) {}
  } finally {
    busy.delete(msg.from);
  }
});

client.initialize();
