from os import environ
from strawberry import Schema
from user.user_graphql import Query
from sanic import Sanic, Config
from user.utilities.types import Context, UserApp
from user.user_graphql import UserGraphQLView
from common.obra import ResourceManager
from common.database import DatabaseManager


def create_app(ctx=Context()) -> Sanic:
    app = Sanic("TQ-admin-backend", ctx=ctx)

    app.add_route(
        UserGraphQLView.as_view("graphql_user", schema=Schema(query=Query)),
        "/graphql",
    )

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
