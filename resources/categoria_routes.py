# resources/categoria_routes.py

# Remova: from app import app
from typing import List
from flask_openapi3 import Tag
from http import HTTPStatus

from sqlalchemy.exc import IntegrityError

from db import db
from models.categoria import CategoriaModel

from schemas.schemas import CategoriaInputSchema, CategoriaViewSchema, ListagemCategoriasSchema, ErrorSchema, \
                            CategoriaBuscaIdSchema


categoria_tag = Tag(name="Categoria", description="Operações de categorias")

def apresenta_categoria(categoria: CategoriaModel) -> CategoriaViewSchema:
    return CategoriaViewSchema.model_validate(categoria)

def apresenta_categorias(categorias: List[CategoriaModel]) -> ListagemCategoriasSchema:
    return {"categorias": [CategoriaViewSchema.model_validate(c) for c in categorias]}


def register_categoria_routes(app):

    @app.post('/categorias', tags=[categoria_tag],
              responses={
                  HTTPStatus.CREATED: CategoriaViewSchema,
                  HTTPStatus.BAD_REQUEST: ErrorSchema,
                  HTTPStatus.CONFLICT: ErrorSchema
              })
    def add_categoria(body: CategoriaInputSchema):
        app.logger.debug(f"Adicionando categoria: '{body.nome}'")
        
        nova_categoria = CategoriaModel(nome=body.nome)
        try:
            db.session.add(nova_categoria)
            db.session.commit()
            app.logger.debug(f"Adicionada categoria: '{nova_categoria.nome}'")
            return apresenta_categoria(nova_categoria), HTTPStatus.CREATED
        except IntegrityError as e:
            error_msg = "Categoria com este nome já existe."
            app.logger.warning(f"Erro ao adicionar categoria '{nova_categoria.nome}', {error_msg}")
            return {"message": error_msg}, HTTPStatus.CONFLICT
        except Exception as e:
            error_msg = f"Não foi possível salvar a nova categoria: {e}"
            app.logger.error(f"Erro inesperado ao adicionar categoria: {e}", exc_info=True)
            return {"message": error_msg}, HTTPStatus.INTERNAL_SERVER_ERROR

    @app.get('/categorias', tags=[categoria_tag],
             responses={HTTPStatus.OK: ListagemCategoriasSchema})
    def get_all_categorias():
        app.logger.debug("Coletando todas as categorias.")
        categorias = CategoriaModel.query.all()
        app.logger.debug(f"{len(categorias)} categorias encontradas.")
        return apresenta_categorias(categorias), HTTPStatus.OK