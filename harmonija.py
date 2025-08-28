import streamlit as st
import boot


st.set_page_config(
    page_title="TONOSAI Studio",
    page_icon="static/favicon.png",
    layout="wide",
)
from lib.ui import header_badges, footer

header_badges()


import streamlit as st
import base64
import os

# 🎨 Konfiguracija stranice
st.set_page_config(page_title="TONOSAI | Vila Harmonija", page_icon="🧚", layout="centered")

# 🌌 Pozadinski stil
st.markdown("""
    <style>
        .stApp {
            background-color: #0f1021;
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        h1 {
            color: #ffd3e3;
            text-align: center;
        }
        .fade-in {
            animation: fadeIn 3s ease-in-out;
        }
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)

# 🎵 Učitaj zvuk (opciono)
audio_path = "static/audio/vila_ambient_loop.ogg"
if os.path.exists(audio_path):
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/ogg")

# 🖼️ Prikaži sliku vile
img_path = "static/images/harmonia_fairy_spirit.png"
if os.path.exists(img_path):
    st.image(img_path, caption="🌸 Vila Harmonija 🌸", width=300)
else:
    st.error("⚠️ Slika vile nije pronađena.")

# ✨ Poetski tekst
st.markdown("""
<div class="fade-in">
    <h1>✨ Dobrodošao u svet Harmonije ✨</h1>
    <p style='text-align:center; font-size:18px;'>
        U svetu <b>TONOSAI</b>, vodi te Vila Harmonija — duh ravnoteže i lepote.<br>
        Ona šapuće kroz zvuke, boje i misli…<br><br>
        **Kosmos** + **Čovek** + **AI** = <span style="color:#b0f0ff">Živa Harmonija</span><br><br>
        🌿 Umetnost. Nauka. Duh. Zvuk. Sloboda. 🌿
    </p>
</div>
""", unsafe_allow_html=True)
footer()
