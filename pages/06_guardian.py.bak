# pages/06_guardian.py — TONOSAI | Igra: Čuvar konstelacije
import streamlit as st
import streamlit.components.v1 as components
from lib.ui import header_badges, footer
import boot  # globalni stilovi

st.set_page_config(page_title="TONOSAI | Čuvar konstelacije", page_icon="✨", layout="wide")
header_badges()

# ---- Sidebar: podešavanja ----
with st.sidebar:
    st.subheader("✨ Čuvar konstelacije — podešavanja")

    scale_mode = st.selectbox(
        "Skala zvezda",
        ["Triada C (1–5/4–3/2)", "Pentatonika C", "Dorska (D Dorian)", "Solfeggio (432/528/639 Hz)"],
        index=1,
    )

    base_ref = st.slider("Ref. frekvencija C (Hz)", 220, 640, 528, 1,
                         help="Koristi se za sve skale osim Solfeggio.")

    speed    = st.slider("Brzina igrača", 2, 12, 6)
    density  = st.slider("Gustina zvezda (manje=više)", 5, 60, 15)
    master   = st.slider("Glasnoća", 0.0, 1.0, 0.60, 0.01)
    canvas_h = st.slider("Visina platna (px)", 300, 900, 520, 10)

    st.markdown("---")
    focus_mode = st.toggle("🧠 Fokus mode", False,
                           help="Diskretniji zvuk i tamniji puls – za duboki rad.")

    st.markdown("---")
    breath_on   = st.toggle("Healing HUD — Dah ON", True)
    breath_mode = st.selectbox("Uzorak daha", ["Box 4–4–4–4", "4–7–8"], index=0)
    sec_per_cnt = st.slider("Sekundi po broju", 0.5, 2.0, 1.0, 0.1)

    st.markdown("---")
    boss_every_s = st.slider("Boss na svakih (sek)", 20, 120, 45, 5)

def ratios_for(name: str):
    if "Pentatonika" in name: return [1.0, 9/8, 5/4, 3/2, 5/3]
    if "Dorska" in name:      return [1.0, 9/8, 6/5, 4/3, 3/2, 8/5, 9/5]
    return [1.0, 5/4, 3/2]  # triada

# Skala u Hz
if "Solfeggio" in scale_mode:
    scale_hz = [432.0, 528.0, 639.0]
else:
    scale_hz = [round(base_ref*r, 3) for r in ratios_for(scale_mode)]

# Breath pattern u sekundama (ciklusi)
if "4–7–8" in breath_mode:
    breath_segments = [4, 7, 8, 0]
else:
    breath_segments = [4, 4, 4, 4]
breath_segments = [round(x*sec_per_cnt, 3) for x in breath_segments]

# Fokus mod – blago stišavanje i tamniji puls neba
focus_gain = 0.8 if focus_mode else 1.0
focus_sky  = 0.85 if focus_mode else 1.0   # multiplikator alfa pulsa

html = f"""
<div id="wrap" style="position:relative;width:100%;max-width:1200px;margin:0 auto;">
  <canvas id="game" style="width:100%;height:{canvas_h}px;border-radius:16px;display:block;background:
    radial-gradient(circle at 50% 30%, rgba(255,255,255,0.04), rgba(0,0,0,0.0) 60%),
    linear-gradient(180deg,#04060b,#0a0f1f); box-shadow:0 8px 24px rgba(0,0,0,0.35)"></canvas>

  <div id="hud" style="position:absolute;left:12px;top:10px;color:#fff;font:600 14px/1.4 system-ui, -apple-system, Segoe UI, Roboto">
    ⭐ Score: <b id="sc">0</b>
    <span style="margin-left:10px;">✴ Combo: <b id="cb">1x</b></span>
    <span id="bossLbl" style="margin-left:10px;opacity:.85;"></span>
  </div>

  <!-- Healing HUD -->
  <div id="breath" style="position:absolute;left:50%;top:10px;transform:translateX(-50%);
       color:#fff;text-align:center;font:600 13px/1.2 system-ui;display:{'block' if breath_on else 'none'};">
    <div id="bLabel" style="opacity:.95;">dah</div>
    <canvas id="bRing" width="120" height="120" style="margin-top:4px;"></canvas>
  </div>

  <div id="ctrl" style="position:absolute;right:12px;top:10px;display:flex;gap:8px;flex-wrap:wrap">
    <a href="/" target="_top" style="background:#111;border:1px solid #333;border-radius:10px;padding:6px 10px;color:#fff;text-decoration:none">🏠 Studio</a>
    <button id="btn-tilt" style="background:#111;border:1px solid #333;border-radius:10px;padding:6px 10px;color:#fff;cursor:pointer">🎮 Tilt</button>
  </div>
</div>

<script>
(()=>{{
  // ===== Parametri iz Pythona =====
  const scaleHz   = {scale_hz};
  const speed     = {speed};
  const density   = {density};
  const masterV   = ({master}) * ({focus_gain});
  const H         = {canvas_h};
  const breathOn  = {str(breath_on).lower()};
  const breathSeg = {breath_segments};
  const bossEvery = {boss_every_s} * 1000;
  const focusSky  = {focus_sky};

  // Canvas
  const cvs = document.getElementById('game');
  const ctx = cvs.getContext('2d');
  function fit(){{
    const w = cvs.clientWidth | 0, h = H;
    cvs.width  = w * devicePixelRatio;
    cvs.height = h * devicePixelRatio;
    ctx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);
  }}
  new ResizeObserver(fit).observe(document.getElementById('wrap')); fit();

  // Audio
  let AC=null, master=null;
  function audioCtx(){{
    if(!AC){{
      AC = new (window.AudioContext||window.webkitAudioContext)();
      master = AC.createGain(); master.gain.value = masterV; master.connect(AC.destination);
    }}
    return AC;
  }}
  function beep(freq=440, dur=0.25, type='sine', gain=1.0){{
    audioCtx();
    const o = AC.createOscillator();
    const g = AC.createGain();
    o.type=type; o.frequency.value=freq;
    const now = AC.currentTime;
    g.gain.setValueAtTime(0, now);
    g.gain.linearRampToValueAtTime(gain, now+0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, now+dur);
    o.connect(g).connect(master);
    o.start(); o.stop(now+dur+0.05);
  }}

  // Player & kontrole
  const player = {{ x: 80, y: 140, vx:0, vy:0, r:12 }};
  const keys = {{}};
  window.addEventListener('keydown', e=>keys[e.key]=true);
  window.addEventListener('keyup',   e=>keys[e.key]=false);

  // Tilt
  let tiltOn=false, tiltZero={{beta:0,gamma:0}};
  function askMotion(){{
    if (typeof DeviceOrientationEvent!=='undefined' && DeviceOrientationEvent.requestPermission) {{
      DeviceOrientationEvent.requestPermission().then(state=>{{ if(state==='granted') window.addEventListener('deviceorientation', onTilt); }});
    }} else {{
      window.addEventListener('deviceorientation', onTilt);
    }}
  }}
  function onTilt(e){{
    if(!tiltOn) return;
    const gb = (e.beta  || 0) - tiltZero.beta;
    const gg = (e.gamma || 0) - tiltZero.gamma;
    player.vx = Math.max(-1, Math.min(1, gg/20));
    player.vy = Math.max(-1, Math.min(1, gb/20));
  }}
  document.getElementById('btn-tilt').addEventListener('click', ()=>{{
    tiltOn = !tiltOn;
    if(tiltOn){{ tiltZero={{beta:0,gamma:0}}; askMotion(); beep(528,0.12,'sine',0.6); }}
  }});

  // Stars
  const stars = [];
  function spawnStar(){{
    const w = cvs.clientWidth;
    stars.push({{ x: w+20, y: 30+Math.random()*(H-60), r: 4+Math.random()*3, vx: -(1.2+Math.random()*1.8) }});
  }}
  let tSpawn = 0;

  // Score/Combo
  let score=0, combo=1, comboTimer=0;
  const scEl=document.getElementById('sc');
  const cbEl=document.getElementById('cb');
  function addScore(n){{
    score += Math.max(1, n*combo);
    scEl.textContent = score;
    comboTimer = performance.now();
    if (performance.now() - lastToneTime < 900) combo = Math.min(5, combo+1);
    cbEl.textContent = combo + 'x';
  }}
  let lastToneTime = 0;

  // Starburst prstenovi
  const rings = [];
  function spawnRings(x,y,count=4){{
    for(let i=0;i<count;i++) rings.push({{x:x, y:y, r:6+i*6, alpha:0.8, dr:1.8+i*0.2}});
  }}

  // Boss — Čuvar konstelacije (redosled)
  let bossActive=false, bossPts=[], bossIdx=0, bossEndAt=0, nextBossT=performance.now()+bossEvery;
  const bossLbl = document.getElementById('bossLbl');

  function spawnBoss(){{
    bossActive=true; bossIdx=0;
    const w=cvs.clientWidth;
    const cx=w*0.68, cy=H*0.34, R=Math.min(w,H)*0.09;
    bossPts = [
      {{x: cx-R,   y: cy+R*0.6}},
      {{x: cx,     y: cy-R}},
      {{x: cx+R,   y: cy+R*0.6}},
      {{x: cx,     y: cy+R*0.1}}
    ];
    bossEndAt = performance.now() + 18000;
    bossLbl.textContent = '👁 Čuvar konstelacije: 1→2→3→4';
    beep(432,0.18,'triangle',0.8);
  }}

  // Healing dah — faze i puls
  const breathLabel = document.getElementById('bLabel');
  const breathRing  = document.getElementById('bRing');
  const br = breathRing.getContext('2d');
  let breathStart = performance.now();

  function breathPhase(now){{
    const seg = breathSeg;
    const T = seg[0]+seg[1]+seg[2]+seg[3];
    const t = ((now - breathStart)/1000) % (T || 1);
    let phase='udah', prog=0, idx=0, acc=0;
    for(let i=0;i<4;i++){{ 
      const dur = seg[i];
      if (t < acc + dur) {{ idx=i; prog = dur? (t-acc)/dur : 1; break; }}
      acc += dur;
    }}
    if(idx===0) phase='udah';
    else if(idx===1) phase='zadrži';
    else if(idx===2) phase='izdah';
    else phase='mir';
    return {{phase, prog, idx}};
  }}

  function drawBreathHUD(now){{
    if(!breathOn) return 0.0;
    const {{phase, prog, idx}} = breathPhase(now);
    let glow = 0.15;
    if(idx===0) glow = 0.25 + 0.25*prog;      // udah
    else if(idx===2) glow = 0.25 + 0.25*(1-prog); // izdah
    // fokus režim: tamniji puls
    glow *= focusSky;

    breathLabel.textContent = phase;

    const w=breathRing.width, h=breathRing.height;
    br.setTransform(1,0,0,1,0,0);
    br.clearRect(0,0,w,h);
    br.translate(w/2,h/2);
    br.beginPath(); br.arc(0,0,48,0,Math.PI*2); br.strokeStyle='rgba(255,255,255,0.15)'; br.lineWidth=8; br.stroke();
    br.beginPath(); br.arc(0,0,48,-Math.PI/2, -Math.PI/2 + prog*2*Math.PI);
    br.strokeStyle='rgba(255,255,255,0.9)'; br.lineWidth=8; br.lineCap='round'; br.stroke();
    br.fillStyle='rgba(255,255,255,0.9)';
    br.font='700 14px system-ui'; br.textAlign='center'; br.textBaseline='middle';
    br.fillText(phase, 0, 0);

    return glow;
  }}

  // Glavni loop
  function step(ts){{
    // spawn
    if(ts - tSpawn > density*10) {{ tSpawn = ts; spawnStar(); }}

    // combo decay
    if (ts - comboTimer > 1500) combo = Math.max(1, combo-1), cbEl.textContent = combo+'x';

    // boss
    if (!bossActive && ts > nextBossT) {{ spawnBoss(); nextBossT = ts + bossEvery; }}

    // kretanje igrača
    const w=cvs.clientWidth;
    if(!tiltOn) {{
      player.vx = (keys['ArrowRight']?1:0) - (keys['ArrowLeft']?1:0);
      player.vy = (keys['ArrowDown']?1:0) - (keys['ArrowUp']?1:0);
    }}
    player.x += player.vx*speed*2;
    player.y += player.vy*speed*2;
    player.x = Math.max(10, Math.min(w-10, player.x));
    player.y = Math.max(10, Math.min(H-10, player.y));

    // kretanje zvezda
    for(let s of stars) s.x += s.vx*2;
    while(stars.length && stars[0].x < -20) stars.shift();

    // sudar sa zvezdom ⇒ ton + poeni
    for(let i=stars.length-1;i>=0;i--){{
      const s=stars[i];
      const dx=s.x-player.x, dy=s.y-player.y;
      if(dx*dx+dy*dy < (s.r+player.r)*(s.r+player.r)){{
        stars.splice(i,1);
        const pick = scaleHz[Math.floor(Math.random()*scaleHz.length)];
        beep(pick, 0.18, 'sine', 0.9);
        addScore(1);
        lastToneTime = ts;
        spawnRings(player.x, player.y, 2);
      }}
    }}

    // boss logika (redosled)
    if(bossActive){{
      // crtaj veze i tačke
      ctx.save();
      ctx.strokeStyle='rgba(255,255,255,0.35)';
      ctx.lineWidth=2;
      ctx.beginPath();
      for(let i=0;i<bossPts.length;i++){{ const p=bossPts[i]; if(i===0) ctx.moveTo(p.x,p.y); else ctx.lineTo(p.x,p.y); }}
      ctx.stroke();

      for(let i=0;i<bossPts.length;i++){{ 
        const p=bossPts[i];
        const isNext = (i===bossIdx);
        ctx.beginPath(); ctx.arc(p.x,p.y, isNext?10:8, 0, Math.PI*2);
        ctx.fillStyle = isNext? 'rgba(255,255,255,0.95)' : 'rgba(255,255,255,0.6)';
        ctx.shadowColor = 'rgba(255,255,255,0.6)'; ctx.shadowBlur = isNext? 20:10;
        ctx.fill(); ctx.shadowBlur=0; ctx.shadowColor='transparent';
        ctx.fillStyle='rgba(0,0,0,0.7)'; ctx.font='700 11px system-ui'; ctx.textAlign='center'; ctx.textBaseline='middle';
        ctx.fillText(String(i+1), p.x, p.y);
      }}
      ctx.restore();

      // kontakt sa sledećom tačkom
      if(bossIdx < bossPts.length){{
        const p = bossPts[bossIdx];
        const dx=p.x-player.x, dy=p.y-player.y;
        if(dx*dx+dy*dy < (player.r+10)*(player.r+10)){{
          bossIdx++;
          beep(528,0.14,'triangle',0.9);
          addScore(2);
          spawnRings(p.x,p.y,3);
        }}
      }}

      if(bossIdx >= bossPts.length){{            // uspeh
        bossActive=false; bossLbl.textContent='✨ Konstelacija zaključana! +bonus';
        addScore(8);
        spawnRings(player.x, player.y, 6);
      }}
    }} else {{
      bossLbl.textContent='';
    }}

    // crtanje
    ctx.clearRect(0,0,w,H);

    // healing puls neba
    let baseGlow = 0.0;
    if (breathOn) baseGlow = drawBreathHUD(performance.now());
    const skyAlpha = (0.12 + baseGlow*0.2);
    ctx.fillStyle = 'rgba(255,255,255,' + (skyAlpha.toFixed(3)) + ')';
    ctx.fillRect(0,0,w,H);

    // zvezde
    for(const s of stars){{
      ctx.beginPath(); ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
      ctx.fillStyle='rgba(255,255,255,0.9)'; ctx.fill();
    }}

    // player
    ctx.beginPath(); ctx.arc(player.x,player.y,player.r,0,Math.PI*2);
    ctx.fillStyle='hsl(45 80% 60%)';
    ctx.shadowColor='rgba(255,220,120,0.7)'; ctx.shadowBlur=20; ctx.fill();
    ctx.shadowBlur=0; ctx.shadowColor='transparent';

    // starburst prstenovi
    for(let i=rings.length-1;i>=0;i--){{
      const r = rings[i];
      r.r += r.dr; r.alpha *= 0.965;
      ctx.beginPath(); ctx.arc(r.x, r.y, r.r, 0, Math.PI*2);
      ctx.strokeStyle = 'rgba(255,255,255,' + r.alpha.toFixed(3) + ')';
      ctx.lineWidth = 2 + Math.max(0, 8 - r.r*0.07);
      ctx.stroke();
      if(r.alpha < 0.04) rings.splice(i,1);
    }}

    requestAnimationFrame(step);
  }}
  requestAnimationFrame(step);
}})();
</script>
"""

st.title("✨ TONOSAI — Čuvar konstelacije")
components.html(html, height=canvas_h + 8, scrolling=False)
footer()
