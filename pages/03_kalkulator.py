import streamlit as st

st.set_page_config(
    page_title="TONOSAI — Zvezde",         # slobodno menjaj naslov po stranici
    page_icon="static/favicon.png",
    layout="wide"
)

import streamlit as st

st.set_page_config(page_title="TONOSAI • Vila Harmonia Kalkulator", page_icon="🎼", layout="centered")

# 🌟 Naslov i uvod
st.title("🎼 TONOSAI • Vila Harmonia – Kalkulator Kreativnog Paketa")
st.markdown("""
Dobrodošao, Kosmički Putniče! 🌌  
Ja sam **vila Harmonia**, tvoj vodič kroz zvučne svetove i kreativne izbore.  
Odaberi sve što ti duša poželi i kreiraj svoju **zvučnu galaksiju**. ✨🎶
""")

# 🎛️ Usluge sa cenama
usluge = {
    "🎼 Ambijentalna muzika (528 Hz)": 200,
    "🎧 AI generator muzičkih fraza": 300,
    "🎙️ Glasovna naracija (vila Harmonia)": 150,
    "🌌 Parallax i fade-in efekti": 250,
    "🧘 Paket za meditaciju (3 sesije)": 400,
    "🎮 Zvuk za video igre (pozadine + efekti)": 500,
    "📦 Kompletna saradnja (TONOSAI magija)": 1000
}

# 📋 Prikaz izbora
odabrane = []
ukupna_cena = 0

st.markdown("## ✨ Odaberi elemente svog paketa:")

for naziv, cena in usluge.items():
    if st.checkbox(f"{naziv} – {cena} €"):
        odabrane.append(naziv)
        ukupna_cena += cena

# 🌈 Rezultat
st.markdown("---")
st.markdown("## 📦 Tvoj izbor:")
if odabrane:
    for o in odabrane:
        st.write(f"- {o}")
    st.success(f"💰 Ukupna cena tvog paketa: {ukupna_cena} €")
else:
    st.info("Još uvek nisi ništa izabrao. Vila Harmonia čeka tvoju inspiraciju...")

# 🎇 Zaključak
st.markdown("---")
st.caption("TONOSAI Studio • Spoj AI-ja, zvuka i umetnosti. Uvek vođeni Harmonijom. 🌌🎶")