from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.tournament import PlayerCreate, PlayerOut, TournamentCreate, TournamentOut
from app.services.tournament import TournamentService

router = APIRouter(prefix="/tournaments", tags=["tournaments"])


@router.post("", response_model=TournamentOut, status_code=status.HTTP_201_CREATED)
async def create_tournament(payload: TournamentCreate, session: AsyncSession = Depends(get_session)):
    svc = TournamentService(session)
    t = await svc.create_tournament(payload.name, payload.max_players, payload.start_at)
    return TournamentOut(
        id=t.id,
        name=t.name,
        max_players=t.max_players,
        start_at=t.start_at,
        registered_players=0,
    )


@router.post("/{tournament_id}/register", status_code=status.HTTP_204_NO_CONTENT)
async def register_player(tournament_id: int, payload: PlayerCreate, session: AsyncSession = Depends(get_session)):
    svc = TournamentService(session)
    try:
        await svc.register_player(tournament_id, payload.name, str(payload.email))
    except ValueError:
        raise HTTPException(status_code=404, detail="Tournament not found")
    except KeyError:
        raise HTTPException(status_code=400, detail="Email already registered")
    except RuntimeError:
        raise HTTPException(status_code=400, detail="Players limit reached")
    return None


@router.get("/{tournament_id}/players", response_model=list[PlayerOut])
async def list_players(tournament_id: int, session: AsyncSession = Depends(get_session)):
    svc = TournamentService(session)
    try:
        players = await svc.list_players(tournament_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return [PlayerOut(name=p.name, email=p.email) for p in players]
