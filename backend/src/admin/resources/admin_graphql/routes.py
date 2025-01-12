from __future__ import annotations
from typing import TYPE_CHECKING
from sanic import Blueprint
from strawberry.sanic.views import GraphQLView
from sanic.request import File
from strawberry.file_uploads import Upload
from admin.resources.admin_graphql import Query, Mutation
from strawberry import Schema
from admin.auth.decorators import login_required
from strawberry.http.temporal_response import TemporalResponse
from os import environ

if TYPE_CHECKING:
    from admin.utilities.types import AdminRequest, GraphQLContext


class AuthGraphQLView(GraphQLView):
    decorators = (
        [login_required] if environ.get("BUILD_TARGET", "dev") != "dev" else None
    )

    async def get_context(
        self, request: AdminRequest, response: TemporalResponse
    ) -> GraphQLContext:
        return {
            "request": request,
            "response": response,
            "resource_manager": request.app.ctx.resource_manager,
        }


graphql_blueprint = Blueprint("graphql", url_prefix="/graphql")


graphql_blueprint.add_route(
    AuthGraphQLView.as_view(
        schema=Schema(query=Query, mutation=Mutation),
        graphql_ide="graphiql",
        multipart_uploads_enabled=True,
    ),
    "/",
)
