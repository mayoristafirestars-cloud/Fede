#!/usr/bin/env python3
"""
Bot interactivo Plan Fede via Telegram.

Deploy: /opt/coronel-sur/backend/bot/recordatorios_plan_fede.py

Funcionalidad:
- Recordatorios programados con botones inline (Hecho/Skip/Cambio).
- Long-polling para recibir botones apretados y mensajes de texto.
- Bitácora JSONL con eventos (sent/ok/skip/edit/libre).
- Trackeo automático de kcal, proteína y quema.
- Comandos: /start /resumen /semana /nota /comi.

Variables de entorno:
  TELEGRAM_BOT_TOKEN
  TELEGRAM_CHAT_ID

Zona horaria: America/Argentina/Buenos_Aires
"""

import base64
import json
import logging
import os
import re
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

TZ = ZoneInfo("America/Argentina/Buenos_Aires")
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = str(os.environ["TELEGRAM_CHAT_ID"])
BITACORA = Path("/opt/coronel-sur/backend/bot/bitacora_fede.jsonl")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# GitHub sync (opcional — si GITHUB_TOKEN no está seteado, no sincroniza)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_OWNER = os.environ.get("GITHUB_OWNER", "mayoristafirestars-cloud")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "Fede")
GITHUB_BRANCH = os.environ.get(
    "GITHUB_BRANCH", "claude/add-doctor-nutritionist-generation-FeC6Q"
)

DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
OBJETIVO_KCAL = 2100
OBJETIVO_PROT = 190

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("recordatorios-fede")

# (dia, "HH:MM", mensaje, kcal_ingerida, proteina_g, kcal_quemada)
RECORDATORIOS = [
    # ===== LUNES (gym A) =====
    (0, "05:30", "💧 En 30 min a despertar. Vaso 300 ml + pizca de sal.", 0, 0, 0),
    (0, "06:00", "🍌 Pre-entreno en 30 min: media banana (80 g) + café 150 ml + agua con sal 300 ml.", 70, 1, 0),
    (0, "07:30", "🥤 Post-entreno + gym A hecho. En 30 min: whey 35 g + creatina 5 g + agua 300 ml.", 140, 28, 350),
    (0, "09:00", "🍳 Desayuno en 30 min: 4 huevos duros + palta 90 g + verdura tomate 100 g + queso port salut 20 g + oliva 5 ml.", 570, 32, 0),
    (0, "09:15", "💊 Suplementos en 30 min: Vit D3 + Omega-3.", 0, 0, 0),
    (0, "12:30", "🍽️ Almuerzo en 30 min: pollo 220 g + papa hervida 100 g + ensalada + oliva 12 ml + limón.", 555, 55, 0),
    (0, "13:30", "☕ ¡Último mate del día en 30 min! Después solo agua o infusiones sin cafeína.", 0, 0, 0),
    (0, "16:00", "🥛 Merienda en 30 min: yogur griego 170 g + nueces 12 g + canela.", 175, 15, 0),
    (0, "18:30", "🐟 Cena en 30 min: pescado merluza 200 g + verdura zapallo 150 g + verdura morrón 70 g + anchoa 20 g + 1 huevo duro + oliva 12 ml.", 470, 55, 0),
    (0, "21:30", "🌙 Snack ancla en 30 min: yogur griego 170 g + chía 10 g + magnesio 300 mg. Bajá luces.", 150, 12, 0),
    (0, "22:00", "😴 A dormir en 30 min. Celular afuera del cuarto.", 0, 0, 0),
    # Total lun: ~2130 kcal · 198g p · 350 quema · neto 1780

    # ===== MARTES (gym B) =====
    (1, "05:30", "💧 En 30 min a despertar. Vaso 300 ml + sal.", 0, 0, 0),
    (1, "06:00", "🍇 Pre-entreno en 30 min: pasas 30 g + café 150 ml + agua con sal 300 ml.", 85, 1, 0),
    (1, "07:30", "🥤 Post-entreno + gym B hecho. En 30 min: whey 35 g + creatina 5 g + agua 300 ml.", 140, 28, 400),
    (1, "09:00", "🍳 Desayuno en 30 min: 4 huevos duros + queso port salut 30 g + palta 80 g + verdura tomate 100 g + oliva 5 ml.", 590, 34, 0),
    (1, "09:15", "💊 Suplementos: Vit D3 + Omega-3.", 0, 0, 0),
    (1, "12:30", "🍽️ Almuerzo en 30 min: pollo 220 g + boniato hervido 100 g + ensalada + oliva 12 ml.", 530, 55, 0),
    (1, "13:30", "☕ ¡Último mate del día en 30 min!", 0, 0, 0),
    (1, "16:00", "🥛 Merienda en 30 min: cottage 200 g + fruta frutillas 30 g + canela.", 180, 24, 0),
    (1, "18:30", "🐟 Cena en 30 min: pescado salmón 180 g + verdura espinaca salteada 150 g + hongos 80 g + oliva 12 ml.", 430, 40, 0),
    (1, "21:30", "🌙 Snack ancla + magnesio 300 mg.", 150, 12, 0),
    (1, "22:00", "😴 A dormir en 30 min.", 0, 0, 0),
    # Total mar: ~2105 kcal · 194g p · 400 quema · neto 1705

    # ===== MIÉRCOLES (descanso + bici) =====
    (2, "05:30", "💧 En 30 min a despertar. Vaso 300 ml de agua.", 0, 0, 0),
    (2, "06:00", "🍳 Desayuno en 30 min: 3 huevos duros + ricota 80 g + palta 60 g + verdura tomate 100 g + oliva 5 ml.", 550, 32, 0),
    (2, "06:15", "💊 Suplementos: Vit D3 + Omega-3 + Creatina 5 g.", 0, 0, 0),
    (2, "09:30", "🥛 Media mañana en 30 min: yogur griego 200 g + nueces 10 g + fruta arándanos 20 g.", 250, 18, 0),
    (2, "12:30", "🍽️ Almuerzo en 30 min: pescado atún 180 g + 2 huevos duros + verdura espinaca 150 g + queso 30 g + ensalada + palta 60 g + oliva 15 ml.", 620, 62, 0),
    (2, "13:00", "🚴 Bici 40 min en 30 min. Zona 2 (FC 105-118 lpm), ruta plana, post-almuerzo.", 0, 0, 300),
    (2, "13:30", "☕ Último mate del día en 30 min.", 0, 0, 0),
    (2, "16:00", "🥛 Merienda en 30 min: ricota 150 g + almendras 10 g + cacao amargo 3 g.", 200, 20, 0),
    (2, "16:30", "⭐ Momento hobby en 30 min (30-45 min).", 0, 0, 0),
    (2, "18:30", "🐟 Cena en 30 min: pescado sardinas 120 g + verdura tomate 100 g + palta 60 g + aceitunas 15 g + oliva + limón.", 450, 40, 0),
    (2, "21:30", "🌙 Snack ancla + magnesio 300 mg.", 150, 12, 0),
    (2, "22:00", "😴 A dormir en 30 min.", 0, 0, 0),
    # Total mie: ~2400 kcal · 204g p · 300 quema · neto 2100

    # ===== JUEVES (gym A) =====
    (3, "05:30", "💧 En 30 min a despertar. Agua + sal.", 0, 0, 0),
    (3, "06:00", "🍌 Pre-entreno en 30 min: media banana 80 g + café + agua con sal.", 70, 1, 0),
    (3, "07:30", "🥤 Post-entreno + gym A hecho. En 30 min: whey 35 g + creatina 5 g + agua.", 140, 28, 350),
    (3, "09:00", "🍳 Desayuno diferente en 30 min: yogur griego 200 g + fruta frutillas 100 g + almendras 15 g + canela + 3 huevos duros aparte.", 550, 40, 0),
    (3, "09:15", "💊 Suplementos: Vit D3 + Omega-3.", 0, 0, 0),
    (3, "12:30", "🍽️ Almuerzo en 30 min: pollo 200 g + papa hervida 100 g + 1 huevo duro + ensalada nicoise (hojas verdes + verdura tomate) + palta 50 g + oliva 12 ml.", 620, 55, 0),
    (3, "13:30", "☕ ¡Último mate!", 0, 0, 0),
    (3, "16:00", "🥛 Merienda en 30 min: yogur griego 170 g + nueces 12 g + fruta arándanos 20 g.", 180, 15, 0),
    (3, "18:30", "🐟 Cena en 30 min: pescado merluza 200 g + verdura brócoli 200 g + 1 huevo duro + anchoa 20 g + oliva 12 ml.", 450, 50, 0),
    (3, "21:30", "🌙 Snack ancla + magnesio 300 mg.", 150, 12, 0),
    (3, "22:00", "😴 A dormir.", 0, 0, 0),
    # Total jue: ~2160 kcal · 201g p · 350 quema · neto 1810

    # ===== VIERNES (gym 14:00 + cena LIBRE) =====
    (4, "05:30", "💧 En 30 min a despertar. Agua 400 ml.", 0, 0, 0),
    (4, "06:00", "🍳 Desayuno en 30 min: 4 huevos duros + queso 30 g + palta 80 g + verdura tomate 100 g + oliva 5 ml.", 585, 35, 0),
    (4, "06:15", "💊 Suplementos: Vit D3 + Omega-3.", 0, 0, 0),
    (4, "10:00", "🥛 Media mañana en 30 min: yogur griego 150 g + nueces 10 g + fruta frutillas 30 g.", 190, 15, 0),
    (4, "12:00", "🍇 Pre-entreno LIVIANO en 30 min: pasas 30 g + café + agua con sal 400 ml. NO comer sólido pesado 11-14 h.", 85, 1, 0),
    (4, "13:30", "🏋️ ¡Gym en 30 min! Complex B.", 0, 0, 0),
    (4, "14:45", "🥤 Post-entreno en 30 min: whey 35 g + creatina 5 g + agua.", 140, 28, 400),
    (4, "15:30", "🍽️ Almuerzo-merienda en 30 min: pollo 220 g + papa hervida 150 g + ensalada + palta 70 g + almendras + oliva.", 620, 55, 0),
    (4, "18:30", "🎉 CENA LIBRE en 30 min. Elegí UNA: pizza 2 porciones / parrilla 250 g magra / sushi 12-15 piezas / pasta 300 g. Máx 1 vino tinto.", 700, 35, 0),
    (4, "22:00", "😴 A dormir.", 0, 0, 0),
    # Total vie: ~2320 kcal · 169g p · 400 quema · neto 1920

    # ===== SÁBADO (descanso + bici) =====
    (5, "05:30", "💧 En 30 min a despertar. Agua 300 ml.", 0, 0, 0),
    (5, "06:00", "🍳 Desayuno en 30 min: 3 huevos duros + jamón cocido magro 30 g + queso port salut 30 g + palta 50 g + verdura tomate 100 g + oliva 5 ml.", 500, 32, 0),
    (5, "06:15", "💊 Suplementos: Vit D3 + Omega-3 + Creatina 5 g.", 0, 0, 0),
    (5, "09:30", "🥛 Media mañana en 30 min: cottage 150 g + fruta frutillas 50 g + nueces 7 g.", 180, 22, 0),
    (5, "12:30", "🍽️ Almuerzo en 30 min: pollo 220 g + verdura brócoli 150 g + verdura zapallo hervido 100 g + ensalada + palta 40 g + oliva 12 ml.", 500, 55, 0),
    (5, "13:00", "🚴 Bici 40 min en 30 min. Zona 2, ruta plana.", 0, 0, 300),
    (5, "13:30", "☕ ¡Último mate!", 0, 0, 0),
    (5, "16:00", "🐟 Merienda en 30 min: pescado sardinas 100 g + palta 50 g + verdura tomate cherry 80 g + galleta de arroz 1.", 260, 22, 0),
    (5, "16:30", "⭐ Hobby / familia.", 0, 0, 0),
    (5, "18:30", "🍽️ Cena en 30 min: pollo 180 g + 2 huevos duros + queso 25 g + verdura espinaca al vapor 150 g + hongos + anchoa 15 g + oliva.", 500, 55, 0),
    (5, "21:30", "🌙 Snack ancla + magnesio.", 150, 12, 0),
    (5, "22:00", "😴 A dormir.", 0, 0, 0),
    # Total sab: ~2090 kcal · 198g p · 300 quema · neto 1790

    # ===== DOMINGO (descanso + bici + batch cooking) =====
    (6, "05:30", "💧 En 30 min a despertar. Agua 300 ml.", 0, 0, 0),
    (6, "06:00", "🍳 Desayuno en 30 min: 3 huevos duros + palta 60 g + verdura tomate 100 g + queso 30 g + oliva 5 ml.", 500, 28, 0),
    (6, "06:15", "💊 Suplementos: Vit D3 + Omega-3 + Creatina 5 g.", 0, 0, 0),
    (6, "09:30", "🍳 BATCH COOKING en 30 min: pollo 1,8 kg horno + 20 huevos duros + papa/boniato hervidos + verduras al vapor + aderezos.", 0, 0, 0),
    (6, "12:30", "🍽️ Almuerzo en 30 min: pollo del horno 220 g + ensalada completa + palta 60 g + aceitunas + nueces + oliva.", 620, 55, 0),
    (6, "13:30", "☕ ¡Último mate!", 0, 0, 0),
    (6, "14:00", "🚴 Bici 40 min en 30 min. Zona 2, al sol.", 0, 0, 300),
    (6, "16:00", "🥛 Merienda en 30 min: yogur griego 200 g + nueces 10 g + cacao amargo 3 g.", 195, 15, 0),
    (6, "16:30", "⭐ Hobby / hijos (30-45 min).", 0, 0, 0),
    (6, "18:30", "🍽️ Cena Caesar en 30 min: pollo 180 g + hojas verdes lechuga romana + 1 huevo duro + anchoa 20 g + parmesano 15 g + aderezo.", 470, 40, 0),
    (6, "21:30", "🌙 Snack ancla + magnesio.", 150, 12, 0),
    (6, "22:00", "😴 A dormir. Cargar tensiómetro para lunes.", 0, 0, 0),
    # Total dom: ~1935 kcal · 150g p · 300 quema · neto 1635

    # ===== WELLNESS: mindfulness, hidratación, movimiento =====
    # Diarios (todos los días): respiración, agua, journal, meditación
    *[(d, "05:35", "🌬️ Respiración 2 min + estiramiento 3 min al despertar (después del agua).", 0, 0, 0) for d in range(7)],
    *[(d, "10:30", "💧 Hidratación: 500 ml de agua entre desayuno y almuerzo.", 0, 0, 0) for d in range(7)],
    *[(d, "13:05", "🌬️ Respiración box breathing 3 min post-almuerzo (4 inhalo · 4 retengo · 4 exhalo · 4 pausa).", 0, 0, 0) for d in range(7)],
    *[(d, "15:00", "💧 Hidratación: 500 ml de agua entre almuerzo y merienda.", 0, 0, 0) for d in range(7)],
    *[(d, "21:00", "📔 Journal + gratitud 2 min. Escribí 3 cosas del día + 1 gratitud.", 0, 0, 0) for d in range(7)],
    *[(d, "21:45", "🧘 Meditación 10 min pre-sueño. App: Insight Timer / Calm / YouTube (10 min sleep).", 0, 0, 0) for d in range(7)],
    # Días laborales (Lun-Vie): micro-pausa de tarde
    *[(d, "17:00", "🧠 Micro-pausa 3 min. Lejos del celular. Cuello, hombros, mirada lejos.", 0, 0, 0) for d in range(5)],
    # Días de descanso (Mié, Sáb, Dom): sol matinal para ritmo circadiano
    *[(d, "07:00", "☀️ 10 min al sol / aire libre. Vit D natural y ritmo circadiano.", 0, 0, 0) for d in [2, 5, 6]],
    # Caminatas post-almuerzo en días sin bici (Lun, Mar, Jue)
    *[(d, "13:15", "🚶 Caminata 10 min post-almuerzo. Zona 2 tranquila, al aire libre si podés.", 0, 0, 0) for d in [0, 1, 3]],
]

# Index por key = "Dia-HH:MM" para lookup rápido
RECORDATORIOS_BY_KEY = {
    f"{DIAS[d]}-{h}": (d, h, m, k, p, q) for d, h, m, k, p, q in RECORDATORIOS
}


# ============ BITÁCORA ============

_lock = threading.Lock()


def bitacora_append(kind, key="", texto="", comentario="", kcal=0, prot=0, quema=0):
    BITACORA.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(TZ).isoformat(),
        "kind": kind,
        "key": key,
        "texto": texto,
        "comentario": comentario,
        "kcal": kcal,
        "prot": prot,
        "quema": quema,
    }
    with _lock:
        with BITACORA.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def bitacora_read(desde=None):
    if not BITACORA.exists():
        return []
    out = []
    with BITACORA.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                e = json.loads(line)
            except Exception:
                continue
            if desde and e.get("ts", "") < desde.isoformat():
                continue
            out.append(e)
    return out


# ============ TELEGRAM API ============

def _post(method, payload):
    try:
        r = requests.post(f"{API}/{method}", json=payload, timeout=15)
        if not r.ok:
            log.error("%s fail: %s", method, r.text[:200])
        return r
    except Exception as e:
        log.error("%s exc: %s", method, e)
        return None


def enviar(texto, reply_markup=None):
    payload = {"chat_id": CHAT_ID, "text": texto}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    _post("sendMessage", payload)


def enviar_recordatorio(key, mensaje):
    kb = {
        "inline_keyboard": [[
            {"text": "✅ Hecho", "callback_data": f"ok|{key}"},
            {"text": "⏭️ Skip", "callback_data": f"skip|{key}"},
            {"text": "✏️ Cambio", "callback_data": f"edit|{key}"},
        ]]
    }
    enviar(mensaje, reply_markup=kb)
    d, h, m, k, p, q = RECORDATORIOS_BY_KEY[key]
    bitacora_append("sent", key, mensaje, kcal=k, prot=p, quema=q)


def answer_callback(cbq_id, texto=""):
    _post("answerCallbackQuery", {"callback_query_id": cbq_id, "text": texto})


# ============ CÁLCULO ============

def calcular_dia(events):
    """Totales del día basados en eventos ok + edits + libres."""
    kcal_in = 0
    prot = 0
    quema = 0
    ok_keys = set()
    skip_keys = set()
    edit_keys = set()
    sent_keys = set()

    for e in events:
        k = e.get("kind")
        if k == "sent":
            sent_keys.add(e.get("key", ""))
        elif k == "ok":
            ok_keys.add(e.get("key", ""))
            base = RECORDATORIOS_BY_KEY.get(e.get("key", ""))
            if base:
                _, _, _, kk, pp, qq = base
                kcal_in += kk
                prot += pp
                quema += qq
        elif k == "skip":
            skip_keys.add(e.get("key", ""))
        elif k == "edit":
            edit_keys.add(e.get("key", ""))
            kcal_in += e.get("kcal", 0) or 0
            prot += e.get("prot", 0) or 0
        elif k == "libre":
            kcal_in += e.get("kcal", 0) or 0
            prot += e.get("prot", 0) or 0

    return {
        "kcal_in": kcal_in,
        "prot": prot,
        "quema": quema,
        "neto": kcal_in - quema,
        "ok": len(ok_keys),
        "skip": len(skip_keys),
        "edit": len(edit_keys),
        "sent": len(sent_keys),
    }


def resumen_hoy():
    ahora = datetime.now(TZ)
    hoy_ini = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
    events = bitacora_read(desde=hoy_ini)
    stats = calcular_dia(events)
    pct = int(100 * stats["ok"] / stats["sent"]) if stats["sent"] else 0

    edits = [e for e in events if e.get("kind") == "edit" and e.get("comentario")]
    libres = [e for e in events if e.get("kind") == "libre" and e.get("comentario")]

    linea_edits = ""
    if edits:
        linea_edits = "\n\n✏️ Cambios:\n" + "\n".join(
            f"• {e.get('key', '')}: {e.get('comentario', '')}" for e in edits[-5:]
        )
    linea_libres = ""
    if libres:
        linea_libres = "\n\n📝 Notas:\n" + "\n".join(
            f"• {e.get('comentario', '')}" for e in libres[-5:]
        )

    return (
        f"📊 HOY {DIAS[ahora.weekday()]} {ahora.strftime('%d/%m')}\n"
        f"━━━━━━━━━━━━━━\n"
        f"✅ Cumplidas: {stats['ok']}/{stats['sent']} ({pct}%)\n"
        f"⏭️ Skips: {stats['skip']}\n"
        f"✏️ Modificadas: {stats['edit']}\n\n"
        f"🍽️ Kcal ingeridas: {stats['kcal_in']} / {OBJETIVO_KCAL}\n"
        f"🥩 Proteína: {stats['prot']} g / {OBJETIVO_PROT} g\n"
        f"🔥 Quemadas: {stats['quema']} kcal\n"
        f"⚖️ Balance neto: {stats['neto']} kcal"
        f"{linea_edits}{linea_libres}"
    )


def resumen_semana():
    ahora = datetime.now(TZ)
    desde = ahora - timedelta(days=7)
    events = bitacora_read(desde=desde)

    por_dia = {}
    for e in events:
        try:
            d = datetime.fromisoformat(e["ts"]).date()
        except Exception:
            continue
        por_dia.setdefault(d, []).append(e)

    lineas = ["📈 ÚLTIMOS 7 DÍAS", "━━━━━━━━━━━━━━"]
    total_kcal = 0
    total_prot = 0
    total_quema = 0
    total_ok = 0
    total_sent = 0
    for d in sorted(por_dia.keys()):
        s = calcular_dia(por_dia[d])
        total_kcal += s["kcal_in"]
        total_prot += s["prot"]
        total_quema += s["quema"]
        total_ok += s["ok"]
        total_sent += s["sent"]
        dow = DIAS[d.weekday()]
        pct = int(100 * s["ok"] / s["sent"]) if s["sent"] else 0
        lineas.append(
            f"{dow} {d.strftime('%d/%m')}: {s['kcal_in']} kcal · {s['prot']}g p · {pct}% ✅"
        )

    n = len(por_dia) or 1
    lineas.append("━━━━━━━━━━━━━━")
    lineas.append(
        f"Promedio: {total_kcal // n} kcal · {total_prot // n}g p · "
        f"{total_quema // n} quema"
    )
    lineas.append(
        f"Adherencia global: "
        f"{int(100 * total_ok / total_sent) if total_sent else 0}%"
    )
    return "\n".join(lineas)


# ============ GITHUB SYNC ============

def generar_reporte_dia_md(events, fecha):
    """Genera markdown legible del día para que agentes lo lean."""
    stats = calcular_dia(events)
    pct = int(100 * stats["ok"] / stats["sent"]) if stats["sent"] else 0
    dow = DIAS[fecha.weekday()]

    lineas = [
        f"# Bitácora Fede — {fecha.isoformat()} ({dow})",
        "",
        "## Resumen",
        f"- **Adherencia**: {stats['ok']}/{stats['sent']} recordatorios ({pct}%)",
        f"- **Skips**: {stats['skip']} · **Modificadas**: {stats['edit']}",
        f"- **Kcal ingeridas**: {stats['kcal_in']} / {OBJETIVO_KCAL}",
        f"- **Proteína**: {stats['prot']} g / {OBJETIVO_PROT} g",
        f"- **Kcal quemadas**: {stats['quema']}",
        f"- **Balance neto**: {stats['neto']} kcal",
        "",
        "## Detalle recordatorios",
        "",
        "| Hora | Recordatorio | Estado | Kcal | Prot |",
        "|---|---|---|---|---|",
    ]

    estados = {}
    for e in events:
        k = e.get("kind")
        key = e.get("key", "")
        if k in ("ok", "skip", "edit") and key:
            estados[key] = k

    dia_num = fecha.weekday()
    dia_recordatorios = [
        (h, m, kk, pp) for d, h, m, kk, pp, qq in RECORDATORIOS if d == dia_num
    ]
    emoji_map = {"ok": "✅", "skip": "⏭️", "edit": "✏️", "-": "—"}
    for h, m, kk, pp in dia_recordatorios:
        key = f"{DIAS[dia_num]}-{h}"
        estado = estados.get(key, "-")
        emoji = emoji_map[estado]
        m_short = (m[:70] + "…") if len(m) > 70 else m
        kcal_show = kk if estado == "ok" else "-"
        prot_show = pp if estado == "ok" else "-"
        lineas.append(f"| {h} | {m_short} | {emoji} | {kcal_show} | {prot_show} |")

    lineas.append("")

    edits = [e for e in events if e.get("kind") == "edit" and e.get("comentario")]
    if edits:
        lineas.append("## Cambios anotados (✏️)")
        for e in edits:
            k_str = (
                f" — {e['kcal']} kcal · {e['prot']}g p"
                if e.get("kcal") else ""
            )
            lineas.append(f"- **{e.get('key', '')}**: {e['comentario']}{k_str}")
        lineas.append("")

    libres = [e for e in events if e.get("kind") == "libre" and e.get("comentario")]
    if libres:
        lineas.append("## Notas libres (comidas extra, comentarios)")
        for e in libres:
            k_str = (
                f" — {e['kcal']} kcal · {e['prot']}g p"
                if e.get("kcal") else ""
            )
            lineas.append(f"- {e['comentario']}{k_str}")
        lineas.append("")

    lineas.append("---")
    lineas.append("*Generado automáticamente por el bot Plan Fede.*")
    return "\n".join(lineas)


def _github_put_file(path, contenido_str, mensaje_commit):
    """Sube o actualiza un archivo en el repo via GitHub API."""
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    r = requests.get(
        url, params={"ref": GITHUB_BRANCH}, headers=headers, timeout=15
    )
    sha = r.json().get("sha") if r.status_code == 200 else None
    body = {
        "message": mensaje_commit,
        "content": base64.b64encode(contenido_str.encode("utf-8")).decode("ascii"),
        "branch": GITHUB_BRANCH,
    }
    if sha:
        body["sha"] = sha
    r = requests.put(url, json=body, headers=headers, timeout=30)
    if r.ok:
        log.info("sync %s OK", path)
        return True
    log.error("sync %s FAIL %d: %s", path, r.status_code, r.text[:200])
    return False


def sync_a_github(fecha):
    """Genera reporte + jsonl y los sube al repo GitHub."""
    if not GITHUB_TOKEN:
        log.warning("GITHUB_TOKEN no configurado, saltando sync")
        return False

    ini = datetime.combine(fecha, datetime.min.time(), tzinfo=TZ)
    fin = ini + timedelta(days=1)
    todos = bitacora_read(desde=ini)
    events = [e for e in todos if e.get("ts", "") < fin.isoformat()]

    if not events:
        log.info("sync %s: sin eventos, saltando", fecha)
        return False

    md = generar_reporte_dia_md(events, fecha)
    jsonl_body = "\n".join(json.dumps(e, ensure_ascii=False) for e in events) + "\n"

    msg = f"bot: bitácora {fecha.isoformat()}"
    ok1 = _github_put_file(f"salud/bitacora/{fecha.isoformat()}.md", md, msg)
    ok2 = _github_put_file(
        f"salud/bitacora/raw/{fecha.isoformat()}.jsonl", jsonl_body, msg
    )
    return ok1 and ok2


# ============ PARSE ============

_num_re = re.compile(r"\b(\d+)\b")


def parse_kcal_prot(text):
    """Extrae últimos 1-2 números como kcal, prot."""
    nums = _num_re.findall(text)
    if len(nums) >= 2:
        return int(nums[-2]), int(nums[-1])
    if len(nums) == 1:
        return int(nums[-1]), 0
    return 0, 0


# ============ POLLING ============

def polling_loop():
    # Descartar backlog al arrancar: pedir el último y avanzar offset
    try:
        r = requests.get(
            f"{API}/getUpdates", params={"offset": -1, "timeout": 0}, timeout=10
        )
        j = r.json()
        results = j.get("result", []) if j.get("ok") else []
        offset = results[-1]["update_id"] + 1 if results else 0
    except Exception as e:
        log.error("polling startup: %s", e)
        offset = 0
    log.info("polling iniciado desde offset=%d", offset)

    esperando_edit = {}  # chat_id -> key
    iter_count = 0

    while True:
        iter_count += 1
        try:
            r = requests.get(
                f"{API}/getUpdates",
                params={"offset": offset, "timeout": 25},
                timeout=30,
            )
            data = r.json()
            if not data.get("ok"):
                log.warning("Telegram no-ok en iter %d: %s", iter_count, data)
                time.sleep(3)
                continue
            results = data.get("result", [])
            if results:
                log.info("iter %d: %d updates recibidos", iter_count, len(results))
            elif iter_count % 20 == 0:
                # Heartbeat cada ~20 iters (~10 min) para saber que sigue vivo
                log.info("polling vivo (iter %d, offset=%d)", iter_count, offset)
            for update in results:
                offset = update["update_id"] + 1
                try:
                    _handle_update(update, esperando_edit)
                except Exception as e:
                    log.error("handle update fail: %s | update=%s", e, update)
        except requests.Timeout:
            # Timeout es normal en long-poll cuando no hay updates
            continue
        except Exception as e:
            log.error("polling iter %d: %s", iter_count, e)
            time.sleep(3)


def _handle_update(update, esperando_edit):
    # ---- callback_query (botón apretado) ----
    if "callback_query" in update:
        cq = update["callback_query"]
        payload = cq.get("data", "")
        if "|" in payload:
            action, key = payload.split("|", 1)
        else:
            action, key = payload, ""
        texto_orig = cq.get("message", {}).get("text", "")
        base = RECORDATORIOS_BY_KEY.get(key)
        if action == "ok":
            k = base[3] if base else 0
            p = base[4] if base else 0
            q = base[5] if base else 0
            bitacora_append("ok", key, texto_orig, kcal=k, prot=p, quema=q)
            answer_callback(cq["id"], "✅ Registrado")
        elif action == "skip":
            bitacora_append("skip", key, texto_orig)
            answer_callback(cq["id"], "⏭️ Salteado")
        elif action == "edit":
            answer_callback(cq["id"], "Contame el cambio")
            esperando_edit[str(cq["from"]["id"])] = key
            enviar(
                f"✏️ Contame qué comiste/hiciste distinto para: {key}\n\n"
                f"Formato opcional al final: <kcal> <proteína g>\n"
                f"Ej: 'sándwich pollo 450 30' → 450 kcal, 30g proteína.\n"
                f"Sin números → anota solo el texto."
            )
        return

    # ---- mensaje de texto ----
    msg = update.get("message", {})
    text = (msg.get("text") or "").strip()
    chat_id = str(msg.get("chat", {}).get("id", ""))
    if not text or not chat_id:
        return
    log.info("msg recibido de chat=%s: %r", chat_id, text[:100])

    if text.startswith("/ping"):
        enviar("🏓 pong")
        return
    if text.startswith("/start"):
        enviar(
            "👋 Bot Plan Fede activo.\n\n"
            "Comandos:\n"
            "/resumen — resumen de HOY (kcal, proteína, adherencia)\n"
            "/semana — últimos 7 días\n"
            "/sync — subir bitácora de hoy a GitHub ya\n"
            "/nota <texto> — anotación libre\n"
            "/comi <texto> <kcal> <prot> — anotar comida extra\n\n"
            "En cada recordatorio tenés los botones:\n"
            "✅ Hecho · ⏭️ Skip · ✏️ Cambio\n\n"
            "Auto-sync a GitHub todas las noches 23:30.\n"
            "Los agentes Nutri y Médico leen esa carpeta."
        )
    elif text.startswith("/resumen"):
        enviar(resumen_hoy())
    elif text.startswith("/semana"):
        enviar(resumen_semana())
    elif text.startswith("/sync"):
        if not GITHUB_TOKEN:
            enviar("❌ GITHUB_TOKEN no configurado en el service.")
        else:
            hoy = datetime.now(TZ).date()
            if sync_a_github(hoy):
                enviar(f"✅ Sync a GitHub OK: salud/bitacora/{hoy.isoformat()}.md")
            else:
                enviar("❌ Sync falló. Ver logs del service.")
    elif text.startswith("/nota "):
        nota = text[6:].strip()
        kcal, prot = parse_kcal_prot(nota)
        bitacora_append("libre", "", "", comentario=nota, kcal=kcal, prot=prot)
        respuesta = f"📝 Anotado: {nota}"
        if kcal:
            respuesta += f"\n({kcal} kcal · {prot}g p)"
        enviar(respuesta)
    elif text.startswith("/comi "):
        c = text[6:].strip()
        kcal, prot = parse_kcal_prot(c)
        bitacora_append("libre", "", "", comentario=c, kcal=kcal, prot=prot)
        enviar(f"🍽️ Anotado: {c}\n{kcal} kcal · {prot}g p")
    elif chat_id in esperando_edit:
        key = esperando_edit.pop(chat_id)
        kcal, prot = parse_kcal_prot(text)
        bitacora_append("edit", key, "", comentario=text, kcal=kcal, prot=prot)
        respuesta = f"✅ Cambio registrado en {key}: {text}"
        if kcal:
            respuesta += f"\n({kcal} kcal · {prot}g p)"
        enviar(respuesta)
    else:
        kcal, prot = parse_kcal_prot(text)
        bitacora_append("libre", "", "", comentario=text, kcal=kcal, prot=prot)
        respuesta = f"📝 Anotado: {text}"
        if kcal:
            respuesta += f"\n({kcal} kcal · {prot}g p)"
        respuesta += "\n\n(Comandos: /start)"
        enviar(respuesta)


# ============ SCHEDULER ============

def cargar_enviados_hoy():
    hoy_ini = datetime.now(TZ).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    events = bitacora_read(desde=hoy_ini)
    return {e.get("key", "") for e in events if e.get("kind") == "sent"}


def scheduler_loop():
    log.info(
        "scheduler iniciado — %d recordatorios cargados", len(RECORDATORIOS)
    )
    ya_enviados = cargar_enviados_hoy()
    ultimo_dia = datetime.now(TZ).weekday()
    ultimo_sync = None
    while True:
        ahora = datetime.now(TZ)
        dia = ahora.weekday()
        hhmm = ahora.strftime("%H:%M")
        if dia != ultimo_dia:
            ya_enviados = set()
            ultimo_dia = dia

        # Sync diario a GitHub a partir de las 23:30
        if (ahora.hour == 23 and ahora.minute >= 30) or ahora.hour >= 0 and ahora.hour < 5:
            hoy_date = ahora.date()
            if ultimo_sync != hoy_date and GITHUB_TOKEN:
                try:
                    if sync_a_github(hoy_date):
                        ultimo_sync = hoy_date
                        log.info("sync diario OK para %s", hoy_date)
                except Exception as e:
                    log.error("sync diario error: %s", e)

        for d, hora, mensaje, *_ in RECORDATORIOS:
            key = f"{DIAS[d]}-{hora}"
            if d == dia and hora == hhmm and key not in ya_enviados:
                try:
                    enviar_recordatorio(key, mensaje)
                    ya_enviados.add(key)
                except Exception as e:
                    log.error("scheduler send fail %s: %s", key, e)
        time.sleep(30)


# ============ MAIN ============

def main():
    try:
        requests.post(f"{API}/deleteWebhook", timeout=10)
    except Exception:
        pass
    log.info("iniciado — %d recordatorios cargados", len(RECORDATORIOS))
    t = threading.Thread(target=polling_loop, daemon=True)
    t.start()
    scheduler_loop()


if __name__ == "__main__":
    main()
