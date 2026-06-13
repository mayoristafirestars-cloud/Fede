# secrets/

Acá van los archivos con credenciales que NUNCA se suben a git.

## Google Cloud service account

Cuando crees la service account en Google Cloud Console y descargues el
JSON de la key, guardalo en esta carpeta con un nombre claro:

```
secrets/google-service-account.json
```

Después, en tu `.env` poné:

```
GOOGLE_SERVICE_ACCOUNT_FILE=secrets/google-service-account.json
```

## Protección

La carpeta está en `.gitignore` (ver raíz del proyecto `chatbot/`):

```
secrets/*
!secrets/.gitkeep
!secrets/README.md
```

Esto significa que todo archivo dentro de `secrets/` se ignora automáticamente,
salvo este README y el `.gitkeep` (que sirven sólo para que la carpeta exista
en el repo vacía). Si alguna vez ves que `git status` te muestra un archivo
nuevo de esta carpeta, **PARÁ y revisá** — probablemente sea una credencial
que no debería estar trackeada.

## Qué hacer si una credencial se filtró

1. Entrá a Google Cloud Console y **revocá** la key comprometida.
2. Generá una nueva key en la misma service account.
3. Reemplazá el archivo JSON en esta carpeta.
4. Reiniciá el bot.
