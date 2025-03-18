from .request_format import *
from .response_format import *


class RegisterForm(ConfigBaseModel):
    username: str
    password: str

