# Bitácora automática — Plan Fede

Esta carpeta se llena **automáticamente** con archivos generados por el bot de Telegram (`recordatorios_plan_fede.py`) que corre en el servidor Coronel.

## Estructura

- `YYYY-MM-DD.md` — reporte diario legible (para agentes y humanos)
- `raw/YYYY-MM-DD.jsonl` — eventos crudos del día (formato JSONL, uno por línea)

## Contenido de cada reporte diario

Cada archivo `.md` incluye:

1. **Resumen del día**
   - Adherencia: N/M recordatorios cumplidos (X%)
   - Kcal ingeridas / objetivo 2100
   - Proteína / objetivo 190 g
   - Kcal quemadas (ejercicio)
   - Balance neto

2. **Tabla de detalle** con cada recordatorio del día y su estado
   - ✅ Hecho
   - ⏭️ Skip
   - ✏️ Cambio
   - — Sin respuesta

3. **Cambios anotados**: cuando el usuario reemplazó una comida por otra

4. **Notas libres**: comentarios que el usuario le mandó al bot durante el día

## Cómo se genera

- El bot corre en `/opt/coronel-sur/backend/bot/recordatorios_plan_fede.py`
- Cada botón que el usuario toca en Telegram se registra en `bitacora_fede.jsonl`
- Cada noche a las 23:30 (Argentina) el bot:
  1. Genera el markdown del día
  2. Lo sube a este repo vía GitHub API en `salud/bitacora/YYYY-MM-DD.md`
  3. Sube también el JSONL crudo en `salud/bitacora/raw/YYYY-MM-DD.jsonl`
- También podés forzar un sync manual con el comando `/sync` en Telegram

## Cómo lo usan los agentes

- **Nutricionista**: analiza tendencias de comida (¿alcanza los 190g de proteína? ¿está en déficit? ¿reemplaza siempre la misma comida?) y ajusta el plan en `salud/dieta-actual.md`.
- **Médico**: cruza síntomas reportados con la adherencia y el estado nutricional real de los últimos 7-14 días.
- **Entrenador**: verifica que los recordatorios de gym/bici se estén cumpliendo antes de cambiar volumen o intensidad.
- **Psicólogo**: mira las notas libres para detectar patrones emocionales (hambre por estrés, atracones, cambios de humor).

## Fallback

Si el archivo del día NO existe, es porque:
- El bot estuvo caído
- El GITHUB_TOKEN no está configurado en el service del server
- No hubo eventos ese día (el bot no reportó nada)

En ese caso, el agente debe pedirle al usuario que corra `/sync` en Telegram o revise el servicio en el servidor.
