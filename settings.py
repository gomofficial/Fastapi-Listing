from os import environ as env


# RUNTIME_CONTEXT = env.get('RUNTIME_CONTEXT', 'uvicorn')


# if RUNTIME_CONTEXT == 'docker':
#     SECRET_KEY:str = env['Secret_Key']
#     SQLALCHEMY_DATABASE_URL:str = "postgresql+asyncpg://"+str(env['POSTGRES_USER'])+":"+env['POSTGRES_PASSWORD']+"@db:5432/"+env['POSTGRES_DB']
# else:
SECRET_KEY:str = 'SOME_SECRET_KEY'
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./todo.db"


ACCESS_TOKEN_EXPIRE_MINUTES:int = 30
ALGORITHM:str = "HS256"