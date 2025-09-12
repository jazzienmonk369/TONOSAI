# pages/showcase.py
import os, streamlit as st
VERSION = os.getenv("TONOSAI_VERSION", "v0.1.1")

st.markdown("<hr>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1,1,1])
with c1:
    st.page_link("pages/manifest.py", label="🌠 Manifest")
with c2:
    st.page_link("pages/99_team.py", label="👩‍🚀 Tim")
with c3:
    st.caption(f"verzija: {VERSION}")

import streamlit as st
from pathlib import Path

def find_audio(base):
    audio_dir = Path("static/audio")
    for ext in (".ogg", ".mp3", ".wav"):
        p = audio_dir / f"{base}{ext}"
        if p.exists(): 
            return p
    return None

# primer korišćenja:
tones = { name: find_audio(name.lower()) for name in ["432hz", "528hz"] }
ambients = { k: find_audio(v) for k,v in {"Šuma":"forest","Reka":"river","Kiša":"rain"}.items() }


st.set_page_config(page_title="Showcase — TONOSAI", page_icon="🎬", layout="wide")

st.title("🎬 TONOSAI Showcase")
st.caption("Kratka kosmička izložba: Manifest → Balans 2.0")

with st.expander("Scenarij (3–5 min) – vodič za snimanje", expanded=False):
    st.markdown("""
**1. Intro (0:00–0:30)** – zvezdano nebo + logo, lagani 528Hz vibrafon.  
**2. Manifest (0:30–1:30)** – klik na zvezdu, poetska poruka + zvonce.  
**3. Balans 2.0 (1:30–2:30)** – priroda + 432/528Hz ton.  
**4. Završnica (2:30–3:00)** – poziv zajednici, fade-out.
""")

# --- Demonstracioni "flow" unutar app-a
c1, c2 = st.columns(2)

with c1:
    st.subheader("🌠 Manifest (demo)")
    st.write("Klikni zvezdu da otvoriš poruku.")
    colA, colB = st.columns(2)
    with colA:
        if st.button("⭐ Kosmos"):
            st.success("Sve je povezano. Svaka misao je svetlost u mreži.")
    with colB:
        if st.button("🌿 Čovek"):
            st.success("Dah, ritam i namera su naš instrument.")

with c2:
    st.subheader("🌿 Balans 2.0 (demo)")
    amb = st.selectbox("Ambijent", ["Šuma", "Reka", "Kiša"])
    ton = st.radio("Ton", ["432Hz", "528Hz"], horizontal=True)
    st.write(f"Preporuka: **{amb} + {ton}** — 5–10 minuta, disanje 4–4–6.")

st.divider()
st.markdown("**Snimanje videa?** Otvori OBS → prikaži uvod, klikni 1–2 zvezde u Manifestu → prikaži Balans 2.0 → završna poruka.")
# --- Audio preview (432 / 528 + priroda) ---
from pathlib import Path

st.subheader("🔊 Audio preview")

AUDIO_DIR = Path("static/audio")
tones = {
    "432Hz": AUDIO_DIR / "432hz.ogg",
    "528Hz": AUDIO_DIR / "528hz.ogg",
}
ambients = {
    "Šuma":  AUDIO_DIR / "forest.ogg",
    "Reka":  AUDIO_DIR / "river.ogg",
    "Kiša":  AUDIO_DIR / "rain.ogg",
}

colT, colA = st.columns(2)

with colT:
    st.caption("Tonska paleta")
    for name, p in tones.items():
        if p.exists():
            st.audio(str(p))
            st.text(name)
        else:
            st.warning(f"Nedostaje: {p.as_posix()}")

with colA:
    st.caption("Prirodni ambijenti (opciono)")
    for name, p in ambients.items():
        if p.exists():
            st.audio(str(p))
            st.text(name)
        else:
            st.info(f"Dodaj fajl: {p.as_posix()}")
            # --- Auto-loop podloga (mute/volume) ---
from pathlib import Path

def find_audio(base):
    d = Path("static/audio")
    for ext in (".ogg", ".mp3", ".wav"):
        p = d / f"{base}{ext}"
        if p.exists():
            return p
    return None

st.subheader("🎧 Podloga (loop)")

c1, c2 = st.columns([2,3])
with c1:
    loop_amb  = st.selectbox("Ambijent podloge", ["Šuma","Reka","Kiša"], key="loop_amb")
    loop_tone = st.selectbox("Ton podloge", ["432Hz","528Hz"], key="loop_tone")
with c2:
    loop_mute = st.checkbox("Mute", value=False, key="loop_mute")
    loop_vol  = st.slider("Jačina podloge", 0, 100, 35, key="loop_vol")

tone_file = find_audio("432hz" if st.session_state["loop_tone"]=="432Hz" else "528hz")
amb_key   = {"Šuma":"forest", "Reka":"river", "Kiša":"rain"}[st.session_state["loop_amb"]]
amb_file  = find_audio(amb_key)

if tone_file or amb_file:
    html = f"""
    <audio id="loopTone" src="{tone_file.as_posix() if tone_file else ''}" loop autoplay></audio>
    <audio id="loopAmb"  src="{amb_file.as_posix()  if amb_file  else ''}" loop autoplay></audio>
    <script>
      const vol  = {st.session_state["loop_vol"]}/100.0;
      const mute = {str(st.session_state["loop_mute"]).lower()};
      ['loopTone','loopAmb'].forEach(id => {{
        const a = document.getElementById(id);
        if (!a) return;
        a.volume = vol;
        a.muted  = mute;
      }});
    </script>
    """
    st.components.v1.html(html, height=0)
else:
    st.info("Dodaj fajlove u **static/audio/** (432hz / 528hz + forest/river/rain).")

