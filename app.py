import streamlit as st
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import tempfile

# Function to generate melody
def generate_melody(theme, tempo):
    melodies = {
        "happy": [440, 494, 523, 587, 659],  # Frequencies in Hz
        "sad": [220, 247, 262, 294, 330],
        "adventure": [330, 392, 440, 494, 523],
        "relaxing": [262, 330, 392, 440, 494],
        "rnb": [392, 440, 523, 587, 659]
    }
    
    melody = melodies.get(theme, [440, 494, 523])  # Default melody
    return melody, int(tempo)

# Function to generate sound file
def generate_audio(melody, tempo):
    song = AudioSegment.silent(duration=0)
    duration = 60000 // tempo  # Duration of each note in ms

    for freq in melody:
        note = Sine(freq).to_audio_segment(duration=duration)
        song += note + AudioSegment.silent(duration=50)  # Add a small pause

    return song

# Streamlit UI
st.title("🎵 AI Music Composer")
st.write("Pick a theme, choose a tempo, and generate a melody.")

# User Inputs
theme = st.selectbox("Choose a theme:", ["happy", "sad", "adventure", "relaxing", "rnb"])
tempo = st.slider("Tempo (BPM):", 60, 180, 120)

if st.button("Generate Music"):
    melody, tempo = generate_melody(theme, tempo)
    song = generate_audio(melody, tempo)

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        song.export(f.name, format="mp3")
        st.audio(f.name, format="audio/mp3")

    st.success(f"Generated {theme} melody at {tempo} BPM! 🎶")

