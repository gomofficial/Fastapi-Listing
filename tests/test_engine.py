from db import Base, get_db
from main import app, lifespan

from fastapi.testclient import TestClient
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
    )

TestingSessionLocal = async_sessionmaker(
                            bind=engine,
                            autocommit=False,
                            autoflush=False,
                            expire_on_commit=False,
                            )

@asynccontextmanager
async def override_lifespan(app: FastAPI):
    async with engine.begin() as conn:
        print("arash ========================================")
        print("arash ========================================")
        print("arash ========================================")
        print("arash ========================================")

        print("arash ========================================")
        print("arash ========================================")

        print("arash ========================================")
        print("arash ========================================")

        print("arash ========================================")

        await conn.run_sync(Base.metadata.create_all)
    yield


async def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        await db.close()

app.dependency_overrides[lifespan] = override_lifespan
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
