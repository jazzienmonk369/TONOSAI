# pages/02_konstelacija.py
from __future__ import annotations
import os, json, random, hashlib, colorsys
import streamlit as st
import streamlit.components.v1 as components

# globalni CSS / UI helperi
import boot
from lib.ui import header_badges, footer
# ── Ambijentalni zvuk (opciono) ─────────────────────────────────────────────
import os, random
from streamlit.components.v1 import html as _html

st.write("")  # small spacing
play_amb = st.toggle("🔊 Ambijent (pozadinska petlja)", value=False)

AUDIO_DIR = "static/audio"
if play_amb:
    files = [f for f in os.listdir(AUDIO_DIR) if f.lower().endswith((".wav", ".mp3"))]
    if files:
        pick = random.choice(files)              # random loop per run
        src = f"{AUDIO_DIR}/{pick}"

        # HTML <audio> so we can loop + set volume
        _html(
            f"""
            <audio controls autoplay loop style="width:100%;">
              <source src="{src}" type="audio/{'wav' if src.endswith('.wav') else 'mpeg'}">
              Your browser does not support the audio element.
            </audio>
            <script>
              // set gentle volume
              const a = document.querySelector('audio');
              if (a) a.volume = 0.22;
            </script>
            """,
            height=60,
        )
    else:
        st.info("Ubaci par WAV/MP3 fajlova u `static/audio/` (npr. *tonosai_ambient_528hz.wav*).")


# ──────────────────────────────────────────────────────────────────────────────
# Page meta (JEDAN poziv!)
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TONOSAI — Konstelacije",
    page_icon="static/favicon.png",
    layout="wide",
)

# PyVis (uz bezbedan fallback)
try:
    from pyvis.network import Network
except Exception:
    st.error("PyVis nije instaliran. Dodaj `pyvis` u requirements.txt i redeploy.")
    st.stop()

# Header
header_badges()
st.title("🌌 Zvezdana Konstelacija Tima TONOSAI")

# ──────────────────────────────────────────────────────────────────────────────
# Preseti (podrazumevani)
# ──────────────────────────────────────────────────────────────────────────────
PRESETS = {
    "Aurora":     {"count": 120, "spread": 0.80, "hue": 200, "seed": 42},
    "Solar Wind": {"count": 200, "spread": 0.60, "hue":  45, "seed": 7},
    "Neptune":    {"count":  90, "spread": 1.00, "hue": 220, "seed": 99},
    "Orion":      {"count": 160, "spread": 0.95, "hue": 280, "seed": 314},
}

def _apply_params(p: dict):
    st.session_state["konst_count"]  = int(p["count"])
    st.session_state["konst_spread"] = float(p["spread"])
    st.session_state["konst_hue"]    = int(p["hue"])
    st.session_state["konst_seed"]   = int(p["seed"])

# init state
if "konst_count" not in st.session_state:
    _apply_params(PRESETS["Aurora"])

# ──────────────────────────────────────────────────────────────────────────────
# Query params (NEW API)
# ──────────────────────────────────────────────────────────────────────────────
qp = st.query_params  # dict-like

def _qp(key, cast, fallback):
    raw = qp.get(key, None)
    if isinstance(raw, list):
        raw = raw[0] if raw else None
    if raw is None:
        return fallback
    try:
        return cast(raw)
    except Exception:
        return fallback

# Ako je link otvoren sa parametrima, presnimi podrazumevane vrednosti
st.session_state["konst_count"]  = _qp("count",  int,   st.session_state["konst_count"])
st.session_state["konst_spread"] = _qp("spread", float, st.session_state["konst_spread"])
st.session_state["konst_hue"]    = _qp("hue",    int,   st.session_state["konst_hue"])
st.session_state["konst_seed"]   = _qp("seed",   int,   st.session_state["konst_seed"])

# ──────────────────────────────────────────────────────────────────────────────
# Kontrole (preset + slideri)
# ──────────────────────────────────────────────────────────────────────────────
with st.form("konst_controls"):
    c1, c2, c3 = st.columns([2, 1, 1])
    preset_name = c1.selectbox("🎛 Preset", list(PRESETS.keys()))
    apply_btn   = c2.form_submit_button("Primeni")
    random_btn  = c3.form_submit_button("🎲 Randomize")

    count  = st.slider("⭐ Broj zvezda", 20, 400, st.session_state["konst_count"])
    spread = st.slider("🌌 Rasipanje", 0.2, 1.5, st.session_state["konst_spread"])
    hue    = st.slider("🎨 Boja (Hue)", 0, 360, st.session_state["konst_hue"])
    seed   = st.number_input("🔢 Seed", 1, 9999, st.session_state["konst_seed"])

if apply_btn:
    _apply_params(PRESETS[preset_name])
    st.rerun()

if random_btn:
    _apply_params({
        "count":  random.randint(60, 200),
        "spread": round(random.uniform(0.4, 1.2), 2),
        "hue":    random.randint(0, 360),
        "seed":   random.randint(1, 9999),
    })
    st.rerun()

# Upamti poslednje vrednosti
st.session_state["konst_count"]  = count
st.session_state["konst_spread"] = spread
st.session_state["konst_hue"]    = hue
st.session_state["konst_seed"]   = seed

# Sačuvaj share link (novi API)
if st.button("🔗 Sačuvaj link sa ovim podešavanjima"):
    st.query_params = {
        "count": count,
        "spread": spread,
        "hue": hue,
        "seed": seed,
    }
    st.success("Link je ažuriran u address baru — samo kopiraj i podeli!")

st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# Preset manager (download / upload JSON, opcioni Gist)
# ──────────────────────────────────────────────────────────────────────────────
def current_preset_dict() -> dict:
    return {
        "count":  int(st.session_state["konst_count"]),
        "spread": float(st.session_state["konst_spread"]),
        "hue":    int(st.session_state["konst_hue"]),
        "seed":   int(st.session_state["konst_seed"]),
    }

with st.expander("💾 Preseti (sačuvaj / učitaj)"):
    cdl, cul = st.columns(2)

    # Download JSON
    preset_json = json.dumps(current_preset_dict(), indent=2)
    cdl.download_button(
        "⬇️ Download trenutni preset (JSON)",
        data=preset_json,
        file_name="konstelacija_preset.json",
        mime="application/json",
    )

    # Upload JSON
    up = cul.file_uploader("Učitaj preset (JSON)", type=["json"])
    if up is not None:
        try:
            pdata = json.loads(up.read().decode("utf-8"))
            _apply_params(pdata)
            st.success("Preset učitan ✅")
            st.rerun()
        except Exception as e:
            st.error(f"Nevalidan JSON: {e}")

    # (Opcionalno) GitHub Gist — zahteva st.secrets["GITHUB_TOKEN"]
    if "GITHUB_TOKEN" in st.secrets:
        import requests
        token = st.secrets["GITHUB_TOKEN"]
        gist_id = st.text_input("Gist ID (postojeći) ili ostavi prazno za novi")
        if st.button("☁️ Snimi preset u Gist"):
            headers = {"Authorization": f"token {token}"}
            payload = {
                "description": "TONOSAI konstelacija preset",
                "public": False,
                "files": {"preset.json": {"content": preset_json}},
            }
            if gist_id.strip():
                r = requests.patch(f"https://api.github.com/gists/{gist_id}", json=payload, headers=headers)
            else:
                r = requests.post("https://api.github.com/gists", json=payload, headers=headers)
            if r.ok:
                gid = r.json()["id"]
                st.success(f"Gist snimljen ✅ ID: {gid}")
            else:
                st.error(f"Gist greška: {r.status_code} {r.text}")

st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# Team mod (konstelacija iz liste imena) + tooltips
# ──────────────────────────────────────────────────────────────────────────────
TEAM_META = {
    "TONOSAI":  "Core / Orkestracija",
    "Harmonia":"Algoritamska harmonija",
    "Cosma":   "Vizuelna kosmologija",
    "Neura":   "AI eksperimenti",
    "Orion":   "Ritam i groove",
    "Chronos": "Tempo & vreme",
    "Echo":    "Ambijenti i FX",
}

def hsl_to_hex(h, s=70, l=52):
    r, g, b = colorsys.hls_to_rgb(h/360.0, l/100.0, s/100.0)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

def color_for_name(name: str) -> str:
    hue_local = int(hashlib.md5(name.encode("utf-8")).hexdigest(), 16) % 360
    return hsl_to_hex(hue_local, 70, 52)

use_team = st.checkbox("👥 Koristi listu imena (Team mod)")
names_default = "TONOSAI, Harmonia, Cosma, Neura, Orion, Chronos, Echo"
names_text = st.text_area("Imena (odvojena zarezom)", names_default, disabled=not use_team)
names = [n.strip() for n in names_text.split(",") if n.strip()] if use_team else []

# ──────────────────────────────────────────────────────────────────────────────
# Kreiranje mreže (PyVis)
# ──────────────────────────────────────────────────────────────────────────────
random.seed(seed)
net = Network(height="520px", width="100%", bgcolor="#000000", font_color="white")

# Verziono-otporno uključivanje Barnes-Hut; podešavanja idu kroz set_options JSON
try:
    net.barnes_hut()
except Exception:
    pass

net.set_options("""
{
  "edges": {"smooth": false},
  "interaction": {"hover": true},
  "physics": {
    "enabled": true,
    "stabilization": {"enabled": true, "iterations": 200},
    "barnesHut": {
      "gravitationalConstant": -8000,
      "centralGravity": 0.3,
      "springLength": 120,
      "springConstant": 0.001,
      "damping": 0.9,
      "avoidOverlap": 0.1
    }
  }
}
""")

if use_team and names:
    center_id = "center_tonosai"
    net.add_node(center_id,
                 label="TONOSAI",
                 title=TEAM_META.get("TONOSAI", "Član tima"),
                 color="#6c5ce7", shape="dot", size=24)

    prev = None
    first_member_id = None
    for i, name in enumerate(names):
        node_id = f"member_{i}"
        title_txt = f"{name} — {TEAM_META.get(name, 'Član tima')}"
        net.add_node(node_id, label=name, title=title_txt,
                     color=color_for_name(name), shape="dot", size=15)
        net.add_edge(center_id, node_id)
        if prev is not None:
            net.add_edge(prev, node_id)
        else:
            first_member_id = node_id
        prev = node_id

    if prev and first_member_id and len(names) > 2:
        net.add_edge(prev, first_member_id)
else:
    # Random zvezdano nebo (prema sliderima)
    for i in range(count):
        net.add_node(i, color=f"hsl({hue}, 100%, 60%)", title=f"Node {i}")
    edge_count = max(1, int(count * 0.7))
    for _ in range(edge_count):
        a = random.randrange(count)
        b = min(count - 1, max(0, int(a + random.gauss(0, spread * 10))))
        if a != b:
            net.add_edge(a, b)

# Render u memoriji i prikaz
html = net.generate_html()
components.html(html, height=540, scrolling=True)

# PNG export (klijent-sajt; hvata #mynetwork koji PyVis pravi)
components.html("""
<div style="margin-top:6px">
  <button id="shot"
          style="padding:8px 12px;border:1px solid #444;border-radius:8px;background:#111;color:#fff;cursor:pointer">
    📸 Sačuvaj PNG
  </button>
</div>
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script>
  const btn = document.getElementById('shot');
  btn.onclick = async () => {
    const el = parent.document.querySelector('#mynetwork');
    if(!el){ alert('Mreža nije spremna.'); return; }
    const canvas = await html2canvas(el, {backgroundColor: null, scale: 2});
    const a = document.createElement('a');
    a.download = 'konstelacija.png';
    a.href = canvas.toDataURL('image/png');
    a.click();
  };
</script>
""", height=40)

# Download HTML
st.download_button(
    "⬇️ Preuzmi konstelaciju (HTML)",
    data=html,
    file_name="konstelacija.html",
    mime="text/html",
)

st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# Ambijentalni zvuk (loop)
# ──────────────────────────────────────────────────────────────────────────────
st.subheader("🔊 Ambijentalni zvuk")
audio_dir = "static/audio"
audio_files = []
try:
    if os.path.isdir(audio_dir):
        audio_files = [f for f in os.listdir(audio_dir)
                       if f.lower().endswith((".mp3", ".ogg", ".wav"))]
        audio_files.sort()
except Exception:
    audio_files = []

if not audio_files:
    st.info("Dodaj kratke loop fajlove u **static/audio/** (npr. `space_1.mp3`, `space_2.mp3`).")
else:
    colA, colB = st.columns([1, 3])
    amb_on = colA.toggle("Uključi", value=False)
    choice = colB.selectbox("Izbor trake", ["🎲 Random"] + audio_files, disabled=not amb_on)
    vol = st.slider("Jačina", 0.0, 1.0, 0.25, 0.01, disabled=not amb_on)

    if amb_on:
        if choice == "🎲 Random":
            # pseudo-stabilno po seed-u, da ne iznenadi korisnika na reload
            rng = random.Random(seed)
            fname = rng.choice(audio_files)
        else:
            fname = choice

        # koristi /static/... path da radi i na Streamlit Cloud-u
        src = f"/static/audio/{fname}"
        components.html(f"""
        <audio id="amb" src="{src}" loop controls autoplay style="width:100%"></audio>
        <script>
          const a = document.getElementById('amb');
          try {{ a.volume = {vol}; }} catch(e) {{}}
        </script>
        """, height=52)

st.page_link("app.py", label="← Vrati se na početni meni")
footer()
