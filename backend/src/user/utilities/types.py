from sanic import Sanic, Config, Request
from types import SimpleNamespace
from common.types import Context


class UserRequest(Request[Sanic[Config, Context], SimpleNamespace]):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


type UserApp = Sanic[Config, Context]
