import unittest.mock

import pytest
from httpx import Response
from litestar import Litestar, status_codes
from litestar.testing import AsyncTestClient

from application.schemas.enums import Period
from application.schemas.responses import ResponseSchema
from application.services.habit import HabitService


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.validation
@pytest.mark.parametrize(
    """
    habit_dict,
    expected_status_code
    """,
    [
        pytest.param(
            dict(title="test habit", count=2, period=Period.WEEKLY.name),
            status_codes.HTTP_201_CREATED,
            id="OK",
        ),
        pytest.param(
            dict(title="test habit"),
            status_codes.HTTP_201_CREATED,
            id="OK: default count/period",
        ),
        pytest.param(
            dict(title="test habit", count=0),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: invalid count",
        ),
        pytest.param(
            dict(title="test habit", period=""),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: empty period",
        ),
        pytest.param(
            dict(title="test habit", period="UNDEFINED"),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: undefined period",
        ),
        pytest.param(
            dict(),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: missing title",
        ),
        pytest.param(
            dict(title="a" * 1),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: short title",
        ),
        pytest.param(
            dict(title="a" * 51),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: long title",
        ),
    ],
)
async def test_add_new_habit(
    habit_dict: dict,
    expected_status_code: int,
    add_habit_resp_dict: dict,
    token_cookie: dict,
    test_client: AsyncTestClient[Litestar],
):
    """Тест проверяет валидацию модели на уровне эндпоинта добавление новой привычки."""

    with (
        unittest.mock.patch.object(
            target=HabitService,
            attribute=HabitService.add_new_habit.__name__,
            new=unittest.mock.AsyncMock(return_value=add_habit_resp_dict),
        ) as mock_habit,
    ):

        response: Response[ResponseSchema] = await test_client.post(
            "/api/habits", json=habit_dict, cookies=token_cookie
        )

        assert response.status_code == expected_status_code

        if response.status_code == status_codes.HTTP_201_CREATED:
            payload = response.json()["payload"]
            assert payload["id"] == mock_habit.return_value["id"]
            assert payload["title"] == mock_habit.return_value["title"]
