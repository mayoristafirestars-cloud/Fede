# Rutina actual (fuerza) — 4 días/semana — FUERZA CON BARRA, PESOS PROYECTADOS

**Vigente desde:** 29/09/2026 (lunes) hasta 21/11/2026 — 8 semanas.
**Reemplaza a:** bloque "Cadena de movimientos" (14/09/2026). Fede pidió más dificultad y los principales con barra para cargar peso.
**Fuente única:** `rutina_fuerza.py` (de ahí salen este documento, `Plan-Fede-Rutina-Fuerza.pdf` y los recordatorios del bot con el peso de cada semana).

## Estructura

- **4 básicos con barra**, uno por día: press banca (lunes), sentadilla (martes), press militar de pie (jueves), peso muerto convencional (viernes).
- Se programan en **% del Training Max** (TM ≈ 90 % del máximo estimado): 5×5 en las semanas 1-2 y 5; serie pesada de 2-3 reps al 87,5-95 % + series de volumen en las semanas 3, 6 y 7.
- **Secundarios con barra** (remo, rumano, press inclinado, sentadilla frontal, hip thrust) con progresión lineal semanal.
- **Accesorios en superseries** (fondos + curl, tríceps + martillo) y dominadas.
- **Semana 4 descarga** y **semana 8 test**: serie pesada a máximas reps dejando 1, para medir y armar el bloque siguiente.

## Training Max (estimados desde los pesos del 25/09/2026)

| Básico | TM semanas 1-4 | TM semanas 5-8 |
|---|---|---|
| Press banca | 60 kg | 62,5 kg |
| Sentadilla | 80 kg | 85 kg |
| Peso muerto | 100 kg | 105 kg |
| Press militar | 37,5 kg | 40 kg |

Estimación: mancuernas 20 kg c/u en press → barra ×1,15; rumano 70 kg → peso muerto ×1,25; sentadilla ≈ 80 % del peso muerto; militar ≈ 62 % de la banca. **La semana 1 calibra**: si el 5×5 sale con más de 3 en reserva, se sube 5 kg y se cambia el TM en `rutina_fuerza.py` (se recalcula todo).

## Seguridad — restricción médica vigente

ECG y presión en farmacia siguen pendientes (carpeta `estudios/` vacía). Hasta tenerlos: mínimo 1 repetición en reserva siempre (también en el test), respiración controlada (aire adentro al bajar, afuera al subir, nunca más de 1 repetición sin respirar), sentadilla y banca con barras de seguridad o ayudante. Con ECG normal se habilitan singles pesados y test de máximo real.

## Series × reps por semana

| Semana | Tipo | Básicos (% del TM) | Secundarios | Accesorios |
|---|---|---|---|---|
| S1 · 29/09 | Carga | 5×5 al 75 % · RIR 2-3 | 4×8 · RIR 2-3 | 3×10-12 · RIR 2 |
| S2 · 06/10 | Carga | 5×5 al 80 % · RIR 2 | 4×8 · RIR 2 | 3×12 · RIR 2 |
| S3 · 13/10 | Carga | 1×3 al 87.5 % + 4×5 al 77.5 % · RIR 1-2 | 4×6 · RIR 2 | 3×10 · RIR 1-2 |
| S4 · 20/10 | Descarga | 3×5 al 65 % · RIR 4 | 3×6 · RIR 4 | 2×10 · RIR 4 |
| S5 · 27/10 | Carga | 5×5 al 82.5 % · RIR 2 | 4×6 · RIR 2 | 3×12 · RIR 2 |
| S6 · 03/11 | Carga | 1×3 al 90 % + 4×4 al 80 % · RIR 1-2 | 4×5 · RIR 1-2 | 3×10 · RIR 1-2 |
| S7 · 10/11 | Carga | 1×2 al 95 % + 3×3 al 85 % · RIR 1-2 | 4×5 · RIR 1-2 | 3×12 · RIR 1-2 |
| S8 · 17/11 | Test | 1×máx dejando 1 al 100 % + 3×3 al 80 % · RIR 1 | 4×5 · RIR 1-2 | 3×10 · RIR 1-2 |

## Pesos proyectados por día (kg)

En los básicos: serie pesada / series de volumen.

## Lunes 07:00 — Torso A · Press banca

| Ejercicio | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | Descanso |
|---|---|---|---|---|---|---|---|---|---|
| **Press banca con barra** (pesada/volumen) | 45 | 47,5 | 52,5/47,5 | 40 | 52,5 | 55/50 | 60/52,5 | 62,5/50 | 3 min |
| Remo con barra | 45 | 47,5 | 50 | 45 | 50 | 52,5 | 55 | 55 | 2 min |
| Jalón al pecho | 45 | 45 | 50 | 45 | 50 | 50 | 55 | 55 | 90 s |
| Superserie: Fondos asistidos + Curl con barra ⚠ calibrar | 20 | 20 | 22,5 | 20 | 22,5 | 22,5 | 25 | 25 | 90 s |
| Face pull en polea ⚠ calibrar | 15 | 15 | 17,5 | 15 | 17,5 | 17,5 | 20 | 20 | 60 s |

- **Press banca con barra:** Pies firmes, omóplatos juntos. Bajá al pecho en 2 s, sin rebotar.
- **Remo con barra:** Torso a 45°, tirá la barra al ombligo. Sin tirón con la cadera.
- **Jalón al pecho:** Pecho arriba, bajá la barra al esternón.
- **Superserie: Fondos asistidos + Curl con barra:** Fondos 3×máx dejando 2 y sin descanso curl con barra (el kg es del curl).
- **Face pull en polea:** Tirá la soga a la frente, codos altos. Salud de hombro.

## Martes 07:00 — Pierna A · Sentadilla

| Ejercicio | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | Descanso |
|---|---|---|---|---|---|---|---|---|---|
| **Sentadilla trasera con barra** (pesada/volumen) | 60 | 65 | 70/62,5 | 52,5 | 70 | 77,5/67,5 | 80/72,5 | 85/67,5 | 3 min |
| Peso muerto rumano con barra | 70 | 72,5 | 75 | 70 | 75 | 77,5 | 80 | 80 | 2 min |
| Sentadilla búlgara con mancuernas (kg c/u) | 15 | 15 | 17,5 | 15 | 17,5 | 17,5 | 20 | 20 | 90 s |
| Curl femoral en máquina ⚠ calibrar | 30 | 30 | 35 | 30 | 35 | 35 | 40 | 40 | 75 s |
| Rueda abdominal | — | — | — | — | — | — | — | — | 60 s |

- **Sentadilla trasera con barra:** Barra sobre trapecio, bajá hasta la paralela como mínimo, rodillas afuera.
- **Peso muerto rumano con barra:** Cadera atrás, barra pegada a las piernas, espalda neutra.
- **Sentadilla búlgara con mancuernas:** Las reps son por pierna.
- **Curl femoral en máquina:** Subida explosiva, bajada en 3 s.
- **Rueda abdominal:** 3 × 8-12. Si no sale desde las rodillas completa, rango corto.

## Jueves 07:00 — Torso B · Press militar

| Ejercicio | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | Descanso |
|---|---|---|---|---|---|---|---|---|---|
| **Press militar de pie con barra** (pesada/volumen) | 27,5 | 30 | 32,5/30 | 25 | 32,5 | 35/32,5 | 37,5/35 | 40/32,5 | 3 min |
| Press inclinado con barra | 35 | 37,5 | 40 | 35 | 40 | 42,5 | 45 | 45 | 2 min |
| Dominadas (asistidas si hace falta) | — | — | — | — | — | — | — | — | 2 min |
| Remo en polea sentado | 45 | 45 | 50 | 45 | 50 | 50 | 55 | 55 | 90 s |
| Superserie: Extensión de tríceps en polea + Curl martillo ⚠ calibrar | 20 | 20 | 22,5 | 20 | 22,5 | 22,5 | 25 | 25 | 75 s |

- **Press militar de pie con barra:** Glúteos y abdomen apretados, barra en línea recta, cabeza pasa adelante al final.
- **Press inclinado con barra:** Banco a 30°, bajá a la clavícula.
- **Dominadas (asistidas si hace falta):** 4 × máximo dejando 1. Cuando salgan 8 limpias, sumá peso con cinturón.
- **Remo en polea sentado:** Apretá omóplatos al final, sin balancearte.
- **Superserie: Extensión de tríceps en polea + Curl martillo:** Sin descanso entre los dos. Martillo con 10-12,5 kg c/u (el kg es del tríceps).

## Viernes 13:30 — Pierna B · Peso muerto

| Ejercicio | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | Descanso |
|---|---|---|---|---|---|---|---|---|---|
| **Peso muerto convencional con barra** (pesada/volumen) | 75 | 80 | 87,5/77,5 | 65 | 87,5 | 95/85 | 100/90 | 105/85 | 3-4 min |
| Sentadilla frontal con barra ⚠ calibrar | 40 | 42,5 | 45 | 40 | 45 | 47,5 | 50 | 50 | 2 min |
| Hip thrust con barra | 80 | 85 | 90 | 80 | 90 | 95 | 100 | 100 | 2 min |
| Zancada caminando con mancuernas (kg c/u) ⚠ calibrar | 15 | 15 | 17,5 | 15 | 17,5 | 17,5 | 20 | 20 | 90 s |
| Farmer walk pesado (kg c/u) ⚠ calibrar | 27,5 | 27,5 | 30 | 27,5 | 30 | 32,5 | 32,5 | 32,5 | 2 min |

- **Peso muerto convencional con barra:** Barra sobre el medio del pie, espalda neutra, empujá el piso. Cada rep desde el piso.
- **Sentadilla frontal con barra:** Codos altos, torso vertical. Si la muñeca molesta, agarre cruzado.
- **Hip thrust con barra:** Pausa 1 s arriba apretando glúteo.
- **Zancada caminando con mancuernas:** Las reps son pasos por pierna.
- **Farmer walk pesado:** El carry más pesado de la semana. Hombros atrás.

## Reglas de oro

1. Calentamiento 8 min (bici + movilidad) y aproximación antes del básico: barra sola ×10, 50 % ×5, 70 % ×3, 85 % ×1 del peso del día.
2. Respiración con barra: tomá aire y apretá el abdomen antes de bajar, soltalo durante la subida. Nunca más de 1 repetición sin respirar.
3. Mínimo 1 repetición en reserva: nada de fallo hasta tener el ECG. La semana 8 también es dejando 1.
4. Semana 1 = calibración: si el 5×5 sale sobrado (más de 3 en reserva), subí 5 kg por serie y anotalo con /nota. Se ajusta el TM y se recalcula todo.
5. Si no te salen las reps del peso proyectado: repetí esa semana antes de seguir.
6. Sentadilla y banca con barras de seguridad o ayudante. Siempre.
7. Si dormiste menos de 5 h: hacé el básico solo hasta las series livianas y cortá ahí.
8. Dolor en el pecho, mareo, falta de aire rara o palpitaciones: cortás la sesión.
9. Miércoles, sábado y domingo: bici zona 2, 40 min (FC 105-118).

## Revisión

- **Semana 1:** ajustar los TM con lo que salió en el 5×5.
- **Semana 4 (20/10):** descarga + remedición (peso, cintura, cadera).
- **Semana 8 (17/11):** test + cierre. Con esos números se arma el bloque siguiente.
