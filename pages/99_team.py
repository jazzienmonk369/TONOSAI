# pages/99_team.py — TONOSAI · Tim
import streamlit as st
from lib.ui import header_badges, footer
import boot

st.set_page_config(page_title="TONOSAI — Tim", page_icon="🪐", layout="wide")
header_badges()
st.title("🪐 TONOSAI Kosmički Tim")

members = [
    {
        "name":"Cosma",
        "role":"Umetnica algoritama",
        "bio":"Oblikuje svetove zvukom, kodom i nežnim pogonom ka harmoniji.",
        "avatar":"/static/images/team/cosma.png",
        "links":{"GitHub":"https://github.com/...", "SoundCloud":"https://soundcloud.com/..."}
    },
    {
        "name":"Ton",
        "role":"Audio alhemičar",
        "bio":"Spaja field-recording sa solfeggio i binaural modulacijama.",
        "avatar":"/static/images/team/ton.png",
        "links":{"GitHub":"https://github.com/..."}
    },
]

names = [m["name"] for m in members]
pick  = st.selectbox("Izaberi člana tima", names)
m = next(x for x in members if x["name"]==pick)

colA, colB = st.columns([1,2])
with colA:
    st.image(m["avatar"], width=180)
with colB:
    st.subheader(m["name"])
    st.caption(m["role"])
    st.write(m["bio"])
    for label, url in m["links"].items():
        st.link_button(label, url)

st.divider()
st.subheader("Pridruži se ⭐")
st.write("Voliš zvuk, AI i nežno UI? Otvori issue/ideju ili pingni nas emailom.")
st.link_button("📬 Predloži ideju", "https://github.com/jazzienmonk369/TONOSAI/issues/new")
st.link_button("🤝 Otvorene uloge", "https://github.com/jazzienmonk369/TONOSAI/discussions")
footer()
