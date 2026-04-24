import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
import tempfile
import speech_recognition as sr

st.set_page_config(page_title="Voice GenAI Bot", layout="wide")
st.title("🎤 Voice AI Content Generator")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Function to convert audio to text
def speech_to_text(audio_bytes):
    recognizer = sr.Recognizer()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_bytes)
        audio_file = f.name

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except:
        return ""

# Voice Input
st.subheader("🎙️ Record Product")
audio1 = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop")

product = ""
audience = ""

if audio1:
    product = speech_to_text(audio1["bytes"])
    st.success(f"Product: {product}")

st.subheader("🎙️ Record Audience")
audio2 = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop")

if audio2:
    audience = speech_to_text(audio2["bytes"])
    st.success(f"Audience: {audience}")

# Generate content
if st.button("🚀 Generate Content"):
    if product and audience:
        prompt = f"Write marketing content for {product} targeting {audience}."

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content
        st.write(result)

    else:
        st.warning("Please record both Product and Audience")
