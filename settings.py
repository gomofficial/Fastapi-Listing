from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    
    class Config:
        env_file = ".env"

    SECRET_KEY:str
    SQLALCHEMY_SQLITE_DATABASE_URL:str
    SQLALCHEMY_DATABASE_URL:str
    SQLALCHEMY_LOCAL_DATABASE_URL:str 
    ACCESS_TOKEN_EXPIRE_MINUTES:str
    ALGORITHM:str
    REDIS_URL:str
    WHEATHER_API_KEY:str
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    POSTGRES_DB:str
    DATABASE_URL:str
    PGDATA:str
    CELERY_BROKER_URL:str
    CELERY_RESULT_BACKEND:str
    PGADMIN_DEFAULT_EMAIL:str
    PGADMIN_DEFAULT_PASSWORD:str

settings = Settings()


