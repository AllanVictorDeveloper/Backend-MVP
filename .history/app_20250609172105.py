from flask import jsonify
from marshmallow import ValidationError

# Importe 'ma' e 'db' do seu db.py e ma.py
from ma import ma
from db import db

# Importe a instância do servidor (server) do seu instance.py
from server.instance import server

# Importe seus modelos aqui para que o SQLAlchemy os reconheça
from models.despesa import despesaModel # Assumindo models/despesa.py
from models.categoria import categoriaModel # Assumindo models/categoria.py

# Importe seus recursos/namespaces para que o Flask-RESTx os registre
# Exemplo: Se você tem um arquivo routes/despesa_resource.py
# from resources.despesa import DespesaList, Despesa
# E depois adiciona ao api.add_resource(...) ou @api.route(...)

# Inicialize o Flask-RESTx com a instância 'api'
api = server.api
app = server.app

# Importe e adicione seus namespaces (endpoints) ao Flask-RESTx
# Você precisará criar arquivos para isso, por exemplo, em uma pasta 'resources'.
# Exemplo:
# from resources.despesa_resource import DespesaNamespace
# from resources.categoria_resource import CategoriaNamespace
# api.add_namespace(DespesaNamespace)
# api.add_namespace(CategoriaNamespace)


@app.before_first_request
def create_tables(): # Renomeei para create_tables para clareza
    db.create_all()

# Este bloco só é executado quando o script app.py é rodado diretamente (python app.py)
# Se você usar 'flask run', o Flask CLI já gerencia isso, mas ter ambos é seguro.
if __name__ == '__main__':
    db.init_app(app) # Inicializa o SQLAlchemy com o app Flask
    ma.init_app(app) # Inicializa o Marshmallow com o app Flask
    server.run() # Inicia o servidor Flask