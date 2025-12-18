from urllib.parse import unquote
import uuid
from flask_openapi3 import APIBlueprint, Tag
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError

from models import Session
from models.restaurante import Restaurante
from schemas.error import ErrorSchema
from schemas.restaurante import ListagemRestaurantesSchema, RestauranteBuscaSchema, RestauranteSchema, RestauranteViewSchema

restaurantes_bp = APIBlueprint(
    'restaurantes',
    __name__,
    url_prefix='/restaurantes',
    abp_tags=[Tag(name='Restaurantes', description='Operações de restaurantes')]
)

@restaurantes_bp.post('/criar', responses={"201": RestauranteViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def criar_restaurante(form: RestauranteSchema):
    """Adiciona um novo restaurante à base de dados

    Retorna uma representação do restaurante.
    """
    try:
        restaurante = Restaurante(
            nome_restaurante = form.nome_restaurante,
            endereco_1 = form.endereco_1,
            endereco_2 = form.endereco_2,
            culinaria = form.culinaria
        )

        Session.add(restaurante)
        Session.commit()

        return RestauranteViewSchema.model_validate(restaurante).model_dump(), HTTPStatus.CREATED
    
    except IntegrityError:
        Session.rollback()

        return {"erro": "Email já existe"}, HTTPStatus.CONFLICT
    
    except Exception as e:
        Session.rollback()
        return {"erro": str(e)}, HTTPStatus.BAD_REQUEST

    finally:
        Session.remove()

@restaurantes_bp.get('/', responses={"200": ListagemRestaurantesSchema, "404": ErrorSchema})
def buscar_restaurante(query:RestauranteBuscaSchema):
    """Busca e retorna os dados detalhados de um restaurante a partir do id
    """
   
    try:
        numero_restaurante = query.id_restaurante
        restaurante = Session.query(Restaurante).filter(Restaurante.restaurante_id == numero_restaurante).first()

        if not restaurante:
            return {
                "status": "error",
                "mensagem": f"Restaurante não localizado no sistema."
            }, HTTPStatus.NOT_FOUND
        else:
            return {
                "status": "sucess",
                "dados": RestauranteViewSchema.model_validate(restaurante).model_dump()
            }, HTTPStatus.OK
    
    except Exception as e:
        return {"status": "error", "mensagem": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    finally:
        Session.remove()


@restaurantes_bp.delete('/',
            responses={"200": ListagemRestaurantesSchema, "404": ErrorSchema})
def deletar_restaurante(query:RestauranteBuscaSchema):
    """Remove um restaurante do sistema com base no uuid fornecido.
    Retorna uma resposta indicando o sucesso ou a falha da operação.
    """
    
    numero_restaurante = query.id_restaurante
   
    try:
        restaurante = Session.query(Restaurante).filter(Restaurante.restaurante_id == numero_restaurante).first()
        
        if restaurante:
            Session.query(Restaurante).filter(Restaurante.restaurante_id == numero_restaurante).delete()
            Session.commit()
            
            return {
                "status": "sucess",
                "mensagem": f"Restaurante ({numero_restaurante}) '{restaurante.nome_restaurante}' removido com sucesso."
            }, HTTPStatus.OK
        else:
            return {
                "status": "error",
                "mensagem": f"Restaurante não encontrado no sistema."
            }, HTTPStatus.NOT_FOUND
    
    except IntegrityError:
        Session.rollback()
    
        return {"status": "error", "mensagem": "Não é possível deletar"}, HTTPStatus.CONFLICT
    
    except Exception as e:
        Session.rollback()

        return {"status": "error", "mensagem": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    finally:
        Session.remove()

@restaurantes_bp.patch('/', responses={"200": ListagemRestaurantesSchema, "404": ErrorSchema})
def atualizar_restaurante(query:RestauranteBuscaSchema):
    numero_restaurante = query.id_restaurante