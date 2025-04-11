from sanic.blueprints import Blueprint
from sanic import response
from admin.utilities.types import AdminRequest
from admin.auth.decorators import login_required
from os import environ
from common.utilities.environment import dev_mode, frontend_url

auth_blueprint = Blueprint("auth", "/auth")


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
        samesite="Strict",
        secure=not dev_mode,
        domain=frontend_url,
    )

    # Removing the port from the cookie domain since separating cookies per port isn't allowed. On production when
    # running the admin and user frontends in different subdomains they will not be set for both. Doing this to hide the session_id
    # from the user frontend.

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
