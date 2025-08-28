import streamlit as st
import boot


st.set_page_config(
    page_title="TONOSAI Studio",
    page_icon="static/favicon.png",
    layout="wide",
)
from lib.ui import header_badges, footer

header_badges()
footer()

