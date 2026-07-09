# 📖 MANUAL DE OPERACIÓN — Ecosistema Dist Coronel Sur

Guía completa para operar Eva, Max y el sistema de gestión **sin ayuda técnica**.
Guardá este archivo o imprimilo.

---

## 1. El mapa: qué es cada cosa

| Pieza | Qué hace | Dónde vive |
|---|---|---|
| **Eva** | Vendedora virtual: atiende clientes por WhatsApp 24hs, pasa precios (2 listas), fotos, arma pedidos | `vendedor_server.py` (cerebro) + `vendedor-bridge` (WhatsApp) |
| **Max** | Tu asistente personal: investiga en internet lo que le pidas | `max_server.py` + `whatsapp-bridge` |
| **Sistema Coronel Sur** | Gestión web: facturación, CRM, inventario, reportes, pedidos de Eva | carpeta `coronel-sur`, se ve en el navegador |
| **Vigilante** | Avisa a tu WhatsApp si algo se cae | `watchdog.py` |
| **Malcom** | Humano 😄 — recibe los pedidos confirmados por WhatsApp | +54 9 2954 82-9943 |

**El flujo de un pedido:**
Cliente → WhatsApp de Eva → confirma pedido → 1) aviso a Malcom por WhatsApp, 2) presupuesto automático en el sistema (pestaña Agente).

---

## 2. Operación diaria en la PC del negocio

**Prender todo** (después de encender la PC):
1. Doble click en `2-arrancar.bat` → Max (2 ventanas)
2. Doble click en `3-arrancar-vendedor.bat` → Eva (2 ventanas)
3. Doble click en `iniciar.bat` (dentro de `coronel-sur`) → el sistema en el navegador
4. (Opcional) `4-vigilante.bat` → el vigilante

**Reglas de oro:**
- ⚠️ Las ventanas negras NUNCA se cierran ni se minimizan a lo loco.
- ⚠️ NO hacer click ADENTRO de una ventana negra: se congela (título dice "Seleccionar"). Si pasa: tecla **ESC**.
- Los mensajes que llegan mientras todo está apagado NO se responden después.

**Entrar al sistema:** navegador → `http://localhost:8000` → clave (por defecto `coronel2026` — cambiala, ver sección 7).

---

## 3. Actualizar precios y stock

1. En FactuPyme: exportar el **Inventario** como CSV.
2. Guardarlo como `negocio\inventario.csv` (reemplazando el anterior).
3. **Listo.** Eva lo detecta sola en el próximo mensaje (sin reiniciar).
4. Para el sistema de gestión: doble click en `importar.bat` (usa el mismo archivo).

**Hacé esto cada vez que cambien precios.** Si no, Eva vende con precios viejos.

---

## 4. Problemas comunes y sus soluciones

### "Eva/Max no responde"
1. ¿Están las 2 ventanas abiertas (cerebro + WhatsApp)? ¿La PC tiene internet?
2. ¿Alguna ventana dice "Seleccionar" en el título? → click en ella + ESC
3. Mirá la ventana del WhatsApp: ¿dice "Bridge conectado"/"Vendedor conectado"?
   - Si muestra un QR → la sesión se desvinculó: escanearlo de nuevo con el teléfono del bot
4. Mirá la ventana del cerebro: ¿hay un bloque "ERROR COMPLETO"? → sacale foto (para pedir ayuda) y reiniciá con el paso 5
5. Reinicio limpio (soluciona el 90%):
   ```
   taskkill /f /im python.exe
   taskkill /f /im node.exe
   wmic process where "CommandLine like '%wwebjs_auth%'" call terminate
   ```
   (en una ventana negra nueva: Windows+R → cmd) y volver a arrancar con los .bat

### "Error: The browser is already running"
Proceso fantasma. Correr el tercer comando del reinicio limpio (el de `wwebjs_auth`) o reiniciar la PC.

### "Error 400 pelado de la API"
Casi siempre la API key mal guardada. Verificar con `type .env` (en la carpeta del proyecto) que la línea `ANTHROPIC_API_KEY=` esté completa (termina en letras/números, sin cortes).

### "Credit balance too low"
Se acabó el crédito de la API → https://console.anthropic.com/settings/billing → Add credits.

### El bot ignora a un número que debería responder (Max)
WhatsApp a veces usa IDs internos. En la ventana del bridge de Max aparece `Mensaje entrante de XXXX@lid` → agregar esos dígitos a `whatsapp-bridge\allowed.txt` (una línea más) y reiniciar.

### Un cliente se queja de lo que le dijo Eva
Sistema → pestaña **Agente** → Últimas conversaciones → filtrar por su teléfono. Ahí está TODO lo que se dijeron.

---

## 5. El VPS (cuando esté): comandos básicos

Conectarse (PowerShell de Windows): `ssh root@IP-DEL-SERVIDOR`

| Quiero... | Comando |
|---|---|
| Ver si todo corre | `systemctl status eva-server eva-bridge max-server max-bridge coronel-sur vigilante` |
| Reiniciar a Eva | `systemctl restart eva-server eva-bridge` |
| Reiniciar a Max | `systemctl restart max-server max-bridge` |
| Reiniciar el sistema | `systemctl restart coronel-sur` |
| Ver qué está pasando (logs de Eva) | `journalctl -u eva-server -f` (salir: Ctrl+C) |
| Ver el QR para re-vincular WhatsApp | `systemctl stop eva-bridge` → `cd /opt/fede/vendedor-bridge && node bridge.js` → escanear → Ctrl+C → `systemctl start eva-bridge` |
| Actualizar el código | `cd /opt/fede && git pull && systemctl restart eva-server eva-bridge max-server max-bridge coronel-sur` |
| Subir inventario nuevo desde tu PC | `scp C:\ruta\inventario.csv root@IP:/opt/fede/negocio/inventario.csv` |

---

## 6. Configuración: el archivo `.env`

Está en la carpeta principal. Una línea por variable:

| Variable | Qué es |
|---|---|
| `ANTHROPIC_API_KEY` | La llave de la IA (secreta, no compartir) |
| `CORONEL_URL` | URL del sistema (para que Eva le mande pedidos): `http://127.0.0.1:8000` |
| `AGENTE_TOKEN` | Contraseña interna Eva↔Sistema (deben coincidir en ambos) |
| `CORONEL_CLAVE` | La clave para entrar al sistema web |
| `ALERTA_WHATSAPP` | TU número: recibe alertas del vigilante y el resumen diario (ej `5492954525928`) |
| `RESUMEN_HORA` | Hora del resumen diario de Eva (default 21) |
| `LIMITE_POR_NUMERO_HORA` | Máx. mensajes por cliente por hora (default 20) |
| `LIMITE_GLOBAL_DIA` | Máx. mensajes totales por día (default 400) |
| `EVA_MODEL` / `MAX_MODEL` | Cambiar el modelo de IA (default Sonnet; Haiku = más barato) |
| `WHISPER_MODEL` | Motor de audio: `small` (default), `base` (rápido), `medium` (mejor) |

Después de tocar el `.env`: reiniciar (cerrar ventanas → .bat de nuevo; en VPS `systemctl restart ...`).

---

## 7. Seguridad — checklist

- [ ] Cambiar la clave del sistema: en el `.env` → `CORONEL_CLAVE=TuClaveNueva`
- [ ] La API key NUNCA se pega en chats, mails ni capturas
- [ ] Si la API key se filtró: https://console.anthropic.com/settings/keys → borrar la vieja → crear nueva → actualizar `.env`
- [ ] El archivo `.env` no se comparte ni se sube a ningún lado
- [ ] Backups: el sistema guarda copias diarias automáticas en `coronel-sur\backend\db\backups` (últimos 14 días). Cada tanto, copiá la más nueva a un pendrive/Drive.

---

## 8. Guía del piloto con clientes reales

Antes de difundir el número de Eva a todos:

1. **Semana 1**: dale el número a 5-10 clientes de confianza ("estamos probando atención automática 24hs, escribile").
2. **Cada día**: pestaña Agente → leer las conversaciones. Anotar: ¿respondió mal algo? ¿no encontró un producto que SÍ hay? ¿algún precio raro?
3. Ajustar el `negocio\info.md` con lo que falte (es texto, se edita con Bloc de notas; Eva lo toma al reiniciar).
4. **Cuando 9 de 10 conversaciones salgan bien** → difundir: estados de WhatsApp, sticker con QR en el mostrador (generá el QR con el link `https://wa.me/54XXXXXXXXXX`), pie de las facturas.

---

## 9. Qué NO tocar (a menos que sepas lo que hacés)

- Los archivos `.py`, `.js` y las carpetas `node_modules`, `.wwebjs_auth`
- `sesiones_eva.json` / `sesiones_max.json` (la memoria de los bots)
- La carpeta `backend\db` del sistema (la base de datos)

**SÍ podés editar tranquilo:** `negocio\info.md` (datos del negocio), `negocio\inventario.csv` (precios), `.env` (configuración), `whatsapp-bridge\allowed.txt` (números de Max).
