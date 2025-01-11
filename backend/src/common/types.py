from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
from sanic import Sanic, Config, Request
from sanic.response import HTTPResponse
from types import SimpleNamespace
from strawberry import Info

if TYPE_CHECKING:
    from common.resource_manager import ResourceManager

type ResourceInfo = Info[GraphQLContext]


class Context:
    resource_manager: ResourceManager


class UserRequest(Request[Sanic[Config, Context], SimpleNamespace]):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class GraphQLContext(TypedDict):
    request: UserRequest
    response: HTTPResponse
    resource_manager: ResourceManager
