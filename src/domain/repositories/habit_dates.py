from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from domain.models.habit_dates import HabitDates


class HabitDatesRepository(SQLAlchemyAsyncRepository[HabitDates]):

    model_type = HabitDates
