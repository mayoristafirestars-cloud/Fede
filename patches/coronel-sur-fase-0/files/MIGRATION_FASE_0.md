# Migración Fase 0 — Seguridad crítica

Esta es la guía para aplicar los cambios de Fase 0 sobre el CRM
Coronel Sur. Son cambios **no destructivos** para los usuarios
existentes (el login con "1234" sigue funcionando durante la
transición, gracias a la compatibilidad retroactiva MD5→bcrypt).

## Qué cambia

| Área | Antes | Después |
|---|---|---|
| Hash de passwords | MD5 (roto) | bcrypt factor 12 (estándar) |
| Sesiones | Diccionario en memoria | Tabla `sesiones` persistente |
| Expiración de sesión | Nunca | 8hs absolutas + 60min inactividad |
| Endpoints `/api/admin/*` | Sin auth | Requieren rol admin |
| Mutaciones por GET | Sí (Google bots pueden ejecutarlas) | Sólo POST |
| Hashes hardcodeados | Sí (`ef92b7...` visible en código) | Eliminados |
| Persistencia de DB | Se pierde con cada deploy | Render Disk en `/data` |
| Headers HTTP | Ninguno | HSTS, CSP, X-Frame-Options, etc. |
| Auditoría | — | Tabla `auditoria` lista para log |
| Backups | — | Script + cron a Drive, encriptado |

## Orden de pasos

Seguilos en este orden. Cada paso es independiente pero la secuencia
está pensada para no romper nada en producción.

---

### Paso 1 — Aplicar el patch al repo

El patch `fase-0-seguridad.patch` contiene todos los cambios. Lo aplicás
sobre el repo privado `Coronel-Sur`.

```bash
cd Coronel-Sur
git checkout main
git pull origin main
git checkout -b fase-0-seguridad
git apply --3way fase-0-seguridad.patch   # o: patch -p1 < fase-0-seguridad.patch
```

Si `git apply` tira algún conflicto porque tu `main` cambió después del
clon que hice yo, usá los archivos completos que están en el repo
`Fede/patches/coronel-sur-fase-0/`:

- Copialos sobre tu working tree respetando las rutas.
- `git add` + `git commit` manual.

**IMPORTANTE**: si el archivo `backend/db/coronel_sur.db` aparece en
`git status` como modificado/untracked, **NO lo commitees**. Eso es
parte del fix — ver Paso 5.

### Paso 2 — Instalar dependencias nuevas

```bash
pip install -r requirements.txt
```

Agrega: `bcrypt`, `cryptography`, `itsdangerous`, `google-auth`,
`google-api-python-client`.

### Paso 3 — Probar local

```bash
cd backend
python main.py
# En otra terminal
curl http://localhost:8000/health
# {"status":"ok"}
```

Probá hacer login con el usuario `fede` / `1234`:

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"fede","password":"1234"}'
```

Debería devolver `{"ok":true, "token":"...", "debe_cambiar_password": 0}`
y en la DB el hash de `fede` ya debería estar en bcrypt (empezar con
`$2b$`). Eso es la migración automática funcionando.

Probá un endpoint admin sin token (debería dar 401):

```bash
curl -X POST http://localhost:8000/api/admin/fix-tablas
# {"detail":"Token requerido"}
```

Con token admin (debería funcionar):

```bash
TOKEN="..."  # el token que devolvió el login
curl -X POST http://localhost:8000/api/admin/fix-tablas \
  -H "Authorization: Bearer $TOKEN"
```

### Paso 4 — Commit y push a tu repo privado

```bash
git add -A
git status   # verificar que NO aparezca backend/db/coronel_sur.db
git commit -m "Fase 0: seguridad crítica (bcrypt, sesiones DB, auth admin, headers)"
git push origin fase-0-seguridad
```

Armá un PR en GitHub desde `fase-0-seguridad` → `main`. Revisá los
diffs. Cuando estés conforme, mergeás.

### Paso 5 — Limpiar `coronel_sur.db` del historial de git

Seguí `scripts/remove_db_from_history.md`. **Esto reescribe el
historial**. Después del merge del PR, pero antes de abrir el repo a
colaboradores o volver a público.

### Paso 6 — Configurar Render

En el dashboard de Render, servicio `coronel-sur`:

1. **Settings → Plan**: cambiar de *Free* a **Starter** (USD 7/mes).
2. **Settings → Disks**: agregar disco
   - Name: `coronel-sur-data`
   - Mount path: `/data`
   - Size: 1 GB
3. **Environment** → Agregar:
   - `DB_PATH=/data/coronel_sur.db`
4. **Deploy** manual de la branch con los cambios.

El primer deploy crea la DB vacía en `/data/coronel_sur.db`. Los
siguientes deploys ya no la pisan.

### Paso 7 — Cargar los datos en la nueva DB

Una vez que el servicio responda en `/health`:

```bash
# Loguearse como admin (con MD5 legacy "1234" todavía funciona)
curl -X POST https://coronel-sur.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"fede","password":"1234"}'

# Usar el token:
TOKEN="..."

# Crear tablas en la nueva DB persistente
curl -X POST https://coronel-sur.onrender.com/api/admin/fix-tablas \
  -H "Authorization: Bearer $TOKEN"

# Reimportar el inventario (en lotes de 500, repetir hasta offset=9500)
for offset in 0 500 1000 1500 2000 2500 3000 3500 4000 4500 5000 5500 6000 6500 7000 7500 8000 8500 9000 9500; do
  curl -X POST "https://coronel-sur.onrender.com/api/admin/reimportar-inventario?offset=$offset" \
    -H "Authorization: Bearer $TOKEN"
  sleep 1
done
```

Los clientes y ventas históricas hay que re-importarlos con los
scripts de `importador/` — revisar ese workflow aparte.

### Paso 8 — Rotar passwords

**Crítico**: los hashes MD5 de "1234" estuvieron expuestos en el repo
público durante varias horas, por lo que deben considerarse
comprometidos.

Desde tu máquina local (no desde Render):

```bash
# Apuntar a la DB de producción? No, mejor hacerlo via endpoint.
# Opción A: por endpoint POST /api/auth/usuarios (más seguro)
```

Opción recomendada: desde el frontend, loguearte como fede/1234 una
última vez → ir a la sección de usuarios → cambiar TU password a una
fuerte. Después cambiar las de malcolm y anamar como admin.

Opción alternativa (script directo, solo si tenés acceso a la DB):

```bash
# Sólo funciona si podés acceder con Shell de Render:
python scripts/rotate_passwords.py
```

### Paso 9 — Configurar backups nocturnos

1. En Render, crear un **Cron Job** (servicio separado, gratis):
   - **Name**: `coronel-sur-backup`
   - **Command**: `cd /opt/render/project/src && python scripts/backup_nightly.py`
   - **Schedule**: `0 3 * * *` (03:00 UTC = 00:00 ART)
   - **Environment**: conectar al mismo repo.

2. En el Cron Job, Environment variables:
   - `DB_PATH=/data/coronel_sur.db` (tiene que montar el mismo disco)
   - `BACKUP_ENCRYPTION_KEY` → generala con:
     ```bash
     python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
     ```
     Copiá el output y pegalo como value. **Guardala también en un
     password manager** — si la perdés, los backups no sirven.
   - `BACKUP_DRIVE_FOLDER_ID` → ID de una carpeta nueva en Drive,
     compartida con la service account `coronel-sur-bot-reader@...`
     como **Editor** (no Viewer, porque tiene que crear archivos).
   - `GOOGLE_SERVICE_ACCOUNT_FILE=/etc/secrets/google-service-account.json`

3. Subir el JSON de la service account como Secret File en el Cron Job
   también (mismo procedimiento que en el servicio web).

4. Probar ejecución manual:
   - Click en "Trigger Run" en el Cron Job.
   - Ver logs — debería decir "✓ Backup completado".
   - Ir a Drive, verificar que apareció un archivo
     `coronel_sur_backup_YYYYMMDD_HHMMSS.db.enc`.

### Paso 10 — Verificación final

Checklist:

- [ ] `/health` devuelve `{"status":"ok"}`.
- [ ] Login con password vieja (`1234`) sigue funcionando **una vez**,
      y al siguiente login el hash en DB ya es bcrypt.
- [ ] Llamar `/api/admin/fix-tablas` sin Bearer devuelve 401.
- [ ] Llamar `/api/admin/fix-tablas` con Bearer admin funciona.
- [ ] Los usuarios rotaron passwords (ya nadie usa "1234").
- [ ] En Drive apareció el primer backup encriptado.
- [ ] En `git log --all -- backend/db/coronel_sur.db` no aparece nada.
- [ ] Headers de seguridad presentes:
      `curl -I https://coronel-sur.onrender.com/` muestra
      `strict-transport-security`, `x-frame-options`, `content-security-policy`.

## Qué NO cambió (y sigue pendiente para Fase 1+)

- Migrations automáticas (Alembic) — ver roadmap.
- Logging estructurado — ver roadmap.
- Rate limiting — ver roadmap.
- 2FA para rol admin — Fase 5.
- Cloudflare en frente — Fase 5.

---

## Rollback

Si algo se rompe fuerte y querés volver atrás:

```bash
# Local
git checkout main
# En Render, redeploy desde el último deploy estable
```

La compatibilidad retroactiva MD5 significa que incluso si la DB tiene
hashes bcrypt y volvés al código viejo, **nadie puede loguearse con la
versión vieja** (el código viejo sólo sabe verificar MD5 y los hashes
ya son bcrypt). Por eso: antes de mergear Fase 0, asegurate de tener
una backup del estado actual.

Para mitigar eso, podés correr el rollback script (no incluido todavía
— hacelo manual si hace falta): reemplazá los hashes bcrypt en la tabla
`usuarios` por los MD5 originales si hiciste backup de esa columna
antes. Pero es mejor no llegar a eso: el patch está probado y no debería
fallar.
