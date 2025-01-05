from flask import request, make_response
from auth import user as user_auth
from auth import create_session, remove_session, login_required, get_session
from sanic.blueprints import Blueprint
from sanic import response
from sanic.request import Request
import json

auth_blueprint = Blueprint("auth", "/auth")


@auth_blueprint.get("/usuario-creado")
def main_user_created(request: Request):
    user_count = user_auth.get_user_count()
    return response.text(user_count)


@auth_blueprint.post("/crear-cuenta")
def create_account(request: Request):
    user_count = user_auth.get_user_count()
    if user_count > 0:
        return response.text("Cuenta principal ya creada.", 401)

    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    if not email or not name or not password:
        return response.text(
            "Información incompleta. Correo y contraseña requeridas.", 400
        )

    if not user_auth.validate_email(email) or not user_auth.validate_password(password):
        return response.text(
            "Datos incompletos. Verifique su correo electrónico y contraseña para ver si el formato es correcto.",
            400,
        )

    if user_auth.get_user_by_email(email):
        return response.text("Usuario con este correo ya existe.", 401)

    user_id = user_auth.create_user(email, name, password)

    user_session = create_session(user_id)

    res = response.empty(200)
    res.add_cookie(
        "session_id",
        user_session.session_id,
        expires=user_session.expires_at,
        httponly=True,
        samesite="None",
        secure=True,
    )

    return res


@auth_blueprint.post("/iniciar-sesion")
def login(request: Request):
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return response.text(
            "Información incompleta. Proveer correo y contraseña.", 401
        )

    user = user_auth.login(email, password)

    if not user:
        return response.text("Credenciales invalidas.", 401)

    user_session = create_session(user.id)

    res = response.empty(200)
    res.add_cookie(
        "session_id",
        user_session.session_id,
        expires=user_session.expires_at,
        httponly=True,
        samesite="None",
        secure=True,
    )

    return res


@auth_blueprint.post("/cerrar-sesion")
def logout(request: Request):
    session_id: bytes = request.cookies.get("session_id")
    res = response.text("Cierre de sesión exitoso.", 200)

    if session_id:
        remove_session(session_id)
        res.delete_cookie("session_id")
        return res

    res.body = "Sesión no encontrada."
    return res


@auth_blueprint.get("/info-usuario")
@login_required
def get_user_info(request: Request):
    session_id = request.cookies.get("session_id")

    if session_id:
        sess = get_session(session_id)

        if sess:
            return response.json(
                json.dumps(user_auth.get_user_by_id(sess.user_id).__dict__)
            )

        return response.empty(404)
