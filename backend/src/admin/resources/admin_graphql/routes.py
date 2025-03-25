from __future__ import annotations
from typing import TYPE_CHECKING
from sanic import Blueprint
from strawberry.sanic.views import GraphQLView
from admin.resources.admin_graphql import Query, Mutation
from strawberry import Schema
from admin.auth.decorators import login_required
from strawberry.http.temporal_response import TemporalResponse
from common.utilities.environment import dev_mode

if TYPE_CHECKING:
    from admin.utilities.types import AdminRequest, GraphQLContext


class AuthGraphQLView(GraphQLView):
    decorators = [login_required] if not dev_mode else None

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
        graphql_ide="graphiql" if dev_mode else None,
        multipart_uploads_enabled=True,
    ),
    "/",
)
