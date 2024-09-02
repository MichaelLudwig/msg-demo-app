import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
import pandas as pd
import altair as alt
from vega_datasets import data


#--------------Balkendiagamm------------------------------------------------------

st.header("Bar Chart", anchor="barchart", divider="blue")

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

st.header("Pie Chart", anchor="piechart", divider="blue")

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

st.header("Klima Chart", anchor="climachart", divider="blue")

@st.cache_data
def get_chart_98185(use_container_width: bool):
    
    #from vega_datasets import data

    source = data.seattle_weather.url

    step = 30
    overlap = 1

    chart = alt.Chart(source, height=step).transform_timeunit(
        Month='month(date)'
    ).transform_joinaggregate(
        mean_temp='mean(temp_max)', groupby=['Month']
    ).transform_bin(
        ['bin_max', 'bin_min'], 'temp_max'
    ).transform_aggregate(
        value='count()', groupby=['Month', 'mean_temp', 'bin_min', 'bin_max']
    ).transform_impute(
        impute='value', groupby=['Month', 'mean_temp'], key='bin_min', value=0
    ).mark_area(
        interpolate='monotone',
        fillOpacity=0.8,
        stroke='lightgray',
        strokeWidth=0.5
    ).encode(
        alt.X('bin_min:Q', bin='binned', title='Maximum Daily Temperature (C)'),
        alt.Y(
            'value:Q',
            scale=alt.Scale(range=[step, -step * overlap]),
            axis=None
        ),
        alt.Fill(
            'mean_temp:Q',
            legend=None,
            scale=alt.Scale(domain=[30, 5], scheme='redyellowblue')
        )
    ).facet(
        row=alt.Row(
            'Month:T',
            title=None,
            header=alt.Header(labelAngle=0, labelAlign='right', format='%B')
        )
    ).properties(
        title='Seattle Weather',
        bounds='flush'
    ).configure_facet(
        spacing=0
    ).configure_view(
        stroke=None
    ).configure_title(
        anchor='end'
    )

    st.altair_chart(chart, theme="streamlit", use_container_width=True)


get_chart_98185(True)

#------------------Aktien Chart ------------------------------------------------------

st.header("Aktien Chart", anchor="stockchart", divider="blue")

#@st.experimental_memo
def get_chart_98552(use_container_width: bool):
    #import altair as alt
    #from vega_datasets import data

    source = data.stocks()

    chart = alt.Chart(source).mark_line(point=True).encode(
        x='date:T',
        y='price:Q',
        color='symbol:N'
    )

    st.altair_chart(chart, theme="streamlit", use_container_width=True)


get_chart_98552(True)

#------------------Gantt Chart ------------------------------------------------------
st.header("Gantt Chart", anchor="ganttchart", divider="blue")

def get_chart_56029(use_container_width: bool):
    import altair as alt
    import pandas as pd

    source = pd.DataFrame([
        {"task": "A", "start": 1, "end": 3},
        {"task": "B", "start": 3, "end": 8},
        {"task": "C", "start": 8, "end": 10}
    ])

    chart = alt.Chart(source).mark_bar().encode(
        x='start',
        x2='end',
        y='task'
    )

    st.altair_chart(chart, theme="streamlit", use_container_width=True)


get_chart_56029(True)

#------------------Heatmap ------------------------------------------------------
st.header("Heatmap", anchor="heatmap", divider="blue")

def get_chart_2303(use_container_width: bool):
    #import altair as alt
    #from vega_datasets import data

    source = data.movies.url

    chart = alt.Chart(source).mark_rect().encode(
        alt.X('IMDB_Rating:Q', bin=alt.Bin(maxbins=60)),
        alt.Y('Rotten_Tomatoes_Rating:Q', bin=alt.Bin(maxbins=40)),
        alt.Color('count():Q', scale=alt.Scale(scheme='greenblue'))
    )

    st.altair_chart(chart, theme="streamlit", use_container_width=True)
get_chart_2303(True)

#------------------ US Airports ------------------------------------------------------
st.header("US Airports", anchor="airports", divider="blue")

def get_chart_99637(use_container_width: bool):
    import altair as alt
    from vega_datasets import data

    airports = data.airports()
    states = alt.topo_feature(data.us_10m.url, feature='states')

    # US states background
    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).properties(
        width=500,
        height=300
    ).project('albersUsa')

    # airport positions on background
    points = alt.Chart(airports).mark_circle(
        size=10,
        color='steelblue'
    ).encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        tooltip=['name', 'city', 'state']
    )

    chart = background + points

    st.altair_chart(chart, theme="streamlit", use_container_width=True)

get_chart_99637(True)

#------------------ Interactive Chart ------------------------------------------------------
st.header("Interaktiver Chart", anchor="interactive", divider="blue")

def get_chart_61030(use_container_width: bool):
    #import altair as alt
    #import pandas as pd
    #import numpy as np

    np.random.seed(0)

    n_objects = 20
    n_times = 50

    # Create one (x, y) pair of metadata per object
    locations = pd.DataFrame({
        'id': range(n_objects),
        'x': np.random.randn(n_objects),
        'y': np.random.randn(n_objects)
    })

    # Create a 50-element time-series for each object
    timeseries = pd.DataFrame(np.random.randn(n_times, n_objects).cumsum(0),
                              columns=locations['id'],
                              index=pd.RangeIndex(0, n_times, name='time'))

    # Melt the wide-form timeseries into a long-form view
    timeseries = timeseries.reset_index().melt('time')

    # Merge the (x, y) metadata into the long-form view
    timeseries['id'] = timeseries['id'].astype(int)  # make merge not complain
    data = pd.merge(timeseries, locations, on='id')

    # Data is prepared, now make a chart

    selector = alt.selection_single(empty='all', fields=['id'])

    base = alt.Chart(data).properties(
        width=250,
        height=250
    ).add_selection(selector)

    points = base.mark_point(filled=True, size=200).encode(
        x='mean(x)',
        y='mean(y)',
        color=alt.condition(selector, 'id:O', alt.value('lightgray'), legend=None),
    )

    timeseries = base.mark_line().encode(
        x='time',
        y=alt.Y('value', scale=alt.Scale(domain=(-15, 15))),
        color=alt.Color('id:O', legend=None)
    ).transform_filter(
        selector
    )

    chart = points | timeseries

    st.altair_chart(chart, theme="streamlit", use_container_width=True)
get_chart_61030(True)

#------------------ Regression Chart ------------------------------------------------------
st.header("Regression Chart", anchor="regression", divider="blue")

def get_chart_78749(use_container_width: bool):
    #import numpy as np
    #import pandas as pd
    #import altair as alt

    # Generate some random data
    rng = np.random.RandomState(1)
    x = rng.rand(40) ** 2
    y = 10 - 1.0 / (x + 0.1) + rng.randn(40)
    source = pd.DataFrame({"x": x, "y": y})

    # Define the degree of the polynomial fits
    degree_list = [1, 3, 5]

    base = alt.Chart(source).mark_circle(color="black").encode(
            alt.X("x"), alt.Y("y")
    )

    polynomial_fit = [
        base.transform_regression(
            "x", "y", method="poly", order=order, as_=["x", str(order)]
        )
        .mark_line()
        .transform_fold([str(order)], as_=["degree", "y"])
        .encode(alt.Color("degree:N"))
        for order in degree_list
    ]

    chart = alt.layer(base, *polynomial_fit)

    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])

    with tab1:
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
    with tab2:
        st.altair_chart(chart, theme=None, use_container_width=True)
    get_chart_78749(True)
