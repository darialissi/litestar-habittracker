from uuid import UUID

from litestar.contrib.sqlalchemy.base import BigIntAuditBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Habit(BigIntAuditBase):
    __tablename__ = "habits"

    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    current_strike_days: Mapped[int]
    max_strike_days: Mapped[int]

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="habits")  # type: ignore # noqa: F821
