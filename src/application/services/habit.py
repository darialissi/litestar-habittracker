from datetime import datetime, timedelta, timezone

from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from application.schemas.habit import HabitDTO
from application.services import errors
from domain.models.habit import Habit


class HabitService:

    def __init__(self, repo: SQLAlchemyAsyncRepository):
        self.habit_repo = repo

    async def add_habit(self, habit: HabitDTO, user_fk: str) -> Habit:
        h_dict = habit.model_dump()
        h_dict.update({"author": user_fk})
        habit = await self.habit_repo.add(self.habit_repo.model_type(**h_dict))
        await self.habit_repo.session.commit()
        return habit

    async def update_habit_strike(self, habit: Habit) -> Habit:
        today = datetime.now(timezone.utc)

        # Обновляем кол-во подряд выполненных дней и дату начала текущей серии
        if habit.current_streak_start_date.date() + timedelta(days=1) == today.date() or (
            habit.current_streak_start_date.date() != today.date() and habit.current_streak_days > 0
        ):

            habit.current_streak_days += 1

        else:
            habit.current_streak_start_date = today
            habit.current_streak_days = 1

        habit.max_streak_days = max(habit.max_streak_days, habit.current_streak_days)

        updated = await self.habit_repo.update(habit)
        await self.habit_repo.session.commit()
        return updated

    async def get_habit(self, **filters) -> Habit | None:
        habit = await self.habit_repo.get_one_or_none(**filters)
        return habit

    async def get_all_habits(self, **filters) -> list[Habit]:
        habits = await self.habit_repo.list(**filters)
        return habits

    async def add_new_habit(self, data: HabitDTO, username: str) -> Habit:

        if await self.get_habit(title=data.title, author=username):
            raise errors.HabitAlreadyExistsError(title=data.title, username=username)

        return await self.add_habit(data, user_fk=username)

    async def update_habit(self, data: HabitDTO, username: str) -> Habit:

        if not (habit := await self.get_habit(title=data.title, author=username)):
            raise errors.HabitNotFoundError(title=data.title, username=username)

        return await self.update_habit_strike(habit)
