import streamlit as st
from pptx import Presentation
from io import BytesIO
from pptx.util import Inches, Pt
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT


def open_pptx_template():
    # Pfad zur PowerPoint-Datei
    pptx_path = "msg_digital_template.pptx"
    
    try:
        # Öffnen der PowerPoint-Präsentation
        presentation = Presentation(pptx_path)
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

aws_migration_slides = [
    {
        "titel": "Einführung in AWS Migration",
        "inhalt": [
            "Definition von Cloud-Migration",
            "Vorteile der Migration zu AWS",
            "Überblick über den AWS-Migrationsansatz",
            "Wichtige Überlegungen vor der Migration",
            "AWS Migration Competency Partner"
        ]
    },
    {
        "titel": "AWS Migration-Strategien",
        "inhalt": [
            "Rehosting (Lift-and-Shift)",
            "Replatforming",
            "Refactoring / Re-architecting",
            "Repurchasing",
            "Retire und Retain Strategien"
        ]
    },
    {
        "titel": "AWS Migration Tools",
        "inhalt": [
            "AWS Migration Hub",
            "AWS Application Discovery Service",
            "AWS Database Migration Service (DMS)",
            "AWS Server Migration Service (SMS)",
            "AWS CloudEndure Migration"
        ]
    },
    {
        "titel": "Phasen der AWS Migration",
        "inhalt": [
            "Assess: Bewertung der Migrationsbereitschaft",
            "Mobilize: Vorbereitung der Organisation",
            "Migrate & Modernize: Durchführung der Migration",
            "Operate & Optimize: Betrieb in der Cloud",
            "Sicherheit und Compliance während der Migration"
        ]
    },
    {
        "titel": "Best Practices für AWS Migration",
        "inhalt": [
            "Erstellung einer klaren Migrationsstrategie",
            "Durchführung von Proof-of-Concepts",
            "Automatisierung des Migrationsprozesses",
            "Kontinuierliche Überwachung und Optimierung",
            "Schulung und Vorbereitung des Teams"
        ]
    }
]

def add_slides(presentation,slides):

    # Definiere das Layout für die neuen Folien
    #slide_layout = presentation.slide_layouts[6]  # Layout mit Titel und Inhalt
    
    # Wähle das Layout "Titel und Inhalt weiß"
    slide_layout = None
    for layout in presentation.slide_layouts:
        if layout.name == "Titel und Inhalt weiß":
            slide_layout = layout
            break

    if not slide_layout:
        slide_layout = presentation.slide_layouts[1]
    
     # Füge die neuen Folien nach der Titelfolie ein
    for index, slide_data in enumerate(slides, start=1):
        # Füge eine neue Folie nach der Titelfolie ein
        new_slide = presentation.slides.add_slide(slide_layout)
        
         # Verschiebe die neue Folie an die richtige Position (index + 1, da die Zählung bei 0 beginnt)
        xml_slides = presentation.slides._sldIdLst
        xml_slides.insert(index, xml_slides[-1])  # Verschiebe das letzte Element an die richtige Position
        del xml_slides[-1]  # Entferne das duplizierte letzte Element
        
        # Setze den Titel
        title_shape = new_slide.shapes.title
        if title_shape:
            title_shape.text = slide_data.get("titel", "")
        else:
            print(f"Warnung: Kein Titeltextfeld für Folie '{slide_data.get('titel', '')}'")
        
        # Füge den Inhalt hinzu
        content = new_slide.placeholders[1] if len(new_slide.placeholders) > 1 else None
        if content:
            tf = content.text_frame
            
            for punkt in slide_data.get("inhalt", []):
                p = tf.add_paragraph()
                p.text = punkt
                p.level = 1

            
            # Formatiere den Text
            for paragraph in tf.paragraphs:
                if paragraph.font:
                    paragraph.font.size = Pt(18)
                    paragraph.space_before = Pt(6)
        else:
            print(f"Warnung: Kein Inhaltstextfeld für Folie '{slide_data.get('titel', '')}'")
    
    

st.title("PowerPoint AI")

presentation = open_pptx_template()
add_slides(presentation, aws_migration_slides)




#--Hauptbereich ---------------------------------------------------------------------------------------------------------------------------------------
ppt_title=st.text_input("Titel der Präsentation")
ppt_subtitle=st.text_input("Untertitel der Präsentaion")

#--Sidebar ---------------------------------------------------------------------------------------------------------------------------------------
st.sidebar.title("App-Steuerung")


#Schaltflächen für den Word Export
st.sidebar.subheader("PowerPoint Export", divider='grey')
if st.sidebar.button("PowerPoint Dokument generieren", key="ppt_export"):
    generate_ppt(presentation, ppt_title, ppt_subtitle)










