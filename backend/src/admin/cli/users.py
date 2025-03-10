import argparse
from os import environ
from admin.db.database import DatabaseManager
from admin.auth.user import UserManager
from common.utils import read_secret
from admin.auth import errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utility file for user management.")

    subparser = parser.add_subparsers(dest="command", required=True)

    new_parser = subparser.add_parser("new", help="Creates a new admin user.")
    new_parser.add_argument(
        "-n",
        "--name",
        nargs=1,
        required=True,
        help="The name of the person this account belongs to.",
    )
    new_parser.add_argument(
        "-e",
        "--email",
        nargs=1,
        type=str,
        help="The email to relate this account to.",
        required=True,
    )
    new_parser.add_argument(
        "-p",
        "--password",
        type=str,
        nargs=1,
        help="The password used to access this account.",
        required=True,
    )

    delete_parser = subparser.add_parser(
        "delete", help="Deletes the admin user identified by the given email."
    )
    delete_parser.add_argument(
        "email",
        nargs=1,
        help="The unique email address that identifies the user.",
    )

    change_password_parser = subparser.add_parser(
        "change_password", help="Changes the password for the given account."
    )
    change_password_parser.add_argument(
        "-e",
        "--email",
        type=str,
        nargs=1,
        required=True,
        help="The email of the account that should have the password changed.",
    )
    change_password_parser.add_argument(
        "-p",
        "--password",
        type=str,
        nargs=1,
        required=True,
        help="The new password for the account.",
    )

    list_users_parser = subparser.add_parser("list", help="List all users.")

    args = parser.parse_args()
    command: str = args.command

    database_handler = DatabaseManager(
        environ.get("USERNAME"),
        read_secret("admin_password"),
        environ.get("HOST"),
        environ.get("DB_PORT"),
        environ.get("DB_NAME"),
    )

    user_manager = UserManager(database_handler)

    match command:
        case "new":
            name = args.name[0]
            email = args.email[0]
            password = args.password[0]

            try:
                user_manager.create_user(email, name, password)
                print(f"User {name} ({email}) created with password: {password}")
            except errors.UserAlreadyExists as e:
                print(f"Email {e.email} already registered.")
                exit(1)
            except errors.InvalidLoginData as e:
                print(
                    f"Invalid email or insufficient password. Password must be 8 characters long, contain uppercase, lowercase, number and special character."
                )
        case "delete":
            email = args.email[0]

            delete = False

            while not delete:
                res = input(
                    f"Are you sure you want to delete the account with the email '{email}'? This action can't be undone (Y/N): "
                ).upper()

                if res == "Y":
                    delete = True
                elif res == "N":
                    exit(0)

            deleted_user = user_manager.delete_user(email)

            if deleted_user:
                print(f"User with email '{deleted_user.email}' successfully deleted.")
            else:
                print(f"User with email '{email}' not found.")
        case "change_password":
            email = args.email[0]
            new_password = args.password[0]

            updated_user = user_manager.change_password(email, new_password)

            if updated_user:
                print(
                    f"{updated_user.name}'s password changed successfully. New password: {new_password}"
                )
            else:
                print(f"User with email {email} not found.")
        case "list":
            users = user_manager.users()

            for i, user in enumerate(users):
                print(f"{i+1}. {user.name} ({user.email})")
