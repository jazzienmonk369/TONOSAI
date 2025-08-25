import streamlit as st
import base64
import os

st.set_page_config(
    page_title="TONOSAI | Vizija",
    page_icon="🌌",
    layout="wide"
)

# 🔊 Učitavanje zvuka
def encode_audio(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

click_sound_base64 = encode_audio("static/audio/tono_click.ogg")
bg_music_base64 = encode_audio("static/audio/ambient_loop.ogg")

# 🌌 Slika zvezda
star_local_path = "static/images/star_clickable.png"
star_img_base64 = ""
if os.path.exists(star_local_path):
    with open(star_local_path, "rb") as img:
        star_img_base64 = base64.b64encode(img.read()).decode()

# 🌠 CSS + JS
st.markdown(f"""
    <style>
        .stApp {{
            background-color: #030b26;
            background-image: url("data:image/png;base64,{star_img_base64}");
            background-size: cover;
            background-position: center;
            animation: fadeIn 2s ease-in;
            overflow: hidden;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        .title-text {{
            color: white;
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            margin-top: 80px;
        }}

        .sub-text {{
            color: white;
            text-align: center;
            font-size: 20px;
            margin-top: 10px;
        }}

        .click-star {{
            width: 48px;
            height: 48px;
            position: absolute;
            cursor: pointer;
            transition: transform 0.3s ease;
        }}

        .click-star:hover {{
            transform: scale(1.3) rotate(15deg);
        }}

        #star1 {{ top: 300px; left: 40%; }}
        #star2 {{ top: 500px; left: 60%; }}
        #star3 {{ top: 400px; left: 25%; }}
    </style>

    <script>
        function playClickSoundAndAlert(msg) {{
            var sound = document.getElementById("click-sound");
            if (sound) {{
                sound.currentTime = 0;
                sound.play();
            }}
            alert(msg);
        }}
    </script>
""", unsafe_allow_html=True)

# 🎵 Zvuk klik
if click_sound_base64:
    st.markdown(f"""
        <audio id="click-sound" src="data:audio/ogg;base64,{click_sound_base64}"></audio>
    """, unsafe_allow_html=True)

# 🎵 Pozadinska muzika sa automatskim puštanjem
if bg_music_base64:
    st.markdown(f"""
        <audio autoplay loop>
            <source src="data:audio/ogg;base64,{bg_music_base64}" type="audio/ogg">
        </audio>
    """, unsafe_allow_html=True)

# 🌌 Naslov i poruke
st.markdown('<div class="title-text">Vizija TONOSAI Studija</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">TONOSAI je mesto gde Kosmos, Čovek, AI, umetnost, nauka i duhovnost igraju zajedničku melodiju.</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">🌌 Spoj zvuka, svetlosti i uma vodi nas ka harmoničnijem svetu.</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">💫 Dobrodošli u putovanje među zvezdama.</div>', unsafe_allow_html=True)

# ✨ Zvezde sa klik efektom
stars = [
    ("star1", "✨ Kosmos te čuje – i ti sviraš njegovu pesmu."),
    ("star2", "🎶 Svaka misao je nota u simfoniji svesti."),
    ("star3", "💫 Tvoj zvuk ima oblik svetlosti u noći.")
]

for id_, message in stars:
    st.markdown(f"""
        <img src="data:image/png;base64,{star_img_base64}" class="click-star" id="{id_}" onclick="playClickSoundAndAlert('{message}')">
    """, unsafe_allow_html=True)