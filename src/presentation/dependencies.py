from sqlalchemy.ext.asyncio import AsyncSession

from application.services.habit import HabitService
from application.services.user import UserService
from domain.repositories.habit import HabitRepository
from domain.repositories.habit_dates import HabitDatesRepository
from domain.repositories.user import UserRepository


async def user_service(db_session: AsyncSession):
    return UserService(UserRepository(session=db_session))


async def habit_service(db_session: AsyncSession):
    return HabitService(
        HabitRepository(session=db_session), HabitDatesRepository(session=db_session)
    )
