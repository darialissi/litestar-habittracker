from sqlalchemy.ext.asyncio import AsyncSession

from application.services.auth import AuthService
from application.services.habit import HabitService
from application.services.user import UserService
from config import settings
from domain.repositories.habit import HabitRepository
from domain.repositories.habit_dates import HabitDatesRepository
from domain.repositories.user import UserRepository

auth_service_instance = AuthService(
    secret_key=settings.TOKEN_KEY_SECRET,
    expired_minutes=settings.TOKEN_EXPIRE_MINUTES,
)


async def auth_service():
    return auth_service_instance


async def user_service(db_session: AsyncSession):
    return UserService(UserRepository(session=db_session))


async def habit_service(db_session: AsyncSession):
    return HabitService(
        HabitRepository(session=db_session), HabitDatesRepository(session=db_session)
    )
