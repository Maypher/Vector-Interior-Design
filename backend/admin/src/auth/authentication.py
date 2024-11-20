from db.database import query
from secrets import token_urlsafe
from dataclasses import dataclass
from datetime import datetime, timedelta
from flask import session as flask_session
from functools import wraps


@dataclass
class Session:
    session_id: str
    expires_at: datetime
    user_id: int


def create_session(
    user_id: int, session_duration: timedelta = timedelta(hours=1)
) -> Session:
    """
    Creates a new session for the given user and stores it in the database.
    Raises ValueError if no user with the given id was found.
    """
    session_id = token_urlsafe(16)
    expires_at = datetime.now() + session_duration

    user_exists = query(
        """
        SELECT id FROM administration.usuario WHERE id = %s;
    """,
        (user_id,),
    )

    if user_exists:
        session = Session(session_id, expires_at, user_id)

        # Done in case the generated session id already exists (extremely unlikely)

        query(
            "INSERT INTO administration.session (session_id, expires_at, user_id) VALUES (%s, %s, %s);",
            (session_id, str(expires_at), user_id),
        )

        return session
    else:
        raise ValueError(f"Unable to find user with ID {user_id}")


def get_session(session_id: str) -> Session | None:
    """
    Fetches a session from the database given its id. Returns None if no session was found
    """

    session_data = query(
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


def session_expired(session: Session):
    """Returns true if the given session is expired."""
    return datetime.now() > session.expires_at


def should_refresh_session(
    session: Session, threshold: timedelta = timedelta(minutes=15)
):
    """Returns true if the time to expiration is less than a threshold"""
    return session.expires_at - datetime.now() <= threshold


def refreshes_session(session: Session, extend_by: timedelta = timedelta(minutes=30)):
    new_expiry = session.expires_at + extend_by

    query(
        """
    UPDATE administration.session
    SET expires_at = %s;
""",
        (str(new_expiry),),
    )

    session.expires_at = new_expiry


def remove_session(session_id: str):
    query("DELETE FROM administration.session WHERE session_id=%s", (session_id,))


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session_id = flask_session.get("session_id")
        session = get_session(session_id)

        if session:
            if session_expired(session):
                return "Session expired. Please login again.", 401
            elif should_refresh_session(session):
                refreshes_session(session)
            return func(*args, **kwargs)
        else:
            return "No credentials found. Please login.", 401

    return wrapper
