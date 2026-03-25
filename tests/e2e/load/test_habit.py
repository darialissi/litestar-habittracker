import asyncio
import time

import pytest
from litestar import Litestar, status_codes
from litestar.testing import AsyncTestClient

from application.schemas.habit import HabitDTO
from application.schemas.user import UserDTO

from .utils import percentile


@pytest.mark.asyncio
@pytest.mark.load
class TestHabitLoad:

    async def test_add_habit_load(
        self,
        signin_fixture,
        auth_data: UserDTO,
        token_cookie: dict,
        habit_data: HabitDTO,
        test_client_with_db: AsyncTestClient[Litestar],
    ):
        requests_count = 100
        concurrency = 10
        semaphore = asyncio.Semaphore(concurrency)

        timings = []
        statuses = []

        async def create_habit(i: int):
            async with semaphore:
                payload = habit_data.model_copy(update={"title": f"habit_{i}"})

                start = time.perf_counter()
                response = await test_client_with_db.post(
                    "/api/habits",
                    data=payload.model_dump_json(),
                    cookies=token_cookie,
                )
                elapsed = (time.perf_counter() - start) * 1000

                timings.append(elapsed)
                statuses.append(response.status_code)

        started = time.perf_counter()
        await asyncio.gather(*(create_habit(i) for i in range(requests_count)))
        total_time = time.perf_counter() - started

        success_count = sum(1 for s in statuses if s == status_codes.HTTP_201_CREATED)
        error_count = requests_count - success_count

        success_rate = success_count / requests_count * 100
        error_rate = error_count / requests_count * 100
        rps = requests_count / total_time

        p95 = percentile(timings, 95)
        p99 = percentile(timings, 99)

        assert success_rate == 100, f"success_rate={success_rate:.2f}%"
        assert error_rate == 0, f"error_rate={error_rate:.2f}%"
        assert p95 <= 10, f"p95={p95:.2f}ms"
        assert p99 <= 20, f"p99={p99:.2f}ms"

        print(
            f"concurrency={concurrency}, "
            f"success_rate={success_rate:.2f}%, "
            f"error_rate={error_rate:.2f}%, "
            f"p95={p95:.2f}ms, "
            f"p99={p99:.2f}ms, "
            f"rps={rps:.2f}"
        )
