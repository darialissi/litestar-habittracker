from unittest.mock import AsyncMock, PropertyMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.habit import HabitService
from application.services.user import UserService
from domain.repositories.habit import HabitRepository
from domain.repositories.user import UserRepository


@pytest.fixture
def session_mock() -> AsyncMock:
    empty_session = AsyncMock(spec=AsyncSession)
    type(empty_session).bind = PropertyMock(return_value=None)
    return empty_session


@pytest.fixture
def user_service(session_mock: AsyncMock) -> UserService:
    return UserService(UserRepository(session=session_mock))


@pytest.fixture
def habit_service(session_mock: AsyncMock) -> HabitService:
    return HabitService(HabitRepository(session=session_mock))
