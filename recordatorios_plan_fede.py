#!/usr/bin/env python3
"""
Recordatorios del Plan Fede via Telegram.

Deploy:
  /opt/coronel-sur/backend/bot/recordatorios_plan_fede.py

Uso: se ejecuta como daemon con systemd. Chequea cada 60 seg si
corresponde disparar algun recordatorio y lo manda por Telegram.

Variables de entorno requeridas (usar el mismo bot ya configurado):
  TELEGRAM_BOT_TOKEN   -> token del BotFather
  TELEGRAM_CHAT_ID     -> id del chat privado de Fede

Zona horaria: America/Argentina/Buenos_Aires
"""

import os
import time
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

TZ = ZoneInfo("America/Argentina/Buenos_Aires")
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("recordatorios-fede")

# Dia (0=lunes ... 6=domingo), hora "HH:MM", mensaje.
RECORDATORIOS = [
    # ----- LUNES (gym A) -----
    (0, "05:30", "💧 En 30 min a despertar. Vaso 300 ml + pizca de sal."),
    (0, "06:00", "🍌 Pre-entreno en 30 min: media banana (80 g) + café 150 ml + agua con sal 300 ml."),
    (0, "07:30", "🥤 Post-entreno en 30 min: whey 35 g + creatina 5 g + agua 300 ml."),
    (0, "09:00", "🍳 Desayuno en 30 min: 4 huevos duros + palta 90 g + tomate 100 g + queso port salut 20 g + oliva 5 ml."),
    (0, "09:15", "💊 Suplementos en 30 min: Vit D3 + Omega-3."),
    (0, "12:30", "🍽️ Almuerzo en 30 min: pollo 220 g + papa hervida 100 g + ensalada + oliva 12 ml + limón."),
    (0, "13:30", "☕ ¡Último mate del día en 30 min! Después solo agua o infusiones sin cafeína."),
    (0, "16:00", "🥛 Merienda en 30 min: yogur griego 170 g + nueces 12 g + canela."),
    (0, "18:30", "🐟 Cena en 30 min: merluza 200 g + zapallito 150 g + morrón 70 g + anchoas 20 g + huevo duro + oliva 12 ml."),
    (0, "21:30", "🌙 Snack ancla en 30 min: yogur griego 170 g + chía 10 g + magnesio 300 mg. Bajá luces."),
    (0, "22:00", "😴 A dormir en 30 min. Celular afuera del cuarto."),

    # ----- MARTES (gym B) -----
    (1, "05:30", "💧 En 30 min a despertar. Vaso 300 ml + sal."),
    (1, "06:00", "🍇 Pre-entreno en 30 min: pasas 30 g + café 150 ml + agua con sal 300 ml."),
    (1, "07:30", "🥤 Post-entreno en 30 min: whey 35 g + creatina 5 g + agua 300 ml."),
    (1, "09:00", "🍳 Desayuno en 30 min: 4 huevos duros + queso port salut 30 g + palta 80 g + tomate 100 g + oliva 5 ml."),
    (1, "09:15", "💊 Suplementos: Vit D3 + Omega-3."),
    (1, "12:30", "🍽️ Almuerzo en 30 min: pollo 220 g + boniato hervido 100 g + ensalada + oliva 12 ml."),
    (1, "13:30", "☕ ¡Último mate del día en 30 min!"),
    (1, "16:00", "🥛 Merienda en 30 min: cottage 200 g + frutillas 30 g + canela."),
    (1, "18:30", "🐟 Cena en 30 min: salmón 180 g + espinaca salteada 150 g + champignones 80 g + oliva 12 ml."),
    (1, "21:30", "🌙 Snack ancla + magnesio 300 mg."),
    (1, "22:00", "😴 A dormir en 30 min."),

    # ----- MIÉRCOLES (descanso + bici) -----
    (2, "05:30", "💧 En 30 min a despertar. Vaso 300 ml de agua."),
    (2, "06:00", "🍳 Desayuno en 30 min: 3 huevos duros + ricota 80 g + palta 60 g + tomate 100 g + oliva 5 ml."),
    (2, "06:15", "💊 Suplementos: Vit D3 + Omega-3 + Creatina 5 g."),
    (2, "09:30", "🥛 Media mañana en 30 min: yogur griego 200 g + nueces 10 g + arándanos 20 g."),
    (2, "12:30", "🍽️ Almuerzo en 30 min: atún 180 g + 2 huevos duros + espinaca 150 g + queso 30 g + ensalada + palta 60 g + oliva 15 ml."),
    (2, "13:00", "🚴 Bici 40 min en 30 min. Zona 2 (FC 105-118 lpm), ruta plana, post-almuerzo."),
    (2, "13:30", "☕ Último mate del día en 30 min."),
    (2, "16:00", "🥛 Merienda en 30 min: ricota 150 g + almendras 10 g + cacao amargo 3 g."),
    (2, "16:30", "⭐ Momento hobby en 30 min (30-45 min)."),
    (2, "18:30", "🐟 Cena SARDINAS en 30 min: sardinas 120 g + tomate 100 g + palta 60 g + aceitunas 15 g + oliva + limón."),
    (2, "21:30", "🌙 Snack ancla + magnesio 300 mg."),
    (2, "22:00", "😴 A dormir en 30 min."),

    # ----- JUEVES (gym A) -----
    (3, "05:30", "💧 En 30 min a despertar. Agua + sal."),
    (3, "06:00", "🍌 Pre-entreno en 30 min: media banana 80 g + café + agua con sal."),
    (3, "07:30", "🥤 Post-entreno en 30 min: whey 35 g + creatina 5 g + agua."),
    (3, "09:00", "🍳 Desayuno diferente en 30 min: yogur griego 200 g + frutillas 100 g + almendras 15 g + canela + 3 huevos duros aparte."),
    (3, "09:15", "💊 Suplementos: Vit D3 + Omega-3."),
    (3, "12:30", "🍽️ Almuerzo en 30 min: pollo 200 g + papa hervida 100 g + huevo duro + ensalada nicoise + palta 50 g + oliva 12 ml."),
    (3, "13:30", "☕ ¡Último mate!"),
    (3, "16:00", "🥛 Merienda en 30 min: yogur griego 170 g + nueces 12 g + frutos rojos 20 g."),
    (3, "18:30", "🐟 Cena en 30 min: brótola 200 g + brócoli 200 g + huevo duro + anchoas 20 g + oliva 12 ml."),
    (3, "21:30", "🌙 Snack ancla + magnesio 300 mg."),
    (3, "22:00", "😴 A dormir."),

    # ----- VIERNES (gym 14:00, cena LIBRE) -----
    (4, "05:30", "💧 En 30 min a despertar. Agua 400 ml."),
    (4, "06:00", "🍳 Desayuno en 30 min: 4 huevos duros + queso 30 g + palta 80 g + tomate 100 g + oliva 5 ml."),
    (4, "06:15", "💊 Suplementos: Vit D3 + Omega-3."),
    (4, "10:00", "🥛 Media mañana en 30 min: yogur griego 150 g + nueces 10 g + frutillas 30 g."),
    (4, "12:00", "🍇 Pre-entreno LIVIANO en 30 min: pasas 30 g + café + agua con sal 400 ml. NO comer sólido pesado 11-14 h."),
    (4, "13:30", "🏋️ ¡Gym en 30 min! Complex B."),
    (4, "14:45", "🥤 Post-entreno en 30 min: whey 35 g + creatina 5 g + agua."),
    (4, "15:30", "🍽️ Almuerzo-merienda en 30 min: pollo 220 g + papa hervida 150 g + ensalada + palta 70 g + almendras + oliva."),
    (4, "18:30", "🎉 CENA LIBRE en 30 min. Elegí UNA: pizza 2 porciones / parrilla 250 g magra / sushi 12-15 piezas / pasta 300 g. Máx 1 vino tinto."),
    (4, "22:00", "😴 A dormir."),

    # ----- SÁBADO (descanso + bici) -----
    (5, "05:30", "💧 En 30 min a despertar. Agua 300 ml."),
    (5, "06:00", "🍳 Desayuno en 30 min: 3 huevos duros + jamón cocido magro 30 g + queso port salut 30 g + palta 50 g + tomate 100 g + oliva 5 ml."),
    (5, "06:15", "💊 Suplementos: Vit D3 + Omega-3 + Creatina 5 g."),
    (5, "09:30", "🥛 Media mañana en 30 min: cottage 150 g + frutillas 50 g + nueces 7 g."),
    (5, "12:30", "🍽️ Almuerzo en 30 min: pollo 220 g + brócoli 150 g + zapallitos hervidos 100 g + ensalada + palta 40 g + oliva 12 ml."),
    (5, "13:00", "🚴 Bici 40 min en 30 min. Zona 2, ruta plana."),
    (5, "13:30", "☕ ¡Último mate!"),
    (5, "16:00", "🐟 Merienda SARDINAS en 30 min: sardinas 100 g + palta 50 g + tomate cherry 80 g + galleta de arroz 1."),
    (5, "16:30", "⭐ Hobby / familia."),
    (5, "18:30", "🍽️ Cena en 30 min: pollo 180 g + 2 huevos duros + queso 25 g + espinaca al vapor 150 g + champignones + anchoas 15 g + oliva."),
    (5, "21:30", "🌙 Snack ancla + magnesio."),
    (5, "22:00", "😴 A dormir."),

    # ----- DOMINGO (descanso + bici + batch cooking) -----
    (6, "05:30", "💧 En 30 min a despertar. Agua 300 ml."),
    (6, "06:00", "🍳 Desayuno en 30 min: 3 huevos duros + palta 60 g + tomate 100 g + queso 30 g + oliva 5 ml."),
    (6, "06:15", "💊 Suplementos: Vit D3 + Omega-3 + Creatina 5 g."),
    (6, "09:30", "🍳 BATCH COOKING en 30 min: pollo 1,8 kg horno + 20 huevos duros + papa/boniato hervidos + verduras al vapor + aderezos."),
    (6, "13:00", "🍽️ Almuerzo en 30 min: pollo del horno 220 g + ensalada completa + palta 60 g + aceitunas + nueces + oliva."),
    (6, "13:00", "🚴 Bici 40 min en 30 min. Zona 2, al sol."),
    (6, "13:30", "☕ ¡Último mate!"),
    (6, "16:00", "🥛 Merienda en 30 min: yogur griego 200 g + nueces 10 g + cacao amargo 3 g."),
    (6, "16:30", "⭐ Hobby / hijos (30-45 min)."),
    (6, "18:30", "🍽️ Cena Caesar en 30 min: pollo 180 g + lechuga romana + huevo duro + anchoas 20 g + parmesano 15 g + aderezo."),
    (6, "21:30", "🌙 Snack ancla + magnesio."),
    (6, "22:00", "😴 A dormir. Cargar tensiómetro para lunes."),
]


def enviar_telegram(mensaje: str) -> None:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje}, timeout=15)
    r.raise_for_status()
    log.info("enviado: %s", mensaje[:50])


def main() -> None:
    log.info("iniciado — %d recordatorios cargados", len(RECORDATORIOS))
    ya_enviados_hoy: set[tuple[int, str]] = set()
    ultimo_dia = None

    while True:
        ahora = datetime.now(TZ)
        dia = ahora.weekday()   # 0 = lunes
        hhmm = ahora.strftime("%H:%M")

        # Reset diario al pasar de un día a otro.
        if dia != ultimo_dia:
            ya_enviados_hoy.clear()
            ultimo_dia = dia

        for d, hora, mensaje in RECORDATORIOS:
            key = (d, hora)
            if d == dia and hora == hhmm and key not in ya_enviados_hoy:
                try:
                    enviar_telegram(mensaje)
                    ya_enviados_hoy.add(key)
                except Exception as e:
                    log.error("fallo enviando %s: %s", key, e)

        time.sleep(30)  # tick cada 30 s → precisión de ±30 s


if __name__ == "__main__":
    main()
