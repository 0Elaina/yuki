from collections.abc import AsyncIterator
from typing import cast

from fastapi import Request
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def create_db_engine(database_url: str) -> AsyncEngine:
    """创建数据库引擎"""

    engine = create_async_engine(database_url)
    return engine


def create_session_factory(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """创建会话工厂"""
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_db_session(request: Request) -> AsyncIterator[AsyncSession]:
    """获取数据库会话"""

    session_factory = cast(
        async_sessionmaker[AsyncSession], request.app.state.db_session_factory
    )
    async with session_factory() as session:
        yield session
