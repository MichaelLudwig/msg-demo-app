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


def generate_ppt(presentation, title, subtitle):
    # Ändern des Titels und Untertitels
    for slide in presentation.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                if shape.text == "*title*":
                    shape.text = title
                elif shape.text == "*subtitle*":
                    shape.text = subtitle
    
    # Speichern der Präsentation in einem BytesIO-Objekt
    buffer = BytesIO()
    presentation.save(buffer)
    buffer.seek(0)
    pptx_file = buffer

    # Bereitstellen der Datei zum Download
    st.sidebar.download_button(
        label="PowerPoint-Präsentation herunterladen",
        data=pptx_file,
        file_name="Präsentation.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )


st.title("PowerPoint AI")

presentation = open_pptx_template()
if presentation:
    st.write("Sie können jetzt mit der Präsentation arbeiten.")
else:
    st.write("Die Präsentation konnte nicht geöffnet werden.")





#--Hauptbereich ---------------------------------------------------------------------------------------------------------------------------------------
ppt_title=st.text_input("Titel der Präsentation")
ppt_subtitle=st.text_input("Untertitel der Präsentaion")

#--Sidebar ---------------------------------------------------------------------------------------------------------------------------------------
st.sidebar.title("App-Steuerung")


#Schaltflächen für den Word Export
st.sidebar.subheader("PowerPoint Export", divider='grey')
if st.sidebar.button("PowerPoint Dokument generieren", key="ppt_export"):
    generate_ppt(presentation, ppt_title, ppt_subtitle)










