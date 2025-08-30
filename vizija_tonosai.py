
import os, base64
import streamlit as st
from streamlit.components.v1 import html as components_html

st.set_page_config(page_title="TONOSAI · Vizija", page_icon="✨", layout="wide")

try:
    from lib.ui import header_badges, footer
except Exception:
    header_badges = lambda: None
    footer = lambda: None

header_badges()

# ------------- helpers -------------
def b64(path: str):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

def data_uri(mime: str, b64str):
    return f"data:{mime};base64,{b64str}" if b64str else None

IMG = "static/images"
AUD = "static/audio"

bg_uri   = data_uri("image/png", b64(f"{IMG}/star_sky_bg.png"))
star_uri = data_uri("image/png", b64(f"{IMG}/star_clickable.png"))
loop_uri = data_uri("audio/ogg", b64(f"{AUD}/ecosystem_formula_loop.ogg"))
c2_uri   = data_uri("audio/ogg", b64(f"{AUD}/c2_note.ogg"))
e_uri    = data_uri("audio/ogg", b64(f"{AUD}/harp_e.ogg"))
g_uri    = data_uri("audio/ogg", b64(f"{AUD}/harp_g.ogg"))

missing = [name for name, ok in [
    ("static/images/star_sky_bg.png", bg_uri),
    ("static/images/star_clickable.png", star_uri),
    ("static/audio/ecosystem_formula_loop.ogg", loop_uri),
    ("static/audio/c2_note.ogg", c2_uri),
    ("static/audio/harp_e.ogg", e_uri),
    ("static/audio/harp_g.ogg", g_uri),
] if ok is None]
if missing:
    st.warning("Nedostaju fajlovi: " + ", ".join(missing))

INIT_BG_VOL = 28
INIT_FX_VOL = 55

# ---------- top Home bar (JS-based for robustness) ----------
components_html("""
<div style="display:flex; gap:10px; align-items:center; margin:4px 0 8px 0;">
  <button id="homeBtn" style="background:#0e1c33;color:#e8f2ff;border:1px solid #2c3e5b;padding:8px 12px;border-radius:12px;cursor:pointer;">🏠 Home</button>
  <script>
    const hb = document.getElementById('homeBtn');
    hb?.addEventListener('click', ()=>{
      try { window.top.location.search = ''; } catch(e) {}
      try { window.top.location.hash = ''; } catch(e) {}
      try { window.top.location.href = window.location.pathname; } catch(e) {}
    });
  </script>
</div>
""", height=40, scrolling=False)

# ------------- main component -------------
components_html(f"""
<style>
  html, body {{ margin:0; padding:0; overflow:hidden; }}
  .scene {{
    position:relative; width:100vw; height:82vh;
    background: {'url('+bg_uri+') center/cover no-repeat fixed' if bg_uri else '#02081a'};
    transition: transform .15s ease-out;
  }}
  .overlay {{
    position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
    color:#ffffff; font: 600 28px/1.35 system-ui, -apple-system, Segoe UI, Roboto;
    text-shadow:0 2px 20px #000a;
    animation: fade .9s ease both; padding: 0 4vw; text-align:center;
  }}
  @keyframes fade {{ from {{opacity:0; transform:translateY(10px)}} to {{opacity:1; transform:none}} }}
  .hud {{
    position:absolute; right:18px; bottom:18px; display:flex; gap:10px; z-index:6;
    align-items:center; padding:8px 10px; border-radius:16px;
    background: rgba(0,0,0,.25); backdrop-filter: blur(6px);
  }}
  .btn {{ background:rgba(0,0,0,.45); color:#fff; border:1px solid rgba(255,255,255,.25);
         padding:8px 12px; border-radius:999px; cursor:pointer; font: 500 14px/1 system-ui; }}
  .knob {{ display:flex; align-items:center; gap:8px; color:#fff; font:500 12px/1 system-ui; }}
  .knob input[type=range] {{ width:120px; accent-color:#9ecbff; }}

  .star {{ position:absolute; width:48px; height:48px; cursor:pointer; z-index:3;
           filter: drop-shadow(0 0 8px rgba(255,255,255,.75)); transition: transform .25s ease; }}
  .star:hover {{ transform: scale(1.12) rotate(6deg); }}
  .s1 {{ top: 18%; left: 22%; }}
  .s2 {{ top: 42%; left: 58%; }}
  .s3 {{ top: 66%; left: 30%; }}

  /* Portal stars */
  .s4 {{ top: 28%; left: 78%; width:60px; height:60px; z-index:4; }}
  .s5 {{ top: 22%; left: 38%; width:56px; height:56px; z-index:4; }}
  .s6 {{ top: 60%; left: 72%; width:56px; height:56px; z-index:4; }}
  .portal-ring::after {{ content:''; position:absolute; inset:-8px; border-radius:50%;
                         box-shadow:0 0 28px 6px rgba(150,210,255,.55); animation:pulse 1.8s ease-in-out infinite; }}
  .ring-green::after {{ box-shadow:0 0 28px 6px rgba(120,255,200,.55); }}
  .ring-violet::after {{ box-shadow:0 0 28px 6px rgba(200,140,255,.55); }}
  @keyframes pulse {{ 0% {{ transform:scale(0.92); opacity:.75; }} 50% {{ transform:scale(1.02); opacity:1; }} 100% {{ transform:scale(0.92); opacity:.75; }} }}

  /* Toasts */
  .toast-wrap {{ position:absolute; left:50%; bottom:96px; transform:translateX(-50%);
                 display:flex; flex-direction:column; gap:8px; z-index:7; pointer-events:none; }}
  .toast {{ background:rgba(0,0,0,.70); color:#fff; padding:10px 14px; border-radius:12px;
            font:600 16px/1.3 system-ui; box-shadow:0 8px 30px rgba(0,0,0,.35); }}
  .toast.show {{ animation: toast-in .25s ease both; }}
  @keyframes toast-in {{ from {{opacity:0; transform:translate(-50%, 10px)}} to {{opacity:1; transform:translate(-50%, 0)}} }}

  /* Modal */
  .modal {{ position:fixed; inset:0; background:rgba(4,10,24,.65); display:none; align-items:center; justify-content:center; z-index:8; }}
  .modal.show {{ display:flex; }}
  .card {{ width:min(640px, 92vw); background:#0f1f39; color:#e8f2ff; border:1px solid #2b3b5a; border-radius:16px; padding:18px; box-shadow:0 20px 80px rgba(0,0,0,.5); }}
  .card h3 {{ margin:0 0 8px 0; font:700 22px/1.2 system-ui; }}
  .card p {{ margin:0 0 14px 0; font:500 14px/1.5 system-ui; opacity:.95; }}
  .card .row {{ display:flex; gap:10px; justify-content:flex-end; }}
  .card .row button {{ background:#1b2e52; color:#e8f2ff; border:1px solid #3a4e75; padding:8px 12px; border-radius:10px; cursor:pointer; }}
  .card .row button.primary {{ background:#2b6fda; border-color:#2b6fda; }}
</style>

<div class="scene" id="scene">
  <div class="overlay">Dobrodošao u TONOSAI — mesto gde čovek + AI + zvuk = život.</div>

  <!-- Tone stars -->
  {"".join([
    f'<img class="star s{i}" data-tone="{tone}" src="{star_uri}" alt="star {tone}"/>'
    for i, tone in [(1,"c2"), (2,"e"), (3,"g")]
  ])}

  <!-- Portal stars -->
  <img class="star s4 portal-ring" data-portal="zvucni_balans" src="{star_uri}" alt="portal zvucni"/>
  <img class="star s5 portal-ring ring-green" data-portal="ai_improvizator" src="{star_uri}" alt="portal improvizator"/>
  <img class="star s6 portal-ring ring-violet" data-portal="guardian" src="{star_uri}" alt="portal guardian"/>

  <!-- HUD -->
  <div class="hud">
    <button class="btn" id="toggle">Play</button>
    <button class="btn" id="mute">Mute</button>
    <div class="knob"><span>BG</span><input type="range" id="bgVol" min="0" max="100" value="{INIT_BG_VOL}"/><span id="bgLbl">{INIT_BG_VOL}%</span></div>
    <div class="knob"><span>FX</span><input type="range" id="fxVol" min="0" max="100" value="{INIT_FX_VOL}"/><span id="fxLbl">{INIT_FX_VOL}%</span></div>
  </div>

  <div id="toast" class="toast-wrap"></div>

  <!-- Hidden links for robust navigation -->
  <div style="display:none">
    <a id="to_home1" href="" target="_top"></a>
    <a id="to_home2" href="home.py" target="_top"></a>
    <a id="to_home3" href="pages/home.py" target="_top"></a>

    <a id="to_zvuk1" href="zvucni_balans" target="_top"></a>
    <a id="to_zvuk2" href="?zvucni_balans" target="_top"></a>
    <a id="to_zvuk3" href="pages/zvucni_balans.py" target="_top"></a>

    <a id="to_improv1" href="ai_improvizator" target="_top"></a>
    <a id="to_improv2" href="?ai_improvizator" target="_top"></a>
    <a id="to_improv3" href="pages/ai_improvizator.py" target="_top"></a>

    <a id="to_guard1" href="guardian" target="_top"></a>
    <a id="to_guard2" href="?guardian" target="_top"></a>
    <a id="to_guard3" href="pages/guardian.py" target="_top"></a>
  </div>
</div>

<audio id="bg" src="{loop_uri or ''}" loop></audio>
<audio id="c2" src="{c2_uri or ''}"></audio>
<audio id="e"  src="{e_uri or ''}"></audio>
<audio id="g"  src="{g_uri or ''}"></audio>

<!-- Modal -->
<div id="portalModal" class="modal">
  <div class="card">
    <h3 id="pm_title">Portal</h3>
    <p id="pm_text">Opis</p>
    <div class="row">
      <button id="pm_cancel">Nazad</button>
      <button class="primary" id="pm_go">Uđi</button>
    </div>
  </div>
</div>

<script>
  const scene  = document.getElementById('scene');
  const bg     = document.getElementById('bg');
  const toggle = document.getElementById('toggle');
  const mute   = document.getElementById('mute');

  const bgVol  = document.getElementById('bgVol');
  const fxVol  = document.getElementById('fxVol');
  const bgLbl  = document.getElementById('bgLbl');
  const fxLbl  = document.getElementById('fxLbl');

  const tones = ['c2','e','g'].map(id => document.getElementById(id)).filter(Boolean);

  const portalMeta = {{
    zvucni_balans: {{
      title: "Zvučni balans",
      text:  "Uravnoteži frekvencije, harmonizuj dah i misao — mikro-rituali mira."
    }},
    ai_improvizator: {{
      title: "AI Improvizator",
      text:  "Interaktivni jam: čovek + AI komponuju u trenutku — igra kreativne svesti."
    }},
    guardian: {{
      title: "Guardian",
      text:  "Zaštitnički tonovi, mindful alarmi i granice — fokus i briga u jednoj auri."
    }}
  }};

  // Toasts
  function showToast(msg, ms=2200) {{
    const wrap = document.getElementById('toast');
    const d = document.createElement('div');
    d.className = 'toast show';
    d.textContent = msg;
    wrap.appendChild(d);
    setTimeout(()=>{{ d.style.transition='opacity .5s, transform .5s'; d.style.opacity=0; d.style.transform='translate(-50%,6px)'; setTimeout(()=>wrap.removeChild(d),520); }}, ms);
  }}

  // Volumes
  if (bg) bg.volume = (parseInt(bgVol.value,10) || 0) / 100;
  tones.forEach(a => a.volume = (parseInt(fxVol.value,10) || 0) / 100);

  // Parallax
  scene.addEventListener('mousemove', (e)=>{{
    const x = (e.clientX / window.innerWidth)  - .5;
    const y = (e.clientY / window.innerHeight) - .5;
    scene.style.transform = `translate3d(${{x * -10}}px, ${{y * -8}}px, 0)`;
  }});

  // Unlock
  const unlock = ()=>{{ if (bg && bg.paused) {{ bg.play().then(()=>{{ toggle.textContent='Pause'; showToast("▶️ Pokrenuto"); }}).catch(()=>{{}}); }} }};
  window.addEventListener('click', unlock, {{ once:true }});
  window.addEventListener('touchstart', unlock, {{ once:true }});

  // HUD
  toggle.addEventListener('click', ()=>{{ if (!bg) return; if (bg.paused) {{ bg.play(); toggle.textContent='Pause'; showToast("▶️ Play"); }} else {{ bg.pause(); toggle.textContent='Play'; showToast("⏸ Pause"); }} }});
  mute.addEventListener('click', ()=>{{ if (!bg) return; bg.muted = !bg.muted; mute.textContent = bg.muted ? 'Unmute' : 'Mute'; showToast(bg.muted ? "🔇 Mute" : "🔊 Unmute"); }});
  bgVol.addEventListener('input', (e)=>{{ const v=(parseInt(e.target.value,10)||0)/100; if (bg) bg.volume=v; bgLbl.textContent=Math.round(v*100)+'%'; }});
  fxVol.addEventListener('input', (e)=>{{ const v=(parseInt(e.target.value,10)||0)/100; tones.forEach(a=>a.volume=v); fxLbl.textContent=Math.round(v*100)+'%'; }});

  // Tone stars
  const texts = { c2: "✨ Kosmos te čuje — i ti sviraš njegovu pesmu.", e: "🎶 Svaka misao je nota u simfoniji svesti.", g: "💫 Tvoj zvuk ima oblik svetlosti u noći." };
  document.querySelectorAll('.star.s1, .star.s2, .star.s3').forEach(s=>{{
    s.addEventListener('click', ()=>{{ const id=s.dataset.tone; const a=document.getElementById(id); if(a){{ try{{ a.currentTime=0; a.play(); }}catch(e){{}} }} showToast(texts[id]||"⭐"); s.animate([{{transform:'scale(1)'}},{{transform:'scale(1.25)'}},{{transform:'scale(1)'}}],{{duration:320,easing:'ease-out'}}); }});
  }});

  // Modal helpers
  const modal = document.getElementById('portalModal');
  const pm_title = document.getElementById('pm_title');
  const pm_text  = document.getElementById('pm_text');
  const pm_go    = document.getElementById('pm_go');
  const pm_cancel= document.getElementById('pm_cancel');
  let currentPortal = null;

  function openPortalModal(key){{ currentPortal = key; const meta = portalMeta[key] || {{title:'Portal', text:''}}; pm_title.textContent = meta.title; pm_text.textContent = meta.text; modal.classList.add('show'); }}
  function closePortalModal(){{ modal.classList.remove('show'); currentPortal=null; }}
  pm_cancel.addEventListener('click', closePortalModal);
  pm_go.addEventListener('click', ()=>{{ if(currentPortal) goPortal(currentPortal); closePortalModal(); }});
  modal.addEventListener('click', (e)=>{{ if(e.target===modal) closePortalModal(); }});

  // Portal navigation (multiple fallbacks for Streamlit routes)
  function goPortal(key){{
    showToast("🌀 Portal: " + (portalMeta[key]?.title || key));
    const map = {{
      'zvucni_balans': ['to_zvuk1','to_zvuk2','to_zvuk3'],
      'ai_improvizator': ['to_improv1','to_improv2','to_improv3'],
      'guardian': ['to_guard1','to_guard2','to_guard3'],
      'home': ['to_home1','to_home2','to_home3']
    }};
    const ids = map[key] || [];
    for (const id of ids) {{ const a = document.getElementById(id); if (a) {{ a.click(); return; }} }}
    try {{ window.top.location.search = key==='home' ? '' : ('?'+key); }} catch(e) {{}}
    if (key==='home') try {{ window.top.location.href = window.location.pathname; }} catch(e) {{}}
  }}

  // Portal stars click -> modal
  document.querySelectorAll('[data-portal]').forEach(s=>{{ s.addEventListener('click', ()=>{{ s.animate([{{transform:'scale(1)'}},{{transform:'scale(1.3) rotate(8deg)'}},{{transform:'scale(1)'}}],{{duration:480,easing:'ease-out'}}); openPortalModal(s.dataset.portal); }}); }});
</script>
""", height=730, scrolling=False)

# ---------- CTA + Contact ----------
st.markdown("### ")
cta = st.columns([1,2,1])[1]
with cta:
    try:
        st.page_link("home.py", label="👉 Uđi u studio", icon="🌌")
    except Exception:
        if st.button("👉 Uđi u studio", type="primary"):
            try:
                st.switch_page("home.py")
            except Exception:
                st.info("Ako se ništa ne desi, klikni **home** u levom meniju.")

st.markdown(
    """
    <div style="margin: 18px auto; max-width: 900px;">
      <div style="background:#14243b; color:#e8f2ff; padding:12px 16px; border-radius:12px;">
        Kontakt: <a href="mailto:jazzienmonk369@gmail.com" style="color:#9ecbff; text-decoration:none;">jazzienmonk369@gmail.com</a>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

footer()
