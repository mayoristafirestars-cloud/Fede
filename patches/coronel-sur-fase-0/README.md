# Fase 0 — Paquete de seguridad para Coronel-Sur

Este directorio contiene todo lo que necesitás para aplicar la Fase 0
(seguridad crítica) al repo privado `mayoristafirestars-cloud/Coronel-Sur`.

## Contenido

- **`fase-0-seguridad.patch`** — patch único con todos los cambios.
  Aplicable con `git apply --3way`.
- **`files/`** — copia completa de todos los archivos modificados o
  creados. Fallback si el patch no aplica limpio, o si preferís copiar
  archivo por archivo.
- **`files/MIGRATION_FASE_0.md`** — guía paso a paso para Fede.
  **Leelo primero**: explica qué hace cada cambio y el orden para
  aplicarlos sin romper producción.
- **`files/scripts/remove_db_from_history.md`** — instrucciones para
  limpiar el historial de git del `.db` commiteado (usando
  `git filter-repo`).

## Cómo aplicar (resumen)

### Opción A: patch único (recomendado)

```bash
# En tu repo privado Coronel-Sur (PC local)
cd Coronel-Sur
git checkout main
git pull origin main
git checkout -b fase-0-seguridad

# Aplicar el patch
git apply --3way /ruta/al/fase-0-seguridad.patch

# Revisar
git status
git diff --stat

# Commit y push
git add -A
git commit -m "Fase 0: seguridad crítica (bcrypt, sesiones DB, auth admin)"
git push origin fase-0-seguridad
```

Armar PR en GitHub desde `fase-0-seguridad` → `main`, revisar diffs y
mergear cuando estés conforme.

### Opción B: copiar archivos uno por uno

Si el patch tira conflictos porque tu `main` avanzó después de que yo
cloné el repo, copiá los archivos de `files/` sobre tu working tree
respetando las rutas. Después `git add -A` + commit manual.

**IMPORTANTE**: si aparece `backend/db/coronel_sur.db` como modificado
o como archivo a commitear, **NO lo commitees**. Ese archivo debe
desaparecer del repo — ver Paso 5 en `MIGRATION_FASE_0.md`.

## Resumen de cambios por archivo

| Archivo | Acción | Qué cambia |
|---|---|---|
| `.gitignore` | modificado | más estricto: *.db, secrets/, *.pem |
| `requirements.txt` | modificado | +bcrypt, cryptography, itsdangerous, google-auth |
| `render.yaml` | modificado | plan Starter, disk /data 1GB, healthCheckPath |
| `MIGRATION_FASE_0.md` | nuevo | guía paso a paso de aplicación |
| `backend/main.py` | modificado | middleware de headers de seguridad, endpoint /health |
| `backend/db/database.py` | modificado | detecta /data persistente, +tablas sesiones y auditoria, quita hashes hardcodeados |
| `backend/routers/auth.py` | modificado | usa bcrypt con fallback MD5, sesiones en DB, invalida sesiones al cambiar pass |
| `backend/routers/admin.py` | modificado | todos los endpoints requieren admin, solo POST, quita GETs mutativos |
| `backend/security/__init__.py` | nuevo | exporta API del módulo |
| `backend/security/passwords.py` | nuevo | bcrypt + fallback MD5 + política de fortaleza |
| `backend/security/sessions.py` | nuevo | sesiones persistentes con expiración |
| `backend/security/dependencies.py` | nuevo | require_auth, require_admin, require_role |
| `backend/security/headers.py` | nuevo | middleware HSTS, CSP, X-Frame-Options, etc. |
| `scripts/__init__.py` | nuevo | paquete |
| `scripts/backup_nightly.py` | nuevo | backup SQLite → Fernet → Google Drive |
| `scripts/rotate_passwords.py` | nuevo | setup inicial de passwords fuertes |
| `scripts/remove_db_from_history.md` | nuevo | guía git filter-repo |
| `backend/db/coronel_sur.db` | **borrado** | NO debe vivir en el repo |

## Compatibilidad y rollback

- Los usuarios existentes con password "1234" (MD5) **pueden seguir
  logueándose sin cambiar nada**. El código detecta MD5 legacy,
  valida, y re-hashea a bcrypt transparentemente.
- Al migrar todos los hashes, desactivar el fallback MD5 es un cambio
  de una línea en `security/passwords.py` (Fase 5).
- Rollback: revertir el merge. Pero ojo: si ya se re-hashearon hashes
  a bcrypt, el código viejo no los entiende (sólo maneja MD5). Lo mejor
  es no hacer rollback parcial — avanzar o mantener el branch.

## Verificación rápida tras el deploy

```bash
# Health check público
curl https://coronel-sur.onrender.com/health

# Admin sin token → debe dar 401
curl -X POST https://coronel-sur.onrender.com/api/admin/fix-tablas

# Headers de seguridad presentes
curl -I https://coronel-sur.onrender.com/
# Buscar: strict-transport-security, x-frame-options, content-security-policy
```

Cualquier duda, me avisás y vamos paso por paso.
