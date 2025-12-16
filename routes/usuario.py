from flask_openapi3 import APIBlueprint, Tag
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError

from models import Session
from models.usuario import Usuario
from schemas.error import ErrorSchema
from schemas.usuario import UsuarioSchema, UsuarioViewSchema, apresenta_usuario

usuarios_bp = APIBlueprint(
    'usuarios',
    __name__,
    url_prefix='/usuarios',
    abp_tags=[Tag(name='Usuários', description='Operações de usuário')]
)

@usuarios_bp.post('/criar', responses={"201": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
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

        return apresenta_usuario(usuario), HTTPStatus.CREATED
    
    except IntegrityError:
        Session.rollback()

        return {"erro": "Email já existe"}, HTTPStatus.CONFLICT
    
    except Exception as e:
        Session.rollback()
        return {"erro": str(e)}, HTTPStatus.BAD_REQUEST

    finally:
        Session.close()

# @usuarios_bp.get('/usuarios/listar', tags=[usuario_tag],
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