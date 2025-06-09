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



    categoria = db.relationship("Categoria")


    def __init__(self, nome_despesa:str, valor:float, data_despesa:Union[DateTime, None] = None, 
                 data_vencimento_mensal:Union[DateTime, None] = None):
        self.nome_despesa = nome_despesa
        self.valor = valor
        self.data_despesa = data_despesa
        self.data_vencimento_mensal =  data_vencimento_mensal

