from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tournament import Tournament
from app.repositories.tournament import TournamentRepository


class TournamentService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = TournamentRepository(session)

    async def create_tournament(self, name: str, max_players: int, start_at) -> Tournament:
        return await self.repo.create_tournament(name=name, max_players=max_players, start_at=start_at)

    async def register_player(self, tournament_id: int, name: str, email: str) -> None:
        async with self.repo.session.begin():
            t = await self.repo.get_tournament_for_update(tournament_id)
            if not t:
                raise ValueError("Tournament not found")

            current = await self.repo.count_players(tournament_id)
            if current >= t.max_players:
                raise RuntimeError("Players limit reached")

            await self.repo.add_player(tournament_id, name, email)

    async def list_players(self, tournament_id: int):
        t = await self.repo.get_tournament_for_update(tournament_id)
        if not t:
            raise ValueError("Tournament not found")
        return await self.repo.list_players(tournament_id)
