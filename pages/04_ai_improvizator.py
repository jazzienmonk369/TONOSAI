import streamlit as st

st.set_page_config(
    page_title="TONOSAI — Zvezde",         # slobodno menjaj naslov po stranici
    page_icon="static/favicon.png",
    layout="wide"
)

import streamlit as st

st.set_page_config(page_title="AI Improvizator 🎶", page_icon="🎵")

st.title("🎶 TONOSAI AI Improvizator")
st.markdown("Ovde ćeš moći da generišeš AI muzičke fraze, biraš skalu, tempo i instrument.")

# Dummy interface (test)
scale = st.selectbox("Izaberi skalu:", ["C-dur", "G-dur", "A-mol"])
tempo = st.slider("Tempo (BPM)", 60, 180, 90)

if st.button("🎼 Generiši frazu"):
    st.success("FRAZA: C – E – G – C (test primer)")