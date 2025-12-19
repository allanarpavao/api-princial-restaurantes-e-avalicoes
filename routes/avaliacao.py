from urllib.parse import unquote
import uuid
from flask_openapi3 import APIBlueprint, Tag
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError

from models import Session
from models.avaliacao import Avaliacao
from schemas.error import ErrorSchema
from schemas.avaliacao import AvaliacaoSchema, AvaliacaoViewSchema

avaliacoes_bp = APIBlueprint(
    'avaliacoes',
    __name__,
    url_prefix='/avaliacoes',
    abp_tags=[Tag(name='Avalicoes', description='Operações de avaliacoes')]
)

@avaliacoes_bp.post('/criar', responses={"201": AvaliacaoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def criar_avaliacao(form: AvaliacaoSchema):
    """Adiciona uma nova avaliacao a um restaurante

    Retorna uma representação da avaliacao
    """


    # validar usuario
    # validar restaurante
    try:
        avaliacao = Avaliacao(
            usuario_id = form.usuario_id,
            restaurante_id = form.restaurante_id,
            nota = form.nota,
            comentario = form.comentario
        )

        Session.add(avaliacao)
        Session.commit()

        return AvaliacaoViewSchema.model_validate(avaliacao).model_dump(), HTTPStatus.CREATED
    
    except IntegrityError as e:
        Session.rollback()

        return {"erro": str(e.orig)}, HTTPStatus.CONFLICT
    
    except Exception as e:
        Session.rollback()
        return {"erro": str(e)}, HTTPStatus.BAD_REQUEST

    finally:
        Session.remove()

# @avaliacoes_bp.get('/<int:restaurante_id>', responses={"200": ListagemRestaurantesSchema, "404": ErrorSchema})
# def buscar_restaurante(path:RestaurantePathSchema):
#     """Busca e retorna os dados detalhados de um restaurante a partir do id
#     """
   
#     try:
#         numero_restaurante = path.restaurante_id
#         restaurante = Session.query(Restaurante).filter(Restaurante.restaurante_id == numero_restaurante).first()

#         if not restaurante:
#             return {
#                 "status": "error",
#                 "mensagem": f"Restaurante não localizado no sistema."
#             }, HTTPStatus.NOT_FOUND
#         else:
#             return {
#                 "status": "sucess",
#                 "dados": RestauranteViewSchema.model_validate(restaurante).model_dump()
#             }, HTTPStatus.OK
    
#     except Exception as e:
#         return {"status": "error", "mensagem": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
    
#     finally:
#         Session.remove()


# @avaliacoes_bp.delete('/<int:restaurante_id>',
#             responses={"200": ListagemRestaurantesSchema, "404": ErrorSchema})
# def deletar_restaurante(path: RestaurantePathSchema):
#     """Remove um restaurante do sistema com base no id fornecido.
#     Retorna uma resposta indicando o sucesso ou a falha da operação.
#     """
    
#     numero_restaurante = path.restaurante_id
   
#     try:
#         restaurante = Session.query(Restaurante).filter(Restaurante.restaurante_id == numero_restaurante).first()
        
#         if restaurante:
#             Session.query(Restaurante).filter(Restaurante.restaurante_id == numero_restaurante).delete()
#             Session.commit()
            
#             return {
#                 "status": "sucess",
#                 "mensagem": f"Restaurante ({numero_restaurante}) '{restaurante.nome_restaurante}' removido com sucesso."
#             }, HTTPStatus.OK
#         else:
#             return {
#                 "status": "error",
#                 "mensagem": f"Restaurante não encontrado no sistema."
#             }, HTTPStatus.NOT_FOUND
    
#     except IntegrityError:
#         Session.rollback()
    
#         return {"status": "error", "mensagem": "Não é possível deletar"}, HTTPStatus.CONFLICT
    
#     except Exception as e:
#         Session.rollback()

#         return {"status": "error", "mensagem": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

#     finally:
#         Session.remove()

# @avaliacoes_bp.patch('/<int:restaurante_id>', responses={"200": RestauranteViewSchema, "404": ErrorSchema, "400": ErrorSchema})
# def atualizar_restaurante(path: RestaurantePathSchema, body: RestauranteUpdateSchema):
#     """Atualiza parcialmente um restaurante existente.
#     Apenas os campos enviados serão atualizados
#     """
#     # breakpoint()
#     restaurante = Session.query(Restaurante).filter(Restaurante.restaurante_id == path.restaurante_id).first()

#     if not restaurante:
#         return {"erro": "Restaurante não encontrado"}, HTTPStatus.NOT_FOUND
    
#     try:
#         dados_update = body.model_dump(exclude_unset=True)

#         for campo, valor in dados_update.items():
#             setattr(restaurante, campo, valor)
        
#         Session.commit()
#         return RestauranteViewSchema.model_validate(restaurante).model_dump(), HTTPStatus.OK

#     except IntegrityError:
#         Session.rollback()
    
#         return {"status": "error", "mensagem": "Não é possível editar restaurante"}, HTTPStatus.CONFLICT
    
#     except Exception as e:
#         Session.rollback()

#         return {"status": "error", "mensagem": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
    
#     finally:
#         Session.remove()