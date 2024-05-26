from redis.asyncio import Redis
from fastapi import Request
from datetime import datetime, timedelta
from exceptions import RateLimitException, DeviceLimitException, AuthenticationException


redis = Redis(host='localhost', port=6379, db=0)


async def rate_limit_user(request: Request):
    userIp = request.client.host
    # Increment our most recent redis key
    now = datetime.now()
    current_minute = now.strftime("%Y-%m-%dT%H:%M")

    redis_key = f"rate_limit_{userIp}"
    current_count = await redis.incr(redis_key)


    # If we just created a new key (count is 1) set an expiration
    if current_count == 1:
        await redis.expireat(name=redis_key, when=now + timedelta(minutes=1))
    
    # Check rate limit
    if current_count > 5:
        raise RateLimitException
    
    print(request.client.host)
    return True

async def set_device_token(token, username):
    try:
        now = datetime.now()
        redis_key = f"{username}"
        # print(token)
        await redis.set(redis_key, token)
        await redis.expireat(name=redis_key, when=now + timedelta(minutes=30))
    except Exception as e:
        print(e)

async def verify_device(token, username):
    redis_key = f"{username}"
    device_token =await redis.get(redis_key)
    if device_token is None:
        raise AuthenticationException()
    elif token != str(device_token.decode()):
        raise DeviceLimitException()
    return True


async def delete_key(key):
    redis_key = f"{key}"
    await redis.delete(key)
