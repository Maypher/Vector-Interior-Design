from common.database import DatabaseManager
from common.common_graphql import schemas
import typing
from sanic.log import logger
from psycopg.rows import class_row


class ResourceManager:
    database_manager: DatabaseManager
    allow_private: bool

    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager
        self.allow_private = False

    def get_project_by_id(self, id: int) -> typing.Optional[schemas.Project]:
        """Returns the project matching the given id or None."""
        return self.database_manager.query(
            f"""
        SELECT * FROM project
        WHERE id = %s {"AND public" if not self.allow_private else ""};
        """,
            (id,),
            count=1,
            row_factory=class_row(schemas.Project),
        )

    def get_projects(self) -> list[schemas.Project]:
        """Retrieves a list of all projects."""
        data = self.database_manager.query(
            f"""
            SELECT * FROM project {"WHERE public" if not self.allow_private else ""} 
            ORDER BY index;
        """,
        )

        return [schemas.Project(**project) for project in data]

    def get_projects_by_name(self, name: str) -> list[schemas.Project]:
        """Returns all the projects like a given name."""

        data = self.database_manager.query(
            f"""
            SELECT * FROM project
            WHERE name ILIKE %s {"AND public" if not self.allow_private else ""}
            ORDER BY index;
        """,
            (f"%{name}%",),
        )
        return [schemas.Project(**project) for project in data]

    def get_space_by_id(self, id: int) -> typing.Optional[schemas.Space]:
        """Returns the space matching the given id or None."""

        return self.database_manager.query(
            f"""
        SELECT space.*
        FROM space 
        {"JOIN project ON space.project_id = project.id" if not self.allow_private else ""}
        WHERE space.id = %s {"AND project.public" if not self.allow_private else ""};
        """,
            (id,),
            1,
            row_factory=class_row(schemas.Space),
        )

    def get_spaces_by_project(self, project_id: int) -> list[schemas.Space]:
        """Returns all ambientes for the given project_id."""

        # TODO: Check if this bypasses private constrains
        return self.database_manager.query(
            """
        SELECT * FROM space 
        WHERE project_id = %s ORDER BY index;
        """,
            (project_id,),
            row_factory=class_row(schemas.Space),
        )

    def get_image_by_filename(self, filename: str) -> typing.Optional[schemas.Image]:
        image = self.database_manager.query(
            f"""
            SELECT image.* FROM image 
            {"JOIN space ON image.space_id = space.id JOIN project ON space.project_id = project.id" if not self.allow_private else ""}
            WHERE filename = %s {"AND project.public" if not self.allow_private else ""};
            """,
            (filename,),
            count=1,
            row_factory=class_row(schemas.Image),
        )

        return image
