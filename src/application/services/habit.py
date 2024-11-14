from datetime import timedelta

from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from application.schemas.habit import HabitDTO


class HabitService:

    def __init__(self, repo: SQLAlchemyAsyncRepository):
        self.habit_repo = repo

    async def add_habit(self, habit: HabitDTO):
        pass

    async def get_habit(self, **filters):
        habit = await self.habit_repo.get_one_or_none(**filters)
        return habit

    async def get_all_habits(self, **filters):
        habits = await self.habit_repo.list_and_count(**filters)
        return habits
