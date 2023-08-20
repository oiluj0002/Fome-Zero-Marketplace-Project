import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(
    page_title = 'Home',
    page_icon = '🔵'
)

with st.sidebar:
    image = Image.open('logo.png')
    st.image(image, width= 120)

    st.title('Fome Zero')
    st.header('Marketplace de restaurantes')
    st.markdown('''---''')

    st.header('Dados tratados')
    df = pd.read_csv('dataset/fome_zero_cleaned.csv')
    @st.cache_data
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    csv = convert_df(df)
    st.download_button(
        label="Download",
        data=csv,
        file_name='fome_zero_cleaned.csv',
        mime='text/csv',
    )
    st.markdown('''---''')

    st.header('Powered by Oiluj')

st.write('# Fome Zero - Strategy Dashboard')

st.markdown(
    """
        Data Dashboard foi construído para acompanhar os principais indicadores dos restaurantes cadastrados na plataforma Fome Zero.

        ### Como utilizar esse Strategy Dashboard?
        - Visão Geral:
            - Métricas gerais dos dados.
            - Insights de geolocalização.
        - Visão Países:
            - Acompanhamento dos indicadores entre os países.
        - Visão Cidades:
            - Acompanhamento dos indicadores entre as cidades.
        - Visão Restaurantes:
            - Indicadores dos restaurantes cadastrados.
            - Indicadores dos tipos de culinária.

        ### Ask for Help
        - Júlio Gabriel
            - Email: juliogabriel.pe@gmail.com
            - Discord: @oiluj0002
    """
)