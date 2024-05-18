from os import environ as env


SECRET_KEY:str = 'SOME_SECRET_KEY'
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./todo.db"


ACCESS_TOKEN_EXPIRE_MINUTES:int = 30
ALGORITHM:str = "HS256"