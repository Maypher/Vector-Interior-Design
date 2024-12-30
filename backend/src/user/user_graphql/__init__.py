import strawberry
from common import obra
from common.common_graphql import schemas
from common.database import generic_database
import typing


@strawberry.type()
class Query:
    @strawberry.field(
        description="Returns all the obras ordered by index limited by page_size. Can be filtered by name."
    )
    def obras(
        self,
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
        if name:
            return obra.get_obras_by_name(name, page, page_size)

        return obra.get_obras(page, page_size)

    @strawberry.field(description="Returns the obra matching the given ID or null.")
    def obra(
        self,
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of the obra to get.")
        ],
    ) -> typing.Optional[schemas.Obra]:
        return obra.get_obra_by_id(id)

    @strawberry.field(description="Returns the ambiente matching the given ID or null.")
    def ambiente(
        self,
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of ambiente to get.")
        ],
    ) -> typing.Optional[schemas.Ambiente]:
        return obra.get_ambiente_by_id(id)

    @strawberry.field(
        description="Returns the image matching the given filename or null."
    )
    def image(
        self,
        filename: typing.Annotated[
            str, strawberry.argument(description="The filename of the image to get.")
        ],
    ) -> typing.Optional[schemas.Image]:
        return obra.get_image_by_filename(filename)

    @strawberry.field(description="All the images shown in the main page")
    def mainPageImages(self) -> typing.List[schemas.Image]:
        image_filenames = generic_database.query(
            """
            SELECT archivo from imagen JOIN imagenConfig on imagenConfig.imagen_id = imagen.id 
            WHERE imagen.pagina_principal ORDER BY imagenConfig.indice;
            """
        )

        return [obra.get_image_by_filename(filename[0]) for filename in image_filenames]
