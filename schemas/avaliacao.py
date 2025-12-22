from pydantic import BaseModel
from typing import Optional, List

from datetime import datetime

from uuid import UUID
from models.avaliacao import Avaliacao

class AvaliacaoSchema(BaseModel):
    """Define os campos de uma nova avaliacao
    """

    usuario_id: str = "7a743fa4-57b5-4b0b-b97a-5da34a58bf62"
    restaurante_id: int = 5
    nota: int = 4
    comentario: str = "Adorei!"


class AvaliacaoViewSchema(BaseModel):
    """Define como a avalicao será retornada
    """

    usuario_id: str
    restaurante_id: int
    nota: int
    comentario: str
    data_avaliacao: datetime
    

    class Config:
        from_attributes = True

class AvaliacaoPathSchema(BaseModel):
    id_restaurante: int
    id_usuario: UUID