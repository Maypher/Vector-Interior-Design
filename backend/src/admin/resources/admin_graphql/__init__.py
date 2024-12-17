import typing
import strawberry
import strawberry.file_uploads
from strawberry.flask.views import GraphQLView
from auth.authentication import login_required
from common.common_graphql import schemas
from common import obra
from admin.resources import obra as adminObra
from admin.resources.admin_graphql import errors


class AuthGraphQLView(GraphQLView):
    @login_required
    def dispatch_request(self):
        return super().dispatch_request()


@strawberry.type
class Query:
    @strawberry.field(
        description="Returns all the obras ordered by index limited by page_size. Can be filtered by name."
    )
    def obras(
        self, page: int = 1, page_size: int = 10, name: typing.Optional[str] = None
    ) -> schemas.ObraResult:
        if name:
            return obra.get_obras_by_name(name, page, page_size, True)

        return obra.get_obras(page, page_size, True)

    @strawberry.field(description="Returns the obra matching the given ID or None.")
    def obra(self, id: int) -> typing.Optional[schemas.Obra]:
        return obra.get_obra_by_id(id, allow_private=True)

    @strawberry.field(description="Returns the ambiente matching the given ID or None.")
    def ambiente(self, id: int) -> typing.Optional[schemas.Ambiente]:
        return obra.get_ambiente_by_id(id, False)

    @strawberry.field(
        description="Returns the image matching the given filename or None."
    )
    def image(self, filename: str) -> typing.Optional[schemas.Image]:
        return obra.get_image_by_filename(filename)


@strawberry.type
class Mutation:
    @strawberry.mutation(description="Creates a new obra.")
    def createObra(self, name: str, description: str, area: int) -> schemas.Obra:
        return adminObra.create_obra(name, description, area)

    @strawberry.mutation(
        description="Deletes a given obra returning the deleted data. If None it means the obra wasn't found."
    )
    def deleteObra(self, id: int) -> typing.Optional[schemas.Obra]:
        return adminObra.delete_obra(id)

    @strawberry.mutation(
        description="Updates the obra identified by ID with the given parameters. All are optional, leave blank to not update."
    )
    def updateObra(
        self,
        id: int,
        name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        area: typing.Optional[int] = None,
        thumbnail: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        public: typing.Optional[bool] = None,
    ) -> typing.Optional[schemas.Obra]:
        return adminObra.update_obra(
            id, name, description, area, thumbnail, index, public
        )

    @strawberry.mutation(description="Creates a new ambiente.")
    def createAmbiente(
        self, obra_id: int, name: str, description: typing.Optional[str] = None
    ) -> typing.Union[schemas.Ambiente, errors.ObraNotFoundAmbiente]:
        return adminObra.create_ambiente(obra_id, name, description)

    @strawberry.mutation(
        description="Updates the ambiente identified by id with the given parameters. All are optional. Returns the updated data or None if no ambiente was found."
    )
    def updateAmbiente(
        id: int,
        name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
    ) -> typing.Optional[schemas.Ambiente]:
        return adminObra.update_ambiente(id, name, description, index)

    @strawberry.mutation(
        description="Deletes a given ambiente returning the deleted data. If None it means the ambiente wasn't found."
    )
    def deleteAmbiente(self, id: int) -> typing.Optional[schemas.Ambiente]:
        return adminObra.delete_ambiente(id)

    @strawberry.mutation(
        description="Creates a a new image for the given ambiente. Returns an error if the ambiente wasn't found or the filetype isn't supported."
    )
    def createImage(
        self, ambiente_id: int, image: strawberry.file_uploads.Upload, alt_text: str
    ) -> typing.Union[
        schemas.Image, errors.AmbienteNotFoundImage, errors.UnsupportedFileType
    ]:
        return adminObra.create_image(image, alt_text, ambiente_id)

    @strawberry.mutation(
        description="Updates the image identified by filename. All parameters are optional. Returns the updated image or None if no image was found."
    )
    def updateImage(
        self,
        filename: str,
        alt_text: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
    ) -> typing.Optional[schemas.Image]:
        return adminObra.update_image(filename, alt_text, index)

    @strawberry.mutation(
        description="Deletes the image identified by filename returning the deleted entry. Returns None if no image was found."
    )
    def deleteImage(self, filename: str) -> typing.Optional[schemas.Image]:
        return adminObra.delete_image(filename)
