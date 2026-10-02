from sqlalchemy import create_engine, insert, text
from sqlalchemy.engine import Engine

from src.models.models import Base, DadosAPI
from src.utils.preprocessing import prepare_data

# Cria engine
def _get_engine(connection_string: str) -> Engine:
    return create_engine(connection_string)

# Upa os dados da API no banco de dados
def upload_sql(engine: Engine, data):
    Base.metadata.create_all(engine)

    data = prepare_data(data)
    with engine.begin() as conn:
        conn.execute(insert(DadosAPI), data)

    print(f"{len(data)} registro(s) salvo(s)")

# Limpa o banco de dados
def clean_database(engine: Engine):
    with engine.begin() as conn:
        conn.execute(text('DROP TABLE IF EXISTS "DadosSilver" CASCADE'))
        conn.execute(text('DROP TABLE IF EXISTS "DadosAPI" CASCADE'))
    Base.metadata.create_all(engine)

# Executa query no database
def run_query(
    engine: Engine,
    query:str,
):
    with engine.begin() as conn:
        resultado = conn.execute(text(query))
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

    result = run_query(engine, silver_query)
    return result
