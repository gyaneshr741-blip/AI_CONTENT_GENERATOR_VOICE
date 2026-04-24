import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
import tempfile

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Voice Product Assistant", layout="wide")
st.title("🎤 Voice AI Product Assistant")

# Groq API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------------- SPEECH TO TEXT ----------------
def speech_to_text(audio_bytes):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_bytes)
            audio_path = f.name

        with open(audio_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=file,
                model="whisper-large-v3"
            )

        return transcription.text

    except Exception as e:
        st.error(f"❌ Error in transcription: {e}")
        return ""

# ---------------- INPUT MODE ----------------
mode = st.radio("Choose Input Method:", ["Text", "Voice"])

query = ""

# TEXT INPUT
if mode == "Text":
    query = st.text_input("Ask about any product")

# VOICE INPUT
elif mode == "Voice":
    st.subheader("🎙️ Speak your question")

    audio = mic_recorder(
        start_prompt="Start Recording",
        stop_prompt="Stop Recording",
        key="unique_voice_key"   # IMPORTANT
    )

    if audio:
        query = speech_to_text(audio["bytes"])
        st.success(f"You said: {query}")

# ---------------- GENERATE RESPONSE ----------------
if st.button("🚀 Get Information"):
    if query.strip() != "":
        prompt = f"""
        User question: {query}

        Give clear product information:
        - What it is
        - Features
        - Advantages
        - Price range
        - Simple explanation
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content
        st.session_state["output"] = result

    else:
        st.warning("⚠️ Please enter or speak a question")

# ---------------- OUTPUT ----------------
if "output" in st.session_state:
    st.subheader("📄 Result")
    content = st.text_area("", st.session_state["output"], height=300)

    st.download_button(
        label="⬇️ Download",
        data=content,
        file_name="product_info.txt",
        mime="text/plain"
    )
