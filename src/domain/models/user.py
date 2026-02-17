from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(BigIntAuditBase):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    habits: Mapped[set["Habit"]] = relationship(back_populates="user")  # type: ignore # noqa: F821
    habit_dates: Mapped[set["HabitDates"]] = relationship(back_populates="user")  # type: ignore # noqa: F821
