from admin.db.migrations import MigrationManager, MigrationFileManager
from psycopg import errors
from common.database import DatabaseManager
from common.utils import read_secret
from os import environ
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Utility file to create and handle migrations."
    )

    parser.add_argument(
        "command", choices=("migrate", "rollback", "new"), help="The command to run."
    )

    parser.add_argument(
        "-n", "--name", type=str, nargs=1, help="The name of the migration to create."
    )

    parser.add_argument(
        "-v",
        "--version",
        type=int,
        nargs=1,
        help="Migrates or rollbacks to the specified version. On migrate it applies all migrations up to the specified version, including it. On rollback it rolls back migrations up to the specified version but doesn't apply it.",
    )

    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        nargs=1,
        help="The directory where the migrations are stored.",
        default="./migrations/",
    )

    args = parser.parse_args()
    command: str = args.command

    if command == "new":
        name = args.name

        if not name:
            print("A new needs to be provided for the new migration.")
            exit(1)

        file_manager = MigrationFileManager()

        file_manager.new_migration(name[0])
    else:
        try:
            migration_database_handler = DatabaseManager(
                environ.get("USERNAME"),
                read_secret("admin_password"),
                environ.get("HOST"),
                environ.get("DB_PORT"),
                environ.get("DB_NAME"),
            )

            migration_manager = MigrationManager(migration_database_handler)
        except errors.InsufficientPrivilege:
            print(
                "Unable to initialize migration system due to insufficient privileges."
            )
            exit(1)

        if command == "rollback":
            if args.version is not None:
                migration_manager.rollback_migrations(args.version[0])

            else:
                print("Rollback requires a version to be specified.")
        else:
            if args.version is not None:
                migration_manager.apply_migrations(args.version[0])

            else:
                migration_manager.apply_migrations()
