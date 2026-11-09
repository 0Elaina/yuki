"""Alembic 仅读取数据库配置，不创建 Web 应用或连接 Redis。"""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import Connection, pool
from sqlalchemy.ext.asyncio import create_async_engine

from yuki.infrastructure.config import PostgresSettings
from yuki.infrastructure.database.base import Base
from yuki.modules.characters.models import Character  # noqa: F401
from yuki.modules.conversations.models import Conversation  # noqa: F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

# 业务模型在这里显式导入后，其表才会进入自动生成所用的 metadata。
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    settings = PostgresSettings.settings_cached()
    context.configure(
        url=settings.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    settings = PostgresSettings.settings_cached()
    engine = create_async_engine(
        settings.url,
        connect_args=settings.connect_args,
        poolclass=pool.NullPool,
        hide_parameters=True,
    )
    try:
        async with engine.connect() as connection:
            await connection.run_sync(do_run_migrations)
    finally:
        await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
