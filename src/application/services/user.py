from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from application.schemas.auth import UserCredMasked
from domain.models.user import User


class UserService:

    def __init__(self, repo: SQLAlchemyAsyncRepository):
        self.user_repo = repo

    async def add_user(self, user: UserCredMasked) -> User:
        u_dict = user.model_dump()
        user = await self.user_repo.add(self.user_repo.model_type(**u_dict))
        await self.user_repo.session.commit()
        return user

    async def get_user(self, **filters) -> User | None:
        user = await self.user_repo.get_one_or_none(**filters)
        return user

    async def add_or_get_user(self, data: UserCredMasked) -> User:

        if not (user := await self.get_user(username=data.username)):
            user = await self.add_user(data)

        return user
