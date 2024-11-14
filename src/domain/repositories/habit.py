from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from domain.models.habit import Habit


class HabitRepository(SQLAlchemyAsyncRepository[Habit]):

    model_type = Habit
