import streamlit as st
import boot  # naš globalni CSS

try:
    from pyvis.network import Network
    HAVE_PYVIS = True
except Exception as e:
    HAVE_PYVIS = False
    st.error("PyVis nije instaliran. Dodaj `pyvis` u requirements.txt i redeploy.")
    st.stop()

import random
import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components
import boot


# 1) Samo jedan page_config:
st.set_page_config(page_title="TONOSAI — Konstelacije",
                   page_icon="static/favicon.png",
                   layout="wide")
from lib.ui import header_badges, footer

header_badges()


# ---  PRESETI  ---
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

if "konst_count" not in st.session_state:
    _apply_params(PRESETS["Aurora"])

st.title("🌌 Zvezdana Konstelacija Tima TONOSAI")

# ---  Preset + kontrole (može i bez forme ako ti više odgovara) ---
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

# zapamti poslednje vrednosti
st.session_state["konst_count"]  = count
st.session_state["konst_spread"] = spread
st.session_state["konst_hue"]    = hue
st.session_state["konst_seed"]   = seed

# ---  PyVis mreža (primer povezivanja sa kontrolama) ---
random.seed(seed)
net = Network(height="520px", width="100%", bgcolor="#000000", font_color="white")

# Napravi čvorove (boja prema hue)
for i in range(count):
    net.add_node(i, color=f"hsl({hue}, 100%, 60%)", title=f"Node {i}")

# Napravi grube veze u zavisnosti od 'spread'
edge_count = max(1, int(count * 0.7))
for _ in range(edge_count):
    a = random.randrange(count)
    b = min(count - 1, max(0, int(a + random.gauss(0, spread * 10))))
    if a != b:
        net.add_edge(a, b)

# 3) Bez snimanja fajla: generiši HTML u memoriji
html = net.generate_html()
components.html(html, height=540, scrolling=True)

# 2) Nazad na početnu bez slugova/“/”
st.page_link("app.py", label="← Vrati se na početni meni")
footer()

