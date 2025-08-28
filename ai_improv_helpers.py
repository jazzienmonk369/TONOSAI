# pages/04_ai_improvizator.py
import io, wave, random, math
import numpy as np
import streamlit as st
import boot


# ── Page & theme ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TONOSAI — AI Improvizator",
    page_icon="static/favicon.png",
    layout="wide",
)
from lib.ui import header_badges, footer

header_badges()


# Kosmički CSS (isti kao na home-u)
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{
  background: radial-gradient(1200px 600px at 15% -10%, #10163c 0%, #0a0f2a 45%, #070b1f 100%);
}
section[data-testid="stSidebar"] > div:first-child{
  background:#0b1030; border-right:1px solid #273056;
}
h1,h2,h3,h4 { color:#E6E8FF !important; }
a { color:#77a0ff !important; }
</style>
""", unsafe_allow_html=True)

st.title("🎹 AI Improvizator")

# ── Skale i pomoćne funkcije ───────────────────────────────────────────────────
KEYS = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
SCALES = {
    "Pentatonic":        [0, 3, 5, 7, 10],             # minor pent
    "Major":             [0, 2, 4, 5, 7, 9, 11],
    "Natural minor":     [0, 2, 3, 5, 7, 8, 10],
    "Dorian":            [0, 2, 3, 5, 7, 9, 10],
}

def midi_to_freq(m: int) -> float:
    # A4 (69) = 440 Hz
    return 440.0 * (2.0 ** ((m - 69) / 12.0))

def key_to_midi(key_name: str, octave: int = 4) -> int:
    k = KEYS.index(key_name)
    return 12 * (octave + 1) + k  # C4=60

def adsr_envelope(n: int, sr: int, a=0.01, d=0.04, s=0.8, r=0.05) -> np.ndarray:
    """Jednostavan ADSR u sekundama."""
    env = np.ones(n, dtype=np.float32)
    na, nd, nr = int(a*sr), int(d*sr), int(r*sr)
    if na > 0:
        env[:na] = np.linspace(0, 1, na)
    if nd > 0:
        env[na:na+nd] = np.linspace(1, s, nd)
    if nr > 0:
        env[-nr:] = np.linspace(s, 0, nr)
    return env

def synth_sine(freq: float, dur: float, sr: int = 44100, vol: float = 0.12) -> np.ndarray:
    """Jednostavan sinus sa blagim ADSR; vol smanjen (~−18 dB po noti)."""
    n = int(dur * sr)
    t = np.arange(n) / sr
    y = np.sin(2 * np.pi * freq * t).astype(np.float32)
    y *= adsr_envelope(n, sr)
    return vol * y

def notes_to_wav(notes, sr: int = 44100) -> io.BytesIO:
    """Spaja note u jedan signal, peak-limit ≈ −12 dBFS i vraća WAV u memoriji."""
    parts = [synth_sine(f, d, sr=sr) for f, d in notes]
    audio = np.concatenate(parts) if parts else np.zeros(1, dtype=np.float32)

    # Peak-limit na ~0.25 (≈ −12 dBFS)
    peak = float(np.max(np.abs(audio)))
    if peak > 0:
        audio = audio / peak * 0.25

    pcm = (audio * 32767).astype(np.int16)

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)     # mono
        wf.setsampwidth(2)     # 16-bit
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())
    buf.seek(0)
    return buf





# ── UI ─────────────────────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
key_name   = col1.selectbox("🎼 Tonalitet", KEYS, index=KEYS.index("C"))
scale_name = col2.selectbox("🎚 Skala", list(SCALES.keys()), index=0)
bpm        = col3.slider("⏱ Tempo (BPM)", 60, 180, 120)
steps      = col4.slider("🧩 Broj koraka", 8, 64, 24)
seed       = col5.number_input("🔢 Seed", 1, 9999, 42)

dur_choice = st.radio("Trajanje nota", ["osmine", "četvrtine", "mešano"], horizontal=True)
generate   = st.button("🎛 Generiši frazu", use_container_width=True)

# ── Generisanje fraze ─────────────────────────────────────────────────────────
if generate:
    random.seed(int(seed))

    base_midi   = key_to_midi(key_name, octave=4)
    scale_ints  = SCALES[scale_name]

    beat = 60.0 / bpm
    if dur_choice == "osmine":
        possible_durs = [0.5 * beat]
    elif dur_choice == "četvrtine":
        possible_durs = [1.0 * beat]
    else:
        possible_durs = [0.5 * beat, 1.0 * beat]

    degree = 0
    notes  = []
    for _ in range(steps):
        degree += random.choice([-2, -1, 0, 1, 2])
        degree  = max(min(degree, 12), -12)

        octave_shift = degree // len(scale_ints)
        scale_degree = degree %  len(scale_ints)
        midi = base_midi + scale_ints[scale_degree] + 12 * octave_shift
        freq = midi_to_freq(midi)
        dur  = random.choice(possible_durs)
        notes.append((freq, dur))

    wav_buf = notes_to_wav(notes)
    st.audio(wav_buf, format="audio/wav")
    st.download_button("⬇️ Preuzmi WAV", wav_buf, file_name="improv.wav", mime="audio/wav")

    with st.expander("🎵 Pregled (prvih 12)"):
        preview = [f"{key_name} {scale_name} – f={f:.1f}Hz, d={d:.2f}s" for f, d in notes[:12]]
        st.write("\n".join(preview))

st.page_link("app.py", label="← Vrati se na početni meni")
footer()

