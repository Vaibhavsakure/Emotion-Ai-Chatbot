import streamlit as st
from emotion_model import detect_emotion
from intent_model import detect_intent
from hf_reply import hf_stream_reply

from gtts import gTTS
import base64
from datetime import datetime
import time
import os

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(page_title="Emotion AI ChatBot", page_icon="🎤", layout="centered")

# ------------------------------------------------------
# CSS (Beautiful ChatGPT + Voice UI)
# ------------------------------------------------------
st.markdown("""
<style>

* {font-family:'Inter',sans-serif;}

.stApp {
    background: linear-gradient(160deg, #0f172a, #1e293b);
}

/* Title */
.title {
    text-align:center;
    font-size:3rem;
    font-weight:800;
    background:linear-gradient(135deg,#6366f1,#a78bfa,#ec4899);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

/* Chat window */
.chat-window {
    padding:20px;
    max-height:520px;
    overflow-y:auto;
}

/* User bubble */
.msg-user {
    background:linear-gradient(135deg,#6366f1,#8b5cf6);
    color:white;
    padding:14px 20px;
    border-radius:20px 20px 4px 20px;
    max-width:70%;
    margin-left:auto;
    margin-bottom:15px;
    box-shadow:0 4px 20px rgba(99,102,241,0.25);
}

/* Bot bubble */
.msg-bot {
    background:white;
    color:#1e293b;
    padding:14px 20px;
    border-radius:20px 20px 20px 4px;
    max-width:70%;
    margin-right:auto;
    margin-bottom:25px;
    box-shadow:0 4px 20px rgba(0,0,0,0.15);
}

/* Play button */
.voice-btn {
    background:#6366f1;
    color:white;
    padding:6px 14px;
    border-radius:10px;
    font-size:0.8rem;
    margin-top:-10px;
    cursor:pointer;
}

.stButton>button {
    background:linear-gradient(135deg,#6366f1,#8b5cf6);
    color:white;
    border:none;
    padding:10px 20px;
    border-radius:12px;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)



# ------------------------------------------------------
# HEADER
# ------------------------------------------------------
st.markdown("<h1 class='title'>Emotion AI ChatBot 🤖</h1>", unsafe_allow_html=True)
st.write("<p style='text-align:center;color:#94a3b8;'>AI that understands emotions + speaks replies.</p>", unsafe_allow_html=True)



# ------------------------------------------------------
# Init chat memory
# ------------------------------------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []



# ------------------------------------------------------
# Function to Convert Bot Text → MP3
# ------------------------------------------------------
def generate_voice(text, index):
    """Generates an MP3 file using gTTS."""
    try:
        filename = f"voice_{index}.mp3"
        tts = gTTS(text=text, lang="en")
        tts.save(filename)

        with open(filename, "rb") as f:
            audio_bytes = f.read()
        
        b64 = base64.b64encode(audio_bytes).decode()

        audio_html = f"""
        <audio controls autoplay style="width: 260px; margin-top: 10px;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        return audio_html
    except Exception as e:
        return f"<p style='color:red;'>Voice error: {e}</p>"



# ------------------------------------------------------
# SHOW CHAT MESSAGES
# ------------------------------------------------------
st.markdown("<div class='chat-window'>", unsafe_allow_html=True)

for i, msg in enumerate(st.session_state.chat):
    cls = "msg-user" if msg["sender"] == "user" else "msg-bot"

    st.markdown(f"<div class='{cls}'>{msg['message']}</div>", unsafe_allow_html=True)

    # Add voice player for bot messages
    if msg["sender"] == "bot":
        audio_html = generate_voice(msg["clean_msg"], i)
        st.markdown(audio_html, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)



# ------------------------------------------------------
# INPUT FORM
# ------------------------------------------------------
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])

    with col1:
        user_msg = st.text_input("", placeholder="Type your message...")

    with col2:
        send = st.form_submit_button("Send")



# ------------------------------------------------------
# HANDLE SEND BUTTON
# ------------------------------------------------------
if send and user_msg.strip():
    st.session_state.chat.append({"sender": "user", "message": user_msg})

    emotion = detect_emotion(user_msg)
    intent = detect_intent(user_msg)

    placeholder = st.empty()
    bot_typing = "Typing..."
    placeholder.markdown(f"<div class='msg-bot'>{bot_typing}</div>", unsafe_allow_html=True)

    bot_reply = ""
    for chunk in hf_stream_reply(user_msg, emotion, intent, st.session_state.chat):
        bot_reply += chunk
        placeholder.markdown(f"<div class='msg-bot'>{bot_reply}...</div>", unsafe_allow_html=True)

    full_reply = bot_reply + f"<br><br>💬 Emotion: <b>{emotion}</b> | 🎯 Intent: <b>{intent}</b>"

    st.session_state.chat.append({
        "sender": "bot",
        "message": full_reply,
        "clean_msg": bot_reply   # For TTS only
    })

    st.rerun()



# ------------------------------------------------------
# CLEAR CHAT
# ------------------------------------------------------
if st.button("🗑️ Clear Chat"):
    st.session_state.chat = []
    st.rerun()
