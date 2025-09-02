import streamlit as st
from streamlit.components.v1 import html as _html

st.set_page_config(page_title="AI Improvizator", page_icon="🎛", layout="wide")

st.title("🎛 AI Improvizator")
st.write("Interaktivni jam: čovek + AI (ovde demo) komponuju u trenutku. Klikni padove, uključi ambijent, igraj se sa jačinom.")

# link nazad
st.page_link("vizija_tonosai.py", label="← Nazad na viziju", icon="↩️")

# UI
colA, colB = st.columns([1,2], gap="large")
with colA:
    amb_on  = st.toggle("🔊 Ambijent (loop)", value=True)
    amb_vol = st.slider("BG jačina", 0.0, 1.0, 0.30, 0.01, disabled=not amb_on)
    fx_vol  = st.slider("FX jačina", 0.0, 1.0, 0.55, 0.01)

with colB:
    st.markdown("#### Padovi")
    st.markdown("Klikni: **C** / **E** / **G**")

# ugnezdeni HTML + JS (statički fajlovi)
loop = "/static/audio/ecosystem_formula_loop.ogg"
C    = "/static/audio/c2_note.ogg"
E    = "/static/audio/harp_e.ogg"
G    = "/static/audio/harp_g.ogg"

_html(f"""
<div style="display:flex;gap:14px;align-items:center;margin-top:6px">
  <button id="padC" style="padding:14px 22px;border-radius:12px;border:1px solid #33405a;background:#112;border-color:#2a3d63;color:#e8f2ff;cursor:pointer">C</button>
  <button id="padE" style="padding:14px 22px;border-radius:12px;border:1px solid #33405a;background:#112;border-color:#2a3d63;color:#e8f2ff;cursor:pointer">E</button>
  <button id="padG" style="padding:14px 22px;border-radius:12px;border:1px solid #33405a;background:#112;border-color:#2a3d63;color:#e8f2ff;cursor:pointer">G</button>
  <button id="stop" style="margin-left:8px;padding:14px 22px;border-radius:12px;border:1px solid #33405a;background:#301f1f;border-color:#603a3a;color:#ffd8d8;cursor:pointer">Stop</button>
</div>

<audio id="bg" src="{loop}" loop></audio>
<audio id="aC" src="{C}"></audio>
<audio id="aE" src="{E}"></audio>
<audio id="aG" src="{G}"></audio>

<script>
  const bg = document.getElementById('bg');
  const aC = document.getElementById('aC');
  const aE = document.getElementById('aE');
  const aG = document.getElementById('aG');

  // inicijalni volumeni iz Streamlit slidera
  const AMB = {str(amb_vol)};
  const FX  = {str(fx_vol)};
  if (bg) bg.volume = AMB;
  [aC,aE,aG].forEach(a => {{ if(a) a.volume = FX; }});

  // unlock – prvi klik/touch
  const unlock = () => {{
    try {{ if({str(amb_on).lower()} && bg.paused) bg.play(); }} catch(e) {{}}
    window.removeEventListener('click', unlock);
    window.removeEventListener('touchstart', unlock);
  }};
  window.addEventListener('click', unlock, {{once:true}});
  window.addEventListener('touchstart', unlock, {{once:true}});

  // Padovi
  function tap(a){{ try{{ a.currentTime = 0; a.play(); }}catch(e){{}} }}

  document.getElementById('padC').onclick = () => tap(aC);
  document.getElementById('padE').onclick = () => tap(aE);
  document.getElementById('padG').onclick = () => tap(aG);

  document.getElementById('stop').onclick = () => {{
    [aC,aE,aG,bg].forEach(a => {{ try{{ a.pause(); }}catch(e){{}} }});
  }};
</script>
""", height=90)
