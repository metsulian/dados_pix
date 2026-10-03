from src.utils.database import run_query
from src.utils.database import _get_engine
import streamlit as st
import pandas as pd
import plotly.express as px

from src.config import DB_CONNECTION

engine = _get_engine(DB_CONNECTION)

def exibir_total(x):
    if x >= 10**6 and x < 10**9:
        return(f'{round(x / 10**6, 2)} Milhões')
    elif x >= 10**9 and x < 10**12:
        return(f'{round(x / 10**9, 2)} Bilhões')
    elif x >= 10**12:
        return(f'{round(x / 10**12, 2)} Trilhões')

st.set_page_config(layout="wide")

st.title('📊 Estatísticas e Indicadores do Pix')


regioes = df['Regiao'].unique().tolist()
regioes.insert(0, 'TODAS')

datas = sorted(df['AnoMes'].dt.year.unique())
if len(datas) > 1: del datas[0]

with st.sidebar:
    st.header('Filtros Globais')
    regiao_select = st.selectbox('Regiões', regioes)
    
    if regiao_select == 'TODAS':
        df_estados_aux = df
    else: 
        df_estados_aux = df[df['Regiao'] == regiao_select]
    estados = sorted(df_estados_aux['Estado'].unique())
    
    estado_select = st.selectbox('Estado (Análise Regional)', estados)
    data_select = st.select_slider('Ano Limite', options=datas, value=2026)
    

df_filtrado = df_filtrado[df_filtrado['AnoMes'].dt.year <= data_select]
df_filtrado_estado = df_filtrado[df_filtrado['Estado'] == estado_select]



coluna_1, coluna_2 = st.columns(2)
with coluna_1:
    st.metric('Quantidade de Transações PF', exibir_total(df_filtrado['QT_PagadorPF'].sum()))
    st.metric('Valor Total Pago PF', exibir_total(df_filtrado['VL_PagadorPF'].sum()))
    
with coluna_2:
    st.metric('Quantidade de Transações PJ', exibir_total(df_filtrado['QT_PagadorPJ'].sum()))
    st.metric('Valor Total Pago PJ', exibir_total(df_filtrado['VL_PagadorPJ'].sum()))


aba_macro, aba_regional, aba_perfil = st.tabs([
    "📈 Visão Temporal", 
    "🗺️ Análise Regional", 
    "👥 Perfil PF vs PJ"
])


with aba_macro:
    df_agrupado = df_filtrado.groupby(['AnoMes', 'Estado'])['VL_PagadorTotal'].sum().reset_index()
    fig_linhas = px.line(
        df_agrupado, x='AnoMes', y='VL_PagadorTotal', color='Estado', 
        title='Evolução Mensal do Volume Total Pago por Estado (R$)',
        labels={'VL_PagadorTotal': 'Volume Pago (R$)', 'AnoMes': 'Período', 'Estado': 'Estado'},
    )

    df_estado_agrupado = df_filtrado.groupby('Estado').agg({'VL_PagadorTotal': 'sum', 'VL_RecebedorTotal': 'sum'}).reset_index()
    df_estado_melt = pd.melt(df_estado_agrupado, id_vars=['Estado'], value_vars=['VL_PagadorTotal', 'VL_RecebedorTotal'], var_name='Tipo de Transacao', value_name='Valor Total')
    df_estado_melt['Tipo de Transacao'] = df_estado_melt['Tipo de Transacao'].map({'VL_PagadorTotal': 'Total Pago', 'VL_RecebedorTotal': 'Total Recebido'})
    
    fig_balanco = px.bar(
        df_estado_melt, x='Estado', y='Valor Total', color='Tipo de Transacao', barmode='group', 
        title='Comparativo de Fluxo Comercial Regional: Total Pago vs. Total Recebido',
        labels={'Valor Total': 'Montante Comercial (R$)', 'Tipo de Transacao': 'Fluxo'},
    )

    df_agrupado_balanco = df_filtrado.groupby(['AnoMes', 'Estado'])[['Balanco']].sum().reset_index()
    fig_linhas_balanco = px.line(
        df_agrupado_balanco, x='AnoMes', y='Balanco', color='Estado', 
        title='Evolução do Saldo de Balanço Líquido Mensal por Estado (R$)',
        labels={'Balanco': 'Saldo Líquido (R$)', 'AnoMes': 'Período', 'Estado': 'Estado'},
    )

    df_estado_balanco = df_filtrado.groupby('Estado')['Balanco'].sum().reset_index()
    fig_estado_balanco = px.bar(
        df_estado_balanco, x='Estado', y='Balanco', 
        title='Resultado Acumulado do Balanço Comercial Líquido por Estado',
        labels={'Balanco': 'Saldo Comercial (R$)'},
    )

    st.plotly_chart(fig_linhas, use_container_width=True)
    st.plotly_chart(fig_linhas_balanco, use_container_width=True)
    st.plotly_chart(fig_balanco, use_container_width=True)
    st.plotly_chart(fig_estado_balanco, use_container_width=True)


with aba_regional:

    df_agrupado_medias = df_filtrado_estado.groupby(['AnoMes']).agg({'VL_MedioPF': 'sum', 'VL_MedioPJ': 'sum'}).reset_index()
    df_agrupado_medias_melt = pd.melt(df_agrupado_medias, id_vars=['AnoMes'], value_vars=['VL_MedioPF', 'VL_MedioPJ'], var_name='Media PF vs PJ', value_name='Medias')
    df_agrupado_medias_melt['Media PF vs PJ'] = df_agrupado_medias_melt['Media PF vs PJ'].map({'VL_MedioPF': 'Média PF', 'VL_MedioPJ': 'Média PJ'})

    fig_linhas_medias = px.line(
        df_agrupado_medias_melt, x='AnoMes', y='Medias', color='Media PF vs PJ', 
        title=f'Evolução de Tíquete Médio por Transação — {estado_select}',
        labels={'Medias': 'Valor Médio (R$)', 'Media PF vs PJ': 'Segmento', 'AnoMes': 'Período'},
    )

    vol_pf_estado = df_filtrado_estado['VL_PagadorPF'].sum()
    vol_pj_estado = df_filtrado_estado['VL_PagadorPJ'].sum()
    fig_share_vol_estado = px.pie(
        names=['Pessoa Física (PF)', 'Pessoa Juridica (PJ)'], values=[vol_pf_estado, vol_pj_estado], 
        title=f'Participação no Volume Financeiro Ocupado - {estado_select}',
    )

    qtd_pf_estado = df_filtrado_estado['QT_PagadorPF'].sum()
    qtd_pj_estado = df_filtrado_estado['QT_PagadorPJ'].sum()
    fig_qtd_estado = px.pie(
        names=['Pessoa Física (PF)', 'Pessoa Juridica (PJ)'], values=[qtd_pf_estado, qtd_pj_estado], 
        title=f'Participação no Volume de Transações (Quantidade) - {estado_select}',
    )

    top_municipios_pf = df_filtrado_estado.groupby('Municipio')['VL_PagadorPF'].sum().reset_index().sort_values(by='VL_PagadorPF', ascending=False).head(5)
    fig_top_municipios_pf = px.bar(
        top_municipios_pf, x='VL_PagadorPF', y='Municipio', 
        title=f'Top 5 Municípios por Movimentação PF - {estado_select}',
        labels={'VL_PagadorPF': 'Volume PF (R$)', 'Municipio': 'Cidade'},
    )

    top_municipios_pj = df_filtrado_estado.groupby('Municipio')['VL_PagadorPJ'].sum().reset_index().sort_values(by='VL_PagadorPJ', ascending=False).head(5)
    fig_top_municipios_pj = px.bar(
        top_municipios_pj, x='VL_PagadorPJ', y='Municipio', 
        title=f'Top 5 Municípios por Movimentação PJ - {estado_select}',
        labels={'VL_PagadorPJ': 'Volume PJ (R$)', 'Municipio': 'Cidade'},
    )

    top_municipios = df_filtrado_estado.groupby('Municipio')['VL_PagadorTotal'].sum().reset_index().sort_values(by='VL_PagadorTotal', ascending=False).head(5)
    fig_municipios = px.bar(
        top_municipios, x='Municipio', y='VL_PagadorTotal', 
        title=f'Top 5 Municípios Líderes em Volume Financeiro Total — {estado_select}',
        labels={'VL_PagadorTotal': 'Volume Total Pago (R$)', 'Municipio': 'Cidade'},
    )

    st.plotly_chart(fig_linhas_medias, use_container_width=True)
    st.plotly_chart(fig_municipios, use_container_width=True)

    col_reg_1, col_reg_2 = st.columns(2)   
    with col_reg_1:
        st.plotly_chart(fig_share_vol_estado, use_container_width=True)
        st.plotly_chart(fig_top_municipios_pf, use_container_width=True)
    with col_reg_2:
        st.plotly_chart(fig_qtd_estado, use_container_width=True)
        st.plotly_chart(fig_top_municipios_pj, use_container_width=True)


with aba_perfil:
    col_1, col_2 = st.columns(2)   

    vol_pf = df_filtrado['VL_PagadorPF'].sum()
    vol_pj = df_filtrado['VL_PagadorPJ'].sum()
    fig_share_vol = px.pie(
        names=['Pessoa Física (PF)', 'Pessoa Juridica (PJ)'], values=[vol_pf, vol_pj], 
        title='Share Macro: Distribuição Geral do Volume Financeiro (R$)',
        color_discrete_sequence=['#D9381E', '#F2A922']
    )

    qtd_pf = df_filtrado['QT_PagadorPF'].sum()
    qtd_pj = df_filtrado['QT_PagadorPJ'].sum()
    fig_qtd = px.pie(
        names=['Pessoa Física (PF)', 'Pessoa Juridica (PJ)'], values=[qtd_pf, qtd_pj], 
        title='Share Macro: Distribuição Geral da Quantidade de Transações',
        color_discrete_sequence=['#D9381E', '#F2A922']
    )

    qtd_pes_pagador_pf = df_filtrado['QT_PES_PagadorPF'].sum()
    qtd_pes_pagador_pj = df_filtrado['QT_PES_PagadorPJ'].sum()
    fig_qtd_pes_pag = px.pie(
        names=['Pessoa Física (PF)', 'Pessoa Juridica (PJ)'], values=[qtd_pes_pagador_pf, qtd_pes_pagador_pj], 
        title='Distribuição Demográfica de Clientes Pagadores Únicos',
        color_discrete_sequence=['#6B1D2F', '#FFCD38']
    )

    qtd_pes_recebedor_pf = df_filtrado['QT_PES_RecebedorPF'].sum()
    qtd_pes_recebedor_pj = df_filtrado['QT_PES_RecebedorPJ'].sum()
    fig_qtd_pes_receb = px.pie(
        names=['Pessoa Física (PF)', 'Pessoa Juridica (PJ)'], values=[qtd_pes_recebedor_pf, qtd_pes_recebedor_pj], 
        title='Distribuição Demográfica de Clientes Recebedores Únicos',
        color_discrete_sequence=['#6B1D2F', '#FFCD38']
    )

    with col_1:
        st.plotly_chart(fig_share_vol, use_container_width=True)
        st.plotly_chart(fig_qtd_pes_pag, use_container_width=True)

    with col_2:
        st.plotly_chart(fig_qtd, use_container_width=True)
        st.plotly_chart(fig_qtd_pes_receb, use_container_width=True)