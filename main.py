from fastapi import FastAPI, Request, Header
from routers import user_router, listing_router
from db import engine, Base
from utils import log
from utils.utils import increase_count_file
from contextlib import asynccontextmanager
import time

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    increase_count_file()
    yield

app = FastAPI(lifespan=lifespan)



app.include_router(user_router, prefix='/account', tags=['account'])
app.include_router(listing_router, prefix='/listing', tags=['listing'])


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    user_ip     = request.client.host
    path        = request.url.path
    requestType = request.method
    log("REQUEST TYPE: ",requestType," PATH: ",path," IP: ",user_ip)
    response = await call_next(request)
    
    return response