from flask_openapi3 import Tag
from flask import redirect
from urllib.parse import unquote
from http import HTTPStatus

from sqlalchemy.exc import IntegrityError
from sqlalchemy import text, func

from typing import List
from server.instance import create_app

from db import db
from models.despesa import DespesaModel
from models.categoria import CategoriaModel
from schemas.schemas import DespesaInputSchema, DespesaViewSchema, ListagemDespesasSchema, ErrorSchema, \
                     DespesaBuscaIdSchema

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from flask_cors import CORS
from seed import seed_categories


app = create_app()
CORS(app)


home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")

from resources.despesa_routes import register_despesa_routes
from resources.categoria_routes import register_categoria_routes


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')



if __name__ == '__main__':
    db.init_app(app)

    with app.app_context(): 
        db.create_all()
        seed_categories(app, db)
        register_despesa_routes(app)
        register_categoria_routes(app)

    app.run(debug=True, host='0.0.0.0', port=5000)