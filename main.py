from fastapi import FastAPI, Request, Header
from routers import user_router, listing_router, bots_router
from db import engine, Base
from utils import (log, )
from utils.utils import increase_count_file
from contextlib import asynccontextmanager
from utils._redis import *
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from utils.celery_worker import weather_forcast


app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["localhost:3000"] 
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    increase_count_file()
    yield

app = FastAPI(lifespan=lifespan,
              title="Listing",
              description="Listing API for Dornica.",
              summary="Listing API for Dornica.",
              version="0.0.1",
              terms_of_service="http://github.com/gomofficial/",
              contact={
                    "name": "GOMOFFICIAL",
                    "url": "http://gomofficial.github.io/",
                    "email": "gomofficial@gmail.com",
                },
               license_info={
                    "name": "Apache 2.0",
                    "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
                },)


app.include_router(user_router, prefix='/account', tags=['account'])
app.include_router(listing_router, prefix='/listing', tags=['listing'])
app.include_router(bots_router, prefix='/bots', tags=['bots'])


@app.middleware("http")
async def request_logger(request: Request, call_next):
    user_ip     = request.client.host
    path        = request.url.path
    requestType = request.method
    log("REQUEST TYPE: ",requestType," PATH: ",path," IP: ",user_ip)
    response = await call_next(request)
    
    return response


@app.middleware('http')
async def validate_ip(request: Request, call_next):

    # Exclude the login view from IP validation
    if request.url.path not in ["/account/token", "/account/register", "/account/", "/listing/all"]:
        # Check if IP is allowed
        await verify_device_ip(request)

    # Proceed if IP is allowed
    return await call_next(request)
