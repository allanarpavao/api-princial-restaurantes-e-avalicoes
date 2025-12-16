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

class Usuario(Base):
    __tablename__ = "usuarios"

    # criacao do usuario
    usuario_id: Mapped[str] = mapped_column(String(36), primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()))
    
    # campos
    nome_usuario: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(20), nullable=False)
    data_criacao: Mapped[Optional[datetime]] = mapped_column(DateTime(), default=datetime.now())

    # relacionamento
    avaliacoes: Mapped[list['Avaliacao']] = relationship("Avaliacao", back_populates="usuario", cascade='all, delete-orphan')

    def __init__(self, nome_usuario:str, email:str, senha:str, data_criacao:Optional[DateTime] = None):
        self.usuario_id = str(uuid.uuid4())
        self.nome_usuario = nome_usuario
        self.email = email
        self.senha = senha

        if data_criacao:
            self.data_criacao = data_criacao

    def __repr__(self) -> str:
        return f"Usuario(id={self.usuario_id}, nome={self.nome_usuario})"