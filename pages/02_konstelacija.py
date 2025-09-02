from __future__ import annotations

import os, json, random, hashlib, colorsys
import streamlit as st
import streamlit.components.v1 as components

# Opcioni UI helpers
try:
    import boot  # noqa: F401
    from lib.ui import header_badges, footer
except Exception:
    header_badges = lambda: None
    footer = lambda: None

# Bezbedan secrets helper (radi i bez secrets.toml)
def get_secret(name: str, default=None):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return os.environ.get(name, default)

GITHUB_TOKEN = get_secret("GITHUB_TOKEN")

st.set_page_config(page_title="TONOSAI — Konstelacije", page_icon="🌌", layout="wide")

# PyVis (uz fallback)
try:
    from pyvis.network import Network
except Exception:
    st.error("PyVis nije instaliran. Dodaj `pyvis` u requirements.txt i pokreni ponovo.")
    st.stop()

header_badges()
st.title("🌌 Zvezdana Konstelacija Tima TONOSAI")

# Default parametri
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

if "konst_count" not in st.session_state:
    _apply_params(PRESETS["Aurora"])

qp = st.query_params

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

st.session_state["konst_count"]  = _qp("count",  int,   st.session_state["konst_count"])
st.session_state["konst_spread"] = _qp("spread", float, st.session_state["konst_spread"])
st.session_state["konst_hue"]    = _qp("hue",    int,   st.session_state["konst_hue"])
st.session_state["konst_seed"]   = _qp("seed",   int,   st.session_state["konst_seed"])

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

st.session_state["konst_count"]  = count
st.session_state["konst_spread"] = spread
st.session_state["konst_hue"]    = hue
st.session_state["konst_seed"]   = seed

if st.button("🔗 Sačuvaj link sa ovim podešavanjima"):
    st.query_params = {"count": count, "spread": spread, "hue": hue, "seed": seed}
    st.success("Link je ažuriran u address baru — samo kopiraj i podeli!")

st.divider()

def current_preset_dict() -> dict:
    return {
        "count":  int(st.session_state["konst_count"]),
        "spread": float(st.session_state["konst_spread"]),
        "hue":    int(st.session_state["konst_hue"]),
        "seed":   int(st.session_state["konst_seed"]),
    }

with st.expander("💾 Preseti (sačuvaj / učitaj)"):
    cdl, cul = st.columns(2)
    preset_json = json.dumps(current_preset_dict(), indent=2)

    cdl.download_button(
        "⬇️ Download trenutni preset (JSON)",
        data=preset_json,
        file_name="konstelacija_preset.json",
        mime="application/json",
    )

    up = cul.file_uploader("Učitaj preset (JSON)", type=["json"])
    if up is not None:
        try:
            pdata = json.loads(up.read().decode("utf-8"))
            _apply_params(pdata)
            st.success("Preset učitan ✅")
            st.rerun()
        except Exception as e:
            st.error(f"Nevalidan JSON: {e}")

    # (Opcionalno) GitHub Gist — koristi bezbedan secret
    gist_id = st.text_input("Gist ID (postojeći) ili ostavi prazno za novi")
    if st.button("☁️ Snimi preset u Gist"):
        import requests
        headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
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
    import colorsys as _cs
    r, g, b = _cs.hls_to_rgb(h/360.0, l/100.0, s/100.0)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

def color_for_name(name: str) -> str:
    hue_local = int(hashlib.md5(name.encode("utf-8")).hexdigest(), 16) % 360
    return hsl_to_hex(hue_local, 70, 52)

use_team = st.checkbox("👥 Koristi listu imena (Team mod)")
names_default = "TONOSAI, Harmonia, Cosma, Neura, Orion, Chronos, Echo"
names_text = st.text_area("Imena (odvojena zarezom)", names_default, disabled=not use_team)
names = [n.strip() for n in names_text.split(",") if n.strip()] if use_team else []

count  = st.session_state["konst_count"]
spread = st.session_state["konst_spread"]
hue    = st.session_state["konst_hue"]
seed   = st.session_state["konst_seed"]

# PyVis mreža
random.seed(seed)
net = Network(height="520px", width="100%", bgcolor="#000000", font_color="white")
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
    net.add_node(center_id, label="TONOSAI",
                 title=TEAM_META.get("TONOSAI","Član tima"),
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
    # Random zvezdano nebo
    for i in range(count):
        net.add_node(i, color=f"hsl({hue}, 100%, 60%)", title=f"Node {i}")
    edge_count = max(1, int(count * 0.7))
    for _ in range(edge_count):
        a = random.randrange(count)
        b = min(count - 1, max(0, int(a + random.gauss(0, spread * 10))))
        if a != b:
            net.add_edge(a, b)

html_out = net.generate_html()
components.html(html_out, height=540, scrolling=True)

# PNG export (klijent)
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

st.download_button(
    "⬇️ Preuzmi konstelaciju (HTML)",
    data=html_out,
    file_name="konstelacija.html",
    mime="text/html",
)

st.page_link("vizija_tonosai.py", label="← Nazad na Viziju", icon="🏠")
footer()