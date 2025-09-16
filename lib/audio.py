# lib/audio.py
from io import BytesIO
import wave
import numpy as np

# ---- Pure-Python WAV (bez 'soundfile') ----
def wav_bytes_pcm16(y: np.ndarray, sr: int = 44100) -> BytesIO:
    """
    Pretvori -1..1 float numpy niz u 16-bit PCM WAV (BytesIO u memoriji).
    Radi bez spoljašnjih biblioteka.
    """
    y = np.asarray(y, dtype=np.float32)
    y = np.clip(y, -1.0, 1.0)
    pcm16 = (y * 32767.0).astype(np.int16)

    buf = BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)   # mono
        wf.setsampwidth(2)   # 16-bit
        wf.setframerate(sr)
        wf.writeframes(pcm16.tobytes())
    buf.seek(0)
    return buf

# (Opciono) Jednostavan fade-in/out u ms; radi bez librosa
def fade_io(y: np.ndarray, sr: int, fade_in_ms=0, fade_out_ms=0):
    y = y.copy()
    fi = int(sr * fade_in_ms / 1000)
    fo = int(sr * fade_out_ms / 1000)
    if fi > 0:
        y[:fi] *= np.linspace(0.0, 1.0, fi)
    if fo > 0:
        y[-fo:] *= np.linspace(1.0, 0.0, fo)
    return y
