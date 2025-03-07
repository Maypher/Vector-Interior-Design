from admin.auth.routes import auth_blueprint
from admin.resources.admin_graphql.routes import graphql_blueprint
from sanic import Sanic
from sanic.config import Config
from os import environ
from admin.utilities.types import Context
from admin.db.database import AdminDatabaseManager
from admin.auth.session import SessionManager
from admin.auth.user import UserManager
from admin.resources.resource_manager import AdminResourceManager
from admin.utilities.types import AdminApp
from sanic_ext import Extend, Config
from common.utils import read_secret
from sanic.log import logger


def create_app(
    config=Config(), ctx=Context(), database_manager: AdminDatabaseManager = None
) -> Sanic:
    app = Sanic("TQ-admin-backend", ctx=ctx)
    # Done this way because for some reason when setting it directly in the Sanic instance it's
    # treating it as a Namespace which causes an error.
    app.update_config(config)
    app.blueprint(graphql_blueprint)
    app.blueprint(auth_blueprint)
    app.config.CORS_ORIGINS = [
        environ.get("FRONTEND_URL", ""),
        "https://192.168.0.8:5173",
    ]
    app.config.CORS_SUPPORTS_CREDENTIALS = True
    app.config.CORS_ALLOW_HEADERS = ["Content-Type"]
    Extend(app)

    @app.before_server_start
    def init_context(app: AdminApp):
        db_manager = database_manager or AdminDatabaseManager(
            environ.get("USERNAME"),
            read_secret("admin_password"),
            environ.get("HOST"),
            environ.get("DB_PORT"),
            environ.get("DB_NAME"),
        )
        app.ctx.database_manager = db_manager
        app.ctx.session_manager = SessionManager(db_manager)
        app.ctx.user_manager = UserManager(db_manager)
        app.ctx.resource_manager = AdminResourceManager(db_manager)

    return app
