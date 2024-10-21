import streamlit as st
from pptx import Presentation
from io import BytesIO

def open_pptx_template():
    # Pfad zur PowerPoint-Datei
    pptx_path = "msg_digital_template.pptx"
    
    try:
        # Öffnen der PowerPoint-Präsentation
        presentation = Presentation(pptx_path)
        st.write(f"Die Präsentation '{pptx_path}' wurde erfolgreich geöffnet.")
        st.write(f"Anzahl der Folien: {len(presentation.slides)}")
        
        # Hier können Sie weitere Aktionen mit der geöffneten Präsentation durchführen
        
        return presentation
    except Exception as e:
        st.write(f"Fehler beim Öffnen der Präsentation: {e}")
        return None


st.title("PowerPoint AI")


pres = open_pptx_template()
if pres:
    st.write("Sie können jetzt mit der Präsentation arbeiten.")
else:
    st.write("Die Präsentation konnte nicht geöffnet werden.")
