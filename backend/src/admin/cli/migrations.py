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

    subparser = parser.add_subparsers(dest="command", required=True)

    new_parser = subparser.add_parser(
        "new", help="Creates a new migration and rollback files."
    )
    new_parser.add_argument(
        "name", type=str, nargs=1, help="The name of the migration to create."
    )

    migrate_parser = subparser.add_parser(
        "migrate",
        help="Migrates to the given version or latest if no version was specified.",
    )
    migrate_parser.add_argument(
        "version", nargs="?", type=int, help="The version to migrate to."
    )

    rollback_parser = subparser.add_parser(
        "rollback", help="Rollback to the given version (Stops at version + 1)."
    )
    rollback_parser.add_argument(
        "version", nargs=1, type=int, help="The version to rollback to."
    )

    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        nargs=1,
        help="The directory where the migrations are stored.",
        default="../migrations/",
    )

    args = parser.parse_args()
    command: str = args.command

    if command == "new":
        name = args.name[0]
        file_manager = MigrationFileManager(migration_folder=args.directory)
        file_manager.new_migration(name)
    else:
        try:
            migration_database_handler = DatabaseManager(
                environ.get("USERNAME"),
                read_secret("admin_password"),
                environ.get("HOST"),
                environ.get("DB_PORT"),
                environ.get("DB_NAME"),
            )

            migration_manager = MigrationManager(
                migration_database_handler, migration_folder=args.directory
            )
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
