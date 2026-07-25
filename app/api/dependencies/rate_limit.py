from fastapi import Depends, HTTPException, Request, status
from redis.asyncio import Redis

from app.core.config import settings
from app.core.redis import get_redis


async def rate_limit_register(
    request: Request,
    redis: Redis = Depends(get_redis),
) -> None:
    """Ограничение регистрации по IP."""

    client_ip = request.client.host

    key = f"rate_limit:register:{client_ip}"

    requests_count = await redis.incr(key)

    if requests_count == 1:
        await redis.expire(
            key,
            settings.rate_limit_window_seconds,
        )

    if requests_count > settings.rate_limit_requests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Слишком много попыток регистрации.",
        )