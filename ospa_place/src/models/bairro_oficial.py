from models.base import Base

from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, Float


class BairroOficial(Base):
    __tablename__ = "bairro_oficial"
    __table_args__ = {"schema": "silver"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_bac = Column(Integer)
    codigo = Column(Integer)
    tipo = Column(String(30))
    nome = Column(String(50))
    area_km2 = Column(Float)
    perimetr_m = Column(Float)
    geometria = Column(Geometry("MULTIPOLYGON", srid=31983))

    def __repr__(self):
        return f"<BairroOficial(nome='{self.nome}', codigo={self.codigo})>"
