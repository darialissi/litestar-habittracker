from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from domain.models.habit import Habit


class HabitRepository(SQLAlchemyAsyncRepository[Habit]):

    model_type = Habit
