import strawberry
import typing
from common.common_graphql import enums


@strawberry.input(description="Determines what borders a resource should have.")
class BordersInput:
    n: typing.Optional[bool] = strawberry.field(
        description="Determines if the resource should have a border on the top."
    )
    s: typing.Optional[bool] = strawberry.field(
        description="Determines if the resource should have a border on the bottom."
    )
    e: typing.Optional[bool] = strawberry.field(
        description="Determines if the resource should have a border on left."
    )
    o: typing.Optional[bool] = strawberry.field(
        description="Determines if the resource should have a border on right."
    )


@strawberry.input(description="The display configuration for an image in phones.")
class phoneConfigInput:
    borders: typing.Optional[BordersInput] = strawberry.field(
        description="Indicates what borders the image should have.", default=None
    )
    alignment: typing.Optional[enums.Alignment] = strawberry.field(
        description="The alignment of the image.", default=None
    )
    descriptionPos: typing.Optional[enums.Direction] = strawberry.field(
        description="The position of the description relative to the image.",
        default=None,
    )
