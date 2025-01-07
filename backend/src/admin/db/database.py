from os import environ
from common.database import DatabaseManager


class AdminDatabaseManager(DatabaseManager):
    def __init__(self, username, password, host, db_port, db_name):
        super().__init__(username, password, host, db_port, db_name)
