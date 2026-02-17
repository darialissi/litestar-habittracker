from datetime import datetime, timezone

import pytest
from httpx import Response
from litestar import Litestar, status_codes
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

        response: Response[HabitReturnDTO] = await test_client_with_db.post(
            "/api/habits", data=habit_data.model_dump_json(), cookies=token_cookie
        )

        assert response.status_code == status_codes.HTTP_201_CREATED, response.json()

        payload: dict = response.json()["payload"]

        assert payload.get("id") == 1
        assert payload.get("author") == auth_data.username
        assert payload.get("title") == habit_data.title
        assert payload.get("count") == habit_data.count
        assert payload.get("period_in_days") == habit_data.period_in_days
        assert payload.get("current_streak_days") == 0
        assert payload.get("max_streak_days") == 0

    async def test_get_habit(
        self,
        signin_fixture,
        auth_data: UserDTO,
        token_cookie: dict,
        habit_data: HabitDTO,
        test_client_with_db: AsyncTestClient[Litestar],
    ):

        response: Response[HabitReturnDTO] = await test_client_with_db.get(
            "/api/habits", cookies=token_cookie
        )

        assert response.status_code == status_codes.HTTP_404_NOT_FOUND, response.json()
        assert response.json()["errors"]

        await test_client_with_db.post(
            "/api/habits", data=habit_data.model_dump_json(), cookies=token_cookie
        )

        response: Response[HabitReturnDTO] = await test_client_with_db.get(
            "/api/habits", cookies=token_cookie
        )

        assert response.status_code == status_codes.HTTP_200_OK, response.json()

    async def test_update_habit(
        self,
        signin_fixture,
        add_habit_fixture,
        auth_data: UserDTO,
        token_cookie: dict,
        habit_counter_data: HabitCounterUpdateDTO,
        test_client_with_db: AsyncTestClient[Litestar],
    ):

        response: Response[HabitReturnDTO] = await test_client_with_db.patch(
            "/api/habits", data=habit_counter_data.model_dump_json(), cookies=token_cookie
        )

        assert response.status_code == status_codes.HTTP_200_OK, response.json()

        payload: dict = response.json()["payload"]
        assert payload.get("current_streak_start_date") == TODAY_DATE
        assert payload.get("current_streak_days") == 1
        assert payload.get("max_streak_days") == 1

        response: Response[HabitReturnDTO] = await test_client_with_db.patch(
            "/api/habits", data=habit_counter_data.model_dump_json(), cookies=token_cookie
        )

        assert response.status_code == status_codes.HTTP_400_BAD_REQUEST, response.json()
        assert response.json()["errors"]

    async def test_update_habit_not_found(
        self,
        signin_fixture,
        auth_data: UserDTO,
        token_cookie: dict,
        habit_counter_data: HabitCounterUpdateDTO,
        test_client_with_db: AsyncTestClient[Litestar],
    ):

        response: Response[HabitReturnDTO] = await test_client_with_db.patch(
            "/api/habits", data=habit_counter_data.model_dump_json(), cookies=token_cookie
        )

        assert response.status_code == status_codes.HTTP_404_NOT_FOUND, response.json()

        assert response.json()["errors"]
        assert not response.json()["payload"]

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

        response: Response[HabitReturnDTO] = await test_client_with_db.get(
            "/api/habits/statistics", params=params, cookies=token_cookie
        )

        assert response.status_code == status_codes.HTTP_200_OK, response.json()

        payload: dict = response.json()["payload"]

        assert payload.get("title") == habit_data.title
        assert payload.get("count") == habit_data.count
        assert payload.get("period") == habit_data.period
        assert payload.get("period_in_days") == habit_data.period_in_days
        assert payload.get("current_period_count") == 1
        assert payload.get("completed_at_dates") == [TODAY_DATE]
        assert payload.get("current_streak_start_date") == TODAY_DATE
        assert payload.get("current_streak_days") == 1
        assert payload.get("max_streak_days") == 1

    async def test_get_habit_statistics_not_found(
        self,
        signin_fixture,
        auth_data: UserDTO,
        token_cookie: dict,
        test_client_with_db: AsyncTestClient[Litestar],
    ):

        params = {"title": "unknown"}

        response: Response[HabitReturnDTO] = await test_client_with_db.get(
            "/api/habits/statistics", params=params, cookies=token_cookie
        )

        assert response.status_code == status_codes.HTTP_404_NOT_FOUND, response.json()

        assert response.json()["errors"]
        assert not response.json()["payload"]

    async def test_get_habits_overall(
        self,
        signin_fixture,
        update_habit_fixture,
        auth_data: UserDTO,
        token_cookie: dict,
        habit_data: HabitDTO,
        test_client_with_db: AsyncTestClient[Litestar],
    ):

        params = {"days": 5}

        response: Response[HabitReturnDTO] = await test_client_with_db.get(
            "/api/habits/overall", params=params, cookies=token_cookie
        )

        assert response.status_code == status_codes.HTTP_200_OK, response.json()

        payload: dict = response.json()["payload"]

        assert isinstance(payload.get("habits"), list)
        assert len(payload["habits"]) == 1
