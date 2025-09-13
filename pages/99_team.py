# pages/99_team.py
import streamlit as st
from pathlib import Path
from tn_components import render_footer

st.set_page_config(page_title="TONOSAI — Tim", page_icon="👩‍🚀", layout="centered")
st.title("🪐 TONOSAI Kosmički Tim")

# --- CSS (značkice/karte) ---
st.markdown("""
<style>
.badges { display:flex; gap:8px; margin:4px 0 14px 0; }
.badge  { padding:4px 8px; font-size:12px; border-radius:999px;
          background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.16);
          backdrop-filter: blur(4px);
          box-shadow: 0 0 0 1px rgba(255,255,255,.02), 0 0 10px rgba(96,165,250,.10); }

.card   { background: rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08);
          border-radius:16px; padding:16px; }
.avatar { border-radius:14px; border:1px solid rgba(255,255,255,.12); }
.tags   { display:flex; gap:6px; flex-wrap:wrap; margin-top:8px; }
.tag    { font-size:11px; padding:2px 8px; border-radius:999px;
          background: rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.12); }
</style>
""", unsafe_allow_html=True)

# Bedževi: Kosmos · Zvuk · Čovek · AI
st.markdown(
    '<div class="badges">'
    '<div class="badge">🌌 Kosmos</div>'
    '<div class="badge">🎵 Zvuk</div>'
    '<div class="badge">🧑 Čovek</div>'
    '<div class="badge">🤖 AI</div>'
    '</div>',
    unsafe_allow_html=True
)

TEAM_DIR = Path("static/images/team")  # ili "static/images" ako tu držiš png-ove

TEAM = {
    "Astra":    {"img": TEAM_DIR / "astra.png",    "bio": "Čuvar konstelacija i vizuelne magije.", "tags": ["konstelacije","dizajn","svetlo"], "emoji": "✨"},
    "Cosma":    {"img": TEAM_DIR / "cosma.png",    "bio": "Navigator zvezdanih ideja.",             "tags": ["vizija","narativ","zvezde"],     "emoji": "🛰️"},
    "Harmonia": {"img": TEAM_DIR / "harmonia.png", "bio": "Vila koja pomaže da nađeš frekvencu.",   "tags": ["432Hz","528Hz","vođenje"],       "emoji": "🧚‍♀️"},
}

name = st.selectbox("Izaberi člana tima", list(TEAM.keys()))
member = TEAM[name]
img_path = member["img"]
fallback = Path("static/images/tonosai_logo.png")  # fallback ako nema avatara

st.markdown('<div class="card">', unsafe_allow_html=True)
# Brzi linkovi ka relevantnim modulima
LINKS = {
    "Cosma":    [("🌠 Manifest", "pages/manifest.py"),
                 ("🎬 Showcase", "pages/showcase.py")],
    "Harmonia": [("🌿 Balans 2.0", "pages/balans_2_0.py"),
                 ("🎬 Showcase", "pages/showcase.py")],
    "Astra":    [("✨ Konstelacija", "pages/02_konstelacija.py"),
                 ("🌠 Manifest", "pages/manifest.py")],
}

st.write("")
st.caption("Brzi ulazi")
cols = st.columns(len(LINKS[ name ]))
for i, (label, target) in enumerate(LINKS[name]):
    with cols[i]:
        st.page_link(target, label=label)


if img_path.exists():
    st.image(str(img_path), width=220, caption=name)
elif fallback.exists():
    st.image(str(fallback), width=220, caption="(placeholder)")
    st.warning(f"Nedostaje slika: {img_path.as_posix()}")
else:
    st.warning(f"Nedostaje slika: {img_path.as_posix()}")

st.subheader(f"{member['emoji']} {name}")
st.write(member["bio"])
st.markdown('<div class="tags">' + "".join(f'<div class="tag">{t}</div>' for t in member["tags"]) + '</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


TEAM_DIR = Path("static/images/team")
TEAM = {
    "Cosma":     {"img": TEAM_DIR / "cosma.png",     "bio": "Navigator zvezdanih ideja.",                 "tags": ["vizija", "narativ", "zvezde"], "emoji": "🛰️"},
    "Harmonia":  {"img": TEAM_DIR / "harmonia.png",  "bio": "Vila koja pomaže da nađeš frekvencu.",      "tags": ["432Hz", "528Hz", "vođenje"],   "emoji": "🧚‍♀️"},
    "Astra":     {"img": TEAM_DIR / "astra.png",     "bio": "Čuvar konstelacija i vizuelne magije.",      "tags": ["konstelacije", "dizajn", "svetlo"], "emoji": "✨"},
}

name = st.selectbox("Izaberi člana tima", list(TEAM.keys()))
member = TEAM[name]
img_path = member["img"]
fallback = Path("static/images/TONOSAI_Logo.png")

st.markdown('<div class="card">', unsafe_allow_html=True)

# Avatar sa fallback-om
if img_path.exists():
    st.image(str(img_path), width=220, caption=name, output_format="PNG")
elif fallback.exists():
    st.image(str(fallback), width=220, caption="(placeholder)", output_format="PNG")
    st.warning(f"Nedostaje slika: {img_path.as_posix()}")
else:
    st.warning(f"Nedostaje slika: {img_path.as_posix()}")

# Bio + tagovi
st.subheader(f"{member['emoji']} {name}")
st.write(member["bio"])
st.markdown('<div class="tags">' + "".join(f'<div class="tag">{t}</div>' for t in member["tags"]) + "</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
from tn_components import render_footer
render_footer(active="team")

