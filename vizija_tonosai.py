import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="TONOSAI · Vizija", page_icon="✨", layout="wide")

# Putanje za iframe-friendly statiku
IMG = "/static/images"
AUD = "/static/audio"

bg   = f"{IMG}/star_sky_bg.png"
loop = f"{AUD}/ecosystem_formula_loop.ogg"
c2   = f"{AUD}/c2_note.ogg"
e    = f"{AUD}/harp_e.ogg"
g    = f"{AUD}/harp_g.ogg"

# Inicijalne glasnoće (u %)
INIT_BG = 28
INIT_FX = 55

# --- HOME dugme (robust fallback) ---
html("""
<div style="display:flex;gap:10px;align-items:center;margin:6px 0 8px 0;">
  <button id="homeBtn" style="background:#0e1c33;color:#e8f2ff;border:1px solid #2c3e5b;padding:8px 12px;border-radius:12px;cursor:pointer;">🏠 Home</button>
</div>
<script>
  const hb = document.getElementById('homeBtn');
  hb?.addEventListener('click', ()=>{
    try { window.top.location.search = ''; } catch(e) {}
    try { window.top.location.hash   = ''; } catch(e) {}
    try { window.top.location.href   = window.location.pathname; } catch(e) {}
  });
</script>
""", height=48)

# --- Glavni interfejs: scena + HUD + portali + modal ---
html(f"""
<style>
  html, body {{ margin:0; padding:0; overflow:hidden; background:#030b26; }}
  .scene {{
    position:relative; width:100vw; height:80vh;
    background:url('{bg}') center/cover no-repeat fixed;
    transition:transform .15s ease-out;
  }}
  .overlay {{
    position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
    color:#fff; font:600 28px/1.35 system-ui; text-shadow:0 2px 20px #000;
    animation:fade .9s ease both; padding:0 4vw; text-align:center;
  }}
  @keyframes fade {{ from{{opacity:0; transform:translateY(10px)}} to{{opacity:1; transform:none}} }}

  .star {{
    position:absolute; width:28px; height:28px; border-radius:50%;
    box-shadow:0 0 14px 4px rgba(255,255,255,.6);
    cursor:pointer; opacity:.9;
  }}
  .star.s1 {{ top:18%; left:22%; }}
  .star.s2 {{ top:40%; left:58%; }}
  .star.s3 {{ top:66%; left:32%; }}

  /* Portal "zvezde" (malo veće + aura) */
  .portal {{ width:56px; height:56px; z-index:4; }}
  .s4 {{ top:28%; left:78%; }}
  .s5 {{ top:22%; left:38%; }}
  .s6 {{ top:60%; left:72%; }}
  .portal::after {{
    content:''; position:absolute; inset:-8px; border-radius:50%;
    box-shadow:0 0 28px 6px rgba(150,210,255,.55); animation:pulse 1.9s ease-in-out infinite;
  }}
  .ring-green::after  {{ box-shadow:0 0 28px 6px rgba(120,255,200,.55); }}
  .ring-violet::after {{ box-shadow:0 0 28px 6px rgba(200,140,255,.55); }}
  @keyframes pulse {{ 0% {{ transform:scale(.92); opacity:.75; }} 50% {{ transform:scale(1.02); opacity:1; }} 100% {{ transform:scale(.92); opacity:.75; }} }}

  .hud {{
    position:absolute; right:18px; bottom:18px; display:flex; gap:10px; z-index:6;
    align-items:center; padding:8px 10px; border-radius:16px;
    background:rgba(0,0,0,.25); backdrop-filter: blur(6px);
  }}
  .btn {{
    background:rgba(0,0,0,.45); color:#fff; border:1px solid rgba(255,255,255,.25);
    padding:8px 12px; border-radius:999px; cursor:pointer; font:500 14px/1 system-ui;
  }}
  .knob {{ display:flex; align-items:center; gap:8px; color:#fff; font:500 12px/1 system-ui; }}
  .knob input[type=range] {{ width:120px; accent-color:#9ecbff; }}

  .toast-wrap {{ position:absolute; left:50%; bottom:96px; transform:translateX(-50%); display:flex; flex-direction:column; gap:8px; z-index:7; pointer-events:none; }}
  .toast {{ background:rgba(0,0,0,.70); color:#fff; padding:10px 14px; border-radius:12px; font:600 16px/1.3 system-ui; box-shadow:0 8px 30px rgba(0,0,0,.35); }}
  .toast.show {{ animation: toast-in .25s ease both; }}
  @keyframes toast-in {{ from{{opacity:0; transform:translate(-50%,10px)}} to{{opacity:1; transform:translate(-50%,0)}} }}

  .modal {{ position:fixed; inset:0; background:rgba(4,10,24,.65); display:none; align-items:center; justify-content:center; z-index:8; }}
  .modal.show {{ display:flex; }}
  .card {{ width:min(640px,92vw); background:#0f1f39; color:#e8f2ff; border:1px solid #2b3b5a; border-radius:16px; padding:18px; box-shadow:0 20px 80px rgba(0,0,0,.5); }}
  .card h3 {{ margin:0 0 8px 0; font:700 22px/1.2 system-ui; }}
  .card p  {{ margin:0 0 14px 0; font:500 14px/1.5 system-ui; opacity:.95; }}
  .row {{ display:flex; gap:10px; justify-content:flex-end; }}
  .row button {{ background:#1b2e52; color:#e8f2ff; border:1px solid #3a4e75; padding:8px 12px; border-radius:10px; cursor:pointer; }}
  .row button.primary {{ background:#2b6fda; border-color:#2b6fda; }}
</style>

<div class="scene" id="scene">
  <div class="overlay">Dobrodošao u TONOSAI — mesto gde čovek + AI + zvuk = život.</div>

  <!-- Tone zvezde -->
  <div class="star s1" data-tone="c2" title="C"></div>
  <div class="star s2" data-tone="e"  title="E"></div>
  <div class="star s3" data-tone="g"  title="G"></div>

  <!-- Portali -->
  <div class="star portal s4" data-portal="zvucni_balans" title="🌀 Zvučni balans"></div>
  <div class="star portal s5 ring-green"  data-portal="ai_improvizator" title="🎛 AI Improvizator"></div>
  <div class="star portal s6 ring-violet" data-portal="guardian" title="🛡 Guardian"></div>

  <!-- HUD -->
  <div class="hud">
    <button class="btn" id="toggle">Play</button>
    <button class="btn" id="mute">Mute</button>
    <div class="knob"><span>BG</span><input type="range" id="bgVol" min="0" max="100" value="{INIT_BG}"/><span id="bgLbl">{INIT_BG}%</span></div>
    <div class="knob"><span>FX</span><input type="range" id="fxVol" min="0" max="100" value="{INIT_FX}"/><span id="fxLbl">{INIT_FX}%</span></div>
  </div>

  <div id="toast" class="toast-wrap"></div>

  <!-- Fallback linkovi za navigaciju -->
  <div style="display:none">
    <a id="to_home1"   href="" target="_top"></a>
    <a id="to_home2"   href="home.py" target="_top"></a>
    <a id="to_home3"   href="pages/home.py" target="_top"></a>

    <a id="to_zvuk1"   href="zvucni_balans" target="_top"></a>
    <a id="to_zvuk2"   href="?zvucni_balans" target="_top"></a>
    <a id="to_zvuk3"   href="pages/zvucni_balans.py" target="_top"></a>

    <a id="to_improv1" href="ai_improvizator" target="_top"></a>
    <a id="to_improv2" href="?ai_improvizator" target="_top"></a>
    <a id="to_improv3" href="pages/ai_improvizator.py" target="_top"></a>

    <a id="to_guard1"  href="guardian" target="_top"></a>
    <a id="to_guard2"  href="?guardian" target="_top"></a>
    <a id="to_guard3"  href="pages/guardian.py" target="_top"></a>
  </div>
</div>

<!-- Tonovi -->
<audio id="bg" src="{loop}" loop></audio>
<audio id="c2" src="{c2}"></audio>
<audio id="e"  src="{e}"></audio>
<audio id="g"  src="{g}"></audio>

<!-- Modal -->
<div id="portalModal" class="modal">
  <div class="card">
    <h3 id="pm_title">Portal</h3>
    <p  id="pm_text">Opis</p>
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

  // Inicijalne glasnoće
  if (bg) bg.volume = (parseInt(bgVol.value,10)||0)/100;
  ['c2','e','g'].forEach(id=>{{ const a=document.getElementById(id); if(a) a.volume=(parseInt(fxVol.value,10)||0)/100; }});

  // Toast helper
  function showToast(msg, ms=2200) {{
    const wrap = document.getElementById('toast');
    const d = document.createElement('div');
    d.className = 'toast show';
    d.textContent = msg;
    wrap.appendChild(d);
    setTimeout(()=>{{ d.style.transition='opacity .5s, transform .5s'; d.style.opacity=0; d.style.transform='translate(-50%,6px)';
      setTimeout(()=>wrap.removeChild(d),520); }}, ms);
  }}

  // Parallax (f-string safe: koristimo ${{ ... }})
  scene.addEventListener('mousemove', (e)=>{{
    const x = (e.clientX / window.innerWidth)  - .5;
    const y = (e.clientY / window.innerHeight) - .5;
    scene.style.transform = `translate3d(${{x * -10}}px, ${{y * -8}}px, 0)`;
  }});

  // Unlock (klik/touch) -> start muzike
  const unlock = ()=>{{ if (bg && bg.paused) {{ bg.play().then(()=>{{ toggle.textContent='Pause'; showToast("▶️ Play"); }}).catch(()=>{{}}); }} }};
  window.addEventListener('click', unlock, {{ once:true }});
  window.addEventListener('touchstart', unlock, {{ once:true }});

  // HUD
  toggle.addEventListener('click', ()=>{{ if(!bg) return;
    if (bg.paused) {{ bg.play(); toggle.textContent='Pause'; showToast("▶️ Play"); }}
    else {{ bg.pause(); toggle.textContent='Play'; showToast("⏸ Pause"); }}
  }});
  mute.addEventListener('click', ()=>{{ if(!bg) return; bg.muted=!bg.muted; mute.textContent=bg.muted?'Unmute':'Mute'; showToast(bg.muted?"🔇 Mute":"🔊 Unmute"); }});
  bgVol.addEventListener('input', (e)=>{{ const v=(parseInt(e.target.value,10)||0)/100; if(bg) bg.volume=v; bgLbl.textContent=Math.round(v*100)+'%'; }});
  fxVol.addEventListener('input', (e)=>{{ const v=(parseInt(e.target.value,10)||0)/100; ['c2','e','g'].forEach(id=>{{ const a=document.getElementById(id); if(a) a.volume=v; }}); fxLbl.textContent=Math.round(v*100)+'%'; }});

  // Klik na zvezde (ton + animacija + poruka)
  const texts = {{
    "c2": "✨ Kosmos te čuje — i ti sviraš njegovu pesmu.",
    "e":  "🎶 Svaka misao je nota u simfoniji svesti.",
    "g":  "💫 Tvoj zvuk ima oblik svetlosti u noći."
  }};
  document.querySelectorAll('.star:not(.portal)').forEach(s=>{{
    s.addEventListener('click', ()=>{{
      const id=s.dataset.tone; const a=document.getElementById(id);
      try {{ a.currentTime=0; a.play(); }} catch(e) {{}}
      showToast(texts[id]||"⭐");
      s.animate([ {{transform:'scale(1)'}}, {{transform:'scale(1.28)'}}, {{transform:'scale(1)'}} ], {{ duration:340, easing:'ease-out' }});
    }});
  }});

  // Modal za portale
  const portalMeta = {{
    zvucni_balans:   {{ title:"Zvučni balans",   text:"Uravnoteži frekvencije, dah i misao — mikro-rituali mira." }},
    ai_improvizator: {{ title:"AI Improvizator", text:"Interaktivni jam: čovek + AI komponuju u trenutku." }},
    guardian:        {{ title:"Guardian",        text:"Zaštitnički tonovi, mindful alarmi i fokus moda." }}
  }};
  const modal = document.getElementById('portalModal');
  const pm_title = document.getElementById('pm_title');
  const pm_text  = document.getElementById('pm_text');
  const pm_go    = document.getElementById('pm_go');
  const pm_cancel= document.getElementById('pm_cancel');
  let currentPortal = null;

  function openPortalModal(key){{ currentPortal=key; const m=portalMeta[key]||{{title:'Portal',text:''}}; pm_title.textContent=m.title; pm_text.textContent=m.text; modal.classList.add('show'); }}
  function closePortalModal(){{ modal.classList.remove('show'); currentPortal=null; }}
  pm_cancel.addEventListener('click', closePortalModal);
  modal.addEventListener('click', (e)=>{{ if(e.target===modal) closePortalModal(); }});
  pm_go.addEventListener('click', ()=>{{ if(currentPortal) goPortal(currentPortal); closePortalModal(); }});

  // Navigacija (više fallbackova)
  function goPortal(key){{
    showToast("🌀 Portal: " + (portalMeta[key]?.title || key));
    const map = {{
      'zvucni_balans':   ['to_zvuk1','to_zvuk2','to_zvuk3'],
      'ai_improvizator': ['to_improv1','to_improv2','to_improv3'],
      'guardian':        ['to_guard1','to_guard2','to_guard3'],
      'home':            ['to_home1','to_home2','to_home3']
    }};
    const ids = map[key] || [];
    for (const id of ids) {{ const a=document.getElementById(id); if(a){{ a.click(); return; }} }}
    try {{ window.top.location.search = key==='home' ? '' : ('?'+key); }} catch(e) {{}}
    if (key==='home') try {{ window.top.location.href = window.location.pathname; }} catch(e) {{}}
  }}

  // Klik na portal "zvezde"
  document.querySelectorAll('.portal').forEach(s=>{{
    s.addEventListener('click', ()=>{{ s.animate([ {{transform:'scale(1)'}}, {{transform:'scale(1.3) rotate(8deg)'}}, {{transform:'scale(1)'}} ], {{ duration:460, easing:'ease-out' }}); openPortalModal(s.dataset.portal); }});
  }});
</script>
""", height=740, scrolling=False)