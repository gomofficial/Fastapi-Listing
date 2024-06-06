from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    
    class Config:
        env_file = ".env"
        extra    = 'ignore'

    SECRET_KEY:str
    SQLALCHEMY_SQLITE_DATABASE_URL:str
    SQLALCHEMY_DATABASE_URL:str
    SQLALCHEMY_LOCAL_DATABASE_URL:str 
    ACCESS_TOKEN_EXPIRE_MINUTES:str
    ALGORITHM:str
    REDIS_URL:str
    WHEATHER_API_KEY:str

settings = Settings()


