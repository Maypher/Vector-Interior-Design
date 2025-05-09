from os import environ
from strawberry import Schema
from user.user_graphql import Query
from sanic import Sanic
from user.utilities.types import Context, UserApp
from user.user_graphql import UserGraphQLView
from common.resource_manager import ResourceManager
from common.utils import read_secret
from common.database import DatabaseManager
from sanic_ext import Extend, Config
import os
from common.utilities.environment import dev_mode


def create_app(ctx=Context()) -> Sanic:
    app = Sanic("TQ-user-backend", ctx=ctx)

    app.add_route(
        UserGraphQLView.as_view(
            schema=Schema(query=Query), graphql_ide="graphiql" if dev_mode else None
        ),
        "/graphql",
        methods=["POST", "GET"],
    )
    app.config.FORWARDED_SECRET = read_secret("nginx_forward_secret")
    app.update_config(Config)

    Extend(app)

    @app.before_server_start
    def init_context(app: UserApp):
        database_manager = DatabaseManager(
            environ.get("USERNAME"),
            read_secret("user_password"),
            environ.get("HOST"),
            environ.get("DB_PORT"),
            environ.get("DB_NAME"),
        )
        app.ctx.resource_manager = ResourceManager(database_manager)

    return app
