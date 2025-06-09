from ma import ma
from models.despesa import DespesaModel


class DespesaSchema(ma.SQLAlchemyAutoSchema):
    class Mete:
        model = DespesaModel
        load_instance = True