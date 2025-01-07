from __future__ import annotations
from admin.db.database import AdminDatabaseManager
from admin.auth.session import SessionManager
from admin.auth.user import UserManager
from admin.resources.obra import AdminResourceManager
from sanic import Request, Sanic, Config
from sanic.response import HTTPResponse
from typing import TypedDict
from types import SimpleNamespace


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
