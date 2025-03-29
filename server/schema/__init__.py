from .request_format import *
from .response_format import *


class RegisterForm(ConfigBaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=50)
    group_id: int | None = None
