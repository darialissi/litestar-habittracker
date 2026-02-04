import unittest.mock

import pytest

from application.schemas.habit import HabitReturnDTO
from application.services import errors
from application.services.habit import HabitService
from domain.models.habit import Habit

HABIT = Habit(title="test habit")


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.validation
@pytest.mark.parametrize(
    """
    get_habit_response,
    update_habit_strike_response,
    is_expected_habit
    """,
    [
        pytest.param(
            HABIT,
            HABIT,
            True,
            id="OK",
        ),
        pytest.param(
            None,
            None,
            False,
            id="FAIL: habit not found",
            marks=pytest.mark.xfail(raises=errors.HabitNotFoundError),
        ),
    ],
)
async def test_update_habit(
    get_habit_response: Habit | None,
    update_habit_strike_response: Habit,
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
            attribute=HabitService.update_habit_strike.__name__,
            new=unittest.mock.AsyncMock(return_value=update_habit_strike_response),
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
