from db import get_db
from main import app, lifespan
from db.models import *

from fastapi.testclient import TestClient
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

testingengine = create_async_engine(url="sqlite+aiosqlite:///./test.db", connect_args={"check_same_thread": False})

TestingSessionLocal = async_sessionmaker(
                            bind=testingengine,
                            autocommit=False,
                            autoflush=False,
                            expire_on_commit=False,
                            )


class Base(DeclarativeBase, MappedAsDataclass):
    pass

# Base = declarative_base()


@asynccontextmanager
async def override_lifespan(app: FastAPI):
    async with testingengine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


async def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        await db.close()


# app.dependency_overrides[lifespan] = override_lifespan
# app.dependency_overrides[get_db] = override_get_db

client = TestClient(app, )
