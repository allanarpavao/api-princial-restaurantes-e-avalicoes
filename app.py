from flask import redirect
from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from http import HTTPStatus
from urllib.parse import unquote
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Session
from models.usuario import Usuario
from schemas.usuario import UsuarioSchema


info = Info(title="StackUp", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# tags
home_tag = Tag(name="Documentação", description="Documentação: Swagger")
usuario_tag = Tag(name="Usuários", description="Operações de usuário")



@app.route('/')
def index():
    return redirect('/openapi')

@app.post('/usuarios/criar', tags=[usuario_tag])
          #responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})

def criar_usuario(form: UsuarioSchema):
    """Adiciona um novo usuário à base de dados

    Retorna uma representação dos usuários.
    """
    try:
        usuario = Usuario(
            nome_usuario = form.nome_usuario,
            email = form.email,
            senha = form.senha
        )

        
        Session.add(usuario)
        Session.commit()

        return HTTPStatus.CREATED
    
    finally:
        Session.close()

#apresenta_usuario(usuario),


if __name__ == '__main__':
    app.run(debug=True, port=5000)

# @app.post('/usuarios/criar', tags=[usuario_tag],
#           responses={"201": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})

# def cadastrar_usuario(form: CadastroUsuarioSchema):
#     """Adiciona um novo usuário à base de dados

#     Retorna uma representação dos usuários.
#     """
#     usuario = Usuario(
#         email = form.email,
#         nome_usuario = form.nome_usuario,
#         senha = form.senha
#     )
#     try:
#         session = Session()
#         session.add(usuario)
#         session.commit()
#         return {
#             "status": "success",
#             "message": "Usuário cadastrado com sucesso!",
#             "usuario": apresenta_usuario(usuario)
#         }, HTTPStatus.CREATED
    
#     except IntegrityError:
#         return {
#             "status": "error",
#             "message": "Já existe um usuário com esse nome."
#         }, HTTPStatus.CONFLICT
    
#     except Exception as e:
#         return {
#             "status": "error",
#             "message": f"Erro inesperado: {str(e)}"
#         }, HTTPStatus.BAD_REQUEST



# @app.get('/usuarios/listar', tags=[usuario_tag],
#          responses={"200": ListagemUsuariosSchema})
# def listar_usuarios():
#     """ Retorna uma lista de todos os usuários cadastrados
#     """
#     session = Session()
#     usuarios = session.query(Usuario).all()

#     if not usuarios:
#         return {
#             "status": "success",
#             "mensagem": "Nenhum usuário encontrado.",
#             "usuarios": [],
#             "quantidade": 0
#         }, HTTPStatus.OK

#     return {
#         "status": "success",
#         "mensagem": f"{len(usuarios)} usuário(s) encontrado(s).",
#         "usuarios": apresenta_usuarios(usuarios)["usuarios"],
#         "quantidade": len(usuarios)
#     }, HTTPStatus.OK

# @app.get('/usuarios/<nome_usuario>', tags=[usuario_tag],
#          responses={"200": ListagemUsuariosSchema, "404": ErrorSchema})
# def buscar_usuario(query:UsuarioBuscaSchema):
#     """Busca e retorna os dados detalhados de um usuário a partir do nome de usuário informado
#     """
#     nome_usuario = query.nome

#     session = Session()
#     usuario = session.query(Usuario).filter(Usuario.nome_usuario == nome_usuario).first()

#     if not usuario:
#         return {
#             "status": "error",
#             "mensagem": f"Usuário '{nome_usuario}' não foi localizado no sistema."
#         }, HTTPStatus.NOT_FOUND
#     else:
#         return {
#             "status": "sucess",
#             "dados": {
#             "nome_usuario": usuario.nome_usuario,
#             "email": usuario.email,
#             "data_insercao": usuario.data_insercao
#         }
#     }, HTTPStatus.OK

# @app.delete('/usuarios', tags=[usuario_tag],
#             responses={"200": ListagemUsuariosSchema, "404": ErrorSchema})
# def deletar_usuario(query:UsuarioBuscaSchema):
#     """Remove um usuário do sistema com base no nome de usuário fornecido.
#     Retorna uma resposta indicando o sucesso ou a falha da operação.
#     """
#     usuario_nome = unquote(unquote(query.nome))
#     session = Session()
#     count = session.query(Usuario).filter(Usuario.nome_usuario == usuario_nome).delete()
#     session.commit()
#     if count:
#         return {
#             "status": "sucess",
#             "mensagem": f"Usuário '{usuario_nome}' removido com sucesso."
#         }, HTTPStatus.OK
#     else:
#         return {
#             "status": "error",
#             "mensagem": f"Usuário '{usuario_nome}' não encontrado na base."
#         }, HTTPStatus.NOT_FOUND