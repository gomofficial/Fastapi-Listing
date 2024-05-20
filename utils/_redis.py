from redis.asyncio import Redis
from fastapi import Request
from datetime import datetime, timedelta
from exceptions import RateLimitException


redis = Redis(host='redis', port=6379, db=0)


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


async def allowed_ip(request: Request):
    userIp = request.client.host

    redis_key = f"allowed_ip_list"

    return True

