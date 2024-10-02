import streamlit as st
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import base64

st.set_page_config(layout="wide")

#hole dir den ai_key entweder aus der OS Umgebungsvariable oder dem Streamlit Secret Vault
if "AZURE_OPENAI_API_KEY" in os.environ:
    client = openai.AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2023-03-15-preview",
        azure_endpoint="https://mlu-azure-openai-service-sw.openai.azure.com/"
    )
    openAI_model = "gpt-4o-mini-sw"
    #st.session_state.ai_api_info="Azure OpenAI - Region Europa"
elif "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    openAI_model = "gpt-4o-mini"
    #st.session_state.ai_api_info="powered by OpenAI"
else:
    raise ValueError("Kein gültiger API-Schlüssel gefunden.")

import streamlit as st 
import os 
from dotenv import load_dotenv
import base64
from openai import OpenAI


load_dotenv()

def encode_image(image):
    return base64.b64encode(image.read()).decode('utf-8')

st.title('Wasserzeichen AI')
image_file = st.file_uploader('Lade eine Bilddatei hoch',type = ['png', 'jpg', 'jpeg'])
if image_file:
    st.image(image_file,caption = 'Hochgeladenes Bild',use_column_width =True)

    base64_image = encode_image(image_file)

    response = client.chat.completions.create(
        model = openAI_model,
    messages=[
        {"role": "system", "content": "Du bist ein Assistent der in Markdown antwortet"},
        {"role": "user", "content": [
        {"type": "text", "text": "Gibt es in diesem Bild ein Wasserzeichen und wenn ja von welchem Anbieter"},
            {"type": "image_url", "image_url": {
            "url": f"data:image/png;base64,{base64_image}"}
                    }
                ]}
            ],
            temperature=0.0,
        )
    st.write("Verwendete AI Tokens zur Analyse des Bildes: " + str(response.usage.total_tokens))
    st.markdown(response.choices[0].message.content)