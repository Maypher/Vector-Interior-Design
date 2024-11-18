from db.database import database
from os import listdir, path
import re
import time

"""
Used to create and apply migrations.
Created migrations are given the name [unix time]_[name]_[migration#]_[up|down].sql
"""


def createMigrationTable():
    # Creates a migration table if it doesn't exist
    database.execute(
        """
    CREATE TABLE IF NOT EXISTS administration.migration (
        id INTEGER PRIMARY KEY,
        version INTEGER NOT NULL DEFAULT 0
    );
    INSERT INTO administration.migration (id, version)
    SELECT 1, 0 WHERE NOT EXISTS (SELECT 1 FROM administration.migration); 
    """
    )

    database.commit()


def getMigrationFileVersion(filename: str):
    version = int(filename.split("_")[-2])
    return version


def getLatestMigrationFileVersion(migrationFolder: str = "./migrations"):
    maxVersion = 0

    for file in yieldSQLFiles(migrationFolder):
        with file:
            filename: str = path.basename(file)
            try:
                version = getMigrationFileVersion(filename)
                maxVersion = max(version, maxVersion)
            except (IndexError, ValueError):
                pass
    return maxVersion


def newMigration(name: str, path: str = "./migrations/"):
    migrationVersion = getLatestMigrationFileVersion() + 1
    filename = f"{round(time.time())}_{name}_{migrationVersion}"

    with open(f"{path}{filename}_up.sql", "w") as upFile:
        upFile.write("-- Write migration here.")
    with open(f"{path}{filename}_down.sql", "w") as downFile:
        downFile.write("-- Write migration rollback here.")


def getMigrationVersion():
    try:
        result = database.execute(
            """
        SELECT version FROM administration.migration;
        """
        ).fetchone()[0]
    except Exception as e:
        print(e)
    else:
        return int(result)


def yieldSQLFiles(directory: str = "./migrations", down: bool = False):
    for file in listdir(directory):
        if file.endswith(f"{"down" if down else "up"}.sql"):
            file = open(f"{directory }/{file}", "r")
            yield file


def apply_migration(migration: str):
    # Execute the migration
    database.execute(migration)

    # Update the migration version
    database.execute(
        """
    UPDATE administration.migration
    SET version = version + 1
    WHERE id = 1;
    """
    )


def apply_migrations(count: int = -1):
    createMigrationTable()
    dbVersion = getMigrationVersion()
    versionToApply = dbVersion + 1

    for index, migration in enumerate(yieldSQLFiles()):
        with migration:
            filename = path.basename(migration.name)
            migrationVersion = getMigrationFileVersion(filename)

            # Stop at the given migration
            if index + 1 == count:
                break
            elif migrationVersion <= dbVersion:
                # Skip already applied migrations
                continue

            # If there's a migration missing roll back
            if migrationVersion > versionToApply + 1:
                print(f"Migration #{versionToApply + 1} missing. Rolling back...")
                database.rollback()
                return

            try:
                apply_migration(migration.read())
                print(f"Applied migration {path.basename(migration.name)}")
            except Exception as e:
                print(f"Unable to apply migration {index + 1}: {e}")
                print(f"Rolling back all migrations...")
                database.rollback()
                return

    database.commit()
    print("Successfully applied all migrations...")
