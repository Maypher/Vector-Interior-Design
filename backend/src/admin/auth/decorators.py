from __future__ import annotations
from sanic import response
from functools import wraps
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from admin.utilities.types import AdminRequest


def login_required(f):
    @wraps(f)
    async def wrapper(request: AdminRequest, *args, **kwargs):
        session_id = request.cookies.get("session_id")
        session = request.app.ctx.session_manager.get_session(session_id)

        if session:
            if session.expired:
                return response.text(
                    "Sesión expirada. Por favor iniciar sesión de nuevo.", 401
                )
            elif session.should_refresh_session():
                request.app.ctx.session_manager.refresh_session(session)
                res: response.HTTPResponse = await f(request, *args, **kwargs)
                res.add_cookie(
                    "session_id",
                    session.session_id,
                    expires=session.expires_at,
                    httponly=True,
                    samesite="None",
                    secure=False,
                )
                return res
            else:
                return await f(request, *args, **kwargs)
        else:
            return response.text(
                "Credenciales no encontrada. Por favor iniciar sesión.", 401
            )

    return wrapper
