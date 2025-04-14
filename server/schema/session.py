from typing import Literal
from pydantic import BaseModel, Field


class SessionToken(BaseModel):
    access_token: str
    token_type: Literal["Bearer"]


class RegisterForm(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=50)
    group_id: int | None = None
