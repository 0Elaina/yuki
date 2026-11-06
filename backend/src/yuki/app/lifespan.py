"""创建数据库和 Redis 客户端，退出时释放资源。"""

from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager

from fastapi import FastAPI

from yuki.infrastructure.config import PostgresSettings, RedisSettings
from yuki.infrastructure.database.session import Database
from yuki.infrastructure.redis import create_redis


@asynccontextmanager
async def application_lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with AsyncExitStack() as resources:
        database = Database(PostgresSettings.settings_cached())
        resources.push_async_callback(database.close)

        redis = create_redis(RedisSettings.settings_cached())
        resources.push_async_callback(redis.aclose)

        app.state.database = database
        app.state.redis = redis
        yield
