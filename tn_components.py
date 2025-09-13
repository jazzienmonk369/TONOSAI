# tn_components.py
import os
import streamlit as st

def render_footer(active=None):
    """Univerzalni footer sa linkovima i verzijom."""
    version = os.getenv("TONOSAI_VERSION", "v0.1.1")

    st.markdown("""
    <style>
      .tn-hr { height:1px; border:0; margin:26px 0 16px 0;
               background: linear-gradient(90deg,
                 rgba(255,255,255,0) 0%,
                 rgba(255,255,255,.22) 12%,
                 rgba(255,255,255,.22) 88%,
                 rgba(255,255,255,0) 100%); }
    </style>
    <div class="tn-hr"></div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns([1.1, 1.2, 1.0, 1.2, 1.6])
    with c1:
        st.page_link("pages/manifest.py", label=("🌠 Manifest"  + (" •" if active=="manifest" else "")))
    with c2:
        st.page_link("pages/balans_2_0.py", label=("🌿 Balans 2.0" + (" •" if active=="balans" else "")))
    with c3:
        st.page_link("pages/99_team.py", label=("👩‍🚀 Tim"       + (" •" if active=="team" else "")))
    with c4:
        st.page_link("pages/showcase.py", label=("🎬 Showcase"   + (" •" if active=="showcase" else "")))
    with c5:
        st.caption(f"version: {version} · open for everyone ✨")
