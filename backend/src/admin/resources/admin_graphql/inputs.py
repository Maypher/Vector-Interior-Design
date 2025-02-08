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
class PhoneConfigInput:
    borders: typing.Optional[BordersInput] = strawberry.field(
        description="Indicates what borders the image should have."
    )
    alignment: typing.Optional[enums.Alignment] = strawberry.field(
        description="The alignment of the image."
    )
    description_pos: typing.Optional[enums.Location] = strawberry.field(
        description="The position of the description relative to the image.",
        default=strawberry.UNSET,
    )
    description_alignment: typing.Optional[str] = strawberry.field(
        description="The alignment of the description."
    )


@strawberry.input(description="The display configuration for an image in phones.")
class DesktopConfigInput:
    group_alignment: typing.Optional[enums.ImageGroupAlignment] = strawberry.field(
        description="Indicates the vertical alignment of an image inside a group.",
        default=strawberry.UNSET,
    )
    group_end: typing.Optional[bool] = strawberry.field(
        description="Force a group to end. This is used if two consecutive groups are needed so they don't merge into one."
    )
    image_size: typing.Optional[int] = strawberry.field(
        description="The size of the image in a range 0-100."
    )
    image_borders: typing.Optional[BordersInput] = strawberry.field(
        description="What borders should the image have.",
    )
    description_position: typing.Optional[enums.Location] = strawberry.field(
        description="The position of the description relative to the image.",
        default=strawberry.UNSET,
    )
    description_alignment: typing.Optional[str] = strawberry.field(
        description="The alignment of the description text. **Should by any of tailwind's text-align variations.**"
    )
    description_borders: typing.Optional[BordersInput] = strawberry.field(
        description="What borders should the description have.",
    )
    description_logo_position: typing.Optional[enums.Location] = strawberry.field(
        description="The position of the logo relative to the description.",
        default=strawberry.UNSET,
    )
    logo_position: typing.Optional[enums.Location] = strawberry.field(
        description="The position of the logo relative to the image.",
        default=strawberry.UNSET,
    )
    logo_borders: typing.Optional[BordersInput] = strawberry.field(
        description="What borders should the logo have.",
    )


@strawberry.input(
    description="The configuration of how an image will be shown in the main page of mobile devices."
)
class MainPageImagePhoneConfigInput:
    image_borders: typing.Optional[BordersInput] = (
        strawberry.field(
            description="What borders should the image have", default=None
        ),
    )
    description_position: typing.Optional[enums.Location] = strawberry.field(
        description="The position of where to put the description relative to the image.",
        default=strawberry.UNSET,
    )
    logo_position: typing.Optional[enums.Location] = strawberry.field(
        description="The position of where to put the logo relative to the image.",
        default=strawberry.UNSET,
    )
    logo_borders: typing.Optional[BordersInput] = strawberry.field(
        description="The borders of the logo.", default=None
    )
    overflow: typing.Optional[bool] = strawberry.field(
        description="Determines if the image should overflow to the edge of the screen or not.",
        default=None,
    )


@strawberry.input(
    description="The configuration for an image that's shown in the main page of desktop devices."
)
class MainPageImageDesktopConfigInput:
    image_position: typing.Optional[enums.DesktopImagePosition] = strawberry.field(
        description="The position of the image in the screen.", default=None
    )
    description_position: typing.Optional[enums.Location] = strawberry.field(
        description="The position of the description relative to the image.",
        default=strawberry.UNSET,
    )
    description_borders: typing.Optional[BordersInput] = strawberry.field(
        description="The borders of the description.", default=None
    )
    logo_position: typing.Optional[enums.Location] = strawberry.field(
        description="The position of the logo relative to the image.",
        default=strawberry.UNSET,
    )
    logo_borders: typing.Optional[BordersInput] = strawberry.field(
        description="The borders of the logo.", default=None
    )
    description_logo_position: typing.Optional[enums.Location] = strawberry.field(
        description="The position of the logo relative to the description.",
        default=strawberry.UNSET,
    )
    description_logo_borders: typing.Optional[BordersInput] = strawberry.field(
        description="The borders of the description logo.", default=None
    )
    overflow: typing.Optional[bool] = strawberry.field(
        description="Determines if the image should overflow to the borders of the screen.",
        default=None,
    )
