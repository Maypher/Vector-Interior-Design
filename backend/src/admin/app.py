from flask import Flask, jsonify
from os import environ
from admin.db.migrations import MigrationManager
from admin.auth.routes import auth_blueprint
from admin.resources import obra_admin_routes, image_admin_routes, ambiente_admin_routes
from psycopg import errors
from sys import argv
from admin.db.database import admin_database
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY")
CORS(
    app,
    supports_credentials=True,
    origins=[environ.get("FRONTEND_URL"), "https://192.168.0.8:5173"],
)
app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,  # Required for "None", set to False if not using HTTPS
)

app.register_blueprint(auth_blueprint)
app.register_blueprint(obra_admin_routes)
app.register_blueprint(ambiente_admin_routes)
app.register_blueprint(image_admin_routes)


def apply_migrations(command: str | None = None, migrate_to: int | None = None):
    try:
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
            if migrate_to:
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
    except (errors.InsufficientPrivilege, errors.ProgrammingError):
        exit(-1)


if __name__ == "__main__":
    try:
        migrate_or_rollback = argv[1]
    except IndexError:
        migrate_or_rollback = "migrate"
    try:
        migrate_to = argv[2]
    except IndexError:
        migrate_to = None

    if migrate_or_rollback not in ("migrate", "rollback"):
        print("Invalid arguments. Should be 'migrate' or 'rollback'.")
        exit(1)

    if migrate_to is not None:
        try:
            migrate_to = int(migrate_to)
        except ValueError:
            print("migrate or rollback needs either a numeric value or nothing.")
            exit(1)

    apply_migrations(migrate_or_rollback, migrate_to)

    app.run(port=environ.get("PORT"), host="0.0.0.0", debug=True)
