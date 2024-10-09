import streamlit as st
import openai
from openai import OpenAI
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.core.exceptions import ClientAuthenticationError

st.set_page_config(layout="wide")

def is_managed_identity_available():
    try:
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(
            credential, "https://cognitiveservices.azure.com/.default"
        )
        # Versuchen Sie, einen Token zu erhalten
        token = token_provider()
        return True
        st.text("Token erhalten: " + token)
    except ClientAuthenticationError:
        st.text("ClientAuthenticationError")
        return False
    except Exception as e:
        st.text("Unerwarteter Fehler beim Abrufen des Tokens: " + {str(e)})
        return False

#Vorbereitung für Zugriff über Azure Managed Identity falls vorhanden


if 'ai_api_info' not in st.session_state:
        st.session_state.ai_api_info = ""


#hole dir den ai_key entweder aus der OS Umgebungsvariable oder dem Streamlit Secret Vault
if "AZURE_OPENAI_API_KEY" in os.environ:
    client = openai.AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2023-03-15-preview",
        azure_endpoint="https://mlu-azure-openai-service-sw.openai.azure.com/"
    )
    openAI_model = "gpt-4o-mini-sw"
    st.session_state.ai_api_info="Azure OpenAI Key - Region Europa"
elif os.getenv('USER') == 'appuser':
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    openAI_model = "gpt-4o-mini"
    st.session_state.ai_api_info="powered by OpenAI"
#elif os.getenv('WEBSITE_INSTANCE_ID'):
elif is_managed_identity_available():
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = openai.AzureOpenAI(
        azure_ad_token_provider=token_provider,
        api_version="2023-03-15-preview",
        azure_endpoint="https://mlu-azure-openai-service-sw.openai.azure.com/"        
    )
    openAI_model = "gpt-4o-mini-sw"
    st.session_state.ai_api_info="Azure OpenAI MI - Region Europa"
else:
    st.session_state.ai_api_info="Kein gültiger API-Schlüssel gefunden und Managed Identity nicht abrufbar."
    raise ValueError("Kein gültiger API-Schlüssel gefunden.")

# initialize chat session in streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# streamlit page title
st.title("🤖 Azure OpenAI GPT-4o-mini ChatBot")
st.text(st.session_state.ai_api_info)

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