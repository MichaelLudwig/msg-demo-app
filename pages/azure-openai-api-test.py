import streamlit as st
import openai
import os

client = openai.AzureOpenAI(
    api_key="1d304241086e4f81adf346216e983c59",
    api_version="2023-03-15-preview",
    azure_endpoint="https://mlu-azure-openai-service-sw.openai.azure.com/"
    )
openAI_model = "gpt-4o-mini-sw"


st.title("Chat-GPT mit Azure OpenAI Service")

# Initialisieren Sie den Chat-Verlauf
if "messages" not in st.session_state:
    st.session_state.messages = []

# Funktion zum Abrufen der Antwort von der Azure OpenAI Service GPT-4-Instanz
def get_response(prompt):
    response = client.chat.completions.create(
        model=openAI_model,  # Ersetzen Sie dies durch den Namen Ihres GPT-4-Deployments
        messages=[
            {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]

# Benutzer-Eingabe
user_input = st.text_input("Du:", key="input")

if st.button("Senden"):
    if user_input:
        # Fügen Sie die Benutzer-Nachricht zum Chat-Verlauf hinzu
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Abrufen der Antwort von der GPT-4-Instanz
        response = get_response(user_input)
        
        # Fügen Sie die Antwort zum Chat-Verlauf hinzu
        st.session_state.messages.append({"role": "assistant", "content": response})

# Anzeigen des Chat-Verlaufs
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"**Du:** {message['content']}")
    else:
        st.write(f"**Assistent:** {message['content']}")