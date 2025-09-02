# vizija_tonosai.py — TONOSAI · Vizija (portali + ambijent)
import json
import streamlit as st
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="TONOSAI · Vizija", page_icon="✨", layout="wide")

# Putanje i inic vrednosti
IMG         = "/static/images"
AUDIO_ROOT  = "/static/audio"
INIT_BG     = 28   # %
INIT_FX     = 55   # %

cfg_json = json.dumps({
    "IMG": IMG,
    "AUDIO_ROOT": AUDIO_ROOT,
    "INIT_BG": INIT_BG,
    "INIT_FX": INIT_FX,
})

html_src = r"""
<style>
  html,body { margin:0; padding:0; overflow:hidden; background:#030b26; }
  .scene {
    position:relative; width:100vw; height:82vh;
    background:url('__IMG__/star_sky_bg.png') center/cover no-repeat fixed;
    transition:transform .15s ease-out;
  }
  .overlay {
    position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
    padding:0 4vw; text-align:center;
    color:#fff; font:700 32px/1.35 system-ui; text-shadow:0 2px 22px #000; letter-spacing:.2px;
    animation: fade .9s ease both;
  }
  @keyframes fade { from{opacity:0; transform:translateY(10px)} to{opacity:1; transform:none} }

  .star { position:absolute; width:28px; height:28px; border-radius:50%; cursor:pointer; opacity:.9;
          box-shadow:0 0 14px 4px rgba(255,255,255,.65); }
  .s1 { top:18%; left:22%; } .s2 { top:40%; left:58%; } .s3 { top:66%; left:32%; }

  .portal { width:56px; height:56px; z-index:4; }
  .p1 { top:28%; left:78%; } .p2 { top:22%; left:38%; } .p3 { top:60%; left:72%; }
  .portal::after { content:''; position:absolute; inset:-8px; border-radius:50%;
    box-shadow:0 0 28px 6px rgba(150,210,255,.55); animation:pulse 1.9s ease-in-out infinite; }
  .green::after  { box-shadow:0 0 28px 6px rgba(120,255,200,.55); }
  .violet::after { box-shadow:0 0 28px 6px rgba(200,140,255,.55); }
  @keyframes pulse { 0%{transform:scale(.92); opacity:.75} 50%{transform:scale(1.02); opacity:1} 100%{transform:scale(.92); opacity:.75} }

  .hud{
    position:absolute; right:18px; bottom:18px; display:flex; gap:10px; z-index:6;
    align-items:center; padding:8px 10px; border-radius:16px;
    background:rgba(0,0,0,.25); backdrop-filter: blur(6px);
  }
  .btn{
    background:rgba(0,0,0,.45); color:#fff; border:1px solid rgba(255,255,255,.25);
    padding:8px 12px; border-radius:999px; cursor:pointer; font:500 14px/1 system-ui;
  }
  .knob{ display:flex; align-items:center; gap:8px; color:#fff; font:500 12px/1 system-ui; }
  .knob input[type=range]{ width:120px; accent-color:#9ecbff; }

  .toast-wrap{ position:absolute; left:50%; bottom:96px; transform:translateX(-50%);
               display:flex; flex-direction:column; gap:8px; z-index:7; pointer-events:none; }
  .toast{ background:rgba(0,0,0,.70); color:#fff; padding:10px 14px; border-radius:12px;
          font:600 16px/1.3 system-ui; box-shadow:0 8px 30px rgba(0,0,0,.35); }
  .toast.show{ animation: toast-in .25s ease both; }
  @keyframes toast-in { from{opacity:0; transform:translate(-50%,10px)} to{opacity:1; transform:translate(-50%,0)} }

  .modal{ position:fixed; inset:0; background:rgba(4,10,24,.65); display:none; align-items:center; justify-content:center; z-index:8; }
  .modal.show{ display:flex; }
  .card{ width:min(640px,92vw); background:#0f1f39; color:#e8f2ff; border:1px solid #2b3b5a; border-radius:16px; padding:18px; box-shadow:0 20px 80px rgba(0,0,0,.5); }
  .card h3{ margin:0 0 8px 0; font:700 22px/1.2 system-ui; }
  .card p { margin:0 0 14px 0; font:500 14px/1.5 system-ui; opacity:.95; }
  .row{ display:flex; gap:10px; justify-content:flex-end; }
  .row button{ background:#1b2e52; color:#e8f2ff; border:1px solid #3a4e75; padding:8px 12px; border-radius:10px; cursor:pointer; }
  .row button.primary{ background:#2b6fda; border-color:#2b6fda; }
</style>

<div class="scene" id="scene">
  <div class="overlay">Dobrodošao u TONOSAI — mesto gde čovek + AI + zvuk = život.</div>

  <div class="star s1" data-tone="c2" title="C"></div>
  <div class="star s2" data-tone="e"  title="E"></div>
  <div class="star s3" data-tone="g"  title="G"></div>

  <div class="star portal p1" data-portal="zvucni_balans" title="🌀 Zvučni balans"></div>
  <div class="star portal p2 green"  data-portal="ai_improvizator" title="🎛 AI Improvizator"></div>
  <div class="star portal p3 violet" data-portal="guardian" title="🛡 Guardian"></div>

  <div class="hud">
    <button class="btn" id="playBtn">Play</button>
    <button class="btn" id="muteBtn">Mute</button>
    <div class="knob"><span>BG</span><input type="range" id="bgVol" min="0" max="100"/><span id="bgLbl"></span></div>
    <div class="knob"><span>FX</span><input type="range" id="fxVol" min="0" max="100"/><span id="fxLbl"></span></div>
  </div>

  <div id="toasts" class="toast-wrap"></div>
</div>

<audio id="bg" preload="auto"><source src="__AUDIO__/ecosystem_formula_loop.ogg" type="audio/ogg" /></audio>
<audio id="c2" preload="auto"><source src="__AUDIO__/c2_note.ogg" type="audio/ogg" /></audio>
<audio id="e"  preload="auto"><source src="__AUDIO__/harp_e.ogg" type="audio/ogg" /></audio>
<audio id="g"  preload="auto"><source src="__AUDIO__/harp_g.ogg" type="audio/ogg" /></audio>

<div style="display:none">
  <a id="zb1" href="zvucni_balans" target="_top"></a>
  <a id="ai1" href="ai_improvizator" target="_top"></a>
  <a id="gd1" href="guardian" target="_top"></a>
</div>

<script id="cfg" type="application/json">__CFG__</script>

<script>
  const CFG   = JSON.parse(document.getElementById('cfg').textContent);
  const scene = document.getElementById('scene');
  const bg    = document.getElementById('bg');
  const playB = document.getElementById('playBtn');
  const muteB = document.getElementById('muteBtn');
  const bgVol = document.getElementById('bgVol');
  const fxVol = document.getElementById('fxVol');
  const bgLbl = document.getElementById('bgLbl');
  const fxLbl = document.getElementById('fxLbl');

  bgVol.value = CFG.INIT_BG;  bgLbl.textContent = CFG.INIT_BG + '%';
  fxVol.value = CFG.INIT_FX;  fxLbl.textContent = CFG.INIT_FX + '%';

  function toast(msg, ms=2200){
    const wrap=document.getElementById('toasts');
    const d=document.createElement('div'); d.className='toast show'; d.textContent=msg;
    wrap.appendChild(d);
    setTimeout(()=>{
      d.style.transition='opacity .5s, transform .5s';
      d.style.opacity=0; d.style.transform='translate(-50%,6px)';
      setTimeout(()=>wrap.removeChild(d),520);
    }, ms);
  }

  scene.addEventListener('mousemove', e=>{
    const x=(e.clientX/window.innerWidth)-.5, y=(e.clientY/window.innerHeight)-.5;
    scene.style.transform = `translate3d(${x * -10}px, ${y * -8}px, 0)`;
  });

  async function unlock(){
    try { await bg.play(); playB.textContent='Pause'; } catch(e) {}
  }
  window.addEventListener('click', unlock, {once:true});
  window.addEventListener('touchstart', unlock, {once:true});

  if (bg) bg.volume = (parseInt(bgVol.value,10)||0)/100;
  ['c2','e','g'].forEach(id=>{ const a=document.getElementById(id); if(a) a.volume=(parseInt(fxVol.value,10)||0)/100; });

  playB.addEventListener('click', ()=>{
    if(!bg) return;
    if(bg.paused){ bg.play(); playB.textContent='Pause'; toast('▶️ Play'); }
    else          { bg.pause(); playB.textContent='Play';  toast('⏸ Pause'); }
  });
  muteB.addEventListener('click', ()=>{
    if(!bg) return;
    bg.muted=!bg.muted; muteB.textContent=bg.muted?'Unmute':'Mute';
    toast(bg.muted?'🔇 Mute':'🔊 Unmute');
  });
  bgVol.addEventListener('input', e=>{
    const v=(parseInt(e.target.value,10)||0)/100; if(bg) bg.volume=v; bgLbl.textContent=Math.round(v*100)+'%';
  });
  fxVol.addEventListener('input', e=>{
    const v=(parseInt(e.target.value,10)||0)/100;
    ['c2','e','g'].forEach(id=>{ const a=document.getElementById(id); if(a) a.volume=v; });
    fxLbl.textContent=Math.round(v*100)+'%';
  });

  function playTone(id){
    const el=document.getElementById(id);
    if (el) { try{ el.currentTime=0; el.play(); return; }catch(_){} }
    try{
      const AC = new (window.AudioContext||window.webkitAudioContext)();
      const g=AC.createGain(); g.gain.value=(parseInt(fxVol.value,10)||0)/100; g.connect(AC.destination);
      const osc=AC.createOscillator(); osc.type='sine';
      osc.frequency.value = id==='c2'?130.81 : id==='e'?164.81 : 196.00;
      osc.connect(g); osc.start(); osc.stop(AC.currentTime+0.25);
    }catch(_){}
  }

  const texts = {
    c2: "✨ Kosmos te čuje — i ti sviraš njegovu pesmu.",
    e:  "🎶 Svaka misao je nota u simfoniji svesti.",
    g:  "💫 Tvoj zvuk ima oblik svetlosti u noći."
  };
  document.querySelectorAll('.star:not(.portal)').forEach(s=>{
    s.addEventListener('click', ()=>{
      const id=s.dataset.tone; playTone(id);
      toast(texts[id]||"⭐");
      s.animate([{transform:'scale(1)'},{transform:'scale(1.28)'},{transform:'scale(1)'}],{duration:340,easing:'ease-out'});
    });
  });

  // Modal & router
  const MOD = document.createElement('div');
  MOD.className='modal';
  MOD.innerHTML = `
    <div class="card">
      <h3 id="pm_title">Portal</h3>
      <p  id="pm_text">Opis</p>
      <div class="row">
        <button id="pm_cancel">Nazad</button>
        <button class="primary" id="pm_go">Uđi</button>
      </div>
    </div>`;
  document.body.appendChild(MOD);
  const PMT = MOD.querySelector('#pm_title');
  const PMX = MOD.querySelector('#pm_text');
  const GO  = MOD.querySelector('#pm_go');
  const BK  = MOD.querySelector('#pm_cancel');
  let current=null;

  const meta = {
    zvucni_balans:   {title:"Zvučni balans",   text:"Preset 432/528/639 Hz, fokus i harmonija."},
    ai_improvizator: {title:"AI Improvizator", text:"Interaktivni jam: čovek + AI."},
    guardian:        {title:"Guardian",        text:"Zaštitnički tonovi, mindful alarmi i fokus."}
  };

  function openModal(key){ current=key; const m=meta[key]||{title:"Portal",text:""}; PMT.textContent=m.title; PMX.textContent=m.text; MOD.classList.add('show'); }
  function closeModal(){ MOD.classList.remove('show'); current=null; }
  BK.addEventListener('click', closeModal);
  MOD.addEventListener('click', e=>{ if(e.target===MOD) closeModal(); });
  GO.addEventListener('click', ()=>{ if(current) goPortal(current); closeModal(); });

  document.querySelectorAll('.portal').forEach(s=>{
    s.addEventListener('click', ()=>{
      s.animate([{transform:'scale(1)'},{transform:'scale(1.28) rotate(6deg)'},{transform:'scale(1)'}],{duration:420,easing:'ease-out'});
      openModal(s.dataset.portal);
    });
  });

  function goPortal(key){
    const map = {zvucni_balans:'zb1', ai_improvizator:'ai1', guardian:'gd1'};
    const A = document.getElementById(map[key]);
    if (A) A.click(); else alert('Ne mogu da otvorim stranu — koristi levi meni.');
  }
</script>
"""

html_src = (html_src
            .replace("__IMG__", IMG)
            .replace("__AUDIO__", AUDIO_ROOT)
            .replace("__CFG__", cfg_json))

st_html(html_src, height=760, scrolling=False)
