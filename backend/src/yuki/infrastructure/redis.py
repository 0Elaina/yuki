"""Redis 原生异步客户端及项目键名。"""

from typing import Final

from redis.asyncio import Redis

from yuki.infrastructure.config import RedisSettings

KEY_PREFIX: Final = "yuki:"


def create_redis(settings: RedisSettings) -> Redis:
    return Redis(
        host=settings.host,
        port=settings.port,
        password=settings.password.get_secret_value(),
        db=settings.db,
        socket_connect_timeout=settings.connect_timeout_seconds,
        socket_timeout=settings.command_timeout_seconds,
        decode_responses=True,
    )


def redis_key(*parts: str | int) -> str:
    return KEY_PREFIX + ":".join(str(part) for part in parts)
