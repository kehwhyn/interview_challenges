from models.base import Base

from geoalchemy2 import Geometry
from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column


class BairroOficial(Base):
    __tablename__ = "bairro_oficial"
    __table_args__ = {"schema": "silver"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_bac: Mapped[int]
    codigo: Mapped[int]
    tipo: Mapped[str] = mapped_column(String(30))
    nome: Mapped[str] = mapped_column(String(50))
    area_km2: Mapped[float] = mapped_column(Numeric(10,3))
    perimetr_m: Mapped[float] = mapped_column(Numeric(10,3))
    geometria: Mapped[Geometry] = mapped_column(Geometry("MULTIPOLYGON", srid=31983))

    def __repr__(self) -> str:
        return f"<BairroOficial(nome='{self.nome}', codigo={self.codigo})>"
