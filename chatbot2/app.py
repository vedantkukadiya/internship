import streamlit as st

from services.gemini_client import GeminiClient
from memory.session_memory import SessionMemory
from prompts.career_prompt import build_prompt
from config.settings import Settings


st.set_page_config(
    page_title="Career Advisor AI",
    page_icon="🤖",
    layout="centered"
)


if "memory" not in st.session_state:
    st.session_state.memory = SessionMemory(Settings.MAX_HISTORY)

if "client" not in st.session_state:
    st.session_state.client = GeminiClient()


st.title("🎓 Career Advisor Chatbot")
st.write("Powered by Gemini AI")


# Show Chat History
for msg in st.session_state.memory.get():

    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])

    else:
        st.chat_message("assistant").write(msg["content"])


# Input Box
user_input = st.chat_input("Ask your career question...")


if user_input:

    # Show user message
    st.chat_message("user").write(user_input)

    st.session_state.memory.add("user", user_input)

    # Loading
    with st.spinner("Thinking..."):

        prompt = build_prompt(
            st.session_state.memory.get(),
            user_input
        )

        response = st.session_state.client.generate(prompt)

    # Show AI response
    st.chat_message("assistant").write(response)

    st.session_state.memory.add("assistant", response)
