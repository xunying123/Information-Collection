from typing import TypeVar
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from contextvars import ContextVar
from functools import wraps
from typing import Generic

_T = TypeVar("T")

from werkzeug.local import LocalProxy
class Globalize(LocalProxy[_T]):
    def __init__(self, name: str, dependency: AsyncGenerator):
        cvar = ContextVar[_T | None](name)
        super().__init__(cvar)

        @wraps(dependency)
        async def wrapped(*args, **kwargs):
            func = asynccontextmanager(dependency)
            async with func(*args, **kwargs) as gen:
                cvar.set(gen)
                yield gen
                cvar.set(None)

        object.__setattr__(self, "app_dependency_", wrapped)
    
    @property
    def app_dependency(self):
        return object.__getattribute__(self, "app_dependency_")
