from enum import Enum
import strawberry


@strawberry.enum(description="The place to put content relative to the image.")
class Direction(Enum):
    N = "N"
    S = "S"
    E = "E"
    O = "O"
