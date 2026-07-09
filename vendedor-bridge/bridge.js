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
const fs = require('fs');
const path = require('path');

const API_URL = process.env.VENDEDOR_API_URL || 'http://127.0.0.1:8003/api/vendedor';

// WhatsApp del vendedor humano que recibe los pedidos confirmados (Malcom).
const VENDEDOR_HUMANO = (process.env.VENDEDOR_HUMANO || '5492954829943') + '@c.us';

// ---- Límites anti-abuso (que nadie queme el crédito de la API) ----
const LIMITE_POR_NUMERO_HORA = parseInt(process.env.LIMITE_POR_NUMERO_HORA || '20', 10);
const LIMITE_GLOBAL_DIA = parseInt(process.env.LIMITE_GLOBAL_DIA || '400', 10);
// Numero del dueño para avisarle si se alcanza el tope global (opcional)
const ALERTA_WHATSAPP = (process.env.ALERTA_WHATSAPP || '').replace(/[^0-9]/g, '');

// Resumen diario por WhatsApp al dueño (necesita ALERTA_WHATSAPP)
const RESUMEN_HORA = parseInt(process.env.RESUMEN_HORA || '21', 10);
const CORONEL_URL = (process.env.CORONEL_URL || '').replace(/\/$/, '');
const AGENTE_TOKEN = process.env.AGENTE_TOKEN || 'eva-coronel-2026';

const ventanasPorNumero = new Map(); // from -> [timestamps ultima hora]
const yaAvisados = new Set();        // numeros ya avisados de que se pasaron
const clientesHoy = new Set();       // numeros distintos que escribieron hoy
let diaActual = new Date().toDateString();
let mensajesHoy = 0;
let alertaGlobalEnviada = false;
let resumenEnviadoHoy = false;

function chequearLimites(from) {
  const ahora = Date.now();
  const hoy = new Date().toDateString();
  if (hoy !== diaActual) {
    diaActual = hoy;
    mensajesHoy = 0;
    alertaGlobalEnviada = false;
    resumenEnviadoHoy = false;
    clientesHoy.clear();
  }
  if (mensajesHoy >= LIMITE_GLOBAL_DIA) return { ok: false, motivo: 'global' };

  const recientes = (ventanasPorNumero.get(from) || []).filter((t) => ahora - t < 3600000);
  if (recientes.length >= LIMITE_POR_NUMERO_HORA) {
    ventanasPorNumero.set(from, recientes);
    return { ok: false, motivo: 'numero' };
  }
  recientes.push(ahora);
  ventanasPorNumero.set(from, recientes);
  mensajesHoy++;
  clientesHoy.add(from);
  return { ok: true };
}

// ---- Resumen diario al dueño ----
async function enviarResumenDiario() {
  if (!ALERTA_WHATSAPP) return;
  let extra = '';
  if (CORONEL_URL) {
    try {
      const r = await fetch(CORONEL_URL + '/api/agente/resumen-diario', {
        headers: { 'X-Token': AGENTE_TOKEN },
      });
      if (r.ok) {
        const d = await r.json();
        extra =
          `\n🛒 Pedidos confirmados: *${d.pedidos}* por *$${Number(d.total_pedidos).toLocaleString('es-AR')}*` +
          (d.ultimas_consultas && d.ultimas_consultas.length
            ? '\n\nÚltimas consultas:\n' + d.ultimas_consultas.map((c) => '· ' + c).join('\n')
            : '');
      }
    } catch (_) {}
  }
  const texto =
    `📊 *RESUMEN DEL DÍA — EVA*\n` +
    `💬 Mensajes atendidos: *${mensajesHoy}*\n` +
    `👥 Clientes distintos: *${clientesHoy.size}*` +
    extra;
  try {
    await client.sendMessage(ALERTA_WHATSAPP + '@c.us', texto);
    console.log('Resumen diario enviado.');
  } catch (e) {
    console.error('No pude enviar el resumen diario:', e.message);
  }
}

setInterval(() => {
  const ahora = new Date();
  if (ahora.getHours() === RESUMEN_HORA && !resumenEnviadoHoy) {
    resumenEnviadoHoy = true;
    enviarResumenDiario();
  }
}, 60000);

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

let conectado = false;

client.on('ready', () => {
  conectado = true;
  console.log('✅ Vendedor conectado. Atendiendo clientes por WhatsApp.');
});

client.on('auth_failure', (msg) => console.error('❌ Fallo de auth:', msg));
client.on('disconnected', (reason) => {
  conectado = false;
  console.error('❌ Desconectado:', reason, '- reiniciando en 10s');
  setTimeout(() => client.initialize(), 10000);
});

// ---- Latido para el vigilante (watchdog.py) + envio de alertas ----
const RAIZ = path.join(__dirname, '..');
const LATIDO = path.join(RAIZ, 'eva-bridge.alive');
const COLA_ALERTAS = path.join(RAIZ, 'alertas.txt');

async function procesarColaAlertas() {
  if (!conectado || !ALERTA_WHATSAPP) return;
  const mio = COLA_ALERTAS + '.eva';
  try { fs.renameSync(COLA_ALERTAS, mio); } catch (_) { return; } // vacia u otro la tomo
  try {
    const contenido = fs.readFileSync(mio, 'utf8').trim();
    fs.unlinkSync(mio);
    if (contenido) {
      await client.sendMessage(ALERTA_WHATSAPP + '@c.us', '🚨 *ALERTA DEL SISTEMA*\n\n' + contenido);
      console.log('Alerta(s) del vigilante enviada(s).');
    }
  } catch (e) { console.error('No pude enviar alertas:', e.message); }
}

setInterval(() => {
  if (conectado) { try { fs.writeFileSync(LATIDO, String(Date.now())); } catch (_) {} }
  procesarColaAlertas();
}, 30000);

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

// POST con un reintento automático: si la API tuvo un hipo momentáneo,
// el cliente ni se entera.
async function postConReintento(url, body) {
  let ultimoError;
  for (let intento = 1; intento <= 2; intento++) {
    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      if (res.ok) return res.json();
      const err = await res.text();
      ultimoError = new Error(`Vendedor API ${res.status}: ${err.slice(0, 200)}`);
    } catch (e) {
      ultimoError = e;
    }
    if (intento === 1) {
      console.log('Fallo la API, reintento en 3s...');
      await new Promise((r) => setTimeout(r, 3000));
    }
  }
  throw ultimoError;
}

function preguntarAlVendedor(sessionId, mensaje, telefono) {
  return postConReintento(API_URL, { session_id: sessionId, message: mensaje, telefono });
}

function mandarAudioAlVendedor(sessionId, audioB64, mimetype, telefono) {
  return postConReintento(API_URL + '/audio', {
    session_id: sessionId, audio_b64: audioB64, mimetype, telefono,
  });
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

    // Límites anti-abuso
    const permiso = chequearLimites(msg.from);
    if (!permiso.ok) {
      console.log(`Rate limit (${permiso.motivo}): ${msg.from}`);
      if (permiso.motivo === 'numero' && !yaAvisados.has(msg.from)) {
        yaAvisados.add(msg.from);
        setTimeout(() => yaAvisados.delete(msg.from), 3600000);
        await msg.reply(
          'Recibí muchos mensajes tuyos muy seguido 🙏 Dame un respiro y en un rato seguimos. ' +
          'Si es urgente, llamanos al 2954-701980.'
        );
      }
      if (permiso.motivo === 'global' && ALERTA_WHATSAPP && !alertaGlobalEnviada) {
        alertaGlobalEnviada = true;
        try {
          await client.sendMessage(
            ALERTA_WHATSAPP + '@c.us',
            `⚠️ *ALERTA EVA*: se alcanzó el límite de ${LIMITE_GLOBAL_DIA} mensajes en el día. ` +
            'Eva dejó de responder hasta mañana. Si es tráfico real, subí LIMITE_GLOBAL_DIA; ' +
            'si no, puede ser un ataque: revisá la ventana del bridge.'
          );
        } catch (_) {}
      }
      return;
    }

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
