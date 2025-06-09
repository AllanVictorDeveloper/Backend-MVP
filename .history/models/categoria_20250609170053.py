from db import db

class despesaModel(db.Model):
    __tablename__ = 'despesas'

    id = db.Column("pk_categoria", db.Integer, primary_key=True)
    nome = db.Column(db.String(140), nullable=False)

