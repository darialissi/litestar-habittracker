from litestar.contrib.sqlalchemy.base import BigIntAuditBase
from litestar.contrib.sqlalchemy.plugins import (
    AsyncSessionConfig,
    EngineConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)

from config import settings

engine_config = EngineConfig(echo="debug")
session_config = AsyncSessionConfig(expire_on_commit=False)

sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=settings.DATABASE_URL_asyncpg,
    engine_config=engine_config,
    session_config=session_config,
    metadata=BigIntAuditBase.metadata,
)  # Create 'db_session' dependency.

sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)


async def create_tables() -> None:
    async with sqlalchemy_config.get_engine().begin() as conn:
        await conn.run_sync(sqlalchemy_config.metadata.create_all)


async def drop_tables() -> None:
    async with sqlalchemy_config.get_engine().begin() as conn:
        await conn.run_sync(sqlalchemy_config.metadata.drop_all)
