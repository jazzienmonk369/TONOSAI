import streamlit as st
import boot


st.set_page_config(
    page_title="TONOSAI Studio",
    page_icon="static/favicon.png",
    layout="wide",
)
from lib.ui import header_badges, footer

header_badges()


import streamlit as st

def prikazi_loop_player():
    st.subheader("🔁 Loop Player")
    st.write("Ovde ćeš moći da puštaš loop-ove i eksperimentišeš sa ritmovima... 🥁")
    footer()
