import unittest.mock

import pytest
from litestar import Litestar, Response, status_codes
from litestar.testing import AsyncTestClient

from application.schemas.user import UserReturnDTO
from application.services.user import UserService

USER = dict(
    id=1, username="testuser", created_at="2025-01-01T00:00:00", updated_at="2025-01-01T00:00:00"
)


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.validation
@pytest.mark.parametrize(
    """
    user_dict,
    expected_status_code
    """,
    [
        pytest.param(
            dict(username="testuser", password="testpass"),
            status_codes.HTTP_201_CREATED,
            id="OK",
        ),
        pytest.param(
            dict(password="testpass"),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: missing username",
        ),
        pytest.param(
            dict(username="testuser"),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: missing password",
        ),
        pytest.param(
            dict(username="a" * 4, password="testpass"),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: short username",
        ),
        pytest.param(
            dict(username="a" * 4, password="test"),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: short password",
        ),
        pytest.param(
            dict(username="a" * 31, password="testpass"),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: long username",
        ),
        pytest.param(
            dict(username="????????", password="testpass"),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: invalid username",
        ),
    ],
)
async def test_auth_user(
    user_dict: dict, expected_status_code: int, test_client: AsyncTestClient[Litestar]
):
    """Тест проверяет валидацию модели на уровне эндпоинта аутентификации пользователя."""

    with (
        unittest.mock.patch.object(
            target=UserService,
            attribute=UserService.get_user.__name__,
            new=unittest.mock.AsyncMock(return_value=USER),
        ) as mock_user,
        unittest.mock.patch.object(
            target=UserService,
            attribute=UserService.auth_user.__name__,
            new=unittest.mock.AsyncMock(return_value="mocked_token"),
        ),
    ):

        resp: Response[UserReturnDTO] = await test_client.post(
            "/api/account/signin", json=user_dict
        )

        assert resp.status_code == expected_status_code

        if resp.status_code == status_codes.HTTP_201_CREATED:
            response = resp.json()
            assert response["id"] == mock_user.return_value["id"]
            assert response["username"] == mock_user.return_value["username"]
            assert resp.headers.get("set-cookie") is not None
