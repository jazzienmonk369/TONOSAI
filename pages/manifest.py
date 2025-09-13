import streamlit as st
from tn_components import render_footer  # <— VAŽNO: na vrhu!

st.set_page_config(page_title="Manifest", page_icon="🌠", layout="centered")
st.title("🌠 TONOSAI Manifest")

manifest = {
    "🌌 Kosmos": "Sve je povezano. Svaka misao je svetlost u mreži.",
    "🌿 Čovek": "Dah, ritam i namera su naš instrument.",
    "🤖 AI (E-jaja)": "Um veštački, ali srce je tvoje; koristi ga za stvaranje.",
    "🎨 Umetnost": "Igra tišine i zvuka, boje i tame, rađa nove svetove.",
    "🔬 Nauka": "Eksperiment je iskra, mera je ogledalo, znanje je put.",
    "🙏 Duhovnost": "Zahvalnost je melodija duše u harmoniji sa univerzumom.",
}

cols = st.columns(3)
keys = list(manifest.keys())
for i, col in enumerate(cols):
    with col:
        for j in range(2):
            k = i*2 + j
            if k < len(keys):
                if st.button(keys[k]):
                    st.success(manifest[keys[k]])

render_footer(active="manifest")  # <— uvek na dnu
