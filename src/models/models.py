from sqlalchemy import ForeignKey
from datetime import date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class DadosAPI(Base):
    __tablename__ = "DadosAPI"
 
    id: Mapped[int] = mapped_column(primary_key=True) 
    AnoMes: Mapped[date]
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


class DadosSilver(Base):
    __tablename__ = "DadosSilver"

    id: Mapped[int] = mapped_column(ForeignKey("DadosAPI.id"), primary_key=True)
    VL_PagadorTotal: Mapped[float]
    QT_PagadorTotal: Mapped[int]
    VL_RecebedorTotal: Mapped[float]
    QT_RecebedorTotal: Mapped[int]
    VL_PagadorMedioPF: Mapped[float]
    VL_PagadorMedioPJ: Mapped[float]
    VL_RecebedorMedioPF: Mapped[float]
    VL_RecebedorMedioPJ: Mapped[float]
    VL_Pagador_TotalMedio: Mapped[float]
    VL_Recebedor_TotalMedio: Mapped[float]
    Balanco: Mapped[float]
    Pct_PJ_Pagador: Mapped[float]
    Pct_PJ_Recebedor: Mapped[float]
    Rel_Exportacao: Mapped[float]
    VL_Pagador_Pessoa: Mapped[float]
    VL_Recebedor_Pessoa: Mapped[float]
    Transacoes_Pessoa: Mapped[float]
