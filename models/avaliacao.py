from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, DateTime, Integer, Text
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import uuid

from models import Base
# from models.avaliacao import Avaliacao

class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    ## primary key dupla
    usuario_id: Mapped[str] = mapped_column(String(36), ForeignKey('usuarios.usuario_id'), primary_key=True, nullable=False)
    restaurante_id: Mapped[int] = mapped_column(Integer, ForeignKey('restaurantes.restaurante_id'), primary_key=True, nullable=False)

    # campos
    nota: Mapped[int] = mapped_column(Integer, nullable=False)
    comentario: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    data_avaliacao: Mapped[Optional[datetime]] = mapped_column(DateTime(), default=datetime.now())

    # relacionamento
    usuario: Mapped['Usuario'] = relationship("Usuario", back_populates="avaliacoes", foreign_keys=[usuario_id])
    restaurante: Mapped['Restaurante'] = relationship("Restaurante", back_populates="avaliacoes", foreign_keys=[restaurante_id])

    def __init__(self, nota:int, comentario:str, data_avaliacao:Optional[DateTime] = None):
        self.nota = nota
        self.comentario = comentario

        if data_avaliacao:
            self.data_avaliacao = data_avaliacao