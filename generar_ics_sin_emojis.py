#!/usr/bin/env python3
"""Version sin emojis en SUMMARY - mas compatible."""
import sys
sys.path.insert(0, '/home/user/Fede')
from generar_ics_recordatorios import EVENTS as ORIG, BASE_DATES, DTSTAMP_FIXED, escape, TZ
from pathlib import Path

OUT = Path("/home/user/Fede/Plan-Fede-Recordatorios-simple.ics")

# Mapa emoji → prefijo texto
def clean(txt):
    reps = [
        ("💧", "[AGUA]"), ("🍌", "[PRE]"), ("🍇", "[PRE]"), ("🥤", "[POST]"),
        ("🍳", "[COMIDA]"), ("💊", "[SUPL]"), ("🍽️", "[COMIDA]"), ("☕", "[MATE]"),
        ("🥛", "[MERIENDA]"), ("🐟", "[CENA]"), ("🌙", "[SNACK]"), ("😴", "[DORMIR]"),
        ("🚴", "[BICI]"), ("⭐", "[HOBBY]"), ("🏋️", "[GYM]"), ("🎉", "[LIBRE]"),
    ]
    for a, b in reps:
        txt = txt.replace(a, b)
    # Sacar caracteres unicode raros que queden
    return "".join(c if ord(c) < 128 or c in "áéíóúñÁÉÍÓÚÑüÜ" else "" for c in txt).strip()


def make_event(idx, dia, hora, summary, description):
    fecha = BASE_DATES[dia]
    hh, mm = hora[:2], hora[2:]
    end_mm = int(mm) + 15
    end_hh = int(hh)
    if end_mm >= 60:
        end_hh += 1
        end_mm -= 60
    dtstart_utc_hh = str((int(hh) + 3) % 24).zfill(2)
    dtend_utc_hh = str((end_hh + 3) % 24).zfill(2)
    dtstart = f"{fecha}T{dtstart_utc_hh}{mm}00Z"
    dtend = f"{fecha}T{dtend_utc_hh}{str(end_mm).zfill(2)}00Z"
    uid = f"planfede-{dia}-{hora}-{idx}@fede"

    lines = [
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{DTSTAMP_FIXED}",
        f"DTSTART:{dtstart}",
        f"DTEND:{dtend}",
        f"SUMMARY:{escape(clean(summary))}",
        f"DESCRIPTION:{escape(clean(description))}",
        f"RRULE:FREQ=WEEKLY;BYDAY={dia}",
        "STATUS:CONFIRMED",
        "TRANSP:OPAQUE",
        "SEQUENCE:0",
        "BEGIN:VALARM",
        "ACTION:DISPLAY",
        f"DESCRIPTION:{escape(clean(summary))}",
        "TRIGGER:-PT0M",
        "END:VALARM",
        "END:VEVENT",
    ]
    return "\r\n".join(lines)


def main():
    parts = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Plan Fede//ES",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Plan Fede",
    ]
    for i, (dia, hora, s, d) in enumerate(ORIG):
        parts.append(make_event(i, dia, hora, s, d))
    parts.append("END:VCALENDAR")
    OUT.write_text("\r\n".join(parts) + "\r\n", encoding="utf-8")
    print(f"OK: {OUT}")
    print(f"Eventos: {len(ORIG)}")


if __name__ == "__main__":
    main()
