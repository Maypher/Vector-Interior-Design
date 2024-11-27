import pytest
from common import database
import os


@pytest.fixture(autouse=True, scope="session")
def database_setup():
    manager = database.DatabaseManager(
        "postgres", os.environ.get("POSTGRES_PASSWORD"), "database", "5432", "postgres"
    )

    manager.database_connection.autocommit = True

    manager.query(
        """
        CREATE DATABASE testing;
    """
    )

    manager.database_connection.autocommit = False

    yield

    manager.database_connection.autocommit = True

    manager.query(
        """
        DROP DATABASE testing;
    """
    )

    manager.database_connection.autocommit = False
