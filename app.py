import streamlit as st
import time

from services.gemini_client import GeminiClient
from memory.session_memory import SessionMemory
from prompts.career_prompt import build_prompt
from config.settings import Settings


# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Career Advisor AI",
    page_icon="🤖",
    layout="centered"
)


# -------------------------
# INITIALIZE SESSION STATE
# -------------------------
if "memory" not in st.session_state:
    st.session_state.memory = SessionMemory(Settings.MAX_HISTORY)

if "client" not in st.session_state:
    st.session_state.client = GeminiClient()


# -------------------------
# HEADER
# -------------------------
st.title("🎓 Career Advisor Chatbot")
st.caption("AI-powered career guidance using Google Gemini")

st.divider()


# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:

    st.header("📜 Chat History")

    history = st.session_state.memory.get()

    if history:
        for i, msg in enumerate(history):
            role = "🧑 You" if msg["role"] == "user" else "🤖 AI"
            st.write(f"{role}: {msg['content'][:60]}...")

    else:
        st.info("No conversation yet.")

    st.divider()

    # Clear Chat Button
    if st.button("🗑 Clear Chat"):
        st.session_state.memory.clear()
        st.success("Chat cleared!")
        time.sleep(1)
        st.rerun()


# -------------------------
# DISPLAY CHAT MESSAGES
# -------------------------
for msg in st.session_state.memory.get():

    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# -------------------------
# USER INPUT
# -------------------------
user_input = st.chat_input("Ask your career question...")


if user_input:

    # Add user message
    st.session_state.memory.add("user", user_input)

    with st.chat_message("user"):
        st.write(user_input)

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                prompt = build_prompt(
                    st.session_state.memory.get(),
                    user_input
                )

                response = st.session_state.client.generate(prompt)

            except Exception as e:
                response = "Something went wrong. Please try again."

        st.write(response)

    # Add assistant message
    st.session_state.memory.add("assistant", response)