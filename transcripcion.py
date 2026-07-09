"""
Transcripción de audios de WhatsApp (compartida por Max y Eva).
Usa faster-whisper local. El modelo se carga la primera vez que llega
un audio (la primera descarga puede tardar varios minutos).
"""
import os
import tempfile
import threading

# 'small' = buen balance calidad/velocidad en español.
# Otras opciones: 'base' (más rápido, menos preciso), 'medium' (mejor, más lento).
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_whisper = None
_lock = threading.Lock()


def get_whisper():
    global _whisper
    with _lock:
        if _whisper is None:
            from faster_whisper import WhisperModel

            print(f"[audio] Cargando modelo de transcripcion '{WHISPER_MODEL}' "
                  "(la primera vez descarga el modelo, puede tardar varios minutos)...")
            _whisper = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
            print("[audio] Modelo listo.")
    return _whisper


def transcribir(audio_bytes: bytes, suffix: str = ".ogg") -> str:
    model = get_whisper()
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        f.write(audio_bytes)
        ruta = f.name
    try:
        # El modelo no es thread-safe: un audio a la vez.
        with _lock:
            segments, _info = model.transcribe(ruta, language="es", vad_filter=True)
            return " ".join(s.text.strip() for s in segments).strip()
    finally:
        try:
            os.unlink(ruta)
        except OSError:
            pass


def sufijo_por_mime(mimetype: str) -> str:
    return ".mp3" if ("mp3" in mimetype or "mpeg" in mimetype) else ".ogg"
