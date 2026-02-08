from collections.abc import AsyncIterator

import pytest
from litestar import Litestar
from litestar.testing import AsyncTestClient

from app import app
from application.schemas.habit import HabitDTO
from application.schemas.user import UserDTO
from infrastructure.database import create_tables, drop_tables

app.debug = True


@pytest.fixture
async def test_client_with_db() -> AsyncIterator[AsyncTestClient[Litestar]]:
    app.on_startup = [create_tables]
    app.on_shutdown = [drop_tables]
    async with AsyncTestClient(app=app) as client:
        yield client


@pytest.fixture
async def signin_fixture(
    auth_data: UserDTO, token_cookie: dict, test_client_with_db: AsyncTestClient[Litestar]
):
    await test_client_with_db.post("/api/account/signin", data=auth_data.model_dump_json())


@pytest.fixture
async def add_habit_fixture(
    habit_data: HabitDTO, token_cookie: dict, test_client_with_db: AsyncTestClient[Litestar]
):
    await test_client_with_db.post(
        "/api/habits", data=habit_data.model_dump_json(), cookies=token_cookie
    )


@pytest.fixture
async def update_habit_fixture(
    habit_data: HabitDTO,
    token_cookie: dict,
    test_client_with_db: AsyncTestClient[Litestar],
    add_habit_fixture,
):
    await test_client_with_db.patch(
        "/api/habits", data=habit_data.model_dump_json(), cookies=token_cookie
    )
