from sqlalchemy import create_engine, insert, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.engine import Engine

class Base(DeclarativeBase):
    pass

class LevantamentoMensal(Base):
    __tablename__ = "DadosPix"
 
    id: Mapped[int] = mapped_column(primary_key=True)  # gerado automaticamente
    AnoMes: Mapped[int]
    Municipio_Ibge: Mapped[int]
    Municipio: Mapped[str]
    Estado_Ibge: Mapped[str]
    Estado: Mapped[str]
    Sigla_Regiao: Mapped[str]
    Regiao: Mapped[str]
    VL_PagadorPF: Mapped[float]
    QT_PagadorPF: Mapped[int]
    VL_PagadorPJ: Mapped[float]
    QT_PagadorPJ: Mapped[int]
    VL_RecebedorPF: Mapped[float]
    QT_RecebedorPF: Mapped[int]
    VL_RecebedorPJ: Mapped[float]
    QT_RecebedorPJ: Mapped[int]
    QT_PES_PagadorPF: Mapped[int]
    QT_PES_PagadorPJ: Mapped[int]
    QT_PES_RecebedorPF: Mapped[int]
    QT_PES_RecebedorPJ: Mapped[int]

def _get_engine(connection_string: str) -> Engine:
    return create_engine(connection_string)

def upload_sql(engine, data):
    Base.metadata.create_all(engine)

    with engine.begin() as conn:
        conn.execute(insert(LevantamentoMensal), data)

    print(f"{len(data)} registro(s) salvo(s) com sucesso!")

def run_query(
    engine: Engine,
    query:str,
):
    with engine.begin() as conn:
        resultado = conn.execute(text(query))
        if resultado.returns_rows:
            return [dict(linha) for linha in resultado.mappings()]
        return resultado.rowcount

