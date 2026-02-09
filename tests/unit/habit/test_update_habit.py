import unittest.mock
from datetime import datetime

import pytest

from application.schemas.habit import HabitReturnDTO
from application.services import errors
from application.services.habit import HabitService
from domain.models.habit import Habit
from domain.models.habit_dates import HabitDates

HABIT = Habit(id=0)
RECORD = HabitDates(id=0, completed_at=datetime.today())


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.validation
@pytest.mark.parametrize(
    """
    get_habit_response,
    get_habit_date_response,
    update_habit_streak_response,
    is_expected_habit
    """,
    [
        pytest.param(
            HABIT,
            None,
            HABIT,
            True,
            id="OK",
        ),
        pytest.param(
            None,
            None,
            None,
            False,
            id="FAIL: habit not found",
            marks=pytest.mark.xfail(raises=errors.HabitNotFoundError),
        ),
        pytest.param(
            HABIT,
            RECORD,
            None,
            False,
            id="FAIL: existed record",
            marks=pytest.mark.xfail(raises=errors.HabitAlreadyCompletedTodayError),
        ),
    ],
)
async def test_update_habit(
    get_habit_response: Habit | None,
    get_habit_date_response: HabitDates | None,
    update_habit_streak_response: Habit | None,
    is_expected_habit: bool,
    habit_service: HabitService,
    habit_data: HabitReturnDTO,
):

    with (
        unittest.mock.patch.object(
            target=HabitService,
            attribute=HabitService.get_habit.__name__,
            new=unittest.mock.AsyncMock(return_value=get_habit_response),
        ),
        unittest.mock.patch.object(
            target=HabitService,
            attribute=HabitService.get_habit_date.__name__,
            new=unittest.mock.AsyncMock(return_value=get_habit_date_response),
        ),
        unittest.mock.patch.object(
            target=HabitService,
            attribute=HabitService.update_habit_streak.__name__,
            new=unittest.mock.AsyncMock(return_value=update_habit_streak_response),
        ),
    ):

        resp: Habit = await habit_service.update_habit(
            data=habit_data,
            username="testuser",
        )

        if is_expected_habit:
            assert resp
        else:
            assert resp is None
