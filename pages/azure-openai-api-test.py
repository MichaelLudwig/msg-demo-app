import streamlit as st
import openai
from streamlit_chat import message

# Streamlit Setup
st.set_page_config(page_title="Chatbot", page_icon="🤖")




client = openai.AzureOpenAI(
    api_key="1d304241086e4f81adf346216e983c59",
    api_version="2023-03-15-preview",
    azure_endpoint="https://mlu-azure-openai-service-sw.openai.azure.com/"
)
openAI_model = "gpt-4o-mini-sw"


st.title("Chat-GPT mit Azure OpenAI Service")

# Chat-Verlauf initialisieren
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "Du bist ein hilfreicher Assistent."}]

# Funktion zum Abrufen der Antwort von der Azure OpenAI Service GPT-4-Instanz
def get_response(prompt):
    response = client.chat.completions.create(
        model=openAI_model,  # Ersetzen Sie dies durch den Namen Ihres GPT-4-Deployments
        messages=st.session_state["messages"]
    )
    return response.choices[0].message.content


# Eingabe des Nutzers
user_input = st.text_input("Frag etwas")

if user_input:
    # Speichere die Nutzeranfrage im Verlauf
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # GPT-4 Antwort generieren
    with st.spinner("GPT-4 denkt nach..."):
        response = get_response(user_input)
    
    # Antwort im Chat-Verlauf speichern
    st.session_state["messages"].append({"role": "assistant", "content": response})

# Chat-Verlauf anzeigen
if st.session_state["messages"]:
    for i, msg in enumerate(st.session_state["messages"]):
        if msg["role"] == "user":
            message(msg["content"], is_user=True, key=str(i) + '_user')
        else:
            message(msg["content"], key=str(i))

# Benutzer-Eingabe und Senden der Nachricht
if st.button("Senden", key="send_button"):
    user_input = st.session_state.input  # Hier sollte es st.session_state.input sein
    if user_input:
        # Fügen Sie die Benutzer-Nachricht zum Chat-Verlauf hinzu
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Abrufen der Antwort von der GPT-4-Instanz
        response = get_response(user_input)  # Hier muss get_response verwendet werden
        
        # Fügen Sie die Antwort zum Chat-Verlauf hinzu
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Leeren des Eingabefelds
        st.session_state.input = ""
