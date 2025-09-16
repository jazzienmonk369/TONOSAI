import streamlit as st
import boot


st.set_page_config(
    page_title="TONOSAI — Zvezde",         # slobodno menjaj naslov po stranici
    page_icon="static/favicon.png",
    layout="wide"
)
from lib.ui import header_badges, footer

header_badges()


# pages/05_game.py — TONOSAI | Igra: Zvezdani Sakupljač (starburst + comet boss)
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="TONOSAI | Igra", page_icon="🎮", layout="wide")

# ---- Sidebar: podešavanja ----
with st.sidebar:
    st.subheader("🎮 Igra — podešavanja")

    scale_mode = st.selectbox(
        "Skala zvezda",
        [
            "Triada C (1–5/4–3/2)",
            "Pentatonika C",
            "Dorska (D Dorian)",
            "Solfeggio (396–528–639–741–852)"
        ],
        index=1,
    )
    base_ref = st.slider("Ref. frekvencija C (Hz)", 220, 640, 528, 1)
    speed    = st.slider("Brzina igrača", 2, 12, 6)
    density  = st.slider("Gustina zvezda (manje=više)", 5, 60, 15)
    master   = st.slider("Glasnoća", 0.0, 1.0, 0.6, 0.01)
    canvas_h = st.slider("Visina platna (px)", 300, 900, 520, 10)

    st.markdown("---")
    waves_every = st.slider("Talasi (starburst/boss) na N sekundi", 6, 30, 12)
    boss_chance = st.slider("Šansa da talas bude KOMET (%)", 0, 100, 35)

# ---- Skale / palete ----
def ratios_for(name: str):
    if "Pentatonika" in name: return [1.0, 9/8, 5/4, 3/2, 5/3]
    if "Dorska" in name:      return [1.0, 9/8, 6/5, 4/3, 3/2, 8/5, 9/5]
    return [1.0, 5/4, 3/2]  # triada

def scale_freqs(scale_name: str, ref: float):
    if "Solfeggio" in scale_name:
        # klasični set (bez 963 ovde da ostane mekano)
        return [396.0, 417.0, 432.0, 528.0, 639.0, 741.0, 852.0]
    # ostale — preko odnosa
    return [round(ref*r, 3) for r in ratios_for(scale_name)]

def palette_for(scale_name: str):
    # [nebogradientTop, nebogradientBottom, playerHue]
    if "Solfeggio" in scale_name: return ("#0a121a", "#0f1f14", 95)   # zlatno-zelene
    if "Pentatonika" in scale_name: return ("#090c18", "#0a0f1f", 45) # toplo zvezdano
    if "Dorska" in scale_name: return ("#060915", "#101426", 220)     # hladnije plave
    return ("#070914", "#0a0f1f", 35)                                  # triada—med toplo

scale_hz = scale_freqs(scale_mode, base_ref)
bg_top, bg_bot, hue_player = palette_for(scale_mode)

# ---- HTML / CSS / JS ----
html = f"""
<div id="wrap" style="position:relative;width:100%;">
  <canvas id="game" style="width:100%;height:{canvas_h}px;border-radius:16px;display:block;background:
    radial-gradient(circle at 50% 30%, rgba(255,255,255,0.04), rgba(0,0,0,0.0) 62%),
    linear-gradient(180deg,{bg_top},{bg_bot});
    box-shadow:0 10px 28px rgba(0,0,0,0.38)"></canvas>

  <div id="hud" style="position:absolute;left:12px;top:10px;color:#fff;font:500 14px/1.4 system-ui">
    ⭐ Score: <b id="sc">0</b>
    <span id="mult" style="margin-left:10px;opacity:.85"></span>
  </div>

  <div id="btns" style="position:absolute;right:12px;top:10px;display:flex;gap:8px;flex-wrap:wrap;">
    <a href="/" target="_top" style="background:#111;border:1px solid #333;border-radius:10px;padding:6px 10px;color:#fff;text-decoration:none">🏠 Studio</a>
    <button id="btn-tilt"  style="background:#111;border:1px solid #333;border-radius:10px;padding:6px 10px;color:#fff;cursor:pointer">🎯 Tilt</button>
    <button id="btn-rec"   style="background:#111;border:1px solid #333;border-radius:10px;padding:6px 10px;color:#fff;cursor:pointer">⏺ Rec</button>
    <button id="btn-stop"  style="background:#111;border:1px solid #333;border-radius:10px;padding:6px 10px;color:#fff;cursor:pointer" disabled>⏹ Stop</button>
    <a id="dl-webm" download="tonosai_game.webm" style="display:none;background:#111;border:1px solid #333;border-radius:10px;padding:6px 10px;color:#fff;text-decoration:none">⬇️ WebM</a>
  </div>

  <!-- tilt indikator -->
  <div id="tiltDot" style="position:absolute;right:18px;top:52px;width:10px;height:10px;border-radius:50%;background:#666;box-shadow:0 0 8px rgba(255,255,255,.35);opacity:.75"></div>
</div>

<script>
(()=>{{
  // ===== Config iz Pythona =====
  const scaleHz   = {scale_hz};
  const speedBase = {speed};
  const density   = {density};      // manji = više
  const masterV   = {master};
  const H         = {canvas_h};
  const wavesEveryMs = {int(waves_every*1000)};
  const bossChance    = {boss_chance}/100.0;
  const playerHue     = {hue_player};

  // ===== Canvas =====
  const cvs = document.getElementById('game');
  const ctx2 = cvs.getContext('2d');
  function fit(){{
    const w = cvs.clientWidth|0, h = H;
    cvs.width = w * window.devicePixelRatio;
    cvs.height= h * window.devicePixelRatio;
    ctx2.setTransform(window.devicePixelRatio,0,0,window.devicePixelRatio,0,0);
  }}
  new ResizeObserver(fit).observe(document.getElementById('wrap')); fit();

  // ===== Audio (simple synth + pad) =====
  let AC=null, master=null, mixDest=null, mediaRec=null, chunks=[];
  function ctx(){{
    if(!AC){{
      AC = new (window.AudioContext||window.webkitAudioContext)();
      master = AC.createGain(); master.gain.value = masterV; master.connect(AC.destination);
    }}
    return AC;
  }}
  function beep(freq=440, dur=0.25){{
    ctx();
    const o = AC.createOscillator(); o.type='sine'; o.frequency.value=freq;
    const g = AC.createGain();
    const now = AC.currentTime;
    g.gain.setValueAtTime(0, now);
    g.gain.linearRampToValueAtTime(0.9, now+0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, now+dur);
    o.connect(g).connect(master);
    o.start(); o.stop(now+dur+0.06);
  }}
  function chordPad(frequencies, dur=2.4, type='sine'){{ // mekši reward
    ctx();
    const now = AC.currentTime;
    const g = AC.createGain(); g.gain.value = 0.0;
    g.connect(master);
    const oscs=[];
    for(const f of frequencies){{
      const o=AC.createOscillator(); o.type=type; o.frequency.value=f;
      o.connect(g); o.start(now);
      oscs.push(o);
    }}
    g.gain.linearRampToValueAtTime(0.75, now+0.2);
    g.gain.exponentialRampToValueAtTime(0.0001, now+dur);
    setTimeout(()=>oscs.forEach(o=>o.stop()), (dur+0.1)*1000);
  }}

  // ===== Recording (MediaRecorder) =====
  const btnRec  = document.getElementById('btn-rec');
  const btnStop = document.getElementById('btn-stop');
  const dlWebm  = document.getElementById('dl-webm');
  btnRec?.addEventListener('click', async () => {{
    try {{
      ctx();
      if(!mixDest){{ mixDest = AC.createMediaStreamDestination(); master.connect(mixDest); }}
      mediaRec = new MediaRecorder(mixDest.stream);
      chunks = [];
      mediaRec.ondataavailable = (e)=>{{ if(e.data && e.data.size>0) chunks.push(e.data); }};
      mediaRec.onstop = ()=>{{
        const blob = new Blob(chunks, {{type:'video/webm'}});
        const url  = URL.createObjectURL(blob);
        dlWebm.href = url; dlWebm.style.display = 'inline-block';
      }};
      mediaRec.start();
      btnRec.disabled=true; btnStop.disabled=false; dlWebm.style.display='none';
    }} catch(e) {{
      console.warn('MediaRecorder error', e);
    }}
  }});
  btnStop?.addEventListener('click', ()=>{{ try{{ mediaRec?.stop(); }}catch(_){{}} btnRec.disabled=false; btnStop.disabled=true; }});

  // ===== Player & input =====
  const player = {{ x: 96, y: H*0.55, r: 12, aura: 0 }};
  const keys = {{}};
  window.addEventListener('keydown', e=>keys[e.key]=true);
  window.addEventListener('keyup',   e=>keys[e.key]=false);

  // Tilt control
  let tiltOn=false, tiltZero={{beta:0,gamma:0}};
  const tiltDot=document.getElementById('tiltDot');
  async function askMotion(){{
    try{{
      if (typeof DeviceMotionEvent!=='undefined' && DeviceMotionEvent.requestPermission) {{
        const p = await DeviceMotionEvent.requestPermission();
        if(p!=='granted') return;
      }}
      window.addEventListener('deviceorientation', onTilt, true);
    }}catch(_e){{}}
  }}
  function onTilt(e){{
    if(!tiltOn) return;
    const b=(e.beta||0)-tiltZero.beta, g=(e.gamma||0)-tiltZero.gamma; // pitch/roll
    player.x += g*0.3; player.y += b*0.3;
    tiltDot.style.background = 'lime';
    setTimeout(()=> tiltDot.style.background='#666', 90);
  }}
  document.getElementById('btn-tilt')?.addEventListener('click', ()=>{{
  tiltOn = !tiltOn;
  if (tiltOn) {{ tiltZero = {{beta:0,gamma:0}}; askMotion(); }}
}});


  // ===== Objects =====
  const stars = [];            // obične + starburst (tip: 'star'|'burst')
  let comet = null;            // boss: {{x,y,r,vx,vy,hits,need,tr}}
  const burstNotes = [];       // za sekvencijalno mapiranje nota u starburst-u

  function spawnStar(){{
    const w = cvs.clientWidth, h = H;
    stars.push({{ x:w+20, y: 24+Math.random()*(h-48), r: 4+Math.random()*3, vx: -(1.2+Math.random()*1.8), type:'star' }});
  }}

  // Starburst generator
  function spawnStarburst(cx, cy, count=12, speed=1.8){{
    burstNotes.length = 0;
    for(let i=0;i<count;i++) burstNotes.push(scaleHz[i%scaleHz.length]);
    for(let i=0;i<count;i++) {{
      const ang = (i/count)*Math.PI*2;
      const vx = Math.cos(ang)*speed, vy=Math.sin(ang)*speed*0.8;
      stars.push({{ x:cx, y:cy, r:3.5, vx, vy, type:'burst', life: 4000 }});
    }}
    // mali vizuelni flash (nežno)
    player.aura = Math.min(1, player.aura+0.6);
  }}

  // Boss – COMET (meki susret, 2 dodira)
  function spawnComet(){{
    const w=cvs.clientWidth, h=H;
    const y= 80+Math.random()*(h-160);
    comet = {{
      x: w+40, y, r: 16, vx: -2.0, vy: (Math.random()<0.5?0.25:-0.25), hits:0, need:2,
      tr: []  // trail
    }};
  }}

  // ===== Wave manager =====
  let nextWaveAt = performance.now() + 2000;
  function maybeWave(ts){{
    if(ts < nextWaveAt) return;
    nextWaveAt = ts + wavesEveryMs;
    if(Math.random() < bossChance) spawnComet();
    else {{
      const w=cvs.clientWidth, h=H;
      spawnStarburst(w*0.5, h*0.45, 12, 1.8);
    }}
  }}

  // ===== Score / combo =====
  let score=0; const scEl=document.getElementById('sc');
  let mult=1, lastHitT=0; const multEl=document.getElementById('mult');
  function addScore(base){{
    score += base*mult; scEl.textContent=score;
  }}
  function onHit(){{
    const t=performance.now();
    if(t - lastHitT < 850) mult = Math.min(3, mult+1);
    else mult = 1;
    lastHitT = t;
    multEl.textContent = mult>1 ? '✦ x'+mult : '';
    player.aura = Math.min(1, player.aura+0.35);
  }}

  // ===== Main loop =====
  function step(ts){{
    // spawn običnih
    if(ts % (density*10) < 16) spawnStar();

    // talasi
    maybeWave(ts);

    // input
    const w=cvs.clientWidth, h=H;
    const vx = ((keys['ArrowRight']?1:0) - (keys['ArrowLeft']?1:0));
    const vy = ((keys['ArrowDown']?1:0)  - (keys['ArrowUp']?1:0));
    player.x += vx*speedBase*2;
    player.y += vy*speedBase*2;
    player.x = Math.max(10, Math.min(w-10, player.x));
    player.y = Math.max(10, Math.min(h-10, player.y));

    // move stars
    for(let i=stars.length-1;i>=0;i--){{
      const s=stars[i];
      s.x += (s.vx||0)*2; s.y = (s.y + (s.vy||0)*2);
      if(s.life) s.life -= 16;
      if(s.x < -24 || (s.life && s.life<=0)) {{ stars.splice(i,1); continue; }}
      // collide
      const dx=s.x-player.x, dy=s.y-player.y;
      if(dx*dx+dy*dy < (s.r+player.r)*(s.r+player.r)){{
        stars.splice(i,1);
        const freq = (s.type==='burst') ? burstNotes[(score+ i) % burstNotes.length] : scaleHz[Math.floor(Math.random()*scaleHz.length)];
        beep(freq, 0.20);
        addScore(1);
        onHit();
      }}
    }}

    // move comet
    if(comet){{
      comet.x += comet.vx*2.0; comet.y += comet.vy*2.0;
      // bounce a little
      if(comet.y < 40 || comet.y > h-40) comet.vy *= -1;
      // trail
      comet.tr.push([comet.x, comet.y]); if(comet.tr.length>22) comet.tr.shift();
      // collide
      const dx=comet.x-player.x, dy=comet.y-player.y;
      if(dx*dx+dy*dy < (comet.r+player.r)*(comet.r+player.r)){{
        comet.hits += 1;
        player.aura = Math.min(1, player.aura+0.6);
        // reward note
        beep(scaleHz[(comet.hits)%scaleHz.length], 0.25);
        addScore(3);
        onHit();
        // mali knock vel
        comet.x += 10; player.x -= 6;
        if(comet.hits >= comet.need){{
          // veliki reward: pad akord (C-dur po referenci base_ref aproks.)
          const tri = [scaleHz[0], scaleHz[Math.min(2,scaleHz.length-1)], scaleHz[Math.min(4,scaleHz.length-1)]];
          chordPad(tri, 2.8, 'sine');
          addScore(10); mult = 3; multEl.textContent='✦ x3';
          comet = null; // nestaje nakon nagrade
        }}
      }}
      // offscreen
      if(comet && comet.x < -40) comet = null;
    }}

    // draw
    ctx2.clearRect(0,0,w,h);

    // stars
    for(const s of stars){{
      ctx2.beginPath(); ctx2.arc(s.x,s.y,s.r,0,Math.PI*2);
      ctx2.fillStyle = (s.type==='burst') ? 'rgba(255,230,180,0.95)' : 'rgba(255,255,255,0.9)';
      ctx2.shadowColor = (s.type==='burst') ? 'rgba(255,200,120,0.7)' : 'rgba(255,255,255,0.5)';
      ctx2.shadowBlur=6; ctx2.fill(); ctx2.shadowBlur=0;
    }}

    // comet
    if(comet){{
      // trail
      ctx2.strokeStyle='rgba(255,220,140,0.6)'; ctx2.lineWidth=3;
      ctx2.beginPath();
      for(let i=0;i<comet.tr.length;i++){{ const p=comet.tr[i]; if(i===0) ctx2.moveTo(p[0],p[1]); else ctx2.lineTo(p[0],p[1]); }}
      ctx2.stroke();

      // body
      ctx2.beginPath(); ctx2.arc(comet.x,comet.y,comet.r,0,Math.PI*2);
      ctx2.fillStyle='rgba(255,200,120,0.95)';
      ctx2.shadowColor='rgba(255,210,130,0.9)'; ctx2.shadowBlur=24; ctx2.fill(); ctx2.shadowBlur=0;

      // hits dots
      for(let i=0;i<comet.need;i++){{ 
        ctx2.beginPath();
        ctx2.arc(comet.x - 18 + i*9, comet.y - comet.r - 10, 3, 0, Math.PI*2);
        ctx2.fillStyle = (i<comet.hits)?'rgba(255,240,200,0.95)':'rgba(120,120,120,0.6)';
        ctx2.fill();
      }}
    }}

    // player (glow with hue by scale)
    const hue = playerHue;
    ctx2.beginPath(); ctx2.arc(player.x,player.y,player.r,0,Math.PI*2);
    ctx2.fillStyle=`hsl(${{hue}} 80% 60%)`;
    ctx2.shadowColor=`hsla(${{hue}},90%,70%,${{0.35 + 0.45*player.aura}})`;
    ctx2.shadowBlur=18 + 24*player.aura;
    ctx2.fill();
    ctx2.shadowBlur=0; ctx2.shadowColor='transparent';
    player.aura = Math.max(0, player.aura - 0.02);

    requestAnimationFrame(step);
  }}
  requestAnimationFrame(step);
}})();
</script>
"""

st.title("🎮 TONOSAI — Zvezdani Sakupljač")
components.html(html, height=canvas_h + 10, scrolling=False)
footer()

