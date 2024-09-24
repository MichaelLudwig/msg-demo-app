import streamlit as st
import openai

# OpenAI API-Client initialisieren
client = openai.AzureOpenAI(
    api_key="1d304241086e4f81adf346216e983c59",
    api_version="2023-03-15-preview",
    azure_endpoint="https://mlu-azure-openai-service-sw.openai.azure.com/"
)
openAI_model = "gpt-4o-mini-sw"

# Streamlit-Seite konfigurieren
st.set_page_config(page_title="Chat-GPT mit Azure OpenAI Service", page_icon="🤖")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hi"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.ChatCompletion.create(
            model=openAI_model,
            messages=[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages], stream=True):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})