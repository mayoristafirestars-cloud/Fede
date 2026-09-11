#!/usr/bin/env python3
"""PDF de la rutina de gym Fede — Cadenas de movimientos.

Diseño moderno, una hoja por día con ejercicios claros y grandes.
"""
from fpdf import FPDF
from pathlib import Path

OUT = Path("/home/user/Fede/Plan-Fede-Rutina-Cadenas.pdf")

# Paleta base
NAVY = (30, 41, 59)
SLATE = (71, 85, 105)
GRAY_LIGHT = (241, 245, 249)
GRAY_MID = (203, 213, 225)
WHITE = (255, 255, 255)
GREEN = (34, 197, 94)
ORANGE = (249, 115, 22)
RED = (239, 68, 68)

# Paleta por día (mismos colores que el PDF de dieta)
DIAS_COLOR = {
    "LUNES":     (59, 130, 246),
    "MARTES":    (16, 185, 129),
    "MIÉRCOLES": (245, 158, 11),
    "JUEVES":    (168, 85, 247),
    "VIERNES":   (239, 68, 68),
    "SÁBADO":    (14, 165, 233),
    "DOMINGO":   (139, 92, 246),
}

# Rutina por día
RUTINA = {
    "LUNES": {
        "sesion": "Superior A",
        "hora": "07:00",
        "duracion": "50-55 min",
        "patrones": "Empuje H + Tracción H + Empuje V + Carry",
        "calentamiento": [
            "Cinta o bici suave 3 min (FC hasta 90-100 lpm)",
            "Band pull-apart 15 reps",
            "Rotación torácica en cuadrupedia 10/lado",
            "Bear crawl 20 pasos",
            "Scapular push-ups 10",
            "1-2 series de aproximación del primer ejercicio",
        ],
        "ejercicios": [
            {"n": 1, "nombre": "Press banca mancuernas", "sr": "3 × 8-10", "rir": "3-4", "desc": "120s",
             "notas": "Escápulas retraídas · pies firmes · bajar controlado · exhalar al subir"},
            {"n": 2, "nombre": "Remo mancuerna a un brazo", "sr": "3 × 8-10/lado", "rir": "3", "desc": "90s",
             "notas": "Apoyo banco · torso paralelo · tirar con el codo · apretar omóplato"},
            {"n": 3, "nombre": "Landmine press a una mano", "sr": "3 × 8-10/lado", "rir": "3", "desc": "90s",
             "notas": "Barra en pivot · empuje diagonal · core apretado · sin arquear lumbar"},
            {"n": 4, "nombre": "Remo polea baja neutro", "sr": "2 × 10-12", "rir": "3", "desc": "75s",
             "notas": "Agarre neutro (triángulo) · torso vertical · apretar omóplatos al final"},
            {"n": 5, "nombre": "Pallof press de pie", "sr": "3 × 10-12/lado", "rir": "2", "desc": "60s",
             "notas": "Anti-rotación · polea a la altura del pecho · empujar sin girar el torso"},
            {"n": 6, "nombre": "Suitcase carry", "sr": "2 × 20-25 m/lado", "rir": "2", "desc": "75s",
             "notas": "Mancuerna pesada de un lado · caminar erguido · sin inclinarse · core apretado"},
            {"n": 7, "nombre": "Plancha", "sr": "3 × máx sostenible", "rir": "-", "desc": "45s",
             "notas": "Cadera alineada · respirar sin aguantar el aire"},
        ]
    },
    "MARTES": {
        "sesion": "Inferior A",
        "hora": "07:00",
        "duracion": "55-60 min",
        "patrones": "Sentadilla + Locomoción + Bisagra + Carry",
        "calentamiento": [
            "Cinta o bici suave 3 min (FC hasta 90-100 lpm)",
            "Hip circles 10/lado",
            "Posición 90/90 con transferencia 8/lado",
            "Sentadilla con peso corporal profunda 10",
            "Bisagra sin peso 10",
            "Dead bug 8/lado",
            "1-2 series de aproximación del goblet squat",
        ],
        "ejercicios": [
            {"n": 1, "nombre": "Goblet squat", "sr": "3 × 8-10", "rir": "3-4", "desc": "120s",
             "notas": "Mancuerna al pecho · talones al piso · rodillas siguen los pies · profundidad limpia"},
            {"n": 2, "nombre": "Zancada caminando con mancuernas", "sr": "2 × 8 pasos/lado", "rir": "3", "desc": "90s",
             "notas": "Locomoción cargada · paso amplio · rodilla trasera casi al piso · empujar con el talón delantero"},
            {"n": 3, "nombre": "Peso muerto rumano con mancuernas", "sr": "3 × 8-10", "rir": "3", "desc": "90s",
             "notas": "Bisagra de cadera · espalda neutra · sentir isquios · no llegar hasta el piso"},
            {"n": 4, "nombre": "Zancada búlgara", "sr": "2 × 8/lado", "rir": "3", "desc": "75s",
             "notas": "Pie trasero apoyado en banco · unilateral · corrige asimetrías"},
            {"n": 5, "nombre": "Farmer walk bilateral", "sr": "2 × 25-30 m", "rir": "2", "desc": "75s",
             "notas": "Mancuernas pesadas a los costados · caminar erguido · agarre firme · respiración controlada"},
            {"n": 6, "nombre": "Dead bug", "sr": "3 × 10/lado", "rir": "-", "desc": "45s",
             "notas": "Lumbar pegada al piso · movimiento lento · base de control lumbo-pélvico"},
        ]
    },
    "JUEVES": {
        "sesion": "Superior B",
        "hora": "07:00",
        "duracion": "50-55 min",
        "patrones": "Tracción V + Empuje V + Empuje H + Carry",
        "calentamiento": [
            "Cinta o bici suave 3 min",
            "Band pull-apart 15 reps",
            "Rotación torácica 10/lado",
            "Bear crawl 20 pasos",
            "Face pull con banda 15",
            "1-2 series de aproximación del jalón",
        ],
        "ejercicios": [
            {"n": 1, "nombre": "Jalón al pecho neutro / dominada asistida", "sr": "3 × 8-10", "rir": "3-4", "desc": "120s",
             "notas": "Agarre neutro · tirar hasta pecho alto · sentir dorsal · sin balanceo"},
            {"n": 2, "nombre": "Press inclinado mancuernas 30°", "sr": "3 × 8-10", "rir": "3", "desc": "90s",
             "notas": "Banco a 30° · bajar hasta sentir estiramiento pecho superior · exhalar al subir"},
            {"n": 3, "nombre": "Push press ligero mancuernas", "sr": "3 × 8-10", "rir": "3", "desc": "90s",
             "notas": "Cadera + piernas dan impulso · empuje vertical integrado · carga LIGERA · sin fallo"},
            {"n": 4, "nombre": "Remo polea sentado neutro", "sr": "3 × 10-12", "rir": "3", "desc": "90s",
             "notas": "Espalda recta · tirar con el codo · apretar omóplatos al final · sin encorvar"},
            {"n": 5, "nombre": "Waiter carry", "sr": "2 × 15-20 m/lado", "rir": "2", "desc": "75s",
             "notas": "Mancuerna arriba (brazo estirado) · caminar erguido · core apretado · un lado a la vez"},
            {"n": 6, "nombre": "Plancha con toque de hombro", "sr": "3 × 10/lado", "rir": "-", "desc": "45s",
             "notas": "Anti-rotación · cadera no rota al tocar el hombro contrario"},
        ]
    },
    "VIERNES": {
        "sesion": "Inferior B",
        "hora": "13:30",
        "duracion": "55-60 min",
        "patrones": "Bisagra fuerte + Sentadilla unilateral + Integrados",
        "calentamiento": [
            "Cinta o bici suave 3 min",
            "Hip circles 10/lado",
            "Posición 90/90 8/lado",
            "Bisagra sin peso 10",
            "Sentadilla búlgara sin peso 8/lado",
            "1-2 series de aproximación del trap bar (muy liviano)",
        ],
        "ejercicios": [
            {"n": 1, "nombre": "Peso muerto Trap bar (hex)", "sr": "3 × 6-8", "rir": "3-4", "desc": "150s",
             "notas": "EXHALAR EN EL ESFUERZO · NUNCA aguantar el aire · barra hexagonal, brazos a los costados"},
            {"n": 2, "nombre": "Hip thrust con barra", "sr": "3 × 8-10", "rir": "3", "desc": "90s",
             "notas": "Espalda alta en banco · pies firmes · apretar glúteos arriba · pausa 1 seg"},
            {"n": 3, "nombre": "Sentadilla búlgara mancuernas", "sr": "2 × 8/lado", "rir": "3", "desc": "90s",
             "notas": "Pie trasero apoyado · empujar con el talón delantero · unilateral"},
            {"n": 4, "nombre": "Kettlebell swing (LIGERO)", "sr": "3 × 8-10", "rir": "2-3", "desc": "90-120s",
             "notas": "Bisagra explosiva · carga MUY ligera · series cortas · descanso largo · NO sostener FC alta"},
            {"n": 5, "nombre": "Farmer walk PESADO", "sr": "2 × 30 m", "rir": "2", "desc": "90s",
             "notas": "Mancuernas más pesadas del día · agarre + core + postura · el ejercicio más funcional"},
            {"n": 6, "nombre": "Turkish get-up (SIN PESO)", "sr": "2 × 2-3/lado", "rir": "-", "desc": "90s",
             "notas": "Solo el patrón esta fase · movimiento lento · integra todo el cuerpo · se agrega peso en Mes 3"},
        ]
    },
}


class PDF(FPDF):
    def __init__(self):
        super().__init__(format="A4", unit="mm")
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(left=15, top=15, right=15)


def draw_rect_filled(pdf, x, y, w, h, color):
    pdf.set_fill_color(*color)
    pdf.rect(x, y, w, h, style="F")


def cover_page(pdf):
    pdf.add_page()

    # Header hero
    draw_rect_filled(pdf, 0, 0, 210, 80, NAVY)

    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 30)
    pdf.set_xy(15, 20)
    pdf.cell(180, 12, "PLAN GYM FEDE")

    pdf.set_font("Helvetica", "", 18)
    pdf.set_xy(15, 36)
    pdf.cell(180, 8, "Cadenas de movimientos · Movement Pattern Training")

    pdf.set_font("Helvetica", "", 12)
    pdf.set_xy(15, 55)
    pdf.cell(180, 6, "4 dias/semana · 12 semanas · Vigente desde 2026-09-11")

    # Cuadro resumen
    y0 = 95
    draw_rect_filled(pdf, 15, y0, 180, 70, GRAY_LIGHT)

    pdf.set_text_color(*NAVY)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_xy(20, y0 + 6)
    pdf.cell(170, 8, "FILOSOFIA DEL BLOQUE")

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*SLATE)

    resumen = [
        "Movimientos multi-articulares por patron funcional (no aislamiento)",
        "Patrones: empuje, traccion, sentadilla, bisagra, carga, rotacion",
        "Series y descansos tradicionales (NO complexes ni HIIT)",
        "FC de trabajo <=121 lpm hasta ECG (restriccion medica activa)",
        "RIR nunca 0 - sin fallo absoluto",
        "Loaded carries (farmer, suitcase, waiter) = bajo riesgo articular",
        "Turkish get-up sin peso las primeras semanas (progresion)",
        "Fase actual: Adaptacion (RIR 3-4) - por sueno fragil actual",
    ]

    y = y0 + 20
    for item in resumen:
        pdf.set_xy(20, y)
        pdf.cell(5, 5, "-")
        pdf.set_xy(25, y)
        pdf.cell(170, 5, item)
        y += 6

    # Estructura semanal
    y0 = 180
    pdf.set_text_color(*NAVY)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_xy(15, y0)
    pdf.cell(180, 8, "LA SEMANA")

    dias_estruc = [
        ("LUNES", "07:00", "Superior A", "Empuje H + Traccion H + Carry"),
        ("MARTES", "07:00", "Inferior A", "Sentadilla + Locomocion + Carry"),
        ("MIÉRCOLES", "-", "DESCANSO", "Bici zona 2 40 min"),
        ("JUEVES", "07:00", "Superior B", "Traccion V + Empuje V + Carry"),
        ("VIERNES", "13:30", "Inferior B", "Bisagra fuerte + Integrados"),
        ("SÁBADO", "-", "DESCANSO", "Bici zona 2 40 min"),
        ("DOMINGO", "-", "DESCANSO", "Bici zona 2 40 min + Batch"),
    ]

    y = y0 + 12
    for dia, hora, ses, foco in dias_estruc:
        color = DIAS_COLOR[dia]
        draw_rect_filled(pdf, 15, y, 4, 10, color)
        draw_rect_filled(pdf, 19, y, 176, 10, GRAY_LIGHT)

        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*NAVY)
        pdf.set_xy(22, y + 2)
        pdf.cell(30, 6, dia)

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*SLATE)
        pdf.set_xy(52, y + 2)
        pdf.cell(15, 6, hora)

        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*NAVY)
        pdf.set_xy(70, y + 2)
        pdf.cell(30, 6, ses)

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*SLATE)
        pdf.set_xy(100, y + 2)
        pdf.cell(95, 6, foco)

        y += 11


def day_page(pdf, dia, info):
    pdf.add_page()

    color = DIAS_COLOR[dia]

    # Header hero del día
    draw_rect_filled(pdf, 0, 0, 210, 32, color)

    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_xy(15, 6)
    pdf.cell(120, 9, dia)

    pdf.set_font("Helvetica", "", 12)
    pdf.set_xy(15, 17)
    pdf.cell(120, 6, f"{info['sesion']} · {info['hora']} · {info['duracion']}")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_xy(15, 24)
    pdf.cell(180, 5, f"Patrones: {info['patrones']}")

    # Duración badge
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(0.4)
    pdf.rect(155, 8, 40, 10, style="D")
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(155, 8)
    pdf.cell(40, 10, info["duracion"], align="C")

    y = 38

    # Calentamiento
    draw_rect_filled(pdf, 15, y, 4, 8, ORANGE)
    pdf.set_text_color(*NAVY)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_xy(22, y + 1)
    pdf.cell(170, 6, "CALENTAMIENTO (8 min)")
    y += 10

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*SLATE)
    for item in info["calentamiento"]:
        pdf.set_xy(22, y)
        pdf.cell(5, 4, "-")
        pdf.set_xy(27, y)
        pdf.cell(165, 4, item)
        y += 4.5
    y += 3

    # Ejercicios
    draw_rect_filled(pdf, 15, y, 4, 8, color)
    pdf.set_text_color(*NAVY)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_xy(22, y + 1)
    pdf.cell(170, 6, "SESION - EJERCICIOS")
    y += 10

    for ej in info["ejercicios"]:
        # Card por ejercicio
        card_h = 15

        # Fondo card
        draw_rect_filled(pdf, 15, y, 180, card_h, WHITE)
        pdf.set_draw_color(*GRAY_MID)
        pdf.set_line_width(0.2)
        pdf.rect(15, y, 180, card_h, style="D")

        # Barrita color
        draw_rect_filled(pdf, 15, y, 3, card_h, color)

        # Número en cuadrado con color
        pdf.set_fill_color(*color)
        pdf.rect(21, y + 4, 7, 7, style="F")
        pdf.set_text_color(*WHITE)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_xy(21, y + 4)
        pdf.cell(7, 7, str(ej["n"]), align="C")

        # Nombre ejercicio
        pdf.set_text_color(*NAVY)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_xy(32, y + 2)
        pdf.cell(105, 5, ej["nombre"])

        # Series x reps y RIR y descanso
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*color)
        pdf.set_xy(140, y + 2)
        pdf.cell(55, 5, f"{ej['sr']} · RIR {ej['rir']} · {ej['desc']}")

        # Notas
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*SLATE)
        pdf.set_xy(32, y + 8)
        pdf.multi_cell(160, 3.5, ej["notas"])

        y += card_h + 1


def notes_page(pdf):
    pdf.add_page()

    draw_rect_filled(pdf, 0, 0, 210, 40, NAVY)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_xy(15, 15)
    pdf.cell(180, 10, "REGLAS DE ORO")

    y = 55

    secciones = [
        ("REGLAS QUE NO SE ROMPEN", [
            "Calentamiento SIEMPRE 8 min - no negociable",
            "FC de trabajo <=121 lpm (restriccion vigente hasta ECG)",
            "Exhalar en el esfuerzo, especialmente trap bar y push press",
            "NUNCA Valsalva prolongada (aguantar el aire) - peligroso con perfil CV",
            "RIR nunca 0 - sin fallo absoluto",
            "Tecnica antes que carga - si se rompe la forma, bajas peso",
            "Si dormiste <6h - sacas 1 serie de cada principal",
        ], RED),
        ("SISTEMA RIR (Reps in Reserve)", [
            "RIR = cuantas reps te quedan al terminar la serie",
            "RIR 3-4 = te quedan 3-4 reps (comodo, tecnica primero)",
            "RIR 2-3 = te quedan 2-3 reps (empujar volumen)",
            "RIR 1-2 = te quedan 1-2 reps (mes 3, no antes)",
            "RIR 0 = fallo absoluto (NO en este bloque)",
        ], NAVY),
        ("PROGRESION 12 SEMANAS", [
            "Mes 1 (semanas 1-4): Adaptacion - RIR 3-4, tecnica",
            "Mes 2 (semanas 5-8): Acumulacion - +1 serie, RIR 2-3",
            "Mes 3 (semanas 9-12): Intensificacion - cargas altas, RIR 1-2",
            "Deload en semana 4/8/12 (bajar volumen 30%)",
            "Remedicion completa cada deload (peso, cintura)",
        ], NAVY),
        ("SEMANA 1 = CALIBRAR CARGAS", [
            "En cada ejercicio principal, hacer 1-2 series de aproximacion subiendo",
            "Encontrar el peso que permita 8-10 reps con RIR 3-4",
            "Anotar carga en el bot con /nota (ej: /nota Press banca 40kg 3x10 RIR3)",
            "El entrenador usa esas notas para calibrar semana 2 en adelante",
        ], GREEN),
        ("SENALES DE ALARMA - CORTAR SESION", [
            "Dolor u opresion en el pecho",
            "Disnea (falta de aire) desproporcionada",
            "Palpitaciones sostenidas o irregulares",
            "Mareo o presincope",
            "Dolor irradiado a brazo/mandibula/espalda",
        ], ORANGE),
    ]

    for titulo, items, color in secciones:
        draw_rect_filled(pdf, 15, y, 4, 8, color)
        pdf.set_text_color(*NAVY)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_xy(22, y + 1)
        pdf.cell(170, 6, titulo)
        y += 10

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*SLATE)
        for item in items:
            pdf.set_xy(22, y)
            pdf.cell(5, 4.5, "-")
            pdf.set_xy(27, y)
            pdf.cell(165, 4.5, item)
            y += 5
        y += 4


def main():
    pdf = PDF()
    cover_page(pdf)
    for dia, info in RUTINA.items():
        day_page(pdf, dia, info)
    notes_page(pdf)
    pdf.output(str(OUT))
    print(f"OK: {OUT}")


if __name__ == "__main__":
    main()
