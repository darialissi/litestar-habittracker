from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from domain.models.habit_dates import HabitDates


class HabitDatesRepository(SQLAlchemyAsyncRepository[HabitDates]):

    model_type = HabitDates
