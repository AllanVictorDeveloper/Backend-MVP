from db import db
from typing import Union
from sqlalchemy import DateTime

class despesaModel(db.Model):
    __tablename__ = 'despesas'

    id = db.Column("pk_produto", db.Integer, primary_key=True)
    nome_despesa = db.Column(db.String(140), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_despesa = db.Column(db.Date)
    data_vencimento_mensal = db.Column(db.Date, nullable=False)
    cadastrado_em = db.Column(db.DateTime,default=db.datetime.now())

    # --- Adições para o Relacionamento ---

    # 1. Chave Estrangeira (Foreign Key)
    # 'categorias.pk_categoria' -> refere-se ao nome da tabela e ao nome da coluna primária na tabela 'categorias'
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.pk_categoria'), nullable=False)

    # 2. Relacionamento (Relationship)
    # Permite acessar o objeto Categoria associado a esta despesa.
    # 'categoriaModel' é o nome da classe do modelo com a qual estamos nos relacionando.
    # backref='despesas' (opcional): cria um atributo 'despesas' na categoriaModel
    #                                que permite acessar todas as despesas daquela categoria.
    categoria = db.relationship('categoriaModel', backref='despesas', lazy=True) 

    # --- Fim das Adições ---


    def __init__(self, nome_despesa: str, valor: float, 
                 data_despesa: Union[DateTime, None] = None, 
                 data_vencimento_mensal: Union[DateTime, None] = None,
                 categoria_id: int = None):
        
        self.nome_despesa = nome_despesa
        self.valor = valor
        self.data_despesa = data_despesa
        self.data_vencimento_mensal = data_vencimento_mensal
        self.categoria_id = categoria_id 


    def __repr__(self): # Adicionei para melhor representação ao debugar
        return f'<Despesa {self.nome_despesa} - Categoria ID: {self.categoria_id}>'
