from pydantic import BaseModel, Field
from typing import Optional, List

from datetime import datetime
from models.restaurante import Restaurante

class RestauranteSchema(BaseModel):
    """Define os campos de um novo restaurante (manual ou Overpass)
    """
    nome: str = Field(..., min_length=1, max_length=200, example="Jappa da Quitanda")
    endereco: str = Field(..., min_length=1, max_length=200, example="Rua XXXX, 123 - Bairro")
    cuisine: str = Field(..., min_length=1, max_length=100, example="japonesa")
    
    latitude: Optional[float] = Field(None, description="Coordenada latitude")
    longitude: Optional[float] = Field(None, description="Coordenada longitude")
    telefone: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=300)
    id_osm: Optional[str] = Field(None, max_length=50, description="ID do Overpass")


class RestauranteViewSchema(BaseModel):
    """Define como o restaurante será retornado
    """

    restaurante_id: int
    nome: str
    endereco: str
    cuisine: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    telefone: Optional[str] = None
    website: Optional[str] = None
    id_osm: Optional[str] = None
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

    nome: Optional[str] = None
    endereco: Optional[str] = None
    cuisine: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    telefone: Optional[str] = None
    website: Optional[str] = None
    id_osm: Optional[str] = None

class RestaurantePathSchema(BaseModel):
    restaurante_id: int = 1