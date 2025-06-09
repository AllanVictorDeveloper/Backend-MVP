from flask import jsonify
from marshmallow import ValidationError
from ma import ma
from db import db
from server.instance import server
from models.despesa import DespesaModel 
from models.categoria import CategoriaModel

api = server.api
app = server.app



@app.before_first_request
def create_tables():
    db.create_all()

    # Exemplo de inserção de dados iniciais (apenas se a tabela estiver vazia)
    if CategoriaModel.query.count() == 0:
        print("Inserindo categorias padrão...")
        db.session.add(CategoriaModel(nome="CARTAO DE CREDITO"))
        db.session.add(CategoriaModel(nome="CARTAO DE DEBITO"))
        db.session.add(CategoriaModel(nome="INTERNET"))
        db.session.add(CategoriaModel(nome="ALUGUEL"))
        db.session.add(CategoriaModel(nome="PIX"))
        db.session.add(CategoriaModel(nome="MORADIA"))
        db.session.add(CategoriaModel(nome="LAZER"))
        db.session.add(CategoriaModel(nome="LUZ"))
        db.session.commit()
        print("Categorias padrão inseridas.")

# Este bloco só é executado quando o script app.py é rodado diretamente (python app.py)
# Se você usar 'flask run', o Flask CLI já gerencia isso, mas ter ambos é seguro.
if __name__ == '__main__':
    db.init_app(app) 
    ma.init_app(app) 
    server.run() 