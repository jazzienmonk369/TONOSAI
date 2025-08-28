# boot.py
from lib.theme import inject_css
import streamlit as st

def footer():
    st.markdown(
        """
        <div style="margin-top:2rem;opacity:.7;font-size:0.9rem">
          Made with ❤️ by TONOSAI · 
          <a href="https://github.com/jazzienmonk369/TONOSAI" target="_blank">GitHub</a> · 
          <a href="https://github.com/jazzienmonk369/TONOSAI/issues" target="_blank">Issues</a> · 
          <a href="mailto:tonosai.studio@gmail.com">tonosai.studio@gmail.com</a>
        </div>""",
        unsafe_allow_html=True,
    )

# auto-poziv iz boot-a:
from lib.theme import inject_css
inject_css()
footer()

import boot


# side-effect: čim se uveze, ubaci CSS
inject_css()
