from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class TournamentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    max_players: int = Field(ge=1, le=10_000)
    start_at: datetime


class TournamentOut(BaseModel):
    id: int
    name: str
    max_players: int
    start_at: datetime
    registered_players: int

    model_config = ConfigDict(from_attributes=True)


class PlayerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr


class PlayerOut(BaseModel):
    name: str
    email: EmailStr
