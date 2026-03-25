import unittest.mock

import pytest
from pydantic import BaseModel

from application.schemas.user import UserDTO
from application.services.user import UserService
from domain.models.user import User

USER = dict(
    id=1, username="testuser", created_at="2025-01-01T00:00:00", updated_at="2025-01-01T00:00:00"
)


class Case(BaseModel):
    get_user_response: dict | None = None
    add_user_response: dict | None = None


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.parametrize(
    "test_case",
    [
        pytest.param(
            Case(get_user_response=USER, add_user_response=None),
            id="OK - existing user",
        ),
        pytest.param(
            Case(get_user_response=None, add_user_response=USER),
            id="OK - new user",
        ),
    ],
)
async def test_add_or_get_user(
    test_case: Case,
    user_service: UserService,
    auth_data: UserDTO,
):

    with (
        unittest.mock.patch.object(
            target=UserService,
            attribute=UserService.get_user.__name__,
            new=unittest.mock.AsyncMock(return_value=test_case.get_user_response),
        ) as mock_existing_user,
        unittest.mock.patch.object(
            target=UserService,
            attribute=UserService.add_user.__name__,
            new=unittest.mock.AsyncMock(return_value=test_case.add_user_response),
        ) as mock_new_user,
    ):

        resp: User = await user_service.add_or_get_user(data=auth_data)

        expected_user = mock_existing_user.return_value or mock_new_user.return_value

        assert resp["id"] == expected_user["id"]
        assert resp["username"] == expected_user["username"]
