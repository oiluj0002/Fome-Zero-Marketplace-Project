#========================================================
# IMPORT LIBRARIES
#========================================================
import pandas as pd
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
    # CLEAN CODE
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

def metric_restaurant( df1 , cuisines ):
    '''
        Função que:
            1. Retorna o número de restaurantes cadastrado por cidade
            2. Plota um gráfico de barras     
        Inputs:
            Dataframe
            cuisines = tipo de culinária desejado ('str')
        Output: Streamlit Metric
    '''
    linhas_select = df1['cuisines'] == cuisines
    df2 = (df1.loc[linhas_select, ['restaurant_id','restaurant_name', 'aggregate_rating', 'country_name', 'city', 'average_cost_for_two_USD', 'cuisines']]
          .sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True])
          .reset_index()
          .head(1))
    if len(df2['aggregate_rating']) == 0:
        st.metric(label = 'N/A', value = 'N/A')
    else:
        st.metric(label = f"{df2['cuisines'].iloc[0]}: {df2['restaurant_name'].iloc[0]}",
                value = f"{df2['aggregate_rating'].iloc[0]}/5.0",
                help = f"País: {df2['country_name'].iloc[0]}.\n\nCidade: {df2['city'].iloc[0]}.\n\n Preço médio para dois: ${df2['average_cost_for_two_USD'].astype(float).round(2).iloc[0]} dólares."
        )       

def restaurant_dataframe( df1 ):
    '''
        Função que:
            1. Retorna um dataframe com os mais bem avaliados restaurantes cadastrados    
        Input: Dataframe
        Output: Dataframe
    '''
    df2 = (df1.loc[:, ['restaurant_id', 'restaurant_name', 'country_name', 'city', 'cuisines', 'average_cost_for_two_USD', 'aggregate_rating', 'votes']].groupby('restaurant_id')
                                                                                                                                              .max()
                                                                                                                                              .sort_values(['aggregate_rating','restaurant_id'], ascending=[False, True])
                                                                                                                                              .reset_index()
                                                                                                                                              .head(qtd_restaurant))
    df2['average_cost_for_two_USD'] = df2['average_cost_for_two_USD'].astype(float).round(2)
    
    return df2

def best_cuisines( df1 ):
    '''
        Função que:
            1. Retorna os melhores tipos de culinária cadastrados
            2. Plota um gráfico de barras     
        Input: Dataframe
        Output: Gráfico de barras
    '''
    df2 = (df1.loc[:, ['cuisines', 'aggregate_rating']].groupby('cuisines')
                                                   .mean()
                                                   .sort_values(['aggregate_rating'], ascending=[False])
                                                   .reset_index()
                                                   .head(qtd_restaurant))
    df2['aggregate_rating'] = df2['aggregate_rating'].astype(float).round(2)

    fig = go.Figure()
    fig.add_trace( go.Bar ( x=df2['cuisines'], y=df2['aggregate_rating'], text=df2['aggregate_rating'],
                            hovertemplate='Tipo de culinária: %{x}<br>Avaliação média: %{y}<extra></extra>' ) )
    fig.update_layout(title={'text':f'Top {qtd_restaurant} - melhores tipos de culinária', 'x':0.5,'xanchor': 'center'})
    fig.update_xaxes(title_text='Tipos de culinária',)
    fig.update_yaxes(title_text='Avaliação média')
    
    return fig

def worst_cuisines( df1 ):
    '''
        Função que:
            1. Retorna os piores tipos de culinária cadastrados
            2. Plota um gráfico de barras     
        Input: Dataframe
        Output: Gráfico de barras
    '''
    df2 = (df1.loc[:, ['cuisines', 'aggregate_rating']].groupby('cuisines')
                                                   .mean()
                                                   .sort_values(['aggregate_rating'], ascending=[True])
                                                   .reset_index()
                                                   .head(qtd_restaurant))
    df2['aggregate_rating'] = df2['aggregate_rating'].astype(float).round(2)

    fig = go.Figure()
    fig.add_trace( go.Bar ( x=df2['cuisines'], y=df2['aggregate_rating'], text=df2['aggregate_rating'],
                            hovertemplate='Tipo de culinária: %{x}<br>Avaliação média: %{y}<extra></extra>' ) )
    fig.update_layout(title={'text':f'Top {qtd_restaurant} - piores tipos de culinária', 'x':0.5, 'xanchor': 'center'})
    fig.update_xaxes(title_text='Tipos de culinária',)
    fig.update_yaxes(title_text='Avaliação média')
    
    return fig
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
st.set_page_config(page_title='Visão Restaurantes', page_icon='🍽️', layout='wide')

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

    #qtd restaurantes
    restaurant_slider = st.slider(
        'Selecione a quantidade de restaurantes:',
        value=10,
        min_value=1,
        max_value=20
    )

    #selecionar países
    country_options = st.multiselect(
        'Selecione quais países deseja visualizar os dados:',
        ['Philippines', 'Brazil', 'Australia', 'United States of America',
        'Canada', 'Singapore', 'United Arab Emirates', 'India',
        'Indonesia', 'New Zealand', 'England', 'Qatar', 'South Africa',
         'Sri Lanka', 'Turkey'],
        default = []
    )

    #selecionar tipo de preço
    price_options = st.multiselect('Selecione a faixa de preço do restaurante:', 
                                   ['gourmet', 'expensive', 'normal', 'cheap'], 
                                   default = [])

    #selecionar reserva restaurantes
    table_booking_options = st.multiselect('Selecione se o restaurante faz reservas:', 
                                           ['Sim', 'Não'],
                                           default=['Sim', 'Não'])
    
    #selecionar entrega restaurantes
    delivery_options = st.multiselect('Selecione se o restaurante realiza entregas:', 
                                      ['Sim', 'Não'],
                                      default=['Sim', 'Não'])
    
    #selecionar online restaurantes
    online_options = st.multiselect('Selecione se o restaurante possui pedidos online:', 
                                    ['Sim', 'Não'],
                                    default=['Sim', 'Não'])

    st.markdown('''---''')

    st.header('Powered by Oiluj')

#filtro restaurantes
qtd_restaurant = restaurant_slider

#filtro países
if not country_options:
    df1 = df1
else:
    linhas_select = df1['country_name'].isin(country_options)
    df1 = df1.loc[linhas_select, :]

#filtro price_type
if not price_options:
    df1 = df1
else:
    linhas_select = df1['price_type'].isin(price_options)
    df1=df1.loc[linhas_select, :]

#filtro has_table_booking
if not table_booking_options:
    df1 = df1
else:
    if 'Sim' in table_booking_options and 'Não' in table_booking_options:
        df1 = df1
    else:
        valores_filtrados = [0 if 'Sim' in table_booking_options else 1]
        linhas_select = df1['has_table_booking'].isin(valores_filtrados)
        df1 = df1.loc[linhas_select, :]

#filtro has_table_booking
if not delivery_options:
    df1 = df1
else:
    if 'Sim' in delivery_options and 'Não' in delivery_options:
        df1 = df1
    else:
        valores_filtrados = [1 if 'Sim' in delivery_options else 0]
        linhas_select = df1['is_delivering_now'].isin(valores_filtrados)
        df1 = df1.loc[linhas_select, :]

#filtro has_table_booking
if not online_options:
    df1 = df1
else:
    if 'Sim' in online_options and 'Não' in online_options:
        df1 = df1
    else:
        valores_filtrados = [1 if 'Sim' in online_options else 0]
        linhas_select = df1['has_online_delivery'].isin(valores_filtrados)
        df1 = df1.loc[linhas_select, :]

#========================================================
# PAGE LAYOUT
#========================================================
st.markdown('# 🍽️ Visão Restaurantes')

st.markdown('## Melhores restaurantes pelos seguintes tipos culinários')
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    metric_restaurant(df1, 'Italian')     
with col2:
    metric_restaurant(df1, 'American') 
with col3:
    metric_restaurant(df1, 'Arabian') 
with col4:
    metric_restaurant(df1, 'Japanese') 
with col5:
    metric_restaurant(df1, 'Home-made') 

st.markdown(f'## Top {qtd_restaurant} melhores restaurantes')
#dataframe melhores restaurantes
df2 = restaurant_dataframe( df1 )
st.dataframe(df2)

col1, col2 = st.columns(2)
with col1:
    # top qtd_restaurant melhores culinárias
    fig = best_cuisines( df1 )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # top qtd_restaurant piores culinárias
    fig = worst_cuisines( df1 )
    st.plotly_chart(fig, use_container_width=True)