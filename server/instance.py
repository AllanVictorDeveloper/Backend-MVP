from flask import Flask, Blueprint
from flask_restx import Api


class Server():
    def __init__(self,):
        self.app = Flask(__name__)
        self.blueprint = Blueprint('api',  __name__, url_prefix='/api')
        # Configurar a API RESTx
        self.api = Api(
            self.blueprint,
            doc="/doc", # Rota para a documentação Swagger UI
            title='Backend MVP',
            description='Uma API Flask para seu MVP'
        )
        self.app.register_blueprint(self.blueprint)

        # Configurações do SQLAlchemy
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
        self.app.config['PROPAGATE_EXCEPTIONS'] = True
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Boa prática para evitar warnings

        # --- Importe seus namespaces (Recursos da API) aqui ---
        # Exemplo: Se você tiver um arquivo resources/despesa.py
        # ou se seus namespaces forem definidos diretamente aqui.
        # Por enquanto, vou remover a linha `self.books = self.books_ns()`
        # e o método `book_ns` porque eles não estão completos e são a causa do erro.
        # Quando você criar seus recursos de Despesa e Categoria, você vai adicioná-los
        # ao 'api' aqui ou em outro arquivo e importá-los.

    def run(self,):
        # O host='0.0.0.0' é útil se você for acessar de outras máquinas na rede local.
        # Em produção, você usaria um servidor WSGI como Gunicorn/Waitress.
        self.app.run(
            port=5000,
            debug=True, # Mantenha True para desenvolvimento
            host='0.0.0.0'
        )


server = Server()