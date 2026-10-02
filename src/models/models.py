from sqlalchemy import ForeignKey
from datetime import date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class DadosAPI(Base):
    __tablename__ = "DadosAPI"
 
    id: Mapped[int] = mapped_column(primary_key=True) 
    AnoMes: Mapped[date]
    Municipio_Ibge: Mapped[int | None]
    Municipio: Mapped[str]
    Estado_Ibge: Mapped[str | None]
    Estado: Mapped[str]
    Sigla_Regiao: Mapped[str | None]
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
    VL_PagadorTotal: Mapped[float | None]
    QT_PagadorTotal: Mapped[int | None]
    VL_RecebedorTotal: Mapped[float | None]
    QT_RecebedorTotal: Mapped[int | None]
    VL_PagadorMedioPF: Mapped[float | None]
    VL_PagadorMedioPJ: Mapped[float | None] 
    VL_RecebedorMedioPF: Mapped[float | None]
    VL_RecebedorMedioPJ: Mapped[float | None]
    VL_Pagador_TotalMedio: Mapped[float | None]
    VL_Recebedor_TotalMedio: Mapped[float | None]
    Balanco: Mapped[float | None]
    Pct_PJ_Pagador: Mapped[float | None]
    Pct_PJ_Recebedor: Mapped[float | None]
    Rel_Exportacao: Mapped[float | None] 
    VL_Pagador_Pessoa: Mapped[float | None]
    VL_Recebedor_Pessoa: Mapped[float | None]
    Transacoes_Pessoa: Mapped[float | None]
