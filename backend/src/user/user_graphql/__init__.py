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
        description="Returns all the obras ordered by index limited by page_size. Can be filtered by name."
    )
    def obras(
        self,
        info: ResourceInfo,
        page: typing.Annotated[
            int, strawberry.argument(description="The page to get.")
        ] = 1,
        page_size: typing.Annotated[
            int, strawberry.argument(description="The size of each page.")
        ] = 10,
        name: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(description="Filter obras by name."),
        ] = None,
    ) -> schemas.ObraResult:
        resource_manager = info.context["resource_manager"]
        if name:
            return resource_manager.get_obras_by_name(name, page, page_size)

        return resource_manager.get_obras(page, page_size)

    @strawberry.field(description="Returns the obra matching the given ID or null.")
    def obra(
        self,
        info: ResourceInfo,
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of the obra to get.")
        ],
    ) -> typing.Optional[schemas.Obra]:
        return info.context["resource_manager"].get_obra_by_id(id)

    @strawberry.field(description="Returns the ambiente matching the given ID or null.")
    def ambiente(
        self,
        info: ResourceInfo,
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of ambiente to get.")
        ],
    ) -> typing.Optional[schemas.Ambiente]:
        return info.context["resource_manager"].get_ambiente_by_id(id)

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
        image_filenames = resource_manager.database_manager.query(
            """
            SELECT archivo from imagen JOIN imagenConfig on imagenConfig.imagen_id = imagen.id 
            WHERE imagen.pagina_principal ORDER BY imagenConfig.indice;
            """
        )

        return [
            resource_manager.get_image_by_filename(filename[0])
            for filename in image_filenames
        ]
