from enum import Enum
import strawberry


@strawberry.enum(description="The place to put content relative to the image.")
class Location(Enum):
    N = "N"
    S = "S"
    E = "E"
    W = "W"


@strawberry.enum(description="The posible alignments for an image in mobile.")
class Alignment(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    CENTER = "CENTER"
    OVERFLOW = "OVERFLOW"


@strawberry.enum(description="The position of the image in the main page of desktop.")
class DesktopImagePosition(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    CENTER = "CENTER"


@strawberry.enum(
    description="The position of the image when in a group in a project's page in desktop."
)
class ImageGroupAlignment(Enum):
    TOP = "TOP"
    MIDDLE = "MIDDLE"
    BOTTOM = "BOTTOM"
