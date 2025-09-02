from typing import AsyncIterator
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.db import get_session
from app.main import app
from app.models.tournament import Base

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@pytest.fixture(scope="function", autouse=True)
async def clear_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def override_get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.mark.anyio
async def test_register_flow():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # create tournament
        resp = await client.post(
            "/tournaments",
            json={"name": "Weekend Cup", "max_players": 2, "start_at": "2025-06-01T15:00:00Z"},
        )
        assert resp.status_code == 201
        tid = resp.json()["id"]

        # first registration ok
        r1 = await client.post(f"/tournaments/{tid}/register", json={"name": "John", "email": "john@example.com"})
        assert r1.status_code == 204

        # duplicate email -> 400
        rdup = await client.post(f"/tournaments/{tid}/register", json={"name": "John 2", "email": "john@example.com"})
        assert rdup.status_code == 400
        assert rdup.json()["detail"] == "Email already registered"

        # second different email ok
        r2 = await client.post(f"/tournaments/{tid}/register", json={"name": "Mary", "email": "mary@example.com"})
        assert r2.status_code == 204

        # limit reached
        r3 = await client.post(f"/tournaments/{tid}/register", json={"name": "Max", "email": "max@example.com"})
        assert r3.status_code == 400
        assert r3.json()["detail"] == "Players limit reached"

        # list players
        lst = await client.get(f"/tournaments/{tid}/players")
        assert lst.status_code == 200
        data = lst.json()
        assert len(data) == 2
        assert {d["email"] for d in data} == {"john@example.com", "mary@example.com"}
