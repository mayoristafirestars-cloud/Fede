# Bitácora Fede — 2026-11-19 (Jue) — @nutricionista

## Ajuste de la dieta: sin cena, merienda-cena adelantada

**Pedido de Fede:** "quiero dejar de cenar, pero sin perder la energía de entrenamiento".

**Propuesta acordada:** no sacar las kcal de la cena sino adelantarlas. Se elimina la comida 4 (cena 19:30). La última comida pasa a ser una merienda-cena temprana con proteína real y verdura, además de lo que tenía la merienda post-bici; el resto de la cena se reparte entre el almuerzo y la merienda-cena. Kcal y proteína diarias, carbohidratos alrededor del gym y la bici, mini, comida 1 de huevos y tope de yemas, sin cambios.

**Horarios nuevos:**
- Lun-jue: mini 06:30, comida 1 08:30, almuerzo 12:30, **merienda-cena 17:30**.
- Viernes (gym 14:00): desayuno 07:00, almuerzo 12:00, mini 13:20, post-entreno 15:35, **merienda-cena 18:30**. Se eligió no fusionar con el post-entreno: quedaban 15 h sin comer antes del Hyrox del sábado y una sola toma de 975 kcal.
- Sábado: mini 07:30, comida 1 10:15, almuerzo 13:00, **merienda-cena 17:30**.
- Domingo: desayuno 09:00, almuerzo 12:30, **merienda-cena 17:30**.

**Qué se movió (la merienda post-bici de las 15:15 y la cena de las 19:30 se funden en una sola comida):**
- Almuerzo: se suma el postre de yogur 150 g y un carbohidrato de la cena (lun papa 150 g; mar boniato 160 g; mié zapallo 300 g crudo; jue papa 150 g; sáb boniato +75 g y yogur; dom boniato 100 g). Viernes sin cambios (el almuerzo es 2 h antes del gym).
- Merienda-cena: yogur 300 g + chía 5 g + maní 20 g + banana 80 g + 2 galletas (lo de la merienda post-bici) + el plato de la cena (pescado, pollo o peceto, verdura, aceite) + magnesio.

**Totales por día (sin cambios):** lun 2.186 kcal / P 207 (mini 199/5, c1 411/39, almuerzo 789/75, merienda-cena 787/88); mar 2.186 / 204 (199/5, 400/42, 772/78, 815/79); mié 2.167 / 205 (199/5, 422/39, 779/80, 767/81); jue 2.176 / 206 (199/5, 400/42, 745/74, 832/85); vie 2.174 / 204 (524/44, 476/46, 199/5, 442/47, merienda-cena 18:30 533/62); sáb 2.196 / 207 (199/5, 422/39, 724/73, 851/90); dom 1.892 / 197 (386/36, 720/78, 786/83). Carbohidratos y grasas de cada día iguales a los del 18/11 (mismos alimentos, otro horario).

**Opción nocturna (evaluada: sí, opcional, mínima y sin sumar kcal):** con la última comida a las 17:30 y 13 h hasta la mini, déficit de 800-900 kcal y despertares a las 3-4 am con sueño de 5-6 h, se deja una opción para hambre real. Es la mitad del lácteo de la merienda-cena (150 g de yogur; domingo 150 g de cottage) apartada con chía 5 g y magnesio para las 20:30 (~115 kcal, 16 g P). Como es la misma comida partida en dos, el día cierra igual con o sin ella. Viernes: sin opción (ya son 5 tomas). Hambre real = sigue después de 15 min con una infusión caliente. A las 3 am: agua o infusión, sin cocinar; si pasa 2 noches seguidas se aparta el yogur desde las 17:30 y se avisa. Entre la merienda-cena y la noche, solo agua o infusiones sin cafeína.

**Lista de compras:** sin cambios de cantidades (se mueven los mismos alimentos); se suma 1 caja de infusiones sin cafeína. Intercambios: se agregan la opción nocturna con cottage (135 g) y qué hacer si no se puede comer a las 17:30 (hasta las 18:30 sin cambios).

**Reglas:** se actualizan "no se saltea ninguna comida" (3 + mini; viernes 4 + mini; domingo 3), la comida de referencia (desde S5, reemplaza la merienda-cena del sábado, hasta las 21:00, máx 700 kcal), y se agrega "nada después de la merienda-cena salvo agua o infusiones".

**Por qué:** adherencia y sueño sin recortar energía. Adelantar en vez de sacar mantiene el déficit planeado y los carbohidratos alrededor del entrenamiento; cerrar la cocina temprano es compatible con la sospecha de resistencia a la insulina. El almuerzo y la merienda-cena concentran la proteína (75-90 g por toma, 2 g/kg diarios sin cambios).

**Alertas / pendientes:**
- Almuerzo más grande (720-790 kcal) 90 min antes de la bici de las 14:00 (sábado 60 min, pero ese crece menos): si cae pesado, mover 100-150 g de boniato o papa a la merienda-cena.
- Seguimiento 2 semanas: noches con opción nocturna, despertares con hambre, energía a las 07:00 y a las 14:00, horas de sueño. Si hay hambre real 3 noches por semana o cae el rendimiento, merienda-cena a las 18:30.
- Sin peso reciente (dato de abril), sin ECG ni analíticas: todo provisorio.

**Qué se le consulta al equipo:**
- Médico: despertares a las 3-4 am con IMC 35,9 (descartar apnea, tensión nocturna); función renal con tomas de 75-90 g de proteína; sigue pendiente el lipidograma por las yemas.
- Entrenador: si el almuerzo más grande molesta en la bici y si hay falta de energía a las 07:00 por cenar temprano.
- Psicólogo: vigilar hambre emocional nocturna con la última comida a las 17:30 y distinguirla del hambre real.

**Cambios que necesita el bot (`dieta_actual.json` y `recordatorios_plan_fede.py`):** reemplazar el JSON por el nuevo `dieta.json`; desaparece la "Comida 4: cena" (el recordatorio de las 19:00); aparecen la "merienda-cena" a las 17:30 (viernes 18:30) con kcal/proteína nuevas y el almuerzo con kcal/proteína nuevas. Los objetivos diarios (2185 / 1890 kcal; 204 / 197 g P) no cambian.

**Impacto:** `salud/dieta-actual.md`, `dieta.json` del scratchpad, `salud/bitacora.md`.

---
*Entrada manual del nutricionista. El bot genera el resumen automático del día en `salud/bitacora/2026-11-19.md` (no tocar).*
