SECRET_KEY:str = 'SOME_SECRET_KEY'
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./fastapi_listing.db"
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:password@db:5432/post_db"
ACCESS_TOKEN_EXPIRE_MINUTES:int = 30
ALGORITHM:str = "HS256"