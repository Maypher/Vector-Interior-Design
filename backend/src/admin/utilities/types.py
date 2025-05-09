from __future__ import annotations
from typing import TYPE_CHECKING
from sanic import Request, Sanic, Config
from types import SimpleNamespace
from typing import TypedDict


if TYPE_CHECKING:
    from admin.db.database import AdminDatabaseManager
    from admin.auth.session import SessionManager
    from admin.auth.user import UserManager
    from admin.resources.resource_manager import AdminResourceManager
    from sanic.response import HTTPResponse


class Context:
    database_manager: AdminDatabaseManager
    session_manager: SessionManager
    user_manager: UserManager
    resource_manager: AdminResourceManager


type AdminApp = Sanic[Config, Context]


class AdminRequest(Request[Sanic[Config, Context], SimpleNamespace]):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class GraphQLContext(TypedDict):
    request: AdminRequest
    response: HTTPResponse
    resource_manager: AdminResourceManager
