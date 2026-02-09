from datetime import datetime

from pydantic import BaseModel


class TokenSchema(BaseModel):
    exp: datetime
    iat: datetime
    sub: str


class UserSchema(BaseModel):
    username: str


class AuthSchema(BaseModel):
    user: UserSchema
    token: str
