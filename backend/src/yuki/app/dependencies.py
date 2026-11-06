"""HTTP 依赖只提供资源，不替业务层管理事务。"""

from collections.abc import AsyncIterator
from typing import Annotated, cast

from fastapi import Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from yuki.infrastructure.database.session import Database


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    database = cast(Database, request.app.state.database)
    async with database.session_factory() as session:
        yield session


def get_redis(request: Request) -> Redis:
    return cast(Redis, request.app.state.redis)


# 函数结束即释放数据库会话，不让流式响应的播放或传输延长其生命周期。
SessionDep = Annotated[AsyncSession, Depends(get_session, scope="function")]
RedisDep = Annotated[Redis, Depends(get_redis)]
