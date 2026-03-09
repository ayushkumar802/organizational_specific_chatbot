import streamlit as st
from model import workflow

st.set_page_config(page_title="Chatbot", page_icon="🤖")

st.title("🤖 My Streamlit Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    # with st.chat_message(msg["role"]):
    #     st.markdown(msg["content"])
    st.chat_message(msg["role"]).markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Bot reply (dummy logic)
    response = workflow.invoke({"messages": st.session_state.messages})
    bot_reply = response['messages'][-1].content

    # Show bot message
    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

