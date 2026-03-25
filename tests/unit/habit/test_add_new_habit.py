import unittest.mock

import pytest
from pydantic import BaseModel, ConfigDict

from application.schemas.habit import HabitReturnDTO
from application.services import errors
from application.services.habit import HabitService
from domain.models.habit import Habit

HABIT = Habit(title="test habit")


class Case(BaseModel):
    get_habit_response: Habit | None = None
    add_habit_response: Habit | None = None
    is_expected_habit: bool = False

    model_config = ConfigDict(arbitrary_types_allowed=True)


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.validation
@pytest.mark.parametrize(
    "test_case",
    [
        pytest.param(
            Case(get_habit_response=None, add_habit_response=HABIT, is_expected_habit=True),
            id="OK",
        ),
        pytest.param(
            Case(get_habit_response=HABIT, add_habit_response=None, is_expected_habit=False),
            id="FAIL: habit already exists",
            marks=pytest.mark.xfail(raises=errors.HabitAlreadyExistsError),
        ),
    ],
)
async def test_add_new_habit(
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
            attribute=HabitService.add_habit.__name__,
            new=unittest.mock.AsyncMock(return_value=test_case.add_habit_response),
        ),
    ):

        resp: Habit = await habit_service.add_new_habit(
            data=habit_data,
            username="testuser",
        )

        if test_case.is_expected_habit:
            assert resp
        else:
            assert resp is None
