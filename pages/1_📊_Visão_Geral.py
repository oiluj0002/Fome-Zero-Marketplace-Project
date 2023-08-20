#========================================================
# IMPORT LIBRARIES
#========================================================
import pandas as pd
import plotly.express as px
import numpy as np
import inflection
import folium
from folium.plugins import MarkerCluster
import plotly.graph_objects as go
import streamlit as st
from streamlit_folium import folium_static
from PIL import Image

#=======================================================
# FUNCTIONS
#=======================================================
def clean_data( df1 ):
    '''
    Função que prepara e limpa o dataframe
        
        Limpezas efetuadas:
            1. Formatação do título das colunas
            2. Remoção de linhas duplicadas
            3. Remoção de colunas com valores idênticos
            4. Formatação da coluna 'cuisines' para mostrar 1 tipo de culinária
            5. Remoção dos 'nan' da coluna 'cuisines'
            6. Remoção de possível erro de digitação
            7. Criação das colunas:
                'color_name'= nome das cores
                'country_name' = nome dos países
                'price_type' = nome do tipo de preço
                'exchange_rate' = taxa de câmbio USD/currency
                'average_cost_for_two_USD' = preço para dois em dólar (data fixa)
        
            Input: Dataframe
            Output: Dataframe
    '''
    #---------------------------------------------------
    # SUBFUNCIONS
    #---------------------------------------------------
    #renomear colunas do dataframe
    def rename_columns(dataframe):
        df = dataframe.copy()
        title = lambda x: inflection.titleize(x)
        spaces = lambda x: x.replace(' ', '')
        snakecase = lambda x: inflection.underscore(x)
        cols_old = list(df.columns)
        cols_old = list(map(title, cols_old))
        cols_old = list(map(spaces, cols_old))
        cols_new = list(map(snakecase, cols_old))
        df.columns = cols_new
        return df
    
    #nome das cores por código
    COLORS = {
    '3F7E00': 'darkgreen',
    '5BA829': 'green',
    '9ACD32': 'lightgreen',
    'CDD614': 'orange',
    'FFBA00': 'red',
    'CBCBC8': 'darkred',
    'FF7800': 'darkred'
    }
    def color_name(color_code):
        return COLORS[color_code]
    
    #preenchimento do nome dos países
    COUNTRIES = {
    1: 'India',
    14: 'Australia',
    30: 'Brazil',
    37: 'Canada',
    94: 'Indonesia',
    148: 'New Zealand',
    162: 'Philippines',
    166: 'Qatar',
    184: 'Singapore',
    189: 'South Africa',
    191: 'Sri Lanka',
    208: 'Turkey',
    214: 'United Arab Emirates',
    215: 'England',
    216: 'United States of America'
    }
    def country_name(country_id):
        return COUNTRIES[country_id]
    
    #rótulo do tipo de preço dos pratos
    def create_price_type(price_range):
        if price_range == 1:
            return 'cheap'
        elif price_range == 2:
            return 'normal'
        elif price_range == 3:
            return 'expensive'
        else:
            return 'gourmet'

    #conversão de moeda para 'US dollar'
    #date = 13-08-2023
    EXCHANGE = {
        'Indonesia': 0.000065735428,
        'Sri Lanka': 0.0031340417,
        'Philippines': 0.073999949,
        'India': 0.012060175,
        'South Africa': 0.052876995,
        'Qatar': 0.27472527,
        'United Arab Emirates': 0.27229408,
        'Singapore': 0.73957914,
        'Brazil': 0.20388112,
        'Turkey': 0.037143494,
        'Australia': 0.65059812,
        'New Zealand': 0.59840393,
        'United States of America': 1,
        'England': 1.2695533,
        'Canada': 0.7441021
    }
    def exchange_rate(country_name):
        return EXCHANGE[country_name]

    #---------------------------------------------------
    # CODE
    #---------------------------------------------------
    #renomeando títulos das colunas
    df1 = rename_columns( df1 )

    #removendo dados duplicados
    df1 = df1.drop_duplicates().reset_index(drop=True)

    #removendo coluna com mesmos valores
    df1 = df1.drop('switch_to_order_menu', axis=1)

    #removendo linha com outlier muito acentuado 
        #Obs: provável erro de digitação, pois custava mais de 2 milhões e era categorizado como 'cheap'
    df1 = df1.drop(356, axis=0).reset_index(drop=True)

    #categorizar restaurantes por um tipo de culinária
    df1['cuisines'] = df1['cuisines'].astype(str)
    df1.loc[:, 'cuisines'] = df1.loc[:, 'cuisines'].apply(lambda x: x.split(', ')[0])

    #retirada dos nan's da coluna cuisines
    linhas_select = df1['cuisines'] != 'nan'
    df1 = df1.loc[linhas_select, :].reset_index(drop=True)

    #criando coluna 'color_name' e preenchendo com o nome das cores
    df1['color_name'] = ''
    for i in range(len(df1)):
        df1.loc[i, 'color_name'] = color_name(df1.loc[i, 'rating_color'])
    
    #criando coluna 'country_name' e preenchendo com o nome dos países
    df1['country_name'] = ''
    for i in range(len(df1)):
        df1.loc[i, 'country_name'] = country_name(df1.loc[i, 'country_code'])
    
    #criando coluna 'price_type'
    df1['price_type'] = ''
    for i in range(len(df1)):
        df1.loc[i, 'price_type'] = create_price_type(df1.loc[i, 'price_range'])
    
    #criando coluna 'exchange_rate' e convertendo os preços para dólar
    df1['exchange_rate'] = ''
    for i in range(len(df1)):
        df1.loc[i, 'exchange_rate'] = exchange_rate(df1.loc[i, 'country_name'])
        #conversão para dólar
    df1['average_cost_for_two_USD'] = np.array(df1['average_cost_for_two']) * np.array(df1['exchange_rate'])

    return df1

def country_map( df1 ):
    '''
        Função que elabora um mapa destacando a localização de todos os restaurantes cadastrados
        Input: dataframe
        Output: mapa
    '''
    df2 = (df1.loc[:, ['restaurant_name', 'longitude', 'latitude', 'cuisines', 'average_cost_for_two_USD', 'color_name', 'aggregate_rating']])
    df2['average_cost_for_two_USD'] = df2['average_cost_for_two_USD'].astype(float).round(2)

    restaurant_map = folium.Map()
    marker_cluster = MarkerCluster().add_to(restaurant_map)
    for i, location_info in df2.iterrows():
        folium.Marker(
            [location_info['latitude'],
            location_info['longitude']],
            popup=folium.Popup(html=f"<b>{location_info['restaurant_name']}</b><br><br>Valor médio para dois: ${location_info['average_cost_for_two_USD']} Dólares<br>Culinária: {location_info['cuisines']}<br>Nota média: {location_info['aggregate_rating']}/5.0", max_width=300),
            icon=folium.Icon(color=location_info['color_name'], icon='utensils', prefix='fa')
        ).add_to(marker_cluster)

    folium_static(restaurant_map, width=1024, height=600)

    return None
#---------------------------------- CODE LOGIC STRUTURE -----------------------------------

#========================================================
# IMPORT DATASET
#========================================================
df = pd.read_csv('dataset/zomato.csv')

#========================================================
# CLEAN DATA
#========================================================
df1 = clean_data( df )

#========================================================
# SET STREAMLIT PAGE WIDTH
#========================================================
st.set_page_config(page_title='Visão Geral', page_icon='📊', layout='wide')

#========================================================
# SIDEBAR LAYOUT
#========================================================
with st.sidebar:
    image = Image.open('logo.png')
    st.image(image, width=120)

    st.title('Fome Zero')
    st.header('Marketplace de restaurantes')
    st.markdown('''---''')

    st.header('Filtros')

    #selecionar países
    country_options = st.multiselect(
        'Selecione quais países deseja visualizar os dados',
        ['Philippines', 'Brazil', 'Australia', 'United States of America',
        'Canada', 'Singapore', 'United Arab Emirates', 'India',
        'Indonesia', 'New Zealand', 'England', 'Qatar', 'South Africa',
         'Sri Lanka', 'Turkey'],
        default = []
    )
    st.markdown('''---''')

    st.header('Powered by Oiluj')

#filtro países
if not country_options:
    df1 = df1
else:
    linhas_select = df1['country_name'].isin(country_options)
    df1 = df1.loc[linhas_select, :]

#========================================================
# PAGE LAYOUT
#========================================================
st.markdown('# 📊 Visão Geral')

with st.container():
    st.markdown('## Métricas Gerais')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        df2 = df1['restaurant_id'].nunique()
        st.metric(label = 'Restaurantes cadastrados', value=df2)
    
    with col2:
        df2 = df1['country_code'].nunique()
        st.metric(label = 'Países cadastrados', value=df2)
    
    with col3:
        df2 = df1['city'].nunique()
        st.metric(label='Cidades cadastradas', value=df2)
    
    with col4:
        df2 = df1['votes'].sum()
        st.metric(label='Total de avaliações realizadas', value=df2)
    
    with col5:
        df2 = df1['cuisines'].nunique()
        st.metric(label='Tipos de culinária', value=df2)

st.markdown('## Mapa dos restaurantes')
country_map(df1)