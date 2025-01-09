from enum import Enum
import strawberry


@strawberry.enum(description="The place to put content relative to the image.")
class Location(Enum):
    N = "N"
    S = "S"
    E = "E"
    W = "W"


@strawberry.enum(description="The posible alignments for an image.")
class Alignment(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    CENTER = "CENTER"
    OVERFLOW = "OVERFLOW"
