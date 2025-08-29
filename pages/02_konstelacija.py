# pages/02_konstelacija.py
import json
import random
import hashlib
import colorsys

import streamlit as st
import streamlit.components.v1 as components

import boot  # naš globalni CSS / tema (side-effect import)
from lib.ui import header_badges, footer

# ── Page meta (pozivamo SAMO jednom) ──────────────────────────────────────────
st.set_page_config(
    page_title="TONOSAI — Konstelacije",
    page_icon="static/favicon.png",
    layout="wide",
)

# ── PyVis (bez duplog set_page_config u except-u) ────────────────────────────
try:
    from pyvis.network import Network
except Exception:
    st.error("PyVis nije instaliran. Dodaj `pyvis` u requirements.txt i redeploy.")
    st.stop()

# ── Header ───────────────────────────────────────────────────────────────────
header_badges()
st.title("🌌 Zvezdana Konstelacija Tima TONOSAI")

# ── Preseti ───────────────────────────────────────────────────────────────────
PRESETS = {
    "Aurora":     {"count": 120, "spread": 0.80, "hue": 200, "seed": 42},
    "Solar Wind": {"count": 200, "spread": 0.60, "hue":  45, "seed": 7},
    "Neptune":    {"count":  90, "spread": 1.00, "hue": 220, "seed": 99},
    "Orion":      {"count": 160, "spread": 0.95, "hue": 280, "seed": 314},
}

def _apply_params(p):
    st.session_state["konst_count"]  = p["count"]
    st.session_state["konst_spread"] = p["spread"]
    st.session_state["konst_hue"]    = p["hue"]
    st.session_state["konst_seed"]   = p["seed"]

# Init state (prvi ulazak)
if "konst_count" not in st.session_state:
    _apply_params(PRESETS["Aurora"])

# ── Query params (NEW API) ───────────────────────────────────────────────────
qp = st.query_params  # čitanje trenutnih query parametara iz URL-a

def _qp(key, cast, fallback):
    """Bezbedno čitanje iz st.query_params sa kastovanjem i default vrednošću."""
    raw = qp.get(key, None)
    if isinstance(raw, list):
        raw = raw[0] if raw else None
    if raw is None:
        return fallback
    try:
        return cast(raw)
    except Exception:
        return fallback

# Ako je link otvoren sa parametrima, presnimi inicijalne vrednosti
st.session_state["konst_count"]  = _qp("count",  int,   st.session_state["konst_count"])
st.session_state["konst_spread"] = _qp("spread", float, st.session_state["konst_spread"])
st.session_state["konst_hue"]    = _qp("hue",    int,   st.session_state["konst_hue"])
st.session_state["konst_seed"]   = _qp("seed",   int,   st.session_state["konst_seed"])

# ── Kontrole ──────────────────────────────────────────────────────────────────
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

# Sačuvaj share link (NEW API — menja address bar odmah)
if st.button("🔗 Sačuvaj link sa ovim podešavanjima"):
    st.query_params = {
        "count": count,
        "spread": spread,
        "hue": hue,
        "seed": seed,
    }
    st.success("Link je ažuriran u address baru — samo kopiraj i podeli!")

# Copy link dugme (clipboard) — mali HTML snip
components.html("""
<button onclick="navigator.clipboard.writeText(window.location.href)"
        style="margin:6px 0 12px 0;padding:8px 12px;border-radius:8px;border:1px solid #444;
               background:#111;color:#fff;cursor:pointer">
  📋 Copy link
</button>
""", height=60)

st.divider()

# ── Team mod (konstelacija iz liste imena) ────────────────────────────────────
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

# ── Kreiranje mreže ───────────────────────────────────────────────────────────
random.seed(seed)
net = Network(height="520px", width="100%", bgcolor="#000000", font_color="white")

# Aktiviraj Barnes-Hut (bez argumenata — radi u svim pyvis verzijama)
try:
    net.barnes_hut()
except Exception:
    pass

# Sva podešavanja kroz vis-network options (JSON-safe preko dict → json.dumps)
options = {
    "edges": {"smooth": False},
    "interaction": {
        "hover": True,
        "navigationButtons": True,   # dugmići za navigaciju
        "keyboard": True             # tastatura (strelice, +/−)
    },
    "physics": {
        "enabled": True,
        "stabilization": {"enabled": True, "iterations": 200, "fit": True},
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
net.set_options(json.dumps(options))

if use_team and names:
    # Centralni čvor
    center_id = "center_tonosai"
    net.add_node(center_id, label="TONOSAI", color="#6c5ce7", shape="dot", size=24)

    # Prsten članova + veze ka centru i susedima
    prev = None
    first_member_id = None
    for i, name in enumerate(names):
        node_id = f"member_{i}"
        net.add_node(node_id, label=name, color=color_for_name(name), shape="dot", size=15)
        net.add_edge(center_id, node_id)
        if prev is not None:
            net.add_edge(prev, node_id)
        else:
            first_member_id = node_id
        prev = node_id

    if prev and first_member_id and len(names) > 2:
        net.add_edge(prev, first_member_id)

else:
    # Random zvezdano nebo — degree-based veličina čvora
    deg = [0] * count
    edges = []

    for _ in range(max(1, int(count * 0.7))):
        a = random.randrange(count)
        b = min(count - 1, max(0, int(a + random.gauss(0, spread * 10))))
        if a != b:
            edges.append((a, b))
            deg[a] += 1
            deg[b] += 1

    for i in range(count):
        size = 8 + deg[i] * 0.6  # veći čvor = veći stepen
        net.add_node(
            i,
            color=f"hsl({hue}, 100%, 60%)",
            size=size,
            title=f"Node {i} (deg {deg[i]})"
        )

    for a, b in edges:
        net.add_edge(a, b)

# Render u memoriji i prikaz
html = net.generate_html()
components.html(html, height=540, scrolling=True)

# Open in new tab (pored preuzimanja)
components.html(
    f"""
<a href="data:text/html;charset=utf-8,{html.replace('"','&quot;')}" target="_blank"
   style="display:inline-block;margin-top:6px;padding:8px 12px;border-radius:8px;border:1px solid #444;
          background:#111;color:#fff;text-decoration:none">
  🔎 Otvori u novom tabu
</a>
""",
    height=42
)

# Download dugme (čist HTML fajl)
st.download_button(
    "⬇️ Preuzmi konstelaciju (HTML)",
    data=html,
    file_name="konstelacija.html",
    mime="text/html",
)

st.page_link("app.py", label="← Vrati se na početni meni")
footer()
