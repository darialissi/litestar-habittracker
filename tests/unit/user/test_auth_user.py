import unittest.mock

import pytest

from application.schemas.user import UserDTO
from application.services.user import UserService
from domain.models.user import User

USER = dict(
    id=1, username="testuser", created_at="2025-01-01T00:00:00", updated_at="2025-01-01T00:00:00"
)


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.parametrize(
    """
    get_user_response,
    add_user_response
    """,
    [
        pytest.param(
            USER,
            None,
            id="OK - existing user",
        ),
        pytest.param(
            None,
            USER,
            id="OK - new user",
        ),
    ],
)
async def test_auth_user(
    get_user_response: dict | None,
    add_user_response: dict | None,
    user_service: UserService,
    auth_data: UserDTO,
):

    with (
        unittest.mock.patch.object(
            target=UserService,
            attribute=UserService.get_user.__name__,
            new=unittest.mock.AsyncMock(return_value=get_user_response),
        ) as mock_existing_user,
        unittest.mock.patch.object(
            target=UserService,
            attribute=UserService.add_user.__name__,
            new=unittest.mock.AsyncMock(return_value=add_user_response),
        ) as mock_new_user,
        unittest.mock.patch.object(
            target=UserService,
            attribute=UserService.create_token.__name__,
            new=unittest.mock.AsyncMock(return_value="mocked_token"),
        ),
    ):

        resp: tuple[User, str] = await user_service.auth_user(data=auth_data)

        expected_user = mock_existing_user.return_value or mock_new_user.return_value

        assert resp[0]["id"] == expected_user["id"]
        assert resp[0]["username"] == expected_user["username"]
