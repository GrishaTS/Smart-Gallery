from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings
from app.models import Model


# Создание асинхронного движка PostgreSQL
engine = create_async_engine(settings.POSTGRES_URL)
postgres_client = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_postgres() -> None:
    """Создает таблицы в базе данных PostgreSQL."""
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_postgres() -> None:
    """Удаляет все таблицы из базы данных PostgreSQL."""
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
