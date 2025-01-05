from admin.auth.routes import auth_blueprint
from admin.resources import obra_admin_routes, image_admin_routes, ambiente_admin_routes
from sanic import Sanic
from sanic.config import Config


def create_app(config=Config()) -> Sanic:
    app = Sanic("TQ-admin-backend", config=config)
    print(app.config)
    app.blueprint(auth_blueprint)
    return app
