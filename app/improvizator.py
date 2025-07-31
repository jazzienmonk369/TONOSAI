import streamlit as st
from mido import Message, MidiFile, MidiTrack
import tempfile
import os

# 🎹 UI podešavanja
st.title("🎼 AI Improvizator – Kosmički Generator Fraza")
st.markdown("Izaberi skalu, broj tonova i tempo!")

# Skale i opcije
skale = ["C dur", "D dorian", "E mol", "F lydian", "G mixolydian", "A eol", "B lokrijan"]
izabrana_skala = st.selectbox("🎵 Izaberi skalu:", skale)

broj_tonova = st.slider("🎶 Broj tonova u frazi:", 3, 16, 8)
tempo = st.slider("⏱️ Tempo (BPM):", 40, 240, 90)

# Dummy baza skale (za sada samo C dur)
skala_tonovi = {
    "C dur": [60, 62, 64, 65, 67, 69, 71, 72],
    "D dorian": [62, 64, 65, 67, 69, 71, 72, 74],
    "E mol": [64, 66, 67, 69, 71, 72, 74, 76],
    # Dodaj ostale po želji
}

# 🎼 Generiši MIDI dugme
if st.button("🎹 Generiši MIDI frazu"):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=0, time=0))

    tonovi = skala_tonovi.get(izabrana_skala, skala_tonovi["C dur"])

    for i in range(broj_tonova):
        note = tonovi[i % len(tonovi)]
        track.append(Message('note_on', note=note, velocity=100, time=0))
        track.append(Message('note_off', note=note, velocity=100, time=int(60000 / tempo)))

    # Sačuvaj u privremeni fajl
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as tmpfile:
        mid.save(tmpfile.name)
        st.success("✅ MIDI fraza generisana!")
        st.download_button("⬇️ Preuzmi MIDI fajl", open(tmpfile.name, "rb"), file_name="improvizacija.mid")

        # Čisti privremeni fajl
        tmp_path = tmpfile.name

# Čišćenje (opciono)
# os.remove(tmp_path)  # Može se uključiti ako želiš automatsko brisanje
