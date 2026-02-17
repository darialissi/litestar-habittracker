from datetime import date, datetime, timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from application.schemas import enums


class HabitDTO(BaseModel):
    """
    Схема модели Habit, валидирует ввод при добавлении новой привычки
    """

    title: str = Field(min_length=2, max_length=50, description="Название привычки")
    count: int = Field(
        ge=1,
        default=1,
        description="Установленное количество выполнений привычки в заданном периоде",
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


class ExtendedHabitReturnDTO(BaseModel):
    """
    Расширенная схема модели Habit, включает в себя данные HabitDates, валидирует вывод
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
    current_streak_start_date: date = Field(
        description="Дата начала текущей непрерывной серии выполнения привычки"
    )
    current_streak_days: int = Field(
        ge=0, description="Количество дней в текущей непрерывной серии выполнения привычки"
    )
    max_streak_days: int = Field(
        ge=0, description="Максимальное количество дней в непрерывной серии выполнения привычки"
    )

    completed_at_dates: list[date] = Field(description="Список дат, когда привычка была выполнена")
    current_period_count: int = Field(
        description="Количество выполнений привычки в текущем периоде", default=0
    )

    created_at: datetime = Field(description="Дата создания привычки")
    updated_at: datetime = Field(description="Дата последнего обновления привычки")

    @model_validator(mode="after")
    def set_current_count(self):
        self.completed_at_dates.sort(reverse=True)

        # Вычисляем кол-во выполнений в текущем периоде
        today = datetime.now().date()
        period_start_date = today - timedelta(days=self.period_in_days)

        self.current_period_count = 0
        for completed_date in self.completed_at_dates:
            if completed_date < period_start_date:
                break
            self.current_period_count += 1

        return self

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
