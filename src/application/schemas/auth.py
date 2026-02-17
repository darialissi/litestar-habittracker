from datetime import datetime

from pydantic import BaseModel


class TokenSchema(BaseModel):
    exp: datetime
    iat: datetime
    sub: str


class TokenDecodedSchema(BaseModel):
    token: str


class UserSchema(BaseModel):
    username: str


class AuthSchema(BaseModel):
    user: UserSchema
    token: str


class UserCred(BaseModel):
    username: str
    password: str
    hashed_password: str


class UserCredMasked(BaseModel):
    username: str
    hashed_password: str
