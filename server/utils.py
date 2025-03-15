from typing import TypeVar
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from contextvars import ContextVar
from functools import wraps
from typing import Generic

_T = TypeVar("T")


class GlobalContextVar(Generic[_T]):
    def __init__(self, name: str, dependency: AsyncGenerator):
        self.__dict__.setdefault("cvar", None)
        self.__dict__.setdefault("app_dependency", None)
        self.cvar = ContextVar[_T | None](name)

        @wraps(dependency)
        async def wrapped(*args, **kwargs):
            func = asynccontextmanager(dependency)
            async with func(*args, **kwargs) as gen:
                self.cvar.set(gen)
                yield gen
                self.cvar.set(None)

        self.app_dependency = wrapped

    def __get_inner(self):
        return self.cvar.get()

    def __getattr__(self, item):
        if item in self.__dict__:
            return super().__getattr__(item)
        return getattr(self.__get_inner(), item)

    def __setattr__(self, key, value):
        if key in self.__dict__:
            return super().__setattr__(key, value)
        return setattr(self.__get_inner(), key, value)

    def __delattr__(self, item):
        delattr(self.__get_inner(), item)

    def __repr__(self):
        return repr(self.__get_inner())

    def __str__(self):
        return str(self.__get_inner())
