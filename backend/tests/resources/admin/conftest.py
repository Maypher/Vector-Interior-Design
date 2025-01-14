from strawberry import Schema
from admin.resources.admin_graphql import Query, Mutation
from admin.app import create_app
import pytest
from sanic_testing.testing import SanicASGITestClient
from admin.db.database import DatabaseManager
from mimesis import Field, ImageFile
from sanic.request import File


@pytest.fixture(scope="class")
def admin_schema() -> Schema:
    return Schema(query=Query, mutation=Mutation)


@pytest.fixture(scope="class")
def test_client(database_manager: DatabaseManager) -> SanicASGITestClient:
    app = create_app(database_manager=database_manager)
    test_client = SanicASGITestClient(app)

    return test_client


@pytest.fixture(scope="function")
def image(mimesis: Field) -> File:
    image_name = mimesis("word")
    image_extension = mimesis("choice", items=[ImageFile.PNG, ImageFile.JPG])
    image_filename = f"{image_name}.{image_extension.value}"
    image_body = mimesis("image", file_type=image_extension)

    return File(
        name=image_filename,
        type=f"image/{image_extension.value}",
        body=image_body,
    )
