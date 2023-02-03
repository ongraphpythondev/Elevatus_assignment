from pydantic import BaseModel, EmailStr
from typing import Union


class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class TokenData(BaseModel):
    email: Union[str, None] = None


class LoginUser(BaseModel):
    username: EmailStr
    password: str


class UserModel(BaseModel):
    name : str
    email : str
    password : str
    