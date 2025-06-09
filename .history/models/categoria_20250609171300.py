from db import db
from typing import Union
from sqlalchemy import DateTime



class categoriaModel(db.Model):
    __tablename__ = 'categorias'

    id = db.Column("pk_categoria", db.Integer, primary_key=True)
    nome = db.Column(db.String(140), nullable=False)
    cadastrado_em = db.Column(db.DateTime,default=db.datetime.now())

    despesas = db.relationship('despesaModel', backref='categoria', lazy=True)

    def __init__(self, nome:str):
        
        self.nome = nome
        
    def __repr__(self): # Adicionei para melhor representação ao debugar
        return f'<Categoria {self.nome}>'

