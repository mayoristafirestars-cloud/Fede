#!/bin/bash
# Baja del repo los archivos del bot del Plan Fede, los valida y reinicia el servicio.
# Uso (desde PowerShell en la PC):  ssh root@167.235.140.223 actualizar-plan-fede
set -u
DIR=/opt/coronel-sur/backend/bot
RAMA=claude/add-doctor-nutritionist-generation-FeC6Q
REPO=mayoristafirestars-cloud/Fede
ARCHIVOS="recordatorios_plan_fede.py dieta_actual.py dieta_actual.json rutina_actual.py rutina_actual.json"
cd "$DIR" || { echo "No existe $DIR"; exit 1; }
T=$(systemctl show recordatorios-plan-fede -p Environment | grep -o 'GITHUB_TOKEN=[^ ]*' | cut -d= -f2)
[ -n "$T" ] || { echo "El servicio no tiene GITHUB_TOKEN: no puedo bajar del repo"; exit 1; }
for f in $ARCHIVOS; do
  curl -fsS -H "Authorization: Bearer $T" -H "Accept: application/vnd.github.raw" -o "$f.nuevo" \
    "https://api.github.com/repos/$REPO/contents/$f?ref=$RAMA" || { echo "FALLÓ la descarga de $f — no cambié nada"; rm -f ./*.nuevo; exit 1; }
done
# Validar antes de tocar lo que anda
for f in $ARCHIVOS; do
  case "$f" in
    *.json) python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$f.nuevo" || { echo "JSON roto: $f — no cambié nada"; rm -f ./*.nuevo; exit 1; } ;;
    *.py)   python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$f.nuevo" || { echo "Python roto: $f — no cambié nada"; rm -f ./*.nuevo; exit 1; } ;;
  esac
done
mkdir -p respaldo && for f in $ARCHIVOS; do [ -f "$f" ] && cp "$f" "respaldo/$f"; mv "$f.nuevo" "$f"; done
systemctl restart recordatorios-plan-fede && sleep 5
echo "----- bot -----"
journalctl -u recordatorios-plan-fede -n 6 --no-pager | grep -E "recordatorios cargados|HORARIO REPETIDO|ERROR|Traceback" || journalctl -u recordatorios-plan-fede -n 6 --no-pager
echo "Listo. Si algo falla: cd $DIR/respaldo && cp * .. && systemctl restart recordatorios-plan-fede"
