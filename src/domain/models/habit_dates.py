from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .common import BaseWithoutID


class HabitDates(BaseWithoutID):
    __tablename__ = "habit_dates"

    completed_at: Mapped[date] = mapped_column(nullable=False, primary_key=True)

    title: Mapped[str] = mapped_column(
        ForeignKey("habits.title", ondelete="CASCADE"), primary_key=True
    )

    habit: Mapped["Habit"] = relationship(back_populates="habit_dates")  # type: ignore # noqa: F821
