from models import Session
from models.usuario import Usuario
from models.restaurante import Restaurante
from uuid import UUID

def validar_usuario_restaurante(usuario_id: UUID, restaurante_id: int):
    """Valida existência de usuário e restaurante.
    """
    usuario = Session.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
    
    if not usuario:
        return {
                "valid": False,
                "error": {
                "status": "error",
                "mensagem": f"Usuario não localizado no sistema."}
            }
    
    restaurante = Session.query(Restaurante).filter(Restaurante.restaurante_id == restaurante_id).first()
    
    if not restaurante:
        return {
                "valid": False,
                "error": {
                "status": "error",
                "mensagem": f"Restaurante não localizado no sistema."}
        }
    return {
        "valid": True,
        "usuario": usuario,
        "restaurante": restaurante
    }