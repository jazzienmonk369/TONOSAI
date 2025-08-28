import streamlit as st
import numpy as np
import math, io, wave, random

st.set_page_config(page_title="TONOSAI — AI Improvizator",
                   page_icon="static/favicon.png",
                   layout="wide")

st.title("🎹 AI Improvizator")

# -----------------------
# Skale i pomoćne funkcije
# -----------------------
KEYS = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
SCALES = {
    "Pentatonic":        [0, 3, 5, 7, 10],              # minor pent
    "Major":             [0, 2, 4, 5, 7, 9, 11],
    "Natural minor":     [0, 2, 3, 5, 7, 8, 10],
    "Dorian":            [0, 2, 3, 5, 7, 9, 10],
}

def midi_to_freq(m):
    # A4 (69) = 440 Hz
    return 440.0 * (2.0 ** ((m - 69) / 12.0))

def key_to_midi(key_name, octave=4):
    k = KEYS.index(key_name)
    return 12 * (octave + 1) + k   # C4=60

def adsr_envelope(n, sr, a=0.01, d=0.04, s=0.8, r=0.05):
    """Jednostavan ADSR u sekundama."""
    env = np.ones(n, dtype=np.float32)
    na, nd, nr = int(a*sr), int(d*sr), int(r*sr)
    # Attack
    if na > 0: env[:na] = np.linspace(0, 1, na)
    # Decay
    if nd > 0: env[na:na+nd] = np.linspace(1, s, nd)
    # Sustain (do poslednjih nr)
    if nr > 0: env[-nr:] = np.linspace(s, 0, nr)
    return env

def synth_sine(freq, dur, sr=44100, vol=0.12):  # bilo je 0.25 → sada ~ −18 dB po noti
    n = int(dur*sr)
    t = np.arange(n) / sr
    y = np.sin(2*np.pi*freq*t).astype(np.float32)
    y *= adsr_envelope(n, sr)
    return (vol * y)


def notes_to_wav(notes, sr=44100):
    ...
    # (staro) if np.max(np.abs(audio)) > 0: audio = audio / np.max(...) * 0.95
    peak = float(np.max(np.abs(audio)))
    if peak > 0:
        TARGET_PEAK = 0.25  # ≈ −12 dBFS (0 dBFS je 1.0)
        audio = audio / peak * TARGET_PEAK


    # norm i konverzija u int16
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio)) * 0.95
    pcm = (audio * 32767).astype(np.int16)

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)      # 16-bit
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())
    buf.seek(0)
    return buf

# -----------------------
# UI kontrole
# -----------------------
col1, col2, col3, col4, col5 = st.columns(5)
key_name = col1.selectbox("🎼 Tonalitet", KEYS, index=KEYS.index("C"))
scale_name = col2.selectbox("🎚 Skala", list(SCALES.keys()), index=0)
bpm = col3.slider("⏱ Tempo (BPM)", 60, 180, 120)
steps = col4.slider("🧩 Broj koraka", 8, 64, 24)
seed = col5.number_input("🔢 Seed", 1, 9999, 42)

dur_choice = st.radio("Trajanje nota", ["osmine", "četvrtine", "mešano"], horizontal=True)
generate = st.button("🎛 Generiši frazu", use_container_width=True)

# -----------------------
# Generisanje fraze
# -----------------------
if generate:
    random.seed(int(seed))

    base_midi = key_to_midi(key_name, octave=4)
    scale_ints = SCALES[scale_name]

    # bpm -> dužine
    beat = 60.0 / bpm
    if dur_choice == "osmine":
        possible_durs = [0.5*beat]
    elif dur_choice == "četvrtine":
        possible_durs = [1.0*beat]
    else:
        possible_durs = [0.5*beat, 1.0*beat]

    # random-walk po skali
    degree = 0
    notes = []
    for _ in range(steps):
        degree += random.choice([-2,-1,0,1,2])
        degree = max(min(degree, 12), -12)

        octave_shift = degree // len(scale_ints)
        scale_degree = degree % len(scale_ints)
        midi = base_midi + scale_ints[scale_degree] + 12*octave_shift
        freq = midi_to_freq(midi)
        dur = random.choice(possible_durs)
        notes.append((freq, dur))

    # Render u wav
    def notes_to_wav(notes, sr=44100):
    # 1) Napravi prazan bafer za ceo klip
    total_samples = int(sum(d for _, d in notes) * sr)
    audio = np.zeros(total_samples, dtype=np.float32)

    # 2) Redom sintetizuj note i „lepi“ ih u bafer
    pos = 0
    for freq, dur in notes:
        y = synth_sine(freq, dur, sr=sr)  # vol se čita iz session_state u synth_sine
        n = len(y)
        audio[pos:pos+n] += y
        pos += n

    # 3) Master normalizacija: na ciljnu „glavnu“ jačinu
    peak = float(np.max(np.abs(audio)))
    if peak > 0:
        TARGET_PEAK = st.session_state.get("target_pk", 0.25)  # ≈ −12 dBFS
        audio = audio / peak * TARGET_PEAK

    # 4) U int16 WAV
    audio = np.clip(audio, -1.0, 1.0)
    pcm = (audio * 32767).astype(np.int16)

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)      # 16-bit
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())
    buf.seek(0)
    return buf


    with st.expander("🎵 Pregled (prvih 12)"):
        preview = [f"{key_name} {scale_name} – f={f:.1f}Hz, d={d:.2f}s" for f,d in notes[:12]]
        st.write("\n".join(preview))

st.page_link("app.py", label="← Vrati se na početni meni")
