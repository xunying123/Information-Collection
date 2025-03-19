from typing import TypeVar
from collections.abc import Callable
from contextvars import ContextVar
from fastapi import Depends
from werkzeug.local import LocalProxy

_T = TypeVar("T")


class Globalize(LocalProxy[_T]):
    def __init__(self, name: str, dependency: Callable):
        cvar = ContextVar[_T | None](name)
        super().__init__(cvar)

        async def setter(_val: _T = Depends(dependency)):
            cvar.set(_val)
            yield
            cvar.set(None)

        object.__setattr__(self, "app_dependency_", setter)

    @property
    def app_dependency(self):
        return object.__getattribute__(self, "app_dependency_")
