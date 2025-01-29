from os import environ
from strawberry import Schema
from user.user_graphql import Query
from sanic import Sanic
from user.utilities.types import Context, UserApp
from user.user_graphql import UserGraphQLView
from common.resource_manager import ResourceManager
from common.database import DatabaseManager
from sanic_ext import Extend, Config
import os


def create_app(ctx=Context()) -> Sanic:
    app = Sanic("TQ-admin-backend", ctx=ctx)

    app.add_route(
        UserGraphQLView.as_view(schema=Schema(query=Query)),
        "/graphql",
    )

    app.update_config(Config)

    app.config.CORS_ALLOW_HEADERS = ["Content-Type"]
    app.config.CORS_ORIGINS = [os.environ.get("FRONTEND_URL")]
    Extend(app)

    @app.before_server_start
    def init_context(app: UserApp):
        database_manager = DatabaseManager(
            environ.get("USERNAME"),
            environ.get("PASSWORD"),
            environ.get("HOST"),
            environ.get("DB_PORT"),
            environ.get("DB_NAME"),
        )
        app.ctx.resource_manager = ResourceManager(database_manager)

    return app
