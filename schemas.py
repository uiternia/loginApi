from pydantic import BaseModel
from typing import Optional
from decouple import config

CSRF_KEY = config('CSRF_KEY')


class CsrfSettings(BaseModel):
    secret_key: str = CSRF_KEY


class SuccessMsg(BaseModel):
    message: str


class UserBody(BaseModel):
    name: str
    email: str
    password: str


class UserBodyLogin(BaseModel):
    email: str
    password: str


class UserInfo(BaseModel):
    id: Optional[str] = None
    name: str
    email: str


class UserEmail(BaseModel):
    id: Optional[str] = None
    email: str


class Csrf(BaseModel):
    csrf_token: str


class MyUser(BaseModel):
    name: str
    email: str
    image: str
