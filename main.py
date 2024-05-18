from fastapi import FastAPI
from routers import user_router
from db import engine, Base

app = FastAPI()


@app.on_event("startup")
async def init_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(user_router, prefix='/account', tags=['account'])
