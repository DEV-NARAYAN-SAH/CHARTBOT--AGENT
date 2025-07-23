import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
groq_client = Groq(api_key=api_key)

# Page Config
st.set_page_config(page_title="Groq Chatbot", page_icon="💬", layout="centered")

# Inject CSS styles
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(to bottom right, #1d2b64, #f8cdda);
        color: #fff;
    }

    .main-card {
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        max-width: 800px;
        margin: auto;
    }

    .header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        color: #ffffff;
        text-shadow: 2px 2px 4px #000;
    }

    .chat-box {
        height: 400px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        padding-right: 10px;
        margin-bottom: 20px;
    }

    .user-message, .assistant-message {
        padding: 14px 20px;
        border-radius: 18px;
        max-width: 70%;
        margin: 10px 0;
        font-size: 1rem;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.15);
        transition: transform 0.2s ease;
    }

    .user-message {
        background-color: #4b6cb7;
        color: white;
        align-self: flex-end;
        border-top-right-radius: 0;
    }

    .assistant-message {
        background-color: #ffe259;
        color: #222;
        align-self: flex-start;
        border-top-left-radius: 0;
    }

    .user-message:hover, .assistant-message:hover {
        transform: scale(1.02);
    }

    .stChatInputContainer {
        background-color: transparent;
    }

    /* Custom send button style */
    button[data-testid="stFormSubmitButton"] {
        background: linear-gradient(to right, #4facfe, #00f2fe) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        box-shadow: 0 5px 15px rgba(0, 242, 254, 0.4) !important;
        transition: 0.3s ease-in-out;
    }

    button[data-testid="stFormSubmitButton"]:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.6) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Page title and container
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<div class="header">💬 Chat with <span style="color:#ffe259;">DEVAI</span></div>', unsafe_allow_html=True)

# Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant. You help with user queries."}
    ]

# Chat history container
st.markdown('<div class="chat-box">', unsafe_allow_html=True)
for msg in st.session_state.messages[1:]:  # skip system message
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# User input
if prompt := st.chat_input("Ask anything..."):
    st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call Groq API
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=st.session_state.messages,
        max_tokens=800,
        temperature=0.7,
    )

    reply = response.choices[0].message.content
    st.markdown(f'<div class="assistant-message">{reply}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": reply})

st.markdown('</div>', unsafe_allow_html=True)
