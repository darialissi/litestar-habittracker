from collections.abc import AsyncIterator
from datetime import timedelta

import pytest
from litestar import Litestar
from litestar.testing import AsyncTestClient

from app import app
from application.schemas.enums import Period
from application.schemas.habit import HabitCounterUpdateDTO, HabitDTO
from application.schemas.user import UserDTO
from config import settings
from utils.auth.token import Token

app.debug = True


@pytest.fixture
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app) as client:
        yield client


@pytest.fixture
def token_cookie(auth_data: UserDTO) -> dict:
    payload = {"sub": auth_data.username}
    token = Token.encode_jwt(
        payload,
        private_key=settings.TOKEN_KEY_SECRET,
        expire=timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES),
    )
    return {settings.AUTH_COOKIE: token}


@pytest.fixture
def auth_data() -> UserDTO:
    return UserDTO(username="aaaaa", password="11111")


@pytest.fixture
def habit_data() -> HabitDTO:
    return HabitDTO(title="Чтение тех. литературы", count=3, period=Period.WEEKLY.name)


@pytest.fixture
def habit_counter_data() -> HabitCounterUpdateDTO:
    return HabitCounterUpdateDTO(title="Чтение тех. литературы")
