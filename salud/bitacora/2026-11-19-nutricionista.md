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

## Segundo ajuste del día: despertar 06:00, desayuno liviano + segundo desayuno, suplementos

**Pedido de Fede:** "me levanto a las 6 y desayuno; un desayuno más liviano y después, en el negocio, otro desayuno; después el almuerzo y la merienda-cena así como está; meteme los suplementos".

**Horarios nuevos (kcal y proteína de cada día sin cambios):**
- Lun-jue (gym 07:00): 06:00 mini liviano (199 kcal, sin cambios de contenido, ahora 1 h antes del gym), **09:00 segundo desayuno en el negocio** (la comida de huevos de siempre, en tupper, con el shake), 12:30 almuerzo, 17:30 merienda-cena. 4 tomas.
- Viernes (gym 14:00): 06:00 desayuno liviano (yogur 150 g + frutillas, 122 kcal / 16 g), 09:30 segundo desayuno (avena 50 g remojada en yogur 100 g + maní 20 g + 2 claras, 402 / 28), **12:15 almuerzo + pre-entreno** (almuerzo 476/46 + mini 199/5 fusionados = 675 / 51), 15:35 post-entreno (442/47), 18:30 merienda-cena (533/62). Total 2.174 / 204. Se fusionó la mini con el almuerzo para no pasar de 5 tomas; el café de las 13:20 queda sin comida. No se fusionó post-entreno con merienda-cena (15 h de ayuno antes del Hyrox).
- Sábado (Hyrox 08:30): mini 07:00 (antes 07:30), 10:15 post-entreno y segundo desayuno, 13:00 almuerzo, 17:30 merienda-cena. 4 tomas.
- Domingo: 07:00 desayuno liviano (cottage 200 g + tomate 100 g + creatina, 152 / 24), 10:00 segundo desayuno (2 huevos duros + palta 50 g, 234 / 12), 12:30 almuerzo, 17:30 merienda-cena. 4 tomas, 1.892 / 197 igual.

**Suplementos dentro de la comida (para que el bot los recuerde):** whey 15 g (vie 20 g) y creatina 5 g en el shake de la comida de huevos; omega-3 1 g de EPA+DHA y vitamina D3 2.000 UI en el almuerzo (todos los días; el viernes en el almuerzo de las 12:15); magnesio glicinato 300 mg en la merienda-cena (ya estaba). Solo el whey tiene kcal y ya estaba contado. Domingo: creatina a las 07:00.

**Cambio de dosis (para el médico):** el omega-3 baja de 2-3 g a **1 g de EPA+DHA** y la D3 pasa de 2.000-4.000 UI a **2.000 UI fija**, porque hay antecedente paterno de arritmia, ECG sin hacer y 25-OH D sin medir; se sube solo si el médico lo indica con el lipidograma. Creatina, omega-3, D3 y magnesio quedan "validar con el médico antes"; whey "OK". Evaluados y no agregados: psyllium (la fibra ya es alta), electrolitos para la bici (Z2 de 45-60 min, sodio prudente), cafeína en cápsulas, multivitamínico (esperar análisis), melatonina y ashwagandha (apnea posible, sospecha de hígado graso).

**Por qué:** pedido de Fede; la mini a las 06:00 da 1 h de digestión antes del gym y la comida de huevos a las 09:00 llega ~35 min después de terminar (si sale flojo, el shake va en el vestuario a las 08:25); el reparto del viernes y el domingo mantiene los mismos alimentos.

**Qué se le consulta al médico:** visto bueno de los 4 suplementos en una consulta; 25-OH D, perfil lipídico, función renal (creatina), ECG y tensión; despertares a las 3-4 am (apnea).
**Al entrenador:** la mini de las 06:00 queda 1 h antes del gym; avisar si cae pesada con pierna A.

**Cambios que necesita el bot (`dieta_actual.json` y `recordatorios_plan_fede.py`):** nuevos horarios (lun-jue mini 06:00 y comida 1 09:00; viernes 06:00, 09:30, 12:15, 15:35, 18:30 sin mini; sábado mini 07:00; domingo 07:00, 10:00, 12:30, 17:30); el viernes y el domingo pasan de 5 y 3 a 5 y 4 tomas; los items de omega-3 y vitamina D3 aparecen dentro del almuerzo.

**Impacto:** `salud/dieta-actual.md`, `salud/suplementacion.md`, `dieta.json` del scratchpad, `salud/bitacora.md`.

---
*Entrada manual del nutricionista. El bot genera el resumen automático del día en `salud/bitacora/2026-11-19.md` (no tocar).*
