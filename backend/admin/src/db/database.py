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


def query(
    query: str, params: Tuple | None = None, count: int = -1, commit: bool = True
):
    """
    Executes a query on the database with the given params and returns the results. Commits changes if any.
    Raises and error if the query fails to be executed. If count = -1 return all, otherwise return the given count.
    Commit determines if queries should be automatically committed after execution.
    """
    with database.cursor() as cur:
        query_result = cur.execute(query, params)
        res = None

        # Check for description because if a query doesn't return anything then fetch*() panics
        if cur.description:
            if count == -1:
                res = query_result.fetchall()
            elif count == 1:
                res = query_result.fetchone()
            else:
                res = query_result.fetchmany(count)

    if commit:
        database.commit()
    return res


def commit():
    """Force commit all pending changes."""
    database.commit()


def rollback():
    """Forcefully rollback any pending commits."""
    database.rollback()
