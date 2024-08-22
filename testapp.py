import streamlit as st
import pandas as pd
import plotly.express as px

# Esimerkkidata annetuista piirteistä
data = {
    'Piirre': ['Pituus (cm)', 'BMI', 'Rasvaprosentti', 'Rasvaton massa (kg)', 'Lihasmassa (kg)', 'VO2max'],
    'Arvo': [166.6, 38.7, 30.0, 75.1, 38.6, 43]
}

df = pd.DataFrame(data)

# Luodaan kupladiagrammi Plotlyllä
fig = px.scatter(df, 
                 x='Piirre', 
                 y='Arvo', 
                 size='Arvo', 
                 color='Arvo',
                 hover_name='Piirre',
                 text='Arvo',
                 size_max=60,  # Maksimikoko kuplille
                 title="Piirteiden visualisointi kuplina")

# Keskitetään teksti kuplien sisälle
fig.update_traces(textposition='middle center')

# Näytetään kaavio Streamlitissä
st.plotly_chart(fig)
