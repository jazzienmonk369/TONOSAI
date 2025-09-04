# home.py — TONOSAI · Home (v3.1: motivi + komete + audio + MOTD + badge)

from __future__ import annotations
from pathlib import Path
import base64, os
from datetime import date
import streamlit as st

st.set_page_config(page_title="TONOSAI", page_icon="🌌", layout="wide")

# ——— Kontrole ———
col_top = st.columns([2, 1, 3])
with col_top[0]:
    theme = st.selectbox("🎨 Motiv", ["Deep Space", "Aurora", "Amethyst"], index=0)
with col_top[1]:
    play = st.toggle("🔊 Ambijent", value=False)
with col_top[2]:
    vol = st.slider("Jačina", 0, 100, 65, 1, disabled=not play)

ACCENT = {"Deep Space": "#60a5fa", "Aurora": "#5eead4", "Amethyst": "#a78bfa"}[theme]
VERSION = os.getenv("TONOSAI_VERSION", "v0.1.1")

# ——— Stil ———
st.markdown(f"""
<style>
:root {{ --accent: {ACCENT}; --bg1:#0a1328; --bg2:#081124; }}
.stApp {{ background: radial-gradient(1200px 800px at 22% -10%, #102048, var(--bg1) 55%, var(--bg2) 80%) !important; }}

/* zvezde */
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

/* hero */
.tn-hero {{ position:relative; z-index:1; text-align:center; padding: 10vh 0 1vh 0; }}
.tn-title {{ font-size:clamp(34px,6vw,56px); font-weight:800; letter-spacing:.2px; margin:0 0 6px 0; }}
.tn-sub   {{ font-size:clamp(13px,2.2vw,16px); opacity:.85; }}

/* divider */
.tn-div {{ height:1px; margin:18px auto 10px auto; max-width: 880px;
  background: linear-gradient(90deg, rgba(255,255,255,0) 0%, var(--accent) 15%, var(--accent) 85%, rgba(255,255,255,0) 100%);
  filter: drop-shadow(0 0 8px color-mix(in oklab, var(--accent) 45%, transparent));
}}

/* about */
.tn-wrap {{ position:relative; z-index:1; max-width: 900px; margin: 8px auto 28px auto; }}
.tn-card {{ background: rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08);
           border-radius:16px; padding:18px 18px; }}
.tn-grid {{ display:grid; grid-template-columns: repeat(3, 1fr); gap:14px; margin-top:14px; }}
.tn-mini {{ background: rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.08);
           border-radius:14px; padding:14px; font-size:14px; }}

/* komete */
.sky {{ position:fixed; inset:0; pointer-events:none; z-index:0; }}
.comet {{
  position:absolute; width:140px; height:2px;
  background: linear-gradient(90deg, rgba(255,255,255,0), color-mix(in oklab, var(--accent) 85%, white 15%));
  filter: drop-shadow(0 0 10px color-mix(in oklab, var(--accent) 60%, transparent));
  transform: rotate(-15deg); opacity:.0; animation: shoot 6s ease-in-out infinite;
}}
.comet:after {{ content:""; position:absolute; left:0; top:-2px; width:8px; height:8px; border-radius:50%;
  background: color-mix(in oklab, var(--accent) 90%, white 10%); }}
@keyframes shoot {{
  0% {{ opacity:0; transform:translate3d(0,0,0) rotate(-15deg); }}
  6% {{ opacity:.7; }}
  50% {{ opacity:.0; transform:translate3d(-420px, 220px, 0) rotate(-15deg); }}
  100% {{ opacity:0; }}
}}

/* audio */
.tn-audio {{ max-width:900px; margin:12px auto 0 auto; }}

/* version badge */
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

# ——— HERO ———
st.markdown("""
<div class="tn-hero">
  <div class="tn-title">Zvezde odzvanjaju… Harmonia te zove.</div>
  <div class="tn-sub">TONOSAI — zvuk · čovek · AI</div>
</div>
<div class="tn-div"></div>
""", unsafe_allow_html=True)

# ——— Ambijent (ecosystem_formula_loop.ogg → fallback ambient_loop.ogg) ———
def audio_src_b64() -> tuple[str, str] | tuple[None, None]:
    primary  = Path("static/audio/ecosystem_formula_loop.ogg")
    fallback = Path("static/audio/ambient_loop.ogg")
    pick = primary if primary.exists() else (fallback if fallback.exists() else None)
    if pick is None:
        return (None, None)
    mime = "audio/ogg" if pick.suffix.lower()==".ogg" else ("audio/mpeg" if pick.suffix.lower()==".mp3" else "audio/wav")
    b64 = base64.b64encode(pick.read_bytes()).decode("ascii")
    return (f"data:{mime};base64,{b64}", mime)

if play:
    src, mime = audio_src_b64()
    if not src:
        st.error("Dodaj **static/audio/ecosystem_formula_loop.ogg** (ili `ambient_loop.ogg`).")
    else:
        # VAŽNO: sve uvučeno unutar else:
        st.components.v1.html(f"""
        <div class="tn-audio">
          <audio id="amb" controls autoplay loop preload="auto" style="width:100%;">
            <source src="{src}" type="{mime}">
          </audio>
        </div>
        <script>
          try {{
            const a = document.getElementById('amb');
            a.volume = {vol/100};
          }} catch (e) {{}}
        </script>
        """, height=60)



# ——— About ———
with st.container():
    st.markdown('<div class="tn-wrap">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="tn-card">
          <h4>✨ O TONOSAI</h4>
          TONOSAI je malo igralište gde se spajaju <b>zvuk</b>, <b>kosmos</b> i <b>AI</b>.
          Sve je minimalističko, nežno i estetski. Moduli su u levom meniju — ovo je ulaz u atmosferu.
          <div class="tn-grid">
            <div class="tn-mini">🎵 432 / 528 / 639 Hz · pulse · binaural</div>
            <div class="tn-mini">⭐ interaktivne zvezde i konstelacije</div>
            <div class="tn-mini">🧠 AI improvizacije & ideje</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ——— Poruka dana ———
MOTD = [
    "Sve je vibracija — uskladi ton i put se otvara.",
    "Tišina zna — pusti je da zapeva prva.",
    "Jedna nota, hiljadu zvezda.",
    "Ritam daha je metronom duše.",
    "Harmonija je most između ideje i dela.",
]
idx = date.today().toordinal() % len(MOTD)
st.caption(MOTD[idx])
