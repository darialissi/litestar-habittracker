from datetime import date, datetime, timedelta, timezone

from advanced_alchemy.filters import LimitOffset, OrderBy
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from application.schemas.habit import HabitDTO
from application.services import errors
from domain.models.habit import Habit
from domain.models.habit_dates import HabitDates


class HabitService:

    def __init__(self, repo: SQLAlchemyAsyncRepository, dates_repo: SQLAlchemyAsyncRepository):
        self.habit_repo = repo
        self.habit_dates_repo = dates_repo

    async def add_habit(self, habit: HabitDTO, user_fk: str) -> Habit:
        h_dict = habit.model_dump()
        h_dict.update({"author": user_fk})
        habit = await self.habit_repo.add(self.habit_repo.model_type(**h_dict))
        await self.habit_repo.session.commit()
        return habit

    async def update_habit_streak(self, habit: Habit) -> Habit:
        today = datetime.now(timezone.utc).date()

        # Добавляем дату выполнения привычки в отдельную таблицу
        new_date = self.habit_dates_repo.model_type(title=habit.title, completed_at=today)
        await self.habit_dates_repo.add(new_date)

        # Обновляем кол-во подряд выполненных дней и дату начала текущей непрерывной серии
        if habit.current_streak_days > 0:
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

    async def get_habit_date(self, title: str, completed_at: date) -> HabitDates | None:
        habit_date = await self.habit_dates_repo.get_one_or_none(
            title=title, completed_at=completed_at
        )
        return habit_date

    async def get_habit_dates_desc(self, title: str, limit: int | None = None) -> list[HabitDates]:
        filters = [
            OrderBy(field_name=self.habit_dates_repo.model_type.completed_at, sort_order="desc"),
            LimitOffset(limit=limit, offset=0),
        ]

        habit_dates = await self.habit_dates_repo.list(*filters, title=title)
        return habit_dates

    async def update_habit(self, data: HabitDTO, username: str) -> Habit:

        if not (habit := await self.get_habit(title=data.title, author=username)):
            raise errors.HabitNotFoundError(title=data.title, username=username)

        existed_record = await self.get_habit_date(
            title=habit.title, completed_at=datetime.now(timezone.utc).date()
        )
        if existed_record:
            raise errors.HabitAlreadyCompletedTodayError(
                title=habit.title, completed_at=existed_record.completed_at
            )

        return await self.update_habit_streak(habit)

    async def get_current_period_habit_dates(
        self, title: str, author: str
    ) -> tuple[Habit, HabitDates]:
        habit = await self.get_habit(title=title, author=author)
        if not habit:
            raise errors.HabitNotFoundError(title=title, username=author)

        habit_dates = await self.get_habit_dates_desc(title=title, limit=habit.period_in_days)

        return habit, habit_dates
