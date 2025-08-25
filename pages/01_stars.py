# pages/01_stars.py — TONOSAI | Kosmičke Zvezde
import streamlit as st
import streamlit.components.v1 as components
import base64, os

st.set_page_config(page_title="TONOSAI | Kosmičke Zvezde", page_icon="🌌", layout="wide")

# ---------- Sidebar ----------
with st.sidebar:
    st.subheader("🔊 Tonovi na klik 🎹")

    map_mode = st.selectbox(
        "Mapiranje tonova",
        ["po veličini zvezde (3 tona)", "nasumično (3 tona)"],
        index=0,
    )

    # Skala za klik zvezda
    scale_mode = st.selectbox(
        "Skala za klik zvezda",
        ["Triada C (1–5/4–3/2)", "Pentatonika C", "Dorska (D Dorian)"],
        index=1,
    )

    # Tri osnovna uzorka (C, E, G) — referenca C=528Hz
    default_1 = "static/audio/c2_note.ogg"
    default_2 = "static/audio/e3_note.ogg"
    default_3 = "static/audio/g3_note.ogg"
    audio1 = st.text_input("Audio 1 — C (528 ref)", value=default_1)
    audio2 = st.text_input("Audio 2 — E", value=default_2)
    audio3 = st.text_input("Audio 3 — G", value=default_3)

    st.markdown("---")
    master_vol  = st.slider("Master glasnoća", 0.1, 1.0, 0.55, 0.01)
    env_attack  = st.slider("Attack (s)", 0.00, 1.00, 0.12, 0.01)
    env_release = st.slider("Release (s)", 0.05, 2.00, 0.70, 0.05)
    pad_on      = st.toggle("Ambijentalni PAD sloj", True)
    pad_tail    = st.slider("PAD tail (s)", 0.5, 6.0, 3.0, 0.1)

    st.markdown("---")
    arp_bpm = st.slider("Arp tempo (BPM)", 30, 120, 60, 1)

    st.markdown("---")
    const_shape = st.selectbox(
        "Oblik konstelacije",
        ["Trougao", "Luk", "Krug", "Orion (pojas)", "Aquila (Altair)", "Trio (gore-desno)", "Deltoid", "Mali luk"],
        index=0,
    )
    hue         = st.slider("Boja konstelacije (hue)", 0, 360, 45)
    const_scale = st.slider("Veličina konstelacije (%)", 30, 140, 52)
    const_x     = st.slider("Pozicija X (%)", 0, 100, 50)
    const_y     = st.slider("Pozicija Y (%)", 0, 100, 28)

    st.markdown("---")
    count          = st.slider("Broj zvezdica", 20, 300, 140, 10)
    canvas_height  = st.slider("Visina platna (px)", 300, 1200, 860, 20)
    min_size       = st.slider("Min. veličina (px)", 1, 6, 2)
    max_size       = st.slider("Max. veličina (px)", 3, 14, 7)
    twinkle_speed  = st.slider("Brzina treperenja (s)", 0.8, 5.0, 1.8, 0.1)
    float_speed    = st.slider("Brzina lelujanja (s)", 2.0, 12.0, 5.0, 0.1)
    amplitude      = st.slider("Amplituda lelujanja (px)", 1, 16, 4)
    jitter         = st.slider("Random varijacija (%)", 0, 60, 25)
    pulse_intensity= st.slider("Intenzitet svetlucanja", 30, 100, 80)

    st.markdown("---")
    enable_clicks  = st.toggle("Aktiviraj klik interakcije", True)
    show_messages  = st.toggle("Prikaži poetske poruke", True)
    show_help      = st.toggle("Prikaži uputstvo ispod platna", False)

# ---------- Helpers ----------
def read_audio_bytes(path: str):
    p = (path or "").strip()
    if not p:
        return None
    if os.path.exists(p):
        try:
            with open(p, "rb") as f:
                return f.read()
        except Exception:
            return None
    return None

def to_data_url(path: str):
    p = (path or "").strip()
    if os.path.exists(p):
        try:
            with open(p, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            mime = "audio/ogg" if p.lower().endswith(".ogg") else "audio/mpeg"
            return f"data:{mime};base64,{b64}"
        except Exception:
            return ""
    return p  # relativan URL ostaje

bytes_list    = [read_audio_bytes(x) for x in [audio1, audio2, audio3]]
js_audio_list = [to_data_url(x)     for x in [audio1, audio2, audio3]]

missing = [
    f"Audio {i+1}: {p}"
    for i, (p, b) in enumerate(zip([audio1, audio2, audio3], bytes_list))
    if b is None and (p or "").strip()
]

poems = [
    "Svetlost je tihi ton srca.",
    "Udiši—izdahni: svemir korača s tobom.",
    "528 je zrak koji grli tišinu.",
    "Mir je geometrija svetla.",
    "Tvoj ritam je karta neba.",
]

# ---- Skale (just intonation) ----
def ratios_for(scale_name: str):
    if "Pentatonika" in scale_name:
        return [1.0, 9/8, 5/4, 3/2, 5/3]
    if "Dorska" in scale_name:
        return [1.0, 9/8, 6/5, 4/3, 3/2, 8/5, 9/5]
    return [1.0, 5/4, 3/2]  # Triada C

scale_ratios = [round(x, 6) for x in ratios_for(scale_mode)]

# ---------- HTML/CSS/JS ----------
html = f"""
<div id='tonosai-sky' class='sky'>
  <svg id='constellation' class='constellation' viewBox='0 0 100 100' preserveAspectRatio='none'>
    <g id='const-g'>
      <line id='line1' x1='30' y1='65' x2='70' y2='65'/>
      <line id='line2' x1='30' y1='65' x2='50' y2='30'/>
      <line id='line3' x1='50' y1='30' x2='70' y2='65'/>
      <circle id='c1' cx='30' cy='65' r='1.8'/>
      <circle id='c2' cx='50' cy='30' r='1.8'/>
      <circle id='c3' cx='70' cy='65' r='1.8'/>
    </g>
  </svg>
</div>

<div class='controls'>
  <a href='/' id='btn-home' class='btn' target='_top'>🏠 Studio</a>
  <button id='btn-cmaj528' title='C–E–G (C=528 Hz)'>▶︎ C-dur 528</button>
  <button id='btn-cmaj432' title='C–E–G (C=432 Hz)'>▶︎ C-dur 432</button>
  <button id='btn-arp'  title='Arpeđo (blagi strum)'>♫ Arp</button>
  <button id='btn-full' title='Prikaži preko celog ekrana'>⛶ Fullscreen</button>
  <button id='btn-exit' title='Izađi iz fullscreen-a' style='display:none'>✕ Izađi</button>
  <button id='btn-rec'  title='Snimi svirku'>⏺ Rec</button>
  <button id='btn-stop' title='Zaustavi snimanje' disabled>⏹ Stop</button>
  <a id='dl-wav' download='tonosai.webm' style='display:none;margin-left:8px'>⬇️ Preuzmi WebM</a>
</div>

<style>
:root {{ --fsBarH: 56px; }}
.sky {{
  position: relative; width: 100%; height: {canvas_height}px; overflow: hidden;
  border-radius: 18px; box-shadow: 0 8px 30px rgba(0,0,0,0.25);
  background:
    radial-gradient(ellipse at 50% 30%, rgba(255,255,255,0.06), rgba(0,0,0,0.02) 40%, rgba(0,0,0,0.0) 60%),
    linear-gradient(180deg, #04060b 0%, #070914 40%, #0a0f1f 100%);
}}
.controls {{ position: relative; z-index: 1001; display:flex; gap:8px; flex-wrap:wrap; }}

body.fs .sky {{
  position: fixed; inset: 0; width: 100vw;
  height: calc(100vh - var(--fsBarH));
  margin-top: var(--fsBarH);
  z-index: 9999; border-radius: 0; box-shadow: none;
}}
body.fs .controls {{
  position: fixed; right: 14px; top: 12px; z-index: 10000; display: flex; gap: 8px;
}}

/* SVG preko zvezda, ali da ne blokira prazna mesta */
.constellation {{ position: absolute; inset: 0; z-index: 2; pointer-events: none; }}
.constellation line {{
  pointer-events: stroke; cursor: grab;
  stroke: hsla({hue}, 100%, 80%, 0.95);
  stroke-width: 2.2; stroke-linecap: round;
  filter: drop-shadow(0 0 10px hsla({hue}, 100%, 70%, 0.9));
}}
.constellation circle {{
  pointer-events: all; cursor: grab;
  fill: #fff; stroke: hsla({hue}, 100%, 70%, 0.9); stroke-width: 0.8;
  filter: drop-shadow(0 0 8px hsla({hue}, 100%, 70%, 0.85));
}}

.star {{
  position: absolute; background: white; border-radius: 50%; opacity: 0.85;
  filter: drop-shadow(0 0 6px rgba(255,255,255,0.35)); cursor: pointer; z-index: 1;
}}
.msg {{
  position: absolute; color: rgba(255,255,255,0.92);
  font-family: system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  font-size: 12px; pointer-events: none; transform: translate(-50%,-160%);
  opacity: 0; animation: fadeRise 1.8s ease forwards;
  text-shadow: 0 2px 10px rgba(0,0,0,0.6); white-space: nowrap;
}}
@keyframes fadeRise {{
  0%   {{ opacity: 0; transform: translate(-50%,-120%); }}
  15%  {{ opacity: 1; }}
  100% {{ opacity: 0; transform: translate(-50%,-220%); }}
}}
@keyframes twinkle {{
  0%,100% {{ opacity: 0.25; }}
  50%     {{ opacity: {pulse_intensity/100:.2f}; }}
}}
@keyframes float {{
  0%,100% {{ transform: translateY(0px); }}
  50%     {{ transform: translateY(-{amplitude}px); }}
}}
@keyframes breathe {{
  0%,100% {{ opacity: 0.55; }}
  50%     {{ opacity: 0.95; }}
}}
</style>

<script>
(() => {{
  function showErr(e) {{
    const box = document.createElement('pre');
    box.textContent = 'TONOSAI JS error:\\n' + (e && (e.stack||e.message||e));
    box.style.cssText = 'position:fixed;left:10px;bottom:10px;max-width:70vw;max-height:40vh;overflow:auto;background:#210;padding:12px 14px;border:1px solid #843;border-radius:8px;color:#fff;z-index:100000;font:12px/1.4 ui-monospace,Consolas,monospace;';
    document.body.appendChild(box);
  }}

  try {{
    // ===== Parametri iz Pythona =====
    const N           = {count};
    const minSize     = {min_size};
    const maxSize     = {max_size};
    const twinkle     = {twinkle_speed};
    const floatS      = {float_speed};
    const jitterPct   = {jitter} / 100.0;
    const enableClicks= {str(enable_clicks).lower()};
    const showMessages= {str(show_messages).lower()};
    const poems       = {poems};
    const audioList   = {js_audio_list};
    const masterVol   = {master_vol};
    const envA        = {env_attack};
    const envR        = {env_release};
    const padOn       = {str(pad_on).lower()};
    const padTail     = {pad_tail};
    const bpm         = {arp_bpm};
    const shapeName   = {repr(const_shape)};
    let   S  = {const_scale} / 100.0;
    let   PX = {const_x};
    let   PY = {const_y};
    const scale       = {scale_ratios};

    // ===== Elementi =====
    const sky  = document.getElementById('tonosai-sky');
    const svg  = document.getElementById('constellation');
    const g    = document.getElementById('const-g');
    const c1   = document.getElementById('c1');
    const c2   = document.getElementById('c2');
    const c3   = document.getElementById('c3');
    const l1   = document.getElementById('line1');
    const l2   = document.getElementById('line2');
    const l3   = document.getElementById('line3');
    const btn528 = document.getElementById('btn-cmaj528');
    const btn432 = document.getElementById('btn-cmaj432');
    const btnArp = document.getElementById('btn-arp');
    const btnFull= document.getElementById('btn-full');
    const btnExit= document.getElementById('btn-exit');
    const btnRec = document.getElementById('btn-rec');
    const btnStop= document.getElementById('btn-stop');
    const dlWav  = document.getElementById('dl-wav');

    if (!sky) return;

    // ===== Konstelacija =====
    function setAttr(el, a) {{ for (const k in a) el.setAttribute(k, a[k]); }}
    function updateLines() {{
      setAttr(l1, {{x1:c1.getAttribute('cx'), y1:c1.getAttribute('cy'), x2:c3.getAttribute('cx'), y2:c3.getAttribute('cy')}});
      setAttr(l2, {{x1:c1.getAttribute('cx'), y1:c1.getAttribute('cy'), x2:c2.getAttribute('cx'), y2:c2.getAttribute('cy')}});
      setAttr(l3, {{x1:c2.getAttribute('cx'), y1:c2.getAttribute('cy'), x2:c3.getAttribute('cx'), y2:c3.getAttribute('cy')}});
    }}
    function applyShape(name) {{
      if (name === 'Luk') {{
        setAttr(c1, {{cx:30, cy:70}}); setAttr(c2, {{cx:50, cy:55}}); setAttr(c3, {{cx:70, cy:70}});
      }} else if (name === 'Krug') {{
        const R=24,cx=50,cy=50,a1=-100*Math.PI/180,a2=-40*Math.PI/180,a3=80*Math.PI/180;
        setAttr(c1, {{cx:cx+R*Math.cos(a1), cy:cy+R*Math.sin(a1)}});
        setAttr(c2, {{cx:cx+R*Math.cos(a2), cy:cy+R*Math.sin(a2)}});
        setAttr(c3, {{cx:cx+R*Math.cos(a3), cy:cy+R*Math.sin(a3)}});
      }} else if (name === 'Orion (pojas)') {{
        setAttr(c1, {{cx:40, cy:56}}); setAttr(c2, {{cx:50, cy:50}}); setAttr(c3, {{cx:60, cy:44}});
      }} else if (name === 'Aquila (Altair)') {{
        setAttr(c1, {{cx:45, cy:35}}); setAttr(c2, {{cx:62, cy:28}}); setAttr(c3, {{cx:70, cy:42}});
      }} else if (name === 'Trio (gore-desno)') {{
        setAttr(c1, {{cx:60, cy:35}}); setAttr(c2, {{cx:78, cy:30}}); setAttr(c3, {{cx:82, cy:46}});
      }} else if (name === 'Deltoid') {{
        setAttr(c1, {{cx:30, cy:60}}); setAttr(c2, {{cx:50, cy:28}}); setAttr(c3, {{cx:70, cy:62}});
      }} else if (name === 'Mali luk') {{
        setAttr(c1, {{cx:40, cy:60}}); setAttr(c2, {{cx:50, cy:54}}); setAttr(c3, {{cx:60, cy:60}});
      }} else {{
        setAttr(c1, {{cx:30, cy:65}}); setAttr(c2, {{cx:50, cy:30}}); setAttr(c3, {{cx:70, cy:65}});
      }}
      updateLines();
    }}
    function updateTransform() {{
      g.setAttribute('transform', `translate(${{PX}}, ${{PY}}) scale(${{S}}) translate(-50, -50)`);
    }}
    applyShape(shapeName);
    updateTransform();

    // drag/scale
    function toLocal(evt) {{
      const pt = svg.createSVGPoint(); pt.x = evt.clientX; pt.y = evt.clientY;
      const inv = g.getScreenCTM().inverse();
      return pt.matrixTransform(inv);
    }}
    const drag = {{ kind:null, node:null, offX:0, offY:0, startX:0, startY:0, startPX:PX, startPY:PY, startS:S }};
    function beginDrag(e, forceKind) {{
      const t = e.target;
      const kind = forceKind || (t.tagName === 'circle' ? 'node' : (e.altKey ? 'scale' : 'move'));
      drag.kind = kind;
      if (kind === 'node') {{
        drag.node = t; const p = toLocal(e);
        drag.offX = p.x - parseFloat(t.getAttribute('cx'));
        drag.offY = p.y - parseFloat(t.getAttribute('cy'));
      }} else {{
        const p = toLocal(e);
        drag.startX = p.x; drag.startY = p.y;
        drag.startPX = PX; drag.startPY = PY; drag.startS = S;
      }}
      try {{ svg.setPointerCapture(e.pointerId); }} catch(_) {{}}
    }}
    function doDrag(e) {{
      if (!drag.kind) return;
      if (drag.kind === 'node') {{
        const p = toLocal(e);
        const nx = (p.x - drag.offX).toFixed(2), ny = (p.y - drag.offY).toFixed(2);
        drag.node.setAttribute('cx', nx); drag.node.setAttribute('cy', ny); updateLines();
      }} else if (drag.kind === 'move') {{
        const p = toLocal(e); PX = drag.startPX + (p.x - drag.startX); PY = drag.startPY + (p.y - drag.startY); updateTransform();
      }} else if (drag.kind === 'scale') {{
        const p = toLocal(e); const cx=50, cy=50;
        const d0=Math.max(5, Math.hypot(drag.startX-cx, drag.startY-cy));
        const d1=Math.hypot(p.x-cx, p.y-cy);
        S = Math.min(1.4, Math.max(0.1, drag.startS*(d1/d0))); updateTransform();
      }}
    }}
    function endDrag(e) {{ drag.kind=null; drag.node=null; try {{ svg.releasePointerCapture(e.pointerId); }} catch(_) {{}} }}
    [l1,l2,l3].forEach(el => el?.addEventListener('pointerdown', e => beginDrag(e, 'move')));
    [c1,c2,c3].forEach(el => el?.addEventListener('pointerdown', e => beginDrag(e, 'node')));
    svg.addEventListener('pointermove', doDrag);
    svg.addEventListener('pointerup', endDrag);
    svg.addEventListener('pointerleave', endDrag);
    svg.addEventListener('wheel', (e)=>{{ e.preventDefault(); const k=(e.deltaY<0)?1.05:0.95; S=Math.min(1.4, Math.max(0.1, S*k)); updateTransform(); }}, {{passive:false}});

    // ===== Zvezde =====
    function rand(min, max)  {{ return Math.random() * (max - min) + min; }}
    function randInt(min, max){{ return Math.floor(Math.random() * (max - min + 1)) + min; }}
    const midThreshold = (minSize + maxSize) / 2.0;

    for (let i = 0; i < N; i++) {{
      const s = document.createElement('div'); s.className='star';
      s.style.left = rand(0,100).toFixed(3)+'%'; s.style.top  = rand(0,100).toFixed(3)+'%';
      const size = randInt(minSize, maxSize); s.style.width=size+'px'; s.style.height=size+'px';
      const tVar = twinkle*(1 + (Math.random()*2-1)*jitterPct);
      const fVar = floatS*(1 + (Math.random()*2-1)*jitterPct);
      const d = rand(0, twinkle);
      s.style.animation = `twinkle ${{tVar}}s ease-in-out ${{d}}s infinite, float ${{fVar}}s ease-in-out ${{(d/2).toFixed(2)}}s infinite`;
      if (enableClicks) s.addEventListener('click', (ev)=> playStar(size, ev));
      sky.appendChild(s);
    }}

    // ===== WebAudio =====
    let AC = null; let master = null; const buffers = {{}};
    async function ctx() {{
      if (!AC) {{
        AC = new (window.AudioContext||window.webkitAudioContext)();
        master = AC.createGain(); master.gain.value = masterVol; master.connect(AC.destination);
      }}
      return AC;
    }}
    async function fetchBuffer(url) {{
      const ac = await ctx(); if (!url) return null;
      if (buffers[url]) return buffers[url];
      const res = await fetch(url); const arr = await res.arrayBuffer();
      const buf = await ac.decodeAudioData(arr); buffers[url]=buf; return buf;
    }}
    function envNode(ac, a, r) {{
      const g = ac.createGain();
      g.gain.setValueAtTime(0, ac.currentTime);
      g.gain.linearRampToValueAtTime(1, ac.currentTime + a);
      g.gain.linearRampToValueAtTime(0, ac.currentTime + a + r);
      return g;
    }}
    function play(buf, rate=1.0, vol=0.85, a=envA, r=envR) {{
      const ac = AC; if (!ac||!buf) return;
      const src = ac.createBufferSource(); src.buffer = buf; src.playbackRate.value = rate;
      const e = envNode(ac, a, r); const gG = ac.createGain(); gG.gain.value = vol;
      src.connect(e).connect(gG).connect(master); src.start();
    }}
    const ratios528 = [1.0, 1.25, 1.5];
    const ratios432 = [432/528, (432/528)*1.25, (432/528)*1.5];
    const baseC  = audioList[0] || '';
    const srcs   = [ audioList[0]||'', audioList[1]||baseC, audioList[2]||baseC ];
    function msPerBeat() {{ return 60000 / Math.max(30, Math.min(200, bpm)); }}

    async function playChord(ratios, strum=false) {{
      try {{ await ctx(); }} catch(_) {{ return; }}
      const bufs = await Promise.all(srcs.map(u => u ? fetchBuffer(u) : null));
      const gap = strum ? msPerBeat()/2 : 0;
      for (let i=0;i<3;i++) {{
        const b = bufs[i]; if (!b) continue;
        if (gap>0) await new Promise(r=>setTimeout(r, i*gap));
        play(b, ratios[i], 0.75, envA, envR);
        if (padOn) play(b, ratios[i], 0.35, envA*1.5, padTail);
      }}
      [c1,c2,c3].forEach(n => n.style.animation = `breathe 1.2s ease-in-out 0s 1`);
    }}

    function playStar(size, ev) {{
      const pick = scale[Math.floor(Math.random()*scale.length)];
      ctx().then(async () => {{
        const b = await fetchBuffer(baseC || srcs[0]);
        play(b, pick, 0.8);
        if (showMessages) {{
          const rect = sky.getBoundingClientRect();
          const msg = document.createElement('div'); msg.className='msg';
          msg.style.left=(ev.clientX-rect.left)+'px'; msg.style.top=(ev.clientY-rect.top)+'px';
          msg.textContent = poems[Math.floor(Math.random()*poems.length)];
          sky.appendChild(msg); setTimeout(()=>msg.remove(),1800);
        }}
      }});
    }}

    // Dugmad
    btn528?.addEventListener('click', ()=> playChord(ratios528,false));
    btn432?.addEventListener('click', ()=> playChord(ratios432,false));
    btnArp ?.addEventListener('click', ()=> playChord(ratios528,true));

    // ===== Fullscreen =====
    async function enterRealFullscreen(el) {{
      if (el.requestFullscreen) return el.requestFullscreen();
      if (el.webkitRequestFullscreen) return el.webkitRequestFullscreen();
      if (el.msRequestFullscreen) return el.msRequestFullscreen();
      throw new Error('Fullscreen API not available');
    }}
    function enterCssFullscreen() {{ document.body.classList.add('fs'); btnExit.style.display = 'inline-block'; }}
    function exitCssFullscreen()  {{ document.body.classList.remove('fs'); btnExit.style.display = 'none'; }}

    btnFull?.addEventListener('click', async () => {{
      try {{
        await enterRealFullscreen(document.documentElement);
        btnExit.style.display = 'inline-block';
      }} catch (_) {{
        enterCssFullscreen();
      }}
    }});
    btnExit?.addEventListener('click', async () => {{
      try {{ await (document.exitFullscreen?.() || document.webkitExitFullscreen?.() || document.msExitFullscreen?.()); }} catch(_) {{}}
      exitCssFullscreen();
    }});
    ['fullscreenchange','webkitfullscreenchange','msfullscreenchange'].forEach(ev => {{
      document.addEventListener(ev, () => {{
        const fsOn = !!(document.fullscreenElement || document.webkitFullscreenElement || document.msFullscreenElement);
        btnExit.style.display = fsOn ? 'inline-block' : 'none';
        if (!fsOn) exitCssFullscreen();
      }});
    }});

    // ===== Snimanje (MediaRecorder → WebM) =====
    let mediaRec = null; let chunks = [];
    btnRec?.addEventListener('click', async () => {{
      try {{
        await ctx();
        const dest = AC.createMediaStreamDestination();
        master.connect(dest);
        mediaRec = new MediaRecorder(dest.stream);
        chunks = [];
        mediaRec.ondataavailable = (e)=>{{ if (e.data && e.data.size>0) chunks.push(e.data); }};
        mediaRec.onstop = async ()=>{{
          const blob = new Blob(chunks, {{type:'audio/webm'}});
          const url  = URL.createObjectURL(blob);
          dlWav.href = url; dlWav.style.display = 'inline-block';
        }};
        mediaRec.start();
        btnRec.disabled = true; btnStop.disabled = false; dlWav.style.display='none';
      }} catch (e) {{
        console.warn('MediaRecorder not available:', e);
      }}
    }});
    btnStop?.addEventListener('click', ()=>{{ try {{ mediaRec?.stop(); }} catch(_e) {{}} btnRec.disabled=false; btnStop.disabled=true; }});
  }} catch(e) {{
    showErr(e);
  }}
}})();
</script>
"""

# ---------- Layout ----------
st.markdown("<style>.main .block-container { padding-top: 0.8rem; padding-bottom: 0.6rem; }</style>", unsafe_allow_html=True)
st.title("✨ TONOSAI — Kosmičke Zvezde")
components.html(html, height=canvas_height + 120)

# Dijagnostika
if missing:
    items = "- " + "\n- ".join(missing)
    st.warning("Fajl nije pronađen (proveri putanju/razmake):\n\n" + items)

with st.expander("🔉 Test tonova (ručno)"):
    c1_col, c2_col, c3_col = st.columns(3)
    for i, (lbl, b) in enumerate(zip(["C", "E", "G"], bytes_list)):
        with (c1_col if i == 0 else c2_col if i == 1 else c3_col):
            if b:
                st.audio(b, format="audio/ogg")
            else:
                st.caption(f"Audio {i+1} ({lbl}) nije pronađen")

if show_help:
    st.markdown(
        """
**Napomene**
- C–E–G je u *just intonation* (1 : 5/4 : 3/2); „C-dur 528/432“ su iste razmere sa različitim referencama.
- *Skala za klik zvezda* bira odnos (Triada/Pentatonika/Dorska) i svaka zvezda nasumično svira jednu notu te skale.
- PAD sloj blago produžava ton; Arp tempo utiče na „strum“.
- Interakcije: linije = pomeri figuru; krugovi = menjaj čvor; **ALT+prevuci = skaliraj**; točkić = zoom.
- Tastatura: **R** (reset), **F** (fullscreen), **L** (lock konstelacije).
        """,
        unsafe_allow_html=True,
    )
