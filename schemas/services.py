from pydantic import BaseModel, Field

class BuscaRestaurantesProximidadeRequest(BaseModel):
    """Schema para buscar restaurantes próximos"""
    latitude: float = Field(..., description="Latitude", example=-23.5505)
    longitude: float = Field(..., description="Longitude", example=-46.6333)
    raio_km: float = Field(default=5.0, description="Raio em km")
    tipo: str = Field(default="pizza", description="Tipo de estabelecimento")
