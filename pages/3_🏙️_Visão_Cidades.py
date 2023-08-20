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

def restaurant_by_city( df1 ):
    '''
        Função que:
            1. Retorna o número de restaurantes cadastrado por cidade
            2. Plota um gráfico de barras     
        Input: Dataframe
        Output: Gráfico de barras
    '''
    df2 = (df1.loc[:, ['city', 'restaurant_id', 'country_name']].groupby(['city', 'country_name'])
                                                                .count()
                                                                .sort_values('restaurant_id', ascending=False)
                                                                .reset_index()
                                                                .head(10))
    fig = go.Figure()
    for country, group in df2.groupby('country_name'):    
        fig.add_trace( go.Bar ( x=group['city'], y=group['restaurant_id'], name=country, text=group['restaurant_id'],
                                hovertemplate='País: %s<br>Cidade: %%{x}<br>Quantidade de restaurantes: %%{y}<extra></extra>'% country) )
    fig.update_layout(legend_title_text='País',
                    title={'text':'Top 10 - cidades com mais restaurantes cadastrados', 'x':0.5, 'xanchor': 'center'})
    fig.update_xaxes(title_text='Cidade', categoryorder='total descending')
    fig.update_yaxes(title_text='Quantidade de restaurantes')
    
    return fig

def high_aggregate_rating_by_city( df1 ):
    '''
        Função que:
            1. Retorna o número de restaurantes acima de 4.0 de avaliação média por cidade
            2. Plota um gráfico de barras     
        Input: Dataframe
        Output: Gráfico de barras    
    '''
    linhas_select = df1['aggregate_rating'] > 4
    df2 = (df1.loc[linhas_select, ['city', 'restaurant_id', 'country_name']].groupby(['city', 'country_name'])
                                                                            .count()
                                                                            .sort_values('restaurant_id', ascending=False)
                                                                            .reset_index()
                                                                            .head(10))

    fig = go.Figure()
    for country, group in df2.groupby('country_name'):
        fig.add_trace( go.Bar ( x=group['city'], y=group['restaurant_id'], name=country, text=group['restaurant_id'],
                                hovertemplate='País: %s<br>Cidade: %%{x}<br>Quantidade de restaurantes: %%{y}<extra></extra>'% country) )
    fig.update_layout(legend_title_text='País',
                    title={'text':'Top 10 - cidades com avaliação média maior que 4', 'x':0.5, 'xanchor': 'center'})
    fig.update_xaxes(title_text='Cidade', categoryorder='total descending')
    fig.update_yaxes(title_text='Quantidade de restaurantes')
    
    return fig

def low_aggregate_rating_by_city( df1 ):
    '''
        Função que:
            1. Retorna o número de restaurantes abaixo de 2.5 de avaliação média por cidade
            2. Plota um gráfico de barras     
        Input: Dataframe
        Output: Gráfico de barras      
    '''
    linhas_select = df1['aggregate_rating'] < 2.5
    df2 = (df1.loc[linhas_select, ['city', 'restaurant_id', 'country_name']].groupby(['city', 'country_name'])
                                                                            .count()
                                                                            .sort_values('restaurant_id', ascending=False)
                                                                            .reset_index()
                                                                            .head(10))

    fig = go.Figure()
    for country, group in df2.groupby('country_name'):    
        fig.add_trace( go.Bar ( x=group['city'], y=group['restaurant_id'], name=country, text=group['restaurant_id'],
                                hovertemplate='País: %s<br>Cidade: %%{x}<br>Quantidade de restaurantes: %%{y}<extra></extra>'% country) )
    fig.update_layout(legend_title_text='País',
                    title={'text':'Top 10 - cidades com avaliação média menor que 2.5', 'x':0.5, 'xanchor': 'center'})
    fig.update_xaxes(title_text='Cidade', categoryorder='total descending')
    fig.update_yaxes(title_text='Quantidade de restaurantes')
    
    return fig

def cuisines_by_city( df1 ):
    '''
        Função que:
            1. Retorna os tipos de culinárias cadastrados por cidade
            2. Plota um gráfico de barras     
        Input: Dataframe
        Output: Gráfico de barras    
    '''
    df2 = (df1.loc[:, ['city', 'cuisines', 'country_name']].groupby(['city', 'country_name'])
                                                        .nunique()
                                                        .sort_values('cuisines', ascending=False)
                                                        .reset_index()
                                                        .head(10))

    fig = go.Figure()
    for country, group in df2.groupby('country_name'):    
        fig.add_trace( go.Bar ( x=group['city'], y=group['cuisines'], name=country, text=group['cuisines'],
                                hovertemplate='País: %s<br>Cidade: %%{x}<br>Tipos de culinária: %%{y}<extra></extra>'% country) )
    fig.update_layout(legend_title_text='País', 
                    title={'text':'Top 10 - quantidade de tipos de culinária por cidade', 'x':0.5, 'xanchor': 'center'})
    fig.update_xaxes(title_text='Cidade', categoryorder='total descending')
    fig.update_yaxes(title_text='Tipos de culinária')
    
    return fig

def average_cost_by_city( df1 ):
    '''
        Função que:
            1. Retorna o custo médio para 2 por cidade
            2. Plota um gráfico de barras     
        Input: Dataframe
        Output: Gráfico de barras    
    '''
    df2 = (df1.loc[:, ['city', 'average_cost_for_two_USD', 'country_name']].groupby(['city', 'country_name'])
                                                                        .max()
                                                                        .sort_values('average_cost_for_two_USD', ascending=False)
                                                                        .reset_index()
                                                                        .head(10))
    df2['average_cost_for_two_USD'] = df2['average_cost_for_two_USD'].astype(float).round(2)

    fig = go.Figure()
    for country, group in df2.groupby('country_name'):    
        fig.add_trace( go.Bar ( x=group['city'], y=group['average_cost_for_two_USD'], name=country, text=group['average_cost_for_two_USD'],
                                hovertemplate='País: %s<br>Cidade: %%{x}<br>Preço médio para dois (USD): %%{y}<extra></extra>'% country) )
    fig.update_layout(legend_title_text='País', 
                    title={'text':'Top 10 - Preço médio de um prato para dois em Dólares Americanos (USD) por cidade', 'x':0.5, 'xanchor': 'center'})
    fig.update_xaxes(title_text='Cidade', categoryorder='total descending')
    fig.update_yaxes(title_text='Preço médio para dois (USD)')
    
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
st.set_page_config(page_title='Visão Cidades', page_icon='🏙️', layout='wide')

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
st.markdown('# 🏙️ Visão Cidades')

# Gráfico barras top 10 qtd restaurantes por cidade
fig = restaurant_by_city( df1 )
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    # Gráfico barras top 10 cidades > 4 aggregate_rating
    fig = high_aggregate_rating_by_city( df1 )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Gráfico barras top 10 cidades < 2.5 aggregate_rating
    fig = low_aggregate_rating_by_city( df1 )
    st.plotly_chart(fig, use_container_width=True)

# Gráfico barras top 10 custo médio para 2 por cidade
fig = average_cost_by_city( df1 )
st.plotly_chart(fig, use_container_width=True)

# gráfico barras top 10 mais tipos de cuisines por cidade
fig = cuisines_by_city( df1 )
st.plotly_chart(fig, use_container_width=True)