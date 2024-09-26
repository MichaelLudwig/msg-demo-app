import streamlit as st
import openai

import os
import json

st.set_page_config(layout="wide")

#hole dir den ai_key entweder aus der OS Umgebungsvariable oder dem Streamlit Secret Vault
if "AZURE_OPENAI_API_KEY" in os.environ:
    ai_key = os.getenv("AZURE_OPENAI_API_KEY")
else:
    try:
        ai_key = st.secrets["AZURE_OPENAI_API_KEY"]
    except KeyError:
        # Wenn weder die Umgebungsvariable noch der Secret gesetzt ist
        ai_key = ""

client = openai.AzureOpenAI(
    api_key=ai_key,
    api_version="2023-03-15-preview",
    azure_endpoint="https://mlu-azure-openai-service-sw.openai.azure.com/"
)
openAI_model = "gpt-4o-mini-sw"

# initialize chat session in streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# streamlit page title
st.title("🤖 Azure OpenAI GPT-4o-mini ChatBot")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# input field for user's message
user_prompt = st.chat_input("Frag GPT-4o-mini...")

if user_prompt:
    # add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # send user's message to GPT-4o and get a response
    response = client.chat.completions.create(
        model=openAI_model,
        messages=[
            {"role": "system", "content": "Du bist ein hilfreicher Assistent"},
            *st.session_state.chat_history
        ]
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display GPT-4o's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)