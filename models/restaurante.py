from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, DateTime, Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import uuid

from models import Base
from models.avaliacao import Avaliacao

class Restaurante(Base):
    __tablename__ = "restaurantes"

    # criacao do restaurante id
    restaurante_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    
    # campos
    nome_restaurante: Mapped[str] = mapped_column(String(200), nullable=False)
    endereco_1: Mapped[str] = mapped_column(String(50), nullable=False)
    endereco_2: Mapped[str] = mapped_column(String(50))
    culinaria: Mapped[str] = mapped_column(String(30), nullable=False)
    data_criacao: Mapped[Optional[datetime]] = mapped_column(DateTime(), default=datetime.now())

    # relacionamento
    avaliacoes: Mapped[list['Avaliacao']] = relationship("Avaliacao", back_populates="restaurante", cascade='all, delete-orphan')

    def __init__(self, nome_restaurante:str, endereco_1:str, endereco_2:str, culinaria:str, data_criacao:Optional[DateTime] = None):
        self.nome_restaurante = nome_restaurante
        self.endereco_1 = endereco_1
        self.endereco_2 = endereco_2
        self.culinaria = culinaria

        if data_criacao:
            self.data_criacao = data_criacao

    def __repr__(self) -> str:
        return f"Restaurante(id={self.restaurante_id}, nome={self.nome_restaurante})"