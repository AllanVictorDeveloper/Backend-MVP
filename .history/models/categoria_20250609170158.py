from db import db

class categoriaModel(db.Model):
    __tablename__ = 'categorias'

    id = db.Column("pk_categoria", db.Integer, primary_key=True)
    nome = db.Column(db.String(140), nullable=False)

