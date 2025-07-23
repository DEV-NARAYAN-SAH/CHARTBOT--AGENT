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
st.set_page_config(page_title="Groq Chatbot", page_icon="💬")

st.title("💬 Chat with DEVAI (Groq)")

# Initialize chat memory in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant. You help with user queries."}
    ]

# Show chat history
for msg in st.session_state.messages[1:]:  # skip system message
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask anything..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call Groq API
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=st.session_state.messages,
        max_tokens=800,
        temperature=0.7,
    )

    reply = response.choices[0].message.content
    st.chat_message("assistant").markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
