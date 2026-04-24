import streamlit as st
from groq import Groq
import speech_recognition as sr

# Page config
st.set_page_config(page_title="Voice GenAI Bot", layout="wide")
st.title("🎤 Voice AI Content Generator")

# Initialize Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Function: Voice Input
def get_voice_input(label):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info(f"🎙️ Speak {label}...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        st.success(f"{label}: {text}")
        return text
    except sr.UnknownValueError:
        st.error("❌ Could not understand audio")
        return ""
    except sr.RequestError:
        st.error("❌ Speech service error")
        return ""

# Choose input method
mode = st.radio("Choose Input Method:", ["Text", "Voice"])

product = ""
audience = ""

# TEXT INPUT
if mode == "Text":
    product = st.text_input("Enter Product")
    audience = st.text_input("Enter Audience")

# VOICE INPUT
else:
    if st.button("🎤 Speak Product"):
        product = get_voice_input("Product")

    if st.button("🎤 Speak Audience"):
        audience = get_voice_input("Audience")

# Generate content
if st.button("🚀 Generate Content"):
    if product and audience:
        prompt = f"Write marketing content for {product} targeting {audience}."

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content
        st.session_state["output"] = result
        st.write(result)

    else:
        st.warning("⚠️ Please provide both Product and Audience")

# Show + Download
if "output" in st.session_state:
    content = st.text_area("Generated Content", st.session_state["output"], height=300)

    st.download_button(
        label="⬇️ Download as TXT",
        data=content,
        file_name="marketing_content.txt",
        mime="text/plain"
    )
