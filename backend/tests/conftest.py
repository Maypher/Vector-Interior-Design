import pytest
import pytest_asyncio
from common import database
from admin.resources.resource_manager import AdminResourceManager
from admin.db.migrations import MigrationManager
from common.resource_manager import ResourceManager
import os
from mimesis import Field, ImageFile, Locale
from sanic.request import File
from typing import AsyncGenerator


@pytest.fixture(scope="session")
def postgres_manager() -> database.DatabaseManager:
    """Connects to the default 'postgres' database."""
    return database.DatabaseManager(
        "postgres",
        os.environ.get("POSTGRES_PASSWORD"),
        "database",
        "5432",
        "postgres",
        True,
    )


@pytest.fixture(scope="session")
def database_manager(
    postgres_manager: database.DatabaseManager,
) -> database.DatabaseManager:
    """Creates the 'testing' database and returns a DatabaseManager connected to it."""
    # Enable autocommit to execute CREATE DATABASE
    postgres_manager.database_connection.autocommit = True

    # Create the 'testing' database if it doesn't exist
    postgres_manager.database_connection.execute("CREATE DATABASE testing;")

    db_manager = database.DatabaseManager(
        "postgres", os.environ.get("POSTGRES_PASSWORD"), "database", "5432", "testing"
    )

    db_manager.database_connection.execute(
        "CREATE SCHEMA IF NOT EXISTS administration;"
    )

    postgres_manager.database_connection.autocommit = False

    # Return a DatabaseManager connected to 'testing'
    return db_manager


@pytest.fixture(autouse=True, scope="session")
def database_setup(
    postgres_manager: database.DatabaseManager,
    database_manager: database.DatabaseManager,
):
    """Sets up the 'testing' database before running tests."""
    migration_manager = MigrationManager(
        database_manager, migration_folder="../src/admin/migrations/"
    )

    migration_manager.apply_migrations()

    yield

    database_manager.database_connection.close()
    postgres_manager.database_connection.autocommit = True
    postgres_manager.database_connection.execute("DROP DATABASE testing;")


@pytest_asyncio.fixture(scope="class")
async def admin_resource_manager(
    request: pytest.FixtureRequest,
    database_manager: database.DatabaseManager,
) -> AsyncGenerator[AdminResourceManager]:
    resource_manager = AdminResourceManager(database_manager)
    mimesis = Field(Locale.ES)

    params: dict = request.param
    project_count = params.get("project_count", 100)
    space_count = params.get("space_count", 100)
    image_count = params.get("image_count", 100)

    for _ in range(project_count):
        resource_manager.create_project(
            mimesis("word"),
            mimesis("text"),
            mimesis("integer_number", start=100, end=1000),
        )

    for _ in range(space_count):
        # Select a random project to add this space to
        project_id = mimesis("integer_number", start=1, end=project_count)

        resource_manager.create_space(
            project_id,
            mimesis("word"),
            mimesis("choice", items=[None, mimesis("text")]),
        )

    for _ in range(image_count):
        # select a random space to add this image to
        space_id = mimesis("integer_number", start=1, end=space_count)

        image_name = mimesis("uuid")
        image_extension = mimesis("choice", items=[ImageFile.JPG, ImageFile.PNG])
        image_mimetype = f"image/{"jpg" if image_extension == ImageFile.JPG else "png"}"
        image_filename = (
            f"{image_name}.{"jpg" if image_extension == ImageFile.JPG else "png"}"
        )
        image_data = mimesis("image", file_type=image_extension)

        image_file = File(type=image_mimetype, name=image_filename, body=image_data)

        await resource_manager.create_image(image_file, mimesis("sentence"), space_id)

    yield resource_manager
    resource_manager.database_manager.rollback()


@pytest.fixture(scope="class")
def resource_manager(
    database_manager: database.DatabaseManager,
) -> ResourceManager:
    return ResourceManager(database_manager)
