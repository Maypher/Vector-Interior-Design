import strawberry


@strawberry.type(description="Represents an error by the user in a given field")
class FieldError:
    path: str
    message: str
