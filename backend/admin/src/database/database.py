import psycopg
from os import environ
from typing import Tuple

username = environ.get("USERNAME")
password = environ.get("PASSWORD")
host = environ.get("HOST")
dbPort = environ.get("DB_PORT")
dbName = environ.get("DB_NAME")

connectionString = f"postgres://{username}:{password}@{host}:{dbPort}/{dbName}"

database = psycopg.connect(connectionString)


def query(query: str, params: Tuple):
    with database.cursor() as cur:
        return cur.execute(query, params).fetchall()
