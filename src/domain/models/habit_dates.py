from datetime import date

from litestar.contrib.sqlalchemy.base import BigIntAuditBase
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class HabitDates(BigIntAuditBase):
    __tablename__ = "habit_dates"
    __table_args__ = (UniqueConstraint("habit_id", "completed_at", name="uq_habit_date"),)

    completed_at: Mapped[date] = mapped_column(nullable=False)

    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"))

    habit: Mapped["Habit"] = relationship(back_populates="habit_dates")  # type: ignore # noqa: F821
