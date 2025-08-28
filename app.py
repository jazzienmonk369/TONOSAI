import streamlit as st
import boot


st.set_page_config(
    page_title="TONOSAI Studio",
    page_icon="static/favicon.png",
    layout="wide",
)
from lib.ui import header_badges, footer

header_badges()

# --- GitHub badges (fixed, top-right) ---
st.markdown("""
<style>
#tonosai-badges {
  position: fixed;
  top: 12px; right: 12px;
  z-index: 10000;
}
#tonosai-badges img { vertical-align: middle; }
#tonosai-badges a { margin-left: 6px; }
@media (max-width: 900px) {
  #tonosai-badges { top: 56px; }  /* malo niže kad je sidebar otvoren/usko */
}
</style>
<div id="tonosai-badges">
  <a href="https://github.com/jazzienmonk369/TONOSAI" target="_blank" title="Star TONOSAI">
    <img src="https://img.shields.io/github/stars/jazzienmonk369/TONOSAI?label=Stars&style=social" />
  </a>
  <a href="https://github.com/jazzienmonk369/TONOSAI/fork" target="_blank" title="Fork TONOSAI">
    <img src="https://img.shields.io/github/forks/jazzienmonk369/TONOSAI?label=Forks&style=social" />
  </a>
  <a href="https://github.com/jazzienmonk369/TONOSAI/issues" target="_blank" title="Open issues">
    <img src="https://img.shields.io/github/issues/jazzienmonk369/TONOSAI?label=Issues" />
  </a>
</div>
""", unsafe_allow_html=True)

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
import streamlit as st

with st.expander("ℹ️ About TONOSAI"):
    st.markdown("""
**TONOSAI Studio** je eksperimentalni AI sandbox za muziku, kod i harmoniju.
Fokus je na igri sa zvukom i vizuelnim obrascima: konstelacije, improvizacije, mini alati i prototipovi.

**Moduli:**
- Kosmičke Zvezde – interaktivno nebo (klik = ton, akordi, snimanje)
- Konstelacije – preseti, boja/rasipanje/seed (generativna “zvezdana genetika”)
- AI Improvizator – fraze po skali/tempu, export u WAV
- Kalkulator – mali muzičko/kognitivni alatić
- Igra i Guardian – eksperimentalni modovi

**Napomena:** app svira; preporučujemo slušalice i tiši volume.
**Repo:** https://github.com/jazzienmonk369/TONOSAI
    """)


# Sakrij default meni i footer (čistiji izlog)
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="TONOSAI Studio", page_icon="🎛️", layout="wide")
# --- GitHub Star badge (float/fixed gore levo) ---
st.markdown("""
<style>
#tonosai-star {
  position: fixed;
  top: 12px; left: 12px;
  z-index: 1000;
}
</style>
<div id="tonosai-star">
  <a href="https://github.com/jazzienmonk369/TONOSAI" target="_blank" title="Star TONOSAI on GitHub">
    <img src="https://img.shields.io/github/stars/jazzienmonk369/TONOSAI?label=Star%20repo&style=social" />
  </a>
</div>
""", unsafe_allow_html=True)

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
st.markdown("---")
st.markdown(
    """
**📝 Feedback / Report a bug:**  
- Otvori [GitHub Issue](https://github.com/jazzienmonk369/TONOSAI/issues/new?title=%5Bbug%5D%3A+&body=Kratan+opis+problema...%0A%0AKoraci+za+reprodukciju%3A%0A1.%0A2.%0A3.%0A%0AOcekivano+ponasanje%3A%0A%0AOkruzenje%3A+Browser+%2F+OS%3F%0A)  
- Ili pošalji mail: <a href="mailto:jazzienmonk369@gmail.com">jazzienmonk369@gmail.com</a>
    """,
    unsafe_allow_html=True,
)
st.markdown("""
<style>
/* blagi kosmički gradient */
div[data-testid="stAppViewContainer"]{
  background: radial-gradient(1200px 600px at 18% 10%, #0f1c2e 0%, #0a1526 40%, #071021 100%) fixed;
}
/* dugmići malo mekši */
.stButton>button, .stDownloadButton>button{
  border-radius:12px; padding:.5rem 1rem;
}
/* slider akcenat */
[data-baseweb="slider"] [role="slider"]{ background-color:#FFD773 !important; }
</style>
""", unsafe_allow_html=True)

footer()


