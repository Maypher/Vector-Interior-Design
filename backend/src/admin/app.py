from admin.auth.routes import auth_blueprint
from admin.resources.admin_graphql.routes import graphql_blueprint
from sanic import Sanic
from sanic.config import Config
from os import environ
from admin.utilities.types import Context
from admin.db.database import AdminDatabaseManager
from admin.auth.session import SessionManager
from admin.auth.user import UserManager
from admin.resources.obra import AdminResourceManager
from admin.utilities.types import AdminApp
from sanic_ext import Extend, Config


def create_app(config=Config(), ctx=Context()) -> Sanic:
    app = Sanic("TQ-admin-backend", ctx=ctx)
    # Done this way because for some reason when setting it directly in the Sanic instance it's
    # treating it as a Namespace which causes an error.
    app.update_config(config)
    app.blueprint(graphql_blueprint)
    app.blueprint(auth_blueprint)
    app.config.CORS_ORIGINS = [environ.get("FRONTEND_URL"), "https://192.168.0.8:5173"]
    app.config.CORS_SUPPORTS_CREDENTIALS = True
    app.config.CORS_ALLOW_HEADERS = ["Content-Type"]
    Extend(app)

    @app.before_server_start
    def init_context(app: AdminApp):
        database_manager = AdminDatabaseManager(
            environ.get("USERNAME"),
            environ.get("PASSWORD"),
            environ.get("HOST"),
            environ.get("DB_PORT"),
            environ.get("DB_NAME"),
        )
        app.ctx.database_manager = database_manager
        app.ctx.session_manager = SessionManager(database_manager)
        app.ctx.user_manager = UserManager(database_manager)
        app.ctx.resource_manager = AdminResourceManager(database_manager)

    return app
