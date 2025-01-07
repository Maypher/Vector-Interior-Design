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


def create_app(ctx=Context()) -> Sanic:
    app = Sanic("TQ-admin-backend", ctx=ctx)
    app.blueprint(graphql_blueprint)
    app.blueprint(auth_blueprint)

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
