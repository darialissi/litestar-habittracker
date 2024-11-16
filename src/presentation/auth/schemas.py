from datetime import datetime

from pydantic import BaseModel


class TokenSchema(BaseModel):
    exp: datetime
    iat: datetime
    sub: str


class UsernameSchema(BaseModel):
    username: str
