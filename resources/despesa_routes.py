# resources/despesa_routes.py

# Remova: from app import app (não precisamos importar app aqui diretamente)
from flask_openapi3 import Tag
from http import HTTPStatus

from sqlalchemy.exc import IntegrityError 

from db import db
from models.despesa import DespesaModel
from models.categoria import CategoriaModel

from schemas.schemas import DespesaInputSchema, DespesaViewSchema, ListagemDespesasSchema, ErrorSchema, \
                     DespesaBuscaIdSchema

from typing import List 

despesa_tag = Tag(name="Despesa", description="Operações de despesas")

def apresenta_despesa(despesa: DespesaModel) -> DespesaViewSchema:
    return DespesaViewSchema.model_validate(despesa).model_dump()

def apresenta_despesas(despesas: List[DespesaModel]) -> ListagemDespesasSchema:
    return {"despesas": [DespesaViewSchema.model_validate(d).model_dump() for d in despesas]}


def register_despesa_routes(app):
    
    @app.post('/despesas', tags=[despesa_tag],
              responses={
                  HTTPStatus.CREATED: DespesaViewSchema,
                  HTTPStatus.BAD_REQUEST: ErrorSchema,
                  HTTPStatus.CONFLICT: ErrorSchema,
                  HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema
              })
    def add_despesa(body: DespesaInputSchema):
        app.logger.debug(f"Adicionando despesa: '{body.nome_despesa}'")

        if not CategoriaModel.query.get(body.categoria_id):
            error_msg = "Categoria ID não existe."
            app.logger.warning(f"Erro ao adicionar despesa '{body.nome_despesa}', {error_msg}")
            return {"message": error_msg}, HTTPStatus.BAD_REQUEST

        despesa = DespesaModel(
            nome_despesa=body.nome_despesa,
            valor=body.valor,
            data_despesa=body.data_despesa,
            data_vencimento_mensal=body.data_vencimento_mensal,
            categoria_id=body.categoria_id
        )

        try:
            db.session.add(despesa)
            db.session.commit()
            app.logger.debug(f"Adicionada despesa: '{despesa.nome_despesa}'")
            return apresenta_despesa(despesa), HTTPStatus.CREATED 
        except IntegrityError as e:
            error_msg = "Já existe uma despesa com este nome."
            app.logger.warning(f"Erro ao adicionar despesa '{despesa.nome_despesa}', {error_msg}")
            return {"message": error_msg}, HTTPStatus.CONFLICT
        except Exception as e:
            error_msg = f"Não foi possível salvar a nova despesa: {e}"
            app.logger.error(f"Erro inesperado ao adicionar despesa: {e}", exc_info=True)
            return {"message": error_msg}, HTTPStatus.INTERNAL_SERVER_ERROR


    @app.get('/despesas', tags=[despesa_tag],
             responses={HTTPStatus.OK: ListagemDespesasSchema, HTTPStatus.NOT_FOUND: ErrorSchema})
    def get_all_despesas():
        app.logger.debug("Coletando todas as despesas.")
        despesas = DespesaModel.query.all()

        if not despesas:
            return {"despesas": []}, HTTPStatus.OK
        else:
            app.logger.debug(f"{len(despesas)} despesas encontradas.")
            return apresenta_despesas(despesas), HTTPStatus.OK


    @app.get('/despesas/<int:despesa_id>', tags=[despesa_tag],
             responses={HTTPStatus.OK: DespesaViewSchema, HTTPStatus.NOT_FOUND: ErrorSchema})
    def get_despesa_by_id(despesa_id: int):
        app.logger.debug(f"Coletando dados sobre despesa ID: #{despesa_id}")
        despesa = DespesaModel.query.get(despesa_id)

        if not despesa:
            error_msg = f"Despesa com ID {despesa_id} não encontrada."
            app.logger.warning(f"Erro ao buscar despesa '{despesa_id}', {error_msg}")
            return {"message": error_msg}, HTTPStatus.NOT_FOUND
        else:
            app.logger.debug(f"Despesa encontrada: '{despesa.nome_despesa}'")
            return apresenta_despesa(despesa), HTTPStatus.OK


    @app.delete('/despesas/<int:despesa_id>', tags=[despesa_tag],
                responses={HTTPStatus.NO_CONTENT: None, HTTPStatus.NOT_FOUND: ErrorSchema})
    def delete_despesa_by_id(despesa_id: int):
        app.logger.debug(f"Deletando despesa ID: #{despesa_id}")
        despesa = DespesaModel.query.get(despesa_id)

        if not despesa:
            error_msg = f"Despesa com ID {despesa_id} não encontrada para deletar."
            app.logger.warning(f"Erro ao deletar despesa '{despesa_id}', {error_msg}")
            return {"message": error_msg}, HTTPStatus.NOT_FOUND
        else:
            try:
                db.session.delete(despesa)
                db.session.commit()
                app.logger.debug(f"Despesa ID {despesa_id} deletada.")
                return '', HTTPStatus.NO_CONTENT
            except Exception as e:
                db.session.rollback()
                error_msg = f"Erro ao deletar despesa: {e}"
                app.logger.error(f"Erro inesperado ao deletar despesa: {e}", exc_info=True)
                return {"message": error_msg}, HTTPStatus.INTERNAL_SERVER_ERROR