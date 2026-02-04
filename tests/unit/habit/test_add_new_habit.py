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
    add_habit_response,
    is_expected_habit
    """,
    [
        pytest.param(
            None,
            HABIT,
            True,
            id="OK",
        ),
        pytest.param(
            HABIT,
            None,
            False,
            id="FAIL: habit already exists",
            marks=pytest.mark.xfail(raises=errors.HabitAlreadyExistsError),
        ),
    ],
)
async def test_add_new_habit(
    get_habit_response: Habit | None,
    add_habit_response: Habit | None,
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
            attribute=HabitService.add_habit.__name__,
            new=unittest.mock.AsyncMock(return_value=add_habit_response),
        ),
    ):

        resp: Habit = await habit_service.add_new_habit(
            data=habit_data,
            username="testuser",
        )

        if is_expected_habit:
            assert resp
        else:
            assert resp is None
