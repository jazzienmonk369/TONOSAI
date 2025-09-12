import streamlit as st
from pathlib import Path

st.subheader("🧚‍♀️ Harmonia — auto-preporuka")
feel = st.selectbox(
    "Kako se osećaš?",
    ["Umoran/niska energija", "Napet/stres", "Fokus/koncentracija", "Mirno/opušteno"]
)

# Mapa osećaj → (ambijent, ton)
SUGGEST = {
    "Umoran/niska energija": ("Reka", "432Hz"),
    "Napet/stres":           ("Kiša", "528Hz"),
    "Fokus/koncentracija":   ("Šuma", "432Hz"),
    "Mirno/opušteno":        ("Šuma", "528Hz"),
}

# Mala pomoćna: nađi fajl bilo koje ekstenzije
def find_audio(base):
    audio_dir = Path("static/audio")
    for ext in (".ogg", ".mp3", ".wav"):
        p = audio_dir / f"{base}{ext}"
        if p.exists():
            return p
    return None

if st.button("✨ Primeni preporuku"):
    amb_sug, ton_sug = SUGGEST[feel]
    # upiši u session_state tvoje postojeće kontrole (ako se zovu 'Ambijent' i 'Ton')
    st.session_state["Ambijent"] = amb_sug
    st.session_state["Ton"] = ton_sug
    st.success(f"Predlog: **{amb_sug} + {ton_sug}** primenjen.")

    # opciono — odmah pusti ton i ambijent ako fajlovi postoje
    tone_file = find_audio("432hz" if ton_sug=="432Hz" else "528hz")
    amb_key = {"Šuma":"forest", "Reka":"river", "Kiša":"rain"}[amb_sug]
    amb_file = find_audio(amb_key)

    if tone_file: st.audio(str(tone_file))
    if amb_file:  st.audio(str(amb_file))

# Ako želiš da UI kontrole koriste session_state:
# amb = st.selectbox("Ambijent", ["Šuma", "Reka", "Kiša"], key="Ambijent")
# ton = st.radio("Ton", ["432Hz", "528Hz"], key="Ton", horizontal=True)
# --- Preseti: sačuvaj/učitaj ---
import json
from pathlib import Path

PRESETS_PATH = Path("data/presets.json")
PRESETS_PATH.parent.mkdir(exist_ok=True)

def load_presets():
    if PRESETS_PATH.exists():
        return json.loads(PRESETS_PATH.read_text(encoding="utf-8"))
    return {}

def save_presets(p):
    PRESETS_PATH.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")

st.subheader("💾 Preseti")
presets = load_presets()

col_s, col_l = st.columns([1,1])

with col_s:
    name_new = st.text_input("Ime novog preseta", value="Moj preset")
    if st.button("💾 Sačuvaj preset"):
        presets[name_new] = {"amb": st.session_state["Ambijent"], "ton": st.session_state["Ton"]}
        save_presets(presets)
        st.success(f"Sačuvan preset: **{name_new}**")

with col_l:
    choices = ["—"] + list(presets.keys())
    pick = st.selectbox("Učitaj preset", choices, index=0)
    if st.button("📂 Učitaj") and pick != "—":
        st.session_state["Ambijent"] = presets[pick]["amb"]
        st.session_state["Ton"] = presets[pick]["ton"]
        st.success(f"Učitan preset: **{pick}**")



st.set_page_config(page_title="Balans 2.0", page_icon="🌿", layout="centered")
st.title("🌿 TONOSAI Balans 2.0")

amb = st.selectbox("Ambijent", ["Šuma", "Reka", "Kiša"])
ton = st.radio("Ton", ["432Hz", "528Hz"])
st.write(f"Preporuka: **{amb} + {ton}** — 5–10 min, disanje 4–4–6.")
st.info("Dodaj audio fajlove u static/audio pa ćemo uključiti i realno puštanje zvuka.")
