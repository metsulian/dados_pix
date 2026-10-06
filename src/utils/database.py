from sqlalchemy import TextClause
from sqlalchemy import create_engine, insert, text
from sqlalchemy.engine import Engine

from src.models.models import Base, DadosAPI
from src.utils.preprocessing import prepare_data

import logging

logger = logging.getLogger(__name__)

# Cria engine
def _get_engine(connection_string: str) -> Engine:
    return create_engine(connection_string)

# Upa os dados da API no banco de dados
def upload_sql(engine: Engine, data):
    Base.metadata.create_all(engine)
    logger.info("Iniciando o Upload para o Banco de Dados")

    data = prepare_data(data)
    with engine.begin() as conn:
        conn.execute(insert(DadosAPI), data)

    logger.info(f"{len(data)} registro(s) salvo(s)")

# Limpa o banco de dados
def clean_database(engine: Engine):
    logger.info("Iniciando Limpeza do Banco de Dados")
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(text(f'DROP TABLE IF EXISTS "{table.name}" CASCADE'))
    Base.metadata.create_all(engine)
    logger.info("Banco de Dados Limpo")

# Executa query no database
def run_query(
    engine: Engine,
    query:str | TextClause,
    params: dict | None = None
):
    with engine.begin() as conn:
        resultado = conn.execute(text(query), params or {})
        if resultado.returns_rows:
            return [dict(linha) for linha in resultado.mappings()]
        return resultado.rowcount


# Inicializa as tabelas silver e gold
def setup_tables(
    engine: Engine
):

    silver_query = """
        INSERT INTO "DadosSilver" (
            "id",
            "VL_PagadorTotal",
            "QT_PagadorTotal",
            "VL_RecebedorTotal",
            "QT_RecebedorTotal",
            "VL_PagadorMedioPF",
            "VL_PagadorMedioPJ",
            "VL_RecebedorMedioPF",
            "VL_RecebedorMedioPJ",
            "VL_Pagador_TotalMedio",
            "VL_Recebedor_TotalMedio",
            "Balanco",
            "Pct_PJ_Pagador",
            "Pct_PJ_Recebedor",
            "Rel_Exportacao",
            "VL_Pagador_Pessoa",
            "VL_Recebedor_Pessoa",
            "Transacoes_Pessoa"

        )
        SELECT
            "id",
            "VL_PagadorPF" + "VL_PagadorPJ",
            "QT_PagadorPF" + "QT_PagadorPJ",
            "VL_RecebedorPF" + "VL_RecebedorPJ",
            "QT_RecebedorPF" + "QT_RecebedorPJ",
            "VL_PagadorPF" / NULLIF("QT_PagadorPF", 0),
            "VL_PagadorPJ" / NULLIF("QT_PagadorPJ", 0),
            "VL_RecebedorPF" / NULLIF("QT_RecebedorPF", 0),
            "VL_RecebedorPJ" / NULLIF("QT_RecebedorPJ", 0),
            ("VL_PagadorPF" / NULLIF("QT_PagadorPF", 0)) + ("VL_PagadorPJ" / NULLIF("QT_PagadorPJ", 0)),
            ("VL_RecebedorPF" / NULLIF("QT_RecebedorPF", 0)) + ("VL_RecebedorPJ" / NULLIF("QT_RecebedorPJ", 0)),
            ("VL_RecebedorPF" + "VL_RecebedorPJ") - ("VL_PagadorPF" + "VL_PagadorPJ"),
            "VL_PagadorPJ" / NULLIF(("VL_PagadorPF" + "VL_PagadorPJ"), 0),
            "VL_RecebedorPJ" / NULLIF(("VL_RecebedorPF" + "VL_RecebedorPJ"), 0),
            ("VL_RecebedorPF" + "VL_RecebedorPJ") / NULLIF(("VL_PagadorPF" + "VL_PagadorPJ"), 0),
            ("VL_PagadorPF" + "VL_PagadorPJ") / NULLIF(("QT_PES_PagadorPF" + "QT_PES_PagadorPJ"), 0),
            ("VL_RecebedorPF" + "VL_RecebedorPJ") / NULLIF(("QT_PES_RecebedorPF" + "QT_PES_RecebedorPJ"), 0),
            ("QT_PagadorPF" + "QT_PagadorPJ") / NULLIF(("QT_PES_PagadorPF" + "QT_PES_PagadorPJ"), 0)
        FROM "DadosAPI";
    """

    query_gold_estados = """
        INSERT INTO "DadosEstadoGold" (
        "AnoMes",
        "Estado",
        "VL_Pagador_Total_Estado",
        "QT_Pagador_Total_Estado",
        "VL_Recebedor_Total_Estado",
        "QT_RecebedorTotal_Estado",
        "VL_PagadorMedioPF_Estado",
        "VL_PagadorMedioPJ_Estado",
        "VL_RecebedorMedioPF_Estado",
        "VL_RecebedorMedioPJ_Estado",
        "VL_Pagador_TotalMedio_Estado",
        "VL_Recebedor_TotalMedio_Estado",
        "Balanco_Estado",
        "Pct_PJ_Pagador_Estado",
        "Pct_PJ_Recebedor_Estado",
        "Rel_Exportacao_Estado",
        "VL_Pagador_Pessoa_Estado",
        "VL_Recebedor_Pessoa_Estado",
        "Transacoes_Pessoa_Estado",
        "Share_Nacional_Estado",
        "Var_MA_Estado",
        "Var_AMA_Estado"
        )
        WITH agg as (
            SELECT
                b."AnoMes",
                b."Estado",
                SUM(s."VL_PagadorTotal") AS vl_pag,
                SUM(s."QT_PagadorTotal") AS qt_pag,
                SUM(s."VL_RecebedorTotal") AS vl_rec,
                SUM(s."QT_RecebedorTotal") AS qt_rec,
                SUM(s."Balanco") AS balanco,
                SUM(b."VL_PagadorPF") AS vl_pag_pf,
                SUM(b."QT_PagadorPF") AS qt_pag_pf,
                SUM(b."VL_PagadorPJ") AS vl_pag_pj,
                SUM(b."QT_PagadorPJ") AS qt_pag_pj,
                SUM(b."VL_RecebedorPF") AS vl_rec_pf,
                SUM(b."QT_RecebedorPF") AS qt_rec_pf,
                SUM(b."VL_RecebedorPJ") AS vl_rec_pj,
                SUM(b."QT_RecebedorPJ") AS qt_rec_pj,
                SUM(b."QT_PES_PagadorPF" + b."QT_PES_PagadorPJ") as pes_pag,
                SUM(b."QT_PES_RecebedorPF" + b."QT_PES_RecebedorPJ") as pes_rec
        FROM "DadosSilver" s
        JOIN "DadosAPI" b ON b.id = s.id
        GROUP BY b."AnoMes", b."Estado"
        )
        SELECT
            "AnoMes", 
            "Estado",
            vl_pag,
            qt_pag,
            vl_rec,
            qt_rec,
            vl_pag_pf / NULLIF(qt_pag_pf, 0),
            vl_pag_pj / NULLIF(qt_pag_pj, 0),
            vl_rec_pf / NULLIF(qt_rec_pf, 0),
            vl_rec_pj / NULLIF(qt_rec_pj, 0),
            vl_pag / NULLIF(qt_pag, 0),
            vl_rec / NULLIF(qt_rec, 0),
            balanco,
            vl_pag_pj / NULLIF(vl_pag, 0),
            vl_rec_pj / NULLIF(vl_rec, 0),
            vl_rec / NULLIF(vl_pag, 0),
            vl_pag / NULLIF(pes_pag, 0),
            vl_rec / NULLIF(pes_rec, 0),
            qt_pag::float / NULLIF(pes_pag, 0),
            vl_pag / NULLIF(SUM(vl_pag) OVER (PARTITION BY "AnoMes"), 0),
            (balanco - LAG(balanco, 1) OVER w) / NULLIF(ABS(LAG(balanco, 1) OVER w), 0),
            (balanco - LAG(balanco, 12) OVER w) / NULLIF(ABS(LAG(balanco, 12) OVER w), 0)
        FROM agg
        WINDOW w AS (PARTITION BY "Estado" ORDER BY "AnoMes");
    """

    query_gold_municipios = """
        INSERT INTO "DadosMunicipioGold" (
        "AnoMes",
        "Municipio",
        "Estado",
        "VL_Pagador_Total_Municipio",
        "QT_Pagador_Total_Municipio",
        "VL_Recebedor_Total_Municipio",
        "QT_RecebedorTotal_Municipio",
        "VL_PagadorMedioPF_Municipio",
        "VL_PagadorMedioPJ_Municipio",
        "VL_RecebedorMedioPF_Municipio",
        "VL_RecebedorMedioPJ_Municipio",
        "VL_Pagador_TotalMedio_Municipio",
        "VL_Recebedor_TotalMedio_Municipio",
        "Balanco_Municipio",
        "Pct_PJ_Pagador_Municipio",
        "Pct_PJ_Recebedor_Municipio",
        "Rel_Exportacao_Municipio",
        "VL_Pagador_Pessoa_Municipio",
        "VL_Recebedor_Pessoa_Municipio",
        "Transacoes_Pessoa_Municipio",
        "Share_Nacional_Municipio",
        "Share_Estadual_Municipio",
        "Var_MA_Municipio",
        "Var_AMA_Municipio"
        )
        WITH agg as (
            SELECT
                b."AnoMes",
                b."Municipio",
                b."Estado",
                SUM(s."VL_PagadorTotal") AS vl_pag,
                SUM(s."QT_PagadorTotal") AS qt_pag,
                SUM(s."VL_RecebedorTotal") AS vl_rec,
                SUM(s."QT_RecebedorTotal") AS qt_rec,
                SUM(s."Balanco") AS balanco,
                SUM(b."VL_PagadorPF") AS vl_pag_pf,
                SUM(b."QT_PagadorPF") AS qt_pag_pf,
                SUM(b."VL_PagadorPJ") AS vl_pag_pj,
                SUM(b."QT_PagadorPJ") AS qt_pag_pj,
                SUM(b."VL_RecebedorPF") AS vl_rec_pf,
                SUM(b."QT_RecebedorPF") AS qt_rec_pf,
                SUM(b."VL_RecebedorPJ") AS vl_rec_pj,
                SUM(b."QT_RecebedorPJ") AS qt_rec_pj,
                SUM(b."QT_PES_PagadorPF" + b."QT_PES_PagadorPJ") as pes_pag,
                SUM(b."QT_PES_RecebedorPF" + b."QT_PES_RecebedorPJ") as pes_rec
        FROM "DadosSilver" s
        JOIN "DadosAPI" b ON b.id = s.id
        GROUP BY b."AnoMes", b."Estado", b."Municipio"
        )
        SELECT
            "AnoMes", 
            "Municipio",
            "Estado",
            vl_pag,
            qt_pag,
            vl_rec,
            qt_rec,
            vl_pag_pf / NULLIF(qt_pag_pf, 0),
            vl_pag_pj / NULLIF(qt_pag_pj, 0),
            vl_rec_pf / NULLIF(qt_rec_pf, 0),
            vl_rec_pj / NULLIF(qt_rec_pj, 0),
            vl_pag / NULLIF(qt_pag, 0),
            vl_rec / NULLIF(qt_rec, 0),
            balanco,
            vl_pag_pj / NULLIF(vl_pag, 0),
            vl_rec_pj / NULLIF(vl_rec_pj, 0),
            vl_rec / NULLIF(vl_pag, 0),
            vl_pag / NULLIF(pes_pag, 0),
            vl_rec / NULLIF(pes_rec, 0),
            qt_pag::float / NULLIF(pes_pag, 0),
            vl_pag / NULLIF(SUM(vl_pag) OVER (PARTITION BY "AnoMes"), 0),
            vl_pag / NULLIF(SUM(vl_pag) OVER (PARTITION BY "AnoMes", "Estado"), 0),
            (balanco - LAG(balanco, 1) OVER w) / NULLIF(ABS(LAG(balanco, 1) OVER w), 0),
            (balanco - LAG(balanco, 12) OVER w) / NULLIF(ABS(LAG(balanco, 12) OVER w), 0)
        FROM agg
        WINDOW w AS (PARTITION BY "Estado", "Municipio" ORDER BY "AnoMes");
    """

    logger.info("Inicializando Tabelas...")
    result_silver = run_query(engine, silver_query)
    result_gold_estados = run_query(engine, query_gold_estados)
    result_gold_municipios = run_query(engine, query_gold_municipios)
    logger.info("Tabelas Inicializadas")

    return result_silver, result_gold_estados, result_gold_municipios