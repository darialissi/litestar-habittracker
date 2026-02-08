import pytest

from application.schemas.enums import Period


@pytest.fixture
def add_habit_resp_dict(auth_data: dict) -> dict:
    return dict(
        id=1,
        title="test habit",
        count=2,
        period=Period.WEEKLY.name,
        period_in_days=7,
        current_count=0,
        current_streak_start_date="2025-01-01T00:00:00",
        current_streak_days=0,
        max_streak_days=0,
        created_at="2025-01-01T00:00:00",
        updated_at="2025-01-01T00:00:00",
        author=auth_data.username,
    )


@pytest.fixture
def update_habit_resp_dict(add_habit_resp_dict: dict) -> dict:
    habit = dict(add_habit_resp_dict)  # copy
    habit["current_count"] = 1
    habit["current_streak_days"] = 1
    habit["current_streak_start_date"] = "2025-01-02T00:00:00"
    habit["max_streak_days"] = 1
    habit["updated_at"] = "2025-01-02T00:00:00"
    return habit
