import streamlit as st
import pandas as pd
import plotly.express as px

def carregar_dados():
    hapvida = pd.read_csv('RECLAMEAQUI_HAPVIDA.csv')
    hapvida['EMPRESA'] = 'HAPVIDA'

    ibyte = pd.read_csv('RECLAMEAQUI_IBYTE.csv')
    ibyte['EMPRESA'] = 'IBYTE'

    nagem = pd.read_csv('RECLAMEAQUI_NAGEM.csv')
    nagem['EMPRESA'] = 'NAGEM'

    datasets = [hapvida, ibyte, nagem]
    reclame_aqui = pd.concat(datasets)

    reclame_aqui['DATA_RECLAMACAO'] = pd.to_datetime(reclame_aqui['ANO'].astype(str) + '-' + 
                                                     reclame_aqui['MES'].astype(str) + '-' + 
                                                     reclame_aqui['DIA'].astype(str))
    return reclame_aqui

def criar_dashboard(dados):
    st.title('Reclame Aqui')
    st.markdown('Dashboard com informações sobre reclamações de empresas no site Reclame Aqui')

    empresa = st.sidebar.selectbox('Selecione a empresa', ['Todas'] + list(dados['EMPRESA'].unique()))
    estado = st.sidebar.selectbox('Selecione o estado', ['Todos'] + list(dados['LOCAL'].unique()))
    status = st.sidebar.selectbox('Selecione o status', ['Todos'] + list(dados['STATUS'].unique()))

    dados_filtrados = dados.copy()
    if empresa != 'Todas':
        dados_filtrados = dados_filtrados[dados_filtrados['EMPRESA'] == empresa]
    if estado != 'Todos':
        dados_filtrados = dados_filtrados[dados_filtrados['LOCAL'] == estado]
    if status != 'Todos':
        dados_filtrados = dados_filtrados[dados_filtrados['STATUS'] == status]

    st.subheader('Série temporal do número de reclamações')
    fig1 = px.line(dados_filtrados, x='DATA_RECLAMACAO', y='CASOS', color='EMPRESA')
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader('Frequência de reclamações por estado')
    fig2 = px.bar(dados_filtrados, x='LOCAL', y='CASOS', color='EMPRESA')
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader('Frequência de cada tipo de STATUS')
    fig3 = px.bar(dados_filtrados, x='STATUS', y='CASOS', color='EMPRESA')
    st.plotly_chart(fig3, use_container_width=True)

def main():
    dados = carregar_dados()
    criar_dashboard(dados)

if __name__ == "__main__":
    main()
