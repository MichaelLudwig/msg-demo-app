import streamlit as st
from openai import OpenAI
import os

client = OpenAI(api_key="e70fe950222747e790ba6a4ea01f9c6a")
openAI_model = "gpt-4o-mini-sw"
# Setzen Sie Ihre Azure OpenAI Service API-Schlüssel und Endpunkt
client.api_type = "azure"
client.api_base = "https://mlu-azure-openai-service-sw.openai.azure.com/"
#openai.api_version = "azureml://registries/azure-openai/models/gpt-4o-mini/versions/2024-07-18"
#client.api_key = "e70fe950222747e790ba6a4ea01f9c6a"
#openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

st.title("Chat-GPT mit Azure OpenAI Service")

# Initialisieren Sie den Chat-Verlauf
if "messages" not in st.session_state:
    st.session_state.messages = []

# Funktion zum Abrufen der Antwort von der Azure OpenAI Service GPT-4-Instanz
def get_response(prompt):
    response = client.chat.completions.create(
        engine=openAI_model,  # Ersetzen Sie dies durch den Namen Ihres GPT-4-Deployments
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