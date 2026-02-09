import unittest.mock
from datetime import datetime, timezone

import pytest
from litestar import Litestar, Response, status_codes
from litestar.testing import AsyncTestClient

from application.schemas.auth import AuthSchema, UserSchema
from application.schemas.user import UserReturnDTO
from application.services.auth import AuthService
from application.services.user import UserService
from domain.models.user import User

PASSWORD = "testpass"
HASHED_PASSWORD = "hashed-000"

USER = User(
    id=1,
    username="testuser",
    hashed_password=HASHED_PASSWORD,
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc),
)


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.validation
@pytest.mark.parametrize(
    """
    user_dict,
    expected_status_code
    """,
    [
        pytest.param(
            dict(username="testuser", password=PASSWORD),
            status_codes.HTTP_201_CREATED,
            id="OK",
        ),
        pytest.param(
            dict(password=PASSWORD),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: missing username",
        ),
        pytest.param(
            dict(username=PASSWORD),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: missing password",
        ),
        pytest.param(
            dict(username="a" * 4, password=PASSWORD),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: short username",
        ),
        pytest.param(
            dict(username="a" * 4, password="test"),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: short password",
        ),
        pytest.param(
            dict(username="a" * 31, password=PASSWORD),
            status_codes.HTTP_400_BAD_REQUEST,
            id="FAIL: long username",
        ),
        pytest.param(
            dict(username="????????", password=PASSWORD),
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
            target=AuthService,
            attribute=AuthService.hash_password.__name__,
            new=unittest.mock.Mock(return_value=HASHED_PASSWORD),
        ),
        unittest.mock.patch.object(
            target=UserService,
            attribute=UserService.add_or_get_user.__name__,
            new=unittest.mock.AsyncMock(return_value=USER),
        ) as mock_user,
        unittest.mock.patch.object(
            target=AuthService,
            attribute=AuthService.auth_user.__name__,
            new=unittest.mock.Mock(
                return_value=AuthSchema(
                    token="mocked_token", user=UserSchema(username=USER.username)
                )
            ),
        ),
    ):

        resp: Response[UserReturnDTO] = await test_client.post(
            "/api/account/signin", json=user_dict
        )

        assert resp.status_code == expected_status_code, resp.text

        if resp.status_code == status_codes.HTTP_201_CREATED:
            response = resp.json()
            user: User = mock_user.return_value
            assert response["username"] == user.username
            assert resp.headers.get("set-cookie") is not None
