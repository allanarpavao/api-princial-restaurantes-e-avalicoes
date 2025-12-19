from pydantic import BaseModel
from typing import Optional, List

from datetime import datetime
from models.restaurante import Restaurante

class RestauranteSchema(BaseModel):
    """Define os campos de um novo restaurante a ser inserido
    """
    
    nome_restaurante: str = "Jappa da Quitanda"
    endereco_1: str = "Rua XXXX, numero - complemento"
    endereco_2: str = "Bairro, Cidade, Estado, CEP"
    culinaria: str = "mediterranea, indiana, japonesa"


class RestauranteViewSchema(BaseModel):
    """Define como o restaurante será retornado
    """

    restaurante_id: int
    nome_restaurante: str
    endereco_1: str
    endereco_2: str
    culinaria: str
    data_criacao: datetime

    class Config:
        from_attributes = True  # Converte ORM → Pydantic automaticamente


class RestauranteBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca.
        A busca será feita apenas com base id do restaurante.
    """
    id_restaurante: int = 1


class ListagemRestaurantesSchema(BaseModel):
    """ Define como uma listagem de restaurantes será retornada.
    """
    restaurantes: List[RestauranteSchema]


class RestauranteUpdateSchema(BaseModel):
    """Define os campos que podem ser editados de um restaurante cadastrado
    """

    nome_restaurante: Optional[str] = None
    endereco_1: Optional[str] = None
    endereco_2: Optional[str] = None
    culinaria: Optional[str] = None

class RestaurantePathSchema(BaseModel):
    restaurante_id: int = 1