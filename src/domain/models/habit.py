from datetime import date, datetime, timezone

from litestar.contrib.sqlalchemy.base import BigIntAuditBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Habit(BigIntAuditBase):
    __tablename__ = "habits"

    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    count: Mapped[int] = mapped_column(default=1)  # const: n times
    period: Mapped[str] = mapped_column(default="WEEKLY")  # const: period type (weekly, monthly)
    period_in_days: Mapped[int] = mapped_column(default=7)  # const: period in days

    current_streak_start_date: Mapped[date] = mapped_column(
        default=lambda: datetime.now(timezone.utc).date()
    )  # дата начала текущей серии подряд выполненных дней
    current_streak_days: Mapped[int] = mapped_column(default=0)  # подряд выполненных дней
    max_streak_days: Mapped[int] = mapped_column(default=0)  # максимум подряд выполненных дней

    author: Mapped[str] = mapped_column(ForeignKey("users.username", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="habits")  # type: ignore # noqa: F821
    habit_dates: Mapped[set["HabitDates"]] = relationship(back_populates="habit")  # type: ignore # noqa: F821
