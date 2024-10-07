import streamlit as st
import json
import os
from groq import Groq

# initialize the chat history as streamlit session state of not present already
if "chat_history" not in st.session_state:
    if os.path.exists("session_data.json"):
        with open("session_data.json", "r") as file:
            st.session_state.chat_history = json.load(file)

# initialize the current page as streamlit session state of not present already
if "current_page" not in st.session_state:
    st.session_state.current_page = 0

# save the api key to environment variable
GROQ_API_KEY = st.secrets["API_KEY"]
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# initialize the chat history as streamlit session state of not present already
if "chat_history" not in st.session_state:
    if os.path.exists("session_data.json"):
        with open("session_data.json", "r") as file:
            st.session_state.chat_history = json.load(file)
    else:
        st.session_state.chat_history = []

# save the chat history to session_data.json on every interaction
def save_to_file():
    with open("session_data.json", "w") as file:
        json.dump(st.session_state.chat_history, file)

# this will save the chat history to the file after every button press
st.cache(suspend=True)(save_to_file)

# display chat history
st.write("Chat History:")
for i, message in enumerate(st.session_state.chat_history):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# streamlit page configuration
st.set_page_config(
    page_title="LLAMA 3.1. Chat",
    page_icon="🦙",
    layout="centered"
)

# streamlit page title
st.title("🦙 LLAMA 3.1. ChatBot")

# input field for user's message:
user_prompt = st.text_input("Ask LLAMA...", value="", placeholder="Type your question or prompt...", help="Enter your question or prompt")

if user_prompt:
    try:
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

        # sens user's message to the LLM and get a response
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            *st.session_state.chat_history
        ]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )

        assistant_response = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

        # display the LLM's response
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
    except Exception as e:
        st.error("Error: " + str(e))

# display chat history
st.write("Chat History:")
for i, message in enumerate(st.session_state.chat_history):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# buttons to navigate through pages
next_page_button = None
if st.session_state.current_page > 0:
    next_page_button = st.button("Previous Page")
if next_page_button:
    st.session_state.current_page -= 1
next_page_button = None
if st.session_state.current_page < (len(st.session_state.chat_history) - 1) // 5:
    next_page_button = st.button("Next Page")
if next_page_button:
    st.session_state.current_page += 1