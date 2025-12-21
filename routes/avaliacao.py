from urllib.parse import unquote
from flask_openapi3 import APIBlueprint, Tag
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError

from models import Session
from models.avaliacao import Avaliacao
from models.restaurante import Restaurante
from models.usuario import Usuario
from schemas.error import ErrorSchema
from schemas.avaliacao import AvaliacaoPathSchema, AvaliacaoSchema, AvaliacaoViewSchema
from utils.validations import validar_usuario_restaurante

avaliacoes_bp = APIBlueprint(
    'avaliacoes',
    __name__,
    url_prefix='/avaliacoes',
    abp_tags=[Tag(name='Avalicoes', description='Operações de avaliacoes')]
)

@avaliacoes_bp.post('/criar', responses={"201": AvaliacaoViewSchema, "404": ErrorSchema, "409": ErrorSchema, "400": ErrorSchema})
def criar_avaliacao(form: AvaliacaoSchema):
    """Adiciona uma nova avaliacao a um restaurante

    Retorna uma representação da avaliacao
    """
    validacao = validar_usuario_restaurante(
        form.usuario_id,
        form.restaurante_id
    )

    if not validacao["valid"]:
        return validacao["error"], HTTPStatus.NOT_FOUND
    
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

@avaliacoes_bp.get('/<int:id_restaurante>/<id_usuario>', responses={"404": ErrorSchema})
# {"200": ListagemRestaurantesSchema, "404": ErrorSchema}
def buscar_avaliacao(path:AvaliacaoPathSchema):
    """Busca e retorna os dados de uma avaliacao com base no restaurante e usuario
    """
    numero_restaurante = path.id_restaurante
    usuario_id = str(path.id_usuario)

    try:
        validacao = validar_usuario_restaurante(usuario_id, numero_restaurante)
        if not validacao["valid"]:
            
            return validacao["error"], HTTPStatus.NOT_FOUND
        else:
            avaliacao = Session.query(Avaliacao).filter(
            Avaliacao.restaurante_id == numero_restaurante,
            Avaliacao.usuario_id == usuario_id).first()

            if not avaliacao:
                return {
                "status": "error",
                "mensagem": f"Avaliacao não localizada no sistema."
            }, HTTPStatus.NOT_FOUND

            return {
                "status": "success",
                "dados": AvaliacaoViewSchema.model_validate(avaliacao).model_dump()
            }, HTTPStatus.OK
    
    except Exception as e:
        return {"status": "error", "mensagem": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    finally:
        Session.remove()


@avaliacoes_bp.delete('/<int:id_restaurante>/<id_usuario>',
            responses={"404": ErrorSchema})
def deletar_avaliacao(path: AvaliacaoPathSchema):
    """Remove uma avaliacao do sistema com base nos dados de usuario e restaurante fornecido.
    Retorna uma resposta indicando o sucesso ou a falha da operação.
    """
    numero_restaurante = path.id_restaurante
    usuario_id = str(path.id_usuario)
   
    try:
        validacao = validar_usuario_restaurante(usuario_id,numero_restaurante)
        if not validacao["valid"]:
            return validacao["error"], HTTPStatus.NOT_FOUND
        else:
            avaliacao = Session.query(Avaliacao).filter(
                Avaliacao.restaurante_id == numero_restaurante, Avaliacao.usuario_id == usuario_id).first()
       
            if avaliacao:
                Session.query(Avaliacao).filter(
                    Avaliacao.restaurante_id == numero_restaurante, Avaliacao.usuario_id == usuario_id).delete()
                Session.commit()
                
                return {
                    "status": "success",
                    "mensagem": f"Avaliacao removida com sucesso."
                }, HTTPStatus.OK
            else:
                return {
                    "status": "error",
                    "mensagem": f"Avaliacao não encontrada no sistema."
                }, HTTPStatus.NOT_FOUND
        
    except IntegrityError:
        Session.rollback()
    
        return {"status": "error", "mensagem": "Não é possível deletar"}, HTTPStatus.CONFLICT
    
    except Exception as e:
        Session.rollback()

        return {"status": "error", "mensagem": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    finally:
        Session.remove()

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