# Limpiar `backend/db/coronel_sur.db` del historial de git

El archivo de base de datos (6.5 MB, con datos reales de clientes,
productos, ventas y hashes MD5) estuvo commiteado al repo durante
varios commits. Aunque lo borremos ahora, **sigue siendo accesible
en el historial** para quien clone el repo.

Mientras el repo esté privado, el riesgo está contenido a quien tenga
acceso. Pero hay que limpiar el historial igual antes de:

- Hacer el repo público de nuevo.
- Agregar colaboradores.
- Pushear forks.

## Opción recomendada: `git filter-repo`

Es la herramienta oficial que recomienda GitHub (reemplazo moderno de
`git filter-branch`, que está deprecado).

### 1. Instalar

```bash
# macOS
brew install git-filter-repo

# Linux (debian/ubuntu)
sudo apt install git-filter-repo

# Windows
pip install git-filter-repo
```

### 2. Hacer backup local

Antes de tocar el historial, cloná el repo aparte por seguridad:

```bash
git clone https://github.com/mayoristafirestars-cloud/Coronel-Sur.git coronel-sur-backup
```

Si algo sale mal, tenés el estado previo.

### 3. Ejecutar la limpieza

Posicionate en tu clon de trabajo:

```bash
cd Coronel-Sur

# Borrar el .db de TODO el historial
git filter-repo --path backend/db/coronel_sur.db --invert-paths

# Opcional: también borrar otros binarios grandes que hayas commiteado por error
# git filter-repo --path "*.zip" --path "*.xlsx" --invert-paths
```

El comando reescribe la historia: cada commit que tocaba ese archivo
se rehace sin él.

### 4. Forzar push

`git filter-repo` desconecta el remote por seguridad. Hay que volver a
agregarlo y pushear con `--force`:

```bash
git remote add origin https://github.com/mayoristafirestars-cloud/Coronel-Sur.git
git push --force --all origin
git push --force --tags origin
```

⚠️ **Push forzado** sobreescribe el historial en el remoto. Cualquiera
con un clon previo tiene que re-clonar. En tu caso sos el único, así
que no hay impacto.

### 5. Confirmar que el archivo ya no está

```bash
# No debería devolver nada
git log --all --full-history -- backend/db/coronel_sur.db

# Tampoco con grep
git rev-list --all | xargs git grep -l "coronel_sur.db" 2>/dev/null || echo "limpio"
```

### 6. Dejar una marca

Agregá esta linea al `.gitignore` (ya está, pero verificá):

```
*.db
*.sqlite
*.sqlite3
```

Y una regla extra de seguridad — un pre-commit hook que rechace
cualquier `.db` que intentes agregar:

```bash
mkdir -p .githooks
cat > .githooks/pre-commit << 'EOF'
#!/bin/bash
if git diff --cached --name-only | grep -qE '\.(db|sqlite|sqlite3)$'; then
    echo "ERROR: estás intentando commitear un archivo de base de datos."
    echo "Si es un error, hacé: git restore --staged <archivo>"
    exit 1
fi
EOF
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
```

## Después de limpiar

Asumí que los datos que estaban en ese `.db` están **comprometidos**
(los hashes MD5 de "1234" sobre todo). Acciones posteriores:

1. Correr `python scripts/rotate_passwords.py` — genera passwords nuevas
   fuertes con bcrypt y pide cambio obligatorio al login.
2. Revisar logs de tu sistema en Render por si hubo logins sospechosos.
3. Si tu sistema tenía DNI, teléfonos o direcciones de clientes reales,
   considerá si corresponde notificar a los afectados según la Ley
   25.326 de Protección de Datos Personales.
