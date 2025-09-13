# pages/showcase.py
import os
from pathlib import Path
import streamlit as st
from tn_components import render_footer  # footer links + verzija

st.set_page_config(page_title="Showcase — TONOSAI", page_icon="🎬", layout="wide")
st.title("🎬 TONOSAI Showcase")
st.caption("Kratka kosmička izložba: Manifest → Balans 2.0")

with st.expander("Scenarij (3–5 min) – vodič za snimanje", expanded=False):
    st.markdown(
        """
**1. Intro (0:00–0:30)** – zvezdano nebo + logo, lagani 528Hz vibrafon.  
**2. Manifest (0:30–1:30)** – klik na zvezdu, poetska poruka + zvonce.  
**3. Balans 2.0 (1:30–2:30)** – priroda + 432/528Hz ton.  
**4. Završnica (2:30–3:00)** – poziv zajednici, fade-out.
"""
    )

# --- Demo flow
c1, c2 = st.columns(2)
with c1:
    st.subheader("🌠 Manifest (demo)")
    st.write("Klikni zvezdu da otvoriš poruku.")
    ca, cb = st.columns(2)
    with ca:
        if st.button("⭐ Kosmos"):
            st.success("Sve je povezano. Svaka misao je svetlost u mreži.")
    with cb:
        if st.button("🌿 Čovek"):
            st.success("Dah, ritam i namera su naš instrument.")

with c2:
    st.subheader("🌿 Balans 2.0 (demo)")
    amb = st.selectbox("Ambijent", ["Šuma", "Reka", "Kiša"])
    ton = st.radio("Ton", ["432Hz", "528Hz"], horizontal=True)
    st.write(f"Preporuka: **{amb} + {ton}** — 5–10 minuta, disanje 4–4–6.")

st.divider()
st.markdown("**Snimanje videa?** Otvori OBS → prikaži uvod, klikni 1–2 zvezde u Manifestu → prikaži Balans 2.0 → završna poruka.")

# --- Audio preview
AUDIO_DIR = Path("static/audio")
tones = {"432Hz": AUDIO_DIR / "432hz.ogg", "528Hz": AUDIO_DIR / "528hz.ogg"}
ambients = {"Šuma": AUDIO_DIR / "forest.ogg", "Reka": AUDIO_DIR / "river.ogg", "Kiša": AUDIO_DIR / "rain.ogg"}

st.subheader("🔊 Audio preview")
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

# --- Podloga (loop)
def find_audio(base: str) -> Path | None:
    for ext in (".ogg", ".mp3", ".wav"):
        p = AUDIO_DIR / f"{base}{ext}"
        if p.exists():
            return p
    return None

st.subheader("🎧 Podloga (loop)")
c1, c2 = st.columns([2, 3])
with c1:
    loop_amb = st.selectbox("Ambijent podloge", ["Šuma", "Reka", "Kiša"], key="loop_amb")
    loop_tone = st.selectbox("Ton podloge", ["432Hz", "528Hz"], key="loop_tone")
with c2:
    loop_mute = st.checkbox("Mute", value=False, key="loop_mute")
    loop_vol = st.slider("Jačina podloge", 0, 100, 35, key="loop_vol")

tone_file = find_audio("432hz" if st.session_state["loop_tone"] == "432Hz" else "528hz")
amb_file = find_audio({"Šuma": "forest", "Reka": "river", "Kiša": "rain"}[st.session_state["loop_amb"]])

if tone_file or amb_file:
    html = f"""
    <audio id="loopTone" src="{tone_file.as_posix() if tone_file else ''}" loop autoplay></audio>
    <audio id="loopAmb"  src="{amb_file.as_posix()  if amb_file  else ''}" loop autoplay></audio>
    <script>
      const vol  = {st.session_state["loop_vol"]} / 100.0;
      const mute = {str(st.session_state["loop_mute"]).lower()};
      ['loopTone','loopAmb'].forEach(id => {{
        const a = document.getElementById(id);
        if (!a) return;
        a.volume = vol;
        a.muted  = mute;
      }});
    </script>
    """
    # ⬇️ OVO JE NEDOSTAJALO
    st.components.v1.html(html, height=0)
else:
    st.info("Dodaj fajlove u **static/audio/** (432hz / 528hz + forest/river/rain).")

render_footer(active="showcase")
