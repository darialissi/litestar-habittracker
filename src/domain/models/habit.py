from datetime import datetime, timezone

from litestar.contrib.sqlalchemy.base import BigIntAuditBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Habit(BigIntAuditBase):
    __tablename__ = "habits"

    title: Mapped[str] = mapped_column(nullable=False)

    current_strike_start_date: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    current_strike_days: Mapped[int] = mapped_column(default=0)
    max_strike_days: Mapped[int] = mapped_column(default=0)

    author: Mapped[str] = mapped_column(ForeignKey("users.username", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="habits")  # type: ignore # noqa: F821
