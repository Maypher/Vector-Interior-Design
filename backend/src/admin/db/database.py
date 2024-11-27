from os import environ
from common.database import DatabaseManager

admin_database = DatabaseManager(
    environ.get("USERNAME"),
    environ.get("PASSWORD"),
    environ.get("HOST"),
    environ.get("DB_PORT"),
    environ.get("DB_NAME"),
)
