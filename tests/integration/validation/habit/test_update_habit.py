import unittest.mock

import pytest
from litestar import Litestar, Response, status_codes
from litestar.testing import AsyncTestClient

from application.schemas.habit import HabitReturnDTO
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
            dict(title="test habit"),
            status_codes.HTTP_200_OK,
            id="OK",
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
async def test_update_habit(
    habit_dict: dict,
    expected_status_code: int,
    update_habit_resp_dict: dict,
    token_cookie: dict,
    test_client: AsyncTestClient[Litestar],
):
    """Тест проверяет валидацию модели на уровне эндпоинта обновление привычки."""

    with (
        unittest.mock.patch.object(
            target=HabitService,
            attribute=HabitService.update_habit.__name__,
            new=unittest.mock.AsyncMock(return_value=update_habit_resp_dict),
        ) as mock_habit,
    ):

        resp: Response[HabitReturnDTO] = await test_client.patch(
            "/api/habits", json=habit_dict, cookies=token_cookie
        )

        assert resp.status_code == expected_status_code

        if resp.status_code == status_codes.HTTP_200_OK:
            response = resp.json()
            assert response["id"] == mock_habit.return_value["id"]
            assert response["updated_at"] == mock_habit.return_value["updated_at"]
