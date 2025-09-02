from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, BigInteger, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, declared_attr


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        __name = cls.__name__[:1]
        for i in cls.__name__[1:]:
            if i.isupper():
                __name += '_'
            __name += i
        __name = __name.lower()

        if __name.endswith('y'):
            __name = __name[:-1] + 'ie'
        return __name + 's'


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class TimeBasedModel(BaseModel):
    __abstract__ = True
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now())
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())


class Tournament(TimeBasedModel):
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    max_players: Mapped[int] = mapped_column(nullable=False)
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    players: Mapped[list["Player"]] = relationship(back_populates="tournament", cascade="all, delete-orphan")

    @property
    def registered_players(self) -> int:
        return len(self.players)


class Player(TimeBasedModel):
    __table_args__ = (UniqueConstraint("tournament_id", "email", name="uq_player_email_per_tournament"),)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False, index=True)

    tournament_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id", ondelete="CASCADE"), nullable=False)
    tournament: Mapped[Tournament] = relationship(back_populates="players")
