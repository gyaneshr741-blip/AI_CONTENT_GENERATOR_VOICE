import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import tempfile

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Voice Product Info AI", layout="wide")
st.title("🎤 Voice AI Product Assistant")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ------------------ FUNCTION ------------------
def speech_to_text(audio_bytes):
    recognizer = sr.Recognizer()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_bytes)
        audio_path = f.name

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except:
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
        key="voice_input_unique"   # ✅ FIXED ERROR
    )

    if audio:
        query = speech_to_text(audio["bytes"])
        st.success(f"You said: {query}")

# ------------------ AI RESPONSE ------------------
if st.button("🚀 Get Information"):
    if query:
        prompt = f"""
        User asked: {query}

        Provide a clear explanation including:
        - What it is
        - Key features
        - Advantages
        - Price range (if possible)
        - Simple explanation
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content
        st.session_state["output"] = result
        st.write(result)

    else:
        st.warning("⚠️ Please enter or speak a product")

# ------------------ DOWNLOAD ------------------
if "output" in st.session_state:
    content = st.text_area("Generated Information", st.session_state["output"], height=300)

    st.download_button(
        label="⬇️ Download as TXT",
        data=content,
        file_name="product_info.txt",
        mime="text/plain"
    )
