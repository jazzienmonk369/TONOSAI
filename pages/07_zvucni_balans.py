# pages/07_zvucni_balans.py — Zvučni balans (432/528/639 Hz)

import streamlit as st
import streamlit.components.v1 as components
from lib.ui import header_badges, footer
import boot  # stil

st.set_page_config(page_title="TONOSAI — Zvučni balans", page_icon="🌀", layout="wide")
header_badges()
st.title("🌀 Zvučni balans")
st.page_link("vizija_tonosai.py", label="← Home")


col1, col2, col3 = st.columns([2,1,1])

with col1:
    preset = st.selectbox("Preset", ["432 Hz — umirenje", "528 Hz — obnova", "639 Hz — odnosi"], index=1)
    base = {"432":432, "528":528, "639":639}[preset.split()[0]]
    freq = st.slider("Frekvencija (Hz)", 100, 1200, base, 1)
    wave = st.selectbox("Talas", ["sine", "triangle", "sawtooth", "square"], index=0)
    vol  = st.slider("Jačina", 0.0, 1.0, 0.35, 0.01)
with col2:
    lfo_on = st.toggle("Pulse (disanje)", True)
    lfo_hz = st.slider("Pulse brzina (Hz)", 0.05, 3.0, 0.2, 0.01, disabled=not lfo_on)
with col3:
    stereo = st.toggle("Binaural (± beat)", False)
    beat   = st.slider("Beat (Hz)", 0.0, 10.0, 4.0, 0.1, disabled=not stereo)
    dur    = st.slider("Fade (s)", 0.0, 4.0, 1.0, 0.1)

components.html(f"""
<div style="display:flex;gap:10px;align-items:center;margin:.5rem 0 1rem 0">
  <button id="play" style="background:#1b2e52;color:#e8f2ff;border:1px solid #3a4e75;padding:8px 14px;border-radius:12px;cursor:pointer">Play</button>
  <button id="stop" style="background:#0f1f39;color:#e8f2ff;border:1px solid #3a4e75;padding:8px 14px;border-radius:12px;cursor:pointer">Stop</button>
  <span id="state" style="color:#fff;opacity:.85;margin-left:8px">Ready</span>
</div>

<canvas id="viz" height="120" style="width:100%;border-radius:12px;background:linear-gradient(180deg,#04060b,#0b1326)"></canvas>

<script>
(() => {{
  const F_START = {freq};           // Hz
  const WAVE    = "{wave}";
  const VOL     = {vol};
  const FADE    = {dur};            // seconds
  const LFO_ON  = {str(lfo_on).lower()};
  const LFO_HZ  = {lfo_hz};
  const STEREO  = {str(stereo).lower()};
  const BEAT    = {beat};           // Hz diff between ch.

  let AC=null, mL=null, mR=null, oL=null, oR=null, lfo=null, vizAnalyser=null, raf=0;

  const state = document.getElementById('state');
  const cv = document.getElementById('viz');
  const cx = cv.getContext('2d');

  function fit(){{
    const w=cv.clientWidth|0, h=cv.height;
    cv.width = w*devicePixelRatio; cx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);
  }} new ResizeObserver(fit).observe(cv); fit();

  function ac(){{
    if(!AC){{
      AC = new (window.AudioContext||window.webkitAudioContext)();
    }}
    return AC;
  }}

  function makeNode(freq, pan=0){{
    const a = ac();
    const osc = a.createOscillator(); osc.type=WAVE; osc.frequency.value=freq;
    const g = a.createGain(); g.gain.value=0.0001;             // fade-in
    const p = a.createStereoPanner ? a.createStereoPanner() : null;
    const out = p ? (osc.connect(g).connect(p).connect(a.destination), p) : (osc.connect(g).connect(a.destination), g);
    // viz
    vizAnalyser = vizAnalyser || a.createAnalyser(); vizAnalyser.fftSize=512;
    g.connect(vizAnalyser);

    if(p) p.pan.value = pan;
    osc.start();
    return {{osc, g}};
  }}

  function fadeTo(g, target, seconds){{
    const now = AC.currentTime;
    g.gain.cancelScheduledValues(now);
    g.gain.setValueAtTime(g.gain.value, now);
    g.gain.linearRampToValueAtTime(target, now + Math.max(0.001, seconds));
  }}

  function start(){{
    ac().resume();
    const fL = F_START - (STEREO ? BEAT/2 : 0);
    const fR = F_START + (STEREO ? BEAT/2 : 0);

    oL = makeNode(fL, -0.5);
    oR = makeNode(fR, +0.5);
    mL = oL.g; mR = oR.g;

    fadeTo(mL, VOL, FADE);
    fadeTo(mR, VOL, FADE);

    // LFO (pulse amplitude)
    if (LFO_ON){{
      const a=AC, l= a.createOscillator(); l.type='sine'; l.frequency.value=LFO_HZ;
      const lg=a.createGain(); lg.gain.value = VOL*0.5;
      l.connect(lg); lg.connect(mL.gain); lg.connect(mR.gain);
      l.start(); lfo=l;
    }}

    // vizualizacija
    const data = new Uint8Array(vizAnalyser.frequencyBinCount);
    const draw = () => {{
      raf=requestAnimationFrame(draw);
      vizAnalyser.getByteTimeDomainData(data);
      const w=cv.width/devicePixelRatio, h=cv.height/devicePixelRatio;
      cx.clearRect(0,0,w,h);
      cx.strokeStyle='rgba(255,255,255,.9)'; cx.lineWidth=2; cx.beginPath();
      for(let i=0;i<data.length;i++){{ 
        const x = i/data.length * w;
        const y = (data[i]/255)*h;
        i? cx.lineTo(x,y) : cx.moveTo(x,y);
      }} cx.stroke();
    }}; draw();

    state.textContent = 'Playing  ' + F_START + ' Hz'; 
  }}

  function stop(){{
    if(!AC) return;
    try{{ fadeTo(mL, 0.0001, FADE); fadeTo(mR, 0.0001, FADE); }}catch(_){{
      // ignore
    }}
    setTimeout(()=>{{
      try{{ oL.osc.stop(); oR.osc.stop(); }}catch(_){{}}
      if(lfo) try{{ lfo.stop(); }}catch(_){{}}
      oL=oR=mL=mR=lfo=null;
      if(raf) cancelAnimationFrame(raf), raf=0;
      state.textContent='Stopped';
    }}, FADE*1000 + 60);
  }}

  document.getElementById('play').onclick = ()=>start();
  document.getElementById('stop').onclick = ()=>stop();
  window.addEventListener('keydown', e=>{{ if(e.code==='Space'){{ e.preventDefault(); (oL?stop():start()); }} }});
}})();
</script>
""", height=260)

st.page_link("app.py", label="← Home")
footer()
