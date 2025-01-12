from strawberry import Schema
from admin.resources.admin_graphql import Query, Mutation
from admin.app import create_app
import pytest
from sanic_testing.testing import SanicASGITestClient
from admin.db.database import DatabaseManager


@pytest.fixture(scope="class")
def admin_schema() -> Schema:
    return Schema(query=Query, mutation=Mutation)


@pytest.fixture(scope="class")
def test_client(database_manager: DatabaseManager) -> SanicASGITestClient:
    app = create_app(database_manager=database_manager)
    test_client = SanicASGITestClient(app)

    return test_client
