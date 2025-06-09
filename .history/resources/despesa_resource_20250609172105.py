# resources/despesa_resource.py
from flask_restx import Namespace, Resource, fields
from models.despesa import despesaModel
from models.categoria import categoriaModel # Necessário para relacionamento
from http import HTTPStatus # Para retornar status codes

despesa_ns = Namespace('despesas', description='Operações relacionadas a despesas')

# Modelo para serialização/deserialização de dados (Marshmallow seria melhor aqui)
despesa_model = despesa_ns.model('Despesa', {
    'nome_despesa': fields.String(required=True, description='Nome da despesa'),
    'valor': fields.Float(required=True, description='Valor da despesa'),
    'data_despesa': fields.Date(description='Data da despesa (YYYY-MM-DD)'),
    'data_vencimento_mensal': fields.Date(required=True, description='Data de vencimento mensal (YYYY-MM-DD)'),
    'categoria_id': fields.Integer(required=True, description='ID da categoria associada')
})

@despesa_ns.route('/')
class DespesaList(Resource):
    @despesa_ns.doc('Listar todas as despesas')
    @despesa_ns.marshal_list_with(despesa_model) # Usaria Marshmallow aqui para algo mais robusto
    def get(self):
        return despesaModel.query.all(), HTTPStatus.OK

    @despesa_ns.doc('Criar uma nova despesa')
    @despesa_ns.expect(despesa_model)
    @despesa_ns.marshal_with(despesa_model, code=HTTPStatus.CREATED)
    def post(self):
        data = despesa_ns.payload
        # Validação básica de categoria_id
        if not categoriaModel.query.get(data['categoria_id']):
            despesa_ns.abort(HTTPStatus.BAD_REQUEST, "Categoria ID não existe")

        nova_despesa = despesaModel(**data)
        try:
            nova_despesa.save_to_db() # Você precisaria adicionar um método save_to_db() no seu modelo
            return nova_despesa, HTTPStatus.CREATED
        except Exception as e:
            despesa_ns.abort(HTTPStatus.INTERNAL_SERVER_ERROR, f"Erro ao criar despesa: {e}")

# Adicione métodos save_to_db e delete_from_db nos seus modelos (models/despesa.py e models/categoria.py)
# Exemplo para despesaModel e categoriaModel:
# def save_to_db(self):
#     db.session.add(self)
#     db.session.commit()
#
# def delete_from_db(self):
#     db.session.delete(self)
#     db.session.commit()