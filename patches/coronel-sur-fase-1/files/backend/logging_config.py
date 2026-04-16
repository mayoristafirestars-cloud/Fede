"""
Logging estructurado para Coronel Sur.

Configura un logger principal con formato legible + archivo rotado.
Reemplaza los print() sueltos del código por logs trazables.

Uso:
    from logging_config import setup_logging
    setup_logging()  # llamar una vez al startup

    import logging
    log = logging.getLogger("modulo.nombre")
    log.info("algo pasó", extra={"user": "fede", "accion": "login"})
"""
from __future__ import annotations

import logging
import os
import sys
from logging.handlers import RotatingFileHandler


LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_FILE = os.environ.get("LOG_FILE", "")  # vacío = sólo stdout
LOG_MAX_MB = int(os.environ.get("LOG_MAX_MB", "10"))
LOG_BACKUP_COUNT = int(os.environ.get("LOG_BACKUP_COUNT", "5"))


class _ColorFormatter(logging.Formatter):
    """Colores para la terminal (si soporta ANSI)."""

    GREY = "\033[38;5;245m"
    BLUE = "\033[38;5;39m"
    YELLOW = "\033[38;5;220m"
    RED = "\033[38;5;196m"
    BOLD_RED = "\033[1;38;5;196m"
    RESET = "\033[0m"

    LEVEL_COLORS = {
        logging.DEBUG: GREY,
        logging.INFO: BLUE,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: BOLD_RED,
    }

    def __init__(self, use_color: bool = True):
        super().__init__(
            fmt="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.use_color = use_color

    def format(self, record):
        if self.use_color:
            color = self.LEVEL_COLORS.get(record.levelno, self.GREY)
            record.levelname = f"{color}{record.levelname}{self.RESET}"
            record.name = f"{self.GREY}{record.name}{self.RESET}"
        return super().format(record)


def setup_logging() -> None:
    """Configura el logging una sola vez al arrancar."""
    root = logging.getLogger()

    # Evitar duplicados si se llama más de una vez
    if root.handlers:
        return

    root.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    # Handler stdout
    is_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(_ColorFormatter(use_color=is_tty))
    root.addHandler(console)

    # Handler archivo (rotado)
    if LOG_FILE:
        try:
            os.makedirs(os.path.dirname(LOG_FILE) or ".", exist_ok=True)
            file_handler = RotatingFileHandler(
                LOG_FILE,
                maxBytes=LOG_MAX_MB * 1024 * 1024,
                backupCount=LOG_BACKUP_COUNT,
                encoding="utf-8",
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
            root.addHandler(file_handler)
        except Exception as e:
            root.warning("No pude crear el log file %s: %s", LOG_FILE, e)

    # Silenciar logs ruidosos de librerías
    for noisy in ("httpx", "httpcore", "urllib3", "multipart", "watchfiles"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    root.info(
        "Logging configurado: level=%s, file=%s", LOG_LEVEL, LOG_FILE or "(stdout only)"
    )
