import pytest
from httpx import Response
from litestar import Litestar, status_codes
from litestar.testing import AsyncTestClient

from application.schemas.responses import ResponseSchema
from application.schemas.user import UserDTO


@pytest.mark.asyncio
@pytest.mark.e2e
class TestUser:

    async def test_signin(self, auth_data: UserDTO, test_client_with_db: AsyncTestClient[Litestar]):

        resp: Response[ResponseSchema] = await test_client_with_db.post(
            "/api/account/signin", data=auth_data.model_dump_json()
        )

        assert resp.status_code == status_codes.HTTP_201_CREATED
        assert resp.headers.get("set-cookie") is not None

    async def test_me(
        self,
        auth_data: UserDTO,
        token_cookie: dict,
        test_client_with_db: AsyncTestClient[Litestar],
        signin_fixture,
    ):

        response: Response[ResponseSchema] = await test_client_with_db.get(
            "/api/account/me", cookies=token_cookie
        )

        assert response.status_code == status_codes.HTTP_200_OK

        payload: dict = response.json()["payload"]

        assert payload.get("username") == auth_data.username
        assert payload.get("id") == 1

    async def test_token(
        self,
        auth_data: UserDTO,
        token_cookie: dict,
        token: str,
        test_client_with_db: AsyncTestClient[Litestar],
        signin_fixture,
    ):

        response: Response[ResponseSchema] = await test_client_with_db.get(
            "/api/account/token", cookies=token_cookie
        )

        assert response.status_code == status_codes.HTTP_200_OK

        payload: dict = response.json()["payload"]

        assert payload.get("user").get("username") == auth_data.username
        assert payload.get("token") == token
