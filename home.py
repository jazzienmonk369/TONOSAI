# home.py — TONOSAI Studio (clean start)

import os, base64
from pathlib import Path
from datetime import date
import streamlit as st
from lib.i18n import t

# ── Config (uvek prvi Streamlit poziv)
st.set_page_config(page_title="TONOSAI Studio", page_icon="✨", layout="wide")
VERSION = os.getenv("TONOSAI_VERSION", "v0.1.1")

# ── Jezik (jedan widget, jedinstven key)
if "lang" not in st.session_state:
    st.session_state["lang"] = "sr"
lang = st.sidebar.selectbox(
    t("ui.lang") if "ui.lang" in t.__globals__.get("_CACHE", {}).get(st.session_state["lang"], {}) else "Language / Jezik",
    ["sr", "en"],
    index=["sr", "en"].index(st.session_state["lang"]),
    key="lang_home"
)
st.session_state["lang"] = lang

# ── Kontrole (tema + ambijent)
col_top = st.columns([2, 1, 3])
with col_top[0]:
    theme = st.selectbox("🎨 Motiv", ["Deep Space", "Aurora", "Amethyst"], index=0)
with col_top[1]:
    play = st.toggle("🔊 Ambijent", value=False)
with col_top[2]:
    vol = st.slider("Jačina", 0, 100, 65, 1, disabled=not play)

ACCENT = {"Deep Space": "#60a5fa", "Aurora": "#5eead4", "Amethyst": "#a78bfa"}[theme]

# ── Stil / pozadina / hero
st.markdown(f"""
<style>
:root {{ --accent: {ACCENT}; --bg1:#0a1328; --bg2:#081124; }}
html, body, [data-testid="stAppViewContainer"] {{
  background: radial-gradient(1200px 800px at 22% -10%, #102048, var(--bg1) 55%, var(--bg2) 80%);
}}
.tn-stars, .tn-stars:after {{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0; opacity:.25;
  background:
    radial-gradient(2px 2px at 14% 32%, rgba(255,255,255,.28) 40%, transparent 60%),
    radial-gradient(2px 2px at 76% 58%, rgba(255,255,255,.18) 40%, transparent 60%),
    radial-gradient(1.6px 1.6px at 42% 82%, rgba(255,255,255,.22) 40%, transparent 60%),
    radial-gradient(1px 1px at 88% 22%, rgba(255,255,255,.20) 40%, transparent 60%),
    radial-gradient(1.2px 1.2px at 10% 70%, rgba(255,255,255,.16) 40%, transparent 60%);
  background-repeat:no-repeat; animation: twinkle 7s ease-in-out infinite alternate;
}}
.tn-stars:after {{ opacity:.16; filter: blur(.4px); animation-duration: 10s; }}
@keyframes twinkle {{ from {{ transform: translateY(0px)}} to {{ transform: translateY(-2px)}} }}

.sky {{ position:fixed; inset:0; pointer-events:none; z-index:0; }}
.comet {{
  position:absolute; width:140px; height:2px;
  background: linear-gradient(90deg, rgba(255,255,255,0), color-mix(in oklab, var(--accent) 85%, white 15%));
  filter: drop-shadow(0 0 10px color-mix(in oklab, var(--accent) 60%, transparent));
  transform: rotate(-15deg); opacity:0; animation: shoot 6s ease-in-out infinite;
}}
.comet:after {{ content:""; position:absolute; left:0; top:-2px; width:8px; height:8px; border-radius:50%;
  background: color-mix(in oklab, var(--accent) 90%, white 10%); }}
@keyframes shoot {{
  0% {{ opacity:0; transform:translate3d(0,0,0) rotate(-15deg); }}
  6% {{ opacity:.7; }}
  50% {{ opacity:0; transform:translate3d(-420px, 220px, 0) rotate(-15deg); }}
  100% {{ opacity:0; }}
}}

.fade-in {{ animation: fade 1.0s ease-in-out both; }}
@keyframes fade {{ from {{opacity:0; transform: translateY(6px);}} to {{opacity:1; transform:none;}} }}
.tn-hero {{ position:relative; z-index:1; text-align:center; padding: 7vh 0 1vh 0; }}
.tn-title {{ font-size:clamp(34px,6vw,56px); font-weight:800; letter-spacing:.2px; margin:0 0 6px 0; }}
.tn-sub   {{ font-size:clamp(13px,2.2vw,16px); opacity:.85; }}
.tn-div   {{ height:1px; margin:18px auto 10px auto; max-width: 880px;
  background: linear-gradient(90deg, rgba(255,255,255,0) 0%, var(--accent) 15%, var(--accent) 85%, rgba(255,255,255,0) 100%);
  filter: drop-shadow(0 0 8px color-mix(in oklab, var(--accent) 45%, transparent));
}}
.tn-wrap {{ position:relative; z-index:1; max-width: 900px; margin: 8px auto 28px auto; }}
.tn-card {{ background: rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08);
           border-radius:16px; padding:18px 18px; }}
.tn-grid {{ display:grid; grid-template-columns: repeat(3, 1fr); gap:14px; margin-top:14px; }}
.tn-mini {{ background: rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.08);
           border-radius:14px; padding:14px; font-size:14px; }}

.ver-badge {{
  position:fixed; right:14px; bottom:10px; z-index:9999;
  padding:6px 10px; border-radius:999px; font-size:12px; opacity:.9;
  background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.16);
  backdrop-filter: blur(4px);
}}
</style>
<div class="tn-stars"></div>
<div class="sky">
  <div class="comet" style="top:12%; left:82%; animation-delay:2.2s;"></div>
  <div class="comet" style="top:28%; left:70%; animation-delay:8.5s;"></div>
  <div class="comet" style="top:64%; left:90%; animation-delay:14.2s;"></div>
</div>
<div class="ver-badge">{VERSION}</div>
""", unsafe_allow_html=True)

# ── Logo + naslov
IMG_PATH = "static/images/TONOSAI_Logo.png"
st.markdown('<div class="tn-hero">', unsafe_allow_html=True)
if Path(IMG_PATH).exists():
    st.image(IMG_PATH)
st.markdown('<div class="tn-div"></div>', unsafe_allow_html=True)

# ── About (i18n)
st.markdown('<div class="tn-wrap">', unsafe_allow_html=True)
st.markdown(f"""
<div class="tn-card">
  <h4>{t("home.about.title")}</h4>
  {t("home.about.lead")}
  <div class="tn-grid">
    <div class="tn-mini">{t("home.about.badge.tones")}</div>
    <div class="tn-mini">{t("home.about.badge.stars")}</div>
    <div class="tn-mini">{t("home.about.badge.ai")}</div>
  </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Ambijentalni audio
def audio_src_b64():
    primary  = Path("static/audio/ecosystem_formula_loop.ogg")
    fallback = Path("static/audio/ambient_loop.ogg")
    pick = primary if primary.exists() else (fallback if fallback.exists() else None)
    if not pick: return (None, None)
    mime = "audio/ogg" if pick.suffix.lower()==".ogg" else ("audio/mpeg" if pick.suffix.lower()==".mp3" else "audio/wav")
    b64 = base64.b64encode(pick.read_bytes()).decode("ascii")
    return (f"data:{mime};base64,{b64}", mime)

if play:
    src, mime = audio_src_b64()
    if not src:
        st.error("Dodaj static/audio/ecosystem_formula_loop.ogg (ili ambient_loop.ogg).")
    else:
        st.components.v1.html(f"""
        <div style="max-width:900px; margin:12px auto 0 auto;">
          <audio id="amb" controls autoplay loop preload="auto" style="width:100%;">
            <source src="{src}" type="{mime}">
          </audio>
        </div>
        <script>try{{document.getElementById('amb').volume={vol/100};}}catch(e){{}}</script>
        """, height=64)

# ── Brzi linkovi
c1, c2, c3 = st.columns(3)
with c1: st.page_link("pages/manifest.py", label=t("home.links.manifest"))
with c2: st.page_link("pages/showcase.py", label=t("home.links.showcase"))
with c3: st.page_link("pages/balans_2_0.py", label=t("home.links.balans20"))

# ── Poruka dana
MOTD = [
    "Sve je vibracija — uskladi ton i put se otvara.",
    "Tišina zna — pusti je da zapeva prva.",
    "Jedna nota, hiljadu zvezda.",
    "Ritam daha je metronom duše.",
    "Harmonija je most između ideje i dela.",
]
st.caption(MOTD[date.today().toordinal() % len(MOTD)])
