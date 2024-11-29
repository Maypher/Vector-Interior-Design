from flask import Blueprint, request, session
from auth import user as user_auth
from auth import create_session, remove_session, login_required, get_session
from flask import session
import json

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.get("/usuario-creado")
def main_user_created():
    user_count = user_auth.get_user_count()
    return str(user_count)


@auth_blueprint.post("/crear-cuenta")
def create_account():
    user_count = user_auth.get_user_count()
    if user_count > 0:
        return "Main account already created.", 401

    request_data: dict = json.loads(request.form)

    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    if not email or not name or not password:
        return "Incomplete data. Provide an email, name and password.", 400

    if not user_auth.validate_email(email) or not user_auth.validate_password(password):
        return (
            "Incomplete data. Please check your email and password for correct formatting.",
            400,
        )

    if user_auth.get_user_by_email(email):
        return "User with this email already exists", 401

    user_id = user_auth.create_user(email, name, password)

    user_session = create_session(user_id)

    session["session_id"] = user_session.session_id

    return "", 200


@auth_blueprint.post("/iniciar-sesion")
def login():
    request_data: dict = json.loads(request.json)
    email = request_data.get("email")
    password = request_data.get("password")

    if not email or not password:
        return "Incomplete data. Provide an email and a password.", 401

    user = user_auth.login(email, password)

    if not user:
        return "Invalid credentials.", 401

    user_session = create_session(user.id)

    session["session_id"] = user_session.session_id

    return "", 200


@auth_blueprint.post("/cerrar-sesion")
def logout():
    session_id: bytes = session.get("session_id")

    if session_id:
        remove_session(session_id)
        session.pop("session_id")

    return "Cierre de sesión exitoso.", 200


@auth_blueprint.get("/info-usuario")
@login_required
def get_user_info():
    session_id = session.get("session_id")

    if session_id:
        sess = get_session(session_id)

        if sess:
            return user_auth.get_user_by_id(sess.user_id).__dict__

        return "", 404
