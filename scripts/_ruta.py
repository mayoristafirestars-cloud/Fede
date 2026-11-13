"""Agrega backend/ al path para que los scripts usen los mismos módulos que el servidor."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"))

from config import cargar_env  # noqa: E402

cargar_env()
