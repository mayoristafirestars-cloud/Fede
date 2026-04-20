# CLAUDE.md — Proyecto Fede + Coronel Sur

## Reglas permanentes de trabajo

### ⚡ Las soluciones tienen que ser DEFINITIVAS

Cuando Fede pide un fix o una mejora, no ofrecer parches temporales ni
workarounds que se vayan a romper otra vez. Apuntar siempre a la solución
que resuelve el problema **para siempre**:

- Si un bug ocurre porque un wrapper está mal, arreglar el wrapper (no
  parchear el síntoma).
- Si un dato se pierde al redeployar, configurar persistencia real (disco,
  Postgres externo).
- Si un endpoint es inseguro, asegurarlo bien (auth middleware + validación),
  no esconder la URL.
- Si hace falta instalar una herramienta (Git, librería, servicio),
  instalarla — no inventar rodeos que cuesten el triple de tiempo.

No perder tiempo con soluciones que tengan fecha de vencimiento corta.

### 📋 Otras reglas del proyecto

- **Español rioplatense** para todo lo que vea el cliente final.
- **Claude Haiku 4.5** por defecto para el bot (abaratar costo); subir a
  Sonnet 4.6 si la calidad no alcanza.
- **bcrypt factor 12** para passwords; NUNCA MD5 en código nuevo.
- **Nunca** commitear `.db`, `.env`, ni JSONs de service account.
- **Sólo POST** para endpoints que modifican estado.
- **Todo endpoint `/api/admin/*`** requiere rol admin.

---

## Estado actual (2026-04-18)

### Repositorios
- `mayoristafirestars-cloud/Fede` — repo público donde Claude tiene acceso
  vía MCP. Contiene patches preparados para Coronel-Sur en
  `patches/coronel-sur-fase-N/`.
- `mayoristafirestars-cloud/Coronel-Sur` — repo privado con el CRM real.
  **Claude NO tiene acceso MCP** a este repo; los cambios se aplican
  manualmente desde GitHub web o Git for Windows.

### Stack Coronel-Sur
- FastAPI + Python 3.11 + Uvicorn.
- Base de datos: **PostgreSQL** (DATABASE_URL en Render).
- Frontend: HTML/CSS/JS vanilla en `frontend/templates/index.html`.
- Deploy: Render (servicio `coronel-sur`, URL `https://coronel-sur.onrender.com`).
- Roles: `fede` admin, `malcolm` facturación, `anamar` crm.

### Fases de trabajo
- **Fase 0 (seguridad crítica)** — patch listo en `patches/coronel-sur-fase-0/`.
  Bcrypt, sesiones persistentes, auth admin, sólo POST, headers seguros.
  Estado: parcialmente aplicado (fix PGCur ya está en main).
- **Fase 1 (infraestructura)** — Alembic, structlog, slowapi. Pendiente.
- **Fase 2 (bot multicanal)** — patch listo en `patches/coronel-sur-fase-2/`.
  Pendiente aplicar.
- **Fase 3 (AFIP)** — diseño definido (facturas fiscales vs presupuestos
  internos). Pendiente WSFE.
- **Fase 4 (frontend)** — rediseño con design system + dark mode. Pendiente.
- **Fase 5 (seguridad avanzada)** — 2FA, Cloudflare, auditoría. Pendiente.
- **Fase 6 (event bus)** — para multiagentes. Pendiente.

### Bugs resueltos
- **PGCur eager-fetch en SELECT** → fix aplicado a main el 2026-04-18.
  Antes: `PGCur.__init__` consumía la primera fila de todo SELECT cuya
  primera columna se llamara `id`, rompiendo login y check-de-duplicados.
  Después: sólo consume si el original fue un `INSERT`.

### Decisiones arquitecturales aprobadas
- El bot multicanal se **integra al CRM** como router, no es servicio
  separado. Comparten DB, deploy y auth.
- Todos los agentes futuros leen del **single source of truth** (la DB
  del CRM). No duplicar datos.
- Google Sheets **descartado** como fuente para el bot desde que está
  la DB persistente en Postgres.
- Render en plan **Starter** cuando haya que escalar (no Free, que
  duerme tras 15 min).
