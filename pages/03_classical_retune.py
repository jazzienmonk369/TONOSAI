import streamlit as st
lang_selector("03_classical_retune")
from lib.ui import lang_selector
from lib.i18n import t

st.header(t("nav.classical_retune"))

try:
    import librosa, soundfile as sf
    HAVE_LIBROSA = True
except Exception:
    HAVE_LIBROSA = False
    st.info(t("msg.librosa_missing"))

upload = st.file_uploader("Upload WAV/MP3", type=["wav","mp3","ogg"])
src_ref = st.selectbox("Source A4", [440.0, 442.0], index=0)
target = st.selectbox("Target A4", [440.0, 432.0, 444.0], index=1)

if upload:
    if not HAVE_LIBROSA:
        st.audio(upload)  # samo sviraj
    else:
        import io, numpy as np
        y, sr = librosa.load(upload, sr=None, mono=True)
        cents = 1200 * np.log2(target / src_ref)
        y2 = librosa.effects.pitch_shift(y, sr=sr, n_steps=cents/100)
        buf = io.BytesIO(); sf.write(buf, y2, sr, format="WAV"); buf.seek(0)
        st.audio(buf)
        st.download_button("Download WAV", buf, file_name="retuned.wav", mime="audio/wav")
