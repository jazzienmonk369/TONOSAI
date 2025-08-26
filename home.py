import streamlit as st

st.set_page_config(
    page_title="TONOSAI Studio",
    page_icon="static/favicon.png",
    layout="wide",
)

import streamlit as st
import os

# 🌌 Konfiguracija stranice
st.set_page_config(page_title="TONOSAI | Kosmičke Zvezde", page_icon="🌌", layout="centered")

# 📂 Putanje do foldera
audio_path = "static/audio"
img_path = "static/star_images"

# 🎵 Pozadinska muzika
st.audio(os.path.join(audio_path, "vibraphone_motif_528hz_slowfade.ogg"))

# 🌠 Poetska poruka
st.markdown("<h2 style='text-align: center; color: white;'>Zvezde odzvanjaju... Harmonia te zove.</h2>", unsafe_allow_html=True)

# 🎨 Stil za zvezde koje svetlucaju i lelujaju
st.markdown(
    """
    <style>
    .star-button {
        animation: pulse 3s infinite ease-in-out, float 4s infinite ease-in-out;
        border-radius: 50%;
        font-size: 36px;
        padding: 10px 20px;
        margin: 10px;
        border: none;
        cursor: pointer;
        background-color: transparent;
        transition: transform 0.3s ease;
    }

    .star-button:hover {
        transform: scale(1.1) rotate(3deg);
        box-shadow: 0 0 15px rgba(255,255,255,0.8);
    }

    @keyframes pulse {
        0% { opacity: 0.8; }
        50% { opacity: 1; }
        100% { opacity: 0.8; }
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }

    /* 🌌 Pozadina */
    .stApp {
        background-image: url('static/star_images/star_sky_bg.png');
        background-size: cover;
        background-position: center;
    }

    /* Centriranje dugmadi */
    .star-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        margin-top: 30px;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🌟 HTML za dugmad-zvezde
st.markdown(
    """
    <div class="star-container">
        <button class="star-button" onclick="playStar1()">🎵</button>
        <button class="star-button" onclick="playStar2()">🌟</button>
        <button class="star-button" onclick="playStar3()">🧚‍♀️</button>
    </div>
    """,
    unsafe_allow_html=True
)

# 🔊 JavaScript za zvuk kliknutih zvezda
st.markdown(
    f"""
    <script>
    function playStar1() {{
        new Audio("{audio_path}/click_star1_528hz.ogg").play();
    }}
    function playStar2() {{
        new Audio("{audio_path}/click_star2_732hz.ogg").play();
    }}
    function playStar3() {{
        new Audio("{audio_path}/click_star3_432hz.ogg").play();
    }}
    </script>
    """,
    unsafe_allow_html=True
)