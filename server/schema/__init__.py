from .request_format import *
from .response_format import *


class RegisterForm(ConfigBaseModel):
    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=8, max_length=20)
    name: str = Field(min_length=1, max_length=20)
    group_id: int | None = None
