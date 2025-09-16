import streamlit as st
import boot
# lib/ui.py
import streamlit as st
from lib.i18n import t

def lang_selector(page_id: str = "page"):
    """Sidebar jezički preklopnik sa unikatnim ključem po stranici."""
    if "lang" not in st.session_state:
        st.session_state["lang"] = "sr"
    key = f"lang_{page_id}"          # ← garantuje unikatan key po stranici
    current = st.session_state["lang"]
    choice = st.sidebar.selectbox(
        t("ui.lang") if callable(t) else "Language / Jezik",
        ["sr", "en"],
        index=["sr","en"].index(current),
        key=key
    )
    st.session_state["lang"] = choice



REPO = "jazzienmonk369/TONOSAI"
APP_URL = "https://tonosai.streamlit.app"

def get_version():
    try:
        from tonosai_version import __version__
        return __version__
    except Exception:
        return "dev"

def header_badges():
    st.markdown(
        f"""
        <div style="display:flex;gap:10px;align-items:center;margin:.25rem 0 1rem 0;">
          <a href="https://github.com/{REPO}" target="_blank" rel="noopener">
            <img alt="GitHub" src="https://img.shields.io/badge/GitHub-repo-181717?logo=github&logoColor=white">
          </a>
          <a href="https://github.com/{REPO}/stargazers" target="_blank" rel="noopener">
            <img alt="Stars" src="https://img.shields.io/github/stars/{REPO}?style=social">
          </a>
          <a href="https://github.com/{REPO}/forks" target="_blank" rel="noopener">
            <img alt="Forks" src="https://img.shields.io/github/forks/{REPO}?style=social">
          </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

def footer():
    st.markdown(
        f"""
        <hr style="opacity:.2;margin-top:2rem;margin-bottom:.5rem;">
        <div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;font-size:0.92rem;opacity:.9">
          <span>Made with ❤️ by TONOSAI</span>
          <span>•</span>
          <a href="https://github.com/{REPO}/issues/new?title=%5Bbug%5D%3A+&labels=bug&body=Steps+to+reproduce%3A%0A-+...%0AExpected%3A%0AActual%3A%0A" target="_blank" rel="noopener">Report a bug</a>
          <span>·</span>
          <a href="https://github.com/{REPO}/issues/new?title=Idea%3A+&labels=enhancement&body=What's+the+idea%3F" target="_blank" rel="noopener">Request a feature</a>
          <span>·</span>
          <a href="https://github.com/{REPO}" target="_blank" rel="noopener">Repo</a>
          <span style="margin-left:auto;">v{get_version()}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
