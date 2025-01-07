from __future__ import annotations
from db.database import DatabaseManager
from secrets import token_urlsafe
from datetime import datetime, timedelta
from dataclasses import dataclass
from admin.auth import errors


@dataclass
class Session:
    session_id: str
    expires_at: datetime
    user_id: int

    @property
    def expired(self):
        """Returns true if the current session is expired."""
        return datetime.now() > self.expires_at

    def should_refresh_session(self, threshold: timedelta = timedelta(minutes=15)):
        """Returns true if the time to expiration is less than a threshold"""
        return self.expires_at - datetime.now() <= threshold


class SessionManager:
    database_manager: DatabaseManager

    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    def create_session(
        self, user_id: int, session_duration: timedelta = timedelta(hours=1)
    ) -> Session:
        """
        Creates a new session for the given user and stores it in the database.
        Raises ValueError if no user with the given id was found.
        """
        session_id = token_urlsafe(16)
        expires_at = datetime.now() + session_duration

        user_exists = self.database_manager.query(
            """
            SELECT id FROM administration.usuario WHERE id = %s;
        """,
            (user_id,),
        )

        if user_exists:
            session = Session(session_id, expires_at, user_id)

            # Done in case the generated session id already exists (extremely unlikely)

            self.database_manager.query(
                "INSERT INTO administration.session (session_id, expires_at, user_id) VALUES (%s, %s, %s);",
                (session_id, str(expires_at), user_id),
            )

            return session
        else:
            raise errors.UserNotFound(user_id)

    def get_session(self, session_id: str) -> Session | None:
        """
        Fetches a session from the database given its id. Returns None if no session was found
        """

        session_data = self.database_manager.query(
            """
        SELECT expires_at, user_id FROM administration.session WHERE session_id = %s;
    """,
            (session_id,),
            1,
        )

        if session_data:
            return Session(
                session_id,
                session_data[0],
                session_data[1],
            )

        return None

    def refresh_session(
        self, session: Session, extend_by: timedelta = timedelta(minutes=30)
    ):
        """Extends the expiration time of the given session."""
        new_expiry = session.expires_at + extend_by

        self.database_manager.query(
            """
        UPDATE administration.session
        SET expires_at = %s;
    """,
            (str(new_expiry),),
        )

        session.expires_at = new_expiry

    def remove_session(self, session_id: str):
        """Immediately expires the session identified by `session_id`"""
        self.database_manager.query(
            "DELETE FROM administration.session WHERE session_id=%s", (session_id,)
        )
