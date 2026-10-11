#!/usr/bin/env python3
"""Genera Plan-Longevidad-Fede.pdf"""
from pathlib import Path
from fpdf import FPDF
from fpdf.fonts import FontFace

OUT = Path("/home/user/Fede/Plan-Longevidad-Fede.pdf")
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PURPLE = (109, 40, 217)
DARK = (30, 30, 30)
GRAY = (100, 100, 100)


def H2(pdf, text):
    pdf.add_page()
    pdf.set_fill_color(*PURPLE)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 9, text, fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_text_color(*DARK)


def H3(pdf, text):
    if pdf.get_y() > pdf.h - 40:
        pdf.add_page()
    pdf.ln(2)
    pdf.set_font("DejaVu", "B", 11)
    pdf.set_text_color(*PURPLE)
    pdf.cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)


def P(pdf, text, size=9, color=DARK, indent=0):
    pdf.set_font("DejaVu", "", size)
    pdf.set_text_color(*color)
    if indent:
        pdf.set_x(pdf.l_margin + indent)
    pdf.multi_cell(pdf.epw - indent, 4.5, text, new_x="LMARGIN", new_y="NEXT")


def table(pdf, rows, col_widths=None):
    pdf.set_font("DejaVu", "", 8)
    kw = {"line_height": 4.5, "text_align": "LEFT",
          "headings_style": FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=PURPLE)}
    if col_widths:
        kw["col_widths"] = col_widths
    with pdf.table(**kw) as t:
        for row in rows:
            tr = t.row()
            for cell in row:
                tr.cell(str(cell))
    pdf.ln(2)


def main():
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_font("DejaVu", "", FONT_REG)
    pdf.add_font("DejaVu", "B", FONT_BOLD)

    # ===== PORTADA =====
    pdf.add_page()
    pdf.set_fill_color(*PURPLE)
    pdf.rect(0, 0, pdf.w, 55, "F")
    pdf.set_y(14)
    pdf.set_font("DejaVu", "B", 24)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, "Plan de Longevidad", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 13)
    pdf.cell(0, 7, "Fede — Healthspan integral", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 6, "Vivir bien hasta los 90+", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(22)
    pdf.set_text_color(*DARK)
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(0, 7, "Punto de partida", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 10)
    datos = [
        ("Edad / sexo", "47 anos, M"),
        ("Peso / altura", "105 kg / 171 cm (IMC 35.9)"),
        ("Cintura / cadera", "102 cm / 109 cm (ICC 0,94)"),
        ("Actividad basal", "8.000 pasos/dia, 7,3 km/dia"),
        ("Sueno", "6 h (objetivo 7 h)"),
        ("Alcohol", "corte reciente"),
        ("Antecedentes", "padre marcapasos | mama diabetes T2 | abuela cancer"),
        ("Medicacion", "ninguna"),
        ("Fitness funcional", "SRT ok | flexiones 15-20 | plancha 10-15s | equilibrio ok"),
        ("Restricciones", "FC max 121 lpm hasta ECG basal"),
    ]
    for k, v in datos:
        pdf.set_font("DejaVu", "B", 10)
        pdf.cell(55, 6, k, border="B")
        pdf.set_font("DejaVu", "", 10)
        pdf.cell(0, 6, v, border="B", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(5)
    P(pdf, "IMPORTANTE: este plan NO reemplaza consulta medica. Los labs y estudios se llevan al medico. La restriccion de FC 121 lpm se levanta cuando el clinico + cardiologo lo aprueben.", color=GRAY, size=8)

    # ===== 7 PALANCAS =====
    H2(pdf, "Las 7 palancas de estilo de vida")
    table(pdf, [
        ["#", "Palanca", "Estado"],
        ["1", "Fuerza (gym Complexes A/B/A/B)", "Arrancado — 4 dias/sem"],
        ["2", "Zona 2 (caminata sostenida)", "OK — 7,3 km/dia + caminata dedicada dias descanso"],
        ["3", "VO2max (bloques cortos alta intensidad)", "BLOQUEADO hasta ECG"],
        ["4", "Sueno (7 h objetivo)", "En construccion — hoy 6 h"],
        ["5", "Nutricion (low-carb mediterranea)", "Definida — 2.250/2.050 kcal"],
        ["6", "Salud mental / estres", "Pendiente — hobby + psicologo"],
        ["7", "Screening medico", "En agenda — labs + estudios preventivos"],
    ])

    # ===== FUERZA =====
    H2(pdf, "1. Fuerza — Complexes A/B/A/B")
    P(pdf, "Ya definido en 'rutina-actual.md'. 4 dias/semana. FC max 121 lpm hasta ECG.")
    table(pdf, [
        ["Dia", "Hora", "Sesion"],
        ["Lunes", "07:00", "Dia A (Empuje + Bisagra)"],
        ["Martes", "07:00", "Dia B (Tiron + Sentadilla)"],
        ["Miercoles", "—", "DESCANSO + caminata Z2"],
        ["Jueves", "07:00", "Dia A"],
        ["Viernes", "14:00", "Dia B"],
        ["Sabado", "—", "DESCANSO + caminata Z2"],
        ["Domingo", "—", "DESCANSO + batch cooking"],
    ])

    # ===== ZONA 2 =====
    H2(pdf, "2. Zona 2 — cardio de longevidad")
    P(pdf, "Objetivo: 150+ min/semana en zona 2 (FC 60–70% del maximo, esfuerzo donde podes hablar pero no cantar). Ya cubierto por la caminata basal.")
    P(pdf, "AJUSTE: los dias de descanso (Mie/Sab/Dom), sumar una caminata dedicada de 30–40 min a ritmo firme (5,5–6 km/h). No paseando — zona 2 pura.")

    # ===== VO2max =====
    H2(pdf, "3. VO2max — BLOQUEADO hasta ECG basal")
    P(pdf, "Cuando el ECG salga OK y el clinico habilite alta intensidad, se suma:")
    P(pdf, "• Protocolo noruego 4x4: 4 min FC alta + 3 min FC baja x 4 rondas. 1x/semana. En bici o cinta.", indent=2)
    P(pdf, "• Es el marcador MAS asociado con longevidad. Sube expectativa de vida en anos.", indent=2)
    P(pdf, "ANTES del ECG: NO se hace. Riesgo cardiovascular alto por antecedente paterno.", color=(180, 0, 0))

    # ===== SUEÑO =====
    H2(pdf, "4. Sueno — subir de 6 h a 7 h")
    H3(pdf, "Horario objetivo")
    P(pdf, "• Acostarse: 22:30", indent=2)
    P(pdf, "• Levantarse: 05:30 (Lun/Mar/Jue gym) | 06:30 (Vie/Mie/Sab/Dom)", indent=2)
    H3(pdf, "Higiene del sueno (todos los dias)")
    for line in [
        "15:00 → ultima cafeina (cafe + mate). Despues: agua o infusiones sin teina.",
        "21:30 → luces bajas, pantalla en modo oscuro o modo lectura.",
        "22:00 → magnesio glicinato 300 mg (validar con medico).",
        "22:15 → 15 min de lectura en cama (papel o e-reader sin retroiluminacion).",
        "Cuarto oscuro (persiana + antifaz si hace falta), fresco (18–20 °C), silencioso.",
        "Sin celular en la mesa de luz. Cargador AFUERA del dormitorio.",
    ]:
        P(pdf, "• " + line, indent=2)
    H3(pdf, "Regla alcohol")
    P(pdf, "Cero por 4 semanas minimo. Despues: maximo 1 copa de vino tinto la cena del viernes. Cero durante la semana.", indent=2)

    # ===== NUTRICION =====
    H2(pdf, "5. Nutricion — ya definida")
    P(pdf, "Ver 'Dieta-Fede-Semanal.pdf' y 'dieta-actual.md'. Low-carb mediterranea, 2.250 kcal dias gym / 2.050 kcal descanso.")
    P(pdf, "Proteina objetivo:", size=10)
    P(pdf, "• Hoy (105 kg): 200 g/dia (~1,9 g/kg)", indent=2)
    P(pdf, "• En objetivo (95 kg): 155 g/dia (~1,6 g/kg)", indent=2)
    P(pdf, "Repartida en 5 comidas de 30–50 g cada una (post-entreno, desayuno, almuerzo, merienda, cena).")

    # ===== SALUD MENTAL =====
    H2(pdf, "6. Salud mental / estres")
    H3(pdf, "Fortalezas ya identificadas")
    for line in [
        "Proposito claro (hijos + proyectos del negocio) — es oro para longevidad.",
        "Sin quejas cognitivas.",
        "Motivacion alta.",
    ]:
        P(pdf, "• " + line, indent=2)
    H3(pdf, "A trabajar")
    P(pdf, "HOBBY (no tenes ninguno hoy):", size=10)
    P(pdf, "Elegir 1 actividad NO relacionada con negocio ni gym. Sugerencias: pescar, cocinar recetas nuevas, aprender un instrumento, huerta, deporte social (padel, tenis). Reemplaza la dopamina que daba el alcohol.", indent=2)
    P(pdf, "PSICOLOGO:", size=10)
    P(pdf, "Consulta pendiente para trabajar reemplazo emocional del alcohol + manejo de estres cronico.", indent=2)
    P(pdf, "SOL:", size=10)
    P(pdf, "15–20 min/dia al menos. En invierno aprovechar mediodia. Es vitamina D + estado de animo.", indent=2)

    # ===== SCREENING =====
    H2(pdf, "7. Screening medico")
    H3(pdf, "Prioridad ALTA (este mes)")
    for line in [
        "Analisis de sangre completo (con extras de longevidad — ver tabla abajo)",
        "ECG basal (obligatorio antes de intensidad alta)",
        "Tension arterial: 3 mediciones en farmacia en dias distintos",
        "Consulta con clinico presencial",
        "Dermatologo (mapa de lunares — NUNCA fuiste)",
        "Colonoscopia con gastroenterologo (con abuela con cancer, prioridad ALTA)",
        "PSA + control urologico",
    ]:
        P(pdf, "• " + line, indent=2)
    H3(pdf, "Prioridad MEDIA (30–60 dias)")
    for line in [
        "Ecografia abdominal (descartar higado graso)",
        "Ergometria (si el clinico lo indica tras ECG)",
        "Oftalmologo (fondo de ojos + control ocular)",
        "Comprar tensiometro digital de brazo (medir 2x/semana en casa)",
    ]:
        P(pdf, "• " + line, indent=2)

    # ===== LABS DE LONGEVIDAD =====
    H2(pdf, "Labs para llevar al medico — version LONGEVIDAD")
    P(pdf, "Ademas de los basicos ya listados, pedir explicitamente:")
    table(pdf, [
        ["Marcador", "Por que", "Frecuencia"],
        ["ApoB", "Mejor predictor CV que LDL. Cuenta particulas aterogenicas.", "Anual"],
        ["Lp(a)", "Riesgo CV genetico. Se mide 1 sola vez en la vida.", "1 sola vez"],
        ["hs-CRP", "Inflamacion de bajo grado (predictor CV).", "Anual"],
        ["HbA1c", "Glucemia promedio 3 meses.", "Anual"],
        ["HOMA-IR", "Resistencia a insulina.", "Anual"],
        ["Homocisteina", "Marcador CV y neurologico (opcional).", "1 vez"],
        ["PSA", "Prostata.", "Anual"],
        ["25-OH Vitamina D", "Nivel real para dosificar D3.", "2x/ano"],
        ["TSH + T4 libre", "Tiroides completa.", "Anual"],
        ["Ferritina + Transferrina", "Depositos de hierro.", "Anual"],
        ["Testosterona total + libre", "Post 45. Correlaciona con energia/musculo.", "Anual"],
    ])

    # ===== CHECKLIST DIARIO =====
    H2(pdf, "Checklist diario de longevidad")
    P(pdf, "Poner en la mesa de luz. Tildar cada noche.", color=GRAY, size=9)
    pdf.ln(2)
    pdf.set_font("DejaVu", "", 10)
    diario = [
        "[ ] 300 ml de agua al despertar (con pizca de sal)",
        "[ ] Sol 15+ min (mediodia en invierno)",
        "[ ] 8.000+ pasos",
        "[ ] Proteina en las 5 comidas",
        "[ ] Ultima cafeina antes de las 15:00",
        "[ ] Sin alcohol",
        "[ ] Acostado 22:30, sin pantallas 15 min antes",
        "[ ] 5 min de silencio o respiracion lenta",
    ]
    for line in diario:
        pdf.multi_cell(0, 5.5, line, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    H3(pdf, "Semanal")
    pdf.set_font("DejaVu", "", 10)
    for line in [
        "[ ] 4 sesiones de fuerza completadas",
        "[ ] 1 caminata dedicada 30–40 min zona 2 (dia descanso)",
        "[ ] Mediciones (peso + cintura) lunes en ayunas",
        "[ ] 1 rato de hobby minimo",
        "[ ] Bitacora actualizada",
    ]:
        pdf.multi_cell(0, 5.5, line, new_x="LMARGIN", new_y="NEXT")

    # ===== FASES =====
    H2(pdf, "Fases del plan")
    H3(pdf, "FASE 1 — Fundacion (Semanas 1–4)")
    for line in [
        "Instalar los 8 habitos del checklist diario",
        "Arrancar gym Complexes A/B/A/B",
        "Sacar turnos: clinico + dermatologo + gastroenterologo + urologo",
        "Hacer analisis de sangre completo (con extras de longevidad)",
        "Sacar ECG basal + tomar TA 3 veces",
        "Elegir 1 hobby y probarlo",
    ]:
        P(pdf, "• " + line, indent=2)
    H3(pdf, "FASE 2 — Amplificacion (Semanas 5–12)")
    for line in [
        "Con ECG OK: sumar VO2max 1x/semana",
        "Con lab en mano: ajustar dieta y suplementacion",
        "Sueno consolidado en 7 h",
        "Consulta con psicologo (o coach) sobre estres + alcohol + hobby",
        "Peso objetivo intermedio: −5 kg (100 kg)",
    ]:
        P(pdf, "• " + line, indent=2)
    H3(pdf, "FASE 3 — Sostenimiento (Meses 4–12)")
    for line in [
        "Peso objetivo: −10 kg (95 kg)",
        "Cintura objetivo: −8 cm (94 cm)",
        "Estudios anuales (repetir todo lo hecho en Fase 1)",
        "Progresion del gym a nuevo bloque (Dia C = 5 dias opcional)",
    ]:
        P(pdf, "• " + line, indent=2)

    # ===== METRICAS =====
    H2(pdf, "Metricas de longevidad — revisar cada 3 meses")
    table(pdf, [
        ["Metrica", "Hoy", "6 meses", "12 meses"],
        ["Peso", "105 kg", "100 kg", "95 kg"],
        ["Cintura", "102 cm", "96 cm", "92 cm"],
        ["ICC (cintura/cadera)", "0,94", "0,90", "0,88"],
        ["Sueno", "6 h", "7 h", "7,5 h"],
        ["Plancha (core)", "10-15 seg", "45 seg", "60 seg"],
        ["Flexiones", "15-20", "25-30", "30+"],
        ["Pasos/dia", "8.000", "9.000", "10.000"],
        ["Alcohol", "recien cortado", "0 semanal", "1 copa/vie"],
        ["Hobby", "0", "1 activo", "1 consolidado"],
    ])

    # ===== LO QUE NO HACEMOS =====
    H2(pdf, "Lo que NO hacemos (medicina basada en evidencia)")
    for line in [
        "NMN, resveratrol, 'anti-aging pills': sin evidencia solida en humanos.",
        "Ayunos extremos 48h+: no aportan mas que el deficit calorico. Riesgo en obesidad G2.",
        "Suplementos 'quemadores de grasa': contraindicados con perfil cardiovascular.",
        "Testosterona sintetica sin diagnostico: solo si hay hipogonadismo real + endocrino.",
        "Dietas cetogenicas estrictas prolongadas sin control lipidico: pueden subir LDL.",
    ]:
        P(pdf, "• " + line, indent=2)
    pdf.ln(3)
    P(pdf, "Lo que SI funciona (y hacemos): fuerza, cardio, sueno, proteina, verduras, pescado, sol, red social, proposito, screening.", color=PURPLE, size=10)

    pdf.output(str(OUT))
    print(f"PDF generado: {OUT}")
    print(f"Tamano: {OUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
