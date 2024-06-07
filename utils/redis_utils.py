from redis.asyncio import Redis
from fastapi import Request
from datetime import datetime, timedelta
from exceptions import RateLimitException, DeviceLimitException, TokenWhiteListException, AllowedIPException
from fastapi import Depends
from settings import settings

redis = Redis(host=settings.REDIS_URL, port=6379, db=0)


async def rate_limit_user(request: Request):
    userIp = request.client.host

    now = datetime.now()
    current_minute = now.strftime("%Y-%m-%dT%H:%M")

    redis_key = f"rate_limit_{userIp}"
    current_count = await redis.incr(redis_key)


    if current_count == 1:
        await redis.expireat(name=redis_key, when=now + timedelta(minutes=1))
    
    if current_count > 5:
        raise RateLimitException
    
    return True


async def set_device_token(token, username):
    try:
        now = datetime.now()
        redis_key = f"{username}"
        await redis.set(redis_key, token)
        await redis.expireat(name=redis_key, when=now + timedelta(minutes=30))
    except Exception as e:
        print(e)


async def verify_device(token, username):
    redis_key = f"{username}"
    device_token =await redis.get(redis_key)
    if token != str(device_token.decode()):
        raise DeviceLimitException()
    return True


async def token_whitelist(username):
    redis_key = f"{username}"
    device_token =await redis.get(redis_key)
    if device_token is None:
        raise TokenWhiteListException()
    return True


async def set_device_ip(request:Request):
    await redis.sadd('ip_set', str(request.client.host))



async def verify_device_ip(request:Request):
    if await redis.sismember('ip_set', str(request.client.host)):
        return True
    raise TokenWhiteListException()


async def delete_key(key:str):
    redis_key = f"{key}"
    await redis.delete(key)


async def delete_ip(request:Request):
    await redis.srem('ip_set', str(request.client.host))