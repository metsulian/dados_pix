import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

def apply_theme():
    pio.templates["pix"] = go.layout.Template(
    layout=dict(
            font=dict(family="Chakra Petch, sans-serif", color="#EDEDED", size=13),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            colorway=["#00C2A8", "#5B8DEF", "#F5A524", "#E5484D"],
            xaxis=dict(showgrid=False, linecolor="#262626"),
            yaxis=dict(gridcolor="#1A1A1A", zeroline=False),
            margin=dict(l=70, r=20, t=60, b=90),
            title=dict(font=dict(size=16), x=0),
        )
    )
    pio.templates.default = "pix"

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

    fig.update_traces(hole=0.6, textinfo="percent", textfont=dict(size=16, color="#F5EDE6"))
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
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

    fig.update_traces(
    textposition="outside",
    textfont=dict(color="#F5EDE6", size=12),
    marker_line_width=0,
    cliponaxis=False,
)
    fig.update_layout(
        bargap=0.3,
        yaxis_title=None,
        xaxis_title=None,
        xaxis=dict(showticklabels=True, showgrid=False),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    st.plotly_chart(fig, theme=None, use_container_width=True)

def make_series(data: list, title: str):
    df = pd.DataFrame(data)

    fig = px.line(
        df,
        x=df.columns[1],
        y=df.columns[0],
        title=title
    )

    fig.update_layout(title_x=0.5, title_xanchor="center")
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    st.plotly_chart(fig)