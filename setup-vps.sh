#!/bin/bash
# ============================================================
#  Instalador de Eva + Max en un VPS Ubuntu (22.04 / 24.04 / 26.04)
#  Uso:  curl -fsSL https://raw.githubusercontent.com/mayoristafirestars-cloud/Fede/claude/build-ai-agent-H9XwU/setup-vps.sh | bash
# ============================================================
set -e

REPO_URL="https://github.com/mayoristafirestars-cloud/Fede.git"
BRANCH="claude/build-ai-agent-H9XwU"
DIR="/opt/fede"

echo ""
echo "=== [1/6] Instalando paquetes del sistema ==="
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq git curl python3 python3-venv python3-full ca-certificates gnupg build-essential ffmpeg >/dev/null

# Node.js 20 (NodeSource)
if ! command -v node >/dev/null || [ "$(node -v | cut -c2-3)" -lt 18 ]; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - >/dev/null
    apt-get install -y -qq nodejs >/dev/null
fi

# Dependencias de Chromium para los bridges de WhatsApp
apt-get install -y -qq libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libpango-1.0-0 libpangocairo-1.0-0 libcairo2 \
    libxss1 fonts-liberation >/dev/null 2>&1 || true
apt-get install -y -qq libasound2 >/dev/null 2>&1 || apt-get install -y -qq libasound2t64 >/dev/null 2>&1 || true

echo "=== [2/6] Descargando el proyecto ==="
if [ -d "$DIR/.git" ]; then
    cd "$DIR" && git fetch origin "$BRANCH" && git reset --hard "origin/$BRANCH"
else
    git clone --branch "$BRANCH" --depth 1 "$REPO_URL" "$DIR"
fi
cd "$DIR"

echo "=== [3/6] Instalando dependencias de Python (entorno virtual) ==="
VENV="$DIR/venv"
python3 -m venv "$VENV"
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q -r requirements.txt
"$VENV/bin/pip" install -q -r coronel-sur/requirements.txt
PY="$VENV/bin/python"

echo "=== [4/6] Instalando dependencias de Node (puede tardar) ==="
(cd whatsapp-bridge && npm install --no-fund --no-audit --loglevel=error)
(cd vendedor-bridge && npm install --no-fund --no-audit --loglevel=error)

echo "=== [5/6] Configuracion ==="
if [ ! -f .env ]; then
    echo ""
    read -rp "Pega tu API key de Anthropic (sk-ant-...): " KEY < /dev/tty
    read -rp "Tu numero de WhatsApp para alertas y resumen diario (ej 5492954525928): " ALERTA < /dev/tty
    read -rp "Clave para entrar al sistema de gestion (inventa una): " CLAVE < /dev/tty
    cat > .env <<ENV
ANTHROPIC_API_KEY=$KEY
CORONEL_URL=http://127.0.0.1:8000
AGENTE_TOKEN=eva-$(head -c 16 /dev/urandom | md5sum | cut -c1-16)
CORONEL_CLAVE=$CLAVE
ALERTA_WHATSAPP=$ALERTA
RESUMEN_HORA=21
ENV
    echo "Configuracion guardada en $DIR/.env"
fi
if [ ! -f whatsapp-bridge/allowed.txt ]; then
    echo ""
    echo "Numeros que pueden hablar con MAX (tu asistente personal)."
    echo "Formato: uno por linea al final; aca ponelos separados por coma."
    read -rp "Numeros (ej: 5492954525928,3513534906621): " NUMS < /dev/tty
    echo "$NUMS" | tr ',' '\n' > whatsapp-bridge/allowed.txt
    echo "Guardado."
fi

echo "=== [6/6] Creando servicios (arranque automatico) ==="
make_service() {
    local name="$1" workdir="$2" cmd="$3"
    cat > "/etc/systemd/system/$name.service" <<EOF
[Unit]
Description=$name
After=network-online.target
Wants=network-online.target

[Service]
WorkingDirectory=$workdir
ExecStart=$cmd
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1
EnvironmentFile=-$DIR/.env

[Install]
WantedBy=multi-user.target
EOF
}

make_service "max-server" "$DIR" "$VENV/bin/python -m uvicorn max_server:app --host 127.0.0.1 --port 8002"
make_service "eva-server" "$DIR" "$VENV/bin/python -m uvicorn vendedor_server:app --host 127.0.0.1 --port 8003"
make_service "max-bridge" "$DIR/whatsapp-bridge" "/usr/bin/node bridge.js"
make_service "eva-bridge" "$DIR/vendedor-bridge" "/usr/bin/node bridge.js"
make_service "coronel-sur" "$DIR/coronel-sur" "$VENV/bin/python backend/main.py"
make_service "vigilante" "$DIR" "$VENV/bin/python watchdog.py"

# enable = arrancan solos en cada reinicio del servidor.
# Los cerebros y el vigilante se inician ya; los bridges se habilitan para
# el arranque automático pero se inician a mano la primera vez (hay que
# escanear el QR de WhatsApp).
systemctl daemon-reload
systemctl enable --now max-server eva-server coronel-sur vigilante >/dev/null
systemctl enable max-bridge eva-bridge >/dev/null

# HTTPS automático con Caddy (opcional, requiere un dominio apuntando a este VPS)
echo ""
read -rp "¿Tenes un dominio apuntando a este servidor? (ej gestion.tudominio.com, ENTER para saltar): " DOMINIO < /dev/tty
if [ -n "$DOMINIO" ]; then
    echo "=== Instalando Caddy (HTTPS automatico) ==="
    apt-get install -y -qq debian-keyring debian-archive-keyring apt-transport-https curl >/dev/null
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' \
        | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg 2>/dev/null
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' \
        > /etc/apt/sources.list.d/caddy-stable.list
    apt-get update -qq && apt-get install -y -qq caddy >/dev/null
    cat > /etc/caddy/Caddyfile <<CADDY
$DOMINIO {
    reverse_proxy 127.0.0.1:8000
}
CADDY
    systemctl reload caddy 2>/dev/null || systemctl restart caddy
    echo "HTTPS configurado: https://$DOMINIO (el certificado se emite solo en ~1 min)"
fi

IP=$(hostname -I | awk '{print $1}')
echo ""
echo "============================================================"
echo " INSTALACION BASE COMPLETA"
echo ""
echo " Ya corriendo:"
echo "  - Cerebro de Max     (puerto 8002, interno)"
echo "  - Cerebro de Eva     (puerto 8003, interno)"
echo "  - Sistema Coronel Sur: http://$IP:8000  (entra con tu clave)"
echo ""
echo " FALTA: subir el inventario y escanear los QR de WhatsApp."
echo " Segui las instrucciones que te da Claude."
echo "============================================================"
