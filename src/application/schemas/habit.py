from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from application.schemas import enums


class HabitDTO(BaseModel):
    """
    Схема модели Habit, валидирует ввод при добавлении новой привычки
    """

    title: str = Field(min_length=2, max_length=50, description="Название привычки")
    count: int = Field(
        ge=1, default=1, description="Установленное количество выполнений привычки в заданном периоде"
    )
    period: Literal["WEEKLY", "MONTHLY"] = Field(
        default=enums.Period.WEEKLY.name,
        description="Период, за который нужно выполнить привычку заданное кол-во раз",
    )

    @property
    def period_in_days(self):
        return enums.Period[self.period].value

    model_config = ConfigDict(from_attributes=True)


class HabitCounterUpdateDTO(BaseModel):
    """
    Схема модели Habit, валидирует ввод при обновлении счетчика привычки
    """

    title: str = Field(min_length=2, max_length=50, description="Название привычки")

    model_config = ConfigDict(from_attributes=True)


class HabitStatisticsReturn(BaseModel):
    """
    Схема модели Habit, валидирует вывод общей статистики
    """

    title: str = Field(description="Название привычки")
    count: int = Field(
        description="Установленное количество выполнений привычки в заданном периоде"
    )
    period: str = Field(
        description="Установленный период, за который нужно выполнить привычку заданное кол-во раз"
    )
    period_in_days: int = Field(
        description="Установленный период в днях, за который нужно выполнить привычку заданное кол-во раз"
    )
    # statistics fields
    current_count: int = Field(
        description="Количество выполнений привычки в текущем периоде (скользящее окно)"
    )
    dates_in_period: list[date] = Field(
        description="Список дат выполнения привычки в текущем периоде (скользящее окно)"
    )
    current_streak_start_date: date = Field(
        description="Дата начала текущей непрерывной серии выполнения привычки"
    )
    current_streak_days: int = Field(
        ge=0, description="Количество дней в текущей непрерывной серии выполнения привычки"
    )
    max_streak_days: int = Field(
        ge=0, description="Максимальное количество дней в непрерывной серии выполнения привычки"
    )

    model_config = ConfigDict(from_attributes=True)


class HabitReturnDTO(BaseModel):
    """
    Общая схема модели Habit, валидирует вывод
    """

    id: int = Field(description="ID привычки")
    title: str = Field(description="Название привычки")
    count: int = Field(
        description="Установленное количество выполнений привычки в заданном периоде"
    )
    period: str = Field(
        description="Установленный период, за который нужно выполнить привычку заданное кол-во раз"
    )
    period_in_days: int = Field(
        description="Период в днях, за который нужно выполнить привычку заданное кол-во раз"
    )
    current_streak_start_date: date = Field(
        description="Дата начала текущей непрерывной серии выполнения привычки"
    )
    current_streak_days: int = Field(
        ge=0, description="Количество дней в текущей непрерывной серии выполнения привычки"
    )
    max_streak_days: int = Field(
        ge=0, description="Максимальное количество дней в непрерывной серии выполнения привычки"
    )
    created_at: datetime = Field(description="Дата создания привычки")
    updated_at: datetime = Field(description="Дата последнего обновления привычки")

    author: str = Field(description="Автор привычки")

    model_config = ConfigDict(from_attributes=True)
