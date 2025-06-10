from flask_openapi3 import OpenAPI, Info

def create_app():
    info = Info(title="Backend MVP", version="1.0.0", description='Api do sistema de controle de despesas mensais.')
    app = OpenAPI(__name__, info=info)

    # Mova as configurações de app.config para cá
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True

    return app