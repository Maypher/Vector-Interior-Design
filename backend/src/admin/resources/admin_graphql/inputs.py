import strawberry
import typing
from common.common_graphql import enums


@strawberry.input(description="Determines what borders a resource should have.")
class BordersInput:
    n: bool = strawberry.field(
        description="Determines if the resource should have a border on the top."
    )
    s: bool = strawberry.field(
        description="Determines if the resource should have a border on the bottom."
    )
    e: bool = strawberry.field(
        description="Determines if the resource should have a border on left."
    )
    w: bool = strawberry.field(
        description="Determines if the resource should have a border on right."
    )

    def to_bits(self) -> str:
        """Returns the borders as a bit string to be inserted into the database"""
        bit_string = "".join("1" if b else "0" for b in (vars(self).values()))

        # Transform it into binary and then a string because if only binary
        # postgres treats it as a smallint and it fails
        borders = bin(int(bit_string, 2))
        borders = f"{bit_string}"

        return borders


@strawberry.input(description="The display configuration for an image in phones.")
class phoneConfigInput:
    borders: typing.Optional[BordersInput] = strawberry.field(
        description="Indicates what borders the image should have.", default=None
    )
    alignment: typing.Optional[enums.Alignment] = strawberry.field(
        description="The alignment of the image.", default=None
    )
    description_pos: typing.Optional[enums.Location] = strawberry.field(
        description="The position of the description relative to the image.",
        default=None,
    )
    description_alignment: typing.Optional[str] = strawberry.field(
        description="The alignment of the description."
    )


@strawberry.input(
    description="The configuration of how an image will be shown in the main page of mobile devices."
)
class MainPageImagePhoneConfigInput:
    image_borders: typing.Annotated[
        typing.Optional[BordersInput],
        strawberry.argument("What borders should the image have"),
    ] = None
    description_position: typing.Annotated[
        typing.Optional[enums.Location],
        strawberry.argument(
            description="The position of where to put the description relative to the image."
        ),
    ] = strawberry.UNSET
    logo_position: typing.Annotated[
        typing.Optional[enums.Location],
        strawberry.argument(
            description="The position of where to put the logo relative to the image."
        ),
    ] = strawberry.UNSET
    logo_borders: typing.Annotated[
        typing.Optional[BordersInput],
        strawberry.argument("What borders should the logo have"),
    ] = None
    overflow: typing.Annotated[
        typing.Optional[bool],
        strawberry.argument(
            description="Determines if the image should overflow to the edge of the screen or not."
        ),
    ] = (strawberry.UNSET,)
