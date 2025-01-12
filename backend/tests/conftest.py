import pytest
from common import database
from admin.resources.resource_manager import AdminResourceManager
from admin.db.migrations import MigrationManager
from common.resource_manager import ResourceManager
import os


@pytest.fixture(scope="session")
def postgres_manager() -> database.DatabaseManager:
    """Connects to the default 'postgres' database."""
    return database.DatabaseManager(
        "postgres", os.environ.get("POSTGRES_PASSWORD"), "database", "5432", "postgres"
    )


@pytest.fixture(scope="session")
def database_manager(
    postgres_manager: database.DatabaseManager,
) -> database.DatabaseManager:
    """Creates the 'testing' database and returns a DatabaseManager connected to it."""
    # Enable autocommit to execute CREATE DATABASE
    postgres_manager.database_connection.autocommit = True

    # Create the 'testing' database if it doesn't exist
    postgres_manager.query("CREATE DATABASE testing;")

    db_manager = database.DatabaseManager(
        "postgres", os.environ.get("POSTGRES_PASSWORD"), "database", "5432", "testing"
    )

    db_manager.query("CREATE SCHEMA IF NOT EXISTS administration;")

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


@pytest.fixture(scope="class")
def admin_resource_manager(
    database_manager: database.DatabaseManager,
) -> AdminResourceManager:
    return AdminResourceManager(database_manager)


@pytest.fixture(scope="class")
def resource_manager(
    database_manager: database.DatabaseManager,
) -> ResourceManager:
    return ResourceManager(database_manager)
