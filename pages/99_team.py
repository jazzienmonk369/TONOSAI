import streamlit as st

st.set_page_config(
    page_title="TONOSAI — Zvezde",         # slobodno menjaj naslov po stranici
    page_icon="static/favicon.png",
    layout="wide"
)

import streamlit as st

# 🌌 Stranica i stil
st.set_page_config(page_title="TONOSAI | Kosmički Tim", page_icon="🌌", layout="centered")

st.title("🌌 TONOSAI Kosmički Tim")

# 🎯 Izbor člana
clanovi = {
    "TONOS": "🎼 Vodič frekvencija i ritma – usklađuje AI i muzičke talase.",
    "Harmonia": "🧚 Vila harmonije – čuvarica balansa zvuka, boje i duše.",
    "Cosma": "🌠 Umetnica algoritama – oblikuje zvučne svetove kroz kod.",
    "Neura": "🧠 AI mozak – analizira, spaja, povezuje kosmičke podatke.",
    "Orion": "🔭 Vizuelni posmatrač – mapira pejzaže i animira duhove prostora.",
    "Chronos": "⏳ Čuvar vremena – sekvencira ritmove i tajminge u projektima.",
    "Echo": "🔊 Odjek prošlih glasova – čuva uspomene, arhive i snimke."
}

izbor = st.selectbox("🪐 Izaberi člana tima:", ["—"] + list(clanovi.keys()))

if izbor and izbor != "—":
    st.markdown(f"## {izbor}")
    st.success(clanovi[izbor])
