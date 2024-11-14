from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from domain.models.user import User


class UserRepository(SQLAlchemyAsyncRepository[User]):

    model_type = User
