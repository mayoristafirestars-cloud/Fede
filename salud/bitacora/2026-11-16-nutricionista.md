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
*Entrada manual del nutricionista. El bot genera el resumen automático del día en este mismo archivo.*
