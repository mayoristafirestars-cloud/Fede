"""
Vigilante del ecosistema: chequea cada minuto que todo esté vivo y
encola alertas cuando algo se cae (y cuando se recupera).

Qué vigila:
  - Cerebro de Max      http://127.0.0.1:8002/health
  - Cerebro de Eva      http://127.0.0.1:8003/health
  - Sistema Coronel Sur http://127.0.0.1:8000/health
  - WhatsApp de Max     archivo max-bridge.alive (latido cada 30s)
  - WhatsApp de Eva     archivo eva-bridge.alive (latido cada 30s)

Las alertas se escriben en alertas.txt; el primer bridge de WhatsApp
que esté vivo las envía al número de ALERTA_WHATSAPP y las borra.

Correr: python3 watchdog.py   (o como servicio systemd en el VPS)
"""
import os
import time
import urllib.request
from pathlib import Path

BASE = Path(__file__).parent
ALERTAS = BASE / "alertas.txt"
INTERVALO = 60          # segundos entre chequeos
LATIDO_MAX = 120        # segundos sin latido = bridge caído

CHEQUEOS_HTTP = {
    "Cerebro de Max": "http://127.0.0.1:8002/health",
    "Cerebro de Eva": "http://127.0.0.1:8003/health",
    "Sistema Coronel Sur": "http://127.0.0.1:8000/health",
}
CHEQUEOS_LATIDO = {
    "WhatsApp de Max": BASE / "max-bridge.alive",
    "WhatsApp de Eva": BASE / "eva-bridge.alive",
}

estado_previo: dict[str, bool] = {}


def encolar_alerta(texto: str) -> None:
    try:
        with open(ALERTAS, "a", encoding="utf-8") as f:
            f.write(texto + "\n")
    except Exception as e:
        print(f"[watchdog] no pude encolar alerta: {e}")


def esta_vivo_http(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return r.status == 200
    except Exception:
        return False


def esta_vivo_latido(ruta: Path) -> bool:
    try:
        return (time.time() - ruta.stat().st_mtime) < LATIDO_MAX
    except OSError:
        return False


def chequear(nombre: str, vivo: bool) -> None:
    antes = estado_previo.get(nombre)
    estado_previo[nombre] = vivo
    if antes is None:
        # primer chequeo: solo avisar si arranca caído
        if not vivo:
            print(f"[watchdog] {nombre}: CAIDO (al iniciar)")
            encolar_alerta(f"🔴 *{nombre}* está caído.")
        return
    if antes and not vivo:
        print(f"[watchdog] {nombre}: SE CAYO")
        encolar_alerta(f"🔴 *{nombre}* se cayó. Revisalo cuando puedas.")
    elif not antes and vivo:
        print(f"[watchdog] {nombre}: volvió")
        encolar_alerta(f"🟢 *{nombre}* volvió a funcionar.")


def main():
    print("[watchdog] Vigilante iniciado. Chequeando cada", INTERVALO, "segundos.")
    # darle tiempo a que todo arranque antes del primer chequeo
    time.sleep(90)
    while True:
        for nombre, url in CHEQUEOS_HTTP.items():
            chequear(nombre, esta_vivo_http(url))
        for nombre, ruta in CHEQUEOS_LATIDO.items():
            chequear(nombre, esta_vivo_latido(ruta))
        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()
