from db.database import DatabaseManager
from os import listdir, path
from io import TextIOWrapper
import re
from psycopg import errors
from typing import Tuple

"""
Used to create and apply migrations.
Created migrations are given the name [unix time]_[name]_[migration#]_[up|down].sql
"""


class MigrationManager:
    """
    Handles all migrations for a database.

    :param database_manager: The database manager that should execute the migrations.
    Should have CREATE SCHEMA, CREATE TABLE, INSERT, UPDATE and any other privileges required by the migration files.

    :param migration_folder: Where to find the migration SQL files.
    :param migration_filename_regex: The regex that should be used to read the SQL files from the migration folder. Don't include '.sql' in the query.
    :param migration_version_regex: The regex to get the version of a migration from its filename. Should only include one digit regex since it will take the first digit it finds.
    :param up_regex: Regex to determine if a migration is up.
    :param down_regex: Regex to determine if a migration is down.
    """

    database_manager: DatabaseManager
    migration_folder: str
    migration_filename_regex: re.Pattern
    migration_version_regex: re.Pattern
    up_regex: re.Pattern
    down_regex: re.Pattern
    migration_version_regex: re.Pattern
    migration_schema: str = "migrations"
    migration_table: str = "migration"

    def __init__(
        self,
        database_manager: DatabaseManager,
        migration_folder: str,
        migration_filename_regex: str = r"^(\d+)_(\w+)_(\d+)_(up|down).sql",
        migration_version_regex: str = r".*?_(\d+)_(up|down).sql",
        up_regex: str = r"_up.sql",
        down_regex: str = r"_down.sql",
    ):
        migration_regex_ends_in_sql = migration_filename_regex.endswith(".sql")

        self.migration_folder = migration_folder
        self.database_manager = database_manager
        self.migration_filename_regex = re.compile(
            f"{migration_filename_regex}{".sql" if not migration_regex_ends_in_sql else ""}"
        )
        self.migration_version_regex = re.compile(migration_version_regex)
        self.up_regex = re.compile(up_regex)
        self.down_regex = re.compile(down_regex)

        try:
            self.check_migrations_existence()
            self.create_migration_table()
        except FileNotFoundError as e:
            print(e)
            raise e
        except errors.InsufficientPrivilege as e:
            print(
                """Unable to initialize migration manager due to insufficient permissions. 
            Required permissions are CREATE SCHEMA, CREATE TABLE, INSERT and UPDATE."""
            )
            raise e

    def create_migration_table(self):
        # Creates a migration table if it doesn't exist
        self.database_manager.query(
            f"""
            DO $$
            BEGIN
                CREATE SCHEMA IF NOT EXISTS {self.migration_schema};

                -- Create the table if it doesn't exist and insert entry.
                -- Not using CREATE IF NOT EXISTS because it should insert a migration entry on creation as to not have duplicate migration versions.
                IF NOT EXISTS (
                    SELECT 1 
                    FROM information_schema.tables 
                    WHERE table_schema = '{self.migration_schema}' AND table_name = '{self.migration_table}'
                ) THEN
                    -- Create the table
                    CREATE TABLE {self.migration_schema}.{self.migration_table} (
                        id SERIAL PRIMARY KEY,
                        version INTEGER NOT NULL DEFAULT 0
                    );

                    -- Insert the default row
                    INSERT INTO {self.migration_schema}.{self.migration_table} (version) VALUES (0);
                END IF;
            END;
            $$;
        """
        )

    def check_migrations_existence(self):
        """
        Checks that every up migration has a down migration. Raises FileNotFoundError if there are up or down migrations missing.
        Should be called before apply_migrations.
        """
        missing_down_files: list[str] = []
        missing_version_files: list[str] = []
        current_version_found = 0

        # Validates integrity of all files so that other methods don't have to.
        # Checks that every up file has a sequential order. Ex: 1, 2, 3, 4
        for file in self.yield_sql_files():
            with file:
                version = self.get_migration_file_version(path.basename(file.name))
                if version > current_version_found + 1:
                    missing_version_files.append(path.basename(file.name))

                current_version_found += 1

        if missing_version_files:
            raise FileNotFoundError(
                f"Unable to find the following up migrations: {missing_version_files}"
            )

        # Checks that every up file has a respective down file.
        for file in self.yield_sql_files(down=True):
            version = re.match(self.up_regex, path.basename(file.name))
            if version != current_version_found:
                missing_version_files.append(path.basename(file.name))

            current_version_found -= 1

        if missing_down_files:
            raise FileNotFoundError(
                f"Unable to find the down migration for {missing_down_files}."
            )

    def get_migration_file_version(self, filename: str) -> int | None:
        """Gets the number of the migration from the filename or None if not found."""
        for match in re.search(self.migration_version_regex, filename).groups():
            if match.isdigit():
                return int(match)

    def get_latest_migration_version(self) -> int:
        """
        Gets the latest migration value from the migrations directory using the version regex.
        """
        maxVersion = 0

        for file in self.yield_sql_files(self.migration_folder):
            with file:
                filename: str = path.basename(file)
                version = self.get_migration_file_version(filename)

                if version:
                    maxVersion = max(version, maxVersion)

        return maxVersion

    def get_migration_version(self):
        """Gets the migration version from the database."""
        result = self.database_manager.query(
            f"""
        SELECT version FROM {self.migration_schema}.{self.migration_table};
        """,
            count=1,
        )[0]

        return int(result)

    def yield_sql_files(self, down: bool = False):
        """Yields all migration files that follow the string format. Returns all down files if down, otherwise all up files."""

        up_files: list[Tuple[int, TextIOWrapper]] = []
        down_files: list[Tuple[int, TextIOWrapper]] = []

        for file in listdir(self.migration_folder):
            migration_file = f"{self.migration_folder}/{file}"

            if not down and re.search(self.up_regex, file):
                file_version = self.get_migration_file_version(file)
                up_files.append((file_version, open(migration_file, "r")))
            elif re.search(self.down_regex, file):
                file_version = self.get_migration_file_version(file)
                down_files.append((file_version, open(migration_file, "r")))

        if not down:
            up_files.sort(key=lambda x: x[0])
            for _, file in up_files:
                yield file
                file.close()
        else:
            down_files.sort(key=lambda x: x[0], reverse=True)
            for _, file in down_files:
                yield file
                file.close()

    def apply_migration(self, migration: str, rollback=False):
        """
        Applies the given migration. Doesn't commit since that should happen only if there were no issues applying all migrations.
        """

        # Execute the migration
        self.database_manager.query(migration, commit=False)

        # Update the migration version
        self.database_manager.query(
            f"""
        UPDATE {self.migration_schema}.{self.migration_table}
        SET version = version {"-" if rollback else "+"} 1
        WHERE id = 1;
        """,
            commit=False,
        )

    def apply_migrations(self, final: int = -1):
        """Applies all migrations inside the migrations directory. Up to migration final. Leave at -1 to apply all"""
        db_version: int = self.get_migration_version()
        version_to_apply = db_version + 1
        # List of applied migrations used to log the final message
        applied_migrations = 0

        for index, migration in enumerate(self.yield_sql_files()):
            with migration:
                filename: str = path.basename(migration.name)
                migration_version: int = self.get_migration_file_version(filename)

                # Stop at the given migration. Final + 1 because the final migration should be applied.
                if index + 1 == final + 1:
                    break
                elif migration_version <= db_version:
                    # Skip already applied migrations
                    continue

                # If there's a migration missing roll back
                if migration_version > version_to_apply + 1:
                    print(f"Migration #{version_to_apply + 1} missing. Rolling back...")
                    self.database_manager.rollback()
                    return

                # Uses try except even though apply_migration doesn't raise an error since the sql file itself could be malformed
                try:
                    self.apply_migration(migration.read())
                    applied_migrations = migration_version
                except errors.ProgrammingError as e:
                    print(
                        f"Unable to apply migration {index + 1} due to a syntax error: \n{e}"
                    )
                    print(f"Rolling back all migrations...")
                    self.database_manager.rollback()
                    return
                except errors.InsufficientPrivilege as e:
                    print(
                        f"""
                        Unable to apply migration {index + 1} due to insufficient privileges: \n{e}"
                    """
                    )
                    self.database_manager.rollback()
                    return

        if applied_migrations:
            self.database_manager.commit()
            new_db_version = self.get_migration_version()
            print(
                f"Successfully applied migrations. Went from version {db_version} to {new_db_version}."
            )

    def rollback_migrations(self, final: int = -1):
        """Rolls back all migrations up to final. Leave as is to rollback everything."""

        db_version = self.get_migration_version()

        rollback_to = db_version

        for index, rollback in enumerate(self.yield_sql_files(down=True)):
            filename: str = path.basename(rollback.name)
            migration_version: int = self.get_migration_file_version(filename)

            rollback_to_apply = db_version - index

            # Stop the rollbacks at the given final or when end is reached.
            if rollback_to_apply <= 0 or rollback == final - 1:
                break
            # Skip rollbacks of unapplied migrations
            elif rollback > db_version:
                continue

            try:
                self.apply_migration(rollback.read(), rollback=True)
                rollback_to = rollback_to_apply
            except errors.ProgrammingError as e:
                print(f"Unable to run rollback {filename} due to malformed SQL.")
                self.database_manager.rollback()
                return
            except errors.InsufficientPrivilege as e:
                print(
                    f"""
                        Unable to apply rollback {migration_version} due to insufficient privileges: \n{e}"
                    """
                )
                self.database_manager.rollback()
                return

        if rollback_to:
            self.database_manager.commit()
            new_db_version = self.get_migration_version()
            print(
                f"Rollback successful. Went from version {db_version} to {new_db_version}."
            )
