FROM python:3.12.14-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    NATIVA_ENV=production CORONEL_SECURE_COOKIE=1 \
    CORONEL_DB_PATH=/var/lib/nativa/nativa.db \
    CORONEL_MEDIA_DIR=/var/lib/nativa/uploads
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --uid 10001 --create-home nativa \
    && mkdir -p /var/lib/nativa/uploads \
    && chown -R nativa:nativa /var/lib/nativa
COPY backend/ backend/
COPY frontend/ frontend/
COPY scripts/ scripts/
RUN chmod -R a+rX /app
USER nativa
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=3)"
CMD ["uvicorn", "main:app", "--app-dir", "backend", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
