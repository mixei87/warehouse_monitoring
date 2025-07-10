from logging import getLogger
from typing import AsyncGenerator

from sqlalchemy import text, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings
from app.models import Base, Movement  # noqa

# Синхронный движок
sync_engine = create_engine(settings.DATABASE_URL_SYNC)

# Асинхронный движок
engine = create_async_engine(
    settings.DATABASE_URL,
    future=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=20,
    max_overflow=20,
)
async_session = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
