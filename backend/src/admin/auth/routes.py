from sanic.blueprints import Blueprint
from sanic import response
from admin.utilities.types import AdminRequest
from admin.auth.decorators import login_required
from sanic.log import logger

auth_blueprint = Blueprint("auth", "/auth")


@auth_blueprint.get("/usuario-creado")
async def main_user_created(request: AdminRequest):
    user_count = request.app.ctx.user_manager.get_user_count()
    return response.text(str(user_count))


@auth_blueprint.post("/crear-cuenta")
async def create_account(request: AdminRequest):
    user_count = request.app.ctx.user_manager.get_user_count()
    if user_count > 0:
        return response.text("Cuenta principal ya creada.", 401)

    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    if not email or not name or not password:
        return response.text(
            "Información incompleta. Correo y contraseña requeridas.", 400
        )

    user_manager = request.app.ctx.user_manager

    if not user_manager.validate_email(email) or not user_manager.validate_password(
        password
    ):
        return response.text(
            "Datos incompletos. Verifique su correo electrónico y contraseña para ver si el formato es correcto.",
            400,
        )

    if user_manager.get_user_by_email(email):
        return response.text("Usuario con este correo ya existe.", 401)

    user_id = user_manager.create_user(email, name, password)

    user_session = request.app.ctx.session_manager.create_session(user_id)

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
async def login(request: AdminRequest):
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return response.text(
            "Información incompleta. Proveer correo y contraseña.", 401
        )

    user = request.app.ctx.user_manager.login(email, password)

    if not user:
        return response.text("Credenciales invalidas.", 401)

    user_session = request.app.ctx.session_manager.create_session(user.id)

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
async def logout(request: AdminRequest):
    session_id: bytes = request.cookies.get("session_id")
    res = response.text("Cierre de sesión exitoso.", 200)

    if session_id:
        request.app.ctx.session_manager.remove_session(session_id)
        res.delete_cookie("session_id")
        return res

    res.body = "Sesión no encontrada."
    return res


@auth_blueprint.get("/info-usuario")
@login_required
async def get_user_info(request: AdminRequest):
    session_id = request.cookies.get("session_id")

    if session_id:
        sess = request.app.ctx.session_manager.get_session(session_id)

        if sess:
            return response.json(
                request.app.ctx.user_manager.get_user_by_id(sess.user_id).__dict__
            )

        return response.empty(404)
