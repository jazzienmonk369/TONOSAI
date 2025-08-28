import streamlit as st

st.set_page_config(
    page_title="TONOSAI Studio",
    page_icon="static/favicon.png",
    layout="wide",
)
st.markdown(
    """
    <style>
      .topbar {display:flex; gap:1rem; align-items:center; opacity:.9}
      .topbar a {text-decoration:none; padding:.35rem .6rem; border-radius:.6rem; 
                 background:#0e1625; border:1px solid #22324d; font-size:.9rem}
    </style>
    <div class="topbar">
      <a href="https://github.com/jazzienmonk369/TONOSAI" target="_blank">⭐ GitHub</a>
      <a href="#" onclick="navigator.clipboard.writeText(window.location.href); 
               alert('Link kopiran!'); return false;">🔗 Copy link</a>
    </div>
    """,
    unsafe_allow_html=True,
)


st.subheader("🚀 Brzi start")
c1, c2, c3 = st.columns(3)
st.page_link("pages/01_stars.py",          label="⭐ Kosmičke Zvezde")
st.page_link("pages/02_konstelacija.py",   label="🔭 Konstelacije")   # <-- ispravno
st.page_link("pages/03_kalkulator.py",     label="🧮 Kalkulator")
st.page_link("pages/04_ai_improvizator.py",label="🎹 AI Improvizator")
st.page_link("pages/05_game.py",           label="🎮 Igra (Collector)")
st.page_link("pages/06_guardian.py",       label="🛡️ Čuvar")
st.page_link("pages/99_team.py",           label="👥 Tim")


# app.py — TONOSAI Studio (home)
import streamlit as st
import streamlit as st

st.set_page_config(
    page_title="TONOSAI Studio — kosmičke zvezde & zvuk",
    page_icon="✨",          # ili "static/favicon.png" kad dodaš sličicu
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/jazzienmonk369/TONOSAI/issues",
        "Report a bug": "https://github.com/jazzienmonk369/TONOSAI/issues/new",
        "About": "TONOSAI Studio — eksperimenti sa harmonijom, kosmičkim vizualima i healing vibrom.",
    },
)

# Sakrij default meni i footer (čistiji izlog)
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="TONOSAI Studio", page_icon="🎛️", layout="wide")
st.title("🎛️ TONOSAI Studio")
st.caption("Eksperimentalni audio-vizuelni alati. Izaberi modul ispod.")

# Helper koji radi i na starijim verzijama Streamlita (ako nema page_link)
def link_or_button(page: str, label: str, icon: str = None):
    if hasattr(st, "page_link"):
        st.page_link(page, label=label, icon=icon)
    else:
        if st.button(f"{icon or ''} {label}".strip()):
            try:
                st.switch_page(page)
            except Exception:
                st.info("Ako se stranice ne otvore automatski, koristi **Pages** meni sa leve strane.")

cols = st.columns(3)

with cols[0]:
    st.subheader("⭐ Kosmičke Zvezde")
    st.write("Interaktivno nebo: klik na zvezde = ton, konstelacije = akordi, snimanje.")
    link_or_button("pages/01_stars.py", "Otvori", "⭐")

with cols[1]:
    st.subheader("🌌 Konstelacije")
    st.write("Preset oblici, varijacije i boje.")
    link_or_button("pages/02_konstelacija.py", "Otvori", "🌌")

with cols[2]:
    st.subheader("🧮 Kalkulator")
    st.write("Mali muzički/kognitivni kalkulator.")
    link_or_button("pages/03_kalkulator.py", "Otvori", "🧮")

with cols[0]:
    st.subheader("🎮 Igra")
    st.write("Zvezdani sakupljač sa tonovima skale.")
    link_or_button("pages/05_game.py", "Otvori", "🕹️")
    st.markdown("### ✨ Čuvar konstelacije")
st.write("Boss (redosled tačaka) + starburst + healing dah HUD.")
st.page_link("pages/06_guardian.py", label="Otvori ✨ Čuvar", icon="✨")


with cols[1]:
    st.subheader("🎼 AI Improvizator")
    st.write("Generisanje muzičkih fraza po skali/tempu.")
    link_or_button("pages/04_ai_improvizator.py", "Otvori", "🎼")

with cols[2]:
    st.subheader("👥 Tim")
    st.write("O tvoračkom timu.")
    link_or_button("pages/99_team.py", "Otvori", "👥")

st.divider()
st.markdown(
    """
**Kako pokrenuti lokalno**
1. Otvori terminal u folderu projekta  
2. `pip install -r requirements.txt`  
3. `streamlit run app.py`
"""
)
