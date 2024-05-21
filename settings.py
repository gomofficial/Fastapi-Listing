SECRET_KEY:str = 'SOME_SECRET_KEY'
# SQLALCHEMY_SQLITE_DATABASE_URL = "sqlite:///./fastapi_listing.db"
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:password@db:5432/post_db"
SQLALCHEMY_LOCAL_DATABASE_URL = "postgresql+psycopg2://postgres:password@db:5432/post_db"
ACCESS_TOKEN_EXPIRE_MINUTES:int = 30
ALGORITHM:str = "HS256"

WHEATHER_API_KEY  = "71c76fe9c1b84c2b86c180859242005"

