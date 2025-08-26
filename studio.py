import streamlit as st

st.set_page_config(
    page_title="TONOSAI Studio",
    page_icon="static/favicon.png",
    layout="wide",
)

# app.py — TONOSAI Studio (home)
import streamlit as st
st.set_page_config(page_title="TONOSAI Studio", page_icon="🎛️", layout="wide")

st.title("🎛️ TONOSAI Studio")
st.caption("Eksperimentalni audio-vizuelni alati. Izaberi modul ispod.")

st.markdown("### ⭐ Kosmičke Zvezde")
st.write("Interaktivno nebo: klik na zvezde = ton, konstelacije = akordi, snimanje u .wav.")

cols = st.columns(3)
open_ok = cols[0].button("Otvori ⭐ Kosmičke Zvezde")

if open_ok:
    # Pokušaj direktnog prelaza (novije verzije Streamlita)
    try:
        st.switch_page("pages/stars.py")
    except Exception:
        st.info("Ako se stranice ne prikazuju automatski, koristi **Pages** meni sa leve strane (multi-page).")

st.divider()
st.markdown(
    """
**Kako pokrenuti lokalno**
1. Otvori terminal u folderu projekta  
2. `pip install -r requirements.txt`  
3. `streamlit run app.py`
"""
)
