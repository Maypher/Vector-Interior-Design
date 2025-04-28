from dataclasses import dataclass
from admin.db.database import AdminDatabaseManager
import bcrypt
import re
from admin.auth import errors
from psycopg import rows
from psycopg.rows import class_row


@dataclass
class User:
    id: int
    name: str
    email: str


class UserManager:
    database_manager: AdminDatabaseManager

    def __init__(self, database_manager: AdminDatabaseManager):
        self.database_manager = database_manager

    @staticmethod
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

    @staticmethod
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

    def create_user(self, email: str, name: str, password: str) -> int:
        """
        Creates a new user in the database. Raises `UserAlreadyExists` if email already exists
        or `InvalidData` if email or password are invalid.
        """

        user_exists = self.database_manager.query(
            """
            SELECT 1 FROM administration.admin_user WHERE email=%s;
        """,
            (email,),
            count=1,
            row_factory=rows.scalar_row,
        )

        if user_exists:
            raise errors.UserAlreadyExists(email)

        if not self.validate_email(email) or not self.validate_password(password):
            raise errors.InvalidLoginData()

        salt = bcrypt.gensalt()
        pwd = password.encode()

        hashed_pwd = bcrypt.hashpw(pwd, salt).decode("utf-8")

        user_id = self.database_manager.query(
            """
        INSERT INTO administration.admin_user (name, email, password_hash) VALUES (%s, %s, %s) RETURNING id;
    """,
            (name, email, hashed_pwd.decode()),
            1,
            row_factory=rows.tuple_row,
        )[0]

        return user_id

    def get_user_by_id(self, user_id: int) -> User | None:
        """
        Returns the user identified by id or None if no user is found.
        """
        return self.database_manager.query(
            """
            SELECT id, name, email FROM administration.admin_user WHERE id = %s;
        """,
            (user_id,),
            1,
            row_factory=rows.class_row(User),
        )

    def get_user_by_email(self, email: str) -> User | None:
        """Returns the user identified by email or None if no user is found"""
        return self.database_manager.query(
            """
            SELECT id, name, email FROM administration.admin_user WHERE email = %s;
        """,
            (email,),
            1,
            row_factory=rows.class_row(User),
        )

    def get_user_count(self) -> int:
        """
        Returns the amount of users created.
        Used for allowing only one user creation from the frontend when first starting the server.
        """

        return self.database_manager.query(
            """
        SELECT count(*) FROM administration.admin_user
    """,
            count=1,
            row_factory=rows.tuple_row,
        )[0]

    def login(self, email: str, password: str) -> User | None:
        user_data = self.database_manager.query(
            """
        SELECT id, name, email, password_hash FROM administration.admin_user WHERE email = %s;
    """,
            (email,),
            1,
        )

        if not user_data:
            return None

        password_hash: str = user_data.pop("password_hash")

        # If password is invalid
        if not bcrypt.checkpw(password.encode(), password_hash.encode()):
            return None

        return User(**user_data)

    def change_password(self, email: str, new_password: str) -> User | None:
        """Changes the password for the given email. Returns the updated user or `None` if the email is not found."""

        salt = bcrypt.gensalt()
        pwd = new_password.encode()

        hashed_pwd = bcrypt.hashpw(pwd, salt).decode("utf-8")

        updated_user = self.database_manager.query(
            """
            UPDATE administration.admin_user SET password_hash = %s 
            WHERE email = %s RETURNING id, email, name;
            """,
            (hashed_pwd, email),
            count=1,
            row_factory=class_row(User),
        )

        return updated_user

    def delete_user(self, email: str) -> User | None:
        return self.database_manager.query(
            """
            DELETE FROM administration.admin_user WHERE email = %s RETURNING id, email, name;
            """,
            (email,),
            1,
            row_factory=class_row(User),
        )

    def users(self) -> list[User]:
        """Returns a list of all available users."""
        return self.database_manager.query(
            """
                SELECT id, name, email FROM administration.admin_user;
            """,
            row_factory=class_row(User),
        )
