import asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from dataset.src.models import Model

DATABASE_URL = "sqlite+aiosqlite:///./dataset/clip.db"

engine = create_async_engine(DATABASE_URL, echo=False)
sqlite_client = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
