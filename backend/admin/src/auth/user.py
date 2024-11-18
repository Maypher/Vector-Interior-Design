from dataclasses import dataclass
from db.database import query
import bcrypt
import re


@dataclass
class User:
    id: int
    name: str
    email: str


def validate_email(email: str) -> bool:
    """
    Validates that an email is correctly structured.
    """
    # Don't ask me to explain the regex :)
    return (
        re.match(
            r"^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$",
            email,
        )
        is not None
    )


def validate_password(password: str):
    """
    Validates that a password is 8 characters long, at least one uppercase, one lowercase, one number and one special character.
    """
    # You already know the answer :)
    return (
        re.match(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$',
            password,
        )
        is not None
    )


def create_user(email: str, name: str, password: str):
    """
    Creates a new user in the database. Returns an error if email or password are invalid or if the email already exists.
    """

    salt = bcrypt.gensalt()
    pwd = password.encode()

    hashed_pwd = bcrypt.hashpw(pwd, salt)

    user_id = query(
        """
    INSERT INTO administration.usuario (name, email, password_hash) VALUES (%s, %s, %s) RETURNING id;
""",
        (name, email, hashed_pwd.decode()),
        1,
    )[0]

    return user_id


def get_user_by_id(user_id: int) -> User | None:
    """
    Returns the user identified by id or None if no user is found.
    """
    user_data = query(
        """
        SELECT id, name, email FROM administration.usuario WHERE id = %s
    """,
        (user_id,),
        1,
    )

    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None


def get_user_by_email(email: str) -> User | None:
    """Returns the user identified by email or None if no user is found"""
    user_data = query(
        """
        SELECT id, name, email FROM administration.usuario WHERE email = %s
    """,
        (email,),
        1,
    )

    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None


def get_user_count() -> int:
    """
    Returns the amount of users created. Used for allowing only one user creation from the frontend when first starting the server.
    """

    res = query(
        """
    SELECT count(*) FROM administration.usuario
""",
        count=1,
    )[0]

    return res


def login(email: str, password: str) -> User | None:
    user_data = query(
        """
    SELECT id, name, email, password_hash FROM administration.usuario WHERE email = %s
""",
        (email,),
        1,
    )

    if not user_data:
        return None

    password_hash: str = user_data[3]

    # If password is invalid
    if not bcrypt.checkpw(password.encode(), password_hash.encode()):
        return None

    return User(user_data[0], user_data[1], user_data[2])
