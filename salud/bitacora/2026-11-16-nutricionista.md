# Bitácora Fede — 2026-11-16 (Lun)

## Cambio de dieta — @nutricionista

**Qué:** `salud/dieta-actual.md` pasa a DEFINICIÓN ESTRICTA para 8 semanas (16/11/2026 al 10/01/2027). La dieta Paleo + lácteos anterior queda archivada en `salud/dieta-actual-anterior.md`.
- Objetivo único que resuelve la discrepancia del bot (1.800 kcal / 190 g) y la dieta (2.250 kcal / 200 g): lunes a sábado ~2.170 kcal (2.121 a 2.218 según el día), P ~205 g, C ~200 g, G ~64 g; domingo 1.926 kcal, P 199 g, C 116 g, G 77 g.
- Déficit estimado de 800-900 kcal/día sobre ~3.000 kcal de gasto (estimado, sin peso reciente). Ritmo esperado: semana 1 de -1,5 a -2,5 kg; desde la semana 2 de 0,6 a 0,8 kg/semana; en 8 semanas de -5 a -7 kg y de -5 a -7 cm de cintura.
- 8 tomas por día con gramos exactos: pre-entreno, post-entreno, desayuno, almuerzo, pre-bici (13:30), bici Z2 (14:00), post-bici (15:15), cena (19:30) y snack ancla (21:30).
- Carbohidratos alrededor del gym y la bici (banana, galletas de arroz, avena, arroz integral, boniato); lentejas, avena y boniato/papa enfriados por la sospecha de resistencia a la insulina.
- Viernes: el gym de las 14:00 ocupa el horario de la bici, hoy sin bici (dieta del día armada sin pre/post-bici). Miércoles: bici corta de 30-40 min (el gym ya trae Z2); si el Z2 se pasa a las 14:00, esa bici lo reemplaza. Domingo: caminata 60 min o bici 40 min, una sola.
- Reglas: alcohol 0, sin comida libre semanas 1-4 (desde la semana 5, una comida de referencia el sábado a la noche, máx 700 kcal, solo si el peso baja según lo esperado), todo con balanza, todas las comidas marcadas en el bot.

**Por qué:** pedido de Fede ("dieta estricta, bajar bastante, galletas de arroz si hace falta, gramos precisos, bici todos los días a las 14:00"). Con 6 días de gym de 85 min más bici, 1.800 kcal es un déficit de ~1.200 kcal y 2.250 kcal estaba pensada para 4 días de gym. Proteína ~1,95 g/kg para no perder músculo con 5-6 h de sueño.

**Pendiente / alertas:**
- Sin pesaje desde 17/04 (105 kg): pesar hoy en ayunas y registrar en `mediciones.md`; el plan se recalcula con ese dato.
- Adherencia marcada en el bot: 0 % en los días leídos (07/11 al 10/11). Sin datos reales no se puede ajustar: pedir que use los botones.
- Estudios: `salud/estudios/` sigue vacío. Se pide al médico ECG, tensión, glucemia, insulina, HbA1c, perfil lipídico, función renal y hepática, 25-OH D; validar el déficit y los suplementos (creatina, omega-3, vitamina D3, magnesio).
- Bot: actualizar `OBJETIVO_KCAL` y `OBJETIVO_PROT` y los recordatorios de comidas (ver abajo).

**Cambios que necesita el bot (`recordatorios_plan_fede.py`):**
- OBJETIVO_KCAL 1800 a 2170 (lun-sáb) y 1930 (domingo); OBJETIVO_PROT 190 a 205.
- Post-entreno 08:20 a 08:30; desayuno 09:00 a 10:00 (avena/yogur/cottage en lugar de 4 huevos + palta); sin pasas de uva; viernes con horarios nuevos (desayuno 06:30, media mañana 10:00, almuerzo 12:00, pre-entreno 13:20, post-entreno 15:35, sin cena libre).
- Nuevos: pre-bici 13:30, bici 14:00 (lun, mar, mié corta, jue, sáb; domingo caminata o bici), post-bici 15:15, cena 19:30. La merienda-cena de las 16:30 se elimina.
- Snack de las 21:30: yogur griego 150 g + chía 5 g (antes 100 g + 5 g).

**Impacto:** `salud/dieta-actual.md`, `salud/dieta-actual-anterior.md`, `salud/bitacora.md`, `salud/bitacora/2026-11-16.md`, `dieta.json` del scratchpad (para el PDF).

---

## Ajuste de la dieta: 4 comidas + 1 mini, pasta de maní y zapallo en vez de arroz — @nutricionista

**Qué:** `salud/dieta-actual.md` y `dieta.json` pasan de unas 10 tomas por día a **4 comidas grandes + 1 mini**, con pasta de maní y zapallo en la freidora de aire en lugar de arroz.
- **Esquema (lun-jue):** mini pre-entreno 06:30, comida 1 post-entreno 08:30 (bowl), comida 2 almuerzo 12:30, comida 3 merienda post-bici 15:15, comida 4 cena 19:30. **Viernes:** comida 1 desayuno 07:00, comida 2 almuerzo 12:00, mini pre-entreno 13:20, comida 3 post-entreno 15:35 (licuado), cena 19:30. **Sábado:** mini 07:30, comida 1 10:15, almuerzo 13:00, merienda 15:15, cena 19:30. **Domingo:** 4 comidas (09:00, 12:30, 15:15, 19:30), sin mini.
- Agua con sal, café, mate, suplementos y bici ya no son tomas: van dentro de una comida o en hidratación. El snack de las 21:30 desaparece: yogur griego 150 g + chía 5 g + magnesio quedan como postre de la cena. Pre-bici de 13:30 eliminado (los carbohidratos pasan al almuerzo y a la merienda).
- **Pasta de maní** 100 % maní, pesada: 20 g en la comida 1 y 20 g en la comida 3 (118 kcal, 5 g P, 10 g G por porción; 236 kcal y 20 g G por día). Domingo solo 20 g en la merienda. Reemplaza nueces, palta y parte del aceite.
- **Zapallo anco en freidora** (cubos de 2 cm, 200 °C, 15-20 min, 3 ml de aceite en spray): 400 g crudos (300 g cocidos) en el almuerzo de lunes y sábado; 300 g crudos (225 g cocidos) en la cena de miércoles y viernes. Arroz integral eliminado del plan, el batch cooking, la lista de compras y los intercambios. Se compensa con boniato en el almuerzo, avena de 50 g, banana y pasta de maní.
- **Totales:** lun 2.196 kcal (P 205, C 228, G 57); mar 2.198 (P 201, C 206, G 67); mié 2.166 (P 203, C 210, G 63); jue 2.197 (P 201, C 215, G 63); vie 2.159 (P 207, C 200, G 63); sáb 2.195 (P 205, C 228, G 57); dom 1.892 (P 197, C 113, G 72).
- **Cambio de kcal:** lun-sáb 2.170 a 2.185 en promedio (+15), domingo 1.926 a 1.892 (-34). Proteína ~204 g y déficit de 800-900 kcal sin cambios. Carbohidratos ~215 g (antes ~200) y grasas ~62 g (antes ~64).
- Reglas de ajuste actualizadas: -170 kcal (avena 50 a 30 g, maní de la merienda 20 a 10 g, 1 galleta) o +190 kcal (boniato 150 g + maní 10 g en la cena). Lista de compras: se agregan pasta de maní (350 g) y zapallo (1,8 kg con cáscara); se sacan arroz integral, nueces, arándanos y manzana.

**Por qué:** pedido textual de Fede: "¿podés meter pasta de maní? En vez de arroz, ¿podés meter zapallo en la freidora de aire? No tantas comidas... me vas a volver loco." Menos tomas hace más probable que marque todo en el bot (adherencia marcada en 0 %). Con 4 comidas de 440-610 kcal y 37-69 g de proteína por comida se mantiene la proteína ~204 g repartida.

**Pendiente / alertas:**
- El hambre nocturna puede subir al sacar el snack de las 21:30: si pasa, repetir el postre de yogur con chía como única toma extra y avisar. Vigilar señales de TCA (psicólogo).
- Sábado: almuerzo a las 13:00, una hora antes de la bici; si cae pesado, arrancar muy suave 15 min.
- Perfil lipídico pendiente: la grasa ahora viene sobre todo de pasta de maní, pescado y oliva.
- Sin pesaje desde 17/04: pesar en ayunas y registrar en `mediciones.md`.

**Cambios que necesita el bot (`recordatorios_plan_fede.py`):**
- OBJETIVO_KCAL 2185 (lun-sáb) y 1890 (domingo); OBJETIVO_PROT 204 (lun-sáb) y 197 (domingo).
- Dejar solo 5 tomas marcables por día (4 comidas + 1 mini; domingo 4) con los horarios y kcal/proteína de arriba. Sacar de las tomas marcables: despertar 05:30, pre-bici 13:30, bici 14:00, post-bici 15:15 como toma suelta, snack 21:30 y media mañana de las 10:00. La bici puede quedar como recordatorio sin botón de comida.
- Viernes y sábado con horarios propios (ver esquema). Cena 19:30 incluye el postre con el magnesio.

**Impacto:** `salud/dieta-actual.md`, `dieta.json` del scratchpad (para el PDF), `salud/bitacora.md`.

---
*Entrada manual del nutricionista. El bot genera el resumen automático del día en este mismo archivo.*
