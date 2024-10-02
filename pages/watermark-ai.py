import streamlit as st
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
from PIL import Image

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




load_dotenv()


st.title('Wasserzeichen AI')
image_file = st.file_uploader('Lade eine Bilddatei hoch',type = ['png', 'jpg', 'jpeg'])

if image_file:    
    image = Image.open(image_file)
    small_image_file = image.resize([int(0.25 * s) for s in image.size])
    st.image(small_image_file,caption = 'Hochgeladenes Bild')

    # Erstelle einen Button "Image analysieren" , erst bei Klick soll die Analyse starten
    # Button zum Starten der Analyse
    if st.button("Bild analysieren"):
        with st.spinner("Analyse läuft..."):    
            base64_image = base64.b64encode(small_image_file.read()).decode('utf-8')

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