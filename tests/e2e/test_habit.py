from datetime import datetime, timezone

import pytest
from litestar import Litestar, Response, status_codes
from litestar.testing import AsyncTestClient

from application.schemas.habit import HabitCounterUpdateDTO, HabitDTO, HabitReturnDTO
from application.schemas.user import UserDTO

TODAY_DATE = datetime.now(timezone.utc).date().strftime("%Y-%m-%d")


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

        assert resp.status_code == status_codes.HTTP_201_CREATED, resp.json()

        resp = resp.json()
        assert resp.get("id") == 1
        assert resp.get("author") == auth_data.username
        assert resp.get("title") == habit_data.title
        assert resp.get("count") == habit_data.count
        assert resp.get("period_in_days") == habit_data.period_in_days
        assert resp.get("current_streak_days") == 0
        assert resp.get("max_streak_days") == 0

    async def test_get_habit(
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

        assert resp.status_code == status_codes.HTTP_404_NOT_FOUND, resp.json()

        await test_client_with_db.post(
            "/api/habits", data=habit_data.model_dump_json(), cookies=token_cookie
        )

        resp: Response[HabitReturnDTO] = await test_client_with_db.get(
            "/api/habits", cookies=token_cookie
        )

        assert resp.status_code == status_codes.HTTP_200_OK, resp.json()

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

        resp = resp.json()
        assert resp.get("current_streak_start_date") == TODAY_DATE
        assert resp.get("current_streak_days") == 1
        assert resp.get("max_streak_days") == 1

    async def test_get_habit_statistics(
        self,
        signin_fixture,
        update_habit_fixture,
        auth_data: UserDTO,
        token_cookie: dict,
        habit_data: HabitDTO,
        test_client_with_db: AsyncTestClient[Litestar],
    ):

        params = {"title": habit_data.title}

        resp: Response[HabitReturnDTO] = await test_client_with_db.get(
            "/api/habits/statistics", params=params, cookies=token_cookie
        )

        assert resp.status_code == status_codes.HTTP_200_OK, resp.json()

        resp = resp.json()
        assert resp.get("title") == habit_data.title
        assert resp.get("count") == habit_data.count
        assert resp.get("period") == habit_data.period
        assert resp.get("period_in_days") == habit_data.period_in_days
        assert resp.get("current_count") == 1
        assert resp.get("dates_in_period") == [TODAY_DATE]
        assert resp.get("current_streak_start_date") == TODAY_DATE
        assert resp.get("current_streak_days") == 1
        assert resp.get("max_streak_days") == 1
