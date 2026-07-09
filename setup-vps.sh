#!/bin/bash
# ============================================================
#  Instalador de Eva + Max en un VPS Ubuntu (22.04 / 24.04)
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
apt-get install -y -qq git curl python3 python3-pip ca-certificates gnupg >/dev/null

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

echo "=== [3/6] Instalando dependencias de Python ==="
pip3 install -q -r requirements.txt --break-system-packages 2>/dev/null \
    || pip3 install -q -r requirements.txt

echo "=== [4/6] Instalando dependencias de Node (puede tardar) ==="
(cd whatsapp-bridge && npm install --no-fund --no-audit --loglevel=error)
(cd vendedor-bridge && npm install --no-fund --no-audit --loglevel=error)

echo "=== [5/6] Configuracion ==="
if [ ! -f .env ]; then
    echo ""
    read -rp "Pega tu API key de Anthropic (sk-ant-...): " KEY < /dev/tty
    echo "ANTHROPIC_API_KEY=$KEY" > .env
    echo "API key guardada en $DIR/.env"
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

[Install]
WantedBy=multi-user.target
EOF
}

make_service "max-server" "$DIR" "/usr/bin/python3 -m uvicorn max_server:app --host 127.0.0.1 --port 8002"
make_service "eva-server" "$DIR" "/usr/bin/python3 -m uvicorn vendedor_server:app --host 127.0.0.1 --port 8003"
make_service "max-bridge" "$DIR/whatsapp-bridge" "/usr/bin/node bridge.js"
make_service "eva-bridge" "$DIR/vendedor-bridge" "/usr/bin/node bridge.js"

systemctl daemon-reload
systemctl enable --now max-server eva-server >/dev/null

echo ""
echo "============================================================"
echo " INSTALACION BASE COMPLETA"
echo ""
echo " Los cerebros (max-server y eva-server) ya estan corriendo."
echo ""
echo " FALTA: subir el inventario y escanear los QR de WhatsApp."
echo " Segui las instrucciones que te da Claude."
echo "============================================================"
