import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
import tempfile

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Voice Product Info AI", layout="wide")
st.title("🎤 Voice AI Product Assistant")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ------------------ SPEECH TO TEXT (WHISPER) ------------------
def speech_to_text(audio_bytes):
    try:
        # Save audio temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_bytes)
            audio_path = f.name

        # Use Groq Whisper model
        with open(audio_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=file,
                model="whisper-large-v3"   # ✅ robust & accurate
            )

        return transcription.text

    except Exception as e:
        st.error(f"Transcription error: {e}")
        return ""

# ------------------ INPUT MODE ------------------
mode = st.radio("Choose Input Method:", ["Text", "Voice"])

query = ""

# ------------------ TEXT INPUT ------------------
if mode == "Text":
    query = st.text_input("Ask about any product")

# ------------------ VOICE INPUT ------------------
else:
    st.subheader("🎙️ Ask using voice")

    audio = mic_recorder(
        start_prompt="Start Recording",
        stop_prompt="Stop Recording",
        key="voice_input_unique"
    )

    if audio:
        query = speech_to_text(audio["bytes"])
        st.success(f"You said: {query}")
        if st.button("🚀 Get Information"):
    if query:
        prompt = f"""
        User asked: {query}

        Provide explanation with:
        - Features
        - Advantages
        - Price
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content
        st.write(result)

    else:
        st.warning("Please enter something")
