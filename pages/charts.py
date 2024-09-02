import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
import altair as alt
#from vega_datasets import data

#--------------Donut Charts------------------------------------------------------

# Funktion zum Erstellen eines Donut-Charts
def create_donut_chart(percentage):
    if percentage <= 25:
        color = 'red'
    elif percentage <= 50:
        color = 'orange'
    elif percentage <= 75:
        color = '#1f77b4'
    else:
        color = 'green'
    
    fig, ax = plt.subplots()
    ax.pie([percentage, 100 - percentage], 
           labels=['', ''], 
           startangle=90, 
           colors=[color, '#d3d3d3'], 
           wedgeprops={'width': 0.3})
    
    # Prozentsatz in der Mitte des Donuts anzeigen
    ax.text(0, 0, f"{percentage}%", ha='center', va='center', fontsize=20, color=color)
    
    # Chart als Bild in einem BytesIO-Objekt speichern
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf


# Streamlit App
st.title("Tabelle mit Fertigstellungsgrad")

# Dummy-Daten
data = [
    {"text": "Lorem ipsum dolor sit amet, consectetur adipiscing. Sed do eiusmod tempor incididunt ut labore et dolore.", "percentage": 15},
    {"text": "Sed do eiusmod tempor incididunt ut labore et dolore. Magna aliqua. Ut enim ad minim veniam, quis nostrud.", "percentage": 30},
    {"text": "Magna aliqua. Ut enim ad minim veniam, quis nostrud. Exercitation ullamco laboris nisi ut aliquip ex ea.", "percentage": 55},
    {"text": "Exercitation ullamco laboris nisi ut aliquip ex ea. Lorem ipsum dolor sit amet, consectetur adipiscing. ", "percentage": 90},
]

# Tabelle erstellen
for row in data:
    col1, col2 = st.columns([3, 1])
    
    # Text in der ersten Spalte anzeigen
    col1.write(row["text"])

    # Slider zur Anpassung des Prozentsatzes
    row["percentage"] = col1.slider(f"Prozentwert für diesen Eintrag:", min_value=0, max_value=100, value=row["percentage"], step=5)
    
    
    # Donut-Chart in der zweiten Spalte anzeigen
    donut_chart = create_donut_chart(row["percentage"])
    col2.image(donut_chart, use_column_width=True)


#--------------Balkendiagamm------------------------------------------------------

# Daten für die CO2-Emissionen und Kostenverteilung
emission_categories = ['<12', '12 bis <17', '17 bis <22', '22 bis <27', '27 bis <32', '32 bis <37', '37 bis <42', '42 bis <47', '47 bis <52', '>=52']
mieter_percent = [100, 90, 80, 70, 60, 50, 40, 30, 20, 5]
vermieter_percent = [0, 10, 20, 30, 40, 50, 60, 70, 80, 95]

# Erstellen der Balkendiagramme
fig, ax = plt.subplots(figsize=(12, 6))

bar_width = 0.6
x = np.arange(len(emission_categories))

mieter_bars = ax.bar(x, mieter_percent, bar_width, label='Mieter', color='#1f77b4')
vermieter_bars = ax.bar(x, vermieter_percent, bar_width, bottom=mieter_percent, label='Vermieter', color='#ff7f0e')

# Prozentzahlen auf den Balken anzeigen
for i, (mieter, vermieter) in enumerate(zip(mieter_percent, vermieter_percent)):
    ax.text(i, mieter / 2, f'{mieter}%', ha='center', va='center', color='white', fontsize=12, fontweight='bold')
    ax.text(i, mieter + vermieter / 2, f'{vermieter}%', ha='center', va='center', color='black', fontsize=12, fontweight='bold')

# Beschriftungen und Titel
ax.set_xlabel('CO2-Emissionen in kg/(m²a)')
ax.set_ylabel('Kostenverteilung (%)')
ax.set_title('Stufenmodell zur Aufteilung der CO2-Kosten zwischen Mieter und Vermieter')
ax.set_xticks(x)
ax.set_xticklabels(emission_categories)
ax.legend()

# Zusätzliche Beschriftung für die Achsen unten
ax.annotate('Emissionsarme Gebäude', xy=(0, -0.1), xytext=(0, -0.2), xycoords='axes fraction', textcoords='offset points',
            ha='center', va='top', fontsize=10, color='blue', arrowprops=dict(arrowstyle='->', color='blue'))

ax.annotate('Emissionsreiche Gebäude', xy=(1, -0.1), xytext=(0, -0.2), xycoords='axes fraction', textcoords='offset points',
            ha='center', va='top', fontsize=10, color='blue', arrowprops=dict(arrowstyle='->', color='blue'))

# Layout anpassen
plt.tight_layout()

# Streamlit plot anzeigen
st.pyplot(fig)

#--------------Piechart------------------------------------------------------

# Daten für die Segmente
labels = ['Benzin', 'Diesel', 'Kerosin', 'Erdgas', 'Fernwärme', 'Heizöl', 'Strom']
sizes = [16.7, 12.0, 4.5, 28.2, 5.3, 3.8, 29.4]
colors = ['#ffcc00', '#3366cc', '#0099cc', '#ff6600', '#ff9900', '#cc0000', '#ffff00']
explode = (0, 0, 0, 0, 0, 0, 0)  # Hervorhebung der Segmente, falls gewünscht

# Erstellen der Tortengrafik
fig, ax = plt.subplots()
ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, pctdistance=0.85)

# Zeichnen eines Kreises in die Mitte der Tortengrafik, um einen Donut-Effekt zu erzeugen
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig.gca().add_artist(centre_circle)

# Sicherstellen, dass die Tortengrafik gleichmäßig rund ist
ax.axis('equal')

# Hinzufügen der Gesamtbeschriftungen für die Kategorien
ax.text(-1.6, 1, 'Verkehr\n33,2 %', ha='center', va='center', fontsize=14, weight='bold')
ax.text(1.6, 1, 'Strom\n29,4 %', ha='center', va='center', fontsize=14, weight='bold')
ax.text(0, -1.5, 'Wärme\n37,3 %', ha='center', va='center', fontsize=14, weight='bold')

# Layout anpassen
plt.tight_layout()

# Streamlit plot anzeigen
st.pyplot(fig)

#------------------krasser Chart ------------------------------------------------------

