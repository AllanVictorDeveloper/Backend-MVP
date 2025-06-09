from flask_restx import Namespace, Resource, fields
from models.despesa import DespesaModel
from models.categoria import CategoriaModel 
from http import HTTPStatus

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
    @despesa_ns.marshal_list_with(despesa_model)

    def get(self):
        return despesaModel.query.all(), HTTPStatus.OK

    @despesa_ns.doc('Criar uma nova despesa')
    @despesa_ns.expect(despesa_model)
    @despesa_ns.marshal_with(despesa_model, code=HTTPStatus.CREATED)
    def post(self):
        data = despesa_ns.payload

        if not categoriaModel.query.get(data['categoria_id']):
            despesa_ns.abort(HTTPStatus.BAD_REQUEST, "Categoria ID não existe")

        nova_despesa = despesaModel(**data)
        try:
            nova_despesa.save_to_db() # Você precisaria adicionar um método save_to_db() no seu modelo
            return nova_despesa, HTTPStatus.CREATED
        except Exception as e:
            despesa_ns.abort(HTTPStatus.INTERNAL_SERVER_ERROR, f"Erro ao criar despesa: {e}")
