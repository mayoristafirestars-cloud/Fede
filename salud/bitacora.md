# Bitácora

> Diario general + registro de cambios que hacen los agentes.
> Entradas nuevas arriba.

## Formato
```
## YYYY-MM-DD
**Autor:** @agente (o yo)
**Qué:** cambio hecho / observación
**Por qué:** razón
**Impacto:** qué archivos se tocaron
```

## 2026-08-27
**Autor:** @medico
**Qué:** Validación médica del plan de gym 4×/semana (Complexes A/B/A/B, hipertrofia) que se está formalizando con el entrenador. Screening preventivo pre-entreno.

**Contexto revisado:** perfil.md, historia-familiar.md, lesiones.md, mediciones.md (única fila, 17/04), suplementacion.md, plan-longevidad.md, agenda.md, carpeta estudios/ (vacía — sin ECG ni análisis todavía) y bitácora automática del bot (21/08 al 27/08).

**Hallazgo crítico:** a 4 meses de la evaluación inicial (17/04) sigue sin hacerse NINGÚN estudio de la lista de prioridad alta: sin ECG, sin análisis de sangre, sin TA registrada (ni en farmacia ni en casa), sin repetir cintura/mediciones desde el 17/04 (una sola fila cargada). Fede viene entrenando desde el 21/04 bajo el límite autoimpuesto de FC 121 lpm, pero esto es una aproximación, no un dato clínico real de FC máxima ni de respuesta cardíaca al esfuerzo.

**Nota sobre bitácora del bot (21/08–27/08):** todos los días muestran adherencia 0% y kcal/proteína en 0, con la columna "Estado" en "—" (sin respuesta) para prácticamente todos los recordatorios, salvo textos narrativos tipo "gym A hecho" dentro del recordatorio de post-entreno (que es el texto programado, no una confirmación real). Esto **no debe leerse como que Fede dejó de comer o de entrenar** — todo indica una falla de registro del bot (botones no capturados) más que un cambio real de conducta. Marcado para que el usuario corra `/sync` en Telegram o revise el servicio. No cambia la recomendación médica, pero impide usar estos 7 días como base objetiva de adherencia/déficit para evaluar fatiga o rendimiento.

**Diagnóstico:**
1. El plan de 4×/semana con complexes/hipertrofia **puede continuar**, pero bajo las mismas restricciones vigentes en `lesiones.md` (tope de FC 121 lpm = 70% de FC máx estimada, sin HIIT/Tabata/sprints, sin trabajo al fallo con Valsalva sostenida) hasta tener ECG.
2. FC máx estimada (fórmula Tanaka, más precisa que 220-edad en adultos con sobrepeso): 208 − (0,7×47) ≈ **174 lpm**. Zona de trabajo en fuerza/complexes hasta ECG: **≤ 70% (≈121 lpm)** sostenido, tolerando picos breves hasta 75% (≈131 lpm) en series cortas, nunca sostenido. Zona 2 (cardio): 60–70% = **105–122 lpm** (coincide con lo que ya usa el entrenador en bici, 105–118 lpm — correcto).
3. No se recomienda test de 1RM verdadero (esfuerzo máximo con Valsalva, obesidad grado II + riesgo CV sin ECG = mala combinación). Sí sirve un baseline de fuerza vía RM estimado a partir de series de 8–10 reps a RPE 8 (submáximo), más plancha/flexiones (ya en plan-longevidad.md) y opcionalmente dinamometría de mano (sin estrés cardiovascular, buen marcador de fuerza global y longevidad).
4. Señales de alarma — suspender el entreno YA y consultar guardia si aparecen: dolor u opresión en el pecho, dificultad respiratoria desproporcionada al esfuerzo, palpitaciones sostenidas o irregulares, mareo/presíncope, visión en túnel, sudoración fría fuera de lo esperable, dolor irradiado a brazo/mandíbula/espalda, taquicardia que no cede con el reposo.
5. Señales de sobreentrenamiento — bajar volumen si aparecen: FC de reposo matinal +5–7 lpm sostenida varios días sobre el basal, sueño que empeora (ya de por sí en 6 h, objetivo 7 h), irritabilidad/ánimo bajo, caída de rendimiento sesión a sesión, dolor articular persistente >48–72 h, apetito descontrolado o al revés inapetencia.

**Impacto:** `agenda.md` — nueva sección de alerta al tope marcando el bloqueo de progresión de intensidad hasta ECG + análisis + TA. No se tocaron `perfil.md`, `lesiones.md`, `rutina-actual.md` (restricciones ya vigentes desde 17/04 se mantienen sin cambios).

**Próximo paso:** turno con clínico esta semana para ECG + orden de análisis. Pedir al usuario que revise el bot de Telegram (posible falla de registro de adherencia).

---

## 2026-04-19 (noche 2)
**Autor:** coordinador (con Fede)
**Que:** Fede pidio cambiar de "low-carb mediterranea" a **PALEO + LACTEOS (Primal)** despues de mirar contenido sobre Marcos Llorente. Se acepto el cambio porque el 90% del plan actual ya cumplia (huevos, carne, pescado, verduras, tuberculos hervidos, frutos secos, palta, oliva, frutillas, banana, miel).
**Cambios concretos:**
- OUT: pan integral (los 4 desayunos de dias gym).
- Compensacion: +1 huevo duro en cada desayuno + mas palta + mas papa hervida en el post-entreno del viernes.
- Se descartan explicitamente los pilares no-evidence de Llorente: NO usar protector solar (riesgo cancer piel), NO gafas de sol (retina), excluir legumbres (contra la resistencia a insulina), excluir lacteos (Fede eligio mantenerlos).
- Se aceptan opcionales bajo-riesgo si le gustan: modo nocturno del celular 21:00, ducha fresca al final, caminar descalzo en el pasto al sol los fines de semana.
**Impacto:** `dieta-actual.md` renombrada a "Paleo + lacteos (Primal)". PDF Plan-Fede.pdf regenerado.

---

## 2026-04-19 (noche)
**Autor:** coordinador (con Fede)
**Que:** Fede consulto sobre usar GLOW GHK-CU (ALLUVI Healthcare) — blend inyectable subcutaneo de BPC-157 + TB-500 + GHK-Cu que le habian ofrecido. **Decision conjunta: NO usarlo por ahora.**
**Por que:** los 3 peptidos son "research use only", sin evidencia clinica seria en humanos. Riesgos especificos para el perfil de Fede:
- GHK-Cu sistemico puede sobrecargar higado (esteatosis pendiente de descartar por eco).
- BPC-157 + TB-500 son angiogenicos → riesgo teorico con antecedente familiar de cancer.
- Sin ECG basal ni analisis en mano.
- Mercado gris, pureza no garantizada.
**Condicion para reconsiderar:** tener labs completos + ECG + eco abdominal, y validacion presencial con medico clinico llevando la caja.
**Impacto:** `suplementacion.md` seccion nueva "FUERA DEL PLAN — no incluidos".

---

## 2026-04-19 (tarde)
**Autor:** @nutricionista (via coordinador)
**Que:** Menu semanal detallado dia por dia con variedad agregado al final de `dieta-actual.md`. Timing ajustado al entreno 08:00 AM (pre 06:30 liviano, post 09:15 batido, desayuno principal 10:30). Distribucion de hidratacion por franja horaria (3 L dias gym, 2,7 L descanso). Variedad completa de proteinas: pollo, pescado blanco, pescado graso, carne vacuna, huevos, atun, legumbres. Viernes cena = comida libre.
**Por que:** Fede pidio mayor granularidad: plato a plato, gramo a gramo, todos los dias con variedad, agua especifica, horarios ajustados a entreno 8 am.
**Impacto:** `dieta-actual.md` con seccion nueva "MENU SEMANAL DETALLADO" al final (7 dias completos con kcal y macros por comida).

---

## 2026-04-19
**Autor:** @nutricionista
**Que:** Plan alimentario inicial completo cargado en `dieta-actual.md`. Suplementacion inicial cargada en `suplementacion.md`.
**Por que:** Fede arranca gym el lunes 21/04/2026. Plan armado sobre TDEE 2.650–2.850 kcal (Apple Watch), deficit conservador 400–500 kcal = 2.250 kcal dias de entreno / 2.050 kcal dias de descanso. Macros dias entreno: P 190 g / C 210 g / G 65 g. Criterios aplicados: alta sospecha resistencia insulina (antecedente materno + obesidad grado II) → carbos orientados peri-entreno y manana, carga glucemica baja-media en el resto del dia; sueno 6 h → deficit conservador para no sumar estres fisiologico; corte reciente de alcohol → snack nocturno obligatorio como ancla anti-recaida; perfil comerciante → batch cooking dominical + comidas de 3 minutos.
**Impacto:** `dieta-actual.md` (creado completo), `suplementacion.md` (actualizado con creatina, omega-3, vitamina D y proteina en polvo — todos pendientes de validacion medica post-analisis).
**Proxima revision:** semana 3 (aprox. 12/05/2026) — revisar peso + cintura. Si no hay cambio, ajuste de -200 kcal.

---

## 2026-04-17 (noche)
**Autor:** @medico
**Qué:** Carga de hábitos, sueño y estado de ánimo inicial. Fede arranca gym el lunes 21/04.
**Por qué:** Autoeval del paciente. Datos clave que cambian el plan:
- **Sueño 6 h** (objetivo 7–8): el propio Fede lo identifica como su MAYOR problema.
- **Alcohol: corte voluntario declarado** ("no voy a tomar más") — lo usaba para relajarse. Requiere intervención del psicólogo.
- **No fuma**. Café por la mañana + mate siempre (revisar horario).
- **Estrés "medio"** crónico, perfil de comerciante + antecedente paterno de ansiedad.
- **Decisión del paciente:** arranca gym el lunes. Se mantiene la restricción de FC máx 121 lpm hasta ECG.
**Impacto:** `sueño.md`, `habitos.md`, `estado-animo.md`. 
**Próximo paso:** priorizar al psicólogo (sueño, alcohol, estrés) y al entrenador (rutina inicial conservadora para el lunes).

---

## 2026-04-17 (tarde 3)
**Autor:** @medico
**Qué:** Carga de actividad basal del Apple Watch. 748 kcal activas/día, 7,3 km/día, 25 min ejercicio/día. FC/FR "típico". Sueño y TA sin datos.
**Por qué:** Fede compartió screenshots de la app Salud.
**Impacto:** `perfil.md` con sección de actividad basal + implicancias para nutri/entrenador/psicólogo. Sigue pendiente TA (farmacia) y sueño (autoevaluación).

---

## 2026-04-17 (tarde 2)
**Autor:** @medico
**Qué:** Levantada restricción #2 (brazo derecho). Fede confirma dominancia diestra y funcionalidad plena.
**Por qué:** Asimetría explicada por dominancia, fractura sin secuela. El entrenador puede incluir press/dominadas/fondos sin precauciones extra por este motivo.
**Impacto:** `lesiones.md`, `perfil.md`.

---

## 2026-04-17 (tarde)
**Autor:** @medico
**Qué:** Carga de antropometría. Cintura 102 cm (umbral alarma), cadera 109, ICC 0.94 (riesgo aumentado), panza 107, pecho 111, brazo izq 36 / der 38 (posible dominancia), pierna pendiente.
**Por qué:** Fede pasó las medidas a pedido del médico.
**Impacto:** `mediciones.md` cargada primera fila. `perfil.md` actualizado con interpretación. TA sigue pendiente (el reloj no sirve).

---

## 2026-04-17
**Autor:** @medico
**Qué:** Evaluación médica inicial completa. Primera carga de datos del paciente.
**Por qué:** Fede cargó su perfil por primera vez. Se realizó screening de riesgo y planificación de estudios.
**Impacto:**
- `perfil.md` — agregada sección "Notas del médico" con evaluación inicial: IMC 35.9 (obesidad grado II), riesgo cardiovascular moderado-alto, datos faltantes críticos, restricciones para el equipo.
- `lesiones.md` — agregadas restricciones de entrenamiento vigentes: límite de FC, precaución brazo derecho, sin HIIT hasta estudios, monitoreo de presión.
- `agenda.md` — cargados estudios pendientes: análisis de sangre completo (prioridad alta), ECG basal (prioridad alta), tensión arterial basal, circunferencia de cintura, consulta clínico presencial, ecografía abdominal (media), ergometría (condicional).
**Datos de entrada registrados:** peso 105 kg, talla 171 cm, edad 47 años, 8000 pasos/día, sin medicación, fractura previa brazo derecho resuelta, padre con marcapasos/ansiedad, madre con diabetes tipo 2, abuela fallecida por cáncer.

---
