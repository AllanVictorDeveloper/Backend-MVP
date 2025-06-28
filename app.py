
from flask_openapi3 import Tag, OpenAPI, Info
from flask import redirect, current_app
from http import HTTPStatus

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from db import db
from models.despesa import DespesaModel
from models.categoria import CategoriaModel
from schemas.schemas import DespesaBuscaIdSchema, DespesaInputSchema, DespesaViewSchema, ListagemDespesasSchema, ErrorSchema, \
                        CategoriaInputSchema, CategoriaViewSchema, ListagemCategoriasSchema, DespesaAtualizarInputSchema

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from flask_cors import CORS
from seed import seed_categories
from typing import List

# --- Inicialize o app principal como OpenAPI ---
info = Info(title="Backend MVP", version="1.0.0", description='Api do sistema de controle de despesas mensais.')
app = OpenAPI(__name__, info=info) # Crie a instância OpenAPI

# Configure o CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure o app.config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


# --- TAGS ---
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
despesa_tag = Tag(name="Despesa", description="Operações de despesas")
categoria_tag = Tag(name="Categoria", description="Operações de categorias")

# --- FUNÇÕES DE APRESENTAÇÃO ---
def apresenta_despesa(despesa: DespesaModel) -> DespesaViewSchema:
    return DespesaViewSchema.model_validate(despesa).model_dump()

def apresenta_despesas(despesas: List[DespesaModel]) -> ListagemDespesasSchema:
    return {"despesas": [DespesaViewSchema.model_validate(d).model_dump() for d in despesas]}

def apresenta_categoria(categoria: CategoriaModel) -> CategoriaViewSchema:
    return CategoriaViewSchema.model_validate(categoria).model_dump()

def apresenta_categorias(categorias: List[CategoriaModel]) -> ListagemCategoriasSchema:
    return {"categorias": [CategoriaViewSchema.model_validate(c).model_dump() for c in categorias]}


# --- ROTAS DA HOME / DOCS ---
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# --- ROTAS DE DESPESAS ---
@app.post('/cadastrar_despesas', tags=[despesa_tag],
          responses={
              HTTPStatus.CREATED: DespesaViewSchema,
              HTTPStatus.BAD_REQUEST: ErrorSchema,
              HTTPStatus.CONFLICT: ErrorSchema,
              HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema
          })
def add_despesa(body: DespesaInputSchema):
    current_app.logger.debug(f"Adicionando despesa: '{body.nome_despesa}'")

    if not CategoriaModel.query.get(body.categoria_id):
        error_msg = "Categoria ID não existe."
        current_app.logger.warning(f"Erro ao adicionar despesa '{body.nome_despesa}', {error_msg}")
        return {"message": error_msg}, HTTPStatus.BAD_REQUEST

    despesa = DespesaModel(
        nome_despesa=body.nome_despesa,
        valor=body.valor,
        data_despesa=body.data_despesa,
        data_vencimento_mensal=body.data_vencimento_mensal,
        categoria_id=body.categoria_id
    )
    current_app.logger.debug(f"Despesa criada: {despesa}")
    try:
        db.session.add(despesa)
        db.session.commit()
        current_app.logger.debug(f"Adicionada despesa: '{despesa.nome_despesa}'")
        return apresenta_despesa(despesa), HTTPStatus.CREATED
    except IntegrityError as e:
        error_msg = e.orig.args[0] if e.orig else "Erro de integridade ao adicionar despesa."
        db.session.rollback()  
        current_app.logger.warning(f"Erro ao adicionar despesa '{despesa.nome_despesa}', {error_msg}")
        return {"message": error_msg}, HTTPStatus.CONFLICT
    except Exception as e:
        db.session.rollback()
        error_msg = f"Não foi possível salvar a nova despesa: {e}"
        current_app.logger.error(f"Erro inesperado ao adicionar despesa: {e}", exc_info=True)
        return {"message": error_msg}, HTTPStatus.INTERNAL_SERVER_ERROR


@app.put('/atualizar_despesa', tags=[despesa_tag],
          responses={
              HTTPStatus.OK: DespesaViewSchema,
              HTTPStatus.BAD_REQUEST: ErrorSchema,
              HTTPStatus.CONFLICT: ErrorSchema,
              HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema
          })
def update_despesa(body: DespesaAtualizarInputSchema):
    current_app.logger.debug(f"Iniciando atualização para despesa ID: {body.despesa_id} com dados: {body}")

    # 1. Buscar a despesa existente
    despesa = DespesaModel.query.options(joinedload(DespesaModel.categoria)).get(body.despesa_id)

    if not despesa:
        error_msg = f"Despesa com ID {body.despesa_id} não encontrada para atualizar."
        current_app.logger.warning(error_msg)
        return {"message": error_msg}, HTTPStatus.NOT_FOUND

    if body.categoria_id and not CategoriaModel.query.get(body.categoria_id):
        error_msg = f"Categoria com ID {body.categoria_id} não existe."
        current_app.logger.warning(f"Erro ao atualizar despesa '{body.despesa_id}', {error_msg}")
        return {"message": error_msg}, HTTPStatus.BAD_REQUEST

    try:
        despesa.nome_despesa = body.nome_despesa
        despesa.valor = body.valor
        despesa.data_despesa = body.data_despesa
        despesa.data_vencimento_mensal = body.data_vencimento_mensal
        despesa.categoria_id = body.categoria_id

        # 4. Commit as mudanças
        db.session.commit()
        current_app.logger.debug(f"Despesa ID {body.despesa_id} atualizada com sucesso.")
        return apresenta_despesa(despesa), HTTPStatus.OK
    except IntegrityError as e:
        db.session.rollback() # Em caso de erro de integridade, reverta
        error_msg = "Já existe uma despesa com este nome." # Ou nome_despesa deve ser único
        current_app.logger.warning(f"Erro de integridade ao atualizar despesa '{body.despesa_id}': {error_msg}")
        return {"message": error_msg}, HTTPStatus.CONFLICT
    except Exception as e:
        db.session.rollback() # Em caso de qualquer outro erro, reverta
        error_msg = f"Erro inesperado ao atualizar despesa ID {body.despesa_id}: {e}"
        current_app.logger.error(error_msg, exc_info=True)
        return {"message": error_msg}, HTTPStatus.INTERNAL_SERVER_ERROR



@app.get('/buscar_despesas', tags=[despesa_tag],
         responses={HTTPStatus.OK: ListagemDespesasSchema, HTTPStatus.NOT_FOUND: ErrorSchema})
def get_all_despesas():
    current_app.logger.debug("Coletando todas as despesas.")
    despesas = DespesaModel.query.options(joinedload(DespesaModel.categoria)).all()

    if not despesas:
        return {"despesas": []}, HTTPStatus.OK
    else:
        current_app.logger.debug(f"{len(despesas)} despesas encontradas.")
        return apresenta_despesas(despesas), HTTPStatus.OK


@app.get('/buscar_despesas_por_id', tags=[despesa_tag],
         responses={HTTPStatus.OK: DespesaViewSchema, HTTPStatus.NOT_FOUND: ErrorSchema})
def get_single_despesa(body: DespesaBuscaIdSchema):
    despesa = DespesaModel.query.options(joinedload(DespesaModel.categoria)).get(body.despesa_id)

    if not despesa:
        error_msg = f"Despesa com ID {body.despesa_id} não encontrada."
        current_app.logger.warning(f"Erro ao buscar despesa '{body.despesa_id}', {error_msg}")
        return {"message": error_msg}, HTTPStatus.NOT_FOUND
    else:
        current_app.logger.debug(f"Despesa encontrada: '{despesa.nome_despesa}'")
        return apresenta_despesa(despesa), HTTPStatus.OK


@app.delete('/deletar_despesa', tags=[despesa_tag],
            responses={HTTPStatus.NO_CONTENT: None, HTTPStatus.NOT_FOUND: ErrorSchema})
def delete_despesa_by_id(body: DespesaBuscaIdSchema):
    despesa_id = body.despesa_id
    despesa = DespesaModel.query.get(despesa_id)

    if not despesa:
        error_msg = f"Despesa com ID {despesa_id} não encontrada para deletar."
        current_app.logger.warning(f"Erro ao deletar despesa '{despesa_id}', {error_msg}")
        return {"message": error_msg}, HTTPStatus.NOT_FOUND
    else:
        try:
            db.session.delete(despesa)
            db.session.commit()
            current_app.logger.debug(f"Despesa ID {despesa_id} deletada.")
            return '', HTTPStatus.NO_CONTENT
        except Exception as e:
            db.session.rollback()
            error_msg = f"Erro ao deletar despesa: {e}"
            current_app.logger.error(f"Erro inesperado ao deletar despesa: {e}", exc_info=True)
            return {"message": error_msg}, HTTPStatus.INTERNAL_SERVER_ERROR


# --- ROTAS DE CATEGORIAS ---
# @app.post('/cadastrar_categoria', tags=[categoria_tag],
#           responses={
#               HTTPStatus.CREATED: CategoriaViewSchema,
#               HTTPStatus.BAD_REQUEST: ErrorSchema,
#               HTTPStatus.CONFLICT: ErrorSchema
#           })
# def add_categoria(body: CategoriaInputSchema):
#     current_app.logger.debug(f"Adicionando categoria: '{body.nome}'")

#     nova_categoria = CategoriaModel(nome=body.nome)
#     try:
#         db.session.add(nova_categoria)
#         db.session.commit()
#         current_app.logger.debug(f"Adicionada categoria: '{nova_categoria.nome}'")
#         return apresenta_categoria(nova_categoria), HTTPStatus.CREATED
#     except IntegrityError as e:
#         error_msg = "Categoria com este nome já existe."
#         current_app.logger.warning(f"Erro ao adicionar categoria '{nova_categoria.nome}', {error_msg}")
#         return {"message": error_msg}, HTTPStatus.CONFLICT
#     except Exception as e:
#         error_msg = f"Não foi possível salvar a nova categoria: {e}"
#         current_app.logger.error(f"Erro inesperado ao adicionar categoria: {e}", exc_info=True)
#         return {"message": error_msg}, HTTPStatus.INTERNAL_SERVER_ERROR

@app.get('/buscar_categorias', tags=[categoria_tag],
         responses={HTTPStatus.OK: ListagemCategoriasSchema})
def get_all_categorias():
    categorias = CategoriaModel.query.all()
    current_app.logger.debug(f"{len(categorias)} categorias encontradas.")
    return apresenta_categorias(categorias), HTTPStatus.OK


# --- INICIALIZAÇÃO DO APP ---
if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        db.create_all()
        seed_categories(app, db)

    app.run(debug=True, host='0.0.0.0', port=5000)