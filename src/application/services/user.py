from datetime import timedelta

from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from application.schemas.user import UserDTO
from config import settings
from utils.auth.password import Password
from utils.auth.token import Token


class UserService:

    def __init__(self, repo: SQLAlchemyAsyncRepository):
        self.user_repo = repo

    async def add_user(self, user: UserDTO):
        u_dict = user.model_dump()
        password = u_dict.pop("password")
        u_dict.update(
            {"hashed_password": Password.hash_password(password).decode("utf-8")}
        )
        user = await self.user_repo.add(self.user_repo.model_type(**u_dict))
        await self.user_repo.session.commit()
        return user

    async def auth_user(self, user: UserDTO):
        payload = {"sub": user.username}
        token = Token.encode_jwt(
            payload,
            private_key=settings.TOKEN_KEY_SECRET,
            expire=timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES),
        )
        return token

    async def get_user(self, **filters):
        user = await self.user_repo.get_one_or_none(**filters)
        return user
