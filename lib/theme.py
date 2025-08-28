# lib/theme.py
import streamlit as st
from pathlib import Path
import boot


_DEFAULT_CSS = """
/* blagi kosmički gradient preko cele pozadine */
div[data-testid="stAppViewContainer"]{
  background: radial-gradient(1200px 600px at 18% 10%, #0f1c2e 0%, #0a1526 40%, #071021 100%) fixed;
}
/* mekani dugmići */
.stButton>button,.stDownloadButton>button{
  border-radius:12px;padding:.5rem 1rem;
}
/* malo naglašen slider “thumb” */
[data-baseweb="slider"] [role="slider"]{
  background-color:#FFD773 !important;
}
"""

def inject_css():
    """Učita static/style.css ako postoji; u suprotnom sipa lep default CSS."""
    css_path = Path("static/style.css")
    css = css_path.read_text(encoding="utf-8") if css_path.exists() else _DEFAULT_CSS
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
