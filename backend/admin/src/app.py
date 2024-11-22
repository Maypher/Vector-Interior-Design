from flask import Flask, jsonify
from os import environ
from db.migrations import MigrationManager
from db.database import DatabaseManager
from auth.routes import auth_blueprint
from resources.routes import obra_routes
from psycopg import errors
from sys import argv

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY")

app.register_blueprint(auth_blueprint)
app.register_blueprint(obra_routes)


@app.route("/")
def hello_world():
    return jsonify({"msg": "Hello"})


def apply_migrations(command: str | None = None, migrate_to: int | None = None):
    try:
        # TODO Create testing credentials in database and rollback functionality
        migration_database_manager = DatabaseManager()
        migration_manager = MigrationManager(migration_database_manager, "./migrations")
    except errors.InsufficientPrivilege:
        exit(1)

    if command not in ("migrate", "rollback"):
        print("Invalid command. Must be one of 'migrate' or 'rollback'.")
        exit(1)

    try:
        if command == "migrate":
            if migrate_to:
                migration_manager.apply_migrations(migrate_to)
            else:
                migration_manager.apply_migrations()
    except (errors.InsufficientPrivilege, errors.ProgrammingError):
        exit(-1)


if __name__ == "__main__":
    migrate_or_rollback = argv[1]
    migrate_to = argv[2]

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
