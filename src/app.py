from src.queries.queries import get_top_pj,get_top_pf, get_top_bal, get_top_pag, get_municipios, get_estados, get_silver, get_gold_estados_series, get_gold_municipios_series, get_gold_municipios, get_gold_estados, get_ano_mes
from src.utils.graphs import make_pie, make_top_bar, make_series
from src.utils.database import _get_engine
from src.utils.preprocessing import show_values
import streamlit as st

from src.config import DB_CONNECTION

engine = _get_engine(DB_CONNECTION)

st.set_page_config(layout="wide")
st.title('📊 Estatísticas e Indicadores do Pix por Município')

estados = [r["Estado"] for r in get_estados(engine)]
estados.insert(0, "TODOS")
estado = st.selectbox("Selecione um Estado:", estados)

if estado == "TODOS":
        municipios = ["TODOS"]
else:
    municipios = [r["Municipio"] for r in get_municipios(engine, estado)]
    municipios.insert(0, "TODOS")
municipio = st.selectbox("Selecione um Município:", municipios)

meses = [r["AnoMes"] for r in get_ano_mes(engine)]
meses.reverse()

aba = st.radio(
    "Seção",
    ["📈 Visão Geral", "🗺️ Análise Estadual", "🏙️ Análise Municipal"],
    horizontal=True,
    key="aba_ativa",
    label_visibility="collapsed",
)

if aba == "📈 Visão Geral":    
    silver_data = get_silver(engine, estado=estado, municipio=municipio)[0]
    top_pag = get_top_pag(engine, estado)
    top_bal = get_top_bal(engine, estado)
    top_pf = get_top_pf(engine, estado)
    top_pj = get_top_pj(engine, estado)

    col1, col2 = st.columns(2)

    vl_total = silver_data["vl_pag_total"]
    qt_pagamentos = silver_data["qt_pag_total"]
    total_pf = silver_data["vl_pag_pf"]
    balanco = silver_data["balanco"]
    qt_pf_ativos = silver_data["qtd_pf_ativo"]
    rec_total = silver_data["vl_rec_total"]
    qt_rec = silver_data["qt_rec_total"]
    total_pj = silver_data["vl_pag_pj"]
    vl_pag_medio = silver_data["val_medio_pag"]
    qt_pj_ativos = silver_data["qtd_pj_ativo"]

    pct_pag_pf = silver_data["pct_pag_pf"]
    pct_pag_pj = silver_data["pct_pag_pj"]
    pct_rec_pf = silver_data["pct_rec_pf"]
    pct_rec_pj = silver_data["pct_rec_pj"]
    with col1:
        if vl_total:
            st.metric("Total pago:", show_values(vl_total))
        else: 
            st.metric("Total pago:", "Não Obtido")

        if qt_pagamentos:
            st.metric("Quantidade de Pagamentos:", show_values(qt_pagamentos))
        else:
            st.metric("Quantidade de Pagamentos:", "Não Obtida")

        if total_pf:
            st.metric("Total Pago por PF:", show_values(total_pf))
        else:
            st.metric("Total Pago por PF:", "Não Obtido")

        if balanco:
            st.metric("Balanço:", show_values(balanco))
        else:
            st.metric("Balanço:", "Não Obtido")
        
        if qt_pf_ativos:
            st.metric("Quantidade de PF Ativas:", show_values(qt_pf_ativos))
        else:
            st.metric("Quantidade de PF Ativas:", "Não Obtida")

        if pct_pag_pj and pct_pag_pf:
            make_pie(
                ["Pessoa Física (PF)", "Pessoa Jurídica (PJ)"], 
                [pct_pag_pf, pct_pag_pj], 
                f"Distribuição de Pagamentos (PF vs PJ) - {estado}"
            )
        
        make_top_bar(top_pag, title=f"Top 10 Municípios - Valor Pago Total - {estado}", y_label="Valor Pago")
        make_top_bar(top_pf, title=f"Top 10 Municípios - Valor Pago por PF - {estado}", y_label="Valor Pago")
    with col2:
        if rec_total:
            st.metric("Total recebido:", show_values(rec_total))
        else:
            st.metric("Total recebido:", "Não Obtido")

        if qt_rec:
            st.metric("Quantidade de Recebimentos:", show_values(qt_rec))
        else:
            st.metric("Quantidade de Recebimentos:", "Não Obtida")

        if total_pj:
            st.metric("Total Pago por PJ:", show_values(total_pj))
        else:
            st.metric("Total Pago por PJ:", "Não Obtido")

        if vl_pag_medio:
            st.metric("Valor Médio de Pagamento:", show_values(vl_pag_medio))
        else:
            st.metric("Valor Médio de Pagamento:", "Não Obtido")
        
        if qt_pj_ativos:
            st.metric("Quantidade de PJ Ativas:", show_values(qt_pj_ativos))
        else:
            st.metric("Quantidade de PJ Ativas:", "Não Obtida")

        if pct_rec_pf and pct_rec_pj:
            make_pie(
                ["Pessoa Física (PF)", "Pessoa Jurídica (PJ)"], 
                [pct_rec_pf, pct_rec_pj], 
                f"Distribuição de Recebimentos (PF vs PJ) - {estado}"
            )

        make_top_bar(top_bal, title=f"Top 10 Municípios por Balanço - {estado}", y_label="Balanço")
        make_top_bar(top_pj,  title=f"Top 10 Municípios por Valor Pago por PJ - {estado}", y_label="Valor Pago")

elif aba == "🗺️ Análise Estadual":
    ano_mes_estado = st.selectbox(
        "Selecione um mês:", 
        meses, 
        key="mes_estado",
        format_func=lambda d: d.strftime("%Y-%m")
    )
    if estado == 'TODOS':
        st.warning("Selecione um estado!")
    else:
        if not get_gold_estados(engine, estado, ano_mes_estado):
            st.warning(f"Dados Não Obtidos para {estado} - {ano_mes_estado}")
        else:
            gold_estado_data = get_gold_estados(engine, estado, ano_mes_estado)[0]
            gold_estado_series = get_gold_estados_series(engine, estado)
            col3, col4 = st.columns(2)

            vl_total_estado = gold_estado_data["VL_Pagador_Total_Estado"]
            balanco_estado = gold_estado_data["Balanco_Estado"]
            var_mes_estado = gold_estado_data["Var_MA_Estado"]
            pct_pj_estado = gold_estado_data["Pct_PJ_Pagador_Estado"]
            share_nacional_estado = gold_estado_data["Share_Nacional_Estado"]
            var_ano_anterior_estado = gold_estado_data["Var_AMA_Estado"]
            with col3:
                if vl_total_estado:
                    st.metric("Valor Total Pago", show_values(vl_total_estado))
                else:
                    st.metric("Valor Total Pago", "Não Obtido")
                
                if balanco_estado:
                    st.metric(f"Balanço Estadual em {ano_mes_estado}", show_values(balanco_estado))
                else:
                    st.metric(f"Balanço Estadual em {ano_mes_estado}", "Não Obtido")

                if var_mes_estado:
                    st.metric("Variação do Balanço em Relação ao Último Mês", f"{(var_mes_estado*100):.2f}%")
                else:
                    st.metric("Variação do Balanço em Relação ao Último Mês", "Não Obtida")

                make_series([
                    {"Valor_Pagador_Total": r["VL_Pagador_Total_Estado"],
                    "Data": r["AnoMes"]
                    } for r in gold_estado_series], f"Série Histórica Total Pago - {estado}")
                make_series([
                    {"Balanco": r["Balanco_Estado"],
                    "Data": r["AnoMes"]
                    } for r in gold_estado_series], f"Série Histórica Balanço - {estado}")
            with col4:
                if pct_pj_estado:
                    st.metric("Porcentagem do Valor Pago PJ", f"{(pct_pj_estado*100):.2f}%")
                else:
                    st.metric("Porcentagem do Valor Pago PJ", "Não Obtida")

                if share_nacional_estado:
                    st.metric(f"Share Nacional em {ano_mes_estado}", f"{(share_nacional_estado*100):.2f}%")
                else:
                    st.metric(f"Share Nacional em {ano_mes_estado}", "Não Obtido")

                if var_ano_anterior_estado:
                    st.metric("Variação do Balanço em Relação ao Mesmo Mês do Ano Anterior", f"{(var_ano_anterior_estado*100):.2f}%")
                else:
                    st.metric("Variação do Balanço em Relação ao Mesmo Mês do Ano Anterior", "Não Obtida")

                make_series([
                    {"Share Nacional": r["Share_Nacional_Estado"],
                    "Data": r["AnoMes"]
                    } for r in gold_estado_series], f"Série Histórica Share Nacional - {estado}")
                make_series([
                    {"% PJ": r["Pct_PJ_Pagador_Estado"],
                    "Data": r["AnoMes"]
                    } for r in gold_estado_series], f"Série Histórica Participação PJ - {estado}")

elif aba == "🏙️ Análise Municipal":
    ano_mes_municipio = st.selectbox(
        "Selecione um mês:", 
        meses, 
        key="mes_municipio",
        format_func=lambda d: d.strftime("%Y-%m")
    )
    if estado == 'TODOS':
        st.warning("Selecione um estado!")
    if municipio == "TODOS":
        st.warning("Selecione um município!")
    else:
        gold_municipio_data = get_gold_municipios(engine, estado, municipio, ano_mes_municipio)
        gold_municipio_series = get_gold_municipios_series(engine, estado, municipio)
        if not gold_municipio_data:
            st.warning("Sem dados para este município neste mês.")
        else:
            gold_municipio_data = gold_municipio_data[0]
            col5, col6 = st.columns(2)

            vl_total_municipio = gold_municipio_data["VL_Pagador_Total_Municipio"]
            balanco_municipio = gold_municipio_data["Balanco_Municipio"]
            var_mes_anterior_municipio = gold_municipio_data["Var_MA_Municipio"]
            pct_pj = gold_municipio_data["Pct_PJ_Pagador_Municipio"]
            share_nacional_municipio = gold_municipio_data["Share_Nacional_Municipio"]
            share_estadual_municipio = gold_municipio_data["Share_Estadual_Municipio"]
            with col5:
                if vl_total_municipio:
                    st.metric("Valor Total Pago", show_values(vl_total_municipio))
                else:
                    st.metric("Valor Total Pago", "Não Obtido")

                if balanco_municipio:
                    st.metric(f"Balanço Municipal em {ano_mes_municipio}", show_values(balanco_municipio))
                else:
                    st.metric(f"Balanço Municipal em {ano_mes_municipio}", "Não Obtido")

                if var_mes_anterior_municipio:
                    st.metric("Variação do Balanço em Relação ao Último Mês", f"{(var_mes_anterior_municipio):.2f}%")
                else:
                    st.metric("Variação do Balanço em Relação ao Último Mês", "Não Obtida")
                
                make_series([
                    {"Valor_Pagador_Total": r["VL_Pagador_Total_Municipio"],
                    "Data": r["AnoMes"]
                    } for r in gold_municipio_series], f"Série Histórica Total Pago - {municipio}")
                make_series([
                    {"Balanco": r["Balanco_Municipio"],
                    "Data": r["AnoMes"]
                    } for r in gold_municipio_series], f"Série Histórica Balanço - {municipio}")
                make_series([
                    {"Share Estadual": r["Pct_PJ_Pagador_Municipio"],
                    "Data": r["AnoMes"]
                    } for r in gold_municipio_series], f"Série Histórica Participação PJ - {municipio}")

            with col6:
                if pct_pj:
                    st.metric("Porcentagem do Valor Pago PJ", f"{(pct_pj*100):.2f}%")
                else: 
                    st.metric("Porcentagem do Valor Pago PJ", "Não Obtida")

                if share_nacional_municipio:
                    st.metric(f"Share Nacional em {ano_mes_municipio}", f"{(share_nacional_municipio*100):.2f}%")
                else:
                    st.metric(f"Share Nacional em {ano_mes_municipio}", "Não Obtido")

                if share_estadual_municipio:
                    st.metric(f"Share Estadual em {ano_mes_municipio}", f"{(share_estadual_municipio*100):.2f}%")
                else:
                    st.metric(f"Share Estadual em {ano_mes_municipio}", "Não Obtido")

                make_series([
                    {"Share Nacional": r["Share_Nacional_Municipio"],
                    "Data": r["AnoMes"]
                    } for r in gold_municipio_series], f"Série Histórica Share Nacional - {municipio}")
                make_series([
                    {"Share Estadual": r["Share_Estadual_Municipio"],
                    "Data": r["AnoMes"]
                    } for r in gold_municipio_series], f"Série Histórica Share Estadual - {municipio}")