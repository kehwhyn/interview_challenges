from models.base import Base

from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, Boolean, Float


class AtividadeEconomica(Base):
    __tablename__ = "atividade_economica"
    __table_args__ = {"schema": "silver"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_ativ_econ_estabelecimento = Column(Integer)
    cnae_principal = Column(String(7))
    descricao_cnae_principal = Column(String(200))
    cnae = Column(String(2000))
    data_inicio_atividade = Column(String(10))
    natureza_juridica = Column(String(100))
    porte_empresa = Column(String(24))
    area_utilizada = Column(Float)
    ind_simples = Column(Boolean)
    ind_mei = Column(Boolean)
    ind_possui_alvara = Column(Boolean)
    tipo_unidade = Column(String(100))
    forma_atuacao = Column(String(2000))
    desc_logradouro = Column(String(20))
    nome_logradouro = Column(String(50))
    numero_imovel = Column(Integer)
    complemento = Column(String(50))
    nome_bairro = Column(String(50))
    nome = Column(String(200))
    nome_fantasia = Column(String(200))
    cnpj = Column(String(14))
    geometria = Column(Geometry("POINT", srid=31983))

    def __repr__(self):
        return f"<AtividadeEconomica(cnpj='{self.cnpj}', cnae_principal='{self.cnae_principal}')>"
