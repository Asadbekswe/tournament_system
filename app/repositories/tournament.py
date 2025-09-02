from __future__ import annotations

from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tournament import Player, Tournament


class TournamentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_tournament(self, name: str, max_players: int, start_at) -> Tournament:
        t = Tournament(name=name, max_players=max_players, start_at=start_at)
        self.session.add(t)
        await self.session.commit()
        await self.session.refresh(t)
        return t

    async def get_tournament_for_update(self, tournament_id: int) -> Tournament | None:
        stmt = select(Tournament).where(Tournament.id == tournament_id).with_for_update()
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def count_players(self, tournament_id: int) -> int:
        stmt = select(func.count(Player.id)).where(Player.tournament_id == tournament_id)
        res = await self.session.execute(stmt)
        return int(res.scalar_one() or 0)

    async def list_players(self, tournament_id: int) -> Sequence[Player]:
        res = await self.session.execute(
            select(Player).where(Player.tournament_id == tournament_id).order_by(Player.id))
        return list(res.scalars().all())

    async def add_player(self, tournament_id: int, name: str, email: str) -> Player:
        p = Player(name=name, email=email, tournament_id=tournament_id)
        self.session.add(p)
        await self.session.commit()
        await self.session.refresh(p)
        return p
