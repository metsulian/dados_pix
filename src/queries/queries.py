from src.utils.database import run_query

def get_estados(engine):
    query = """
        SELECT DISTINCT "Estado"
        FROM "DadosEstadoGold"
        ORDER BY "Estado"
    """
    return run_query(engine, query)

def get_municipios(engine, estado:str):
    query = """
        SELECT DISTINCT "Municipio"
        FROM "DadosMunicipioGold"
        WHERE (:estado = 'TODOS' OR "Estado" = :estado)
        ORDER BY "Municipio"
    """
    return run_query(engine, query, params={
        "estado": estado
    })

def get_silver(engine, estado:str, municipio:str):
    query = """
        SELECT
            SUM(s."VL_PagadorTotal") AS vl_pag_total,
            SUM(s."VL_RecebedorTotal") AS vl_rec_total,
            SUM(s."QT_PagadorTotal") AS qt_pag_total,
            SUM(s."QT_RecebedorTotal") AS qt_rec_total,
            SUM(b."VL_PagadorPF") AS vl_pag_pf,
            SUM(b."VL_PagadorPJ") AS vl_pag_pj,
            SUM(b."VL_PagadorPF") / NULLIF(SUM(s."VL_PagadorTotal"), 0) AS pct_pag_pf,
            SUM(b."VL_PagadorPJ") / NULLIF(SUM(s."VL_PagadorTotal"), 0) AS pct_pag_pj,
            SUM(b."VL_RecebedorPF") / NULLIF(SUM(s."VL_RecebedorTotal"), 0) AS pct_rec_pf,
            SUM(b."VL_RecebedorPJ") / NULLIF(SUM(s."VL_RecebedorTotal"), 0) AS pct_rec_pj,
            SUM(s."Balanco") AS balanco,
            SUM(s."VL_PagadorTotal") / SUM(s."QT_PagadorTotal") AS val_medio_pag,
            SUM(b."QT_PES_PagadorPF") AS qtd_pf_ativo,
            SUM(b."QT_PES_PagadorPJ") AS qtd_pj_ativo
        FROM "DadosSilver" s
        JOIN "DadosAPI" b ON s.id = b.id
        WHERE (:estado = 'TODOS' OR b."Estado" = :estado)
        AND (:municipio = 'TODOS' OR b."Municipio" = :municipio)
    """

    return run_query(engine, query, {
        "estado": estado,
        "municipio": municipio
    })

def get_top_pag(engine, estado:str):
    query = """
        SELECT 
            b."Estado", 
            b."Municipio",
            SUM(s."VL_PagadorTotal") AS vl_pag_total
        FROM "DadosSilver" s
        JOIN "DadosAPI" b ON s.id = b.id
        WHERE (:estado = 'TODOS' OR b."Estado" = :estado)
        GROUP BY b."Estado", b."Municipio"
        ORDER BY vl_pag_total DESC
        LIMIT 10;
    """

    return run_query(engine, query, {
        "estado": estado
    })

def get_top_bal(engine, estado:str):
    query = """
        SELECT 
            b."Estado", 
            b."Municipio",
            SUM(s."Balanco") AS bal
        FROM "DadosSilver" s
        JOIN "DadosAPI" b ON s.id = b.id
        WHERE (:estado = 'TODOS' OR b."Estado" = :estado)
        GROUP BY b."Estado", b."Municipio"
        ORDER BY bal DESC
        LIMIT 10;
    """

    return run_query(engine, query, {
        "estado": estado
    })

def get_top_pf(engine, estado:str):
    query = """
        SELECT
            b."Estado",
            b."Municipio",
            SUM(b."VL_PagadorPF") AS val
        FROM "DadosAPI" b
        WHERE (:estado = 'TODOS' OR b."Estado" = :estado)
        GROUP BY b."Estado", b."Municipio"
        ORDER BY val DESC
        LIMIT 10;
    """

    return run_query(engine, query, {
        "estado": estado
    })

def get_top_pj(engine, estado:str):
    query = """
        SELECT
            b."Estado",
            b."Municipio",
            SUM(b."VL_PagadorPJ") AS val
        FROM "DadosAPI" b
        WHERE (:estado = 'TODOS' OR b."Estado" = :estado)
        GROUP BY b."Estado", b."Municipio"
        ORDER BY val DESC
        LIMIT 10;
    """

    return run_query(engine, query, {
        "estado": estado
    })

def get_ano_mes(engine):
    query = """
        SELECT DISTINCT "AnoMes"
        FROM "DadosEstadoGold"
        ORDER BY "AnoMes" ASC;
    """

    return run_query(engine, query)

def get_gold_estados(engine, estado:str, ano_mes):
    query = """
        SELECT
            "AnoMes",
            "Balanco_Estado",
            "Share_Nacional_Estado",
            "Var_MA_Estado",
            "Var_AMA_Estado",
            "Rel_Exportacao_Estado",
            "VL_Pagador_Total_Estado",
            "Pct_PJ_Pagador_Estado"
        FROM "DadosEstadoGold"
        WHERE ("Estado" = :estado)
        AND ("AnoMes" = :ano_mes);
    """

    return run_query(engine, query, {
        "estado": estado,
        "ano_mes": ano_mes
    })

def get_gold_estados_series(engine, estado:str):
    query = """
        SELECT
            "AnoMes",
            "VL_Pagador_Total_Estado",
            "Balanco_Estado",
            "Share_Nacional_Estado",
            "Pct_PJ_Pagador_Estado"
        FROM "DadosEstadoGold"
        WHERE "Estado" = :estado;
    """

    return run_query(engine, query, {
        "estado": estado
    })

def get_gold_municipios(engine, estado:str, municipio:str, ano_mes):
    query = """
        SELECT
            "AnoMes",
            "Estado",
            "Municipio",
            "VL_Pagador_Total_Municipio",
            "Balanco_Municipio",
            "Pct_PJ_Pagador_Municipio",
            "VL_Pagador_Pessoa_Municipio",
            "Transacoes_Pessoa_Municipio",
            "Share_Nacional_Municipio",
            "Share_Estadual_Municipio",
            "Var_MA_Municipio",
            "Var_AMA_Municipio"
        FROM "DadosMunicipioGold"
        WHERE "Estado" = :estado
          AND "AnoMes" = :ano_mes
          AND "Municipio" = :municipio
    """

    return run_query(engine, query, {
        "estado": estado,
        "ano_mes": ano_mes,
        "municipio": municipio
    })

def get_gold_municipios_series(engine, estado: str, municipio: str):
    query = """
        SELECT
            "AnoMes",
            "Estado",
            "Municipio",
            "VL_Pagador_Total_Municipio",
            "Balanco_Municipio",
            "Share_Nacional_Municipio",
            "Share_Estadual_Municipio",
            "Pct_PJ_Pagador_Municipio"
        FROM "DadosMunicipioGold"
        WHERE "Estado" = :estado
          AND "Municipio" = :municipio
        ORDER BY "AnoMes"
    """
    
    return run_query(engine, query, params={
        "estado": estado,
        "municipio": municipio,
    })
