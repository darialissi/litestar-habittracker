from datetime import datetime, timedelta, timezone

from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from application.schemas.habit import HabitDTO, HabitReturnDTO


class HabitService:

    def __init__(self, repo: SQLAlchemyAsyncRepository):
        self.habit_repo = repo

    async def add_habit(self, habit: HabitDTO, user_fk: str):
        h_dict = habit.model_dump()
        h_dict.update({"author": user_fk})
        habit = await self.habit_repo.add(self.habit_repo.model_type(**h_dict))
        await self.habit_repo.session.commit()
        return habit

    async def update_habit_strike(self, habit: HabitReturnDTO):
        today = datetime.now(timezone.utc)

        if habit.current_strike_start_date.date() + timedelta(days=1) == today.date() or (
            habit.current_strike_start_date.date() != today.date() and habit.current_strike_days > 0
        ):

            habit.current_strike_days += 1

        else:
            habit.current_strike_start_date = today
            habit.current_strike_days = 1

        habit.max_strike_days = max(habit.max_strike_days, habit.current_strike_days)

        habit = await self.habit_repo.update(self.habit_repo.model_type(**habit.model_dump()))
        await self.habit_repo.session.commit()
        return habit

    async def get_habit(self, **filters):
        habit = await self.habit_repo.get_one_or_none(**filters)
        return habit

    async def get_all_habits(self, **filters):
        habits = await self.habit_repo.list(**filters)
        return habits
