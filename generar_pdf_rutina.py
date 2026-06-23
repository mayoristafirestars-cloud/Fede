#!/usr/bin/env python3
"""Genera Rutina-Fede-Gym.pdf (version simple y robusta)"""
from pathlib import Path
from fpdf import FPDF
from fpdf.fonts import FontFace

ROOT = Path("/home/user/Fede")
OUT = ROOT / "Rutina-Fede-Gym.pdf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

RED = (220, 38, 38)
DARK = (30, 30, 30)
GRAY = (100, 100, 100)


def main():
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_font("DejaVu", "", FONT_REG)
    pdf.add_font("DejaVu", "B", FONT_BOLD)

    # ===== PORTADA =====
    pdf.add_page()
    pdf.set_fill_color(*RED)
    pdf.rect(0, 0, pdf.w, 45, "F")
    pdf.set_y(12)
    pdf.set_font("DejaVu", "B", 24)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, "Rutina de Gym", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 13)
    pdf.cell(0, 7, "Fede — Complexes de Barra", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(20)
    pdf.set_text_color(*DARK)
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(0, 7, "Datos del plan", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 10)
    datos = [
        ("Vigente desde", "Lunes 21/04/2026"),
        ("Duracion", "4 semanas (S1–S4)"),
        ("Frecuencia", "4 dias/semana (Lun / Mar / Jue / Vie)"),
        ("Formato", "A / B / A / B (Full Body Complexes)"),
        ("Horario", "08:00 AM"),
        ("FC maxima de trabajo", "121 lpm (hasta ECG)"),
        ("Restricciones activas", "Sin HIIT, sin sprints"),
        ("Monitoreo", "Apple Watch — FC en cada serie"),
        ("Objetivo", "Bajar grasa + salud cardiovascular"),
    ]
    for k, v in datos:
        pdf.set_font("DejaVu", "B", 10)
        pdf.cell(55, 6, k, border="B")
        pdf.set_font("DejaVu", "", 10)
        pdf.cell(0, 6, v, border="B", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)
    pdf.set_font("DejaVu", "B", 11)
    pdf.set_text_color(*RED)
    pdf.cell(0, 7, "Reglas de oro", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(*DARK)
    reglas = [
        "1. Calentamiento 8 min SIEMPRE. No es opcional.",
        "2. Tecnica antes que carga. Si se rompe la cadena, bajas peso.",
        "3. FC debajo de 121 lpm. Si sube, descansa mas entre series.",
        "4. Velocidad: concentrico 2 seg / excentrico 3 seg.",
        "5. Pausa entre series: 90s (S1) / 75s (S2) / 60s (S3-S4).",
        "6. Si dormiste mal esa noche: salteas el finalizador.",
    ]
    for r in reglas:
        pdf.multi_cell(0, 5, r)
        pdf.ln(0.3)

    # ===== DISTRIBUCION SEMANAL =====
    pdf.add_page()
    pdf.set_fill_color(*RED)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 9, "Distribucion semanal", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.set_font("DejaVu", "", 9)
    with pdf.table(
        col_widths=(25, 35, 120),
        line_height=5,
        text_align="LEFT",
        headings_style=FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=RED),
    ) as table:
        r = table.row(); r.cell("Dia"); r.cell("Sesion"); r.cell("Foco")
        r = table.row(); r.cell("Lunes"); r.cell("Dia A"); r.cell("Empuje + Bisagra")
        r = table.row(); r.cell("Martes"); r.cell("Dia B"); r.cell("Tiron + Sentadilla")
        r = table.row(); r.cell("Miercoles"); r.cell("DESCANSO"); r.cell("Caminata")
        r = table.row(); r.cell("Jueves"); r.cell("Dia A"); r.cell("Empuje + Bisagra (igual lunes)")
        r = table.row(); r.cell("Viernes"); r.cell("Dia B"); r.cell("Tiron + Sentadilla (igual martes)")
        r = table.row(); r.cell("Sabado"); r.cell("DESCANSO"); r.cell("Caminata")
        r = table.row(); r.cell("Domingo"); r.cell("DESCANSO"); r.cell("Caminata + batch cooking")

    pdf.ln(4)
    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 5, "A/B/A/B: repetimos A y B dos veces en la semana. Mas volumen sin saturar grupos. El Dia C (Full Complex) lo sumamos al bloque 2 cuando tengas ECG y analisis.")

    # ===== CALENTAMIENTO =====
    pdf.add_page()
    pdf.set_fill_color(*RED)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 9, "Calentamiento (8 min — igual los 3 dias)", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_text_color(*DARK)
    pdf.set_font("DejaVu", "", 10)
    cal = [
        "1. Caminata en cinta 5 km/h, inclinacion 0 — 3 min. FC objetivo 90-95 lpm.",
        "2. Movilidad articular — 3 min:",
        "    • Circulos de hombro: 10 rep cada sentido",
        "    • Hip circles: 10 rep cada lado",
        "    • Sentadilla goblet con peso corporal: 10 rep",
        "    • Bisagra de cadera sin peso: 10 rep",
        "3. Serie de activacion con barra vacia (20 kg) — 2 min. Una pasada completa del complex del dia, 5 reps de cada movimiento, sin cargar.",
    ]
    for line in cal:
        pdf.multi_cell(0, 5, line)
        pdf.ln(0.3)

    # ===== DIAS A / B / C =====
    def day_block(letra, titulo, foco, patron, ejercicios, series_txt, carga_txt, finalizador):
        pdf.add_page()
        pdf.set_fill_color(*RED)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("DejaVu", "B", 14)
        pdf.cell(0, 10, f"DIA {letra} — {titulo}", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        pdf.set_text_color(*DARK)
        pdf.set_font("DejaVu", "B", 10)
        pdf.cell(0, 6, f"Foco: {foco}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("DejaVu", "", 9)
        pdf.set_text_color(*GRAY)
        pdf.multi_cell(0, 5, f"Patron de la cadena: {patron}")
        pdf.ln(2)
        pdf.set_text_color(*DARK)

        pdf.set_font("DejaVu", "B", 10)
        pdf.cell(0, 6, f"Complex {letra} (misma barra, sin soltar)", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

        pdf.set_font("DejaVu", "", 9)
        with pdf.table(
            col_widths=(8, 75, 12, 85),
            line_height=5,
            text_align="LEFT",
            headings_style=FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=RED),
        ) as table:
            r = table.row()
            r.cell("#"); r.cell("Ejercicio"); r.cell("Reps"); r.cell("Tecnica clave")
            for n, (ej, reps, tec) in enumerate(ejercicios, 1):
                r = table.row()
                r.cell(str(n)); r.cell(ej); r.cell(str(reps)); r.cell(tec)

        pdf.ln(3)
        pdf.set_font("DejaVu", "B", 9)
        pdf.cell(0, 5, f"Series totales: {series_txt}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 5, f"Carga de arranque S1: {carga_txt}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

        if finalizador:
            pdf.set_font("DejaVu", "B", 10)
            pdf.set_text_color(*RED)
            pdf.cell(0, 6, f"Finalizador Dia {letra} (opcional)", new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(*GRAY)
            pdf.set_font("DejaVu", "", 8)
            pdf.multi_cell(0, 4, "Solo si FC < 110 al terminar el complex y dormiste bien.")
            pdf.ln(1)
            pdf.set_font("DejaVu", "", 9)
            pdf.set_text_color(*DARK)
            with pdf.table(
                col_widths=(80, 15, 15, 15, 55),
                line_height=5,
                text_align="LEFT",
                headings_style=FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=RED),
            ) as table:
                r = table.row()
                r.cell("Ejercicio"); r.cell("Series"); r.cell("Reps"); r.cell("RIR"); r.cell("Carga S1")
                for ej, se, re_, rir, carga in finalizador:
                    r = table.row()
                    r.cell(ej); r.cell(str(se)); r.cell(str(re_)); r.cell(str(rir)); r.cell(carga)

    day_block(
        "A", "Empuje + Bisagra (Lunes y Jueves)", "Empuje + Bisagra de cadera",
        "Sent. frontal → RDL → Remo pecho → Press pie → Good Morning",
        [
            ("Sentadilla frontal (barra en clavic.)", 6, "Talones al piso, rodillas siguen pie, pecho arriba"),
            ("Romanian Deadlift (bisagra)", 6, "Cadera atras, barra cerca del cuerpo, espalda neutra"),
            ("Remo al pecho (Pendlay Row)", 6, "Torso casi horizontal, codos 45°, barra al esternon"),
            ("Press de pie con barra (OHP)", 6, "Gluteos apretados, sin hiperextender lumbar"),
            ("Good Morning", 6, "Bisagra lenta, espalda neutra, sensacion en isquios"),
        ],
        "S1: 3 / S2: 3 / S3: 4 / S4: 4",
        "30 kg (barra 20 + 5 kg cada lado). Si la cadena se rompe, bajar a barra vacia.",
        [
            ("Press de banco con mancuernas", 2, 10, 3, "14 kg por mano (2×7)"),
            ("Extension de triceps con polea (rope)", 2, 12, 3, "15 kg"),
        ],
    )

    day_block(
        "B", "Tiron + Sentadilla (Martes y Viernes)", "Tiron + Sentadilla",
        "Dominada/Jalon → Sent. trasera → Remo → Hip Thrust → Curl",
        [
            ("Sentadilla trasera (barra trapecios)", 6, "Profundidad paralela o hasta donde la movilidad permita"),
            ("Remo con barra supino", 6, "Codos pegados al cuerpo, aprieta dorsal al final"),
            ("Power Clean a la cintura", 4, "Tiron de piso a cintura. Si no domina: High Pull"),
            ("Romanian Deadlift", 6, "Igual que dia A"),
            ("Shrug con barra", 8, "Sin rotar hombros, solo subir/bajar"),
        ],
        "S1: 3 / S2: 3 / S3: 4 / S4: 4",
        "30 kg. Eslabon debil: Power Clean/High Pull. Si se ven mal, bajar a 25 kg.",
        [
            ("Jalon al pecho en polea (agarre ancho)", 2, 10, 3, "45 kg"),
            ("Curl de biceps con mancuernas (alterno)", 2, "10 c/lado", 3, "10 kg por mano"),
        ],
    )

    # ===== PROGRESION =====
    pdf.add_page()
    pdf.set_fill_color(*RED)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 9, "Progresion de cargas (Semanas 1 a 4)", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(*DARK)
    with pdf.table(
        col_widths=(25, 30, 30, 40, 50),
        line_height=5,
        text_align="LEFT",
        headings_style=FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=RED),
    ) as table:
        r = table.row()
        r.cell("Semana"); r.cell("Carga sugerida"); r.cell("Series"); r.cell("Pausa entre series"); r.cell("Objetivo")
        r = table.row()
        r.cell("S1"); r.cell("30 kg"); r.cell("3"); r.cell("90 seg"); r.cell("Grabar patron motor. Tecnica primero.")
        r = table.row()
        r.cell("S2"); r.cell("32,5 kg"); r.cell("3"); r.cell("75 seg"); r.cell("Subir carga si S1 se vio bien.")
        r = table.row()
        r.cell("S3"); r.cell("35 kg"); r.cell("4"); r.cell("60 seg"); r.cell("Sumar serie. Volumen mayor.")
        r = table.row()
        r.cell("S4"); r.cell("37,5 kg"); r.cell("4"); r.cell("60 seg"); r.cell("Semana tope del bloque.")

    pdf.ln(6)
    pdf.set_font("DejaVu", "B", 11)
    pdf.set_text_color(*RED)
    pdf.cell(0, 7, "Deload y proximos pasos", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(*DARK)
    deload = [
        "• Semana 5: DELOAD (40-50 % de la carga S4, mismas reps). Recuperacion activa.",
        "• Revision a los 28 dias: medir cintura, peso y FC en reposo.",
        "• Si todo OK + ECG normal: proximo bloque suma Dia C (Full Complex) los miercoles -> 5 dias.",
        "• Tras ECG basal y analisis: evaluar levantar restriccion de FC y sumar HIIT corto opcional.",
    ]
    for line in deload:
        pdf.multi_cell(0, 5, line)
        pdf.ln(0.3)

    pdf.output(str(OUT))
    print(f"PDF generado: {OUT}")
    print(f"Tamano: {OUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
