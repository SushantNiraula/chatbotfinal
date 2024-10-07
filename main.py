import streamlit as st
import json
import os
import datetime  # Added datetime import

# Initialize the chat history if not present already
if "chat_history" not in st.session_state:
    if os.path.exists("session_data.json"):
        with open("session_data.json", "r") as file:
            st.session_state.chat_history = json.load(file)
    else:
        st.session_state.chat_history = []

# Initialize the current page if not present already
if "current_page" not in st.session_state:
    st.session_state.current_page = 0

# Save the API key to environment variable
GROQ_API_KEY = st.secrets["API_KEY"]
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Initialize Groq client (Check the package import)
try:
    from groq import Groq
    client = Groq()
except ImportError:
    st.error("Groq package not found. Please install it.")

# Save chat history to session_data.json after every interaction
def save_to_file():
    with open("session_data.json", "w") as file:
        json.dump(st.session_state.chat_history, file)

# Streamlit page configuration
st.set_page_config(
    page_title="LLAMA 3.1. Chat",
    page_icon="🦙",
    layout="centered"
)

# Streamlit page title
st.title("🦙 LLAMA 3.1. ChatBot")

# Input field for user's message:
user_prompt = st.text_input("Ask LLAMA...", value="", placeholder="Type your question or prompt...")

if user_prompt:
    try:
        # Display user message
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

        # Send user's message to the LLM and get a response
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            *st.session_state.chat_history
        ]

        # Get the response from the model (Handle this correctly depending on API)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        assistant_response = response.choices[0].message.content

        # Save the assistant's response
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        # Save to file
        save_to_file()
    except Exception as e:
        st.error("Error: " + str(e))

# Display chat history (pagination logic)
start = st.session_state.current_page * 5
end = start + 5
for i, message in enumerate(st.session_state.chat_history[start:end]):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Buttons to navigate through pages
col1, col2 = st.columns(2)
with col1:
    if st.session_state.current_page > 0:
        if st.button("Previous Page"):
            st.session_state.current_page -= 1

with col2:
    if st.session_state.current_page < (len(st.session_state.chat_history) - 1) // 5:
        if st.button("Next Page"):
            st.session_state.current_page += 1
