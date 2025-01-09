import strawberry
import strawberry.sanic
import strawberry.sanic.views
from common import obra
from common.common_graphql import schemas
from common.types import GraphQLContext, ResourceInfo

import typing
from user.utilities import types


class UserGraphQLView(strawberry.sanic.views.GraphQLView):
    async def get_context(self, request: types.UserRequest, response) -> GraphQLContext:
        return {
            "request": request,
            "response": response,
            "resource_manager": request.app.ctx.resource_manager,
        }


@strawberry.type()
class Query:
    @strawberry.field(
        description="Returns all the project ordered by index. Can be filtered by name."
    )
    def projects(
        self,
        info: ResourceInfo,
        name: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(description="Filter obras by name."),
        ] = None,
    ) -> list[schemas.Project]:
        resource_manager = info.context["resource_manager"]
        if name:
            return resource_manager.get_projects_by_name(name)

        return resource_manager.get_projects()

    @strawberry.field(description="Returns the project matching the given ID or null.")
    def project(
        self,
        info: ResourceInfo,
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of the obra to get.")
        ],
    ) -> typing.Optional[schemas.Project]:
        return info.context["resource_manager"].get_project_by_id(id)

    @strawberry.field(description="Returns the space matching the given ID or null.")
    def space(
        self,
        info: ResourceInfo,
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of ambiente to get.")
        ],
    ) -> typing.Optional[schemas.Space]:
        return info.context["resource_manager"].get_space_by_id(id)

    @strawberry.field(
        description="Returns the image matching the given filename or null."
    )
    def image(
        self,
        info: ResourceInfo,
        filename: typing.Annotated[
            str, strawberry.argument(description="The filename of the image to get.")
        ],
    ) -> typing.Optional[schemas.Image]:
        return info.context["resource_manager"].get_image_by_filename(filename)

    @strawberry.field(description="All the images shown in the main page")
    def mainPageImages(self, info: ResourceInfo) -> typing.List[schemas.Image]:
        resource_manager = info.context["resource_manager"]
        images_data = resource_manager.database_manager.query(
            """
            SELECT image.* FROM image JOIN main_page_config on main_page_config.image_id = image.id
            JOIN space on image.space_id = space.id JOIN project ON space.project_id = project.id
            WHERE image.main_page AND project.public ORDER BY main_page_config.index;
            """
        )

        return [schemas.Image(**image) for image in images_data]
