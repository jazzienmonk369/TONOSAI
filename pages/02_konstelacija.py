import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components
import os

# 🌌 Konfiguracija stranice
st.set_page_config(page_title="TONOSAI | Konstelacija", page_icon="✨", layout="wide")

st.markdown("""
    <style>
        section[data-testid="stSidebar"] > div:first-child {
            background-color: #0a0a2a;
            border-right: 2px solid #3c3c66;
        }

        .block-container {
            padding-top: 2rem;
        }

        .css-1d391kg, .css-ffhzg2 {
            color: #e0e0ff !important;
        }

        .konstelacija-frame iframe {
            border: none !important;
        }

        h1, h2, h3, h4 {
            color: #ffccff !important;
        }

        a {
            color: #ff7675 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🌌 Zvezdana Konstelacija Tima TONOSAI")

# 🧠 PyVis mreža
net = Network(height="500px", width="100%", bgcolor="#000000", font_color="white")

# Čvorovi
net.add_node("TONOS", label="TONOS", color="#6c5ce7")
net.add_node("Harmonia", label="Harmonia", color="#00cec9")
net.add_node("Cosma", label="Cosma", color="#ffeaa7")
net.add_node("Neura", label="Neura", color="#fab1a0")
net.add_node("Orion", label="Orion", color="#81ecec")
net.add_node("Chronos", label="Chronos", color="#ff7675")
net.add_node("Echo", label="Echo", color="#a29bfe")

# Veze
net.add_edge("TONOS", "Harmonia")
net.add_edge("Harmonia", "Cosma")
net.add_edge("Cosma", "Orion")
net.add_edge("Harmonia", "Neura")
net.add_edge("TONOS", "Echo")
net.add_edge("Echo", "Chronos")

# Renderovanje mreže
net.save_graph("konstelacija.html")

# Prikaz u okviru
with open("konstelacija.html", 'r', encoding='utf-8') as f:
    html_content = f.read()
    components.html(html_content, height=520, width=1100)

# Dugme za povratak
st.markdown("""
<div style='margin-top: 2rem;'>
    <a href="/" style="text-decoration: none; font-weight: bold; font-size: 18px;">
        ← Vrati se na početni meni
    </a>
</div>
""", unsafe_allow_html=True)