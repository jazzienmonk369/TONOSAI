# pages/vizija_tonosai.py
import streamlit as st
from lib.ui import lang_selector
from lib.i18n import t

st.set_page_config(page_title="Vizija TONOSAI")
lang_selector("vizija")  # ← jedinstven key: lang_vizija

st.title(t("vision.title"))            # koristi ključeve iz i18n
st.write(t("vision.lead"))

import streamlit as st
st.set_page_config(page_title="Vizija TONOSAI", page_icon="🖋", layout="centered")

st.title("🖋 Vizija TONOSAI")
st.markdown("""
TONOSAI je most između zvuka, čoveka i AI.  
Kroz jednostavne rituale i nežne alate, vraćamo se harmoniji.
""")

st.page_link("pages/02_konstelacija.py", label="↩ Nazad na Konstelacije")
