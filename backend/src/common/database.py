import psycopg
from typing import Tuple, Callable
from psycopg.rows import RowFactory, dict_row


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
        row_factory: RowFactory = dict_row,
    ):
        """
        Executes a query on the database with the given params and returns the results. Commits changes if any.
        Raises and error if the query fails to be executed. If count = -1 return all, otherwise return the given count.
        Commit determines if queries should be automatically committed after execution.
        """
        with self.database_connection.cursor(row_factory=row_factory) as cur:
            try:
                query_result = cur.execute(query, params)
            except Exception as e:
                self.database_connection.rollback()
                raise e

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
