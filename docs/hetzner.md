# Nativa en Hetzner

Servidor nuevo de Nativa: 116.203.234.174, CPX12, Ubuntu 26.04, Python del sistema 3.14.4. No es el servidor de Coronel.
La aplicación se verificó en Python 3.12; el Dockerfile mantiene esa versión sin cambiar el Python del sistema.
La imagen Docker está preparada pero aún debe construirse y verificarse en el servidor.

## Preparación del servidor

Desde la sesión root de Nativa:

```bash
apt-get update
apt-get install -y docker.io git ca-certificates
systemctl enable --now docker
```

## Instalación después de transferir el código revisado

El checkout de trabajo contiene archivos nuevos aún no publicados en GitHub. No clonar el repositorio suponiendo que ya incluye esta versión. Transferir primero el código revisado sin bases, fotos ni secretos, o publicarlo en una rama y obtener esa rama.

Dentro de la carpeta que contiene el Dockerfile:

```bash
docker build -t nativa:inicial .
docker volume create nativa-datos
```

Antes de crear usuarios, trasladar de forma privada la base y fotos existentes si se quiere conservar la configuración local de Nativa. No iniciar una base vacía y luego sobrescribir operaciones reales.

Crear el primer dueño desde la terminal, sin escribir claves en comandos:

```bash
docker run --rm -it -v nativa-datos:/var/lib/nativa nativa:inicial python scripts/crear_dueno.py
```

Iniciar la aplicación sólo en la interfaz local del servidor:

```bash
docker run -d --name nativa --restart unless-stopped --log-opt max-size=10m --log-opt max-file=3 -p 127.0.0.1:8000:8000 -v nativa-datos:/var/lib/nativa nativa:inicial
curl --fail http://127.0.0.1:8000/healthz
```

Esto no publica el sistema a Internet. Falta configurar un nombre DNS, un proxy HTTPS y probar el acceso desde fuera. No desactivar Secure en las cookies para exponer HTTP. No abrir el puerto 8000 al público. El volumen contiene base y fotos y sobrevive al reemplazo del contenedor; no ejecutar `docker volume rm nativa-datos`.

Después: configurar respaldos diarios privados fuera del servidor y probar su restauración; revisar firewall conservando acceso SSH; configurar HTTPS antes de operar. Ver scripts/respaldo.py y docs/publicacion-sistema.md. El despliegue no está completado por crear estos archivos.
