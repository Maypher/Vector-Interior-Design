import psycopg
from os import environ
from typing import Tuple


class DatabaseManager:
    database_connection: psycopg.Connection

    def __init__(
        self, username: str, password: str, host: str, db_port: str, db_name: str
    ):
        connection_string = (
            f"postgres://{username}:{password}@{host}:{db_port}/{db_name}"
        )

        self.database_connection = psycopg.connect(connection_string)

    def query(
        self,
        query: str,
        params: Tuple | None = None,
        count: int = -1,
        commit: bool = True,
    ):
        """
        Executes a query on the database with the given params and returns the results. Commits changes if any.
        Raises and error if the query fails to be executed. If count = -1 return all, otherwise return the given count.
        Commit determines if queries should be automatically committed after execution.
        """
        with self.database_connection.cursor() as cur:
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
            self.commit()
        return res

    def commit(self):
        """Force commit all pending changes."""
        self.database_connection.commit()

    def rollback(self):
        """Forcefully rollback any pending commits."""
        self.database_connection.rollback()


generic_database = DatabaseManager(
    environ.get("COMMON_USERNAME"),
    environ.get("COMMON_PASSWORD"),
    environ.get("COMMON_HOST"),
    environ.get("COMMON_DB_PORT"),
    environ.get("COMMON_DB_NAME"),
)
