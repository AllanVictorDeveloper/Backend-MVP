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

    
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.pk_categoria'), nullable=False)

   
    categoria = db.relationship('categoriaModel', backref='despesas', lazy=True) 

   
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


    @classmethod
    def findy_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def findy_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
    

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()