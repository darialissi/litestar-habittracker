import pytest
from litestar import Litestar, Response, status_codes
from litestar.testing import AsyncTestClient

from application.schemas.user import UserDTO, UserReturnDTO


@pytest.mark.asyncio
class TestUser:

    async def test_signin(self, auth_data: UserDTO, test_client: AsyncTestClient[Litestar]):

        resp: Response[UserReturnDTO] = await test_client.post(
            "/api/account/signin", data=auth_data.model_dump_json()
        )

        assert resp.status_code == status_codes.HTTP_201_CREATED
        assert resp.headers.get("set-cookie") is not None

    async def test_me(
        self,
        auth_data: UserDTO,
        token_cookie: dict,
        test_client: AsyncTestClient[Litestar],
        signin_fixture,
    ):

        resp: Response[UserReturnDTO] = await test_client.get(
            "/api/account/me", cookies=token_cookie
        )

        assert resp.status_code == status_codes.HTTP_200_OK
        assert resp.json().get("username") == auth_data.username
        assert resp.json().get("id") == 1
