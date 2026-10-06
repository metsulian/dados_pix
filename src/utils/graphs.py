import pandas as pd
import streamlit as st
import plotly.express as px

def make_pie(pieces: list, values: list, title: str):
    df_pie = pd.DataFrame({
        "Tipo": pieces,
        "Percentual": values
    })

    fig = px.pie(
        df_pie,
        names="Tipo",
        values="Percentual",
        title=title,
    )

    fig.update_traces(textinfo="percent+label")
    st.plotly_chart(fig)

def make_top_bar(data: list, title: str, y_label: str):
    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x=df.columns[1],
        y=df.columns[2],
        title=title,
        text_auto=True,
        labels={f"{df.columns[2]}": f"{y_label}"}
    )

    fig.update_layout(title_x=0.5, title_xanchor="center")
    st.plotly_chart(fig)

def make_series(data: list, title: str):
    df = pd.DataFrame(data)

    fig = px.line(
        df,
        x=df.columns[1],
        y=df.columns[0],
        title=title
    )

    fig.update_layout(title_x=0.5, title_xanchor="center")
    st.plotly_chart(fig)