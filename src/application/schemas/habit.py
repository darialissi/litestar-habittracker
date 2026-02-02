from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HabitDTO(BaseModel):
    """
    Схема модели Habit, валидирует ввод
    """

    title: str = Field(min_length=5)

    model_config = ConfigDict(from_attributes=True)


class HabitReturnDTO(BaseModel):
    """
    Общая схема модели Habit, валидирует вывод
    """

    id: int
    title: str
    current_streak_start_date: datetime
    current_streak_days: int = Field(ge=0)
    max_streak_days: int = Field(ge=0)
    created_at: datetime
    updated_at: datetime

    author: str

    model_config = ConfigDict(from_attributes=True)
