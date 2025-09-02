from datetime import datetime

from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimeBasedModel


class Tournament(TimeBasedModel):
    name: Mapped[str] = mapped_column(String(), nullable=False)
    email: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    start_at: Mapped[datetime] = mapped_column(DateTime())
    max_players: Mapped[int] = mapped_column(Integer(), default=0)


class Player(TimeBasedModel):
    pass
