"""持有数据库引擎与会话工厂，事务由业务层开启。"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from yuki.infrastructure.config import PostgresSettings


class Database:
    def __init__(self, settings: PostgresSettings) -> None:
        self.engine = create_async_engine(
            settings.url,
            connect_args=settings.connect_args,
            pool_size=settings.pool_size,
            max_overflow=settings.max_overflow,
            pool_timeout=settings.pool_timeout_seconds,
            pool_pre_ping=True,
            hide_parameters=True,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autobegin=False,
            expire_on_commit=False,
            autoflush=True,
        )

    async def close(self) -> None:
        await self.engine.dispose()
