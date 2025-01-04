from admin.db.migrations import MigrationManager
from psycopg import errors
from common.database import DatabaseManager
from os import environ
import argparse


def apply_migrations(command: str | None = None, migrate_to: int | None = None):
    try:
        admin_database = DatabaseManager(
            environ.get("USERNAME"),
            environ.get("PASSWORD"),
            environ.get("HOST"),
            environ.get("DB_PORT"),
            environ.get("DB_NAME"),
        )

        migration_manager = MigrationManager(admin_database, "./migrations/")
    except errors.InsufficientPrivilege:
        print("Unable to initialize migration system due to insufficient privileges.")
        exit(1)

    if command not in ("migrate", "rollback"):
        print("Invalid command. Must be one of 'migrate' or 'rollback'.")
        exit(1)

    try:
        if command == "migrate":
            print("applying migrations")
            if migrate_to is not None:
                migration_manager.apply_migrations(migrate_to)
                print(f"Applied migrations up to version {migrate_to}")
            else:
                migration_manager.apply_migrations()
                print("Applied all migrations")
        elif command == "rollback":
            print("Rolling back...")
            if migrate_to:
                migration_manager.rollback_migrations(final=migrate_to)
                print(f"Rolled back migrations up to version {migrate_to}")
            else:
                migration_manager.rollback_migrations()
                print(f"Rolled back all migrations")
    except (errors.InsufficientPrivilege, errors.ProgrammingError) as e:
        print(e)
        exit(-1)


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

    args = parser.parse_args()

    try:
        migration_database_handler = DatabaseManager(
            environ.get("USERNAME"),
            environ.get("PASSWORD"),
            environ.get("HOST"),
            environ.get("DB_PORT"),
            environ.get("DB_NAME"),
        )

        migration_manager = MigrationManager(
            migration_database_handler, "./migrations/"
        )
    except errors.InsufficientPrivilege:
        print("Unable to initialize migration system due to insufficient privileges.")
        exit(1)

    if args.command in ("migrate", "rollback"):
        if args.version is not None:
            apply_migrations(args.command, args.version)
        else:
            apply_migrations(args.command)
    else:
        if args.name is not None:
            migration_manager.create_migration(args.name)
            print("Migration and rollback created successfully.")
        else:
            print("When creating a new migration, you must provide a name.")
            exit(1)
