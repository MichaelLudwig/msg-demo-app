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
    st.print(response.choices[0].message)
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
    .chat-input button:disabled {
        background-color: #ccc;
        cursor: not-allowed;
    }
    .message {
        margin: 10px 0;
    }
    .message.user {
        text-align: right;
    }
    .message.assistant {
        text-align: left;
    }
    .message .content {
        display: inline-block;
        padding: 10px;
        border-radius: 5px;
    }
    .message.user .content {
        background-color: #e1ffc7;
    }
    .message.assistant .content {
        background-color: #f0f0f0;
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
                <div class="content">{message['content']}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="message assistant">
                <div class="content">{message['content']}</div>
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

# JavaScript für die Eingabe und das Senden der Nachricht
st.markdown("""
    <script>
    const input = document.getElementById('user-input');
    const button = document.getElementById('send-button');
    const chatHistory = document.getElementById('chat-history');

    button.addEventListener('click', () => {
        const userInput = input.value;
        if (userInput) {
            window.parent.postMessage({ type: 'user_input', content: userInput }, '*');
            input.value = '';
        }
    });

    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            button.click();
        }
    });

    window.addEventListener('message', (event) => {
        if (event.data.type === 'new_message') {
            const message = document.createElement('div');
            message.className = `message ${event.data.role}`;
            message.innerHTML = `<div class="content">${event.data.content}</div>`;
            chatHistory.appendChild(message);
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
    });
    </script>
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
        
        # Senden der neuen Nachrichten an das Frontend
        st.markdown(f"""
            <script>
            window.parent.postMessage({{ type: 'new_message', role: 'user', content: '{user_input}' }}, '*');
            window.parent.postMessage({{ type: 'new_message', role: 'assistant', content: '{response}' }}, '*');
            </script>
        """, unsafe_allow_html=True)