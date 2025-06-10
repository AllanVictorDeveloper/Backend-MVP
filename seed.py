# seed.py (Refatorado)

from datetime import datetime
from models.categoria import CategoriaModel 


def seed_categories(app_instance, db_instance): # Recebe app e db como argumentos
    """
    Insere categorias padrão no banco de dados, se ainda não existirem.
    """
    with app_instance.app_context():
        print("Verificando e inserindo categorias padrão...")

        default_categories = [
            "Moradia",
            "Lazer",
            "Alimentação",
            "Transporte",
            "Saúde",
            "Educação",
            "Contas Fixas",
            "Cartão de Crédito",
            "Pix",
            "Cartão de Debito",
            "Outros"
        ]

        for category_name in default_categories:
            existing_category = CategoriaModel.query.filter_by(nome=category_name).first()

            if not existing_category:
                new_category = CategoriaModel(nome=category_name)
                db_instance.session.add(new_category) # Usa a instância de db passada
            else:
                print()
        
        try:
            db_instance.session.commit() # Usa a instância de db passada
        except Exception as e:
            db_instance.session.rollback() # Usa a instância de db passada
            print(f"Erro ao inserir categorias padrão: {e}")
