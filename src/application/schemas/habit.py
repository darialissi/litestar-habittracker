from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HabitDTO(BaseModel):
    """
    Схема модели Habit, валидирует ввод
    """

    title: str

    model_config = ConfigDict(from_attributes=True)


class HabitReturnDTO(BaseModel):
    """
    Общая схема модели Habit, валидирует вывод
    """

    id: int
    title: str
    current_strike_days: int = Field(default=0, ge=0)
    max_strike_days: int = Field(default=0, ge=0)
    created_at: datetime
    updated_at: datetime

    user_id: int

    model_config = ConfigDict(from_attributes=True)
