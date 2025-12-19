from routes.usuario import usuarios_bp
from routes.restaurante import restaurantes_bp
from routes.avaliacao import avaliacoes_bp

BLUEPRINTS = [
    usuarios_bp,
    restaurantes_bp,
    avaliacoes_bp
]