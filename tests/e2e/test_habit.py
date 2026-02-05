import pytest
from litestar import Litestar, Response, status_codes
from litestar.testing import AsyncTestClient

from application.schemas.habit import HabitCounterUpdateDTO, HabitDTO, HabitReturnDTO
from application.schemas.user import UserDTO


@pytest.mark.asyncio
@pytest.mark.e2e
class TestHabit:

    async def test_add_habit(
        self,
        signin_fixture,
        auth_data: UserDTO,
        token_cookie: dict,
        habit_data: HabitDTO,
        test_client_with_db: AsyncTestClient[Litestar],
    ):

        resp: Response[HabitReturnDTO] = await test_client_with_db.post(
            "/api/habits", data=habit_data.model_dump_json(), cookies=token_cookie
        )

        assert resp.status_code == status_codes.HTTP_201_CREATED
        assert resp.json().get("id") == 1
        assert resp.json().get("author") == auth_data.username
        assert resp.json().get("title") == habit_data.title
        assert resp.json().get("current_streak_days") == 0

    async def test_habit(
        self,
        signin_fixture,
        auth_data: UserDTO,
        token_cookie: dict,
        habit_data: HabitDTO,
        test_client_with_db: AsyncTestClient[Litestar],
    ):

        resp: Response[HabitReturnDTO] = await test_client_with_db.get(
            "/api/habits", cookies=token_cookie
        )

        assert resp.status_code == status_codes.HTTP_404_NOT_FOUND

        await test_client_with_db.post(
            "/api/habits", data=habit_data.model_dump_json(), cookies=token_cookie
        )

        resp: Response[HabitReturnDTO] = await test_client_with_db.get(
            "/api/habits", cookies=token_cookie
        )

        assert resp.status_code == status_codes.HTTP_200_OK

    async def test_update_habit(
        self,
        signin_fixture,
        add_habit_fixture,
        auth_data: UserDTO,
        token_cookie: dict,
        habit_counter_data: HabitCounterUpdateDTO,
        test_client_with_db: AsyncTestClient[Litestar],
    ):

        resp: Response[HabitReturnDTO] = await test_client_with_db.patch(
            "/api/habits", data=habit_counter_data.model_dump_json(), cookies=token_cookie
        )

        assert resp.status_code == status_codes.HTTP_200_OK, resp.json()
        assert resp.json().get("current_streak_days") == 1
        assert resp.json().get("max_streak_days") == 1
