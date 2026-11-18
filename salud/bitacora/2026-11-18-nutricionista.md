# Bitácora Fede — 2026-11-18 (Mié) — @nutricionista

## Ajuste de la dieta: mini con pasta de maní y comida 1 de huevos

**Pedido de Fede:** después del gym no quiere otro desayuno de avena ("lo que desayuno antes de ir me gusta porque no me cae pesado"). Antes del gym come banana + 2 galletas de arroz con pasta de maní + café y quiere mantenerlo. Después del gym quiere algo con huevos, que puede cocinar antes de ir.

**Qué cambió (`salud/dieta-actual.md` y `dieta.json` del scratchpad):**
- **Mini pre-entreno** (lun-sáb, y viernes a las 13:20): banana 80 g + 2 galletas de arroz (18 g) + **10 g de pasta de maní** + café. 199 kcal, 5 g de proteína (antes 140 kcal, 2 g). 10 g es poco volumen para que no caiga pesado.
- **Comida 1 post-entreno** (lun-jue y sáb): el bowl de avena, whey 35 g y maní 20 g (480 kcal, 40 g P) se reemplaza por una comida de huevos cocinada la noche anterior, que se come fría o tibia: A) tortilla de espinaca y boniato (lunes), 411 kcal y 39 g P; B) omelette de champiñones, morrón y papa (martes y jueves), 400 kcal y 42 g P; C) huevos duros con boniato y tomate (miércoles y sábado), 422 kcal y 39 g P. Todas llevan 2 huevos enteros + 3 claras + whey 15 g con creatina 5 g en un shake con agua.
- **Viernes:** la mini de las 13:20 queda igual que el resto de la semana (con maní). El post-entreno de las 15:35 pasa del licuado (whey, yogur, maní, banana) a una tortilla en tupper (2 huevos, 4 claras, espinaca, boniato 130 g) más shake de whey 20 g con creatina: 442 kcal y 47 g P. El desayuno cambia el huevo duro por 2 claras.
- **Martes (cena):** salmón de 150 a 120 g, boniato de 100 a 160 g y claras de 2 a 3 (605 kcal, 59 g P) para compensar la grasa de los huevos y mantener kcal y proteína.
- **Tope de yemas (sin lipidograma):** máximo 3 por día y unas 15 por semana. Lun 2, mar 2, mié 3 (2 + 1 huevo duro del almuerzo), jue 2, vie 2, sáb 2, dom 2. Las claras completan la proteína.
- **Totales por día:** lun 2.186 kcal (P 207, C 217, G 60); mar 2.186 (P 204, C 203, G 67); mié 2.167 (P 205, C 207, G 64); jue 2.176 (P 206, C 199, G 67); vie 2.174 (P 204, C 203, G 64); sáb 2.196 (P 207, C 225, G 58); dom 1.892 (P 197, C 113, G 72, sin cambios). Promedio lun-sáb: 2.181 kcal y 205 g de proteína (objetivo ~2.185 y ~204).
- **Lista de compras:** se agregan huevos (41 por semana, o 15 + ~860 g de claras líquidas pasteurizadas), espinaca, champiñones, más boniato (1,5 kg), papa (500 g), tomate y morrón; baja la pasta de maní (200 g por semana, antes 260 g), el yogur (2,8 kg), el whey (120 g), las frutillas (300 g) y el salmón (350 g). La avena queda solo para el desayuno del viernes (100 g). Intercambios con huevo/claras, claras líquidas, espinaca y champiñones.

**Por qué:** adherencia. El pre-entreno que ya tolera y le gusta se mantiene tal cual (con maní) y el post-entreno lo hace en un tupper que sale de la heladera, sin cocinar a las 08:30. Los huevos aportan proteína y saciedad con poco carbohidrato, que encaja con la sospecha de resistencia a la insulina; el boniato o la papa de la comida 1 mantienen los carbohidratos post-entreno. Los números cierran sin cambiar el déficit.

**Pendiente / alertas:**
- Sin lipidograma: el tope de 3 yemas por día y 15 por semana es provisorio. Si el análisis sale alterado o el médico pide menos, se pasa a 1 yema por día y el resto en claras.
- Seguridad: tortilla, omelette y duros bien cocidos, en la heladera apenas se enfríen y consumidos dentro de las 48 horas.
- La mini suma 10 g de maní antes del gym: si cae pesada en las sesiones de pierna, sacarla y pasarla a la merienda.
- Adherencia marcada en el bot: revisar si ahora sube con el esquema de huevos.

**Cambios que necesita el bot (`recordatorios_plan_fede.py` y `dieta_actual.json`):**
- Mini pre-entreno: 199 kcal y 5 g de proteína con 10 g de maní (todos los días con mini, incluido el viernes).
- Comida 1 post-entreno (lun-jue y sáb) con las tres variantes de huevos y las kcal/proteína de arriba; viernes: desayuno 524 kcal y 44 g P, post-entreno 442 kcal y 47 g P; martes: cena 605 kcal y 59 g P.
- Objetivos del día sin cambios en lo esencial: OBJETIVO_KCAL 2185 / 1890 y OBJETIVO_PROT 204 / 197.

**Qué se le consulta al equipo:** al médico, si el tope de yemas es adecuado hasta tener lipidograma; al entrenador, si la mini con maní cae bien en los días de pierna.

**Impacto:** `salud/dieta-actual.md`, `dieta.json` del scratchpad (para el PDF), `salud/bitacora.md`.

---
*Entrada manual del nutricionista. El bot genera el resumen automático del día en `salud/bitacora/2026-11-18.md`.*
