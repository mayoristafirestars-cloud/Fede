#!/usr/bin/env python3
"""Genera Dieta-Fede-Semanal.pdf desde salud/dieta-actual.md"""
import re
from pathlib import Path
from fpdf import FPDF

ROOT = Path("/home/user/Fede")
SRC = ROOT / "salud" / "dieta-actual.md"
OUT = ROOT / "Dieta-Fede-Semanal.pdf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


class DietaPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DejaVu", "B", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, "Dieta Semanal — Fede", align="R", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(130, 130, 130)
        self.cell(0, 8, f"Pagina {self.page_no()}", align="C")


def clean_md(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\*(.+?)\*", r"\1", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    return s.strip()


def parse_table(lines, i):
    rows = []
    while i < len(lines) and lines[i].strip().startswith("|"):
        line = lines[i].strip()
        if re.match(r"^\|[\s\-|:]+\|$", line):
            i += 1
            continue
        cells = [clean_md(c) for c in line.strip("|").split("|")]
        rows.append(cells)
        i += 1
    return rows, i


def render_table(pdf, rows):
    if not rows:
        return
    ncols = len(rows[0])
    usable = pdf.w - pdf.l_margin - pdf.r_margin
    col_w = usable / ncols
    pdf.set_font("DejaVu", "B", 8)
    pdf.set_fill_color(15, 118, 110)
    pdf.set_text_color(255, 255, 255)
    for cell in rows[0]:
        pdf.cell(col_w, 6, cell[:60], border=1, fill=True, align="L")
    pdf.ln()
    pdf.set_font("DejaVu", "", 8)
    pdf.set_text_color(30, 30, 30)
    fill = False
    for row in rows[1:]:
        if pdf.get_y() > pdf.h - 30:
            pdf.add_page()
        pdf.set_fill_color(245, 247, 250) if fill else pdf.set_fill_color(255, 255, 255)
        for cell in row[:ncols]:
            pdf.cell(col_w, 5.5, cell[:60], border=1, fill=True, align="L")
        pdf.ln()
        fill = not fill
    pdf.ln(2)


def render_md(pdf, md_text):
    lines = md_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            pdf.ln(2)
            i += 1
            continue

        if stripped.startswith("|"):
            rows, i = parse_table(lines, i)
            render_table(pdf, rows)
            continue

        if stripped.startswith("### "):
            text = clean_md(stripped[4:])
            if pdf.get_y() > pdf.h - 40:
                pdf.add_page()
            pdf.ln(3)
            pdf.set_font("DejaVu", "B", 12)
            pdf.set_text_color(15, 118, 110)
            pdf.multi_cell(0, 6, text)
            pdf.set_draw_color(15, 118, 110)
            pdf.set_line_width(0.3)
            y = pdf.get_y()
            pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
            pdf.ln(1)
        elif stripped.startswith("## "):
            text = clean_md(stripped[3:])
            pdf.add_page()
            pdf.set_fill_color(15, 118, 110)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("DejaVu", "B", 14)
            pdf.cell(0, 10, text, fill=True, new_x="LMARGIN", new_y="NEXT", align="L")
            pdf.ln(2)
        elif stripped.startswith("# "):
            text = clean_md(stripped[2:])
            pdf.set_font("DejaVu", "B", 18)
            pdf.set_text_color(15, 118, 110)
            pdf.multi_cell(0, 10, text)
            pdf.ln(3)
        elif stripped.startswith("---"):
            pdf.ln(2)
            pdf.set_draw_color(200, 200, 200)
            y = pdf.get_y()
            pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
            pdf.ln(3)
        elif stripped.startswith("- ") or stripped.startswith("* "):
            text = clean_md(stripped[2:])
            pdf.set_font("DejaVu", "", 9)
            pdf.set_text_color(30, 30, 30)
            pdf.set_x(pdf.l_margin + 4)
            pdf.multi_cell(0, 5, "• " + text)
        elif re.match(r"^\d+\. ", stripped):
            text = clean_md(stripped)
            pdf.set_font("DejaVu", "", 9)
            pdf.set_text_color(30, 30, 30)
            pdf.set_x(pdf.l_margin + 4)
            pdf.multi_cell(0, 5, text)
        else:
            text = clean_md(stripped)
            pdf.set_font("DejaVu", "", 9)
            pdf.set_text_color(30, 30, 30)
            pdf.multi_cell(0, 5, text)
        i += 1


def main():
    md = SRC.read_text(encoding="utf-8")

    pdf = DietaPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_font("DejaVu", "", FONT_REG)
    pdf.add_font("DejaVu", "B", FONT_BOLD)

    # Portada
    pdf.add_page()
    pdf.set_fill_color(15, 118, 110)
    pdf.rect(0, 0, pdf.w, 50, "F")
    pdf.set_y(15)
    pdf.set_font("DejaVu", "B", 26)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 14, "Dieta Semanal", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 14)
    pdf.cell(0, 8, "Fede — Plan plato por plato", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(20)
    pdf.set_text_color(30, 30, 30)
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(0, 7, "Datos del plan", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 10)
    datos = [
        ("Vigente desde", "Lunes 21/04/2026"),
        ("Calorias dias de gym", "2.250 kcal"),
        ("Calorias dias de descanso", "2.050 kcal"),
        ("Macros dias gym", "P 190 g | C 210 g | G 65 g"),
        ("Macros dias descanso", "P 185 g | C 175 g | G 60 g"),
        ("Hidratacion dia gym", "3,0 L"),
        ("Hidratacion dia descanso", "2,7 L"),
        ("Horario entreno", "08:00 AM (Lun/Mie/Vie)"),
        ("Comida libre", "Viernes a la noche"),
        ("Deficit", "~400-500 kcal/dia"),
        ("Objetivo", "Bajar 10 kg (105 -> 95 kg)"),
    ]
    for k, v in datos:
        pdf.set_font("DejaVu", "B", 10)
        pdf.cell(55, 6, k, border="B")
        pdf.set_font("DejaVu", "", 10)
        pdf.cell(0, 6, v, border="B", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(8)
    pdf.set_font("DejaVu", "B", 11)
    pdf.set_text_color(15, 118, 110)
    pdf.cell(0, 7, "Rotacion semanal de proteinas", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    rot = [
        ["Dia", "Almuerzo", "Cena"],
        ["Lunes", "Pollo + batata", "Merluza + zapallitos"],
        ["Martes", "Pollo + lentejas", "Tortilla de espinaca"],
        ["Miercoles", "Carne magra + arroz integral", "Pollo grille + ensalada"],
        ["Jueves", "Atun + garbanzos", "Brotola + brocoli"],
        ["Viernes", "Salmon + papa", "LIBRE"],
        ["Sabado", "Milanesa al horno", "Omelette con vegetales"],
        ["Domingo", "Asado moderado", "Ensalada completa"],
    ]
    render_table(pdf, rot)

    pdf.ln(3)
    pdf.set_font("DejaVu", "B", 11)
    pdf.set_text_color(15, 118, 110)
    pdf.cell(0, 7, "3 reglas de oro", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(30, 30, 30)
    reglas = [
        "1. Proteina en CADA comida. Siempre. Si falta la proteina, falta la comida.",
        "2. Carbos simples/almidones: manana o peri-entreno. De noche solo proteina y verduras.",
        "3. El snack nocturno (yogur griego + chia) no es opcional mientras el alcohol sea tentacion.",
    ]
    for r in reglas:
        pdf.multi_cell(0, 5, r)
        pdf.ln(0.5)

    # Secciones del menu (de LUNES en adelante)
    lines = md.split("\n")
    start_idx = None
    for idx, l in enumerate(lines):
        if l.strip().startswith("### LUNES"):
            start_idx = idx
            break
    if start_idx is None:
        # fallback: dump completo
        render_md(pdf, md)
    else:
        # Agarrar hasta el final del resumen semanal
        end_idx = len(lines)
        for idx, l in enumerate(lines[start_idx:], start=start_idx):
            if l.strip().startswith("## BATCH COOKING"):
                end_idx = idx
                break
        # Primero: secciones previas clave (hidratacion)
        hidrat_start = None
        for idx, l in enumerate(lines):
            if l.strip().startswith("### HIDRATACION"):
                hidrat_start = idx
                break
        if hidrat_start is not None:
            hidrat_end = start_idx
            render_md(pdf, "\n".join(lines[hidrat_start:hidrat_end]))
        # Despues el menu dia a dia
        render_md(pdf, "\n".join(lines[start_idx:end_idx]))

    pdf.output(str(OUT))
    print(f"PDF generado: {OUT}")
    print(f"Tamano: {OUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
