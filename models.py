from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str
    name: str


class Login(BaseModel):
    email: str
    password: str
