from dataclasses import dataclass
from db.database import AdminDatabaseManager
import bcrypt
import re
from admin.auth import errors


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
            SELECT id FROM administration.usuario WHERE email=%s
        """,
            (email,),
            count=1,
        )[0]

        if user_exists:
            raise errors.UserAlreadyExists(email)

        if not self.validate_email(email) or not self.validate_password(password):
            raise errors.InvalidLoginData()

        salt = bcrypt.gensalt()
        pwd = password.encode()

        hashed_pwd = bcrypt.hashpw(pwd, salt)

        user_id = self.database_manager.query(
            """
        INSERT INTO administration.usuario (name, email, password_hash) VALUES (%s, %s, %s) RETURNING id;
    """,
            (name, email, hashed_pwd.decode()),
            1,
        )[0]

        return user_id

    def get_user_by_id(self, user_id: int) -> User | None:
        """
        Returns the user identified by id or None if no user is found.
        """
        user_data = self.database_manager.query(
            """
            SELECT id, name, email FROM administration.usuario WHERE id = %s
        """,
            (user_id,),
            1,
        )

        if user_data:
            return User(user_data[0], user_data[1], user_data[2])
        return None

    def get_user_by_email(self, email: str) -> User | None:
        """Returns the user identified by email or None if no user is found"""
        user_data = self.database_manager.query(
            """
            SELECT id, name, email FROM administration.usuario WHERE email = %s
        """,
            (email,),
            1,
        )

        if user_data:
            return User(user_data[0], user_data[1], user_data[2])
        return None

    def get_user_count(self) -> int:
        """
        Returns the amount of users created. Used for allowing only one user creation from the frontend when first starting the server.
        """

        res = self.database_manager.query(
            """
        SELECT count(*) FROM administration.usuario
    """,
            count=1,
        )[0]

        return res

    def login(self, email: str, password: str) -> User | None:
        user_data = self.database_manager.query(
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
