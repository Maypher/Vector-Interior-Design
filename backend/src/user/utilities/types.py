from common.database import DatabaseManager
from typing import TypedDict
from sanic.response import HTTPResponse
from sanic import Sanic, Config, Request
from types import SimpleNamespace
from common.obra import ResourceManager


class Context:
    resource_manager: ResourceManager


class UserRequest(Request[Sanic[Config, Context], SimpleNamespace]):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


type UserApp = Sanic[Config, Context]


class GraphQLContext(TypedDict):
    request: UserRequest
    response: HTTPResponse
    resource_manager: ResourceManager
