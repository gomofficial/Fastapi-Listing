from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from settings import settings

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = async_sessionmaker(
                            bind=engine,
                            autocommit=False,
                            autoflush=False,
                            expire_on_commit=False,
                            )

class Base(DeclarativeBase, MappedAsDataclass):
    pass

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
