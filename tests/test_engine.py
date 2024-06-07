from fastapi.testclient import TestClient
from main import app
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from settings import settings
from db.engine import Base, get_db
from main import app
import asyncio

engine = create_async_engine(
    settings.SQLALCHEMY_SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


# asyncio(Base.metadata.create_all)


async def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        await db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(
    app,
    raise_server_exceptions=True,
    backend="asyncio",
    backend_options=None,
    follow_redirects=True,
)

