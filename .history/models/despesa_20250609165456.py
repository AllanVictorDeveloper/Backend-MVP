from db import db

class despesaModel(db.Model):
    __tablename__ = 'despesas'

    id = db.Column("pk_produto", db.Integer, primary_key=True)
    nome_despesa = db.Column(db.String(140), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_despesa = db.Column(db.Date)
    data_vencimento_mensal = db.Column(db.Date, nullable=False)
    cadastrado_em = db.Column(db.DateTime,default=db.datetime.now())