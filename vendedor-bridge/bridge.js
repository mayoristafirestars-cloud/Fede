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

// Cache: id de WhatsApp -> numero real del contacto
const numerosReales = new Map();

async function numeroRealDe(msg) {
  if (numerosReales.has(msg.from)) return numerosReales.get(msg.from);
  let numero = '';
  try {
    const contacto = await msg.getContact();
    numero = (contacto && contacto.number ? contacto.number : '').replace(/[^0-9]/g, '');
  } catch (_) {}
  if (!numero && msg.from.endsWith('@c.us')) {
    numero = msg.from.replace(/[^0-9]/g, '');
  }
  numerosReales.set(msg.from, numero);
  return numero;
}

async function preguntarAlVendedor(sessionId, mensaje, telefono) {
  const res = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, message: mensaje, telefono }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Vendedor API ${res.status}: ${err.slice(0, 200)}`);
  }
  return res.json(); // {response, fotos, pedido}
}

async function mandarAudioAlVendedor(sessionId, audioB64, mimetype, telefono) {
  const res = await fetch(API_URL + '/audio', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, audio_b64: audioB64, mimetype, telefono }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Vendedor API ${res.status}: ${err.slice(0, 200)}`);
  }
  return res.json();
}

function partir(texto, maxLen = 3500) {
  const partes = [];
  for (let i = 0; i < texto.length; i += maxLen) {
    partes.push(texto.slice(i, i + maxLen));
  }
  return partes;
}

const MSG_NO_VEO =
  'Por ahora no puedo ver fotos ni archivos 🙈 Contame por texto qué producto ' +
  'buscás y te paso precio y foto al toque.';

client.on('message', async (msg) => {
  try {
    if (msg.from.endsWith('@g.us') || msg.from === 'status@broadcast') return;

    const esAudio = msg.type === 'ptt' || msg.type === 'audio';
    const esOtroMedio = ['image', 'video', 'document', 'sticker'].includes(msg.type);
    const texto = (msg.body || '').trim();
    if (!texto && !esAudio && !esOtroMedio) return;

    console.log(
      esAudio
        ? `Cliente ${msg.from}: [audio]`
        : `Cliente ${msg.from}: ${esOtroMedio ? '[' + msg.type + '] ' : ''}"${texto.slice(0, 60)}"`
    );

    if (busy.has(msg.from)) return;
    busy.add(msg.from);

    // Foto/archivo sin texto: avisar amablemente y listo.
    if (esOtroMedio && !texto) {
      await client.sendMessage(msg.from, MSG_NO_VEO);
      busy.delete(msg.from);
      return;
    }

    const telefono = await numeroRealDe(msg);

    let data;
    if (esAudio) {
      const media = await msg.downloadMedia();
      if (!media || !media.data) {
        await client.sendMessage(msg.from, 'No me llegó bien el audio 😅 ¿Me lo mandás de nuevo o me escribís?');
        busy.delete(msg.from);
        return;
      }
      data = await mandarAudioAlVendedor(msg.from, media.data, media.mimetype || 'audio/ogg', telefono);
    } else {
      // Si mandó foto CON texto, procesamos el texto y aclaramos lo de la foto.
      data = await preguntarAlVendedor(msg.from, texto, telefono);
      if (esOtroMedio && data.response) {
        data.response = '(La foto no la puedo ver 🙈, pero leí tu mensaje 👇)\n\n' + data.response;
      }
    }

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
        const numeroCliente = telefono || msg.from.replace('@c.us', '').replace('@lid', '');
        await client.sendMessage(
          VENDEDOR_HUMANO,
          `🛒 *NUEVO PEDIDO* (via asistente)\nCliente: +${numeroCliente}\nWhatsApp: https://wa.me/${numeroCliente}\n\n${data.pedido}`
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
