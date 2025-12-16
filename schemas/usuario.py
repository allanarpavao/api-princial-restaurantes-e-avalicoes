from pydantic import BaseModel
from typing import Optional, List

from datetime import datetime
from models.usuario import Usuario

class UsuarioSchema(BaseModel):
    """Define os campos de um novo usuário a ser inserido
    """
    email: str = "exemplo@gmail.com"
    nome_usuario: str = "exemplo_usuario"
    senha: str = "senha123"