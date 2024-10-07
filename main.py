import streamlit as st
import json
import os
import datetime

# Set page configuration at the top
st.set_page_config(
    page_title="LLAMA 3.1. Chat",
    page_icon="🦙",
    layout="centered"
)

# Initialize the chat history if not present already
if "chat_sessions" not in st.session_state:
    if os.path.exists("chat_sessions.json"):
        with open("chat_sessions.json", "r") as file:
            st.session_state.chat_sessions = json.load(file)
    else:
        st.session_state.chat_sessions = {}

# Function to save chat sessions to file
def save_sessions_to_file():
    with open("chat_sessions.json", "w") as file:
        json.dump(st.session_state.chat_sessions, file)

# Initialize current chat session
if "current_session" not in st.session_state:
    st.session_state.current_session = None

# Sidebar: Show all past chat sessions
with st.sidebar:
    st.title("Past Chats")
    selected_session = st.selectbox("Select a session", options=list(st.session_state.chat_sessions.keys()), index=0 if st.session_state.chat_sessions else -1)
    
    if selected_session:
        st.session_state.current_session = selected_session
        st.write("Selected Chat:", selected_session)
    
    # Button to start a new chat session
    if st.button("Start New Chat"):
        new_session_name = f"Chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.session_state.chat_sessions[new_session_name] = []
        st.session_state.current_session = new_session_name
        save_sessions_to_file()
        # Use experimental_set_query_params() to trigger a rerun
        st.experimental_set_query_params(new_chat=new_session_name)

# Check if there is a current session
if st.session_state.current_session:
    current_chat = st.session_state.chat_sessions[st.session_state.current_session]
else:
    current_chat = []

# Page title
st.title("🦙 LLAMA 3.1. ChatBot")

# Initialize user input in session state to clear after submit
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Input field for user's message
user_prompt = st.text_input("Ask LLAMA...", value=st.session_state.user_input, placeholder="Type your question or prompt...")

if user_prompt and st.session_state.current_session:
    try:
        # Append user's message to the chat session
        current_chat.append({
            "role": "user",
            "content": user_prompt,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.session_state.chat_sessions[st.session_state.current_session] = current_chat

        # Prepare messages for API (without the timestamp)
        messages_for_api = [
            {"role": "system", "content": "You are a helpful assistant"},
            *[
                {"role": msg["role"], "content": msg["content"]} for msg in current_chat
            ]
        ]

        # Simulated API response
        assistant_response = "Simulated response from LLM based on: " + user_prompt

        # Append assistant's response to the chat session
        current_chat.append({
            "role": "assistant",
            "content": assistant_response,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.session_state.chat_sessions[st.session_state.current_session] = current_chat

        # Clear the user input field after sending
        st.session_state.user_input = ""

        # Save updated chat sessions
        save_sessions_to_file()

        # Use experimental_set_query_params() to trigger a rerun
        st.experimental_set_query_params(chat_updated=datetime.datetime.now().timestamp())

    except Exception as e:
        st.error(f"Error: {str(e)}")

# Display the chat history of the current session
if st.session_state.current_session:
    st.write(f"Chat: {st.session_state.current_session}")
    for message in current_chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Save updated sessions to file periodically
save_sessions_to_file()
