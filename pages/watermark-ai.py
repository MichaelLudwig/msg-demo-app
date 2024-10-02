import streamlit as st
import openai
from openai import OpenAI
import os
import io
from PIL import Image
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

def analyze_image(image):
    # Bild in Bytes umwandeln
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # Bytes in Base64 kodieren
    base64_image = base64.b64encode(img_byte_arr).decode('utf-8')

    # Anfrage an GPT-4 Vision senden
    response = client.chat.completions.create(
        model=openAI_model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analysiere dieses Bild auf Wasserzeichen. Gib die Art des Wasserzeichens und die Wahrscheinlichkeit an, mit der es identifiziert wurde."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ],
            }
        ],
        max_tokens=300,
    )
    
    return response.choices[0].message['content']

st.title("Wasserzeichen-Detektor")

uploaded_file = st.file_uploader("Wählen Sie ein Bild zum Analysieren", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Hochgeladenes Bild", use_column_width=True)
    
    if st.button("Auf Wasserzeichen überprüfen"):
        with st.spinner("Analyse läuft..."):
            result = analyze_image(image)
        st.write("Analyseergebnis:")
        st.write(result)