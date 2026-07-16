#!/usr/bin/env python3
"""Genera Rutina-Diaria-Fede.pdf - cronograma hora por hora de cada dia"""
from pathlib import Path
from fpdf import FPDF
from fpdf.fonts import FontFace

OUT = Path("/home/user/Fede/Rutina-Diaria-Fede.pdf")
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BLUE = (37, 99, 235)
DARK = (30, 30, 30)
GRAY = (100, 100, 100)


def H2(pdf, text, color=BLUE):
    pdf.add_page()
    pdf.set_fill_color(*color)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 9, text, fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_text_color(*DARK)


def timeline(pdf, rows):
    pdf.set_font("DejaVu", "", 8)
    with pdf.table(
        col_widths=(15, 40, 130),
        line_height=4.5,
        text_align="LEFT",
        headings_style=FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=BLUE),
    ) as t:
        head = t.row()
        head.cell("Hora"); head.cell("Que"); head.cell("Detalle")
        for h, q, d in rows:
            r = t.row()
            r.cell(h); r.cell(q); r.cell(d)
    pdf.ln(2)


def checklist(pdf, items):
    pdf.set_font("DejaVu", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Checklist del dia", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(*DARK)
    for it in items:
        pdf.multi_cell(0, 5, "[  ]  " + it, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def main():
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(12, 12, 12)
    pdf.set_auto_page_break(True, margin=12)
    pdf.add_font("DejaVu", "", FONT_REG)
    pdf.add_font("DejaVu", "B", FONT_BOLD)

    # ===== PORTADA =====
    pdf.add_page()
    pdf.set_fill_color(*BLUE)
    pdf.rect(0, 0, pdf.w, 50, "F")
    pdf.set_y(14)
    pdf.set_font("DejaVu", "B", 24)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, "Rutina Diaria", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 13)
    pdf.cell(0, 7, "Fede — Cronograma hora por hora", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(18)
    pdf.set_text_color(*DARK)
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(0, 7, "Resumen visual de la semana", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.set_font("DejaVu", "", 8)
    with pdf.table(
        line_height=4.5,
        text_align="LEFT",
        headings_style=FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=BLUE),
    ) as t:
        r = t.row()
        for h in ["Dia", "05:30", "07:00", "09:30", "13:00", "16:30", "20:30", "22:00"]:
            r.cell(h)
        rows = [
            ["Lun", "Pre-gym", "GYM A", "Desayuno", "Almuerzo", "Merienda", "Cena", "Snack+Dormir"],
            ["Mar", "Pre-gym", "GYM B", "Desayuno", "Almuerzo", "Merienda", "Cena", "Snack+Dormir"],
            ["Mie", "—", "Caminata Z2", "Desayuno", "Almuerzo", "Merienda", "Cena", "Snack+Dormir"],
            ["Jue", "Pre-gym", "GYM A", "Desayuno", "Almuerzo", "Merienda", "Cena", "Snack+Dormir"],
            ["Vie", "—", "(dorm)", "Desayuno", "Media man.", "Alm 17h post-gym 14h", "CENA LIBRE", "Snack opc"],
            ["Sab", "—", "Caminata Z2", "Desayuno", "Almuerzo", "Merienda", "Cena", "Snack+Dormir"],
            ["Dom", "—", "Caminata Z2", "Desayuno", "Batch+Alm", "Merienda+hobby", "Caesar", "Snack+Dormir"],
        ]
        for row in rows:
            r = t.row()
            for cell in row:
                r.cell(cell)

    pdf.ln(5)
    pdf.set_font("DejaVu", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Que hay en este PDF", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(*DARK)
    for line in [
        "• Cada dia con su cronograma completo hora por hora.",
        "• TODO integrado: comidas + gym + suplementos + agua + sol + habitos.",
        "• Checklist por dia para tildar.",
        "• Al final: tabla de suplementos + guia de agua.",
    ]:
        pdf.multi_cell(0, 5, line, new_x="LMARGIN", new_y="NEXT")

    # ===== LUNES =====
    H2(pdf, "LUNES — GYM 07:00 (Dia A: Empuje + Bisagra)")
    timeline(pdf, [
        ("05:30", "Despertar", "Vaso agua 300 ml + pizca sal"),
        ("05:35", "Bano rapido, ropa gym", ""),
        ("05:45", "Pre-entreno", "Media banana 80g + cafe 150ml + agua con sal 300ml"),
        ("06:30", "Salir al gym", ""),
        ("06:50", "Calentamiento 8 min", "Cinta 5km/h + movilidad + barra vacia"),
        ("07:00", "ENTRENO Dia A", "Complex A: sent. frontal → RDL → remo pecho → press pie → good morning"),
        ("08:00", "Post-entreno", "Whey 35g + agua 300ml (sin fruta)"),
        ("08:15", "Volver a casa, ducha", ""),
        ("09:00", "Sol 15 min con desayuno", "Ventana/balcon, cara y brazos"),
        ("09:30", "DESAYUNO", "3 huevos duros + pan 30g + palta 70g + tomate 100g + queso 20g + oliva 5ml"),
        ("09:45", "Suplementos AM", "Vitamina D3 + Omega-3"),
        ("10:00", "Trabajo/negocio", "Agua 500ml entre 10-13h"),
        ("13:00", "ALMUERZO", "Pollo 220g + papa hervida 100g + ensalada + oliva 12ml + limon"),
        ("13:15", "Suplemento", "Omega-3 (2do)"),
        ("14:00", "ULTIMO MATE del dia", "Sin azucar. Despues solo agua o infusiones sin teina"),
        ("15:00", "Agua 500 ml", ""),
        ("16:30", "MERIENDA", "Yogur griego 170g + nueces 12g + canela"),
        ("17:00", "Trabajo/negocio", "Agua 500ml entre 17-20h"),
        ("20:00", "Cerrar dia laboral", "Sin pantallas de trabajo despues"),
        ("20:30", "CENA", "Merluza 200g + zapallito 150g + morron 70g + anchoas 20g + huevo duro 1 + oliva 12ml"),
        ("21:30", "Bajar luces + relax", "Lectura, charla, TV suave. Sin trabajo."),
        ("22:00", "SNACK NOCTURNO ANCLA", "Yogur griego 170g + chia 10g + canela"),
        ("22:00", "Magnesio glicinato 300 mg", "Con el snack o justo antes"),
        ("22:15", "15 min lectura en cama", "Papel o e-reader sin retroiluminacion"),
        ("22:30", "DORMIR", "Cuarto oscuro, 18-20°C, celular AFUERA"),
    ])
    checklist(pdf, [
        "Agua total: ~3,0 L",
        "Sol 15 min",
        "8000+ pasos (contando ida/vuelta gym)",
        "4 comidas + snack nocturno",
        "Sin alcohol",
        "Sin cafeina despues de 15:00",
        "Acostado 22:30",
    ])

    # ===== MARTES =====
    H2(pdf, "MARTES — GYM 07:00 (Dia B: Tiron + Sentadilla)")
    timeline(pdf, [
        ("05:30", "Despertar", "Agua 300ml + sal"),
        ("05:45", "Pre-entreno", "Pasas de uva 30g (punadito) + cafe + agua con sal"),
        ("06:30", "Salir al gym", ""),
        ("07:00", "ENTRENO Dia B", "Complex B: sent. trasera → remo supino → power clean → RDL → shrug"),
        ("08:00", "Post-entreno", "Whey + agua (sin fruta)"),
        ("09:30", "DESAYUNO", "3 huevos duros + queso port salut 30g + pan 30g + palta 60g + tomate 100g + oliva 5ml"),
        ("09:45", "Suplementos AM", "Vit D3 + Omega-3"),
        ("13:00", "ALMUERZO", "Pollo 220g + boniato hervido 100g + ensalada (lechuga + rucula + tomate + cebolla + palta + aceitunas + nueces) + oliva 12ml"),
        ("14:00", "ULTIMO MATE", ""),
        ("16:30", "MERIENDA", "Cottage 200g + frutillas 30g + canela"),
        ("20:30", "CENA", "Salmon 180g + espinaca salteada 150g + champignones 80g + ajo + oliva 12ml"),
        ("22:00", "Snack + magnesio", "Yogur 170g + chia 10g"),
        ("22:30", "DORMIR", ""),
    ])
    checklist(pdf, [
        "Agua ~3,0 L", "Sol 15 min", "8000+ pasos",
        "4 comidas + snack", "Sin alcohol",
        "Sin cafeina despues 15:00", "Acostado 22:30",
    ])

    # ===== MIERCOLES =====
    H2(pdf, "MIERCOLES — DESCANSO (dia clave para longevidad)")
    timeline(pdf, [
        ("06:30", "Despertar", "Agua 300ml (sin sal — no entrenas)"),
        ("07:00", "CAMINATA Z2 dedicada", "30-40 min ritmo firme 5,5-6 km/h. Al sol si podes"),
        ("07:30", "DESAYUNO", "3 huevos duros + ricota 80g + palta 60g + tomate 100g + oliva 5ml. Sin pan."),
        ("07:45", "Suplementos AM", "Vit D3 + Omega-3 + CREATINA 5g (dia sin gym)"),
        ("10:00", "MEDIA MANANA", "Yogur griego 200g + nueces 10g + frutillas 30g"),
        ("13:00", "ALMUERZO", "Atun 180g + huevos duros 2 + espinaca 150g + queso 30g + lechuga + tomate + palta 60g + oliva 15ml"),
        ("14:00", "ULTIMO MATE", ""),
        ("16:30", "MERIENDA", "Ricota 150g + almendras 10g + cacao amargo 3g"),
        ("17:00", "HOBBY", "30-45 min de lo que elijas (pescar, cocinar, instrumento, huerta, padel). CLAVE."),
        ("20:30", "CENA", "Pollo 180g + brocoli al vapor 200g + champignones 80g + aceitunas 15g + oliva 12ml"),
        ("22:00", "Snack + magnesio", ""),
        ("22:30", "DORMIR", ""),
    ])
    checklist(pdf, [
        "Caminata Z2 30-40 min HECHA",
        "Hobby minimo 30 min",
        "Agua ~2,7 L", "Sol 15+ min",
        "3 comidas + media manana + merienda + snack",
        "Sin alcohol", "Acostado 22:30",
    ])

    # ===== JUEVES =====
    H2(pdf, "JUEVES — GYM 07:00 (Dia A: Empuje + Bisagra)")
    timeline(pdf, [
        ("05:30", "Despertar + agua con sal", ""),
        ("05:45", "Pre-entreno", "Media banana 80g + cafe + agua con sal"),
        ("07:00", "ENTRENO Dia A", "Igual lunes"),
        ("08:00", "Post-entreno", "Whey + agua (sin fruta)"),
        ("09:30", "DESAYUNO diferente", "Yogur griego proteico 200g + frutillas 100g + almendras 15g + canela + huevos duros 2 aparte + pan 30g"),
        ("09:45", "Suplementos AM", "Vit D3 + Omega-3"),
        ("13:00", "ALMUERZO", "Pollo 200g + papa hervida 100g + huevo duro 1 + ensalada nicoise + oliva 12ml"),
        ("14:00", "ULTIMO MATE", ""),
        ("16:30", "MERIENDA", "Yogur griego 170g + nueces 12g + frutos rojos 20g"),
        ("20:30", "CENA", "Brotola 200g + brocoli al vapor 200g + huevo duro 1 + anchoas 20g + oliva 12ml"),
        ("22:00", "Snack + magnesio", ""),
        ("22:30", "DORMIR", ""),
    ])
    checklist(pdf, [
        "Agua ~3,0 L", "Sol 15 min", "8000+ pasos",
        "4 comidas + snack", "Sin alcohol",
        "Sin cafeina despues 15:00", "Acostado 22:30",
    ])

    # ===== VIERNES =====
    H2(pdf, "VIERNES — GYM 14:00 (Dia B) — CENA LIBRE")
    timeline(pdf, [
        ("06:30", "Despertar", "Agua 400ml"),
        ("07:30", "DESAYUNO", "3 huevos duros + queso port salut 30g + palta 60g + tomate 100g + oliva 5ml. Sin pan."),
        ("07:45", "Suplementos AM", "Vit D3 + Omega-3"),
        ("10:30", "MEDIA MANANA", "Yogur griego 150g + nueces 10g + frutillas 30g"),
        ("12:30", "PRE-ENTRENO LIVIANO", "Pasas de uva 30g (punadito) + cafe + agua con sal 400ml. NO comer solido pesado 11-14h"),
        ("13:30", "Salir al gym", ""),
        ("14:00", "ENTRENO Dia B", ""),
        ("15:15", "Post-entreno", "Whey + agua (sin fruta — almuerzo viene a las 17h)"),
        ("15:30", "Volver casa, ducha", ""),
        ("17:00", "ALMUERZO-MERIENDA", "Pollo 220g + papa hervida 100g + espinaca + rucula + tomates cherry + palta + almendras + pan integral 30g + oliva 12ml"),
        ("17:15", "Cafe descafeinado / infusion", "Excepcion controlada por gym tarde"),
        ("20:30", "CENA LIBRE", "UNA opcion: pizza (2 porciones) / parrilla (250g magra) / sushi (12-15 piezas) / pasta (300g). Sin alcohol o max 1 vino."),
        ("22:00", "Snack OPCIONAL", "Si la cena fue abundante, salteala. Sino yogur 100g"),
        ("22:30", "DORMIR", ""),
    ])
    checklist(pdf, [
        "Comida libre elegida CONSCIENTE (no atracon)",
        "Sin alcohol (o max 1 copa) — anotar si tomas",
        "Acostado 22:30",
        "Agua ~3,2 L",
    ])

    # ===== SABADO =====
    H2(pdf, "SABADO — DESCANSO")
    timeline(pdf, [
        ("06:30", "Despertar", "Agua 300ml"),
        ("07:00", "CAMINATA Z2 dedicada", "30-40 min ritmo firme. Al sol."),
        ("07:30", "DESAYUNO", "3 huevos duros + jamon cocido magro 30g + queso port salut 30g + palta 50g + tomate 100g + oliva 5ml"),
        ("07:45", "Suplementos AM", "Vit D3 + Omega-3 + CREATINA 5g"),
        ("10:00", "MEDIA MANANA", "Cottage 150g + frutillas 50g + nueces 7g"),
        ("13:00", "ALMUERZO", "Pollo 220g + brocoli 150g + zapallitos hervidos 100g + ensalada + palta 40g + oliva 12ml"),
        ("14:00", "ULTIMO MATE", ""),
        ("16:30", "MERIENDA", "Huevo duro 1 + tomate 100g + oliva 5ml + almendras 10g"),
        ("17:00", "HOBBY / tiempo con familia", ""),
        ("20:30", "CENA", "Pollo 180g + huevos duros 2 + queso port salut 25g + espinaca 150g + champignones 80g + anchoas 15g + oliva 10ml"),
        ("22:00", "Snack + magnesio", ""),
        ("22:30", "DORMIR", ""),
    ])
    checklist(pdf, [
        "Caminata Z2 HECHA",
        "Hobby / familia >30 min",
        "Agua ~2,7 L", "Sol 15+ min",
        "Sin alcohol", "Acostado 22:30",
    ])

    # ===== DOMINGO =====
    H2(pdf, "DOMINGO — DESCANSO + BATCH COOKING")
    timeline(pdf, [
        ("06:30", "Despertar", "Agua 300ml"),
        ("07:00", "CAMINATA Z2", "30-40 min al sol"),
        ("07:30", "DESAYUNO", "3 huevos duros + palta 60g + tomate 100g + queso 30g + oliva 5ml. Sin pan."),
        ("07:45", "Suplementos AM", "Vit D3 + Omega-3 + CREATINA 5g"),
        ("10:00", "BATCH COOKING 90 min", "1) Pollo 1,8kg horno 2) 20 huevos duros 3) Papa+boniato hervidos 4) Verduras vapor 5) Aderezos. Mate + arandanos 30g mientras"),
        ("12:00", "Ducha, guardar tuppers", ""),
        ("13:30", "ALMUERZO", "Pollo horno 220g + ensalada completa (lechuga + tomate + cebolla + pepino + zanahoria + palta + aceitunas + nueces) + oliva 12ml"),
        ("14:00", "ULTIMO MATE", ""),
        ("16:30", "MERIENDA", "Yogur griego 200g + nueces 10g + cacao amargo 3g"),
        ("17:00", "HOBBY / hijos", "Aprovechar el domingo, ideal aire libre"),
        ("19:00", "Preparar semana", "Revisar mediciones (peso + cintura del lunes en ayunas), planificar"),
        ("20:30", "CENA Caesar low-carb", "Pollo 180g + lechuga romana 100g + huevo duro 1 + anchoas 20g + parmesano 15g + oliva 12ml + aderezo"),
        ("22:00", "Snack + magnesio", ""),
        ("22:30", "DORMIR", "Cargar tensiometro + tomar TA de referencia"),
    ])
    checklist(pdf, [
        "Caminata Z2 HECHA",
        "Batch cooking HECHO",
        "Hobby / familia >45 min",
        "Mediciones del lunes preparadas",
        "Sin alcohol", "Acostado 22:30",
    ])

    # ===== SUPLEMENTOS =====
    H2(pdf, "Suplementos — donde entran")
    pdf.set_font("DejaVu", "", 9)
    with pdf.table(
        line_height=5,
        text_align="LEFT",
        headings_style=FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=BLUE),
    ) as t:
        r = t.row(); r.cell("Suplemento"); r.cell("Cuando"); r.cell("Dias")
        rows = [
            ["Vit D3 (2000-4000 UI)", "Con desayuno", "TODOS"],
            ["Omega-3 (2-3 g)", "Almuerzo o cena", "TODOS"],
            ["Creatina (5 g)", "Post-entreno (gym) o desayuno (descanso)", "TODOS"],
            ["Whey (35 g)", "Post-entreno", "Lun / Mar / Jue / Vie"],
            ["Magnesio glicinato (300 mg)", "22:00 con snack nocturno", "TODOS"],
            ["Sal extra (2 g)", "Repartir en el dia", "Primera semana"],
        ]
        for row in rows:
            r = t.row()
            for cell in row:
                r.cell(cell)

    pdf.ln(3)
    pdf.set_font("DejaVu", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 6, "Agua total por dia", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(*DARK)
    for line in [
        "• Al despertar: 300-400 ml (con pizca de sal los dias gym)",
        "• Manana: 500-800 ml",
        "• Con almuerzo: 200-300 ml",
        "• Tarde: 500-700 ml (incluye mate)",
        "• Con cena: 200 ml",
        "• TOTAL DIA GYM: 3,0-3,2 L",
        "• TOTAL DIA DESCANSO: 2,7-3,0 L",
    ]:
        pdf.multi_cell(0, 5, line, new_x="LMARGIN", new_y="NEXT")

    pdf.output(str(OUT))
    print(f"PDF generado: {OUT}")
    print(f"Tamano: {OUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
