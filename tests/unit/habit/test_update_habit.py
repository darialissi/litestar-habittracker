import unittest.mock
from datetime import datetime

import pytest
from pydantic import BaseModel, ConfigDict

from application.schemas.habit import HabitReturnDTO
from application.services import errors
from application.services.habit import HabitService
from domain.models.habit import Habit
from domain.models.habit_dates import HabitDates

HABIT = Habit(id=0)
RECORD = HabitDates(id=0, completed_at=datetime.today())


class Case(BaseModel):
    get_habit_response: Habit | None = None
    get_habit_date_response: HabitDates | None = None
    update_habit_streak_response: Habit | None = None
    is_expected_habit: bool = False

    model_config = ConfigDict(arbitrary_types_allowed=True)


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.validation
@pytest.mark.parametrize(
    "test_case",
    [
        pytest.param(
            Case(
                get_habit_response=HABIT,
                get_habit_date_response=None,
                update_habit_streak_response=HABIT,
                is_expected_habit=True,
            ),
            id="OK",
        ),
        pytest.param(
            Case(
                get_habit_response=None,
                get_habit_date_response=None,
                update_habit_streak_response=None,
                is_expected_habit=False,
            ),
            id="FAIL: habit not found",
            marks=pytest.mark.xfail(raises=errors.HabitNotFoundError),
        ),
        pytest.param(
            Case(
                get_habit_response=HABIT,
                get_habit_date_response=RECORD,
                update_habit_streak_response=None,
                is_expected_habit=False,
            ),
            id="FAIL: existed record",
            marks=pytest.mark.xfail(raises=errors.HabitAlreadyCompletedTodayError),
        ),
    ],
)
async def test_update_habit(
    test_case: Case,
    habit_service: HabitService,
    habit_data: HabitReturnDTO,
):

    with (
        unittest.mock.patch.object(
            target=HabitService,
            attribute=HabitService.get_habit.__name__,
            new=unittest.mock.AsyncMock(return_value=test_case.get_habit_response),
        ),
        unittest.mock.patch.object(
            target=HabitService,
            attribute=HabitService.get_habit_date.__name__,
            new=unittest.mock.AsyncMock(return_value=test_case.get_habit_date_response),
        ),
        unittest.mock.patch.object(
            target=HabitService,
            attribute=HabitService.update_habit_streak.__name__,
            new=unittest.mock.AsyncMock(return_value=test_case.update_habit_streak_response),
        ),
    ):

        resp: Habit = await habit_service.update_habit(
            data=habit_data,
            username="testuser",
        )

        if test_case.is_expected_habit:
            assert resp
        else:
            assert resp is None
