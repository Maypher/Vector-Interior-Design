import strawberry
from common.common_graphql.errors import FieldError
import typing


@strawberry.type(
    description="An error indicating that the given obra doesn't exist when creating an ambiente."
)
class ObraNotFoundAmbiente:
    obra_id: int = strawberry.field(description="The obra ID given by the user.")


@strawberry.type(
    description="An error indicating an uploaded image isn't the correct file type."
)
class UnsupportedFileType:
    filetype: str = strawberry.field(description="The type of the uploaded file.")


@strawberry.type(
    description="An error indicating that the given ambiente wasn't found when creating an image."
)
class AmbienteNotFoundImage:
    ambiente_id: int = strawberry.field(
        description="The given non-existent ambiente ID."
    )
