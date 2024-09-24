import streamlit as st
import openai


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
    return response.choices[0].message.content


# CSS-Stile für das Layout
st.markdown("""
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        height: 80vh;
        max-height: 80vh;
        border: 1px solid #ccc;
        border-radius: 10px;
        overflow: hidden;
    }
    .chat-history {
        flex: 1;
        padding: 20px;
        overflow-y: auto;
        background-color: #ffffff;
    }
    .chat-input {
        display: flex;
        padding: 10px;
        border-top: 1px solid #ccc;
        background-color: #f9f9f9;
    }
    .chat-input input {
        flex: 1;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        margin-right: 10px;
    }
    .chat-input button {
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        background-color: #007bff;
        color: white;
        cursor: pointer;
    }
    .message {
        margin: 10px 0;
        padding: 10px;
        border-radius: 5px;
        max-width: 70%;
    }
    .message.user {
        background-color: #e1ffc7; /* Hellgrün */
        margin-left: auto; /* Rechtsbündig */
        text-align: right;
    }
    .message.assistant {
        background-color: #cce5ff; /* Hellblau */
        text-align: left; /* Links */
    }
    </style>
""", unsafe_allow_html=True)

# HTML-Layout für den Chat
st.markdown("""
    <div class="chat-container">
        <div class="chat-history" id="chat-history">
""", unsafe_allow_html=True)

# Anzeigen des Chat-Verlaufs
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
            <div class="message user">
                {message['content']}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="message assistant">
                {message['content']}
            </div>
        """, unsafe_allow_html=True)

st.markdown("""
        </div>
        <div class="chat-input">
            <input type="text" id="user-input" placeholder="Geben Sie Ihre Nachricht ein..." maxlength="500">
            <button id="send-button">Senden</button>
        </div>
    </div>
""", unsafe_allow_html=True)

# Benutzer-Eingabe und Senden der Nachricht
user_input = st.text_input("Du:", key="input", placeholder="Geben Sie Ihre Nachricht ein...", label_visibility="collapsed", max_chars=500)

if st.button("Senden", key="send_button"):
    if user_input:
        # Fügen Sie die Benutzer-Nachricht zum Chat-Verlauf hinzu
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Abrufen der Antwort von der GPT-4-Instanz
        response = get_response(user_input)
        
        # Fügen Sie die Antwort zum Chat-Verlauf hinzu
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Leeren des Eingabefelds
        st.session_state.input = ""

