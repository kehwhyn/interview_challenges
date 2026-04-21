from models.base import Base

from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String


class PontoOnibus(Base):
    __tablename__ = "ponto_onibus"
    __table_args__ = {"schema": "silver"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_ponto_onibus_linha = Column(Integer)
    cod_linha = Column(String(6))
    nome_linha = Column(String(50))
    nome_sub_linha = Column(String(50))
    origem = Column(String(30))
    identificador_ponto_onibus = Column(Integer)
    geometria = Column(Geometry("POINT", srid=31983))

    def __repr__(self):
        return f"<PontoOnibus(id='{self.id}')>"