from collections.abc import AsyncIterator
from datetime import timedelta

import pytest
from litestar import Litestar
from litestar.testing import AsyncTestClient

from app import app
from application.schemas.habit import HabitDTO
from application.schemas.user import UserDTO
from config import settings
from infrastructure.database import create_tables, drop_tables
from utils.auth.token import Token

app.debug = True


@pytest.fixture
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    app.on_startup.append(create_tables)
    app.on_shutdown.append(drop_tables)
    async with AsyncTestClient(app=app) as client:
        yield client


@pytest.fixture
def auth_data() -> UserDTO:
    return UserDTO(username="aaaaa", password="11111")


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
async def signin_fixture(
    auth_data: UserDTO, token_cookie: dict, test_client: AsyncTestClient[Litestar]
):
    await test_client.post("/api/account/signin", data=auth_data.model_dump_json())


@pytest.fixture
def habit_data() -> HabitDTO:
    return HabitDTO(title="Уделять 1 час чтению книги ежедневно")


@pytest.fixture
async def add_habit_fixture(
    habit_data: HabitDTO, token_cookie: dict, test_client: AsyncTestClient[Litestar]
):
    await test_client.post("/api/habits", data=habit_data.model_dump_json(), cookies=token_cookie)
