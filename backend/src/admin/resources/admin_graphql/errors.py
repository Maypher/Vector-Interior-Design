import strawberry


@strawberry.type(
    description="An error indicating that the given project doesn't exist when creating an space."
)
class ProjectNotFoundSpace:
    project_id: int = strawberry.field(description="The project ID given by the user.")


@strawberry.type(
    description="An error indicating an uploaded image isn't the correct file type."
)
class UnsupportedFileType:
    filetype: str = strawberry.field(description="The type of the uploaded file.")


@strawberry.type(
    description="An error indicating that the given space wasn't found when creating an image."
)
class SpaceNotFoundImage:
    space_id: int = strawberry.field(description="The given non-existent space ID.")
